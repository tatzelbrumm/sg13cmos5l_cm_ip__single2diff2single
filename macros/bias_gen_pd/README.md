<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bias_gen_pd: selectable reference current, without a mirror tree

`bias_sel_pd` without its tree `Xt`: the harness `ibias` through TEN / TEP, the Oguey–Aebischer core `oa_core_pd` and
the Banba core `bg_core_pd`, selected by the same decode (nand2_hv / nor2_hv / inv_hv), into one output `iref`.
Since 2026-10-28 both pads instantiate it next to their tree (`xg` + `xt` in place of `bias_sel_pd` /
`bias_sel_noab_pd`, device for device); the same cell serves the floorplan in which the generator sits in the slot's
main area and only the trees go into the pads. `bias_sel_pd` stays as the combined reference cell with its CACE suite.

| sel1 sel0 | iref |
|---|---|
| 0 0 | harness `ibias` (sourced; 5 uA = iDAC code 20) through TEN / TEP |
| 0 1 | `oa_core_pd` |
| 1 0 | `bg_core_pd` |
| 1 1 | both cores (currents add, about 10 uA) |

`iref` is a *sourced* current: it has to go into an NMOS input diode, i.e. one `bias_tree_pd`, or `bias_dist_pd` to
feed several trees. en_3v3 = 0: both cores off, TEN / TEP open, `iref` high-Z; the receiving tree or `bias_dist_pd`
pulls its own input to vss. Unlike `bias_sel_pd` the block needs no `en_3v3_b` (that was the tree's).

Ports (order): `vdd vss ibias iref en_3v3 sel0_3v3 sel1_3v3`.

## Files

```
schematic/xschem/bias_gen_pd.sch/.sym   bias_sel_pd's sheet (2026-10-25 state) with Xt, its labels, the six bias
                                        outputs, vddo / vsso and en_3v3_b removed, net ir renamed iref, pin iref added
schematic/xschem/xschemrc               adds hv_logic, oa_core_pd, bg_core_pd
netlist/source/bias_gen_pd.spice        source netlist (with ../../bias_tree_pd/netlist/source/bias_ref_pd.spice and
                                        hv_logic.spice)
```

Checked 2026-10-27: xschem's netlist of the sheet against the source subckt, device by device; equal, with TEN / TEP
drawn with drain and source the other way round (as in `bias_sel_pd`'s sheet). Not simulated: no CACE suite yet.
The behaviour is that of `bias_sel_pd` minus the tree; its suite (`sel_params` ... `tran_params`) can be taken over
with a `bias_tree_pd` or replica loads on `iref`.
