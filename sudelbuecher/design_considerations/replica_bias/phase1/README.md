<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Replica bias, Phase 1: derivations behind the survey

Notes for `docs/replica_bias/SURVEY.md` on design branch `claude/c4-replica-bias`. 2026-11-06, cloud session (task file
`docs/launch/replica_bias_TASK.md` on `harness-test`). Read only: no simulation.

## Files

| file | content |
|---|---|
| `survey_tables.py` | regenerates every table of `SURVEY.md` from committed CSVs and from `results_s2d.txt` §3; `python3 -I survey_tables.py <design checkout> <notes checkout>` |
| `../../../logs/replica-bias/phase1_survey_tables.log` | its output (2026-11-06T13:51Z) |

## 1. One target for S2D vcm and D2S vref

- `d2s_mpdda_pd`: units A (vinp, vref), B (vref, vinn), C1 = C2 (vref, vfb). Every unit has vref on one gate.
- With the input common mode vicm = vref + c, the input units carry f(u + c) + f(u − c) against 2 f(vfb − vref).
  - For an odd f the offset stays zero.
  - The gain becomes [f'(c) + f'(−c)] / 2 f'(0) ≈ f'(c) / f'(0): second order in c, and it eats the units' linear
    range (`proposed_improvements.md` §II).
- In the single → diff → single chain, vicm is the S2D output common mode, vcm + CM error (5…18 mV systematic, σ 12 mV
  under mismatch).
- So D2S vref = S2D vcm, ideally the same net. How large c may be is gap G2: no run has it.

## 2. The band criterion

INL ≤ 2 mV (the S2D `dc_params` limit) with ±0.5 V on the unit gates (S2D u = ±0.5 V; D2S vd = ±1 V). Edges are linear
interpolations between the swept vcm values of `results_s2d.txt` §3 (ideal fixture, vref = vcm).

The pad-level `range_params` (real bias, iovdd 3.0 V only, 4 × 4 vref × vcm) agree at the common points:
- vcm 1.2 V: ≤ 0.72 mV at pad level against ≤ 0.69 mV (§3);
- vcm 1.4 V at ss / −40 °C: 13.6 mV at pad level against 19.1 mV (§3; different vref).

## 3. The edges, and what sets them

- **Top.** The tail XT (5 / 6 µm, 5 µA, gate vbp) leaves saturation as the follower XM (20 / 1 µm) raises its source:
  `V_g,max ≈ iovdd − V_SD,sat(XT) − |V_GS(XM)|`.
  - At tt 27 °C, 3.3 V (§1): V_SD,sat(XT) = 0.431 V and |V_GS(XM)| = 0.739 V give 2.13 V. The INL criterion tolerates a
    little triode, and its edge is about 2.15 V.
  - The tail's gate line vbp = iovdd − V_SG(BP) (BP is the same 5 / 6 µm device at 5 µA; vbp = 1.972 V at tt, 3.3 V,
    D2S README). So V_SD,sat(XT) = V_SG(BP) − |Vth|. A replica of BP + XM, fed from the same tree, reproduces the top
    edge with its iovdd, corner, temperature and current dependence.
- **Bottom of vcm (S2D outputs).** *Inferred:* at vcm − 0.5 V the output NMOS cascode CX (30 / 3 µm at vbnc) leaves
  saturation. x ≈ 0.378 V and V_DS,sat(CX) ≈ 0.166 V at tt 27 °C (§1), so voutn ≥ about 0.55 V. Data: no iovdd
  dependence (1.079 / 1.070 / 1.067 V at ss / 125 °C); worst hot. To be confirmed by an OP at 125 °C (gap G5).
- **Bottom of S2D vref.** The input follower's drain is on x; its source is at vin + |V_GS|. At 125 °C, ff, |V_GS|
  shrinks and the follower leaves saturation near vin = 0.09 V (`window_params`).

## 4. A divider for comparison

A divider from iovdd to V with Thevenin resistance R_th has R1 + R2 = R_th · iovdd² / (V (iovdd − V)) and draws
I = V (iovdd − V) / (R_th · iovdd).

For V = 1.2 V from 3.3 V: I = 0.764 V / R_th, so 76 µA at 10 kΩ, 7.6 µA at 100 kΩ, 0.76 µA at 1 MΩ.

It is ratiometric to iovdd (0.364 V/V): 1.09 V at 3.0 V, right at the band's bottom edge (1.08 V at ss / 125 °C). The
top edge moves at about 0.9 V/V and the bottom edge not at all, so a ratiometric divider follows neither. The R_th the
pads need is gap G6.
