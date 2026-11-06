<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Run log: replica bias for vref / vcm (task `docs/launch/replica_bias_TASK.md`, branch `harness-test`)

Cloud session, 2026-11-06. Design checkout `/home/user/sg13cmos5l_cm_ip__single2diff2single` (branch
`claude/c4-replica-bias`), notes worktree `/home/user/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher` (branch
`claude/c4-replica-bias-sudel`). Times UTC.

## Tool versions (once)

| tool | version |
|---|---|
| ngspice | ngspice-47 |
| xschem | 3.4.8RC |
| CACE | 2.11.0 (the S2D README names 2.13.0 for the runs of 2026-10-25/26) |
| KLayout | 0.30.12 |
| magic | 8.3.685 |
| netgen | 1.5.324 |
| Python | 3.13.18 |
| git | 2.43.0 |
| PDK | `/foss/pdks/ihp-sg13cmos5l` (IHP-Open-PDK `df4c5054`, 2026-10-14) |

## Phase 1: survey (read only)

| # | time | cwd | command | exit | log | what changed |
|---|---|---|---|---|---|---|
| 1 | 13:40 | design checkout | `git remote -v; git status -sb; git fetch origin harness-test` | 0 | — | remote branch `origin/harness-test` fetched |
| 2 | 13:40 | design checkout | `git show origin/harness-test:docs/launch/replica_bias_TASK.md` | 0 | — | task file read |
| 3 | 13:40 | — | `add_repo tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single access=push` (session tool) | ok | — | repo already attached, push access |
| 4 | 13:40 | design checkout | `git ls-remote --heads origin` | 0 | — | neither `claude/c4-replica-bias` nor `claude/c4-replica-bias-sudel` existed |
| 5 | 13:40 | design checkout | `git fetch origin toplevel sudel_buecher` | 0 | — | — |
| 6 | 13:40 | design checkout | `git checkout -b claude/c4-replica-bias origin/toplevel` (`cf88683`); `git worktree add -b claude/c4-replica-bias-sudel ../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher origin/sudel_buecher` (`aecf1bb`) | 0 | — | both branches created |
| 7 | 13:40 | design checkout / notes worktree | `git push -u origin claude/c4-replica-bias`; `git push -u origin claude/c4-replica-bias-sudel` | 0 | — | both branches on the remote (push access confirmed) |
| 8 | 13:41–13:46 | design checkout | read (`cat`, `sed -n`, `grep`): `macros/sg13cmos5l_IOPad{Single2Diff,Diff2Single}/{README.md,FILL_IN.md}`, `netlist/source/*.spice`, `verification/cace/*.yaml`, `templates/*_tb_dc.sch`, `testbenches/spice/*.spice`; `macros/{oa_core_pd,bias_tree_pd,bias_tree_noab_pd,bias_dist_pd,bias_gen_pd,bias_sel_pd,slot}/README.md`; `macros/bias_tree_pd/netlist/source/bias_ref_pd.spice`; `docs/state-and-next-task.md`; `git show origin/harness-test:docs/launch/slot7_testplatform_TASK.md` | 0 | — | none |
| 9 | 13:42–13:45 | design checkout | inline `python3` pivots of `range_params.csv`, `window_params.csv`, `dc_params.csv` (S2D, schematic and pex), `dc_params.csv`, `dc_3v0_params.csv` (D2S); `yaml.safe_load` of both pad yamls and loop fixtures (conditions per group) | 0 | superseded by row 13 | none |
| 10 | 13:45 | design checkout | `git fetch --depth=1000 origin toplevel`; `git log --format='%h %ad %s' --date=… -- <results dirs>` | 0 | — | deeper local history (shallow clone), for the dates of the run table |
| 11 | 13:46–13:50 | notes worktree | read: `sudelbuecher/description/s2d_d2s_pinbuffers.md`; `design_considerations/s2d_input_buffer/{s2d_input_buffer.md,sim/results_s2d.txt}`; `class_ab_pad_driver/improvements/{proposed_improvements.md,bias.md}`, `power_down/log.md`; `pad_buffer_layout/pad_cell_2026-10-31/sanity_2026-11-03/README.md`; `logs/claude/c3-s2d-pad-layout/p5-sim-cace-*.out` (timing) | 0 | — | none |
| 12 | 13:47 | design checkout | `ngspice --version; xschem --version; cace --version; klayout -v; magic --version; netgen -batch quit; python3 --version; git --version; git -C /foss/pdks/ihp-sg13cmos5l log -1` | 0 | — | versions above |
| 13 | 13:51 | design checkout | `python3 -I /home/user/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/replica_bias/phase1/survey_tables.py /home/user/sg13cmos5l_cm_ip__single2diff2single /home/user/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher \| tee …/sudelbuecher/logs/replica-bias/phase1_survey_tables.log` | 0 | notes branch `sudelbuecher/logs/replica-bias/phase1_survey_tables.log` | none (tables of `SURVEY.md`) |
| 14 | 13:55 | design checkout | wrote `docs/replica_bias/{SURVEY,RUNLOG,SUMMARY}.md`; notes branch: `design_considerations/replica_bias/phase1/{survey_tables.py,README.md}` | 0 | — | new files |
| 15 | 13:56–13:58 | design checkout | copied `pad_buffer_layout/pad_cell_s2d/chatlog_tools/{build,verify}_chatlog.py` (session C3) to `replica_bias/chatlog_tools/`; changed: one bracketed line per tool call, live path starts at the last record that has a `uuid` (the first run failed with `IndexError`: the transcript's last line had none); then `python3 -I …/build_chatlog.py ~/.claude/projects/-home-user-sg13cmos5l-cm-ip--single2diff2single/f7165478-7787-531e-a1d8-6ec7206ebfcb.jsonl …/sudelbuecher/chatlog/2026-11-06_claude_replica_bias.md …/chatlog_tools/header.md` and `python3 -I …/verify_chatlog.py <same transcript> <same log>` | 0 | verify: texts 8, missing 0; reasoning windows found 0 | chat log + README entry. **Gap:** the transcript keeps only 6–7 of about 20 visible assistant messages as text records; the rest are not reconstructed (stated in the log header) |
| 16 | 13:59 | both checkouts | `git add …; git commit; git push -u origin claude/c4-replica-bias`, `… claude/c4-replica-bias-sudel` | see git | — | Phase 1 committed and pushed |

No simulation was run in Phase 1. Phase 1 ends with the question to the user (task file: "Then STOP and ask the user").
