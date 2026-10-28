# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""oa_core_pd: Oguey-Aebischer reference core with power-down, assembled from the six OA primitives of
pad_buffer_cells.gds (oa_pmir, oa_pcas, oa_misc_p, oa_nmir, oa_mcs, oa_misc_n), unchanged, plus top-level
wiring on Metal1 / Metal2 only (Metal3 and above stay free for the slot).

Written 2026-10-28 by Claude (Opus 5.5). Run with the pip module klayout >= 0.28 (tested 0.30.12):
    python3 oa_core_pd_build.py [path/to/pad_buffer_cells.gds] [out.gds]

How the primitives stay unchanged: the script reads the whole library, deletes every cell that is not in
the hierarchy of the six primitives, and adds the top cell. Names and geometry of the primitives and their
sub-cells are therefore the library's own (checked by XOR in oa_core_pd_verify.py).

New cells: oa_core_pd (top: rails, wiring, pins) and oa_pmir_image_jumpers (the point image, about the
centre of oa_pmir, of oa_pmir's own left-side M1 jumpers, vias and M2 band tracks; placed with oa_pmir's
transformation, so oa_pmir's net wiring is point-symmetric).

Rule values used for the wiring (sg13cmos5l_tech_default.json): M1_a 0.16, M1_b 0.18, M1_e 0.22 (next to
M1 wider than M1_e_w 0.30), V1_a 0.19, V1_b 0.22, V1_c 0.01, V1_c1 0.05, Mn_a 0.20, Mn_b 0.21, Mn_c 0.005,
Mn_d 0.144, grid 0.005; M2.c1 0.05 (sg13cmos5l_maximal.drc, no json key). Wires are 0.29 um wide on both metals (narrower than M1_e_w and
Mn_e_w, so wide-metal spacing only applies next to the cells' rings and rails).
"""
import os
import sys
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "inputs", "pad_buffer_cells.gds")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "oa_core_pd.gds")
TOP = "oa_core_pd"
PRIMS = ["oa_pmir", "oa_pcas", "oa_misc_p", "oa_nmir", "oa_mcs", "oa_misc_n"]

# ------------------------------------------------------------------------------------------------
# Placement (um). Origin of each primitive cell and its orientation. Block: x 0 ... BX, y 0 ... BY.
# ------------------------------------------------------------------------------------------------
PMX, PMY = 3.755, 48.6               # oa_pmir, M0 (mirrored about x): its band B (lower in the cell) on top
PCX, PCY = PMX + 27.85, PMY - 10.52  # oa_pcas, M0: source tracks in line with pmir band B, drains face down
NX, NY = 32.5, PMY - 27.91           # oa_nmir, R0, below pcas
NNX, NNY = 65.4, NY                  # oa_misc_n, R0: its vss tie in line with nmir's tie
MPX, MPY = 73.98, PMY - 0.41         # oa_misc_p, R180: ks at its bottom (towards misc_n), SVPG at top left
MX, MY = 0.27, PMY - 46.07           # oa_mcs, R0, along the bottom
BX, BY = 76.0, PMY + 2.14            # block extent (BX = misc_p NWell edge, BY = top of the vdd rail)
ORIENT = {"oa_pmir": ("M0", PMX, PMY), "oa_pcas": ("M0", PCX, PCY), "oa_nmir": ("R0", NX, NY),
          "oa_misc_n": ("R0", NNX, NNY), "oa_misc_p": ("R180", MPX, MPY), "oa_mcs": ("R0", MX, MY)}

# Rails (Metal1) along the bottom (vss) and top (vdd) edges
VSS_RAIL = (0.0, 0.0, BX, 1.42)      # overlaps oa_mcs's ptap M1 (y MY-1.71 ... MY-1.11)
VDD_RAIL = (0.0, PMY + 0.64, BX, BY)  # overlaps the top ring sides of oa_pmir and oa_misc_p

# Tracks and turning points of the top-level wiring
W = 0.29                             # wire width, M1 and M2
X_TRK = PCX + 19.27                  # right end of pcas's M2 tracks
X_VPC, X_VBR, X_VNC, X_IOUT = 51.35, 51.85, 52.35, 52.95   # where pcas's drain tracks turn
Y_VPC, Y_VBR = PMY - 16.10, PMY - 16.71                    # vpc / vbr runs east, above nmir / misc_n
Y_BAR = NY + 10.60                   # centre of nmir's and misc_n's top gate bars (M1)
X_VRES, X_VBRCH = 64.15, 64.70       # channel between nmir and misc_n: vres (M1), vbr (M2)
Y_MCSBAR = MY + 4.00                 # mcs vbr gate bar (M1) centre
X_MCSBAR = 46.70                     # where vbr lands on the mcs bar
X_VPG = 63.00                        # vpg runs up here, left of misc_p
VSS_STRAP = (68.0, 1.0, 72.0, NY - 1.11)   # misc_n tie down to the vss rail
VDD_STRAPS = [(32.0, PCY + 2.0, 34.0, PMY + 0.64), (46.0, PCY + 2.0, 48.0, PMY + 0.64)]  # pcas ring -> rail

LAY = {"M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25), "V1": (19, 0), "M2": (10, 0), "M2pin": (10, 2),
       "M2txt": (10, 25)}

# ------------------------------------------------------------------------------------------------
ly = db.Layout()
ly.read(LIB)
keep = set()
for n in PRIMS:
    c = ly.cell(n)
    keep.add(c.cell_index())
    keep |= set(c.called_cells())
for ci in [c.cell_index() for c in ly.each_cell()]:
    if ci not in keep:
        ly.delete_cell(ci)          # deletes only that cell; the kept cells and their instances stay
assert sorted(c.name for c in ly.top_cells()) == sorted(PRIMS), [c.name for c in ly.top_cells()]
LI = {k: ly.layer(*v) for k, v in LAY.items()}
top = ly.create_cell(TOP)
TR = {"R0": db.DTrans.R0, "M0": db.DTrans.M0, "R180": db.DTrans.R180}
T = {}
for n, (o, x, y) in ORIENT.items():
    T[n] = db.DTrans(TR[o], db.DVector(x, y))
    top.insert(db.DCellInstArray(ly.cell(n).cell_index(), T[n]))


def g5(v):
    return round(v / 0.005) * 0.005


def box(cell, lay, x0, y0, x1, y1):
    cell.shapes(LI[lay]).insert(db.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


def seg(lay, x0, y0, x1, y1, w=W):
    """Horizontal or vertical wire with square ends extended by w/2 (corners join, vias enclosed)."""
    h = w / 2
    box(top, lay, min(x0, x1) - h, min(y0, y1) - h, max(x0, x1) + h, max(y0, y1) + h)


def path(lay, pts, w=W):
    for (a, b), (c, d) in zip(pts[:-1], pts[1:]):
        assert a == c or b == d, ("not Manhattan", pts)
        seg(lay, a, b, c, d, w)


def via(x, y, m1=True, m2=True):
    """Via1 0.19 x 0.19 (V1.a) with 0.29 x 0.29 pads (0.05 enclosure: V1.c1 / Mn.c1)."""
    box(top, "V1", x - 0.095, y - 0.095, x + 0.095, y + 0.095)
    if m1:
        box(top, "M1", x - 0.145, y - 0.145, x + 0.145, y + 0.145)
    if m2:
        box(top, "M2", x - 0.145, y - 0.145, x + 0.145, y + 0.145)


def pin(metal, net, x0, y0, x1, y1):
    box(top, metal + "pin", x0, y0, x1, y1)
    top.shapes(LI[metal + "txt"]).insert(db.DText(net, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))


def tr(cell, x, y):
    p = T[cell] * db.DPoint(x, y)
    return g5(p.x), g5(p.y)


# ------------------------------------------------------------------------------------------------
# 1. oa_pmir: point image of its own band wiring (left M1 jumpers, their vias, the 8 M2 band tracks)
# ------------------------------------------------------------------------------------------------
pm = ly.cell("oa_pmir")
nb = db.Region(pm.begin_shapes_rec(ly.find_layer(31, 0))).bbox()
cx, cy = (nb.left + nb.right) / 2, (nb.bottom + nb.top) / 2      # dbu; NWell centre = array centre
img = ly.create_cell("oa_pmir_image_jumpers")
R = db.Trans(db.Trans.R180, db.Vector(2 * cx, 2 * cy))          # point reflection about (cx, cy)
for lay in ("M1", "V1", "M2"):                                   # jumpers and their vias end left of
    for s in pm.shapes(LI[lay]).each():                          # x = NWell edge + 0.1 um; M2: all tracks
        if lay == "M2" or s.bbox().right <= nb.left + 100:
            img.shapes(LI[lay]).insert(s.polygon.transformed(R))
top.insert(db.DCellInstArray(img.cell_index(), T["oa_pmir"]))
PMIR_CENTRE = (cx * ly.dbu, cy * ly.dbu)

# band B (pmir cell y 8.755 ... 10.545) to pcas source tracks: straight M2, same order and pitch
for yc in (8.9, 9.4, 9.9, 10.4):                                  # vpg c2 c8 co in pmir cell coordinates
    xa, ya = tr("oa_pmir", 24.06, yc)
    xb, _ = tr("oa_pcas", -1.77, 0)
    box(top, "M2", xa - 0.2, ya - 0.145, xb + 0.2, ya + 0.145)

# ------------------------------------------------------------------------------------------------
# 2. pcas drain tracks (M0: below its row) and vpg (top source track) leave at its right end
# ------------------------------------------------------------------------------------------------
yt = {n: tr("oa_pcas", 0, y)[1] for n, y in
      (("vpg", -1.62), ("iout", 2.80), ("vnc", 3.30), ("vbr", 3.80), ("vpc", 4.30))}
# iout: up to the top edge in M2 (pin there); it leaves the high-impedance drains at once
seg("M2", X_TRK, yt["iout"], X_IOUT, yt["iout"])
seg("M2", X_IOUT, yt["iout"], X_IOUT, BY - W / 2)
# vnc: down in M1 onto nmir's top gate bar
seg("M2", X_TRK, yt["vnc"], X_VNC, yt["vnc"]); via(X_VNC, yt["vnc"])
seg("M1", X_VNC, yt["vnc"], X_VNC, Y_BAR - 0.13 + W / 2)
# vpc: M1 down, M2 east above misc_n, M2 down to MC10's drain, M1 east to MS3's drain
NNXv = lambda x: NNX + x
seg("M2", X_TRK, yt["vpc"], X_VPC, yt["vpc"]); via(X_VPC, yt["vpc"])
seg("M1", X_VPC, yt["vpc"], X_VPC, Y_VPC); via(X_VPC, Y_VPC)
x_mc10d, y_mc10d = NNXv(1.53), NNY + 5.0
seg("M2", X_VPC, Y_VPC, x_mc10d, Y_VPC); via(x_mc10d, Y_VPC)
seg("M2", x_mc10d, Y_VPC, x_mc10d, y_mc10d); via(x_mc10d, y_mc10d)       # M1 pad on the 0.16 um stripe
x_ms3d = NNXv(7.09)
seg("M1", x_mc10d, Y_VPC, x_ms3d, Y_VPC)
box(top, "M1", x_ms3d - 0.10, NNY + 9.90, x_ms3d + 0.10, Y_VPC)         # onto MS3's drain stub (y 9.35 ... 10)
# vbr: M1 down, M2 east, M2 down the channel to the mcs gate bar; branch onto misc_n's vbr gate bar
seg("M2", X_TRK, yt["vbr"], X_VBR, yt["vbr"]); via(X_VBR, yt["vbr"])
seg("M1", X_VBR, yt["vbr"], X_VBR, Y_VBR); via(X_VBR, Y_VBR)
path("M2", [(X_VBR, Y_VBR), (X_VBRCH, Y_VBR), (X_VBRCH, Y_MCSBAR), (X_MCSBAR, Y_MCSBAR)])
via(X_MCSBAR, Y_MCSBAR, m1=False)                                      # mcs bar M1 is 0.26 tall
x_vbrg = NNXv(0.90)
seg("M2", X_VBRCH, Y_BAR, x_vbrg, Y_BAR); via(x_vbrg, Y_BAR, m1=False)
# vpg: M2 east, M1 under iout, M2 east and up, onto SVPG's drain pad (oa_misc_p)
x_hop = X_IOUT + 0.60
seg("M2", X_TRK, yt["vpg"], X_VPC, yt["vpg"]); via(X_VPC, yt["vpg"])
seg("M1", X_VPC, yt["vpg"], x_hop, yt["vpg"]); via(x_hop, yt["vpg"])
x_svd, y_svd = tr("oa_misc_p", 7.54, 1.175)
path("M2", [(x_hop, yt["vpg"]), (X_VPG, yt["vpg"]), (X_VPG, y_svd), (x_svd, y_svd)])
via(x_svd, y_svd, m1=False)

# ------------------------------------------------------------------------------------------------
# 3. oa_misc_p <-> oa_misc_n: ks (high impedance) and en_3v3_b; en_3v3 to the top edge
# ------------------------------------------------------------------------------------------------
x_ks, y_ks = tr("oa_misc_p", 5.5, 13.275)                              # ks stub (cell 5.25..5.75, 12.95..13.6)
x_ms2d, y_ms2d = NNXv(3.81), NNY + 7.0
y_ksj = NNY + 12.81                                                    # jog under misc_p's ring
via(x_ks, y_ks, m1=False)
path("M2", [(x_ks, y_ks), (x_ks, y_ksj), (x_ms2d, y_ksj), (x_ms2d, y_ms2d)])
via(x_ms2d, y_ms2d)                                                    # M1 pad on MS2's drain stripe
x_ksg = NNXv(5.90)
seg("M2", x_ms2d, Y_BAR, x_ksg, Y_BAR); via(x_ksg, Y_BAR, m1=False)    # MS3 gate bar
y_kss, x_kss = NNY + 8.0, NNX + 9.6
seg("M2", x_ms2d, y_kss, x_kss, y_kss); via(x_kss, y_kss)
path("M1", [(x_kss, y_kss), (x_kss, NNY + 9.51), (NNXv(8.82), NNY + 9.51)])   # onto SKS's drain stripe
# en_3v3_b: misc_p MS1 gate column (cell x -0.91..-0.65) down to SKS's gate bar, and east to the pin
x_eb, y_eb = tr("oa_misc_p", -0.78, 12.4)
y_ebj = NNY + 11.31
x_sksg = NNXv(8.405)
via(x_eb, y_eb, m1=False)
path("M2", [(x_eb, y_eb), (x_eb, y_ebj), (x_sksg, y_ebj), (x_sksg, Y_BAR)])
via(x_sksg, Y_BAR, m1=False)
seg("M2", x_eb, y_ebj, BX - W / 2, y_ebj)
# en_3v3: SVPG's gate pad straight up to the top edge
x_en, y_en = tr("oa_misc_p", 8.35, 0.565)
via(x_en, y_en, m1=False)
seg("M2", x_en, y_en, x_en, BY - W / 2)

# ------------------------------------------------------------------------------------------------
# 4. nmir <-> misc_n / mcs: d10, vss tie, vres
# ------------------------------------------------------------------------------------------------
y_d10 = NY + 5.0
box(top, "M1", NX + 31.09, y_d10 - W / 2, NNXv(0.23), y_d10 + W / 2)    # r1 end stripe (d10) -> MC10 source
box(top, "M1", NX + 31.0, NY - 1.71, NNXv(0.30), NY - 1.11)            # nmir tie -> misc_n tie (vss)
box(top, "M1", *VSS_STRAP)
y_vres = NY - 4.02                                                     # nmir r2 vres trunk centre
seg("M2", NX + 27.5, y_vres, X_VRES, y_vres); via(X_VRES, y_vres)
path("M1", [(X_VRES, y_vres), (X_VRES, MY + 2.0), (MX + 61.73 + W / 2, MY + 2.0)])  # onto MCL's drain stripe

# ------------------------------------------------------------------------------------------------
# 5. Rails, straps, pins (pin layer / text convention of pad_buffer_cells.py: <metal>.pin + <metal>.text)
# ------------------------------------------------------------------------------------------------
box(top, "M1", *VSS_RAIL)
box(top, "M1", *VDD_RAIL)
for s in VDD_STRAPS:
    box(top, "M1", *s)
pin("M1", "vss", *VSS_RAIL)
pin("M1", "vdd", *VDD_RAIL)
pin("M2", "iout", X_IOUT - W / 2, BY - 0.5, X_IOUT + W / 2, BY)
pin("M2", "en_3v3", x_en - W / 2, BY - 0.5, x_en + W / 2, BY)
pin("M2", "en_3v3_b", BX - 0.5, y_ebj - W / 2, BX, y_ebj + W / 2)

bb = top.dbbox()
assert abs(bb.left) < 1e-6 and abs(bb.bottom) < 1e-6 and abs(bb.right - BX) < 1e-6 and abs(bb.top - BY) < 1e-6, bb
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False   # no date in the GDS header: the same input gives the same file
ly.write(OUT, opt)
print("wrote %s: top %s, %.3f x %.3f um = %.0f um2, pmir centre (cell) %s"
      % (OUT, TOP, bb.width(), bb.height(), bb.width() * bb.height(), PMIR_CENTRE))
