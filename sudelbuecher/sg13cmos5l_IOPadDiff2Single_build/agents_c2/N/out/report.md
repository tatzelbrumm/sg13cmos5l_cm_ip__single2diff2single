# N report: compact NMOS cells of d2s_mpdda_pd, IHP sg13cmos5l (2026-10-31, 17:00-17:45 CET)
"Measured" = from `d2s_n_cells.gds` (`measure.py`, `measure_out.txt`) or the check logs in `logs/`. "Reasoning" is marked. Rule values: `sg13cmos5l_tech_default.json` ("J"
key) or `sg13cmos5l_maximal.drc` ("MAX"), through A3's adapter; no number of my own except layout choices (stub heights, jog levels).

## Result (measured)
| cell | before (library) | after | F's max | DRC run_drc.py | LVS run_lvs.py |
|---|---|---|---|---|---|
| `sinks_6x6_c` (upright) | 53.37 x 18.12 = 967 | **15.525 x 46.79 = 726** (-25 %) | 18.0 x 53.5 (want 17.5 x 52) | 0 | match |
| `sinks_6x6_s2d_c` (R90, native) | | 46.79 x 15.525 | | 0 | match |
| `d2s_casc_n_c` (upright) | 36.12 x 11.94 = 431 | **9.73 x 33.12 = 322** (-25 %) | 11.0 x 34.0 | 0 | match |
| `d2s_ab_n_c` | 11.34 x 7.01 = 80 | **6.86 x 5.44 = 37** (-53 %) | 7.5 x 9.5 | 0 | match |
| `d2s_pd_n_c` | 2.50 x 2.04 = 5.1 | **3.52 x 2.04 = 7.2** | 3.5 x 2.5 | 0 | match |
- DRC = `run_drc.py --no_density --mp=4` (main tables incl. LU.b, plus the maximal deck with LU.a/c/c1/d/d1, Pin, angle, offgrid), 0 items, no "generated an exception" (`checks_summary.txt`, `logs/`). LVS = `run_lvs.py --disable_tap_extraction`, no `--implicit_nets`.
- The checks bite (injected on copies): removing the pSD of the tie gives LU.b; removing the vbnc Via1 of casc gives LVS "do not match".
- First runs failed and were fixed once each (sinks: TGO.f sliver 0.84 wide at the tie; ab_n: three contacts outside the M1 bar, Via1 off the bar; casc: strap not touching the tie, LVS BNC source floating; pd: poly bar 0.03 outside the TGO); the runs listed above are the clean ones after the last fix. Two builds give the same bytes.
- `d2s_pd_n_c` is 0.02 wider than F's 3.5: the minimum is 0.27 (TGO) + 1.13 + 0.21 (Act_b) + 1.13 + 0.21 (Act_b = pSD_d 0.18 + pSD_c1 0.03) + 0.30 (tie) + 0.27 (TGO) = 3.52 with its own tie. Without a tie it would be 3.01, but then LU.b fails on its own. Merging it into `d2s_ab_n_c` (shared tie) was not built.

## Construction (same for all cells)
- Library PCell fingers unrotated (gate vertical, W along y), stacked along y at Gat.b1 0.25 (poly of a column merges), columns side by side at Act.b 0.21; devices are copies of the library cells (nmosHV, $12 = 2/6, $1 = 15/3, $2 = 1/8, $3 = 4.4/1, $5 = 1/0.45). Metal1 / Metal2 / Via1 only; no NWell; TGO as one polygon (Activ + TGO_a 0.27, closed at TGO_e 0.86).
- One p+ tie strip per cell on one outer edge (Activ 0.30 = Cnt_a + 2 Cnt_c, pSD +0.03 = pSD_c1, contacts at 0.34, extension beyond contact 0.07 <= LU_d 6). None between columns (Christoph's rule 1). Bulk = vss through the tie's M1.
- Gate contacts sit on a poly plate beyond the end of the columns (Cnt_e 0.14, M1_b 0.18 to the stripe ends). Via1 only on M1 pads of 0.21 x (0.29 or 1.11); M2 0.29 wide.

## sinks_6x6_c
- Device map (measured, bottom to top; S left / D right in A, mirrored in B = point reflection):
  A: BN, SY, SX, SX, SY, SY, SX, dummy(2/6); B: dummy(2/6), SX, SY, SY, SX, SX, SY, dummy(2/6). `X Y Y X X Y / Y X X Y Y X` as before, BN and a dummy at the ends. SX = 6 x 6/6, SY = 6 x 6/6.
- Centroids of X and Y: both (7.2375, 22.875) in cell coordinates (asserted in the build): the narrow dummies shift column B by the same 4.0 for all its fingers, so the equality of the library map survives.
- Finger count is a parameter: `rep` of `sinks()` (env `SINK_REP`), the map repeats per column: A = BN, (Y X X Y Y X) x rep, dummy; B = point-reflected. rep = 4 (the 4x option) builds to 15.525 x 159.29 um, centroid assert passes, DRC 0 and LVS match (checked in /tmp, not shipped).
- x / y: each D stripe has an M1 stub (offset 1.5 in A, 4.5 in B within the finger) to the M2 trunks x / y in the 1.115 channel (0.51 pitch); crossings are M1 under M2. Bottom pins jog to x 10.80 / 11.31 so that they meet casc_n's x / y top pins (3.80 / 4.31 + 7.0, F's x offsets 59.5 / 66.5).
- vss bus: S lines of both columns and the dummies' D stripes, joined by an M1 strap above column A; the tie strip is a separate M1 strip that joins the bus only at the tap pad (0.6 x 0.6, y 5.54-6.14 above the bottom). LU.b: farthest N+ Activ 14.69 um from the tie (limit 20), one tie strip on the right edge.
- `sinks_6x6_s2d_c` = the same cell flattened and rotated R90 (left -> bottom, bottom -> right), same map, same fingers; this is also the "native" delivery F offered. No s2d-specific change.

## d2s_casc_n_c
- CX CX in the left column, CY CY in the right column (S inner = x / y, D outer = l1 / b), BNC (1/8) above, on one poly plate with both columns (diode: its D stripe on the vbnc bar). The library had CX CY / CY CX; cascodes need no centroid (`layout_primitives.md` P6), so the map is a deliberate change (pure stripe lines, no M1 crossing; reasoning: mismatch of a cascode is divided by the cascode gain).
- LU.b: farthest N+ Activ 8.89 um. The tie runs the full height at x 9.16-9.46, beyond BNC (8.68 wide).

## d2s_ab_n_c and d2s_pd_n_c
- ab_n: ABN, FNL, RN2 side by side (b|ABN|a, l1|FNL|l2, vabn|RN2|dabn); vabn bar over the three gates; LU.b 5.67. Right edge: TGO runs 0.62 (NW_d1) beyond the N+ Activ (Activ ends at x 6.24, outline at 6.86), so F can put the NWell at the outline edge.
- pd_n: SB (S vsso left, D b right), SABN (S vss, D vabn), poly bar, en_3v3_b over SB's gate; tie right of SABN, joined to the vss stripe under the Activ. LU.b 2.68.

## Edge table (measured; N+ / P+ Activ distance inside the outline; TGO is the outline everywhere, no NWell, no pSD outside the tie)
| cell | left | right | bottom | top |
|---|---|---|---|---|
| sinks | N+ 0.27 | tie P+ 0.27 (x 14.955-15.255) | N+ 0.52 | N+ 0.52 |
| casc | N+ 0.27 | tie P+ 0.27 (x 9.16-9.46) | N+ 0.52 | N+ 0.52 |
| ab_n | tie P+ 0.27 (x 0.27-0.57) | N+ 0.62 | N+ 0.52 | N+ 0.52 |
| pd_n | N+ 0.27 | tie P+ 0.27 (x 2.95-3.25) | N+ 0.52 | N+ 0.52 |
NW.d1 / NW.f1 0.62 therefore costs F 0.35 at a 0.27 edge and 0.10 at a 0.52 edge (reasoning from these numbers).

## Pins (coordinates from the cell's lower-left corner; centre x, y; every pin box lies on the outline edge)
| cell | pin | side | layer | position (centre) | size |
|---|---|---|---|---|---|
| sinks | x | bottom | M2 | 10.80, 0.30 | 0.29 x 0.60 |
| sinks | y | bottom | M2 | 11.31, 0.30 | 0.29 x 0.60 |
| sinks | vbn | bottom | M2 | 1.47, 0.285 | 0.29 x 0.57 |
| sinks | x / y | left | M2 | 0.35, 17.52 / 0.35, 11.27 | 0.70 x 0.29 |
| sinks | vss (tap pad = the bus's single tap) | right | M1 | 15.225, 5.84 | 0.60 x 0.60 |
| casc | b / l1 | bottom | M2 | 7.69, 0.30 / 0.42, 0.30 | 0.29 x 0.60 |
| casc | x / y | top | M2 | 3.80, 32.82 / 4.31, 32.82 | 0.29 x 0.60 |
| casc | vbnc | left | M2 | 0.35, 31.095 | 0.70 x 0.29 |
| casc | vss | right | M1 | 9.575, 5.175 | 0.31 x 0.31 |
| ab_n | a / dabn | bottom | M1 | 2.31, 0.16 / 6.09, 0.16 | 0.29 x 0.32 |
| ab_n | b | bottom | M2 | 0.93, 0.30 | 0.29 x 0.60 |
| ab_n | l1 / l2 / vabn | top | M2 | 2.82 / 4.20 / 4.71, 5.14 | 0.29 x 0.60 |
| ab_n | vss | left | M1 | 0.155, 2.175 | 0.31 x 0.31 |
| pd_n | vsso / b | bottom | M1 | 0.42 / 1.25, 0.16 | 0.29 x 0.32 |
| pd_n | en_3v3_b / vss / vabn | top | M1 | 0.835 / 1.76 / 2.59, 1.88 | 0.29 x 0.32 |
Pin boxes: Metal1.pin 8/2 + text 8/25, Metal2.pin 10/2 + text 10/25. The sinks' R90 copy has the same pins rotated (`measure_out.txt`).
- Metal2 keep-out for F: the whole outline except the vss tap column (sinks x >= 14.9, casc x >= 9.1). Inside are the x / y / l1 / b trunks, jogs and exits; extra M2 over the fingers would also change the matched stress and coupling (reasoning). Via stack on the tap pad: Via1 on the pad, M2 over it.

## Netlist changes for the backannotation (reference: `d2s_n_cells.cdl`, one line per drawn finger)
1. SX / SY: `w=36u l=6u ng=4` -> 6 fingers 6/6 each (same total W / L; `layout_primitives.md` §7 decision 1; I_Q +3.4 % as simulated there). BN = 1 finger 6/6 in the column (as library).
2. Dummies of the sinks: 3 x 2/6 (D = S = vss, G = vbn), the library had 3 x 6/6. Gate area on vbn falls by 36 um2 (reasoning: negligible); no current.
3. casc_n: CX, CY `ng=2` unchanged (2 x 15/3 each), BNC 1/8 unchanged; map change as above.
4. ab_n: RN1 dropped; RN2 source is `dabn` (library: n2); port list `a b dabn l1 l2 vabn vss`. W/L unchanged (4.4/1).
5. pd_n: SB source `vsso`, SABN source `vss` (library: shared vss). **Bulk:** `d2s_mpdda_pd` has XSB bulk = vsso; the layout has one substrate (the cell's tie = vss), so the CDL uses bulk vss for SB. Either change the sheet's SB bulk to vss, or give SB its own tie net in the parent (reasoning: vsso and vss are two nets tied to the same p-substrate).

## Open points / not done
- `d2s_pd_n` not merged into `d2s_ab_n`; pd_n is 0.02 wider than F's maximum.
- Rule numbers outside the PDK files: M2 pin / trunk width 0.29 = Via1 0.19 + 2 x 0.05 (MAX M2.c1 output text; no json key); trunk pitch 0.51 = 0.29 + 0.22 (>= Mn_b 0.21).
- Nothing was checked with extraction of parasitics; no simulation (R of the bus not measured).
