<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Cleaned-out pad template for `sg13cmos5l_IOPadSingle2Diff` (draft for review, 2026-11-03, version 2)

IHP's `sg13cmos5l_IOPadAnalog` frame, with its protection rebuilt from Christoph's PCells (`scripts/pcells`) in narrow
frames. All of it now sits in the bottom region between the narrow NWell legs, and the rest of the cell is cleared
for the s2d buffer. The top cell is `sg13cmos5l_IOPadSingle2Diff`. This file is not the macro's layout
(`../sg13cmos5l_IOPadSingle2Diff.klay.gds`), and no make target reads this folder. Version 1 (IHP's own protection
cells, SecondaryProtection kept) is commit 0f131b6.

| file | |
|---|---|
| `sg13cmos5l_IOPadSingle2Diff_template.gds` | the template (sha256 ffa05cbe68ef…), PCell context kept (libraries `SG13_cm_clamps`, `SG13_dev`) |
| `sg13cmos5l_IOPadSingle2Diff_template.png` | the whole cell, M3 / M4 / TM1 and their vias hidden |
| `sg13cmos5l_IOPadSingle2Diff_template_esd.png` | the protection zone, y 0–70 |
| `IOPadAnalog.png` | IHP's cell, for comparison |
| `build_template.py` | the generator: `PDKPATH=/foss/pdks/ihp-sg13cmos5l python3 build_template.py <notes>/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/out/padctx` |

## Protection (y 5.38–39.02, between the NWell legs)

Two columns. Each keeps IHP's vertical order and relative position: diode directly on the clamp, rings abutting.

| | PCell, parameters | origin (µm) | bbox (µm) | IHP equivalent |
|---|---|---|---|---|
| CN | `Clamp_N_M1` ng 20, l 0.6u, frame fit | 1.20, 6.00 | 0.58–37.82 × 5.38–16.52 | `Clamp_N20N0D` array (80 µm frame) |
| DN | `DCNDiode` l 27.78u | 2.67, 17.56 | 0.39–38.01 × 15.28–30.10 | `DCNDiode` |
| CP | `Clamp_P_M1` ng 20, l 0.6u, frame fit | 42.23, 6.00 | 42.05–78.41 × 5.82–25.44 | `Clamp_P20N0D` array (80 µm frame) |
| DP | `DCPDiode` l 27.78u | 43.70, 26.92 | 41.86–78.60 × 25.08–39.02 | `DCPDiode` |
| RN | `rppd` w 0.5u, l 3.54u (1959 Ω) | 38.80, 9.52 | gap between the columns | CN's 0D gate tie (gate → iovss) |
| RP | `rppd` w 0.5u, l 12.9u (6768 Ω) | 40.60, 22.93 | gap between the columns | CP's 0D gate tie (gate → iovdd) |

The secondary protection is left out for now (Christoph, 2026-11-03). The buffer's input would be `pad` directly.

Wiring (cell `esd_wiring`):
- **pad:** one 0.62 µm M2 strap per clamp drain, 10 per column (IHP: 10 × 0.61). Each runs from the pad bar (y 0–3)
  up over its diode's two stripes, with Via1 onto drains and stripes. Strap 6 of the left column continues to y 40
  as the core-side `pad` pin for the buffer (M2 pin and text in the top cell, x 20.40–21.02).
- **iovss:** Via1 / M2 / Via2 stubs go into the M3 iovss rails (7–32.5, 34.5–60) from CN's inner ring, DN's anode
  frame, CP's outer ring and DP's guard ring. The stubs sit between the pad straps.
- **iovdd:**
  - CP's inner ring joins DP's cathode frame through 9 short M2 links between the pad straps and the right side.
  - DP's frame goes up to M3 iovdd (66–91.5) through two 1.26 µm M2 straps on its side bars, x 43.70–44.96 and
    75.50–76.76. IHP has 2.2 µm over DCP.
  - The n-side guard (CN's outer ring, DN's guard ring, the left leg) goes up to M3 iovdd by an M2 line at
    x 1.02–1.52, the right leg by one at x 79.00–79.45.
- **Gate ties:** each gate bus has an M1 landing on its 0.16 µm end, then M2 to its rppd. RN's other end goes in M1
  to CP's outer ring (iovss), RP's in M2 to DP's frame strap (iovdd).

Frame kept from IOPadAnalog:
- the ring rails M3 / M4 / TM1 with Via3 / TopVia1;
- the pad exit (M2 bar x 5–75, y 0–3, with its Via2);
- the NWell legs x −0.62–0.77 / 79.23–80.62, y 5.38–61.62. Their n+ taps are redrawn: Activ / M1 x 0–0.4 and
  79.6–80, y 6–61, one contact column;
- prBoundary.

Edges:
- C2's `edge_stubs` above y 84. The left iovdd n+ stub at y 148.5 is now tied like the right one.
- `edge_stubs_low`: a p+ iovss stub at IHP's interval y 65–84.26 at each edge. Its M1 joins C2's stub above.

## Free region for the buffer

- **Extent:** y ≈ 39–180, x ≈ 1.8–78.2, plus x 1.8–38, y 30–39 above the N column. That is ≈ 10 600–11 000 µm²,
  against 7165 µm² in version 1 (estimate; no latch-up spacing to the ESD zone included yet).
- **Routing obstacles:**
  - the iovdd M2 lines x 1.02–1.52, 43.70–44.96, 75.50–76.76 and 79.00–79.45, up to y 66.8;
  - the `pad` pin strap x 20.40–21.02, up to y 40.
- **Not done:** IOPadAnalog separates its ESD zone from the core with the p+ plate. Nothing replaces it here yet,
  neither an isolator ring nor a spacing rule. DRC with the latch-up rules on is clean, but that covers only what the
  deck implements.

## Checks (notes branch, `sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_s2d/template/`)

- **IHP DRC on the template alone:**
  - `sg13cmos5l_maximal.drc` with latch-up on: 0 errors (`template_maximal.lyrdb`);
  - `run_drc.py --no_density`: 32 tables, no exception, "No DRC violations" (`main_template/`).
- **Row `Filler1000 | IOPadAnalog | template | Filler200 | IOPadIOVdd | template | Filler1000` (C2's `row_check.py`,
  `row/`):**
  - the template's edge intervals are IOPadAnalog's on every layer;
  - every rail and every band is one net through the row (26 of 26);
  - maximal deck with latch-up and `run_drc.py` (LU.b): 0 violations.
- **Extraction (IHP KLayout LVS, deep, `--disable_tap_extraction`, `lvs/template_extracted.cir`):**

  | device | extracted |
  |---|---|
  | NMOS clamp | `sg13_hv_nmos` W 88 / L 0.6 (20 × 4.4): pad, gate on RN, iovss |
  | PMOS clamp | `sg13_hv_pmos` W 266.4 / L 0.6 (20 × 2 × 6.66): pad, gate on RP, iovdd |
  | diodes | `dantenna` pad / iovss and `dpantenna` pad / iovdd, each 2 stripes, 35.0 µm² |
  | gate ties | rppd 3.54u to iovss, 12.9u to iovdd |
  | ports | `iovdd`, `iovss` (merged with `vss`, as in IHP's cell and C2's), `pad` |

  These are IHP's IOPadAnalog values without SecondaryProtection.
- **One difference to IHP:** RP sits on the substrate, so its bulk is `sub!`. In IHP's Clamp_P20N0D the rppd's bulk
  is iovdd (`XR0 net2 iovdd iovdd rppd`).
