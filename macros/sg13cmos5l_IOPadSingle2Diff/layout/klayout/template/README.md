<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Cleaned-out pad template for `sg13cmos5l_IOPadSingle2Diff` (draft for review, 2026-11-03, version 4)

This is IHP's `sg13cmos5l_IOPadAnalog` frame with its protection rebuilt from Christoph's PCells (`scripts/pcells`).
The protection is packed at the pad side, between the narrow NWell legs, and the rest of the cell is cleared for
the s2d buffer. The top cell is `sg13cmos5l_IOPadSingle2Diff`. This file is not the macro's layout
(`../sg13cmos5l_IOPadSingle2Diff.klay.gds`), and no make target reads this folder.

Earlier versions are in git:

| version | commit | arrangement |
|---|---|---|
| 1 | 0f131b6 | IHP's own protection cells, SecondaryProtection kept |
| 2 | c58a305 | two columns, diode on clamp |
| 3 | 933fa9c | diodes at the pad, clamps at the top of the leg region, a 21 µm gap of straps between them |

Schematic of the protection: `../../../schematic/xschem/s2d_pad_esd.sch` (and `.sym`). Its notes explain the
resistors. Its xschem netlist equals this layout's extraction device by device.

| file | |
|---|---|
| `sg13cmos5l_IOPadSingle2Diff_template.gds` | the template (sha256 80b38a47cc65…); the PCell context is kept (libraries `SG13_cm_clamps`, `SG13_dev`) |
| `sg13cmos5l_IOPadSingle2Diff_template.png` | the whole cell, M3 / M4 / TM1 and their vias hidden |
| `sg13cmos5l_IOPadSingle2Diff_template_esd.png` | the protection zone, y 0–70 |
| `IOPadAnalog.png` | IHP's cell, for comparison |
| `build_template.py` | the generator: `PDKPATH=/foss/pdks/ihp-sg13cmos5l python3 build_template.py <notes>/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/out/padctx` |

## Protection (y 5.38–41.6 at the pad side, between the NWell legs)

Christoph, 2026-11-03:
- "Diodes side by side closest to the pads. No long metal wires towards the core. Clamps side by side."
- "If there's no good reason for keeping the wires that long, shorten them."

| | PCell, parameters | origin (µm) | bbox (µm) |
|---|---|---|---|
| DN | `DCNDiode` l 27.78u | (2.67, 7.66), bottom row left | 0.39–38.01 × 5.38–20.20 |
| DP | `DCPDiode` l 27.78u | (43.70, 7.66), bottom row right | 41.86–78.60 × 5.82–19.76 |
| CN | `Clamp_N_M1` ng 20, l 0.6u, frame fit | (1.20, 19.58), on DN, n+ rings abutting | 0.58–37.82 × 18.96–30.10 |
| CP | `Clamp_P_M1` ng 20, l 0.6u, frame fit | (42.23, 19.58), on DP, p+ rings abutting | 42.05–78.41 × 19.40–39.02 |
| RN | `rppd` w 0.5u, l 3.54u (1959 Ω) | (38.80, 23.16), in the gap between the columns | CN's gate → iovss |
| RP | `rppd` w 0.5u, l 12.9u (6768 Ω) | (40.60, 23.17), in the gap between the columns | CP's gate → iovdd |

The rings abut as in IHP's cells, where DCNDiode sits on Clamp_N and DCPDiode on Clamp_P. The secondary protection
is left out for now, so the buffer's input would be `pad` directly.

Wiring (cell `esd_wiring`, M2 with Via1 / Via2):
- **pad:** one 0.62 µm strap per clamp drain, 10 per column (IHP: 10 × 0.61). Each runs from the pad bar (y 0–3)
  over the diode stripes to the clamp drains. Their length is 24 µm on the left and 33 µm on the right; version 3
  had 47 / 56 µm. One left strap ends 1.7 µm above CN, at y 31.2, as the core-side `pad` pin (M2 pin and text in
  the top cell, x 20.40–21.02).
- **iovss:** Via1 / M2 / Via2 stubs into the M3 iovss rails (7–32.5, 34.5–60), from DN's anode frame, DP's guard
  ring, CN's inner ring, CP's outer ring and RN's far end.
- **iovdd:** this is the one connection that has to be long, because M3 / M4 / TM1 over the whole zone (y 7–60) are
  iovss rails and the first iovdd metal is the M3 rail at y 66.
  - 9 straps between the right column's pad straps, plus one on DP's right side bar, join DP's cathode frame and
    CP's inner ring. They end in a 2.2 µm M2 bar just above CP (y 39.4–41.6), which matches IHP's iovdd width
    over DCP.
  - Two risers at the column's edges, x 42.6–45.2 and 75.5–78.4, take the bar up into M3 iovdd. The band above the
    clamps stays free between them.
  - The n-side guards (DN's guard ring, CN's outer ring) join the left leg in M1. Each leg has a 6 µm M2 tie into
    M3 iovdd at its top.
- **gate ties:** an M1 landing on each 0.16 µm gate-bus end, then M2 to the rppd. RN's far end goes by Via1 / Via2
  into M3 iovss; RP's goes in M2 to DP's cathode frame.

Frame kept from IOPadAnalog:
- the ring rails M3 / M4 / TM1, with Via3 / TopVia1;
- the pad exit;
- the NWell legs, with their n+ taps redrawn (Activ / M1 x 0–0.4 and 79.6–80, y 6–61, one contact column);
- prBoundary.

Edges: C2's `edge_stubs` above y 84 (the left iovdd n+ stub tied like the right one), and a p+ iovss stub at IHP's
y 65–84.26 at each edge.

## Free region for the buffer (estimate)

| part | area |
|---|---|
| left half, from y ≈ 31.5 (above CN and its pad pin), x 1.8–38 | ≈ 1100 µm² to y 62 |
| right half, from y ≈ 42 (above the iovdd bar), x 45.2–75.5 between the risers | ≈ 600 µm² to y 62 |
| everything above y 62 | ≈ 9000 µm² |
| total | ≈ 10 600 µm² (version 3: ≈ 9000) |

- **Routing obstacles:** the two iovdd risers (M2, up to y 66.8), the leg ties at the edges, and RP / RN in the gap
  (to y 36.7).
- **Not done yet:** IOPadAnalog separates its ESD zone from the core with the p+ plate, and nothing here replaces it,
  neither an isolator nor a spacing rule. DRC with the latch-up rules on is clean, but that covers only what the deck
  implements.

## Checks (notes branch, `sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_s2d/template/`)

- **IHP DRC on the template alone:**
  - `sg13cmos5l_maximal.drc` with latch-up on: 0 errors;
  - `run_drc.py --no_density`: 32 tables, no exception, "No DRC violations".
- **Row `Filler1000 | IOPadAnalog | template | Filler200 | IOPadIOVdd | template | Filler1000`** (C2's
  `row_check.py`):
  - the edge intervals are IOPadAnalog's on every layer;
  - 26 of 26 rails and bands are one net through the row;
  - row DRC (maximal with latch-up; `run_drc.py` with LU.b): 0.
- **Extraction** (IHP KLayout LVS, deep, `--disable_tap_extraction`, `lvs/template_extracted.cir`):
  - NMOS clamp W 88 / L 0.6, PMOS clamp W 266.4 / L 0.6;
  - `dantenna` / `dpantenna` 2 × 35.0 µm² each;
  - rppd 3.54u and 12.9u;
  - ports `iovdd`, `iovss` (merged with `vss`, as in IHP's cell), `pad`.
- **Schematic against layout:** `lvs/cmp_esd.py` (the xschem netlist of `s2d_pad_esd.sch` vs the extraction): 6 of 6
  device classes equal. A copy with one terminal moved fails.
- **One difference to IHP:** RP lies on the substrate (bulk `sub!`); in IHP's Clamp_P20N0D its bulk is iovdd.
