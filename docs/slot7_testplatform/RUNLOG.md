<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# RUNLOG: slot 7 as a stand-alone test platform for the bias references

Cloud session, 2026-11-06. Task file: `docs/launch/slot7_testplatform_TASK.md` on `harness-test` (read with
`git show origin/harness-test:docs/launch/slot7_testplatform_TASK.md`, commit `0767ed6`). One entry per step: UTC
time, cwd, exact command, exit status, log file, what changed. Long logs are in the notes branch
`claude/c5-slot7-testplatform-sudel` under `sudelbuecher/logs/slot7-testplatform/` (named `logs/...` below).
Scratch work directory of the container: `/home/user/work` (not committed; logs copied to the notes branch).

## Tool versions (once)

| tool | version |
|---|---|
| KLayout (binary and python module `klayout`) | 0.30.12 |
| ngspice | ngspice-47 (PSP103 via OSDI, `SPICE_USERINIT_DIR=$PDK_ROOT/$PDK/libs.tech/ngspice`) |
| magic | 8.3.685 |
| netgen | 1.5.324 |
| xschem | 3.4.8RC |
| cace | 2.11.0 |
| python | 3.13.18 |
| PDK | `/foss/pdks/ihp-sg13cmos5l` |

## Starting points

| repository | branch created | from | commit |
|---|---|---|---|
| `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single` | `claude/c5-slot7-testplatform` | `origin/toplevel` | `cf88683b74ce1284ddc7cd327c4effeb771606a3` |
| same, worktree `../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher` | `claude/c5-slot7-testplatform-sudel` | `origin/sudel_buecher` | `aecf1bb0b574e5936f3e7b3b384a0f2ab5885815` |
| `tatzelbrumm/sg13cmos5l_cm_slot7` | `claude/c5-testplatform` | `origin/main` | `40ba9b030d0c3e321438600fea5ae0a13439799a` |
| `tatzelbrumm/sg13cmos5l_ocd_chipalooza` | `claude/c5-testplatform-test` | `origin/custom-pad-test` | `45831b854cb2aa1b0d57157a94431d684e6a28b6` |

## Entries

### 2026-11-06T13:38Z — check that the branch names are free
- cwd: each repository root under `/home/user`
- command: `git ls-remote --heads origin` (all three repositories)
- exit: 0
- result: none of `claude/c5-slot7-testplatform`, `claude/c5-slot7-testplatform-sudel`, `claude/c5-testplatform`,
  `claude/c5-testplatform-test` existed (the design repository has the parallel task's `claude/c4-replica-bias-sudel`).

### 2026-11-06T13:39Z — create and push the branches (proves push access to all three)
- cwd: `/home/user/sg13cmos5l_cm_ip__single2diff2single`
- commands:
  - `git fetch origin toplevel sudel_buecher harness-test`
  - `git checkout -b claude/c5-slot7-testplatform origin/toplevel`
  - `git worktree add -b claude/c5-slot7-testplatform-sudel ../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher origin/sudel_buecher`
  - `git push -u origin claude/c5-slot7-testplatform`
  - `git -C ../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher push -u origin claude/c5-slot7-testplatform-sudel`
  - in `/home/user/sg13cmos5l_cm_slot7`: `git fetch origin main && git checkout -b claude/c5-testplatform origin/main && git push -u origin claude/c5-testplatform`
  - in `/home/user/sg13cmos5l_ocd_chipalooza`: `git fetch origin custom-pad-test && git checkout -b claude/c5-testplatform-test origin/custom-pad-test && git push -u origin claude/c5-testplatform-test`
- exit: 0 for every command; each push printed `* [new branch]`.
- note: the worktree's own `CLAUDE.md` forbids git there; it is written for the local sandbox (an `unlink` problem
  with `index.lock`). In this cloud container git works there (the push above succeeded), and the task file requires
  commits and pushes on the notes branch, so git is used in the worktree in this session.

### 2026-11-06T13:40Z–13:52Z — survey (read only)
- cwd: the three repositories
- commands (read only, no output files): `cat`/`sed -n`/`grep` of `CLAUDE.md`, `macros/README.md`,
  `macros/{oa_core_pd,bg_core_pd,en_ctrl_3v3,ocd_analog_switches,hv_logic}/README.md` and netlists,
  `git show origin/harness-test:macros/slot/{README.md,harness_test/*}`,
  harness `verilog/rtl/{slot7_wrapper.v,chipalooza_frame.v,user_project_control.v,user_project_control_base.v,housekeeping.v,router.v}`,
  harness `scripts/run_gen_user_wrappers.sh`, `magic/slot7_wrapper.mag`, `config.txt`, `docs/custom_pads/FINDINGS.md`;
  KLayout python dumps of `macros/slot/layout/klayout/slot.klay.gds`, `macros/slot/reference/slot7_wrapper.gds`
  (from `harness-test`) and `macros/ocd_analog_switches/layout/klayout/{analog_switch_small,sw_lvl_shift}.klay.gds`;
  rule values from `$PDK_ROOT/$PDK/libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json`.
- exit: 0
- findings (each fact of the task file checked): see `PLAN.md` section 1.

### 2026-11-06T13:45Z — prototype of the ratioed enable stage (ngspice, scratch)
- cwd: `/tmp/claude-0/.../scratchpad/proto` (scratch)
- command: a loop over `mos_{tt,ss,ff,sf,fs}` x `.temp -40/27/125` x pull-up W/L `0.3/10`, `0.3/20` of a netlist
  `p.sp` with an hv PMOS pull-up against three series hv NMOS 2/0.45, gates at 1.08 V, supply 3.6 V; `ngspice -b p.sp`
- exit: 0 (30 runs)
- result: pulled-down node <= 37 mV (0.3/10) and <= 18 mV (0.3/20) in all 30 runs; static current 1.26..2.44 uA
  (0.3/20) per enabled channel; off state 3.6 V, leakage <= 49 pA. Chosen: 0.3/20.

### 2026-11-06T13:52:43Z — KLayout DRC of the harness switch `analog_switch_small` (reused unchanged)
- cwd: `/home/user/work/drc`
- command: `klayout -b -zz -r /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc -rd input=/home/user/sg13cmos5l_cm_ip__single2diff2single/macros/ocd_analog_switches/layout/klayout/analog_switch_small.klay.gds -rd report=/home/user/work/drc/analog_switch_small.lyrdb -rd feol=True -rd beol=True -rd run_mode=deep -rd threads=4 -rd topcell=analog_switch_small`
- exit: 0
- log: `logs/p3_drc_analog_switch_small.log`; result: 0 items in the report (the THKOX discrepancy noted in
  `macros/ocd_analog_switches/README.md` does not trip a rule).
