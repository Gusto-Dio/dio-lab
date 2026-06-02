---
name: project-bt72272-coveredcal-terminations
description: "BT-72272 — CoveredCal_Terminations, bug Can't terminate employee para EE com future effective date, Windows migration, SearchForGroup race condition Angular SPA"
metadata:
  node_type: memory
  type: project
  originSessionId: e63eaeb7-a294-498d-8d21-15aa2451fdd6
---

# BT-72272 — CoveredCal_Terminations

**Status:** In Progress | **Assignee:** Diógenes Ribeiro
**Reporter:** Tammy Borders

---

## O Bug Original

Bot falhava com "Can't terminate employee" para EEs com **future effective date** — o portal CoveredCal já tem a terminação agendada (mostra "Account Termination Notice"), o botão "Update Enrollment" não aparece, e o bot jogava BRE antes de tentar terminar.

**Causa:** `CancelCoverage.xaml` checava o botão "Update Enrollment" e jogava BRE se não encontrava, sem considerar que para EEs com terminação já agendada o fluxo é diferente.

---

## Processo

**Caminho:** `Processes/Benefits/CarrierAutomations/MemberSubmission/CoveredCal/CoveredCal_Terminations/`
**Versão Prod:** 5.8.2 (Legacy) | **Versão em dev:** 6.0.4 (Windows)
**Queue:** `CoveredCal_Terminations` (Prod folder 46023, Staging folder 48382 queue ID 22318)

---

## Branches

- **Processo:** `BT-72272-CoveredCal-Terminations-fix` — 65+ commits à frente do origin, **precisa push**
- **Library:** `BT-72272-Gusto-Benefits-CoveredCal-SearchForGroup-fix` — 4+ commits à frente do origin, **precisa push**

---

## Fixes no Processo (CancelCoverage.xaml)

1. **Remove `inOpenEnrollment` guard** (Edit Application button check) — primeiro fix original
2. **Detect pre-existing Account Termination Notice** (fix future effective date EE):
   - Antes do check de Update Enrollment, faz `GetAttribute relativeVisibility` do H4 "Account Termination Notice"
   - Se visível → pula fluxo de terminação inteiro, vai direto para screenshot
   - Se NÃO visível E NÃO tem Update Enrollment → throw "Can't terminate employee"
   - Selector: `<html app='chrome.exe' /><webctrl tag='H4' aaname='*Account Termination Notice ' />`

## Fix no Processo (ProcessTransaction.xaml)

- `NavigateTo` antes de chamar `gcg:SearchForGroup` navega para `in_Config("URL_SearchEmployerPage")` em vez de dashboard-broker
- Config key: `URL_SearchEmployerPage = https://myccsb.com/marketplace/#/app/search-customer`

## Fix na Library Gusto_Benefits (SearchForGroup.xaml)

**Problema raiz:** Library 1.532.5 era Legacy — SearchForGroup funcionava. Library 1.550.x é Windows — SearchForGroup falhava com "UiElement is no longer valid" ao tentar clicar "Search Employer" após RefreshBrowser. Angular SPA reconstrói o DOM e a referência fica stale.

**Histórico de tentativas:**
- 1.550.4: WaitForReady="COMPLETE" no Click → não resolveu
- 1.550.5: DelayBefore=3000 no Click → não resolveu  
- 1.550.6: InterruptibleWhile wait loop → não resolveu de forma confiável
- **1.550.7: NavigateTo `#/app/search-customer`** — removeu RefreshBrowser+Click, navega direto para a página de busca → **navegação funciona!**

**Problema atual com 1.550.7:** O TypeInto 'Customer Account Number' e Click 'search' estão FORA do BrowserScope. Após o BrowserScope(NavigateTo) fechar, o Angular ainda está renderizando. TypeInto falha com "UiElement is no longer valid".

**Próximo fix — Library 1.550.8:**
- Mover `TypeInto` e `Click 'search'` para DENTRO do BrowserScope
- Selectors:
  - TypeInto: `<html ... title='Benefits Marketplace | marketplace' /><webctrl id='CustomerID' tag='INPUT' />`
  - Click search: `<html ... title='Benefits Marketplace | marketplace' /><webctrl id='se*' tag='BUTTON' />`
- DelayBefore do TypeInto pode ser mantido em 1500ms (dentro do BrowserScope terá referência fresca)

---

## Estado do Staging (2026-05-29)

- Library `Gusto_Benefits 1.550.7` ✅ no Staging Libraries feed
- Processo `CoveredCal_Terminations 6.0.4` ✅ publicado
- Release: 6.0.4 ✅
- Item na fila: `2284029159` (Group 712702, TermDate 2026-05-30) — New

---

## NuGet cache local (importante para pack)

Para pack do processo funcionar com Library 1.550.x, o nupkg precisa estar em:
`C:\Users\diogenesribei_gsto\.nuget\packages\gusto_benefits\1.550.X\`

Estrutura necessária: `.nupkg.metadata`, `.nupkg.sha512`, `.nuspec`, `lib/`, `content/`, `contentFiles/`, e o `.nupkg` file.

Para 1.550.8: copiar estrutura da 1.550.7 e substituir com o novo nupkg + extrair lib/ correto do nupkg.

---

## Tickets relacionados

- **BT-68821** — mesmo bug, referenciado por Tammy no ticket
- **BT-72272** — ticket ativo
