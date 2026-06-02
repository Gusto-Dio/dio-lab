---
name: feedback-buildkite-branch-behind-develop
description: "Buildkite usa git diff origin/develop..HEAD — branch atrás do develop inclui processos não relacionados no diff, causando falhas no check_dependency.sh"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 46927386-82ed-4fa1-946a-18d42e326071
---

Antes de abrir qualquer PR, sempre fazer merge do develop na branch para evitar falhas falsas no Buildkite.

**Why:** O pipeline `.buildkite/pipeline.sh` usa `git diff origin/develop..HEAD --name-only` (dois pontos) para identificar quais projetos checar. A diferença crítica:
- `..` (dois pontos) — diff direto entre os dois commits: inclui tudo que é diferente entre `develop` e `HEAD`, incluindo o que o develop recebeu após a criação da branch
- `...` (três pontos) — diff desde o ponto de divergência: mostra só o que foi modificado na branch

Com `..`, se outros PRs foram mergeados no develop depois que a branch foi criada, esses processos aparecem no diff. O `check_dependency.sh` roda para cada um e falha nos que não foram atualizados para a versão atual da lib. Confirmado em BT-72337 em 2026-05-19.

**How to apply — 4 passos em ordem (validado em BT-73029, 2026-05-27 — zero falhas no Buildkite):**

1. **Stage explícito por arquivo** — nunca `git add .` ou `git add -A`:
   ```powershell
   git add "Processes/Carrier/Process/File.xaml" "Processes/Carrier/Process/project.json" ...
   git status --short  # confirmar que nenhum arquivo fora do escopo está staged
   ```

2. **Checar diff antes do push:**
   ```powershell
   git fetch origin develop
   git diff origin/develop..HEAD --name-only
   ```

3. **Se aparecer arquivo fora do escopo → merge develop:**
   ```powershell
   git merge origin/develop --no-edit
   # Resolver conflitos nos arquivos intencionalmente modificados com --ours
   git add <arquivos-conflitados> && git commit
   ```

4. **Verificar diff novamente após o merge, só então push:**
   ```powershell
   git diff origin/develop..HEAD --name-only
   # Deve mostrar APENAS os arquivos do ticket
   git push
   ```

**Regra do dependencylock:** Manter versão atual da lib mesmo após merge — resolver conflito com `--ours`. Sem o lock atualizado, o robot pode usar versão antiga em produção.
