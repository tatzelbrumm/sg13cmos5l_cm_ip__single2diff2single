# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""bg_pnp_c: the bandgap's pnp array (Q1 centre + 8 x Q2, pnpMPA 2x2) with the wiring the library cell lacks.
Written 2026-10-28 by Claude (Opus 5.5).

    python3 build_bg_pnp_c.py <pad_buffer_cells.gds> <out.gds> <out.cdl>

"Placed only" (cell_tree.md) = the library bg_pnp is a 3 x 3 AREF of the unmodified pnpMPA cell at 7.15 x 5.67 um
pitch whose collector rings overlap into one lattice; emitters and bases are not connected, there are no pins
(log 2026-10-27 16:31: its LVS matched 9 devices only with floating bases). Kept unchanged here: the AREF (same
cell, origin, pitch) and the device labels. Added (all top level):
  - base = collector = vss (sheet: Q1 / Q2 C = B = vss): Metal1 fill between each base ring (outer edge) and its
    collector ring (inner edge), so the M1 of all bases and the collector lattice is one vss plane;
  - emitters: 3 x 3 Via1 on each emitter's Metal1, a Metal2 pad;
  - e2 (the 8 outer emitters, Q2): Metal2 frame through the top and bottom rows and the left column, the right
    column only below its middle device: the gap lets ea out; e2 leaves to the right edge between the lower rows;
  - ea (Q1, centre): Metal2 up to the row boundary, then right through the gap to the right edge;
  - pins: e2, ea on the right edge (Metal2), vss on the Metal1 collector lattice (left and right edges).
The common centroid is the device placement (Q1 in the centre of the 3 x 3); the emitter wiring is not mirror
symmetric (the ea exit); [reasoning] its Metal2 resistance (a few squares, < 1 ohm) at 0.3 uA per emitter is
negligible against the emitter.
Rule values: out/v2/process/ihp_sg13cmos5l.py (V1_a 0.19, V1_b 0.22, V1_c1 0.05, Mn_b 0.21, grid 0.005).
"""
import importlib.util
import os
import sys

import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("adapter", os.path.join(HERE, "..", "out", "v2", "process",
                                                                      "ihp_sg13cmos5l.py"))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
R = P.rules()
LIB, OUT, CDL = sys.argv[1], sys.argv[2], sys.argv[3]
g5 = lambda v: round(round(v / R["grid"]) * R["grid"], 4)
W = g5(R["via1.size"] + 2 * R["via1.enc_end"])      # 0.29 wire
H = W / 2

src = db.Layout()
src.read(LIB)
lib = src.cell("bg_pnp")
pnp = src.cell("pnpMPA")
arr = [i for i in lib.each_inst()][0]
ly = db.Layout()
ly.dbu = src.dbu
dev = ly.create_cell("pnpMPA")
for li in src.layer_indexes():
    info = src.get_info(li)
    for s in pnp.shapes(li).each():
        dev.shapes(ly.layer(info.layer, info.datatype)).insert(s)
top = ly.create_cell("bg_pnp_c")
top.insert(db.CellInstArray(dev.cell_index(), arr.trans, arr.a, arr.b, arr.na, arr.nb))
for li in src.layer_indexes():                         # the library cell's own labels (63/0)
    info = src.get_info(li)
    for s in lib.shapes(li).each():
        top.shapes(ly.layer(info.layer, info.datatype)).insert(s)
L = {k: ly.layer(*P.LAYERS[k]) for k in ("m1", "via1", "m2", "m2.pin", "m2.text", "m1.pin", "m1.text")}
ox, oy = arr.trans.disp.x * ly.dbu, arr.trans.disp.y * ly.dbu
va, vb = arr.a, arr.b                                  # AREF step vectors: one is the x step, one the y step
sx = va if va.x != 0 else vb
sy = vb if sx is va else va
nx_, ny_ = (arr.na, arr.nb) if sx is va else (arr.nb, arr.na)
px, py = sx.x * ly.dbu, sy.y * ly.dbu                    # 7.15, 5.67
XS = [g5(ox + k * px) for k in range(nx_)]
YS = [g5(oy + k * py) for k in range(ny_)]
assert len(XS) == 3 and len(YS) == 3 and px > 0 and py > 0, (XS, YS)
bb = top.dbbox()


def box(lay, x0, y0, x1, y1):
    top.shapes(L[lay]).insert(db.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


# 1. base ring -> collector ring, Metal1 annulus (base M1 outer +-2.37 x +-1.63, collector M1 inner +-3.40 x +-2.66)
for x in XS:
    for y in YS:
        ring = db.Region(db.DBox(x - 3.40, y - 2.66, x + 3.40, y + 2.66).to_itype(ly.dbu)) - \
            db.Region(db.DBox(x - 2.37, y - 1.63, x + 2.37, y + 1.63).to_itype(ly.dbu))
        top.shapes(L["m1"]).insert(ring)
# 2. emitter vias (3 x 3 at V1_a + V1_b) and Metal2 pads
vp = g5(R["via1.size"] + R["via1.space"])
a = R["via1.size"] / 2
pad = g5(2 * vp + R["via1.size"] + 2 * R["via1.enc_end"] + 0.1) / 2
for x in XS:
    for y in YS:
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                box("via1", x + i * vp - a, y + j * vp - a, x + i * vp + a, y + j * vp + a)
        box("m2", x - pad, y - pad, x + pad, y + pad)
# 3. e2 frame (Metal2): top row, bottom row, left column, right column below the middle device
box("m2", XS[0] - H, YS[2] - H, XS[2] + H, YS[2] + H)
box("m2", XS[0] - H, YS[0] - H, XS[2] + H, YS[0] + H)
box("m2", XS[0] - H, YS[0] - H, XS[0] + H, YS[2] + H)
box("m2", XS[2] - H, YS[0] - H, XS[2] + H, YS[1] + H)
y_e2 = g5((YS[0] + YS[1]) / 2)                         # between the two lower rows
box("m2", XS[2] - H, y_e2 - H, bb.right, y_e2 + H)
# 4. ea: Q1 (centre) up to the row boundary between the middle and top rows, right through the gap
y_ea = g5((YS[1] + YS[2]) / 2)
box("m2", XS[1] - H, YS[1], XS[1] + H, y_ea + H)
box("m2", XS[1] - H, y_ea - H, bb.right, y_ea + H)
# pins: e2 / ea on the right edge (Metal2); vss on the collector lattice (Metal1, left / right edge strips)
for net, y in (("e2", y_e2), ("ea", y_ea)):
    box("m2.pin", bb.right - W, y - H, bb.right, y + H)
    top.shapes(L["m2.text"]).insert(db.DText(net, g5(bb.right - H), y))
cl = (XS[0] - 3.75, XS[0] - 3.40)                        # left collector strip (M1) of the left column
box("m1.pin", cl[0], YS[1] - 0.5, cl[1], YS[1] + 0.5)
top.shapes(L["m1.text"]).insert(db.DText("vss", g5((cl[0] + cl[1]) / 2), YS[1]))
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(OUT, opt)
with open(CDL, "w") as f:
    f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
            "* bg_pnp_c (build_bg_pnp_c.py, 2026-10-28, Claude): Q1 (centre, ea) and 8 x Q2 (e2), pnpMPA a=4p p=8u,\n"
            "* C = substrate = B = vss\n.SUBCKT bg_pnp_c e2 ea vss\n")
    f.write("QQ1 vss vss ea pnpMPA AE=4p PE=8u\n")
    for k in range(8):
        f.write("QQ2_%d vss vss e2 pnpMPA AE=4p PE=8u\n" % k)
    f.write(".ENDS bg_pnp_c\n")
nb = top.dbbox()
print("bg_pnp_c: %.3f x %.3f um = %.1f um2 (library bg_pnp 22.20 x 17.76 = 394.3); e2 pin y %.3f, ea pin y %.3f, "
      "right edge x %.3f" % (nb.width(), nb.height(), nb.width() * nb.height(), y_e2, y_ea, nb.right))
