# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B: the template as routing context for the block (after C2 F2's make_ctx.py).
    python3 make_ctx.py <template.gds> <out.gds>
padctx_f: the template's Metal1 / Via1 / Metal2 in x 0..80, y 26..180, flattened and clipped (obstacles for the
router: the protection's wiring, the iovdd bar and risers, the leg ties, the edge stubs), the pad pin (Metal2 strap
x 20.40..21.02, top y 31.18) as pin `pad`, and a prBoundary box (0, 26, 80, 180) that fixes the block's extent (so
the core-side port pins land on y 180). In the pad the cell is dropped: the template has all of it."""
import sys

import klayout.db as db

src, out = sys.argv[1:3]
s = db.Layout()
s.read(src)
top = s.cell('sg13cmos5l_IOPadSingle2Diff')
ly = db.Layout()
ly.dbu = s.dbu
c = ly.create_cell('padctx_f')
clip = db.Region(db.DBox(0, 26.0, 80, 180.0).to_itype(s.dbu))
for (l, d) in ((8, 0), (19, 0), (10, 0)):
    r = (db.Region(top.begin_shapes_rec(s.find_layer(l, d))) & clip).merged()
    c.shapes(ly.layer(l, d)).insert(r)
c.shapes(ly.layer(10, 2)).insert(db.DBox(20.40, 30.58, 21.02, 31.18))
c.shapes(ly.layer(10, 25)).insert(db.DText('pad', 20.71, 30.88))
c.shapes(ly.layer(189, 4)).insert(db.DBox(0, 26.0, 80, 180.0))
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(out, opt)
print('padctx_f', c.dbbox())
