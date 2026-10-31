import klayout.db as d,sys
l=d.Layout(); l.read('/home/user/c2/N/inputs/pad_buffer_klayout/pad_buffer_cells.gds')
for n in sys.argv[1:]:
    c=l.cell(n); print('==',n)
    for li in l.layer_indexes():
        i=l.get_info(li)
        for s in c.shapes(li).each():
            if s.is_text(): print(i.layer,i.datatype,'TEXT',s.text.string,s.text.x*l.dbu,s.text.y*l.dbu)
            else:
                b=s.bbox().to_dtype(l.dbu)
                if i.layer in (6,): 
                    continue
                print(i.layer,i.datatype,b)
        n6=c.shapes(l.layer(6,0)).size(); 
    print('contacts',n6)
