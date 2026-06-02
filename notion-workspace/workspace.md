# Workspace — IDs, Databases e Campos

## IDs fixos

| Recurso | ID |
|---|---|
| Hub page | `35dad673c6c281ca9beed83cf58fdb22` |
| Processes DB | `ba7266d884b6425c9fc0036b483bd8d0` |
| Incidents DB | `5c5a55e5b865443ba41f31b19f8ea7b1` |

URL da página de setup do Claude Code (publicada no Notion para o time):
`https://www.notion.so/35dad673c6c281d09313e23bf1a2652d`

---

## Localização no Notion

```
BizTech RPA Docs
  └── RPA BenOps          ← Hub page (35dad673...)
        ├── Processes DB  ← ba7266d8...
        └── Incidents DB  ← 5c5a55e5...
```

---

## Processes DB — campos

| Campo | Tipo Notion | Valores aceitos / notas |
|---|---|---|
| Title | title | Nome do processo (ex: "UHC_SamX_Renewal_Modern") |
| Status | select | "In Progress" / "Pending Review" / "Ready for Deployment" / "Deployed to Prod" |
| PR Number | rich_text | Ex: "#2733 Open — Awaiting Review" ou "#2699 Merged" |
| Jira Ticket | rich_text | Ex: "BT-73075" — chave de cross-reference |
| Last Synced | date | ISO 8601 (YYYY-MM-DD) — atualizado pelo `/benops-sync` |

### Regra de derivação do Status (usada pelo `/benops-sync`)

| Condição | Status derivado |
|---|---|
| Jira = Done AND PR merged | "Deployed to Prod" |
| Jira = Done AND PR open | "Ready for Deployment" |
| PR com review = CHANGES_REQUESTED | "Pending Review" |
| PR open AND reviewers pendentes | "Pending Review" |
| Jira = In Progress AND PR open | "In Progress" |
| Jira = In Progress AND sem PR | "In Progress" |
| Sem match em nenhum dos dois | skip (não atualiza) |

---

## Incidents DB — campos

| Campo | Tipo Notion | Valores aceitos / notas |
|---|---|---|
| Title | title | Summary do ticket Jira |
| Date | date | `resolutiondate` se Done; `created` se ainda em aberto |
| Process | rich_text | Nome do processo (lookup via Processes DB) |
| Jira Ticket | rich_text | Chave (ex: "BT-72018") — chave de deduplicação |
| Root Cause | rich_text | Preenchido manualmente após o sync |
| Fix Applied | rich_text | Preenchido manualmente após o sync |

**Regra de deduplicação:** o `/benops-sync` verifica o campo `Jira Ticket` antes de criar. Se a chave já existe, não cria duplicata.

---

## Hub page — timestamp

A página Hub tem uma linha de texto com o timestamp do último sync:

```
Synced daily via /benops-sync · Last synced: YYYY-MM-DD HH:MM
```

O `/benops-sync` (Step 6) atualiza essa linha a cada execução via `notion-update-page` no Hub page ID.

---

## MCP tool usado

| Operação | Tool |
|---|---|
| Ler databases | `mcp__claude_ai_Notion_Gusto__notion-query-data-sources` |
| Atualizar página/linha | `mcp__claude_ai_Notion_Gusto__notion-update-page` |
| Criar linha nova (Incidents) | `mcp__claude_ai_Notion_Gusto__notion-create-pages` |
| Busca geral | `mcp__claude_ai_Notion_Gusto__notion-search` |
| Fetch de página | `mcp__claude_ai_Notion_Gusto__notion-fetch` |
