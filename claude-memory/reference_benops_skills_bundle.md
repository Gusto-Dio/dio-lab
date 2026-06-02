---
name: reference-benops-skills-bundle
description: "Skills do bundle biztech-rpa-skills instaladas localmente — triage, migration-repair, test-cases"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 46927386-82ed-4fa1-946a-18d42e326071
---

Três skills instaladas em 2026-05-19 via `install-all.ps1` do bundle `biztech-rpa-skills-bundle.zip`:

| Skill | Comando | Propósito |
|---|---|---|
| `uipath-benops-triage` | `/benops-triage-agent BT-XXXXX` | First response: lê Slack + Jira, diagnostica Produção, estima SP, posta business update + dev handoff |
| `uipath-migration-repair` | `/uipath-migration-repair` | Fix mecânico para projetos falhando em `uip rpa pack` após migração Legacy → Windows |
| `uipath-test-cases-from-ticket` | `/uipath-test-cases-from-ticket BT-XXXXX` | Cria casos de teste no Staging amostrando queue items de Produção via QueueItemRecreator |

**Fluxo encadeado:**
`Ticket → /benops-triage-agent → /uipath-migration-repair (se migration) → /uipath-test-cases-from-ticket (quando fix em PR)`

**Localização:** `~/.claude/skills/` + `~/.claude/commands/`
