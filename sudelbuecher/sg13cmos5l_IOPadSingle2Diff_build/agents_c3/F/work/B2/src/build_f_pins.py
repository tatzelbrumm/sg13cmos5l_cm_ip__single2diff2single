# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_f_pins.py (F, C3 stage B): s2d_loads_f and s2d_casc_p_f = P's cells with staggered pin tracks.

    python3 build_f_pins.py <s2d_p3_cells.gds> <s2d_p3_cells.cdl> <out.gds> <out.cdl>

P's edge pins sit on Metal2 tracks 0.20 wide at 0.41 pitch (Mn_a 0.20 + Mn_b 0.21). The router lands with 0.29 um
squares (Via1 0.19 + 2 x V1_c1 0.05), so the middle track of three is unreachable at the edge (measured: loads.dd and
casc_p.voutp enclosed). Change, Metal2 only: some tracks run on beyond the pin edge (R0 x = 0), so that every pin
has a free landing: each triple of tracks fans out beyond the pin edge (R0 x = 0, outside the cell): the middle
track runs straight on to x -1.6, the outer two run 0.6 out, jog 0.6 away from the middle (0.2 wide, Mn_b 0.21 from
the middle track) and run on to x -1.6. The three tips are then 1.01 / 1.01 apart.
  s2d_loads_f:  lp / dd / ln (y 5.65 / 6.06 / 6.47)
  s2d_casc_p_f: dd / ln / lp (1.185 / 1.595 / 2.005) and voutp / vcmfb / voutn (5.895 / 6.305 / 6.715)
No device layer, Metal1 or Via1 changes; the netlists are P's (subckts renamed).
"""
import sys

import klayout.db as db

PG, PC, OG, OC = sys.argv[1:5]
EXT = {'s2d_loads_c3': ('s2d_loads_f', [5.65]), 's2d_casc_p_c3': ('s2d_casc_p_f', [1.185, 5.895])}
W, OUT, JOG, END = 0.20, 0.6, 0.6, -1.6     # track width, straight run, jog, tip


def fan(c, y0):
    """triple of 0.20 tracks at y0, y0 + 0.41, y0 + 0.82 (bottom edges), all ending at x = 0"""
    m = c.shapes(c.layout().layer(10, 0))
    m.insert(db.DBox(END, y0 + 0.41, 0.0, y0 + 0.41 + W))                    # middle: straight on
    for yb, s in ((y0, -1), (y0 + 0.82, 1)):                                 # outer: out, jog away, on
        yj = yb + s * JOG
        m.insert(db.DBox(-OUT, yb, 0.0, yb + W))
        m.insert(db.DBox(-OUT - W, min(yb, yj), -OUT, max(yb, yj) + W))
        m.insert(db.DBox(END, yj, -OUT, yj + W))
src = db.Layout()
src.read(PG)
ly = db.Layout()
ly.dbu = src.dbu
for old, (new, exts) in EXT.items():
    c = ly.create_cell(new)
    c.copy_tree(src.cell(old))
    for y0 in exts:
        fan(c, y0)
    print(new, c.dbbox())
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(OG, opt)
out, keep = [], None
for line in open(PC):
    t = line.split()
    if t and t[0].upper() == '.SUBCKT':
        keep = EXT.get(t[1], (None,))[0]
        if keep:
            line = line.replace(t[1], keep, 1)
    if keep:
        out.append(line.rstrip('\n'))
        if t and t[0].upper() == '.ENDS':
            out[-1] = '.ENDS ' + keep
            out.append('')
            keep = None
open(OC, 'w').write('* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n'
                    '* s2d_loads_f / s2d_casc_p_f: P\'s netlists, renamed (build_f_pins.py, C3 stage B)\n'
                    + '\n'.join(out) + '\n')
