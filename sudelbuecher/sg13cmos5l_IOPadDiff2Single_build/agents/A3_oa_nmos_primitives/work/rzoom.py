"""python3 rzoom.py gds cell out.png x0 x1 y0 y1 scale"""
import sys, klayout.db as db, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
from matplotlib.collections import PatchCollection
ly=db.Layout(); ly.read(sys.argv[1]); top=ly.cell(sys.argv[2])
x0,x1,y0,y1,sc=map(float,sys.argv[4:9])
win=db.DBox(x0,y0,x1,y1)
def polys(L):
    li=ly.find_layer(*L)
    if li is None: return []
    r=(db.Region(top.begin_shapes_rec(li)).merged()) & db.Region(win.to_itype(ly.dbu))
    return [[(q.x*ly.dbu,q.y*ly.dbu) for q in p.to_simple_polygon().each_point()] for p in r.each()]
fig,ax=plt.subplots(figsize=((x1-x0)*sc,(y1-y0)*sc))
for L,fc,a,ec in (((44,0),"#c8c870",0.15,"#888800"),((14,0),"#ccb899",0.25,None),((1,0),"#00b000",0.35,None),((5,0),"#bf4026",0.5,None),((6,0),"#006666",0.9,None),((8,0),"#2f8fdf",0.35,"#1060a0"),((19,0),"#ff3030",0.9,None),((10,0),"#9a9ab0",0.35,"#303050")):
    ps=polys(L)
    if ps: ax.add_collection(PatchCollection([MPoly(p,closed=True) for p in ps],facecolor=fc,alpha=a,edgecolor=ec or fc,linewidth=0.5))
for L,col in (((8,25),"#0b3d91"),((10,25),"#600060"),((63,0),"#333333")):
    li=ly.find_layer(*L)
    if li is None: continue
    it=top.begin_shapes_rec(li)
    while not it.at_end():
        s=it.shape()
        if s.is_text():
            t=s.text.transformed(it.trans()); X,Y=t.x*ly.dbu,t.y*ly.dbu
            if x0<=X<=x1 and y0<=Y<=y1: ax.text(X,Y,t.string,fontsize=8,color=col)
        it.next()
ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); ax.set_aspect("equal"); ax.grid(True,lw=0.2)
fig.tight_layout(); fig.savefig(sys.argv[3],dpi=100)
