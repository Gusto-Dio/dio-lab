# Continuidade de Sessão — Notion

> Leia este arquivo primeiro antes de qualquer trabalho no Notion.
> Última atualização: 2026-06-03

---

## Estado atual (2026-06-03)

### O que está funcionando

- Hub page criada, acessível e redesenhada (layout 2 colunas) ✅
- Processes DB com 17 processos + campos de carrier unificados ✅
- Standup Topics DB criada com 11 itens migrados do Google Doc ✅
- `/benops-sync` operacional — roda no `/morning` automaticamente ✅
- Claude Code Setup page publicada para onboarding do time ✅

### O que foi feito em 2026-06-02

| O que | Detalhe |
|---|---|
| Carriers DB + Processes DB unificadas | 3 campos novos no Processes DB: `Carrier Status`, `Portal URL`, `Carrier Notes`. Carriers DB trashada. |
| Hub page redesenhada | Layout 2 colunas (Welcome + Team / Navigate + Quick Links). Sem "How to use" verboso. |
| Team DB → callout | Team DB trashada; lista de membros no callout do Hub. |
| Alerts DB e Incidents DB removidas | Não estavam sendo utilizadas. Trashadas. |
| Standup Topics DB criada | 11 itens migrados do Google Doc da Sri. Campo `Jira Ticket` para rastrear conversão em tickets. |

### O que ainda está pendente

| Item | Descrição | Prioridade |
|---|---|---|
| Processes DB — processos faltantes | Verificar se UHC_SamX e CoveredCal têm linha no DB | Média |
| Standup Topics — Jira Tickets | Preencher campo `Jira Ticket` nos itens que já têm ticket associado | Baixa |
| Portal URL e Carrier Notes | Preencher manualmente no Processes DB por carrier | Baixa |

---

## Como adicionar um novo processo ao Processes DB

1. Identifique o nome do processo (`UHC_SamX_Renewal_Modern`, etc.)
2. Use `mcp__claude_ai_Notion_Gusto__notion-create-pages` com parent = Processes DB ID (`ba7266d884b6425c9fc0036b483bd8d0`)
3. Campos obrigatórios: `Process`, `Carrier`, `Jira Ticket` (para o sync funcionar)
4. O `/benops-sync` vai preencher Status, PR Number e Last Synced automaticamente

---

## Como adicionar um item ao Standup Topics DB

1. Use `mcp__claude_ai_Notion_Gusto__notion-create-pages` com parent = Standup Topics DB data source (`4ca84260-cb84-4c31-b14c-07edcea4e1e6`)
2. Campos obrigatórios: `Topic`, `Category`, `Status`
3. Preencher `Jira Ticket` quando o item virar ticket Jira
4. Atualizar `Last Discussed` e `Notes` a cada standup

---

## Pessoas-chave

| Nome | Papel no contexto do Notion |
|---|---|
| Sri Perinkolam (`U07KMNHHFB6`) | Usuária principal do Hub — acompanha status dos bots e usa o Standup Topics DB nas dailys |
| Oscar Nuñez (`U05UYA9S4G7`) | Engenheiro — pode precisar atualizar Processes DB ao fechar tickets |
| Hari | Engenheiro — assignee de Kaiser CA MLE e outros processos |
| Ahsen | Engenheiro — assignee de vários processos BCBS/Anthem |
| Diogenes Ribeiro | Maintainer do Hub e das skills que o atualizam |

---

## Comandos úteis para trabalhar no Notion

```
# Ver estado atual do Hub
/benops-sync

# Fazer o briefing diário (já inclui sync no final)
/morning

# Buscar uma página específica no Notion
mcp__claude_ai_Notion_Gusto__notion-search query="BenOps RPA"

# Ler o conteúdo do Hub
mcp__claude_ai_Notion_Gusto__notion-fetch pageId="35dad673c6c281ca9beed83cf58fdb22"

# Listar linhas do Processes DB
mcp__claude_ai_Notion_Gusto__notion-query-data-sources databaseId="ba7266d884b6425c9fc0036b483bd8d0"

# Listar linhas do Standup Topics DB
mcp__claude_ai_Notion_Gusto__notion-query-data-sources databaseId="7a77a12fba92465f9226e372383a1299"
```

---

## Perguntas frequentes de sessão nova

**"O Hub já existe ou precisa ser criado?"**
Já existe. URL: https://www.notion.so/35dad673c6c281ca9beed83cf58fdb22

**"Quais IDs usar?"**
Ver `workspace.md` — todos mapeados com tipo e propósito.

**"O sync está quebrando — o que verificar?"**
1. Confirmar que o MCP Notion está autenticado (token válido)
2. Verificar se os IDs do `workspace.md` ainda batem com o que existe no Notion
3. Rodar `notion-fetch` no Hub page ID para confirmar acesso

**"Como adicionar um campo novo a uma database?"**
Usar `mcp__claude_ai_Notion_Gusto__notion-update-data-source` com DDL:
`ADD COLUMN "Nome" TIPO` — suporta SELECT, RICH_TEXT, DATE, URL, etc.
Atualizar `workspace.md` com o novo campo após adicionar.

**"Quais processos têm linha no Processes DB?"**
Rodar `notion-query-data-sources` no Processes DB ID e listar os títulos. Comparar com os processos ativos no Orchestrator.

**"A Sri mencionou algo — já está no Notion?"**
Verificar Standup Topics DB primeiro — itens do Google Doc da Sri foram migrados em 2026-06-02.
