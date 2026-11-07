<!--
Saved verbatim by the main session on 2026-11-07 at the user's request: the NMOS specialist agent could not write .md
files in this session and returned this report in its hand-back. Text unchanged, except that a model name in the byline is replaced by `claude`.
-->
# Report: tree_nmos (NMOS half of bias_tree_noab_pd, slot 7, IHP sg13cmos5l)
2026-11-07, claude. "Measured" means read from the GDS or the logs; anything else is marked as reasoning.

## Floorplan
One row of rotated fingers: W along x, L along y. Sources are at the bottom on the tie, drains at the top. Each gate net has one continuous poly plate.
```
 s | d  A  B  C  B  A  B  A  B  A  C  A  B  d | N  N  N  N  N | c
   |<------------- poly plate ni ------------>|<- plate vbn ->|<-vbnc
 ============ p+ tie strip + Metal1 vss plate along the whole bottom ============
```

**Letters.** Each is one 1.2/6 finger unless noted.
- d = one half of MDBN
- A = NI, B = NBP, C = NBPC
- N = BN
- c = BNC (1/8)
- s = TDN + TGN drawn as one Activ stack with two gates (1/0.45 each). Bottom to top: vss | en_3v3_b gate | ni | en_3v3 gate | iref. It uses the nmosHV ng=2 PCell, whose two gate polys are separate, so each gate gets its own contact and net.

**Pitches.**
- Fingers sit at 1.45 µm: W 1.2 + Gat.b1 0.25. The poly of neighbouring fingers overlaps, so each plate is one polygon.
- Between two plates the Activ gap is 0.54: end cap 0.18 + Gat.b 0.18 + end cap 0.18.

**Gate contact columns.** One per plate, 0.20 µm from the Activ, each with a Metal1 column:
- ni: left of the left dummy
- vbn: right of BN
- vbnc: right of BNC

The diode connections (NI, BN, BNC) are made in Metal1 at the top.

**Wiring above the row.**
- Each drain has a Metal1 pad, 0.26 tall.
- Three Metal2 tracks, 0.26 wide at 0.47 pitch:
  - track 1, y 6.40–6.66: vbp, lying directly over the pads
  - track 2, y 6.87–7.13: ni, which also lands on the ni gate column
  - track 3, y 7.34–7.60: vbpc
- Metal1 stubs, 0.26 wide, connect the other fingers' pads to their tracks.
- Each dummy's drain (vss) reaches the vss plate through a Metal2 strap drawn over that dummy finger.

**Height.** BNC (L = 8, Activ 8.68 tall) sets the cell height. The three tracks fit inside that height at no extra cost.

## Area
| layout | size (µm) | area | devices | gate area / bbox |
|---|---|---|---|---|
| naive `tree_row_n` (in `bias_tree_noab_pd.gds`) | 49.08 × 8.61 | 422.6 µm² | all 8 | 34.5 % |
| `bias_tree_noab_n_c3` | 24.21 × 9.215 | 223.1 µm² | no BN, no BNC | 45.6 % |
| **tree_nmos** | 32.21 × 9.73 (x −2.31…29.90, y −0.78…8.95) | **313.4 µm²** | all 8 | 46.5 % |

The whole naive tree is 57.31 × 34.41 µm = 1972 µm².

## Matching (ni plate)
**Why it is matched by construction.**
- All four ni devices use the same 1.2/6 unit, so NI : NBP : NBPC = 5 : 5 : 2 exactly.
- All 14 fingers share one poly plate and one source plate. They have the same orientation and the same current direction.
- The two halves of MDBN are the end dummies. Every active finger therefore has a gate finger 0.25 µm away on both sides.

**Centroids (measured).**
- Row centre x = 10.025.
- NBPC = 10.025, exact.
- NI = 10.17 and NBP = 9.88, so NI and NBP are 0.29 µm (0.2 pitch) apart.

**Why the centroid cannot be exact in one row (reasoning).** NI and NBP each have 5 units, an odd count. In 12 slots each would need a centroid sum of 27.5, which integers cannot give.

**How the order was chosen.** I searched all 16632 orders of the 12 inner slots. `ABCBABABACAB` is the order I kept:
- it has the smallest centroid error, 0.2 slot;
- it has the smallest second-moment difference, so it also handles a quadratic gradient best;
- no two neighbouring fingers belong to the same device.

**Alternatives not chosen.** Each would cost a second row of about 7 µm height, or much more Activ-gap overhead:
- a third row;
- half-width 0.6/6 fingers.

**Size of the offset (reasoning).** A 1 %/mm gradient across 0.29 µm gives about 3 ppm current error. That is negligible against the random mismatch of 7.2 µm² fingers.

**Metal over channels.** None over the matched fingers: the drain tracks run above the Activ. The only metal over a channel is each dummy's vss strap.

**BN.** It is a load diode, not part of the mirror. It has its own plate after the 0.54 µm gap.

## Pins (cell coordinates in µm; pin box plus text on the same metal)
| net | layer | box | where it is |
|---|---|---|---|
| vss | M1 | (−2.310, −0.780; −1.310, −0.480) | Label only. The Metal1 vss plate runs the full width at y −0.78…0.23 along the bottom edge and covers the p+ tie, so a vss rail can join it anywhere. |
| en_3v3_b | M2 | (−2.270, 8.660; −1.990, 8.950) | top edge |
| en_3v3 | M1 | (−2.250, 8.660; −1.990, 8.950) | top edge, under the en_3v3_b riser (same x, different metal) |
| iref | M2 | (−1.430, 8.660; −1.150, 8.950) | top edge |
| ni | M1 | (−0.460, 8.660; −0.200, 8.950) | top of the ni gate column; ni is also on Metal2 track 2 |
| vbpc | M1 | (4.820, 8.660; 5.080, 8.950) | stub of finger 3; also track 3 |
| vbp | M1 | (9.170, 8.660; 9.430, 8.950) | stub of finger 6; also track 1 |
| vbn | M1 | (27.790, 8.660; 28.050, 8.950) | top of the vbn gate column |
| vbnc | M1 | (28.380, 8.660; 29.840, 8.950) | top edge |

**Notes for the assembler.**
- All signal pins are on the top edge, toward the PMOS half.
- Metal2 is free above y 7.81 for x > −0.95.
- Metal1 is free above y 7.6 except for the pin stubs and the gate columns.
- The PMOS NWell must stay at least 0.35 µm above the top edge over BNC (from NW.d1 0.62; reasoning).

## Latch-up and ties (measured)
- One p+ tie strip, Activ (−1.79, −0.51; 29.38, −0.21), with one contact row at 0.34 pitch.
  - It sits 0.21 below the row (Act.b).
  - pSD encloses it by 0.03 (pSD.c1), which leaves 0.18 to the N+ Activ (pSD.d).
  - It lies inside the common ThickGateOx rectangle.
- No ring, no NWell, no tap between fingers.
- The farthest N+ from the tie is the top of BNC at 8.89 µm, against the LU.b limit of 20 µm. For the mirror it is 6.89 µm.

## Checks
**DRC, main deck (the required command).** `ihp-sg13cmos5l.drc` with feol/beol True, run_mode deep, threads 4, topcell tree_nmos: **0 items**.

**DRC, maximal rule deck.** `rule_decks/sg13cmos5l_maximal.drc`: **0 items**.

**Negative tests, run on scratch copies and then deleted.** They show the decks do see this layout:

| change | result | caught by |
|---|---|---|
| finger pitch 1.42 | 17 × Gat.b1 | maximal deck only |
| pSD enclosure 0.06 | 21 × pSD.d | maximal deck only |
| tie removed | 3 × LU.b | main deck |

**LVS.** Both comparisons give "Circuits match uniquely".

**Caution about the LVS exit code.** `sak-lvs.sh` returns 0 even when there are property errors. A reference with NBPC at 3.6u still gave rc = 0 with "Property errors were found". Read `tree_nmos.lvs.out`, not the exit code.

## Decisions
1. **1.2/6 unit, rotated, one row.**
   - 1.2 µm is the largest unit W that divides both 6 and 2.4.
   - With L much larger than W, separate Activs at the Gat.b1 gap pack tighter than shared-diffusion fingers along L.
   - BNC sets the height anyway, so a second row would only add height.
2. **MDBN as the two end dummies.** Its two 1.2/6 halves are the end dummies, as in the source netlist: D = S = vss, gate on the ni plate. No extra dummies were needed.
3. **BN and BNC in the same row,** each on its own plate. They share the tie and the vss plate with the mirror.
4. **TDN and TGN as one Activ stack** sharing the ni diffusion, placed bottom-left next to the ni gate column.
5. **Spice netlist written one line per finger.** Netgen merges the fingers back to the source W.
6. **Not done:** BNC turned horizontal and moved to a band above BN. My estimate is about 282 µm² (−10 %), but BNC's source would need a vss path up through Metal2 and the pin edge would get crowded. I did not draw it.
