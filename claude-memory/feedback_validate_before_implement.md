---
name: feedback-validate-before-implement
description: Sempre apresentar análise e tese ao usuário para confirmação antes de qualquer implementação — nunca assumir que a análise está certa e implementar direto
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 699252c5-0dfb-4bbb-8fc4-1eb59b9e3428
---

Nunca implementar direto após análise, mesmo que a lógica pareça sólida.

**Why:** Diogenes pediu explicitamente "não faça nenhum ajuste ainda, analise bem" (erro auraErrorBox) e reforçou "valide a tese antes de implementação" (erro RetryScope 1.549.0). Implementar sem validação é assumir que a análise está certa — e já erramos mais de uma vez por isso neste ticket.

**How to apply:** Após qualquer análise de bug ou lógica:
1. Apresentar a tese ao usuário: "Root cause é X porque Y — posso implementar?"
2. Aguardar confirmação explícita
3. Só então implementar
Sem exceções, mesmo que o raciocínio pareça óbvio.
