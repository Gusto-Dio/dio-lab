---
name: XAML edit skill protocol — invoke before any edit
description: Must call uipath:uipath-rpa skill before editing any .xaml file, even when analysis is already done
type: feedback
originSessionId: 848027dd-e12e-49f1-89d2-a9eaf3333032
---
Always invoke the `uipath:uipath-rpa` skill before making the first XAML edit in a session — no exceptions, even when the analysis from the previous session is fully loaded and the fix is already known.

**Why:** CLAUDE.md marks this NON-NEGOTIABLE. Rationalizations like "I already know what to do" or "it's just an attribute change" are exactly the red flags listed in superpowers:using-superpowers. The skill also requires `get-errors` per-file validation after every edit, which would have been missed without invoking it.

**How to apply:** In any session where a `.xaml` file will be edited: invoke `uipath:uipath-rpa` skill FIRST, before opening any Edit tool on a XAML file. `git branch` confirmation + skill invocation are both mandatory prerequisites.
