<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C0: cloud pilot — toolchain, and one check reproduced

Claude Code cloud session, environment `sg13cmos5l`, clone of `main`. Read
`sudelbuecher/cloud_environment.md`, section "Claude Code cloud sessions", first.

**Git, for this task only (Christoph's permission):** `git fetch origin sudel_buecher`, the worktree
in step 1, commits on `claude/c0-pilot-sudel`, and pushing that one branch. Nothing else: never push
`main` or `sudel_buecher`, no tags, no force pushes, no merges. This task changes nothing on `main`.

1. **Records worktree:** `git fetch origin sudel_buecher && git worktree add -b claude/c0-pilot-sudel
   ../sudel origin/sudel_buecher`. Never switch the main checkout to `sudel_buecher`.
2. **Toolchain:** read `/foss/setup.log` (every `_OK` line and `SETUP_DONE`; under about 300 s means
   the environment gets cached). Check:
   - `klayout -b -v`: KLayout 0.30.12;
   - `python3 -c "import klayout.db as d; print(d.__version__)"`: 0.30.12;
   - `xschem --version`: 3.4.8RC;
   - `ngspice -v`: ngspice-47;
   - `git -C /foss/pdks/IHP-Open-PDK rev-parse HEAD`: c271a7e9…;
   - `ls $PDK_ROOT/ihp-sg13cmos5l/libs.tech/ngspice/osdi`: psp103.osdi among others.
   If KLayout or the PDK is missing, skip step 3, report why, and stop.
3. **Reproduce agent A2's bg_core_pd checks** (`../sudel/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/
   agents/A2_oa_core_pd_layout/report_bg.md`; package in `../sudel/sudelbuecher/design_considerations/
   pad_buffer_layout/bg_core_pd_2026-10-28/`, including `run_checks.sh` and `tools/`):
   - sha256 of `macros/bg_core_pd/layout/gds/bg_core_pd.gds` against the package's `bg_core_pd.gds`;
   - DRC and LVS of that GDS the way the package runs them, in a scratch directory outside both
     checkouts; adapt only paths that assumed another machine, and list each adaptation;
   - compare with the report: DRC 0 of 74 rules; LVS MATCH against `bg_core_pd.cdl`.
4. **Time** every step (wall clock).
5. **Report:** write `../sudel/sudelbuecher/cloud_sessions/C0_pilot_report.md` with SPDX header:
   versions found, setup.log times, results against A2's, what failed and why, the times; short.
   Commit it on `claude/c0-pilot-sudel` and push that branch. Then say in the session that it's done
   and give the branch name.
