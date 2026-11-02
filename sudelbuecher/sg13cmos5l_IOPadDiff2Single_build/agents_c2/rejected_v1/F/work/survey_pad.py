import klayout.db as db, sys
ly=db.Layout(); ly.read(sys.argv[1])
top=ly.top_cells()
print("tops",[c.name for c in top])
t=[c for c in top if c.name=='sg13cmos5l_IOPadDiff2Single'][0]
print("bbox",t.dbbox())
for inst in t.each_inst():
    c=ly.cell(inst.cell_index)
    print("inst",c.name, inst.dtrans, c.dbbox().transformed(inst.dcplx_trans))
# layers shapes in top in y>84
for li in ly.layer_indexes():
    info=ly.get_info(li)
    r=db.Region(t.begin_shapes_rec(li))
    r2=r & db.Region(db.Box(0,int(84/ly.dbu),int(80/ly.dbu),int(181/ly.dbu)))
    if not r2.is_empty():
        print(info, "above84 bbox", r2.bbox().to_dtype(ly.dbu), "n", r2.count())
# labels
for li in ly.layer_indexes():
    info=ly.get_info(li)
    for s in t.each_shape(li):
        if s.is_text() and s.dtext.y>80: print("text",info,s.dtext)
