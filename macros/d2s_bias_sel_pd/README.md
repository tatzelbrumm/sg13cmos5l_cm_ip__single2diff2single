<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# d2s_bias_sel_pd: pad-driver bias with a selectable reference current

The bias of `d2s_mpdda_pd` (the class-AB pad driver) inside `sg13cmos5l_IOPadDiff2Single`. One mirror tree with the
six bias diodes (`d2s_bias_in_tree_pd`, the tree of `d2s_bias_in_pd`) is fed by one of three reference currents:

| sel1 sel0 | reference into the tree | |
|---|---|---|
| 0 0 | harness `ibias` through a transmission gate (TEN / TEP) | the harness iDAC *sources* its current (PMOS, 250 nA per code step, `sg13cmos5l_ocd_ip__biasgen2`), hence the `_in` topology (NMOS input diode NI); 5 uA = code 20 |
| 0 1 | Oguey-Aebischer core `oa_core_pd` | no resistor, no BJT |
| 1 0 | bandgap core `bg_core_pd` | rhigh + pnpMPA |
| 1 1 | both cores | currents add (about 2x bias) |

en_3v3 = 0 switches everything off: the tree's own TG and TDN, both cores (MS1, SKS, SVPG), and TEN / TEP.
`en_3v3_b` = NOT en_3v3 comes in as a port, from `XIB` in `en_ctrl_3v3` (until 2026-10-25 the local inverter `Xi`
= `inv_3v3_pd` made it here). The CACE templates carry Xi's two devices in their code block (XIBP / XIBN, same vdd
and ground), so the results below still hold: nominal dc (sel 0-3 enabled, sel 3 disabled) and tran identical.
A disabled core's output (POC drain) is off, so the cores share the tree input `ir` without a switch.
`d2s_bias_out_pd` (external NMOS sink) is not used here: nothing in the slot sinks a reference current.

Ports (order): `vdd vss vddo vsso ibias vbp vbn vbpc vbnc vabp vabn en_3v3 sel0_3v3 sel1_3v3 en_3v3_b`.
In the pad cell vdd = vddo = iovdd and vss = vsso = iovss; RP1 / RN1 still need Kelvin connections to OP's / ON's
source rails (see `bias.md` in the notes worktree, `design_considerations/class_ab_pad_driver/improvements/`).

## Files

```
netlist/source/d2s_bias_sel_pd.spice     source netlist (uses d2s_bias_ref_pd.spice in
                                         ../sg13cmos5l_IOPadDiff2Single/netlist/source, and hv_logic.spice)
schematic/xschem/d2s_bias_sel_pd.sch/.sym       top sheet (label style) and symbol
schematic/xschem/d2s_bias_in_tree_pd.sch/.sym   tree + the six diodes: d2s_bias_in_pd's sheet without its inverter
schematic/xschem/oa_core_pd.sch/.sym, bg_core_pd.sch/.sym   the cores, cut from d2s_bias_oa_pd / d2s_bias_bg_pd
schematic/xschem/inv_3v3_pd.sch/.sym     unused since 2026-10-25 (en_3v3_b is a port); kept
verification/cace/d2s_bias_sel_pd.yaml   CACE suite, groups below
verification/cace/results/d2s_bias_sel_pd/   CSV and CACE summaries of the last `make sim-cace`
```

The sub-sheets keep the device placement and wiring of the hand-edited flat sheets in `macros/d2s_bias_*_pd`
(cut out of them: devices of the other blocks removed, dangling wires pruned, port pins added). The six bias
diodes are drawn inline in the tree sheet, interleaved column by column as in the flat sheet, not as a separate
`d2s_bias_diodes` sheet. Every sheet netlists to the source subcircuits device by device (checked 2026-10-20).

| group | what | runs |
|---|---|---:|
| sel_params | each code at tt, 27 C, 3.3 V, ibias 5 uA | 4 |
| pvt_params | codes 0 / 1 / 2, 5 MOS corners x -40 / 125 C | 30 |
| supply_params | codes 0 / 1 / 2 at vdd = vddo = 3.0 / 3.3 / 3.6 V | 9 |
| rpnp_params | code 2 at rhigh wcs / bcs x pnpMPA wcs / bcs | 4 |
| iref_params | code 0 at ibias = 2.5 / 5 / 7.5 uA (iDAC codes 10 / 20 / 30) | 3 |
| pd_params | disabled, codes 0 / 3 at tt / ff x 27 / 125 C | 8 |
| tran_params | settling: enable with sel 0 / 1 / 2; sel 0->1, 1->2, 2->0; at ss / tt / ff, 27 C | 18 |

The six bias currents are measured as drain currents of replica loads: one copy of each bias diode with its gate on
the bias line and its drain forced to the gate voltage by an ideal buffer. The harness iDAC is modelled as a PMOS
mirror on its own 3.3 V supply. Limits are proposals (worst case + ~30 %).

## Results (CACE, schematic netlist, 2026-10-20)

Design currents 5 / 5 / 2 / 2 / 5 / 5 uA (vbp, vbn, vbnc, vbpc, vabp, vabn); percentages below are against them.
vbn, vabp and vabn follow vbp within 1 % in every run; vbnc and vbpc sit at +4 / -3 % of their 2 uA design value
(the mirror ratios of the tree) and follow vbp likewise. Full numbers: the CSV files.

| | harness ibias (00) | Oguey-Aebischer (01) | bandgap (10) |
|---|---|---|---|
| vbp current, tt 27 C | 5.06 uA | 5.05 uA | 5.06 uA |
| over 5 MOS corners x -40 / 125 C | 5.05-5.08 uA (+1.0 ... +1.6 %) | 3.10-7.11 uA (-38 / +42 %) | 4.97-4.99 uA (-0.6 ... -0.2 %) |
| rhigh / pnpMPA corners | - | - | 4.00-6.49 uA (-20 / +30 %, rhigh dominates) |
| vdd 3.0 -> 3.6 V | +0.4 % | +0.6 % | +0.6 % |
| supply current of the cell, tt 27 C | 19.2 uA | 27.4 uA | 29.7 uA |

- Code 11 (both cores): 10.06 uA on vbp, 56.9 uA from vdd.
- Harness code scales as expected: ibias 2.5 / 5 / 7.5 uA gives 2.55 / 5.06 / 7.57 uA on vbp.
- Disabled (en_3v3 = 0): vdd 4.9 nA worst (ff, 125 C), every bias current <= 0.14 nA, vddo 0.05 nA, ibias pin
  0.02 nA.
- With code 01 / 10 at 125 C the harness mirror (still sourcing into the opened TG) pulls ibias up to its rail: the
  `I ibias` column of pvt_params shows leakage of up to 0.13 nA through TEN / TEP there.

Settling of vbp to 1 % of its final value (ss / tt / ff, 27 C, report only):

| event | harness (00) | Oguey-Aebischer (01) | bandgap (10) |
|---|---|---|---|
| enable (en_3v3 0 -> 1) | 0.21-0.22 us | 24-29 us | 0.36-0.38 us |
| sel change into this code | 0.14 us (from 10) | 24 us (from 00) | 0.37 us (from 01) |

The Oguey-Aebischer core is the slow one, consistent with the power-down session's start-up results for
d2s_bias_oa_pd (I_Q within 10 % after 8-15 us); the cause was not investigated here.

Not done: layout, extraction, Monte Carlo (the source decks in the notes worktree have it for the separate
variants: `run_bias.py mc`), PSRR per rail (also in `run_bias.py`), start-up from a 0 V supply ramp.
