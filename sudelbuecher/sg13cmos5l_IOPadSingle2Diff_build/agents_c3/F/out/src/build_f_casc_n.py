# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_f_casc_n.py (F, C3 stage B): s2d_casc_n_f = N's s2d_casc_n_c3 with exits for xc / yc at the band end.

    python3 build_f_casc_n.py <s2d_n3_cells.gds> <s2d_n3_cells.cdl> <out.gds> <out.cdl>

In the pad, casc_n stands R270 in the left pocket with its band end (R0 left edge: band, x, y) at the top. N drew
xc / yc pins only at the far end. Change: the two full-length source levels of xc (Metal2 y -1.44 .. -1.15, below
row 1, from x 9.945) and yc (Metal2 y 11.10 .. 11.39, above row 2, from x 8.445) run on in Metal2 to the band-end
edge (x -2.52), with an M2 pin each (datatype 2 box + datatype 25 text). Their neighbours y (-0.94 .. -0.65) and x
(10.60 .. 10.89) stay Mn.b 0.21 away (sg13cmos5l_tech_default.json Mn_b); they cross only Metal1 (the dummies'
plates, the x / y verticals, the ring). No device layer changes; the netlist is N's (subckt renamed).
"""
import sys

import klayout.db as db

NG, NC, OG, OC = sys.argv[1:5]
src = db.Layout()
src.read(NG)
ly = db.Layout()
ly.dbu = src.dbu
c = ly.create_cell('s2d_casc_n_f')
c.copy_tree(src.cell('s2d_casc_n_c3'))
M2, M2P, M2T = ly.layer(10, 0), ly.layer(10, 2), ly.layer(10, 25)
for net, (y0, y1), x_end in (('xc', (-1.44, -1.15), 9.945), ('yc', (11.10, 11.39), 8.445)):
    c.shapes(M2).insert(db.DBox(-2.52, y0, x_end, y1))
    c.shapes(M2P).insert(db.DBox(-2.52, y0, -2.02, y1))
    c.shapes(M2T).insert(db.DText(net, -2.27, round((y0 + y1) / 2, 3)))
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(OG, opt)
out, keep = [], False
for line in open(NC):
    t = line.split()
    if t and t[0].upper() == '.SUBCKT':
        keep = t[1] == 's2d_casc_n_c3'
        if keep:
            line = line.replace('s2d_casc_n_c3', 's2d_casc_n_f', 1)
    if keep:
        out.append(line.rstrip('\n').replace('.ENDS s2d_casc_n_c3', '.ENDS s2d_casc_n_f'))
    if t and t[0].upper() == '.ENDS':
        keep = False
open(OC, 'w').write('* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n'
                    '* s2d_casc_n_f: N\'s s2d_casc_n_c3 netlist, renamed (build_f_casc_n.py, C3 stage B)\n'
                    + '\n'.join(out) + '\n')
print('s2d_casc_n_f', c.dbbox())
