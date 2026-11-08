"""compare_pad_v3.py <rb_avg_v3.gds> <s2d pad gds>: the row end of rb_avg (gate column + end dummy 1/4) against the
row end of the pad's s2d_loads_f (gate column + end dummy X, the same 1/4 finger, both from C3's rows()/gate_cols()),
device layers, flat XOR in a window from the row's end Activ edge - 0.65 to + 1.0 (the dummy) over the Activ height.
Also the finger cell against the pad's pmosHV_w1_l4$1 (all layers)."""
import sys
import klayout.db as db
a, p = db.Layout(), db.Layout(); a.read(sys.argv[1]); p.read(sys.argv[2]); U = a.dbu
DEV = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "pSD": (14, 0)}
def reg(ly, c, ld):
    i = ly.find_layer(*ld)
    return db.Region(c.begin_shapes_rec(i)).merged() if i is not None else db.Region()
def lowrow(ly, c):
    """Activ boxes of the lowest finger row (merged per finger), sorted left to right"""
    bs = [q.bbox() for q in reg(ly, c, (1, 0)).each() if 4600 < q.bbox().height() < 4700]
    yb = min(b.bottom for b in bs)
    return sorted([b for b in bs if b.bottom == yb], key=lambda b: b.left)
for rb in ("rb_avg_u", "rb_avg_l"):
    for side in ("left", "right"):
        out = []
        ca, cp = a.cell(rb), p.cell("s2d_loads_f")
        fa, fp = lowrow(a, ca), lowrow(p, cp)
        ea, ep = (fa[0], fp[0]) if side == "left" else (fa[-1], fp[-1])
        for ld in DEV.values():
            res = []
            for ly, c, e in ((a, ca, ea), (p, cp, ep)):
                x = e.left if side == "left" else e.right
                sg = 1 if side == "left" else -1
                w = db.Region(db.Box(min(x - sg * 650, x + sg * 1000), e.bottom, max(x - sg * 650, x + sg * 1000), e.top))
                res.append((reg(ly, c, ld) & w).moved(-x, -e.bottom))
            x = res[0] ^ res[1]
            if not x.is_empty():
                out.append("%d/%d %.4f um2" % (ld[0], ld[1], x.area() * U * U))
        print("%s %s row end (gate column + end dummy) vs pad s2d_loads_f lower row %s end: %s" % (rb, side, side, "XOR 0" if not out else "XOR " + ", ".join(out)))
ca, cp = a.cell("rb_pmosHV_w1_l4"), p.cell("pmosHV_w1_l4$1")
lays = sorted({(i.layer, i.datatype) for L in (a, p) for i in L.layer_infos()})
d = [ld for ld in lays if not (reg(a, ca, ld) ^ reg(p, cp, ld)).is_empty()]
print("finger rb_pmosHV_w1_l4 vs pad pmosHV_w1_l4$1, all layers:", "XOR 0" if not d else "differs on %s" % d)
