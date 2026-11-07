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
| `bias_tree_rb` | `netlist/source/pad_ref_rb.spice`, `schematic/xschem/bias_tree_rb.sch` | TGN / TGP / TDN (reference switch, as bias_tree_pd), NI 6u/6u (`ni`), NBP 2.4u/6u → BP 2u/6u (`vbp`), PBNC 2u/6u → BNC 1u/8u (`vbnc`); TGP drawn with drain ni, source iref as Christoph drew it; layout dummies: MDPBN 5u/6u (D = S = B = vdd, gate vbp) in the PBN slot of the copied pad tree row; MDTN6 2u/6u, MDTN7 2.4u/6u (D = S = B = vss, gate ni) in the NMOS tree row rb_tree_n |
| `vcm_rb` | `../vcm_rb` | top-edge detector, fold-node replica, average, unit-device OTA buffer; takes `ni vbp vbnc` |
| `vref_s2d_rb` | `../vref_s2d_rb` | x-node replica follower (4 × 15u/3u) with its sink; takes `ni vbnc`; no capacitor |
| `bypass_rb` | `netlist/source/pad_ref_rb.spice`, `schematic/xschem/bypass_rb.sch` | the bypass capacitors, in a cell of their own (Christoph, 2026-11-07): CBM 4 × and CBR 9 × 12u × 12u hv NMOS to vss on vcm and vref (ncm, ncr; the 9th vref capacitor sits in the layout's rb_cload, the pad's CLN slot; Christoph: "I don't see any reason how a 9th capacitor should hurt"). vcm_rb keeps its CB, the minimum for its buffer's phase margin; vref_s2d_rb needs none (a follower, no loop) |
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
| enable | vcm 0.64 … 1.32 µs, overshoot ≤ 34 mV (OA core ≤ 0.28 V); vref 0.39 … 1.29 µs (OA core: the core's start-up, ≤ 25 µs) | with bypass_rb |
| S2D enable kick | vcm ≤ 0.112 V, vref ≤ 0.096 V (without bypass_rb 0.236 / 0.212 V); S2D enable time 1.44 µs either way | references on before the pad |
| output impedance | vcm 21 … 35 kΩ, vref 18 … 26 kΩ (1 kHz / 1 MHz) | |
| stability, each block alone | vcm_rb's buffer: no peaking without load, ≤ 1.25 with 50 … 200 fF, ≤ 1.09 with its CB at any load; vref_s2d_rb: no loop | `explore_stability.py` |
| closed loop | S2D INL ≤ 1.73 mV, D2S INL ≤ 1.72 mV, round trip INL ≤ 0.75 mV, S2D enable 1.39 … 1.45 µs, S2D pad range 0 … ≥ 1.09 V up to 27 °C: all as with the own trees | `../vcm_rb/testbenches/rb_char/results/` |

**Against dividers** (same outputs and output impedances, tt / 27 °C / 3.3 V): two dividers draw 28.8 + 19.9 =
48.7 µA, this cell 24.1 µA including its reference (0.5×). The dividers cannot track the band or the S2D input edge
and cannot be switched off (`docs/replica_bias/SUMMARY.md`).

## Files

```
netlist/source/pad_ref_rb.spice     bias_tree_rb and pad_ref_rb (with ../../../vcm_rb, ../../../vref_s2d_rb netlists)
schematic/xschem/                   bias_tree_rb.sch / .sym, bypass_rb.sch / .sym, pad_ref_rb.sch / .sym, xschemrc
schematic/*.png / .svg              renders of the two sheets
verification/gen_cace.py            writes the CACE suite (pins read from pad_ref_rb.sym)
verification/cace/                  pad_ref_rb.yaml, templates/, results/pad_ref_rb/
layout/primitives/                  layout primitives collected from the s2d pad cell, row plan, area estimate
Makefile                            from oa_core_pd's (gen: ../vcm_rb/gen_makefiles.py): sim-cace, check-sheet
                                    (pad_ref_rb, bias_tree_rb, bypass_rb), sim-char
```

`make check-sheet` netlists the sheets with xschem and compares them with the source netlist: devices (bias_tree_rb
11 = 11 with the three layout dummies, bypass_rb 2 = 2) and subcell instances with their parameters (pad_ref_rb 4 = 4,
`Xb ncm=4 ncr=9`), ports equal. The sheets of the two blocks are checked from their own macros (vcm_rb 26 = 26,
vref_s2d_rb 13 = 13, with their layout dummies). The whole hierarchy flattened was topology-equivalent to the source
(32 devices, checked before the dummies were added).

## Open points

- **Layout:** rows drawn per cell by layout agents from C3's row generators (P: PMOS rows, P3: rb_avg, N: NMOS rows and
  capacitors), each DRC 0, LVS match, mirror-symmetric; reports on the notes branch
  (`sudelbuecher/design_considerations/replica_bias/layout/`). The lead's check: all 42 active devices drawn with the
  circuit's nets and sizes, every dummy in the netlists (bias_tree_rb, vcm_rb, vref_s2d_rb). Christoph's decisions:
  rb_casc keeps the pad's 8 slots and band, its empty track places drawn as dummy M2 tracks on vdd; the 9th vref
  capacitor in rb_cload. Next: assembly (agent F), routing, flat LVS of pad_ref_rb, PEX.
- **Bias current:** the iref leg comes from `bias_dist_pd` (3 inputs, 4 switchable 1 : 1 outputs: S2D, D2S, this
  cell, a spare). That cell is a sheet only, never simulated, without layout. The decks so far feed this cell from
  its own `bias_gen_pd` with the pads' selection: the ideal case, without leg-to-leg mismatch.
- **Bypass capacitors: decided** (Christoph, 2026-11-07): NMOS to vss only, 4 more on vcm and 7 more on vref (6 + the
  layout's 9th), in bypass_rb. The comparison (`../vcm_rb/testbenches/rb_char/explore_bypass.py`): PMOS to iovdd multiplies the S2D's
  input-referred iovdd ripple at 1 MHz by 4 … 7; more NMOS area does the same for the kick without it. The hv
  varicap (0.7 pF flat, 2.6 fF/µm²) is not used: unproven in cmos5l and hard on the simulator. MIM is not in cmos5l.
