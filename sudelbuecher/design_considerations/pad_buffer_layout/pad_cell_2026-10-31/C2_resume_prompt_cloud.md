<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C2 resume prompt for a Claude Code cloud session (environment `sg13cmos5l`, setup script of claude-cloud-config)

Start the session on repository `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`, branch `claude/c2-pad-layout`, then
paste:

```
You are the lead of task C2 (layout of the sg13cmos5l_IOPadDiff2Single pad cell), resuming from a handoff of an
earlier cloud session. The base is the two branches on origin: claude/c2-pad-layout (design, checked out here) and
claude/c2-pad-layout-sudel (notes). Develop on claude/c2-pad-layout; don't create it again. Fetch, make sure this
checkout is claude/c2-pad-layout at origin's state (stop and ask me if not), and add the notes branch as a worktree:
git fetch origin claude/c2-pad-layout-sudel && git worktree add ../sudel claude/c2-pad-layout-sudel
(track origin; fast-forward only). Never switch the design checkout to a notes branch.

First, environment checks: /foss/setup.log needs TOOLS_OK, PDK_OK, OSDI_OK, CACE_OK, SETUP_DONE. Check that
$PDK_ROOT/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/layers_def.drc resolves; if it is a dangling link, run
git -C /foss/pdks/IHP-Open-PDK sparse-checkout add /ihp-sg13g2/libs.tech/klayout/tech/ and say so (the setup script
needs that path). Grep every run_drc.py log for "generated an exception".

Read, in this order: CLAUDE.md; in ../sudel: sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31/
HANDOFF.md, decisions.md and report.md; sudelbuecher/cloud_sessions/C2_pad_cram_draft.md (the task brief: its rules,
cost rules and git rules apply; its worktree is the ../sudel above); sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/
agents_c2/F2/BRIEF.md. HANDOFF.md says ~/EDA paths for local use: here the design checkout is the current directory
and the notes worktree is ../sudel.

Git for this task: commit and push only claude/c2-pad-layout and claude/c2-pad-layout-sudel (no other branch, no force
push, no merge, no tags, no pull request).

Do HANDOFF.md "Next steps" 1–2 now: F2's workspace at /home/user/c2/F2 (inputs/ read-only copies as its brief lists,
work/, out/), start F2 in the background on Opus with effort high, stage A only. When F2 reports, check its cells as the
handoff says, copy its out/ and work/ into agents_c2/F2/ in ../sudel, commit and push the notes branch, show me the
placement picture, and stop for my review. Commit and push after every finished step: the container dies with the
session, and a new session resumes from the pushed state (read the newest commits and agents_c2/F2/ first).
```
