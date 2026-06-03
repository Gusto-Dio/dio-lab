# Workspace — IDs, Databases e Campos

> **Language policy:** All Notion content must be in English. No Portuguese in any field, page, or property.

## IDs fixos

| Recurso | ID |
|---|---|
| Hub page | `35dad673c6c281ca9beed83cf58fdb22` |
| Processes DB | `ba7266d884b6425c9fc0036b483bd8d0` |
| Standup Topics DB | `7a77a12fba92465f9226e372383a1299` |
| Library DB | `de5770484c4949e9844cee53b7b35527` |
| Runbooks DB | `7d5fe4fbbe2d485686f44c86ef147c4a` |

URL da página de setup do Claude Code (publicada no Notion para o time):
`https://www.notion.so/35dad673c6c281d09313e23bf1a2652d`

---

## Localização no Notion

```
BizTech RPA Docs
  └── 🤖 BenOps RPA Hub          ← Hub page (35dad673...)
        ├── 📋 Standup Topics DB  ← 7a77a12f... (data source: 4ca84260...)
        ├── 🤖 Processes DB       ← ba7266d8... (data source: fa093b20...)
        ├── 🔧 Runbooks DB        ← 7d5fe4fb... (data source: 4b0bf63d...)
        ├── 📦 Library DB         ← de5770484... (data source: 27a0a131...)
```

**Databases removidas:**
- 🏥 Carriers DB — merged into Processes DB (2026-06-02)
- 👥 Team DB — replaced by callout in Hub page (2026-06-02)
- ⚠️ Alerts DB — not in use (2026-06-02)
- 🚨 Incidents DB — not in use (2026-06-02)

---

## Hub page — layout

Redesigned 2026-06-02, inspired by Revenue Notion page:

**Left column:** Welcome callout + Team callout (alphabetical, with local + PDT hours)
**Right column:** Navigate callout (→ links to databases) + Quick Links callout (Operations / Developer / Reference)

Sync timestamp on first line:
```
Synced daily via /benops-sync (GitHub PRs + Jira tickets) · Last synced: YYYY-MM-DD HH:MM
```

---

## Processes DB — fields

| Field | Notion Type | Notes |
|---|---|---|
| Process | title | Process name (e.g. "UHC_SamX_Renewal_Modern") |
| Carrier | select | Anthem / BCBS MA / BCBS TX / BCBS IL / BCBS OK / BSCA / Kaiser / UHC / Beam / Principal / CoveredCal |
| Carrier Status | select | Active / On Hold / Deprecated — filled manually |
| Portal URL | url | Carrier portal URL — filled manually |
| Carrier Notes | rich_text | Carrier quirks and notes — filled manually |
| Type | select | NHE / Term / MemberUpdate / GroupSub / Recon / PacketCollection |
| Assignee | select | Diogenes / Ahsen / Hari / Oscar |
| Status | select | Not Started / In Progress / Pending Review / Ready for Deployment / Deployed to Prod / On Hold |
| Version | text | Gusto_Benefits library version |
| PR Number | rich_text | e.g. "#2733 Open — Awaiting Review" or "#2699 Merged" |
| Jira Ticket | rich_text | e.g. "BT-73075" — cross-reference key |
| Last Synced | date | ISO 8601 (YYYY-MM-DD) — updated by `/benops-sync` |

### Status derivation rules (used by `/benops-sync`)

| Condition | Derived Status |
|---|---|
| Jira = Done AND PR merged | "Deployed to Prod" |
| Jira = Done AND PR open | "Ready for Deployment" |
| PR with CHANGES_REQUESTED | "Pending Review" |
| PR open AND pending reviewers | "Pending Review" |
| Jira = In Progress AND PR open | "In Progress" |
| Jira = In Progress AND no PR | "In Progress" |
| No match | skip (do not update) |

---

## Standup Topics DB — fields

| Field | Notion Type | Notes |
|---|---|---|
| Topic | title | Standup item description |
| Category | select | Blocker / Action Item / Documentation / Hackathon / Process / FYI |
| Priority | select | High / Medium / Low |
| Status | select | Open / In Progress / Done / Parked |
| Resource | select | Diogenes / Oscar / Hari / Ahsen / Sri / Team |
| Target Date | date | Target completion date |
| Last Discussed | date | Last daily where the item was discussed |
| Notes | rich_text | Accumulated comments — updated each standup. **Must be in English.** |
| Jira Ticket | rich_text | Filled when topic becomes a Jira ticket (e.g. "BT-73075") |

**Origin:** migrated from [BenOps RPA Daily Stand up Notes](https://docs.google.com/document/d/1CXncG2oonWdKgIwi7dgw8_3bxPK3kEdqSk4x42rpG3Y) on 2026-06-02.

---

## Library DB — fields

| Field | Notion Type | Notes |
|---|---|---|
| Library | title | Library package name |
| GitHub Version | text | Latest version in GitHub repo |
| Orchestrator Version | text | Latest version deployed in Production Orchestrator |
| Framework | select | Windows / Legacy |
| Status | select | Up to Date / Behind / Not Deployed / Orch Ahead / Orchestrator Only |
| Type | select | Core / Carrier-Specific / Modern / IDP / Payroll |
| BenOps | checkbox | Whether BenOps team uses this library |
| Depends On | rich_text | Gusto_ libraries this lib depends on |
| Notes | rich_text | Observations |

**Data source:** Orchestrator Production Libraries feed — `odata/Libraries` (tid=11015, fid=46023).
**Important:** Do NOT use `uip package list` — it reads from the Processes feed and returns stale versions. Always validate via the Libraries feed or Orchestrator UI.

**Status meanings:**
- `Up to Date` — GitHub version = Orchestrator version
- `Behind` — GitHub has newer version not yet published to Orchestrator
- `Orch Ahead` — Orchestrator has newer version not yet committed to GitHub
- `Not Deployed` — Only in GitHub, not in Orchestrator
- `Orchestrator Only` — Only in Orchestrator, not found in GitHub repo

---

## Runbooks DB — fields

| Field | Notion Type | Notes |
|---|---|---|
| Title | title | Runbook name (numbered: "1. Title") |
| Carrier | text | Affected carrier or "All" |
| Process | text | Affected process or "All processes" |
| Symptoms | text | When to use this runbook |
| Last Updated | date | Last update date |

**Views:**
- `Default view` — all rows (may include legacy entries)
- `All Runbooks` — filtered to show only numbered runbooks 1–8, sorted by Title ASC

**Content:** Full step-by-step content lives inside each runbook page body (not in the fields). All content must be in English.

**Current runbooks (2026-06-03):**
1. Buildkite failed on PR
2. Bot failing in production — initial triage
3. DebuggerApi in migrated process
4. Navigation flapping — RetryScope + NCheckState
5. Legacy → Windows migration
6. Library version bump
7. Full PR flow — from commit to merge
8. Publish library to Orchestrator

---

## MCP tools usados

| Operação | Tool |
|---|---|
| Ler databases | `mcp__claude_ai_Notion_Gusto__notion-query-data-sources` |
| Atualizar página/linha | `mcp__claude_ai_Notion_Gusto__notion-update-page` |
| Criar linha nova | `mcp__claude_ai_Notion_Gusto__notion-create-pages` |
| Criar database nova | `mcp__claude_ai_Notion_Gusto__notion-create-database` |
| Alterar schema de database | `mcp__claude_ai_Notion_Gusto__notion-update-data-source` |
| Criar view | `mcp__claude_ai_Notion_Gusto__notion-create-view` |
| Atualizar view | `mcp__claude_ai_Notion_Gusto__notion-update-view` |
| Busca geral | `mcp__claude_ai_Notion_Gusto__notion-search` |
| Fetch de página | `mcp__claude_ai_Notion_Gusto__notion-fetch` |
