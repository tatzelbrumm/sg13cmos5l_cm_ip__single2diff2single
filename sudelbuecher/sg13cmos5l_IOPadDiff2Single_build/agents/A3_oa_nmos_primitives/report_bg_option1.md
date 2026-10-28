# bg_n4, option 1 (dummies D = S = G = g), 2026-10-28 05:43–05:50

A3's report, verbatim:

**Summary (three lines)**
1. Option 1 is in: all 9 bg_n4 dummies (8 × 2/4 in the NA/NB rows plus the 2/1 next to MS2) now have D = S = G = g, B = vss, with the poly still continuous.
2. It fit without growing the cell: same outline (18.12 × 22.80 µm) and every pin box identical to the first version (checked by comparing the GDS). DRC 0, LVS match, latch-up unchanged (farthest N+ 10.33 µm).
3. A connectivity check on metal only (substrate excluded) puts the bottom tie, the top tie and the MS2/MS3/SKS sources on one vss net, and both dummy straps on g.

**Option 1 section for the report**
- **What changed**
  - The two dummy straps are now on g. Each g track (on R0's top and R3's bottom contact row) lands 3 vias on each strap. Neither strap touches the ties any more.
  - MS2's source plate now starts at MS2 (x 2.25), so the left dummy can be on g.
  - Gate area on g that is no longer inverted: 8 × 2 × 4 + 2 × 1 = 66 µm².
- **What it cost**
  - No area. One problem had to be solved first: in the first version the left dummy strap was the only metal vss path between the bottom tie and the top group (top tie, MS2/MS3/SKS sources).
  - New vss path: Metal1 along the bottom tie, then up a right outer column (x 15.54–15.83, y −0.49 to 19.60) into SKS's source tab. That column was free space under MS3/SKS.
  - To free the bottom-tie corner for that path, the lowest ea and eb tracks (R0 bottom, R1 bottom) continue to Metal2 risers (x −1.33…−1.04 and 15.54…15.83) down to the bottom lanes. The ea/eb joiners now stop at those tracks instead of running to the bottom edge.
- **Symmetry of ea / eb**
  - Lengths are still mirror images: vertical runs per device 20.62 µm each, bottom lanes 8.475 µm each, same via counts.
  - The Metal1/Metal2 split now differs: ea has a 0.785 µm M2 riser and a 19.05 µm M1 joiner; eb has 5.675 µm M2 and 9.27 µm M1.
  - This PDK copy has no sheet resistances, so I can't give the exact offset. At 2.5 µA per branch it is a few squares of metal (my estimate, not computed).
- **Checks:** DRC 0 (72 rules); LVS match with dummies 16/4 and 2/1 as g g g vss; pins and outline compared against version 1 and identical; the build gives the same bytes on every run.
- **Skill rules added**
  - [generic] rule 28: bias a dummy at Vgs = 0 by strapping D/S to the gate net when the poly must stay continuous. If the straps were the supply path between ties, plan a separate supply path first.
  - [IHP] rule 28: what option 1 cost here, as listed above. Rule 26 is updated, and pattern P4 and the generic SKILL draft now show the new dummy nets.

**Changed files** (sha256, first 12 hex), under `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/`:
```
eca26681a054  out_bg/bg_n_cells.gds              (option 1)
a852499389af  out_bg/bg_n_cells.cdl              (dummies g g g vss)
9beea461fa71  out_bg/bg_n_cells_v1.gds           (first version, kept)
bbc9f4521c10  out_bg/bg_n_cells_v1.cdl           (first version, kept)
ea2c7d3144e1  out_bg/build_bg_n.py
50c7c13c054d  out_bg/build_bg_n_v1.py            (reproduces the v1 files byte for byte)
af3d913c968e  out_bg/bg_n4.png
da0b9f931957  out_bg/bg_n4_before_after.png
9bd010618051  out_bg/logs/drc_bg_n4.txt
77a4743c15ab  out_bg/logs/lvs_bg_n4.txt
01fd36a5d05d  out_bg/logs/lvs_bg_n4.lvsdb
3ecde419eb65  out_bg/logs/verify_bg_n4.txt
8b4e3ed1bb84  out_bg/logs/build_stdout.txt
fb5fa844c548  out/skill/generic/rules.md
cb4f83378b1b  out/skill/generic/patterns.md
2ae675588640  out/skill/generic/SKILL_draft.md
e0358994368c  out/skill/ihp_sg13cmos5l/rules.md
af3d913c968e  out/skill/ihp_sg13cmos5l/pictures/bg_n4.png
da0b9f931957  out/skill/ihp_sg13cmos5l/pictures/bg_n4_before_after.png
ea63222c3a98  out/logs/score_check.txt
```
The DRC log has the same checksum as before because its text is identical (0 violations, same antenna numbers).
