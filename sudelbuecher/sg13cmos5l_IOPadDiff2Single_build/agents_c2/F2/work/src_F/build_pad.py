# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Agent F (C2, 2026-10-31): F's cells in the pad top of sg13cmos5l_IOPadDiff2Single (stage 2), and with a third
argument the assembled d2s_block and the Kelvin vfb line (stage 3).

    python3 build_pad.py <out_pad.gds> <cells_dir> [<d2s_block.gds>]

Changes to the pad top (PCell instances, TopLayersTo4, Metal3ViasUp, contacts untouched):
  - cap_cma -> d2s_cma: CMA unchanged in its device layers; its Metal1 U loses the bottom strip (y 39.3 .. 41.85),
    so that a p+ ring fits under the junction; the two S/D + ntap columns are fed from the junction by Metal2 tabs
    with Via1 (the 332 Via1 of m2_junction onto the old strip are removed). Its own Metal2 strap = the junction's
    left half (same net, same shape).
  - cap_cmb -> d2s_cmb: geometry identical (renamed, pins added for the standalone check).
  - cm_rings (new): p+ rings (iovss) around CMA and CMB (stage 3: CMB's added) in the existing 1.80 um gaps (NW.b1) to the DCN guard well (below),
    the band well (left) and CMB's well (right), joined to DCPDiode's p+ guard ring (iovss) above.
  - guard_tie (new): Metal2 from the DCN guard / band Metal1 (net guard) up to Via2 into the Metal3 iovdd rail.
  - nw_isolator (new): n+ in NWell (iovdd) above the P frame's outer p+ ring; Via1 / Via2 into the M3 iovdd rail.
  - edge_stubs (new): IOPadAnalog's edge intervals above y 84 at both edges, each tied to its rail.
Rule values: sg13cmos5l_tech_default.json, keys named at each use.
"""
import os
import sys

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import PAD, RULES, Drawer, g5, save  # noqa: E402

OUT, CELLS = sys.argv[1], sys.argv[2]
ly = db.Layout()
ly.read(PAD)
top = ly.top_cell()
TOPNAME = top.name
LI = {k: ly.layer(*v) for k, v in {"M1": (8, 0), "M2": (10, 0), "Via1": (19, 0), "M1txt": (8, 25)}.items()}
um = lambda b: b.to_itype(ly.dbu)


def new_cell(name):
    c = ly.create_cell(name)
    top.insert(db.DCellInstArray(c.cell_index(), db.DTrans()))
    return c, Drawer(ly, c)


# ---- d2s_cma (from cap_cma) ------------------------------------------------------------------------------------
cma = ly.cell("cap_cma")
cma.name = "d2s_cma"
m1 = cma.shapes(LI["M1"])
m1.clear()
for s in list(cma.shapes(LI["M1txt"]).each()):
    cma.shapes(LI["M1txt"]).erase(s)
D = Drawer(ly, cma)
Y_RING = (40.25, 40.55)                  # p+ ring bottom leg (Activ); between DCN guard NWell 39.66 and CMA NWell 41.46
COL_B = g5(Y_RING[1] + 0.30)             # column Metal1 starts 0.30 above the ring's Metal1 (M1_b 0.18)
COLS = ((3.24, 4.13), (36.41, 37.30))    # the original U's columns (x), kept
for x0, x1 in COLS:
    D.box("M1", x0, COL_B, x1, 49.93)
D.box("M1", 3.0, 50.46, 36.21, 50.82)    # gate head (net a), unchanged
# Metal2: the junction's left half (same shape as m2_junction's) + tabs over both columns, Via1 2 x n
D.box("M2", 3.0, 39.3, 37.88, 41.3)
VY = [g5(41.0 + 0.41 * k) for k in range(22) if 41.0 + 0.41 * k <= 49.70]
for x0, x1 in COLS:
    D.box("M2", x0, 39.3, x1 - 0.05, 49.80)
    for xv in (x0 + 0.20, x0 + 0.61):
        for yv in VY:
            D.via1(xv, yv)
D.pin("M2", "pad", 3.24, 45.0, 3.80, 45.5)
D.pin("M1", "a", 10.0, 50.46, 10.5, 50.82)
n_cma_v1 = 2 * 2 * len(VY)

# ---- d2s_cmb (cap_cmb renamed, pins for the standalone check) ----------------------------------------------------
cmb = ly.cell("cap_cmb")
cmb.name = "d2s_cmb"
for s in list(cmb.shapes(LI["M1txt"]).each()):
    cmb.shapes(LI["M1txt"]).erase(s)
Dc = Drawer(ly, cmb)
Dc.pin("M1", "b", 57.0, 41.5, 57.5, 41.85)
Dc.pin("M1", "pad", 57.0, 50.46, 57.5, 50.82)

# ---- m2_junction: drop the Via1 onto the removed Metal1 strip ---------------------------------------------------
jn = ly.cell("m2_junction")
v1 = jn.shapes(LI["Via1"])
gone = [s for s in v1.each() if s.dbox.top <= 41.6 and s.dbox.left >= 3.0 and s.dbox.right <= 37.9]
for s in gone:
    v1.erase(s)
n_gone = len(gone)

# ---- m2_comb_p: CMB's gate fed from ONE pad line (k = 21, x 72.465) instead of eleven, so that a secondary stage
#      can be inserted by cutting at one place (lead 18:15): the 20 Via1 under pad lines k = 11 .. 20 are removed
cp_ = ly.cell("m2_comb_p")
v1c = cp_.shapes(LI["Via1"])
gone_g = [s for s in v1c.each() if 50.4 < s.dbox.center().y < 50.9 and s.dbox.center().x < 72.0]
for s in gone_g:
    v1c.erase(s)
assert len(gone_g) == 20, len(gone_g)

# ---- cma_ring: p+ (iovss) around CMA ------------------------------------------------------------------------------
ring, R = new_cell("cm_rings")
XL = (1.39, 1.69)        # band NWell 0.77 + 0.62 .. ; CMA NWell 2.57 - 0.88 (NW_f 0.24, TGO_b 0.27)
XR = (38.59, 38.89)      # CMA NWell 37.97 + 0.62 .. ; CMB NWell 39.77 - 0.88
Y_TOPJ = 51.76           # DCPDiode's p+ guard ring Activ y 51.42 .. 51.76 (iovss), joined
R.ptie(XL[0], Y_RING[0], XR[1], Y_RING[1], horizontal=True)
R.ptie(XL[0], Y_RING[1], XL[1], 51.42, horizontal=False)
R.ptie(XR[0], Y_RING[1], XR[1], 51.42, horizontal=False)
R.ptie(XL[0], 51.42, 2.95, Y_TOPJ, horizontal=True)       # left: over to the DCP ring's corner (Activ from x 2.8)
# CMB's own ring (lead 2026-10-31: each capacitor its own guard ring): the bottom leg continues under the junction's
# right half to a right leg 0.62 beyond CMB's well (75.17), joined to DCPDiode's p+ ring (x .. 77.2) above. The leg
# between CMA and CMB belongs to both rings (one 1.80 um gap holds one leg only: 0.62 + 0.30 + 0.62 = 1.54).
XRB = (75.79, 76.09)
R.ptie(XR[1], Y_RING[0], XRB[1], Y_RING[1], horizontal=True)
R.ptie(XRB[0], Y_RING[1], XRB[1], 51.42, horizontal=False)
R.pin("M1", "iovss", XR[0], 45.0, XR[1], 45.5)

# ---- guard_tie: guard (DCN guard ring / 6-61 band) -> M3 iovdd ------------------------------------------------------
gt, G = new_cell("guard_tie")
GX = (1.25, 1.65)        # 0.25 right of the b line (x 0.5 .. 1.0), Mn_b 0.21
G.box("M2", GX[0], 25.9, GX[1], 67.05)
for k in range(26):      # on the DCN guard Metal1 (x 1.0 .. 3.2, y 25.12 .. 39.04)
    G.via1(sum(GX) / 2, 26.2 + 0.48 * k)
for y in (66.25, 66.75):  # M3 iovdd rail 66 .. 91.5 (Vn_c 0.005 / Vn_c1 0.05 inside the M2 end)
    G.via2(sum(GX) / 2, y)
G.pin("M2", "guard", GX[0], 30.0, GX[1], 30.5)

# ---- nw_isolator: n+ in NWell (iovdd) above the P frame -------------------------------------------------------------
iso, I = new_cell("nw_isolator")
# frame p+ ring Activ top 84.26: NWell >= +NW_f 0.24 (84.50); 84.55 used. n+ Activ: NW_e 0.24 inside, pSD_d 0.18
# from the frame's pSD (84.44).
I.ntie(2.84, 84.79, 77.16, 85.09, horizontal=True, well_enc=0.24)
xs = [g5(9.045 + 3.02 * k) for k in range(21)]
xs = [x for x in xs if not 37.0 < x < 40.8]       # dabn / dabp lines at x 38.15 .. 39.55 (y up to 86.0)
xs = [x for x in xs if not 56.5 < x < 58.2]       # kept free: pad line k = 16 up to the CMB-stage reserve
for x in xs:
    I.box("M2", x - 0.30, 84.45, x + 0.30, 86.15)  # 0.25 from the comb straps' ends (84.2) and the a join (86.4)
    I.via1(x, 84.94)
    for yv in (85.45, 85.86):           # Vn_b 0.22: pitch 0.41
        I.via2(x, yv)
I.pin("M1", "iovdd", 20.0, 84.79, 20.5, 85.09)

# ---- edge_stubs: both edges ------------------------------------------------------------------------------------------
st, S = new_cell("edge_stubs")


def stubs(m, right=False):
    """m(x) maps a left-edge x to this edge"""
    def B(lay, x0, y0, x1, y1):
        S.box(lay, m(x0), y0, m(x1), y1)
    # p+ iovss 84.51 .. 139.92 (Activ, Substrate), M1 to 140.17, pSD to 140.35 (IOPadAnalog intervals)
    B("Activ", 0, 84.51, 1.2, 139.92)
    B("Sub", 0, 84.51, 1.2, 139.92)
    B("pSD", -0.18, 84.26, 1.38, 140.35)
    B("M1", 0, 84.0, 1.2, 140.17)
    for xc in (0.40, 0.80):
        for k in range(int((139.6 - 84.8) / 0.36) + 1):
            S.cont(m(xc), 84.83 + 0.36 * k)
    B("M2", 0.25, 126.0, 0.95, 134.0)
    for k in range(int((133.7 - 126.3) / 0.41) + 1):
        S.via1(m(0.6), 126.3 + 0.41 * k)
        S.via2(m(0.6), 126.3 + 0.41 * k)
    # n+ in NWell, iovdd, 148.35 .. 148.65 (NWell 147.73 .. 149.27), tied by Metal2 down to M3 iovdd (<= 119)
    B("NWell", -0.62, 147.73, 1.80, 149.27)
    B("Activ", 0, 148.35, 1.2, 148.65)
    B("M1", 0, 148.42, 1.2, 148.58)
    for xc in (0.25, 0.59, 0.93):
        S.cont(m(xc), 148.50)
    B("M1", 0.75, 148.20, 1.65, 148.80)
    if right:                                  # left: tied by Metal1 to the front-end vdd line of d2s_block
        S.via1(m(1.45), 148.50)
        B("M2", 1.30, 118.55, 1.60, 148.80)
        S.via2(m(1.45), 118.75)
    # p+ vss 156.85 .. 157.15 (Activ 0.25 short of the edge, M1 to it), Via1 / Via2 into M3 vss (140 .. 158)
    B("Activ", 0.25, 156.85, 1.6, 157.15)
    B("Sub", 0.25, 156.85, 1.6, 157.15)
    B("pSD", -0.18, 156.67, 1.78, 157.33)
    B("M1", 0, 156.92, 0.21, 157.08)            # at the edge as IOPadAnalog (0.16)
    B("M1", 0.21, 156.855, 1.6, 157.145)
    for xc in (0.59, 0.93, 1.27):
        S.cont(m(xc), 157.0)
    B("M2", 0.25, 156.855, 1.10, 157.145)     # ends 0.255 left of the vbpc line (x 1.355) of d2s_block
    for xc in (0.45, 0.90):              # V1_b / Vn_b 0.22: pitch 0.45
        S.via1(m(xc), 157.0)
        S.via2(m(xc), 157.0)
    # n+ in NWell, vdd, 166.85 .. 167.15 (NWell 166.23 .. 167.77, kept to x 0.75: NW_b1 1.8 to the iovdd wells)
    B("NWell", -0.62, 166.23, 0.75, 167.77)
    B("Activ", 0, 166.85, 0.51, 167.15)
    B("M1", 0, 166.92, 0.21, 167.08)            # at the edge as IOPadAnalog (0.16)
    B("M1", 0.21, 166.855, 0.51, 167.145)
    S.cont(m(0.33), 167.0)
    B("M2", 0.10, 166.855, 0.70, 167.145)    # Mn_d 0.144 um2
    S.via1(m(0.36), 167.0)
    S.via2(m(0.36), 167.0)


stubs(lambda x: x)
stubs(lambda x: 80.0 - x, right=True)
S.pin("M1", "iovss", 0.1, 100.0, 0.6, 100.5)

# ---- stage 3: d2s_block and the Kelvin vfb line --------------------------------------------------------------------
EXTRA = ()
if len(sys.argv) > 3:
    blk_src = db.Layout()
    blk_src.read(sys.argv[3])
    blk = ly.create_cell("d2s_block")
    blk.copy_tree(blk_src.cell("d2s_block"))
    # drop the block's copies of pad-top shapes (joins, dabp / dabn stubs, M3 rails, frame ring M1, their labels):
    # they were there for the block's own LVS; here the pad's originals are present
    for lay, boxes in (((10, 0), [(3.2, 86.4, 77.5, 87.0), (0.5, 87.4, 79.5, 88.0), (38.15, 85.0, 38.45, 86.0),
                                  (38.94, 85.0, 39.55, 86.0)]),
                       ((8, 0), [(0.5, 83.95, 79.5, 84.25)]),
                       ((30, 0), [(0.0, 84.0, 80.0, 91.5), (0.0, 93.5, 80.0, 119.0), (0.0, 126.0, 80.0, 134.0)])):
        sh = blk.shapes(ly.layer(*lay))
        for s_ in list(sh.each()):
            if s_.is_box() and any(abs(s_.dbox.left - b_[0]) < 1e-6 and abs(s_.dbox.bottom - b_[1]) < 1e-6 and
                                   abs(s_.dbox.right - b_[2]) < 1e-6 and abs(s_.dbox.top - b_[3]) < 1e-6 for b_ in boxes):
                sh.erase(s_)
    for lay in ((10, 25), (10, 2), (8, 25), (8, 2), (30, 25), (30, 2)):
        sh = blk.shapes(ly.layer(*lay))
        for s_ in list(sh.each()):
            t = s_.dtext if s_.is_text() else None
            b_ = s_.dbox if s_.is_box() else None
            if (t and t.string in ("a", "b", "dabn", "dabp", "iovss", "iovdd") ) or \
               (b_ and b_.top <= 88.2 and lay in ((10, 2), (8, 2))) or (b_ and lay == (30, 2)):
                sh.erase(s_)
    top.insert(db.DCellInstArray(blk.cell_index(), db.DTrans()))
    kv, K = new_cell("vfb_kelvin")
    # Kelvin line from the pad junction's left end (x 3.0, y 39.3 .. 41.3; low current there [r]) up the left edge
    # channel (Metal2 x 1.90 .. 2.20: 0.25 from guard_tie, 0.40 from the b line), Metal1 under the b join, Metal3 in
    # the gap 119 .. 126 east to d2s_block's landing (Via2 at x 15.25, y 125.30).
    K.box("M2", 1.90, 39.80, 3.40, 40.40)
    K.box("M2", 1.90, 39.80, 2.20, 87.10)
    K.via1(2.05, 86.95)
    K.box("M1", 1.90, 86.80, 2.20, 88.55)
    K.via1(2.05, 88.40)
    K.box("M2", 1.90, 88.25, 2.20, 125.60)
    K.via2(2.05, 125.30)
    K.box("M3", 1.90, 125.00, 15.40, 125.60)
    K.pin("M2", "vfb", 1.90, 60.0, 2.20, 60.5)
    EXTRA = ("vfb_kelvin",)          # d2s_block itself is written by build_block.py (with its LVS-only copies)

# ---- write -----------------------------------------------------------------------------------------------------------
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
opt.write_context_info = True            # keep the PCell context (clamps, diodes) as read
ly.write(OUT, opt)
for c in ("d2s_cma", "d2s_cmb", "cm_rings", "guard_tie", "nw_isolator", "edge_stubs") + EXTRA:
    o = db.SaveLayoutOptions()
    o.gds2_write_timestamps = False
    o.write_context_info = False
    o.select_cell(ly.cell(c).cell_index())
    ly.write(os.path.join(CELLS, c + ".gds"), o)
print("pad: top %s; junction Via1 removed %d; d2s_cma column Via1 %d" % (TOPNAME, n_gone, n_cma_v1))
