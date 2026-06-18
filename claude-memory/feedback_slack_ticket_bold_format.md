---
name: feedback-slack-ticket-bold-format
description: Formatação correta de negrito ao abrir tickets via slack_send_message tool
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b34f1999-1635-4a0d-b256-c45279f51c29
---

Ao usar `slack_send_message` para abrir tickets no canal C01CBJW8M16, usar `**texto**` (markdown padrão) para negrito — NÃO `*texto*` (que é itálico em markdown padrão, e resulta em texto sem negrito no Slack).

**Why:** A ferramenta converte markdown padrão (`**bold**`) para mrkdwn do Slack. Usar `*texto*` renderiza como itálico ou asteriscos literais, quebrando o formato esperado pelo bot de criação de tickets.

**How to apply:** Template correto para abertura de ticket:
```
<!subteam^S03UN81PXHA>
**Priority:** High
**Type**: Bug
**Impacted Automation**: `ProcessName`
**Issue**: descrição
**Impact**: impacto
**Recommendation/Asks**: recomendação
Thanks!
**Sent using** <@U0AG9LAAEAE|Slack MCP>
```

Nota: no template de referência (BT-73253), `**Priority:**` tem os dois pontos DENTRO do negrito; os demais campos têm os dois pontos FORA.
