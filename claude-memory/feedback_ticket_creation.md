---
name: feedback-ticket-creation
description: "Como criar tickets Jira corretamente — usar o canal Slack de suporte, não criar direto via API"
metadata:
  node_type: memory
  type: feedback
  originSessionId: session-2026-06-02
---

Criar tickets via Slack no canal de suporte (`C01CBJW8M16`), não diretamente via Jira API.

**Why:** O time tem um bot que cria tickets no padrão correto a partir de mensagens no canal. Criar direto via API pula esse fluxo e gera tickets fora do padrão, sem os campos obrigatórios preenchidos corretamente.

**How to apply:** Ao criar qualquer ticket novo, postar no canal `C01CBJW8M16` com o formato:

```
@platform-rpa-team
*Priority:* High/Medium/Low/Urgent
*Type:* Bug/Task/Story
*Impacted Automation:* NomeDoProcesso
*Issue:* Descrição breve do problema
*Impact:* O que está sendo impactado
*Recommendation/Asks:* O que precisa ser feito
Thanks!
```

O bot responde com o número do ticket criado (ex: "BT-XXXXX has been created").
