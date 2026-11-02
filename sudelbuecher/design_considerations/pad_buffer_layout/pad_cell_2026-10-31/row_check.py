# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Abutment checks of a pad cell against IHP's sg13cmos5l_io pads and fillers (C2, phase 1 and phase 4).

python3 row_check.py <pad.gds> <pad cell> <out dir>

Writes into <out dir>:
  edges.md   per layer, y intervals of the merged shapes on each cell edge (x = 0, x = 80), pad cell vs IOPadAnalog
  row.gds    Filler1000 | IOPadAnalog | pad | Filler200 | IOPadIOVdd | pad | Filler1000 (top cell 'row')
  nets.md    each ring rail and each band: is it one net through the row (klayout.db LayoutToNetlist)
DRC of row.gds is run separately: IHP's sg13cmos5l_maximal.drc (-rd latchUpRules=true) and run_drc.py (main tables, LU.b).
"""
import sys, os
import klayout.db as db

IO = '/foss/pdks/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds'
ROW = ['sg13cmos5l_Filler1000', 'sg13cmos5l_IOPadAnalog', 'PAD', 'sg13cmos5l_Filler200',
       'sg13cmos5l_IOPadIOVdd', 'PAD', 'sg13cmos5l_Filler1000']
WIDTH = {'sg13cmos5l_Filler1000': 5.0, 'sg13cmos5l_Filler200': 1.0}       # µm; pads 80 (prBoundary 189/4)
LAYERS = {'Activ': (1, 0), 'GatPoly': (5, 0), 'Cont': (6, 0), 'nSD': (7, 0), 'Metal1': (8, 0), 'Metal2': (10, 0),
          'pSD': (14, 0), 'Via1': (19, 0), 'Via2': (29, 0), 'Metal3': (30, 0), 'NWell': (31, 0),
          'Substrate': (40, 0), 'ThickGateOx': (44, 0), 'Via3': (49, 0), 'Metal4': (50, 0), 'TopVia1': (125, 0),
          'TopMetal1': (126, 0)}
# expected bands, edge to edge (brief C2, phase 1): name, layer test, y0, y1, rail
BANDS = [('NWell n+', 'ntap', 6.0, 61.0, 'iovdd'), ('p+ ring', 'ptap', 65.0, 84.4, 'iovss'),
         ('p+ plate', 'ptap', 84.5, 140.0, 'iovss'), ('n+ in NWell', 'ntap', 148.35, 148.65, 'iovdd'),
         ('p+', 'ptap', 156.85, 157.15, 'vss'), ('n+ in NWell', 'ntap', 166.85, 167.15, 'vdd')]


def edge_intervals(ly, cell, li, x):
    """y intervals (µm) of the merged shapes of layer li that cover the line x (µm)."""
    r = db.Region(cell.begin_shapes_rec(li)).merged()
    probe = db.Region(db.Box(int(round(x * 1000)) - 1, -10**6, int(round(x * 1000)) + 1, 10**6))
    return sorted((round(p.bbox().bottom / 1000, 3), round(p.bbox().top / 1000, 3)) for p in (r & probe).each())


def load(pad_gds, pad_cell):
    ly = db.Layout()
    ly.read(IO)
    pad = db.Layout()
    pad.read(pad_gds)
    target = ly.create_cell('PAD')
    target.copy_tree(pad.cell(pad_cell))
    return ly


def edges_md(ly, out):
    rows = []
    cells = ['PAD', 'sg13cmos5l_IOPadAnalog', 'sg13cmos5l_IOPadIOVdd', 'sg13cmos5l_IOPadIOVss',
             'sg13cmos5l_Filler200', 'sg13cmos5l_Filler1000']
    for name, ld in LAYERS.items():
        li = ly.find_layer(*ld)
        if li is None:
            continue
        for side in ('left', 'right'):
            iv = {}
            for c in cells:
                x = 0.0 if side == 'left' else WIDTH.get(c, 80.0)
                iv[c] = edge_intervals(ly, ly.cell(c), li, x)
            ref = iv['sg13cmos5l_IOPadAnalog']
            same = 'same' if iv['PAD'] == ref else 'DIFFERENT'
            rows.append((name, side, same, iv))
    with open(os.path.join(out, 'edges.md'), 'w') as f:
        f.write('# Shapes on the cell edges: y intervals (µm) per layer\n\n'
                '`same` = the pad cell has exactly IOPadAnalog\'s intervals on that edge. '
                'Fillers: left x = 0, right x = width.\n\n')
        f.write('| layer | edge | pad vs IOPadAnalog | pad cell | IOPadAnalog | IOPadIOVdd | IOPadIOVss | Filler200 | Filler1000 |\n')
        f.write('|---|---|---|---|---|---|---|---|---|\n')
        fmt = lambda v: ' '.join(f'{a:g}–{b:g}' for a, b in v) or '–'
        for name, side, same, iv in rows:
            f.write(f'| {name} | {side} | {same} | ' + ' | '.join(fmt(iv[c]) for c in cells) + ' |\n')
    return rows


def build_row(ly, out):
    top = ly.create_cell('row')
    x = 0.0
    for name in ROW:
        top.insert(db.DCellInstArray(ly.cell(name).cell_index(), db.DTrans(x, 0)))
        x += WIDTH.get(name, 80.0)
    keep = set([top.cell_index()]) | set(top.called_cells())
    for c in [c.cell_index() for c in ly.each_cell()]:
        if c not in keep:
            ly.delete_cell(c)
    ly.write(os.path.join(out, 'row.gds'))
    return top, x


def nets_md(ly, top, length, out):
    # extract on a flat copy: in a hierarchical extraction, net names of different subcircuits collide in `names`
    flat = db.Layout(); flat.dbu = ly.dbu
    ftop = flat.create_cell('row'); ftop.copy_tree(top); ftop.flatten(True)
    src, ly, top = ly, flat, ftop
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, top, []))
    L = {n: l2n.make_layer(ly.layer(*ld), n) for n, ld in LAYERS.items()}
    activ = L['Activ'] - L['GatPoly']
    ntap = (activ & L['NWell']) - L['pSD']
    ptap = (activ & L['pSD']) - L['NWell']
    l2n.register(ntap, 'ntap'); l2n.register(ptap, 'ptap')
    stack = [ntap, L['Cont'], L['Metal1'], L['Via1'], L['Metal2'], L['Via2'], L['Metal3'], L['Via3'], L['Metal4'],
             L['TopVia1'], L['TopMetal1']]
    l2n.connect(L['NWell']); l2n.connect(L['NWell'], ntap)
    for a, b in zip(stack[1:], stack[2:]):
        l2n.connect(a, b)
    l2n.connect(L['Cont'], ntap); l2n.connect(L['Cont'], ptap)
    for n in ('Metal1', 'Metal2', 'Metal3', 'Metal4', 'TopMetal1'):
        l2n.connect(L[n])
    l2n.extract_netlist()
    circ = l2n.netlist().circuit_by_name('row')
    lines = ['# One net through the row?\n', f'Row length {length:g} µm. A band passes if every cell of the row has '
             'shapes of it in the band\'s y range and all of them are one net; the net\'s M3 / M4 / TM1 rail is '
             'named by the labels (x/25) on it. A band or rail passes if one net is present in every cell of the row.\n',
             '| what | y (µm) | expected rail | cells with shapes | nets | result |', '|---|---|---|---|---|---|']
    xs, x = [], 0.0
    for name in ROW:
        w = WIDTH.get(name, 80.0); xs.append((name, x, x + w)); x += w

    def nets_in(layer, y0, y1):
        found = {}
        for name, xa, xb in xs:
            probe = db.Region(db.DBox(xa + 0.01, y0, xb - 0.01, y1).to_itype(ly.dbu))
            hit = set()
            for net in circ.each_net():
                r = l2n.shapes_of_net(net, layer, True)
                if not (r & probe).is_empty():
                    hit.add(net.expanded_name())
            found[f'{name}@{xa:g}'] = hit
        return found

    names = {}
    for mname in ('Metal1', 'Metal2', 'Metal3', 'Metal4', 'TopMetal1'):
        tl = ly.find_layer(LAYERS[mname][0], 25)
        if tl is None:
            continue
        for it in top.begin_shapes_rec(tl).each():
            if it.shape().is_text():
                t = it.shape().text.transformed(it.trans())
                net = l2n.probe_net(L[mname], db.Point(t.x, t.y))
                if net:
                    names.setdefault(net.expanded_name(), set()).add(t.string)
    names = {k: '/'.join(sorted(v)) for k, v in names.items()}

    def label(f):
        common = set.intersection(*f.values())
        return ' (' + ', '.join(names.get(n, '?') for n in sorted(common)) + ')' if common else ''

    def detail(f):
        ids = {}
        for v in f.values():
            for n in sorted(v):
                ids.setdefault(n, len(ids) + 1)
        return '; '.join(f'n{i} = {names.get(n, "?")}' for n, i in ids.items()) + ' — ' + ', '.join(k.split('@')[0].replace('sg13cmos5l_', '') + ' ' + ('/'.join(f'n{ids[n]}' for n in sorted(v)) or '–')
                         for k, v in f.items())

    # rails: the ring metals as bands of M3 (the rails' y ranges are read from IOPadAnalog's left edge)
    for name, test, y0, y1, rail in BANDS:
        f = nets_in(ntap if test == 'ntap' else ptap, y0, y1)
        allnets = set().union(*f.values())
        have = sum(1 for v in f.values() if v)
        ok = bool(set.intersection(*f.values()))
        lines.append(f'| {name} | {y0:g}–{y1:g} | {rail} | {have} of {len(f)} | {len(allnets)} | {"pass" + label(f) if ok else "FAIL: " + detail(f)} |')
    for mname in ('Metal3', 'Metal4', 'TopMetal1'):
        for y0, y1 in edge_intervals(src, src.cell('sg13cmos5l_IOPadAnalog'), src.find_layer(*LAYERS[mname]), 0.0):
            f = nets_in(L[mname], y0 + 0.05, y1 - 0.05)
            allnets = set().union(*f.values())
            have = sum(1 for v in f.values() if v)
            ok = bool(set.intersection(*f.values()))
            lines.append(f'| {mname} rail | {y0:g}–{y1:g} | | {have} of {len(f)} | {len(allnets)} | {"pass" + label(f) if ok else "FAIL: " + detail(f)} |')
    with open(os.path.join(out, 'nets.md'), 'w') as fo:
        fo.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    pad_gds, pad_cell, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    ly = load(pad_gds, pad_cell)
    edges_md(ly, out)
    top, length = build_row(ly, out)
    nets_md(ly, top, length, out)
    print(open(os.path.join(out, 'nets.md')).read())
