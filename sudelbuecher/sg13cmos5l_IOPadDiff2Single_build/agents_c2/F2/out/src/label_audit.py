# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 stage B2: list every text vdd / vss / vddo / vsso in a GDS (flattened, with the cell that holds it).
    python3 label_audit.py <gds> [top]"""
import sys
from collections import Counter

import klayout.db as db

ly = db.Layout()
ly.read(sys.argv[1])
top = ly.cell(sys.argv[2]) if len(sys.argv) > 2 else ly.top_cell()
NAMES = {"vdd", "vss", "vddo", "vsso"}
cnt = Counter()
for li in ly.layer_indexes():
    info = ly.get_info(li)
    it = top.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text() and s.text_string in NAMES:
            p = it.trans() * s.text.position()
            cnt[(s.text_string, "%d/%d" % (info.layer, info.datatype), it.cell().name)] += 1
            if len(sys.argv) > 3:
                print(s.text_string, info, it.cell().name, p.to_dtype(ly.dbu))
        it.next()
for k, v in sorted(cnt.items()):
    print("%-5s %-6s %-40s %d" % (k + (v,)))
