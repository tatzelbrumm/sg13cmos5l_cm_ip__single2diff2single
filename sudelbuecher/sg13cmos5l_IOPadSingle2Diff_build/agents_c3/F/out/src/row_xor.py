# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Device rows of F's split tails against P's s2d_tails_c3 (C3): Activ / GatPoly / Cont / Via1 / M1 inside each row's
window (row Activ box +- 0.70 um in x, gate tabs and contact columns included, the ring 0.80 out excluded; +- 0 in
y). P's upper row is compared after M0 (F builds both rows in P's lower-row frame).
    python3 row_xor.py <p3_cells.gds> <s2d_tails_f.gds>"""
import sys

import klayout.db as db

LAY = {'Activ': (1, 0), 'GatPoly': (5, 0), 'Cont': (6, 0), 'Metal1': (8, 0), 'Via1': (19, 0)}


def rows_of(ly, cell):
    act = db.Region(cell.begin_shapes_rec(ly.layer(1, 0))).merged()
    # device Activ only: the stripes of the 8 devices (the ring is outside); split at the cell's middle line
    return act


def window_regions(ly, cell, box, trans):
    out = {}
    w = db.Region(box)
    for k, (l, d) in LAY.items():
        out[k] = (db.Region(cell.begin_shapes_rec(ly.layer(l, d))).merged() & w).transformed(trans)
    return out


p = db.Layout(); p.read(sys.argv[1])
f = db.Layout(); f.read(sys.argv[2])
u = 1000
pc = p.cell('s2d_tails_c3')
# P's rows: device Activ (ring excluded: the ring strips are 0.30 wide, the device Activ 6+ high) in the lower / upper half
pa = [q.bbox() for q in db.Region(pc.begin_shapes_rec(p.layer(1, 0))).merged().each() if q.bbox().height() > 5000 and 1000 < q.bbox().width() < 10000]
mid = pc.bbox().center().y
prow = {'lo': db.Box(), 'hi': db.Box()}
for b in pa:
    prow['lo' if b.center().y < mid else 'hi'] += b
fails = 0
for name, key in (('s2d_tails_lo_f', 'lo'), ('s2d_tails_hi_f', 'hi')):
    fc = f.cell(name)
    fa = db.Box()
    for q in db.Region(fc.begin_shapes_rec(f.layer(1, 0))).merged().each():
        if q.bbox().height() > 5000 and 1000 < q.bbox().width() < 10000:
            fa += q.bbox()
    pb = prow[key]
    m0 = key == 'hi'
    # map P's row onto F's frame: (M0 for the upper row), then move Activ box corners together
    t0 = db.Trans(db.Trans.M0, 0, 0) if m0 else db.Trans()
    pbt = pb.transformed(t0)
    t = db.Trans(fa.left - pbt.left, fa.bottom - pbt.bottom) * t0
    pw = pb.enlarged(700, 0)
    fw = fa.enlarged(700, 0)
    rp = window_regions(p, pc, pw, t)
    rf = window_regions(f, fc, fw, db.Trans())
    for k in LAY:
        x = (rp[k] ^ rf[k]).merged()
        a = x.area() / (u * u)
        fails += a > 0
        print('%-15s %-8s XOR %.4f um2 %s' % (name, k, a, '' if a == 0 else x.bbox()))
print('row_xor: %s' % ('all rows equal P\'s in the window' if not fails else '%d layer differences' % fails))
print('expected (the listed changes): GatPoly 2 x 0.35 x 0.34 = P\'s row-to-row poly bridge stubs at the row ends; '
      'Metal1 2 x 0.70 x 0.14 = P\'s vdd plate legs between gate column and ring; Via1 = the new vbp edge stubs '
      '(right end in both rows, left end in tails_hi: P had one stub, on the lower row). Activ and Cont: 0.')
