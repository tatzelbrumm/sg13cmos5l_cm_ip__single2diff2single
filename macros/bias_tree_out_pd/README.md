<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bias_tree_out_pd: mirror tree for a reference current out of iref, power-down

The opposite-polarity twin of `bias_tree_pd` (2026-10-28). `iref` *sinks* the reference: the current flows out of
`iref` into an NMOS sink outside. The circuit is `bias_out_pd`, the precedent for this polarity ("mirror image of
`bias_in_pd`"), without its inverter IP / IN; `en_3v3_b` is a port, as for `bias_tree_pd`.

- **Input:** PI is a PMOS input diode, a copy of BP (5u / 6u). It sits behind the transmission gate TGN / TGP; TDP
  pulls pi to vdd while disabled.
- **Mirrors:** PI's gate line pi drives the PMOS sources PBN, PBNC and PABN into BN, BNC and vabn. BN's gate line
  vbn drives the NMOS sinks NBP, NBPC and NABP from BP, BPC and vabp.
- **Outputs:** the same bias voltages and currents as `bias_tree_pd`: vbp 5 uA, vbpc 2 uA, vbn 5 uA, vbnc 2 uA,
  and vabp / vabn 5 uA each, from the same four diodes (`bias_diodes`).

Ports (order): `vdd vss iref vbp vbn vbpc vbnc vabp vabn en_3v3 en_3v3_b`. The ports, their order and the symbol are
`bias_tree_pd`'s, so the two trees swap in a sheet without rewiring. Only the reference's direction differs.

What it is for: a current distribution between reference block(s) and the pads' trees.
- With `bias_tree_pd` (NMOS input diode), the distribution has to *source* the copies.
  - `bias_dist_pd` does that: NI (NMOS diode) → NM → PD (PMOS diode) → PO0..3.
  - That is two mirrors between the reference and the tree.
- With this tree, a distribution can hand out copies straight from its NMOS input mirror (NMOS sinks, one per tree).
  - That saves one mirror stage, and its mismatch.
  - Each tree's PMOS input diode is then the second half of the copy.
  - Not built: a `bias_dist_pd` variant with NMOS outputs would be the counterpart.

## Files

```
schematic/xschem/bias_tree_out_pd.sch/.sym   bias_out_pd's sheet without IP / IN (and their wiring), en_3v3_b as an
                                             input pin; the symbol is bias_tree_pd's with its own description
schematic/xschem/xschemrc                    copy of bias_tree_noab_pd's
netlist/source/bias_tree_out_pd.spice        source netlist: bias_out_pd's subckt without Xi; uses bias_diodes of
                                             ../bias_tree_pd/netlist/source/bias_ref_pd.spice
Makefile.new                                 bias_tree_noab_pd's Makefile with TOP = bias_tree_out_pd (rename to Makefile)
```

Checked 2026-10-28:
- xschem's netlist of the sheet equals the source subckt device by device (14 devices);
- the symbol's pin order equals the source's port order;
- `bias_out_pd` = `inv_3v3_pd` + `bias_tree_out_pd` (flattened, 16 devices).

Not simulated on its own and no CACE suite; `bias_out_pd`'s suite characterizes the same tree with its inverter.
Not used by any sheet yet.
