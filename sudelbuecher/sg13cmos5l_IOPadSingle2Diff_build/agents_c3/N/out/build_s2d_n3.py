# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""s2d_n3_cells: the NMOS layout primitives and the R block of the IOPadSingle2Diff pad buffer s2d_mpdda_pd and
its bias tree (agent N, C3 2026-11-03). Built on build_d2s_n2.py (agent N2, C2) and F2's fixes of its cells.

    cd out && python3 build_s2d_n3.py        ->  s2d_n3_cells.gds, s2d_n3_cells.cdl

Cells: sinks_6x6_s2d_c3, s2d_sinks_cmfb_c3, s2d_casc_n_c3, s2d_pd_n_c3, s2d_cload_c3, s2d_rhigh_c3,
bias_tree_noab_n_c3 (the two sink blocks also as their unturned cores *_core).

Rules (BRIEF.md): device layers mirror-symmetric about every row's center line and, in two-row blocks, about the
line between the rows; the same dummy at both ends of every row; dummies D = S = vss, gate by abutment; gate
contacts on poly as tall as the gate (no necks); unmodified SG13_dev PCells; taps only at the periphery, as a
closed p+ ring.

How a row is built (as N2):
  - every MOS is one SG13_dev nmosHV finger (ng=1), turned R270 so W runs along the row and L across it; fingers
    0.25 apart (Gat.b1), so their poly endcaps merge into one gate strip per row. Devices right of the cell's
    vertical axis are placed mirrored about their own center, so each row is an exact mirror image;
  - gate contact columns at both row ends (casc_n: also beside BNC), contacts on a poly fill as tall as the gate,
    M1 column 0.26 um; the columns of both rows joined in M1 through the band;
  - inner stripes (band) carry the drains: 1.11 um M1 tabs with 3 Via1 onto M2 tracks (row 1 tabs 0.75 left of
    the finger center, row 2 0.75 right); outer stripes carry the sources;
  - end dummies: outer stripe plated into the ring, inner stripe joined to the ring by a 0.29 um M1 lane between
    the dummy and the gate column (the library's sinks_6x6 lane, log 2026-10-27 01:03); no metal over a channel,
    except the M1 strap of the sinks' BN twin (F2's fix of the removed center columns).
Rule values (sg13cmos5l_tech_default.json): Act_b 0.21, Gat_b 0.18, Gat_b1 0.25, Gat_d 0.07, Cnt_a 0.16, Cnt_b
0.18, Cnt_c 0.07, Cnt_d 0.07, Cnt_e 0.14, Cnt_f 0.11, M1_b 0.18, M1_c1 0.05, M1_d 0.09, M1_e 0.22, V1_a 0.19,
V1_b 0.22, V1_c 0.01, V1_c1 0.05, M2_b 0.21, pSD_c1 0.03, pSD_d 0.18, pSD_j1 0.40, TGO_a 0.27, EXTB_c 0.31, LU_b 20.
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


GAP, MID = 0.25, 0.85        # finger gap (Gat.b1); gap holding a gate column (casc_n, beside BNC)
TAB, VOFF = 1.11, 0.75       # drain tab: 3 x V1_a 0.19 + 2 x V1_b 0.22 + 2 x V1_c1 0.05; offset from finger center
TP = 0.50                    # M2 track pitch: 0.29 + M2_b 0.21
TM = 0.295                   # band edge to first track center: far tab end 0.145 + M1_e 0.22 - stripe inset 0.07
TIEW = 0.30                  # tie Activ: Cnt_a 0.16 + 2 x Cnt_c 0.07
LANE = 0.29                  # dummy lane (vss) beside an end dummy
COL = 0.64                   # gate column center from the row end: lane 0.29 + M1_e 0.22 + column half 0.13
RS = 0.18                    # ring M1 to the nearest unrelated M1 (M1_b); 0.22 where the neighbor is wide


class Cell:
    def __init__(self, name):
        self.name, self.c = name, ly.create_cell(name)
        self.cdl, self.pins = [], []

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
        the bottom / top Activ edge. mx: mirrored about its own center line (devices right of the axis)."""
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

    def ring(self, x0, y0, x1, y1):
        """closed p+ substrate tie ring (vss), Activ 0.30 wide with outer edges x0 .. x1, y0 .. y1, pSD 0.03
        around (pSD_c1); contacts along the horizontal legs over their full length, along the vertical legs
        between them (Cnt_b 0.18 at the corners); M1 0.26 over every contact (Activ inset 0.02, M1_c1 0.05 all
        round). Returns the inner M1 edges (left, bottom, right, top)."""
        legs = ((x0, y0, x1, y0 + TIEW), (x0, y1 - TIEW, x1, y1), (x0, y0, x0 + TIEW, y1), (x1 - TIEW, y0, x1, y1))
        for a, b, cc, d in legs:
            self.box("Activ", a, b, cc, d)
            self.box("pSD", a - 0.03, b - 0.03, cc + 0.03, d + 0.03)
            self.box("M1", a + 0.02, b + 0.02, cc - 0.02, d - 0.02)
        for p in centered(x0 + 0.07, x1 - 0.07):
            self.cont(p, y0 + 0.07)
            self.cont(p, y1 - 0.23)
        for p in centered(y0 + 0.41, y1 - 0.41):
            self.cont(x0 + 0.07, p)
            self.cont(x1 - 0.23, p)
        self.rg = (x0 + TIEW - 0.02, y0 + TIEW - 0.02, x1 - TIEW + 0.02, y1 - TIEW + 0.02)
        return self.rg

    def gate_col(self, xc, granges, y0, y1, fill):
        """gate contact column at x center xc: contacts on a poly fill (x range 'fill') as tall as each gate
        range, M1 0.26 wide from y0 to y1."""
        for g0, g1 in granges:
            self.box("GatPoly", fill[0], g0, fill[1], g1)
            for p in centered(g0 + 0.07, g1 - 0.07):
                self.cont(xc - 0.08, p)
        self.box("M1", xc - 0.13, y0, xc + 0.13, y1)

    def bridge(self, dev, side, xc):
        """M1 from a stripe ('bot' / 'top') of dev to the gate column at xc (diodes, switches)."""
        s0, s1 = dev[side]
        xe = dev["x0"] + 0.1 if xc < dev["x0"] else dev["x1"] - 0.1
        self.box("M1", xc, s0, xe, s1)

    def plate(self, dev, side):
        """M1 plate from a stripe of dev into the ring's bottom ('bot') or top ('top') leg."""
        if side == "bot":
            self.box("M1", dev["x0"], self.rg[1], dev["x1"], dev["bot"][1])
        else:
            self.box("M1", dev["x0"], dev["top"][0], dev["x1"], self.rg[3])

    def lane(self, dev, inner, left):
        """vss lane of an end dummy: M1 0.29 wide beside its outer Activ edge, from its inner stripe into the
        ring leg on the far side of the row (no metal over the channel)."""
        xa = dev["x0"] - LANE if left else dev["x1"]
        if inner == "top":                            # row 1: inner stripe on top, lane down to the bottom leg
            self.box("M1", xa, self.rg[1], xa + LANE, dev["top"][1])
        else:
            self.box("M1", xa, dev["bot"][0], xa + LANE, self.rg[3])

    def tab(self, xc, ya, yb, yv, w=TAB):
        """M1 tab from ya to yb, centered on xc, Via1s at yv (3 on 1.11, 1 on 0.29)."""
        self.box("M1", xc - w / 2, ya, xc + w / 2, yb)
        for k in ((-0.41, 0, 0.41) if w >= TAB else (0,)):
            self.via(xc + k, yv)

    def track(self, x0, x1, y):
        self.box("M2", x0, y - 0.145, x1, y + 0.145)

    def tgo(self):
        """one ThickGateOx rectangle: every Activ (devices and ring) + 0.27 (TGO_a)."""
        r = pya.Region(self.c.begin_shapes_rec(LI["Activ"])).bbox().to_dtype(ly.dbu)
        self.box("TGO", r.left - 0.27, r.bottom - 0.27, r.right + 0.27, r.top + 0.27)
        return r


def centered(a, b, size=0.16, pitch=0.34):
    """lower edges of contacts filling [a, b], mirror-symmetric about the range center on the 0.005 grid (so mirror
    images coincide). If the span is an odd number of 5 nm steps, the count is made even and the middle gap is
    0.005 wider than the pitch."""
    n = int((b - a - size) / pitch + 1e-6) + 1
    rest = round((b - a - size - (n - 1) * pitch) * NM)
    if rest % 10 == 0:
        return [g5(a + rest / NM / 2 + k * pitch) for k in range(n)]
    n -= n % 2
    c2 = round((a + b - size) * NM)                     # twice the center, nm (odd multiple of 5)
    lo = [(c2 - 5) // 2 - round(pitch * NM) // 2 - k * round(pitch * NM) for k in range(n // 2)]
    assert min(lo) >= round(a * NM) - 1, (a, b)
    return sorted([g5(p / NM) for p in lo] + [g5((c2 - p) / NM) for p in lo])


def place_row(cell, seq, yb, axis):
    """seq: device tuples (label, w, l, d, g, s) and 'C' (a gate column between two devices). Fingers from x = 0;
    those right of 'axis' mirrored. Returns the devices and the x ranges of the C gaps."""
    x, devs, gaps = 0.0, [], []
    for it in seq:
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


def end_cols(X):
    """gate columns at both row ends, COL outside them (room for the dummy lanes); fill from the column out to
    0.10 from the row's Activ (it merges with the gates' endcaps)."""
    return [(-COL, (-COL - 0.15, -0.10)), (X + COL, (X + 0.10, X + COL + 0.15))]


# ======================================================================================================
# Two-row blocks: sinks, sinks_cmfb, casc_n. Row 1 (bottom) and row 2 (top) mirror images about the band.
# ======================================================================================================
def two_rows(cell, r1, r2, band, mid_cols=False):
    """places both rows, end (and mid) gate columns, band tracks; returns geometry."""
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
    cols = end_cols(X)
    if mid_cols:                                        # the two gaps beside BNC: fill 0.25 short of BNC's side
        cols += [((a + b) / 2, (a + 0.10, b - 0.25) if k == 0 else (a + 0.25, b - 0.10)) for k, (a, b) in
                 enumerate(gp1)]
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


def ring_x(X, outer_m1):
    """ring leg Activ x range left of a block whose outermost inner M1 edge is at -outer_m1 (mirrored right)."""
    xi = g5(-outer_m1 - RS + 0.02)                      # ring Activ inner edge
    return xi - TIEW, xi, X - xi, X - xi + TIEW


def sink_block(name, m1, m2, f, band):
    """two rows of 6/6 fingers on vbn, row 2 the image of row 1 about the band; a narrow 2/6 dummy at both ends of
    both rows (D = S = vss, gate vbn by abutment); gate columns at the row ends only; drains to the band tracks;
    sources plated into the closed p+ ring. f: map key -> (label, w, l, d, g, s); 'T' (BN's twin) is strapped."""
    c = Cell(name)
    dn = ("dummy", 2, 6, "vss", "vbn", "vss")
    seq = lambda m: [dn] + [f[k] for k in m] + [dn]
    g = two_rows(c, seq(m1), seq(m2), band)
    X, top, tr = g["X"], g["top"], g["tr"]
    xa, xb, xc_, xd = ring_x(X, COL + 0.13)
    c.ring(xa, -0.21 - TIEW, xd, top + 0.21 + TIEW)
    for row, devs in ((1, g["d1"]), (2, g["d2"])):
        inner, outer = ("top", "bot") if row == 1 else ("bot", "top")
        for k, (dv, it) in enumerate(zip(devs, seq(m1 if row == 1 else m2))):
            lab, w, l, d, gn, s = it
            c.plate(dv, outer)                            # sources and dummies' outer stripes: vss
            if d in band and d != "vbn" or lab == "BN":
                drains(c, g, dv, row, d)
            elif k in (0, len(devs) - 1):
                c.lane(dv, inner, k == 0)
            else:                                         # BN's twin: inner stripe strapped across its channel
                c.box("M1", dv["xc"] - 0.145, dv["bot"][0], dv["xc"] + 0.145, dv["top"][1])
    x0 = xa - 0.27
    for n, t in tr.items():
        c.track(x0, X + COL + 0.145, t)
        c.pin("M2", n, x0, t - 0.145, x0 + 0.5, t + 0.145)
    for xc in g["cols"]:
        c.via(xc, tr["vbn"])
    c.pin("M1", "vss", xa + 0.02, -0.49, xa + 0.52, -0.23)
    c.tgo()
    c.info = "rows: D | %s | D  /  D | %s | D; ring" % (" ".join(m1), " ".join(m2))
    return c


def turned(core, name):
    """the core block turned R90 (pins on the bottom edge), as N2's sinks_6x6_s2d_c2."""
    v = Cell(name)
    v.c.insert(pya.DCellInstArray(core.c.cell_index(), pya.DTrans(pya.DTrans.R90, pya.DVector(0, 0))))
    v.cdl, v.info = core.cdl, core.name + " turned R90"
    v.pins = [(n, m, -y, x) for n, m, x, y in core.pins]
    return v


def sinks(name):
    """SX / SY 6 + 6 fingers 6/6 on vbn, rows X Y Y X X Y / Y X X Y Y X (layout_primitives.md section 5) split at
    the center, BN (diode) in the middle of row 1, its twin T (dummy 6/6) in the middle of row 2."""
    f = {"X": ("SX", 6, 6, "x", "vbn", "vss"), "Y": ("SY", 6, 6, "y", "vbn", "vss"),
         "BN": ("BN", 6, 6, "vbn", "vbn", "vss"), "T": ("BNtwin", 6, 6, "vss", "vbn", "vss")}
    m1 = ["X", "Y", "Y", "BN", "X", "X", "Y"]
    m2 = [{"X": "Y", "Y": "X", "BN": "T"}[k] for k in m1]
    return sink_block(name, m1, m2, f, ["x", "vbn", "y"])


def sinks_cmfb(name):
    """SXC / SYC 4 + 4 fingers 6/6 on vbn, cross-coupled rows X Y Y X / Y X X Y; no diode."""
    f = {"X": ("SXC", 6, 6, "xc", "vbn", "vss"), "Y": ("SYC", 6, 6, "yc", "vbn", "vss")}
    return sink_block(name, list("XYYX"), list("YXXY"), f, ["xc", "vbn", "yc"])


def casc_n(name):
    """CX (x -> voutp), CY (y -> voutn), CXC (xc -> vcmfb), CYC (yc -> vdd), 2 x 15/3 each, point-symmetric rows
    CXC CX [BNC] CY CYC / CYC CY [BNC] CX CXC; BNC (1/8, diode) alone in the middle, spanning both rows and the
    band (on both symmetry axes); narrow 2/3 dummies at both ends of both rows. Band tracks: drains and vbnc;
    sources on three M2 levels below row 1 and three above row 2, joined by M1 verticals (x, y left; xc, yc
    right) inside the ring."""
    c = Cell(name)
    dev = {"CX": ("CX", 15, 3, "voutp", "vbnc", "x"), "CY": ("CY", 15, 3, "voutn", "vbnc", "y"),
           "CXC": ("CXC", 15, 3, "vcmfb", "vbnc", "xc"), "CYC": ("CYC", 15, 3, "vdd", "vbnc", "yc")}
    dn = ("dummy", 2, 3, "vss", "vbnc", "vss")
    slot = ("slot", 1, 3, None, None, None)              # BNC's place in both rows, between two gate columns
    r1 = [dn, dev["CXC"], dev["CX"], "C", slot, "C", dev["CY"], dev["CYC"], dn]
    r2 = [dn, dev["CYC"], dev["CY"], "C", slot, "C", dev["CX"], dev["CXC"], dn]
    band = ["vcmfb", "voutp", "vbnc", "voutn", "vdd"]
    g = two_rows(c, r1, r2, band, mid_cols=True)
    X, top, tr, d1, d2, colx = g["X"], g["top"], g["tr"], g["d1"], g["d2"], g["cols"]
    bnc = c.mos("BNC", 1, 8, g["gaps"][0][1], g5((top - 8.68) / 2), "vbnc", "vbnc", "vss")
    for gr in (d1[0]["gate"], d2[0]["gate"]):           # fill joined to BNC's gate only where they overlap in y
        y0, y1 = max(gr[0], bnc["gate"][0]), min(gr[1], bnc["gate"][1])
        c.box("GatPoly", bnc["x0"] - 0.25, y0, bnc["x0"] - 0.10, y1)
        c.box("GatPoly", bnc["x1"] + 0.10, y0, bnc["x1"] + 0.25, y1)
    # source levels: k = 0 nearest the row; (net, row-1 level, row-2 level), verticals left (x, y) / right
    lev = {"x": (0, 1), "yc": (0, 2), "y": (1, 0), "xc": (2, 0)}
    vx = {"x": -COL - 0.13 - 0.22 - 0.29, "y": -COL - 0.13 - 2 * 0.22 - 2 * 0.29}
    vx["xc"], vx["yc"] = X - vx["x"] - 0.29, X - vx["y"] - 0.29
    ylo = lambda k: g5(-TM - TP * k)
    yhi = lambda k: g5(top + TM + TP * k)
    ends = {}
    for row, devs, seqr in ((1, d1, r1), (2, d2, r2)):
        live = [it for it in seqr if it not in ("C", slot)]
        for k, (dv, it) in enumerate(zip(devs, live)):
            lab, w, l, d, gn, s = it
            inner, outer = ("top", "bot") if row == 1 else ("bot", "top")
            if lab == "dummy":
                continue
            drains(c, g, dv, row, d)
            if row == 1:
                y = ylo(lev[s][0])
                xt = dv["xc"] + VOFF
                c.tab(xt, y - 0.145, dv["bot"][1], y)
            else:
                y = yhi(lev[s][1])
                xt = dv["xc"] - VOFF
                c.tab(xt, dv["top"][0], y + 0.145, y)
            ends.setdefault((s, row), []).append(xt)
    # ring: outside the outer verticals (x) and the outermost source levels (y)
    xa, xb, xc_, xd = ring_x(X, -vx["y"])
    ya = g5(ylo(2) - 0.145 - 0.22 + 0.02 - TIEW)
    c.ring(xa, ya, xd, g5(top - ya))
    # dummies: outer stripe plated into the ring, inner stripe by a lane; BNC: drain to the left middle column,
    # source down to the ring
    for row, devs in ((1, d1), (2, d2)):
        inner, outer = ("top", "bot") if row == 1 else ("bot", "top")
        for k in (0, len(devs) - 1):
            c.plate(devs[k], outer)
            c.lane(devs[k], inner, k == 0)
    c.bridge(bnc, "top", colx[2])
    c.box("M1", bnc["xc"] - 0.3, c.rg[1], bnc["xc"] + 0.3, bnc["bot"][1])
    # verticals and source levels
    for s, (k1, k2) in lev.items():
        xv = vx[s]
        y1, y2 = ylo(k1), yhi(k2)
        c.box("M1", xv, y1 - 0.145, xv + 0.29, y2 + 0.145)
        c.via(xv + 0.145, y1)
        c.via(xv + 0.145, y2)
        for row, y in ((1, y1), (2, y2)):
            xs = ends[(s, row)]                          # tab ends: 3 Via1 at +-0.41, M2_c1 0.05
            a, b = min(xs + [xv + 0.41]) - 0.555, max(xs + [xv - 0.12]) + 0.555
            if row == 1:                                 # the bottom levels run on to the pin edge
                a, b = (xa - 0.27, b) if xv < 0 else (a, xd + 0.27)
            c.track(a, b, y)
        if xv < 0:
            c.pin("M2", s, xa - 0.27, y1 - 0.145, xa + 0.23, y1 + 0.145)
        else:
            c.pin("M2", s, xd - 0.23, y1 - 0.145, xd + 0.27, y1 + 0.145)
    for n, t in tr.items():
        c.track(xa - 0.27, X + COL + 0.145, t)
        c.pin("M2", n, xa - 0.27, t - 0.145, xa + 0.23, t + 0.145)
    for xc in colx:
        c.via(xc, tr["vbnc"])
    c.pin("M1", "vss", xa + 0.02, ya + 0.02, xa + 0.52, ya + 0.28)
    c.tgo()
    c.info = "rows: D | CXC CX [BNC] CY CYC | D  /  D | CYC CY [BNC] CX CXC | D; ring"
    return c


# ======================================================================================================
# Output ties TPN / TNN and the load capacitors CLP / CLN
# ======================================================================================================
def pd_pair(c, x0, ys):
    """TPN (voutp - vcm) and TNN (voutn - vcm), 1/0.45 each, gate en_3v3_b: two PCells in their own orientation
    (L along x) at 0.83 pitch sharing the vcm stripe (Christoph's compaction of bias_tree_sw, log 2026-10-27
    17:30); the gates joined by one poly cap above the Activ, contacted 0.18 above it (17:43; Cnt_e 0.14, M1_b
    0.18 to the stripes), cap 0.55 above the Activ so no poly piece beyond the endcap zone is narrower than 0.30;
    M1 bar 0.21 (Via1-ready, V1_c 0.01); vcm pad 0.21 x 0.29 on the middle stripe (Via1-ready)."""
    dev = pya.Layout.create_cell(ly, "nmosHV", "SG13_dev", {"w": "1u", "l": "0.45u", "ng": "1"})
    for k, (lab, d) in enumerate((("TPN", "voutp"), ("TNN", "voutn"))):
        c.c.insert(pya.DCellInstArray(dev.cell_index(), pya.DTrans(pya.DVector(g5(x0 + 0.83 * k), g5(ys)))))
        c.cdl.append("M%s_%d %s en_3v3_b vcm vss sg13_hv_nmos w=1u l=0.45u ng=1 m=1" % (lab, len(c.cdl), d))
        c.note(lab, x0 + 0.565 + 0.83 * k, ys - 0.3)
    c.box("GatPoly", x0 + 0.34, ys + 1.10, x0 + 1.62, ys + 1.55)
    for xq in (0.485, 1.315):
        c.cont(x0 + xq, ys + 1.18)
    c.box("M1", x0 + 0.27, ys + 1.18, x0 + 1.69, ys + 1.39)
    c.box("M1", x0 + 0.875, ys + 0.355, x0 + 1.085, ys + 0.645)
    return dict(p=(x0 + 0.07, x0 + 0.23), m=x0 + 0.98, n=(x0 + 1.73, x0 + 1.89), ys=ys, bar=ys + 1.285,
                en=x0 + 0.42)


def pd_n(name):
    """the output ties alone (no tap: they live inside s2d_cload_c3, whose ring is their tap); pins on the
    stripes, the vcm pad and the gate bar, no stubs."""
    c = Cell(name)
    p = pd_pair(c, 0, 0)
    c.pin("M1", "voutp", p["p"][0], 0.25, p["p"][1], 0.75)
    c.pin("M1", "voutn", p["n"][0], 0.25, p["n"][1], 0.75)
    c.pin("M1", "vcm", p["m"] - 0.105, 0.355, p["m"] + 0.105, 0.645)
    c.pin("M1", "en_3v3_b", 0.27, 1.18, 0.75, 1.39)
    c.box("TGO", -0.27, -0.52, 2.23, 1.82)
    c.info = "TPN | vcm | TNN (shared vcm stripe), no tap"
    return c


def cload(name):
    """CLP (gate voutp) and CLN (gate voutn), hv NMOS 12 x 12, S / D / B on vss, mirror images; gate contact
    columns on their inner sides (fill as tall as the gate), the output ties TPN / TNN between them (the drains
    join the columns directly); closed p+ ring, S / D plates into its top and bottom legs. Pins: voutp, en_3v3_b,
    vcm, voutn on M2 at the top edge."""
    c = Cell(name)
    a = c.mos("CLP", 12, 12, 0, 0, "vss", "voutp", "vss")
    xs = 12.80                                           # tie pair: its Activ + 0.25 leaves 0.30 of the fill
    X = g5(2 * (xs + 0.98))
    b = c.mos("CLN", 12, 12, X - 12, 0, "vss", "voutn", "vss", mx=True)
    H = 12.68
    c.ring(-0.73, -0.51, X + 0.73, H + 0.51)             # side legs: pSD_j1 0.40 from the gates over Activ
    for dv in (a, b):
        c.plate(dv, "bot")
        c.plate(dv, "top")
    ys = g5(H + 0.21 - 0.25 - 0.30 - 1.25)               # 0.30 of its cap outside the Activ + 0.25 zones
    p = pd_pair(c, xs, ys)
    yt = H + 0.51 + 0.03                                 # top edge (ring pSD)
    for xc, fill, pn, sx in ((12.33, (12.10, 12.60), "voutp", p["p"][1]), (X - 12.33, (X - 12.60, X - 12.10),
                                                                           "voutn", p["n"][0])):
        c.gate_col(xc, [a["gate"]], 0.36, 12.32, fill)
        c.box("M1", min(xc, sx), ys, max(xc, sx), ys + 1.0)          # tie drain to its column
        c.via(xc, 12.1)
        c.box("M2", xc - 0.145, 11.955, xc + 0.145, yt)
        c.pin("M2", pn, xc - 0.145, yt - 0.4, xc + 0.145, yt)
    for xc, yv, pn in ((p["m"], ys + 0.5, "vcm"), (p["en"], p["bar"], "en_3v3_b")):
        c.via(xc, yv)
        c.box("M2", xc - 0.145, yv - 0.145, xc + 0.145, yt)
        c.pin("M2", pn, xc - 0.145, yt - 0.4, xc + 0.145, yt)
    c.pin("M1", "vss", -0.71, -0.49, -0.21, -0.23)
    c.tgo()
    c.info = "CLP [voutp | TPN vcm TNN | voutn] CLN; ring"
    return c


# ======================================================================================================
# Bias tree without the class-AB branch: NBPC NBP NI D, switches TGN / TDN at the row ends
# ======================================================================================================
def bias_tree(name):
    """NBPC (2.4/6) at one end and its twin D (2.4/6 dummy, D = S = vss) at the other, NBP and NI (6/6) between,
    gate ni; the row is mirror-symmetric with nothing on its axis. TGN (iref - ni, gate en_3v3) left and TDN
    (ni - vss, gate en_3v3_b) right of the row's gate columns, mirror images, each with its own column; ni track
    (M2) above the row joins NI's drain and both columns; closed p+ ring."""
    c = Cell(name)
    seq = [("NBPC", 2.4, 6, "vbpc", "ni", "vss"), ("NBP", 6, 6, "vbp", "ni", "vss"), ("NI", 6, 6, "ni", "ni", "vss"),
           ("dummy", 2.4, 6, "vss", "ni", "vss")]
    X = row_len(seq)
    devs, _ = place_row(c, seq, 0.0, X / 2)
    H = 6.68
    tn = g5(H + 0.38)                                    # ni track
    yl = g5(tn + TP)                                     # Via1 landing of the drains going to the top edge
    ys = g5(H / 2 - 0.565)                               # switches: gate centered on the row's gate
    tg = c.mos("TGN", 1, 0.45, -1.96, ys, "iref", "en_3v3", "ni")
    td = c.mos("TDN", 1, 0.45, X + 0.96, ys, "ni", "en_3v3_b", "vss", mx=True)
    xa = -3.06                                           # ring: 0.30 of TGN's column fill outside Activ + 0.25
    yt = g5(yl + 0.145 + RS - 0.02 + TIEW)
    c.ring(xa, -0.51, X - xa, yt)
    top = yt + 0.27
    gr = devs[0]["gate"]
    for xc, fill in ((-0.33, (-0.60, -0.10)), (X + 0.33, (X + 0.10, X + 0.60))):
        c.gate_col(xc, [gr], 0.36, tn + 0.145, fill)
        c.via(xc, tn)
    for dv in devs:
        c.plate(dv, "bot")
    c.track(-0.475, X - xa + 0.27, tn)
    c.pin("M2", "ni", X - xa - 0.23, tn - 0.145, X - xa + 0.27, tn + 0.145)
    c.tab(devs[2]["xc"], devs[2]["top"][0], tn + 0.145, tn)                  # NI: diode
    xd = devs[3]["xc"]                                                       # D: drain into the top leg
    c.box("M1", xd - TAB / 2, devs[3]["top"][0], xd + TAB / 2, c.rg[3])
    for dv, n in ((devs[0], "vbpc"), (devs[1], "vbp"), (tg, "iref")):
        y0 = dv["top"][0]
        c.tab(dv["xc"], y0, yl + 0.145, yl, w=0.29)
        c.box("M2", dv["xc"] - 0.145, yl - 0.145, dv["xc"] + 0.145, top)
        c.pin("M2", n, dv["xc"] - 0.145, top - 0.4, dv["xc"] + 0.145, top)
    c.gate_col(-2.29, [tg["gate"]], tg["gate"][0], tg["gate"][1], (-2.56, -2.06))
    c.gate_col(X + 2.29, [td["gate"]], td["gate"][0], td["gate"][1], (X + 2.06, X + 2.56))
    c.bridge(tg, "bot", -0.33)                          # TGN source (ni) to the row's left gate column
    c.bridge(td, "top", X + 0.33)                        # TDN drain (ni) to the right gate column
    c.box("M1", td["xc"] - 0.145, c.rg[1], td["xc"] + 0.145, td["bot"][1])  # TDN source down to the ring
    gy = (tg["gate"][0] + tg["gate"][1]) / 2
    for xc, x1, n in ((-2.29, xa - 0.27, "en_3v3"), (X + 2.29, X - xa + 0.27, "en_3v3_b")):
        c.via(xc, gy)
        c.box("M2", xc + (0.145 if x1 < xc else -0.145), gy - 0.145, x1, gy + 0.145)
        c.pin("M2", n, min(x1, x1 + (0.5 if x1 < 0 else -0.5)), gy - 0.145, max(x1, x1 + (0.5 if x1 < 0 else -0.5)),
              gy + 0.145)
    c.pin("M1", "vss", xa + 0.02, -0.49, xa + 0.52, -0.23)
    c.tgo()
    c.info = "row: [TGN] | NBPC NBP NI D | [TDN]; ring"
    return c


# ======================================================================================================
# s2d_rhigh: 6 x unit_r2 resistor as 4 x rhigh 0.5 / 12.65 in series, mirror-symmetric sequence, a dummy strip at
# both ends; wired as N2's d2s_rhigh_c2 (Via1 on each head, M2 stub to a link level, M1 link), closed p+ ring.
# ======================================================================================================
def rhigh(name):
    c = Cell(name)
    U = ["A1", "A2", "F1", "F2", "M1", "M2"]
    half = U + U[::-1]
    MAP = ["dummy"] + half + half + ["dummy"]
    P, SEG = 0.68, 12.65                                # pitch: rhigh 0.5 + Gat_b 0.18 (library, DRC clean)
    n = len(MAP)
    seg = pya.Layout.create_cell(ly, "rhigh", "SG13_dev", {"w": "0.5u", "l": "%gu" % SEG, "b": "0"})
    HB, HT = (-0.41, -0.15), (12.80, 13.06)             # head M1 of the PCell (measured)
    xh = lambda i: g5(i * P + 0.25)
    for i, u in enumerate(MAP):
        c.c.insert(pya.DCellInstArray(seg.cell_index(), pya.DTrans(pya.DVector(g5(i * P), 0))))
        c.note(u, xh(i), SEG / 2)
    links = {"b": [], "t": []}
    term = []
    for u in U:
        ps = [i for i, m in enumerate(MAP) if m == u]
        nodes = ["sa_" + u, u + "_1", u + "_2", u + "_3", "sb_" + u]
        for k in range(4):
            c.cdl.append("R%s_%d %s %s vss rhigh w=0.5u l=%gu m=1 b=0" % (u, k, nodes[k], nodes[k + 1], SEG))
        links["b"] += [(ps[0], ps[1]), (ps[2], ps[3])]
        links["t"] += [(ps[1], ps[2])]
        term += [(nodes[0], ps[0]), (nodes[4], ps[3])]
    c.cdl += ["Rdummy_%d vss vss vss rhigh w=0.5u l=%gu m=1 b=0" % (k, SEG) for k in range(2)]
    W, S1 = 0.29, 0.18
    lev = {}
    for side in ("b", "t"):                              # interval coloring: nested links on separate levels
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
    # ring: side legs 0.54 from the strips (EXTB_c 0.31 from the EXTBlock at -0.2, as the library), top / bottom
    # legs M1_b from the outermost link levels; symmetric in y about the strip center
    ym = SEG / 2
    y1 = g5(yl["t"][-1] + W / 2 + S1 - 0.02 + TIEW)
    xr = g5((n - 1) * P + 0.5)
    c.ring(-0.54 - TIEW, g5(2 * ym - y1), xr + 0.54 + TIEW, y1)
    ytop = y1 + 0.03
    for nm, i in term:                                  # terminals: M2 from the top head to the top edge
        c.via(xh(i), yh["t"])
        c.box("M2", xh(i) - W / 2, yh["t"] - W / 2, xh(i) + W / 2, ytop)
        c.pin("M2", nm, xh(i) - W / 2, ytop - 0.4, xh(i) + W / 2, ytop)
    for (x0, x1) in ((c.rg[0], 0.48), ((n - 1) * P + 0.02, c.rg[2])):    # dummy heads strapped into the ring
        for hy in (HB, HT):
            c.box("M1", x0, hy[0], x1, hy[1])
    c.pin("M1", "vss", -0.82, ym - 0.5, -0.56, ym + 0.5)
    c.info = "strips: %s; ring" % " ".join(MAP)
    return c


# ======================================================================================================
core_s = sinks("sinks_6x6_s2d_c3_core")
core_c = sinks_cmfb("s2d_sinks_cmfb_c3_core")
cells = [turned(core_s, "sinks_6x6_s2d_c3"), turned(core_c, "s2d_sinks_cmfb_c3"), casc_n("s2d_casc_n_c3"),
         pd_n("s2d_pd_n_c3"), cload("s2d_cload_c3"), rhigh("s2d_rhigh_c3"), bias_tree("bias_tree_noab_n_c3")]
cells += [core_s, core_c]

opt = pya.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write("s2d_n3_cells.gds", opt)
with open("s2d_n3_cells.cdl", "w") as f:
    f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
            "* s2d_n3_cells.cdl: reference netlists of s2d_n3_cells.gds (build_s2d_n3.py, agent N, C3 2026-11-03).\n"
            "* One line per finger / segment as drawn, every dummy a device; bulk = vss (substrate).\n")
    for k in cells:
        nets = sorted({p[0] for p in k.pins})
        f.write("\n.SUBCKT %s %s\n%s\n.ENDS %s\n" % (k.name, " ".join(nets), "\n".join(k.cdl), k.name))
for k in cells:
    b = k.c.dbbox()
    print("%-24s %6.2f x %6.2f um  %7.1f um2  %s" % (k.name, b.width(), b.height(), b.width() * b.height(), k.info))
    for n, m, x, y in sorted(k.pins):
        print("    pin %-9s %s (%.3f, %.3f)" % (n, m, x, y))
