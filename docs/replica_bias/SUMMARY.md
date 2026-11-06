<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Replica bias for vref / vcm: summary

**Status (2026-11-06):**
- Phase 1 (survey) done.
- Phase 2 (design and simulation, schematic level) done.
- Phase 3 (layout) not started; floorplan below.

Detail: `SURVEY.md` (survey, gaps G1–G12 and their results), `RUNLOG.md` (every command), the two macro READMEs.

**Targets** (the user's answer: 1a, 2A, all gap runs).

| voltage | target | band where the pads stay linear (INL ≤ 2 mV, ±0.5 V on the unit gates) |
|---|---|---|
| S2D `vcm` = D2S `vref` (= D2S input common mode) | centre of the band, tracking PVT, iovdd and reference current | 1.031 … 1.262 V at iovdd 3.0 V, … 1.530 V at 3.3 V, … > 1.65 V at 3.6 V; 1.126 … 1.244 V with the Oguey–Aebischer core at 125 °C |
| S2D `vref` | about 0.5 V (pad range from 0 V) | above 0.46 … 0.54 V at 125 °C; below 0.4 V up to 27 °C |

**Blocks** (`macros/vcm_rb`, `macros/vref_s2d_rb`). Both are made from one 5 µA reference each, with replicas of the
pads' devices (hv MOS of the pads' sizes only, no resistor), and have `en_3v3` / `en_3v3_b`.

| block | principle | result |
|---|---|---|
| vcm_rb | top-edge detector (unit tail + input follower), fold-node replica, average by three PMOS diodes, unit-device OTA buffer | 1.12 … 1.40 V; inside the band of both pads at every PVT point and reference (worst margin 40 mV); σ 6.5 mV; 22 … 35 kΩ |
| vref_s2d_rb | fold-node replica at low density (follower from its own vbnc) | 0.48 … 0.50 V at 27 °C, 0.44 … 0.46 at −40 °C, 0.57 … 0.60 at 125 °C; ≥ 31 mV above the S2D INL edge; σ 3.8 mV; 18 … 28 kΩ |

**Closed loop** (pads with the blocks):
- **S2D:** INL ≤ 1.73 mV. The ideal fixed 0.5 / 1.2 V reaches 3.65 mV.
- **D2S:** INL ≤ 1.72 mV.
- **Round trip:** INL ≤ 0.75 mV (ideal fixed: 3.14 mV).
- **S2D enable:** 1.4 µs, as with ideal sources.
- **S2D pad range:** 0 … ≥ 1.09 V up to 27 °C.

**Current against a divider** (same output, same output impedance, tt / 27 °C / 3.3 V):

| | block (incl. its 5 µA reference) | divider | divider rhigh |
|---|---:|---:|---:|
| vcm_rb, 1.26 V, 27 kΩ | 22.5 µA | 28.8 µA | 115 kΩ |
| vref_s2d_rb, 0.49 V, 21 kΩ | 10.5 µA | 19.9 µA | 166 kΩ |

**So the saving is 0.8× and 0.5×, not "well below".** At the impedance the pads need (G6: ≤ about 30 kΩ, so that the
S2D's enable does not kick the pins), a divider needs little rhigh either. What the divider cannot do:
- **Track the band:** ratiometric, 1.09 V at 3.0 V, below the band with the OA core at 125 °C.
- **Follow the S2D input edge:** a flat 0.5 V gives INL up to 3.6 mV at ff / 125 °C.
- **Switch off:** it draws its current with everything off.

**Floorplan (sketch, not drawn).**
- **Rail:** the top edge is referenced to the pads' unit rail, so both blocks sit on the same supply as the pads'
  units:
  - in the custom-pad route, the IO ring rails, at the slot's pad-side edge;
  - in the slot fallback, vdd_3v3 / vss_3v3, next to the two pad macros.
- **Size:** gate areas 542 µm² (vcm_rb) and 564 µm² (vref_s2d_rb); with hv spacing and wells, each about
  50 × 60 µm.
- **Reference:** each block takes a 5 µA leg from bias_dist_pd (or its own bias_gen_pd) of the same selection as the
  pads.
- **Enable:** vcm_rb's must cover every user of vcm.
- **Wiring:**

```
   slot main area                                   | pad side (x >= 520 um: pin stubs only)
   bias_gen_pd --> bias_dist_pd --+-- 5 uA --> [vcm_rb]      --- vcm  --+--> S2D pad vcm
                                  |                                     +--> D2S pad vref
                                  +-- 5 uA --> [vref_s2d_rb] --- vref ----> S2D pad vref
   en_ctrl_3v3 (en_3v3 / en_3v3_b) --> both blocks (vcm_rb enabled while either pad or the next stage runs)
```

**Open points:**
- **Layout and extraction** of both blocks.
- **The vcm overshoot at enable** (+0.19 V, +0.48 V with the OA core): sequence the pads after the references, or slow
  the buffer's start.
- **The S2D zero point drifts +0.9 mV/K** by design. For a ground-referenced signal that is a temperature-dependent
  offset, and vref is not observable unless routed out.
- **D2S output offset 5.5 mV** with the OA core at ff / 125 °C (limit 5 mV; the same with an ideal reference).
- **Closed loop in CACE:** done in decks with the templates' measurement code, not in CACE templates of the pads.
- **Round trip:** with ideal sources at the blocks' DC outputs, because the deck with the blocks inside does not
  converge.

**What would move to the delivery repo later:**
- the two macros (netlist, sheet, symbol, CACE suite, and layout once drawn);
- in the slot: two bias_dist_pd legs, the blocks, the vcm / vref nets to the pads in place of the harness `vbias`.
