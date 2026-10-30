**Summary (five lines)**
1. `oa_n10` holds M10, M11, MC10, MS2, MS3 and SKS in 36.72 × 19.965 = 733 µm². It replaces oa_nmir + oa_misc_n (832 + 120 = 952 µm²). `oa_mcs_c` is 31.22 × 8.57 = 268 µm² and replaces oa_mcs (376 µm²).
2. Fingers are R270, one array per row at the Gat.b1 gap, interdigitated by rows `A B A A B A A B A`. M10 and M11 share one centroid, and a script checks that. Each Metal2 track runs directly over a row of S/D contacts, so rows sit at Act.b 0.21 with no band and no tap between them.
3. Each cell has one p+ tie strip with a single contact row. There is no ring and no NWell. The farthest N+ Activ is 18.90 µm (oa_n10) and 7.48 µm (oa_mcs_c) from its tie, against LU_b 20. The two cells can overlap their ties: together 36.72 × 27.70 = 1017 µm², against 1327.
4. DRC with the Python subset: 0 violations on both cells and on the overlapped pair. LVS: both match. The copied device cells are XOR-identical to the library, and the build gives the same bytes every run.
5. Backannotation: M10 ng 8→18 and M11 ng 4→9, total W and L unchanged. 20 narrow 2/1 dummies replace the old 10/1 dummy. The skill export is in `out/skill/generic/` and `out/skill/ihp_sg13cmos5l/`.

---

# oa_core_pd NMOS primitives, compact (IHP sg13cmos5l): report
2026-10-28, 02:39–03:24 CET, cloud workspace only. "Measured" means taken from the GDS or the check logs; reasoning is marked as such. Tags: [generic] = lesson for any process, [IHP] = the sg13cmos5l value.

**Sizes (bounding boxes, measured)**
| before | after |
|---|---|
| oa_nmir 34.12 × 24.38 = 832 µm² + oa_misc_n 9.51 × 12.61 = 120 µm² | oa_n10 36.72 × 19.965 = 733 µm² |
| oa_mcs 62.50 × 6.01 = 376 µm² | oa_mcs_c 31.22 × 8.57 = 268 µm² |
| total 1327 µm² | both cells with the shared tie: 1017 µm² (−23 %) |

**oa_n10: which device sits on which finger (measured)**
- **Device cells:** every finger is the unmodified library cell `nmosHV$7` (10/1), R270, one array per row at 10.25 µm pitch (Gat.b1 gap 0.25). Row pitch is 1.89 = 1.68 + Act.b 0.21.
- **End dummies:** `nmosHV_w2_l1` (2/1). The library has no 2/1 cell, so it is built from the 10/1 and 2/4 cells, and the script checks it layer by layer against both.
- **Rows, bottom to top (Activ y):**
  - X0 at 0.00: `d A A A d`
  - X1 at 1.89: B row
  - X2 at 3.78 and X3 at 5.67: A rows
  - X4 at 7.56: B row
  - X5 at 9.45 and X6 at 11.34: A rows
  - X7 at 13.23: B row
  - X8 at 15.12: A row
  - Y at 17.01: `e C S e`
- **x positions:** dummy 0–2; fingers 2.25–12.25, 12.50–22.50, 22.75–32.75; dummy 33–35.
- **Letters:** A = M10 (18 fingers), B = M11 (9), C = MC10, S = MS2, d and e = dummies (20 in all).
- **MS3 and SKS:** MS3 (`nmosHV$9`, R0) at (25.00, 17.05) and SKS (`nmosHV$5`, R0) at (27.89, 17.05), in the free end of row Y.
- **Why MS3 and SKS are inside oa_n10 and not a separate tap-less cell (reasoning):** row Y is two fingers short, so x 25–33 is empty anyway. MS3 and SKS join row Y's vss and ks tracks and the vpc track above it locally.
- **Matching [generic]:** the row pattern is mirror- and point-symmetric.
- **Wiring:**
  - Each row has S on its bottom contact row and D on its top contact row. One M2 track runs over each, with 3 Via1 per finger on an M1 pad.
  - At the left end, from the outside in: d10 joiner, vnc gate bar, dummy strap (vss). The right end mirrors it, with the vres joiner outermost.
  - d10 (M10 drain = MC10 source) stays internal.

**oa_mcs_c (measured)**
- MCS and MCL (`nmosHV$8`, 3.4/30) are a 1 × 2 array at 3.65 pitch (Gat.b1 gap), R0. The 30 µm gates run horizontally and the gate poly is one plate.
- Reasoning for the orientation: 31 µm wide matches oa_n10's 36.7 µm, so it stacks under it. Vertical gates would make it about 8.6 × 31 µm next to a 20 µm tall cell.
- Wiring: sources on the left, joined to the tie. A gate contact row below MCS is joined to MCS's drain (diode). MCL's drain (vres) goes up to the top edge.
- No dummies (the brief did not ask for them).

**Ties and latch-up (measured; LU_b 20 µm comes from the json only [IHP])**
| cell | tie strip (Activ, µm) | farthest N+ Activ | other sides |
|---|---|---|---|
| oa_n10 | (0.00, −0.51; 35.00, −0.21) | 18.90 µm (top of row Y) | no tie, no ring, no tap between rows |
| oa_mcs_c | (0.00, 7.48; 30.68, 7.78) | 7.48 µm | none |

- [IHP] Tie Activ is 0.30 = Cnt.a + 2 Cnt.c, with one contact row at 0.34 pitch; M1 is 0.26.
- **Sharing the tie:** oa_mcs_c placed at (4.91, −7.99) relative to oa_n10 (right edges flush) overlaps oa_n10's tie exactly: same contact grid, same y. Its vres riser also lands on oa_n10's. DRC of that pair: 0.
- No NWell anywhere. ThickGateOx is drawn as one polygon that follows the devices (14 vertices in oa_n10).

**Checks (measured)**
- **DRC** with the Python subset (72 rules): 0 on oa_n10, oa_mcs_c and the pair; largest antenna ratio 0.37.
  - To show the checker sees these cells, I broke copies on purpose. Deleting the tie gave LU.b. Moving MS3 0.1 µm left gave Act.b, Gat.b1 and Cnt.f. Moving one row 0.03 µm down gave Act.b and Cnt.f.
  - IHP's own Ruby deck was not run [IHP]: the container has KLayout 0.28.16 without Ruby, and several included deck files are missing from the PDK copy.
- **LVS:** oa_n10 matches (8 devices after combining parallel fingers); oa_mcs_c matches (2). Removing one Via1, and adding one M2 short, each gave a mismatch.

**Backannotation (every ng / w change)**
- M10: 180/1, ng 8 → 18 × 10/1. Total W unchanged; v1 already used 18 fingers.
- M11: 90/1, ng 4 → 9 × 10/1. Total W unchanged.
- MC10, MS2, MS3, SKS, MCS, MCL: no change.
- Dummies (new): 18 × 2/1 with G = vnc and 2 × 2/1 with G = vbr, all with D = S = B = vss.
  - They replace the old single 10/1 dummy. In the v1 `oa_core_pd.cdl`, MDUMN becomes W = 36u L = 1u, plus a new W = 4u L = 1u device on vbr.
  - Not simulated: this adds gate area on vnc (36 against 10 µm²) and 4 µm² on vbr.

**Pins (cell coordinates in µm, box plus text, measured)**
- **oa_n10:**
  - vss, M1, (−0.860, −0.490; −0.570, −0.230), left edge
  - vres, M2, (35.295, −0.780; 35.585, −0.490), bottom edge
  - vbr, M1, (−0.390, 18.895; −0.180, 19.185), top edge
  - vpc, M2, (6.695, 18.895; 6.985, 19.185), top edge
  - en_3v3_b, M1, (28.375, 18.895; 28.535, 19.185), top edge
  - ks, M2, (28.725, 18.895; 29.015, 19.185), top edge
  - vnc, M1, (35.180, 18.895; 35.390, 19.185), top edge
- **oa_mcs_c:**
  - vss, M1, (−0.270, 7.500; 0.020, 7.760), left edge
  - vres, M2, (30.385, 7.760; 30.675, 8.050), top edge
  - vbr, M2, (−0.270, −0.430; 0.020, −0.140), left edge
- vbr has one pin per cell, so the assembler must join oa_n10's (top left) and oa_mcs_c's (left edge): about 20 µm along the left edge.

**Where I departed from the brief or the earlier style**
1. **Tracks over the contacts:** M2 tracks run over the contact rows instead of short tabs into bands between rows. The "drain tabs" are now 3-Via1 pads on the contact row.
2. **Dummy gates:** they stay on the row's gate strip (vnc or vbr), as in bg_nab, with S = D = vss through the strap. I read "gates tied off" as the 2026-10-27 convention, not as gate = vss.
3. **Pair cell:** the overlapped oa_n10 + oa_mcs_c cell is only a check. It is in `logs/`, not in `oa_n_cells.gds`.
4. **No NWell:** the user's 02:58 notice ("separate nwells … are EXTREMELY wasteful") needed no change, since I drew no NWell. [IHP] An n+ ring in its own NWell would cost 2.16 µm per side (NW.d1 0.62 + NW.e1 0.62 + 0.30 + NW.e1 0.62), against 0.51 µm for a p+ tie.

**Lessons for the bandgap NMOS cells (bg_nab, bg_misc_n)**
- [generic] Interdigitating by rows and keeping each row to one device type removes the bands. bg_nab could be `d A d / d B d / d B d / d A d`; my estimate (not drawn) is about 16 × 20 µm, against 48.9 × 8.2 µm today.
- [IHP] With one tie strip, four rows of L = 4 µm reach 19.56 µm (4 × 4.68 + 3 × 0.21 + 0.21), close to the 20 µm limit. Add a second strip, or share a tie with the oa NMOS group if the blocks abut.
- [generic] bg_misc_n is row Y here with gate g: `e S e`, then MS3 and SKS in the free end. It fits best as the top row of the bandgap's NMOS block, facing the PMOS side, sharing that block's tie.
- [IHP] The 2/4 dummy cell already exists (`nmosHV$11`). A missing W/L variant can be built with `derive_mos`, which checks the result against two existing variants.
- [generic] Put the short row toward the cells that use its nets, put the tie toward a neighbour of the same substrate type, and start the tie's contact grid at the shared edge.

---

**Skill export**
- `out/skill/generic/` has no IHP names or rule values. It holds the patterns in score form (a script checks the score's symmetry claims), the generator and renderer that take every value from a process adapter, an adapter template, the rules list, a SKILL draft with a section on porting to another process, and a tile picture.
- `out/skill/ihp_sg13cmos5l/` holds the IHP adapter (each value with its json key and deck file), IHP know-how, quirks and missing deck files, the rules with IHP values, the pitfalls and workarounds, the IHP check tools, and the pictures with numbers.
- Every rule in both `rules.md` files is tagged [generic] or [IHP].
- The 03:01 notice (no closed ring, ties follow the outline) and the 03:04 notice (polygonal outlines, process adapter) are both applied and recorded in the rules.
- One thing to know: writing `REPORT_oa_n.md` was blocked for me, so the report exists only in this reply.

**Deliverables** (sha256, first 12 hex), all under `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/out/`:
```
865aa155d8b6  oa_n_cells.gds
735f26ba6857  oa_n_cells.cdl
0c6da929db75  build_oa_n.py
c473676e527f  oa_n10.png
e1e7ffc65722  oa_mcs_c.png
978807d01c20  logs/drc_oa_n10.txt
8cc6022dfedb  logs/drc_oa_mcs_c.txt
9fa205e2a1ad  logs/drc_oa_n_pair.txt
5b35dab9d872  logs/oa_n_pair_check.gds
0cf93b0cf791  logs/lvs_oa_n10.txt
bab7ab561f68  logs/lvs_oa_mcs_c.txt
62fc31231941  logs/lvs_oa_n10.lvsdb
ba16c38b1dcf  logs/lvs_oa_mcs_c.lvsdb
0a69c804662f  logs/verify_oa_n.txt
0bb312fc85cf  logs/score_check.txt
c529751a2972  logs/build_stdout.txt
f8d90dbec97d  skill/generic/SKILL_draft.md
5b90f40db005  skill/generic/patterns.md
ec19ca4ac215  skill/generic/rules.md
c7aaf018fd2c  skill/generic/generator.py
e1eca22f02f2  skill/generic/render.py
bcbeee2f2f1f  skill/generic/adapter_template.py
91da3a8c2701  skill/generic/pictures/tile_roles.png
09cb34875553  skill/ihp_sg13cmos5l/SKILL_draft.md
258e55411717  skill/ihp_sg13cmos5l/rules.md
ca39002fbeb6  skill/ihp_sg13cmos5l/adapter.py
5963938172cd  skill/ihp_sg13cmos5l/make_pictures.py
08bee6b69296  skill/ihp_sg13cmos5l/pictures/tile.png
acdf9707a290  skill/ihp_sg13cmos5l/pictures/before_after.png
def182fe8c18  skill/ihp_sg13cmos5l/pictures/rule_savings.png
b299abdca91f  skill/ihp_sg13cmos5l/tools/oa_core_pd_drc.py
88fc4331c034  skill/ihp_sg13cmos5l/tools/oa_core_pd_lvs.py
```
