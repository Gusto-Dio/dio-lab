# Workspace — IDs, Databases e Campos

## IDs fixos

| Recurso | ID |
|---|---|
| Hub page | `35dad673c6c281ca9beed83cf58fdb22` |
| Processes DB | `ba7266d884b6425c9fc0036b483bd8d0` |
| Standup Topics DB | `7a77a12fba92465f9226e372383a1299` |

URL da página de setup do Claude Code (publicada no Notion para o time):
`https://www.notion.so/35dad673c6c281d09313e23bf1a2652d`

---

## Localização no Notion

```
BizTech RPA Docs
  └── 🤖 BenOps RPA Hub          ← Hub page (35dad673...)
        ├── 📋 Standup Topics DB  ← 7a77a12f... (data source: 4ca84260...)
        ├── 🤖 Processes DB       ← ba7266d8... (data source: fa093b20...)
        ├── 🔧 Runbooks DB        ← 7d5fe4fb...
        └── 📦 Library DB         ← de5770484...
```

**Databases removidas em 2026-06-02:**
- 🏥 Carriers DB — campos vazios; infos de carrier incorporadas no Processes DB
- 👥 Team DB — substituída por callout simples no Hub page
- ⚠️ Alerts DB — não estava sendo utilizada
- 🚨 Incidents DB — não estava sendo utilizada

---

## Hub page — layout

Redesenhada em 2026-06-02 com layout 2 colunas inspirado no Revenue Notion page:

**Coluna esquerda:** callout Welcome + callout Team (lista alfabética)
**Coluna direita:** callout Navigate (→ links para databases) + callout Quick Links (Operations / Developer / Reference)

Timestamp de sync na primeira linha:
```
Synced daily via /benops-sync (GitHub PRs + Jira tickets) · Last synced: YYYY-MM-DD HH:MM
```
O `/benops-sync` atualiza essa linha a cada execução via `notion-update-page`.

---

## Processes DB — campos

| Campo | Tipo Notion | Valores aceitos / notas |
|---|---|---|
| Process | title | Nome do processo (ex: "UHC_SamX_Renewal_Modern") |
| Carrier | select | Anthem / BCBS MA / BCBS TX / BCBS IL / BCBS OK / BSCA / Kaiser / UHC / Beam / Principal / CoveredCal |
| Carrier Status | select | Active / On Hold / Deprecated — preenchido manualmente |
| Portal URL | url | URL do portal do carrier — preenchido manualmente |
| Carrier Notes | rich_text | Quirks e notas do carrier — preenchido manualmente |
| Type | select | NHE / Term / MemberUpdate / GroupSub / Recon / PacketCollection |
| Assignee | select | Diogenes / Ahsen / Hari / Oscar |
| Status | select | Not Started / In Progress / Pending Review / Ready for Deployment / Deployed to Prod / On Hold |
| Version | text | Versão da Gusto_Benefits library |
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

## Standup Topics DB — campos

| Campo | Tipo Notion | Valores aceitos / notas |
|---|---|---|
| Topic | title | Descrição do item de standup |
| Category | select | Blocker / Action Item / Documentation / Hackathon / Process / FYI |
| Priority | select | High / Medium / Low |
| Status | select | Open / In Progress / Done / Parked |
| Resource | select | Diogenes / Oscar / Hari / Ahsen / Sri / Team |
| Target Date | date | Data alvo para conclusão |
| Last Discussed | date | Última daily em que o item foi discutido |
| Notes | rich_text | Comentários acumulados — atualizado a cada standup |
| Jira Ticket | rich_text | Preenchido quando o tópico vira ticket (ex: "BT-73075") |

**Origem:** migrado do Google Doc [BenOps RPA Daily Stand up Notes](https://docs.google.com/document/d/1CXncG2oonWdKgIwi7dgw8_3bxPK3kEdqSk4x42rpG3Y) em 2026-06-02.
Histórico anterior preservado no Google Doc como referência.

---

## MCP tools usados

| Operação | Tool |
|---|---|
| Ler databases | `mcp__claude_ai_Notion_Gusto__notion-query-data-sources` |
| Atualizar página/linha | `mcp__claude_ai_Notion_Gusto__notion-update-page` |
| Criar linha nova | `mcp__claude_ai_Notion_Gusto__notion-create-pages` |
| Criar database nova | `mcp__claude_ai_Notion_Gusto__notion-create-database` |
| Alterar schema de database | `mcp__claude_ai_Notion_Gusto__notion-update-data-source` |
| Busca geral | `mcp__claude_ai_Notion_Gusto__notion-search` |
| Fetch de página | `mcp__claude_ai_Notion_Gusto__notion-fetch` |
