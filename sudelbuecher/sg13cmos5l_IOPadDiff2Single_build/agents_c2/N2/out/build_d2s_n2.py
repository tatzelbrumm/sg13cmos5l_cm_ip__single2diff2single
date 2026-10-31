# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""d2s_n2_cells: the NMOS layout primitives of the IOPadDiff2Single front end and bias tree, and the R block,
rebuilt after Christoph's rejection of 2026-10-31 18:55 (agent N2, C2 2026-10-31).

    cd out && python3 build_d2s_n2.py        ->  d2s_n2_cells.gds, d2s_n2_cells.cdl

Cells: sinks_6x6_c2, sinks_6x6_s2d_c2, d2s_casc_n_c2, d2s_ab_n_c2, d2s_pd_n_c2, bias_tree_n_c2, d2s_rhigh_c2.

Rules of the rebuild (BRIEF.md): device layers mirror-symmetric about every row's centre line and, in two-row
blocks, about the line between the rows; the same dummy at both ends of every row; gate contacts in columns on
poly as tall as the gate (no necks); unmodified SG13_dev PCells; taps only at the periphery.

How a row is built:
  - every MOS is one SG13_dev nmosHV finger (ng=1), turned R270 so W runs along the row and L across it; fingers
    0.25 apart (Gat.b1), so their poly endcaps merge into one gate strip per row. Devices right of the cell's
    vertical axis are placed mirrored (M90 about their own centre): the PCell's contact column is not exactly
    symmetric along W (0.005 um grid steps), so mirrored placement makes the row an exact mirror image;
  - gate contact columns: at both row ends (and, where the map needs gate access inside the row, in a 0.85 um
    gap on both sides of the centre device), contacts on a poly fill as tall as the gate, M1 column 0.26 um
    (Via1 fits), the columns of both rows joined in M1 straight through the band;
  - inner stripes (the band between the rows) carry the drains: 1.11 um M1 tabs with 3 Via1 onto M2 tracks
    in the band (lower row tabs 0.75 left of the finger centre, upper row 0.75 right, so near and far tabs never
    meet); outer stripes: sources, M1 plates into the p+ tie strip at the block's top and bottom edge;
  - dummies have D = S = G (on the gate net): both stripes bridged in M1 to the adjacent gate column. Vgs = 0, no
    channel, no metal over any channel.
Rule values (sg13cmos5l_tech_default.json): Act_b 0.21, Gat_b1 0.25, Gat_c 0.18, Gat_d 0.07, Cnt_a 0.16, Cnt_b
0.18, Cnt_c 0.07, Cnt_d 0.07, Cnt_e 0.14, M1_b 0.18, M1_c1 0.05, M1_d 0.09, M1_e 0.22 (> 0.3 wide, run > 1 um),
V1_a 0.19, V1_b 0.22, V1_c 0.01, V1_c1 0.05, Mn_b 0.21, pSD_c1 0.03, pSD_d 0.18, pSD_j1 0.40, TGO_a 0.27,
EXTB_c 0.31, LU_b 20.
"""
import os
import sys

pdk = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "ihp-sg13cmos5l"))
sys.path += [pdk + "/libs.tech/klayout/python", pdk + "/libs.tech/klayout/python/pycell4klayout-api/source/python"]
import pya                              # noqa: E402
import sg13cmos5l_pycell_lib            # noqa: E402,F401  (registers the PCell library SG13_dev)

ly = pya.Layout()
ly.dbu = 0.001
ly.technology_name = "sg13cmos5l"
LAY = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25),
       "Via1": (19, 0), "M2": (10, 0), "M2pin": (10, 2), "M2txt": (10, 25), "pSD": (14, 0), "TGO": (44, 0),
       "TEXT": (63, 0)}
LI = {k: ly.layer(*v) for k, v in LAY.items()}
NM = 1000


def g5(v):
    return round(round(v / 0.005) * 0.005, 4)


GAP, MID = 0.25, 0.85        # finger gap (Gat.b1); gap holding a gate column (sym_check: poly piece >= 0.30)
TAB, VOFF = 1.11, 0.75       # drain tab: 3 x V1_a 0.19 + 2 x V1_b 0.22 + 2 x V1_c1 0.05; offset from finger centre
TP = 0.50                    # M2 track pitch: 0.29 + Mn_b 0.21
TM = 0.295                   # band edge to first track centre: far tab end 0.145 + M1_e 0.22 - stripe inset 0.07
TIEW = 0.30                  # tie Activ: Cnt_a 0.16 + 2 x Cnt_c 0.07


class Cell:
    def __init__(self, name):
        self.name, self.c = name, ly.create_cell(name)
        self.cdl, self.pins, self.ties = [], [], []

    def box(self, lay, x0, y0, x1, y1):
        self.c.shapes(LI[lay]).insert(pya.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))

    def pin(self, metal, net, x0, y0, x1, y1):
        self.box(metal + "pin", x0, y0, x1, y1)
        self.c.shapes(LI[metal + "txt"]).insert(pya.DText(net, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))
        self.pins.append((net, metal, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))

    def note(self, text, x, y):
        self.c.shapes(LI["TEXT"]).insert(pya.DText(text, g5(x), g5(y)))

    def via(self, x, y):
        self.box("Via1", x - 0.095, y - 0.095, x + 0.095, y + 0.095)

    def cont(self, x, y):                        # x, y: lower left corner
        self.box("Cont", x, y, x + 0.16, y + 0.16)

    def mos(self, label, w, l, x0, yb, d, g, s, mx=False):
        """one nmosHV finger, W along x: Activ [x0, x0+w] x [yb, yb+l+0.68]; stripes 0.07 .. 0.23 inside
        the bottom / top Activ edge. mx: mirrored about its own centre line (devices right of the axis)."""
        dev = pya.Layout.create_cell(ly, "nmosHV", "SG13_dev", {"w": "%gu" % w, "l": "%gu" % l, "ng": "1"})
        h = l + 0.68
        t = pya.DTrans(pya.DTrans.R270, pya.DVector(0, h))
        if mx:
            t = pya.DTrans(pya.DTrans.M90, pya.DVector(w, 0)) * t
        self.c.insert(pya.DCellInstArray(dev.cell_index(), pya.DTrans(pya.DVector(g5(x0), g5(yb))) * t))
        self.cdl.append("M%s_%d %s %s %s vss sg13_hv_nmos w=%gu l=%gu ng=1 m=1" % (label, len(self.cdl), d, g, s, w, l))
        self.note(label, x0 + w / 2, yb + h / 2)
        return dict(x0=x0, x1=x0 + w, yb=yb, yt=yb + h, w=w, l=l, bot=(yb + 0.07, yb + 0.23),
                    top=(yb + h - 0.23, yb + h - 0.07), gate=(yb + 0.34, yb + 0.34 + l), xc=x0 + w / 2)

    def tie(self, x0, y0, x1, y1):
        """p+ substrate tie (vss): Activ, pSD 0.03 around (pSD_c1), one centred contact row along the long
        side, M1 over the contacts (M1_c 0 across, M1_c1 0.05 at the ends)."""
        self.box("Activ", x0, y0, x1, y1)
        self.box("pSD", x0 - 0.03, y0 - 0.03, x1 + 0.03, y1 + 0.03)
        horiz = (x1 - x0) > (y1 - y0)
        a, b = (x0, x1) if horiz else (y0, y1)
        pos = centred(a + 0.07, b - 0.07)
        q = ((y0 + y1) / 2 if horiz else (x0 + x1) / 2) - 0.08
        for p in pos:
            self.cont(p, q) if horiz else self.cont(q, p)
        m = (pos[0] - 0.05, pos[-1] + 0.21)
        if horiz:
            self.box("M1", m[0], q, m[1], q + 0.16)
        else:
            self.box("M1", q, m[0], q + 0.16, m[1])
        self.ties.append((x0, y0, x1, y1))
        return (m[0], q, m[1], q + 0.16) if horiz else (q, m[0], q + 0.16, m[1])

    def gate_col(self, xc, granges, y0, y1, fill):
        """gate contact column at x centre xc: contacts on a poly fill (x range 'fill') as tall as each gate
        range, M1 0.26 wide from y0 to y1."""
        for g0, g1 in granges:
            self.box("GatPoly", fill[0], g0, fill[1], g1)
            for p in centred(g0 + 0.07, g1 - 0.07):
                self.cont(xc - 0.08, p)
        self.box("M1", xc - 0.13, y0, xc + 0.13, y1)

    def bridge(self, dev, side, xc):
        """M1 from a stripe ('bot' / 'top') of dev to the gate column at xc (dummies, diodes)."""
        s0, s1 = dev[side]
        xe = dev["x0"] + 0.1 if xc < dev["x0"] else dev["x1"] - 0.1
        self.box("M1", xc, s0, xe, s1)

    def tab(self, xc, ya, yb, yv, w=TAB):
        """M1 tab from ya to yb, centred on xc, Via1s at yv (3 on 1.11, 1 on 0.29)."""
        self.box("M1", xc - w / 2, ya, xc + w / 2, yb)
        for k in ((-0.41, 0, 0.41) if w >= TAB else (0,)):
            self.via(xc + k, yv)

    def track(self, x0, x1, y):
        self.box("M2", x0, y - 0.145, x1, y + 0.145)

    def tgo(self):
        """one ThickGateOx rectangle: every Activ (devices and ties) + 0.27 (TGO_a)."""
        r = pya.Region(self.c.begin_shapes_rec(LI["Activ"])).bbox().to_dtype(ly.dbu)
        self.box("TGO", r.left - 0.27, r.bottom - 0.27, r.right + 0.27, r.top + 0.27)


def centred(a, b, size=0.16, pitch=0.34):
    """lower edges of contacts filling [a, b], centred on a 0.005 grid (so mirror images coincide)."""
    n = int((b - a - size) / pitch + 1e-6) + 1
    while n > 0:
        rest = round((b - a - size - (n - 1) * pitch) * NM)
        if rest >= 0 and rest % 10 == 0:
            return [g5(a + rest / NM / 2 + k * pitch) for k in range(n)]
        n -= 1
    raise ValueError((a, b))


def place_row(cell, seq, yb, axis):
    """seq: device tuples (label, w, l, d, g, s) and 'C' (a gate column between two devices). Fingers from x = 0;
    those right of 'axis' mirrored. Returns the devices and the x ranges of the C gaps."""
    x, devs, gaps = 0.0, [], []
    for k, it in enumerate(seq):
        if it == "C":
            gaps.append((x - GAP, x - GAP + MID))
            x += MID - GAP
            continue
        lab, w, l, d, g, s = it
        if lab == "slot":                                # space reserved for a device placed by the caller
            x = g5(x + w + GAP)
            continue
        devs.append(cell.mos(lab, w, l, x, yb, d, g, s, mx=(x + w / 2 > axis + 1e-6)))
        x = g5(x + w + GAP)
    return devs, gaps


def row_len(seq):
    return g5(sum(it[1] for it in seq if it != "C") + GAP * (len([i for i in seq if i != "C"]) - 1)
              + (MID - GAP) * seq.count("C"))


# ======================================================================================================
# Two-row blocks: sinks_6x6, d2s_casc_n. Row 1 (bottom) and row 2 (top) mirror images about the band.
# ======================================================================================================
def two_rows(cell, r1, r2, band, gcols_mid=True):
    """places both rows, end and mid gate columns, band tracks; returns geometry."""
    X = row_len(r1)
    assert X == row_len(r2)
    ax = X / 2
    H = r1[0][2] + 0.68
    A = H
    tr = {n: g5(A + TM + TP * k) for k, n in enumerate(band)}
    B = g5(A + 2 * TM + TP * (len(band) - 1))
    d1, gp1 = place_row(cell, r1, 0.0, ax)
    d2, gp2 = place_row(cell, r2, B, ax)
    top = B + H
    gr = [d1[0]["gate"], d2[0]["gate"]]
    cols = [(-0.33, (-0.60, -0.10)), (X + 0.33, (X + 0.10, X + 0.60))]
    if gcols_mid:
        cols += [((a + b) / 2, (a + 0.10, b - 0.10)) for a, b in gp1]
    for xc, fill in cols:
        cell.gate_col(xc, gr, 0.07, top - 0.07, fill)
    return dict(X=X, H=H, A=A, B=B, top=top, tr=tr, d1=d1, d2=d2, cols=[c[0] for c in cols], gaps=gp1)


def drains(cell, g, dev, row, net):
    """inner stripe of dev to band track 'net': row 1 tab up, row 2 tab down."""
    t = g["tr"][net]
    if row == 1:
        cell.tab(dev["xc"] - VOFF, dev["top"][0], t + 0.145, t)
    else:
        cell.tab(dev["xc"] + VOFF, t - 0.145, dev["bot"][1], t)


def nearest_col(g, dev):
    return min(g["cols"], key=lambda c: abs(c - dev["xc"]))


def sinks(name, nf=6):
    """SX / SY nf + nf fingers 6/6 on vbn, rows X Y Y X X Y / Y X X Y Y X (layout_primitives.md section 5),
    BN (diode) in the middle of row 1, its twin (dummy 6/6) in the middle of row 2, a narrow 2/6 dummy at both
    ends of both rows. Band tracks x, vbn, y; sources to the tie strips (one vss net, pin on the bottom tie)."""
    assert nf % 2 == 0
    c = Cell(name)
    half = ("XYYX" * nf)[:nf // 2]
    sw = {"X": "Y", "Y": "X"}
    right = "".join(sw[ch] for ch in half[::-1])
    m1 = list(half) + ["BN"] + list(right)
    m2 = [sw[ch] if ch in sw else "T" for ch in m1]
    f = {"X": ("SX", 6, 6, "x", "vbn", "vss"), "Y": ("SY", 6, 6, "y", "vbn", "vss"),
         "BN": ("BN", 6, 6, "vbn", "vbn", "vss"), "T": ("BNtwin", 6, 6, "vbn", "vbn", "vbn")}
    dn = ("dummy", 2, 6, "vbn", "vbn", "vbn")
    seq = lambda m: [dn] + [f[k] for k in m[:nf // 2]] + ["C", f[m[nf // 2]], "C"] + [f[k] for k in m[nf // 2 + 1:]] + [dn]
    g = two_rows(c, seq(m1), seq(m2), ["x", "vbn", "y"])
    X, A, B, top, tr = g["X"], g["A"], g["B"], g["top"], g["tr"]
    # ties at the bottom and top edge (Act_b 0.21 from the rows), joined by M1 joiners outside the end columns
    xl, xr = -0.97, X + 0.97
    tb = c.tie(xl, -0.21 - TIEW, xr, -0.21)
    tt = c.tie(xl, top + 0.21, xr, top + 0.21 + TIEW)
    for x0 in (xl, X + 0.68):
        c.box("M1", x0, tb[1], x0 + 0.29, tt[3])
    for row, devs in ((1, g["d1"]), (2, g["d2"])):
        for dv, it in zip(devs, [i for i in seq(m1 if row == 1 else m2) if i != "C"]):
            lab, w, l, d, gn, s = it
            inner, outer = ("top", "bot") if row == 1 else ("bot", "top")
            if s == "vss":                               # source plate into the tie
                c.box("M1", dv["x0"], tb[1], dv["x1"], dv["bot"][1]) if row == 1 else \
                    c.box("M1", dv["x0"], dv["top"][0], dv["x1"], tt[3])
            else:
                c.bridge(dv, outer, nearest_col(g, dv))
            if d in ("x", "y"):
                drains(c, g, dv, row, d)
            else:
                c.bridge(dv, inner, nearest_col(g, dv))
    for n, t in tr.items():
        c.track(xl, X + 0.33 + 0.145, t)
        c.pin("M2", n, xl, t - 0.145, xl + 0.5, t + 0.145)
    for xc in g["cols"]:
        c.via(xc, tr["vbn"])
    c.pin("M1", "vss", tb[0], tb[1], tb[0] + 0.5, tb[3])
    c.tgo()
    c.info = "rows: D | %s | D  /  D | %s | D" % (" ".join(m1), " ".join(m2))
    return c


def casc_n(name):
    """CX (x -> l1) / CY (y -> b) 2 x 15/3 each, cross-quad CX CY / CY CX; BNC (1/8, diode) turned like the
    rows, alone in the middle of the map (on both symmetry axes); narrow 2/3 dummies at both ends of both rows.
    Band tracks l1, vbnc, b (drains); sources below row 1 / above row 2 on two M2 levels each, x and y joined
    by M1 verticals at the left (x) and right (y) end; ties at the top and bottom edge."""
    c = Cell(name)
    cx = ("CX", 15, 3, "l1", "vbnc", "x")
    cy = ("CY", 15, 3, "b", "vbnc", "y")
    dn = ("dummy", 2, 3, "vbnc", "vbnc", "vbnc")
    slot = ("slot", 1, 3, None, None, None)              # BNC's place in both rows, between two gate columns
    r1 = [dn, cx, "C", slot, "C", cy, dn]
    r2 = [dn, cy, "C", slot, "C", cx, dn]
    g = two_rows(c, r1, r2, ["l1", "vbnc", "b"])
    X, top, tr, d1, d2, colx = g["X"], g["top"], g["tr"], g["d1"], g["d2"], g["cols"]
    ax = X / 2
    bnc = c.mos("BNC", 1, 8, g["gaps"][0][1], g5((top - 8.68) / 2), "vbnc", "vbnc", "vss")
    # dummies: both stripes to their end column; BNC: drain (top) to the left middle column, source to the tie
    for dv in (d1[0], d1[-1], d2[0], d2[-1]):
        xc = nearest_col(g, dv)
        c.bridge(dv, "bot", xc)
        c.bridge(dv, "top", xc)
    c.bridge(bnc, "top", colx[2])
    for row, devs in ((1, d1), (2, d2)):
        for dv in devs[1:-1]:
            drains(c, g, dv, row, "l1" if dv["xc"] < ax and row == 1 or dv["xc"] > ax and row == 2 else "b")
    # source levels: near (x) and far (y) below row 1, mirrored above row 2
    lo = {"x": g5(-TM + 0.0), "y": g5(-TM - TP)}
    hi = {"x": g5(top + TM), "y": g5(top + TM + TP)}
    for row, devs in ((1, d1), (2, d2)):
        for dv in devs[1:-1]:
            n = "x" if dv["xc"] < ax and row == 1 or dv["xc"] > ax and row == 2 else "y"
            if row == 1:
                c.tab(dv["xc"] + VOFF, lo[n] - 0.145, dv["bot"][1], lo[n])
            else:
                c.tab(dv["xc"] - VOFF, dv["top"][0], hi[n] + 0.145, hi[n])
    yt0 = g5(lo["y"] - 0.145 - 0.22 - 0.07 - 0.16)     # tie M1 (contacts) 0.22 below the far level's tabs
    yt1 = g5(hi["y"] + 0.145 + 0.22 + 0.07 + 0.16)
    xvx, xvy = -0.97, X + 0.68                          # x vertical left, y vertical right (0.22 from the columns)
    xl, xr = -1.48, X + 1.48                            # vss joiners outside them
    tb = c.tie(xl, yt0 - 0.07, xr, yt0 - 0.07 + TIEW)
    tt = c.tie(xl, yt1 + 0.07 - TIEW, xr, yt1 + 0.07)
    for x0 in (xl, X + 1.19):
        c.box("M1", x0, tb[1], x0 + 0.29, tt[3])
    c.box("M1", bnc["xc"] - 0.3, tb[1], bnc["xc"] + 0.3, bnc["bot"][1])      # BNC source to the bottom tie
    for n, xv in (("x", xvx), ("y", xvy)):
        c.box("M1", xv, lo[n] - 0.145, xv + 0.29, hi[n] + 0.145)
        for y in (lo[n], hi[n]):
            c.via(xv + 0.145, y)
    # source tracks: from the tabs to the verticals; x pin at the left edge, y at the right edge
    for n, lv in (("x", lo), ("x", hi), ("y", lo), ("y", hi)):
        xs = [dv["xc"] + (VOFF if lv is lo else -VOFF) for row, devs in ((1, d1), (2, d2)) for dv in devs[1:-1]
              if (lv is lo) == (row == 1) and ("x" if dv["xc"] < ax and row == 1 or dv["xc"] > ax and row == 2 else "y") == n]
        a = min(xs + [xvx if n == "x" else xvy + 0.29]) - 0.555
        b = max(xs + [xvx if n == "x" else xvy + 0.29]) + 0.555
        if lv is lo:                                     # the bottom levels run on to the pin edge
            a, b = (xl, b) if n == "x" else (a, xr)
        c.track(max(a, xl), min(b, xr), lv[n])
    c.pin("M2", "x", xl, lo["x"] - 0.145, xl + 0.5, lo["x"] + 0.145)
    c.pin("M2", "y", xr - 0.5, lo["y"] - 0.145, xr, lo["y"] + 0.145)
    for n, t in tr.items():
        c.track(xl, X + 0.33 + 0.145, t)
        c.pin("M2", n, xl, t - 0.145, xl + 0.5, t + 0.145)
    for xc in colx:
        c.via(xc, tr["vbnc"])
    c.pin("M1", "vss", tb[0], tb[1], tb[0] + 0.5, tb[3])
    c.tgo()
    c.info = "rows: D | CX [BNC] CY | D  /  D | CY [BNC] CX | D  (BNC one device spanning both rows)"
    return c


# ======================================================================================================
# One-row cells: d2s_ab_n, d2s_pd_n, bias_tree_n. Ties as vertical strips at both ends (X-symmetric).
# ======================================================================================================
def one_row(c, seq, dummies_to_col=True):
    X = row_len(seq)
    devs, _ = place_row(c, seq, 0.0, X / 2)
    H = seq[0][2] + 0.68
    gr = [devs[0]["gate"]]
    yc0, yc1 = (0.07, H - 0.07) if dummies_to_col else (max(gr[0][0] + 0.05, 0.39), min(gr[0][1] - 0.05, H - 0.39))
    if yc1 - yc0 < 0.35:                                # M1_d: 0.26 x 0.35 >= 0.09 um2
        m = (yc0 + yc1) / 2
        yc0, yc1 = m - 0.175, m + 0.175
    for xc, fill in ((-0.33, (-0.60, -0.10)), (X + 0.33, (X + 0.10, X + 0.60))):
        c.gate_col(xc, gr, yc0, yc1, fill)
    return X, H, devs


def bottom_pins(c, X, devs_nets, plate_net="vss"):
    """sources: a tie strip under the row (0.645 below it), source tabs with Via1 at y -0.35 and M2 straight
    down over the tie to the bottom edge (M2 pins); devices whose source is vss get an M1 plate into the tie."""
    tb = c.tie(-0.97, -0.945, X + 0.97, -0.645)
    for dv, s in devs_nets:
        w = min(TAB, dv["w"] - 0.4) if dv["w"] >= 1.5 else 0.29
        if s == plate_net:
            c.box("M1", dv["x0"], tb[1], dv["x1"], dv["bot"][1])
            continue
        c.tab(dv["xc"], -0.495, dv["bot"][1], -0.35, w)
        c.box("M2", dv["xc"] - w / 2, -1.0, dv["xc"] + w / 2, -0.205)
        c.pin("M2", s, dv["xc"] - w / 2, -1.0, dv["xc"] + w / 2, -0.7)
    c.pin("M1", "vss", tb[0], tb[1], tb[0] + 0.5, tb[3])
    return tb


def ab_n(name):
    """RN2 (diode, source dabn) in the middle, FNL and ABN on either side, 4.4/1 each, gate vabn; narrow
    2/1 dummies at both ends (D = S = G = vabn); vabn M2 track above the row joins RN2's drain and both gate
    columns; drains l2 / a up to M1 pins on the top edge, sources down to M2 pins on the bottom edge."""
    c = Cell(name)
    dn = ("dummy", 2, 1, "vabn", "vabn", "vabn")
    seq = [dn, ("FNL", 4.4, 1, "l2", "vabn", "l1"), ("RN2", 4.4, 1, "vabn", "vabn", "dabn"),
           ("ABN", 4.4, 1, "a", "vabn", "b"), dn]
    X, H, devs = one_row(c, seq)
    for dv, xc in ((devs[0], -0.33), (devs[-1], X + 0.33)):
        c.bridge(dv, "bot", xc)
        c.bridge(dv, "top", xc)
    tv = g5(H + 0.38)
    ytop = g5(tv + 0.145 + 0.6)
    for xc in (-0.33, X + 0.33):
        c.box("M1", xc - 0.13, H - 0.2, xc + 0.13, tv + 0.145)
        c.via(xc, tv)
    c.track(-0.475, X + 0.475, tv)
    c.pin("M2", "vabn", -0.475, tv - 0.145, 0.025, tv + 0.145)
    for dv, d in zip(devs[1:-1], ("l2", "vabn", "a")):
        if d == "vabn":
            c.tab(dv["xc"], dv["top"][0], tv + 0.145, tv)
        else:
            c.box("M1", dv["xc"] - 0.555, dv["top"][0], dv["xc"] + 0.555, ytop)
            c.pin("M1", d, dv["xc"] - 0.555, ytop - 0.3, dv["xc"] + 0.555, ytop)
    bottom_pins(c, X, zip(devs[1:-1], ("l1", "dabn", "b")))
    c.tgo()
    c.info = "row: D | FNL RN2 ABN | D"
    return c


def pd_n(name):
    """XSB (b -> vsso) and XSABN (vabn -> vss), 1/0.45 each, gate en_3v3_b, separate sources, no dummies
    (switches, no matching: rule 1 (b)); gate columns at both ends; tie strip under the row."""
    c = Cell(name)
    seq = [("SB", 1, 0.45, "b", "en_3v3_b", "vsso"), ("SABN", 1, 0.45, "vabn", "en_3v3_b", "vss")]
    X, H, devs = one_row(c, seq, dummies_to_col=False)
    ytop = g5(H + 0.6)
    for dv, d in zip(devs, ("b", "vabn")):
        c.box("M1", dv["xc"] - 0.145, dv["top"][0], dv["xc"] + 0.145, ytop)
        c.pin("M1", d, dv["xc"] - 0.145, ytop - 0.3, dv["xc"] + 0.145, ytop)
    bottom_pins(c, X, zip(devs, ("vsso", "vss")))
    gy = sum(devs[0]["gate"]) / 2
    c.pin("M1", "en_3v3_b", -0.46, gy - 0.1, -0.20, gy + 0.1)
    c.tgo()
    c.info = "row: SB SABN (no dummies)"
    return c


def bias_tree_n(name):
    """NBPC (2.4/6) and its twin (dummy 2.4/6) at the ends, NBP NI NABP (6/6) between, NI (diode) in the
    middle; gate ni. Switches TGN (iref -> ni, gate en_3v3) left and TDN (ni -> vss, gate en_3v3_b) right of
    the row's gate columns, mirror images; ni track above the row; tie strip below."""
    c = Cell(name)
    seq = [("NBPC", 2.4, 6, "vbpc", "ni", "vss"), ("NBP", 6, 6, "vbp", "ni", "vss"), ("NI", 6, 6, "ni", "ni", "vss"),
           ("NABP", 6, 6, "vabp", "ni", "vss"), ("dummy", 2.4, 6, "ni", "ni", "ni")]
    X, H, devs = one_row(c, seq)
    tb = c.tie(-2.96, -0.21 - TIEW, X + 2.96, -0.21)
    for dv in devs[:-1]:                                 # sources into the tie
        c.box("M1", dv["x0"], tb[1], dv["x1"], dv["bot"][1])
    c.bridge(devs[-1], "bot", X + 0.33)
    c.bridge(devs[-1], "top", X + 0.33)
    tn = g5(H + 0.38)
    ytop = g5(tn + 0.145 + 0.6)
    c.box("M1", -0.46, H - 0.2, -0.20, tn + 0.145)
    c.box("M1", X + 0.20, H - 0.2, X + 0.46, tn + 0.145)
    for xc in (-0.33, X + 0.33):
        c.via(xc, tn)
    c.track(-0.33 - 0.145, X + 0.33 + 0.145, tn)
    c.pin("M2", "ni", X + 0.33 - 0.355, tn - 0.145, X + 0.33 + 0.145, tn + 0.145)
    for dv in devs[:-1]:
        if dv is devs[2]:
            c.tab(dv["xc"], dv["top"][0], tn + 0.145, tn)
        else:
            wt = min(TAB, dv["w"] - 0.4)
            c.box("M1", dv["xc"] - wt / 2, dv["top"][0], dv["xc"] + wt / 2, ytop)
    for dv, n in zip((devs[0], devs[1], devs[3]), ("vbpc", "vbp", "vabp")):
        wt = min(TAB, dv["w"] - 0.4)
        c.pin("M1", n, dv["xc"] - wt / 2, ytop - 0.3, dv["xc"] + wt / 2, ytop)
    # switches: 1/0.45, W along x, 0.96 left / right of the row's Activ ends (poly 0.18 from the column fill)
    ys = g5(H / 2 - 0.565)
    tg = c.mos("TGN", 1, 0.45, -1.96, ys, "iref", "en_3v3", "ni")
    td = c.mos("TDN", 1, 0.45, X + 0.96, ys, "ni", "en_3v3_b", "vss", mx=True)
    c.gate_col(-2.29, [tg["gate"]], tg["gate"][0], tg["gate"][1], (-2.56, -2.06))
    c.gate_col(X + 2.29, [td["gate"]], td["gate"][0], td["gate"][1], (X + 2.06, X + 2.56))
    c.bridge(tg, "bot", -0.33)                          # TGN source (ni) to the row's left gate column
    c.bridge(td, "top", X + 0.33)                        # TDN drain (ni) to the right gate column
    c.box("M1", tg["xc"] - 0.145, tg["top"][0], tg["xc"] + 0.145, ytop)        # iref up to the top edge
    c.pin("M1", "iref", tg["xc"] - 0.145, ytop - 0.3, tg["xc"] + 0.145, ytop)
    c.box("M1", td["xc"] - 0.145, tb[1], td["xc"] + 0.145, td["bot"][1])        # TDN source down to the tie
    c.pin("M1", "en_3v3", -2.42, tg["gate"][0], -2.16, tg["gate"][1])
    c.pin("M1", "en_3v3_b", X + 2.16, td["gate"][0], X + 2.42, td["gate"][1])
    c.pin("M1", "vss", tb[0], tb[1], tb[0] + 0.5, tb[3])
    c.tgo()
    c.info = "row: [TGN] | NBPC NBP NI NABP D | [TDN]"
    return c


# ======================================================================================================
# d2s_rhigh: 4 x unit_r2 resistor as 4 x rhigh 0.5 / 12.65 in series, map of layout_primitives.md section 5
# with a dummy strip at both ends; wired as bg_res_c (Via1 on each head, M2 stub to a link level, M1 link).
# ======================================================================================================
def rhigh(name):
    c = Cell(name)
    MAP = ["dummy", "A", "B", "C1", "C2", "C2", "C1", "B", "A", "A", "B", "C1", "C2", "C2", "C1", "B", "A", "dummy"]
    P, SEG = 0.68, 12.65                                # pitch: rhigh 0.5 + Gat_b 0.18 (library, DRC clean)
    seg = pya.Layout.create_cell(ly, "rhigh", "SG13_dev", {"w": "0.5u", "l": "%gu" % SEG, "b": "0"})
    HB, HT = (-0.41, -0.15), (12.80, 13.06)             # head M1 of the PCell (measured)
    xh = lambda i: g5(i * P + 0.25)
    for i, u in enumerate(MAP):
        c.c.insert(pya.DCellInstArray(seg.cell_index(), pya.DTrans(pya.DVector(g5(i * P), 0))))
        c.note(u, xh(i), SEG / 2)
    links = {"b": [], "t": []}
    for u in ("A", "B", "C1", "C2"):
        ps = [i for i, m in enumerate(MAP) if m == u]
        nodes = ["sa_" + u, u + "_1", u + "_2", u + "_3", "sb_" + u]
        for k in range(4):
            c.cdl.append("R%s_%d %s %s vss rhigh w=0.5u l=%gu m=1 b=0" % (u, k, nodes[k], nodes[k + 1], SEG))
        links["b"] += [(ps[0], ps[1]), (ps[2], ps[3])]
        links["t"] += [(ps[1], ps[2])]
        for i, n in ((ps[0], nodes[0]), (ps[3], nodes[4])):
            c.pins.append((n, None, i, None))
    c.cdl += ["Rdummy_%d vss vss vss rhigh w=0.5u l=%gu m=1 b=0" % (k, SEG) for k in range(2)]
    W, S1 = 0.29, 0.18
    lev = {}
    for side in ("b", "t"):                              # interval colouring: nested links on separate levels
        out = []
        for a, b in sorted(links[side], key=lambda t: t[1] - t[0]):
            for L in out:
                if all(xh(a) - W / 2 >= xh(o[1]) + W / 2 + S1 or xh(o[0]) - W / 2 >= xh(b) + W / 2 + S1 for o in L):
                    L.append((a, b))
                    break
            else:
                out.append([(a, b)])
        lev[side] = out
    yl = {"b": [g5(HB[0] - S1 - W / 2 - k * (W + S1)) for k in range(len(lev["b"]))],
          "t": [g5(HT[1] + S1 + W / 2 + k * (W + S1)) for k in range(len(lev["t"]))]}
    yh = {"b": (HB[0] + HB[1]) / 2, "t": (HT[0] + HT[1]) / 2}
    for side in ("b", "t"):
        for k, L in enumerate(lev[side]):
            y = yl[side][k]
            for a, b in L:
                c.box("M1", xh(a) - W / 2, y - W / 2, xh(b) + W / 2, y + W / 2)
                for i in (a, b):
                    c.via(xh(i), y)
                    c.via(xh(i), yh[side])
                    c.box("M2", xh(i) - W / 2, min(y, yh[side]) - W / 2, xh(i) + W / 2, max(y, yh[side]) + W / 2)
    ytop = g5(yl["t"][-1] + W / 2)
    ybot = g5(yl["b"][-1] - W / 2)
    term = c.pins
    c.pins = []
    for n, _, i, _ in term:                              # terminals: M2 from the top head to the top edge
        c.via(xh(i), yh["t"])
        c.box("M2", xh(i) - W / 2, yh["t"] - W / 2, xh(i) + W / 2, ytop)
        c.pin("M2", n, xh(i) - W / 2, ytop - 0.4, xh(i) + W / 2, ytop)
    # ties left and right, Activ 0.54 from the strips (EXTB_c 0.31 from the EXTBlock at -0.2, as the library),
    # symmetric in y about the strip centre; dummy heads strapped into them in M1
    xr = g5(17 * P + 0.5)
    ym = SEG / 2
    tl = c.tie(-0.54 - TIEW, 2 * ym - ytop, -0.54, ytop)
    trr = c.tie(xr + 0.54, 2 * ym - ytop, xr + 0.54 + TIEW, ytop)
    for (x0, x1) in ((tl[0], 0.48), (17 * P + 0.02, trr[2])):
        for hy in (HB, HT):
            c.box("M1", x0, hy[0], x1, hy[1])
    c.pin("M1", "vss", tl[0], ym - 0.5, tl[2], ym + 0.5)
    c.info = "strips: %s" % " ".join(MAP)
    return c


# ======================================================================================================
cells = [sinks("sinks_6x6_c2"), casc_n("d2s_casc_n_c2"), ab_n("d2s_ab_n_c2"), pd_n("d2s_pd_n_c2"),
         bias_tree_n("bias_tree_n_c2"), rhigh("d2s_rhigh_c2")]
# s2d variant: the same block turned by 90 degrees (pins x / vbn / y on the bottom edge), as v1's variant
v = Cell("sinks_6x6_s2d_c2")
v.c.insert(pya.DCellInstArray(cells[0].c.cell_index(), pya.DTrans(pya.DTrans.R90, pya.DVector(0, 0))))
v.cdl, v.info = cells[0].cdl, "sinks_6x6_c2 turned R90"
v.pins = [(n, m, -y, x) for n, m, x, y in cells[0].pins]
cells.insert(1, v)

opt = pya.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write("d2s_n2_cells.gds", opt)
with open("d2s_n2_cells.cdl", "w") as f:
    f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
            "* d2s_n2_cells.cdl: reference netlists of d2s_n2_cells.gds (build_d2s_n2.py, agent N2, C2 2026-10-31).\n"
            "* One line per finger / segment as drawn, every dummy a device; bulk = vss (substrate).\n")
    for k in cells:
        nets = sorted({p[0] for p in k.pins})
        f.write("\n.SUBCKT %s %s\n%s\n.ENDS %s\n" % (k.name, " ".join(nets), "\n".join(k.cdl), k.name))
for k in cells:
    b = k.c.dbbox()
    print("%-18s %6.2f x %6.2f um  %s" % (k.name, b.width(), b.height(), k.info))
    for n, m, x, y in sorted(k.pins):
        print("    pin %-9s %s (%.3f, %.3f)" % (n, m, x, y))
