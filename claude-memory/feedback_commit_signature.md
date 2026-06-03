---
name: feedback-commit-signature
description: Nunca incluir assinatura Co-Authored-By do Claude nos commits
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 98590504-4792-4a14-9557-738927f122f3
---

Nunca incluir a linha `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` nas mensagens de commit.

**Why:** O usuário não quer a assinatura do Claude nos commits do repositório.

**How to apply:** Em todos os commits, escrever apenas a mensagem de commit — sem nenhuma linha Co-Authored-By.
