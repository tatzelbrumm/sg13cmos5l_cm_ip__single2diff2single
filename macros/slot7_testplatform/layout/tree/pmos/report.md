<!--
Saved verbatim by the main session on 2026-11-07 at the user's request: the PMOS specialist agent could not write .md
files in this session and returned this report in its hand-back. Text unchanged.
-->
# report.md: tree_pmos, the PMOS devices of bias_tree_noab_pd, compact and matched

2026-11-07, Claude (Opus 5.5), PMOS specialist for slot 7's tree (the role A4 had for oa_pmir_c / bg_pmir_pcas_c). [m] = measured on the GDS or by a tool, [r] = reasoning.

## Result [m]

| cell | size | gate area W·L, share of cell |
|---|---|---|
| **tree_pmos**: BP, PBN, PBNC, MDBP, BPC, TGP | 20.985 x 8.430 = **176.9 um²** | 88.45 um² = 50 % |
| naive `tree_row_p` (same devices; its wiring is in the 57.3 x 34.4 parent) | 36.77 x 8.00 = 294.2 um² | 30 %; tree_pmos is **−40 %** |
| S2D pad `bias_tree_noab_p_c3`: PBN, PBNC, dummy, TGP only (no BP, no BPC), with an ntap ring | 12.94 x 10.37 = 134.2 um² | 54.45 um² = 41 %; tree_pmos is +32 % area for +62 % gate area |

- **DRC:** 0 items.
- **LVS:** "Circuits match uniquely"; 17 → 6 devices on both sides; 8 nets.
- **Latch-up check:**
  - The run deck checks only the NMOS rule LU.b (`rule_decks/feol/7_2_latchup.drc`).
  - The PMOS rule LU.a (from `sg13cmos5l_maximal.drc`) is therefore checked by `check_tree_pmos.py`. It grows the tie inside the NWell in 0.5 um steps, as the maximal deck does.
  - Result: 0 of 17 P+ shapes uncovered; farthest P+ corner 6.89 um from the tie.
- **Reproducible:** two builds gave the same sha256.

## Floorplan (score)

```
row tree_pmos      # fingers rotated R270: W across, L = 6 up; pitch 1.25, gap 0.25; sources up
  src vdd (top plate + N tie) ; gate vbp ; bulk vdd
  lanes vbp vbn vbnc            # Metal2 over the channels, bottom to top, y 1.02 / 1.43 / 1.84
  voice a BP   1/6 drain=vbp  (5, the diode)    voice b PBN  1/6 drain=vbn (5)
  voice c PBNC 1/6 drain=vbnc (2)               voice x MDBP 1/6 centre dummy, D = S = vdd
  voice r MDBP 0.5/6 end rests
  | k/t | n g | r a b c a b b x a b a c a b r | g n' |
  symmetry M90 about the row centre, with a and b swapped at ±1, ±5, ±6
```

- **Legend:**
  - `k` = BPC 1/4, rotated R270, top aligned, diode.
  - `t` = TGP 1/0.45, unrotated (R0), under BPC.
  - `n` = vbn drop; `n'` = vbnc drop.
  - `g` = vbp gate column (poly tab plus a contact column). The left one carries the pin; the right one also reaches the bottom edge, without a label.
- **Vertical:**
  - The cell bottom (y 0) is the NWell edge, 0.62 below the row's diffusion (NW_c1).
  - Row diffusion runs y 0.62 to 7.30, with the drain stripes at the bottom.
  - Three Metal2 lanes run over the lower channel. There is no track band below the row; L = 6 makes the channel tall enough to carry them (A4's G17).
  - Sources are at the top, under the Metal1 vdd plate (y 7.07 to 8.43).
  - The N tie diffusion is y 7.51 to 7.81, one contact row, 0.03 above the PCells' pSD (pSD_d1).
  - The NWell top is 8.43 (NW_e1 0.62 above the tie).
- **Exits:**
  - vbp leaves through both gate columns, with a Via1 from its lane.
  - vbn and vbnc leave on 0.21 um Metal1 drops just outside the gate columns. These are Metal1 under Metal2, so no staircase is needed.
  - vbpc leaves down BPC's own gate column.
  - TGP is unrotated, so iref, en_3v3_b (gate contact below the diffusion) and ni all leave at the bottom.
- **Well and implants:**
  - One NWell = ThickGateOx rectangle, equal to the cell bbox.
  - One pSD over all P+, which closes the pSD_b 0.31 notches between the PCells' implants.
  - No ring, and no tie between devices.
- **Device cells:** unmodified SG13_dev pmosHV PCells, made static and renamed `tree_pmos_u1l6`, `tree_pmos_r05l6`, `tree_pmos_bpc_w1l4`, `tree_pmos_tgp_w1l045`.
- **Metals:** Metal1 and Metal2 only.

## Matching [m]

- **Same unit cell everywhere:** BP, PBN and PBNC are 5, 5 and 2 copies of the same 1/6 finger, in the same orientation and the same y range. The 5:5:2 ratio therefore holds whatever narrow-width effects a 1 um finger has. Any gradient in y is common to all fingers.
- **Exact common centroid in x:** the row has 13 positions with the dummy x in the centre; the odd counts 5 and 5 need an odd number of positions. Positions, measured from the vias, in pitches from the centre:

  | device | positions | centroid | mean square (pitch²) |
  |---|---|---|---|
  | BP | −6 −3 +1 +3 +5 | 0.000 | 16 |
  | PBN | −5 −2 −1 +2 +6 | 0.000 | 14 |
  | PBNC | −4 +4 | 0.000 | 16 |

  An exhaustive search found no arrangement with exact centroids and three equal second moments. This one has the smallest worst difference (2 pitch²) and only one adjacent pair of the same device (b b).
- **Mirror check:** comparing the row with its mirror image, Activ, GatPoly, Cont, pSD, Metal1 and Metal2 differ by 0.000 um². Via1 differs by 12 vias (0.433 um²), which are exactly the three swapped a/b pairs.
- **Metal over the channels:** every real finger has the same Metal1 tab (0.21 x 1.30 um) and all three lanes over it; only its via picks the net.
- **Neighbours:** every real finger has a finger 0.25 away on both sides, under the merged gate strip. The row ends with the 0.5/6 rests.

## Dummies: no variant netlist needed

MDBP (W 2, L 6) is drawn as x 1/6 + rL 0.5/6 + rR 0.5/6. That keeps the W sum at 2 and the same L, with D = S = B = vdd and G = vbp, so Netgen merges them back into the netlist's MDBP.
- The rests are 0.5 wide rather than A4's minimum of 0.3, because the netlist fixes the total W and the full-width centre dummy is needed for the exact centroid.
- The fingered netlist is `tree_pmos.spice`. Its subckt is `tree_pmos vdd vbp vbn vbnc vbpc iref ni en_3v3_b`, with one line per finger; the dummies are XMDBP_rL, XMDBP_x and XMDBP_rR.

## Pins [m]

Cell coordinates in um; bbox (0, 0; 20.985, 8.430). All pins are Metal1 pin shapes (8/2) with a text label (8/25).

| net | pin box | metal behind it |
|---|---|---|
| vdd | (0, 8.13; 20.985, 8.43), top edge | vdd plate y 7.07 to 8.43 across the full width, with the N tie (0.62, 7.51; 20.365, 7.81) under it. The tree's vdd rail joins along the top. |
| vbpc | (0.230, 0; 0.440, 0.300) | BPC gate column, up to y 6.85 |
| iref | (0.665, 0; 0.875, 0.300) | TGP left S/D line, up to y 1.82 |
| en_3v3_b | (1.080, 0; 1.290, 0.300) | TGP gate pad, up to y 1.23 |
| ni | (1.495, 0; 1.705, 0.300) | TGP right S/D line, up to y 1.82 |
| vbn | (1.885, 0; 2.095, 0.300) | drop to the vbn lane (Via1 at y 1.43) |
| vbp | (2.275, 0; 2.485, 0.300) | left gate column, up to y 6.85. The right gate column (x 20.345 to 20.555) also reaches y 0: same net, no label. |
| vbnc | (20.735, 0; 20.945, 0.300) | drop to the vbnc lane (Via1 at y 1.84) |

**For the assembler:**
- **Signal pins:** all are 0.21 um Metal1 lines ending at the bottom edge, with room for a Via1 on each.
- **Cell edges:** the bottom and side edges are the NWell / ThickGateOx edge. NMOS N+ diffusion inside ThickGateOx must stay 0.62 from it (NW_d1).
- **vdd plate:** it is wide Metal1, so neighbouring Metal1 needs 0.22 spacing (M1_e).
- **Upper metals:** Metal3 and Metal4 are free.

## Decisions

1. **One row, not two.** Two point-symmetric rows of 6 cannot centre the odd counts 5 and 5 without extra dummies or swaps. One row with a centre dummy gives exact centroids. The flat 21 x 8.4 um strip suits a PMOS-on-top, NMOS-below tree with the vdd rail on top; two rows would be about 12.5 x 15.3 = 190 um² [r].
2. **Lanes over the channels** rather than a band under the row. This saves about 1.3 um of height.
3. **Tie inside the cell**, in the top margin under the vdd plate. The cell has to be DRC-clean on its own, and the tie only adds the 0.51 um between the row and the well edge. No ring.
4. **BPC over TGP at the left end.** BPC (L = 4) is 2 um shorter than the row, and TGP fits in that space. Both have their own gates, so they sit outside the row's gate strip, with the poly 0.43 um apart.
5. **Pins at the bottom edge**, as the current routed tree in `make_slot_7.py` has its pins at its bottom.

## Checks and problems hit

- **First DRC run:** one Cnt.b error (0.175 um) in the tie row, because each contact was snapped to the 5 nm grid separately (pitfall P11 of the assembly skill). Fixed by snapping the first contact once and stepping by the on-grid pitch; DRC then reported 0.
- **LVS** matched on the first run.
- **Magic's area bookkeeping:** Magic assigns the whole vdd source/drain area to one dummy (`as=32.78p` on a rest). This has no effect on LVS, but matters if a PEX of this cell is ever compared device by device.
- **KLayout LVS not run:** `sak-lvs.sh -k` needs a CDL file. The required Magic + Netgen LVS matches.
