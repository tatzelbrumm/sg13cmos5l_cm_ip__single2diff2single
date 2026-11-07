# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): frame_f = prBoundary (0, 0, W, H) of pad_ref_rb plus F's own router terminals
(rb_place.FPINS, Metal2 with pin boxes and texts).
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
for net, (x0, y0, x1, y1) in g.get('FPINS', []):      # router terminals drawn by F (e.g. a strap's landing)
    b = db.DBox(x0, y0, x1, y1)
    for ld in ((10, 0), (10, 2)):
        c.shapes(ly.layer(*ld)).insert(b)
    c.shapes(ly.layer(10, 25)).insert(db.DText(net, (x0 + x1) / 2, (y0 + y1) / 2))
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[2], opt)
print('frame_f %.3f x %.3f' % (W, H))
