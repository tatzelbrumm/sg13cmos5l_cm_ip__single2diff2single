# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_efs.py: layout of ls_up_fs (fail-safe 1.2 -> 3.3 V level shifter) and en_ctrl_3v3 v2 (three ls_up_fs),
IHP sg13cmos5l, hv devices. C4, Claude, agent E, 2026-11-08.

    python3 build_efs.py <out dir> [--no-png]       (PDK_ROOT, default /foss/pdks; lib/ next to this file)

Reuse: agent D's bdp_cells.py (inv_hv, strips, frame, gate_pad, cont_row) and C3's build_s2d_p3.py (box, fill,
pin, tap, mos, place), copied unchanged into lib/. Every new cell is prefixed efs_ (inv_hv -> efs_inv_hv).

ls_up_fs (cell frame, um; x = 0 is the left NWell / TGO edge, W = 9.44):
  row y 0 .. 4.90 = D's standard-cell row: p+ vss strip 0..0.30, NMOS 0.73..1.73, NWell from 2.55, PMOS
      3.17..4.17, N+ vddh strip 4.60..4.90; left to right efs_xn1 (XN1), XI1, XI2, XI3 (efs_inv_hv)
  leaker block above it, in the same NWell: 10 strips XPL10..XPL1 (pmosHV 0.3u/20u PCells, rotated: L along y),
      Activ 0.25 apart (Gat.b1), one merged gate plate on `in`, contacted by a poly tab as long as the gate on
      the left (0.60 beyond the Activ); serpentine by M1 jumpers at alternating ends (vddh enters at strip 0
      bottom from the vddh strip, x leaves at strip 9 bottom); XPF (0.3u/5u, rotated) right of strip 9, drain
      joined to x at the bottom, source to the right tie column at its top, gate tab (net y) on its right
  N+ tie ring around the leaker block: row vddh strip (bottom), columns at both sides, vddh rail on top
  M2: in (drop from the leaker tab to XN1's gate line), x (riser from XN1's drain, track under the leaker,
      onto the strip-9/XPF jumper), y (riser from XI1's drain, track over the vddh strip, rise to XPF's tab),
      out_b (Metal2 over XI3, Via1 down to a Metal1 line to the right edge)
Pins: in M1 left edge, out / out_b M1 right edge, vddh M1 top rail, vss M1 bottom strip.
Rule values: sg13cmos5l_tech_default.json (keys in comments) and the rule texts of sg13cmos5l_maximal.drc.
"""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("BDP_P_DIR", os.path.join(HERE, "lib"))
sys.path.insert(0, os.path.join(HERE, "lib"))
import bdp_cells as B        # noqa: E402  D's cell code, unchanged copy
import pya                   # noqa: E402

P, ly, box, pin, fill = B.P, B.ly, B.box, B.pin, B.fill
g5 = P.g5
YN, YP, TS, TD, L1, L2, LINE, VP = B.YN, B.YP, B.TS, B.TD, B.L1, B.L2, B.LINE, B.VP

# ---------------------------------------------------------------- geometry of ls_up_fs
NWL = 0.62                   # NW.e1: NWell enclosure of an NWell tie inside TGO
TL = (NWL, NWL + 0.30)       # left tie column (Activ 0.30 = Cnt.a + 2 Cnt.c)
S0 = TL[1] + 0.82            # strip 0 Activ left: the tab poly keeps 0.32 >= 0.30 beyond both 0.25 endcap zones
                             # (strip 0 and the tie column; sym_check N), Gat.d 0.07, M1.b 0.18
SP = 0.55                    # strip pitch: Activ 0.30 + 0.25 (Gat.b1; end caps merge into one plate)
NS = 10
XPF_X = S0 + (NS - 1) * SP + 0.30 + 0.65   # XPF Activ left: poly gap 0.29 >= Gat.b1 0.25
TR = (XPF_X + 0.30 + 0.82, XPF_X + 0.30 + 1.12)   # right tie column (same 0.82 as on the left)
W = g5(TR[1] + NWL)
YB = 5.20                    # leaker Activ bottom: pSD (0.18 beyond) 0.03 (pSD.d1) above the vddh strip
LA, LF = 20.68, 5.68         # Activ length of the rotated 0.3/20 and 0.3/5 PCells
YT = YB + LA
RAIL = (g5(YT + 0.22), g5(YT + 0.52))   # top vddh rail: pSD.d1 0.03 above the strips' pSD (0.18)
NWT = g5(RAIL[1] + NWL)
J = (0.02, 0.28)             # jumper M1 band relative to the Activ end (contact 0.07..0.23)
XN = 0.90                    # XN1 origin (its drain riser 0.23 >= Mn.b 0.21 from the in drop)
XI = [2.30, 3.70, 5.10]      # XI1..XI3 origins: Act.b 0.21 / M1.b 0.18 to the neighbour (pitch 1.40)
IN_X = S0 - 0.38             # in tab M1 column center
XO = XPF_X + 0.76            # out_b Via1 down to Metal1 (right of the y rise, Mn.b)
CDLS = {}


def via(c, xc, yc):
    box(c, "Via1", xc - 0.095, yc - 0.095, xc + 0.095, yc + 0.095)


def m2v(c, xc, y0, y1, hw=0.145):
    box(c, "M2", xc - hw, y0, xc + hw, y1)


def gate_tab(c, act_x, y0, y1, side, m1=None):
    """poly tab as long as the gate (no neck) 0.60 beyond the Activ edge act_x, contacts 0.30..0.46 from it
    (Cnt.e 0.14), Metal1 0.25..0.51 (0.26 wide, Via1-ready); m1 = (y0, y1) of the contacted part"""
    s = 1 if side > 0 else -1
    box(c, "GatPoly", act_x, y0, act_x + s * 0.60, y1)
    m0, m1_ = m1 or (y0 + 0.02, y1 - 0.02)
    fill(c, "Cont", act_x + s * 0.30, m0 + 0.05, act_x + s * 0.46, m1_ - 0.05)
    box(c, "M1", act_x + s * 0.25, m0, act_x + s * 0.51, m1_)


def rot(c, key, xl, yb, label=None):
    """rotated pmosHV (R90: L along y): Activ x [xl, xl+w], y from yb"""
    w = key[0]
    return P.place(c, key, pya.DTrans(pya.DTrans.R90, pya.DVector(xl + w, yb)), label)


def xn1():
    """XN1: nmosHV 1u/0.45u in a row cell (D's single() pattern): gate pad at L2 Via1-ready, source down into the
    vss strip, drain stripe up to a Via1 pad under the vddh strip (VP)"""
    c = ly.create_cell("efs_xn1")
    P.place(c, B.nmos(1, 0.45), pya.DTrans(pya.DVector(0, YN)), "XN1")
    box(c, "GatPoly", 0.34, YN + 1.18, 0.79, B.PN)
    B.gate_pad(c, 0.565, L2, viapad=True)
    box(c, "M1", 0.07, TS[1], 0.23, YN)
    box(c, "M1", 0.90, YN + 1.0, 1.06, VP[1])
    box(c, "M1", 0.875, VP[0], 1.085, VP[1])
    via(c, 0.98, (VP[0] + VP[1]) / 2)
    B.frame(c, -0.125, 1.235)
    return c


def ls_core(inv, xn):
    c = ly.create_cell("efs_ls_core")     # the whole level shifter, no labels (placed by both top cells)
    # ---- row
    c.insert(pya.DCellInstArray(xn.cell_index(), pya.DTrans(pya.DVector(XN, 0))))
    for x in XI:
        c.insert(pya.DCellInstArray(inv.cell_index(), pya.DTrans(pya.DVector(x, 0))))
    bnd = [(XN - 0.125, XN + 1.235)] + [(x + 0.15, x + 1.255) for x in XI]
    # vss strip (p+, full width less TGO.a) and vddh strip (N+, NW.e1 inside the NWell); contacts in the gaps
    for (y0, y1), lo, hi, p in ((TS, 0.30, W - 0.30, True), (TD, NWL, W - NWL, False)):
        box(c, "Activ", lo, y0, hi, y1)
        box(c, "M1", lo, y0, hi, y1)
        if p:
            box(c, "pSD", lo - 0.03, y0 - 0.03, hi + 0.03, y1 + 0.03)
        edges = [lo] + [e for b in bnd for e in b] + [hi]
        for a, b in zip(edges[0::2], edges[1::2]):
            if b - a - 0.18 >= 0.16:
                B.cont_row(c, a + 0.09, b - 0.09, y0 + 0.07)
    # ---- leaker block: 10 strips, serpentine
    key = P.mos(0.3, 20)
    xs = [g5(S0 + i * SP) for i in range(NS)]
    for i, x in enumerate(xs):
        rot(c, key, x, YB, "PL%d" % (NS - i))
    gate_tab(c, S0, YB + 0.34, YB + LA - 0.34, -1)                        # in: poly tab on the left
    box(c, "M1", xs[0], TD[1], xs[0] + 0.30, YB + J[1])                  # strip 0 bottom = vddh
    for i in range(1, NS - 1, 2):                                       # bottom jumpers (1,2) (3,4) ...
        box(c, "M1", xs[i], YB + J[0], xs[i + 1] + 0.30, YB + J[1])
    for i in range(0, NS, 2):                                           # top jumpers (0,1) (2,3) ...
        box(c, "M1", xs[i], YT - J[1], xs[i + 1] + 0.30, YT - J[0])
    # XPF: rotated 0.3/5, drain (bottom) = x, source (top) = vddh to the right column, gate tab y on the right
    rot(c, P.mos(0.3, 5), XPF_X, YB, "PF")
    gate_tab(c, XPF_X + 0.30, YB + 0.34, YB + LF - 0.34, 1, m1=(YB + 0.36, YB + 1.60))
    box(c, "M1", xs[-1], YB + J[0], XPF_X + 0.30, YB + J[1])             # x: strip 9 bottom + XPF drain
    box(c, "M1", XPF_X, YB + LF - J[1], TR[1], YB + LF - J[0])           # XPF source -> right column
    # ---- tie ring: columns and top rail (row vddh strip = bottom side)
    for x0, x1 in (TL, TR):
        P.tap(c, x0, TD[0], x1, RAIL[1], (x0 + 0.07, TD[1] + 0.15, x1 - 0.07, RAIL[0] - 0.15))
    P.tap(c, TL[0], RAIL[0], TR[1], RAIL[1], (TL[0] + 0.07, RAIL[0] + 0.07, TR[1] - 0.07, RAIL[1] - 0.07))
    box(c, "NWell", 0, 2.55, W, NWT)
    box(c, "TGO", 0, -0.27, W, NWT)
    # ---- routing
    xg = XN + 0.565                                                     # in: XN1 gate pad line to the left edge
    box(c, "M1", 0, L2 - 0.07, xg, L2 + 0.28)
    via(c, IN_X, L2 + 0.105)
    m2v(c, IN_X, L2 - 0.07, YB + 0.67)
    via(c, IN_X, YB + 0.52)                                             # onto the in tab
    xd = XN + 0.98                                                      # x: XN1 drain -> XI1 gate at L1
    box(c, "M1", XN + 0.90, LINE[0], XI[0] + 0.565, LINE[1])
    m2v(c, xd, VP[0], YB + J[1])
    box(c, "M2", xd - 0.145, YB + J[0], XPF_X - 0.18, YB + J[1])        # track under the leaker
    via(c, XPF_X - 0.325, YB + 0.15)                                    # onto the strip-9 / XPF jumper
    yd = XI[0] + 0.98                                                   # y: XI1 drain -> XI2 gate, riser
    box(c, "M1", XI[0] + 0.90, LINE[0], XI[1] + 0.565, LINE[1])
    box(c, "M1", yd - 0.105, VP[0], yd + 0.105, VP[1])
    via(c, yd, (VP[0] + VP[1]) / 2)
    m2v(c, yd, VP[0], 4.88)
    yx = XPF_X + 0.30 + 0.38                                            # XPF tab column center
    box(c, "M2", yd - 0.145, 4.62, yx + 0.145, 4.88)
    m2v(c, yx, 4.62, YB + 0.67)
    via(c, yx, YB + 0.52)
    box(c, "M1", XI[1] + 0.90, LINE[0], XI[2] + 0.565, LINE[1])         # out_b: XI2 drain -> XI3 gate
    via(c, XI[1] + 1.35, (LINE[0] + LINE[1]) / 2)
    box(c, "M2", XI[1] + 1.205, LINE[0], XO + 0.145, LINE[1])           # over XI3's drain stripe, then Via1
    box(c, "M1", XO - 0.145, LINE[0], W, LINE[1])                       # down to Metal1 to the right edge (the
    via(c, XO, (LINE[0] + LINE[1]) / 2)                                 # edge column stays free of Metal2)
    box(c, "M1", XI[2] + 0.90, L2 - 0.07, W, L2 + 0.19)                 # out: XI3 drain to the right edge
    c.geo = {"xs": xs, "yx": yx, "xd": xd, "yd": yd}
    return c




def ls_up_fs(core):
    """top cell ls_up_fs = efs_ls_core + its pin labels (en_ctrl_3v3 places the core, so that the flat LVS of
    en_ctrl_3v3 sees only its own labels)"""
    c = ly.create_cell("ls_up_fs")
    c.insert(pya.DCellInstArray(core.cell_index(), pya.DTrans()))
    pin(c, "M1", "in", 0, L2 - 0.07, 0.50, L2 + 0.28)
    pin(c, "M1", "out", W - 0.50, L2 - 0.07, W, L2 + 0.19)
    pin(c, "M1", "out_b", W - 0.50, LINE[0], W, LINE[1])
    pin(c, "M1", "vddh", W / 2 - 1.0, RAIL[0], W / 2 + 1.0, RAIL[1])
    pin(c, "M1", "vss", W / 2 - 1.0, TS[0], W / 2 + 1.0, TS[1])
    return c


# ---------------------------------------------------------------- en_ctrl_3v3: three stacked, rails shared
def en_ctrl(ls):
    c = ly.create_cell("en_ctrl_3v3")
    rc = (RAIL[0] + RAIL[1]) / 2
    ya, yb_, yc = 0.0, 2 * rc, 2 * rc - TS[1]          # XE normal; XS0 mirrored (shares XE's rail); XS1 normal
    ts = [pya.DTrans(pya.DVector(0, ya)), pya.DTrans(pya.DTrans.M0, pya.DVector(0, yb_)),
          pya.DTrans(pya.DVector(0, yc))]
    for t in ts:
        c.insert(pya.DCellInstArray(ls.cell_index(), t))
    nets = [("en_1v2", "en_3v3", "en_3v3_b"), ("sel0_1v2", "sel0_3v3", None), ("sel1_1v2", "sel1_3v3", None)]
    for t, (ni, no, nb) in zip(ts, nets):
        for net, m, x0, y0, x1, y1 in (
                (ni, "M1", 0, L2 - 0.07, 0.50, L2 + 0.28), (no, "M1", W - 0.50, L2 - 0.07, W, L2 + 0.19),
                (nb, "M1", W - 0.50, LINE[0], W, LINE[1])):
            if net:
                b = t * pya.DBox(x0, y0, x1, y1)
                pin(c, m, net, b.left, b.bottom, b.right, b.top)
    for t, (y0, y1), net in ((ts[0], TS, "vss"), (ts[0], RAIL, "vddh"), (ts[2], TS, "vss"), (ts[2], RAIL, "vddh")):
        b = t * pya.DBox(W / 2 - 1.0, y0, W / 2 + 1.0, y1)
        pin(c, "M1", net, b.left, b.bottom, b.right, b.top)
    # vddh strap: XS1's rails are vss (shared with XS0) and its own vddh rail on top, so its vddh is joined to the
    # XE / XS0 rail by a Metal2 strap over the left tie columns (x 0.67..0.96: Mn.b 0.255 to the in drops), Via1 on
    # every vddh rail / strip it crosses
    xs = TL[0] + 0.195
    ys = [rc, yb_ - (TD[0] + TD[1]) / 2, yc + (TD[0] + TD[1]) / 2, yc + rc]
    box(c, "M2", xs - 0.145, ys[0] - 0.145, xs + 0.145, ys[-1] + 0.145)
    for y in ys:
        via(c, xs, y)
    # vss strap: XE's vss strip and the XS0 / XS1 strip are otherwise joined only through the substrate; Metal2
    # strap at the right edge (x 8.80..9.09: Mn.b >= 0.25 to the y rise and the out_b Metal2), Via1 on both strips
    xv = TR[0] + 0.185
    ys = [(TS[0] + TS[1]) / 2, yc + (TS[0] + TS[1]) / 2]
    box(c, "M2", xv - 0.145, ys[0] - 0.145, xv + 0.145, ys[-1] + 0.145)
    for y in ys:
        via(c, xv, y)
    # ports not connected inside (vddl, vdd1v2_sense, vdd3v3_sense): labelled Metal2 stubs on the left edge over
    # XE's leaker block, isolated (no Via1), 0.40 x 0.40, 0.60 apart
    for i, net in enumerate(("vddl", "vdd1v2_sense", "vdd3v3_sense")):
        y = 12.0 + i * 1.0
        box(c, "M2", 0, y, 0.40, y + 0.40)                  # Mn.d 0.144 um2
        pin(c, "M2", net, 0, y, 0.40, y + 0.40)
    return c


# ---------------------------------------------------------------- previews (D's render, unchanged in substance)
def render(c, fn, out, win=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon
    b = c.dbbox().enlarged(1.6, 0.4) if win is None else pya.DBox(*win)     # margin: edge pin names readable
    s = min(30.0 / b.width(), 24.0 / b.height())
    fig, ax = plt.subplots(figsize=(max(5.0, b.width() * s) + 1.5, max(4.0, b.height() * s) + 1.2))
    for lay, fc, a, ec in P.STYLE:
        ps = [Polygon([(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()])
              for p in pya.Region(c.begin_shapes_rec(P.LI[lay])).merged().each()]
        ax.add_collection(PatchCollection(ps, facecolor=fc, alpha=a, edgecolor=ec or fc, linewidth=0.7 if ec else 0))
    fs = 8
    it = c.begin_shapes_rec(P.LI["TEXT"])
    while not it.at_end():
        t = it.shape()
        if t.is_text() and t.text_string not in ("pmosHV", "nmosHV", "well"):
            p = it.dtrans() * pya.DPoint(t.dtext.trans.disp.x, t.dtext.trans.disp.y)
            ax.text(p.x, p.y, t.text_string, fontsize=6, color="#5a1a5a", weight="bold", ha="center",
                    va="center", clip_on=True, rotation=90 if t.text_string.startswith("PL") else 0)
        it.next()
    for lay, col in (("M1txt", "#0b3d91"), ("M2txt", "#3b2a70")):
        for t in c.shapes(P.LI[lay]).each():
            p = t.dtext.trans.disp
            ax.text(p.x, p.y, t.dtext.string, fontsize=fs, color=col, weight="bold", ha="center", va="center",
                    clip_on=True, bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    ax.set_xlim(b.left, b.right)
    ax.set_ylim(b.bottom, b.top)
    ax.set_aspect("equal")
    ax.set_xlabel("um")
    w = c.dbbox()
    ax.set_title("%s (%.2f x %.2f um)\nNWell green, TGO olive, pSD tan, Activ green, GatPoly red, Cont black,\n"
                 "Metal1 blue, Via1 red, Metal2 violet; pins labelled" % (c.name, w.width(), w.height()), fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(out, fn), dpi=120)
    plt.close(fig)


def write(cell, path):
    l2 = pya.Layout()
    l2.dbu = ly.dbu
    l2.create_cell(cell.name).copy_tree(cell)
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    l2.write(path, opt)


def main(out, png=True):
    os.makedirs(out, exist_ok=True)
    inv = B.inv_hv()
    B.strip_labels(inv)
    inv.name = "efs_inv_hv"
    xn = xn1()
    core = ls_core(inv, xn)
    ls = ls_up_fs(core)
    en = en_ctrl(core)
    for c in list(ly.each_cell()):
        if c.name.startswith(("pmosHV", "nmosHV")):
            c.name = "efs_" + c.name.replace("$", "_")
    write(ls, os.path.join(out, "ls_up_fs.gds"))
    write(en, os.path.join(out, "en_ctrl_3v3.gds"))
    for c in (ls, en):
        b = c.dbbox()
        print("%-12s bbox %s  %.2f x %.2f um = %.1f um2" % (c.name, b, b.width(), b.height(), b.width() * b.height()))
    print("cells:", sorted(c.name for c in ly.each_cell()))
    if png:
        render(ls, "ls_up_fs.png", out)
        render(en, "en_ctrl_3v3.png", out)
        render(ls, "ls_up_fs_row.png", out, (-1.2, -0.5, W + 1.2, 7.2))


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]), "--no-png" not in sys.argv)
