# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B2: routing length per net and layer, and the longest parallel runs beside the pad net.

    python3 net_metrics.py <run.lvsdb> <pad.gds> <net> [<net> ...]

Nets by schematic name from the LVS cross-reference (as the lead's long_nets_rdb.py). Length: only the routing
metal (shapes drawn in s2d_block's own top cell and in pwr_f, i.e. router wires and F's drawn wiring, not the cells'
internal metal), merged per layer and cut into rectangles; each rectangle counts with its long side (a slight
overcount at corners). Parallel runs: for every other net, its metal (all of it, cells included) on the same or an
adjacent metal layer within 1.0 um of the pad net's routing metal, cut into pieces; the longest piece's long side."""
import sys

import klayout.db as db

lvsdb, gds = sys.argv[1], sys.argv[2]
names = [a for a in sys.argv[3:] if not a.startswith('--d=')]
DIST = float(next((a[4:] for a in sys.argv[3:] if a.startswith('--d=')), '1.0'))   # um; 0.7 = inside the shields' far edge
TOP = 'sg13cmos5l_IOPadSingle2Diff'
l = db.LayoutVsSchematic()
l.read(lvsdb)
pair = next(p for p in l.xref().each_circuit_pair() if p.first() and p.first().name == TOP)
nets = {np_.second().name.lower(): np_.first() for np_ in l.xref().each_net_pair(pair) if np_.first() and np_.second()}
lay_nets = [np_.first() for np_ in l.xref().each_net_pair(pair) if np_.first()]
sname = {np_.first().expanded_name(): (np_.second().name if np_.second() else '?') for np_ in l.xref().each_net_pair(pair) if np_.first()}
G = db.Layout()
G.read(gds)
gt = G.cell(TOP)
u = G.dbu
GL = {'M1': (8, 0), 'M2': (10, 0), 'M3': (30, 0)}
full = {k: db.Region(gt.begin_shapes_rec(G.find_layer(*v))).merged() for k, v in GL.items()}
# routing metal: s2d_block's own shapes and pwr_f, in top coordinates
blk = G.cell('s2d_block')
bt = [i.cplx_trans for i in gt.each_inst() if i.cell.name == 's2d_block'][0]
route = {}
for k, v in GL.items():
    li = G.find_layer(*v)
    r = db.Region(blk.shapes(li)).transformed(bt) if li is not None else db.Region()
    for i in blk.each_inst():
        if i.cell.name == 'pwr_f':
            r += db.Region(i.cell.begin_shapes_rec(li)).transformed(bt * i.cplx_trans)
    route[k] = r.merged()


def net_layers(net):
    out = {}
    for ln in l.layer_names():
        r = l.shapes_of_net(net, l.layer_by_name(ln), True).merged()
        if r.is_empty():
            continue
        for k, g in full.items():
            if (r - g).is_empty() and not r.is_empty():
                out[k] = (out.get(k, db.Region()) + r).merged()
                break
    return out


def length(reg):
    return sum(max(b.width(), b.height()) for b in (p.bbox() for p in reg.decompose_convex_to_region().each())) * u


print('| net | M1 um | M2 um | M3 um |')
print('|---|---:|---:|---:|')
geo = {}
for n in names:
    net = nets.get(n.lower())
    if net is None:
        print('| %s | not in xref | | |' % n)
        continue
    g = net_layers(net)
    geo[n] = g
    print('| %s | %.1f | %.1f | %.1f |' % (n, *(length(g.get(k, db.Region()) & route[k]) for k in ('M1', 'M2', 'M3'))))
if 'pad' in geo:
    ADJ = {'M1': ('M1', 'M2'), 'M2': ('M1', 'M2', 'M3'), 'M3': ('M2', 'M3')}
    padr = {k: geo['pad'].get(k, db.Region()) & route[k] for k in GL}
    best = []
    for net in lay_nets:
        if net is nets['pad']:
            continue
        g = net_layers(net)
        m, where = 0.0, ''
        for k, pr in padr.items():
            if pr.is_empty():
                continue
            zone = pr.sized(int(DIST / u)) - pr
            for k2 in ADJ[k]:
                o = g.get(k2)
                if o is None:
                    continue
                for p in (o & zone).merged().each():
                    b = p.bbox()
                    if max(b.width(), b.height()) * u > m:
                        m = max(b.width(), b.height()) * u
                        where = '%s beside pad %s at %s' % (k2, k, b.to_dtype(u))
        if m > 0:
            best.append((m, sname.get(net.expanded_name(), net.expanded_name()).lower(), where))
    best.sort(reverse=True)
    print('\nlongest parallel run beside the pad net (same / adjacent metal, <= %.1f um), top 10:' % DIST)
    for m, n, w in best[:10]:
        print('  %-12s %6.1f um  (%s)' % (n, m, w))
