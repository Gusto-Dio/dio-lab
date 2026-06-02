---
name: process-diary
description: "Diário vivo do processo de trabalho com Claude — como trabalhamos, ferramentas, padrões de diagnóstico, retrospectivas e backlog de melhorias"
metadata:
  node_type: memory
  type: project
  originSessionId: session-2026-06-02
---

# Diário de Processo — BizTech RPA com Claude

> Documento vivo. Atualizar a cada sessão significativa.
> Última atualização: 2026-06-02

---

## 1. Como trabalhamos

### Idiomas
- Conversa: Português (BR)
- Código, commits, branch names, PR titles/bodies, Jira comments, Slack: Inglês

### Fluxo padrão de ticket
1. Investigar — ler o Jira, checar git log, inspecionar o XAML e logs do Orchestrator
2. Formar hipótese de root cause → **apresentar ao usuário e aguardar confirmação** antes de implementar
3. Implementar na branch correta (nunca em `develop`)
4. Testar no Staging: copiar itens de Prod → rodar via Studio → documentar transaction IDs
5. Commit + verificar diff limpo vs develop
6. PR com descrição completa (changes, root cause, transações testadas)
7. Internal note no Jira (técnico) + comentário público (usuário) + Slack para reviewers

### Regras não-negociáveis
- `git branch` antes de qualquer edição de arquivo
- `uipath:uipath-rpa` skill invocada antes de qualquer edit em `.xaml`
- Nunca editar arquivos em `Libraries/` para corrigir bug de processo
- Validar hipótese com o usuário antes de implementar
- Diff limpo verificado (`git diff origin/develop..HEAD --name-only`) antes de push
- Merge develop antes de push se branch estiver atrás
- Branches separadas por processo quando dois processos são afetados pelo mesmo ticket
- Nunca oferecer para aprovar PRs — Diogenes sempre aprova manualmente

---

## 2. Tipos de tarefa recorrentes

| Tipo | Descrição | Frequência |
|---|---|---|
| **Windows migration** | Migrar processo Legacy → Windows (targetFramework, lib bumps, selectors) | Alta |
| **Portal bug fix** | Identificar e corrigir comportamento inesperado do portal via XAML | Alta |
| **Staging workflow** | Pack → upload nupkg → criar/atualizar release → copiar itens Prod→Staging → testar via Studio | Toda sessão de teste |
| **PR lifecycle** | Branch limpa → diff verificado → merge develop → push → PR com transações → Jira + Slack | Toda entrega |
| **Queue management** | Copiar itens de Prod para Staging via REST API para teste isolado | Frequente |
| **Diagnóstico de falha** | Ler erro do Orchestrator → inspecionar XAML → salvar HTML do portal → formar hipótese | Alta |
| **Comunicação** | Internal notes no Jira (técnico) + comentário público (usuário) + Slack para reviewers | Toda entrega |

---

## 3. Padrões de diagnóstico e fix

### 1. Diagnóstico top-down
Orchestrator log → exception type e message → localizar workflow → isolar atividade → hipótese de root cause → apresentar ao usuário antes de implementar.

### 2. Evidência do portal
Quando o erro é de interação com portal: salvar HTML via Chrome "Save page" → grep para IDs, textos e estrutura DOM real → comparar com selector atual no XAML.
- Python/urllib e curl são **bloqueados pelo Cloudflare WAF** — usar `Invoke-RestMethod` do PowerShell.

### 3. Regra do root cause
Nunca corrigir sintoma. `StepForPolicyYear` não era bug de timeout — era passo não tratado. `ErrorDuringDateSelection` não era falso positivo — era passo intermediário ausente.

### 4. Lógica robusta para portais lentos
Sempre preferir `InterruptibleWhile` com timeout generoso (20-30s) a `UiElementExists` com timeout fixo curto. Portais SPA (Angular) são lentos e imprevisíveis.

### 5. Isolamento de teste
Nunca testar em Prod diretamente. Copiar itens via REST API para Staging, rodar via Studio na branch do fix, documentar IDs das transações antes de abrir PR.

### 6. Buildkite-first
Antes de qualquer push: `git diff origin/develop..HEAD --name-only` para confirmar que o diff contém apenas os arquivos do ticket. Se sujo → `git merge origin/develop --no-edit` primeiro.

### 7. Library antes do processo
Se o processo depende de uma versão de library não mergeada em develop, a PR da library deve ser mergeada primeiro e o `dependencylock.json` atualizado — ou o Buildkite falha no processo PR com "Please upgrade".

---

## 4. Ferramentas e recursos

### Claude Skills

| Skill | Quando usar |
|---|---|
| `uipath:uipath-rpa` | Obrigatório antes de qualquer edit em `.xaml` |
| `uipath:uipath-platform` | Operações no Orchestrator (folders, releases, queues) |
| `superpowers:brainstorming` | Planejar algo novo antes de implementar |
| `superpowers:systematic-debugging` | Bot falhando inesperadamente em Prod |
| `benops-ticket-investigation` | Investigação completa de ticket antes de começar |
| `analyze` | Revisar diff da branch antes de commitar |
| `/morning` | Briefing diário: Slack + Jira + GitHub + contatos prioritários |
| `/followup` | Status update para leads |

### MCP Tools

| Tool | Uso |
|---|---|
| `mcp__claude_ai_Jira_Confluence__*` | Comentários, internal notes, transições de ticket |
| `mcp__claude_ai_Slack_Gusto_Offical__*` | Notificações ao time, mensagens para canal |
| `mcp__claude_ai_Github-Gusto__*` | Criar/atualizar PRs, listar branches |

### CLI e APIs

| Ferramenta | Uso | Observação |
|---|---|---|
| `uip rpa pack` | Gerar `.nupkg` | Usar `--skip-analyze` para warnings pré-existentes |
| `Invoke-RestMethod` (PowerShell) | Upload packages, criar releases, copiar queue items | **Único cliente que passa o Cloudflare WAF** |
| `git` | Branches, commits, merge, push | Nunca `--no-verify` |

### Orchestrator Staging — IDs fixos

| Recurso | ID / Valor |
|---|---|
| Folder `Benefits` (releases) | `48382` |
| Folder `Benefits/CarrierAutomation` (packages/queues) | `946022` |
| Tenant Staging ID | `324912ec-2ae5-4a97-984e-059b065b392c` |
| Tenant Production ID | `78c0c8e5-61bf-4ca9-9b71-61eb56059c45` |
| Jira cloudId | `3fd33630-4e39-4689-ad04-db32e3843117` |
| Slack canal do time | `C0ANAPHL1NE` |

### Endpoints REST Orchestrator confirmados

```powershell
# Upload package (folder 946022)
POST /odata/Processes/UiPath.Server.Configuration.OData.UploadPackage
-Form @{ file = Get-Item $nupkg }

# Criar release (folder 48382)
POST /odata/Releases
Body: { Name, ProcessKey, ProcessVersion }

# Atualizar release (folder 48382)
PATCH /odata/Releases(<id>)
Body: { ProcessVersion }

# Adicionar queue item
POST /odata/Queues/UiPathODataSvc.AddQueueItem
Body: { itemData: { Name, Priority, Reference, SpecificContent } }
```

---

## 5. Retrospectivas

### 2026-06-02 — Sessão longa (BT-72272 + BT-72297)

**Entregues:**
- BT-72272 CoveredCal_Terminations: PRs #2741 (Gusto_Benefits lib 1.550.8) + #2699 (processo 6.0.5)
  - Fixes: StepForPolicyYear (novo passo intermediário do portal), ErrorDuringDateSelection, future effective date EE, SearchForGroup SPA race condition
  - Testado: 2 transações Staging (policy year único + multi-policy-year)
- BT-72297 BCBS_IL/TX GroupSubmissions: PRs #2742 (IL v2.1.2) + #2743 (TX v2.1.3)
  - Fix: portalPlan regex silent skip + dep add guard
  - Testado: 5 transações IL + 1 transação TX

**Aprendizados técnicos:**
- Portais Angular SPA → sempre `InterruptibleWhile`, nunca timeout fixo
- `Invoke-RestMethod` é o único cliente que passa Cloudflare (Python/urllib bloqueado com erro 1010)
- Releases ficam no folder 48382 (Benefits), packages no 946022 (Benefits/CarrierAutomation)
- `dependencylock.json` exige match exato → library PR deve ser mergeada antes do processo PR
- Branches separadas por processo facilitam review independente

**O que funcionou bem:** diagnóstico via HTML do portal, isolamento via Staging antes de PR, comunicação clara no Jira + Slack com merge order explícito.

**O que pode melhorar:** dependência de itens manuais para testar cenários específicos (dep add, plan change) — sem automação de geração de dados de teste.

---

## 6. Backlog de melhorias

### Velocidade

| # | Melhoria | Impacto | Esforço | Status |
|---|---|---|---|---|
| V1 | **Script de Staging deploy** — pack + upload + update release em um comando parametrizado por processo | Alto | Médio | Pendente |
| V2 | **Script de cópia Prod→Staging** — parametrizado por queue name e quantidade, sem remontar a lógica toda sessão | Alto | Baixo | Pendente |
| V3 | **Hook git pré-push** — roda diff automaticamente e avisa se sujo antes do push | Médio | Baixo | Pendente |
| V4 | **Template de mensagem Slack** — para notificação de PR pronto, evitar redigir do zero | Baixo | Baixo | Pendente |

### Confiabilidade

| # | Melhoria | Impacto | Esforço | Status |
|---|---|---|---|---|
| C1 | **Verificação de token Staging** — checar expiração no início de sessões que envolvem Orchestrator, evitar 401 no meio do fluxo | Alto | Baixo | Pendente |
| C2 | **Banco de transações de referência** — itens de Prod com dep add e plan change salvos para teste quando fila estiver vazia | Alto | Médio | Pendente |
| C3 | **Validação de activity type antes de editar XAML** — grep automático antes de adicionar qualquer nova atividade | Médio | Baixo | Pendente |
| C4 | **Formalizar padrão HTML** — salvar HTML do portal e grep elementos como parte padrão do diagnóstico, não só quando conveniente | Médio | Baixo | Pendente |

### Rastreabilidade

| # | Melhoria | Impacto | Esforço | Status |
|---|---|---|---|---|
| R1 | **Retrospectiva automática** — ao encerrar sessão, gerar entrada no diário com PRs, transações e aprendizados | Alto | Médio | Pendente |
| R2 | **Links de PRs dependentes no Jira** — usar `createIssueLink` para marcar "blocks/is blocked by" entre library PR e processo PR | Médio | Baixo | Pendente |
| R3 | **Mapa de processos por carrier** — documento vivo: processo → library → queue → folder, para não redescobrir a cada sessão | Alto | Médio | Pendente |

### Prioridade imediata (baixo esforço, alto impacto)
1. **C1** — verificação de token (5 min, evita interrupções)
2. **V2** — script de cópia Prod→Staging (repetimos toda sessão)
3. **V1** — script de deploy Staging (3 passos manuais → 1 comando)
