---
name: feedback-orchestrator-library-publish
description: Publicar biblioteca Gusto_Benefits no Orchestrator exige Studio — CLI tem 403 no Libraries feed
metadata:
  node_type: memory
  type: feedback
  originSessionId: 699252c5-0dfb-4bbb-8fc4-1eb59b9e3428
---

Nunca tentar publicar bibliotecas UiPath no Orchestrator via `uip or packages upload` — vai para o feed errado.

**Why:** `uip or packages upload` sem `--feed-id` envia para o **Processes feed** (correto para processos, errado para libs). Com `--feed-id <libraries-feed-id>` retorna 403 Forbidden. O robot busca dependências de biblioteca no **Libraries feed** — se não encontrar a versão exata, usa a mais recente disponível sem erro visível. Descoberto em BT-72337 em 2026-05-19.

**How to apply:**
- Para publicar **bibliotecas** via CLI (método confirmado em 2026-05-19):
  1. Pack: `uip rpa pack "<project-dir>" "<output-dir>" --skip-analyze --format json`
  2. Upload via REST API (funciona, ao contrário do `uip or packages upload`):
     ```bash
     ACCESS_TOKEN=$(grep UIPATH_ACCESS_TOKEN ~/.uipath/.auth | cut -d= -f2-)
     curl -X POST "https://cloud.uipath.com/abf7bd92-ded9-4aa2-aff0-05d621da9180/Staging/orchestrator_/odata/Libraries/UiPath.Server.Configuration.OData.UploadPackage" \
       -H "Authorization: Bearer $ACCESS_TOKEN" \
       -H "X-UIPATH-TenantName: Staging" \
       -F "file=@<path-to.nupkg>"
     ```
  3. Confirmar upload: `curl -s ".../odata/Libraries?...top=10&orderby=Version desc" | grep Gusto_Benefits`
- Para publicar **processos**: `uip or packages upload <file.nupkg>` funciona (vai para Processes feed, que é o correto)
- Studio ainda é alternativa válida: Design → Publish → selecionar tenant correto
- Se suspeitar que robot está rodando lib errada: verificar stack trace — se mostrar atividade do código antigo (ex: `InterruptibleDoWhile` em vez de `RetryScope`), é lib desatualizada

## IDs dos feeds no Staging (gustoinc/Staging)

| Feed | ID |
|---|---|
| Processes | `53879387-6e9b-452f-89c9-68a210e60b84` |
| Libraries | `44c65672-bef9-4f33-8043-034f45b3da31` |
| Personal Workspace | `e2cf8746-beae-4c2f-b23f-aa8088c46e4f` |

NuGet push URL do Libraries feed (para referência futura):
`https://cloud.uipath.com/abf7bd92-ded9-4aa2-aff0-05d621da9180/Staging/orchestrator_/nuget/v3/44c65672bef94f338043034f45b3da31/packages/`
