"""Render a GDS cell (flattened) with matplotlib: device layers + metals, labels."""
import klayout.db as db, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
from matplotlib.collections import PatchCollection
STYLE = [  # (layer, dt, name, facecolor, alpha, edge)
    ((31,0),"NWell","#268c6b",0.15,None),
    ((44,0),"ThickGateOx","#c8c870",0.06,None),
    ((14,0),"pSD","#ccb899",0.10,None),
    ((1,0),"Activ","#00b000",0.35,None),
    ((5,0),"GatPoly","#bf4026",0.55,None),
    ((6,0),"Cont","#00aaaa",0.9,None),
    ((8,0),"Metal1","#2f8fdf",0.35,"#1060a0"),
    ((19,0),"Via1","#5050ff",0.9,None),
    ((10,0),"Metal2","#9a9ab0",0.40,"#505070"),
    ((29,0),"Via2","#ff3736",0.9,None),
    ((30,0),"Metal3","#d80000",0.30,"#800000"),
]
def polys(ly, cell, L):
    li = ly.find_layer(*L)
    if li is None: return []
    r = db.Region(cell.begin_shapes_rec(li)).merged()
    out = []
    for p in r.each():
        pts = [(q.x*ly.dbu, q.y*ly.dbu) for q in p.to_simple_polygon().each_point()]
        out.append(pts)
    return out
def texts(ly, cell, L):
    li = ly.find_layer(*L); out=[]
    if li is None: return out
    it = cell.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            t = s.text.transformed(it.trans()); out.append((t.string, t.x*ly.dbu, t.y*ly.dbu, it.cell().name))
        it.next()
    return out
def render(ly, cell, out, layers=None, title=None, labels=((8,25),(10,25),(30,25)), toplabels_only=False, dpi=200, size=None, notes=False, box=None):
    bb = cell.dbbox() if box is None else box
    w, h = bb.width(), bb.height()
    if size is None:
        s = 14.0/max(w,h); size=(max(4,w*s)+0.5, max(4,h*s)+0.8)
    fig, ax = plt.subplots(figsize=size)
    for L,name,fc,a,ec in STYLE:
        if layers and name not in layers: continue
        ps = polys(ly, cell, L)
        if not ps: continue
        pc = PatchCollection([MPoly(p, closed=True) for p in ps], facecolor=fc, alpha=a, edgecolor=ec or fc, linewidth=0.3)
        ax.add_collection(pc)
    for L in labels:
        for s,x,y,cn in texts(ly, cell, L):
            if toplabels_only and cn != cell.name: continue
            col = {8:"#0b3d91",10:"#202020",30:"#800000"}.get(L[0],"k")
            ax.text(x,y,s,fontsize=4 if not toplabels_only else 6,color=col,ha="center",va="center")
    if notes:
        for s,x,y,cn in texts(ly, cell, (63,0)):
            if cn in ("oa_pmir","oa_pcas","oa_nmir_r1","oa_nmir_r2","oa_mcs","oa_misc_n","oa_misc_p", cell.name):
                ax.text(x,y,s,fontsize=3,color="#806000",ha="left",va="bottom")
    ax.set_xlim(bb.left-0.5, bb.right+0.5); ax.set_ylim(bb.bottom-0.5, bb.top+0.5)
    ax.set_aspect("equal"); ax.set_xlabel("x (µm)"); ax.set_ylabel("y (µm)")
    ax.set_title(title or cell.name, fontsize=9)
    ax.grid(True, lw=0.2, alpha=0.4)
    fig.tight_layout(); fig.savefig(out, dpi=dpi); plt.close(fig)
if __name__ == "__main__":
    ly = db.Layout(); ly.read(sys.argv[1])
    for n in sys.argv[3:]:
        render(ly, ly.cell(n), "%s/%s.png" % (sys.argv[2], n), notes=True)
