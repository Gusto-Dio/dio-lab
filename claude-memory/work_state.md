---
name: work-state-active-prs-in-progress-work-pendencias
description: "Estado atual de todas as PRs abertas, trabalho em andamento e próximos passos por ticket"
metadata: 
  node_type: memory
  type: project
  originSessionId: e63eaeb7-a294-498d-8d21-15aa2451fdd6
---

# Estado do trabalho — atualizado 2026-06-18 (PR #2803 BT-73633)

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
| #2762 | BT-73380 | BCBS_IL_Reconciliation — Gusto_Benefits 1.550.11 bump (v1.9.5) MFA email fix | 2026-06-08 |
| #2770 | BT-73383 | CoveredCal_NewHireEnrollment_Modern — Navigate to Employee Dashboard CV→DOM fix (v1.0.21) | 2026-06-08 |

---

## Em andamento

### BT-73371 — Anthem_GroupSubmissions_MemberLevel — Migração Legacy → Modern
- **Status: PR #2802 MERGED (2026-06-17)**
- PR: https://github.com/Gusto/biztech-uipath-rpa/pull/2802
- v1.0.3: Modern Windows, JSON config reader, arg fixes, config key renames
- Testado no Studio local sem erros

### BT-73387 — BSCA_NewHireEnrollment — Screenshot errada + mensagem vaga
- **Status: PR #2799 aberta — aguardando review**
- PR: https://github.com/Gusto/biztech-uipath-rpa/pull/2799
- Branch: `BT-73387-BSCA-NewHireEnrollment-screenshot-error-message-fix`
- Fix: TryCatch em torno de CompleteEnrollment intercepta "Portal exception", tira screenshot antes do reset, rethrow com mensagem específica de payroll report (v7.0.2)
- Testado no Staging: nova mensagem confirmada nos logs

### BT-73415 — BSCA_GroupSubmissions_MemberLevel — Edit Subscriber NClick fix
- **Status: PR #2798 aberta — aguardando aprovação**
- Branch: `BT-73415-BSCA-GroupSubmissions-MemberLevel-member-roster-fix`
- PR: https://github.com/Gusto/biztech-uipath-rpa/pull/2798
- Ticket: BT-73415 (In Progress)
- v6.2.8: Studio-captured `uix:NClick` (HardwareEvents) targeting `<span class="btnLabel">Edit Subscriber</span>` via `aaname`; NCheckState guard + RetryScope; VerifyOptions Disappears
- Bumped `Gusto_Benefits` 1.550.12 → 1.551.1 (fix assembly error)
- Publicado no Staging Orchestrator (v6.2.8); testado com sucesso no Studio debug
- PR description atualizada com nota explicando ausência de IDs (transações vêm da fila Salesforce)
- Revisores: oscarmiza, ahsennur, harinathreddy-m
- **Próximo:** merge + deploy Prod + monitorar execuções

---

## PRs abertas — aguardando review

### PR #2796 — Guardian PacketCollection v1.20.6 — portal error state check
- **Status: Open — Buildkite passou — aguardando review/merge**
- Branch: `BT-73457-Guardian-PacketCollection-gmail-imap-fix`
- Ticket: BT-73457 (reaberto para esse fix)
- Fix: `NCheckState` em dois pontos de `CollectPacket.xaml` — detecta "We're experiencing issues" e lança BRE
- Próximo: merge + monitorar execuções em Prod

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

## BT-73383 — CoveredCal_NewHireEnrollment_Modern — Navigate to Employee Dashboard fix (FECHADO 2026-06-08)
- PR #2770 mergeada, v1.0.21 em Produção ✅
- Fix: CV removido → DOM puro (SearchSteps=Selector); RetryScope 5x/5s adicionado
- Ticket encerrado pelo Diogenes

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

## BT-73253 / BT-73321 — UHC_SamX_GroupSubmissions_Renewal_Modern — FECHADO 2026-06-04
- PRs mergeadas: #2748 (v1.3.7), #2750 (v1.3.8), #2751 (v1.3.9)
- Rodando bem em Prod ✅
- Fix final: NCheckState CV → DOM selector em `Framework/InitEnvironment.xaml` (SAMx One menu)

---

## BT-73380 — BCBS_IL_Reconciliation — MFA email fix — FECHADO 2026-06-08
- PR #2762 mergeada e aprovada ✅
- **v1.9.5 em Produção** — Gusto_Benefits 1.550.11
- Fix: lib atualizada para versão enviada pelo Hari (resolve "File not found" no MFA email)

---

## BT-73427 — UHC_SamX_Renewal_Modern — Eligibility Audit check (FECHADO 2026-06-09)
- PR #2774 mergeada e aprovada ✅
- **v1.3.10 em Produção** — trigger reabilitada, monitorando
- Fix: `NCheckState` em `SearchForGroup.xaml`; BRE se "Eligibility Audit- Open" detectado
- Testado com Carrier Order `a0mR700000EMBG5IAP` (Group 1505610, MA) — único cenário disponível fornecido pela Bri
- **Validação Prod (job 501450556, 2026-06-09 19:38–21:18):** 22 grupos processados, todos com "Eligibility Audit- Open: not detected. Continuing" — nenhum BRE disparado; check funcionando corretamente ✅

---

## BT-73633 — BCBS_TX_GroupSubmissions_NewPlan — duplicate portal applications on retry
- **Status: PR #2803 aberta — aguardando review**
- Branch: `BT-73633-BCBS-TX-GroupSubmissions-NewPlan-fix-duplicate-retry`
- PR: https://github.com/Gusto/biztech-uipath-rpa/pull/2803
- v2.0.11: dois `SetTransactionProgress` checkpoints em `ProcessTransaction.xaml`; BRE thrown se retry detecta progresso anterior; Gusto_Benefits 1.550.12 → 1.551.1 (Buildkite fix)
- 3 transações testadas no Staging (v2.0.10): 2368642620 ✅, 2368657865 ✅, 2368658104 ✅; re-publicado como v2.0.11 com nova lib

## BT-73683 — BCBS_IL_MemberUpdates — assembly load failure
- **Status: PR #2804 aberta — aguardando review**
- Branch: `BT-73683-BCBS-IL-MemberUpdates-bump-Gusto-Benefits-1551`
- PR: https://github.com/Gusto/biztech-uipath-rpa/pull/2804
- v5.13.13: Gusto_Benefits 1.550.12 → 1.551.1 (1.551.0 removida do feed de Prod)
- 1 transação testada no Staging: 2368762947 (500R7000010qfzUIAQ) ✅

---

## BT-73296 — BCBS_TX_GroupSubmissions_NewPlan — invalid access code (ABERTO 2026-06-03)
- Status: **Aberto — aguardando triagem (Oscar deu ack)**
- Ticket: https://gustohq.atlassian.net/browse/BT-73296
- Slack thread: https://gustohq.slack.com/archives/C01CBJW8M16/p1780507142711899
- **100% fault rate desde 08/mai (26 dias)**
- Diagnóstico: bot loga com sucesso (`Credential_BCBS_TX`), BCBS exige access code → `GetAccessCode.xaml` lê Gmail via IMAP (`Credential_Gmail`) → obtém código → `LoginToBCBSTXIL.xaml` digita → BCBS rejeita (`ThrowInvalidCode`)
- PR #2720 (Oscar, 27/mai) aplicou fix `Activate=True + DelayBetweenKeys=200ms` mas falha persiste
- Versão em Prod: 2.0.4 / Gusto_Benefits 1.550.3 (em sync com develop)
- **Hipótese A:** regex em `GetAccessCode.xaml` (`[\s|\>](\d{4,})[\s|\<]` sobre HTMLBody) extrai número errado — formato do email BCBS pode ter mudado
- **Hipótese B:** `DelayBetweenKeys=200ms` ainda insuficiente para Production — testar 300–400ms
- Próximos passos: adicionar log de `accessToken` antes de digitar; ou testar delay maior em `LoginToBCBSTXIL.xaml`

---

## BT-71897 — BCBS TX GroupSubmissions NewPlan
- Status: **Done** (mergeado por Oscar v2.0.4 — substituído por BT-73296)

---

## Backlog de pendências técnicas

- **Anthem_NewHireEnrollment — waits entre páginas:** adicionar `WaitForReady` ou `UiElementExists` com retry em cada Invoke que transita de página (`EnterDependentsInformation.xaml` e outros). Risco de flapping em rede lenta. Retomar quando houver capacidade.

---

## Skills repo — atualizado 2026-05-21 (sessão 5)
- Repo: `Gusto-Dio/benops-rpa-skills` (privado) — v1.4.0
- Plugin instalado: `benops-rpa@benops-rpa-skills`
