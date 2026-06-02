# BenOps RPA — Notion Workspace

**Finalidade desta pasta:** continuidade de sessão Claude. Qualquer sessão nova pode ler estes arquivos e retomar o trabalho no Notion sem depender da memória da sessão anterior.

---

## O que é o BenOps RPA Hub

O Hub é a página central do time RPA BenOps no Notion. Criado para dar visibilidade operacional ao time (Sri, Oscar, Ahsen, Harinath) sobre o estado de cada processo automatizado — sem precisar entrar no Jira ou no GitHub.

**URL:** https://www.notion.so/35dad673c6c281ca9beed83cf58fdb22

### O que fica lá

| Componente | Função |
|---|---|
| Página Hub | Landing com timestamp do último sync |
| Processes DB | Uma linha por processo automatizado; status, PR vinculado, ticket Jira |
| Incidents DB | Registro histórico de bugs/incidentes para post-mortem e análise de padrão |

---

## Arquivos desta pasta

| Arquivo | Conteúdo |
|---|---|
| `workspace.md` | IDs do workspace, estrutura das databases, campos e valores aceitos |
| `skills.md` | Skills que interagem com o Notion — como funcionam, quando usar |
| `history.md` | O que foi construído, quando e em resposta a quê |
| `session-continuity.md` | O que uma sessão nova precisa saber para continuar o trabalho |

---

## Como retomar o trabalho

1. Ler `session-continuity.md` primeiro — estado atual e próximos passos
2. Ler `workspace.md` para ter os IDs e campos corretos
3. Rodar `/benops-sync` para ver o estado atual antes de fazer qualquer mudança
