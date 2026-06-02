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

## Jira MCP — cloudId

Usar `gustohq.atlassian.net` como cloudId (site URL, não UUID). UUID também funciona: `3fd33630-4e39-4689-ad04-db32e3843117`.

`gusto.atlassian.net` e `gusto` falham (404/invalid domain).

**Why:** Confirmado em 2026-05-21 via `getAccessibleAtlassianResources` — retornou `url: "https://gustohq.atlassian.net"`.

**How to apply:** Sempre passar `gustohq.atlassian.net` como cloudId nas chamadas Jira MCP.
