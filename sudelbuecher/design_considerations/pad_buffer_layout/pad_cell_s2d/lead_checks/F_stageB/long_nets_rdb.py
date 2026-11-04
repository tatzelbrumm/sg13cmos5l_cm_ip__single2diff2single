# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Marker database of chosen nets of a matched LVS run, for KLayout's Marker Browser (C3, lead).

python3 long_nets_rdb.py <run.lvsdb> <layout.gds> <out.lyrdb> <net> [<net> ...]

Nets are named by their schematic names; the layout nets come from the LVS cross-reference, so internal nets without a
layout label work too. The deck's conductor layers are derived (no GDS number), so each of the net's layers is named
by the GDS layer of the layout its shapes lie on (Metal1 8/0, Via1 19/0, Metal2 10/0, Via2 29/0, Metal3 30/0).
One category per net, one item per layer, shapes in top-cell coordinates; the item's first value gives the area.
"""
import sys
import klayout.db as db, klayout.rdb as rdb
lvsdb, gds, out, names = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
l = db.LayoutVsSchematic(); l.read(lvsdb)
top_name = 'sg13cmos5l_IOPadSingle2Diff'
pair = next(p for p in l.xref().each_circuit_pair() if p.first() and p.first().name == top_name)
by_schem = {np.second().name.lower(): np.first() for np in l.xref().each_net_pair(pair) if np.first() and np.second()}
G = db.Layout(); G.read(gds); gt = G.cell(top_name)
# cut layers first: a contact or via also lies inside its metals
METAL = {'Cont': (6, 0), 'Via1': (19, 0), 'Via2': (29, 0), 'Metal1': (8, 0), 'Metal2': (10, 0), 'Metal3': (30, 0)}
gr = {k: db.Region(gt.begin_shapes_rec(G.find_layer(*v))).merged() for k, v in METAL.items()}
dbu = l.internal_layout().dbu
assert abs(dbu - G.dbu) < 1e-12
db_ = rdb.ReportDatabase('long nets'); db_.top_cell_name = top_name
cell = db_.create_cell(top_name)
for name in names:
    cat = db_.create_category(name)
    net = by_schem.get(name.lower())
    if net is None:
        cat.description = 'not in the LVS cross-reference'; continue
    acc = {}
    for ln in l.layer_names():
        r = l.shapes_of_net(net, l.layer_by_name(ln), True).merged()
        if r.is_empty():
            continue
        lay = next((k for k, g in gr.items() if (r - g).is_empty()), None)
        if lay in (None, 'Cont'):
            continue                                  # device, implant and contact layers of the net: not shown
        acc[lay] = (acc.get(lay, db.Region()) + r).merged()
    for lay in ('Metal1', 'Via1', 'Metal2', 'Via2', 'Metal3'):
        if lay not in acc:
            continue
        r = acc[lay]
        it = db_.create_item(cell.rdb_id(), cat.rdb_id())
        it.add_value(f'{lay}: {r.area() * dbu * dbu:.2f} µm² in {r.count()} shapes')
        for p in r.each():
            it.add_value(p.to_dtype(dbu))
    cat.description = f'net {name} (LVS cross-reference)'
db_.save(out)
print('wrote', out, '| nets found:', {n: (n.lower() in by_schem) for n in names})
