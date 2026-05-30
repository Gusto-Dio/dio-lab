"""Creates pre-diagnosed Jira tickets via Jira REST API."""

from datetime import date

import requests

from agent.ai_analyst import RCAResult
from agent.failure_listener import FaultedJob
from config.settings import settings


def create_ticket(job: FaultedJob, rca: RCAResult) -> str | None:
    """Creates a Jira ticket and returns the ticket key (e.g. BT-73001)."""
    today = date.today().isoformat()
    title = f"[RCA-AUTO] {job.process_name} — {rca.failure_type} — {today}"

    transactions_text = "\n".join(f"* {tid}" for tid in rca.affected_transactions) or "* (none identified)"
    file_ref = f"`{rca.affected_file}`" + (f" line ~{rca.line_number}" if rca.line_number else "") if rca.affected_file else "(see logs)"

    description = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "Summary"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": rca.root_cause}]},
            {"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "Root Cause"}]},
            {"type": "paragraph", "content": [
                {"type": "text", "text": f"Failure type: {rca.failure_type} | Confidence: {rca.confidence} | Domain: {rca.triage_domain}"}
            ]},
            {"type": "paragraph", "content": [{"type": "text", "text": f"Affected file: {file_ref}"}]},
            {"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "Affected Transactions"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": transactions_text}]},
            {"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "Suggested Fix"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": rca.suggested_fix}]},
            {"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": "Metadata"}]},
            {"type": "paragraph", "content": [
                {"type": "text", "text": f"Severity: {rca.severity.upper()} | Process: {job.process_name} | Job key: {job.key}"}
            ]},
        ],
    }

    payload = {
        "fields": {
            "project": {"key": settings.jira_project_key},
            "summary": title,
            "description": description,
            "issuetype": {"name": "Bug"},
            "labels": ["rca-auto", rca.failure_type, f"severity-{rca.severity}"],
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.jira_token}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(
            f"{settings.jira_base_url}/rest/api/3/issue",
            json=payload,
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        key = resp.json().get("key", "")
        print(f"[JiraCreator] Created ticket: {key}")
        return key
    except Exception as exc:
        print(f"[JiraCreator] Failed to create ticket: {exc}")
        return None
