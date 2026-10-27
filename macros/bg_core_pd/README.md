<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bg_core_pd: Banba current-mode bandgap core with power-down

The reference core of `bias_bg_pd`: a current-mode (Banba type) bandgap without op-amp, pnpMPA (Q2 = 8 x Q1) and rhigh.
Each branch carries V_BE1 / R1 + U_T ln 8 / R0 = 2.5 uA; PO / POC deliver twice that, about 5 uA, *sourced* out of
`iout` into an NMOS input diode: a `bias_tree_pd`, or an input of `bias_dist_pd`. Flat over temperature and MOS
corners, it follows the rhigh corners (about -20 % / +30 %, `bias_bg_pd/README.md`).

Ports (order): `vdd vss iout en_3v3 en_3v3_b`. Disabled as `oa_core_pd`: MS1 off, SKS and SVPG on, `iout` high-Z.

## Files

```
schematic/xschem/bg_core_pd.sch/.sym   the core, cut on 2026-10-20 from the flat sheet of bias_bg_pd (dangling wires
                                       removed 2026-10-22); moved here unchanged on 2026-10-27 from
                                       macros/d2s_bias_sel_pd/schematic/xschem
schematic/xschem/xschemrc              self-contained (copy of bias_bg_pd's)
```

Source netlist: `../bias_tree_pd/netlist/source/bias_ref_pd.spice`, subckt `bg_core_pd`. Used by `bias_sel_pd` and `bias_gen_pd`.
No CACE suite of its own: the core is characterized in `bias_bg_pd` (with the tree) and in `bias_sel_pd` (code 10).
