import klayout.db as db, sys
ly=db.Layout(); ly.read("/home/user/c2/F/inputs/repo/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds")
t=ly.top_cell()
win=[float(v) for v in sys.argv[1:5]]
layers=[(1,0),(31,0),(14,0),(44,0),(8,0),(10,0),(19,0),(6,0),(5,0)]
for l,d in layers:
    li=ly.find_layer(l,d)
    r=(db.Region(t.begin_shapes_rec(li)).merged() & db.Region(db.DBox(*win).to_itype(ly.dbu))).merged()
    if l==6 or l==19:
        print((l,d),"count",r.count(), r.bbox().to_dtype(ly.dbu)); continue
    print((l,d),[p.bbox().to_dtype(ly.dbu).__str__() + ("" if p.is_box() else "*") for p in r.each()])
