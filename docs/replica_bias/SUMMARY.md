<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Replica bias for vref / vcm: summary

**Status (2026-11-07):**
- Phase 1 (survey) done.
- Phase 2 (design and simulation, schematic level) done.
- Phase 2b (Christoph's option A): both blocks share one bias tree in the new cell `pad_ref_rb`; every DC result
  unchanged, current 33 → 24.1 µA; sheets redrawn from Christoph's hand-compacted versions; CACE 8 / 8 pass.
- Phase 3 (layout): primitives collected from the s2d pad cell, row plan and area estimate
  (`macros/pad_ref_rb/layout/primitives/README.md`); assembly not started.

Detail: `SURVEY.md` (survey, gaps G1–G12 and their results), `RUNLOG.md` (every command), the macro READMEs
(`macros/pad_ref_rb`, `macros/vcm_rb`, `macros/vref_s2d_rb`).

**Targets** (the user's answer: 1a, 2A, all gap runs).

| voltage | target | band where the pads stay linear (INL ≤ 2 mV, ±0.5 V on the unit gates) |
|---|---|---|
| S2D `vcm` = D2S `vref` (= D2S input common mode) | centre of the band, tracking PVT, iovdd and reference current | 1.031 … 1.262 V at iovdd 3.0 V, … 1.530 V at 3.3 V, … > 1.65 V at 3.6 V; 1.126 … 1.244 V with the Oguey–Aebischer core at 125 °C |
| S2D `vref` | about 0.5 V (pad range from 0 V) | above 0.46 … 0.54 V at 125 °C; below 0.4 V up to 27 °C |

**Blocks** (`macros/vcm_rb`, `macros/vref_s2d_rb`, together in `macros/pad_ref_rb`). Since 2026-11-07 both hang on
one shared bias tree `bias_tree_rb` made from one 5 µA reference, with one enable `en_3v3` / `en_3v3_b` (before: one
reference and one tree each). Replicas of the pads' devices only (hv MOS of the pads' sizes, no resistor).

| block | principle | result |
|---|---|---|
| vcm_rb | top-edge detector (unit tail + input follower), fold-node replica, average by three PMOS diodes, unit-device OTA buffer | 1.12 … 1.40 V; inside the band of both pads at every PVT point and reference (worst margin 40 mV); σ 5.3 mV; 22 … 35 kΩ |
| vref_s2d_rb | fold-node replica at low density (follower from the tree's vbnc) | 0.48 … 0.50 V at 27 °C, 0.44 … 0.46 at −40 °C, 0.57 … 0.60 at 125 °C; ≥ 31 mV above the S2D INL edge; σ 3.7 mV; 18 … 28 kΩ |

**Closed loop** (pads with the blocks; unchanged by the shared tree):
- **S2D:** INL ≤ 1.73 mV. The ideal fixed 0.5 / 1.2 V reaches 3.65 mV.
- **D2S:** INL ≤ 1.72 mV.
- **Round trip:** INL ≤ 0.75 mV (ideal fixed: 3.14 mV).
- **S2D enable:** 1.4 µs, as with ideal sources.
- **S2D pad range:** 0 … ≥ 1.09 V up to 27 °C.

**Current against a divider** (same output, same output impedance, tt / 27 °C / 3.3 V):

| | replica | divider | divider rhigh |
|---|---:|---:|---:|
| vcm, 1.26 V, 27 kΩ | | 28.8 µA | 115 kΩ |
| vref, 0.49 V, 21 kΩ | | 19.9 µA | 166 kΩ |
| both: pad_ref_rb, incl. its one 5 µA reference | 24.1 µA | 48.7 µA | |
| both, as two blocks with own trees (2026-11-06) | 33.0 µA | | |

**So the shared cell takes half the current of two dividers (0.5×); as separate blocks it was 0.68×.** At the impedance the pads need (G6: ≤ about 30 kΩ, so that the
S2D's enable does not kick the pins), a divider needs little rhigh either. What the divider cannot do:
- **Track the band:** ratiometric, 1.09 V at 3.0 V, below the band with the OA core at 125 °C.
- **Follow the S2D input edge:** a flat 0.5 V gives INL up to 3.6 mV at ff / 125 °C.
- **Switch off:** it draws its current with everything off.

**Floorplan (sketch, not drawn).**
- **Rail:** the top edge is referenced to the pads' unit rail, so both blocks sit on the same supply as the pads'
  units:
  - in the custom-pad route, the IO ring rails, at the slot's pad-side edge;
  - in the slot fallback, vdd_3v3 / vss_3v3, next to the two pad macros.
- **Size:** one cell for both references. From the collected primitives: about 4800 µm² of rows (13 bypass
  capacitors more than half of it), about 85 × 85 µm routed (`macros/pad_ref_rb/layout/primitives/README.md`; before the shared tree: 2 × 50 × 60 µm).
- **Reference:** one 5 µA leg from `bias_dist_pd`, fed from the same source as the pads' own legs, so that the
  replica tracks the pads' reference current.
- **Enable:** one for the cell; it must cover every user of vcm.
- **Wiring:**

```
   slot main area                                   | pad side (x >= 520 um: pin stubs only)
   bias_gen_pd --> bias_dist_pd --+-- 5 uA --> S2D pad iref
                                  +-- 5 uA --> D2S pad iref
                                  +-- 5 uA --> [pad_ref_rb: bias_tree_rb -> vcm_rb, vref_s2d_rb]
                                  |                 vcm  --+--> S2D pad vcm
                                  |                        +--> D2S pad vref
                                  |                 vref ----> S2D pad vref
                                  +-- spare
   en_ctrl_3v3 (en_3v3 / en_3v3_b) --> pad_ref_rb (enabled while either pad or the next stage runs)
```

**Open points:**
- **Layout and extraction** of pad_ref_rb (primitives collected; decisions on flat LVS and the tree row's spare slot).
- **The bias distribution:** `bias_dist_pd` (sheet only) has never been simulated. The chain bias_gen_pd →
  bias_dist_pd → both pads and pad_ref_rb, with leg-to-leg mismatch, is not simulated yet; the decks so far give
  pad_ref_rb its own bias_gen_pd of the same selection.
- **Bypass capacitors: decided 2026-11-07.** A cell of its own, `bypass_rb`: 4 more 12u × 12u NMOS to vss on vcm
  (vcm_rb keeps CB for its buffer's phase margin), 8 on vref (vref_s2d_rb has none). The S2D enable kick drops to
  0.112 / 0.096 V (from 0.236 / 0.212). PMOS to iovdd was rejected: it multiplies the S2D's input-referred iovdd
  ripple at 1 MHz by 4 … 7. Side finding: the D2S output follows iovdd by 0.38 V/V at any frequency up to 1 MHz,
  because vcm tracks the band by design (an ideal vcm: 0.3 mV/V).
- **The vcm overshoot at enable** (≤ 37 mV, ≤ 0.23 V with the OA core; with own trees +0.19 / +0.48 V): sequence the
  pads after the references if it matters.
- **The S2D zero point drifts +0.9 mV/K** by design. For a ground-referenced signal that is a temperature-dependent
  offset, and vref is not observable unless routed out.
- **D2S output offset 5.5 mV** with the OA core at ff / 125 °C (limit 5 mV; the same with an ideal reference).
- **Closed loop in CACE:** done in decks with the templates' measurement code, not in CACE templates of the pads.
- **Round trip:** with ideal sources at the blocks' DC outputs, because the deck with the blocks inside does not
  converge.

**What would move to the delivery repo later:**
- the three macros pad_ref_rb, vcm_rb, vref_s2d_rb (netlists, sheets, symbols, CACE suite, and layout once drawn);
- in the slot: one bias_dist_pd leg, pad_ref_rb, the vcm / vref nets to the pads in place of the harness `vbias`.
