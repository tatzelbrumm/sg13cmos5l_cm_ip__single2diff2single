"""point-symmetry check of oa_pmir_c: XOR of each layer with its 180-degree image about the array centre"""
import sys, klayout.db as db
gds, cn = sys.argv[1], sys.argv[2]
ly = db.Layout(); ly.read(gds); c = ly.cell(cn)
b = c.bbox(); cx2, cy2 = b.left + b.right, b.bottom + b.top          # 2 x centre (dbu)
img = db.ICplxTrans(1, 180, False, cx2, cy2)                      # p -> -p + 2c
def reg(L, D):
    li = ly.find_layer(L, D)
    return db.Region(c.begin_shapes_rec(li)).merged() if li is not None else db.Region()
print("centre (um):", cx2 / 2 * ly.dbu, cy2 / 2 * ly.dbu)
for name, L in (("Activ", (1, 0)), ("GatPoly", (5, 0)), ("Cont", (6, 0)), ("pSD", (14, 0)), ("NWell", (31, 0)),
                ("ThickGateOx", (44, 0)), ("Metal1", (8, 0)), ("Via1", (19, 0)), ("Metal2", (10, 0))):
    r = reg(*L)
    x = r ^ r.transformed(img)
    print("%-12s area %9.3f um2  XOR with point image %8.3f um2" % (name, r.area() * ly.dbu ** 2, x.area() * ly.dbu ** 2))
# real devices only: fingers by their 63/0 tags
li = ly.find_layer(63, 0); act = reg(1, 0)
tags = {}
for it in c.begin_shapes_rec(li).each():
    s = it.shape()
    if s.is_text() and it.cell().name == cn:
        p = it.trans() * s.text_trans.disp
        tags[(p.x, p.y)] = s.text_string
fingers = {}
for p in act.each():
    for (x, y), t in tags.items():
        if p.inside(db.Point(x, y)):
            fingers[(x, y)] = (t, p)
real = db.Region([p for (t, p) in fingers.values() if t in ("PO", "P8", "P2", "P0")])
xr = real ^ real.transformed(img)
print("real fingers (PO P8 P2 P0) Activ: %d fingers, XOR with image %.3f um2" % (real.count(), xr.area() * ly.dbu ** 2))
for p in xr.each():
    bb = p.bbox()
    print("   differs at", bb.to_dtype(ly.dbu), [t for (xy, (t, q)) in fingers.items() if q.bbox() == bb or (q.bbox().transformed(img) == bb)])
bad = 0
for (x, y), (t, p) in fingers.items():
    q = db.Point(cx2 - x, cy2 - y)
    t2 = tags.get((q.x, q.y))
    exp = {"P0": "dummy", "dummy": "P0"}.get(t, t)
    if t2 != exp:
        bad += 1; print("   map mismatch", t, "->", t2)
print("letter map under R180: %d fingers, %d mismatches (P0 <-> inner dummy expected)" % (len(fingers), bad))
