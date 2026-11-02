# room left when cap_cma / cap_cmb are removed: free of devices (Activ/GatPoly/NWell + 0.62) and Metal1/Metal2 (+space)
import klayout.db as db, sys
ly=db.Layout(); ly.read(sys.argv[1]); t=ly.top_cell()
for n in ("cap_cma","cap_cmb"):
    c=ly.cell(n); print(n, "bbox", c.dbbox(), [ (ly.get_info(l).layer, ly.get_info(l).datatype) for l in ly.layer_indexes() if not c.bbox_per_layer(l).empty()])
    for inst in list(t.each_inst()):
        if inst.cell.name==n: print(" placed at", inst.dbbox()); inst.delete()
R=lambda l:db.Region(t.begin_shapes_rec(ly.layer(*l))).merged()
dev=(R((1,0))+R((5,0))+R((31,0))).merged()
used=(R((8,0)).sized(180)+R((10,0)).sized(210)+dev.sized(620)).merged()
win=db.Region(db.Box(-620,30000,80620,62000))
free=(db.Region(t.bbox())-used)&win
for s in (5,3):
    big=free.sized(-int(s*500)).sized(int(s*500))&free
    print(f">= {s} um pieces, y 30-62:", [(round(p.area()*1e-6),p.bbox().to_dtype(ly.dbu)) for p in sorted(big.each_merged(),key=lambda p:-p.area())[:6]])
fm=(db.Region(t.bbox())-(R((8,0)).sized(180)+R((10,0)).sized(210)).merged())&win
big=fm.sized(-2500).sized(2500)&fm
print("free of M1 and M2 only, >= 5 um, y 30-62:", [(round(p.area()*1e-6),p.bbox().to_dtype(ly.dbu)) for p in sorted(big.each_merged(),key=lambda p:-p.area())[:6]])
