import klayout.db as db, sys
ly=db.Layout(); ly.read(sys.argv[1])
c=ly.cell(sys.argv[2])
want=set(sys.argv[3].split(',')) if len(sys.argv)>3 else None
for li in ly.layer_indexes():
    i=ly.get_info(li); k="%d/%d"%(i.layer,i.datatype)
    if want and k not in want: continue
    r=db.Region(c.begin_shapes_rec(li))
    if r.is_empty(): continue
    print(k, "n=",r.count())
    for p in list(r.merged().each())[:40]:
        b=p.bbox(); print("   ",[round(v*ly.dbu,3) for v in (b.left,b.bottom,b.right,b.top)], "pts",p.num_points())
