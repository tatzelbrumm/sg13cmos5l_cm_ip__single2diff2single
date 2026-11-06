<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# slot7_testplatform: finished-style sheets

Redraws of the draft sheets in `../xschem/` (one labelled stub per terminal, from `gen_sheets.py`) in the finished
analog style of the `xschem-analog-schematic` skill: ports in one column at the far left, outputs on the right edge,
rails as wires, one column per current branch, real orthogonal wires, `lab_pin` only for long nets. Written
2026-11-06 (cloud session). **The draft sheets in `../xschem/` are unchanged**, so both can be compared and this
version adopted (copy the four `.sch` / `.sym` files over, or put this directory first on the library path).

| file | what |
|---|---|
| `tp_en_ctrl.sch` / `.sym` | the enable cell, 43 hv devices, same cell name, ports and port order as the source |
| `slot7_testplatform.sch` / `.sym` | `xctl` (`tp_en_ctrl.sym` from here), `xoa` / `xbg` (`oa_core_pd.sym`, `bg_core_pd.sym`), `xtg0` / `xtg1` (`xgate.sym`, `macros/ocd_analog_switches`) |
| `xschemrc` | the one of `../xschem/` with **this** directory instead of `../xschem` (no basename clash with the draft `tp_en_ctrl.sym`) plus the reused macros' directories |
| `check_drawn.py` | netlists both sheets with xschem and compares them with the source netlist |

## Check

```sh
export PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l
python3 check_drawn.py              # RESULT: MATCH
python3 check_drawn.py --selftest   # selftest: PASS (changed label and missing symbols both detected)
```

`check_drawn.py` netlists each sheet (`--tcl 'set top_is_subckt 1'`, absolute paths, `PWD` set, old netlist deleted
first, `IS MISSING` searched), compares with `../../netlist/source/slot7_testplatform.spice` device by device (model,
terminal nets in order, w / l / ng) and the port order of the `.subckt` header, checks that each `.sym` has its pins
in `.subckt` order with the sheet's port names, and lints the drawing (wire ends touching nothing; wire ends of
different nets touching). Result 2026-11-06: `tp_en_ctrl` 43 / 43 devices, `slot7_testplatform` 5 / 5 devices,
0 differences, lint 0 findings, `RESULT: MATCH`. The self-test changes one `lab_pin vdd_1v2` to `vss_1v2` in a copy
(the compare reports `PR0 ... vdd_1v2 vs sheet vss_1v2`) and netlists the top sheet with an rc that lacks the
reused macros (`xoa`, `xbg`, `xtg0`, `xtg1` `IS MISSING`); both must be detected. Outputs go to `check_out/`
(ignored).

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
