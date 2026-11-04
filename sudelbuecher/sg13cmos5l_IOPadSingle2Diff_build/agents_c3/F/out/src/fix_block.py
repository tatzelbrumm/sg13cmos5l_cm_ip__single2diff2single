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
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[1], opt)
print('fix_block: trimmed %.4f um2 of router Metal2 in the band gaps (%d pieces)' % (cut.area() * ly.dbu ** 2,
                                                                                   cut.count()))
