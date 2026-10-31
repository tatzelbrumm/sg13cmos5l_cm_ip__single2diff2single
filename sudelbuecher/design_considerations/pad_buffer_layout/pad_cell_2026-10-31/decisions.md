<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C2: Christoph's decisions during the session (verbatim, Europe/Berlin)

| time | words | consequence |
|---|---|---|
| about 16:50 | "63/0 "Gate Decode" box is TEXT DRAWING, right? that can go." and "Gate decode can go if it's only TEXT DRAWING." | Checked: 63/0 is `TEXT.drawing` in `sg13cmos5l.lyp`; the top cell's shape is one polygon box x 36.355–45.815, y 147.73–180.62, no label. Deleted at integration (phase 4); the PCells' own 63/0 texts (`sub!`, `dant`, `dpant`) stay. Open point 5 of 2026-10-28 closes with it. |
| about 16:50 | "Leave CMB as is for now. When task F reports back, discuss options what to do with CMB. Maybe it's advantageous to split CMB into different parallel capacitors that, combined, will be a linear-ish capacitor without the area requirements of an actual linear, passive, capacitor." | CMB laid out as in the sheet. Relayed verbatim to K as a target for its splits / phase margin stages. CMB options to be discussed with Christoph when K reports back (see the correction below). |
| about 16:55 | "Correction: When task K reports back, start discussing capacitor options." | The capacitor discussion (CMA / CMB types and splits, CMB's orientation) starts with K's report, not with F's. |
| about 17:55 | "F should adapt its floorplan to compacted layout primitives (maybe put in context), not top down with an unrealistic floorplan cast in stone." and "DO NOT FORCE FLOORPLAN CONSTRAINTS ON THE LAYOUT PRIMITIVE AGENTS." | Method changed for stage 3: F builds the floorplan bottom-up from the drawn cells in the pad context; the stage 1/2 floorplan is not binding; nothing goes back to P / N as a constraint. Relayed verbatim to F at 17:57. (P and N had already finished, to F's stage-1 maxima.) |
| about 18:00 | "F can tweak the layout primitives ex post facto and build the floorplan from there." | F may change its copies of P's / N's cells (named `<cell>_f`, each DRC / LVS clean on its own, every change listed). Relayed verbatim to F. |
| about 18:00 | "What kind of idiocy is the suggestion to share wells between CMA and CMB?!?" | The lead's suggestion (17:4x: if CMB is turned around, CMA and CMB share one pad well and one guard ring) is withdrawn. CMA and CMB stay separate: each its own well, region and guard ring, whatever CMB's orientation. Correction sent to F. |
| about 18:05 | "Still haven't made uo my mind about CMB. Would a series resistor help, ESD wise?" then "yes, resume K with 587 Ω and 2 kΩ" | CMB still undecided. K resumed for a stage 5: IHP's secondary stage (rppd 587 Ω or 2 kΩ + two clamp diodes) in front of CMB's gate, loop and step; two extra decks. |
| about 18:15 | "yes, have F reserve a spot for the CMB stage" | F reserves a spot (2 kΩ case: rppd 1 × 7.435 µm + dantenna + dpantenna, short pad-side and CMB-gate connections) while routing, keeps CMB's gate feed cuttable at one place; the stage is not drawn until Christoph decides. |
| about 18:17 | "as long as the bias tree fits comfortably." | The bias tree has priority: F places and routes it comfortably first; the CMB-stage reserve only from what is left, else reported. |
