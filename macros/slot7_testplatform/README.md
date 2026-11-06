<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# slot7_testplatform: slot 7 as a stand-alone test platform for the two bias reference cores (stages A and B)

Written 2026-11-06 (cloud session). Plan, pin map, measurement procedure: `docs/slot7_testplatform/PLAN.md`;
steps and numbers: `docs/slot7_testplatform/RUNLOG.md`; one-page result: `docs/slot7_testplatform/SUMMARY.md`.

`oa_core_pd` (Oguey–Aebischer) and `bg_core_pd` (Banba bandgap), each with a fail-safe 3.3 V enable, their output
currents (~5 uA, sourced) through bare hv transmission gates (`xgate`) onto `analog_bus0` / `analog_bus1`, so that an
SMU on the chip pin `analog[0]` / `analog[1]` measures them. Control from `dig_in[3:0]` and `enable`, read-back on
`dig_out[3:0]`. No custom pad is used; the 13 custom-pad pins stay as labelled stubs.

| cell | what | ports |
|---|---|---|
| `tp_en_ctrl` | 4 channels `en<k> = en<k>_1v2 AND enable AND (vdd_1v2 present)`: ratioed (hv PMOS 0.3/20 against an hv NMOS stack), then two hv inverters; read-back `rb<k>` on 1.2 V; tie-lows `lo4..lo11`; `NRD` pulls a floating `vdd_1v2` low. 43 devices | `vdd_3v3 vss_3v3 vdd_1v2 vss_1v2 en0_1v2..en3_1v2 enable en0 en0_b .. en3 en3_b rb0..rb3 lo4..lo11` |
| `slot7_testplatform` | `tp_en_ctrl`, `oa_core_pd`, `bg_core_pd`, 2 x `xgate` | the slot pins it uses |
| `slot_7` (layout top) | `slot7_testplatform` on the slot frame of the current delivery `slot_7.gds`, with its 13 pad stubs | all slot pins |

## Files

```
netlist/source/slot7_testplatform.spice      source netlist (tp_en_ctrl, slot7_testplatform)
netlist/layout/slot_7_magic.ext.spc          magic's LVS extraction of final/gds/slot_7.gds (devices, no parasitics)
schematic/xschem/                            tp_en_ctrl.sch/.sym, slot7_testplatform.sch/.sym: DRAFT sheets (one labelled
                                             stub per terminal) from gen_sheets.py; check_sheets.py netlists them with
                                             xschem and compares with the source netlist device by device (MATCH)
testbenches/ngspice/run_tb.py                static / sweep / tran / leak over 5 corners x -40/27/125 C x supplies;
                                             --dut layout runs the same on the extracted netlist
testbenches/ngspice/summarize.py             the tables in results/summary.md
testbenches/ngspice/results/                 CSV + summary.md (netlists/ is regenerated, not committed)
layout/scripts/pbc_row.py                    row builder for hv MOS rows of IHP PCells (copied from pad_buffer_cells.py)
layout/scripts/tp_en_ctrl.py                 tp_en_ctrl layout (rows + a channel router: M2 drops, M3 tracks, M4 columns)
layout/scripts/make_slot_7.py                slot_7.gds: placement, routing, TopMetal1 supply bands, sub-cell prefix slot7_
layout/scripts/build_views.sh                final/gds, final/lef (magic) from a base slot_7.gds; lef_merge_pins.py
layout/gds/tp_en_ctrl.gds                    the enable cell alone
final/gds/slot_7.gds, final/lef/slot_7.lef   the slot views; final/lib, final/vh unchanged from the delivery (same ports)
```

Rebuild (design repo root, `export PDK_ROOT=/foss/pdks; source .designinit`):
`macros/slot7_testplatform/layout/scripts/build_views.sh <delivery>/final/gds/slot_7.gds` (base: delivery `main` 40ba9b0).

## Checks (2026-11-06, details in RUNLOG)

- `tp_en_ctrl`: PDK KLayout DRC (feol + beol) 0; magic + netgen LVS against the source subckt: "Circuits match uniquely"
  (43 devices, 35 nets).
- `slot_7.gds`: PDK KLayout DRC 0 (custom-pad variant and the `--pads foundry` variant); magic + netgen LVS: "Netlists
  match uniquely" (104 devices, 72 nets) with three known port errors: `s7_an_0_outp` / `s7_an_0_outn` are joined to
  `s7_an_1_vinp` / `s7_an_1_vinn` by the delivery's stand-in Metal4 lines (kept unchanged), and the frame's Metal2
  strip at x 533..535 (relabelled `vss_1v2` by the harness) is not connected inside the slot (`vss_1v2_uq0`), as
  before; property errors only on `mm_ok`.
- Sheets: xschem netlist = source netlist, device by device (`check_sheets.py`, with a self-test).
- Simulation: `results/summary.md`.

## Stage B (2026-11-06)

`netlist/source/slot7_stage_b.spice`: `tp_en_ctrl_b` (9 channels), `slot7_stage_b` (tree, 3 reference xgates, 4 mux
xgates, ibias1 xgate), top `slot7_testplatform_ab`. Layout cells `layout/gds/tp_en_ctrl_b.gds`, `layout/gds/bias_tree_noab_pd.gds`
from `layout/scripts/routed_cell.py`; `make_slot_7.py --stage-b` / `build_views.sh <base> --stage-b` (`final/` now holds
the stage-B views; stage A: branch `claude/slot7-stage-a`). LVS reference `netlist/lvs/slot_7_lvs.spice`. Simulation
`testbenches/ngspice/run_tb_b.py`, `summarize_b.py`, results in `results_b/` and `results_b_layout/`. Pin map and
measurement: `docs/slot7_testplatform/PLAN.md` section 9. Stage-A sheets unchanged; no sheets for stage B yet (finished-style
redraws of the stage-A sheets: branch `claude/c5-slot7-schematics`, `schematic/xschem_drawn/`).
