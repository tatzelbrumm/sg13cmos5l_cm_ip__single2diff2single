<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# pad_ref_rb v2: routing-driven placement as built (Claude, agent F, C4, 2026-11-07)

[M] measured on `pad_ref_rb.gds` / `logs/route.txt`, [R] reasoning. Pins of every row: `pin_map.md`; every net with
its placed pins: `net_list.md`. Placement table and capacitor list: `src/rb_place.py`.

## Faces that meet

| net(s) | faces brought together | how | length M1 / M2 [M] |
|---|---|---|---|
| ts, bt | tails' top pins (M0) / tubs' bottom pins (R0) | tails 2.345 left of the tubs: TR under MR, BT under BA / BB | 0 / 3.3, 0 / 3.5 |
| vbp | tails' right stub / tree_p's left stub | abutted; tree_n's vbp from its top pin | 39.1 / 27.0 |
| vbnc | tree_p's bottom pin (M0) / rb_casc's right-edge pin (R180) | tree_p at the right end, over rb_casc's vbnc end | 19.8 / 1.6 |
| xp | rb_casc's top-left pin / tree_n's top pin / avg's bottom pin | all three at the left half | 19.5 / 16.7 |
| gh, m | tubs' top pins / avg's top and side pins / tree_n's top pin | avg beside the tubs, 2.5 um well gap (NW.b1 1.80) | 25.1 / 11.6, 17.1 / 1.1 |
| bd, vcm | tubs' BA bottom / BB top; mirror's right edge (M90); cload's bottom pins (M0) | cload over BB, mirror left of avg | 29.2 / 14.4, 66.3 / 14.3 |
| vref | rb_casc top right, capr's bus, tree_n's SF pin, cload, the pin | capr under rb_casc, the pin at the right edge low | 48.1 / 65.8 |
| en_3v3, en_3v3_b, iref | left-edge pins / tree_n's left edge, TGP on tree_p, cload's SPDs | tree_n at the left edge | 0 / 0.8, 71.0 / 26.4, 62.9 / 2.8 |

## Router setup

- **Router:** C2's grid router `generator.py`, unchanged. Grid 0.27 um, wire / via pad 0.29 um, M1 horizontal and M2
  vertical preferred (non-preferred cost 1.6, via cost 6).
- **Keep-outs:**
  - every transistor gate + 0.1 um, on M1 and M2;
  - capacitor gates are open to routing;
  - each pin owns a 0.7 um deep strip of the edge.
- **Route order:** the router's own (scarcest pin access first). iref failed in round 0, so the retry loop moved it
  to the front, and everything routed in round 1 [M].
- **Channels (um):**
  - capr / rb_casc abut;
  - rb_casc to the row above: 1.5;
  - tails to tubs: 3.23 (tree_p's top 1.80 below the tubs, NW.b1);
  - avg to capv: 1.0;
  - mirror to avg: 6.8 (bd, vref, vbp, en_3v3_b);
  - right channel at rb_casc: 1.18 (vref, vbnc, casc vdd strap).
