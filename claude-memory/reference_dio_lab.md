---
name: reference-dio-lab
description: "dio-lab — repo privado pessoal em Gusto-Dio para brainstorms, hackathon specs, experimentos e material de referência"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4d63ccc9-4c81-437e-a1b5-7d3b610bf4d3
---

# dio-lab — Workspace Pessoal

**URL:** https://github.com/Gusto-Dio/dio-lab  
**Visibilidade:** Privado  
**Owner:** Gusto-Dio

## Propósito
Armazenar brainstorms, specs de ideias, material de hackathon e experimentos que não pertencem ao repo principal `biztech-uipath-rpa`.

## Conteúdo atual

| Pasta | Projeto | Status |
|---|---|---|
| `benops-rca-agent/` | BenOps RCA Agent — Benefits Hackathon junho 2026 | Em andamento |
| `notion/runbooks.md` | 8 runbooks operacionais BenOps RPA para criar no Notion | Pronto para importar |
| `notion-workspace/` | Docs do workspace Notion: IDs, databases, session continuity | Referência |
| `claude-memory/` | Backup das memórias do Claude Code | Sincronizar ao encerrar sessão |

## Runbooks (notion/runbooks.md)
8 runbooks baseados em situações reais, prontos para criar no Notion:
1. Buildkite PR failures (3 padrões)
2. Bot falhando em produção — triage
3. DebuggerApi em processo migrado
4. Navigation flapping — RetryScope + NCheckState
5. Legacy → Windows migration
6. Library version bump
7. Fluxo completo de PR
8. Publicar library no Orchestrator

**Para criar no Notion:** passar para nova sessão — ler `notion/runbooks.md` do GitHub `Gusto-Dio/dio-lab` e criar subpáginas no hub BenOps RPA.

## Como usar
Quando criar um novo brainstorm ou spec, criar uma nova pasta no repo com README + arquivos relevantes e fazer push via MCP GitHub (owner: `Gusto-Dio`, repo: `dio-lab`).

Ver [[project-hackathon-rca-agent]] para detalhes do projeto atual.
