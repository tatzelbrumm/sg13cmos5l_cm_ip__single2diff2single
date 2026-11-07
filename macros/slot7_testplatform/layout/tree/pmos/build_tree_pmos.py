# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""tree_pmos: the PMOS devices of bias_tree_noab_pd (slot 7), compact and matched.

2026-11-07, claude, in the role of A4 (compact PMOS primitives, 2026-10-28).
Circuit (source of truth, not edited): macros/bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice
(+ bias_diodes in macros/bias_tree_pd/netlist/source/bias_ref_pd.spice). PMOS devices, all sg13_hv_pmos, B = vdd:
  BP (vbp vbp vdd) 5/6, PBN (vbn vbp vdd) 5/6, PBNC (vbnc vbp vdd) 2/6   mirror 5 : 5 : 2 units of 1/6
  MDBP (vdd vbp vdd) 2/6 dummy, BPC (vbpc vbpc vdd) 1/4 diode, TGP (iref en_3v3_b ni) 1/0.45 switch

Floorplan (score, left to right; one row, channel length vertical, sources up to the vdd plate / tie):

    | k | n | g | r a b c a b b x a b a c a b r | g | |       a = BP, b = PBN, c = PBNC (1/6 each)
    | t |   |   |                               |   | |       x = MDBP centre dummy 1/6, r = MDBP rest 0.5/6
                                                               k = BPC 1/4 (diode), t = TGP 1/0.45 (under k)
                                                               n / g = vbn drop / vbp gate column

Usage: python3 build_tree_pmos.py [out.gds] [out.spice]   (defaults: next to this script)
Rule values: libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json, key in the comment.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pdk = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "ihp-sg13cmos5l"))
sys.path += [pdk + "/libs.tech/klayout/python",
             pdk + "/libs.tech/klayout/python/pycell4klayout-api/source/python"]
import pya                               # noqa: E402
import sg13cmos5l_pycell_lib             # noqa: E402,F401  registers SG13_dev

# ---------------------------------------------------------------- rules (json key)
ACT_B = 0.21      # Act_b   Activ space
GAT_D = 0.07      # Gat_d   GatPoly (field) to Activ
CNT_A = 0.16      # Cnt_a   Cont size
CNT_B = 0.18      # Cnt_b   Cont space
CNT_C = 0.07      # Cnt_c   Activ enclosure of Cont
CNT_D = 0.07      # Cnt_d   GatPoly enclosure of Cont
CNT_E = 0.14      # Cnt_e   Cont on GatPoly to Activ
M1_B = 0.18       # M1_b    Metal1 space
M1_E = 0.22       # M1_e    Metal1 space next to wide (> 0.30) Metal1
M1_C1 = 0.05      # M1_c1   Metal1 endcap over Cont
V1_A = 0.19       # V1_a    Via1 size
V1_C = 0.01       # V1_c    Metal1 enclosure of Via1
V1_C1 = 0.05      # V1_c1   Metal1 endcap over Via1
MN_A = 0.20       # Mn_a    Metal2 width
MN_B = 0.21       # Mn_b    Metal2 space
M2_C1 = 0.05      # M2.c1   Metal2 endcap over Via1 (sg13cmos5l_maximal.drc rule text)
NW_C1 = 0.62      # NW_c1   NWell enclosure of P+Activ in ThickGateOx
NW_E1 = 0.62      # NW_e1   NWell enclosure of the N tie in ThickGateOx
PSD_D1 = 0.03     # pSD_d1  pSD space to N+Activ in NWell
FGAP = 0.25       # Gat_b1  finger gap: poly end caps (Gat_c 0.18) merge into one gate strip
TAB = V1_A + 2 * V1_C            # 0.21 Metal1 line that takes a Via1
PITCH2 = MN_A + MN_B             # 0.41 Metal2 track pitch

# ---------------------------------------------------------------- devices
ly = pya.Layout()
ly.dbu = 0.001
ly.technology_name = "sg13cmos5l"
LAY = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25),
       "Via1": (19, 0), "M2": (10, 0), "M2pin": (10, 2), "M2txt": (10, 25), "pSD": (14, 0), "NWell": (31, 0),
       "TGO": (44, 0), "TEXT": (63, 0)}
LI = {k: ly.layer(*v) for k, v in LAY.items()}


def g5(v):
    return round(round(v / 0.005) * 0.005, 3)


def box(c, lay, x0, y0, x1, y1):
    c.shapes(LI[lay]).insert(pya.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


def pin(c, net, x0, y0, x1, y1, metal="M1"):
    box(c, metal + "pin", x0, y0, x1, y1)
    c.shapes(LI[metal + "txt"]).insert(pya.DText(net, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))
    PINS.append((net, metal, g5(x0), g5(y0), g5(x1), g5(y1)))


def via1(c, x, y):
    box(c, "Via1", x - V1_A / 2, y - V1_A / 2, x + V1_A / 2, y + V1_A / 2)


DEVCELLS = {}


def device(name, w, l):
    """Unmodified SG13_dev pmosHV PCell, made static and renamed tree_pmos_<name>."""
    if name not in DEVCELLS:
        pc = ly.create_cell("pmosHV", "SG13_dev", {"w": "%gu" % w, "l": "%gu" % l, "ng": "1"})
        ci = ly.convert_cell_to_static(pc.cell_index())
        ly.delete_cell(pc.cell_index())
        ly.rename_cell(ci, "tree_pmos_" + name)
        DEVCELLS[name] = (ly.cell(ci), w, l)
    return DEVCELLS[name]


# score: letter -> (device, drain net, cell, w, l); the gate of the whole row is vbp, the source vdd
SCORE = "r a b c a b b x a b a c a b r"
VOICE = {"a": ("BP", "vbp", "u1l6", 1.0, 6.0), "b": ("PBN", "vbn", "u1l6", 1.0, 6.0),
         "c": ("PBNC", "vbnc", "u1l6", 1.0, 6.0), "x": ("MDBP", "vdd", "u1l6", 1.0, 6.0),
         "r": ("MDBP", "vdd", "r05l6", 0.5, 6.0)}
TRACKS = ["vbp", "vbn", "vbnc"]          # Metal2 lanes over the channels, bottom to top

PINS = []
DEVS = []                                # (inst name, d, g, s, b, w, l) for the netlist


def build():
    top = ly.create_cell("tree_pmos")
    L6 = 6.0 + 2 * 0.34                  # Activ length of an L = 6 finger (PCell: S/D 0.34 each side)
    yb = NW_C1                           # mirror Activ bottom; cell bottom at 0
    yt = yb + L6                         # mirror Activ top (sources)
    r270 = 3                             # DTrans rotation code: native x (L) -> -y, native y (W) -> x

    def place_r270(cell, x_left, y_top):
        top.insert(pya.DCellInstArray(cell.cell_index(), pya.DTrans(r270, False, g5(x_left), g5(y_top))))

    # ---------------- left column: BPC (k, R270, top aligned) over TGP (t, R0)
    xB = NW_C1                           # their Activ left edge; cell left edge at 0
    bpc, _, _ = device("bpc_w1l4", 1.0, 4.0)
    LB = 4.0 + 0.68
    place_r270(bpc, xB, yt)
    DEVS.append(("XBPC", "vbpc", "vbpc", "vdd", "vdd", 1.0, 4.0))
    yBb = yt - LB                        # BPC Activ bottom (drain = vbpc)
    tgp, _, _ = device("tgp_w1l045", 1.0, 0.45)
    yTt = yBb - 0.30                     # TGP Activ top: its poly end cap 0.18 + 0.12 (>= Gat_d) below BPC's Activ
    yTb = yTt - 1.0
    top.insert(pya.DCellInstArray(tgp.cell_index(), pya.DTrans(pya.DVector(g5(xB), g5(yTb)))))
    DEVS.append(("XTGP", "iref", "en_3v3_b", "ni", "vdd", 1.0, 0.45))
    # BPC gate column (vbpc) on its left; diode joint from the drain stripe; down to the bottom edge = pin
    xk1 = xB - M1_B                      # column right edge: M1_b from the stripes, which reach the Activ edge
    xk0 = xk1 - TAB
    yc_top = yt - 0.23 - M1_E            # column ends M1_e below the vdd plate (stripe bottom yt - 0.23)
    box(top, "M1", xk0, 0, xk1, yc_top)
    gate_contacts(top, xk0, xk1, yBb + 0.34, yt - 0.34, yc_top, xB)
    box(top, "M1", xk1 - 0.01, yBb + 0.07, xB + 0.01, yBb + 0.23)        # drain stripe -> gate column
    pin(top, "vbpc", xk0, 0, xk1, 0.30)
    # TGP: S/D stripes (iref left, ni right) and the gate down to the bottom edge, 0.21 wide
    for net, xs in (("iref", 0.15), ("ni", 0.98)):
        x0 = xB + xs - TAB / 2
        box(top, "M1", x0, 0, x0 + TAB, yTb + 0.5)
        pin(top, net, x0, 0, x0 + TAB, 0.30)
    xg = xB + 0.565                      # gate centre (poly 0.34 .. 0.79)
    cy1 = yTb - CNT_E                    # gate contact top, Cnt_e below the Activ
    box(top, "GatPoly", xB + 0.34, cy1 - CNT_A - CNT_D, xB + 0.79, yTb - 0.18)
    box(top, "Cont", xg - CNT_A / 2, cy1 - CNT_A, xg + CNT_A / 2, cy1)
    box(top, "M1", xg - TAB / 2, 0, xg + TAB / 2, cy1 + M1_C1)
    pin(top, "en_3v3_b", xg - TAB / 2, 0, xg + TAB / 2, 0.30)
    x_ni1 = xB + 0.98 + TAB / 2

    # ---------------- vbn drop, left gate column, the mirror row, right gate column, vbnc drop
    xn0 = max(x_ni1, xB + 1.0) + M1_B    # vbn drop: M1_b from TGP's ni line and BPC's stripes
    xn1 = xn0 + TAB
    xg0 = xn1 + M1_B                     # left gate column (vbp)
    xg1 = xg0 + TAB
    x = xg1 + M1_B                       # first Activ (rest): M1_b from the column (contact >= Cnt_e from Activ)
    ytr = {n: yb + 0.40 + k * PITCH2 for k, n in enumerate(TRACKS)}     # lanes over the channel (from yb + 0.34)
    fingers = []                         # (letter, x_left, w)
    unit, _, _ = device("u1l6", 1.0, 6.0)
    rest, _, _ = device("r05l6", 0.5, 6.0)
    count = {}
    for letter in SCORE.split():
        dev, dnet, cname, w, l = VOICE[letter]
        place_r270(unit if cname == "u1l6" else rest, x, yt)
        if letter == "r":
            tag = "rL" if "MDBP_rL" not in count else "rR"
        elif letter == "x":
            tag = "x"
        else:
            tag = str(sum(1 for k in count if k.startswith(dev + "_")) + 1)
        count[dev + "_" + tag] = 1
        DEVS.append(("X%s_%s" % (dev, tag), dnet, "vbp", "vdd", "vdd", w, l))
        fingers.append((letter, x, w))
        x += w + FGAP
    xa0, xa1 = fingers[0][1], fingers[-1][1] + fingers[-1][2]           # row Activ span
    xr0 = xa1 + M1_B                     # right gate column
    xr1 = xr0 + TAB
    xc0 = xr1 + M1_B                     # vbnc drop
    xc1 = xc0 + TAB
    # gate columns, poly tabs, contacts
    box(top, "M1", xg0, 0, xg1, yc_top)
    gate_contacts(top, xg0, xg1, yb + 0.34, yt - 0.34, yc_top, xa0)
    box(top, "M1", xr0, 0, xr1, yc_top)
    gate_contacts(top, xr0, xr1, yb + 0.34, yt - 0.34, yc_top, xa1)
    pin(top, "vbp", xg0, 0, xg1, 0.30)
    # drain tabs (identical for every real finger), straps of the dummies, vias onto the lanes
    ytab1 = ytr[TRACKS[-1]] + V1_A / 2 + V1_C1
    for letter, x0, w in fingers:
        xc = x0 + w / 2
        dev, dnet = VOICE[letter][:2]
        if dnet == "vdd":
            box(top, "M1", xc - TAB / 2, yb + 0.07, xc + TAB / 2, yt - 0.07)
        else:
            box(top, "M1", xc - TAB / 2, yb + 0.07, xc + TAB / 2, ytab1)
            via1(top, xc, ytr[dnet])
    # lanes: all three over the whole row (identical metal over every channel), then to their exits
    xdn = (xn0 + xn1) / 2
    xdc = (xc0 + xc1) / 2
    end = V1_A / 2 + M2_C1
    lane = {"vbp": ((xg0 + xg1) / 2 - end, (xr0 + xr1) / 2 + end),
            "vbn": (xdn - end, xa1),
            "vbnc": (xa0, xdc + end)}
    for n, (x0, x1) in lane.items():
        box(top, "M2", x0, ytr[n] - MN_A / 2, x1, ytr[n] + MN_A / 2)
    via1(top, (xg0 + xg1) / 2, ytr["vbp"])
    via1(top, (xr0 + xr1) / 2, ytr["vbp"])
    via1(top, xdn, ytr["vbn"])
    via1(top, xdc, ytr["vbnc"])
    box(top, "M1", xn0, 0, xn1, ytr["vbn"] + V1_A / 2 + V1_C1)
    box(top, "M1", xc0, 0, xc1, ytr["vbnc"] + V1_A / 2 + V1_C1)
    pin(top, "vbn", xn0, 0, xn1, 0.30)
    pin(top, "vbnc", xc0, 0, xc1, 0.30)

    # ---------------- outline, tie, vdd plate, wells, implant
    W = g5(max(xc1, xdc + end, xa1 + NW_C1))
    yta0 = yt + 0.18 + PSD_D1            # tie Activ: pSD_d1 above the PCells' pSD (pSD_c 0.18 above Activ)
    yta0 = max(yta0, yt + ACT_B)
    yta1 = yta0 + 2 * CNT_C + CNT_A      # one contact row: 0.30
    H = g5(yta1 + NW_E1)
    xt0, xt1 = NW_E1, W - NW_E1
    box(top, "Activ", xt0, yta0, xt1, yta1)
    n = int((xt1 - xt0 - 2 * CNT_C - CNT_A) // (CNT_A + CNT_B)) + 1
    span = (n - 1) * (CNT_A + CNT_B) + CNT_A
    cx0 = g5((xt0 + xt1) / 2 - span / 2)      # snap the start once, then step by the on-grid pitch (P11)
    for i in range(n):
        x0 = cx0 + i * (CNT_A + CNT_B)
        box(top, "Cont", x0, yta0 + CNT_C, x0 + CNT_A, yta0 + CNT_C + CNT_A)
    box(top, "M1", 0, yt - 0.23, W, H)                                   # vdd plate = the rail side
    pin(top, "vdd", 0, H - 0.30, W, H)
    box(top, "NWell", 0, 0, W, H)
    box(top, "TGO", 0, 0, W, H)
    # one pSD over all P+ (closes the pSD_b 0.31 notches between the PCells' implants), below the tie
    bb = pya.DBox()
    for inst in top.each_inst():
        r = pya.Region(ly.cell(inst.cell_index).begin_shapes_rec(LI["pSD"])).transformed(inst.cplx_trans)
        bb += r.bbox().to_dtype(ly.dbu)
    box(top, "pSD", bb.left, bb.bottom, bb.right, yt + 0.18)
    for letter, x0, w in fingers:
        top.shapes(LI["TEXT"]).insert(pya.DText(letter, g5(x0 + w / 2), g5(yb + 3.5)))
    return top, dict(W=W, H=H, yb=yb, yt=yt, tracks=ytr, fingers=fingers, xa=(xa0, xa1), tie=(xt0, yta0, xt1, yta1),
                     cols=dict(vbpc=(xk0, xk1), vbn=(xn0, xn1), vbpL=(xg0, xg1), vbpR=(xr0, xr1), vbnc=(xc0, xc1)),
                     bpc=(xB, yBb), tgp=(xB, yTb))


def gate_contacts(top, x0, x1, ypoly0, ypoly1, ycol1, xact):
    """Poly tab from the gate strip (y ypoly0 .. ypoly1) to a Metal1 column x0 .. x1 with a contact column.
    xact: the Activ edge the strip ends at (contact >= Cnt_e from it)."""
    xm = (x0 + x1) / 2
    cx0, cx1 = xm - CNT_A / 2, xm + CNT_A / 2
    assert min(abs(xact - cx0), abs(xact - cx1)) >= CNT_E - 1e-9, "contact too close to Activ"
    px0 = min(cx0 - CNT_D, xact)
    px1 = max(cx1 + CNT_D, xact)
    box(top, "GatPoly", px0, ypoly0, px1, ypoly1)
    c0, c1 = ypoly0 + CNT_D, min(ypoly1 - CNT_D, ycol1 - M1_C1)
    n = int((c1 - c0 - CNT_A) // (CNT_A + CNT_B)) + 1
    span = (n - 1) * (CNT_A + CNT_B) + CNT_A
    y = g5((c0 + c1) / 2 - span / 2)
    for i in range(n):
        box(top, "Cont", cx0, y + i * (CNT_A + CNT_B), cx1, y + i * (CNT_A + CNT_B) + CNT_A)


def spice(path, info):
    ports = "vdd vbp vbn vbnc vbpc iref ni en_3v3_b"
    out = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* tree_pmos: PMOS devices of bias_tree_noab_pd as drawn (generated by build_tree_pmos.py).",
           "* Fingers of the same L in parallel; netgen merges them to the source netlist's devices:",
           "*   BP 5 x 1/6 = 5/6, PBN 5 x 1/6 = 5/6, PBNC 2 x 1/6 = 2/6, MDBP 1/6 + 2 x 0.5/6 = 2/6, BPC 1/4, TGP 1/0.45.",
           "* score (left to right): " + SCORE,
           ".subckt tree_pmos " + ports]
    for name, d, g, s, b, w, l in DEVS:
        out.append("%s %s %s %s %s sg13_hv_pmos w=%gu l=%gu ng=1" % (name, d, g, s, b, w, l))
    out.append(".ends tree_pmos")
    open(path, "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    gds = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "tree_pmos.gds")
    sp = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "tree_pmos.spice")
    top, info = build()
    for c in list(ly.top_cells()):
        if c.name != "tree_pmos":
            ly.delete_cell_rec(c.cell_index())
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(gds, opt)
    spice(sp, info)
    bb = top.dbbox()
    print("wrote %s: tree_pmos %.3f x %.3f um = %.1f um2, bbox %s" % (gds, bb.width(), bb.height(),
                                                                     bb.width() * bb.height(), bb))
    for p in PINS:
        print("pin %-9s %s (%.3f, %.3f; %.3f, %.3f)" % p)
    print("lanes", {k: round(v, 3) for k, v in info["tracks"].items()}, "cols", info["cols"])
