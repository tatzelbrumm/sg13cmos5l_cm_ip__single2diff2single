<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# pad_ref_rb: routing-driven placement, the plan as built (Claude, agent F, C4, 2026-11-07)

Working material (lead, 22:2x CET). [M] measured on `pad_ref_rb.gds` / the router log, [R] reasoning. Pin coordinates
of every row: `pin_map.md` (cell frames); every net with its placed pins: `net_list.md`.

## Faces that meet, and the orientation that brings them together

| net(s) | faces | orientation chosen | result [M] |
|---|---|---|---|
| ts, bt | tails' M2 pins (bottom edge in R0) / tubs' M1 pins (bottom edge) | tubs M90 (D BB BA MR D), tails R180 under them, x offset 6.855 so TR sits under MR, BT under BA / BB | ts 3.7 um, bt 3.9 um, one straight M2 jog each |
| vbp | tails' right-edge stub (R0) / tree_p's left-edge stub | both R180, abutted, stubs at the same height (tree_p 0.22 up) | joined by abutment, no wire; one NWell (vdd) |
| vbnc | tree_p's top pin (R0) / casc's left-edge pin | tree_p R180 (pin down), casc M0, left channel | 11.6 um |
| gh | tubs' top pins / tree_n's top pins (R0) / avg top | tree_n R180 (pins down) with its gh pin straight over the tubs' gh pin; avg R0 right of the tubs | 7.8 um |
| m | avg's side pins / tubs' top pin | avg beside the tubs (2.5 um well gap, NW.b1 1.80) | 18.8 um |
| xp | avg bottom / casc top right (M0) / tree_n | avg at the casc's xp end | 34.4 um |
| bd | tubs' BA bottom pin / mirror's right-edge pins (low in R180) | mirror R180 left of the tubs, its pins at the tails-tubs channel | 18.0 um |
| ni, en_3v3_b, iref | tree_n's left edge (R180) / tree_p's TGP pins (top in R180) | the 3.0 um gap between mirror and tubs | ni 31.5 um |
| vcm, vref, en_3v3, en_3v3_b, iref | ports | the port group on the right edge at tree_n's height, en_3v3 straight out of tree_n | see below |

## Route order, layers, channels

- Router: C2's two-metal grid router `generator.py`, unchanged (C3 F's copy). Grid pitch 0.27 um, wire / via pad 0.29
  um, preferred directions M1 horizontal, M2 vertical (non-preferred cost 1.6, via cost 6). No metal over any gate
  (gate + 0.1 um keep-out on M1 and M2), M1 / M2 only.
- Order: the router's own (nets with the scarcest pin access first, then by spanning-tree length); every net routed
  in the first round [M]. With the port group keep-outs below, no reorder round was needed.
- Port group anchor: right edge, x 85.22, pins 0.29 um tall on M2 at 1.08 um pitch (four router tracks), bottom to
  top vref 77.76, vcm 78.84, en_3v3 79.92, en_3v3_b 81.00, iref 82.08 [M] (centres). Each port owns a 1.08 um strip of
  the edge, 0.7 um deep, open to its own net only, so that no net runs along the edge past another port.
- Supplies: vssh (outer) and vddh (inner) Metal2 rails, 1.0 um wide, full height on the left edge; every row's ring
  (or vdd track) is one terminal, so it is wired once [R: one terminal group per ring].

| channel | where (um) | width | carries |
|---|---|---:|---|
| left | x 0-4.0 | 4.0 | vssh, vddh rails; vbnc and vcm risers; casc vdd strap |
| bypass-casc | y 28.13-30.13 | 2.0 | vcm (bypass top bus), vref riser, vssh |
| casc-tails | y 42.50-45.00 | 2.5 | vbnc, xp, vref |
| tails-tubs | y 54.16-57.56 | 3.4 | ts, bt, bd, iref, vcm; NW.b1 (tree_p top 1.97 below the tubs) |
| mirror-tubs | x 23.75-26.75 | 3.0 | vcm, ni, en_3v3_b, iref down to TGP |
| tubs-avg | x 55.45-57.95 | 2.5 | xp, m, vbp |
| above tubs | y 69.53-71.53 / 74.22 | 2.0 / 4.7 | gh, m, vcm, ni, en_3v3_b, vref, xp, vbp |
| right | x 75.72-85.22 above the bypass | 9.5 | vcm, vref, iref, en_3v3_b to the ports |
