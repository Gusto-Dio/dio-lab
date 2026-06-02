---
name: reference-benops-resources
description: "Links e localização dos recursos criados para o time BenOps RPA — Notion, GitHub skills repo, Google Doc"
metadata: 
  node_type: memory
  type: reference
  originSessionId: e63eaeb7-a294-498d-8d21-15aa2451fdd6
---

# BenOps RPA — Recursos do time

## Notion

- **Pasta RPA BenOps**: https://www.notion.so/35dad673c6c281ca9beed83cf58fdb22
  - Localização: BizTech RPA Docs > RPA BenOps
- **Claude Code Setup — BenOps RPA**: https://www.notion.so/35dad673c6c281d09313e23bf1a2652d
  - Guia completo de setup do Claude Code para novos membros

## GitHub — Skills repo

- **Repo**: https://github.com/Gusto-Dio/benops-rpa-skills (conta Gusto-Dio, público)
- **Repo local**: `C:\Users\diogenesribei_gsto\Documents\Projects\benops-rpa-skills`
- **Estrutura**: cada skill em sua própria subpasta (`skill-name/SKILL.md`)
- **Skills publicadas**:
  - `benops-rpa-setup` — setup interativo da VDI para novos membros
  - `benops-ticket-investigation` — investigação estruturada de falhas RPA em produção (Logs → Ticket → Git → PRs → Código → Fix)
- **Como instalar uma skill**:
  ```powershell
  New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\<skill-name>"
  Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Gusto-Dio/benops-rpa-skills/main/<skill-name>/SKILL.md" -OutFile "$env:USERPROFILE\.claude\skills\<skill-name>\SKILL.md"
  ```
- **Localização permanente pendente**: ainda a definir se vai para uma pasta dedicada no repo da Gusto ou como plugin no sfdc-shared

## Google Doc

- **Doc geral do time**: https://docs.google.com/document/d/1JtajuC7_tG7Mm6K5Mwk1xtTNqhD2C-BJk142f5_mRj4
- **Tab BenOps RPA**: `t.uul99gewleik` — setup do Claude Code adicionado em 2026-05-11
