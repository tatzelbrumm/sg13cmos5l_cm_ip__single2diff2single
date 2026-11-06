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

## Phase 2: schematic and simulation

### 2026-11-06T13:55Z — source netlist, first version
- written: `macros/slot7_testplatform/netlist/source/slot7_testplatform.spice` (`tp_en_ctrl` with 2 channels,
  `slot7_testplatform` with `oa_core_pd`, `bg_core_pd`, 2 x `analog_switch_small`)
- written: `macros/slot7_testplatform/testbenches/ngspice/run_tb.py` (static / sweep / tran / leak), `summarize.py`

### 2026-11-06T13:56Z — smoke test (tt, 27 C, nominal)
- cwd: `macros/slot7_testplatform/testbenches/ngspice`
- command: `python3 -c "import run_tb as r; r.CORNERS=['tt']; r.TEMPS=[27]; r.SUPPLIES={'nom':(3.3,1.2)}; r.static()"`
- exit: 1, 1, 0. Two fixes: `.include diodes.lib` (the standard cells' `dantenna`), and bracket-free testbench node
  names (ngspice reads `v(dig_out[0])` as a vector index; the DUT keeps its pin names).
- result: I_OA 4.992 uA, I_BG 4.958 uA at 0.7 V; off states <= 2 pA; vdd_1v2 draws 4.1 uA (all in NRD, the
  pull-down of a floating vdd_1v2); a gated-off vdd_1v2 floats at 0.37 V: charged from `dig_in[2]` / `dig_in[3]`
  through the p-antenna diode of `sg13cmos5l_antennanp` inside `analog_switch_small` (found with ngspice `show all`).

### 2026-11-06T13:58Z — full PVT run, version 1 (analog_switch_small)
- command: `python3 macros/slot7_testplatform/testbenches/ngspice/run_tb.py all` (cwd design repo root)
- log: `logs/p2_run_tb_all_v1_analog_switch_small.log`; stopped by me at 14:05Z after the static set (the design
  changed); CSV kept in the notes branch (`design_considerations/slot7_testplatform/results_v1/`)
- **finding:** state `vdd1v2_off` (vdd_1v2 gated off, dig_in = 1111, enable = 1) turned **both cores on** at
  ff / 125 C / high supply and fs / 125 C / high supply (I_bus = 7.06 / 6.31 uA). Cause: the antenna diode lifts the
  floating vdd_1v2 to 0.62 V, enough for the sense NMOS NV at 125 C. All other states correct in all 45 PVT points.
- **change:** the bus switches are now `xgate` (bare hv transmission gate 2/0.5 of the harness biasgen, layout in
  `macros/ocd_analog_switches`), driven by two more channels of `tp_en_ctrl`. Nothing on the slot's 1.2 V side is then
  driven from `dig_in` except hv NMOS gates, the switches are fail-safe like the cores, and `dig_out[3:0]` read back
  all four enables. `dig_out[11:4]` keep hv NMOS tie-lows (gate vdd_1v2), so no port is shorted to a supply.
  New stress state `vdd1v2_off_1uA`: 1 uA injected into the floating vdd_1v2 (off-leakage of the harness power gate).

### 2026-11-06T14:05Z — sheets (xschem)
- written: `macros/slot7_testplatform/schematic/xschem/{gen_sheets.py,check_sheets.py,xschemrc}`; generated
  `tp_en_ctrl.sch/.sym`, `slot7_testplatform.sch/.sym` (draft style: every terminal a stub + net label; placement in
  rows; pin positions of PDK / macro symbols read from their `.sym`)
- commands (cwd `macros/slot7_testplatform/schematic/xschem`): `python3 gen_sheets.py`; `python3 check_sheets.py`;
  `python3 check_sheets.py --selftest`
- exit: check 0 (`RESULT: MATCH`: tp_en_ctrl 43 / 43 devices, slot7_testplatform 5 / 5, ports in order); selftest 0
  (one label changed in a copy -> 1 difference found).
- on the way: the first top sheet merged 3 x 3 nets (vertical stubs on the corner pins of the tall box symbol touched
  the neighbouring pins); found by the check, fixed (horizontal stubs on the symbol's left / right edge). The first
  selftest changed a wire hint, not a label, and wrongly passed; fixed.

### 2026-11-06T14:06Z..14:11Z — full PVT run, version 2, aborted
- log overwritten by the next run; ngspice did not converge at `static_fs_-40_high_all_off` (floating nodes of the
  disabled bandgap with `gmin` 1e-15). `run_tb.py` now retries a failed run once with `gmin=1e-12 rshunt=1e14`
  (100 Tohm from every node to ground) and records it in the column `retried` and in the log line `retried ...`.

## Phase 3: layout

### 2026-11-06T14:00Z — tp_en_ctrl, 2-channel version (superseded)
- written: `macros/slot7_testplatform/layout/scripts/pbc_row.py` (lines 31..207 of `pad_buffer_cells.py`, sha256
  c3361d8d..., copied unchanged), `tp_en_ctrl.py` (rows + channel router)
- command (cwd `macros/slot7_testplatform/layout`): `python3 scripts/tp_en_ctrl.py gds/tp_en_ctrl.gds`; DRC (command as
  for analog_switch_small, input/topcell tp_en_ctrl): 0; `sak-lvs.sh -d -w /home/user/work/lvs/tp_en_ctrl -s .../tp_en_ctrl.spice -l .../tp_en_ctrl.gds -c tp_en_ctrl`: OK (29 devices). Logs `logs/p3_drc_tp_en_ctrl_v1.log`, `logs/p3_lvs_tp_en_ctrl_v1.log`.

### 2026-11-06T14:08Z — xgate checked, tp_en_ctrl with 4 channels
- `klayout -b -zz -r .../ihp-sg13cmos5l.drc -rd input=.../macros/ocd_analog_switches/layout/klayout/xgate.klay.gds -rd report=/home/user/work/drc/xgate.lyrdb -rd feol=True -rd beol=True -rd run_mode=deep -rd threads=4 -rd topcell=xgate`: exit 0, 0 items (`logs/p3_drc_xgate.log`)
- tp_en_ctrl.py: rows in bands (P band A: channels 0/1 + read-back PMOS in their own n-well; P band B: channels 2/3; N
  band); `python3 scripts/tp_en_ctrl.py gds/tp_en_ctrl.gds`: 90.53 x 68.81 um
- DRC: exit 0, 0 items (`logs/p3_drc_tp_en_ctrl.log`); LVS (`sak-lvs.sh`, as above, against the 4-channel subckt):
  "Circuits match uniquely", 43 devices, 35 nets (`logs/p3_lvs_tp_en_ctrl.log`)

### 2026-11-06T14:14Z — slot_7.gds, first assembly
- base: `/home/user/sg13cmos5l_cm_slot7/final/gds/slot_7.gds` (delivery `main` 40ba9b0), copied to
  `/home/user/work/gds/slot_7_base_delivery_40ba9b0.gds`, sha256 5624ae45efb7761fd0b405ecc785a3f2f3c3a93d93203d0aaca9feb15bedc11c
- command (cwd design repo root): `python3 macros/slot7_testplatform/layout/scripts/make_slot_7.py /home/user/work/gds/slot_7_base_delivery_40ba9b0.gds /home/user/work/gds/slot_7.gds`
- DRC v1: 16 items: 14 x M2.b (my 0.29 um Metal2 pads on the xgate pins closed the 0.24 um gaps between them) and
  2 x M1.f (solid Metal1 plates on the core rails made "wide" metal, >= 10 um, pulling the 0.6 um spacing into the
  cores). Fix: Via2 straight on the xgate pins (enclosure 0.005 / 0.05 is met by the pins); 2 um Metal1 fingers per
  via stack instead of plates. DRC v2: 0 items (`logs/p3_drc_slot_7_v1.log`, `_v2.log`).

### 2026-11-06T14:15Z — LVS of slot_7
- reference: `/home/user/work/lvs/slot_7/slot_7_lvs.spice` (subckt slot_7 = slot7_testplatform + all unused frame pins +
  the 13 pad pins; tp_en_ctrl from the source netlist; cores from `macros/*/netlist/schematic/*_magic.spice`; xgate
  from `macros/ocd_analog_switches/netlist/source/ocd_analog_switches.spice`); copy in the notes branch
- command: `sak-lvs.sh -d -w /home/user/work/lvs/slot_7 -s /home/user/work/lvs/slot_7/slot_7_lvs.spice -l <slot_7.gds> -c slot_7`
- exit 1 ("Top level cell failed pin matching"); `Netlists match uniquely with port and property errors`, 104 / 104
  devices, 72 / 72 nets. Port errors: `s7_an_0_outp`, `s7_an_0_outn` (joined to `s7_an_1_vinp` / `_vinn` by the
  delivery's stand-in Metal4 lines, unchanged on purpose), `vss_1v2_uq0` (the frame's Metal2 strip x 533.15..535.15,
  relabelled vss_1v2 by the harness; not connected inside the slot, as in the delivery). Property errors: `mm_ok` only.

### 2026-11-06T14:16Z..14:19Z — views, LEF pin merge, sub! label, foundry variant
- magic LEF (`lef write ... -hide -pinonly 2um`, as `harness_test/build_views.sh`) wrote two `PIN vss_1v2` blocks
  (the Metal2 strip and the TopMetal1 stub, now connected to devices); `lef_merge_pins.py` merges them into one PIN with
  two PORTs, as in the delivery LEF. PIN names and PORT count (73) then equal the delivery LEF.
- the vss_1v2 TopMetal1 band reached y 61.0 at the slot edge, outside the wrapper's stub (66.365..96.365): changed to
  a connector inside the stub's y range; the LEF pin is again exactly the stub.
- the PDK `ptap1` PCell carries a text `sub!` (40/0); magic makes names ending in `!` global, which at chip level could
  join this tie to other `sub!` nodes: deleted in `make_slot_7.py` (the tie is vss_3v3 by its metal).
- command: `macros/slot7_testplatform/layout/scripts/build_views.sh /home/user/work/gds/slot_7_base_delivery_40ba9b0.gds`
  (log `logs/p3_build_views.log`), exit 0; rebuilt twice, XOR of the two builds: no layer differs.
- final `macros/slot7_testplatform/final/gds/slot_7.gds` sha256 d0cdc81dd0855cc3dc56aeb77543e1eeabfc9a755943d35efbcdfb136a5d8ca6
- foundry-pad variant: `python3 .../make_slot_7.py /home/user/work/gds/slot_frame_harness-test.klay.gds /home/user/work/gds/slot_7_foundry_pads.gds --pads foundry`
  (base = `git show origin/harness-test:macros/slot/layout/klayout/slot.klay.gds`): exit 0
- 14:18:51Z DRC final and foundry variant (same command, inputs as named): exit 0, **0 items each**
  (`logs/p3_drc_slot_7_final.log`, `logs/p3_drc_slot_7_foundry.log`)
- LVS of the final GDS (as above): same result as 14:15Z (`logs/p3_lvs_slot_7.log`)

### 2026-11-06T14:20Z — the extracted layout netlist simulated
- `netlist/layout/slot_7_magic.ext.spc` = the LVS extraction; `run_tb.py static --dut layout` at tt / 27 C / nominal:
  I_OA 4.992 uA, I_BG 4.958 uA (as the schematic), all 11 states correct by read-back (`results_layout/summary.md`).

## Phase 2 (continued): final simulation runs

### 2026-11-06T14:13Z..14:22Z — full run with the convergence retry (gmin 1e-15)
- log overwritten by the next run. Two problems: (a) the first transient (`tran_tt_27`) stopped with "timestep too
  small" in the bandgap's pnpMPA at the 10 ns enable edge, so the run ended there (exit 1); (b) in the static set a
  few points at -40 C (tt / nom, fs / high) showed 0.03 .. 1 uA through an OPEN switch. Re-solved with gmin 1e-12:
  1.9 / 2.2 pA, so (b) were non-physical operating points of the disabled cores' floating nodes at gmin 1e-15.
- change: gmin 1e-12 everywhere (currents below ~10 pA are the simulation floor), 100 ns enable edges.

### 2026-11-06T14:24:22Z — full run, final settings
- command (cwd design repo root): `python3 macros/slot7_testplatform/testbenches/ngspice/run_tb.py all`, log `logs/p2_run_tb_all.log`
- static (495 points: 11 states x 5 corners x 3 temperatures x 3 supply sets) and sweep (15) complete, none retried;
  the transient set stopped again at `tran_tt_-40` (pnpMPA, timestep too small, even with the retry) -> exit 1.
- change: second retry level for a failed run: Gear integration and reltol 1e-3 (marked `:gear`).

### 2026-11-06T14:34:23Z — transient and leakage sets
- command: `python3 macros/slot7_testplatform/testbenches/ngspice/run_tb.py tran && python3 macros/slot7_testplatform/testbenches/ngspice/run_tb.py leak`
  (log `logs/p2_run_tb_tran_leak.log`): exit 0; 3 transients needed Gear (tt / -40, ss / -40, ff / 27), leakage none.
- summary: `python3 macros/slot7_testplatform/testbenches/ngspice/summarize.py > .../results/summary.md`: static: all
  logic levels and read-backs as expected in all 495 points (0 failures); numbers in SUMMARY.md.
- layout netlist (`--dut layout`, tt / ff x 27 / 125 C x nominal / high, all 11 states): same currents as the schematic
  to 4 digits, 0 logic failures (`results_layout/summary.md`).

## Phase 4: delivery and harness verification

### 2026-11-06T14:25Z — delivery repository
- cwd `/home/user/sg13cmos5l_cm_slot7`, branch `claude/c5-testplatform`: copied `macros/slot7_testplatform/final/gds/slot_7.gds`
  (sha256 d0cdc81d...) and `final/lef/slot_7.lef` (431c564a...); `cmp` showed `slot_7.lib` and `slot_7.vh` identical to the
  delivery's (same ports); README: description, provenance rows (P = this branch @ a665f66), checks section.
- commit f2c850111a33775bc1839ca1890e85c04c785c1c, pushed.

### 2026-11-06T14:21Z..14:33Z — harness fork, branch `claude/c5-testplatform-test`
- see the harness's `docs/custom_pads/RUNLOG.md`, section "Slot-7 test platform", and its `logs/c5_testplatform/`:
  submodules, `make setup`, `setup_custom_io.sh`, `s7_version`, `make projects-clean SLOTS=7`, `make projects SLOTS=7`,
  `make projects-gds SLOTS=7`, `make gds-prefill`: all exit 0. slot_7 in the pre-fill GDS: XOR against the delivered GDS
  empty. New `docs/custom_pads/tools/netcheck_slot7_platform.py` on the pre-fill top (clip 1100 2160 2100 2445):
  "all 36 used pins and 27 unused pins OK". Harness commit 9981b94d91ecc5c6e383c6ea3b63338a566e6557, pushed.
- while adapting the net check: clip 1340..2100 x 2160..2475 reached slot 8's vdd_1v2 (second vdd_1v2 net above
  y 2446.6); clip 1100.. brought in the control block, which reuses the names dig_in[k], enable, `out` on its side ->
  labels are now judged only inside slot 7's box; vss_1v2: the frame's Metal2 strip (vss1v2) is a separate piece inside
  the clip, accepted as documented; the slot's own vss_1v2 reaches the control block's ground (DVSS, vssd).

## Records

### 2026-11-06T14:42Z — notes branch `claude/c5-slot7-testplatform-sudel`
- `sudelbuecher/design_considerations/slot7_testplatform/`: `design_notes.md` (decisions, the rejected first version,
  simulation notes, open points), `results_v1_analog_switch_small/` (CSV of the first version), `lvs/` (LVS reference
  netlist of slot_7, netgen reports), `slot_7_foundry_pads.gds` (the `--pads foundry` variant, DRC 0)
- `sudelbuecher/logs/slot7-testplatform/`: all logs named in this RUNLOG
- chat log `sudelbuecher/chatlog/2026-11-06_claude_slot7_testplatform.md` (sha256 f9869504...), exported with
  `docs/slot7_testplatform/tools/export_chatlog.py` from `~/.claude/projects/-home-user/8e15a971-5e3a-5218-b4ab-7a66883211f3.jsonl`;
  the export was not refused. The transcript file lacks part of the assistant's visible text (46 text blocks are in
  it, 203 tool calls): recorded in the log's header, not reconstructed. One line added to `sudelbuecher/chatlog/README.md`.
- notes commit dd4976e, pushed.

## Branches and commits at the end

| repository | branch | commit |
|---|---|---|
| design | `claude/c5-slot7-testplatform` | this commit (after 26b9c6c) |
| design (notes) | `claude/c5-slot7-testplatform-sudel` | dd4976e |
| delivery `sg13cmos5l_cm_slot7` | `claude/c5-testplatform` | f2c8501 |
| harness fork | `claude/c5-testplatform-test` | 9981b94 |

## Stage B (2026-11-06, on the user's request "go ahead with stage B")

### 2026-11-06T18:4xZ — branches and markers
- design `claude/c5-slot7-testplatform` fast-forwarded to `origin/toplevel` 68727a71 (it was merged there); delivery
  `claude/c5-testplatform` re-created from `origin/main` (upstream set to its own remote branch afterwards).
- stage-A markers (user request): tag pushes were refused by GitHub from this session ("the remote end hung up"), so
  marker branches: design `claude/slot7-stage-a` = 68727a7, `claude/slot7-stage-a-notes` = 71e2efe (sudel_buecher),
  delivery `claude/slot7-stage-a` = 39d170f, harness fork `claude/slot7-stage-a` = 9981b94. Local annotated tags
  `slot7-stage-a` exist in this container only.
- delivery `main`: `docs/PROGRESS.md` (progress log for the harness owner), fdb7f22.
- a separate agent redraws the stage-A sheets in finished style (xschem-analog-schematic skill, installed version;
  the repo copy on sudel_buecher `Claude/skills/xschem-analog-schematic/SKILL.md` is older) in its own worktree, branch
  `claude/c5-slot7-schematics`, into `schematic/xschem_drawn/`; the draft sheets in `schematic/xschem/` (which the user
  edits by hand) are not touched by it or by stage B.

### 2026-11-06T18:5xZ — netlist and simulation
- `netlist/source/slot7_stage_b.spice`: `tp_en_ctrl_b` (9 channels), `slot7_stage_b`, `slot7_testplatform_ab`.
- `testbenches/ngspice/run_tb_b.py` (ref / ib1 / failsafe), `summarize_b.py`.
- smoke test (tt, 27 C): with a harness-source model clamped 0.6 V ABOVE the 3.3 V rail, the unselected `ibias0` /
  `ibias1` pins sat at 3.8 V and forward-biased the xgate PMOS junctions: 2.3 uA on `analog_bus3` with its switch off,
  and extra current into `iref` in the OA / BG cases. Model corrected: the source is present only where the harness
  switch would be on, clamped below the rail; otherwise the pin floats. Then OA / BG / ibias0 give the same tree.
- 2026-11-06T18:52:08Z `python3 macros/slot7_testplatform/testbenches/ngspice/run_tb_b.py all` (log `logs/b2_run_tb_b_all.log`):
  exit 0, none retried; `results_b/summary.md`.

### 2026-11-06T18:5xZ — layout
- `layout/scripts/routed_cell.py`: the tp_en_ctrl router generalized (`build_routed`); `tp_en_ctrl.py` itself unchanged.
- `tp_en_ctrl_b` (103.7 x 98.6 um): DRC first 3 x M1.b (tie extension 25 nm short of the ptap's Metal1; extension now
  overlaps by 1 um), then 0; LVS "Circuits match uniquely", 56 devices, 42 nets.
- `bias_tree_noab_pd` (57.3 x 34.4 um): DRC 0; LVS against `macros/bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice`
  + `bias_diodes`: "Circuits match uniquely", 14 devices, 10 nets.
- `make_slot_7.py --stage-b`: stage B at x 145 .. 281 um; stage A's shapes unchanged.
  `python3 .../make_slot_7.py /home/user/work/gds/slot_7_base_delivery_40ba9b0.gds /home/user/work/gds/slot_7_b.gds --stage-b`;
  DRC (deck, feol + beol, deep): 0 on the first build (`logs/b4_drc_slot_7_b_v1.log`).
- LVS `sak-lvs.sh -s netlist/lvs/slot_7_lvs.spice -l <slot_7_b.gds> -c slot_7`: "Netlists match uniquely with port and
  property errors", 190 / 190 devices, 120 / 120 nets; port errors: the same three as stage A.
- views: `build_views.sh <base> --stage-b` (now forwards all options): final GDS = the checked build (XOR empty);
  sha256 abc7a362...; LEF pin names and PORT count (73) unchanged.
- extracted netlist: stage-B tests (tt / ff x 27 / 125 C) identical to the schematic; stage-A tests repeated on it:
  same currents, 0 logic failures.
- design commit efb80141; delivery branch `claude/c5-testplatform` c0726799 (views, README, PROGRESS).

### 2026-11-06T19:03Z..19:08Z — harness fork, stage B
- branch `claude/c5-testplatform-test` (= custom-pad-test 9981b94 before): s7_version = delivery `claude/c5-testplatform`
  c0726799; `make projects-clean / projects / projects-gds SLOTS=7`, `make gds-prefill`: all exit 0; XOR of slot_7 in
  the pre-fill GDS vs the delivered GDS: empty; `netcheck_slot7_platform.py ... 1100 2160 2100 2445 --stage b`: "all 49 used
  pins and 14 unused pins OK". Harness commit c40c99b, pushed. Details: the fork's `docs/custom_pads/RUNLOG.md`.
- `custom-pad-test` and the delivery `main` are not moved (the user decides).

## After stage B (2026-11-06T19:10Z .. 23:55Z): schematic agent, branch organization

- Schematic agent (worktree `/home/user/s2d2s_c5_schematics`, branch `claude/c5-slot7-schematics` from toplevel 68727a71):
  finished-style redraws of the stage-A sheets in `macros/slot7_testplatform/schematic/xschem_drawn/` (tp_en_ctrl: one
  row per channel; top: signal flow left to right), `check_drawn.py`; commit 850dae8f. Re-checked here
  (`PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l python3 check_drawn.py`): tp_en_ctrl 43 / 43, slot7_testplatform 5 / 5
  devices, 0 differences, drawing lint 0, `RESULT: MATCH`; `--selftest`: PASS (changed label and missing symbols
  detected). Nothing outside `xschem_drawn/` changed. The drawn `tp_en_ctrl.sym` keeps pin order and names but moves
  the pins (a sheet using the draft symbol must be rewired to use it).
- The user's question why the harness fork changed: the original task file's phase 4 required the harness verification
  on the fork branch `claude/c5-testplatform-test`; for stage B it was repeated on my own judgment (not asked for).
  Changes in the fork: only that branch and the marker branch `claude/slot7-stage-a`.
- Tim updated `RTimothyEdwards/sg13cmos5l_ocd_chipalooza` `main` (e7d72da, 2 commits: user custom pad handling,
  `scripts/setup_custom.sh`). Read-only check here: the fork's `main` (e0445b6) is not an ancestor (5 commits of the
  fork's own); a test merge into custom-pad-test (throwaway worktree, aborted, nothing pushed) gives one conflict, in
  `scripts/layout_setup.tcl`, the comment line above `addpath custom_io` only. The user merged Tim's `main` into the
  fork's `main` himself (3d9baf5) and fast-forwarded his `custom-pad-test` to `claude/c5-testplatform-test`.
  Note for later: Tim's `setup_custom.sh` and the fork's `setup_custom_io.sh` both write `magic/custom_io`; and
  `claude/c6-submodule-pads` covers what Tim's new commits do.
- Design repo, merged by the user: `toplevel` 312150b5 = stage B (fast-forward) + `claude/c5-slot7-schematics`;
  `sudel_buecher` 88b3fc82 = `claude/c5-slot7-testplatform-sudel`. Checked here: the schematics merge adds only the 8
  `xschem_drawn` files. Not merged yet: `claude/c4-replica-bias` (5 commits; `git merge-tree` against toplevel: clean)
  and `claude/c4-replica-bias-sudel` (1 commit; one conflict in `sudelbuecher/chatlog/README.md`, two index lines,
  keep both).
- Delivery `main` and the fork's `custom-pad-test` with stage B: the user decides (delivery `claude/c5-testplatform`
  681c8dd is 2 commits ahead of `main`, fast-forward).
