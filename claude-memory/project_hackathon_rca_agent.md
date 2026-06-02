---
name: project-hackathon-rca-agent
description: "BenOps RCA Agent — hackathon Benefits junho 2026. Agente Python autônomo que detecta falhas no Orchestrator, analisa com Claude API e cria tickets Jira com RCA pré-diagnosticado"
metadata: 
  node_type: memory
  type: project
  originSessionId: ff825b13-1fef-4b4e-adf7-dd3ecfb928ac
---

# BenOps RCA Agent — Hackathon Benefits June 2026

**Status:** Approved for hackathon implementation
**Spec:** `docs/superpowers/specs/2026-05-26-benops-rca-agent-design.md`

## Repositório
**https://github.com/Gusto-Dio/dio-lab** (privado) — pasta `benops-rca-agent/`

Arquivos no repo:
- `design-spec.md` — spec completa
- `pitch.html` — slide principal (priority check + painel lateral)
- `architecture.html` / `architecture-en.html` — diagrama de arquitetura (PT e EN)
- `demo-script.html` — roteiro do demo (3 min ao vivo)

Arquivos locais originais: `.superpowers/brainstorm/1458-1779811274/content/`

## O que faz
Agente Python rodando na VM (GSTO-FR5-APP002):
1. Polls Orchestrator a cada 60s por jobs Faulted
2. Coleta logs + XAML source + PR history em paralelo
3. Envia contexto ao Claude API → RCA + classificação de falha
4. **Priority Check**: verifica se o processo é high-priority
   - HIGH → cria ticket Jira pré-diagnosticado + alerta Slack com link
   - STANDARD → apenas alerta Slack no canal dev (sem ticket)
5. Meta: falha → diagnóstico em < 60 segundos

## Priority Check (ajuste da Sri)
Classificação dinâmica — lista de processos high-priority configurável em:
- Orchestrator Asset (recomendado)
- JSON/config file no VM
- Google Sheet compartilhada com leads

Processos podem entrar/sair da lista sem mudança de código.

## Failure Classification
`portal_change` | `data_quality` | `business_rule` | `network_timeout` | `library_incompatibility` | `unknown`

## Ticket Levels (naming)
- L1 = **Patch** — selector break, popup, timeout, dependency bump
- L2 = **Impact** — múltiplos arquivos, data quality, business rule
- L3 = **Critical** — Library, portal redesign, falha em cascata

## Award Categories
- Best Use of AI
- Best Impact for CX

## Demo Plan
Runtime: ~3 min ao vivo na VM
1. Explicar problema atual (2+ horas manual)
2. Triggerar job de teste configurado para falhar
3. Mostrar agente rodando no terminal: detect → collect → Claude → ticket → Slack
4. Abrir Jira e Slack ao vivo
5. Landing: 47s vs 2h+
