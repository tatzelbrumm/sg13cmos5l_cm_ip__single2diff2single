# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Picture of one cell (device layers, Metal1 / Metal2, Via1, pins, device notes).
    python3 render_cell.py <gds> <cell> <out.png> [x0 y0 x1 y1]"""
import sys

import klayout.db as db
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.collections import PolyCollection    # noqa: E402

gds, name, png = sys.argv[1:4]
ly = db.Layout()
ly.read(gds)
c = ly.cell(name)
u = ly.dbu
b = c.dbbox() if len(sys.argv) < 8 else db.DBox(*[float(v) for v in sys.argv[4:8]])
STY = [((31, 0), "#2e8b57", 0.08, "NWell"), ((44, 0), "#b8b860", 0.08, "ThickGateOx"), ((14, 0), "#d2b48c", 0.25, "pSD"),
       ((1, 0), "#22aa22", 0.50, "Activ"), ((5, 0), "#c0392b", 0.55, "GatPoly"), ((6, 0), "#111111", 0.9, "Cont"),
       ((8, 0), "#3a8fd9", 0.35, "Metal1"), ((19, 0), "#ff2a2a", 0.9, "Via1"), ((10, 0), "#8e7cc3", 0.40, "Metal2")]
s = min(24.0 / b.width(), 16.0 / b.height())
fig, ax = plt.subplots(figsize=(max(6.0, b.width() * s) + 1, max(4.0, b.height() * s) + 1.2))
for (l, d), col, a, n in STY:
    li = ly.find_layer(l, d)
    if li is None:
        continue
    r = (db.Region(c.begin_shapes_rec(li)) & db.Region(b.to_itype(u))).merged().decompose_trapezoids_to_region()
    ax.add_collection(PolyCollection([[(p.x * u, p.y * u) for p in q.each_point_hull()] for q in r.each()],
                                     facecolor=col, alpha=a, edgecolor="none"))
for (l, d), col in (((8, 25), "#0b3d91"), ((10, 25), "#3b2a70"), ((63, 0), "#5a1a5a")):
    li = ly.find_layer(l, d)
    if li is None:
        continue
    it = c.begin_shapes_rec(li)
    while not it.at_end():
        sh = it.shape()
        if sh.is_text() and sh.text_string not in ("nmosHV", "pmosHV", "well", "sub!"):
            q = it.trans() * db.Point(sh.text.x, sh.text.y)
            if b.contains(db.DPoint(q.x * u, q.y * u)):
                ax.text(q.x * u, q.y * u, sh.text_string, fontsize=8 if l != 63 else 9, ha="center", va="center",
                        color=col, weight="bold", clip_on=True,
                        bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.75) if l != 63 else None)
        it.next()
ax.set_xlim(b.left, b.right)
ax.set_ylim(b.bottom, b.top)
ax.set_aspect("equal")
ax.set_xlabel("um")
w = c.dbbox()
ax.set_title("%s  (cell %.2f x %.2f um)  NWell, ThickGateOx, pSD, Activ green, GatPoly red, Cont black, Metal1 blue, "
             "Via1 red, Metal2 violet" % (name, w.width(), w.height()), fontsize=8)
fig.tight_layout()
fig.savefig(png, dpi=110)
