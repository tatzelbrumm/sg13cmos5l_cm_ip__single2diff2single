"""quick render: python3 render.py gds cell out.png [x0 y0 x1 y1]"""
import sys, klayout.db as db, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as MP
ST = [((31,0),"#2e8b57",0.08,"#2e8b57"),((44,0),"#b8b860",0.0,"#8a8a30"),((14,0),"#d2b48c",0.15,None),
      ((1,0),"#22aa22",0.5,None),((5,0),"#c0392b",0.55,None),((6,0),"#111111",0.9,None),
      ((8,0),"#3a8fd9",0.35,"#1a5f99"),((19,0),"#ff2a2a",0.9,None),((10,0),"#8e7cc3",0.4,"#4b3c80")]
def main(gds, cell, out, win=None):
    ly=db.Layout(); ly.read(gds); c=ly.cell(cell); u=ly.dbu
    b=c.dbbox() if not win else db.DBox(*win)
    w,h=b.width(),b.height(); s=min(24/w, 16/h)*1.0
    fig,ax=plt.subplots(figsize=(max(4,w*s)+1,max(3,h*s)+1))
    for ld,fc,a,ec in ST:
        li=ly.find_layer(*ld)
        if li is None: continue
        r=db.Region(c.begin_shapes_rec(li)).merged()
        ps=[MP([(q.x*u,q.y*u) for q in p.to_simple_polygon().each_point()]) for p in r.each()]
        if ps: ax.add_collection(PatchCollection(ps,facecolor=fc,alpha=a,edgecolor=ec or fc,linewidth=0.6 if ec else 0))
    for ld,col in (((8,25),"#0b3d91"),((10,25),"#3b2a70"),((63,0),"#5a1a5a")):
        li=ly.find_layer(*ld)
        if li is None: continue
        it=c.begin_shapes_rec(li)
        while not it.at_end():
            sh=it.shape()
            if sh.is_text():
                p=it.dtrans()*sh.dtext.trans.disp
                if b.contains(p):
                    ax.text(p.x,p.y,sh.text_string,fontsize=7 if ld[0]!=63 else 6,color=col,weight="bold",ha="center",va="center",clip_on=True,
                        bbox=dict(boxstyle="round,pad=0.1",fc="white",ec="none",alpha=0.7) if ld[0]!=63 else None)
            it.next()
    ax.set_xlim(b.left,b.right); ax.set_ylim(b.bottom,b.top); ax.set_aspect("equal")
    ax.set_title("%s  %.2f x %.2f um  (Activ green, GatPoly red, Cont black, M1 blue, Via1 red, M2 violet, pSD tan, NWell green outline)"%(cell,c.dbbox().width(),c.dbbox().height()),fontsize=8)
    fig.tight_layout(); fig.savefig(out,dpi=110); plt.close(fig)
if __name__=="__main__":
    a=sys.argv[1:]; main(a[0],a[1],a[2],[float(v) for v in a[3:7]] if len(a)>3 else None)
