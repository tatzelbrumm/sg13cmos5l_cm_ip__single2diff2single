# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): working material for routing-driven placement, measured from the rows' GDS.
    python3 pin_map.py <P3 gds> <P gds> <N gds> <pad_ref_rb.gds> <rb_place.py> <pin_map.md> <net_list.md> [<F gds>]
pin_map.md: every pin of every input cell (net, layer, edge, box in the cell's own frame).
net_list.md: per net the cells and pins it joins (placed coordinates in pad_ref_rb), fan-out, class."""
import sys

import klayout.db as db

FILES = sys.argv[1:4] + sys.argv[8:]
OUT_GDS, PLACE, PM, NL = sys.argv[4:8]
CELLS = ['rb_tree_p', 'rb_tails', 'rb_tubs', 'rb_avg', 'rb_tree_n', 'rb_casc', 'rb_mirror', 'rb_cload', 'bypass_rb', 'capr', 'capm', 'capt', 'capv']
src = {}
for f in FILES:
    ly = db.Layout()
    ly.read(f)
    for c in ly.each_cell():
        src.setdefault(c.name, (ly, c, f.split('/')[-1]))


def pins(ly, c):
    out = []
    for metal, (l, d) in (('M1', (8, 2)), ('M2', (10, 2))):
        li, lt = ly.find_layer(l, d), ly.find_layer(l, 25)
        if li is None or lt is None:
            continue
        boxes = [s.dbbox() for s in c.shapes(li).each() if not s.is_text()]
        for s in c.shapes(lt).each():
            if s.is_text():
                p = db.DPoint(s.text.x * ly.dbu, s.text.y * ly.dbu)
                hit = [b for b in boxes if b.contains(p)]
                if hit:
                    out.append((s.text_string, metal, min(hit, key=lambda b: b.area())))
    return out


def edge(b, bb):
    e = [n for n, v in (('left', abs(b.left - bb.left)), ('right', abs(b.right - bb.right)),
                        ('bottom', abs(b.bottom - bb.bottom)), ('top', abs(b.top - bb.top))) if v < 0.05]
    return '/'.join(e) if e else 'inside'


SENS = {'ni', 'vbp', 'vbnc', 'gh', 'm', 'xp', 'bd', 'ts', 'bt'}
OUTS = {'vcm': 'output (port)', 'vref': 'output (port)', 'iref': 'input (port, 5 uA sourced)',
        'en_3v3': 'input (port, enable)', 'en_3v3_b': 'input (port, enable)', 'vddh': 'supply (pin)', 'vssh': 'supply (pin)'}
with open(PM, 'w') as o:
    o.write('<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->\n')
    o.write('# Pin map of the input rows (Claude, agent F, C4; measured by pin_map.py from the delivered GDS)\n\n')
    o.write('Cell frame of each delivered cell (R0); edge = the bounding-box edge the pin box touches.\n\n')
    o.write('| cell (file) | size um | pin | net | layer | edge | box (x0, y0; x1, y1) |\n|---|---|---|---|---|---|---|\n')
    for name in CELLS:
        if name not in src:
            continue
        ly, c, f = src[name]
        bb = c.dbbox()
        for net, metal, b in sorted(pins(ly, c), key=lambda t: (t[0], t[2].left)):
            o.write('| %s (%s) | %.2f x %.2f | %s | %s | %s | %s | (%.3f, %.3f; %.3f, %.3f) |\n' % (
                name, f, bb.width(), bb.height(), net, {'vdd': 'vddh', 'vss': 'vssh'}.get(net, net), metal,
                edge(b, bb), b.left, b.bottom, b.right, b.top))
# placed pins
ly = db.Layout()
ly.read(OUT_GDS)
top = ly.cell('pad_ref_rb')
g = {}
exec(open(PLACE).read(), g)
nets = {}
for inst in top.each_inst():
    c = ly.cell(inst.cell_index)
    if c.name not in CELLS:
        continue
    o = [p[2] for p in g['PLACE'] if p[1] == c.name][0]
    for net, metal, b in pins(ly, c):
        pb = b.transformed(inst.dcplx_trans)
        nets.setdefault(net, []).append((c.name, o, metal, pb))
with open(NL, 'w') as o:
    o.write('<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->\n')
    o.write('# Net list of pad_ref_rb by cell pins (Claude, agent F, C4; measured by pin_map.py on out/pad_ref_rb.gds)\n\n')
    o.write('Placed pin boxes in pad_ref_rb coordinates (um). Fan-out = number of cells joined (+ the port where '
            'there is one). Sensitive = a bias or internal analog node of the replica (high impedance or matched).\n\n')
    o.write('| net | class | fan-out | cell (orientation): pin layer, box |\n|---|---|---:|---|\n')
    for net in sorted(nets, key=lambda n: (n in ('vddh', 'vssh'), n)):
        cells = sorted({p[0] for p in nets[net]})
        cls = 'sensitive' if net in SENS else OUTS.get(net, '')
        port = net in ('vcm', 'vref', 'iref', 'en_3v3', 'en_3v3_b')
        txt = '; '.join('%s (%s): %s (%.2f, %.2f; %.2f, %.2f)' % (cn, oo, m, b.left, b.bottom, b.right, b.top)
                        for cn, oo, m, b in sorted(nets[net], key=lambda t: t[0]))
        o.write('| %s | %s | %d%s | %s |\n' % (net, cls, len(cells), ' + port' if port else '', txt))
print('pin map: %s; nets: %d' % (PM, len(nets)))
