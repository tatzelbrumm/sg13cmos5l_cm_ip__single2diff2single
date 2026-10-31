# F stage 1: floorplan of the amplifier block, y 84–178 (2026-10-31 16:58 CET)

Picture: `floorplan_stage1.png` (both variants). Script: `../work/floorplan_stage1.py` (rectangles, overlap check,
areas). Requests to P / N: `requests_for_P_N.md`.

- Coordinates are absolute µm in the 80 × 180 pad cell.
- **[m]** = measured from `inputs/repo/.../sg13cmos5l_IOPadDiff2Single.klay.gds` or `pad_buffer_cells.gds` (klayout.db
  0.30.12). **[r]** = my reasoning / estimate.
- Rule values come from `sg13cmos5l_tech_default.json` (key named), and LU from layout rules §7.2.

## 1. What is already there below y 88 [m]

- **P frame** (Clamp_P_M1) up to y 84.44 (pSD). Its outer p+ ring (iovss) is Activ / M1 up to 84.26. The frame's
  NWell top is at 83.08.
- **Metal2 above the frame:**
  - comb straps end at y 84.2;
  - `dabn` at x 38.15–38.45 and `dabp` at x 38.94–39.55, each with a pin at y 85–86;
  - **a join** at y 86.4–87.0 (x 3.2–77.5);
  - **b join** at y 87.4–88.0 (x 0.5–79.5).
  - Metal1 above y 84.26 is free.
- **Left edge channel** x 1.0–3.2: Metal2 is free from y 23.09 to 86.4, except the junction's end (x 3.0–3.2,
  y 39.3–41.3) and CMA's gate landing (x 3.1, y 50.49).
- **M3 / M4 rails:**
  - iovdd 66–91.5 and 93.5–119;
  - iovss 126–134;
  - vss 140–158;
  - vdd 160–178.
  - M3 gaps: 119–126 and 134–140 (also 91.5–93.5 and 158–160, which the brief does not use).
- **IOPadAnalog's core-side pins** are on M2 at the top edge, pin box y 179–180 (pad x 26.1–50.9, padres
  x 57.46–57.75). I use the same pin convention.
- **Library cells** (bbox, current GDS), in µm:

  | cell | bbox |
  |---|---|
  | d2s_inputs | 34.8 × 28.8 |
  | d2s_tails | 35.3 × 21.8 |
  | d2s_loads | 58.3 × 9.1 |
  | d2s_casc_p | 36.6 × 13.6 |
  | d2s_ab_p | 10.0 × 9.7 |
  | sinks_6x6 | 53.4 × 18.1 |
  | d2s_casc_n | 36.1 × 11.9 |
  | d2s_ab_n | 11.3 × 7.0 |
  | d2s_rhigh | 14.8 × 17.5 |
  | bias_tree_n | 27.4 × 11.1 |
  | bias_tree_p | 18.8 × 11.6 |

  `cell_tree.md` has older sizes.

## 2. Why columns, not the bands of `layout_primitives.md` §4 [r]

- **Bands fail on width.** The a / b joins are at the bottom, so casc_p (a), casc_n (b) and the class-AB group want
  the bottom row. In their native rows that is 34 + 16 + 34 = 84 µm, more than the 75 available.
- **The sinks** (≈ 50 µm wide in any 2-row map) need a row of their own. So do the tubs and tails (34 µm, column
  aligned).
- **Turning the cascodes and loads upright** gives two narrow outer columns, P on the left and N on the right, which
  reach the joins directly. The matched input stage (tubs over tails over rhigh) then goes in a 34 µm centre column.

## 3. Variant 1 (recommended)

Three columns: PMOS left, NMOS right, the input stage in the centre. Block bottom y 88.6: the b join at 88.0 plus
margin for the blocks' M2 (Mn_b 0.21).

| block | x | y | notes |
|---|---|---|---|
| NWell isolator (mine) | 2.6–77.4 | 84.50–85.28 | n+ 84.74–85.04 in NWell, iovdd; Via1 / Via2 into M3 iovdd through M2 pads at y 84.45–86.15 between the comb stubs |
| casc_p, upright | 2.5–15.0 | 88.6–122.6 | a on M1 down under the b join to the a join |
| loads, upright | 2.5–17.7 | 123.2–156.2 | pl / pr / l2 to casc_p directly below |
| d2s_rhigh (mine) | 15.8–30.6 | 90.0–104.5 | 4 × 150 kΩ chains; the sa / sb channel (M1) is at y 104.7–107.9, x 15.8–53.5 |
| ab_n | 31.6–39.1 | 88.6–98.1 | dabn on M1 down to its pin (x 38.3) |
| ab_p | 39.6–47.4 | 88.6–98.1 | dabp on M1 down to its pin (x 39.2) |
| pd_p / pd_n | 47.9–51.9 / 52.6–56.1 | 88.6–91.6 | SA: own Via2 tap into M3 iovdd 66–91.5. SB: own tap onto the frame's p+ ring (iovss) |
| bias_tree_pd (mine), L-shape | 47.9–66.0 and 54.1–66.0 | 92.2–107.6 and 107.6–123.0 | ≈ 470 µm² for ≈ 400 of devices. Fallback: the top spare band |
| tails (BP) | 19.5–53.5 | 108.2–123.2 | one Via2 tap into M3 iovdd 93.5–119 at the bottom-left corner |
| d2s_inputs (tubs) | 19.5–53.5 | 125.0–152.0 | NW.b1 1.8 to the tails (below) and to the loads (left) |
| casc_n, upright | 66.5–77.5 | 88.6–122.6 | b on M2 straight down onto the b join |
| sinks_6x6, upright | 59.5–77.5 | 123.5–177.0 | one Via2 tap into M3 iovss 126–134 on its right edge |
| spare / CMB reserve | 2.5–59.0 | 157.0–177.5 | ≈ 1160 µm². Also 2.5–17.7 × 156.8–… |

- **Channels:**
  - left x 17.7–19.5 (vfb, the NWell bridge from casc_p to the tails);
  - right x 53.5–59.5, y 123–177 (x / y crossing in M1; iref / en_3v3 / en_3v3_b down to the tree and the pd cells
    in M2);
  - bottom y 88.6–90.0 under rhigh, and then y 98.6–104.5 above the ab group (l2, vbpc, l1, vabp, vabn).
- **Areas** (planned outlines): PMOS 1523, tubs 918, NMOS 1417, rhigh 215, tree 462. Total 4534 of 6668 µm²
  (x 2.5–77.5, y 88.6–177.5); spare 1158 µm².
- **One iovdd NWell** (rule 2), as one polygon:
  - casc_p + loads;
  - a bridge at x 15–19.5 to the tails;
  - a bridge at x 40–46, y 98–108 from the tails to ab_p, then pd_p and the tree's PMOS.
  - The tubs keep their own 12 wells.

## 4. Variant 2 (alternative)

- **The same:** the left column, the centre (rhigh, ab group, tails, tubs) and casc_n.
- **Sinks** in their native rows across the top: x 2.5–56.0, y 159.0–177.0. This is the coolest spot, and the cell
  stays as delivered.
- **bias_tree_pd** in the right column, x 59.5–77.5, y 123.5–150.0, close to iref / en.
- **Spare:** the bottom-right L (x 47.9–66, y 92–108) and the top-right (y 151–177.5); 756 µm².
- **Cost:**
  - x / y run about 40 µm from the sinks' right end down the right channel to casc_n;
  - the sinks' iovss tap needs an M2 line about 25 µm down to the M3 rail;
  - x, y and the core-input lines share the right channel.
- That is why variant 1 is recommended. The requests are the same for both: variant 2 places the upright sinks
  rotated R90.

## 5. Routing plan

- **Layers.** M2 runs vertical (cell pins, long lines), M1 horizontal (channels, hops). M3 is used only for one
  vfb hop in the gap at y 119.8–120.6.
- **a / b:**
  - b drops in M2 straight onto the b join (87.4–88.0);
  - a drops in M1 under the b join, then Via1 onto the a join (86.4–87.0).
  - Open point 3 of 2026-10-28 is solved this way, with M1 hops and the joins left in place.
- **dabp / dabn:** M1 from ab_p / ab_n down to y 85.55, then Via1 onto the existing pins at y 85–86. This clears the
  isolator's M1 (top 85.02) by ≥ 0.18 (M1_b). No change to `replica_lines`.
- **vfb, the Kelvin line:**
  - it starts at the junction's left end, the low-current end [r], with an M2 jog at y 39.8–40.4 from x 1.95 to the
    junction at x 3.0;
  - M2 at x 1.95–2.35 runs up the left edge channel, with an M1 hop under the b join;
  - M3 at y 119.8–120.6 eastwards over casc_p;
  - Via2 down at x ≈ 18.6, then M2 up the left channel into the tubs' left edge at y ≈ 126.5.
  - About 105 µm, carrying gate current only.
  - Antenna (§7.1): the pad net carries the DCN / DCP diodes, so the vfb gates are protected [r]; I check it in
    stage 3.
- **`guard` tie** (open point): M2 at x 1.25–1.65 from the DCN guard / band Metal1 (y 26–38, x 1.0–3.2) up to Via2
  into M3 iovdd at y 66–67, left of vfb. That is 0.25 from the b line and 0.30 from vfb, so nothing sits at the
  limit.
- **Supply taps:**
  - tails: one Via2 into iovdd;
  - sinks: one Via2 into iovss;
  - loads, casc_p and the well ties: their own taps;
  - SA (vddo) and SB (vsso): their own taps.
  - The bias tree's iovdd / iovss come by M2 from the rails at y ≤ 119 and 126–134.

## 6. Guard rings and edge stubs (mine, stage 2)

- **Above the P frame**, a double ring towards the circuitry (layout rules §7.2.1 item 5): the frame's outer p+
  ring (iovss, existing) plus the new NWell isolator, at the y given in §3.
  - NW.f 0.24 to the p+ ring (outside TGO), NW.e 0.24 around n+, NW_a 0.62.
  - It stops short of the edges, because no NWell is allowed at the edge in 84–147.73.
- **Edge stubs at both edges** (phase 1 §1.2 intervals):

  | stub | x | y | tie |
  |---|---|---|---|
  | p+ iovss | 0–0.9 / 79.1–80 | 84.51–139.92 (M1 84.26–140.17, pSD to 140.35, Substrate as IHP) | M1 into the frame's ring, plus Via2 into M3 iovss at y 126–134 |
  | n+ / NWell iovdd | — | 148.35–148.65 (NWell 147.73–149.27) | M2 at x 0.3–0.7 / 79.3–79.7 down to Via2 into iovdd below y 119 |
  | p+ vss | 0.25–1.6 (Activ set back as IHP) | 156.85–157.15 (M1 to the edge) | Via stack into M3 vss |
  | n+ / NWell vdd | — | 166.85–167.15 (NWell 166.23–167.77) | Via stack into M3 vdd |

  Checked in stage 3 with `row_check.py`.
- **Latch-up:** P / N cells tie themselves at their edges, with no ties between rows. The tubs have butted ties.
  rhigh gets a p+ tie ring or strips (stage 2).

## 7. Core-side pins (M2, pin box y 179.0–180.0, 0.4 wide) [r]

| variant | vinp | vref | vinn | iref | en_3v3 | en_3v3_b |
|---|---|---|---|---|---|---|
| variant 1 | 25.0 | 31.0 | 37.0 | 54.5 | 56.5 | 58.5 |
| variant 2 | 25.0 | 31.0 | 37.0 | 62.0 | 64.0 | 66.0 |

- vinp, vref and vinn go straight down to the tubs' top edge. The other three go down the right channel.
- The lead / slot may prefer other x positions; any x in 19.5–59 costs only a jog. The 63/0 GateDecode box at
  x 36.4–45.8 is TEXT only and no obstacle.

## 8. Points for the lead [r]

1. **bias_tree_pd's sheet** contains Xd = `bias_diodes` (BP, BN, BNC, BPC). In the layout these four sit in the
   tails, sinks, casc_n and casc_p (library, decision 4).
   - My `bias_tree_pd` cell will hold the tree without them.
   - LVS of the pad is then flat.
   - The standalone tree LVS runs against "sheet minus Xd", written as a sheet proposal (rule 4).
2. **CMA / CMB overflow** goes to the spare band (variant 1: y 157–177.5).
   - Prefer moving **CMB** units (well = b, gate = pad) up here. Only the gate is on the pad, so it is not a
     latch-up injector.
   - **CMA** (well = pad) should stay in the ESD zone, inside a guard ring.
   - CMB's gate then needs its own pad line from the comb top (y 81.45) up, with an M1 hop under the joins. That line
     must not share the vfb Kelvin line.
3. **The P / N outlines are budgets**, not measurements. Variant 1 has about 21 µm of vertical slack at the top, so a
   cell that comes out larger moves the blocks up, without a change of plan.
