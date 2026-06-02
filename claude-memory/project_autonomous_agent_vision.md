---
name: project-autonomous-agent-vision
description: Visão de longo prazo para um agente autônomo capaz de atender tickets BenOps RPA de ponta a ponta — roadmap de maturidade, arquitetura e critérios de evolução
metadata:
  type: project
  originSessionId: e63eaeb7-a294-498d-8d21-15aa2451fdd6
---

# Visão — Agente Autônomo BenOps RPA

**Why:** A medida que as skills amadurecem e o padrão de tickets se repete (selector fix, popup handler, InvokeWorkflow missing, dependency bump), o custo de ter um humano em cada etapa supera o ganho de supervisão. O agente autônomo libera o time para tickets complexos e novos carriers.

**How to apply:** Usar este documento como critério de go/no-go em cada fase. Não avançar de fase sem os critérios da fase anterior estarem satisfeitos.

---

## Estado atual (2026-05-12)

### Skills disponíveis
| Skill | Cobertura |
|---|---|
| `benops-rpa-setup` | Setup VDI para novos membros |
| `benops-ticket-investigation` | Investigação estruturada de falhas em produção |
| `/ticket BT-XXXXX` | Contexto completo do ticket (Jira + Git + histórico) |
| `/analyze` | Validação do diff antes do PR |
| `/prep-pr` | Geração de PR estruturado |
| `/test-log` | Análise de log de execução UiPath |

### Gaps para autonomia
- Agent ainda depende de humano para aprovar diagnóstico, revisar XAML, confirmar Staging, e fazer merge
- XAML gerado por agente ainda não foi validado em produção sem revisão
- Não há critério formal de risco por tipo de ticket

---

## Arquitetura recomendada — Autonomia em tiers

### Por que tiers e não autonomia total imediata?

O risco não é uniforme. Um fix de selector em 1 arquivo é fundamentalmente diferente de uma mudança em um workflow compartilhado. Autonomia total sem classificação de risco leva a incidentes em produção. Tiers permitem evoluir progressivamente com dados reais.

### Tier 1 — Low risk (autonomia total candidata)
Características: 1 arquivo, sem Library, sem novo padrão de activity, fix pontual
Exemplos: selector desatualizado, popup não tratado, timeout muito curto, arquivo missing (criar vazio), dependency version bump
Critério de autonomia: agente acerta root cause + fix sem correção humana em 10 tickets consecutivos deste tier

### Tier 2 — Medium risk (autonomia supervisionada)
Características: múltiplos arquivos, novo padrão de activity, mudança em fluxo existente
Exemplos: novo popup handler em ProcessTransaction + EnterDependentsInformation, refactor de selector pattern
Critério de autonomia: taxa de aprovação de PR sem requested changes ≥ 90% em 20 tickets

### Tier 3 — High risk (sempre supervisionado)
Características: mudança em Library, novo workflow de zero, múltiplos carriers, mudança em fluxo de exceção principal
Critério: nunca autônomo — humano aprova antes de Staging

---

## Roadmap de maturidade

### Fase 1 — Skills foundation (agora)
- [x] `benops-ticket-investigation` publicada e testada
- [x] Workflow de atendimento documentado no Notion
- [ ] Skills testadas em 5+ tickets reais — medir taxa de diagnóstico correto
- [ ] Adicionar skill de XAML fix patterns (seletores, popup handlers, InvokeWorkflow)

### Fase 2 — Investigation autonomy (3-6 meses)
Critério de entrada: skill `benops-ticket-investigation` acertou root cause em 10 tickets sem correção humana

Entregáveis:
- Agente investiga e produz diagnóstico + fix proposal sem intervenção
- Humano valida apenas o fix proposal (não o diagnóstico)
- Medir: % de diagnósticos aprovados sem alteração

### Fase 3 — Code generation autonomy (6-12 meses)
Critério de entrada: taxa de PR aprovado sem requested changes ≥ 85% para Tier 1

Entregáveis:
- Skill `benops-xaml-fix-patterns` documentando os padrões validados
- Agente abre PR para Tier 1 tickets sem revisão humana do código
- Humano aprova apenas o merge (gate final)
- Medir: % de PRs aprovados na primeira revisão

### Fase 4 — Validation autonomy (12-18 meses)
Critério de entrada: Fase 3 estável por 3 meses

Entregáveis:
- Agente publica para Staging, dispara QueueItemRecreater, interpreta resultado
- Agente decide pass/fail no Staging sem humano
- Humano só recebe notificação: "Ticket X resolvido, PR mergeado, produção estável"
- Medir: false positives (agente diz pass, falha em prod) e false negatives

### Fase 5 — Full autonomy para Tier 1 (18+ meses)
Critério de entrada: 0 false positives em 30 dias consecutivos na Fase 4

Entregáveis:
- Pipeline: Ticket atribuído → agente fecha ponta a ponta → notifica Sri/Oscar
- Humano recebe sumário, não participa do fluxo
- Tier 2 continua com gate humano no PR
- Tier 3 continua supervisionado completo

---

## Melhor cenário técnico

**Claude Code como orquestrador** com:
- MCP connectors: Jira (leitura/escrita), GitHub (PR creation/merge), Slack (notificações), Orchestrator REST API (logs + publish + trigger)
- Skills BenOps: investigation, XAML patterns, PR prep, test-log
- Hooks de segurança: nunca editar em `develop`, nunca tocar Libraries, sempre Staging antes de Prod
- Gate humano configurável por tier: aprovação via Slack reaction ou GitHub PR approval

**Estrutura do agente autônomo:**
```
Jira webhook → Claude Code agent
  → /ticket BT-XXXXX (contexto)
  → benops-ticket-investigation (diagnóstico)
  → benops-xaml-fix-patterns (gera fix)
  → /analyze (valida diff)
  → /prep-pr (abre PR)
  → [gate Tier 2/3: aguarda review]
  → publica Staging → QueueItemRecreater → valida
  → merge → notifica Sri/Slack
  → fecha Jira
```

---

## Métricas para acompanhar a partir de agora

Em cada ticket resolvido, registrar:
1. Root cause identificado pelo agente = root cause real? (S/N)
2. PR aprovado sem requested changes? (S/N)
3. Staging passou na primeira execução? (S/N)
4. Qual tier o ticket era?

Quando tivermos 20 tickets registrados, reavaliar se estamos prontos para Fase 2.
