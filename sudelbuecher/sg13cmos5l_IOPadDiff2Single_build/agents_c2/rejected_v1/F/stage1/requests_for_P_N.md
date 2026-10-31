# Requests from F to P and N (stage 1, 2026-10-31 16:58 CET)

Floorplan: `floorplan_stage1.md`, picture `floorplan_stage1.png`. These requests serve **variant 1** (recommended). They
also fit variant 2 unchanged, except that the sinks are then placed rotated (see sinks_6x6).

## Conventions for every cell

- **Orientation.** Draw each cell **as placed**: "upright" means the long side vertical. Edges are named as
  placed: bottom = towards the output frame (y 84), top = towards the core pins (y 180).
- **Outline.** The outline is the bounding box of all shapes, including NWell, ThickGateOx and pSD. I add the
  spacing between cells:
  - NW.b1 1.80 between wells on different nets;
  - NW.d1 / NW.f1 0.62 between a well and N+ or P+ of another cell;
  - iovdd wells are merged.
  The maxima below already leave room for that. Smaller is welcome. If a maximum is not reachable, tell me the
  size you get, and do not change the aspect: I move blocks, I don't squeeze them.
- **Pins.** Metal1.pin 8/2 + text 8/25, Metal2.pin 10/2 + text 10/25, as in the library.
  - Pins lie on the outline edge, inside it. The library's M2 stubs outside the cell (x −1.61) are not wanted.
  - Width ≥ 0.29 (one Via1 with M2.c1 endcaps).
  - Per pin, give the side, the layer and the position measured from the cell's lower-left corner.
- **Layers.** Metal1 / Metal2 only, and nothing on Via2 or above. Metal2 runs over your cells: tell me any part
  of the cell where I may not route Metal2 (matched arrays).
- **Ties and rings.**
  - No rings, and no tie between rows of one array (Christoph's rule 2).
  - Each cell must pass LU.a / LU.b on its own, with tie strips at the outline edges named below. If you would
    rather leave a tie to me, name the segment you need, as A4 did for oa_pmir_c.
  - I draw: the guard rings, the NWell isolator above the frame, the edge stubs, the NWell bridges between
    cells, and every Via2 / supply tap.
- **NWell.** In the iovdd PMOS cells (tails, loads, casc_p, ab_p, pd_p), take the NWell and ThickGateOx to the
  outline on the edges marked "merge"; I bridge the wells into one iovdd NWell.
- **Supply pin names** as in `d2s_mpdda_pd`:
  - `vdd` / `vss` for the front end (iovdd / iovss at the pad top);
  - `vddo` / `vsso` for the output-side pull-downs SA / SB, each with its own tap to the ring (`layout_primitives.md`
    §6).
- **Source buses.** The tails' and the sinks' source buses (with BP / BN) each tap the ring at **one** point.
  Give that bus as one Metal1 net and mark the tap point (a 0.6 × 0.6 Metal1 pad on the outline). I put the Via
  stack there.
- **Devices.** Keep the maps of `layout_primitives.md` §5 and the ratios. Narrow dummies are welcome. Every
  dummy is a device in your CDL. Report every finger / ng change as a netlist change.
- **Not in your cells** (I draw them, or they are elsewhere):
  - RP1 / RN1 (they are in the clamp frames);
  - rhigh, bias_tree_pd, CMA / CMB, rings, stubs.
  - The bias diodes stay where the library has them: BP in the tails, BPC in casc_p, BN in the sinks, BNC in
    casc_n.

## P (PMOS)

| cell | max outline W × H (as placed) | position (variant 1) |
|---|---|---|
| d2s_inputs (tub_p20x1 ×8 + dummies) | **34.0 × 27.0** | x 19.5–53.5, y 125.0–152.0 |
| d2s_tails (8 tails + BP + dummies) | **34.0 × 15.0** | x 19.5–53.5, y 108.2–123.2 |
| d2s_loads (PL / PR 2 × 4 + dummies), upright | **15.2 × 33.0** | x 2.5–17.7, y 123.2–156.2 |
| d2s_casc_p (PCL / PCR 2 × 2 × 15/3 + BPC + dummy), upright | **12.5 × 34.0** | x 2.5–15.0, y 88.6–122.6 |
| d2s_ab_p (RP2, FPL, ABP; no RP1) | **7.8 × 9.5** | x 39.6–47.4, y 88.6–98.1 |
| d2s_pd_p (SA, SABP) | **4.0 × 3.0** | x 47.9–51.9, y 88.6–91.6 |

**d2s_inputs**
- Wire it completely; the library cell has the tubs only.
- Tubs and tails share one column pitch, so each tail sits straight below its tub (§2, §5).
- Well = source for each tub (butted ties); the dummy tubs are on `vdd`. The wells stay ≥ NW.b1 inside the cell.
- Pins:
  - **top edge, M2:** `vinp`, `vref`, `vinn`, left to right, ≥ 2 µm apart;
  - **left edge, M2:** `vfb` (gates of C1b, C2b), in the lowest 3 µm. It arrives from the left over an M3 hop in the
    gap at y 119–126, and is the pad's Kelvin line;
  - **right edge, M2:** `x`, `y` (towards the sinks), within 13 µm of the bottom;
  - **bottom edge, M2:** `sa_A … sb_C2` (8), each at its tub's column;
  - **bottom edge, M1:** `vdd` (dummies).
- Tub shape: free inside the outline. ng = 4 × 5/1 instead of 2 × 10/1 is allowed if it saves height; report it as
  a netlist change.

**d2s_tails**
- NWell: merge on the left, right and bottom edges. The top edge faces the tubs' wells: NW.b1 is mine, so take the
  well to the outline there too.
- Pins:
  - **top edge, M2:** `sa_*` / `sb_*` (8) at the tub columns;
  - **bottom edge, M2:** the same 8 nets again (towards d2s_rhigh through my channel at y 104.7–107.9), either as
    through-columns or as separate pins;
  - **right edge, M2:** `vbp` (gates + BP), low;
  - **bottom edge, M1:** `vdd`, the source bus with BP, with its single tap pad at the bottom-left corner, under the
    M3 iovdd rail.

**d2s_loads** (upright; e.g. two columns of 5, ABBA as §5)
- NWell: merge on all edges except the right edge, which faces the tub wells (NW.b1 mine).
- Pins:
  - **bottom edge, M2:** `pl`, `pr`, `l2`, matching casc_p's top pins;
  - **left edge, M1:** `vdd` (sources + n tie strip).

**d2s_casc_p** (upright)
- NWell: merge on all edges.
- Pins:
  - **top edge, M2:** `pl`, `pr`, `l2`;
  - **bottom edge:** `a` on **M1** (it drops under the b join onto the a join at y 86.4–87.0), and `l2` on M2 near the
    right corner;
  - **right edge, M2:** `vbpc` (gates + BPC), within 3 µm of the bottom;
  - **left edge, M1:** `vdd` (BPC source, n tie strip).

**d2s_ab_p**
- Gates on `vabp`; RP2 is a diode with its source on `dabp`. Bulk is `vdd`, with no source on vdd.
- NWell: merge on the top edge (a bridge up to the tails) and on the right edge (pd_p).
- Pins:
  - **bottom edge:** `a` on **M1**, `b` on M2, and `dabp` on **M1** at the left end (it drops to the existing pin at
    x 38.94–39.55, y 85–86);
  - **top edge, M2:** `vabp`, `l1`, `l2`;
  - **left edge, M1:** `vdd` (n tie).

**d2s_pd_p**
- **Split the sources:** SA's source is `vddo`, SABP's source is `vdd`, as two separate pins. The library cell
  shares one diffusion between them.
- NWell: merge on the left edge.
- Pins:
  - **bottom edge, M1:** `a`, `vddo`;
  - **top edge, M1/M2:** `en_3v3`, `vabp`, `vdd`.
- You may merge pd_p into ab_p as one cell (≤ 12.3 × 9.5) if that is smaller; keep the pins.

## N (NMOS)

| cell | max outline W × H (as placed) | position (variant 1) |
|---|---|---|
| sinks_6x6 (SX / SY 6 + 6 × 6/6, BN, dummies), **upright** | **18.0 × 53.5** (wanted ≤ 17.5 × 52) | x 59.5–77.5, y 123.5–177.0 |
| d2s_casc_n (CX / CY 2 × 2 × 15/3 + BNC), upright | **11.0 × 34.0** | x 66.5–77.5, y 88.6–122.6 |
| d2s_ab_n (RN2, FNL, ABN; no RN1) | **7.5 × 9.5** | x 31.6–39.1, y 88.6–98.1 |
| d2s_pd_n (SB, SABN) | **3.5 × 2.5** | x 52.6–56.1, y 88.6–91.1 |

**sinks_6x6** (upright: the two library rows become two columns; the map `X Y Y X X Y / Y X X Y Y X` with BN and the
dummy at the ends is unchanged)
- Ties: strips on the long edges only, none between the columns. With an 18 µm width, one strip on the right edge
  meets LU.b (20 µm).
- Pins:
  - **bottom edge, M2:** `x`, `y` (to casc_n just below) and `vbn` (gates + BN; the tree is below-left);
  - **left edge, M2:** `x`, `y` again (towards the tubs), within 2–28 µm of the bottom;
  - **right edge, M1:** `vss`, the source bus with BN, with its single tap pad at 4–8 µm above the bottom (that is
    y 127.5–131.5, under the M3 iovss rail at 126–134).
- For variant 2 I place the same cell rotated R90 (left → bottom, bottom → right). You need not do anything for it.
- The cell is shared with s2d. If you would rather keep it native, deliver it native with the pins on the native
  bottom (= my left) and native right (= my bottom) edges; I rotate.

**d2s_casc_n** (upright)
- Pins:
  - **bottom edge, M2:** `b` (straight down onto the b join at y 87.4–88.0), and `l1` near the left corner;
  - **top edge, M2:** `x`, `y`, matching the sinks' bottom pins;
  - **left edge, M2:** `vbnc` (gates + BNC);
  - **right edge, M1:** `vss` (BNC source, p tie strip).

**d2s_ab_n**
- Gates on `vabn`; RN2 is a diode with its source on `dabn`. Bulk is `vss`.
- Its right outline edge faces ab_p's NWell: keep N+ Activ ≥ 0.62 inside that edge, or tell me the margin.
- Pins:
  - **bottom edge:** `a` on **M1**, `b` on M2, and `dabn` on **M1** at the right end (it drops to the existing pin at
    x 38.15–38.45, y 85–86);
  - **top edge, M2:** `vabn`, `l1`, `l2`;
  - **left edge, M1:** `vss` (p tie).

**d2s_pd_n**
- **Split the sources:** SB's source is `vsso`, SABN's source is `vss`.
- Pins:
  - **bottom edge, M1:** `b`, `vsso`;
  - **top edge, M1/M2:** `en_3v3_b`, `vabn`, `vss`.
- You may merge it into ab_n (≤ 11 × 9.5).

## What I need back with each cell

- GDS + CDL.
- Outline, and the NWell / TGO / tie positions on each edge.
- Pin table with coordinates.
- DRC (run_drc incl. LU) and LVS results.
- Netlist changes.
