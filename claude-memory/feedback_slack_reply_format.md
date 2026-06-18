---
name: feedback-slack-reply-format
description: Formato de replies conversacionais no Slack — sem markdown, texto corrido
metadata:
  node_type: memory
  type: feedback
  originSessionId: 98cb386a-7cc0-4add-a281-b68343701e7b
---

Replies conversacionais no Slack (perguntas, pedidos, follow-ups em threads) devem usar texto corrido, sem formatação markdown.

**Why:** O usuário ajustou o rascunho ao enviar — removeu todo o bold (`**texto**`), backticks em IDs, e exclamações desnecessárias. O estilo natural dele é mais direto e informal em threads.

**How to apply:** Exemplo confirmado (thread BT-73427, 2026-06-08):
```
Hi @Bri Boyer
We're working on the fix for this. The example order you shared (a0mR700000EanF5IAJ) is no longer available for testing, it appears the Carrier Order has been moved out of the Automation Queue in Salesforce. Could you point us to one or more Carrier Order IDs that currently show "Eligibility Audit- Open" on the UHC SAMx Renewal Dashboard?
We need them to validate the fix in Staging before deploying.
Thanks
```

Regras:
- Sem `**bold**` em replies de thread
- Sem backticks em IDs ou nomes de processo
- IDs entre parênteses simples: `(a0mR700000EanF5IAJ)`
- Sem "!" no fechamento — só "Thanks"
- @mention direto sem formatação especial
- Linha em branco entre parágrafos curtos

Contraste: o formato estruturado com `**Priority:**`, `**Impact:**` etc. é APENAS para abertura de tickets novos no canal (ver [[feedback-slack-ticket-bold-format]]).
