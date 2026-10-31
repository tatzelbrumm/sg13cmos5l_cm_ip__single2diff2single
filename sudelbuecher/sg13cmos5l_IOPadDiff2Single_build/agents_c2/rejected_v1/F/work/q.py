import klayout.db as db, sys
ly=db.Layout(); ly.read("/home/user/c2/F/inputs/repo/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds")
t=ly.top_cell()
def reg(l,d=0):
    return db.Region(t.begin_shapes_rec(ly.layer(l,d))).merged()
def box(x1,y1,x2,y2): return db.Region(db.DBox(x1,y1,x2,y2).to_itype(ly.dbu))
for (name,l,w) in [("M2",10,(0,36,4.5,92)),("M2R",10,(75.5,36,80,92)),("M1",8,(0,36,4.5,92)),("M1R",8,(75.5,36,80,92)),("M2top",10,(0,84,80,92)),("M1top",8,(0,82,80,92)),("NW",31,(0,36,80,92)),("Activ",1,(0,82,80,92)),("pSD",14,(0,82,80,92))]:
    r=reg(l)&box(*w)
    print("==",name)
    for p in r.each():
        print("  ",p.bbox().to_dtype(ly.dbu), "" if p.is_box() else "poly")
print("== channel checks")
for w in [(1.0,12,3.2,86.4),(77.5,12,79.0,86.4),(3.7,82,77.0,86.4)]:
    for l in (10,8,19):
        r=reg(l)&box(*w)
        print(w,l,[p.bbox().to_dtype(ly.dbu) for p in r.each()][:12])
# NW at top of P frame
r=reg(31)&box(0,80,80,90); print("NW",[p.bbox().to_dtype(ly.dbu) for p in r.each()])
r=reg(44)&box(0,80,80,90); print("TGO",[p.bbox().to_dtype(ly.dbu) for p in r.each()])
