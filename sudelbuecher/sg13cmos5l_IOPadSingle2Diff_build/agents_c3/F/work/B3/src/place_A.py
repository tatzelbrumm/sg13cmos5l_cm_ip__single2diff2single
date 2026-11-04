# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3, 2026-11-03), stage A: place P's and N's primitives (and F's reworked copies) in the cleaned-out pad
template, unrouted.   python3 place_A.py <template.gds> <out_dir> <cells.gds>...

Later cell libraries override earlier ones by cell name (so F's `_f` copies replace nothing by accident: they have
their own names). Writes <out_dir>/placement_A.gds (top cell sg13cmos5l_IOPadSingle2Diff = the template + the
placed cells as instances, no routing) and <out_dir>/placement_A.tsv (placed bounding boxes).
The placement itself is the table PLACE in place_cfg.py (one line per cell, with the reason).
"""
import csv
import os
import sys

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from place_cfg import PLACE, KEEP_OUT, REGION  # noqa: E402

TPL, OUT = sys.argv[1], sys.argv[2]
LIBS = sys.argv[3:]
ly = db.Layout()
ly.read(TPL)
top = ly.cell('sg13cmos5l_IOPadSingle2Diff')
src = {}
for f in LIBS:
    s = db.Layout()
    s.read(f)
    for c in s.each_cell():
        src[c.name] = (s, c)

ORI = {'R0': db.DTrans.R0, 'R90': db.DTrans.R90, 'R180': db.DTrans.R180, 'R270': db.DTrans.R270,
       'M0': db.DTrans.M0, 'M45': db.DTrans.M45, 'M90': db.DTrans.M90, 'M135': db.DTrans.M135}
made, rows = {}, []
for name, o, x, y, blk, label in PLACE:
    s, sc = src[name]
    if name not in made:
        made[name] = ly.create_cell(name)
        made[name].copy_tree(sc)
    c = made[name]
    r = db.DTrans(ORI[o], 0, 0)
    b = c.dbbox().transformed(r)
    t = db.DTrans(ORI[o], round(x - b.left, 3), round(y - b.bottom, 3))
    top.insert(db.DCellInstArray(c.cell_index(), t))
    pb = c.dbbox().transformed(t)
    rows.append((label or name, name, o, blk, round(pb.left, 3), round(pb.bottom, 3), round(pb.right, 3),
                 round(pb.top, 3), round(pb.width() * pb.height(), 1)))
bad = 0
for i in range(len(rows)):
    a = db.DBox(*rows[i][4:8])
    if not db.DBox(*REGION).contains(a.p1) or not db.DBox(*REGION).contains(a.p2):
        print('OUTSIDE REGION', rows[i][0]); bad += 1
    for k in KEEP_OUT:
        if a.overlaps(db.DBox(*k)):
            print('IN KEEP-OUT', rows[i][0], k); bad += 1
    for j in range(i + 1, len(rows)):
        if a.overlaps(db.DBox(*rows[j][4:8])):
            print('OVERLAP', rows[i][0], rows[j][0]); bad += 1
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(os.path.join(OUT, 'placement_A.gds'), opt)
with open(os.path.join(OUT, 'placement_A.tsv'), 'w') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['label', 'cell', 'orientation', 'block', 'x0', 'y0', 'x1', 'y1', 'area_um2'])
    w.writerows(rows)
for r in rows:
    print('%-14s %-22s %-4s %s  x %7.3f .. %7.3f  y %7.3f .. %7.3f  %7.1f um2' % (r[0], r[1], r[2], r[3], r[4], r[6],
                                                                                r[5], r[7], r[8]))
print('placement problems:', bad)
