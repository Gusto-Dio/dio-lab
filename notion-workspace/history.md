# Histórico — O que foi construído e por quê

## Contexto: o pedido da Sri

Sri Perinkolam (Onshore Program Manager, Slack: `U07KMNHHFB6`) precisava de visibilidade sobre o estado dos processos automatizados do time RPA BenOps sem precisar entrar no Jira ou no GitHub. O pedido central era:

> "Quero saber quais bots estão em fix, quais estão esperando review, e quais já foram para produção."

A resposta foi criar o **BenOps RPA Hub** no Notion com databases que se atualizam automaticamente via `/benops-sync`.

Em 2026-06-02, a Sri pediu duas melhorias adicionais via Slack:
> "Look into this page as well for more inputs and how we can modify ours" (ref: Revenue Notion page)
> "I would suggest for us to pull in the daily standup notes to Notion — we have many important points there which can be converted to Jira tickets."

---

## Timeline de construção

### 2026-05 — Hub page + Processes DB

- Criada a página Hub `RPA BenOps` dentro de `BizTech RPA Docs`
- Criado o Processes DB com campos: Process, Carrier, Type, Assignee, Status, PR Number, Jira Ticket, Last Synced
- Criado o Incidents DB com campos: Title, Date, Process, Jira Ticket, Root Cause, Fix Applied
- Escrita a skill `/benops-sync` (Step 1–7) que cruza GitHub + Jira → Notion automaticamente
- Integrado ao `/morning`: roda no Step 6 após o briefing diário

### 2026-05 — Claude Code Setup page

- Publicada página de setup do Claude Code no Notion (dentro do Hub)
- Mesmo conteúdo adicionado ao Google Doc do time (tab `RPA BenOps Nov 2025`)
- Objetivo: membros novos (ex: Harinath) conseguem configurar o ambiente sem precisar pedir ajuda

### 2026-06-02 — Redesign do Hub + unificação Carriers/Processes + Standup Topics

**Motivação:** Sri pediu para simplificar o Hub (referenciou o Revenue Notion page como modelo) e para trazer as notas de standup para o Notion.

#### Carriers DB unificada com Processes DB
- A Carriers DB tinha Portal URL e Quirks/Notes 100% vazios — não agregava valor
- Solução: adicionar 3 campos ao Processes DB (`Carrier Status`, `Portal URL`, `Carrier Notes`) e trashar a Carriers DB
- Todas as 17 linhas do Processes DB receberam `Carrier Status = Active`

#### Hub page redesenhada
- Layout 2 colunas inspirado no Revenue Notion page (referência da Sri)
- Coluna esquerda: callout **Welcome** + callout **Team** (lista alfabética, Sri com label PM)
- Coluna direita: callout **Navigate** (→ links para databases) + callout **Quick Links** (Operations / Developer / Reference)
- Removido: bloco verboso "How to use this hub"
- Team DB trashada — substituída pelo callout simples (time pequeno, não precisava de database)
- Alerts DB e Incidents DB trashadas — não estavam sendo utilizadas

#### Standup Topics DB criada
- Migradas 11 itens do [Google Doc de standup da Sri](https://docs.google.com/document/d/1CXncG2oonWdKgIwi7dgw8_3bxPK3kEdqSk4x42rpG3Y)
- Campo `Jira Ticket` adicionado para rastrear quando um tópico vira ticket
- Google Doc preservado como referência histórica (link no Hub)

---

## Por que a estrutura do Hub é assim

### Layout 2 colunas (pós 2026-06-02)

O Hub page serve de "vitrine" para Sri. A coluna esquerda dá contexto (quem somos, quem é o time); a coluna direita dá ação (para onde ir, links rápidos). Databases ficam abaixo — visíveis mas sem poluir o topo da página.

### Processes DB com campos de carrier embutidos

Carriers DB foi eliminada porque era redundante e vazia. Embutir os campos de carrier no Processes DB permite que um engenheiro veja Portal URL e notas do carrier na mesma linha do processo — sem precisar navegar para outra database.

### Standup Topics DB separada do Processes DB

- **Processes DB** = estado operacional de cada bot (atualizado pelo sync)
- **Standup Topics DB** = agenda e action items do time (atualizado manualmente nas dailys)

Ciclos de vida diferentes. A Sri gerencia o Standup Topics; o sync gerencia o Processes.

### Deduplicação por `Jira Ticket`

O `/benops-sync` usa o campo `Jira Ticket` como chave primária para cruzar PRs do GitHub com linhas do Processes DB (via `[BT-XXXXX]` no título da PR). Isso evita duplicatas mesmo rodando várias vezes por dia.

### Status derivado (não manual)

O Status no Processes DB não é preenchido manualmente — o sync o deriva de Jira + GitHub. Manual = esquecido. A Sri esperava que o Hub estivesse sempre atualizado; derivação automática garante isso.

---

## O que a Sri sabe (e não sabe) sobre o Hub

Sri sabe que o Hub existe, que é atualizado automaticamente, e que o Standup Topics DB é onde ficam os itens das dailys. Ela usa o Hub para acompanhar progresso sem pedir updates manuais ao time.

Ela **não** configura o Hub diretamente — a manutenção (adicionar processos, ajustar campos, alterar schemas) é feita pelo Diogenes quando necessário.

O Standup Topics DB é de uso misto: Sri e o time podem atualizar `Notes`, `Status` e `Jira Ticket` diretamente no Notion durante ou após as dailys.
