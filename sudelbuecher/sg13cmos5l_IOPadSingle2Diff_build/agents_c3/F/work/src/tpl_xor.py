# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""The template is untouched (brief rule 5): XOR, layer by layer, of the template's top cell against placement_A's
top cell with F's placed instances removed; also lists F's instances.   python3 tpl_xor.py <template.gds> <placement_A.gds>"""
import sys

import klayout.db as db

TOP = 'sg13cmos5l_IOPadSingle2Diff'
a = db.Layout(); a.read(sys.argv[1])
b = db.Layout(); b.read(sys.argv[2])
tpl_children = {a.cell(i).name for i in a.cell(TOP).each_child_cell()}
bt = b.cell(TOP)
mine = [i for i in bt.each_inst() if i.cell.name not in tpl_children]
for i in mine:
    i.delete()
diff = 0
infos = {(a.get_info(li).layer, a.get_info(li).datatype) for li in a.layer_indexes()}
infos |= {(b.get_info(li).layer, b.get_info(li).datatype) for li in b.layer_indexes()}
for l, d in sorted(infos):
    ra = db.Region(a.cell(TOP).begin_shapes_rec(a.layer(l, d)))
    rb = db.Region(bt.begin_shapes_rec(b.layer(l, d)))
    x = ra ^ rb
    if not x.is_empty():
        diff += 1
        print('layer %d/%d differs: %s' % (l, d, x.bbox().to_dtype(0.001)))
print('removed %d placed instances; template layers differing: %d' % (len(mine), diff))
