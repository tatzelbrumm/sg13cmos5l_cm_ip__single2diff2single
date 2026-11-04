# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# usage: python3 via2_rails.py <gds> <top cell>
# Via2 between M2 and the M3 iovdd rails (66-91.5, 93.5-119), and where their M2 comes from
import sys, klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1]); top = ly.cell(sys.argv[2])
l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, top, []))
L = {k: l2n.make_layer(ly.find_layer(*v), k) for k, v in
     {'m1': (8, 0), 'v1': (19, 0), 'm2': (10, 0), 'v2': (29, 0), 'm3': (30, 0)}.items()}
for a, b in (('m1', 'v1'), ('v1', 'm2'), ('m2', 'v2'), ('v2', 'm3')):
    l2n.connect(L[a], L[b])
for k in ('m1', 'm2', 'm3'):
    l2n.connect(L[k])
l2n.extract_netlist()
v2 = db.Region(top.begin_shapes_rec(ly.find_layer(29, 0)))
for y0, y1 in ((66, 91.5), (93.5, 119)):
    rail = db.Region(db.DBox(0, y0, 80, y1).to_itype(ly.dbu))
    inside = v2 & rail
    print(f'M3 iovdd rail y {y0}-{y1}: {inside.count()} Via2')
    # group by the x range of the M2 shape each via sits on
    m2 = db.Region(top.begin_shapes_rec(ly.find_layer(10, 0))).merged()
    groups = {}
    for p in inside.each():
        for q in m2.interacting(db.Region(p)).each():
            b = q.bbox().to_dtype(ly.dbu)
            groups.setdefault(f'M2 x {b.left:.2f}-{b.right:.2f}, y {b.bottom:.2f}-{b.top:.2f}', []).append(1)
    for k, v in sorted(groups.items()):
        print(f'    {len(v):4d} Via2 on {k}')
