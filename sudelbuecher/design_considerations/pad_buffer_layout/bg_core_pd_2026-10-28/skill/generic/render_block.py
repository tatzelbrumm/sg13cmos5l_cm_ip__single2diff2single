# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""render_block.py: pictures of an assembled block from its GDS (process layers from the adapter), matplotlib.
Written 2026-10-28 by Claude (Opus 5.5).

    python3 render_block.py <adapter.py> <out.png> <gds>:<cell>[:<label>] [<gds>:<cell>[:<label>] ...] [// ...]
            [--scale um_per_inch] [--notes notes.json]
    '//' starts a new row of panels (all rows at the same scale; bg_core_pd 2026-10-28: before / after pairs).
    With the adapter's device_core() (resistor bodies, bipolars) those count as devices, not ties; rhigh bodies
    (adapter layer "polyres") are drawn brown.

One panel per block, all at the same scale (side by side): primitive outlines with their names, the wells
(merged outline), diffusion and poly faint, the block's own lower / upper metal and vias strong, tie stripes,
port pins with net names, outline dimensions, a 10 um scale bar. --notes: JSON list of
{"panel": i, "box": [x0, y0, x1, y1], "text": "...", "color": "..."} annotations (rule that drove a saving).
"""
import importlib.util
import json
import sys

import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                     # noqa: E402
from matplotlib.patches import Polygon as MPoly, Rectangle         # noqa: E402
from matplotlib.collections import PatchCollection                 # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = {sys.argv[i]: sys.argv[i + 1] for i in range(len(sys.argv) - 1) if sys.argv[i].startswith("--")}
spec = importlib.util.spec_from_file_location("adapter", args[0])
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
out = args[1]
panels, rows, row = [], [], 0
for a in args[2:]:
    if a == "//":
        row += 1
        continue
    parts = a.split(":")
    if len(parts) == 1 or a in opt.values():
        continue
    panels.append((parts[0], parts[1], parts[2] if len(parts) > 2 else parts[1]))
    rows.append(row)
notes = json.load(open(opt["--notes"])) if "--notes" in opt else []
scale = float(opt.get("--scale", "12"))          # um per inch


def polys(reg, dbu):
    """hole-free pieces (rings are polygons with holes: drawn as trapezoids)"""
    reg = reg.decompose_trapezoids_to_region()
    return [[(p.x * dbu, p.y * dbu) for p in poly.each_point_hull()] for poly in reg.each()]


def draw(ax, reg, dbu, fc, alpha, ec="none", lw=0.0, z=1):
    ps = [MPoly(p, closed=True) for p in polys(reg, dbu)]
    if ps:
        ax.add_collection(PatchCollection(ps, facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=z))


sizes = []
for gds, cell, label in panels:
    ly = db.Layout()
    ly.read(gds)
    sizes.append(ly.cell(cell).dbbox())
nrow = max(rows) + 1
rw = [sum(b.width() for b, r in zip(sizes, rows) if r == k) + 6.0 * (rows.count(k) - 1) for k in range(nrow)]
rh = [max(b.height() for b, r in zip(sizes, rows) if r == k) for k in range(nrow)]
W = max(rw) + 4.0
H = sum(rh) + 10.0 * nrow
fig = plt.figure(figsize=(W / scale, H / scale), dpi=150)
x_offs = [2.0] * nrow
y_base = [H - sum(rh[:k + 1]) - 10.0 * k - 7.0 for k in range(nrow)]
for pi, ((gds, cell, label), bb) in enumerate(zip(panels, sizes)):
    ly = db.Layout()
    ly.read(gds)
    top = ly.cell(cell)
    dbu = ly.dbu
    k = rows[pi]
    ax = fig.add_axes([x_offs[k] / W, y_base[k] / H, bb.width() / W, bb.height() / H])
    x_offs[k] += bb.width() + 6.0
    L = lambda k, own=False: (db.Region(top.shapes(ly.find_layer(*P.LAYERS[k]))) if own else
                              db.Region(top.begin_shapes_rec(ly.find_layer(*P.LAYERS[k])))).merged() \
        if ly.find_layer(*P.LAYERS[k]) is not None else db.Region()
    nw, tgo, diff, poly = L("nwell"), L("thickox"), L("diff"), L("poly")
    gate = diff & poly
    dev = diff.interacting(gate)
    pres = L("polyres") if "polyres" in P.LAYERS else db.Region()
    if hasattr(P, "device_core"):
        dev = diff & P.device_core(dict(diff=diff, poly=poly, pimp=L("pimp"), nwell=nw, polyres=pres, dbu=dbu))
    tie = diff - dev
    draw(ax, tgo, dbu, "#e8d9b0", 0.35, z=0)
    draw(ax, pres, dbu, "#a0522d", 0.6, z=3)
    draw(ax, nw, dbu, "#9ec9e8", 0.45, ec="#1f6fa8", lw=0.8, z=1)
    draw(ax, dev, dbu, "#5aa05a", 0.55, z=2)
    draw(ax, gate, dbu, "#c03030", 0.7, z=3)
    draw(ax, tie, dbu, "#ffcc00", 0.95, ec="#7a5c00", lw=0.4, z=4)
    draw(ax, L("m1"), dbu, "#3050c0", 0.12, z=5)
    draw(ax, L("m2"), dbu, "#c050c0", 0.10, z=5)
    draw(ax, L("m1", True), dbu, "#2040ff", 0.55, z=6)
    draw(ax, L("m2", True), dbu, "#d020d0", 0.45, z=7)
    draw(ax, L("via1", True), dbu, "#000000", 0.9, z=8)
    for inst in top.each_inst():
        b = inst.dbbox()
        ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False, ec="#222222", lw=0.9,
                               ls="--", zorder=9))
        ax.text(b.left + 0.3, b.top - 0.3, inst.cell.name, fontsize=6.5, va="top", ha="left", zorder=10,
                bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.6))
    for key in ("m1.text", "m2.text"):
        li = ly.find_layer(*P.LAYERS[key])
        if li is None:
            continue
        for s in top.shapes(li).each():
            if s.is_text():
                t = s.dtext
                ax.text(t.x, t.y, t.string, fontsize=6, color="#000000", ha="center", va="center", zorder=11,
                        bbox=dict(fc="#ffffe0", ec="#888800", lw=0.4, alpha=0.9, pad=0.5))
    for n in notes:
        if n.get("panel", 0) != pi:
            continue
        x0, y0, x1, y1 = n["box"]
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=n.get("color", "#d00000"), lw=1.4, zorder=12))
        ax.text(n.get("tx", x1 + 0.3), n.get("ty", y1), n["text"], fontsize=6.5, color=n.get("color", "#d00000"),
                ha=n.get("ha", "left"), va="top", zorder=12, bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.8))
    ax.set_xlim(bb.left, bb.right)
    ax.set_ylim(bb.bottom, bb.top)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=5)
    ax.add_patch(Rectangle((bb.left, bb.bottom), bb.width(), bb.height(), fill=False, ec="black", lw=1.2, zorder=12))
    ax.set_title("%s: %.2f x %.2f um = %.0f um2" % (label, bb.width(), bb.height(), bb.width() * bb.height()),
                 fontsize=8)
    ax.plot([bb.left + 1, bb.left + 11], [bb.bottom - 1.8, bb.bottom - 1.8], color="black", lw=2, clip_on=False)
    ax.text(bb.left + 6, bb.bottom - 2.3, "10 um", fontsize=6, ha="center", va="top")
fig.text(0.01, 0.01, "NWell blue (outline), ThickGateOx tan, device diffusion green, gates red, rhigh bodies brown, ties yellow, "
                     "block Metal1 blue / Metal2 magenta / Via1 black (primitives' metal faint), dashed = primitives",
         fontsize=6)
fig.savefig(out, dpi=150)
print("wrote", out)
