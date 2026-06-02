---
name: work-state-active-prs-in-progress-work-pendencias
description: "Estado atual de todas as PRs abertas, trabalho em andamento e próximos passos por ticket"
metadata: 
  node_type: memory
  type: project
  originSessionId: e63eaeb7-a294-498d-8d21-15aa2451fdd6
---

# Estado do trabalho — atualizado 2026-06-02 (sessão fim do dia)

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
| #2741 | BT-72272 | Gusto_Benefits 1.550.8 — SearchForGroup CoveredCal race condition fix | 2026-06-02 |
| #2699 | BT-72272 | CoveredCal_Terminations — Windows migration + StepForPolicyYear + future effective date fix (v6.0.5) | 2026-06-02 |
| #2742 | BT-72297 | BCBS_IL_GroupSubmissions_MemberLevel_Modern — portalPlan regex + dep add skip fix (v2.1.2) | 2026-06-02 |
| #2743 | BT-72297 | BCBS_TX_GroupSubmissions_MemberLevel_Modern — portalPlan regex + dep add skip fix (v2.1.3) | 2026-06-02 |
| #2744 | BT-72297 | BCBS_TX_GroupSubmissions_MemberLevel_Modern — UiPath.System.Activities 25.4.2→25.10.5 (v2.1.4) | 2026-06-02 |

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

## BT-72272 — CoveredCal_Terminations (FECHADO — 2026-06-02)

- PRs #2741 (lib 1.550.8) + #2699 (processo v6.0.5) mergiadas e pipeline passou ✅

---

## BT-72297 — BCBS_TX/IL GroupSubmissions MemberLevel

- PRs #2742 (IL v2.1.2), #2743 (TX v2.1.3), #2744 (TX v2.1.4) mergiadas em 2026-06-02 ✅
- Deploy para produção confirmado — pipeline passou com sucesso em v2.1.4
- Fix principal: portalPlan regex + dep add silent skip
- Fix deploy: UiPath.System.Activities [25.4.2]→[25.10.5] (RetryScope.LogRetriedExceptions)

---

## BT-73253 — UHC_SamX_GroupSubmissions_Renewal_Modern (NOVO)
- **Status: Scheduled — aguardando trabalho**
- Branch: `BT-73075-UHC-SamX-Renewal-debuggerapi-fix` (criada a partir do develop)
- Fix: `InteractionMode="DebuggerApi"` → `Simulate` em NClicks do `InitEnvironment.xaml` (linhas 150, 218, 233)
- Relacionado a: BT-73075 (seletores ProcessLayer) — tickets separados pois são bugs distintos
- HTML do portal UHC home page precisa ser avaliado para confirmar seletores CV ainda válidos

---

## BT-71897 — BCBS TX GroupSubmissions NewPlan
- Status: **Done** (mergeado por Oscar v2.0.4)
- Observação 2026-06-02: bot com dificuldade de login (invalid access code) em runs via trigger; job manual com retentativas passou. Login usa `LoginToBCBSTXIL` de dentro da `Gusto_Benefits` (não da `Gusto_Benefits_BCBS-TX-IL`). DM enviado para Oscar perguntando se ele já está vendo e se quer apoio.

---

## Backlog de pendências técnicas

- **Anthem_NewHireEnrollment — waits entre páginas:** adicionar `WaitForReady` ou `UiElementExists` com retry em cada Invoke que transita de página (`EnterDependentsInformation.xaml` e outros). Risco de flapping em rede lenta. Retomar quando houver capacidade.

---

## Skills repo — atualizado 2026-05-21 (sessão 5)
- Repo: `Gusto-Dio/benops-rpa-skills` (privado) — v1.4.0
- Plugin instalado: `benops-rpa@benops-rpa-skills`
