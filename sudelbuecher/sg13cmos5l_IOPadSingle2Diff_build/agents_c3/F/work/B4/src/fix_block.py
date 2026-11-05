# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B: post-route trim of s2d_block (in place).   python3 fix_block.py <s2d_block.gds>

The router lands on a cell track with its 0.29 um node square. On the inputs' gate band (six Metal2 tracks 0.26 wide
at 0.48 pitch, P's TP) that square sticks out 0.015 um on each side and leaves 0.205 um to the next track (Mn_b 0.21,
measured by run_drc.py: M2.b). Fix: the router's own Metal2 (top cell only) loses whatever lies in the five gaps
between the band tracks, inside the inputs (x 4.30 .. 51.88: wires outside, e.g. the vertical runs beside the cell,
stay whole); a landing then is exactly track wide (0.26 >= Mn_a 0.20). The gaps hold no other Metal2:
a router wire cannot cross the band, so only the slivers go."""
import sys

import klayout.db as db

ly = db.Layout()
ly.read(sys.argv[1])
top = ly.cell('s2d_block')
M2 = ly.layer(10, 0)
Y0 = 26.0                                   # block -> pad
gaps = db.Region()
for i in range(5):                          # band tracks at pad y 134.40 + 0.48 i (+-0.13), inputs at (4.30, 122.40)
    gaps.insert(db.DBox(4.30, 134.53 + 0.48 * i - Y0, 51.88, 134.75 + 0.48 * i - Y0).to_itype(ly.dbu))
r = db.Region(top.shapes(M2))
cut = r & gaps
top.shapes(M2).clear()
top.shapes(M2).insert((r - gaps).merged())
# stage B2: a router landing that meets F's drawn wiring (pwr_f) at a corner can leave a neck below Mn_a 0.20 (measured:
# M2.a 0.16 at one link). Each such neck gets a fill box (the neck's box grown to 0.20 across), kept only where it
# stays Mn_b 0.21 from every other polygon of Metal2.
MW, MS = int(round(0.20 / ly.dbu)), int(round(0.21 / ly.dbu))
allm2 = db.Region(top.begin_shapes_rec(M2)).merged()
add = db.Region()
for ep in allm2.width_check(MW).each():
    b = ep.bbox()
    if b.width() < b.height():
        g = (MW - b.width() + 1) // 2
        nb = db.Box(b.left - g, b.bottom, b.right + g, b.top)
    else:
        g = (MW - b.height() + 1) // 2
        nb = db.Box(b.left, b.bottom - g, b.right, b.top + g)
    own = allm2.interacting(db.Region(nb))
    if (db.Region(nb).sized(MS) & (allm2 - own)).is_empty():
        add.insert(nb)
if not add.is_empty():
    top.shapes(M2).insert(add.merged())
print('fix_block: %d Metal2 neck fill(s)' % add.count())
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[1], opt)
print('fix_block: trimmed %.4f um2 of router Metal2 in the band gaps (%d pieces)' % (cut.area() * ly.dbu ** 2,
                                                                                   cut.count()))
