import sys, klayout.db as db
lvsdb, gds = sys.argv[1:3]
TOP='sg13cmos5l_IOPadSingle2Diff'
l=db.LayoutVsSchematic(); l.read(lvsdb)
pair=next(p for p in l.xref().each_circuit_pair() if p.first() and p.first().name==TOP)
G=db.Layout(); G.read(gds); gt=G.cell(TOP); u=G.dbu
blk=G.cell('s2d_block'); bt=[i.cplx_trans for i in gt.each_inst() if i.cell.name=='s2d_block'][0]
# tracks in pad coords: inputs at block (4.3,96.4) => pad (4.3,122.4)
tr={n: db.DBox(4.3,122.4+y0,51.88,122.4+y0+0.26) for n,y0 in [('t12.35',12.35),('t12.83',12.83),('t13.31',13.31),('t13.79',13.79),('t14.27',14.27)]}
tr['t11.87']=db.DBox(4.3,122.4+11.87,51.88,122.4+12.13)
for np_ in l.xref().each_net_pair(pair):
    n=np_.first()
    if not n: continue
    nm=np_.second().name if np_.second() else n.expanded_name()
    for ln in ['metal2','via1','metal1','via2','metal3','Metal2','Via1']:
        try: li=l.layer_by_name(ln)
        except Exception: continue
        if li is None: continue
        r=l.shapes_of_net(n,li,True)
        for t,b in tr.items():
            rr=r & db.Region(b.to_itype(u))
            if not rr.is_empty() and ln.lower()!='metal2':
                print(nm, t, ln, [str(p.bbox().to_dtype(u)) for p in rr.each()][:6])
            elif not rr.is_empty(): print(nm,t,ln,'area',round(rr.area()*u*u,2))
