import sys, klayout.db as db
ly=db.Layout(); ly.read(sys.argv[1])
def tree(c, ind=0, maxd=3):
    b=c.dbbox()
    print("  "*ind+"%s [%.3f x %.3f] bbox %s"%(c.name,b.width(),b.height(),b))
    if ind>=maxd: return
    seen={}
    for i in c.each_inst():
        k=i.cell.name
        seen.setdefault(k,[]).append(i)
    for k,v in seen.items():
        for i in v[:6]:
            ia=i.cell_inst
            print("  "*(ind+1)+"inst %s trans %s %s"%(k, i.dcplx_trans, ("AREF na=%d nb=%d a=%s b=%s"%(ia.na,ia.nb,ia.a*ly.dbu,ia.b*ly.dbu)) if ia.is_regular_array() else ""))
        if len(v)>6: print("  "*(ind+1)+"... %d more"%(len(v)-6))
        tree(v[0].cell, ind+2, maxd)
for n in sys.argv[2:]:
    tree(ly.cell(n))
