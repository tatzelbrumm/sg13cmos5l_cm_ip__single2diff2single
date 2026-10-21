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

Used by `macros/en_ctrl_3v3` (inv_hv, nor3_hv) and `macros/d2s_bias_sel_pd` (decoder: nand2_hv, nor2_hv, inv_hv).

- `netlist/source/hv_logic.spice`: the source netlist.
- `schematic/xschem/*.sch / *.sym`: one sheet per gate, PMOS above, NMOS below, nets by label; box symbols with the
  pins in subcircuit port order (inputs left, y right, vdd top, vss bottom).
- Checked 2026-10-20 (cloud, xschem 3.4.8RC `ddc7344`): each sheet netlists to its source subcircuit, device by
  device (model, terminals, w / l / ng / m, port order), with no missing symbols.
- No CACE suite: the gates are characterized as part of `en_ctrl_3v3` and `d2s_bias_sel_pd`. `make sim-cace` does nothing here.
- No layout yet.
