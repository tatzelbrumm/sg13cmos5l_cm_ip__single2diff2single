# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): picture of pad_ref_rb with the routed nets colored (after C3 F's render_A.py).
    python3 render.py <pad_ref_rb.gds> <netmap.gds> <rb_place.py> <out.png> [x0 y0 x1 y1 [title]]"""
import sys

import klayout.db as db
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.collections import PolyCollection    # noqa: E402
from matplotlib.patches import Rectangle              # noqa: E402

gds, nm, place, png = sys.argv[1:5]
g = {}
exec(open(place).read(), g)
win = [float(v) for v in sys.argv[5:9]] if len(sys.argv) > 8 else [-1.0, -1.0, g['W'] + 1, g['H'] + 1]
sub = sys.argv[9] if len(sys.argv) > 9 else ''
full = len(sys.argv) <= 8
ly = db.Layout()
ly.read(gds)
top = ly.cell('pad_ref_rb')
u = ly.dbu
clip = db.Region(db.DBox(*win).to_itype(u))


def polys(reg):
    return [[(p.x * u, p.y * u) for p in q.each_point_hull()] for q in reg.decompose_trapezoids_to_region().each()]


w, h = win[2] - win[0], win[3] - win[1]
fig, ax = plt.subplots(figsize=(14, 14 * h / w + 0.8) if full else (14, max(5, 14 * h / w + 0.8)))
for (l, d), col, a in (((31, 0), '#2e8b57', 0.10), ((1, 0), '#22aa22', 0.30), ((5, 0), '#c0392b', 0.30),
                       ((8, 0), '#7f9fbf', 0.30), ((10, 0), '#a080c0', 0.25)):
    li = ly.find_layer(l, d)
    if li is not None:
        r = (db.Region(top.begin_shapes_rec(li)) & clip).merged()
        ax.add_collection(PolyCollection(polys(r), facecolor=col, alpha=a, edgecolor='none'))
# routed nets
nl = db.Layout()
nl.read(nm)
nc = nl.cell('netmap')
names = sorted([s.text_string for s in nc.shapes(nl.layer(999, 0)).each()], key=lambda s: 0)
names = [s.text_string for s in nc.shapes(nl.layer(999, 0)).each()]
cmap = plt.get_cmap('tab20')
legend = []
for k, net in enumerate(names, 1):
    col = cmap((k - 1) % 20)
    for L, a, hatch in ((0, 0.85, None), (1, 0.55, None), (2, 1.0, None)):
        li = nl.find_layer(1000 + k, L)
        if li is None:
            continue
        r = db.Region(nc.shapes(li)) & clip
        if r.is_empty():
            continue
        ax.add_collection(PolyCollection(polys(r.merged()), facecolor=col if L < 2 else 'black', alpha=a,
                                         edgecolor=col if L == 1 else 'none', lw=0.4))
    legend.append(plt.Line2D([0], [0], color=col, lw=4, label=net))
# cells
for inst, cell, o, x, y in g['PLACE']:
    if cell == 'frame_f':
        continue
    for ci in top.each_inst():
        if ly.cell(ci.cell_index).name == cell:
            b = ci.dbbox()
            ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False, ec='#303030', lw=1.0))
            cx, cy = b.center().x, b.center().y
            if win[0] <= cx <= win[2] and win[1] <= cy <= win[3]:
                ax.text(cx, cy, '%s (%s)\n%.2f x %.2f' % (cell, o, b.width(), b.height()), ha='center',
                        va='center', fontsize=8, weight='bold', color='#202020',
                        bbox=dict(fc='white', ec='none', alpha=0.7, pad=0.4))
# pin texts: the top cell's ports and rails; in close-ups also the rows' pins
for li in ly.layer_indexes():
    info = ly.get_info(li)
    if info.datatype != 25:
        continue
    it = top.begin_shapes_rec(li)
    if full:
        it.max_depth = 0
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            p = it.trans() * db.Point(s.text.x, s.text.y)
            if win[0] <= p.x * u <= win[2] and win[1] <= p.y * u <= win[3]:
                ax.text(p.x * u, p.y * u, s.text_string, fontsize=7 if full else 6, color='#000060',
                        ha='left' if full else 'center')
        it.next()
ax.add_patch(Rectangle((0, 0), g['W'], g['H'], fill=False, ec='black', lw=1.2))
ax.set_xlim(win[0], win[2])
ax.set_ylim(win[1], win[3])
ax.set_aspect('equal')
ax.set_xlabel('x (um)')
ax.set_ylabel('y (um)')
ax.legend(handles=legend, loc='upper left', bbox_to_anchor=(1.01, 1.0), fontsize=8, title='routed nets\n(M1 solid, M2 light)')
ax.set_title('pad_ref_rb (Claude, agent F, C4): %.2f x %.2f um. NWell, Activ, GatPoly, M1, M2 of the rows in pale '
             'colors' % (g['W'], g['H']) + (' - ' + sub if sub else ''), fontsize=9)
fig.tight_layout()
fig.savefig(png, dpi=110 if full else 150)
