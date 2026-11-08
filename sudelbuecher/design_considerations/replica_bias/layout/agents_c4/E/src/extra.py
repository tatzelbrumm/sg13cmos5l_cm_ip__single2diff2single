# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""extra.py: measurements beyond DRC / LVS (Claude, agent D, C4 2026-11-07).
  poly  <gds> <cell>          width of every contacted GatPoly piece outside Activ (no endcap-zone subtraction)
  xor   <gdsA> <cellA> <gdsB> <cellB> [x0 y0 x1 y1]   per-layer XOR (cells aligned at their Activ bbox lower left)
  metal <gds> <cell>          supply connectivity through tie Activ, Cont, M1, Via1, M2 only (no well / substrate)
"""
import sys
import klayout.db as db
L = {'Activ': (1, 0), 'GatPoly': (5, 0), 'Cont': (6, 0), 'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0),
     'pSD': (14, 0), 'NWell': (31, 0), 'TGO': (44, 0)}


def load(g, n):
    ly = db.Layout(); ly.read(g); return ly, ly.cell(n)


def reg(ly, c, k):
    li = ly.find_layer(*L[k])
    return db.Region(c.begin_shapes_rec(li)).merged() if li is not None else db.Region()


a = sys.argv[1:]
if a[0] == 'poly':
    ly, c = load(a[1], a[2]); u = ly.dbu
    p = (reg(ly, c, 'GatPoly') - reg(ly, c, 'Activ')).interacting(reg(ly, c, 'Cont'))
    print('%s: %d contacted poly pieces outside Activ; width check 0.30 um: %d hits; narrowest piece %.3f um' % (
        a[2], p.count(), p.width_check(int(0.30 / u)).count(),
        min(min(q.bbox().width(), q.bbox().height()) for q in p.each()) * u))
elif a[0] == 'xor':
    la, ca = load(a[1], a[2]); lb, cb = load(a[3], a[4]); u = la.dbu
    oa, ob = reg(la, ca, 'Activ').bbox().p1, reg(lb, cb, 'Activ').bbox().p1
    win = db.Box(*[int(round(float(v) / u)) for v in a[5:9]]) if len(a) > 5 else None
    for k in ('Activ', 'GatPoly', 'Cont', 'pSD', 'NWell', 'TGO', 'M1', 'Via1', 'M2'):
        ra, rb = reg(la, ca, k).moved(-oa.x, -oa.y), reg(lb, cb, k).moved(-ob.x, -ob.y)
        if win:
            ra, rb = ra & db.Region(win), rb & db.Region(win)
        x = ra ^ rb
        print('  %-8s XOR %8.4f um2' % (k, x.area() * u * u))
elif a[0] == 'metal':
    ly, c = load(a[1], a[2])
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, c, []))
    tie = l2n.make_polygon_layer(ly.layer(*L['Activ']), 'act')
    gp = l2n.make_polygon_layer(ly.layer(*L['GatPoly']), 'gp')
    tie = tie - tie.interacting(gp)            # Activ pieces without a gate: the ties
    tie = l2n.make_polygon_layer(ly.layer(*L['Activ']), 'act2') & tie
    lay = {k: l2n.make_polygon_layer(ly.layer(*L[k]), k) for k in ('Cont', 'M1', 'Via1', 'M2')}
    t1 = l2n.make_text_layer(ly.layer(8, 25), 't1')
    l2n.register(tie, 'tie')
    for k, r in [('tie', tie)] + list(lay.items()):
        l2n.connect(r)
    l2n.connect(tie, lay['Cont']); l2n.connect(lay['Cont'], lay['M1']); l2n.connect(lay['M1'], lay['Via1'])
    l2n.connect(lay['Via1'], lay['M2']); l2n.connect(lay['M1'], t1)
    l2n.extract_netlist()
    nl = l2n.netlist(); top = nl.circuit_by_name(a[2])
    nets = {}
    for n in top.each_net():
        r = l2n.shapes_of_net(n, tie, True)
        if r.count():
            nets[n.expanded_name()] = r.area() * ly.dbu ** 2
    print('%s: nets holding tie Activ (metal + tie Activ only): %d' % (a[2], len(nets)))
    for k, v in sorted(nets.items()):
        print('   %-12s tie area %8.2f um2' % (k, v))
