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

## Phase 2: design and simulation (scope: user's answer 1a, 2A, 3 all)

User's answer (2026-11-06 ~17:25 UTC): **1a** S2D `vref` = 0.5 V from its own block `vref_s2d_rb`; **2A** `vcm` tracks the
band centre (block `vcm_rb`, shared by S2D `vcm` and D2S `vref`); **3** all gap runs G1–G11.
Environment for every command below: `export PDK_ROOT=/foss/pdks; source .designinit` in the repo root (sets PDK,
SPICE_USERINIT_DIR = the PDK's ngspice dir, so decks run anywhere). Pad macros are not changed: gap runs use new decks on
the pads' source netlists, or temporary yaml copies whose runs are deleted (results copied into the new macros).

| # | time | cwd | command | exit | log / output | what changed |
|---|---|---|---|---|---|---|
| 17 | 17:30 | `macros/<pad>/verification/cace` | G11 smoke test: xschem library-path export as the pad Makefile, then `cace sg13cmos5l_IOPadSingle2Diff.yaml -s schematic -p window_params -j 4` and `cace sg13cmos5l_IOPadDiff2Single.yaml -s schematic -p dc_ibias_params -j 4`; `scripts/cace/cace_to_csv.py` into the scratchpad; `rm -rf _runs _docs netlist .xschem_library_path` | 0 / 0 | S2D 27 runs 30 s, D2S 3 runs 4 s | none committed. S2D identical to the committed 2026-11-05 CSV (27 / 27); D2S moved against 2026-10-20 as the design did (I_Q per device 212.4 → 222.9 µA, Iio 298.7 → 308.4 µA, INL 1.356 → 1.376 mV): CACE 2.11.0 works with both yamls |
| 18 | 17:33 | `macros/vcm_rb/testbenches/pad_char` | new `run_pad_char.py` (decks on the pads' source netlists, template measurement code verbatim); `python3 -I run_pad_char.py val_s2d val_d2s -j 4` | 0 | `results/val_*.tsv` | validation: S2D 13.599 / 5.499 / 32.43 mV against CACE `range_params` 13.60 / 5.50 / 32.43; D2S identical to row 17 |
| 19 | 17:33–18:03 | same | `python3 -I run_pad_char.py g3_s2d_vcm g4_s2d_vref g1_d2s_vref g2_d2s_vicm g10_s2d_sel g10_d2s_sel g5_s2d_op g5_d2s_op g9_loop -j 4` (background) | 0 | notes branch `logs/replica-bias/phase2_pad_char_dc.log`; `results/*.tsv` | 2104 runs; 3 without result (op failure at tt / −40 °C / 3.3 V in the disabled bandgap core's floating rhigh chain) |
| 20 | 17:57–18:00 | same | driver: retry with `.options rshunt=1e12` when a run has no complete result; `python3 -I run_pad_char.py g3_s2d_vcm g4_s2d_vref --rerun-failed -j 3` (twice: the first pass missed a short line) | 0 | `results/g3_s2d_vcm.tsv`, `g4_s2d_vref.tsv` (column `conv`) | 3 runs completed with rshunt; no run without result left |
| 21 | 17:38–17:52 | repo root | `python3 -I macros/vref_s2d_rb/testbenches/spice/explore_ztc.py`; `python3 -I macros/vcm_rb/testbenches/spice/explore_edges.py 0.95 0.9 0.8` / `0.8 0.7 0.6` / `0.8 0.7` | 0 | `macros/vcm_rb/testbenches/spice/results/explore_edges{,_b,_c}.tsv` | exploration (zero-TC currents of the pads' diode sizes; edge-detector replicas on a copy of the pad bias); first run of explore_edges had a node-name clash (`s0` = the harness sel0 line), fixed (`ts<k>`) and rerun |
| 22 | 18:04–18:10 | `macros/vcm_rb/testbenches/pad_char` | `OMP_NUM_THREADS=1 python3 -I -u run_pad_char.py g6_s2d_ac g6_d2s_ac g6_s2d_tran g6_d2s_tran g6_s2d_en -j 4` (background) | 0 | notes branch `logs/replica-bias/phase2_pad_char_g6.log`; `results/g6_*.tsv` | G6: 150 runs, all with result. AC: up to 1 MOhm harmless; steps: bypass >= 1 pF needed above 10 kOhm; S2D enable: vcm pin +-70 mV at 10 kOhm, +0.28 / -0.17 V at 100 kOhm with 1 pF |
| 23 | 18:06–18:20 | repo root | `python3 -I macros/vcm_rb/testbenches/spice/explore_vcm_rb.py` (candidates A-D, then D-G); impedance of candidate G (inline deck, first try without `source .designinit`: no models, rerun with it) | 0 | `macros/vcm_rb/testbenches/spice/results/explore_vcm_rb{,_DEFG}.tsv` | candidate G chosen (worst margin 39 mV); its stack midpoint alone has 0.2-1.06 MOhm: an output buffer added |
| 24 | 18:20–18:25 | repo root | `python3 -I macros/vref_s2d_rb/testbenches/spice/explore_vref.py` (key-case fix, rerun) | 0 | `macros/vref_s2d_rb/testbenches/spice/results/explore_vref.tsv` | follower density chosen (4 x 15u/3u at 1.67 uA) |
| 25 | 18:25–18:30 | — | wrote `macros/vcm_rb/netlist/source/vcm_rb.spice`, `macros/vref_s2d_rb/netlist/source/vref_s2d_rb.spice`; `sed` added `mm_ok=1` to every device (as the pads' sheets) | — | — | the two blocks |
| 26 | 18:30–18:33 | `macros/vcm_rb/testbenches/rb_char` | new `run_rb.py`; smoke test of the four deck types at tt 27 C (inline python) | 0 | `_runs/t_*.log` | blocks: vcm 1.2615 V, vref 0.4937 V; the round-trip deck with both blocks inside does not converge (op, 558 s): replaced by ideal sources at the blocks' DC outputs (exact at DC) |
| 27 | 18:33–18:54 | same | `OMP_NUM_THREADS=1 python3 -I -u run_rb.py rb_dc rb_z rb_mm cl_s2d_dc cl_d2s_dc cl_loop_eq rb_en rb_up -j 4` (background) | 0 | notes branch `logs/replica-bias/phase2_rb_char.log`; `results/*.tsv` | rb_z lost (second AC plot scope: fixed with `set`); rb_up: 6 runs without result at ss / -40 C (transient op at iovdd = 0 fails in the bandgap PNP) |
| 28 | 18:34–18:47 | repo root | `python3 -I macros/vcm_rb/schematic/gen_sheet.py <netlist> <cell> <dir> 6` for both; xschem netlist (`xschem -q -x -n -s --tcl 'set top_subckt 1' ...`) and `gen_sheet.py --check`; `python3 -I macros/vcm_rb/verification/gen_cace.py`; `python3 -I macros/vcm_rb/gen_makefiles.py` (a first attempt with the Makefile text inline in the shell command was refused by the session's safety check because of the recipe's `rm -rf` cleanup line; moved into a script file); `make -C macros/<block> check-sheet` | 0 | — | sheets and symbols: 24 = 24 and 16 = 16 devices, ports equal; CACE suites; Makefiles; first CACE try of vcm_rb pd_params: xschem refused an undriven net (`irefd`), templates rewired, then pass |
| 29 | 18:55–19:04 | repo root | `bash macros/vcm_rb/verification/baseline/run_g7_g8.sh` (background) | 0 | notes branch `logs/replica-bias/phase2_g7_g8.log`; `macros/vcm_rb/verification/baseline/d2s_*`, `macros/vref_s2d_rb/verification/baseline/s2d_mc_vref0v5` | G7: D2S CACE at 1.2 V and 1.65 V and the loop fixture, every limit met; G8: S2D mismatch / process MC at vref 0.5 V. Pad macros unchanged (`git status`) |
| 30 | 18:56–19:00 | `macros/vcm_rb/testbenches/rb_char` | `run_rb.py rb_up --rerun-failed -j 2` (deck now `tran ... uic`); `run_rb.py rb_z -j 2`; `run_rb.py cl_s2d_en -j 2`; `run_rb.py cl_s2d_win -j 2` (twice: the first version referenced the pad source to the block's vref node, so the pad's ESD-diode current at pad < 0 loaded the block; now a ground-referenced source) + inline window evaluation | 0 | `results/rb_up.tsv`, `rb_z.tsv`, `cl_s2d_en.tsv`, `cl_s2d_win.txt` | start-up complete; impedance 22-35 / 18-28 kOhm; S2D enable 1.39-1.44 us with the blocks; S2D pad range 0 ... >= 1.09 V up to 27 C |
| 31 | 19:07–19:10 | repo root | `make -C macros/vcm_rb sim-cace CACE_JOBS=4`; `make -C macros/vref_s2d_rb sim-cace CACE_JOBS=4` (the second failed first: a ': ' in an unquoted yaml string; strings quoted, both rerun) | 0 | notes branch `logs/replica-bias/phase2_sim_cace_*.log`; `macros/*/verification/cace/results/` | vcm_rb 5 / 5 groups pass, vref_s2d_rb 5 / 5 pass |
| 32 | 18:47–19:12 | repo root | `git commit` / `git push origin claude/c4-replica-bias` (`03436eae`, `b32f79df`, `dd8edd2b`) | 0 | — | Phase 2 pushed |

## Phase 3: layout

Not started (decision 19:12 UTC): two hv layouts with DRC / LVS would not fit what is left of this session next to the
records. Delivered instead: the floorplan sketch and area estimate in `SUMMARY.md` (gate area 542 / 564 µm², about
50 × 60 µm each with hv spacing). The sheets, symbols and source netlists are ready for a layout session; `make
klayout-drc`, `make magic-lvs` etc. are in both Makefiles (copied from oa_core_pd).
