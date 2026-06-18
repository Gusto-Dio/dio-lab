---
name: project-bt73387-bsca-nhe-screenshot
description: "BT-73387 — BSCA_NewHireEnrollment — screenshot errada + mensagem de erro genérica ao enrollar EE; investigação iniciada 2026-06-15"
metadata:
  node_type: memory
  type: project
  originSessionId: 9a512c2d-1799-45f7-8926-df6af1af7bfb
---

# BT-73387 — BSCA_NewHireEnrollment — Screenshot errada + mensagem vaga

**Branch:** `BT-73387-BSCA-NewHireEnrollment-screenshot-error-message-fix`
**Ticket:** https://gustohq.atlassian.net/browse/BT-73387
**PR:** https://github.com/Gusto/biztech-uipath-rpa/pull/2799 (aberta 2026-06-16)
**Processo Prod:** Benefits folder (ID 46023)
**Prioridade:** Low — Tammy Borders (reporter, 2026-06-05)

---

## O que pedem

1. **Screenshot errada:** quando BSCA lança "Portal exception" durante enrollment, o bot captura a tela errada. Deveria capturar a página "Exception Review" do portal.
2. **Mensagem genérica:** "Portal exception thrown while trying to enroll EE" é vaga. Tammy quer mensagem que especifique:
   - Carrier review + submissão manual necessária
   - Motivo: BSCA exige relatório de payroll para verificar elegibilidade do EE dentro desse período

**Impacto:** 14% dos casos nos últimos 7 dias.

---

## Logs Prod — Job 498859979 (2026-06-05, key: d8f07976-d949-49de-aa5c-764415b9a0f7)

Erros encontrados (múltiplos por run):

1. `CarrierPortalException: EE already in carrier portal` → `ProcessTransaction.xaml` → Throw "CarrierPortalException"
2. `NavigateToEnrollment: Could not find the UI element` → `<webctrl aaname='Enroll Employee' />` em `title='Account*'` — acontece quando "EE could not be found on carrier portal"
3. `SearchForEmployee: EE could not be found on carrier portal` — em `SearchForEmployee`
4. `SearchForEmployee: Could not find the UI element` → `<webctrl tag='C-EEA_NEW-MEMBER-ROSTER' />` (member roster)
5. `EnterCoverage: Not successfully navigate to the Plan Selections page` → Throw "navigationUnsuccesful" em `ProcessTransaction.xaml` — **este é provavelmente o cenário do "Portal exception"** (BSCA mostra exception review page e o bot não consegue ir para Plan Selections)
6. `EnterDependentsInformation: TypeInto 'First Name': Timeout reached` em `EnterDependentsInformation.xaml`
7. `Screenshot saved` aparece após cada falha (após "Resetting application environment")

---

## Análise dos logs

O erro mais provável para o cenário do ticket é #5: `EnterCoverage: Not successfully navigate to the Plan Selections page`.

Isso acontece quando o BSCA portal mostra a "Exception Review" page (BSCA detecta que o EE precisa de payroll report para verificar elegibilidade) — o bot não reconhece isso e retenta até esgotar, gerando um erro genérico.

O screenshot (`Screenshot saved`) é tirado depois que o erro já aconteceu, provavelmente após o `ResetAllActivities`/reset do ambiente — **não da página Exception Review do portal**. Por isso a tela errada.

---

## Git history — commits recentes

- `4c7d11bc` [BT-72126] BSCA NewHireEnrollment — Fix medical benefit type case mismatch + lib bump 1.550.1 (#2705) — **último commit, ~2026-05-27**
- `bd5b6084` [BT-72126] BSCA NewHireEnrollment — Fix Language Preference, Contact Method, and Add Dependent selectors (#2625)

O ticket foi aberto 2026-06-05, ~9 dias após o último deploy. Pode ser mudança de comportamento do portal BSCA ou simplesmente volume de casos com payroll exception aumentou.

---

## Status final (2026-06-16) — CONCLUÍDO

- PR #2799 **mergiada** em `develop`
- v7.0.2 **em produção**
- Comentário postado no Jira com resumo do fix
- **Próximo:** monitorar execuções Prod (Benefits folder 46023)

## Orchestrator IDs (Prod)

- Benefits folder: 46023
- Jobs faulted vistos: 498859979 (2026-06-05), 504429779 (2026-06-14, "another interactive job" — não relevante)
