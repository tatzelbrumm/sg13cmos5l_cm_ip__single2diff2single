import klayout.db as d,sys
l=d.Layout(); l.read('/home/user/c2/N/inputs/pad_buffer_klayout/pad_buffer_cells.gds')
def tree(c,ind=0,t=None):
    print(' '*ind,c.name,c.dbbox(), 'shapes' ,sum(c.shapes(i).size() for i in l.layer_indexes()))
    for i in c.each_inst():
        ca=i.cell_inst
        print(' '*ind,'  inst',l.cell(ca.cell_index).name, ca.trans if hasattr(ca,'trans') else '', 'na',ca.na,'nb',ca.nb, ca.a, ca.b) if ind<4 else None
for n in sys.argv[1:]: tree(l.cell(n))
