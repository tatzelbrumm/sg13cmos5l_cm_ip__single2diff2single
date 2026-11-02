import klayout.db as d,sys
l=d.Layout(); l.read('/home/user/c2/N/inputs/pad_buffer_klayout/pad_buffer_cells.gds')
for c in l.each_cell():
    if not c.name.startswith('nmosHV'): continue
    a=d.Region(c.shapes(l.layer(1,0))).bbox().to_dtype(l.dbu); p=d.Region(c.shapes(l.layer(5,0))).bbox().to_dtype(l.dbu)
    print(c.name,'bbox',c.dbbox(),'Activ',a,'W(h)',a.height(),'lact',a.width(),'poly',p, 'layers',[ (l.get_info(i).layer,l.get_info(i).datatype) for i in l.layer_indexes() if not c.shapes(i).is_empty()])
