<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# oa_core_pd: Oguey–Aebischer reference-current core with power-down

The reference core of `bias_oa_pd`: no resistor, no BJT (M10 / M11 in weak inversion, vres = U_T ln 16). Its output
`iout` (the POC drain) *sources* about 5 uA into an NMOS input diode: a `bias_tree_pd`, or an input of `bias_dist_pd`.
The current is proportional to mu T^2, about -35 % / +35 % over -40 ... 125 C (`bias_oa_pd/README.md`).

Ports (order): `vdd vss iout en_3v3 en_3v3_b`. Disabled (en_3v3 = 0): MS1 off (gate en_3v3_b), SKS pulls ks to vss,
SVPG pulls vpg to vdd, so PO / POC are off and `iout` is high-Z; disabled cores can share one output node.

## Files

```
schematic/xschem/oa_core_pd.sch/.sym   the core, cut on 2026-10-20 from the flat sheet of bias_oa_pd; moved here
                                       unchanged on 2026-10-27 from macros/d2s_bias_sel_pd/schematic/xschem
schematic/xschem/xschemrc              self-contained (copy of bias_bg_pd's)
layout/gds/oa_core_pd.gds              layout, 2026-10-28: the six OA primitives of ../IOPad/layout/klayout/
                                       pad_buffer_cells.gds (unchanged) placed and wired for the core side of slot 7;
                                       76.00 x 50.74 um, Metal1 / Metal2 only
```

**Layout (2026-10-28).** Built by script from the primitives; vdd rail (Metal1) on top, vss rail at the bottom, iout and
en_3v3 as Metal2 pins on the top edge, en_3v3_b on the right edge. Checked with a Python subset of IHP's DRC rules
(0 violations) and a klayout.db extraction against the sheet's netlist with MS1 split and the dummies added (match,
27 devices); not yet with IHP's own decks (`make klayout-drc` / `make klayout-lvs` here). LVS against the sheet itself
will flag MS1 (8 x 0.5/12.5 in series in the layout) and the 10 dummies, and may flag M10 / M11 (18 / 9 fingers of
10/1 in the layout, ng 8 / 4 in the sheet), until the sheet adopts them. Build script, checks,
renders and report: `_sudelbuecher/sudelbuecher/design_considerations/pad_buffer_layout/oa_core_pd_2026-10-28/`.

Source netlist: `../bias_tree_pd/netlist/source/bias_ref_pd.spice`, subckt `oa_core_pd`. Used by `bias_sel_pd` and `bias_gen_pd`.
No CACE suite of its own: the core is characterized in `bias_oa_pd` (with the tree) and in `bias_sel_pd` (code 01).
