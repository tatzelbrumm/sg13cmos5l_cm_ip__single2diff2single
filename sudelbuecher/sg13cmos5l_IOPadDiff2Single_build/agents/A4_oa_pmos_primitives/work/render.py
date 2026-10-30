"""render.py <gds> <cell> <out.png> [title] : device layers + M1/Via1/M2, labels (8/25, 10/25, 63/0)"""
import sys, klayout.db as db
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle
from matplotlib.collections import PatchCollection
gds, cn, out = sys.argv[1:4]
title = sys.argv[4] if len(sys.argv) > 4 else cn
ly = db.Layout(); ly.read(gds); top = ly.cell(cn); bb = top.dbbox()
def polys(L):
    li = ly.find_layer(*L)
    if li is None: return []
    r = db.Region(top.begin_shapes_rec(li)).merged()
    return [[(q.x*ly.dbu, q.y*ly.dbu) for q in p.to_simple_polygon().each_point()] for p in r.each()]
def draw(ax, ps, fc, a, ec=None, lw=0.3, hatch=None):
    if ps:
        ax.add_collection(PatchCollection([MPoly(p, closed=True) for p in ps], facecolor=fc, alpha=a,
                                          edgecolor=ec or fc, linewidth=lw, hatch=hatch))
w, h = bb.width(), bb.height()
sc = 0.42
fig, ax = plt.subplots(figsize=(max(5, w*sc+2), max(4, h*sc+1.5)))
for L, fc, a, ec in (((31, 0), "#268c6b", 0.12, "#268c6b"), ((44, 0), "#c8c870", 0.10, "#a0a040"), ((14, 0), "#ccb899", 0.12, None),
                     ((1, 0), "#00b000", 0.40, None), ((5, 0), "#bf4026", 0.55, None), ((6, 0), "#003030", 0.9, None),
                     ((8, 0), "#2f8fdf", 0.35, "#1060a0"), ((19, 0), "#ff3030", 0.9, None), ((10, 0), "#9a9ab0", 0.40, "#505070")):
    draw(ax, polys(L), fc, a, ec)
for L, col, fs in (((8, 25), "#0b3d91", 7), ((10, 25), "#303030", 7), ((63, 0), "#aa00aa", 5)):
    li = ly.find_layer(*L)
    if li is None: continue
    for it in top.begin_shapes_rec(li).each():
        s = it.shape()
        if s.is_text():
            t = s.dtext.transformed(it.dtrans())
            ax.text(t.x, t.y, t.string, fontsize=fs, color=col, ha="center", va="center", rotation=0,
                    weight="bold" if L[1] == 25 else "normal")
ax.set_xlim(bb.left-0.5, bb.right+0.5); ax.set_ylim(bb.bottom-0.5, bb.top+0.5)
ax.set_aspect("equal"); ax.grid(True, lw=0.2, alpha=0.4)
ax.set_xlabel("x (um)"); ax.set_ylabel("y (um)")
ax.set_title("%s   %.2f x %.2f um" % (title, w, h), fontsize=10)
ax.add_patch(Rectangle((bb.left, bb.bottom), w, h, fill=False, ec="k", lw=0.6))
fig.tight_layout(); fig.savefig(out, dpi=110); plt.close(fig)
print("wrote", out)
