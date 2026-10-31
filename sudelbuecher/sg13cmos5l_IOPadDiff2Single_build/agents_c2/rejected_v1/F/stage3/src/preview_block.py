# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Preview of d2s_block in the pad context: pad top (y 80..180) + block, device layers and metals, instance outlines
with names. python3 preview_block.py <pad.gds> <block.gds> <out.png> <title>"""
import sys

import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

pad_gds, blk_gds, out, title = sys.argv[1:5]
ly = db.Layout()
ly.read(pad_gds)
top = ly.top_cell()
b = db.Layout()
b.read(blk_gds)
blk = ly.create_cell("d2s_block")
blk.copy_tree(b.cell("d2s_block"))
win = db.DBox(-1, 80, 81, 181)
clip = db.Region(win.to_itype(ly.dbu))
fig, ax = plt.subplots(figsize=(11, 13.5))
STY = [((31, 0), "#c8e6c9", 0.45), ((1, 0), "#81c784", 0.6), ((5, 0), "#e57373", 0.6), ((8, 0), "#64b5f6", 0.35),
       ((10, 0), "#ba68c8", 0.35), ((30, 0), "#ffcc80", 0.12)]
for cell in (top, blk):
    for (l, d), fc, al in STY:
        li = ly.find_layer(l, d)
        if li is None:
            continue
        r = (db.Region(cell.begin_shapes_rec(li)) & clip).merged()
        if (l, d) == (30, 0) and cell is blk:
            continue
        for p in r.each():
            for q in ([p] if not p.holes() else p.decompose_trapezoids()):
                pts = [(v.x * ly.dbu, v.y * ly.dbu) for v in (q.each_point_hull() if hasattr(q, "each_point_hull") else q.each_point())]
                ax.add_patch(Polygon(pts, closed=True, fc=fc, ec="none", alpha=al))
for inst in blk.each_inst():
    c = ly.cell(inst.cell_index)
    bb = c.dbbox().transformed(inst.dcplx_trans)
    ax.add_patch(Rectangle((bb.left, bb.bottom), bb.width(), bb.height(), fc="none", ec="k", lw=1.0))
    ax.text(bb.center().x, bb.center().y, (c.name[:-2] if c.name.endswith("_c") else c.name) + "\n%.2f x %.2f" % (bb.width(), bb.height()),
            ha="center", va="center", fontsize=7, bbox=dict(fc="white", alpha=0.75, lw=0))
for inst in top.each_inst():
    c = ly.cell(inst.cell_index)
    if c.name in ("cm_rings", "cma_ring", "nw_isolator", "edge_stubs", "gate_feeds", "replica_lines", "vfb_kelvin"):
        bb = c.dbbox().transformed(inst.dcplx_trans) & win
        if not bb.empty():
            ax.add_patch(Rectangle((bb.left, bb.bottom), bb.width(), bb.height(), fc="none", ec="#b45f06", lw=0.6, ls="--"))
for y0, y1, n in ((66, 91.5, "iovdd"), (93.5, 119, "iovdd"), (126, 134, "iovss"), (140, 158, "vss"), (160, 178, "vdd")):
    ax.text(80.8, (max(y0, 80) + y1) / 2, "M3 " + n, rotation=90, fontsize=7, va="center")
for spec in (sys.argv[5].split(";") if len(sys.argv) > 5 else []):
    x0, y0, x1, y1, lab = spec.split(",")
    x0, y0, x1, y1 = map(float, (x0, y0, x1, y1))
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec="#cc0000", lw=1.4, ls="--"))
    ax.text(x1, y1 + 0.3, lab, color="#cc0000", fontsize=7, ha="right", va="bottom")
ax.add_patch(Rectangle((0, 0), 80, 180, fc="none", ec="k", lw=1.2))
ax.set_xlim(win.left, win.right + 2)
ax.set_ylim(win.bottom, win.top)
ax.set_aspect("equal")
ax.set_title(title, fontsize=10)
fig.tight_layout()
fig.savefig(out, dpi=140)
