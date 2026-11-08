<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# slot7_with_pads: slot_7 next to the two custom pads, at their harness positions (2026-11-08)

Generated, not hand-drawn, by `compose.py` (KLayout 0.30.12 Python, PDK layer properties
`ihp-sg13cmos5l/libs.tech/klayout/tech/sg13cmos5l.lyp`), in a Claude Code cloud session. No C2PA stamp: the files went
from the container into git directly, not through a chat attachment.

| file | what |
|---|---|
| `slot7_with_pads.png` | whole slot_7 with the S2D pad (lower) and the D2S pad (upper) to its right, core sides facing the slot |
| `slot7_pad_interface.png` | close-up of the slot / pad edge, chip x 1880..1960, y 2255..2465 µm: the 13 slot pins (Metal3) ending at the pads' core pins |
| `slot7_with_pads.gds` | the composed layout (top cell `slot7_with_pads`), chip coordinates |
| `compose.py` | `python3 -I compose.py <dir>`, `<dir>` holding the three input GDS below |

Inputs (`tatzelbrumm/sg13cmos5l_cm_slot7`, `main` @ `454da6a`, slot_7 v2): `final/gds/slot_7.gds`,
`pads/sg13cmos5l_IOPadSingle2Diff/sg13cmos5l_IOPadSingle2Diff.gds`, `pads/sg13cmos5l_IOPadDiff2Single/sg13cmos5l_IOPadDiff2Single.gds`.

Placement, chip coordinates in µm:
- `slot_7` at (1379.95, 2170.05), the slot 7 wrapper position (`make projects-gds`).
- The pads per `magic/sg13cmos5l_padframe.mag` of the harness fork `tatzelbrumm/sg13cmos5l_ocd_chipalooza`, branch
  `delivery-test`: `transform 0 -1 416000 1 0 452000` (S2D, `pad_s7_an_0`) and `… 474000` (D2S, `pad_s7_an_1`) at
  magscale 0.005 µm = rotation 90°, displacement (2080, 2260) / (2080, 2370), plus the 16.1 µm frame offset →
  (2096.1, 2276.1) / (2096.1, 2386.1).

Cross-check: the S2D `vref` core pin (pad x 6.205 µm) lands at y 2282.305 µm, and the slot pin `s7_an_0_vref` (slot y 112.26 µm)
at 2282.31 µm.

What it does **not** show: the harness's own Via2 + 0.29 µm Metal3 straps in the padframe (`scripts/custom_io.tcl`) that
join each pad's Metal2 core pin to its slot pin, and the rest of the padframe and frame. It proves placement and pin
alignment only, not connectivity; for connectivity see the harness net check (`docs/custom_pads/` on the fork).
