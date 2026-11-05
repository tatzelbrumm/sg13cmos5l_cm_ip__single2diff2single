# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Stage B2 picture: chosen nets in colour over the pad candidate (as the lead's vbp_check.png), nets taken from the
LVS cross-reference.   python3 render_nets.py <run.lvsdb> <pad.gds> <out.png> <net>:<colour> ... [--shield <colour>]
The pad net's shields (iovss metal drawn in pwr_f along the pad path) are shown in their own colour."""
import sys

import klayout.db as db
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.collections import PolyCollection    # noqa: E402
from matplotlib.patches import Rectangle              # noqa: E402

lvsdb, gds, png = sys.argv[1:4]
spec = [a.split(':') for a in sys.argv[4:] if ':' in a]
TOP = 'sg13cmos5l_IOPadSingle2Diff'
l = db.LayoutVsSchematic()
l.read(lvsdb)
pair = next(p for p in l.xref().each_circuit_pair() if p.first() and p.first().name == TOP)
nets = {n.second().name.lower(): n.first() for n in l.xref().each_net_pair(pair) if n.first() and n.second()}
G = db.Layout()
G.read(gds)
gt = G.cell(TOP)
u = G.dbu
GL = {'M1': (8, 0), 'M2': (10, 0), 'M3': (30, 0)}
full = {k: db.Region(gt.begin_shapes_rec(G.find_layer(*v))).merged() for k, v in GL.items()}
win = db.Region(db.DBox(0, 26, 80, 180).to_itype(u))
fig, ax = plt.subplots(figsize=(8, 15))


def draw(reg, col, a, lw=0):
    ps = [[(p.x * u, p.y * u) for p in q.each_point_hull()] for q in (reg & win).decompose_trapezoids_to_region().each()]
    ax.add_collection(PolyCollection(ps, facecolor=col, alpha=a, edgecolor='none'))


for (ld, col, a) in (((1, 0), '#999999', 0.18), ((5, 0), '#bbbbbb', 0.15), ((8, 0), '#7f9fbf', 0.12),
                     ((10, 0), '#a08fbf', 0.12)):
    draw(db.Region(gt.begin_shapes_rec(G.find_layer(*ld))).merged(), col, a)
# shields: pwr_f's iovss metal along the pad path (M1 / M2 / M3 of pwr_f that belongs to the iovss net)
blk = G.cell('s2d_block')
bt = [i.cplx_trans for i in gt.each_inst() if i.cell.name == 's2d_block'][0]
pw = [i for i in blk.each_inst() if i.cell.name == 'pwr_f'][0]
for name, col in spec:
    net = nets.get(name.lower())
    if net is None:
        continue
    for ln in l.layer_names():
        r = l.shapes_of_net(net, l.layer_by_name(ln), True).merged()
        for k, g in full.items():
            if not r.is_empty() and (r - g).is_empty():
                draw(r, col, 0.85)
                break
if '--shield' in sys.argv:
    col = sys.argv[sys.argv.index('--shield') + 1]
    ss = nets.get('iovss')
    for ln in l.layer_names():
        r = l.shapes_of_net(ss, l.layer_by_name(ln), True).merged()
        for k, g in full.items():
            if not r.is_empty() and (r - g).is_empty():
                pr = db.Region(pw.cell.begin_shapes_rec(G.find_layer(*GL[k]))).transformed(bt * pw.cplx_trans)
                draw(r & pr & db.Region(db.DBox(19, 30, 53, 138).to_itype(u)), col, 0.85)
                break
for x0, x1 in ((1.8, 4.3), (75.7, 78.2)):
    ax.add_patch(Rectangle((x0, 31.7), x1 - x0, 148.3, fill=False, hatch='////', edgecolor='#e08000', lw=0.6))
for y0, y1 in ((119, 126), (134, 140), (91.5, 93.5), (60, 66), (158, 160)):
    ax.axhspan(y0, y1, color='#2a7ab0', alpha=0.06)
ax.add_patch(Rectangle((0, 0), 80, 180, fill=False, edgecolor='black', lw=0.8))
ax.set_xlim(-1, 81)
ax.set_ylim(26, 181)
ax.set_aspect('equal')
leg = ', '.join('%s %s' % (n, c) for n, c in spec) + (', shields (iovss) %s' % sys.argv[sys.argv.index('--shield') + 1]
                                                    if '--shield' in sys.argv else '')
ax.set_title('F stage B2: long nets over the pad candidate (%s)\nhatched: edge reserve; blue bands: M3 rail gaps' % leg,
             fontsize=8)
fig.tight_layout()
fig.savefig(png, dpi=120)
