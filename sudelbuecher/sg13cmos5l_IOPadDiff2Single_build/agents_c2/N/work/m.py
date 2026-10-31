import klayout.db as d,sys
l=d.Layout(); l.read('/home/user/c2/N/inputs/pad_buffer_klayout/pad_buffer_cells.gds')
print([c.name for c in l.each_cell() if 'nmosHV' in c.name or c.name.startswith('sinks') or c.name.startswith('d2s_')])
def dump(n, rec=False):
    c=l.cell(n); print('==',n,c.dbbox())
    for li in l.layer_indexes():
        i=l.get_info(li)
        it=c.begin_shapes_rec(li) if rec else None
        s=d.Region(c.begin_shapes_rec(li)) if True else None
        if s.is_empty(): continue
        print(i.layer,i.datatype,s.merged().count(), s.bbox().to_dtype(l.dbu) if s.count()<3 else '')
for n in sys.argv[1:]: dump(n)
