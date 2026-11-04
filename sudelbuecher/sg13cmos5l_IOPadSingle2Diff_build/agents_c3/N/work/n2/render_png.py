# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""render_png.py <gds> <cell> <png> [x0 y0 x1 y1]: the cell flattened, device layers + contacts + M1 / Via1 / M2,
pin labels (bold) and device names (grey), optionally a close-up window (um)."""
import sys
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                          # noqa: E402
from matplotlib.patches import Polygon                   # noqa: E402

gds, name, png = sys.argv[1:4]
win = [float(v) for v in sys.argv[4:8]] if len(sys.argv) >= 8 else None
ly = db.Layout()
ly.read(gds)
cell = ly.cell(name)
u = ly.dbu
# layer: (face, edge, alpha, z, fill)
STY = [((44, 0), "none", "#888888", 1.0, 1, False), ((14, 0), "none", "#e08000", 1.0, 2, False),
       ((128, 0), "#ffe680", "#d4a000", 0.9, 3, True), ((1, 0), "#7fc97f", "#2f8f2f", 0.75, 4, True),
       ((5, 0), "#e8443a", "#a01010", 0.6, 5, True), ((6, 0), "#000000", "#000000", 1.0, 8, True),
       ((8, 0), "#4a90e2", "#1f5fa8", 0.35, 6, True), ((10, 0), "#b05ad6", "#7a2aa0", 0.30, 7, True),
       ((19, 0), "#3b1060", "#3b1060", 0.9, 9, True)]
fig, ax = plt.subplots(figsize=(16, 16))
for ld, fc, ec, a, z, fill in STY:
    li = ly.find_layer(*ld)
    if li is None:
        continue
    r = db.Region(cell.begin_shapes_rec(li)).merged()
    if win:
        r = r & db.Region(db.DBox(*win).to_itype(u))
    for p in r.each():
        pts = [(q.x * u, q.y * u) for q in p.to_simple_polygon().each_point()]
        ax.add_patch(Polygon(pts, closed=True, facecolor=fc if fill else "none", edgecolor=ec, alpha=a, zorder=z,
                             lw=0.6 if fill else 1.2, ls="-" if ld != (44, 0) else "--"))
bb = cell.dbbox() if not win else db.DBox(*win)
for ld, col, wt, size in (((8, 25), "#0b3d91", "bold", 9), ((10, 25), "#5a0a7a", "bold", 9), ((63, 0), "#555555", "normal", 7)):
    li = ly.find_layer(*ld)
    if li is None:
        continue
    it = cell.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            t = s.text.transformed(it.trans())
            x, y = t.x * u, t.y * u
            if bb.contains(db.DPoint(x, y)) and t.string not in ("nmosHV", "rhigh", "sub!") and not t.string.startswith("rhigh"):
                ax.text(x, y, t.string, color=col, fontsize=size, fontweight=wt, ha="center", va="center", zorder=12)
        it.next()
ax.set_xlim(bb.left - 0.3, bb.right + 0.3)
ax.set_ylim(bb.bottom - 0.3, bb.top + 0.3)
ax.set_aspect("equal")
ax.set_xlabel("um")
cb = cell.dbbox()
ax.set_title("%s%s  (cell %.2f x %.2f um)  Activ green, GatPoly red, Cont black, M1 blue, Via1 dark, M2 violet, "
             "pSD orange, ThickGateOx dashed" % (name, "  close-up" if win else "", cb.width(), cb.height()), fontsize=9)
w, h = bb.width(), bb.height()
fig.set_size_inches(16, max(4.0, min(16.0, 16 * h / w + 1.2)))
fig.tight_layout()
fig.savefig(png, dpi=110)
