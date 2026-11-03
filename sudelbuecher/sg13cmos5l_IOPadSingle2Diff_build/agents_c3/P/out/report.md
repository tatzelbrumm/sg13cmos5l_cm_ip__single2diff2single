<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
<!-- Saved by the lead from agent P's final reply (the harness refused P's own write of this file). Text as P sent it. -->
# P (C3): PMOS primitives of s2d_mpdda_pd / bias_tree_noab_pd (2026-11-03, 20:47–21:10 CET)

Claude (Opus 5.5), agent P.
- `build_s2d_p3.py` (run in `out/`, needs the PDK) writes the gds, cdl and PNGs. Two runs give byte-identical files
  (gds b456862ae015, the file that was checked in round 2).
- It is built on C2's `build_d2s_p2.py`: the same helpers, rows and gate columns.
- [M] = measured by a tool run, [R] = reasoning. Logs are in `logs/`; `check_summary.txt` covers both rounds.

## Checks [M] (round 2 = final, all 7 cells)

| cell | size µm | area / library (µm²) | DRC | LVS | sym_check | LU µm |
|---|---|---|---|---|---|---|
| tub_p20x1_c3 | 4.30×11.97 | 51.5 / 55.9 = 0.92 | 0 | match | X 0 (--no-y), 0 necks | 10.45 |
| s2d_inputs_c3 | 47.58×26.44 | 1258 / 1354 = 0.93 | 0 | match (deep) | X 0, Y 0, 0 necks | 10.45 |
| s2d_tails_c3 | 45.19×15.83 | 715 / 1088 = 0.66 | 0 | match | X 0, Y 0, 0 necks | 6.89 |
| s2d_loads_c3 | 43.19×12.32 | 532 / 722 = 0.74 | 0 | match | X 0, Y 0, 0 necks | 4.90 |
| s2d_casc_p_c3 | 52.23×12.81 | 669 / 726 = 0.92 | 0 | match | Cont X 0.2688 µm², Y 0, 0 necks | 5.14 |
| s2d_pd_p_c3 | 3.20×2.97 | 9.5 / 7.2 = 1.33 | 0 | match | X 0 (--no-y), 0 necks | 1.45 |
| bias_tree_noab_p_c3 | 12.94×10.37 | 134 / 228 = 0.59 | 0 | match | Cont X 0.0384 µm² (--no-y), 0 necks | 3.55 |

- **DRC:** `run_drc.py --no_density --mp=4`. Every log says "No DRC violations detected", with no line containing
  "exception" or "Violated rules".
- **LVS:** `run_lvs.py --disable_tap_extraction`. The inputs need `--run_mode=deep`, because the tub keeps its own
  labels (as in C2).
- **Library areas:** bounding boxes in `pad_buffer_cells.gds` of s2d_inputs, s2d_tails, s2d_loads, s2d_casc_p,
  s2d_pd_p and tub_p20x1. bias_tree_noab_p is compared with bias_tree_p (which still has PABN) plus bias_tree_swp.
  pd_p is larger because the library cell has no tie.
- **LU:** with C2's `lu.py`, the farthest P+ Activ in the NWell from an N+ tie. LU.a = 20 µm
  (`sg13cmos5l_tech_default.json` LU_a).
- **Round 1 failures (all cells):**
  - tails DRC M2.c1 ×36: the drain M2 pads sat on the wrong side of their vias, which also left the drain nets
    unnamed in LVS;
  - tails DRC M1.b ×2: the BP lane was 0.03 µm under the ring strip;
  - sym_check on loads and casc_p, 2 narrow-poly hits each: a 0.18 µm tongue of the poly bridge in the 0.20 µm gap
    between the two rows' end-cap zones.
- **Fixes:**
  - the drain pads start at the via's far edge;
  - the lane sits 0.24 µm under the ring;
  - the bridge runs 0.25–0.60 µm from the Activ and is 0.35 µm wide.

  Round 2 (all cells) is clean.
- **Residuals [M]:** on Cont only, inside the single center device of a row with an odd device count.
  - casc_p: LNC in both rows, box 19.42–33.60 × 2.445–10.365.
  - bias_tree: PBN, box 4.40–8.54 × 2.63–9.17.
  - The cause is the PCell's contact row, spaced with 5 nm flooring. For w = 15 the contacts sit at 0.07, 0.41, 0.75,
    1.095 …, and their mirror images at 0.07, 0.415, 0.755, 1.10 …, so a single PCell is not its own mirror image.
  - Every device pair is placed as exact M90 images, so everything else comes out 0. An unmodified PCell cannot
    remove this residual.

## Common rules applied [R]

- **Rows:** rotated PCells, Activ 0.25 µm apart, so that the end caps merge and the gate strip is one piece by
  abutment.
  - The right half of each row is the M90 image of the left half, and the upper row is the M0 image of the lower row
    (C2's `rows` / `mirror_row`).
  - Unmodified pmosHV PCells, copied flat.
- **Gate contacts:**
  - tabs as long as the gate at both row ends, 0.60 µm beyond the Activ, with one contact column 0.30–0.46 µm from
    it and an M1 column of 0.26 µm;
  - new: in two-row cells, a poly bridge (0.25–0.60 µm from the end Activ) joins the two rows' tabs at both ends.
    The gates are then one poly net, and no M2 is needed to join the gate columns;
  - upright devices (tub, pd_p, TGP): contacts on the full-width gate heads (Cnt_e 0.14, M1_b 0.18 to the stripe
    ends). In the tub and pd_p the two heads are also joined in poly over the middle stripe end (Gat_d 0.07);
  - no center contacts.
- **Dummies:** source and drain to vdd (ring or tie), gate by abutment (vbp / vcmfb / vbpc). Dummy tubs are all-vdd,
  each in its own well.
- **Taps:**
  - closed N+ rings in tails, loads, casc_p and bias_tree, 0.80 µm from the end Activ and 0.21 µm from the S/D edges;
  - no taps between rows;
  - one NWell and one TGO rectangle per cell (each tub has its own), no notches.
- **M2 only where needed:**
  - ring crossings: tails and bias_tree drains, and the edge stubs of the gate nets vbp / vcmfb / vbpc;
  - column / row joins: the loads and casc_p tracks;
  - the tub's source strap and the inputs' tracks.

  pd_p has no M2.

## Cells

### tub_p20x1_c3

2 × 10/1, w = 20, ng = 2, bulk = source; the origin is the Activ corner.
- **N+ tie:** under the device, 0.43 µm below the Activ (pSD_i1 0.40 + pSD_d1 0.03), instead of left and right of it
  as in C2. It is contacted only under the two source plates, and the drain tab crosses it in M1 without a contact.
- **Width:** 4.30 µm instead of 5.32 (NW_c1 / NW_e1 0.62 on both sides).
- **Sources:** the two source plates are joined by an M2 strap.
- **Pins:** g M1 (1.75,10.18;2.69,10.40); s M1 (0.07,−1.35;0.74,−1.05); d M1 (0.975,−0.62;2.085,−0.32).

### s2d_inputs_c3

Tub pitch 6.10 (4.30 + NW_b1 1.80); the rows are 3.04 µm apart (NW_b1).

```
upper  D | A1a F2b F1b A2a | M1a M2b | D     A1/A2/F1/F2 = the brief's A/B/C1/C2 map; CMFB cross-quad at the right
lower  D | A2b F1a F2a A1b | M1b M2a | D     (as in the library); D = dummy tub, g = d = s = vdd
```

- **Band between the rows:** 6 M2 tracks at 0.48 µm pitch: vref vfbn vcm vdd vfbp vin. Their vias sit between the two
  rows' gate pads. The lower row's tabs are on the right gate head, the upper row's on the left.
- **Drain tracks:** outside each row. x / y run left of the quad and xc / yc right of it, so each pair shares a track
  slot (2 slots per side). x and y are joined by M1 lines at the left edge, xc and yc at the right edge.
- **Sources:** plates out to the outer edges.
- **Pins:**
  - bottom, M1 0.67×0.30 at x0 = 7.08 / 13.18 / 19.28 / 25.38 / 31.48 / 37.58: sb_A2, sa_F1, sa_F2, sb_A1, sb_M1,
    sa_M2;
  - top (y 26.14), same x: sa_A1, sb_F2, sb_F1, sa_A2, sa_M1, sb_M2;
  - left, M2 (x 0–0.5, 0.26 high), y0: vref 11.87, vfbn 12.35, vcm 12.83, vdd 13.31, vfbp 13.79, vin 14.27; x 0.14,
    y 0.62;
  - right, M2 (x 47.08–47.58): xc 0.14, yc 0.62.

### s2d_tails_c3

All devices 5/6, in one NWell on vdd.

```
upper  BP | A1a F2b F1b A2a M1a M2b | D     same column order as the tubs; BP at one end, its full 5/6 twin
lower  D  | A2b F1a F2a A1b M1b M2a | D     (a dummy) at the other end, dummies at both ends of the lower row
```

- **Sources:** both rows face each other under one vdd plate (Act_b 0.21), which runs out to the ring sides between
  the gate columns.
- **Drains:** an M1 pad with 3 Via1 (M1_e 0.22 from the ring), then M2 straight out over the ring to the cell edge.
  The dummies' drains go into the ring strip; BP's drain lane goes into its gate column.
- **Ring:** a closed ring is needed here. Side ties alone would leave P+ up to 21.7 µm from a tie (LU.a 20).
- **Pins:**
  - M2 1.11×0.30 at x0 = 8.915 / 14.165 / 19.415 / 24.665 / 29.915 / 35.165; bottom (y 0): sb_A2, sa_F1, sa_F2,
    sb_A1, sb_M1, sa_M2; top (y 15.53): sa_A1, sb_F2, sb_F1, sa_A2, sa_M1, sb_M2;
  - vbp M2 (0,4.32;0.5,4.62); vdd M1 on the ring (0.62,1.63;0.92,3.63).

### s2d_loads_c3

All 6/4; X = 1/4 dummy.

```
upper  X | LP LN DD DD LN LP | X    the library map P N D D N P P N D D N P folded in two; both rows are the same,
lower  X | LP LN DD DD LN LP | X    so each column holds two fingers of one device (LP, LN, DD centroids at the center)
```

- **Drains:** they face the band (0.70 µm, for pSD_b 0.31). One M1 plate per column joins both rows' drains, and DD's
  two adjacent columns share one plate. M2 tracks lp, dd, ln (0.20 µm wide, 0.41 pitch) join the columns, with pins
  at the left edge.
- **Dummies:** their drain plates run out over the poly bridge to the ring sides.
- **Sources** go into the ring strips; vcmfb leaves through an M2 edge stub from the gate column.
- **Pins:** M2 at x 0–0.5: lp y 5.65–5.85, dd 6.06–6.26, ln 6.47–6.67, vcmfb 3.32–3.62; vdd M1
  (20.595,0.62;22.595,0.92).

### s2d_casc_p_c3

15/3; BPC and X are 1/4.

```
upper  BPC | LPC LNC DC | X     both fingers of each cascode in one column (cascodes need no centroid);
lower  X   | LPC LNC DC | X     BPC at one end, its 1/4 twin at the other, 1/4 dummies at the lower row's ends
```

- **Drains:** they face the band, one plate per column, with M2 tracks voutp, vcmfb, voutn to the left edge.
- **Sources:** M1 tabs with 3 Via1 down to M2 tracks lp, ln, dd inside the ring. Outside the left ring side, three M1
  lines of equal length join them.
- **Row ends:**
  - BPC's drain goes into its gate column;
  - the lower-left dummy's drain runs under BPC's lane (M1_e 0.22) to the ring;
  - the two right-end dummies share one plate.
- **Pins:** M2 at x 0–0.5, y0: dd 1.185, ln 1.595, lp 2.005, vbpc 3.905 (0.30 high), voutp 5.895, vcmfb 6.305,
  voutn 6.715 (0.20 high); vdd M1 (25.51,0.62;27.51,0.92).

### s2d_pd_p_c3

- **Device:** one pmosHV w = 2, ng = 2, i.e. `voutp | TPP | vcm | TNP | voutn`, sharing the vcm stripe (the pair is not
  broken up), mirror-symmetric.
- **Gate:** joined in poly, with 3 contacts on the heads and the bridge; en_3v3 goes in M1 to the top edge.
- **Tie:** an N+ tie below (vdd). vcm runs in M1 straight down across it, and the tie is contacted only left and
  right. No M2.
- **Pins (M1):** en_3v3 (1.47,2.67;1.73,2.97); vcm (1.52,0;1.68,0.30); voutp (0,1.70;0.30,2.00); voutn
  (2.90,1.70;3.20,2.00); vdd (0.62,0.62;1.29,0.92).

### bias_tree_noab_p_c3

- **Row:** `PBNC PBN D` (2/6, 5/6, 2/6 twin). The drains go up over the ring as M2 pads, the sources into the lower ring
  strip, and the dummy's drain into the upper ring strip.
- **TGP** (1/0.45): centered under the ring, in the same NWell, with its gate head down. The ring strip is its tie.
- **Pins:**
  - vbnc M2 (2.165,10.07;3.275,10.37); vbn M2 (5.915,10.07;7.025,10.37); vbp M2 (0,5.75;0.5,6.05);
  - vdd M1 (0.62,3.06;0.92,5.06);
  - bottom M1: iref x 5.875–6.135, en_3v3_b x 6.34–6.60, ni x 6.805–7.065.

## Netlist changes (`s2d_p3_cells.cdl`) [R]

- **Split fingers:** LP / LN / D w = 24 ng = 4 become 4 × 6/4 ng = 1 each; LPC / LNC / DC w = 30 ng = 2 become
  2 × 15/3 ng = 1 each. W, L and finger counts are unchanged.
- **Dummies** (d g s b):
  - inputs: 4 tubs, all vdd;
  - tails: 3 × 5/6, vdd vbp vdd vdd;
  - loads: 4 × 1/4, vdd vcmfb vdd vdd;
  - casc_p: 3 × 1/4, vdd vbpc vdd vdd;
  - bias_tree: 1 × 2/6, vdd vbp vdd vdd.
- **Bias diodes:** BP (tails) and BPC (casc_p) move in from bias_diodes.
- **Instances:** the input devices are X instances of `tub_p20x1_c3`. TPP / TNP are one ng = 2 PCell, listed as two
  1/0.45 devices (LVS extracts them that way).

## Decisions where the brief left room [R]

- **CMFB quad:** at the right of the signal block (library order), not in the middle. x / y and xc / yc then share
  track slots, which saves 4 tracks (≈ 1.9 µm of height). Each group is still common-centroid on its own.
- **casc_p:** three cascodes per row force a center device (the residual above) and put the BPC twin at the far end.
- **TGP** stays in this cell as briefed. Christoph found it out of place in C2, so F may move it; it needs only a vdd
  bulk.
- **pd_p tie:** pd_p keeps its own tie so that it passes DRC (LU.a) on its own. In the pad it can share casc_p's well
  and ring, since voutp / voutn are casc_p drains, which follows "share the well and its tap".
