# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""make_bg_library_set.py: the six library primitives of bg_core_pd side by side (a picture / audit fixture, NOT a
layout: no wiring, 1 um apart), for the area audit and the 'before' panels. 2026-10-28, Claude (Opus 5.5).

    python3 make_bg_library_set.py <pad_buffer_cells.gds> <out.gds>
"""
import sys

import klayout.db as db

ROWS = [["bg_pmir_pcas", "bg_misc_p"], ["bg_nab", "bg_misc_n"], ["bg_res", "bg_pnp"]]   # top row first
src = db.Layout()
src.read(sys.argv[1])
ly = db.Layout()
ly.dbu = src.dbu
top = ly.create_cell("bg_library_set")
need = [n for r in ROWS for n in r]
for n in need:                                             # copy each cell tree (names kept, e.g. rhigh$1)
    c = ly.create_cell(n)
    c.copy_tree(src.cell(n))
y = 0.0
total = 0.0
for row in ROWS:
    h = max(src.cell(n).dbbox().height() for n in row)
    x = 0.0
    for n in row:
        b = src.cell(n).dbbox()
        top.insert(db.DCellInstArray(ly.cell(n).cell_index(), db.DTrans(x - b.left, y - h - b.bottom)))
        x += b.width() + 1.0
        total += b.width() * b.height()
    y -= h + 1.0
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[2], opt)
print("bg_library_set: %d primitives, sum of their boxes %.1f um2" % (len(need), total))
