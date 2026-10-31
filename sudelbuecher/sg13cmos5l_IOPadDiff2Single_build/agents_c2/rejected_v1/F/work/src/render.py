# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Render a cell of a GDS (flattened) to PNG with matplotlib. Agent F, C2 2026-10-31.
  python3 render.py <gds> <cell> <out.png> [x0 y0 x1 y1] [--layers name,name,...] [--title text]"""
import sys

import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

STYLE = [  # name, (layer, dt), face, alpha, edge
    ("NWell", (31, 0), "#c8e6c9", 0.5, "#2e7d32"), ("TGO", (44, 0), "none", 1.0, "#9e9e9e"),
    ("pSD", (14, 0), "none", 1.0, "#e57373"), ("Activ", (1, 0), "#a5d6a7", 0.8, "#1b5e20"),
    ("PolyRes", (128, 0), "#ffe082", 0.9, "#ff8f00"), ("GatPoly", (5, 0), "#ef5350", 0.7, "#b71c1c"),
    ("Cont", (6, 0), "#000000", 1.0, "none"), ("M1", (8, 0), "#42a5f5", 0.45, "#0d47a1"),
    ("Via1", (19, 0), "#4a148c", 1.0, "none"), ("M2", (10, 0), "#ab47bc", 0.35, "#4a148c"),
    ("Via2", (29, 0), "#e65100", 1.0, "none"), ("M3", (30, 0), "#ffb74d", 0.25, "#e65100"),
]


def main(a):
    gds, cell, out = a[0], a[1], a[2]
    win, layers, title = None, None, cell
    rest = a[3:]
    if len(rest) >= 4 and not rest[0].startswith("--"):
        win = [float(v) for v in rest[:4]]
        rest = rest[4:]
    while rest:
        if rest[0] == "--layers":
            layers = rest[1].split(",")
        elif rest[0] == "--title":
            title = rest[1]
        rest = rest[2:]
    ly = db.Layout()
    ly.read(gds)
    c = ly.cell(cell)
    bb = c.dbbox()
    if win is None:
        win = [bb.left - 0.5, bb.bottom - 0.5, bb.right + 0.5, bb.top + 0.5]
    clip = db.Region(db.DBox(*win).to_itype(ly.dbu))
    w, h = win[2] - win[0], win[3] - win[1]
    sc = min(14 / w, 14 / h) if max(w, h) > 0 else 1
    fig, ax = plt.subplots(figsize=(max(4, w * sc + 1), max(4, h * sc + 1)))
    for name, ld, fc, al, ec in STYLE:
        if layers and name not in layers:
            continue
        li = ly.find_layer(*ld)
        if li is None:
            continue
        r = (db.Region(c.begin_shapes_rec(li)).merged() & clip).merged()
        for p in r.each():
            dp = p.to_dtype(ly.dbu)
            parts = [dp] if not dp.holes() else [sp.to_dtype(ly.dbu) for sp in p.decompose_trapezoids()]
            for q in parts:
                pts = [(v.x, v.y) for v in q.each_point()] if hasattr(q, "each_point") else \
                      [(v.x, v.y) for v in q.each_point_hull()]
                ax.add_patch(Polygon(pts, closed=True, fc=fc, alpha=al, ec=ec if not dp.holes() else "none", lw=0.4))
    # labels on pin text layers
    for ld in ((8, 25), (10, 25), (30, 25)):
        li = ly.find_layer(*ld)
        if li is None:
            continue
        it = c.begin_shapes_rec(li)
        while not it.at_end():
            s = it.shape()
            if s.is_text():
                t = s.dtext.transformed(it.dtrans())
                if win[0] <= t.x <= win[2] and win[1] <= t.y <= win[3]:
                    ax.text(t.x, t.y, t.string, fontsize=6, color="k", ha="center", va="center",
                            bbox=dict(fc="white", alpha=0.6, lw=0, pad=0.5))
            it.next()
    ax.set_xlim(win[0], win[2])
    ax.set_ylim(win[1], win[3])
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=9)
    ax.tick_params(labelsize=6)
    fig.tight_layout()
    fig.savefig(out, dpi=170)


if __name__ == "__main__":
    main(sys.argv[1:])
