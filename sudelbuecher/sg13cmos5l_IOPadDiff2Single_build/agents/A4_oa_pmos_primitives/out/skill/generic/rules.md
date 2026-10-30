<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Rules: process-agnostic [generic]

2026-10-28, Claude (Opus 5.5). These are the do / don't rules followed in the compact PMOS primitives (OA core: G1–G16; bandgap
core, 05:20: G17–G24). Each rule is
written with the adapter's generic rule names; the generator computes every spacing from them.
- Every line here is **[generic]**.
- The IHP sg13cmos5l value of each rule, with its deck key, is in `../ihp_sg13cmos5l/rules.md` under the same
  number (G1 here = I1 there).

## Do / don't

| # | rule [generic] | forced by (adapter names) |
|---|---|---|
| G1 | **End dummies one contact wide.** A row's end dummy (the rest) needs only its first neighbour environment: the diffusion edge and the gate strip at `finger_gap`, same L. W = `2 diff_encl_contact + contact_size` (`min` in the score). | contact enclosure; `finger_gap` |
| G2 | **Inner dummies keep full size** when they are a matched device's symmetry partner (P0 <-> x). Otherwise the real neighbours' environment loses its symmetry. | point symmetry of the real devices |
| G3 | **Never a well tap between the rows of an array.** Taps only at the periphery. | the user's rule; latch-up allows it (G6) |
| G4 | **One well per supply net, merged across cells.** The cell's well is one polygon reaching the cell edge (`well_encl_pdiff` beyond the outer diffusion). Neighbouring cells on the same net overlap or abut their wells. There is never a second well on the same net inside a cell. | `well_space_same`, `well_space_diff`, `well_encl_pdiff` (savings in the IHP instance, I4) |
| G5 | **No closed ring by default.** Tap segments go only where the latch-up distance needs them, counting the parent's taps. They follow the outline (any rectilinear path, `tap_path`), never enclose empty area, and are one contact column wide (`2 diff_encl_contact + contact_size`). | `lu_tap_dist`, `lu_tap_cont_ext` |
| G6 | **Check latch-up against the taps the parent will provide.** State them: segment, side, length. Report the farthest P diffusion per tap set (`check.py lu`). | `lu_tap_dist` |
| G7 | **Well outline follows the devices.** Union of the device cells' wells + `well_encl_pdiff` around the diffusion; 45° corners only if the deck's angle rules allow them for the well layer (`WELL_45`); notches below `well_space_same` closed. No bounding rectangle by default. | well angle / grid rules |
| G8 | **Use unmodified device cells** (PCell copies or adapter-drawn equivalents verified XOR 0 against the PCell). Never trim contacts or break an array. | the user's rule; LVS device recognition |
| G9 | **Fingers turned (R270), one AREF per run of equal cells** (repetition); gaps `finger_gap` so the gate end caps merge into one strip. | `finger_gap`, `poly_endcap` |
| G10 | **Drain bands:** tracks `m2_width` at pitch `m2_width + m2_space`. Band height = `2 (m1_space - S/D stripe offset + via1_size/2 + m1_encl_via1) + (n - 1) pitch`. Lower row's tabs at the column's left edge, upper row's at its right edge, 2 vias per tab (`2 via1_size + via1_space + 2 m1_endcap_via1`). | Metal1 / Metal2 / Via1 rules |
| G11 | **Join two bands by a Metal2 staircase over the row ends** (outermost net = outermost line, each track ending at its own line). The gate net needs no line: the Metal1 gate columns carry it. | `m2_space` between a line and the next track |
| G12 | **Gate contact column `m1_space` from the end finger's S/D Metal1**, contact `>= poly_contact_to_diff` from the diffusion, poly tab `poly_encl_contact` beyond it. Its end is `m1_space` from the plates. | `m1_space`, `poly_contact_to_diff`, `poly_encl_contact` |
| G13 | **Supply without a rail:** outer source plates run to the cell edge. The end-column dummies' D = S straps continue through the bands as the supply spine between plates. | connectivity; no area |
| G14 | **Pins on the cell edge**, one per net, `<metal>_pin` box + `<metal>_text`, Metal1 / Metal2 only. Track pins at one band's right end, in the order the neighbour expects. | the user's convention |
| G15 | **The pattern is data.** The score in `patterns.md` builds the cell. Check the point symmetry of the score (`point_image`) and of the layout (`check.py sym`: device layers XOR 0 with the R180 image). | — |
| G16 | **Let the layout drive.** Choose the finger count / series split by area: (n pitch + 2 margins) x (L/n + S/D + 2 margins). For a 0.5/100 chain the optimum is flat: n = 7 ... 10 lie within 0.4 % of n = 8 (the minimum); n = 4 costs +7 %; two rows of 4 cost +10 % (row gap + margins). So keep the existing split, and record any change as backannotation. | area formula (report) |
| G17 | **Short-L fingers: no bands.** When a row is about as high as a track band, run each row's tracks over its own channel and make every row gap the minimum diffusion space. Every finger gets the same tab (identical metal over all matched channels); only the via picks the lane. | `diff_space`; lane positions from the stripe and wide-metal rules (G20) |
| G18 | **Mirror + cascode in one stack:** the cascode row facing a mirror row carries its letters, so in every column the mirror drain and the cascode source are one node. That node is one Metal1 joint across the row gap, with no track for it. The intermediate nets keep one lane each, so they stay single nets and the netlist does not change. | `diff_space`, `m1_space` |
| G19 | **Latin-square maps:** every row and every column holds the same multiset (e.g. b a o o for 1 : 1 : 2). A linear gradient then cancels per row and per column, not only at the centroid; combine with R180. | — |
| G20 | **Wide tabs keep the wide-metal space.** A tab wider than `m1_wide_width` with a run longer than `m1_wide_run` (3 vias) keeps `m1_wide_space` to the facing stripe or plate. That sets the far lane. | `m1_wide_space`, `m1_wide_width`, `m1_wide_run` |
| G21 | **Vias on neighbouring vertical lines, or on a pad and a line, may share a lane:** line gap >= max(`m1_space`, `via1_space - 2 m1_encl_via1`). | `via1_space`, `m1_encl_via1` |
| G22 | **A via on the outermost line needs its Metal2 endcap**, so the cell edge lies `m2_endcap_via1` beyond the via. | `m2_endcap_via1` |
| G23 | **Check the device cell's own symmetry first.** A PCell that floors its contact spread to the grid is not exactly symmetric. Report the array's XOR net of n x the cell's self-XOR. | `grid` |
| G24 | **Side lines carry pins at either end.** Full-height Metal1 lines put a net on the top and the bottom edge at once. A side-edge pin needs Metal1 out to the cell edge. A chain's end can run down a line inside the well margin, so ks / gate reach the bottom without growing the cell. | `m1_space`, `well_encl_pdiff` |

## Pitfalls [generic]

- **A tap-less cell's bulk is an internal net.** In the cell's own LVS reference the well is a floating net (`nw`),
  not the supply. Writing the supply there gives a bulk mismatch: it happened first on `oa_pmir_c`. The parent ties it.
- **Score parser:** a voice attribute `drain=` must reach the field the generator reads. A silent mismatch turned
  every finger into a dummy and the build failed on an empty track.
- **Device reproduction:** a PCell spreads contacts evenly and floors each position to the grid. Rounding instead
  shifts contacts by 1 nm on wide fingers (found by XOR on W >= 5).
- **45° well corners:** sizing by the enclosure + one grid in 45° mode also moves the straight edges out by a grid.
  Intersect with a square sizing to keep straight edges exact.
- **The device cells' own wells have square corners.** The well polygon of a full rectangular array is therefore
  a rectangle, whatever the angle rules allow. Chamfers would need modified PCells (G8).
- **Texts outside a zoomed matplotlib window** are still drawn and wreck the layout: use `clip_on=True`.
- **Two tools give different numbers for the same rule.** Report which tool and which rule implementation.
- **Wide tabs (bandgap stack):** the first DRC run had 8 x V1.b (a pad via and a line via on the same lane, 0.20
  apart) and 8 x M2.c1 (vias on the outermost line at the cell edge). G21 and G22 fixed them. LVS matched at once,
  because the netlist came from the same device list.
