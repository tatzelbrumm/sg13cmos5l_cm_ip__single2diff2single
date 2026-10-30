<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bias_tree_pd: mirror tree with the six bias diodes, power-down

Takes one *sourced* reference current into `iref` (NMOS input diode NI behind the transmission gate TGN / TGP, TDN
pulls ni to vss while disabled) and makes the six bias lines of the pad circuits: vbp (5 uA, unit tails), vbpc (2 uA,
mirror cascodes), vabp (5 uA, RP2 on RP1), vbn (5 uA, fold sinks), vbnc (2 uA, fold cascodes), vabn (5 uA, RN2 on
RN1). RP1 / RN1 sit on the output-stage rails vddo / vsso (the class-AB replicas of OP / ON).

This is the part that goes into a pad. Its reference comes either from the selector next to it (`bias_sel_pd`, the
generator in the pad) or from the slot's main area (`bias_gen_pd`, optionally through `bias_dist_pd`).

Ports (order): `vdd vss vddo vsso iref vbp vbn vbpc vbnc vabp vabn en_3v3 en_3v3_b`.

## Files

```
schematic/xschem/bias_tree_pd.sch/.sym   the tree sheet, cut on 2026-10-20 from the flat sheet of bias_in_pd (then
                                         d2s_bias_in_tree_pd); moved here and renamed on 2026-10-27
schematic/xschem/xschemrc                self-contained (copy of bias_bg_pd's)
netlist/source/bias_ref_pd.spice         source netlists of the whole bias family with power-down: d2s_bias_diodes,
                                         inv_3v3_pd, bias_tree_pd, bias_in_pd, bias_out_pd, oa_core_pd, bias_oa_pd,
                                         bg_core_pd, bias_bg_pd
netlist/source/bias_ref.spice            the same without power-down (d2s_bias_in / _out / _oa / _bg, oa_core, bg_core)
netlist/source/bias_lp.spice             d2s_bias_lp, the bias fixture with ideal currents used by d2s_mpdda.spice
```

The three netlists moved here on 2026-10-27 from `sg13cmos5l_IOPadDiff2Single/netlist/source` (then
`d2s_bias_ref_pd.spice`, `d2s_bias_ref.spice`, `d2s_bias_lp.spice`); every include in both pads' testbenches follows.
Inside them only the cell names changed (`d2s_bias_in_tree_pd` -> `bias_tree_pd`, `d2s_bias_*_pd` -> `bias_*_pd`);
the helper subcircuits keep their names (`d2s_bias_diodes`, `d2s_bias_lp`, `d2s_bias_in` / `_out` / `_oa` / `_bg`).

No CACE suite of its own: the tree is characterized in `bias_in_pd` (external reference) and in `bias_sel_pd`.
