<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Replica bias for vref / vcm: summary

**Status (2026-11-06):** Phase 1 (survey) done; waiting for the user's answer before any simulation. Details:
`SURVEY.md`; commands: `RUNLOG.md`.

**Targets (proposed, from existing runs; band = INL ≤ 2 mV with a ±0.5 V signal on the unit gates):**

| voltage | target | band |
|---|---|---|
| S2D `vcm` = D2S `vref` (= D2S input common mode) | about 1.2 V; better the band's centre, which moves with PVT and iovdd | 1.08 … 1.25 V at iovdd 3.0 V; 1.07 … 1.53 V at 3.3 V; 1.07 … > 1.65 V at 3.6 V (S2D data; D2S not run below 1.65 V) |
| S2D `vref` | 0.5 V (pad range 0 … 1 V, includes iovss) or = vcm (pad range 0.7 … 1.7 V): to be decided | about 0.55 … 1.25 V at 3.0 V |

**Blocks (planned, not built):**
- `vcm_rb`: shared by S2D `vcm` and D2S `vref`.
- `vref_s2d_rb`: only if S2D `vref` ≠ vcm.

D2S `vref` must equal its input common mode, which is S2D `vcm`, so the task's third block (`vref_d2s_rb`) is not
needed.

**Current against a divider:** not yet evaluated. A divider from iovdd at Thevenin resistance R_th draws
`iovdd / (R_th · iovdd² / (V (iovdd − V)))`, which is 0.76 V / R_th at 1.2 V from 3.3 V: 76 µA at 10 kΩ, 7.6 µA at
100 kΩ. It also gives 1.09 V at iovdd 3.0 V, on the band's bottom edge. The required R_th is gap G6.

**Moves to the delivery repo later:** the replica macros (schematic, layout, views) and the pads' vref / vcm wiring;
nothing yet.
