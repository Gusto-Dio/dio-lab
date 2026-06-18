---
name: project-bt73633-bcbs-tx-duplicate-retry
description: "BT-73633 — BCBS_TX_GroupSubmissions_NewPlan: duplicate portal applications on retry"
metadata: 
  node_type: memory
  type: project
  originSessionId: b5576bad-a6b7-4121-9f53-bb17d4e39699
---

## Root cause
`The UiElement is no longer valid` in `EnrollEmployee.xaml` is a SystemException → Catch sets `SetTransactionStatus ErrorType="Application"` → REFramework retries → `ProcessTransaction` restarts from the beginning → `NavigateToNewPlans` + `EnterCompanyInfo` create a NEW portal application → duplicate.

**Why:** Progress field on the queue item was `""` on retry, so the process had no way to know the portal application was already created on a previous attempt.

## Fix — Option A: two progress checkpoints
Added to `ProcessLayer/ProcessTransaction.xaml`:

1. **Check block** (before `Assign "Mark automation as started"`):
   - `If Progress = "PortalApplicationStarted"` → Throw BRE (manual review, no retry)
   - `If Progress = "PortalApplicationCompleted"` → Throw BRE (portal done, post-processing failed — reviewer verifies S3/SFDC manually)

2. **Marker 1** — `SetTransactionProgress "PortalApplicationStarted"` after `NavigateToNewPlans`, before `EnterCompanyInfo`

3. **Marker 2** — `SetTransactionProgress "PortalApplicationCompleted"` after `CloseEEEnrollment`, before `MultipleAssign_35` (automationStatus = "Completed") → before `UploadFilesToS3`

## Branch
`BT-73633-BCBS-TX-GroupSubmissions-NewPlan-fix-duplicate-retry`

## Status
- v2.0.10 committed; 3 transactions tested in Staging (2368642620 ✅, 2368657865 ✅, 2368658104 ✅)
- PR #2803 aberta: https://github.com/Gusto/biztech-uipath-rpa/pull/2803
- Aguardando aprovação e merge

**Why:** Duplicate portal applications were causing 100% fault rate on BCBS TX GroupSubmissions NewPlan.

**How to apply:** When triggering Staging test, verify queue item Progress field is set correctly at each checkpoint. On failure mid-process, retry should result in Failed Business (not a new portal application).
