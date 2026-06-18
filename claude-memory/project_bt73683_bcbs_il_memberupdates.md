---
name: project-bt73683-bcbs-il-memberupdates
description: "BT-73683 — BCBS_IL_MemberUpdates: assembly load failure Gusto_Benefits 1.551.0 not found"
metadata:
  node_type: memory
  type: project
  originSessionId: b5576bad-a6b7-4121-9f53-bb17d4e39699
---

## Root cause
Production was failing with `Could not load file or assembly 'Gusto_Benefits, Version=1.551.0.0'`. Version `1.551.0` was removed from the Orchestrator feed (superseded by `1.551.1`), leaving the deployed process unable to load the dependency at runtime.

Production had only `Gusto_Benefits 1.551.1` in the feed (folder 46023). Develop had `1.550.12`. The deployed version in Production (`5.13.5`) was compiled against `1.551.0` which no longer existed.

## Fix
- Bump `Gusto_Benefits` `1.550.12` → `1.551.1` in `project.json`
- Bump process version `5.13.12` → `5.13.13`

## Branch
`BT-73683-BCBS-IL-MemberUpdates-bump-Gusto-Benefits-1551`

## Status
- v5.13.13 committed and pushed
- 1 transaction tested in Staging (ID 2368762947, ref 500R7000010qfzUIAQ) — Successful
- PR #2804 aberta: https://github.com/Gusto/biztech-uipath-rpa/pull/2804
- Aguardando aprovação e merge + deploy em Produção

**Why:** Single transaction sufficient — fix is purely a lib bump with no logic changes; the test confirms the assembly loads and the process executes end-to-end.

**How to apply:** After merge, deploy to Production (folder 46023) and confirm the process picks up New items from the queue without the assembly error.
