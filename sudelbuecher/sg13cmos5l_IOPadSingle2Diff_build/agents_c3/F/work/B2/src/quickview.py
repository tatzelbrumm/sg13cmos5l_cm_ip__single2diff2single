# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""quick look at a routed cell: python3 quickview.py <gds> <cell> <png> [x0 y0 x1 y1] [dy]"""
import sys
import klayout.db as db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
g, cn, png = sys.argv[1:4]
win = [float(v) for v in sys.argv[4:8]] if len(sys.argv) > 7 else None
dy = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0
ly = db.Layout(); ly.read(g); top = ly.cell(cn); u = ly.dbu
t = db.Trans(0, int(round(dy / u)))
bb = top.dbbox().moved(db.DVector(0, dy))
win = win or [bb.left, bb.bottom, bb.right, bb.top]
clip = db.Region(db.DBox(*win).to_itype(u))
fig, ax = plt.subplots(figsize=(14, 14 * (win[3] - win[1]) / (win[2] - win[0])))
for (l, d), col, a in [((31, 0), '#2e8b57', 0.08), ((1, 0), '#22aa22', 0.3), ((5, 0), '#c0392b', 0.3),
                       ((8, 0), '#1f6fd0', 0.45), ((10, 0), '#9b59b6', 0.45), ((19, 0), '#000000', 0.9)]:
    li = ly.find_layer(l, d)
    if li is None:
        continue
    r = (db.Region(top.begin_shapes_rec(li)).transformed(t) & clip).merged().decompose_trapezoids_to_region()
    ax.add_collection(PolyCollection([[(p.x * u, p.y * u) for p in q.each_point_hull()] for q in r.each()],
                                     facecolor=col, alpha=a, edgecolor='none'))
for (l, d) in ((8, 25), (10, 25)):
    li = ly.find_layer(l, d)
    if li is None:
        continue
    it = top.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            p = (it.trans() * db.Point(s.text.x, s.text.y))
            x, y = p.x * u, p.y * u + dy
            if win[0] <= x <= win[2] and win[1] <= y <= win[3]:
                ax.text(x, y, s.text_string, fontsize=4)
        it.next()
ax.set_xlim(win[0], win[2]); ax.set_ylim(win[1], win[3]); ax.set_aspect('equal')
fig.tight_layout(); fig.savefig(png, dpi=110)
