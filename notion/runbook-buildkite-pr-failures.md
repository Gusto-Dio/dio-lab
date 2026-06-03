# Runbook — Buildkite PR Failures

**Scope:** biztech-uipath-rpa  
**Applies to:** Any PR that triggers a Buildkite pipeline failure  
**Last updated:** 2026-06-03

---

## Overview

Buildkite runs `check_version.sh` and `check_dependency.sh` against every process detected in the diff between the PR branch and `develop`. There are three distinct failure patterns, each with its own fix.

---

## Pattern 1 — Version not bumped

**Error message:**
```
process can't be upgraded from version X.X.X to X.X.X
```

**Cause:** The `projectVersion` in `project.json` is the same as the version already on `develop`. Buildkite requires a strict version increment.

**Fix:**
1. Open `{ProcessFolder}/project.json`
2. Increment `projectVersion` by one patch: `1.3.6` → `1.3.7`
3. Stage only `project.json`:
   ```powershell
   git add "Processes/.../project.json"
   git status --short  # confirm only project.json is staged
   ```
4. Commit and push:
   ```powershell
   git commit -m "[BT-XXXXX] Bump {ProcessName} version X.X.X -> X.X.Y"
   git push
   ```

---

## Pattern 2 — Dirty diff (branch behind develop)

**Symptom:** Buildkite runs `check_dependency.sh` against processes you did not touch. The diff shows files from other tickets that merged into `develop` after your branch was created.

**Cause:** Buildkite uses `git diff origin/develop..HEAD` (two dots). Any process merged into `develop` after your branch was cut appears in the diff — even if you never touched it.

**Diagnosis:**
```powershell
git fetch origin develop
git diff origin/develop..HEAD --name-only
```
If the output includes files outside your ticket's process folder, your branch is behind.

**Fix:**
```powershell
git merge origin/develop --no-edit
# If conflicts on your files, resolve with --ours:
git checkout --ours "Processes/.../YourFile.xaml"
git add "Processes/.../YourFile.xaml"
git commit

# Verify diff is clean before pushing:
git diff origin/develop..HEAD --name-only
# Must show ONLY your ticket's files
git push
```

---

## Pattern 3 — check_dependency.sh fails on an unrelated process

**Error message:**
```
check_dependency.sh Processes/.../SomeOtherProcess
Error: dependency X version Y.Y.Y does not meet requirement
```

**Cause:** Pattern 2 left an unrelated process in the diff. That process has a stale library dependency that `check_dependency.sh` rejects.

**Fix:** Same as Pattern 2 — merge `develop` to remove the unrelated process from the diff. You do not need to update the unrelated process's dependencies.

---

## Pre-PR checklist (prevents all three patterns)

Run these steps before every `git push`:

```powershell
# 1. Confirm only ticket-scope files are staged
git status --short

# 2. Check diff against develop
git fetch origin develop
git diff origin/develop..HEAD --name-only

# 3. If any out-of-scope files appear — merge develop
git merge origin/develop --no-edit

# 4. Verify diff is clean
git diff origin/develop..HEAD --name-only
# Expected: only your process files + project.json

# 5. Confirm version is incremented in project.json
grep "projectVersion" Processes/.../project.json
```

---

## Notes

- Never use `git add .` or `git add -A` — stage files by explicit path only
- The merge commit from `git merge origin/develop --no-edit` is expected and harmless — Buildkite ignores it
- If a conflict arises on a file you intentionally modified, resolve with `--ours` and re-add
