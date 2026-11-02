# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Current paths of the pad net and the rails: metal width crossing horizontal cut lines, per layer (C2, phase 1 / 4).

python3 path_widths.py <gds> <cell> <y1,y2,...> [net ...]      (defaults: pad iovss iovdd)

For each named net (by its x/25 labels) and each cut line y, the summed width (µm) of the net's merged shapes that
cross the line, per metal, and the via counts of the net between consecutive cut lines.
"""
import sys
import klayout.db as db

STACK = [('Cont', 6), ('Metal1', 8), ('Via1', 19), ('Metal2', 10), ('Via2', 29), ('Metal3', 30), ('Via3', 49),
         ('Metal4', 50), ('TopVia1', 125), ('TopMetal1', 126)]
METALS = ['Metal1', 'Metal2', 'Metal3', 'Metal4', 'TopMetal1']


def extract(ly, cell):
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, cell, []))
    L = {n: l2n.make_layer(ly.layer(g, 0), n) for n, g in STACK}
    act = l2n.make_layer(ly.layer(1, 0), 'Activ') - l2n.make_layer(ly.layer(5, 0), 'GatPoly')
    nw = l2n.make_layer(ly.layer(31, 0), 'NWell')
    l2n.register(act, 'act')
    l2n.connect(act); l2n.connect(nw); l2n.connect(act & nw, nw)
    l2n.connect(act, L['Cont'])
    names = [n for n, _ in STACK]
    for a, b in zip(names, names[1:]):
        l2n.connect(L[a], L[b])
    for m in METALS:
        l2n.connect(L[m])
    l2n.extract_netlist()
    nets = {}
    for m in METALS:
        tl = ly.find_layer(dict(STACK)[m], 25)
        if tl is None:
            continue
        for it in cell.begin_shapes_rec(tl).each():
            if it.shape().is_text():
                t = it.shape().text.transformed(it.trans())
                n = l2n.probe_net(L[m], db.Point(t.x, t.y))
                if n:
                    nets.setdefault(t.string, set()).add(n.cluster_id)
    return l2n, L, nets


def net_region(l2n, L, cids, layer):
    r = db.Region()
    circ = l2n.netlist().top_circuit()
    for net in circ.each_net():
        if net.cluster_id in cids:
            r += l2n.shapes_of_net(net, L[layer], True)
    return r.merged()


if __name__ == '__main__':
    gds, cellname, ys = sys.argv[1], sys.argv[2], [float(v) for v in sys.argv[3].split(',')]
    which = sys.argv[4:] or ['pad', 'iovss', 'iovdd']
    ly = db.Layout(); ly.read(gds)
    cell = ly.cell(cellname)
    l2n, L, nets = extract(ly, cell)
    print(f'## {cellname}\n')
    for name in which:
        cids = nets.get(name, set())
        print(f'### net {name} ({len(cids)} labelled cluster(s))\n')
        print('| cut y (µm) | ' + ' | '.join(METALS) + ' |\n|---|' + '---|' * len(METALS))
        regs = {m: net_region(l2n, L, cids, m) for m in METALS}
        for y in ys:
            line = db.Region(db.DBox(-1, y - 0.001, 81, y + 0.001).to_itype(ly.dbu))
            w = [sum(p.bbox().width() for p in (regs[m] & line).each()) * ly.dbu for m in METALS]
            print(f'| {y:g} | ' + ' | '.join(f'{v:.2f}' for v in w) + ' |')
        print('\n| between y (µm) | ' + ' | '.join(v for v, _ in STACK if v.startswith(('Via', 'TopVia'))) + ' |')
        print('|---|' + '---|' * 4)
        for y0, y1 in zip(ys, ys[1:]):
            band = db.Region(db.DBox(-1, y0, 81, y1).to_itype(ly.dbu))
            cnt = [(net_region(l2n, L, cids, v) & band).count() for v, _ in STACK if v.startswith(('Via', 'TopVia'))]
            print(f'| {y0:g}–{y1:g} | ' + ' | '.join(str(c) for c in cnt) + ' |')
        print()
