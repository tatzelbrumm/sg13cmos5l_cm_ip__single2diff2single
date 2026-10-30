# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Pictures rendered from a GDS (matplotlib), 2026-10-28, Claude (Opus 5.5).

Process-free except for the layer map, which comes from the process adapter (P.layer(name)); net names of
unlabelled tracks come from an optional `namer` callback (e.g. an LVS cross reference supplied by the process
part). Functions:
  draw_cell(ax, ly, cell, P, trans=None, window=None, alpha=1.0)   layers in a fixed order
  finger_letters(ax, ly, cell, P, mapping, trans=None)             device names (note layer) -> letters / names
  track_names(ax, ly, cell, P, namer, trans=None)                  net name at the left end of each M2 shape
  pins(ax, ly, cell, P, trans=None)                                pin labels
  scale_bar(ax, x, y, length_um)
  outline(ax, box, label)                                          cell outline with dimensions
"""
import klayout.db as db
from matplotlib.patches import Polygon as MPoly, Rectangle
from matplotlib.collections import PatchCollection

STYLE = [  # (layer name, face, alpha, edge)
    ("thickox", "#d8d890", 0.18, "#a0a040"), ("pimp", "#e0b070", 0.35, None), ("well_n", "#268c6b", 0.12, None),
    ("active", "#30b030", 0.40, None), ("poly", "#c04020", 0.55, None), ("contact", "#005555", 0.90, None),
    ("metal1", "#3090e0", 0.40, "#1060a0"), ("via1", "#ff2020", 0.95, None), ("metal2", "#8080a0", 0.40, "#303050"),
]


def _region(ly, cell, P, name, trans=None, window=None):
    try:
        li = ly.find_layer(*P.layer(name))
    except KeyError:
        return db.Region()
    if li is None:
        return db.Region()
    r = db.Region(cell.begin_shapes_rec(li)).merged()
    if trans is not None:
        r = r.transformed(trans)
    if window is not None:
        r = r & db.Region(window.to_itype(ly.dbu))
    return r


def draw_cell(ax, ly, cell, P, trans=None, window=None, alpha=1.0, skip=()):
    d = ly.dbu
    for name, fc, a, ec in STYLE:
        if name in skip:
            continue
        r = _region(ly, cell, P, name, trans, window)
        ps = [MPoly([(q.x * d, q.y * d) for q in p.to_simple_polygon().each_point()], closed=True) for p in r.each()]
        if ps:
            ax.add_collection(PatchCollection(ps, facecolor=fc, alpha=a * alpha, edgecolor=ec or fc, linewidth=0.4))


def _texts(ly, cell, P, name, trans=None):
    li = ly.find_layer(*P.layer(name))
    out = []
    if li is None:
        return out
    it = cell.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            t = s.text.transformed(it.trans())
            if trans is not None:
                t = t.transformed(trans)
            out.append((t.string, t.x * ly.dbu, t.y * ly.dbu))
        it.next()
    return out


def finger_letters(ax, ly, cell, P, mapping, trans=None, window=None, size=9):
    """mapping: device name on the note layer -> label (e.g. {'M10': 'A'}); unknown names are skipped"""
    for s, x, y in _texts(ly, cell, P, "note", trans):
        if s in mapping and (window is None or window.contains(db.DPoint(x, y))):
            ax.text(x, y, mapping[s], ha="center", va="center", fontsize=size, weight="bold", color="#202020",
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))


def track_names(ax, ly, cell, P, namer, trans=None, window=None, size=7, min_len=1.5):
    """namer(point_um) -> net name of the Metal2 shape there; label at the left end of each horizontal M2 shape"""
    d = ly.dbu
    r = _region(ly, cell, P, "metal2", trans)
    for p in r.each():
        parts = [q.bbox().to_dtype(d) for q in p.decompose_trapezoids()]     # rectilinear -> rectangles
        b = max(parts, key=lambda q: q.width())                               # the widest one: the track
        if b.width() < min_len or b.height() > b.width():
            continue
        pt = db.DPoint(b.left + 0.15, b.center().y)
        if window is not None and not window.contains(pt):
            continue
        nm = namer(pt)
        ax.text(max(b.left, window.left if window else b.left) + 0.2, b.center().y, nm, fontsize=size, va="center",
                color="#300050", bbox=dict(boxstyle="round,pad=0.05", fc="white", ec="none", alpha=0.7))


def pins(ax, ly, cell, P, trans=None, size=8):
    for lay, col in (("metal1_label", "#0b3d91"), ("metal2_label", "#600060")):
        for s, x, y in _texts(ly, cell, P, lay, trans):
            ax.annotate(s, (x, y), fontsize=size, color=col, weight="bold", ha="center", va="bottom",
                        xytext=(0, 4), textcoords="offset points")


def scale_bar(ax, x, y, length, label=None):
    ax.plot([x, x + length], [y, y], color="k", lw=3, solid_capstyle="butt")
    ax.text(x + length / 2, y + 0.15, label or "%g um" % length, ha="center", va="bottom", fontsize=8)


def outline(ax, b, label, color="#aa00aa"):
    ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False, ec=color, lw=1.0, ls="--"))
    ax.text(b.left, b.top + 0.3, "%s  %.2f x %.2f um = %.0f um2" % (label, b.width(), b.height(), b.width() * b.height()),
            fontsize=9, color=color, va="bottom")
