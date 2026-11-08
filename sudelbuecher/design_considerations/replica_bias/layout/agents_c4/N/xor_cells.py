# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""XOR of two cells, flattened, per layer (optionally only some layers, optionally with a transformation of B).

    python3 xor_cells.py <gdsA> <cellA> <gdsB> <cellB> [--layers 1/0,5/0,...] [--dx X --dy Y] [--m90 X]
                         [--win x0,y0,x1,y1]

Prints the XOR area per layer (um2) and its bbox; 'IDENTICAL' if every compared layer is empty.
--dx/--dy shift B; --m90 X mirrors B about x = X first (for a mirrored copy); --win clips both (A's frame).
"""
import sys
import klayout.db as db

a = sys.argv[1:]
ga, ca, gb, cb = a[:4]
opt = {a[i]: a[i + 1] for i in range(4, len(a) - 1, 2)}
LA, LB = db.Layout(), db.Layout()
LA.read(ga)
LB.read(gb)
A, B = LA.cell(ca), LB.cell(cb)
u = LA.dbu
want = None
if "--layers" in opt:
    want = {tuple(int(v) for v in s.split("/")) for s in opt["--layers"].split(",")}
t = db.Trans(0, False, int(round(float(opt.get("--dx", 0)) / u)), int(round(float(opt.get("--dy", 0)) / u)))
if "--m90" in opt:
    t = t * db.Trans(db.Trans.M90, int(round(2 * float(opt["--m90"]) / u)), 0)
win = db.Region(db.DBox(*[float(v) for v in opt["--win"].split(",")]).to_itype(u)) if "--win" in opt else None
keys = {(i.layer, i.datatype) for i in LA.layer_infos()} | {(i.layer, i.datatype) for i in LB.layer_infos()}
tot = 0.0
for k in sorted(keys):
    if want is not None and k not in want:
        continue
    la, lb = LA.find_layer(*k), LB.find_layer(*k)
    ra = db.Region(A.begin_shapes_rec(la)).merged() if la is not None else db.Region()
    rb = db.Region(B.begin_shapes_rec(lb)).merged().transformed(t) if lb is not None else db.Region()
    if win is not None:
        ra, rb = ra & win, rb & win
    x = (ra ^ rb).merged()
    ar = x.area() * u * u
    tot += ar
    if ar > 0:
        print("  %3d/%-2d XOR %10.4f um2  in %s  (A %d, B %d polygons)" % (k[0], k[1], ar, x.bbox().to_dtype(u),
                                                                       ra.count(), rb.count()))
print("%s:%s vs %s:%s%s  total XOR %.4f um2%s" % (ga.split("/")[-1], ca, gb.split("/")[-1], cb,
                                                  " in " + opt["--win"] if win is not None else "", tot,
                                                "  IDENTICAL" if tot == 0 else ""))
