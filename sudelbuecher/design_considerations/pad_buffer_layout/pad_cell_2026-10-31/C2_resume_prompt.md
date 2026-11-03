<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C2 resume prompt (paste into a new Claude Code session; edit the two paths if yours differ)

```
You are the lead of task C2 (layout of the sg13cmos5l_IOPadDiff2Single pad cell), resuming from a handoff.
Design worktree: ~/EDA/sg13cmos5l_cm_ip__single2diff2single (branch claude/c2-pad-layout).
Notes worktree: ~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher (branch claude/c2-pad-layout-sudel).
Check both are on those branches and up to date with origin (git fetch + fast-forward only); never switch the design
worktree to a notes branch.

Read, in this order: CLAUDE.md, docs/local-container.md and the "Local-only" section of docs/traps.md (design
worktree); then in the notes worktree sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31/
HANDOFF.md, decisions.md and report.md; sudelbuecher/cloud_sessions/C2_pad_cram_draft.md (the task brief; its rules,
cost rules and git rules apply); sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/BRIEF.md.

For this task I allow: git commit and push on claude/c2-pad-layout and claude/c2-pad-layout-sudel only (no other
branch, no force push, no merge, no tags); running the PDK's DRC / LVS / PEX and the scripts in the notes folder; one
background subagent at a time.

Do HANDOFF.md "Next steps" 1–2 now: set up F2's workspace at ~/EDA/c2_work/F2 (work/, out/), start F2 in the
background on Opus with effort high, with BRIEF.md and the absolute paths, stage A only. When F2 reports, check its
cells as the handoff says, copy its out/ and work/ into agents_c2/F2/, commit and push the notes branch, show me the
placement picture, and stop for my review. Commit and push after every finished step, so a crash or restart loses at
most the step in progress; if you are a resumed session, first read the newest commits and agents_c2/F2/ to see where
the work stands.
```
