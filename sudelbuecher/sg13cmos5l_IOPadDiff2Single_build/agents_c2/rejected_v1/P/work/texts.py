import klayout.db as db, sys
ly=db.Layout(); ly.read(sys.argv[1])
c=ly.cell(sys.argv[2])
for li in ly.layer_indexes():
    i=ly.get_info(li)
    if i.layer in (63,8,10) and i.datatype in (0,25):
        if i.datatype==0 and i.layer!=63: continue
        it=c.begin_shapes_rec(li)
        while not it.at_end():
            s=it.shape()
            if s.is_text():
                t=s.text.transformed(it.trans())
                print(i.layer,i.datatype,t.string.replace("\n"," | "),t.x*ly.dbu,t.y*ly.dbu)
            it.next()
