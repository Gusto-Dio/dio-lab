---
name: project-bt73415-bsca-member-roster
description: "BT-73415 — BSCA_GroupSubmissions_MemberLevel — PR #2792 aberta, v6.2.6, aguardando review e merge"
metadata:
  node_type: memory
  type: project
  originSessionId: 111d482b-7065-42b9-819d-2780a6f04cbf
---

# BT-73415 — BSCA_GroupSubmissions_MemberLevel — Edit Subscriber fix

**Branch:** `BT-73415-BSCA-GroupSubmissions-MemberLevel-member-roster-fix`
**Ticket:** https://gustohq.atlassian.net/browse/BT-73415
**PR:** https://github.com/Gusto/biztech-uipath-rpa/pull/2792
**Versão:** `6.2.7`

---

## Status (2026-06-15)

- PR #2792 (v6.2.6, SendWindowMessages) foi mergeada para develop e deployada em Prod → **falhou em Prod 2026-06-13**
- v6.2.7 (uix:NClick HardwareEvents + NApplicationCard wrapper) publicado no Staging via CLI — testado 2026-06-15
- **v6.2.7 falhou no Staging**: botão Edit Subscriber visível na tela, bot não clicou. Job 504941132 cancelado.
- **Hipótese principal:** NCheckState retornando `false` (seletor/Guid não bate) → IfExists nunca executa. GUIDs artificiais no NApplicationCard podem causar falha de attach silenciosa.
- **BLOQUEADO**: sem itens na fila do Staging para testar. Retornar quando houver novos itens.

## Próxima abordagem — v6.2.8
1. Remover `NApplicationCard` wrapper (adicionado artificialmente, GUIDs não validados pelo Studio)
2. Adicionar `InvokeCode` antes do click: `document.querySelector('[title="Edit Subscriber"]').scrollIntoView({block:'center',inline:'center'})`
3. Usar `ui:Click SimulateClick=False, SendWindowMessages=False` (hardware events → isTrusted=true)

Racional: scrollIntoView resolve o off-screen (x=2835 > 1920px viewport), e hardware click gera isTrusted=true que o portal Salesforce LWC exige.

---

## Root cause

`Click 'Edit Subscriber'` em `UpdateEmployeeMedicalBenefits.xaml`. Botão renderiza em x=2835 na tabela do portal BSCA (mais membros → tabela mais larga que 1920px do robot). SendWindowMessages enviava WM para coordenadas off-screen; Chrome não roteava para DOM → form nunca abria. Em Staging funciona porque test data renderiza o botão dentro do viewport.

**Fix v6.2.7:** Substituído `ui:Click (SendWindowMessages=True)` por `uix:NClick (InteractionMode=HardwareEvents)`. Modern activity auto-faz scroll-into-view antes do clique hardware. Também gera isTrusted=true (exigido pelo portal Salesforce LWC da BSCA).

**Tentativas anteriores:**
- v6.2.3: hardware click → "outside of screen bounds"
- v6.2.4: SimulateClick=True → isTrusted=false → portal rejeita (form nunca abre)
- v6.2.5/v6.2.6: SendWindowMessages=True → click silencioso off-screen → form nunca abre

---

## Arquivos modificados (v6.2.6)

| Arquivo | Mudança |
|---|---|
| `UpdateEmployeeMedicalBenefits.xaml` | SendWindowMessages=True + NCheckState guards + LogMessages |
| `UpdateEmployeeDetails.xaml` | SimulateClick=True em Member Roster + LogMessages + Sequence wrapper em If.Then |
| `UpdateCoverage.xaml` | NCheckState Plan Selection + LogMessages |
| `AddDependent.xaml` | LogMessages |
| `project.json` | v6.2.6 |

**Nota XAML:** `If.Then` aceita apenas uma Activity. Quando o subagent adicionou LogMessage_7 como segundo filho direto do `If.Then` (bloco `If portalError`), causou erro WF `'Then' property has already been set on 'If'`. Fix: envolver `Click 'ok' + LogMessage_7` numa `<Sequence>`.

---

## Staging validado

Job 503573098, 2026-06-12. 2 transações UpdateEmployeeDetails com sucesso. Transactions via Salesforce SOQL — sem IDs estáticos.

---

## Pós-merge

- Re-habilitar trigger em Prod: Orchestrator Prod, folder 46023 (Benefits), Release 12994
