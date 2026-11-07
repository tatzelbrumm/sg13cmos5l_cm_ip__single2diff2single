# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): every row cell placed in pad_ref_rb against the specialists' delivered cell, all layers
(shapes XOR, texts compared apart from the vdd / vss -> vddh / vssh renaming).
    python3 row_xor.py <pad_ref_rb.gds> <P3 gds> <P gds> <N gds>"""
import sys

import klayout.db as db

out = db.Layout()
out.read(sys.argv[1])
src = {}
for f in sys.argv[2:]:
    ly = db.Layout()
    ly.read(f)
    for c in ly.each_cell():
        src.setdefault(c.name, (ly, c))
REN = {'vdd': 'vddh', 'vss': 'vssh'}
for name in ('rb_tree_p', 'rb_tails', 'rb_tubs', 'rb_avg', 'rb_tree_n', 'rb_casc', 'rb_mirror', 'rb_cload', 'bypass_rb'):
    a = out.cell(name)
    if a is None:
        print('%-10s not placed (replaced by an _f copy)' % name)
        continue
    ly, b = src[name]
    diff = []
    for li in out.layer_indexes():
        info = out.get_info(li)
        lb = ly.find_layer(info.layer, info.datatype)
        ra = db.Region(a.begin_shapes_rec(li))
        rb = db.Region(b.begin_shapes_rec(lb)) if lb is not None else db.Region()
        x = (ra ^ rb)
        if not x.is_empty():
            diff.append('%d/%d %.4f um2' % (info.layer, info.datatype, x.area() * 1e-6))
        ta = sorted((s.text_string, s.text.x, s.text.y) for s in a.shapes(li).each() if s.is_text())
        tb = sorted((REN.get(s.text_string, s.text_string), s.text.x, s.text.y) for s in b.shapes(lb).each()
                    if s.is_text()) if lb is not None else []
        if ta != tb:
            diff.append('%d/%d texts differ' % (info.layer, info.datatype))
    print('%-10s %s' % (name, 'identical to the delivered cell (texts: vdd/vss -> vddh/vssh)' if not diff else '; '.join(diff)))
