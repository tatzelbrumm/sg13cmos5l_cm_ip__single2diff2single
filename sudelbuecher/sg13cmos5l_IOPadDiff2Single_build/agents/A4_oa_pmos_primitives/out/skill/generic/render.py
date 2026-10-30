# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""render.py: draw generated cells from GDS with matplotlib (layers from the process adapter), 2026-10-28, Claude.

    python3 render.py <gds> <cell> <out.png> <adapter.py> [title]

draw(ax, ly, cell, P, dx, dy) draws one cell (all layers, the finger tags of the 'text' layer as large letters,
pins); scalebar(ax, x, y, um); dims(ax, bbox) writes the outline size. make_pictures.py uses them.
"""
import os
import sys
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
from matplotlib.collections import PatchCollection                    # noqa: E402
from matplotlib.patches import Polygon as MPoly, Rectangle            # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generator import load_adapter                                    # noqa: E402
STYLE = [("well", "#2e8b57", 0.10, "#2e8b57", 0.8), ("hvox", "#b8b860", 0.00, "#8a8a30", 0.5),
         ("pimp", "#d2b48c", 0.12, None, 0.0), ("diff", "#22aa22", 0.45, None, 0.0), ("poly", "#c0392b", 0.55, None, 0.0),
         ("contact", "#202020", 0.9, None, 0.0), ("m1", "#3a8fd9", 0.35, "#1a5f99", 0.3),
         ("via1", "#ff2a2a", 0.95, None, 0.0), ("m2", "#8e7cc3", 0.40, "#4b3c80", 0.3)]


def polys(ly, cell, P, k, trans=None):
    li = ly.find_layer(*P.layer(k))
    if li is None:
        return []
    r = db.Region(cell.begin_shapes_rec(li)).merged()
    if trans is not None:
        r = r.transformed(trans)
    return [[(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()] for p in r.each()]


def draw(ax, ly, cell, P, dx=0.0, dy=0.0, letters=True, fs=None, pins=True, short=None, skip=()):
    t = db.Trans(db.Vector(int(round(dx / ly.dbu)), int(round(dy / ly.dbu))))
    for k, fc, a, ec, lw in STYLE:
        ps = polys(ly, cell, P, k, t)
        if ps:
            ax.add_collection(PatchCollection([MPoly(p, closed=True) for p in ps], facecolor=fc, alpha=a,
                                              edgecolor=ec or fc, linewidth=lw))
    if letters:
        li = ly.find_layer(*P.layer("text"))
        for it in cell.begin_shapes_rec(li).each():
            s = it.shape()
            if s.is_text() and s.text_string not in skip:
                p = it.dtrans() * s.dtext.trans.disp
                lab = (short or {}).get(s.text_string, s.text_string)
                ax.text(p.x + dx, p.y + dy, lab, ha="center", va="center", fontsize=fs or 7, color="#5a1a5a",
                        weight="bold", clip_on=True)
    if pins:
        for m, col in (("m1_text", "#0b3d91"), ("m2_text", "#3b2a70")):
            li = ly.find_layer(*P.layer(m))
            if li is None:
                continue
            for s in cell.shapes(li).each():
                if s.is_text():
                    p = s.dtext.trans.disp
                    ax.plot(p.x + dx, p.y + dy, marker="s", ms=3, color=col, clip_on=True)
                    ax.text(p.x + dx + 0.25, p.y + dy, s.text_string, fontsize=7, color=col, weight="bold",
                            va="center", ha="left", clip_on=True,
                            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.8))
    b = cell.dbbox()
    return db.DBox(b.left + dx, b.bottom + dy, b.right + dx, b.top + dy)


def dims(ax, b, text_extra="", fs=8):
    ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False, ec="k", lw=0.8, ls="--"))
    ax.text((b.left + b.right) / 2, b.top + 0.6, "%.2f x %.2f um = %.0f um2%s" % (b.width(), b.height(),
            b.width() * b.height(), text_extra), ha="center", va="bottom", fontsize=fs, weight="bold")


def mark(ax, x, y, n, col="#c0392b"):
    """numbered callout at (x, y)"""
    ax.text(x, y, str(n), fontsize=9, color="white", weight="bold", ha="center", va="center", zorder=10,
            bbox=dict(boxstyle="circle,pad=0.2", fc=col, ec="white", lw=0.8))


def scalebar(ax, x, y, um=5.0):
    ax.plot([x, x + um], [y, y], color="k", lw=3)
    ax.text(x + um / 2, y - 0.4, "%g um" % um, ha="center", va="top", fontsize=8)


if __name__ == "__main__":
    gds, cn, out = sys.argv[1:4]
    P = load_adapter(sys.argv[4])
    ly = db.Layout()
    ly.read(gds)
    c = ly.cell(cn)
    b = c.dbbox()
    sc = 0.45
    fig, ax = plt.subplots(figsize=(max(4, b.width() * sc + 1.5), max(4, b.height() * sc + 1.5)))
    bb = draw(ax, ly, c, P)
    dims(ax, bb)
    scalebar(ax, b.left, b.bottom - 1.0, 2.0 if b.width() < 8 else 5.0)
    ax.set_xlim(b.left - 1.5, b.right + 3.0)
    ax.set_ylim(b.bottom - 2.0, b.top + 2.0)
    ax.set_aspect("equal")
    ax.set_title(sys.argv[5] if len(sys.argv) > 5 else cn, fontsize=10)
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")
    ax.grid(True, lw=0.2, alpha=0.4)
    fig.tight_layout()
    fig.savefig(out, dpi=110)
    print("wrote", out)
