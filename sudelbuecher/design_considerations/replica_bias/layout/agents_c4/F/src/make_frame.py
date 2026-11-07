# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): frame_f = prBoundary (0, 0, W, H) of pad_ref_rb plus the supply rails on the left edge:
vssh (outer) and vddh (inner), Metal2, 1.0 um wide, with pin boxes and texts (the macro's power pins).
    python3 make_frame.py <rb_place.py> <out.gds>"""
import sys

import klayout.db as db

g = {}
exec(open(sys.argv[1]).read(), g)
W, H = g['W'], g['H']
ly = db.Layout()
ly.dbu = 0.001
c = ly.create_cell('frame_f')
c.shapes(ly.layer(189, 4)).insert(db.DBox(0, 0, W, H))
for net, x0 in (('vssh', 0.30), ('vddh', 1.80)):
    b = db.DBox(x0, 0.5, x0 + 1.0, H - 0.5)
    for ld in ((10, 0), (10, 2)):
        c.shapes(ly.layer(*ld)).insert(b)
    c.shapes(ly.layer(10, 25)).insert(db.DText(net, x0 + 0.5, H / 2))
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[2], opt)
print('frame_f %.3f x %.3f' % (W, H))
