# BenOps RCA Agent — Design Spec

**Date:** 2026-05-26  
**Author:** Diogenes Ribeiro (BizTech RPA)  
**Context:** Benefits Hackathon — June 2026  
**Status:** Approved for hackathon implementation

---

## Problem

When a benefits enrollment bot fails in UiPath Orchestrator, an engineer must manually investigate the failure — reading execution logs, reviewing XAML workflow code, and checking PR history to identify the root cause. This process takes 2+ hours per incident. Depending on the ticket queue, the underlying enrollment can remain broken for days or weeks, directly impacting employee benefits coverage.

There is no automated triage. Tickets arrive with no diagnostic context. Engineers with no prior exposure to a process have no documentation to reference.

---

## Solution

An autonomous Python agent running on the BizTech RPA VM (GSTO-FR5-APP002) that:

1. Detects Faulted jobs in Orchestrator via polling
2. Collects all relevant context: execution logs, XAML source, recent PR history
3. Sends that context to the Claude API for root cause analysis and failure classification
4. Creates a pre-diagnosed Jira ticket with structured RCA
5. Posts a summary alert to the team Slack channel

From failure to diagnosed ticket: under 60 seconds.

---

## Architecture

### Components

**1. Failure Listener**  
Polls the Orchestrator API every 60 seconds for jobs with status `Faulted`. Tracks the last-checked timestamp to avoid duplicate processing. On match, hands the job metadata to the Context Collector.

**2. Context Collector**  
Given a faulted job, fetches in parallel:
- Execution logs from Orchestrator API (last 500 lines of the faulted job)
- Main XAML files for the process from GitHub API (`Process.xaml`, `Main.xaml`)
- Last 3 merged PRs for that process path (titles + summary)
- Transaction ID and queue item data (if applicable)

**3. AI Analyst (Claude API)**  
Receives the collected context as a structured prompt. Returns:
- **Failure classification:** `portal_change` | `data_quality` | `business_rule` | `network_timeout` | `library_incompatibility` | `unknown`
- **Root cause:** what broke, which file, estimated line
- **Impact:** affected transaction IDs, duration of failure
- **Suggested fix:** specific recommendation
- **Severity:** `critical` | `high` | `medium`

**4. Jira Ticket Creator**  
Creates a ticket using the Jira REST API with the structured RCA as the description. Links to the Orchestrator job and the relevant GitHub file. Title format: `[RCA-AUTO] {ProcessName} — {failure_type} — {date}`.

**5. Slack Notifier**  
Posts a condensed summary to `#benops-rpa-alerts` (or equivalent channel) with failure type, severity, affected transactions, and a link to the created Jira ticket.

---

## Data Flow

```
Orchestrator (Faulted job)
        │
        ▼
Failure Listener (polling, 60s interval)
        │
        ▼
Context Collector
    ├── Orchestrator API  →  execution logs + transaction data
    ├── GitHub API        →  XAML source + PR history
        │
        ▼
AI Analyst — Claude API
    └── root cause + classification + fix suggestion
        │
        ├── Jira REST API  →  pre-diagnosed ticket created
        └── Slack API      →  alert posted to team channel
```

---

## Dependencies

| Dependency | Status | Purpose |
|---|---|---|
| UiPath Orchestrator API | Already in use | Fetch faulted jobs + logs |
| GitHub API | Already in use | Read XAML + PR history |
| Jira REST API | Already in use | Create RCA tickets |
| Slack API | Already in use | Post team alerts |
| Anthropic Claude API | **New** | Root cause analysis |
| Python 3.11 (VM) | Already installed | Runtime |

All dependencies except the Claude API are already integrated and have tokens available on the VM.

---

## Failure Classification

| Class | Description | Example |
|---|---|---|
| `portal_change` | Carrier updated their web portal; selector broke | Button label changed, new modal appeared |
| `data_quality` | Input data is invalid or in wrong format | Wrong effective date, missing SSN |
| `business_rule` | Carrier rejected submission based on eligibility rules | Coverage not available for member type |
| `network_timeout` | Page load or API response timed out | Orchestrator log shows timeout exception |
| `library_incompatibility` | Process uses outdated Gusto_Benefits library version | Activity signature changed in newer lib |
| `unknown` | Claude could not classify with confidence | Escalate for manual review |

---

## Jira Ticket Structure

```
Title:   [RCA-AUTO] {ProcessName} — {failure_type} — {YYYY-MM-DD}

Summary
  2–3 sentence executive summary of what happened.

Root Cause
  Detailed analysis: what broke, where in the code, why.

Affected Transactions
  - {TransactionID_1}
  - {TransactionID_2}

Suggested Fix
  Specific action: file path, line number if available, what to change.

Severity: HIGH
Links: [Orchestrator Job] [GitHub XAML file]
```

---

## Demo Plan (Hackathon)

**Runtime:** ~3 minutes live on GSTO-FR5-APP002

1. **0:00 – 0:30** — Set the stage: explain the current manual process and the business impact
2. **0:30 – 0:50** — Trigger a test job configured to fail in Orchestrator
3. **0:50 – 1:50** — Show the agent running in the VM terminal: detection → collection → Claude analysis → ticket creation → Slack
4. **1:50 – 2:20** — Open Jira live: show the pre-diagnosed ticket. Open Slack: show the alert
5. **2:20 – 2:50** — Land the impact: 47 seconds vs 2+ hours. Same-day resolution vs days in queue

**Pre-demo setup:**
- `pip install anthropic requests` on VM
- Environment variables set: `ANTHROPIC_API_KEY`, `ORCHESTRATOR_TOKEN`, `JIRA_TOKEN`, `SLACK_TOKEN`
- Test process in Orchestrator configured to produce a known failure
- Jira, Slack, and Orchestrator tabs open in browser

---

## Submission Info

| Field | Value |
|---|---|
| Submitter's Team | BizTech RPA |
| Teams / Areas Impacted | BenOps, CX, Benefits Engineering |
| Roles Needed | Engineering (primary), PM (optional) |
| Teammates Needed | 2 – 4 |

---

## Award Categories

- **Best Use of AI** — Claude API is the core intelligence layer; the agent produces zero-touch root cause analysis
- **Best Impact for CX** — enrollment failures resolved same day instead of sitting in queue for days/weeks

---

## Out of Scope (for hackathon)

- Auto-applying the fix (agent diagnoses, human fixes)
- Auto-documentation generation (separate initiative)
- Webhook-based trigger (polling is sufficient for demo; webhook is a post-hackathon improvement)
- UI dashboard (terminal output + Jira + Slack is sufficient for v1)
