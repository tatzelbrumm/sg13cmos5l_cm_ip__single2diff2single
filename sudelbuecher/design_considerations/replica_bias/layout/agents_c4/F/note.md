<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# pad_ref_rb v2, placed and routed after Christoph's review (Claude, agent F, C4, 2026-11-07, 23:00-23:30 CET)

[M] = tool result, [R] = reasoning. v1 (7352 um2, pins bunched at slot7's bottom right) is kept in `v1/`.
Rebuild and check: `sh src/all.sh <inputs> <out> <work>` (2 min).

## Result [M] (`logs/summary.txt`)

| check | result |
|---|---|
| run_drc.py --no_density | No DRC violations detected, 0 "exception" lines |
| sg13cmos5l_maximal.drc -rd latchUpRules=true | 0 errors |
| flat LVS, --disable_tap_extraction, vs `pad_ref_rb.cdl` | Netlists match |
| negative LVS test (BA's gate moved m -> gh) | Netlists don't match: not vacuous |
| metal-only connectivity (LVS joins vss rings through the substrate) | 16 nets, 0 split |
| the 8 rows vs the delivered cells, all layers | 8 of 8 identical (texts vdd / vss -> vddh / vssh only) |
| sym_check, rows | 0; rb_tree_p Cont 0.0384 (P's known PCell residual) |
| capacitor blocks alone (`cells/logs/`) | DRC 0, maximal + LU 0, LVS match each; sym 0, capt 15.7 um2 (one column) |
| metal over transistor gates / over capacitor gates | 0 / 11.7 um2 M1 + 0.3 um2 M2 |

The CDL is composed from the circuit files with `bypass_rb` replaced by `bypass_rb_drawn.spice` (the drawn
capacitors): 58 devices = 38 active + 20 dummies.

## Area and place [M]

- **73.80 x 76.26 um = 5628 um2.** v1: 7352 um2. Ceiling: 5700. Cell and capacitor boxes: 4822 um2, 86 %.
- **Proposed position:** right edge at slot x 535.0, lower left (461.20, 169.07), spanning y 169.1 .. 245.3. This is
  between the S2D group (112-160) and the D2S group (222-262).
  - The vcm pin is at the D2S vref pin's height, 223.34, so it runs straight out.
- **Pins** (slot coordinates), Metal2, 0.29 um wide:
  - right edge: vref y 179.06 (runs down the right side to the S2D vref, 112.26); vcm y 223.34 (on to the S2D vcm,
    136.02, along the edge).
  - left edge, bottom to top: en_3v3 206.33, en_3v3_b 207.41, iref 208.49 (own enables and own iref leg); vssh 179.06,
    vddh 212.81.
- **vcm and vref are not crossed at the top level** [R]: the vcm route along the edge ends at 136, above the point
  where vref turns in at 112.

## Placement, bottom to top (signal flow; routing in `routing_plan.md`)

- **capr** (vref capacitors), the full width under **rb_casc** (R180: vref top right, xp top left, vbnc / vdd on the
  right edge). capr and rb_casc abut: one ThickGateOx.
- **rb_tree_n** (R0: pins up; en_3v3 on the left edge, at the input pins) | **rb_tails** (M0) | **rb_tree_p** (M0).
  rb_tails and rb_tree_p abut, so the vbp stubs meet; one NWell [M]. rb_tree_p's vbnc pin faces rb_casc's vbnc end.
- **rb_mirror** (M90: bd / vcm on its right edge) with **capm** on it | **rb_avg** (R0) | **rb_tubs** (R0, over the
  tails: TR under MR, BT under BA / BB) | **capt**.
- **capv** | **rb_cload** (M0: pins down, its vcm pin over BB's vcm pin). CB thus sits on the buffer output.

## Capacitors (bypass_rb as drawn: for the lead's backannotation)

All hv NMOS, gate = node, S = D = B = vssh, one finger each. Built by `src/capgen.py`: agent N's `bypass()` code with
the 12 um unit turned into W x L. Same finger, gate column, facing pairs, closed p+ ring and Metal2 gate bus.

| cell | node | count | W (um) | L (um) | gate (um2) | where |
|---|---|---:|---:|---:|---:|---|
| capr | vref | 2 | 34.1 | 16.9 | 1152.6 | full width under rb_casc |
| rb_cload CBR | vref | 1 | 12 | 12 | 144 | rb_cload (the pad's CLN slot), unchanged |
| capv | vcm | 2 | 19.24 | 12.66 | 487.2 | top left |
| capm | vcm | 2 | 8.18 | 3.25 | 53.2 | on rb_mirror |
| capt | vcm | 1 | 2.9 | 12.4 | 36.0 | right of rb_tubs |
| rb_cload CB | vcm | 1 | 12 | 12 | 144 | vcm_rb's CB, unchanged |

- **Totals:** vcm 576.3 + CB 144 = 720.3 um2 (target 720); vref 1152.6 + 144 = 1296.6 um2 (target 1296).
- **Netlist:** `bypass_rb_drawn.spice` holds the subcircuit as drawn: XCBR_cload, XCBR_capr m=2, XCBM_capm m=2,
  XCBM_capt, XCBM_capv m=2.
- **Re-simulation [R]:** capr's 34.1 / 16.9 lies outside the sizes simulated so far; the PSP model scales, but the
  bypass should be re-simulated.

## Changes to the rows

None: the 8 placed rows are XOR 0 against the delivered cells. bypass_rb (N's 3 x 4 array) is replaced by the four
capacitor blocks above. No transistor or dummy is added, removed or re-tied; only bypass_rb's capacitors change.

## Routing [M]

- C2's grid router, unchanged (`src/generator.py`, sha256 cea21b865695). Pitch 0.27 um, wire 0.29 um, M1 horizontal
  and M2 vertical preferred, M1 / M2 only.
- Every net routed, the second round. Totals: M1 469 um, M2 226 um, 76 vias.
- **Keep-outs:** every transistor gate (+0.1 um). The capacitor blocks are open to routing, because metal over a
  bypass gate only adds capacitance to a DC node [R]. Each pin owns its strip of the edge.
- **One strap drawn by F:** M2, 0.29 um, from rb_casc's vdd pin to a vddh terminal in the right channel. When the
  router landed on that pin, it filled the gaps between rb_casc's same-net vdd tracks into a plate wider than 0.3 um
  next to vbnc, which is an M2.e violation (measured in v1 and in v2a).
- **Net lengths M1 / M2 (um):** ts 0 / 3.3, bt 0 / 3.5, m 17.1 / 1.1, vbnc 19.8 / 1.6, xp 19.5 / 16.7, gh 25.1 / 11.6,
  ni 30.5 / 10.4, bd 29.2 / 14.4, vbp 39.1 / 27.0, iref 62.9 / 2.8, en_3v3 0 / 0.8, en_3v3_b 71.0 / 26.4,
  vcm 66.3 / 14.3, vref 48.1 / 65.8, vddh 37.6 / 17.0, vssh 3.0 / 9.6.

## Open points [R]

1. **Area:** 5628 um2 is 1.3 % under the ceiling. The rest is routing channels (1.5 / 3.23 / 1.0 um) and rb_casc's
   72 um length, which sets the width. capm and capt are thin fillers (49 % and 45 % gate per box).
2. **Supplies:** vddh and vssh are single edge pins (0.29 um wide) wired by the router. Supply currents are about
   25 uA. If rails are wanted at the top level, the left edge is free for them.
3. **Re-simulation:** the bypass, with the new capacitor sizes, and the enable settling.
