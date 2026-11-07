<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# slot7_testplatform: finished-style sheets

Redraws of the draft sheets in `../xschem/` (one labelled stub per terminal, from `gen_sheets.py`) in the finished
analog style of the `xschem-analog-schematic` skill: ports in one column at the far left, outputs on the right edge,
rails as wires, one column per current branch, real orthogonal wires, `lab_pin` only for long nets. Written
2026-11-06 (cloud session). **The draft sheets in `../xschem/` are unchanged**, so both can be compared and this
version adopted (copy the four stage-A `.sch` / `.sym` files over, or put this directory first on the library path).
The stage-B sheets (below) have no draft; they exist only here.

| file | what |
|---|---|
| `tp_en_ctrl.sch` / `.sym` | the enable cell, 43 hv devices, same cell name, ports and port order as the source |
| `slot7_testplatform.sch` / `.sym` | `xctl` (`tp_en_ctrl.sym` from here), `xoa` / `xbg` (`oa_core_pd.sym`, `bg_core_pd.sym`), `xtg0` / `xtg1` (`xgate.sym`, `macros/ocd_analog_switches`) |
| `tp_en_ctrl_b.sch` / `.sym` | stage B: nine enable channels, 56 hv devices (`../../netlist/source/slot7_stage_b.spice`) |
| `slot7_stage_b.sch` / `.sym` | stage B: `xctlb`, reference select `xr_oa` / `xr_bg` / `xr_ib0`, `xtree` (`bias_tree_noab_pd.sym`, `macros/bias_tree_noab_pd`), bias mux `xm_vbp` / `xm_vbpc` / `xm_vbnc` / `xm_vbn`, `xi_ib1` |
| `slot7_testplatform_ab.sch` / `.sym` | the new top: stage A's five instances (as in `slot7_testplatform.sch`) and `xb` (`slot7_stage_b`) |
| `xschemrc` | the one of `../xschem/` with **this** directory instead of `../xschem` (no basename clash with the draft `tp_en_ctrl.sym`) plus the reused macros' directories (`bias_tree_noab_pd` added for stage B) |
| `check_drawn.py` | netlists all five sheets with xschem and compares them with the source netlists |

## Check

```sh
export PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l
python3 check_drawn.py              # RESULT: MATCH
python3 check_drawn.py --selftest   # selftest: PASS (changed labels and missing symbols all detected)
```

`check_drawn.py` netlists each sheet (`--tcl 'set top_is_subckt 1'`, absolute paths, `PWD` set, old netlist deleted
first, `IS MISSING` searched), compares with its source netlist (`slot7_testplatform.spice` for `tp_en_ctrl` and
`slot7_testplatform`, `slot7_stage_b.spice` for the three stage-B sheets) device by device (model,
terminal nets in order, w / l / ng) and the port order of the `.subckt` header, checks that each `.sym` has its pins
in `.subckt` order with the sheet's port names, and lints the drawing (wire ends touching nothing; wire ends of
different nets touching). Result 2026-11-06: `tp_en_ctrl` 43 / 43 devices, `slot7_testplatform` 5 / 5 devices,
0 differences, lint 0 findings, `RESULT: MATCH`. The self-test changes one `lab_pin vdd_1v2` to `vss_1v2` in a copy
(the compare reports `PR0 ... vdd_1v2 vs sheet vss_1v2`), one `lab_wire xb3` to `xb4` in a copy of
`tp_en_ctrl_b.sch` (`PU3`, `NI3`, `PA3`, `NA3` reported), and netlists `slot7_testplatform.sch` and `slot7_stage_b.sch`
with an rc that lacks the reused macros (their `xgate`, core and tree instances `IS MISSING`); all must be detected.
Result 2026-11-07, all five sheets: `tp_en_ctrl` 43 / 43, `slot7_testplatform` 5 / 5, `tp_en_ctrl_b` 56 / 56,
`slot7_stage_b` 10 / 10, `slot7_testplatform_ab` 6 / 6 devices, 0 differences, lint 0 findings, `RESULT: MATCH`;
self-test PASS. Outputs go to `check_out/` (ignored).

## Drawing decisions

- **`tp_en_ctrl`: one row per channel, not one column.** Each channel k is a band between its own `vdd_3v3` rail
  (top) and `vss_3v3` rail (bottom): PU<k> over NI<k> (node xb<k>), then the inverters PA/NA and PB/NB, then the
  read-back PR/NR. So `en<k>_1v2` runs straight from its port to the NI<k> gate and `en<k>`, `en<k>_b`, `rb<k>` run
  straight to their output pins; with channel columns all inputs and outputs would have needed labels or
  staircases across the other channels. The band rails hang on two vertical trunks at the left (`vdd_3v3` x = 120,
  `vss_3v3` x = 140); the PU gates are wired to the `vss_3v3` trunk.
- **Shared stack:** the four NI sources join the vertical `ns1` trunk (x = 300), which runs down to NE / NV in the
  bottom block, under the NI column; `enable` and `vdd_1v2` enter there straight from their ports.
- **Read-back supplies are labels:** PR<k> / NR<k> sit lower in the band so that `en<k>` / `en<k>_b` pass above
  them; their `vdd_1v2` / `vss_1v2` are short rail stubs with a `lab_pin` (8 labels). Wired 1.2 V trunks there
  would cross all twelve band outputs and the eight tie-low outputs. NR bulks are wired to the band's `vss_3v3` rail.
- **Tie-lows:** NRD and NL4..NL11 in one row at the bottom, gates on a `vdd_1v2` rail above the row (NRD's drain
  hangs from it), sources on a `vss_1v2` bus, bulks on the bottom `vss_3v3` rail; the drains run to `lo4..lo11` as
  a staircase (leftmost device on the highest track), so no output crosses another.
- Bulks are a 20-unit stub to x + 40 and a vertical to the rail (as in `d2s_mpdda_pd.sch`); these cross the
  device parameter text. Crossings without dots are not connections.
- **`slot7_testplatform`:** `xctl` at the left, each core in a row with its bus switch (`i_oa` / `i_bg` straight
  from `iout` to `in`), `analog_bus0/1` on the right edge, `dig_out[11:0]` as a straight bundle between the two
  rows. The OA row hangs on the top `vdd_3v3` rail, the BG row stands on the bottom `vss_3v3` rail; the other
  supply pin of each of those four instances is a `lab_pin` (as in the top-level sheet of the d2s pad), because a
  second rail pair would have to cross the bundle. The drawn `tp_en_ctrl.sym` therefore differs from the draft
  symbol in pin **positions** (supplies on the top / bottom edge, the enable pins at the height of the core or
  switch pin they drive, read-back / tie-low pins in the middle), not in pin order or names.
- Internal nets carry `lab_wire` names equal to the source netlist (`xb<k>`, `ns1`, `ns2`, `en_oa`, `i_oa`, ...).
- The coordinates were produced by a placement script in the session and then checked by rendering; the script is
  not committed, so these sheets are the source for hand edits from now on.

## Stage B (2026-11-07)

Same style; the stage-A sheets and symbols above were not changed for it.

- **`tp_en_ctrl_b`:** the `tp_en_ctrl` layout with nine rows and without read-back, tie-lows and NRD. The rows are
  shorter (pitch 480 instead of 660: PMOS row, NMOS row, `en<k>` leaves the second inverter's gate trunk above the
  mid-line, `en<k>_b` its drain trunk below it), because nothing has to pass a read-back inverter. `ns1` is again a
  wired trunk down to NE / NV; their bottom `vss_3v3` rail is the port's rail.
- **`slot7_stage_b`:** `xctlb` at the left; every switch and the tree in its own row, ordered by signal flow: the
  three reference switches, the tree, the four mux switches, the ibias1 switch. Each `tp_en_ctrl_b` output pin
  sits at the height of the track it drives, so every enable is one horizontal plus a short vertical into the
  switch's `ena_b` (from above) or `ena` (from below), or straight into the tree's `en_3v3` / `en_3v3_b`. The
  channel-to-row map: en0 `xr_oa`, en1 `xr_bg`, en2 `xr_ib0`, en3 `xtree`, en4 `xm_vbp`, en6 `xm_vbpc`, en7 `xm_vbnc`,
  en5 `xm_vbn`, en8 `xi_ib1` (mux rows in the order of the tree's output pins, so the pins are not in channel
  order on the symbol).
  - `i_oa`, `i_bg`, `ibias0` cannot cross `xctlb`, so their ports sit at the top of the port column (above
    `vdd_3v3`) and run over `xctlb` and down into the reference switches as a staircase (top line, rightmost
    column); `ibias1` sits at the bottom (below `vss_3v3`) and runs under `xctlb` and up into `xi_ib1`. The
    `tp_en_ctrl_b` symbol therefore has `vdd_3v3` / `vss_3v3` as left-side pins (wired straight to the ports).
  - The reference outputs join on a vertical `iref` trunk into the tree; the tree outputs reach the mux inputs as a
    staircase (higher tree pin, column further right, higher row) and cross the mux enable tracks (16 crossings,
    no dots). The mux outputs join on a vertical `analog_bus2` trunk; its port is on the right edge at mid-height.
  - The supplies of the nine switches and the tree are `lab_pin`s (as in the d2s pad's top sheet): rails top and
    bottom could not reach rows in the middle without crossing every enable track.
- **`slot7_testplatform_ab`:** stage A drawn as in `slot7_testplatform.sch` (same coordinates and the same
  `tp_en_ctrl.sym`), `xb` under it. Its own inputs (`dig_in[12:4]`, `ibias0`, `ibias1`) come straight from the port
  column, `analog_bus2/3` go straight to the right edge; the shared `vdd_3v3`, `vss_3v3`, `vdd_1v2`, `enable` and the
  core outputs `i_oa` / `i_bg` reach it by `lab_pin` (long nets from the stage-A part, which would otherwise cross
  the stage-A port lines and the `dig_out` bundle).
