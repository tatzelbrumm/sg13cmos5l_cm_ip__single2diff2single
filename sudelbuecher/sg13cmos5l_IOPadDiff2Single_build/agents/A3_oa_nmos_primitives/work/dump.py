import sys, klayout.db as db
ly=db.Layout(); ly.read(sys.argv[1])
def tree(c, ind=0, t=None):
    b=c.dbbox()
    print("  "*ind + "%s  bbox %.3f..%.3f x %.3f..%.3f (%.2f x %.2f)%s"%(c.name,b.left,b.right,b.bottom,b.top,b.width(),b.height(), "  @"+str(t) if t else ""))
    if ind>3: return
    for inst in c.each_inst():
        ca=inst.cell_inst
        s = str(inst.dcplx_trans)
        if ca.is_regular_array():
            s += " AREF %dx%d a=%s b=%s"%(ca.na,ca.nb,inst.da,inst.db)
        tree(inst.cell, ind+1, s)
for n in sys.argv[2:]:
    c=ly.cell(n)
    if c is None: print("NO", n); continue
    tree(c); print()
