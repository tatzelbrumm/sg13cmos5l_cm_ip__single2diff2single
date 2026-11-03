<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Cleaned-out pad template for `sg13cmos5l_IOPadSingle2Diff` (draft for review, 2026-11-03, version 3)

This is IHP's `sg13cmos5l_IOPadAnalog` frame, with its protection rebuilt from Christoph's PCells (`scripts/pcells`).
All of the protection sits in the bottom region between the narrow NWell legs, and the rest of the cell is cleared
for the s2d buffer. The top cell is `sg13cmos5l_IOPadSingle2Diff`.

This file is not the macro's layout (`../sg13cmos5l_IOPadSingle2Diff.klay.gds`), and no make target reads this
folder. Earlier versions are in git: version 1 (IHP's own protection cells, SecondaryProtection kept) is commit
0f131b6, version 2 (two columns, diode on clamp) is commit c58a305.

The schematic of the protection is `../../../schematic/xschem/s2d_pad_esd.sch` (and `.sym`). Its notes explain the
resistors. Netlisted with xschem, it equals this layout's extraction device by device.

| file | |
|---|---|
| `sg13cmos5l_IOPadSingle2Diff_template.gds` | the template (sha256 657b66af196c…); the PCell context is kept (libraries `SG13_cm_clamps`, `SG13_dev`) |
| `sg13cmos5l_IOPadSingle2Diff_template.png` | the whole cell, with M3 / M4 / TM1 and their vias hidden |
| `sg13cmos5l_IOPadSingle2Diff_template_esd.png` | the protection zone, y 0–70 |
| `IOPadAnalog.png` | IHP's cell, for comparison |
| `build_template.py` | the generator: `PDKPATH=/foss/pdks/ihp-sg13cmos5l python3 build_template.py <notes>/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/out/padctx` |

## Protection (y 5.38–61.44, between the NWell legs)

Christoph, 2026-11-03: "Diodes side by side closest to the pads. No long metal wires towards the core. Clamps side
by side."

| | PCell, parameters | placement | bbox (µm) |
|---|---|---|---|
| DN | `DCNDiode` l 27.78u | (2.67, 7.66), bottom row left | 0.39–38.01 × 5.38–20.20 |
| DP | `DCPDiode` l 27.78u | (43.70, 7.66), bottom row right | 41.86–78.60 × 5.82–19.76 |
| CN | `Clamp_N_M1` ng 20, l 0.6u, frame fit | (1.20, 51.90), mirrored in y, top row left | 0.58–37.82 × 41.38–52.52 |
| CP | `Clamp_P_M1` ng 20, l 0.6u, frame fit | (42.23, 61.26), mirrored in y, top row right | 42.05–78.41 × 41.82–61.44 |
| RN | `rppd` w 0.5u, l 3.54u (1959 Ω) | gap between the columns, x 38.8, y 40.4–44.5 | CN's gate → iovss |
| RP | `rppd` w 0.5u, l 12.9u (6768 Ω) | gap between the columns, x 40.6, y 31.0–44.5 | CP's gate → iovdd |

- **The diodes** sit next to the pad exit (M2 bar y 0–3), so the pad straps to them are 5–17 µm long.
- **The clamps** are mirrored, so that their gate buses face the gap row and the rppds there. CP's iovdd ring then
  lies 7 µm under the M3 iovdd rail.
- **The secondary protection** is left out for now. The buffer's input would be `pad` directly.

Wiring (cell `esd_wiring`, M2 with Via1 / Via2). Nothing goes towards the core except the ties into the M3 iovdd rail
(up to y 66.8) and the pad pin at the zone's top edge.
- **pad:** each clamp drain has one 0.62 µm strap, 10 per column (IHP: 10 × 0.61). The straps run from the pad bar
  over the diode stripes to the clamp drains, with Via1 onto stripes and drains. One right-column strap ends at
  y 61.6 as the core-side `pad` pin (M2 pin and text in the top cell, x 61.43–62.05).
- **iovss:** Via1 / M2 / Via2 stubs into the M3 iovss rails (7–32.5 and 34.5–60), from DN's anode frame, DP's guard
  ring, CN's inner ring, CP's outer ring and RN's far end.
- **iovdd:** 9 M2 straps between the right column's pad straps, plus one on DP's right side bar (1.26 µm), join DP's
  cathode frame and CP's inner ring and run straight up into M3 iovdd (66–91.5). That makes 6.7 µm of strap width;
  IHP has 2.2 µm over DCP. The n-side guards (DN's guard ring, CN's outer ring) join the left leg in M1, and each leg
  has a 6 µm M2 tie into M3 iovdd at its top.
- **gate ties:** an M1 landing sits on each 0.16 µm gate bus end, and M2 runs from it to the rppd. RP's far end
  reaches DP's cathode frame by M2 down the gap.

The frame keeps these parts of IOPadAnalog:
- the ring rails M3 / M4 / TM1 with Via3 / TopVia1;
- the pad exit;
- the NWell legs, with their n+ taps redrawn (Activ / M1 x 0–0.4 and 79.6–80, y 6–61, one contact column);
- prBoundary.

The edges have C2's `edge_stubs` above y 84 (the left iovdd n+ stub tied like the right one) and a p+ iovss stub at
IHP's y 65–84.26 at each edge.

## Free region for the buffer

- **The core side:** y ≈ 62–180, x ≈ 1.8–78.2, which is ≈ 9000 µm² (estimate). It lies above the leg region. The only
  metal crossing into it is the iovdd ties up to y 66.8, in the band under the M3 iovdd rail.
- **The gap row y 20–41** between the diodes and the clamps is inside the protection zone. The pad and iovdd straps
  cross it, so it is not counted as free.
- **Not done:** IOPadAnalog separates its ESD zone from the core with its p+ plate, and nothing replaces that here
  yet, neither an isolator nor a spacing rule. DRC with the latch-up rules on is clean, but that covers only what the
  deck implements.

## Checks (notes branch, `sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_s2d/template/`)

- **IHP DRC on the template alone:**
  - `sg13cmos5l_maximal.drc` with latch-up on: 0 errors;
  - `run_drc.py --no_density`: 32 tables, no exception, "No DRC violations".
- **The row `Filler1000 | IOPadAnalog | template | Filler200 | IOPadIOVdd | template | Filler1000` (C2's
  `row_check.py`):**
  - the template's edge intervals are IOPadAnalog's on every layer;
  - 26 of 26 rails and bands are one net through the row;
  - row DRC (maximal with latch-up, `run_drc.py` with LU.b): 0.
- **Extraction (IHP KLayout LVS, deep, `--disable_tap_extraction`, `lvs/template_extracted.cir`):**
  - NMOS clamp W 88 / L 0.6, PMOS clamp W 266.4 / L 0.6;
  - `dantenna` / `dpantenna` 2 × 35.0 µm² each;
  - rppd 3.54u and 12.9u;
  - ports `iovdd`, `iovss` (merged with `vss`, as in IHP's cell), `pad`.
- **Schematic against layout:** `lvs/cmp_esd.py` compares the xschem netlist of `s2d_pad_esd.sch` with the
  extraction: 6 of 6 device classes equal. A copy with one terminal moved fails, as it should.
- **One difference to IHP:** RP lies on the substrate (bulk `sub!`); in IHP's Clamp_P20N0D its bulk is iovdd.
