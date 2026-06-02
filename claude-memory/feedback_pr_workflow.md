---
name: feedback-pr-workflow
description: "Como Diogenes quer que PRs sejam tratadas — aprovação, review e interação com GitHub"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bf18a2f4-58ae-41e8-8c70-da1004a29386
---

Nunca oferecer para aprovar PRs — Diogenes sempre aprova manualmente.

**Why:** É preferência explícita do usuário. Aprovar PR é uma ação irreversível e visível para o time — deve ser sempre uma decisão humana.

**How to apply:** Ao concluir um review, encerrar com os achados e próximos passos. Não perguntar "vou aprovar?" nem oferecer para submeter o review pelo GitHub. O usuário faz isso por conta própria.

---

PR description e título SEMPRE em inglês — sem exceção.

**Why:** PR #2699 teve descrição escrita em português por engano — gerou constrangimento e exigiu correção pública com comentário explicativo.

**How to apply:** Antes de criar ou atualizar qualquer PR via GitHub MCP, verificar que title e body estão 100% em inglês. Termos técnicos (nomes de atividades, variáveis, config keys) permanecem em inglês naturalmente. A regra já existe no CLAUDE.md mas precisa ser reforçada como feedback crítico.
