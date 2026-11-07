"""surround.py <gds>: rb_avg device layers in a window of +- one pitch around SL1, SU, SL2 (centers 10.68, 18.40,
26.12 in the cell frame), each window moved onto SU's; XOR against SU's window (um2)."""
import sys
import klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1]); c = ly.cell("rb_avg"); u = ly.dbu
DEV = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "pSD": (14, 0), "NWell": (31, 0), "TGO": (44, 0)}
pt, su = 7.72, 18.40
def win(cx, ld):
    r = db.Region(c.begin_shapes_rec(ly.find_layer(*ld))).merged()
    w = db.Region(db.DBox(cx - pt - 2.96, -1, cx + pt + 2.96, 5).to_itype(u))   # one tub + 1 pitch each side
    return (r & w).moved(db.DVector(su - cx, 0).to_itype(u) if hasattr(db.DVector, "to_itype") else db.Vector(int(round((su - cx) / u)), 0))
for name, cx in (("SL1", su - pt), ("SL2", su + pt)):
    tot = 0
    for k, ld in DEV.items():
        tot += (win(cx, ld) ^ win(su, ld)).area() * u * u
    print("%s window (+-1 pitch) vs SU window, device layers: XOR %.4f um2" % (name, tot))
