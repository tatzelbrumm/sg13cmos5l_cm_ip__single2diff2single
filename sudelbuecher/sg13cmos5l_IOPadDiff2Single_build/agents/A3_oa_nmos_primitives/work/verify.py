"""checks beyond DRC/LVS: device cells vs library (XOR + texts), cell sizes, pins on edges, LU distances, layers"""
import sys, klayout.db as db
lib=db.Layout(); lib.read("../inputs/pad_buffer_cells.gds")
o=db.Layout(); o.read("../out/oa_n_cells.gds")
print("1. device cells vs library")
for n in ("nmosHV$7","nmosHV$8","nmosHV$9","nmosHV$5"):
    a,b=o.cell(n),lib.cell(n); bad=[]
    for li in set((i.layer,i.datatype) for i in o.layer_infos())|set((i.layer,i.datatype) for i in lib.layer_infos()):
        la,lb=o.find_layer(*li),lib.find_layer(*li)
        ra=db.Region(a.shapes(la)) if la is not None else db.Region(); rb=db.Region(b.shapes(lb)) if lb is not None else db.Region()
        ta=sorted((s.text_string,s.text.x,s.text.y) for s in (a.shapes(la).each() if la is not None else []) if s.is_text())
        tb=sorted((s.text_string,s.text.x,s.text.y) for s in (b.shapes(lb).each() if lb is not None else []) if s.is_text())
        if not (ra^rb).is_empty() or ta!=tb: bad.append(li)
    print("   %-10s XOR/text differences on layers: %s" % (n, bad or "none"))
print("   derived nmosHV_w2_l1: Activ %s poly %s" % (db.Region(o.cell("nmosHV_w2_l1").shapes(o.layer(1,0))).bbox().to_dtype(o.dbu), db.Region(o.cell("nmosHV_w2_l1").shapes(o.layer(5,0))).bbox().to_dtype(o.dbu)))
print("2. cells")
for cn in ("oa_n10","oa_mcs_c"):
    c=o.cell(cn); bb=c.dbbox()
    print("   %-9s bbox x %.3f..%.3f y %.3f..%.3f = %.3f x %.3f um = %.1f um2" % (cn,bb.left,bb.right,bb.bottom,bb.top,bb.width(),bb.height(),bb.width()*bb.height()))
    used=sorted("%d/%d"%(o.get_info(li).layer,o.get_info(li).datatype) for li in o.layer_indexes() if not db.Region(c.begin_shapes_rec(li)).is_empty() or any(True for _ in []))
    print("      layers with shapes:", " ".join(used))
    for pl,tl in (((8,2),(8,25)),((10,2),(10,25))):
        pi,ti=o.find_layer(*pl),o.find_layer(*tl)
        for s in c.shapes(ti).each():
            t=s.dtext; bx=[p.dbbox() for p in c.shapes(pi).each() if p.dbbox().contains(db.DPoint(t.x,t.y))]
            b=bx[0]
            e=[n for n,ok in (("left",b.left<=bb.left+1e-6),("right",b.right>=bb.right-1e-6),("bottom",b.bottom<=bb.bottom+1e-6),("top",b.top>=bb.top-1e-6)) if ok]
            print("      pin %-9s M%d  box (%.3f, %.3f; %.3f, %.3f)  edge: %s" % (t.string, 1 if pl[0]==8 else 2, b.left,b.bottom,b.right,b.top, ",".join(e) or "inside"))
    # LU: distance from every N+ Activ (not under pSD, minus poly) to the nearest p+ tie
    act=db.Region(c.begin_shapes_rec(o.layer(1,0))).merged(); psd=db.Region(c.begin_shapes_rec(o.layer(14,0))).merged()
    poly=db.Region(c.begin_shapes_rec(o.layer(5,0))).merged()
    tie=act&psd; nact=(act-psd)-poly
    worst=0; wpt=None
    for p in tie.each(): pass
    # sample N+ Activ corners
    for p in nact.each():
        for q in p.each_point_hull():
            d=min(db.Polygon(t).bbox().to_dtype(o.dbu).center().distance(db.DPoint(0,0)) for t in [p])  # dummy
    import math
    def dist(pt, box):
        dx=max(box.left-pt.x,0,pt.x-box.right); dy=max(box.bottom-pt.y,0,pt.y-box.top); return math.hypot(dx,dy)
    tboxes=[t.bbox().to_dtype(o.dbu) for t in tie.each()]
    for p in nact.each():
        for q in p.each_point_hull():
            dp=db.DPoint(q.x*o.dbu,q.y*o.dbu); d=min(dist(dp,b) for b in tboxes)
            if d>worst: worst,wpt=d,dp
    print("      tie segments: %s" % ["(%.3f, %.3f; %.3f, %.3f)"%(b.left,b.bottom,b.right,b.top) for b in tboxes])
    print("      farthest N+ Activ corner from a tie: %.3f um at %s (LU_b 20)" % (worst, wpt))
