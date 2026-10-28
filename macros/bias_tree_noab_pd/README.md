<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bias_tree_noab_pd: mirror tree without the class-AB branches, power-down

`bias_tree_pd` without NABP and PABN (2026-10-27): one sourced reference current into `iref` (NI behind the transmission
gate TGN / TGP, TDN pulls ni to vss while disabled), four bias lines vbp (5 uA), vbpc (2 uA), vbn (5 uA), vbnc (2 uA)
with their diodes BP, BPC, BN, BNC. For the s2d pad, whose buffer `s2d_mpdda_pd` uses these four lines only; with
`bias_tree_pd` its unused class-AB legs drew 10 uA.

Ports (order): `vdd vss iref vbp vbn vbpc vbnc en_3v3 en_3v3_b`.

## Files

```
schematic/xschem/bias_tree_noab_pd.sch/.sym   bias_tree_pd's sheet with NABP, PABN and the columns [8] vabp / [8] vabn
                                              taken out, the columns to their right moved left
schematic/xschem/xschemrc                     copy of bias_tree_pd's
netlist/source/bias_tree_noab_pd.spice        source netlist; uses bias_diodes of ../bias_tree_pd/netlist/source/bias_ref_pd.spice
```

Used by `sg13cmos5l_IOPadSingle2Diff` (`xt`, next to `xg` = `bias_gen_pd`, since 2026-10-28) and by
`bias_sel_noab_pd`; with the generator in the slot's main area it takes `bias_gen_pd`'s or `bias_dist_pd`'s current
like `bias_tree_pd`. Sheet and source netlist agree device by device (2026-10-27).
No CACE suite of its own; not simulated on its own.
