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
