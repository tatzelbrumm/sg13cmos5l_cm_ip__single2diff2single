import sys, klayout.db as db
ly=db.Layout(); ly.read(sys.argv[1]); top=ly.top_cell()
l2n=db.LayoutToNetlist(db.RecursiveShapeIterator(ly, top, []))
L={}
for n,(a,b) in dict(M1=(8,0),V1=(19,0),M2=(10,0),V2=(29,0),M3=(30,0),V3=(49,0),M4=(50,0),TV1=(125,0),TM1=(126,0)).items():
    L[n]=l2n.make_layer(ly.layer(a,b), n)
T={n:l2n.make_text_layer(ly.layer(a,25), n+'t') for n,a in dict(M1=8,M2=10,M3=30,M4=50,TM1=126).items()}
seq=['M1','V1','M2','V2','M3','V3','M4','TV1','TM1']
for n in seq: l2n.connect(L[n])
for a,b in zip(seq,seq[1:]): l2n.connect(L[a],L[b])
for n,t in T.items(): l2n.connect(L[n],t)
l2n.extract_netlist()
for spec in sys.argv[2:]:
    lay,x,y=spec.split(':'); 
    net=l2n.probe_net(L[lay], db.DPoint(float(x),float(y)))
    print(spec, net.expanded_name() if net else None)
