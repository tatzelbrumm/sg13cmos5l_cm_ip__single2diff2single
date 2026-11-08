<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# hv_logic: minimal 3.3 V static CMOS gates (sg13_hv)

IHP's IO library has only 1.2 V (sg13_lv) logic cells (`sg13cmos5l_io_inv_x1`, `_nand2_x1`, `_nor2_x1`), and the
standard-cell library is 1.2 V as well, so the 3.3 V control logic of the pad circuits uses these four gates.
All devices are 1u / 0.45u sg13_hv (NOR stacks: 2u resp. 3u PMOS), the size of the power-down inverters of
`d2s_bias_*_pd` / `d2s_mpdda_pd`.

| cell | function | ports (order) | devices |
|---|---|---|---|
| `inv_hv` | y = not a | `vdd vss a y` | 2 |
| `nand2_hv` | y = not (a and b) | `vdd vss a b y` | 4 |
| `nor2_hv` | y = not (a or b) | `vdd vss a b y` | 4 |
| `nor3_hv` | y = not (a or b or c) | `vdd vss a b c y` | 6 |
| `tg_hv` | transmission gate: a ↔ b while en = 1 / en_b = 0 (bulks on vss / vdd) | `vdd vss en en_b a b` | 2 |

Used by `macros/en_ctrl_3v3` (inv_hv, nor3_hv), `macros/bias_sel_pd` (decoder: nand2_hv, nor2_hv, inv_hv) and
`macros/bias_dist_pd` (bdp_slice: nand2_hv, inv_hv, tg_hv). tg_hv (2026-11-08) is the project's standard 1u / 0.45u
transmission gate made a cell after agent D's layout cell of the same name in bias_dist_pd; its layout lives there
(`../bias_dist_pd/layout/klayout/bias_dist_pd.klay.gds`, cell `bdp_tg_hv`, next to `bdp_inv_hv` and `bdp_nand2_hv`).

- `netlist/source/hv_logic.spice`: the source netlist.
- `schematic/xschem/*.sch / *.sym`: one sheet per gate, PMOS above, NMOS below, nets by label; box symbols with the
  pins in subcircuit port order (inputs left, y right, vdd top, vss bottom).
- Checked 2026-10-20 (cloud, xschem 3.4.8RC `ddc7344`): each sheet netlists to its source subcircuit, device by
  device (model, terminals, w / l / ng / m, port order), with no missing symbols.
- No CACE suite: the gates are characterized as part of `en_ctrl_3v3` and `bias_sel_pd`. `make sim-cace` does nothing here.
- No layout yet.
- **For the hv standard-cell set** (Christoph, 2026-11-08: "the off grid symbols become important once I have you build
  a set of standard cells"): put every cell symbol's pins on the 20-unit grid, with supply pins off center (vdd top at
  x −20, vss bottom at x +20, as in `bias_dist_pd.sym` and `bdp_slice.sym`) so vertical supply lines can run through
  stacked symbols without crossing. Off the grid today: `nand2_hv.sym`, `nor2_hv.sym`, `tg_hv.sym` here, and
  `bdp_slice.sym` (`en_3v3`, `en`, `a`, `b`, and vdd / vss at y ∓70) in `macros/bias_dist_pd`. Moving pins detaches
  the wires of every sheet that places the symbol (today `bdp_slice.sch`, `bias_dist_pd.sch`, `bias_gen_pd.sch`,
  `bias_sel_pd.sch`, `bias_sel_noab_pd.sch`); re-wire and check each with `scripts/xschem/sheet_equiv.py`.
