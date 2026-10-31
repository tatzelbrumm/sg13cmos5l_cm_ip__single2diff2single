import sys, klayout.db as db
ly=db.Layout(); ly.read(sys.argv[1]); u=ly.dbu
for name in sys.argv[2:]:
    c=ly.cell(name); R=lambda l,d=0: db.Region(c.begin_shapes_rec(ly.layer(l,d))).merged()
    act,psd,nw=R(1),R(14),R(31)
    pact=act&psd&nw; tie=(act-psd)&nw
    lo,hi=0.0,40.0
    while hi-lo>0.02:
        m=(lo+hi)/2
        if (pact-tie.sized(int(m/u),int(m/u),3)).is_empty(): hi=m
        else: lo=m
    print("%-16s farthest P+Activ to an N+ tie: %.2f um (LU.a 20)"%(name,hi))
