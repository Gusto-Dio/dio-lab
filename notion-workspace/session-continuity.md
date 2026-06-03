# Session Continuity — Notion

> Read this file first before any Notion work.
> Last updated: 2026-06-03
>
> **Language rule: ALL Notion content must be in English. Never Portuguese.**

---

## Current state (2026-06-03)

### What is working

- Hub page redesigned (2-column layout, all in English) ✅
- Processes DB — 17 processes + carrier fields unified ✅
- Standup Topics DB — 11 items + Jira Ticket field, all in English ✅
- Library DB — 22 libraries mapped (GitHub + Orchestrator Production validated) ✅
- Runbooks DB — 8 runbooks in English, ordered view created ✅
- Team callout with local + PDT hours ✅
- `/benops-sync` operational — runs in `/morning` automatically ✅
- Claude Code Setup page published for team onboarding ✅
- Slack message sent to dev channel for Hub validation ✅

### What was done on 2026-06-02

| What | Detail |
|---|---|
| Carriers DB + Processes DB unified | 3 new fields in Processes DB: `Carrier Status`, `Portal URL`, `Carrier Notes`. Carriers DB trashed. |
| Hub page redesigned | 2-column layout (Welcome + Team / Navigate + Quick Links). Verbose "How to use" removed. |
| Team DB → callout | Team DB trashed; alphabetical member list in Hub callout. |
| Alerts DB and Incidents DB removed | Not in use. Trashed. |
| Standup Topics DB created | 11 items migrated from Sri's Google Doc. Jira Ticket field added. |

### What was done on 2026-06-03

| What | Detail |
|---|---|
| Quick Links reorganized | Sections: Operations / Developer / Reference. `→` per item. Sheets Queue removed. Jira Board link corrected. |
| Team callout with hours | Format: local (country + time) · PDT. Sub-bullet per member. |
| Library DB redesigned | Schema: Library / GitHub Version / Orchestrator Version / Framework / Status / Type / BenOps / Depends On / Notes. 22 libraries populated. |
| Orchestrator validation | Corrected source — must use `odata/Libraries` feed, NOT `uip package list` (returns stale versions). |
| 8 runbooks created | From `notion/runbooks.md` in Gusto-Dio/dio-lab. All in English. Steps column removed. "All Runbooks" view created (sorted, filtered). |
| English-only enforcement | All Notion content translated: runbook pages, Standup Topics notes, Hub page. |
| Slack message sent | Channel `C0ANAPHL1NE` — Sri, Ahsen, Oscar, Hari invited to validate Hub and confirm hours. |

### What is still pending

| Item | Description | Priority |
|---|---|---|
| Broken Bots → Notion | Sri shared spreadsheet with 20 broken processes (8 months). Asked if she wants to bring to Notion. Awaiting response. | Medium |
| Hours validation | Ahsen, Oscar, Hari need to confirm their hours in the Team callout. | Medium |
| Processes DB — missing processes | Verify if UHC_SamX and CoveredCal have rows in the DB | Medium |
| Standup Topics — Jira Tickets | Fill Jira Ticket field on items that already have a ticket | Low |
| Portal URL and Carrier Notes | Fill manually in Processes DB per carrier | Low |
| Library DB — GitHub versions for new libs | 11 libraries added with Orchestrator version only; GitHub versions to be verified | Low |

---

## Team hours (PDT)

| Member | Local | PDT |
|---|---|---|
| Ahsen | Türkiye 8:30am–5:30pm | 10:30pm–7:30am |
| Diogenes | Brazil 1:00pm–9:00pm | 9:00am–6:00pm |
| Hari | EST 9:00am–6:00pm | 7:00am–4:00pm |
| Oscar | Mexico 9:00am–6:00pm | 8:00am–5:00pm |
| Sri | 8:30am–5:30pm | 7:00am–4:30pm |

---

## How to add a new process to Processes DB

1. Identify the process name (`UHC_SamX_Renewal_Modern`, etc.)
2. Use `mcp__claude_ai_Notion_Gusto__notion-create-pages` with parent = Processes DB ID (`ba7266d884b6425c9fc0036b483bd8d0`)
3. Required fields: `Process`, `Carrier`, `Jira Ticket` (for sync to work)
4. `/benops-sync` will fill Status, PR Number, and Last Synced automatically

---

## How to add an item to Standup Topics DB

1. Use `mcp__claude_ai_Notion_Gusto__notion-create-pages` with parent = Standup Topics DB data source (`4ca84260-cb84-4c31-b14c-07edcea4e1e6`)
2. Required fields: `Topic`, `Category`, `Status`
3. Fill `Jira Ticket` when topic becomes a Jira ticket
4. Update `Last Discussed` and `Notes` each standup — **Notes must be in English**

---

## Key people

| Name | Slack ID | Role |
|---|---|---|
| Sri Perinkolam | `U07KMNHHFB6` | PM — tracks bot status, uses Standup Topics DB in dailys |
| Oscar Nuñez | `U05UYA9S4G7` | Engineer — updates Processes DB when closing tickets |
| Hari (Harinath Reddy Mora) | `U0B313V9XBJ` | Engineer — Kaiser CA MLE and other processes |
| Ahsen Turksoy | `U03E8KNP1JB` | Engineer — BCBS/Anthem processes |
| Diogenes Ribeiro | — | Hub maintainer and skill author |

---

## Useful commands

```
# View Hub current state
/benops-sync

# Daily briefing (includes sync at the end)
/morning

# Read Hub content
mcp__claude_ai_Notion_Gusto__notion-fetch pageId="35dad673c6c281ca9beed83cf58fdb22"

# List Processes DB rows
mcp__claude_ai_Notion_Gusto__notion-query-data-sources databaseId="ba7266d884b6425c9fc0036b483bd8d0"

# List Standup Topics DB rows
mcp__claude_ai_Notion_Gusto__notion-query-data-sources databaseId="7a77a12fba92465f9226e372383a1299"

# List Library DB rows
mcp__claude_ai_Notion_Gusto__notion-query-data-sources databaseId="de5770484c4949e9844cee53b7b35527"

# List Runbooks DB rows
mcp__claude_ai_Notion_Gusto__notion-query-data-sources databaseId="7d5fe4fbbe2d485686f44c86ef147c4a"
```

---

## FAQ for new sessions

**"Does the Hub already exist?"**
Yes. URL: https://www.notion.so/35dad673c6c281ca9beed83cf58fdb22

**"Which IDs to use?"**
See `workspace.md` — all mapped with type and purpose.

**"How to add a new field to a database?"**
Use `mcp__claude_ai_Notion_Gusto__notion-update-data-source` with DDL:
`ADD COLUMN "Name" TYPE` — supports SELECT, RICH_TEXT, DATE, URL, CHECKBOX, etc.
Then update `workspace.md` with the new field.

**"How to validate Library versions in Orchestrator?"**
Use the `odata/Libraries` feed directly. Do NOT use `uip package list` — it reads from the Processes feed and returns stale versions.
URL: `https://cloud.uipath.com/gustoinc/Production/orchestrator_/libraries/tenant?tid=11015&fid=46023`

**"Sri mentioned something — is it already in Notion?"**
Check Standup Topics DB first — items from Sri's Google Doc were migrated on 2026-06-02.

**"What about the Broken Bots spreadsheet?"**
Sri shared a spreadsheet with 20 broken processes (8 months of history). We asked if she wants to bring it to Notion. Awaiting her response in the dev channel (`C0ANAPHL1NE`).

**"Is there Portuguese anywhere in Notion?"**
There should not be. Language rule: everything in English. If you find Portuguese, translate it before proceeding.
