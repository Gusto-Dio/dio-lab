---
name: feedback-uip-rpa-pack
description: Requisitos e armadilhas do comando uip rpa pack para publicar processos no Orchestrator
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 10cf6326-1c47-409d-9346-c68f1038fed7
---

Para `uip rpa pack` funcionar, três condições são obrigatórias:

1. **Usar caminho absoluto** — caminho relativo duplica o path internamente e causa `DirectoryNotFoundException`.
2. **`project.uiproj` deve existir** — o packager exige esse arquivo além do `project.json`. Se não existir localmente, criar com conteúdo mínimo:
   ```json
   { "Name": "<ProjectName>", "ProjectType": "Process", "Description": "", "MainFile": "Main.xaml" }
   ```
3. **`description` no `project.json` não pode ser vazio** — NuGet manifest exige. Se estiver vazio, preencher antes de empacotar. A flag `--package-description` NÃO substitui o campo no JSON.

**Why:** Descoberto ao tentar publicar BCBS_MA_NewHireEnrollment 6.0.0 em 2026-05-12 — três falhas sequenciais antes de identificar as três causas.

**How to apply:** Sempre que usar `uip rpa pack`, verificar os três pontos acima antes de executar. Usar `--skip-analyze` para ignorar warnings pré-existentes do Workflow Analyzer sem bloquear o build.
