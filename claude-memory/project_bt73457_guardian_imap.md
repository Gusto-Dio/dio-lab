---
name: project-bt73457-guardian-imap
description: "BT-73457 — Advising_Guardian_PacketCollection IMAP fix: PR #2784 aberta, aguardando review"
metadata:
  node_type: memory
  type: project
  originSessionId: 111d482b-7065-42b9-819d-2780a6f04cbf
---

# BT-73457 — Guardian PacketCollection Gmail IMAP fix

**Branch:** `BT-73457-Guardian-PacketCollection-gmail-imap-fix`
**Ticket:** https://gustohq.atlassian.net/browse/BT-73457
**PR:** https://github.com/Gusto/biztech-uipath-rpa/pull/2784 — **Open, aguardando review**
**Versão final:** `1.20.5`

---

## Status (2026-06-11)

**PR #2784 aberta** — 5 transações testadas end-to-end no Staging com sucesso.

---

## Descoberta crítica — código Prod ≠ código git

O `develop` tinha versão `1.19.18 Legacy` (último commit: BT-70746, Oscar, 05/mar/2026).
**Prod estava em `1.20.0 Windows`** — publicado em 17/abr/2026 diretamente do Studio, sem PR/commit no repo.
A branch foi baseada no código de Prod (1.20.0), não no develop.

---

## Fixes implementados (v1.20.1 → v1.20.5)

### GetAccessCode.xaml — 3 InvokeCodes (Option B)
InvokeCode monolítico (120s) substituído por:
1. **InvokeCode_Connect** — Connect + auth + open folder. Outputs: `imapClient As Object`, `imapFolder As Object`.
2. **InvokeCode_Search** — Busca 60s, `SearchQuery.NotSeen`. Inputs: `imapClient`, `imapFolder`, `wbStartTime`. Output: `out_AccessCode`.
3. **InvokeCode_Disconnect** — Disconnect + dispose. Input: `imapClient`.

### LoginToGuardian.xaml — retry loop + asset configurável
- Loop `While retryCount < maxCodeRetries And IsNullOrWhiteSpace(accessCode)` (era hardcoded 5)
- Cada tentativa vazia → clica "Send again" → espera 10s → próxima tentativa
- Se após N tentativas ainda vazio → Throw
- `GetRobotAsset "Asset_Guardian_MaxCodeRetries"` (TryCatch, fallback 5) → `maxCodeRetries`
- Asset criado no Staging; criar em Prod antes do deploy

### CollectPacket.xaml — selector groupID
- `id='groupId'` → `id='groupID'` em 3 ocorrências (linhas 381, 409, 486)
- Bug estava mascarado pela falha de IMAP — nunca chegava nessa tela antes
- Adicionado `UiElementExists` wait antes do NClick "Renewal Package" H2
- `WaitForReadyArgument` None → Interactive no NClick "Renewal Package"

### ProcessTransaction.xaml — portal navigation retry (3 camadas)
1. Session check (`UiElementExists`) → re-login via `InitAllApplications` se sessão perdida
2. `RetryScope` 6×/6s — Home menu com `NCheckState` + refresh se não encontrado
3. `RetryScope` 6×/6s — Renewal package link com `NCheckState` + refresh se não encontrado
- SFDC upload retry: `RetryScope` 10×/30s com jitter (5–15s) para evitar colisão entre bots

---

## Testes Staging (v1.20.5 — 2026-06-11)

Todos os 5 grupos do John Falk testados com sucesso:

| Queue Item ID | Group | Empresa | Resultado |
|---|---|---|---|
| 2347408729 | 70010 | Global Deals LLC | ✅ Pass |
| 2347408739 | 577144 | Humaning Inc | ✅ Pass |
| 2347408747 | 40366 | Haddy, inc. | ✅ Pass |
| 2347408759 | 86643 | GL Lending LLC | ✅ Pass |
| 2347408768 | 85600 | Manhattan Strategies LLC | ✅ Pass |

Fila Staging: https://cloud.uipath.com/gustoinc/Staging/orchestrator_/queues/5892/transactions

---

## Assets do processo

- `Credential_Guardian` (portal login)
- `Credential_Gmail` (IMAP — crítica para o fix)
- `Credential_SalesforceInstance`, `Credential_SalesforceKey`, `Credential_SalesforceUser`
- **`Asset_Guardian_MaxCodeRetries`** — NOVO — criado no Staging; **criar em Prod antes do deploy**

---

## Staging Orchestrator

- Release Id `9199` — em v1.20.5
- Pasta packages: folder `946022` (Benefits/CarrierAutomation)
- Pasta releases: folder `48382` (Benefits)
- Fila: `Guardian_Packets` (ID 5892)

---

## Status pós-merge (2026-06-15)

- PR #2784 merged, v1.20.5 em Prod ✅
- Ticket BT-73457 fechado ✅
- **Novo problema em Prod:** quando group number é inválido, bot retenta incessantemente → SystemException → re-login → grande demora no processamento da fila

## Fix v1.20.6 — Portal error state check (NCheckState)

**Branch:** `BT-73457-Guardian-PacketCollection-gmail-imap-fix` (reutilizada)
**PR:** https://github.com/Gusto/biztech-uipath-rpa/pull/2796 — **Aberta, Buildkite passou**
**Arquivo:** `ProcessLayer/CollectPacket.xaml`
**Versão:** `1.20.6` (project.json bumpado)

**Mudanças:**
- Adicionado `NCheckState` "Check App State Page Error" em dois pontos de `CollectPacket.xaml`:
  1. Início do inner while loop "Search group Wait for portal response" — antes do TypeInto
  2. Dentro do recovery path "If Invalid group ID" → NApplicationCard → antes do TypeInto
- Selector: `<webctrl parentid='pageContainer' tag='DIV' innertext='*We*experiencing issues*' />`
- Timeout: 30s, WaitForReady=None
- Se detectado: Log Info + `BusinessRuleException("System unavailable: We're experiencing issues, and we're working to fix the problem")`

**Contexto:** usuário do ticket reportou que o erro "We're experiencing issues" aparecia no portal Guardian. Ao investigar, confirmou que pode ter sido temporário (Guardian estava fazendo manutenção). O fix garante que se o erro aparecer novamente, o bot para imediatamente com mensagem clara em vez de falhar silenciosamente.

**Status (2026-06-15):** PR #2796 aberta, Buildkite passou. Aguardando merge e monitoramento das próximas execuções em Prod.
