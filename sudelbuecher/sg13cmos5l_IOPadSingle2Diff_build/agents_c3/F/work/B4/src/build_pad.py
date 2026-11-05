# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B: the pad candidate sg13cmos5l_IOPadSingle2Diff = template v4 + the routed s2d_block.

    python3 build_pad.py <template.gds> <s2d_block.gds> <out_pad.gds>

- s2d_block (route_block.py) goes in at (0, 26) (the router moved it to the origin), without its padctx_f copy.
- Inside the block's cells, the local supply texts become the pad nets (C2 F2's relabel_block.py): vdd -> iovdd,
  vss -> iovss, and the router's supply groups iovdd_* -> iovdd, iovss_* -> iovss. In the flat pad, vdd / vss then
  name only the 1.2 V ring rails.
- Top-level ports as C2 learned them (C2_report.md 4.1 / 4.3): a text on datatype 25 and a pin box on datatype 2 for
  iovdd, iovss, vdd, pad (on the template's own Metal3 / Metal2 texts) and for the seven core-side pins (Metal2 at
  y 180, the block's port pins); no top-level vss text: the template's vss texts (Metal3 30/25, Metal4 50/25) are
  removed, because the vss band's p+ and the iovss ties share the substrate and a vss text names the joined net
  'iovss,vss' (KLayout's port check fails). No template geometry changes (drawing layers).
"""
import sys

import klayout.db as db

TPL, BLK, OUT = sys.argv[1:4]
TOP = 'sg13cmos5l_IOPadSingle2Diff'
CORE = ('outp', 'outn', 'vcm', 'vref', 'iref', 'en_3v3', 'en_3v3_b')
ly = db.Layout()
ly.read(TPL)
top = ly.cell(TOP)
b = db.Layout()
b.read(BLK)
blk = ly.create_cell('s2d_block')
blk.copy_tree(b.cell('s2d_block'))
for inst in list(blk.each_inst()):
    if inst.cell.name.startswith('padctx_f'):
        ci = inst.cell.cell_index()
        inst.delete()
        ly.delete_cell(ci)
top.insert(db.DCellInstArray(blk.cell_index(), db.DTrans(db.DVector(0, 26.0))))


def rename(n):
    if n == 'vdd' or n.startswith('iovdd_'):
        return 'iovdd'
    if n == 'vss' or n.startswith('iovss_'):
        return 'iovss'
    return n


count = 0
for ci in [blk.cell_index()] + list(blk.called_cells()):
    c = ly.cell(ci)
    for li in ly.layer_indexes():
        for s in list(c.shapes(li).each()):
            if s.is_text() and rename(s.text_string) != s.text_string:
                t = s.text
                t.string = rename(t.string)
                s.text = t
                count += 1
# top-level port texts / pins
for li in ly.layer_indexes():
    for s in list(top.shapes(li).each()):
        if s.is_text() and s.text_string == 'vss':
            top.shapes(li).erase(s)
pins = []
for li in ly.layer_indexes():
    inf = ly.get_info(li)
    if inf.datatype != 25:
        continue
    for s in top.shapes(li).each():
        if s.is_text() and s.text_string in ('iovdd', 'iovss', 'vdd', 'pad'):
            p = s.dtext
            pins.append((inf.layer, db.DBox(p.x - 0.25, p.y - 0.15, p.x + 0.25, p.y + 0.15)))
for l, bx in pins:
    top.shapes(ly.layer(l, 2)).insert(bx)
bt = db.DTrans(db.DVector(0, 26.0))
for s in blk.shapes(ly.layer(10, 25)).each():
    if s.is_text() and s.text_string in CORE:
        p = bt * db.DPoint(s.dtext.x, s.dtext.y)
        top.shapes(ly.layer(10, 25)).insert(db.DText(s.text_string, p.x, p.y))
for s in blk.shapes(ly.layer(10, 2)).each():
    if not s.is_text():
        bb = s.dbbox().transformed(bt)
        if bb.top > 179.99:
            top.shapes(ly.layer(10, 2)).insert(bb)
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(OUT, opt)
print('pad candidate:', OUT, top.dbbox(), 'block texts renamed:', count)
