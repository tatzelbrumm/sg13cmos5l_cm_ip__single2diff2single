**Summary (five lines)**
1. `bg_n4` holds NA, NB, MS2, MS3 and SKS in one cell, 18.12 × 22.80 µm = 413 µm², against 492 µm² for bg_nab + bg_misc_n (−16 %). The width is inside A2's 15–22 µm.
2. NA and NB are 2 × 10/4 each in four single-finger rows `A B B A`. The upper two rows run with the current reversed, so the stack is a mirror image including current direction, and NA and NB share one centroid (script-checked).
3. MS2 is a fifth row on top, and MS3 and SKS sit in its free end. That stack is too tall for one tie (21.45 µm > LU_b 20), so there are two one-row p+ tie strips, bottom and top. Farthest N+ is now 10.33 µm; deleting the top strip gives 8 LU.b errors.
4. DRC with the Python subset: 0. LVS: match. Device cells are XOR-identical to the library, and the build gives the same bytes every run.
5. Pins follow A2's request: g, vpc, ks and en_3v3_b on top; ea and eb next to each other on the bottom; vss on the bottom tie. `out/skill/` is extended with tagged rules 19–27, pattern P4 and the pictures. The oa cells did not change (`oa_n_cells.gds` is still 865aa155d8b6).

---

# bg_n4 (bandgap NMOS, IHP sg13cmos5l): report
2026-10-28, 04:29–05:25 CET, cloud workspace only. "Measured" means taken from the GDS or the logs.

**Sizes (measured)**
- Before: bg_nab 48.87 × 8.21 = 401 µm² plus bg_misc_n 7.23 × 12.61 = 91 µm², total 492 µm².
- After: bg_n4 18.12 × 22.80 = 413 µm², both tie strips and all five devices included.

**Finger map (measured)**
All rows are R270 at the Gat.b1 gap of 0.25 µm. Rows sit 0.21 µm apart (Act.b). x positions: dummy 0–2, finger 2.25–12.25, dummy 12.5–14.5.

| row | y (µm) | contents | current direction |
|---|---|---|---|
| R0 | 0.00–4.68 | d, NA, d | S at the bottom |
| R1 | 4.89–9.57 | d, NB, d | S at the bottom |
| R2 | 9.78–14.46 | d, NB, d | reversed: S at the top |
| R3 | 14.67–19.35 | d, NA, d | reversed |
| Y | 19.56–21.24 | e, MS2 | reversed (S = vss on top) |

- MS3 (R0) sits at (12.50, 19.60) and SKS (R0) at (15.39, 19.60), in row Y's free end.
- **Device cells:** the library's `nmosHV$10` (10/4), `$11` (2/4 dummies), `$7` (MS2), `$9` (MS3) and `$5` (SKS). The 2/1 dummy `nmosHV_w2_l1` is the one built for oa_n10.
- **Why not a 2 × 2 cross-quad:** it needs two 10/4 fingers per row, which makes the cell about 27.4 µm wide, against A2's 15–22 µm. The library has no 5/4 cell, and none can be built because there is no W = 5 cell to take the contact layout from.
- **Matching:**
  - Linear gradients in x and y cancel, because NA and NB share one centroid.
  - Each device has one finger in each current direction.
  - Every finger has 0.21 µm of Activ spacing above and below (tie, neighbouring row, or row Y) and dummies 0.25 µm to the left and right.
  - Not compensated: NA sits in the outer rows and NB in the inner rows, so a quadratic gradient along y is not cancelled (reasoning).

**How ea and eb are kept symmetric (measured from the GDS)**
- ea leaves on the left, through a joiner at x −0.86 to −0.57; eb leaves on the right, through a joiner at x 15.07 to 15.36.
- They return on one Metal2 track at the bottom edge and stop 0.21 µm apart on the array's centre line, x = 7.25.
- Per device the two fingers' tracks are 13.11 µm each. The vertical runs down to the bottom track add up to 20.62 µm for both (NA: 0.785 + 19.835; NB: 5.675 + 14.945). The bottom tracks are 8.005 µm each, and both sources have the same number of vias.
- The cell outline's centre is x = 7.73, because MS3 and SKS widen the right side. The pins are symmetric about the device centre at 7.25, not about the outline centre (A2 asked for the latter; this departs from that).

**Tie strips and latch-up (measured; LU_b = 20 µm, json only)**
- Bottom strip: (0.00, −0.51; 14.50, −0.21). It serves N+ up to 10.33 µm away.
- Top strip: (0.00, 21.45; 12.25, 21.75), joined to vss through MS2's source plate and the left dummy strap. It serves N+ up to 7.67 µm away.
- Without the top strip, the farthest N+ would be 21.45 µm from the bottom one (four rows of L = 4 plus row Y).
- No ring, no NWell, no tie between rows.
- Towards the PMOS NWell above: the top tie's Activ is 0.27 µm below the top edge, and N+ Activ is at least 0.78 µm below. With NW.f1 and NW.d1 at 0.62 µm, the NWell must stay at least 0.35 µm above the edge.

**Checks (measured)**
- DRC (`oa_core_pd_drc.py`): 0 violations; largest antenna ratio 0.47.
  - The first run flagged one error: M1.d (minimum metal1 area) on the 0.29 × 0.29 µm pad over MS3's gate contact. The pad is now 0.29 × 0.315 µm.
- LVS: match, 7 devices after combining parallel fingers.
- Every finger cell is XOR-identical to its library cell, and two builds give the same bytes.

**Backannotation**
- NA: 20/4 ng=1 becomes 2 × 10/4; total W stays 20 µm. Same as the library bg_nab.
- NB: same as NA.
- MS2, MS3, SKS: no change.
- Dummies, all with D = S = B = vss and gate on g: 8 × 2/4 (16/4 combined; the library had 4/4) and 1 × 2/1 (new).
- Not simulated: the dummies' gate area on g grows from 16 to 66 µm², which may slow start-up a little.

**Pins (cell coordinates in µm; my assumption: PMOS above, pnp / resistors below, as in A2's floorplan)**
- g: M1 (−0.390, 21.730; −0.180, 22.020), top edge
- vpc: M2 (−1.330, 21.730; −1.040, 22.020), top-left corner
- ks: M1 (16.225, 21.730; 16.515, 22.020), top edge
- en_3v3_b: M1 (15.875, 21.730; 16.035, 22.020), top edge
- ea: M2 (6.855, −0.780; 7.145, −0.490), bottom edge
- eb: M2 (7.355, −0.780; 7.645, −0.490), bottom edge
- vss: M1 (0.280, −0.490; 0.570, −0.230), on the bottom tie strip, 0.29 µm above the bottom edge

**Lessons added to the skill**
1. [generic] Latch-up stack limit (rule 19): if the row stack exceeds the latch-up distance, add a second tie strip on the far side, never between rows. [IHP] One tie strip covers at most 4 rows of L = 4 µm or 10 rows of L = 1 µm.
2. [generic] Reverse the current in the mirror half of `A B B A` (rule 20). This is the `flip` keyword, checked by the new `mirror_y_orient` claim in the score.
3. [generic] Matched sources leave on opposite sides and return on one track to two adjacent pins on the array's centre line (rule 22).
4. [generic] A row whose source is vss can face the tie and connect with one M1 plate (rule 21).
5. [generic] One accepted case of metal over a channel: an M2 stub over a small device's own gate, same net (rule 24).
6. [generic] A pad around a single via must meet the minimum metal area (rule 25). [IHP] M1_d 0.09 µm², so the pad is 0.29 × 0.315.
7. [IHP] Why the cross-quad failed (rule 22), the top tie's metal connection (rule 26), and the NWell spacing above the top edge (rule 27).

---

**Files** (sha256, first 12 hex), under `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/`:
```
9beea461fa71  out_bg/bg_n_cells.gds
bbc9f4521c10  out_bg/bg_n_cells.cdl
f0cfd2a5d408  out_bg/build_bg_n.py
43621de96bbe  out_bg/make_bg_pictures.py
80f6ed453757  out_bg/bg_n4.png
299ef1105b79  out_bg/bg_n4_before_after.png
9bd010618051  out_bg/logs/drc_bg_n4.txt
fa38d7f8aa90  out_bg/logs/lvs_bg_n4.txt
46406668a9ad  out_bg/logs/lvs_bg_n4.lvsdb
3ecde419eb65  out_bg/logs/verify_bg_n4.txt
8b4e3ed1bb84  out_bg/logs/build_stdout.txt
300e613cd958  out/skill/generic/SKILL_draft.md        (extended)
17bb495d685c  out/skill/generic/patterns.md          (P4 added)
ea258a932f3c  out/skill/generic/rules.md             (19-26 added)
38debcaf0e2c  out/skill/generic/generator.py         (flip rows, mirror_y_orient)
f1b77016d2f1  out/skill/generic/adapter_template.py  (m1_area)
e1eca22f02f2  out/skill/generic/render.py
91da3a8c2701  out/skill/generic/pictures/tile_roles.png
463569b73886  out/skill/ihp_sg13cmos5l/SKILL_draft.md (extended)
fe5b3b7b6d2b  out/skill/ihp_sg13cmos5l/rules.md       (19-27 added)
77c5412f8f24  out/skill/ihp_sg13cmos5l/adapter.py     (10/4 device, M1_d)
5963938172cd  out/skill/ihp_sg13cmos5l/make_pictures.py
80f6ed453757  out/skill/ihp_sg13cmos5l/pictures/bg_n4.png
299ef1105b79  out/skill/ihp_sg13cmos5l/pictures/bg_n4_before_after.png
08bee6b69296  out/skill/ihp_sg13cmos5l/pictures/tile.png
acdf9707a290  out/skill/ihp_sg13cmos5l/pictures/before_after.png
def182fe8c18  out/skill/ihp_sg13cmos5l/pictures/rule_savings.png
b299abdca91f  out/skill/ihp_sg13cmos5l/tools/oa_core_pd_drc.py
88fc4331c034  out/skill/ihp_sg13cmos5l/tools/oa_core_pd_lvs.py
ea63222c3a98  out/logs/score_check.txt               (now checks P4 too)
865aa155d8b6  out/oa_n_cells.gds                     (unchanged)
735f26ba6857  out/oa_n_cells.cdl                     (unchanged)
```
