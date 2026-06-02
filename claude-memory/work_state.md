---
name: work-state-active-prs-in-progress-work-pendencias
description: "Estado atual de todas as PRs abertas, trabalho em andamento e próximos passos por ticket"
metadata: 
  node_type: memory
  type: project
  originSessionId: e63eaeb7-a294-498d-8d21-15aa2451fdd6
---

# Estado do trabalho — atualizado 2026-06-02 (sessão)

---

## PRs concluídas (todas merged)

| PR | Ticket | Descrição | Merged |
|---|---|---|---|
| #2569 | BT-72016 | BCBS_TX Terminations — Windows migration | 2026-05-06 |
| #2570 | BT-72018 | BCBS_MA NewHireEnrollment — Windows migration | 2026-05-13 |
| #2580 | BT-72016 | Gusto_Benefits BCBS_TX_IL — login/selector fix | 2026-05-06 |
| #2624 | BT-72126 | Gusto_Benefits BSCA NHE — lib fixes (1.544.0) | 2026-05-13 |
| #2625 | BT-72126 | BSCA NewHireEnrollment — processo | 2026-05-13 |
| #2646 | BT-72124 | Anthem NewHireEnrollment — Windows migration + fixes | 2026-05-14 |
| #2674 | BT-72337 | Gusto_Benefits lib 1.550.0 + FillConfirmationForm fix | 2026-05-20 |
| #2676 | BT-72337 | BSCA_Terminations — Windows migration + lib bump 7.0.1 | 2026-05-20 |
| #2678 | BT-72337 | BSCA_MemberUpdates — Windows migration + lib bump 7.0.0 | 2026-05-20 |
| #2724 | BT-73029 | BSCA_MemberUpdates — canModifyEE fix + card/Next selectors + lib 1.550.1 (7.0.1) | 2026-05-27 |
| #2683 | BT-72337/BT-72410 | BSCA_GroupSubmissions_MemberLevel — lib bump 1.550.1 + CSV fix + column guards (6.2.1) | 2026-05-22 |
| #2691 | BT-72268 | Anthem_Terminations — Gusto_Benefits 1.550.0 bump (7.0.1) | 2026-05-20 |
| #2705 | BT-72337/BT-72126 | BSCA_NewHireEnrollment — benefit_type ProperCase fix + lib 1.550.1 (7.0.1) | 2026-05-27 |
| #2730 | BT-72337/BT-72410 | BSCA_GroupSubmissions_MemberLevel — Gusto_Benefits 1.550.3 (v6.2.2) | 2026-05-28 merged, em Prod |

---

## PRs abertas — aguardando review

### PR #2733 — UHC_SamX_Renewal_Modern (fix original selectors)
- **Status: Open — aguardando review**
- Branch: `BT-73075-UHC-SamX-Renewal-close-icon-fix`
- Ticket: BT-73075

### PR #2737 — UHC_SamX_Renewal_Modern (Oscar — bump + clear skipTests)
- **Status: MERGED para develop** — build pós-merge FALHANDO
- Branch: `BT-73075-UHC-SamX-Renewal-fix-deployment-version` (mergeado)
- Erro: `check_version.sh Processes/.../SF_Updater` → "can't be upgraded from 1.14.2 to 1.14.2"
- Causa: branch sujo com histórico de SF_Updater; merge aconteceu antes do force-push limpo
- **PENDENTE:** decidir se bump SF_Updater 1.14.2→1.14.3 no develop para limpar check

### PR #2726 — CoveredCal_NewHireEnrollment_Modern
- **Status: Open — aguardando Oscar/Hari**
- Branch: `BT-72891-CoveredCal-NewHireEnrollment-effective-date-fix`
- Ticket: BT-72891

---

## BT-72272 — CoveredCal_Terminations (AGUARDANDO REVIEW)

### PRs abertas — merge order obrigatório
1. **PR #2741 — Library** `BT-72272-Gusto-Benefits-CoveredCal-SearchForGroup-fix` → aguardando review Oscar/Hari
2. **PR #2699 — Processo** `BT-72272-CoveredCal-Terminations-fix` → Buildkite passa após merge da #2741

### Estado do Staging (2026-06-02)
- Library `Gusto_Benefits 1.550.8` publicada no Staging Libraries feed ✅
- Processo `CoveredCal_Terminations 6.0.5` publicado no Staging ✅
- Release atualizado para 6.0.5 ✅

### Fixes entregues

#### Processo (v6.0.5, branch BT-72272-CoveredCal-Terminations-fix)
| Fix | Arquivo |
|---|---|
| Legacy→Windows migration, CloseAllApplications KillAllProcesses | `project.json`, `CloseAllApplications.xaml` |
| Remove inOpenEnrollment guard + detect Account Termination Notice (future effective date EE) | `CancelCoverage.xaml` |
| InterruptibleWhile (30s) para aguardar StepForPolicyYear ou dateTaken após date Next | `CancelCoverage.xaml` |
| Seleciona policy year correto quando StepForPolicyYear aparece (EE com políticas em múltiplos anos) | `CancelCoverage.xaml` |
| TimeoutMS dateTaken: 4s → 20s | `CancelCoverage.xaml` |
| NavigateTo URL_SearchEmployerPage antes de SearchForGroup (resolve SPA race condition) | `ProcessTransaction.xaml` |
| URL_SearchEmployerPage config key | `Data/config.json` |
| Gusto_Benefits 1.532.5 → 1.550.8 | `project.json` |

#### Library (v1.550.8, branch BT-72272-Gusto-Benefits-CoveredCal-SearchForGroup-fix)
| Fix | Detalhe |
|---|---|
| SearchForGroup: NavigateTo #/app/search-customer | Remove RefreshBrowser+Click (race condition Angular SPA) |
| TypeInto + Click 'search' movidos para dentro do BrowserScope | DOM fresco após navegação |
| dependencylock.json: 1.550.3 → 1.550.8 | Necessário para Buildkite do processo passar |

### Transações testadas no Staging
| Transaction ID | Empresa | EE | Cenário | Resultado |
|---|---|---|---|---|
| 500R700000zOlkDIAS | BBH Global, Inc. | Kate Sexton | Policy year único | ✅ Pass |
| 500R700000zN3WlIAK | Corridor Security Inc. | Scott Kahn + 3 deps | Multi-policy-year (StepForPolicyYear) | ✅ Pass |

### Slack enviado
- Canal `C0ANAPHL1NE` — @Oscar @Hari notificados sobre merge order (2026-06-02)
- Canal `C0ANAPHL1NE` — follow-up com BCBS como prioridade 1, CoveredCal como prioridade 2 (2026-06-02)

---

## BT-72297 — BCBS_TX/IL GroupSubmissions MemberLevel (AGUARDANDO REVIEW)

### PRs abertas (branches separadas por processo)
- **PR #2742 — BCBS_IL:** https://github.com/Gusto/biztech-uipath-rpa/pull/2742
  - Branch: `BT-72297-BCBS-IL-GroupSubmissions-no-updates-fix`
  - Processo: `BCBS_IL_GroupSubmissions_MemberLevel_Modern v2.1.2`
  - Staging: publicado ✅ (release 373891)
  - Testes: 5 transações IL com sucesso (a0mR700000EhSYsIAN, Ej977IAB, EhFuzIAF, EXleQIAT, EWT22IAH)
- **PR #2743 — BCBS_TX:** https://github.com/Gusto/biztech-uipath-rpa/pull/2743
  - Branch: `BT-72297-BCBS-TX-GroupSubmissions-no-updates-fix`
  - Processo: `BCBS_TX_GroupSubmissions_MemberLevel_Modern v2.1.3`
  - Staging: publicado ✅ (release 373892)
  - Testes: 1 transação TX com sucesso (a0mR700000Eb7SIIAZ)

### Fix
- Root cause: `portalPlan = Regex.Match(currentCoverage, " [A-Z]\d{3}[A-Z]{3}").Value`
  - Se regex falha → `portalPlan = ""` → `String.Contains("") = True` → skip silencioso
  - Também: dep add com plano igual era incorretamente ignorado
- Guards adicionados: `Not String.IsNullOrEmpty(portalPlan)` + `(dependentDetails Is Nothing OrElse dependentDetails.Length = 0)`
- Nota: itens testados são "Same Carrier, NO Plan Changes" (regressão) — itens com dep add/plan change pendentes de validação futura

---

## BT-71897 — BCBS TX GroupSubmissions NewPlan
- Branch: `BT-71897-BCBS-TX-GroupSubmissions-NewPlan`
- Status: **On Hold**

---

## Skills repo — atualizado 2026-05-21 (sessão 5)
- Repo: `Gusto-Dio/benops-rpa-skills` (privado) — v1.4.0
- Plugin instalado: `benops-rpa@benops-rpa-skills`
