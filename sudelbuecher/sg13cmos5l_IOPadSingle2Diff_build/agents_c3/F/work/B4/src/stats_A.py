# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Areas of the stage A placement: per block (sum of cell boxes, and the block's bounding box), the whole block's
bounding box, the free region (place_cfg REGION minus KEEP_OUT) and what is left of it.
    python3 stats_A.py <placement_A.tsv> <p3.gds> <n3.gds>"""
import csv
import os
import sys

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from place_cfg import REGION, KEEP_OUT, CHANNELS  # noqa: E402

rows = list(csv.DictReader(open(sys.argv[1]), delimiter='\t'))
lib = {}
for f in sys.argv[2:4]:
    ly = db.Layout(); ly.read(f)
    for c in ly.top_cells():
        lib[c.name] = c.dbbox().width() * c.dbbox().height()
lib['s2d_tails_c3'] = 45.19 * 15.83
BLOCKS = {'input group (tubs, tails, R)': ['inputs', 'tails_lo', 'tails_hi', 'rhigh'],
          'NMOS fold, left pocket (sinks, casc_n)': ['sinks', 'casc_n'],
          'CMFB sinks (sinks_cmfb)': ['sinks_cmfb'],
          'PMOS output stage (casc_p, loads)': ['casc_p', 'loads'],
          'load capacitors + output ties (cload, pd_p)': ['cload', 'pd_p'],
          'bias tree (tree_n, tree_p)': ['tree_n', 'tree_p']}
B = {r['label']: (db.DBox(*(float(r[k]) for k in ('x0', 'y0', 'x1', 'y1'))), r['cell']) for r in rows}
u = 0.001
print('| block | cells (delivered, um2) | cells (placed, um2) | block bbox (um) | bbox um2 |')
print('|---|---:|---:|---|---:|')
tot_d = tot_p = 0
for name, labs in BLOCKS.items():
    d = sum(lib.get(B[l][1], 0) for l in labs if not B[l][1].endswith('_f'))
    if any(B[l][1].endswith('_f') for l in labs):
        d += lib['s2d_tails_c3']
    p = sum(B[l][0].width() * B[l][0].height() for l in labs)
    bb = db.DBox()
    for l in labs:
        bb += B[l][0]
    tot_d += d; tot_p += p
    print('| %s | %.0f | %.0f | x %.2f-%.2f, y %.2f-%.2f | %.0f |' % (name, d, p, bb.left, bb.right, bb.bottom, bb.top,
                                                                    bb.width() * bb.height()))
env = db.DBox()
for b, _ in B.values():
    env += b
free = db.Region(db.DBox(*REGION).to_itype(u)) - db.Region([db.DBox(*k).to_itype(u) for k in KEEP_OUT])
cells = db.Region([b.to_itype(u) for b, _ in B.values()])
ch = db.Region([db.DBox(*c[:4]).to_itype(u) for c in CHANNELS]) & free
left = free - cells
print('\ncells: delivered %.0f um2, placed %.0f um2' % (tot_d, tot_p))
print('whole block bbox: x %.2f-%.2f, y %.2f-%.2f = %.0f um2' % (env.left, env.right, env.bottom, env.top,
                                                               env.width() * env.height()))
print('free region (REGION - KEEP_OUT): %.0f um2; cells cover %.0f (%.0f %%); left %.0f um2, of it %.0f in the '
      'reserved channels, %.0f elsewhere' % (free.area() * u * u, (free & cells).area() * u * u,
                                             100 * (free & cells).area() / free.area(), left.area() * u * u,
                                             (left & ch).area() * u * u, (left - ch).area() * u * u))
# largest free boxes outside the channels (greedy, rectangles of the merged rest)
rest = (left - ch).merged()
big = sorted(rest.decompose_convex_to_region().each(), key=lambda p: -p.area())[:6]
for p in big:
    b = p.bbox().to_dtype(u)
    print('  free: x %.2f-%.2f, y %.2f-%.2f (%.1f x %.1f um, %.0f um2)' % (b.left, b.right, b.bottom, b.top,
                                                                       b.width(), b.height(), p.area() * u * u))
