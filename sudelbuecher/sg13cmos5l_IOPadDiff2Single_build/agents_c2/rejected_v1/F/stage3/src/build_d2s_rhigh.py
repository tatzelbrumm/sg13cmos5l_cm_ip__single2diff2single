# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""d2s_rhigh: the four unit_r2 resistors (150 kOhm each) of d2s_mpdda_pd as rhigh chains, after bg_res_c
(bg_core_pd_2026-10-28/build_bg_res_c.py): the library's rhigh segment cell (0.5 x 12.65 um, from d2s_rhigh in
pad_buffer_cells.gds, unmodified), 18 positions at 0.68 um pitch, the map of layout_primitives.md section 5
(dummy A B C1 C2 C2 C1 B A A B C1 C2 C2 C1 B A dummy). Agent F, C2, 2026-10-31.

    python3 build_d2s_rhigh.py <out.gds> <out.cdl>

Each resistor: 4 segments, entered at the TOP head of its first segment, links alternately bottom / top, so both
ends land on the top heads: all 8 terminals are Metal2 pins on the TOP edge (towards the tails above).
Links: adjacent heads are bridged in Metal1 at head level; nested links alternate Metal1 (Metal1 stubs from the
heads, no via) and Metal2 (Via1 on the head, Metal2 stub) on one level, so 3 nested links need 2 levels per side.
Dummies: both heads by Metal1 to a p+ tie strip on each side (vss). Rule values (json): M1_b 0.18, Mn_b 0.21,
V1_a 0.19, V1_c1 0.05 (wire 0.29), Cnt_a / Cnt_b / Cnt_c for the tie; pSD 0.03 around the tie as the ptap1 PCell.
"""
import os
import sys

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import LIB, RULES, Drawer, g5, save  # noqa: E402

OUT, CDL = sys.argv[1], sys.argv[2]
PITCH = 0.68                      # library d2s_rhigh pitch (DRC clean there)
SEG_L = 12.65
MAP = ["dummy", "A", "B", "C1", "C2", "C2", "C1", "B", "A", "A", "B", "C1", "C2", "C2", "C1", "B", "A", "dummy"]
HB = (-0.41, -0.15)               # bottom head Metal1 y (measured in the library cell 'rhigh')
HT = (12.80, 13.06)               # top head Metal1 y
HX = (0.02, 0.48)                 # head Metal1 x, relative to the strip origin
W = g5(RULES["V1_a"] + 2 * RULES["V1_c1"])     # 0.29
H = W / 2
S1 = RULES["M1_b"]

src = db.Layout()
src.read(LIB)
ly = db.Layout()
ly.dbu = src.dbu
rcell = ly.create_cell("rhigh")
for li in src.layer_indexes():
    info = src.get_info(li)
    for s in src.cell("rhigh").shapes(li).each():
        rcell.shapes(ly.layer(info.layer, info.datatype)).insert(s)
top = ly.create_cell("d2s_rhigh")
D = Drawer(ly, top)
xc = lambda i: g5(i * PITCH + 0.25)
for i, n in enumerate(MAP):
    top.insert(db.DCellInstArray(rcell.cell_index(), db.DTrans(g5(i * PITCH), 0)))
    D.note(n, xc(i), 6.3)

yb_head, yt_head = (HB[0] + HB[1]) / 2, (HT[0] + HT[1]) / 2
L1b = g5(HB[0] - S1 - H)                  # Metal1 link below the bottom heads
L2b = g5(L1b - H - S1 - H)
L1t = g5(HT[1] + S1 + H)
L2t = g5(L1t + H + S1 + H)
Y_TOP = g5(L2t + H)
Y_BOT = g5(L2b - H)


def link(i, j, side, level, layer):
    """join heads i and j on one side; level 0 = bridge at head level (Metal1)"""
    yh = yb_head if side == "b" else yt_head
    if level == 0:
        hy = HB if side == "b" else HT
        D.box("M1", i * PITCH + HX[0], hy[0], j * PITCH + HX[1], hy[1])
        return
    y = {("b", 1): L1b, ("b", 2): L2b, ("t", 1): L1t, ("t", 2): L2t}[(side, level)]
    for k in (i, j):
        if layer == "M2":
            D.via1(xc(k), yh)
        D.box(layer, xc(k) - H, min(y, yh) - H, xc(k) + H, max(y, yh) + H)
    D.box(layer, xc(i) - H, y - H, xc(j) + H, y + H)


# chains: positions of each resistor, its segments' links, terminals
pos = {r: [i for i, n in enumerate(MAP) if n == r] for r in ("A", "B", "C1", "C2")}
devices, term = [], {}
for r, ps in pos.items():
    nodes = ["sa_" + r, r + "_1", r + "_2", r + "_3", "sb_" + r]
    for k in range(4):
        devices.append(("%s_%d" % (r, k), nodes[k], nodes[k + 1]))
    term["sa_" + r], term["sb_" + r] = ps[0], ps[3]
    # links: seg0 -> seg1 bottom, seg1 -> seg2 top, seg2 -> seg3 bottom
    for (a, b, side) in ((ps[0], ps[1], "b"), (ps[1], ps[2], "t"), (ps[2], ps[3], "b")):
        depth = {1: 0, 3: 1, 5: 1, 7: 2}[b - a]      # span -> nesting depth
        layer = {0: "M1", 1: "M1" if (b - a) == 3 else "M2", 2: "M1"}[depth]
        level = {0: 0, 1: 1, 2: 2}[depth] if (b - a) != 5 else 1
        link(a, b, side, level, layer)
# the nested sets per side: spans 1 (bridge), 3 (M1, level 1), 5 (M2, level 1), 7 (M1, level 2)
for net, i in term.items():
    D.via1(xc(i), yt_head)
    D.box("M2", xc(i) - H, yt_head - H, xc(i) + H, Y_TOP)
    D.pin("M2", net, xc(i) - H, Y_TOP - W, xc(i) + H, Y_TOP)
# ties on both sides, dummies' heads to them
xl1 = g5(-0.54)                        # tie inner Activ edge, as the library d2s_rhigh (ptap1$8 at x -1.32 .. -0.54)
tw = 0.36
xr0 = g5((len(MAP) - 1) * PITCH + 0.5 + 0.54)
D.ptie(xl1 - tw, Y_BOT, xl1, Y_TOP, horizontal=False)
D.ptie(xr0, Y_BOT, xr0 + tw, Y_TOP, horizontal=False)
for i, (xa, xb) in ((0, (xl1 - tw, HX[1])), (len(MAP) - 1, ((len(MAP) - 1) * PITCH + HX[0], xr0 + tw))):
    for hy in (HB, HT):
        D.box("M1", xa, hy[0], xb, hy[1])
for xa in (xl1 - tw, xr0):
    D.pin("M1", "vss", xa, 5.0, xa + tw, 6.0)
devices += [("dummy_L", "vss", "vss"), ("dummy_R", "vss", "vss")]
save(ly, OUT)
bb = top.dbbox()
with open(CDL, "w") as f:
    f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
            "* d2s_rhigh (build_d2s_rhigh.py, agent F, C2 2026-10-31): unit_r2's 4 resistors, each 4 x 0.5/12.65 um\n"
            "* rhigh in series (50.6 um, as rl=50.6u), 2 dummies shorted to vss; bulk = substrate (vss)\n"
            ".SUBCKT d2s_rhigh sa_A sa_B sa_C1 sa_C2 sb_A sb_B sb_C1 sb_C2 vss\n")
    for name, a, b in devices:
        f.write("R%s %s %s vss rhigh w=0.5u l=%gu m=1 b=0\n" % (name, a, b, SEG_L))
    f.write(".ENDS d2s_rhigh\n")
print("d2s_rhigh: bbox %s = %.3f x %.3f um = %.1f um2 (library 14.76 x 17.50 = 258.3)"
      % (bb, bb.width(), bb.height(), bb.width() * bb.height()))
print("pins (top edge, M2):", sorted((n, xc(i)) for n, i in term.items()))
