# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B: the edge reserve as built (Christoph 2026-11-04: x 1.8..4.3 and 75.7..78.2 free of the buffer's
device layers and Metal1, y >= 31.7).   python3 reserve_check.py <pad_candidate.gds>

Only the buffer's shapes count (cell s2d_block and below; the template's own edge structures stay as they are).
Per side and per 1 um band of y: the free width actually kept between the template's edge strip (x 1.8 / 78.2) and
the nearest buffer device-layer or Metal1 shape. Metal2 / Via2 / Metal3 in the reserve are listed (allowed)."""
import sys

import klayout.db as db

ly = db.Layout()
ly.read(sys.argv[1])
blk = ly.cell('s2d_block')
top = ly.cell('sg13cmos5l_IOPadSingle2Diff')
t = [i.dcplx_trans for i in top.each_inst() if i.cell.name == 's2d_block'][0]
DEV = {'Activ': (1, 0), 'GatPoly': (5, 0), 'Cont': (6, 0), 'nSD': (7, 0), 'pSD': (14, 0), 'NWell': (31, 0),
       'ThickGateOx': (44, 0), 'SalBlock': (28, 0), 'EXTBlock': (111, 0), 'PolyRes': (128, 0), 'RES': (24, 0),
       'Metal1': (8, 0)}
OK = {'Metal2': (10, 0), 'Via1': (19, 0), 'Via2': (29, 0), 'Metal3': (30, 0)}
u = ly.dbu


def reg(ld):
    li = ly.find_layer(*ld)
    if li is None:
        return db.Region()
    return db.Region(blk.begin_shapes_rec(li)).transformed(db.ICplxTrans(t, u) if False else t.to_itrans(u)).merged()


bad = db.Region()
print('| layer | in the reserve (um2) |')
print('|---|---:|')
for side, box in (('left', db.DBox(1.8, 31.7, 4.3, 180.0)), ('right', db.DBox(75.7, 31.7, 78.2, 180.0))):
    rb = db.Region(box.to_itype(u))
    for name, ld in DEV.items():
        a = (reg(ld) & rb).area() * u * u
        if a:
            print('| %s %s | %.3f |' % (side, name, a))
        bad += reg(ld) & rb
    for name, ld in OK.items():
        a = (reg(ld) & rb).area() * u * u
        print('| %s %s (allowed) | %.2f |' % (side, name, a))
dev = db.Region()
for ld in DEV.values():
    dev += reg(ld)
dev.merge()
print('\nreserve width kept (um), per y band, from the edge strip (x 1.8 / 78.2) to the nearest buffer device / M1:')
for side in ('left', 'right'):
    rows, last = [], None
    y = 31.7
    while y < 180.0:
        y1 = min(180.0, y + 1.0)
        if side == 'left':
            probe = db.Region(db.DBox(1.8, y, 10.0, y1).to_itype(u)) & dev
            w = (probe.bbox().left * u - 1.8) if not probe.is_empty() else 8.2
        else:
            probe = db.Region(db.DBox(70.0, y, 78.2, y1).to_itype(u)) & dev
            w = (78.2 - probe.bbox().right * u) if not probe.is_empty() else 8.2
        w = round(min(w, 8.2), 2)
        if last is None or abs(w - last[2]) > 1e-6:
            if last:
                rows.append(last)
            last = [y, y1, w]
        else:
            last[1] = y1
        y = y1
    rows.append(last)
    print('  %s: ' % side + '; '.join('y %.1f-%.1f: %s' % (a, b, ('>= 2.5 (%.2f)' % w) if w >= 2.5 else '%.2f' % w)
                                     for a, b, w in rows))
print('\nbuffer device layers / Metal1 inside the reserve: %.4f um2 -> %s' % (bad.area() * u * u,
      'reserve kept everywhere' if bad.is_empty() else 'VIOLATED'))
