"""render one cell: python3 rcell.py gds cell out.png [xmin xmax ymin ymax]"""
import sys, klayout.db as db, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
from matplotlib.collections import PatchCollection
ly=db.Layout(); ly.read(sys.argv[1]); top=ly.cell(sys.argv[2]); bb=top.dbbox()
def polys(L):
    li=ly.find_layer(*L)
    if li is None: return []
    r=db.Region(top.begin_shapes_rec(li)).merged()
    return [[(q.x*ly.dbu,q.y*ly.dbu) for q in p.to_simple_polygon().each_point()] for p in r.each()]
w=bb.width(); h=bb.height()
sc=float(sys.argv[5]) if len(sys.argv)>5 else 0.45
fig,ax=plt.subplots(figsize=(max(6,w*sc),max(4,h*sc)))
for L,fc,a,ec in (((31,0),"#268c6b",0.13,None),((44,0),"#c8c870",0.08,None),((14,0),"#ccb899",0.15,None),((1,0),"#00b000",0.35,None),((5,0),"#bf4026",0.55,None),((6,0),"#00aaaa",0.9,None),((8,0),"#2f8fdf",0.35,"#1060a0"),((19,0),"#ff3030",0.9,None),((10,0),"#9a9ab0",0.45,"#505070")):
    ps=polys(L)
    if ps: ax.add_collection(PatchCollection([MPoly(p,closed=True) for p in ps],facecolor=fc,alpha=a,edgecolor=ec or fc,linewidth=0.3))
it=top.begin_shapes_rec(ly.find_layer(8,25)) if ly.find_layer(8,25) is not None else None
for L,col in (((8,25),"#0b3d91"),((10,25),"#600060"),((63,0),"#555555")):
    li=ly.find_layer(*L)
    if li is None: continue
    it=top.begin_shapes_rec(li)
    while not it.at_end():
        s=it.shape()
        if s.is_text():
            t=s.text.transformed(it.trans()); 
            ax.text(t.x*ly.dbu,t.y*ly.dbu,t.string,fontsize=6 if L!=(63,0) else 4,color=col)
        it.next()
ax.set_xlim(bb.left-0.5,bb.right+0.5); ax.set_ylim(bb.bottom-0.5,bb.top+0.5); ax.set_aspect("equal")
ax.set_title("%s %.2f x %.2f"%(top.name,w,h)); ax.grid(True,lw=0.2)
fig.tight_layout(); fig.savefig(sys.argv[3],dpi=110)
