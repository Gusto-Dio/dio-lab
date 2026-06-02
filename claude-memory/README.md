# Claude Memory — biztech-uipath-rpa

Memórias persistentes do Claude Code para o projeto `biztech-uipath-rpa`.

Este diretório é o backup versionado da memória local do Claude. Em caso de troca de máquina ou perda de dados locais, esses arquivos reconstroem o contexto completo de trabalho.

## Como funciona

Ao iniciar uma sessão no projeto `biztech-uipath-rpa`, o Claude lê automaticamente:
- `MEMORY.md` — índice de todas as memórias
- `work_state.md` — estado atual das PRs e trabalho em andamento

Os demais arquivos são carregados sob demanda conforme o contexto da sessão.

## Estrutura

| Prefixo | Tipo | Descrição |
|---|---|---|
| `MEMORY.md` | Índice | Ponto de entrada — lista todas as memórias |
| `work_state.md` | Projeto | PRs abertas, trabalho em andamento, pendências |
| `process_diary.md` | Projeto | Como trabalhamos, ferramentas, padrões, backlog de melhorias |
| `project_*.md` | Projeto | Contexto específico por ticket/iniciativa |
| `feedback_*.md` | Feedback | Regras aprendidas de sessões anteriores |
| `reference_*.md` | Referência | IDs, contatos, recursos externos |

## Atualização

Atualizar ao encerrar cada sessão significativa:
1. Editar os arquivos relevantes na memória local (`~/.claude/projects/.../memory/`)
2. Copiar para este diretório
3. Commit e push
