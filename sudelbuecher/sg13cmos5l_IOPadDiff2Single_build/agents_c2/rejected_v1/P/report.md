# Agent P report: compact PMOS cells of d2s_mpdda_pd, 2026-10-31 (17:01-17:55 CET)

[m] = measured by a tool in this session, [r] = my reasoning. Rule values: `sg13cmos5l_tech_default.json` keys named in `build_d2s_p.py`
comments (Act_d, Cnt_e, M1_b, M2_b, NW_b1 ... ); no value invented. Nothing outside `/home/user/c2/P/`, no git, no web.

## Result [m]
IHP `run_drc.py` (main + maximal deck, `--no_density`, includes LU.a / LU.b / LU.c / LU.d) and `run_lvs.py --disable_tap_extraction`,
one run per cell on `d2s_p_cells.gds`, last run after the last edit: **6 of 6 cells 0 violations, 6 of 6 LVS match**
(logs: `logs/`, "generated an exception" count 0 in every DRC log). No `--implicit_nets` needed. First-run failures fixed: Act_d (tie
Activ too small), M1_c1 / Cnt.h (contact without Metal1), M2_d (stub area), Pin.f_M2 (pin box outside Metal2), M1_b / M2_b (via pad
vs track), LU.a on the tails (right half > 20 um from the left tie -> second tie strip). Not done: XOR / flat extraction (lead), PEX.

## Cells: size before -> after (um, as placed) and F's maximum
| cell | library | after | F max | devices |
|---|---|---|---|---|
| d2s_inputs_c | 34.80 x 28.80 | **32.05 x 26.71** | 34.0 x 27.0 | 8 tubs (2 x 10/1 ng=2) + 4 dummy tubs 10/1 ng=1 |
| d2s_tails_c | 35.29 x 21.76 | **32.27 x 14.81** | 34.0 x 15.0 | 8 tails 5/6 + BP 5/6 + 2 dummies 0.3/6 + 1 dummy 5/6 |
| d2s_loads_c (upright) | 58.29 x 9.10 | **11.32 x 30.02** | 15.2 x 33.0 | 8 x 6/4 (PL/PR) + 2 dummies 2/4 |
| d2s_casc_p_c (upright) | 36.64 x 13.58 | **11.32 x 33.64** | 12.5 x 34.0 | 4 x 15/3 + BPC 1/4 + dummy 1/4 |
| d2s_ab_p_c | 10.04 x 9.66 | **6.01 x 7.90** | 7.8 x 9.5 | RP2, FPL, ABP 6.66/0.6 (no RP1) |
| d2s_pd_p_c | 3.20 x 2.24 | **3.71 x 2.97** | 4.0 x 3.0 | SA, SABP 1/0.45, sources split |
All inside F's maxima. Cells are standalone-checkable; origin = lower-left of the bounding box of all shapes (NWell, TGO, pSD included).

## Device-to-finger map and wiring
- **inputs**: rows as `layout_primitives.md` s5 (top `Aa C2b C1b Ba`, bottom `Bb C1a C2a Ab`), all tubs R0, same orientation. Tub =
  library PCell + N+ tie strip 0.30 high under the device (butted ties: strip joined to both source columns by Metal1), well =
  source, wells 1.8 apart (NW_b1). Height saved: tie 0.78 -> 0.30 high (pSD_d1 0.03 to the pSD edge), total 25.9 -> 26.7 incl.
  the top tracks. Dummy tubs: ng=1 10/1 (2.92 wide instead of 4.30), gate = D = S = well = vdd, one at each row end.
  Column pitch 6.1 (tub well 4.30 + NW_b1 1.80); real tub k Activ starts at x = 5.34 + 6.1 k (cell frame).
  Metal2 lanes: bottom-row source at tub x+0.15, top-row source at x+2.91 (runs over the lower tub), both straight to the bottom edge;
  drain lanes at x+1.53 end on four Metal1 tracks in the row gap (x: T2+T3, y: T1+T4, ordered so the lanes of one column never
  overlap), x joined by a Metal1 bridge, y by its own Metal2 pin line; both go to the right edge. Gates: Metal1 pads on the library strap.
- **tails**: row 1 top (S up) `d Aa C2b C1b Ba D5`, row 2 bottom (S down, the point image) `d Bb C1a C2a Ab BP`; d = 0.3/6 dummy,
  D5 = full 5/6 dummy; real tails on the tub pitch, centre line = tub centre. One poly gate strip per row (vbp, contacts at the right
  end, outside pSD), pSD filled between the fingers (the 0.30 gaps would break pSD_b). Source bars top and bottom (vdd), joined on the
  left. Drain lanes: through-columns, top-row net at centre +1.38, bottom-row net at centre -1.38, full height: same x as in inputs
  after shifting tails by +2.47 (tails origin is 2.47 left of the inputs origin; tail column k centre = inputs x + 1.53 - 2.47).
- **loads**: two columns of 5, col 1 `d L R R L`, col 2 `L R R L d` (reads L R R L L R R L, R180-symmetric), one poly strip per column,
  S column (vdd) left, D column right; pl / pr Metal2 lanes joined by two Metal1 bars below the columns, gate contacts below.
- **casc_p**: two columns (`a|pr`, `pl|l2`), each two stacked 15/3 fingers = one 30.25 tall Metal1 line per column (PCR left, PCL right;
  the old 2 x 2 interleave is dropped: cascodes need no centroid, `layout_primitives.md` P6). BPC + dummy 1/4 in a row on top.
- **ab_p**: `RP2 | FPL | ABP` in one row, poly bridge on top for the common gate (vabp), contact above RP2 tied to its drain.
- **pd_p**: SA and SABP side by side with their own source columns (vddo / vdd), one poly bridge, contact above SA.

## Taps, wells, latch-up
No tie between rows of an array; ties only at the periphery. One NWell + ThickGateOx rectangle per cell (inputs: one per tub and dummy).
- inputs: tie under every tub (butted to the source), dummies on vdd. loads / casc_p: full-height strip on the left edge (vdd pin).
  ab_p: left strip. tails: left strip + right strip (the cell is 32 wide: with the left strip only, LU.a failed on 5 Activ areas, [m]).
  pd_p: 0.45 x 0.30 N+ at the top edge on the vdd column (needed: no edge named, but LU.a needs one).
- Result [m]: LU.a, LU.b, LU.c, LU.d 0 violations in all six runs. I did not measure the largest tie-to-Activ distance.
- NWell reaches the outline on every edge of every cell (loads/casc_p/ab_p/pd_p/tails); edge exceptions F named
  (loads right, ab_p/pd_p) are F's to space: I cannot cut my own bounding box. Inputs wells: dummy wells 1.8 from the tub wells.

## Netlist changes (for the backannotation)
1. **pd_p: SA bulk is vdd** in my CDL (one well, tie on vdd); the circuit has vddo. At pad level vdd / vddo are the same iovdd well.
2. **tails**: new devices, all with D = S = vdd, G = vbp: 2 x 0.3/6 (narrow) + 1 x 5/6 dummy (library had 3 full dummies). Electrical effect none.
   BP is in row 2 at the right end (library: row 1). Mismatch note [r]: Aa has a narrow dummy on its left, Ab has BP (5 wide) on its
   right, so the two tails of unit A see different row-end environments (unit B mirrored): cannot be made symmetric inside 34 um.
3. **inputs**: dummy tubs 10/1 ng=1 (were 20/1 ng=2); real tubs unchanged (w=20u l=1u ng=2 as in units.spice). No ng change.
4. **loads / casc_p / ab_p**: no device change (ratios, dummies as library; casc_p dummy gate stays vbpc). RP1 not drawn.
5. casc_p: PCL / PCR are 2 x 15/3 stacked in one column each, extracted as W = 30, L = 3 (same as XPCL / XPCR w=30u).

## Pins (side, layer, x, y from the lower-left corner; full list `pins.txt`)
- inputs: top M2 vinp x 7.24-7.44, vref 24.39-24.59, vinn 29.6-30.4 (y 26.51-26.71); left M2 vfb x 0-0.3, y 0.55-0.80;
  right M2 x (31.85-32.05, y 12.48-13.2), y (31.65-32.05, y 13.48-13.68: 0.5 above F's 13 um, [m]); bottom M2 sa_A 8.15, sb_C2 14.25, sb_C1 20.35,
  sa_B 26.45 (top row), sb_B 5.39, sa_C1 11.49, sa_C2 17.59, sb_A 23.69 (centres, y 0-0.4); bottom M1 vdd x 0.69-0.98.
- tails: top and bottom M2 (y 14.41-14.81 and 0-0.4) sa_A 5.78, sb_C2 11.88, sb_C1 17.98, sa_B 24.08, sb_B 3.02, sa_C1 9.12, sa_C2 15.22,
  sb_A 21.32 (centres); right M2 vbp x 31.47-32.27, y 1.3-1.5; bottom-left corner M1 tap pad vdd x 0-0.6, y 0-0.6 (pad is 0.85 wide
  so it merges with the vdd column, notch rule).
- loads: bottom M2 l2 4.0, pl 7.3, pr 8.3 (y 0-0.4); left M1 vdd x 0-0.29, y 15.27-15.56. Not at casc_p's x (pr 4.66, pl 5.17, l2 8.55): shift loads by about -1.
- casc_p: top M2 pr 4.66, pl 5.17, l2 8.55 (y 33.24-33.64); bottom M1 a x 1.135-1.425; bottom M2 l2 8.55; right M2 vbpc x 11.115-11.315, y 1.12-1.52;
  left M1 vdd y 15.49-15.78.
- ab_p: bottom M1 dabp 1.135-1.425 and a 4.115-4.405, bottom M2 b 5.14-5.34; top M2 vabp 2.16-2.36, l2 2.67-2.87, l1 3.65-3.85; left M1 vdd y 3.49-3.78.
- pd_p: bottom M1 a 0.625-0.915, vddo 1.455-1.745; top M1 en_3v3 1.04-1.33, vdd 1.965-2.255, vabp 2.795-3.085.
Source bus tap point (tails): the pad above. The inputs `vdd` bottom bar (Metal1 along the bottom edge, between the two dummy columns) has one pin box.

## Where Metal2 may not run [r]
Over the whole d2s_inputs and d2s_tails area no foreign Metal2 (my lanes are dense and the tubs are matched); in loads, casc_p, ab_p, pd_p
no foreign Metal2 over the Activ columns. Free: nothing inside the cells; the top 1.0 um of inputs above the pins is outside the lanes.

## Not covered / honest limits
- Not drawn as asked: the 3 M3 hops, guard rings, bridges (F). inputs `vdd` pin is Metal1 at the bottom edge as asked.
- Mirror-ratio / centroid maps unchanged except casc_p's interleave (reasoned above) and the tails' row-end environment (netlist change 2).
- Deck: `/foss/pdks/ihp-sg13cmos5l` (KLayout 0.30.12), the full deck ran (the A4 limitation of 2026-10-28 does not apply here).
