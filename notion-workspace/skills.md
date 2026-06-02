# Skills que interagem com o Notion

## `/benops-sync`

**Localização:** `benops-rpa-skills/plugins/benops-rpa/skills/benops-sync/SKILL.md`
**Quando usar:** diariamente, ou sempre que quiser atualizar o Hub com o estado atual de PRs e tickets.

### O que faz (7 passos)

1. Busca todas as PRs abertas e fechadas (últimos 7 dias) no repo `Gusto/biztech-uipath-rpa`
2. Busca tickets Jira do time BenOps (atualizados nos últimos 30 dias)
3. Faz query no Processes DB para pegar todas as linhas com seus IDs
4. Cruza PRs + Jira com cada linha do Processes DB pelo campo `Jira Ticket`
5. Deriva novo Status (ver regras em `workspace.md`) e atualiza apenas linhas com mudança
6. Sincroniza o Incidents DB: cria linhas novas para Bug tickets não registrados ainda
7. Atualiza o timestamp na Hub page

### Config embarcada na skill

```
Hub page ID:      35dad673c6c281ca9beed83cf58fdb22
Processes DB ID:  ba7266d884b6425c9fc0036b483bd8d0
Incidents DB ID:  5c5a55e5b865443ba41f31b19f8ea7b1
GitHub repo:      Gusto/biztech-uipath-rpa
Jira project:     BT
Team members:     currentUser(), "oscar.nunez", "ahsen", "harinath"
```

### Output esperado

```
### BenOps Sync complete
- X processes checked, Y statuses updated: [lista]
- Z new incidents recorded: [lista]
- Timestamp updated on hub page
```

Se não houver mudanças: `No changes detected.`

---

## `/morning`

O `/morning` chama o `/benops-sync` automaticamente no Step 6 após o briefing diário. O sync roda silenciosamente — se não houver mudanças, só adiciona uma linha `🔄 BenOps Hub synced.`

---

## Claude Code Setup page (Notion)

**URL:** https://www.notion.so/35dad673c6c281d09313e23bf1a2652d
**Conteúdo:** Guia de setup do Claude Code para novos membros do time BenOps RPA.
**Localização no Notion:** dentro do Hub page (`RPA BenOps`).
**Mantida por:** Diogenes. Atualizar manualmente quando mudar versão do plugin ou processo de instalação.

O mesmo conteúdo está no Google Doc do time:
- Doc: `https://docs.google.com/document/d/1JtajuC7_tG7Mm6K5Mwk1xtTNqhD2C-BJk142f5_mRj4`
- Tab: `RPA BenOps Nov 2025` (tab ID: `t.uul99gewleik`)

---

## `/benops-triage-agent`

Não interage com Notion diretamente. Lê Slack + Jira, diagnóstica Produção, e posta no Jira + Slack. Se no futuro quisermos registrar incidentes automaticamente no Incidents DB a partir do triage, essa seria a integração natural.
