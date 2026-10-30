import sys; sys.path.insert(0,"../out/v2")
import generator as G, klayout.db as db, numpy as np
cfg=G.load_config("test_v1cells.py")
blk=G.Block(cfg["NAME"],cfg["SOURCES"],cfg["INSTANCES"],cfg["FLOORPLAN"],G.load_rules(cfg["RULES"]),cfg["NETS"],cfg["PORTS"],cfg["PIN_OVERRIDES"],cfg["ROUTER"],None,(),lambda *a: None)
blk.place(); blk.collect_pins()
net=sys.argv[1]
for p in blk.pins:
    if p["net"]==net: print(p["inst"],p["cellpin"],p["metal"],p["box"],"group",p["group"],{m:r.bbox().to_dtype(0.001) for m,r in p["terms"].items()})
# monkeypatch route to stop before routing: build router only
blk.nets=[n for n in blk.nets]
import types
gr=None
orig=G.GridRouter.route_net
def stop(self,k,groups):
    global gr; gr=self
    raise SystemExit
names=[None]+blk.nets; k=names.index(net)
G.GridRouter.route_net=lambda self,kk,groups: (orig(self,kk,groups) if kk!=k else (_ for _ in ()).throw(KeyboardInterrupt((self,groups))))
try:
    blk.route(None)
except KeyboardInterrupt as e:
    gr,groups=e.args[0]
print("groups sizes",[len(g) for g in groups])
y=float(sys.argv[2]); x0,x1=float(sys.argv[3]),float(sys.argv[4])
j=int(np.argmin(abs(gr.ys-y/0.001))); print("line y",gr.ys[j]*0.001)
f=gr.free(k)
for L in (0,1):
    row="".join("." if f[L,i,j] else "#" for i in range(gr.NX) if x0<=gr.xs[i]*0.001<=x1)
    print("L%d"%L,row)
xs=[round(gr.xs[i]*0.001,3) for i in range(gr.NX) if x0<=gr.xs[i]*0.001<=x1]; print(xs)
for kk,nm in enumerate(names):
    if gr.mask[kk,1,:,j].any():
        row="".join("#" if gr.mask[kk,1,i,j] else "." for i in range(gr.NX) if x0<=gr.xs[i]*0.001<=x1)
        if "#" in row: print("blocker",nm,row)
