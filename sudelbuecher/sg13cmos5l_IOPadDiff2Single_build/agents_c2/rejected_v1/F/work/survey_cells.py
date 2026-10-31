import klayout.db as db, sys
ly=db.Layout(); ly.read(sys.argv[1])
names=sys.argv[2:]
for n in names:
    c=ly.cell(n)
    if c is None: print(n,"MISSING"); continue
    b=c.dbbox()
    print(f"== {n} bbox {b} ({b.width():.2f} x {b.height():.2f})")
    for li in ly.layer_indexes():
        info=ly.get_info(li)
        if info.datatype==25 or (info.layer==63):
            for s in c.each_shape(li):
                if s.is_text(): print("  ",info.layer,info.datatype,s.dtext.string, round(s.dtext.x,3), round(s.dtext.y,3))
    # pins boxes
    for li in ly.layer_indexes():
        info=ly.get_info(li)
        if info.datatype==2 and info.layer in (8,10):
            for s in c.each_shape(li):
                if s.is_box(): print("   pinbox",info.layer, s.dbox)
    for inst in c.each_inst():
        cc=ly.cell(inst.cell_index)
        print("   sub",cc.name,inst.dtrans, "na" if inst.size()==1 else inst.size())
