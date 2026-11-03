# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 stage B: the pad-top context of the block, as a cell for the router and the block's own LVS.

    python3 make_ctx.py <pad_ctx.gds> <out.gds>

padtop_ctx_f2: the pad's Metal1 / Via1 / Metal2 in x 0 .. 80, y 84 .. 180 (a / b joins, dabp / dabn stubs, the NWell
isolator's taps, the edge stubs), flattened and clipped, with pin labels on the joins and stubs; copies of the
Metal3 ring rails (iovdd 84 .. 91.5 and 93.5 .. 119, iovss 126 .. 134) for the block's LVS; the vfb landing of the
pad-level Kelvin line (Metal2 x 1.90 .. 2.20, y 88.25 .. 88.85; rejected F's vfb_kelvin); a prBoundary box
(0, 84, 80, 180) that fixes the block's extent. In the pad the cell is dropped: the pad has all of it.
"""
import sys

import klayout.db as db

src, out = sys.argv[1:3]
s = db.Layout()
s.read(src)
top = s.top_cell()
ly = db.Layout()
ly.dbu = s.dbu
c = ly.create_cell("padtop_ctx_f2")
clip = db.Region(db.DBox(0, 84.0, 80, 180.0).to_itype(s.dbu))
L = lambda l, d: ly.layer(l, d)
for (l, d) in ((8, 0), (19, 0), (10, 0)):
    li = s.find_layer(l, d)
    r = (db.Region(top.begin_shapes_rec(li)) & clip).merged()
    c.shapes(L(l, d)).insert(r)


def pin(l, net, x0, y0, x1, y1):
    c.shapes(L(l, 2)).insert(db.DBox(x0, y0, x1, y1))
    c.shapes(L(l, 25)).insert(db.DText(net, (x0 + x1) / 2, (y0 + y1) / 2))


pin(10, "a", 20.0, 86.4, 20.5, 87.0)
pin(10, "b", 20.0, 87.4, 20.5, 88.0)
pin(10, "dabn", 38.15, 85.0, 38.45, 85.5)
pin(10, "dabp", 38.94, 85.0, 39.55, 85.5)
c.shapes(L(10, 0)).insert(db.DBox(1.90, 88.25, 2.20, 88.85))       # vfb landing (pad-level Kelvin line)
pin(10, "vfb", 1.90, 88.25, 2.20, 88.85)
for y0, y1, net in ((84.0, 91.5, "iovdd"), (93.5, 119.0, "iovdd"), (126.0, 134.0, "iovss")):
    c.shapes(L(30, 0)).insert(db.DBox(0, y0, 80, y1))
    pin(30, net, 39.0, y0 + 0.5, 39.5, y0 + 1.0)
c.shapes(L(189, 4)).insert(db.DBox(0, 84.0, 80, 180.0))
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(out, opt)
print("padtop_ctx_f2", c.dbbox())
