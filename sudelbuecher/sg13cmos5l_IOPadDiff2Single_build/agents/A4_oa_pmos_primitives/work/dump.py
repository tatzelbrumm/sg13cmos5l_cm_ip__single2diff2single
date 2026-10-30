import sys, klayout.db as db
ly=db.Layout(); ly.read(sys.argv[1])
own = "--rec" not in sys.argv
for n in [a for a in sys.argv[2:] if not a.startswith("--")]:
    c=ly.cell(n)
    print("=== cell", n, c.dbbox())
    for li in ly.layer_indexes():
        info=ly.get_info(li)
        it = c.shapes(li) if own else None
        shapes = list(c.shapes(li).each()) if own else None
        if own:
            if not shapes: continue
            txt=[s for s in shapes if s.is_text()]
            reg=db.Region([s.polygon for s in shapes if s.is_box() or s.is_polygon() or s.is_path()])
        else:
            reg=db.Region(c.begin_shapes_rec(li)).merged()
            txt=[]
            if reg.is_empty(): continue
        print(" layer %d/%d: %d polys"%(info.layer,info.datatype,reg.count()))
        for p in list(reg.each())[:60]:
            b=p.bbox().to_dtype(ly.dbu)
            print("    %s%s"%(b, "" if p.is_box() else " poly(%d pts)"%p.num_points()))
        for t in txt[:40]:
            print("    TEXT '%s' at %s size %s"%(t.text_string, t.dtext.trans, t.dtext.size))
