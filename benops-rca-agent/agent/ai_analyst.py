"""3-phase AI Analyst using Claude API with Tool Use and Prompt Caching."""

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import anthropic
import requests

from agent.context_collector import JobContext
from config.settings import settings

MODEL = "claude-opus-4-8"
SKILLS_BASE = Path.home() / ".uipath" / ".skills" / "skills"

_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
_skill_knowledge: str | None = None


@dataclass
class RCAResult:
    failure_type: str
    root_cause: str
    affected_file: str
    line_number: int | None
    suggested_fix: str
    severity: str
    affected_transactions: list[str]
    confidence: str
    triage_domain: str


# ── Skill knowledge loader ────────────────────────────────────────────────────

def _load_skill_knowledge() -> str:
    global _skill_knowledge
    if _skill_knowledge is not None:
        return _skill_knowledge

    parts = []
    files_to_load = [
        SKILLS_BASE / "uipath-troubleshoot/references/products/orchestrator/overview.md",
        SKILLS_BASE / "uipath-troubleshoot/references/products/orchestrator/investigation_guide.md",
        SKILLS_BASE / "uipath-troubleshoot/references/products/orchestrator/playbooks/job-faulted-logon-failure.md",
        SKILLS_BASE / "uipath-troubleshoot/references/products/orchestrator/playbooks/queue-items-failing.md",
        SKILLS_BASE / "uipath-troubleshoot/references/products/orchestrator/playbooks/job-stuck.md",
        SKILLS_BASE / "uipath-troubleshoot/references/runtime-exceptions/playbooks/null-reference-exception.md",
        SKILLS_BASE / "uipath-troubleshoot/references/runtime-exceptions/playbooks/argument-null-exception.md",
        SKILLS_BASE / "uipath-rpa/references/xaml/common-pitfalls.md",
    ]
    for path in files_to_load:
        if path.exists():
            parts.append(f"### {path.name}\n{path.read_text()}")

    _skill_knowledge = "\n\n---\n\n".join(parts)
    return _skill_knowledge


def _system_prompt() -> list[dict]:
    knowledge = _load_skill_knowledge()
    taxonomy = """
## BenOps Failure Taxonomy

| failure_type | Description |
|---|---|
| portal_change | Carrier updated web portal; selector broke |
| data_quality | Input data invalid or wrong format |
| business_rule | Carrier rejected submission based on eligibility |
| network_timeout | Page load or API response timed out |
| library_incompatibility | Process uses outdated Gusto_Benefits library version |
| credential_error | Robot credentials expired or locked |
| unknown | Could not classify with confidence |

## Severity levels: critical, high, medium
## Confidence levels: high, medium, low
## Domains: ui_automation, system_activities, runtime_exception, orchestrator, unknown
"""
    return [
        {
            "type": "text",
            "text": f"# UiPath Knowledge Base\n\n{knowledge}\n\n{taxonomy}",
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        },
        {
            "type": "text",
            "text": (
                "You are an expert BenOps RPA analyst. Your job is to perform root cause analysis "
                "on UiPath bot failures in benefits enrollment processes. "
                "Use the UiPath knowledge base above to guide your investigation. "
                "Be precise, evidence-based, and actionable."
            ),
        },
    ]


# ── Phase 1: Triage ───────────────────────────────────────────────────────────

def _phase1_triage(ctx: JobContext) -> dict:
    """Classify the failure domain and generate ranked hypotheses."""
    job = ctx.job
    logs_summary = "\n".join(
        f"[{e.get('Level','?')}] {e.get('Message','')}"
        for e in ctx.execution_logs[:30]
    )
    triage_prompt = f"""Analyze this UiPath bot failure and return a JSON triage result.

## Job Information
- Process: {job.process_name}
- Error: {job.error_message}
- Machine: {job.machine_name}
- Start: {job.start_time} | End: {job.end_time}

## Execution Logs (last 30 entries)
{logs_summary or '(no logs available)'}

## Job History
{json.dumps(ctx.job_history[:5], indent=2)[:500]}

Return ONLY valid JSON in this exact format:
{{
  "domain": "<ui_automation|system_activities|runtime_exception|orchestrator|unknown>",
  "initial_assessment": "<2-3 sentence summary of what happened>",
  "hypotheses": [
    {{
      "type": "<failure_type from taxonomy>",
      "confidence": "<high|medium|low>",
      "rationale": "<why this hypothesis>",
      "evidence_needed": ["<xaml_file|pr_history|job_traces|queue_items|similar_tickets>"]
    }}
  ]
}}

Rank hypotheses by confidence descending. Include 1-3 hypotheses max."""

    response = _client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=_system_prompt(),
        messages=[{"role": "user", "content": triage_prompt}],
    )
    text = next((b.text for b in response.content if b.type == "text"), "{}")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Extract JSON from text if wrapped in prose
        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        return json.loads(match.group()) if match else {"domain": "unknown", "hypotheses": []}


# ── Phase 2+3: Investigation + RCA ───────────────────────────────────────────

def _uip(*args: str) -> str:
    uip_bin = shutil.which("uip")
    result = subprocess.run(
        [uip_bin, *args, "--output", "json"],
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout if result.returncode == 0 else f"Error: {result.stderr.strip()}"


INVESTIGATION_TOOLS = [
    {
        "name": "get_job_traces",
        "description": "Fetch execution traces for the faulted job showing the exact activity execution path, variable values, and where execution stopped. Call this when the error points to a specific activity failure or unexpected workflow path.",
        "input_schema": {
            "type": "object",
            "properties": {"job_key": {"type": "string", "description": "The Orchestrator job key"}},
            "required": ["job_key"],
        },
    },
    {
        "name": "get_xaml_file",
        "description": "Fetch the XAML source code of a workflow file from GitHub. Call this to inspect selectors, activity properties, and workflow logic when you suspect a portal_change, library_incompatibility, or business_rule failure.",
        "input_schema": {
            "type": "object",
            "properties": {
                "process_name": {"type": "string", "description": "The UiPath process folder name"},
                "filename": {"type": "string", "description": "XAML file name, e.g. EnterMemberInformation.xaml"},
            },
            "required": ["process_name", "filename"],
        },
    },
    {
        "name": "get_pr_history",
        "description": "Fetch the last N merged pull requests for this process from GitHub. Call this to check if a recent code change introduced the failure.",
        "input_schema": {
            "type": "object",
            "properties": {
                "process_name": {"type": "string"},
                "count": {"type": "integer", "default": 3},
            },
            "required": ["process_name"],
        },
    },
    {
        "name": "get_queue_items",
        "description": "Fetch failed and successful queue items for comparison. Call this when the failure is data_quality or business_rule related to understand what input data caused the failure.",
        "input_schema": {
            "type": "object",
            "properties": {
                "queue_key": {"type": "string", "description": "Orchestrator queue definition key"},
                "folder_key": {"type": "string"},
            },
            "required": ["queue_key", "folder_key"],
        },
    },
    {
        "name": "get_similar_tickets",
        "description": "Search Jira for past tickets with similar failures in this process. Call this to find known resolutions and check if this is a recurring issue.",
        "input_schema": {
            "type": "object",
            "properties": {
                "process_name": {"type": "string"},
                "error_keywords": {"type": "string", "description": "Key error terms to search"},
            },
            "required": ["process_name"],
        },
    },
    {
        "name": "submit_rca",
        "description": "Submit the final root cause analysis. Call this ONLY when you have gathered enough evidence to confidently identify the root cause. This terminates the investigation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "failure_type": {"type": "string", "enum": ["portal_change", "data_quality", "business_rule", "network_timeout", "library_incompatibility", "credential_error", "unknown"]},
                "root_cause": {"type": "string", "description": "Detailed explanation of what broke and why"},
                "affected_file": {"type": "string", "description": "XAML filename where the failure occurred"},
                "line_number": {"type": "integer", "description": "Approximate line number in the XAML file"},
                "suggested_fix": {"type": "string", "description": "Specific actionable fix recommendation"},
                "severity": {"type": "string", "enum": ["critical", "high", "medium"]},
                "affected_transactions": {"type": "array", "items": {"type": "string"}, "description": "Transaction IDs affected"},
                "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            },
            "required": ["failure_type", "root_cause", "suggested_fix", "severity", "confidence"],
        },
    },
]


def _execute_tool(name: str, tool_input: dict, ctx: JobContext) -> str:
    if name == "get_job_traces":
        return _uip("traces", "spans", "get", "--job-key", tool_input["job_key"])

    if name == "get_xaml_file":
        from agent.context_collector import _fetch_xaml_file
        content = _fetch_xaml_file(tool_input["process_name"], tool_input["filename"])
        return content[:4000]  # limit to 4K chars

    if name == "get_pr_history":
        from agent.context_collector import _fetch_pr_history
        prs = _fetch_pr_history(tool_input["process_name"], tool_input.get("count", 3))
        return json.dumps(prs, indent=2)

    if name == "get_queue_items":
        failed = _uip(
            "resource", "queue-items", "list",
            "--queue-definition-key", tool_input["queue_key"],
            "--folder-key", tool_input["folder_key"],
            "--status", "Failed",
        )
        return failed[:3000]

    if name == "get_similar_tickets":
        headers = {
            "Authorization": f"Bearer {settings.jira_token}",
            "Content-Type": "application/json",
        }
        jql = f'project = {settings.jira_project_key} AND summary ~ "{tool_input["process_name"]}" ORDER BY created DESC'
        try:
            resp = requests.get(
                f"{settings.jira_base_url}/rest/api/3/search",
                headers=headers,
                params={"jql": jql, "maxResults": 5, "fields": "summary,status,created,description"},
                timeout=15,
            )
            resp.raise_for_status()
            issues = resp.json().get("issues", [])
            summary = [
                {"key": i["key"], "summary": i["fields"]["summary"], "status": i["fields"]["status"]["name"]}
                for i in issues
            ]
            return json.dumps(summary, indent=2)
        except Exception as exc:
            return f"Jira search error: {exc}"

    return f"Unknown tool: {name}"


def _phase2_investigate(ctx: JobContext, triage: dict) -> RCAResult:
    """Run tool use loop to investigate hypotheses and produce RCA."""
    job = ctx.job
    hypotheses_text = json.dumps(triage.get("hypotheses", []), indent=2)
    logs_sample = "\n".join(
        f"[{e.get('Level','?')}] {e.get('Message','')}"
        for e in ctx.execution_logs[:20]
    )
    xaml_summary = {
        fname: content[:1500]
        for fname, content in ctx.xaml_source.items()
        if content and not content.startswith("[Could not")
    }

    investigation_prompt = f"""Investigate this UiPath bot failure and determine the root cause.

## Triage Result
Domain: {triage.get('domain', 'unknown')}
Initial Assessment: {triage.get('initial_assessment', '')}

Hypotheses to test (ranked by confidence):
{hypotheses_text}

## Job: {job.process_name} | Key: {job.key}
Error: {job.error_message}

## Execution Logs
{logs_sample or '(none)'}

## XAML Source (pre-loaded)
{json.dumps(xaml_summary, indent=2)[:2000] if xaml_summary else '(not available)'}

## PR History (pre-loaded)
{json.dumps(ctx.pr_history, indent=2)[:1000] if ctx.pr_history else '(none)'}

Use tools to gather additional evidence for the top hypotheses.
When you have enough evidence, call submit_rca with your findings.
Focus on the most likely hypothesis first based on the error message and logs."""

    messages = [{"role": "user", "content": investigation_prompt}]

    # Tool use loop — max 8 iterations to prevent infinite loops
    for _ in range(8):
        response = _client.messages.create(
            model=MODEL,
            max_tokens=4096,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            system=_system_prompt(),
            tools=INVESTIGATION_TOOLS,
            messages=messages,
        )

        # Check for submit_rca call
        rca_call = next(
            (b for b in response.content if b.type == "tool_use" and b.name == "submit_rca"),
            None,
        )
        if rca_call:
            inp = rca_call.input
            return RCAResult(
                failure_type=inp.get("failure_type", "unknown"),
                root_cause=inp.get("root_cause", ""),
                affected_file=inp.get("affected_file", ""),
                line_number=inp.get("line_number"),
                suggested_fix=inp.get("suggested_fix", ""),
                severity=inp.get("severity", "medium"),
                affected_transactions=inp.get("affected_transactions", []),
                confidence=inp.get("confidence", "low"),
                triage_domain=triage.get("domain", "unknown"),
            )

        if response.stop_reason == "end_turn":
            break

        # Append assistant response and execute tools
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use" and block.name != "submit_rca":
                result = _execute_tool(block.name, block.input, ctx)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result[:3000],
                })
        if tool_results:
            messages.append({"role": "user", "content": tool_results})

    # Fallback if Claude didn't call submit_rca
    return RCAResult(
        failure_type=triage.get("hypotheses", [{}])[0].get("type", "unknown") if triage.get("hypotheses") else "unknown",
        root_cause=f"Investigation incomplete. Initial error: {job.error_message}",
        affected_file="",
        line_number=None,
        suggested_fix="Manual investigation required.",
        severity="medium",
        affected_transactions=[],
        confidence="low",
        triage_domain=triage.get("domain", "unknown"),
    )


# ── Public entrypoint ─────────────────────────────────────────────────────────

def analyze(ctx: JobContext) -> RCAResult:
    print(f"[AIAnalyst] Phase 1 — Triage: {ctx.job.process_name}")
    triage = _phase1_triage(ctx)
    print(f"[AIAnalyst] Domain: {triage.get('domain')} | Hypotheses: {len(triage.get('hypotheses', []))}")

    print(f"[AIAnalyst] Phase 2+3 — Investigation + RCA")
    result = _phase2_investigate(ctx, triage)
    print(f"[AIAnalyst] RCA complete: {result.failure_type} ({result.severity}) — confidence: {result.confidence}")
    return result
