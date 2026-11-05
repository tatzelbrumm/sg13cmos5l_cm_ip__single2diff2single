# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F's _f copies against the primitives they come from: XOR per layer (flattened). Only the layers named in each
cell's change list may differ.   python3 xor_cells.py <p3.gds> <n3.gds> <s2d_pins_f.gds> <s2d_casc_n_f.gds>"""
import sys

import klayout.db as db

p3, n3, pf, cnf = sys.argv[1:5]
PAIRS = [(p3, 's2d_loads_c3', pf, 's2d_loads_f'), (p3, 's2d_casc_p_c3', pf, 's2d_casc_p_f'),
         (n3, 's2d_casc_n_c3', cnf, 's2d_casc_n_f')]
for fa, ca, fb, cb in PAIRS:
    a = db.Layout(); a.read(fa)
    b = db.Layout(); b.read(fb)
    keys = {(a.get_info(i).layer, a.get_info(i).datatype) for i in a.layer_indexes()} | \
           {(b.get_info(i).layer, b.get_info(i).datatype) for i in b.layer_indexes()}
    diff = []
    for l, d in sorted(keys):
        ra = db.Region(a.cell(ca).begin_shapes_rec(a.layer(l, d)))
        rb = db.Region(b.cell(cb).begin_shapes_rec(b.layer(l, d)))
        x = ra ^ rb
        if not x.is_empty():
            diff.append('%d/%d %.4f um2' % (l, d, x.area() * a.dbu ** 2))
    print('%s vs %s: %s' % (cb, ca, ', '.join(diff) if diff else 'identical'))
