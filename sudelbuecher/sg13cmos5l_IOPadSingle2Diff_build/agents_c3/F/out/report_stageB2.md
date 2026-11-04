<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
<!-- Saved by the lead from agent F's final reply (the harness refused F's own write of this file). Text as F sent it. -->
# F stage B2: pad, vbp and vbnc rerouted (C3, 2026-11-04, 16:52–17:55 CET)

1. **pad** runs up the middle of the cell, with an iovss shield on each side and one short Metal3 leg in the rail gap
   119–126. No other net runs within 0.7 µm of it, apart from two pieces of 1.9 / 1.7 µm and the Metal3 rail above
   [M]. In stage B, vbnc ran 107 µm beside it.
2. **vbp** comes from the right only: 79 µm instead of 271 µm (M1 + M2) [M], with no vbp routing on the left. The
   tail rows' left vbp stubs are removed (Metal2 / Via1).
3. **vbnc** runs nowhere parallel to the pad (0 µm within 1 µm) [M]. It is 208 µm long (was 235); routing it first
   broke 4 other nets [M].
4. **Every stage B check still passes** [M]:
   - DRC 0 (run_drc.py, and maximal with latch-up);
   - deep LVS match;
   - circuit check EQUAL;
   - row check 25 / 25;
   - template drawing layers 0, reserve 0 µm²;
   - PEX 28 capacitor-only nodes, as before.

   The rebuild is byte-identical; stage B is kept in `stageB_v1/`.

[M] = tool run, [R] = reasoning.
- Build: `sh src/run_B.sh <inputs> <out> <out>`.
- Checks: `sh src/checks_B.sh <inputs> <inputs_B> <out> <tmp>`.
- Numbers: `logs/long_nets_B2.md`.
- Picture: `previews/long_nets_B2.png` (pad blue, vbp red, vbnc green, shields orange).

## The pad line (drawn in `pwr_f` by `src/make_pwr.py`; not routed by the router)

- **Path** (center line):
  1. from the template's pad pin (M2 x 20.40–21.02, top 31.18), M2 up channel C1 (x 21.715);
  2. M2 right, under tails_lo (y 107.85);
  3. M2 up past tails_lo's right end (x 50.85);
  4. Via2, then M3 left in the rail gap (y 121.00, x 50.85 → 46.39), ≥ 1.15 µm from the rails at 119 and 126
     (the rule asks for ≥ 0.5);
  5. Via2 + Via1, then M1 up the 1.80 µm well gap between tub columns 6 and 7 (x 46.39);
  6. Via1 onto the vin track (y 136.80).
- **Why this way** [R]: the tail rows' gates block every straighter path, and above them the Metal3 is the iovdd rail.
  The M1 leg in the well gap keeps off the tub gates.
- **Shields:** 0.30 µm wide, 0.40 µm from the pad line (centers 0.70 apart), on both sides through all three metals.
  - On iovss [R]: it is the substrate and the protection's ground, so it is the pad signal's own reference.
  - Tied at one end only: both shields meet at the pad end in an M1 bridge under the pad's M2, with one Via2 into the
    M3 iovss rail 7–32.5. No supply current flows in them: no loop, no drop along the line.
  - Christoph made them optional. They cost no other route (every net routes), so I kept them.
- **Router keep-out:** no router M1 directly under the pad's C3a leg; a first run had put vbn there for 30 µm.

**Lengths** [M] (routing metal only, from the LVS cross-reference; `src/net_metrics.py`):

| net | before M1 / M2 / M3 µm | after M1 / M2 / M3 µm |
|---|---|---|
| pad | 18.1 / 108.1 / 0 | 16.1 / 120.8 / 4.8 |
| vbp | 36.7 / 233.8 / 0 | 21.9 / 56.9 / 0 |
| vbnc | 83.1 / 151.5 / 0 | 59.2 / 149.2 / 0 |
| vbn | 57.8 / 113.5 / 0 | 55.9 / 96.1 / 0 |
| outp | 68.2 / 69.0 / 0 | 86.2 / 75.4 / 0 |
| outn | 66.7 / 78.3 / 0 | 62.2 / 97.0 / 0 |

**Parallel runs beside the pad** [M] (longest piece of another net in the same or an adjacent metal):

| spacing | before | after |
|---|---|---|
| ≤ 1.0 µm (brief) | vbnc 106.9, vbp 20.2, y 18.4, x 17.2 | sb_f1 30.1 (M1, behind the bottom shield), outp 13.1 (M2, behind the right shield), outn 10.3 (behind the right shield in the well gap), vcm 2.4, others ≤ 2.3 |
| ≤ 0.7 µm (inside the shields' far edge) | vbnc 106.5, y 18.4, vbp 3.4 | y 1.9, sa_m2 1.7, sb_m1 1.1, others ≤ 0.7 |

- In both runs the iovdd M3 rail (93.5–119) lies over the pad's M2 leg for 30 µm. The cell sits under the ring rails,
  so this cannot be avoided [R]. The shields themselves (iovss) also show in the measurement.
- Two attempts did not route all nets [M]: keep-outs in the well gap (7 nets left), and vbnc routed first (4 nets
  left).

## Other changes

- **vbp:**
  - A router keep-out closes the tail rows' left ends to all router nets.
  - The left vbp edge stubs are removed from `s2d_tails_hi_f` / `_lo_f`. Both rows stay DRC 0, maximal 0, LVS match,
    sym 0, and their Activ / Cont still XOR 0 against P's rows [M].
  - vbp now runs in x 49.1–60.5 only [M].
- **Moves:** the iovdd_t tap moved from x 51.50 to 54.30, out of the pad corridor. No cell moved, and the reserve is
  unchanged.
- **`src/fix_block.py`:**
  - one 0.16 µm M2 neck, where a router landing met F's link at a corner, is filled to Mn_a 0.20;
  - the pad line's M2 landings are 0.30 × 0.50 (Mn_d 0.144).
- **Route order:** found by the reorder rounds. The final build routes everything in round 0.

## Open [R]

- vbnc is 208 µm long and runs along the bottom of the right pocket, clear of the pad.
- outp's M2 runs 13 µm beside the pad corridor's right shield, 0.96 µm from the pad line.
