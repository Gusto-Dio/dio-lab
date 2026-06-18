---
name: feedback-orchestrator-api
description: "Quirks e sintaxe correta para queries OData na API do Orchestrator (RobotLogs, Jobs)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 10cf6326-1c47-409d-9346-c68f1038fed7
---

## OData GUID filter — RobotLogs

Para filtrar `RobotLogs` por `JobKey` (campo Edm.Guid), usar o GUID sem aspas e sem prefixo `guid`:

```
$filter=JobKey eq 26e7b255-2834-4d6b-878f-c4914887fbdc
```

- `guid'...'` → erro: "Unrecognized Edm.String literal"
- `'...'` (com aspas) → erro: "incompatible types Edm.Guid and Edm.String"
- Sem aspas → funciona

**Why:** Descoberto ao investigar BT-72124 em 2026-05-12. O campo `JobKey` é Edm.Guid internamente, mas a sintaxe OData v4 para GUID não usa prefixo nem aspas.

**How to apply:** Sempre que filtrar RobotLogs por JobKey, usar o GUID bare.

---

## Orchestrator REST API — headers e folder IDs (Staging)

Usar `Invoke-RestMethod` do PowerShell — Python/urllib e `curl` são bloqueados pelo Cloudflare WAF (erro 1010).

**Header correto:** `X-UIPATH-OrganizationUnitId: <ID_NUMÉRICO>` — não usar `X-UIPATH-OrganizationUnitKey` (GUID).

**Tenant correto para Staging:** `uip login tenant set "Staging"` — tenant ID `324912ec-2ae5-4a97-984e-059b065b392c`. Base URL: `https://cloud.uipath.com/gustoinc/Staging`. NUNCA usar o tenant Production para publicar em Staging.

**Folder IDs Staging:**
- `48382` — pasta `Benefits` (onde ficam as **releases** de CoveredCal, BCBS, etc.)
- `946022` — pasta `Benefits/CarrierAutomation` (onde ficam os **packages** e **queues**)

**Endpoints confirmados:**
- Upload package: `POST /odata/Processes/UiPath.Server.Configuration.OData.UploadPackage` com `-Form @{ file = Get-Item $nupkg }` (folder 946022)
- Criar release: `POST /odata/Releases` com `{ Name, ProcessKey, ProcessVersion }` (folder 48382)
- Atualizar release: `PATCH /odata/Releases(<id>)` com `{ ProcessVersion }` (folder 48382)
- Adicionar queue item: `POST /odata/Queues/UiPathODataSvc.AddQueueItem` (folder da queue)

**Why:** Descoberto em 2026-06-02 ao publicar CoveredCal_Terminations e BCBS_IL/TX no Staging.

**How to apply:** Sempre usar Invoke-RestMethod, header numérico, e verificar qual folder (48382 releases vs 946022 packages).

---

## Reconciliation queues — folder correto (Prod e Staging)

As queues de Reconciliation (`BCBS_IL_Reconciliation`, `BCBS_TX_Reconciliation`, `Kaiser_Reconciliation`, etc.) ficam na pasta **Benefits**, NÃO em Benefits/CarrierAutomation.

**Folder IDs Production:**
- `46023` — Benefits (queues de Reconciliation ficam aqui)
- `944168` — Benefits/CarrierAutomation (outros processos)

**Folder IDs Staging:**
- `48382` — Benefits (queues de Reconciliation ficam aqui)
- `946022` — Benefits/CarrierAutomation (outros processos)

**Why:** Descoberto em 2026-06-05 ao buscar BCBS_IL_Reconciliation — a queue não aparece em CarrierAutomation, apenas em Benefits.

**How to apply:** Ao manipular QueueItems de Reconciliation, sempre usar o folder Benefits (46023/48382), não CarrierAutomation.

---

## QueueItems OData — Reference vs Key

O "transaction ID" que aparece nos logs e na UI do Orchestrator é o campo **Reference**, não o **Key**.

- `Key` (Edm.Guid) = identificador interno do item na queue
- `Reference` (Edm.String) = identificador de negócio, visível na UI

**Filtro correto por Reference:** `$filter=Reference eq '4dc61b59-63f8-40ff-a797-468c90f2d382'`

**Busca alternativa quando só tem o Reference:** filtrar por `QueueDefinitionId eq <id>` + `$orderby=Id desc` e comparar `Reference` na lista retornada.

**Why:** Em 2026-06-05, tentei filtrar por `Key eq <guid>` com o GUID fornecido pelo usuário — retornou 0 resultados sem erro. O GUID era o campo `Reference`. Bare GUID no filtro de Key retorna 0 silenciosamente (não lança erro).

**How to apply:** Quando o usuário fornecer um transaction GUID do Orchestrator, assumir que é o `Reference`. Filtrar por Reference com aspas simples.

---

## Jira MCP — cloudId

Usar `gustohq.atlassian.net` como cloudId (site URL, não UUID). UUID também funciona: `3fd33630-4e39-4689-ad04-db32e3843117`.

`gusto.atlassian.net` e `gusto` falham (404/invalid domain).

**Why:** Confirmado em 2026-05-21 via `getAccessibleAtlassianResources` — retornou `url: "https://gustohq.atlassian.net"`.

**How to apply:** Sempre passar `gustohq.atlassian.net` como cloudId nas chamadas Jira MCP.
