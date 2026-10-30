"""Picture of the top-level (router) wires coloured by net over the instance outlines; scratch helper."""
import sys
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle
gds, cell, out = sys.argv[1], sys.argv[2], sys.argv[3]
box = [float(v) for v in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
ly = db.Layout(); ly.read(gds); top = ly.cell(cell)
# net of each top-level shape: flat connectivity M1-V1-M2 + all labels
fl = db.Layout(); fl.dbu = ly.dbu; c = fl.create_cell(cell); c.copy_tree(top); c.flatten(-1, True)
l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(fl, c, []))
m1 = l2n.make_layer(fl.find_layer(8, 0), "m1"); v1 = l2n.make_layer(fl.find_layer(19, 0), "v1"); m2 = l2n.make_layer(fl.find_layer(10, 0), "m2")
t1 = l2n.make_text_layer(fl.find_layer(8, 25), "t1"); t2 = l2n.make_text_layer(fl.find_layer(10, 25), "t2")
l2n.connect(m1); l2n.connect(m2); l2n.connect(m1, v1); l2n.connect(v1, m2); l2n.connect(m1, t1); l2n.connect(m2, t2)
l2n.extract_netlist()
cols = {}
pal = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#9a6324", "#808000", "#000075", "#e6a800", "#008080", "#800000"]
fig, ax = plt.subplots(figsize=(14, 15))
for inst in top.each_inst():
    b = inst.dbbox(); ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False, ls="--", lw=0.6, ec="k"))
    ax.text(b.left + 0.2, b.top - 0.6, inst.cell.name, fontsize=7)
for L, lay, lw in ((8, m1, 0.0), (10, m2, 0.0)):
    for s in top.shapes(ly.find_layer(L, 0)).each():
        if s.is_text(): continue
        p = s.polygon
        pt = p.bbox().center()
        if not p.inside(pt):
            pt = p.to_simple_polygon().each_point().__next__()
        net = l2n.probe_net(lay, db.DPoint(pt.x * ly.dbu, pt.y * ly.dbu))
        name = net.expanded_name() if net else "?"
        name = name.split(",")[0]
        if name not in cols: cols[name] = pal[len(cols) % len(pal)]
        pts = [(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()]
        ax.add_patch(MPoly(pts, closed=True, fc=cols[name], alpha=0.35 if L == 8 else 0.75, ec=cols[name], lw=0.3, hatch="////" if L == 8 else None))
for s in top.shapes(ly.find_layer(19, 0)).each():
    b = s.dbbox(); ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fc="k"))
for n, col in cols.items():
    ax.plot([], [], color=col, lw=6, label=n)
ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8)
bb = top.dbbox() if box is None else db.DBox(*box)
ax.set_xlim(bb.left, bb.right); ax.set_ylim(bb.bottom, bb.top); ax.set_aspect("equal"); ax.grid(True, lw=0.2)
ax.set_title("top-level wires by net (M1 hatched, M2 solid, vias black)")
fig.tight_layout(); fig.savefig(out, dpi=90)
