<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Rules: IHP sg13cmos5l instances and IHP-only lessons [IHP]

2026-10-28, Claude (Opus 5.5).
- Every value comes from `libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json` (the key is named) or
  from the deck file named. The adapter (`adapter.py`) holds the same values with their sources (table at the end).
- I1 ... I16 are the IHP instances of the generic rules G1 ... G16 in `../generic/rules.md`.
- I17 onwards are IHP-only.

## Instances of the generic rules [IHP]

| # | rule [IHP] | value, source |
|---|---|---|
| I1 | End dummy (rest) of the 2/8 mirror: 0.30/8. Saves 1.70 um per row end, 3.40 um of oa_pmir_c's width. | W = 2 Cnt_c + Cnt_a = 2 x 0.07 + 0.16 = 0.30 (json Cnt_c, Cnt_a). Narrower would be the PCell's dog-bone, a different diffusion shape. |
| I2 | The inner dummy x (P0's point partner) stays 2/8. | — |
| I3 | No ntap between rows. The shared source plate of rows 2 / 3 is Activ 0.21 apart. | Act_b = 0.21 |
| I4 | One NWell for all vdd PMOS cells. P+ to P+ across a cell boundary, what each layout costs: | NW_c1 0.62, NW_b 0.62, NW_b1 1.80 |
|    | - two separate vdd wells: NW_c1 + NW_b + NW_c1 = 1.86 um; | |
|    | - two ringed cells in the old style (Activ -> ring 1.0, ring 0.78, NW_e 0.24 = 2.02 per side): 2.02 + 0.62 + 2.02 = 4.66 um; | |
|    | - merged and abutted: 2 x NW_c1 = 1.24 um, down to Act_b 0.21 if the margins overlap; | |
|    | - wells on different nets: 0.62 + 1.80 + 0.62 = 3.04 um. | |
|    | Saving per shared edge against ringed cells: 3.42 um. | |
| I5 | No closed ring. oa_pmir_c is tap-less. The farthest P+ Activ for each set of parent tap segments: | LU_a = 20.0 (`sg13cmos5l_maximal.drc` LU.a); `../generic/check.py lu`; DRC of the context cells (`lu_context.py`, `tools/oa_core_pd_drc.py`) |
|    | - (a) top + bottom segments in the cell's margins, Activ y 38.46 ... 38.76 and -0.51 ... -0.21, under the vdd plates: 19.23 um at full width. Minimum centred length 7.86 um each; 8.2 um drawn in `ctx_tb`: 0 DRC violations incl. LU.a. The parent's NWell then reaches 0.51 um past the top / bottom edges (NW_e1). | |
|    | - (b) left edge only, Activ x -0.92 ... -0.62: 19.47 um full height. Minimum centred length 29.10 um; 29.4 um drawn in `ctx_left`: rules 0. | |
|    | - (c) left + right edges: 9.92 um. | |
|    | - (d) top edge only: 38.87 um, fails. | |
|    | oa_ms1: one segment along any full edge, 6.37 (left / right) or 13.80 (top / bottom). oa_svpg: at most 1.75. | |
| I6 | LU.a as the deck computes it: `all_ntie` (ntap + soft_n_tie) grown inside NWell by 20 um (`ext_enlarge_inside`, step 0.1). Every P+Activ in NWell not covered is an error. The Python subset (`tools/oa_core_pd_drc.py`) grows ties in 0.5 um isotropic steps. `check.py lu` takes the Euclidean distance; on these convex wells the result is the same. | `sg13cmos5l_maximal.drc` LU.a, lines 2564 ff.; `all_ntie` at 1864 |
| I7 | NWell is in the deck's ACUTE_SCOPE only (no corner < 87°), so 45° well edges are legal. But the PCell's NWell boxes have square corners, so the merged well of a full array stays a rectangle. A chamfer would save 0.066 um² per corner, and only with modified PCells: not done. | `geometry/3_2_angle.drc`, grid 0.005 (`3_1_offgrid.drc`) |
| I8 | Device cells: the library's pmosHV$9 (2/8), $13 (0.5/12.5) and $7 (1/0.45) are copied unmodified. 0.3/8 comes from `adapter.pmos_hv()`, which reproduces all 15 single-finger pmosHV cells of the library, XOR 0 (W 0.5 ... 16, L 0.45 ... 16). | — |
| I9 | Finger gap 0.25: the poly end caps (0.18 + 0.18) merge into one gate strip. The log of 2026-10-26 23:45 found the bounds: 0.21 fails Gat.b1, and gaps between 0.36 and 0.54 are forbidden (the gate strips no longer merge, but are closer than Gat_b). | Gat_b1 0.25, Gat_c 0.18, Gat_b 0.18 |
| I10 | Band = 2 (0.18 - 0.07 + 0.095 + 0.01) + 3 x 0.41 = 1.66 um, was 1.94 (tracks 0.29 at 0.50). Tracks 0.20 = Mn_a = V1_a + 2 Mn_c. Tab 0.70 = 2 x 0.19 + 0.22 + 2 x 0.05, 2 Via1 (2 tabs per 2 um column). | M1_b, Cnt_c, V1_a, V1_c, Mn_a 0.20, Mn_b 0.21, Mn_c 0.005, V1_b 0.22, V1_c1 0.05 |
| I11 | Staircase c2 / c8 / co at 0.41 pitch: 1.02 um of lines over the 1.17 um from the cell edge to the first real finger (0.62 + 0.30 + 0.25). No Metal2 over a real channel. vpg runs through the gate columns. | Mn_a + Mn_b; M2.c1 0.05 (deck text, no json key) |
| I12 | Row end: gate Metal1 column 0.18 ... 0.39 from the end finger (M1_b from its S/D Metal1, 0.21 wide for Via1), contact at 0.205 (>= Cnt_e 0.14), poly tab to 0.435 (Cnt_d 0.07). Column end 0.41 from the Activ end (stripe 0.23 + M1_b). It all fits inside NW_c1 = 0.62. | M1_b, V1_a, V1_c, Cnt_e, Cnt_d, NW_c1 |
| I13 | vdd: top / bottom plates to the cell edge (Metal1); rest straps 0.30 wide through bands A / B; middle plate. | — |
| I14 | Pins: Metal1.pin 8/2 + text 8/25, Metal2.pin 10/2 + text 10/25, as the library. The LVS tool reads texts on 8/25 and 10/25, top cell only. | library convention; `tools/oa_core_pd_lvs.py` |
| I15 | oa_pmir_c, R180 about (9.425, 19.125): XOR 0 on Activ, GatPoly, Cont, pSD, NWell and ThickGateOx. Metal1 13.78 um², Via1 0.14 um² (P0's drain tab vs the inner dummy's strap; staircase); Metal2 27.46 um² (staircase on the left, pins on the right). | `../generic/check.py sym` |
| I16 | MS1 = 8 x 0.5/12.5 in one row: 6.99 x 14.42 um, the area minimum (G16). | — |

## IHP-only lessons and pitfalls [IHP]

| # | lesson [IHP] | source / value |
|---|---|---|
| I17 | **HV PMOS needs ThickGateOx.** The pmosHV PCell draws TGO = its NWell box, because NW_c1 0.62 > TGO_a 0.27. A tap outside TGO must keep TGO_b 0.27 from it and two TGO regions TGO_e 0.86 apart. So a side tap inside TGO (NW_e1 0.62 beyond, 1.425 from the end finger) costs no more than one outside (0.62 + 0.28 + 0.30 + 0.24 = 1.44). | TGO_a, TGO_b, TGO_e, NW_e1, NW_e (json) |
| I18 | **pSD around HV PFET gates is 0.40 in W.** An ntap next to a row end must stay 0.43 from the end finger's Activ, and Gat_d 0.07 from the poly tab. | pSD_i1 0.40, pSD_d1 0.03, Gat_d 0.07 |
| I19 | **Which ties count:** N+ Activ in NWell, not under pSD. nSD is derived (Activ not pSD); no nSD layer is drawn. | `sg13cmos5l_maximal.drc` nSD_drv, `all_ntie` |
| I20 | **Tap-less cells in LVS:** the NWell is a floating bulk net, so the reference writes it as an internal net `nw`, as in the library's `d2s_pd_p`. IHP's `run_lvs.py` is run with `--disable_tap_extraction`, otherwise the ties become resistor devices. | `verification.md` of the library |
| I21 | **The uploaded deck copy is incomplete.** Missing: `layers_def.drc`, `5_5_activ`, `5_8_gatpoly`, `5_16_metal1`, `7_2_latchup`, and the LVS deck. The container's KLayout 0.28.16 cannot run the deck (needs >= 0.29.11 with Ruby). Workaround: the Python subset `tools/oa_core_pd_drc.py` (72 rules from the json; rules whose deck file is missing are marked "json only") and `tools/oa_core_pd_lvs.py` (extraction after the deck's derivations). Both are copied unchanged from the v1 assembly. | v1 report; `tools/` |
| I22 | **M2.c1 (Metal2 endcap over Via1 = 0.05) has no json key**: it is taken from the rule text of the maximal deck. | `sg13cmos5l_maximal.drc` |
| I23 | **PCell quirks:** | `adapter.pmos_hv()`, XOR 0 |
|     | - contacts spread over W are floored to 5 nm (rounding breaks W >= 5); | |
|     | - extra Activ squares under each contact column; | |
|     | - texts 'pmosHV' (63/0, R90, 0.1) and 'pmos' (51/0); | |
|     | - GatPoly pin 5/2; | |
|     | - S/D Metal1 = contact column over the full W; | |
|     | - for W < 0.30 a dog-bone (not reproduced). | |
| I24 | **Tool pitfall:** `oa_core_pd_drc.py`'s antenna step fails on the context cell `ctx_left` (circuit lookup returns None). Its rule part, run directly, reports 0. | this session |
| I25 | **First failures here:** | — |
|     | - LVS of `oa_pmir_c` mismatched on the bulk (vdd in the reference, a floating NWell in the layout; fixed by I20); | |
|     | - the generator's contact positions were off by 1 nm on wide fingers (I23); | |
|     | - the 45° well sizing moved straight edges out by 5 nm (fixed with a square intersect); | |
|     | - the score parser lost `drain=` (every finger a dummy). | |
|     | DRC of the cells failed only on LU.a, which is intended (tap-less). | |
| I26 | **PEX facts known for this project:** no PEX rule files in the upload. Magic full-RC PEX is not reproducible; use EXT_MODE=2. Magic splits ng = 20 into 20 fingers. Mismatch Monte Carlo must run on the schematic (mm_ok). | project CLAUDE.md |
| I27 | **bg_pmir_pcas_c geometry** (G17 / G18 / G20): | Act_b, Cnt_c, Cnt_a, M1_e 0.22, M1_e_w 0.3, M1_e_cr 1.0, V1_c1 |
|     | - rows of 10/1 fingers are 1.68 high (L + 2 x 0.34); all 7 row gaps are Act_b 0.21; | |
|     | - lanes at 0.305 / 0.715 / 1.125 from the drain-side Activ edge; far lane = 1.68 - 0.23 - M1_e 0.22 - 0.105; | |
|     | - gate pad via window 0.555 ... 1.125, so the gate lane is the middle one; | |
|     | - tab 1.11 (3 Via1) > M1_e_w and > M1_e_cr, so 0.22 to the opposite plate. | |
| I28 | **The library's 10/1 PCell (pmosHV$14) is not point-symmetric.** Its contact spread over W = 10 is floored to 5 nm: self-R180 contact XOR 0.0768 um² per finger, so the array's 2.458 um² = 32 x that. The 2/8 PCell (spread 0.18, exact) is symmetric. | `adapter.pmos_hv`, I23 |
| I29 | **Line gap 0.20 = V1_b 0.22 - 2 x V1_c 0.01** (> M1_b 0.18). The cell edge is 0.04 beyond the outer line (M2.c1 0.05 past the via). The first DRC run had 8 x V1.b and 8 x M2.c1. | V1_b, V1_c, M2.c1 (deck text) |
| I30 | **LU of bg_pmir_pcas_c** (45.17 x 16.15): | LU_a 20 |
|     | - one top segment in the top margin (Activ y 15.12 ... 15.42, under the vdd plate): >= 15.67 um centred; 16.0 drawn: DRC 0; | |
|     | - a full-width tie abutting the top edge: 15.53 um; | |
|     | - top + bottom: 7.97 um; | |
|     | - left + right alone: 22.46 um, fails. | |
|     | bg_ms1 / bg_svpg: any top segment (13.6 / 1.4 um). | |
| I31 | **bg_ms1: ks and en_3v3_b on the bottom edge without growing the cell.** The gate column at M1_b 0.18 from finger 0 (contact 0.205 >= Cnt_e, poly tab 0.435 < NW_c1 0.62) runs to the bottom edge. ks runs from finger 7's top on a 0.21 Metal1 line 0.18 right of it (0.39 < NW_c1 0.62). | M1_b, Cnt_e, Cnt_d, NW_c1 |

## Adapter values (generated by `adapter.table()`)

| generic name | value | source |
|---|---:|---|
| `grid` | 0.005 | sg13cmos5l_tech_default.json grid = 0.005 (drawing grid (geometry/3_1_offgrid.drc)) |
| `diff_width` | 0.15 | sg13cmos5l_tech_default.json Act_a = 0.15 (Min. Activ width) |
| `diff_space` | 0.21 | sg13cmos5l_tech_default.json Act_b = 0.21 (Min. Activ space) |
| `finger_gap` | 0.25 | sg13cmos5l_tech_default.json Gat_b1 = 0.25 (Min. space between unrelated 3.3 V GatPoly over Activ; with end caps Gat_c the poly merges into one gate strip) |
| `gate_len_min` | 0.4 | sg13cmos5l_tech_default.json Gat_a4 = 0.4 (Min. GatPoly width = channel length, 3.3 V PFET) |
| `poly_endcap` | 0.18 | sg13cmos5l_tech_default.json Gat_c = 0.18 (Min. GatPoly extension over Activ (end cap)) |
| `poly_to_diff` | 0.07 | sg13cmos5l_tech_default.json Gat_d = 0.07 (Min. GatPoly (field) space to Activ) |
| `contact_size` | 0.16 | sg13cmos5l_tech_default.json Cnt_a = 0.16 (Cont size) |
| `contact_space` | 0.18 | sg13cmos5l_tech_default.json Cnt_b = 0.18 (Min. Cont space) |
| `diff_encl_contact` | 0.07 | sg13cmos5l_tech_default.json Cnt_c = 0.07 (Min. Activ enclosure of Cont) |
| `poly_encl_contact` | 0.07 | sg13cmos5l_tech_default.json Cnt_d = 0.07 (Min. GatPoly enclosure of Cont) |
| `poly_contact_to_diff` | 0.14 | sg13cmos5l_tech_default.json Cnt_e = 0.14 (Min. Cont on GatPoly space to Activ) |
| `diff_contact_to_gate` | 0.11 | sg13cmos5l_tech_default.json Cnt_f = 0.11 (Min. Cont on Activ space to GatPoly) |
| `m1_width` | 0.16 | sg13cmos5l_tech_default.json M1_a = 0.16 (Min. Metal1 width) |
| `m1_space` | 0.18 | sg13cmos5l_tech_default.json M1_b = 0.18 (Min. Metal1 space) |
| `m1_encl_contact` | 0 | sg13cmos5l_tech_default.json M1_c = 0 (Min. Metal1 enclosure of Cont) |
| `m1_endcap_contact` | 0.05 | sg13cmos5l_tech_default.json M1_c1 = 0.05 (Min. Metal1 endcap enclosure of Cont) |
| `m1_area` | 0.09 | sg13cmos5l_tech_default.json M1_d = 0.09 (Min. Metal1 area (um2)) |
| `m1_wide_space` | 0.22 | sg13cmos5l_tech_default.json M1_e = 0.22 (Min. Metal1 space next to Metal1 wider than M1_e_w, parallel run > M1_e_cr) |
| `m1_wide_width` | 0.3 | sg13cmos5l_tech_default.json M1_e_w = 0.3 (Metal1 counts as wide for M1_e above this width) |
| `m1_wide_run` | 1 | sg13cmos5l_tech_default.json M1_e_cr = 1 (M1_e applies above this parallel run) |
| `via1_size` | 0.19 | sg13cmos5l_tech_default.json V1_a = 0.19 (Via1 size) |
| `via1_space` | 0.22 | sg13cmos5l_tech_default.json V1_b = 0.22 (Min. Via1 space) |
| `m1_encl_via1` | 0.01 | sg13cmos5l_tech_default.json V1_c = 0.01 (Min. Metal1 enclosure of Via1) |
| `m1_endcap_via1` | 0.05 | sg13cmos5l_tech_default.json V1_c1 = 0.05 (Min. Metal1 endcap enclosure of Via1) |
| `m2_width` | 0.2 | sg13cmos5l_tech_default.json Mn_a = 0.2 (Min. Metal2 width) |
| `m2_space` | 0.21 | sg13cmos5l_tech_default.json Mn_b = 0.21 (Min. Metal2 space) |
| `m2_encl_via1` | 0.005 | sg13cmos5l_tech_default.json Mn_c = 0.005 (Min. Metal2 enclosure of Via1) |
| `m2_endcap_via1` | 0.05 | ihp_sg13cmos5l literal 0.05: sg13cmos5l_maximal.drc rule text M2.c1 'Min. Metal2 endcap enclosure of Via1 = 0.05' (no json key) |
| `well_width` | 0.62 | sg13cmos5l_tech_default.json NW_a = 0.62 (Min. NWell width) |
| `well_space_same` | 0.62 | sg13cmos5l_tech_default.json NW_b = 0.62 (Min. NWell space or notch, same net (merged below this)) |
| `well_space_diff` | 1.8 | sg13cmos5l_tech_default.json NW_b1 = 1.8 (Min. PWell width between NWell regions, different nets) |
| `well_encl_pdiff` | 0.62 | sg13cmos5l_tech_default.json NW_c1 = 0.62 (Min. NWell enclosure of P+Activ inside ThickGateOx) |
| `well_encl_tap` | 0.62 | sg13cmos5l_tech_default.json NW_e1 = 0.62 (Min. NWell enclosure of an NWell tie in N+Activ inside ThickGateOx) |
| `well_to_ndiff` | 0.62 | sg13cmos5l_tech_default.json NW_d1 = 0.62 (Min. NWell space to external N+Activ inside ThickGateOx) |
| `pimp_encl_pdiff` | 0.18 | sg13cmos5l_tech_default.json pSD_c = 0.18 (Min. pSD enclosure of P+Activ in NWell) |
| `pimp_encl_gate` | 0.4 | sg13cmos5l_tech_default.json pSD_i1 = 0.4 (Min. pSD enclosure of PFET gate inside ThickGateOx) |
| `pimp_to_ntap` | 0.03 | sg13cmos5l_tech_default.json pSD_d1 = 0.03 (Min. pSD space to N+Activ in NWell) |
| `hvox_encl_diff` | 0.27 | sg13cmos5l_tech_default.json TGO_a = 0.27 (Min. ThickGateOx extension over Activ) |
| `hvox_encl_gate` | 0.34 | sg13cmos5l_tech_default.json TGO_c = 0.34 (Min. ThickGateOx extension over GatPoly over Activ) |
| `hvox_space` | 0.86 | sg13cmos5l_tech_default.json TGO_e = 0.86 (Min. ThickGateOx space (merged below this)) |
| `lu_tap_dist` | 20 | sg13cmos5l_tech_default.json LU_a = 20 (sg13cmos5l_maximal.drc LU.a: Max. space from any portion of P+Activ inside NWell to an nSD-NWell tie (grown inside NWell)) |
| `lu_tap_cont_ext` | 6 | sg13cmos5l_tech_default.json LU_d = 6 (sg13cmos5l_maximal.drc LU.d: Max. extension of NWell tie Activ beyond Cont) |

| layer | GDS | source |
|---|---|---|
| `diff` | 1/0 | sg13cmos5l_maximal.drc:1455 Activ |
| `poly` | 5/0 | sg13cmos5l_maximal.drc:1460 GatPoly |
| `poly_pin` | 5/2 | sg13cmos5l_maximal.drc:1461 GatPoly_pin (drawn by the PCell) |
| `contact` | 6/0 | sg13cmos5l_maximal.drc:1464 Cont |
| `m1` | 8/0 | sg13cmos5l_maximal.drc:1467 Metal1 |
| `m1_pin` | 8/2 | sg13cmos5l_maximal.drc:1468 Metal1_pin |
| `m1_text` | 8/25 | Metal1 text: the library's pin convention (pad_buffer_cells.gds); LVS labels |
| `m2` | 10/0 | sg13cmos5l_maximal.drc:1473 Metal2 |
| `m2_pin` | 10/2 | sg13cmos5l_maximal.drc:1474 Metal2_pin |
| `m2_text` | 10/25 | Metal2 text: as m1_text |
| `pimp` | 14/0 | sg13cmos5l_maximal.drc:1478 pSD |
| `via1` | 19/0 | sg13cmos5l_maximal.drc:1480 Via1 |
| `well` | 31/0 | sg13cmos5l_maximal.drc:1490 NWell |
| `hvox` | 44/0 | sg13cmos5l_maximal.drc:1498 ThickGateOx |
| `heat` | 51/0 | drawn by the pmosHV PCell (thermal marker); not read by the DRC deck |
| `text` | 63/0 | sg13cmos5l_maximal.drc:1508 TEXT (device tags) |
