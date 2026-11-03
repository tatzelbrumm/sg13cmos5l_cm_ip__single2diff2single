# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""router metal (top-level Metal1 / Metal2 of d2s_block) over any gate (Activ & GatPoly) of the placed cells.
    python3 gate_metal.py <d2s_block.gds>"""
import sys
import klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1]); top = ly.cell("d2s_block")
m = db.Region(top.shapes(ly.find_layer(8, 0))) + db.Region(top.shapes(ly.find_layer(10, 0)))
tot = 0.0
for inst in top.each_inst():
    c = inst.cell
    if c.name.startswith(("padtop", "pwr")):
        continue
    g = (db.Region(c.begin_shapes_rec(ly.find_layer(1, 0))) & db.Region(c.begin_shapes_rec(ly.find_layer(5, 0))))
    a = (m & g.transformed(inst.cplx_trans)).area() * ly.dbu ** 2
    tot += a
    print("%-16s %.3f um2" % (c.name, a))
print("total %.3f um2 of router Metal1 / Metal2 over gates" % tot)
