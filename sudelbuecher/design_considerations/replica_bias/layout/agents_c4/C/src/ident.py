# byte-level identity of every reused cell (all layers, texts, instances) against its source GDS
import klayout.db as db
R='/home/user/sg13cmos5l_cm_ip__single2diff2single/macros/'
a=db.Layout(); a.read('out/s7_ctrl.gds')
def sig(ly,cell):
    s=[]
    for li in ly.layer_indexes():
        inf=ly.get_info(li)
        for sh in cell.shapes(li).each(): s.append('%d/%d %s'%(inf.layer,inf.datatype,sh))
    for i in cell.each_inst(): s.append('I %s %s'%(i.cell.name,i.cplx_trans))
    return sorted(s)
for src in ['bias_dist_pd/layout/klayout/bias_dist_pd.klay.gds','en_ctrl_3v3/layout/klayout/ls_up_fs.klay.gds']:
    b=db.Layout(); b.read(R+src)
    for c in a.each_cell():
        if c.name=='s7_ctrl': continue
        cb=b.cell(c.name)
        if cb is None: continue
        print('%-26s vs %s: %s' % (c.name, src.split('/')[-1], 'identical' if sig(a,c)==sig(b,cb) else 'DIFFERENT'))
