# free area per metal in the pad cell: cell box minus (metal grown by its min space), in y bands
import klayout.db as db, sys
ly = db.Layout(); ly.read(sys.argv[1])
top = ly.top_cell(); print("top", top.name, top.dbbox())
L = {"Activ":(1,0),"GatPoly":(5,0),"NWell":(31,0),"ThickGateOx":(44,0),"Metal1":(8,0),"Metal2":(10,0),"Metal3":(30,0),"Metal4":(50,0),"TopMetal1":(126,0)}
sp = {"Metal1":0.18,"Metal2":0.21,"Metal3":0.21,"Metal4":0.21,"TopMetal1":1.64,"Activ":0.21,"GatPoly":0.18,"NWell":0.62,"ThickGateOx":0.86}
bb = top.bbox()
cell = db.Region(bb)
def reg(n): return db.Region(top.begin_shapes_rec(ly.layer(*L[n]))).merged()
um = lambda a: a*ly.dbu**2
bands = [(0,84),(84,119),(119,126),(126,134),(134,140),(140,180)]
R = {n: reg(n) for n in L}
print("layer     total-used  " + "  ".join(f"free y{a}-{b}" for a,b in bands))
for n in L:
    used = R[n].sized(int(sp[n]/ly.dbu)) 
    free = cell - used
    row = []
    for a,b in bands:
        box = db.Region(db.Box(bb.left, int(a/ly.dbu), bb.right, int(b/ly.dbu)))
        row.append(um((free & box).area()))
    print(f"{n:11s} {um(R[n].area()):9.0f}  " + "  ".join(f"{x:10.0f}" for x in row))
# free in ALL of Metal1, Metal2 and Activ/GatPoly/NWell (room for a MOS cap + MOM M1-M2 on its own)
dev = (R["Activ"]+R["GatPoly"]+R["NWell"]).merged().sized(int(0.62/ly.dbu))
for combo in (["Metal2"],["Metal1","Metal2"],["Metal1","Metal2","Metal3"]):
    used = dev
    for n in combo: used = used + R[n].sized(int(sp[n]/ly.dbu))
    free = (cell - used.merged())
    # keep only pieces >= 5 um in both directions
    big = free.sized(-int(2.5/ly.dbu)).sized(int(2.5/ly.dbu)) & free
    print("free of devices and", "+".join(combo), "(pieces >= 5 um):", f"{um(big.area()):.0f} um2;", "largest boxes:", sorted([(round(um(p.area())), p.bbox().to_dtype(ly.dbu)) for p in big.each_merged()], key=lambda t:-t[0])[:5])
