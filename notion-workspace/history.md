# Histórico — O que foi construído e por quê

## Contexto: o pedido da Sri

Sri Perinkolam (Onshore Program Manager, Slack: `U07KMNHHFB6`) precisava de visibilidade sobre o estado dos processos automatizados do time RPA BenOps sem precisar entrar no Jira ou no GitHub. O pedido central era:

> "Quero saber quais bots estão em fix, quais estão esperando review, e quais já foram para produção."

A resposta foi criar o **BenOps RPA Hub** no Notion com databases que se atualizam automaticamente via `/benops-sync`.

---

## Timeline de construção

### 2026-05 — Hub page + Processes DB

- Criada a página Hub `RPA BenOps` dentro de `BizTech RPA Docs`
- Criado o Processes DB com campos: Title, Status, PR Number, Jira Ticket, Last Synced
- Criado o Incidents DB com campos: Title, Date, Process, Jira Ticket, Root Cause, Fix Applied
- Escrita a skill `/benops-sync` (Step 1–7) que cruza GitHub + Jira → Notion automaticamente
- Integrado ao `/morning`: roda no Step 6 após o briefing diário

### 2026-05 — Claude Code Setup page

- Publicada página de setup do Claude Code no Notion (dentro do Hub)
- Mesmo conteúdo adicionado ao Google Doc do time (tab `RPA BenOps Nov 2025`)
- Objetivo: membros novos (ex: Harinath) conseguem configurar o ambiente sem precisar pedir ajuda

### 2026-05/06 — benops-rca-agent (Hackathon)

- Sri ajustou o design do agente para incluir **Priority Check** configurável
  - Lista de processos HIGH priority pode ser configurada em: Orchestrator Asset, JSON/config file, ou Google Sheet compartilhada
  - Objetivo: Sri e leads conseguem mover processos entre HIGH e STANDARD sem mudança de código
- O agente faria integração natural com o Incidents DB no futuro (registrar RCA automaticamente)

---

## Por que a estrutura do Hub é assim

### Hub page (landing) + databases separadas

O Hub page serve de "vitrine" para Sri — ela vê o timestamp do último sync e navega para as databases que quer. Não colocamos tudo em uma só página porque o Notion não suporta filtros e views ricas em páginas simples — databases têm isso.

### Processes DB separada de Incidents DB

- **Processes DB** = estado atual de cada bot (vivo, mutável)
- **Incidents DB** = histórico de falhas (append-only, registro permanente)

Esses são conceitos distintos com ciclos de vida diferentes. Misturar na mesma database tornaria os filtros confusos e a leitura da Sri mais difícil.

### Deduplicação por `Jira Ticket`

O `/benops-sync` usa o campo `Jira Ticket` como chave primária para:
1. Cruzar PRs do GitHub com linhas do Processes DB (via `[BT-XXXXX]` no título da PR)
2. Evitar registros duplicados no Incidents DB (verifica antes de criar)

Isso evita que o sync crie sujeira no Notion mesmo rodando várias vezes por dia.

### Status derivado (não manual)

O Status no Processes DB não é preenchido manualmente — o sync o deriva de Jira + GitHub. Isso porque manual = esquecido. A Sri esperava que o Hub estivesse sempre atualizado; derivação automática garante isso.

---

## O que a Sri sabe (e não sabe) sobre o Hub

Sri sabe que o Hub existe e que é atualizado automaticamente. Ela usa para acompanhar progresso sem pedir updates manuais ao time.

Ela **não** configura o Hub diretamente — a manutenção (adicionar processos novos, ajustar campos) é feita pelo Diogenes quando necessário.

O campo `Root Cause` e `Fix Applied` no Incidents DB **é preenchido manualmente** pelo engenheiro depois do fix — o sync lembra disso no output.
