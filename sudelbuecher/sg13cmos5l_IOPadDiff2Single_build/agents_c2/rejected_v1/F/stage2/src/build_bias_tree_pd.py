# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""bias_tree_pd: the bias tree of the pad (sheet macros/bias_tree_pd, subckt bias_tree_pd in bias_ref_pd.spice)
WITHOUT its four bias diodes Xd (BP / BN / BPC / BNC sit in the tails, sinks and cascode cells; lead's decision of
2026-10-31 17:01). Built from the library primitives bias_tree_p, bias_tree_swp, bias_tree_sw, bias_tree_n of
pad_buffer_cells.gds, placed UNCHANGED in one row (left to right), and wired at this level. Agent F, C2 2026-10-31.

    python3 build_bias_tree_pd.py <out.gds> <out.cdl>

Row: [bias_tree_p | swp | sw | bias_tree_n]. swp's NWell abuts bias_tree_p's (one iovdd well); sw sits NW_d1 0.62
from it and TGO_e 0.86 from swp's ThickGateOx; bias_tree_n's p+ ring Activ_b 0.21 from sw. bias_tree_n is shifted
0.185 um down so that its vbp trunk is collinear with bias_tree_p's: one Metal2 bridge joins them over swp / sw.
ni: bias_tree_n's ni trunk, extended left, drops in Metal2 onto sw's ni stripe; sw ni <-> swp ni in Metal2.
iref, en_3v3_b: Metal2 between the two switch cells; iref, en_3v3, en_3v3_b rise in Metal1 to the top edge.
Rule values (json): Act_b 0.21, NW_d1 0.62, TGO_e 0.86, pSD_d 0.18, M1_b 0.18, Mn_b 0.21, V1_a 0.19, V1_c1 0.05.
"""
import os
import sys

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import LIB, Drawer, g5  # noqa: E402

OUT, CDL = sys.argv[1], sys.argv[2]
ly = db.Layout()
ly.read(LIB)
top = ly.create_cell("bias_tree_pd")
D = Drawer(ly, top)
T = {}


def place(name, x, y):
    T[name] = (x, y)
    top.insert(db.DCellInstArray(ly.cell(name).cell_index(), db.DTrans(g5(x), g5(y))))


# placements (local um); offsets = - library bbox lower-left where useful
place("bias_tree_p", 2.02, 1.98)          # bbox 0 .. 18.79 x 0 .. 11.635
place("bias_tree_swp", 19.81, 2.72)       # TGO / NWell from 19.19: TGO_b 0.27 to tree_p's n+ ring (18.55)
place("bias_tree_sw", 22.75, 2.72)        # Activ 22.75 .. 24.71; TGO 22.48 >= swp TGO 21.56 + 0.86
place("bias_tree_n", 26.75, 1.48)         # ring Activ 24.57 >= 24.31 + 0.21 + margin; trunks collinear
P, SWP, SW, N = T["bias_tree_p"], T["bias_tree_swp"], T["bias_tree_sw"], T["bias_tree_n"]
D.box("NWell", P[0] + 16.0, P[1] - 1.98, SWP[0], P[1] + 9.655)   # one iovdd well: tree_p + swp (full height)
H = 0.145                                  # half wire (0.29 = V1_a + 2 V1_c1)

# 1. vbp bridge: tree_p trunk vbp (rel y 6.9, ends x 16.56) -> tree_n trunk vbp (rel y 7.4, starts x -1.81)
yv = P[1] + 6.9
assert abs((N[1] + 7.4) - yv) < 1e-6
D.box("M2", P[0] + 16.56 - 0.1, yv - H, N[0] - 1.81 + 0.1, yv + H)

# 2. ni: tree_n trunk ni (rel y 6.9) extended left to above sw's ni stripe, down to it
yni = N[1] + 6.9
x_sw_ni = SW[0] + 0.98
D.box("M2", x_sw_ni - H, yni - H, N[0] - 1.81 + 0.1, yni + H)
y_ni_low = SW[1] + 0.6                     # on the ni stripes (rel y 0.25 .. 0.75)
D.box("M2", x_sw_ni - H, y_ni_low - H, x_sw_ni + H, yni + H)
x_swp_ni = SWP[0] + 0.98
for x in (x_sw_ni, x_swp_ni):
    D.box("M1", x - H, y_ni_low - H, x + H, y_ni_low + H)
    D.via1(x, y_ni_low)
D.box("M2", x_swp_ni - H, y_ni_low - H, x_sw_ni + H, y_ni_low + H)

# 3. iref: both iref stripes extended down, Metal2 between them, Metal1 riser to the top edge
y_ir = SW[1] - 0.05
x_sw_ir, x_swp_ir = SW[0] + 0.15, SWP[0] + 0.15
for x in (x_sw_ir, x_swp_ir):
    D.box("M1", x - 0.08, y_ir - H, x + 0.08, SW[1] + 0.3)
    D.box("M1", x - H, y_ir - H, x + H, y_ir + H)
    D.via1(x, y_ir)
D.box("M2", x_swp_ir - H, y_ir - H, x_sw_ir + H, y_ir + H)
Y_TOP = g5(P[1] + 9.655)                   # top of tree_p (the cell's top edge)
x_ir_up = g5((SWP[0] + 1.75 + SW[0]) / 2 - 0.3)   # between the two switch cells
D.box("M1", x_ir_up - H, y_ir - H, x_ir_up + H, Y_TOP)
D.via1(x_ir_up, y_ir)
D.pin("M1", "iref", x_ir_up - H, Y_TOP - 0.4, x_ir_up + H, Y_TOP)

# 4. en_3v3_b: swp gate (rel 0.315 .. 0.815, 1.47 .. 1.73) and sw TDN gate (rel 1.25 .. 1.54, 1.18 .. 1.39) rise
#    in Metal1 above the trunks and are joined there in Metal2 (below the trunks the ni riser is in the way)
y_eb = g5(Y_TOP - 0.55)
xg_swp, xg_sw = SWP[0] + 0.565, SW[0] + 1.395
D.box("M1", xg_swp - H, SWP[1] + 1.47, xg_swp + H, y_eb + H)
D.box("M1", xg_sw - H, SW[1] + 1.18, xg_sw + H, Y_TOP)
D.via1(xg_swp, y_eb)
D.via1(xg_sw, y_eb)
D.box("M2", xg_swp - H, y_eb - H, xg_sw + H, y_eb + H)
D.pin("M1", "en_3v3_b", xg_sw - H, Y_TOP - 0.4, xg_sw + H, Y_TOP)
# en_3v3: sw TGN gate (rel 0.42 .. 0.71, 1.18 .. 1.39) straight up
xg_en = SW[0] + 0.565
D.box("M1", xg_en - H, SW[1] + 1.18, xg_en + H, Y_TOP)
D.pin("M1", "en_3v3", xg_en - H, Y_TOP - 0.4, xg_en + H, Y_TOP)

# 5. supplies: sw TDN source (rel 1.73 .. 1.89) to tree_n's left ring (vss); swp ntap to tree_p's right ring (vdd)
D.box("M1", SW[0] + 1.73, SW[1] + 0.25, N[0] - 1.40, SW[1] + 0.75)
D.box("M1", P[0] + 16.0, SWP[1] - 1.51, SWP[0] + 0.545, SWP[1] - 0.91)
D.pin("M1", "vdd", P[0] + 6.0, P[1] - 1.65, P[0] + 7.0, P[1] - 1.05)
D.pin("M1", "vss", N[0] + 11.0, N[1] - 1.545, N[0] + 12.0, N[1] - 0.945)

# 6. bias outputs: Metal2 pins on the trunk ends (tree_p's at the left edge, tree_n's at the right edge)
for net, ry in (("vbp", 6.9), ("vbn", 7.4), ("vabn", 7.9), ("vbnc", 8.4)):
    D.pin("M2", net, P[0] - 1.81, P[1] + ry - H, P[0] - 1.41, P[1] + ry + H)
for net, ry in (("vabp", 7.9), ("vbpc", 8.4)):
    D.pin("M2", net, N[0] + 25.21, N[1] + ry - H, N[0] + 25.61, N[1] + ry + H)

opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
opt.write_context_info = False
opt.select_cell(top.cell_index())
ly.write(OUT, opt)
bb = top.dbbox()
print("bias_tree_pd: bbox %s = %.2f x %.2f um = %.0f um2 (library parts: 27.42x11.11 + 18.79x11.63 + 2 switches)"
      % (bb, bb.width(), bb.height(), bb.width() * bb.height()))
with open(CDL, "w") as f:
    f.write("""* SPDX-FileCopyrightText: 2026 Christoph Maier
* SPDX-License-Identifier: Apache-2.0
* bias_tree_pd as drawn by agent F (C2 2026-10-31): the sheet's bias_tree_pd WITHOUT Xd = bias_diodes (BP, BN,
* BNC, BPC are drawn in the tails, sinks and cascode cells); the library dummies as devices.
.SUBCKT bias_tree_pd vdd vss iref vbp vbn vbpc vbnc vabp vabn en_3v3 en_3v3_b
MTGN iref en_3v3 ni vss sg13_hv_nmos w=1u l=0.45u ng=1 m=1
MTGP iref en_3v3_b ni vdd sg13_hv_pmos w=1u l=0.45u ng=1 m=1
MTDN ni en_3v3_b vss vss sg13_hv_nmos w=1u l=0.45u ng=1 m=1
MNI ni ni vss vss sg13_hv_nmos w=6u l=6u ng=1 m=1
MNBP vbp ni vss vss sg13_hv_nmos w=6u l=6u ng=1 m=1
MNBPC vbpc ni vss vss sg13_hv_nmos w=2.4u l=6u ng=1 m=1
MNABP vabp ni vss vss sg13_hv_nmos w=6u l=6u ng=1 m=1
MNdummy vss ni vss vss sg13_hv_nmos w=2.4u l=6u ng=1 m=1
MPBN vbn vbp vdd vdd sg13_hv_pmos w=5u l=6u ng=1 m=1
MPBNC vbnc vbp vdd vdd sg13_hv_pmos w=2u l=6u ng=1 m=1
MPABN vabn vbp vdd vdd sg13_hv_pmos w=5u l=6u ng=1 m=1
MPdummy vdd vbp vdd vdd sg13_hv_pmos w=2u l=6u ng=1 m=1
.ENDS bias_tree_pd
""")
