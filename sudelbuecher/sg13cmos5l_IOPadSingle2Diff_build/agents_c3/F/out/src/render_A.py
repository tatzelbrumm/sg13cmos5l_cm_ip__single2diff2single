# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Stage A picture (after C2 F2's render_A.py): the pad with the placed cells (named, with sizes), the protection, the
M3 rails and gaps, and the reserved wiring channels.
    python3 render_A.py <placement_A.gds> <placement_A.tsv> <out.png> [x0 y0 x1 y1 [title]]"""
import csv
import os
import sys

import klayout.db as db
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.collections import PolyCollection    # noqa: E402
from matplotlib.patches import Rectangle              # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from place_cfg import CHANNELS  # noqa: E402

gds, tsv, png = sys.argv[1:4]
win = [float(v) for v in sys.argv[4:8]] if len(sys.argv) > 7 else [-1.0, 0.0, 81.0, 181.0]
sub = sys.argv[8] if len(sys.argv) > 8 else ''
full = len(sys.argv) <= 7
ly = db.Layout()
ly.read(gds)
top = ly.cell('sg13cmos5l_IOPadSingle2Diff')
u = ly.dbu
clip = db.Region(db.DBox(*win).to_itype(u))
LAYERS = [((31, 0), '#2e8b57', 0.10), ((44, 0), '#b8b860', 0.05), ((14, 0), '#d2b48c', 0.12),
          ((1, 0), '#22aa22', 0.40), ((5, 0), '#c0392b', 0.40), ((8, 0), '#3a8fd9', 0.22), ((10, 0), '#8e7cc3', 0.25)]
w, h = win[2] - win[0], win[3] - win[1]
fig, ax = plt.subplots(figsize=(13, 13 * h / (w + 14)) if full else (13, max(5, 13 * h / w)))
for (l, d), col, a in LAYERS:
    li = ly.find_layer(l, d)
    if li is None:
        continue
    r = (db.Region(top.begin_shapes_rec(li)) & clip).merged().decompose_trapezoids_to_region()
    ps = [[(p.x * u, p.y * u) for p in q.each_point_hull()] for q in r.each()]
    ax.add_collection(PolyCollection(ps, facecolor=col, alpha=a, edgecolor='none'))
rows = list(csv.DictReader(open(tsv), delimiter='\t'))
COL = {'P': '#1b7a3a', 'N': '#b03030', 'R': '#7a3fb0'}
for r in rows:
    x0, y0, x1, y1 = (float(r[k]) for k in ('x0', 'y0', 'x1', 'y1'))
    col = COL[r['block']]
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor=col, lw=1.6))
    small = (x1 - x0) < 8 or (y1 - y0) < 5
    lab = r['label'] + ('' if r['orientation'] == 'R0' else ' (%s)' % r['orientation'])
    txt = lab if small else '%s\n%s\n%.2f x %.2f' % (lab, r['cell'], x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if win[0] <= cx <= win[2] and win[1] <= cy <= win[3]:
        ax.text(cx, cy, txt, ha='center', va='center', fontsize=6.5 if small else 8, color=col, weight='bold',
                rotation=90 if (x1 - x0) < 15 and (y1 - y0) > 2 * (x1 - x0) else 0,
                bbox=dict(fc='white', ec='none', alpha=0.8, pad=0.5))
# reserved wiring channels
for x0, y0, x1, y1, name in CHANNELS:
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=True, fc='#ffd54f', alpha=0.28, ec='#c79100', lw=0.6,
                           ls='--'))
    if full:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, name, fontsize=5.5, color='#7a5a00', ha='center', va='center',
                rotation=90 if (y1 - y0) > (x1 - x0) else 0)
# pins of the template and of the cells (texts on pin datatype 25 and the template's pad text)
it = top.begin_shapes_rec_overlapping(ly.layer(10, 25), db.DBox(*win))
seen = set()
for (l, d) in ((8, 25), (10, 25)):
    li = ly.find_layer(l, d)
    if li is None:
        continue
    it = top.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            q = it.trans() * db.Point(s.text.x, s.text.y)
            p = (round(q.x * u, 2), round(q.y * u, 2))
            if win[0] <= p[0] <= win[2] and win[1] <= p[1] <= win[3] and (s.text_string, p) not in seen and not full:
                seen.add((s.text_string, p))
                ax.text(p[0], p[1], s.text_string, fontsize=5, color='#303030')
        it.next()
# ring rails (Metal3) beside the cell, and the Metal3 gaps (template layer 30/0)
R = [(7, 32.5, 'iovss'), (34.5, 60, 'iovss'), (66, 91.5, 'iovdd'), (93.5, 119, 'iovdd'), (126, 134, 'iovss'),
     (140, 158, 'vss 1.2'), (160, 178, 'vdd 1.2')]
if full:
    for y0, y1, n in R:
        ax.add_patch(Rectangle((81.0, y0), 2.2, y1 - y0, color='#7f7f7f', alpha=0.5))
        ax.text(84.0, (y0 + y1) / 2, 'M3 %s\n%g-%g' % (n, y0, y1), fontsize=7, va='center')
    for y0, y1 in ((119, 126), (134, 140)):
        ax.add_patch(Rectangle((81.0, y0), 2.2, y1 - y0, fill=False, hatch='..', edgecolor='#2a7ab0'))
        ax.text(84.0, (y0 + y1) / 2, 'M3 free\n%g-%g' % (y0, y1), fontsize=7, va='center', color='#2a7ab0')
        ax.axhspan(y0, y1, xmin=0, xmax=1, color='#2a7ab0', alpha=0.04)
    ax.text(40, 15, 'protection (fixed): DN | DP, CN | CP, RN / RP between', ha='center', fontsize=8,
            bbox=dict(fc='white', ec='none', alpha=0.8))
    ax.text(84.0, 181, 'core-side pins (M2, y 180):\noutp outn vcm vref\niref en_3v3 en_3v3_b', fontsize=7, va='top')
ax.add_patch(Rectangle((0, 0), 80, 180, fill=False, edgecolor='black', lw=1.0))
ax.set_xlim(win[0], win[2] + (14 if full else 0))
ax.set_ylim(win[1], win[3])
ax.set_aspect('equal')
ax.set_xlabel('x (um)')
ax.set_ylabel('y (um)')
ax.set_title(('F stage A (C3): s2d buffer placed in pad template v4, unrouted. Green: PMOS / NWell iovdd, '
              'red: NMOS, violet: rhigh.\nLayers NWell, TGO, pSD, Activ, GatPoly, M1, M2; yellow dashed: reserved '
              'M1 / M2 wiring channels' + (' - ' + sub if sub else '')), fontsize=9)
fig.tight_layout()
fig.savefig(png, dpi=130 if full else 160)
