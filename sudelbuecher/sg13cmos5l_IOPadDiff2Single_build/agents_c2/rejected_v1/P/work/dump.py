import klayout.db as db, sys
ly=db.Layout(); ly.read("/home/user/c2/P/inputs/pad_buffer_klayout/pad_buffer_cells.gds")
def tree(c,ind=0,seen=set()):
    inst=[(i.cell.name, i.trans.disp.x*ly.dbu,i.trans.disp.y*ly.dbu, i.trans.angle, i.trans.is_mirror(), i.is_regular_array() and (i.na,i.nb,i.a.x*ly.dbu,i.b.y*ly.dbu)) for i in c.each_inst()]
    b=c.bbox()
    print(" "*ind+c.name, "%.3f x %.3f"%(b.width()*ly.dbu,b.height()*ly.dbu), "bbox",[round(v*ly.dbu,3) for v in (b.left,b.bottom,b.right,b.top)])
for n in sys.argv[1:]:
    c=ly.cell(n); tree(c)
    for i in c.each_inst():
        print("   inst",i.cell.name,i.trans, (i.na,i.nb,i.a,i.b) if i.is_regular_array() else "")
    for li in ly.layer_indexes():
        info=ly.get_info(li); s=c.shapes(li)
        if s.size(): print("   ",info,s.size())
