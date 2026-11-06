<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Replica bias, Phase 2: how the two blocks came about

Notes for `macros/vcm_rb` and `macros/vref_s2d_rb` on design branch `claude/c4-replica-bias`. Cloud session C4,
2026-11-06. The user's answer to the survey: 1a (S2D vref 0.5 V, own block), 2A (vcm tracks the band centre), 3 (all
gap runs). Every number below is in a TSV on the design branch; commands are in `docs/replica_bias/RUNLOG.md`. Logs
of the long runs are in `../../../logs/replica-bias/`.

## 1. The band, from the gap runs

The criterion is INL ≤ 2 mV with ±0.5 V on the unit gates. The decks are the pads' source netlists with the CACE
templates' measurement code; they reproduce CACE to the last digit.

- **S2D vcm (G3):** the bottom edge is 0.89 / 0.95 / 1.02 V at −40 / 27 / 125 °C, the same at every MOS corner and
  every iovdd.
  - "No absolute threshold": the fold node x is vbnc − V_GS(CX), a difference of two NMOS V_GS.
  - G5 shows the output cascodes CX / CY with the least margin there.
  - The top edge is the unit tail's saturation, about iovdd − 1.25 V on the top gate at ss / −40 °C.
- **D2S (G1):** the same top edge within 8 mV, no bottom edge above 0.8 V. G2: |vicm − vref| ≤ 0.1 V keeps INL
  ≤ 2 mV.
- **Reference current (G10):** the Oguey–Aebischer core at 125 °C (+33 … 42 %) narrows the band to
  1.126 … 1.244 V at 3.0 V. This case argues for a replica fed from the same reference: a divider or a fixed voltage
  cannot follow it.
- **S2D vref (G4):** its bottom edge = x − V_SG(input follower, 5 µA) + 0.676 V, within 4 mV over corners and supplies
  at 125 °C. It is below 0.4 V up to 27 °C and 0.46 … 0.54 V at 125 °C.

## 2. vcm_rb

**Top edge, an edge detector:** a tail replica TR (5u/6u at vbp), into a diode-connected input-follower replica MR
(20u/1u ng=2), into a sink of r × TR's saturated current. Node gh is the gate voltage at which the tail has lost
(1 − r) of its current.
- gh − top gate limit spans 80 / 62 / 36 / 24 / 34 mV for r = 0.95 / 0.9 / 0.8 / 0.7 / 0.6.
- A low r tracks better: the criterion moves away from the saturation knee, where the corners differ most.
- **The block uses r = 0.8** (sink 2 × 2.4u/6u = 4 µA): +0.157 ± 0.018 V.

**Bottom edge.**
- **A current-loss detector failed:** cascode + sink at 10 % loss sat at 0.15 … 0.3 V, far below the INL edge (about
  0.45 … 0.55 V at the output). INL degrades through the cascode's falling output resistance (loop gain) long before
  current is lost.
- **What works:** the fold-node replica xp (one CY finger at vbnc on a 5 µA sink). It is corner-independent
  (0.379 … 0.395 V at 27 °C) with +0.6 mV/K, and bottom edge − xp = 0.559 ± 0.034 V.

**Centre.** Centre = (top − 0.5 + bottom)/2 = (gh + xp)/2 + const: the signal amplitude cancels, and so do most of the
offsets.
- Fit on the bias copies: centre − (gh + xp)/2 = −0.057 ± 0.026 V, over 26 PVT / reference points, including the
  OA-core case and the D2S top edge.

**Averaging without a resistor.** A string between gh and xp would need megohms to keep its current from shifting gh:
"a lot of rhigh area", exactly what the task wants to avoid.
- Two equal PMOS diodes in their own wells carry the same current, so their midpoint is the average whatever the
  current. At (gh − xp)/2 ≈ 0.8 … 1.1 V that current is 20 nA … 0.9 µA, which loads gh only slightly.
- **The offset:** making the lower half two diodes in parallel (candidate G) centres it on average (+1 mV). Candidate D
  (lower 5u/6u) is 3 mV better at the worst point but 36 mV low on average.
- **2 µA versions of TR / CY** track worse (worst margin 19 mV) and were dropped.

**Buffer.** The midpoint alone has 0.2 … 1.06 MΩ. G6 asks for ≤ about 30 kΩ, because the S2D's enable dumps charge
into vcm.
- A 5T OTA in unity gain from the unit devices (pair 20u/1u ng=2, tail 5u/6u, NMOS mirror 6u/6u) gives 22 … 35 kΩ
  with a 12u × 12u NMOS capacitor, offset −0.9 mV. It costs 5 µA.
- A source follower would need a replica level shift at one end of the stack, and there is no headroom for it at
  iovdd 3.0 V.

## 3. vref_s2d_rb

The two requirements together force the temperature behaviour:
- pad range from 0 V: vref ≤ 0.5 V at room;
- linear at ff / 125 °C: vref ≥ 0.55 V;
- so TC ≥ +0.5 mV/K.

The options:
- **rhigh × a reference current:** wrong sign (TC1 −2300 ppm/K) and, with the harness current, ±25 % over the rhigh
  corners. Rejected.
- **An x-type node at low density**, `vbnc − V_GS(F)`, rises like x (+0.6 mV/K) and is corner-tolerant (difference of
  NMOS V_GS).
  - F = 4 × 15u/3u at 1.67 µA gives 0.48 … 0.50 V at 27 °C and ≥ 31 mV above the edge at 125 °C (`explore_vref.py`,
    then the block).
  - Its output is low-impedance (1/gm, about 20 kΩ) at no extra cost.
- **The bypass** is two NMOS capacitors to vss rather than a PMOS one to iovdd, so supply ripple does not reach the
  pad's zero.

## 4. A divider, for comparison

A divider from iovdd to V at Thevenin resistance R_th draws `I = V (iovdd − V) / (R_th · iovdd)`, with
`R1 + R2 = R_th · iovdd² / (V (iovdd − V))`.

At the blocks' own output impedance (tt, 3.3 V):

| case | divider | block (incl. its 5 µA reference) |
|---|---|---|
| vcm 1.26 V, 27 kΩ | 28.8 µA, 115 kΩ total | 22.5 µA |
| vref 0.49 V, 21 kΩ | 19.9 µA, 166 kΩ total | 10.5 µA |

The saving is 0.8× and 0.5×. The task's premise ("several µA per tap and a lot of rhigh area") holds only at higher
impedances, where the pads' enable would kick the pins (G6). The replicas earn their place by tracking:
- a ratiometric divider gives vcm 1.09 V at 3.0 V, below the OA / 125 °C band;
- a flat 0.5 V gives the S2D up to 3.6 mV INL at ff / 125 °C;
- a divider cannot be switched off.

## 5. Things that went wrong on the way (and are fixed)

- **Node-name clash** in the first edge exploration: `s0` was both a detector node and the harness sel0 line.
- **Operating-point failures** at tt / −40 °C in the disabled bandgap core's floating rhigh chain (3 runs of 2104):
  retried with `.options rshunt=1e12`, marked in the TSV column `conv`.
- **The supply-ramp start-up** at ss / −40 °C: the transient op at iovdd = 0 fails in the bandgap PNP; the deck now
  starts with `uic`.
- **The first window deck** referenced the pad source to the block's vref node (an E-source between vsrc and vref),
  so the ESD-diode current at pad < 0 loaded the block. It now uses a ground-referenced source.
  - The closed-loop DC deck has the same coupling; it is harmless there, because pad ≥ −0.12 V.
- **The round-trip deck with both blocks inside** does not converge. It uses ideal sources at the blocks' DC outputs,
  which is exact at DC because the pads draw no DC current from vref / vcm.
