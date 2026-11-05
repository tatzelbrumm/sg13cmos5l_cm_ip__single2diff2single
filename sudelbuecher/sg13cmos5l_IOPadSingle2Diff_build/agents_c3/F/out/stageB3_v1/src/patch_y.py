# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage B3: take net y's Metal1 jumper off the left edge stub (M1.f in the abutted row).
#   python3 patch_y.py <stage-B2 s2d_block.gds> <out s2d_block.gds>
# Block coordinates (pad = block + 26 in y). Stage B2's y left detour: M2 up x 3.09..3.38, left along y 123.17..123.46
# to x 0.66, down to 114.6, Via1, M1 jumper x 1.47..1.76 down to 91.92, Via1, M2 down x 1.47..1.76 to 78.96.
# New: the descent is one Metal2 column x 1.81..2.07 in the reserve (0.21 from the template M2 strip x 1.30..1.60 and
# from the M2 at x 2.28), with a 0.29 jog at y 91.92..92.21 onto the unchanged lower M2. No y Metal1 left of x 4.3.
import sys
import klayout.db as db
src, dst = sys.argv[1:3]
ly = db.Layout(); ly.read(src); top = ly.cell('s2d_block'); u = ly.dbu
L = {k: ly.find_layer(*v) for k, v in dict(M1=(8, 0), V1=(19, 0), M2=(10, 0)).items()}
def dp(s): return db.DPolygon([db.DPoint(*map(float, q.split(','))) for q in s.strip('()').split(';')])
OLD = {'M1': ['(1.47,91.92;1.47,114.575;0.66,114.575;0.66,114.865;1.76,114.865;1.76,91.92)'],
       'V1': ['(1.52,91.97;1.52,92.16;1.71,92.16;1.71,91.97)', '(0.71,114.625;0.71,114.815;0.9,114.815;0.9,114.625)'],
       'M2': ['(3.09,97.05;3.09,123.17;0.95,123.17;0.95,114.575;0.66,114.575;0.66,123.46;3.38,123.46;3.38,97.34;'
              '4.605,97.34;4.605,97.05)']}
NEW_M2 = [(3.09, 97.05, 3.38, 123.46), (3.38, 97.05, 4.605, 97.34), (1.81, 123.17, 3.38, 123.46),
          (1.81, 91.92, 2.07, 123.46), (1.47, 91.92, 2.07, 92.21)]
for k, polys in OLD.items():
    want = [dp(s).to_itype(u) for s in polys]
    for w in want:
        hit = [sh for sh in top.shapes(L[k]).each() if sh.polygon == w or (sh.is_box() and db.Polygon(sh.box) == w)]
        assert len(hit) == 1, (k, w, len(hit))
        top.shapes(L[k]).erase(hit[0])
r = db.Region()
for b in NEW_M2: r.insert(db.DBox(*b).to_itype(u))
for p in r.merged().each(): top.shapes(L['M2']).insert(p)
ly.write(dst)
print('patch_y: removed y M1 jumper + 2 Via1 + upper M2 detour; inserted M2 x 1.81..2.07 (block y 91.92..123.46)')
