---
name: project-bt73075-uhc-samx-renewal
description: "BT-73075 — UHC_SamX_GroupSubmissions_Renewal_Modern, fix seletores close icon (PR #2733) + fix DebuggerApi + robustez (branch debuggerapi-fix)"
metadata: 
  node_type: memory
  type: project
  originSessionId: ff825b13-1fef-4b4e-adf7-dd3ecfb928ac
---

# BT-73075 — UHC_SamX_GroupSubmissions_Renewal_Modern

**Status:** Scheduled | **Assignee:** Oscar Nuñez | **Prioridade declarada:** High
**Bot desabilitado em:** 2026-05-28 (Oscar desabilitou + notificou via Slack)
**Sri designou:** Diogenes faz shadow de Oscar neste ticket

**Why:** Bot falhou com seletor quebrado ao clicar no ícone "X" de fechar no portal SAMx legado. Impacto: +67 transações.

**How to apply:** Alinhar com Oscar sobre abordagem. Dois branches ativos com fixes distintos.

---

## Processo

**Caminho:** `Processes/Benefits/CarrierAutomations/GroupSubmission/UnitedHealthcare/SamX/UHC_SamX_Renewal_Modern/`
**Versão atual:** 1.3.4 | **Framework:** Windows | **Queue:** `UHC_SAMx_GroupSubmissions_Renewal`

### Dependências
| Library | Versão no project.json (branch debuggerapi-fix) |
|---|---|
| Gusto_Benefits_UHC | 1.1.8 |
| Gusto_Benefits_UHC_SAMx | 1.0.10 |
| Gusto_Modern_Generic | 1.3.15 |
| Gusto_Modern_Generic_Benefits | 1.0.4 |

**Nota:** branch close-icon-fix tem 1.0.13 — lib 1.0.13 existe em `~/.nuget/packages/gusto_benefits_uhc_samx/1.0.13/`

---

## Branches ativas

### Branch 1: `BT-73075-UHC-SamX-Renewal-close-icon-fix`
- PR #2733 — aberta, aguardando review Oscar/Hari
- Fix: remove `htmlwindowname='SAMX'` dos seletores (5 ocorrências em 3 arquivos)
- 4 transações Staging Successful: EbDO1IAN, EbMj3IAF, EcgcUIAR, EeaEQIAZ
- v1.3.5 publicada no Staging (release ID 279523)

### Branch 2: `BT-73075-UHC-SamX-Renewal-debuggerapi-fix` ← BRANCH ATUAL
- Ticket: BT-73253 (separado do BT-73075)
- Fixes aplicados em 2026-06-02:

#### Fix 1 — DebuggerApi → Simulate (CONCLUÍDO)
`InteractionMode="DebuggerApi"` → `InteractionMode="Simulate"` em **11 ocorrências** em 4 arquivos:
- `InitEnvironment.xaml` (5x: 3 NApplicationCard + 2 NClick)
- `Framework/InitEnvironment.xaml` (4x: 2 NApplicationCard + 2 NClick)
- `ProcessLayer/ReviewRenewingPlans.xaml` (1x NApplicationCard)
- `ProcessLayer/SearchForGroup.xaml` (1x NApplicationCard)

#### Fix 2 — Robustez: RetryScope + NCheckState + elementFound (CONCLUÍDO — 2026-06-02)
Padrão: `RetryScope(5x, 3s)` → reset `elementFound=False` → `NCheckState(15s)` → IfExists: `elementFound=True` + NClick / IfNotExists: no-op → Condition: `[elementFound]`

**Concluído:**
- [x] Variável `elementFound (Boolean, default=False)` adicionada a `InitEnvironment.xaml` (Sequence raiz)
- [x] Variável `elementFound (Boolean, default=False)` adicionada a `Framework/InitEnvironment.xaml` (Sequence raiz)
- [x] `InitEnvironment.xaml`: NClick_1, NClick_3, NClick_7, NClick_9 wrappados (RetryScope_NClick1/3/7/9)
- [x] `Framework/InitEnvironment.xaml`: NClick_1, NClick_3, NClick_6, NClick_7 wrappados (RetryScope_NClick1/3/6/7)

**Próximo passo:** Testar via Studio (branch `BT-73075-UHC-SamX-Renewal-debuggerapi-fix`), depois preparar PR para BT-73253.

---

## Causa raiz confirmada (close-icon-fix)
- Portal SAMx mudou `window.name` de `'SAMX'` para string vazia `''`
- `title='UHC-SAMx'` permanece correto
- Fix: remover `htmlwindowname='SAMX'` dos seletores

## Causa raiz (debuggerapi-fix)
- `InteractionMode="DebuggerApi"` só funciona no debugger do Studio
- Robot em produção falha silenciosamente/lança exceção

## Item de Staging
- Fila: `UHC_SAMx_GroupSubmissions_Renewal` (folder Benefits, Staging)
- Reference: `a0mR700000EegoTIAR` | Group: `1674620` | Effective: `2026-08-01`

## Nota de infra
- Ao rodar via Orchestrator Prod/Staging: garantir que `.local/` do projeto foi deletado se houve troca de branch com versão diferente de lib
- `Gusto_Benefits_UHC_SAMx` 1.0.10 disponível no feed; 1.0.13 apenas no cache local (`~/.nuget/packages/`)
