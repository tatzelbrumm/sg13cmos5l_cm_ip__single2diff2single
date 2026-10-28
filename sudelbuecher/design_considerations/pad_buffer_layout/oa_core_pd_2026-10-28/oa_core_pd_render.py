# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Renders of oa_core_pd.gds with matplotlib (2026-10-28, Claude):
  oa_core_pd.png     device layers + M1 / Via1 / M2, primitive outlines and names, ports
  oa_core_pd_m1.png  Metal1: primitives' M1 faint, top-level M1 strong with net names
  oa_core_pd_m2.png  Metal2 + Via1 likewise
Net names of the top-level wiring come from the LVS cross reference (oa_core_pd_lvs.py).
    python3 oa_core_pd_render.py oa_core_pd.gds oa_core_pd.cdl
"""
import sys
import os
import importlib.util
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle
from matplotlib.collections import PatchCollection

gds, cdl = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("lvs", os.path.join(here, "oa_core_pd_lvs.py"))
lvsm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lvsm)

ly = db.Layout()
ly.read(gds)
top = ly.cell("oa_core_pd")
bb = top.dbbox()

# net names of top-level shapes: flat extraction, cross reference to the reference netlist
lvs, fly, _ = lvsm.extract(gds, "oa_core_pd", "top")
c = lvs.netlist().circuit_by_name("oa_core_pd")
ref = db.Netlist()
ref.read(cdl, db.NetlistSpiceReader())
ref.combine_devices()
rc = ref.circuit_by_name("oa_core_pd")
rc.name = "oa_core_pd"
lvs.netlist().case_sensitive = False
for p in rc.each_pin():
    pin = c.create_pin(p.name())
    n = c.net_by_name(p.name())
    if n is not None:
        c.connect_pin(pin, n)
lvs.reference = ref
lvs.compare(db.NetlistComparer())
name = {}
for cp in lvs.xref().each_circuit_pair():
    for np_ in lvs.xref().each_net_pair(cp):
        if np_.first() is not None and np_.second() is not None:
            name[np_.first().cluster_id] = np_.second().expanded_name().lower()
lay_of = {(8, 0): "m1", (10, 0): "m2"}
lvs_layers = {"m1": lvs.layer_by_name("m1"), "m2": lvs.layer_by_name("m2")}


def net_at(L, pt):
    n = lvs.probe_net(lvs_layers[lay_of[L]], pt)
    return name.get(n.cluster_id, "?") if n else "?"


def polys(cell, L, own=False):
    li = ly.find_layer(*L)
    if li is None:
        return []
    r = (db.Region(cell.shapes(li)) if own else db.Region(cell.begin_shapes_rec(li))).merged()
    return [[(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()] for p in r.each()]


def draw(ax, ps, fc, a, ec=None, lw=0.3):
    if ps:
        ax.add_collection(PatchCollection([MPoly(p, closed=True) for p in ps], facecolor=fc, alpha=a,
                                          edgecolor=ec or fc, linewidth=lw))


def frame(ax, title):
    ax.set_xlim(bb.left - 1, bb.right + 1)
    ax.set_ylim(bb.bottom - 1, bb.top + 1.5)
    ax.set_aspect("equal")
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")
    ax.set_title(title, fontsize=11)
    ax.grid(True, lw=0.2, alpha=0.4)
    ax.add_patch(Rectangle((bb.left, bb.bottom), bb.width(), bb.height(), fill=False, ec="k", lw=0.8))


def ports(ax):
    for L, col in (((8, 25), "#0b3d91"), ((10, 25), "#303030")):
        li = ly.find_layer(*L)
        for s in top.shapes(li).each():
            t = s.dtext
            ax.annotate(t.string, (t.x, t.y), xytext=(t.x + (1.5 if t.x > bb.right - 1 else 0), t.y + (1.0 if t.y > bb.top - 1 else 0)),
                        fontsize=9, color=col, weight="bold", ha="left" if t.x > bb.right - 1 else "center")


def outlines(ax):
    for inst in top.each_inst():
        n = inst.cell.name
        b = inst.dbbox()
        if n == "oa_pmir_image_jumpers":
            continue
        ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False, ec="#aa00aa", lw=0.8, ls="--"))
        o = {"oa_pmir": "M0", "oa_pcas": "M0", "oa_misc_p": "R180"}.get(n, "R0")
        ax.text(b.left + 0.3, b.top - 0.3, "%s (%s)" % (n, o), fontsize=7.5, color="#aa00aa", va="top")


# 1. whole cell
fig, ax = plt.subplots(figsize=(16, 11.5))
for L, fc, a, ec in (((31, 0), "#268c6b", 0.13, None), ((44, 0), "#c8c870", 0.06, None), ((14, 0), "#ccb899", 0.10, None),
                     ((1, 0), "#00b000", 0.35, None), ((5, 0), "#bf4026", 0.55, None), ((6, 0), "#00aaaa", 0.9, None),
                     ((8, 0), "#2f8fdf", 0.35, "#1060a0"), ((19, 0), "#5050ff", 0.9, None), ((10, 0), "#9a9ab0", 0.45, "#505070")):
    draw(ax, polys(top, L), fc, a, ec)
outlines(ax)
ports(ax)
frame(ax, "oa_core_pd  %.2f x %.2f um = %.0f um2   (NWell, TGO, pSD, Activ, GatPoly, Cont, Metal1, Via1, Metal2)"
      % (bb.width(), bb.height(), bb.width() * bb.height()))
fig.tight_layout()
fig.savefig("oa_core_pd.png", dpi=150)
plt.close(fig)


# 2. per metal level
def metal(L, fn, title, col, via=False):
    fig, ax = plt.subplots(figsize=(16, 11.5))
    draw(ax, polys(top, (31, 0)), "#268c6b", 0.06)
    draw(ax, polys(top, (1, 0)), "#00b000", 0.10)
    draw(ax, polys(top, (5, 0)), "#bf4026", 0.12)
    cells = db.Region()
    li = ly.find_layer(*L)
    for inst in top.each_inst():
        cells += db.Region(inst.cell.begin_shapes_rec(li)).transformed(inst.trans)
    own = db.Region(top.shapes(li)).merged()
    draw(ax, [[(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()] for p in cells.merged().each()],
         "#888888", 0.30)
    draw(ax, [[(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()] for p in own.each()],
         col, 0.85, "k", 0.4)
    if via:
        draw(ax, polys(top, (19, 0)), "#ff3030", 0.95)
    seen = set()
    for sh in top.shapes(li).each():                 # every top-level shape is a box: its centre is on it
        b = sh.dbbox()
        if max(b.width(), b.height()) < 2.0 or b.height() > 1.0 and b.width() > 1.0:
            continue                                  # skip vias / pads and the rails / straps
        nm = net_at(L, b.center())
        key = (nm, round(b.center().x / 4), round(b.center().y / 4))
        if key in seen:
            continue
        seen.add(key)
        rot = 90 if b.height() > b.width() else 0
        ax.text(b.center().x, b.center().y, nm, fontsize=7, rotation=rot, ha="center", va="center", color="k",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.75))
    outlines(ax)
    ports(ax)
    frame(ax, title)
    fig.tight_layout()
    fig.savefig(fn, dpi=150)
    plt.close(fig)


metal((8, 0), "oa_core_pd_m1.png", "oa_core_pd Metal1: top-level M1 (blue, net names) over the primitives' M1 (grey)", "#2f8fdf")
metal((10, 0), "oa_core_pd_m2.png", "oa_core_pd Metal2 + Via1 (red): top-level M2 (dark, net names) over the primitives' M2 (grey)",
      "#6a5acd", via=True)
print("wrote oa_core_pd.png oa_core_pd_m1.png oa_core_pd_m2.png")
