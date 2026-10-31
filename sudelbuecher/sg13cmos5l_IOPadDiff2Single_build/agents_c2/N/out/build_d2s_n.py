# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Compact NMOS cells of d2s_mpdda_pd for the IOPadDiff2Single pad cell (IHP sg13cmos5l), 2026-10-31, agent N.

    python3 build_d2s_n.py [out_dir]          (run from anywhere; reads ../inputs/pad_buffer_klayout/pad_buffer_cells.gds)

Cells (d2s_n_cells.gds, each standalone-checkable; reference netlists d2s_n_cells.cdl):
  sinks_6x6_c      upright, 2 columns of 8 fingers 6/6 (map X Y Y X X Y / Y X X Y Y X, BN and narrow dummies at the ends)
  sinks_6x6_s2d_c  the same cell rotated R90 (native, long side horizontal) for the s2d pad
  d2s_casc_n_c     upright, CX CX | CY CY (15/3) + BNC (1/8)
  d2s_ab_n_c       RN2, FNL, ABN (4.4/1)
  d2s_pd_n_c       SB (source vsso), SABN (source vss) (1/0.45)
Device cells are copied unmodified from the library. Every rule value comes from sg13cmos5l_tech_default.json through
A3's process adapter (inputs/A3/out/skill); rules.md of this build cites each value used.
Drawing convention (all cells): PCell fingers unrotated (gate vertical, W along y, S/D stripes vertical), stacked along
y at Gat.b1 (poly of a column merges), columns side by side at Act.b; no tie between columns, one tie strip at an edge.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INP = os.path.join(HERE, "..", "inputs")
sys.path.insert(0, os.path.join(INP, "A3", "out", "skill", "generic"))
sys.path.insert(0, os.path.join(INP, "A3", "out", "skill", "ihp_sg13cmos5l"))
import klayout.db as db                      # noqa: E402
import generator as g                        # noqa: E402  (A3's process-agnostic helpers: Ctx, Mos, outline, write_cdl)
import adapter as proc                       # noqa: E402  (A3's IHP adapter: rule keys -> json values)

PDK_JSON = "/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json"
LIB = os.path.join(INP, "pad_buffer_klayout", "pad_buffer_cells.gds")
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE
MODEL = "sg13_hv_nmos"
# library device cells (exported SG13_dev nmosHV variants: W / L)
DEV = {"6/6": "nmosHV", "2/6": "nmosHV$12", "15/3": "nmosHV$1", "1/8": "nmosHV$2", "4.4/1": "nmosHV$3",
       "1/0.45": "nmosHV$5"}
# F's placement (variant 1): sinks x 59.5, casc_n x 66.5 -> the sinks' x / y bottom pins sit at the casc's x / y top pins
SINKS_X, CASC_X = 59.5, 66.5

P = proc.Process(PDK_JSON)
lib = db.Layout()
lib.read(LIB)
ly = db.Layout()
ly.dbu = lib.dbu
cx = g.Ctx(P, ly)
DC = {k: g.copy_cell(lib, v, ly) for k, v in DEV.items()}
MS = {k: g.Mos(cx, DC[k], MODEL) for k in DEV}
R = cx.r
FG = R("finger_gap")          # 0.25 Gat_b1: fingers stacked at this gap, polys merge
AB = R("active_space")        # 0.21 Act_b
M1B = R("m1_space")           # 0.18
HW = 0.08                     # half width of the PCell's M1 stripe (0.16 = M1_a)
TW = cx.track_w()             # 0.29 M2 track / pin width
PH = cx.pad_h()               # 0.21 M1 pad across a stripe
VE = R("via1") / 2 + R("via1_m1_endcap")      # 0.145: pad end beyond a via centre
TGO_A = R("thickox_over_active")              # 0.27
CE = R("m1_cont_endcap")                      # 0.05


def snap(v):
    return g.snap(v)


# ------------------------------------------------------------------ drawing helpers (final frame, y up)
def m1(c, x0, y0, x1, y1):
    cx.box(c, "metal1", x0, y0, x1, y1)


def m2(c, x0, y0, x1, y1):
    cx.box(c, "metal2", x0, y0, x1, y1)


def via(c, x, y, n=1, vertical=False):
    cx.vias(c, x, y, n, vertical)


def vpad(c, x, y, n=3):
    """M1 pad centred on a vertical stripe, n Via1 in a column"""
    ln = cx.pad_len(n)
    m1(c, x - PH / 2, y - ln / 2, x + PH / 2, y + ln / 2)
    via(c, x, y, n, vertical=True)


def poly_contacts(c, x0, x1, y, step=None):
    """one row of contacts (centre height y) from x0 to x1; returns the x range covered incl. the M1 end caps"""
    p = cx.cont_pitch()
    n = int((x1 - x0 - R("cont")) / p + 1e-6) + 1
    for k in range(n):
        xx = snap(x0 + k * p)
        cx.box(c, "contact", xx, y - R("cont") / 2, xx + R("cont"), y + R("cont") / 2)
    return snap(x0 - CE), snap(x0 + (n - 1) * p + R("cont") + CE)


def vtie(c, x0, ya, yb):
    """p+ substrate tie strip, one contact column: Activ [x0, x0 + 0.30] x [ya, yb], pSD 0.03 round it (pSD_c1).
    Returns the M1 box (contacts + endcap)."""
    cc, cn, p = R("cont_in_active"), R("cont"), cx.cont_pitch()
    w = cn + 2 * cc
    cx.box(c, "active", x0, ya, x0 + w, yb)
    e = R("tie_impl_enc")
    cx.box(c, "pimp", x0 - e, ya - e, x0 + w + e, yb + e)
    n = int((yb - ya - 2 * cc - cn) / p + 1e-6) + 1
    for k in range(n):
        yy = snap(ya + cc + k * p)
        cx.box(c, "contact", x0 + cc, yy, x0 + cc + cn, yy + cn)
    assert (yb - ya) - (n - 1) * p - cn - cc <= R("tie_cont_ext_max") + 1e-9     # LU.d1
    box = (snap(x0 + cc - CE), snap(ya + cc - CE), snap(x0 + cc + cn + CE), snap(ya + cc + (n - 1) * p + cn + CE))
    m1(c, *box)
    return box


def finger(c, key, x, y):
    c.insert(db.DCellInstArray(DC[key].cell_index(), db.DTrans(snap(x), snap(y))))


def tgo(c, extra=()):
    """ThickGateOx outline: Activ + TGO_a united with the PCells' own TGO, closed at TGO_e (one polygon)"""
    for b in extra:
        cx.box(c, "thickox", *b)
    return g.outline(cx, c, "thickox", [("active", TGO_A), ("thickox", 0.0)], R("thickox_space"))


def normalise(c):
    """translate so that the bounding box starts at (0, 0); returns the bbox (before) and (w, h)"""
    bb = c.dbbox()
    c.transform(db.DTrans(snap(-bb.left), snap(-bb.bottom)))
    return bb, (snap(bb.width()), snap(bb.height()))


def pin1(c, net, x0, y0, x1, y1):
    cx.pin(c, 1, net, x0, y0, x1, y1)


def pin2(c, net, x0, y0, x1, y1):
    cx.pin(c, 2, net, x0, y0, x1, y1)


def dev(nm, d, gt, s, key):
    m = MS[key]
    return ("%s" % nm, d, gt, s, "vss", MODEL, m.W, m.L)


# ================================================================== sinks_6x6_c (upright)
def sinks(name, xt_x_rel, rep=1):
    """xt_x_rel: x pin (centre, from the cell's left edge) of the bottom x pin; y pin is 0.51 right of it"""
    c = ly.create_cell(name)
    m6 = MS["6/6"]
    lact, sc0, sc1 = m6.lact, m6.stripe_c[0], m6.stripe_c[1]
    pitch_tr = 0.51                                              # x / y trunk pitch = casc_n's x / y stripe pitch
    # channel: trunks x / y at xt / xt + 0.51. xt: M2 of the left-edge exit (via on A's D stripe + 0.145) + Mn_b + 0.145
    xt = snap(sc1 + VE + R("m2_space") + TW / 2)
    yt = snap(xt + pitch_tr)
    b0 = snap(yt + VE + M1B - (sc0 - HW))                       # B's D stripe M1 keeps M1_b from the y pad
    # map per column (bottom to top): A = BN, (Y X X Y Y X) x rep, dummy; B = dummy, (X Y Y X X Y) x rep, dummy
    # (B is A point-reflected); rep = 1 is the 6 + 6 fingers of the circuit, rep = 4 the 4x option of P4
    colA = [("B", "6/6")] + [(t, "6/6") for t in "YXXYYX" * rep] + [("d", "2/6")]
    colB = [("d", "2/6")] + [(t, "6/6") for t in "XYYXXY" * rep] + [("d", "2/6")]
    net = {"B": "vbn", "X": "x", "Y": "y", "d": "vss"}
    fing, devl = [], []
    for ci, (col, x0, nm) in enumerate(((colA, 0.0, "A"), (colB, b0, "B"))):
        y = 0.0
        for k, (lt, key) in enumerate(col):
            mm = MS[key]
            finger(c, key, x0, y)
            fing.append(dict(col=nm, k=k, lt=lt, key=key, x0=x0, y0=y, y1=snap(y + mm.W)))
            dn = net[lt]
            nmx = {"B": "BN", "X": "SX", "Y": "SY", "d": "dummy"}[lt]
            devl.append(("%s_%s%d" % (nmx, nm, k), dn, "vbn", "vss", "vss", MODEL, mm.W, mm.L))
            y = snap(y + mm.W + FG)
    yA = max(f["y1"] for f in fing if f["col"] == "A")
    b1 = snap(b0 + lact)
    # --- centroid check (reasoning made measurable): X and Y share one centroid in x and y
    cen = {}
    for lt in "XY":
        pts = [((f["x0"] + lact / 2), (f["y0"] + f["y1"]) / 2) for f in fing if f["lt"] == lt]
        cen[lt] = (round(sum(p[0] for p in pts) / len(pts), 4), round(sum(p[1] for p in pts) / len(pts), 4))
    assert cen["X"] == cen["Y"], cen
    # --- poly gate plates + vbn bar below the columns (BN's D stripe joins the bar: diode)
    cy_ = -(M1B + 0.145)                                         # contact centre: bar [y0-0.47, y0-0.18]
    bar = (snap(cy_ - 0.145), snap(cy_ + 0.145))
    cw = R("cont")
    xs = []
    for x0 in (0.0, b0):
        gx0, gx1 = x0 + m6.sd, x0 + m6.sd + m6.L
        cx.box(c, "poly", gx0, snap(cy_ - cw / 2 - R("cont_in_poly")), gx1, 0.0)
        xs.append(poly_contacts(c, gx0 + R("cont_in_poly"), gx1 - R("cont_in_poly"), cy_))
    m1(c, xs[0][0], bar[0], xs[1][1], bar[1])
    m1(c, sc1 - HW, bar[0], sc1 + HW, 0.0)                       # BN: D stripe down to the bar (finger A0 = BN)
    xv = 1.2
    via(c, xv, cy_)
    ybot = -0.52                                                 # PCell TGO below the first finger
    m2(c, xv - TW / 2, ybot, xv + TW / 2, 0.05)
    pin2(c, "vbn", xv - TW / 2, ybot, xv + TW / 2, 0.05)
    # --- vss bus: S lines of both columns, dummies' D stripes, strap above column A; tie strip on the right edge
    ytop_strap = snap(yA + M1B + PH)
    m1(c, sc0 - HW, 0.0, sc0 + HW, ytop_strap)                                   # A: S line
    m1(c, b0 + sc1 - HW, 0.0, b0 + sc1 + HW, ytop_strap)                         # B: S line
    m1(c, sc1 - HW, [f for f in fing if f["col"] == "A"][-1]["y0"], sc1 + HW, ytop_strap)      # A top dummy D -> strap
    fB = [f for f in fing if f["col"] == "B"]
    m1(c, b0 + sc0 - HW, fB[-1]["y0"], b0 + sc0 + HW, ytop_strap)                # B top dummy D -> strap
    m1(c, b0 + sc0 - HW, snap(fB[0]["y0"] + 0.9), b0 + sc1 + HW, snap(fB[0]["y0"] + 1.1))   # B bottom dummy: D to S
    m1(c, sc0 - HW, snap(ytop_strap - PH), b0 + sc1 + HW, ytop_strap)           # strap
    tx0 = snap(b1 + AB)
    tm = vtie(c, tx0, 0.0, yA)
    edge_r = snap(tx0 + 0.30 + TGO_A)
    yp0 = snap(4.0 - ybot + 0.5)                                 # tap pad 0.6 x 0.6 at 4.5 .. 5.1 above the bottom edge
    m1(c, snap(edge_r - 0.6), yp0, edge_r, snap(yp0 + 0.6))
    m1(c, b0 + sc1 - HW, snap(yp0 + 0.2), snap(edge_r - 0.5), snap(yp0 + 0.2 + PH))      # bus -> pad (single tap)
    pin1(c, "vss", snap(edge_r - 0.6), yp0, edge_r, snap(yp0 + 0.6))
    # --- x / y: M1 stubs from the D stripes into the channel, trunks x / y in M2 (Via1 at the stub ends)
    trunk = {"x": [], "y": []}
    tx = {"x": xt, "y": yt}
    for f in fing:
        if f["lt"] not in "XY":
            continue
        n = f["lt"].lower()
        if f["col"] == "A":
            ys = snap(f["y0"] + 1.5)
            m1(c, sc1 - HW, ys - PH / 2, tx[n] + VE, ys + PH / 2)
        else:
            ys = snap(f["y0"] + 4.5)
            m1(c, tx[n] - VE, ys - PH / 2, b0 + sc0 + HW, ys + PH / 2)
        via(c, tx[n], ys)
        trunk[n].append(ys)
    # left-edge exits: a Via1 on an A finger's D stripe and M2 to the left edge (no crossing of the trunks)
    left = {}
    for n, k in (("x", 2), ("y", 1)):
        f = [f for f in fing if f["col"] == "A"][k]
        assert f["lt"] == n.upper()
        ys = snap(f["y0"] + 4.5)
        m1(c, sc1 - PH / 2, ys - VE, sc1 + PH / 2, ys + VE)
        via(c, sc1, ys)
        m2(c, -TGO_A, ys - TW / 2, sc1 + VE, ys + TW / 2)
        pin2(c, n, -TGO_A, ys - TW / 2, -TGO_A + 0.7, ys + TW / 2)
        left[n] = ys
    # trunks with a jog to the pin positions (xt_x_rel counted from the left edge -0.27)
    pj = {"x": snap(xt_x_rel - TGO_A), "y": snap(xt_x_rel - TGO_A + 0.51)}
    yj = {"x": 3.2, "y": 4.6}
    for n in "xy":
        t = tx[n]
        m2(c, t - TW / 2, yj[n] - TW / 2, t + TW / 2, max(trunk[n]) + VE)
        m2(c, min(t, pj[n]) - TW / 2, yj[n] - TW / 2, max(t, pj[n]) + TW / 2, yj[n] + TW / 2)
        m2(c, pj[n] - TW / 2, ybot, pj[n] + TW / 2, yj[n] + TW / 2)
        pin2(c, n, pj[n] - TW / 2, ybot, pj[n] + TW / 2, ybot + 0.6)
    for f in fing:
        cx.text(c, "note", {"B": "BN", "X": "SX", "Y": "SY", "d": "dummy"}[f["lt"]], f["x0"] + lact / 2,
                (f["y0"] + f["y1"]) / 2)
    tgo(c, extra=[(b0, ybot, edge_r, snap(yA + 0.52))])
    bb, wh = normalise(c)
    info = dict(size=wh, xt=xt, b0=b0, tie=(tx0, edge_r), left=left, pj=pj, bb=bb, centroid=cen, bar=bar)
    return c, info, devl


# ================================================================== d2s_casc_n_c (upright)
def casc(name):
    c = ly.create_cell(name)
    mc, mb = MS["15/3"], MS["1/8"]
    lact, sc0, sc1 = mc.lact, mc.stripe_c[0], mc.stripe_c[1]
    b0 = snap(lact + AB)
    devl = []
    ys0 = [0.0, snap(mc.W + FG)]
    for x0, nm, d, s in ((0.0, "CX", "l1", "x"), (b0, "CY", "b", "y")):
        for k, y in enumerate(ys0):
            finger(c, "15/3", x0, y)
            devl.append(("%s_%d" % (nm, k), d, "vbnc", s, "vss", MODEL, mc.W, mc.L))
    ytop = snap(ys0[1] + mc.W)
    # poly plate between the column tops and BNC: gate contacts of both columns and of BNC on one poly body
    pb = snap(ytop + R("poly_endcap"))                           # column poly ends here
    yb = snap(max(ytop + AB, pb + M1B + 0.29 + R("poly_endcap") + 0.0))   # BNC Activ bottom: bar [pb, pb + 0.29] + M1_b
    # BNC poly bottom = yb - endcap; plate spans pb .. yb - endcap
    cyc = snap(pb + 0.145)                                        # contact centre
    cx.box(c, "poly", mb.sd, snap(pb - 0.03), mb.sd + mb.L, snap(yb - R("poly_endcap") + 0.03))
    finger(c, "1/8", 0.0, yb)
    xr = poly_contacts(c, mb.sd + R("cont_in_poly"), mb.sd + mb.L - R("cont_in_poly") - 0.06, cyc)
    m1(c, xr[0], snap(cyc - 0.145), snap(mb.stripe_c[1] + HW), snap(cyc + 0.145))     # vbnc bar
    m1(c, mb.stripe_c[1] - HW, snap(cyc - 0.145), mb.stripe_c[1] + HW, snap(yb + mb.W))  # BNC D stripe joins the bar
    devl.append(("BNC", "vbnc", "vbnc", "vss", "vss", MODEL, mb.W, mb.L))
    ybt = snap(yb + mb.W)
    # vss: BNC S stripe up and over to the tie strip on the right edge
    ystrap = snap(ybt + M1B + PH)
    tx0 = snap(mb.lact + AB)
    m1(c, mb.stripe_c[0] - HW, yb, mb.stripe_c[0] + HW, ystrap)
    tm = vtie(c, tx0, 0.0, ybt)
    m1(c, mb.stripe_c[0] - HW, snap(ystrap - PH), tm[2], ystrap)
    m1(c, tm[0], tm[3], tm[2], ystrap)
    edge_r = snap(tx0 + 0.30 + TGO_A)
    m1(c, snap(tm[2] - 0.1), 4.5, edge_r, snap(4.5 + 0.31))
    pin1(c, "vss", snap(edge_r - 0.31), 4.5, edge_r, snap(4.5 + 0.31))
    # M2 trunks over the stripes: l1 (left of column 0, down), b (right of column 1, down), x / y (inner, up)
    ybot, ymax = -0.52, snap(ybt + 0.52)
    cxy = snap(0.5 * (ys0[0] + mc.W))
    lines = {"l1": (sc0, 0), "x": (sc1, 1), "y": (b0 + sc0, 1), "b": (b0 + sc1, 0)}
    for n, (xx, up) in lines.items():
        ys = [snap(y + mc.W / 2) for y in ys0]
        for yy in ys:
            vpad(c, xx, yy)
        if up:
            m2(c, xx - TW / 2, ys[0] - 0.555, xx + TW / 2, ymax)
            pin2(c, n, xx - TW / 2, snap(ymax - 0.6), xx + TW / 2, ymax)
        else:
            m2(c, xx - TW / 2, ybot, xx + TW / 2, ys[-1] + 0.555)
            pin2(c, n, xx - TW / 2, ybot, xx + TW / 2, ybot + 0.6)
    # vbnc: Via1 on the bar, M2 to the left edge
    xv = 0.95
    via(c, xv, cyc)
    m2(c, -TGO_A, snap(cyc - TW / 2), snap(xv + VE), snap(cyc + TW / 2))
    pin2(c, "vbnc", -TGO_A, snap(cyc - TW / 2), -TGO_A + 0.7, snap(cyc + TW / 2))
    for nm, x0, y0, mm in (("CX", 0.0, 0.0, mc), ("CX", 0.0, ys0[1], mc), ("CY", b0, 0.0, mc), ("CY", b0, ys0[1], mc),
                           ("BNC", 0.0, yb, mb)):
        cx.text(c, "note", nm, x0 + mm.lact / 2, y0 + mm.W / 2)
    tgo(c)
    bb, wh = normalise(c)
    info = dict(size=wh, bb=bb, x_pin=snap(sc1 + TGO_A), y_pin=snap(b0 + sc0 + TGO_A), b_pin=snap(b0 + sc1 + TGO_A),
                l1_pin=snap(sc0 + TGO_A), vbnc_y=snap(cyc - bb.bottom), tie=(tx0, edge_r))
    return c, info, devl


# ================================================================== d2s_ab_n_c
def ab(name):
    c = ly.create_cell(name)
    m = MS["4.4/1"]
    lact, sc0, sc1, W = m.lact, m.stripe_c[0], m.stripe_c[1], m.W
    pit = snap(lact + AB)
    # fingers left to right: ABN (S b | D a), FNL (S l1 | D l2), RN2 (D vabn | S dabn)
    xs = [0.0, pit, 2 * pit]
    for x in xs:
        finger(c, "4.4/1", x, 0.0)
    devl = [dev("ABN", "a", "vabn", "b", "4.4/1"), dev("FNL", "l2", "vabn", "l1", "4.4/1"),
            dev("RN2", "vabn", "vabn", "dabn", "4.4/1")]
    # poly plate over the three gates at the top, contacts, M1 bar (vabn); RN2's D stripe is part of it (diode)
    pt = snap(W + R("poly_endcap"))
    cyc = snap(W + M1B + 0.145)
    gx0, gx1 = xs[0] + m.sd, xs[2] + m.sd + m.L
    cx.box(c, "poly", gx0, snap(pt - 0.03), gx1, snap(cyc + R("cont") / 2 + R("cont_in_poly")))
    xv = snap(xs[2] + sc0)                                        # vabn: Via1 on the bar over RN2's D stripe, M2 up
    bar_r = snap(xv + VE)
    xr = poly_contacts(c, gx0 + R("cont_in_poly"), bar_r - CE, cyc)
    m1(c, xr[0], snap(cyc - 0.145), bar_r, snap(cyc + 0.145))
    m1(c, xs[2] + sc0 - HW, W, xs[2] + sc0 + HW, snap(cyc + 0.145))
    top = snap(W + 0.52)
    via(c, xv, cyc)
    m2(c, xv - TW / 2, snap(top - 0.7), xv + TW / 2, top)
    pin2(c, "vabn", xv - TW / 2, snap(top - 0.6), xv + TW / 2, top)
    ybot = -0.52
    # M2: b (ABN S, down), l1 / l2 (FNL, up); M1: a (ABN D, down), dabn (RN2 S, down)
    for n, xx in (("l1", xs[1] + sc0), ("l2", xs[1] + sc1)):
        vpad(c, xx, W / 2)
        m2(c, xx - TW / 2, snap(W / 2 - 0.555), xx + TW / 2, top)
        pin2(c, n, xx - TW / 2, snap(top - 0.6), xx + TW / 2, top)
    vpad(c, xs[0] + sc0, W / 2)
    m2(c, xs[0] + sc0 - TW / 2, ybot, xs[0] + sc0 + TW / 2, snap(W / 2 + 0.555))
    pin2(c, "b", xs[0] + sc0 - TW / 2, ybot, xs[0] + sc0 + TW / 2, ybot + 0.6)
    for n, xx in (("a", xs[0] + sc1), ("dabn", xs[2] + sc1)):
        m1(c, xx - HW, ybot, xx + HW, 0.0)
        m1(c, xx - TW / 2, ybot, xx + TW / 2, snap(ybot + 0.32))
        pin1(c, n, xx - TW / 2, ybot, xx + TW / 2, snap(ybot + 0.32))
    # p tie strip on the left edge, vss pin flush with the edge
    tx0 = snap(-AB - 0.30)
    tm = vtie(c, tx0, 0.0, W)
    edge_l = snap(tx0 - TGO_A)
    m1(c, edge_l, 1.5, snap(tm[0] + 0.1), snap(1.5 + 0.31))
    pin1(c, "vss", edge_l, 1.5, snap(edge_l + 0.31), snap(1.5 + 0.31))
    # right edge faces ab_p's NWell: keep N+ Activ >= NW_d1 0.62 inside the outline (TGO covers the margin)
    right = snap(xs[2] + lact)
    margin = R("well_to_nact_hv")
    for nm, xx in (("ABN", xs[0]), ("FNL", xs[1]), ("RN2", xs[2])):
        cx.text(c, "note", nm, xx + lact / 2, W / 2)
    tgo(c, extra=[(right, ybot, snap(right + margin), top)])
    bb, wh = normalise(c)
    return c, dict(size=wh, bb=bb, xs=xs, top=top), devl


# ================================================================== d2s_pd_n_c
def pd(name):
    c = ly.create_cell(name)
    m = MS["1/0.45"]
    lact, sc0, sc1, W = m.lact, m.stripe_c[0], m.stripe_c[1], m.W
    pit = snap(lact + AB)
    finger(c, "1/0.45", 0.0, 0.0)
    finger(c, "1/0.45", pit, 0.0)
    devl = [dev("SB", "b", "en_3v3_b", "vsso", "1/0.45"), dev("SABN", "vabn", "en_3v3_b", "vss", "1/0.45")]
    ybot, top = -0.52, snap(W + 0.52)
    # gates joined by a poly bar above the Activ, one contact over SB's gate -> en_3v3_b pad at the top edge
    pt = snap(W + R("poly_endcap"))
    cyc = snap(W + R("polycont_to_active") + R("cont") / 2)     # contact Cnt_e above the Activ end: poly stays inside the TGO
    gx0, gx1 = m.sd, pit + m.sd + m.L
    cx.box(c, "poly", gx0, snap(pt - 0.03), gx1, snap(cyc + R("cont") / 2 + R("cont_in_poly")))
    gc = snap((m.sd + m.sd + m.L) / 2)
    cx.box(c, "contact", snap(gc - R("cont") / 2), snap(cyc - R("cont") / 2), snap(gc + R("cont") / 2), snap(cyc + R("cont") / 2))
    padx0, padx1 = snap(gc - TW / 2), snap(gc + TW / 2)
    m1(c, padx0, snap(cyc - R("cont") / 2 - CE), padx1, top)
    pin1(c, "en_3v3_b", padx0, snap(top - 0.32), padx1, top)
    # SB: S (vsso) and D (b) stripes down to pads at the bottom edge
    for n, xx in (("vsso", sc0), ("b", sc1)):
        m1(c, xx - HW, ybot, xx + HW, 0.0)
        m1(c, xx - TW / 2, ybot, xx + TW / 2, snap(ybot + 0.32))
        pin1(c, n, xx - TW / 2, ybot, xx + TW / 2, snap(ybot + 0.32))
    # SABN: S (vss) and D (vabn) stripes up to pads at the top edge
    for n, xx in (("vss", pit + sc0), ("vabn", pit + sc1)):
        m1(c, xx - HW, 0.0, xx + HW, top)
        m1(c, xx - TW / 2, snap(top - 0.32), xx + TW / 2, top)
        pin1(c, n, xx - TW / 2, snap(top - 0.32), xx + TW / 2, top)
    # p tie strip right of SABN; it joins vss under the Activ (below the D stripe's end: M1_b)
    tx0 = snap(pit + lact + AB)
    tm = vtie(c, tx0, 0.0, W)
    yh = snap(-M1B - PH)
    m1(c, pit + sc0 - HW, snap(yh - 0.0), tm[2], snap(yh + PH))
    m1(c, pit + sc0 - HW, yh, pit + sc0 + HW, top)
    m1(c, tm[0], yh, tm[2], tm[3])
    cx.text(c, "note", "SB", lact / 2, W / 2)
    cx.text(c, "note", "SABN", pit + lact / 2, W / 2)
    tgo(c)
    bb, wh = normalise(c)
    return c, dict(size=wh, bb=bb, pit=pit, top=top), devl


def rotated_copy(src, name):
    """flat copy of src rotated R90 (left -> bottom, bottom -> right), bbox at (0, 0): the native orientation"""
    c = ly.create_cell(name)
    c.insert(db.DCellInstArray(src.cell_index(), db.DTrans(db.DTrans.R90)))
    c.flatten(False)
    bb = c.dbbox()
    c.transform(db.DTrans(snap(-bb.left), snap(-bb.bottom)))
    return c


if __name__ == "__main__":
    cxn = casc("d2s_casc_n_c")
    casc_c, ci, casc_dev = cxn
    # sinks x pin: from the left edge of sinks = casc x pin + (casc x0 - sinks x0)
    sk, si, sk_dev = sinks("sinks_6x6_c", ci["x_pin"] + CASC_X - SINKS_X, rep=int(os.environ.get("SINK_REP", "1")))
    s2d = rotated_copy(sk, "sinks_6x6_s2d_c")
    ab_c, ai, ab_dev = ab("d2s_ab_n_c")
    pd_c, pi_, pd_dev = pd("d2s_pd_n_c")
    opt = db.SaveLayoutOptions()
    opt.gds2_write_timestamps = False
    opt.write_context_info = False
    ly.write(os.path.join(OUT, "d2s_n_cells.gds"), opt)
    hdr = ("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
           "* d2s_n_cells.cdl: reference netlists of d2s_n_cells.gds, devices as drawn (one line per finger,\n"
           "* dummies included), written by build_d2s_n.py 2026-10-31 (agent N). Bulk = vss (the p tie of the cell).\n\n")
    sk_ports = ["vbn", "vss", "x", "y"]
    g.write_cdl(os.path.join(OUT, "d2s_n_cells.cdl"),
                [("sinks_6x6_c", sk_ports, sk_dev), ("sinks_6x6_s2d_c", sk_ports, sk_dev),
                 ("d2s_casc_n_c", ["b", "l1", "vbnc", "vss", "x", "y"], casc_dev),
                 ("d2s_ab_n_c", ["a", "b", "dabn", "l1", "l2", "vabn", "vss"], ab_dev),
                 ("d2s_pd_n_c", ["b", "en_3v3_b", "vabn", "vss", "vsso"], pd_dev)], hdr)
    print("sinks", si["size"], "casc", ci["size"], "ab", ai["size"], "pd", pi_["size"])
    print("sinks info", {k: v for k, v in si.items() if k != "bb"})
    print("casc info", {k: v for k, v in ci.items() if k != "bb"})
