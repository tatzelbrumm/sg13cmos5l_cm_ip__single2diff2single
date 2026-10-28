<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bias_sel_noab_pd: the s2d pad's bias, selectable reference, no class-AB lines

`bias_sel_pd` with `bias_tree_noab_pd` in place of `bias_tree_pd` (2026-10-27): the same reference selection (harness
`ibias` through TEN / TEP, Oguey-Aebischer core, bandgap core, both), the same enable, four bias lines vbp vbn vbpc
vbnc. `sg13cmos5l_IOPadSingle2Diff` (top sheet and the CACE fixture `s2d_mpdda_pd_sel`) uses it instead of
`bias_sel_pd`, whose vabp / vabn stayed unused there. Since 2026-10-28 the pad has `bias_gen_pd` + `bias_tree_noab_pd`
side by side instead (same devices); this cell is kept as the combined reference.

Ports (order): `vdd vss ibias vbp vbn vbpc vbnc en_3v3 sel0_3v3 sel1_3v3 en_3v3_b`; the symbol is `bias_sel_pd`'s without
the vabp / vabn pins, so the pads' wiring stayed.

## Files

```
schematic/xschem/bias_sel_noab_pd.sch/.sym   bias_sel_pd's sheet with the tree swapped and the vabp / vabn outputs removed
schematic/xschem/xschemrc                    copy of bias_sel_pd's, with bias_tree_noab_pd as dependency
netlist/source/bias_sel_noab_pd.spice        source netlist (uses bias_ref_pd.spice, bias_tree_noab_pd.spice, hv_logic.spice)
```

Checked 2026-10-27: sheet and source netlist are `bias_sel_pd`'s minus NABP / PABN, device by device. No CACE suite
of its own yet; `bias_sel_pd`'s suite covers everything but the two missing legs.
