# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Stage B pictures: the routed pad candidate with the cells named, the edge reserve (hatched), the Metal3 gaps and
the core-side pins.   python3 render_B.py <block_cfg.py> <pad_candidate.gds> <out.png> [x0 y0 x1 y1 [title]]
Writes <out dir>/placement_B.tsv (the placed bounding boxes) next to the picture."""
import csv
import os
import sys

import klayout.db as db
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.collections import PolyCollection    # noqa: E402
from matplotlib.patches import Rectangle              # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[1])))
import block_cfg as B  # noqa: E402

gds, png = sys.argv[2:4]
win = [float(v) for v in sys.argv[4:8]] if len(sys.argv) > 7 else [-1.0, 26.0, 81.0, 181.0]
sub = sys.argv[8] if len(sys.argv) > 8 else ''
full = len(sys.argv) <= 7
rows = []
for inst, cell, o, x, y, nets in B.PLACE:
    if x is None:
        continue
    b = B._cell(cell)[1].dbbox().transformed(db.DTrans(B.ORI[o], 0, 0))
    rows.append((inst, cell, o, x, y, x + b.width(), y + b.height()))
with open(os.path.join(os.path.dirname(os.path.abspath(png)), 'placement_B.tsv'), 'w') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['instance', 'cell', 'orientation', 'x0', 'y0', 'x1', 'y1'])
    w.writerows([(r[0], r[1], r[2]) + tuple(round(v, 3) for v in r[3:]) for r in rows])
ly = db.Layout()
ly.read(gds)
top = ly.cell('sg13cmos5l_IOPadSingle2Diff')
u = ly.dbu
clip = db.Region(db.DBox(*win).to_itype(u))
LAYERS = [((31, 0), '#2e8b57', 0.08), ((1, 0), '#22aa22', 0.30), ((5, 0), '#c0392b', 0.30), ((8, 0), '#1f6fd0', 0.40),
          ((10, 0), '#9b59b6', 0.45), ((19, 0), '#000000', 0.8)]
W, H = win[2] - win[0], win[3] - win[1]
fig, ax = plt.subplots(figsize=(13, 13 * H / (W + 14)) if full else (13, max(5, 13 * H / W)))
for (l, d), col, a in LAYERS:
    li = ly.find_layer(l, d)
    if li is None:
        continue
    r = (db.Region(top.begin_shapes_rec(li)) & clip).merged().decompose_trapezoids_to_region()
    ax.add_collection(PolyCollection([[(p.x * u, p.y * u) for p in q.each_point_hull()] for q in r.each()],
                                     facecolor=col, alpha=a, edgecolor='none'))
COL = {'P': '#1b7a3a', 'N': '#b03030', 'R': '#7a3fb0'}
KIND = {'sinks': 'N', 'cascn': 'N', 'sinkc': 'N', 'treen': 'N', 'cload': 'N', 'rhigh': 'R'}
for inst, cell, o, x0, y0, x1, y1 in rows:
    col = COL[KIND.get(inst, 'P')]
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor=col, lw=1.2))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if win[0] <= cx <= win[2] and win[1] <= cy <= win[3]:
        small = (x1 - x0) < 8 or (y1 - y0) < 5
        ax.text(cx, cy, inst if small else '%s\n%s (%s)' % (inst, cell, o), ha='center', va='center',
                fontsize=6 if small else 7.5, color=col, weight='bold',
                rotation=90 if (x1 - x0) < 15 and (y1 - y0) > 2 * (x1 - x0) else 0,
                bbox=dict(fc='white', ec='none', alpha=0.75, pad=0.4))
for x0, y0, x1, y1 in B.RESERVE:
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, hatch='////', edgecolor='#e08000', lw=0.8))
if full:
    ax.text(3.05, 30.0, 'edge reserve\n(no buffer device\nlayers, no M1)', fontsize=6, color='#c06000', ha='center')
    for y0, y1 in ((119, 126), (134, 140)):
        ax.axhspan(y0, y1, color='#2a7ab0', alpha=0.05)
        ax.text(81.0, (y0 + y1) / 2, 'M3 free\n%g-%g' % (y0, y1), fontsize=7, va='center', color='#2a7ab0')
    for y0, y1, n in ((34.5, 60, 'iovss'), (66, 91.5, 'iovdd'), (93.5, 119, 'iovdd'), (126, 134, 'iovss'),
                      (140, 158, 'vss 1.2'), (160, 178, 'vdd 1.2')):
        ax.add_patch(Rectangle((88.0, y0), 1.5, y1 - y0, color='#7f7f7f', alpha=0.5))
        ax.text(90.0, (y0 + y1) / 2, 'M3 %s' % n, fontsize=7, va='center')
it = top.begin_shapes_rec(ly.layer(10, 25))
while not it.at_end():
    s = it.shape()
    if s.is_text() and it.cell().name == top.name:
        p = it.trans() * db.Point(s.text.x, s.text.y)
        if win[1] <= p.y * u <= win[3] + 1:
            ax.text(p.x * u, min(p.y * u, win[3]) - 0.6, s.text_string, fontsize=6, rotation=90, ha='center',
                    va='top', color='#4b2a80', weight='bold')
    it.next()
ax.add_patch(Rectangle((0, 0), 80, 180, fill=False, edgecolor='black', lw=1.0))
ax.set_xlim(win[0], win[2] + (14 if full else 0))
ax.set_ylim(win[1], win[3])
ax.set_aspect('equal')
ax.set_xlabel('x (um)')
ax.set_ylabel('y (um)')
ax.set_title('F stage B (C3): pad candidate sg13cmos5l_IOPadSingle2Diff, routed (M1 blue, M2 violet, Via1 black); '
             'hatched: edge reserve' + (' - ' + sub if sub else ''), fontsize=9)
fig.tight_layout()
fig.savefig(png, dpi=130 if full else 150)
