# Continuidade de Sessão — Notion

> Leia este arquivo primeiro antes de qualquer trabalho no Notion.
> Última atualização: 2026-06-02

---

## Estado atual (2026-06-02)

### O que está funcionando

- Hub page criada e acessível ✅
- Processes DB com linhas para os processos ativos do time ✅
- Incidents DB com bugs registrados ✅
- `/benops-sync` operacional — roda no `/morning` automaticamente ✅
- Claude Code Setup page publicada para onboarding do time ✅

### O que ainda está pendente / pode ser melhorado

| Item | Descrição | Prioridade |
|---|---|---|
| Processes DB — processos faltantes | Verificar se todos os processos do time têm linha no DB (ex: UHC_SamX, CoveredCal, BCBS_TX/IL) | Média |
| Incidents DB — Root Cause em branco | Vários incidentes recentes têm campos Root Cause e Fix Applied em branco; preencher após fechar tickets | Baixa |
| Integration com RCA Agent | Quando o benops-rca-agent for implementado, ele deve criar linhas no Incidents DB automaticamente via Notion MCP | Futura |
| Priority Check list para Sri | A lista de processos HIGH priority do RCA Agent ainda não foi configurada em lugar nenhum — Sri pediu que fosse configurável (Orchestrator Asset / Google Sheet) | Futura |

---

## Como adicionar um novo processo ao Processes DB

1. Identifique o nome do processo (`UHC_SamX_Renewal_Modern`, etc.)
2. Use `mcp__claude_ai_Notion_Gusto__notion-create-pages` com parent = Processes DB ID (`ba7266d884b6425c9fc0036b483bd8d0`)
3. Campos obrigatórios: `Title`, `Jira Ticket` (para o sync funcionar)
4. O `/benops-sync` vai preencher Status, PR Number e Last Synced automaticamente

---

## Como adicionar manualmente um incidente

1. Use `mcp__claude_ai_Notion_Gusto__notion-create-pages` com parent = Incidents DB ID (`5c5a55e5b865443ba41f31b19f8ea7b1`)
2. Preencher: Title, Date, Process, Jira Ticket
3. Root Cause e Fix Applied: preencher assim que o fix for confirmado

---

## Pessoas-chave

| Nome | Papel no contexto do Notion |
|---|---|
| Sri Perinkolam (`U07KMNHHFB6`) | Usuária principal do Hub — acompanha status dos bots |
| Oscar Nuñez (`U05UYA9S4G7`) | Engenheiro senior — pode precisar atualizar Processes DB ao fechar tickets |
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

# Listar linhas do Incidents DB
mcp__claude_ai_Notion_Gusto__notion-query-data-sources databaseId="5c5a55e5b865443ba41f31b19f8ea7b1"
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

**"A Sri pediu para adicionar um campo novo — como fazer?"**
Notion MCP não tem ferramenta para adicionar campos a databases diretamente. Adicionar via UI do Notion, então atualizar `workspace.md` com o novo campo e ajustar a skill `/benops-sync` se o campo precisar ser sincronizado.

**"Quais processos têm linha no Processes DB?"**
Rodar `notion-query-data-sources` no Processes DB ID e listar os títulos. Comparar com os processos ativos no Orchestrator.
