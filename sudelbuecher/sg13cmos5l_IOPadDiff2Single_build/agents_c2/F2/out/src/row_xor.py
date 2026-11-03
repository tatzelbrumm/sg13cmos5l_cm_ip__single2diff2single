# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Device-layer XOR of a reworked cell against the reviewed original inside a window (the part that should be
unchanged).   python3 row_xor.py <orig.gds> <orig_cell> <new.gds> <new_cell> <dx> <dy> <x0> <y0> <x1> <y1>
(dx, dy) = new - orig coordinate offset; the window is in the new cell's coordinates."""
import sys

import klayout.db as db

LAYERS = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "pSD": (14, 0), "NWell": (31, 0), "ThickGateOx": (44, 0),
          "Metal1": (8, 0)}
a = sys.argv[1:]
lo, ln = db.Layout(), db.Layout()
lo.read(a[0])
ln.read(a[2])
co, cn = lo.cell(a[1]), ln.cell(a[3])
dx, dy = float(a[4]), float(a[5])
w = db.DBox(*[float(v) for v in a[6:10]])
tot = 0.0
for n, (l, d) in LAYERS.items():
    io, inn = lo.find_layer(l, d), ln.find_layer(l, d)
    ro = db.Region(co.begin_shapes_rec(io)).transformed(db.DTrans(db.DVector(dx, dy)).to_itype(lo.dbu)) \
        if io is not None else db.Region()
    rn = db.Region(cn.begin_shapes_rec(inn)) if inn is not None else db.Region()
    wi = db.Region(w.to_itype(ln.dbu))
    x = ((ro & wi) ^ (rn & wi)).merged()
    ar = x.area() * ln.dbu ** 2
    tot += ar
    print("  %-12s XOR %.4f um2%s" % (n, ar, "  in %s" % x.bbox().to_dtype(ln.dbu) if ar else ""))
print("%s vs %s in %s: total %.4f um2" % (a[3], a[1], w, tot))
