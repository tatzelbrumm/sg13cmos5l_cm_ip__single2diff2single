# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): supply connectivity through metal only (Activ, Cont, M1, Via1, M2; no substrate, no well).
LVS joins every substrate tie through the substrate, so an NMOS row whose vss ring is not wired would still match;
this check finds each texted net's metal clusters and says whether all labels of one name sit on one cluster.
    python3 metal_conn.py <gds> <cell>"""
import sys

import klayout.db as db

ly = db.Layout()
ly.read(sys.argv[1])
top = ly.cell(sys.argv[2])
fl = db.Layout()
fl.dbu = ly.dbu
c = fl.create_cell('flat')
c.copy_tree(top)
c.flatten(-1, True)
l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(fl, c, []))
L = {}
for k, ld in (('act', (1, 0)), ('poly', (5, 0)), ('cont', (6, 0)), ('m1', (8, 0)), ('v1', (19, 0)), ('m2', (10, 0))):
    L[k] = l2n.make_layer(fl.layer(*ld), k)
sd = L['act'] - L['poly']
l2n.register(sd, 'sd')
for r in (sd, L['poly'], L['m1'], L['m2']):
    l2n.connect(r)
for a, b in ((sd, L['cont']), (L['poly'], L['cont']), (L['cont'], L['m1']), (L['m1'], L['v1']), (L['v1'], L['m2'])):
    l2n.connect(a, b)
l2n.extract_netlist()
bad = 0
names = {}
for ld, key in (((8, 25), 'm1'), ((10, 25), 'm2')):
    for s in c.shapes(fl.layer(*ld)).each():
        if s.is_text():
            n = l2n.probe_net(L[key], db.DPoint(s.text.x * fl.dbu, s.text.y * fl.dbu))
            names.setdefault(s.text_string, set()).add(n.cluster_id if n is not None else None)
for name, cl in sorted(names.items()):
    ok = len(cl) == 1 and None not in cl
    bad += not ok
    print('%-10s %d label(s) on %d metal cluster(s) %s' % (name, sum(1 for _ in cl), len(cl), 'ok' if ok else 'SPLIT'))
print('split nets:', bad)
