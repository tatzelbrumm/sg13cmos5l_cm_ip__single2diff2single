# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""render_d2s_p.py <gds> <cell> <png> [x1 y1 x2 y2]: flat matplotlib picture of one cell with pin names and a scale bar."""
import sys
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP

LAYERS = [("nw", 31, 0, "#b7e4c7", 0.45, None), ("tgo", 44, 0, "#e9ecef", 0.0, "#adb5bd"), ("psd", 14, 0, "#ffd6a5", 0.35, None),
          ("act", 1, 0, "#2d6a4f", 0.7, None), ("poly", 5, 0, "#c1121f", 0.6, None), ("cont", 6, 0, "#000000", 0.9, None),
          ("m1", 8, 0, "#1d4ed8", 0.45, None), ("v1", 19, 0, "#ffffff", 1.0, "#000000"), ("m2", 10, 0, "#e11d8f", 0.45, None)]

gds, cell, png = sys.argv[1:4]
ly = db.Layout()
ly.read(gds)
c = ly.cell(cell)
bb = c.bbox()
box = [float(v) for v in sys.argv[4:8]] if len(sys.argv) > 7 else [bb.left * ly.dbu, bb.bottom * ly.dbu, bb.right * ly.dbu, bb.top * ly.dbu]
w, h = box[2] - box[0], box[3] - box[1]
fig_w = 11.0
fig, ax = plt.subplots(figsize=(fig_w, max(3.0, fig_w * h / w)), dpi=130)
for name, l, d, col, a, ec in LAYERS:
    r = db.Region(c.begin_shapes_rec(ly.layer(l, d))).merged()
    for p in r.each():
        pts = [(q.x * ly.dbu, q.y * ly.dbu) for q in p.each_point_hull()]
        ax.add_patch(MP(pts, closed=True, facecolor=col if a else "none", alpha=a if a else 1.0, edgecolor=ec or col, lw=0.4))
for lay, tag in ((8, "m1"), (10, "m2")):
    it = c.begin_shapes_rec(ly.layer(lay, 25))
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            t = s.text.transformed(it.trans())
            ax.text(t.x * ly.dbu, t.y * ly.dbu, t.string, fontsize=6, color="#111", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec=("#1d4ed8" if lay == 8 else "#e11d8f"), lw=0.5, alpha=0.8),
                    clip_on=True)
        it.next()
ax.set_xlim(box[0] - 0.3, box[2] + 0.3)
ax.set_ylim(box[1] - 0.3, box[3] + 0.3)
ax.set_aspect("equal")
ax.plot([box[0], box[0] + 5], [box[1] - 0.15, box[1] - 0.15], "k-", lw=2)
ax.text(box[0] + 2.5, box[1] - 0.15, "5 um", fontsize=6, ha="center", va="bottom", clip_on=True)
ax.set_title("%s  %.2f x %.2f um  (Activ green, poly red, M1 blue, M2 magenta, vias white, NWell light green)" % (
    cell, bb.width() * ly.dbu, bb.height() * ly.dbu), fontsize=7)
ax.tick_params(labelsize=6)
fig.tight_layout()
fig.savefig(png)
