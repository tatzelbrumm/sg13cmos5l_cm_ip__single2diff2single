import klayout.db as db
ly=db.Layout(); ly.read("/foss/pdks/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds")
t=ly.cell("sg13cmos5l_IOPadAnalog")
print(t.dbbox())
for l,d in [(10,0),(10,2),(10,25),(8,25),(9,0)]:
    li=ly.find_layer(l,d)
    if li is None: continue
    r=db.Region(t.begin_shapes_rec(li)).merged() & db.Region(db.DBox(0,170,80,181).to_itype(ly.dbu))
    print((l,d),[p.bbox().to_dtype(ly.dbu) for p in r.each()][:20])
    it=t.begin_shapes_rec(li)
    while not it.at_end():
        s=it.shape()
        if s.is_text():
            tx=s.dtext.transformed(it.dtrans())
            print("  text",tx.string,tx.x,tx.y)
        it.next()
