import sys, klayout.db as db, collections
ly=db.Layout(); ly.read(sys.argv[1]); c=ly.cell(sys.argv[2]); cnt=collections.Counter()
for li in ly.layer_indexes():
    for it in c.begin_shapes_rec(li).each():
        s=it.shape()
        if s.is_text() and s.text.string in ('vdd','vss','vddo','vsso'):
            t=s.text.transformed(it.trans()); cnt[(s.text.string, it.cell().name, round(t.y*ly.dbu))]+=1
for k,v in sorted(cnt.items()): print(k,v)
