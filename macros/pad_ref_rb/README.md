<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# pad_ref_rb: replica bias of the custom pads' reference voltages, one shared bias tree

One cell gives both reference voltages of the custom pads:
- `vcm`: S2D `vcm` = D2S `vref`, from `../vcm_rb`;
- `vref`: S2D `vref`, from `../vref_s2d_rb`.

Both blocks hang on one bias tree, `bias_tree_rb`, made from one 5 µA reference current, with one enable. This is
option A of Christoph's question of 2026-11-07, whether the two blocks could share their bias voltage generation.
Before that, each block carried its own copy of the tree and took its own reference current.

Task: `docs/launch/replica_bias_TASK.md` (branch `harness-test`). Records: `docs/replica_bias/` (RUNLOG Phase 2b).

## Cells

| cell | where | what |
|---|---|---|
| `bias_tree_rb` | `netlist/source/pad_ref_rb.spice`, `schematic/xschem/bias_tree_rb.sch` | TGN / TGP / TDN (reference switch, as bias_tree_pd), NI 6u/6u (`ni`), NBP 2.4u/6u → BP 2u/6u (`vbp`), PBNC 2u/6u → BNC 1u/8u (`vbnc`); TGP drawn with drain ni, source iref as Christoph drew it |
| `vcm_rb` | `../vcm_rb` | top-edge detector, fold-node replica, average, unit-device OTA buffer; takes `ni vbp vbnc` |
| `vref_s2d_rb` | `../vref_s2d_rb` | x-node replica follower (4 × 15u/3u) with its sink and bypass; takes `ni vbnc` |
| `pad_ref_rb` | `schematic/xschem/pad_ref_rb.sch` | Xt (tree), Xc (vcm_rb), Xr (vref_s2d_rb) |

**Why sharing costs nothing at DC:** the tree's lines drive gates only. Every DC result is the same as with two own
trees to the last printed digit (rb_dc, the closed loops, the round trip, the S2D window; RUNLOG row 38).

## Ports

| port | dir | |
|---|---|---|
| vdd, vss | inout | the rail of the pads' units. vcm_rb's top edge is referenced to it, so it must be the pads' own iovdd / iovss (custom-pad route: the padframe rails; slot fallback: vdd_3v3 / vss_3v3) |
| iref | in | 5 µA, **sourced** into the cell (NMOS diode NI behind TGN / TGP): a `bias_dist_pd` output fed from the same source as the pads' own iref, so that the replica tracks the pads' reference current |
| vcm | out | to S2D `vcm` and D2S `vref` (gates, plus the S2D's output ties while it is off) |
| vref | out | to S2D `vref` (gates only) |
| en_3v3, en_3v3_b | in | 3.3 V enable and complement (en_ctrl_3v3). Disabled: every current off, vcm and vref pulled to vss. Keep it on while any user of vcm runs |

## Results (schematic, ngspice-47, CACE 2.11.0, 2026-11-07)

CACE `verification/cace/results/pad_ref_rb/`: 8 / 8 groups pass.

| quantity | result | condition |
|---|---|---|
| vcm | 1.120 … 1.193 / 1.242 … 1.295 / 1.289 … 1.395 V | iovdd 3.0 / 3.3 / 3.6 V, 5 MOS corners, −40 / 27 / 125 °C, harness reference |
| vcm, other references | 1.117 … 1.204 V | OA core / bandgap core, 3.0 V (band 1.126 … 1.244 V with the OA core at 125 °C) |
| vref | 0.436 … 0.455 / 0.483 … 0.504 / 0.572 … 0.596 V | −40 / 27 / 125 °C, all corners and supplies |
| supply current | 19.1 µA (tree 3.9, vcm_rb 13.6, vref_s2d_rb 1.6) + 5.0 µA reference = 24.1 µA; the two blocks with own trees took 33 µA | tt, 27 °C, 3.3 V |
| supply current, all PVT | 18.7 … 19.5 µA without the reference; OA core 11.5 … 28.0 µA | |
| mismatch | vcm σ 5.3 mV, vref σ 3.7 mV (100 seeds) | tt, 27 °C, 3.3 V |
| disabled | vcm, vref 0.000 V; ≤ 10 nA | 3.6 V, tt / ff, 27 / 125 °C |
| enable | vcm 0.31 … 1.00 µs, overshoot ≤ 37 mV; vref 0.34 … 1.17 µs (OA core: the core's start-up, ≤ 25 µs) | |
| closed loop | S2D INL ≤ 1.73 mV, D2S INL ≤ 1.72 mV, round trip INL ≤ 0.75 mV, S2D enable 1.39 … 1.45 µs, S2D pad range 0 … ≥ 1.09 V up to 27 °C: all as with the own trees | `../vcm_rb/testbenches/rb_char/results/` |

**Against dividers** (same outputs and output impedances, tt / 27 °C / 3.3 V): two dividers draw 28.8 + 19.9 =
48.7 µA, this cell 24.1 µA including its reference (0.5×). The dividers cannot track the band or the S2D input edge
and cannot be switched off (`docs/replica_bias/SUMMARY.md`).

## Files

```
netlist/source/pad_ref_rb.spice     bias_tree_rb and pad_ref_rb (with ../../../vcm_rb, ../../../vref_s2d_rb netlists)
schematic/xschem/                   bias_tree_rb.sch / .sym, pad_ref_rb.sch / .sym, xschemrc (library paths of both blocks)
schematic/*.png / .svg              renders of the two sheets
verification/gen_cace.py            writes the CACE suite (pins read from pad_ref_rb.sym)
verification/cace/                  pad_ref_rb.yaml, templates/, results/pad_ref_rb/
layout/primitives/                  layout primitives collected from the s2d pad cell, row plan, area estimate
Makefile                            from oa_core_pd's (gen: ../vcm_rb/gen_makefiles.py): sim-cace, check-sheet
                                    (pad_ref_rb and bias_tree_rb), sim-char
```

`make check-sheet` netlists both sheets with xschem and compares them with the source netlist: devices (bias_tree_rb
8 = 8) and subcell instances (pad_ref_rb 3 = 3), ports equal. The sheets of the two blocks are checked from their
own macros (16 = 16, 8 = 8). The whole hierarchy flattened is topology-equivalent to the source (32 devices).

## Open points

- **Layout:** primitives collected (`layout/primitives/README.md`); assembly, routing, DRC / LVS not started.
  Decisions open there: flat LVS of pad_ref_rb, the tree row's spare 5/6 slot.
- **Bias current:** the iref leg comes from `bias_dist_pd` (3 inputs, 4 switchable 1 : 1 outputs: S2D, D2S, this
  cell, a spare). That cell is a sheet only, never simulated, without layout. The decks so far feed this cell from
  its own `bias_gen_pd` with the pads' selection: the ideal case, without leg-to-leg mismatch.
- **Bypass capacitors:** at vref the 12u × 12u NMOS capacitors give 0.20 … 0.43 pF each. More capacitance (room at
  the bottom of slot 7) and its rail are open: a PMOS to iovdd gives 0.64 pF at any voltage but couples iovdd into
  the node; for vcm that is acceptable, for vref (the S2D's zero point) a supply-rejection comparison should decide.
