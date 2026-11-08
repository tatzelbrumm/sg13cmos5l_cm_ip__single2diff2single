# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""rb_n_cells: the NMOS rows and the capacitors of the replica bias pad_ref_rb (agent N, session C4, 2026-11-07),
built with the code that built the S2D pad's rows: session C3's build_s2d_n3.py (agent N, 2026-11-03).

    cd out && python3 build_rb_n.py                    ->  rb_n_cells.gds / .cdl (rb_tree_n, rb_casc, rb_mirror,
                                                           rb_cload, bypass_rb, top cell rb_n_cells)
    python3 build_rb_n.py --pad                        ->  pad_regress.gds / .cdl: the pad's rows bias_tree_noab_n_c3,
                                                           s2d_casc_n_c3, sinks_6x6_s2d_c3_core, s2d_cload_c3 rebuilt
                                                           by this script (XOR against the pad GDS = regression test)
    python3 build_rb_n.py --bypass NCM NCR ROWS COLS   ->  bypass_rb_<NCM>_<NCR>_<ROWS>x<COLS>.gds / .cdl only

Provenance: everything from 'import os' to end_cols(), drains() and ring_x() is C3's text unchanged. two_rows,
sink_block, casc_n, pd_pair, cload and bias_tree are C3's functions with the device list and the nets turned into
arguments (C3's values are the defaults or the PAD_* calls at the end); their geometry statements are C3's. The
additions, each marked 'C4:', are: two_rows / sink_block with one row (the mirror row), casc_n with spare 15/3 slots as
dummies and fewer source levels, bias_tree with two drains on one net, cload with the shared stripe on vss. bypass() is
new: the pad cload's capacitor with its gate column, arrayed.

C3's notes on the rows (unchanged):
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
Rule values (sg13cmos5l_tech_default.json): Act_b 0.21, Gat_b 0.18, Gat_b1 0.25, Gat_c 0.18, Gat_d 0.07, Cnt_a 0.16,
Cnt_b 0.18, Cnt_c 0.07, Cnt_d 0.07, Cnt_e 0.14, Cnt_f 0.11, M1_b 0.18, M1_c1 0.05, M1_d 0.09, M1_e 0.22, V1_a 0.19,
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
    """places both rows, end (and mid) gate columns, band tracks; returns geometry.
    C4: r2 None places row 1 and the band only (the columns end on the top track)."""
    X = row_len(r1)
    assert r2 is None or X == row_len(r2)
    ax = X / 2
    H = r1[0][2] + 0.68
    A = H
    tr = {n: g5(A + TM + TP * k) for k, n in enumerate(band)}
    B = g5(A + 2 * TM + TP * (len(band) - 1))
    d1, gp1 = place_row(cell, r1, 0.0, ax)
    d2, gp2 = place_row(cell, r2, B, ax) if r2 else ([], [])
    top = B + H if r2 else g5(tr[band[-1]] + 0.145 + 0.07)
    gr = [d1[0]["gate"], d2[0]["gate"]] if r2 else [d1[0]["gate"]]
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


def sink_block(name, m1, m2, f, band, gn="vbn"):
    """two rows of 6/6 fingers on vbn, row 2 the image of row 1 about the band; a narrow 2/6 dummy at both ends of
    both rows (D = S = vss, gate vbn by abutment); gate columns at the row ends only; drains to the band tracks;
    sources plated into the closed p+ ring. f: map key -> (label, w, l, d, g, s); 'T' (BN's twin) is strapped.
    C4: gn is the gate net (C3: vbn); m2 None gives row 1 alone, the ring closing over the band (as bias_tree's,
    but M1_e 0.22 from the 1.11 tabs: wider than 0.30, parallel run > 1.0)."""
    c = Cell(name)
    dn = ("dummy", 2, 6, "vss", gn, "vss")
    seq = lambda m: [dn] + [f[k] for k in m] + [dn]
    g = two_rows(c, seq(m1), seq(m2) if m2 else None, band)
    X, top, tr = g["X"], g["top"], g["tr"]
    xa, xb, xc_, xd = ring_x(X, COL + 0.13)
    c.ring(xa, -0.21 - TIEW, xd, top + 0.21 + TIEW if m2 else g5(top - 0.07 + 0.22 - 0.02 + TIEW))
    for row, devs, m in ((1, g["d1"], m1), (2, g["d2"], m2)):
        if not devs:
            continue
        inner, outer = ("top", "bot") if row == 1 else ("bot", "top")
        for k, (dv, it) in enumerate(zip(devs, seq(m))):
            lab, w, l, d, _, s = it
            c.plate(dv, outer)                            # sources and dummies' outer stripes: vss
            if d in band:                                 # C3: 'd in band and d != "vbn" or lab == "BN"' (same set)
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
        c.via(xc, tr[gn])
    c.pin("M1", "vss", xa + 0.02, -0.49, xa + 0.52, -0.23)
    c.tgo()
    c.info = "rows: D | %s | D%s; ring" % (" ".join(m1), "  /  D | %s | D" % " ".join(m2) if m2 else "")
    return c


def sinks(name):
    """SX / SY 6 + 6 fingers 6/6 on vbn, rows X Y Y X X Y / Y X X Y Y X (layout_primitives.md section 5) split at
    the center, BN (diode) in the middle of row 1, its twin T (dummy 6/6) in the middle of row 2."""
    f = {"X": ("SX", 6, 6, "x", "vbn", "vss"), "Y": ("SY", 6, 6, "y", "vbn", "vss"),
         "BN": ("BN", 6, 6, "vbn", "vbn", "vss"), "T": ("BNtwin", 6, 6, "vss", "vbn", "vss")}
    m1 = ["X", "Y", "Y", "BN", "X", "X", "Y"]
    m2 = [{"X": "Y", "Y": "X", "BN": "T"}[k] for k in m1]
    return sink_block(name, m1, m2, f, ["x", "vbn", "y"])


def casc_n(name, dev=None, m1=("CXC", "CX", "CY", "CYC"), m2=("CYC", "CY", "CX", "CXC"),
           band=("vcmfb", "voutp", "vbnc", "voutn", "vdd"), lev=None, side=None, tie=None):
    """CX (x -> voutp), CY (y -> voutn), CXC (xc -> vcmfb), CYC (yc -> vdd), 2 x 15/3 each, point-symmetric rows
    CXC CX [BNC] CY CYC / CYC CY [BNC] CX CXC; BNC (1/8, diode) alone in the middle, spanning both rows and the
    band (on both symmetry axes); narrow 2/3 dummies at both ends of both rows. Band tracks: drains and vbnc;
    sources on three M2 levels below row 1 and three above row 2, joined by M1 verticals (x, y left; xc, yc
    right) inside the ring.
    C4: the device map, slot keys, band, source levels and vertical sides are arguments (defaults: C3's). A band
    entry None leaves its track's place empty, so the row pitch stays; a 'dummy' in a 15/3 slot is built as the
    pad sinks' BN twin T: outer stripe plated into the ring, inner stripe strapped to it in M1 across its own
    channel (no vss on M2); a source net without a level above row 2 has no vertical; the ring sits outside the
    levels and verticals in use. tie: a band net; the empty places then get dummy M2 tracks with the band tracks'
    extents (Christoph 2026-11-07: "reproduce the paths as dummies"), without tabs, tied to that net by an M1
    vertical at the free R0 place inside the ring's right leg."""
    c = Cell(name)
    dev = dev or {"CX": ("CX", 15, 3, "voutp", "vbnc", "x"), "CY": ("CY", 15, 3, "voutn", "vbnc", "y"),
                  "CXC": ("CXC", 15, 3, "vcmfb", "vbnc", "xc"), "CYC": ("CYC", 15, 3, "vdd", "vbnc", "yc")}
    lev = lev or {"x": (0, 1), "yc": (0, 2), "y": (1, 0), "xc": (2, 0)}
    side = side or {"x": "L0", "y": "L1", "xc": "R0", "yc": "R1"}
    dn = ("dummy", 2, 3, "vss", "vbnc", "vss")
    slot = ("slot", 1, 3, None, None, None)              # BNC's place in both rows, between two gate columns
    r1 = [dn, dev[m1[0]], dev[m1[1]], "C", slot, "C", dev[m1[2]], dev[m1[3]], dn]
    r2 = [dn, dev[m2[0]], dev[m2[1]], "C", slot, "C", dev[m2[2]], dev[m2[3]], dn]
    band = [b or "_%d" % k for k, b in enumerate(band)]
    g = two_rows(c, r1, r2, band, mid_cols=True)
    X, top, tr, d1, d2, colx = g["X"], g["top"], g["tr"], g["d1"], g["d2"], g["cols"]
    bnc = c.mos("BNC", 1, 8, g["gaps"][0][1], g5((top - 8.68) / 2), "vbnc", "vbnc", "vss")
    for gr in (d1[0]["gate"], d2[0]["gate"]):           # fill joined to BNC's gate only where they overlap in y
        y0, y1 = max(gr[0], bnc["gate"][0]), min(gr[1], bnc["gate"][1])
        c.box("GatPoly", bnc["x0"] - 0.25, y0, bnc["x0"] - 0.10, y1)
        c.box("GatPoly", bnc["x1"] + 0.10, y0, bnc["x1"] + 0.25, y1)
    # source levels: k = 0 nearest the row; (net, row-1 level, row-2 level), verticals left (x, y) / right
    v0 = {"L0": -COL - 0.13 - 0.22 - 0.29, "L1": -COL - 0.13 - 2 * 0.22 - 2 * 0.29}
    vx = {n: v0[s] if s[0] == "L" else X - v0["L" + s[1]] - 0.29 for n, s in side.items()}
    ylo = lambda k: g5(-TM - TP * k)
    yhi = lambda k: g5(top + TM + TP * k)
    ends, spare = {}, []
    for row, devs, seqr in ((1, d1, r1), (2, d2, r2)):
        live = [it for it in seqr if it not in ("C", slot)]
        for k, (dv, it) in enumerate(zip(devs, live)):
            lab, w, l, d, gn, s = it
            inner, outer = ("top", "bot") if row == 1 else ("bot", "top")
            if lab == "dummy":
                if 0 < k < len(devs) - 1:                # C4: a spare 15/3 slot, the sinks' T (plated after the ring)
                    c.box("M1", dv["xc"] - 0.145, dv["bot"][0], dv["xc"] + 0.145, dv["top"][1])
                    spare.append((dv, outer))
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
    both = [n for n, (k1, k2) in lev.items() if k2 is not None]
    om = max([-vx[n] if vx[n] < 0 else vx[n] + 0.29 - X for n in both] + [COL + 0.13])
    xa, xb, xc_, xd = ring_x(X, om)
    nl = max(k for kk in lev.values() for k in kk if k is not None)
    ya = g5(ylo(nl) - 0.145 - 0.22 + 0.02 - TIEW)
    c.ring(xa, ya, xd, g5(top - ya))
    # dummies: outer stripe plated into the ring, inner stripe by a lane; BNC: drain to the left middle column,
    # source down to the ring
    for row, devs in ((1, d1), (2, d2)):
        inner, outer = ("top", "bot") if row == 1 else ("bot", "top")
        for k in (0, len(devs) - 1):
            c.plate(devs[k], outer)
            c.lane(devs[k], inner, k == 0)
    for dv, outer in spare:
        c.plate(dv, outer)
    c.bridge(bnc, "top", colx[2])
    c.box("M1", bnc["xc"] - 0.3, c.rg[1], bnc["xc"] + 0.3, bnc["bot"][1])
    # verticals and source levels
    for s, (k1, k2) in lev.items():
        xv = vx[s]
        y1, y2 = ylo(k1), (yhi(k2) if k2 is not None else None)
        vl, vr = [], []
        if y2 is not None:
            c.box("M1", xv, y1 - 0.145, xv + 0.29, y2 + 0.145)
            c.via(xv + 0.145, y1)
            c.via(xv + 0.145, y2)
            vl, vr = [xv + 0.41], [xv - 0.12]
        for row, y in ((1, y1), (2, y2)):
            if y is None:
                continue
            xs = ends[(s, row)]                          # tab ends: 3 Via1 at +-0.41, M2_c1 0.05
            a, b = min(xs + vl) - 0.555, max(xs + vr) + 0.555
            if row == 1:                                 # the bottom levels run on to the pin edge
                a, b = (xa - 0.27, b) if xv < 0 else (a, xd + 0.27)
            c.track(a, b, y)
        if xv < 0:
            c.pin("M2", s, xa - 0.27, y1 - 0.145, xa + 0.23, y1 + 0.145)
        else:
            c.pin("M2", s, xd - 0.23, y1 - 0.145, xd + 0.27, y1 + 0.145)
    if tie:                                              # C4: the dummy tracks' tie (M1 at R0, free: assert)
        assert "R0" not in [side[n] for n in both]
        xr = X - v0["L0"] - 0.29 + 0.145
        ts = [t for n, t in tr.items() if n.startswith("_")] + [tr[tie]]
        c.box("M1", xr - 0.145, min(ts) - 0.145, xr + 0.145, max(ts) + 0.145)
        c.track(X + COL + 0.145, xr + 0.145, tr[tie])
        c.via(xr, tr[tie])
    for n, t in tr.items():
        if n.startswith("_"):                            # C4: an empty place in the band, or a dummy track
            if tie:
                c.track(xa - 0.27, xr + 0.145, t)
                c.via(xr, t)
            continue
        c.track(xa - 0.27, X + COL + 0.145, t)
        c.pin("M2", n, xa - 0.27, t - 0.145, xa + 0.23, t + 0.145)
    for xc in colx:
        c.via(xc, tr["vbnc"])
    c.pin("M1", "vss", xa + 0.02, ya + 0.02, xa + 0.52, ya + 0.28)
    c.tgo()
    nm = lambda m: " ".join(dev[k][0] for k in m[:2]) + " [BNC] " + " ".join(dev[k][0] for k in m[2:])
    c.info = "rows: D | %s | D  /  D | %s | D; ring" % (nm(m1), nm(m2))
    return c


# ======================================================================================================
# Output ties TPN / TNN and the load capacitors CLP / CLN
# ======================================================================================================
def pd_pair(c, x0, ys, devs=(("TPN", "voutp"), ("TNN", "voutn")), mid="vcm"):
    """TPN (voutp - vcm) and TNN (voutn - vcm), 1/0.45 each, gate en_3v3_b: two PCells in their own orientation
    (L along x) at 0.83 pitch sharing the vcm stripe (Christoph's compaction of bias_tree_sw, log 2026-10-27
    17:30); the gates joined by one poly cap above the Activ, contacted 0.18 above it (17:43; Cnt_e 0.14, M1_b
    0.18 to the stripes), cap 0.55 above the Activ so no poly piece beyond the endcap zone is narrower than 0.30;
    M1 bar 0.21 (Via1-ready, V1_c 0.01); vcm pad 0.21 x 0.29 on the middle stripe (Via1-ready).
    C4: devs (label, outer stripe net) and the shared stripe's net mid are arguments (defaults: C3's). With mid on
    vss the bar is split into two 0.25 x 0.425 pads around the shared stripe (M1_b 0.18, M1_d 0.09), so the stripe
    reaches the ring in M1 (cload); the poly cap still joins both gates."""
    dev = pya.Layout.create_cell(ly, "nmosHV", "SG13_dev", {"w": "1u", "l": "0.45u", "ng": "1"})
    for k, (lab, d) in enumerate(devs):
        c.c.insert(pya.DCellInstArray(dev.cell_index(), pya.DTrans(pya.DVector(g5(x0 + 0.83 * k), g5(ys)))))
        c.cdl.append("M%s_%d %s en_3v3_b %s vss sg13_hv_nmos w=1u l=0.45u ng=1 m=1" % (lab, len(c.cdl), d, mid))
        c.note(lab, x0 + 0.565 + 0.83 * k, ys - 0.3)
    c.box("GatPoly", x0 + 0.34, ys + 1.10, x0 + 1.62, ys + 1.55)
    for xq in (0.485, 1.315):
        c.cont(x0 + xq, ys + 1.18)
    if mid == "vss":                                    # C4
        for a, b in ((0.27, 0.695), (1.265, 1.69)):
            c.box("M1", x0 + a, ys + 1.18, x0 + b, ys + 1.43)
    else:
        c.box("M1", x0 + 0.27, ys + 1.18, x0 + 1.69, ys + 1.39)
    c.box("M1", x0 + 0.875, ys + 0.355, x0 + 1.085, ys + 0.645)
    return dict(p=(x0 + 0.07, x0 + 0.23), m=x0 + 0.98, n=(x0 + 1.73, x0 + 1.89), ys=ys, bar=ys + 1.285,
                en=x0 + 0.42)


def cload(name, nets=("voutp", "voutn"), labs=("CLP", "CLN"), pd=(("TPN", "voutp"), ("TNN", "voutn")), mid="vcm"):
    """CLP (gate voutp) and CLN (gate voutn), hv NMOS 12 x 12, S / D / B on vss, mirror images; gate contact
    columns on their inner sides (fill as tall as the gate), the output ties TPN / TNN between them (the drains
    join the columns directly); closed p+ ring, S / D plates into its top and bottom legs. Pins: voutp, en_3v3_b,
    vcm, voutn on M2 at the top edge.
    C4: the capacitors' gate nets, labels, the pair and its shared stripe's net are arguments (defaults: C3's).
    A shared stripe on vss runs up in M1 between the split gate bar into the ring's top leg (no vss on M2)."""
    c = Cell(name)
    a = c.mos(labs[0], 12, 12, 0, 0, "vss", nets[0], "vss")
    xs = 12.80                                           # tie pair: its Activ + 0.25 leaves 0.30 of the fill
    X = g5(2 * (xs + 0.98))
    b = c.mos(labs[1], 12, 12, X - 12, 0, "vss", nets[1], "vss", mx=True)
    H = 12.68
    c.ring(-0.73, -0.51, X + 0.73, H + 0.51)             # side legs: pSD_j1 0.40 from the gates over Activ
    for dv in (a, b):
        c.plate(dv, "bot")
        c.plate(dv, "top")
    ys = g5(H + 0.21 - 0.25 - 0.30 - 1.25)               # 0.30 of its cap outside the Activ + 0.25 zones
    p = pd_pair(c, xs, ys, pd, mid)
    yt = H + 0.51 + 0.03                                 # top edge (ring pSD)
    for xc, fill, pn, sx in ((12.33, (12.10, 12.60), nets[0], p["p"][1]), (X - 12.33, (X - 12.60, X - 12.10),
                                                                           nets[1], p["n"][0])):
        c.gate_col(xc, [a["gate"]], 0.36, 12.32, fill)
        c.box("M1", min(xc, sx), ys, max(xc, sx), ys + 1.0)          # tie drain to its column
        c.via(xc, 12.1)
        c.box("M2", xc - 0.145, 11.955, xc + 0.145, yt)
        c.pin("M2", pn, xc - 0.145, yt - 0.4, xc + 0.145, yt)
    for xc, yv, pn in ((p["m"], ys + 0.5, mid), (p["en"], p["bar"], "en_3v3_b")):
        if pn == "vss":                                  # C4: shared source on the rail: M1 up into the ring
            c.box("M1", xc - 0.105, ys + 0.355, xc + 0.105, c.rg[3])
            continue
        c.via(xc, yv)
        c.box("M2", xc - 0.145, yv - 0.145, xc + 0.145, yt)
        c.pin("M2", pn, xc - 0.145, yt - 0.4, xc + 0.145, yt)
    c.pin("M1", "vss", -0.71, -0.49, -0.21, -0.23)
    c.tgo()
    c.info = "%s [%s | %s %s %s | %s] %s; ring" % (labs[0], nets[0], pd[0][0], mid, pd[1][0], nets[1], labs[1])
    return c


# ======================================================================================================
# Bias tree without the class-AB branch: NBPC NBP NI D, switches TGN / TDN at the row ends
# ======================================================================================================
PAD_TREE = [("NBPC", 2.4, 6, "vbpc", "ni", "vss"), ("NBP", 6, 6, "vbp", "ni", "vss"), ("NI", 6, 6, "ni", "ni", "vss"),
            ("dummy", 2.4, 6, "vss", "ni", "vss")]


def bias_tree(name, seq=PAD_TREE):
    """NBPC (2.4/6) at one end and its twin D (2.4/6 dummy, D = S = vss) at the other, NBP and NI (6/6) between,
    gate ni; the row is mirror-symmetric with nothing on its axis. TGN (iref - ni, gate en_3v3) left and TDN
    (ni - vss, gate en_3v3_b) right of the row's gate columns, mirror images, each with its own column; ni track
    (M2) above the row joins NI's drain and both columns; closed p+ ring.
    C4: the row's device list is an argument (default: C3's). Per device by its drain: ni -> NI's 3-via tab onto
    the ni track; vss -> the dummy's tab into the top leg; a net drained by two devices -> 0.29 M1 risers joined by
    an M1 bar one track pitch above the Via1 landing, one Via1 + M2 to the top edge; any other net -> C3's riser
    and M2 to the top edge."""
    c = Cell(name)
    X = row_len(seq)
    devs, _ = place_row(c, seq, 0.0, X / 2)
    H = 6.68
    tn = g5(H + 0.38)                                    # ni track
    yl = g5(tn + TP)                                     # Via1 landing of the drains going to the top edge
    drs = [it[3] for it in seq]
    two = sorted({d for d in drs if d not in ("ni", "vss") and drs.count(d) > 1})       # C4
    yj = g5(yl + TP) if two else yl                      # C4: join bar of the nets in 'two'
    ys = g5(H / 2 - 0.565)                               # switches: gate centered on the row's gate
    tg = c.mos("TGN", 1, 0.45, -1.96, ys, "iref", "en_3v3", "ni")
    td = c.mos("TDN", 1, 0.45, X + 0.96, ys, "ni", "en_3v3_b", "vss", mx=True)
    xa = -3.06                                           # ring: 0.30 of TGN's column fill outside Activ + 0.25
    yt = g5(yj + 0.145 + RS - 0.02 + TIEW)
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
    rise = []
    for dv, it in zip(devs, seq):
        d = it[3]
        if d == "ni":                                                        # NI: diode
            c.tab(dv["xc"], dv["top"][0], tn + 0.145, tn)
        elif d == "vss":                                                     # D: drain into the top leg
            c.box("M1", dv["xc"] - TAB / 2, dv["top"][0], dv["xc"] + TAB / 2, c.rg[3])
        elif d in two:                                                       # C4: riser to the join bar
            c.box("M1", dv["xc"] - 0.145, dv["top"][0], dv["xc"] + 0.145, yj + 0.145)
        else:
            rise.append((dv, d))
    for n in two:                                                            # C4: join bar, one Via1 + M2 pin
        xj = [dv["xc"] for dv, it in zip(devs, seq) if it[3] == n]
        c.box("M1", min(xj) - 0.145, yj - 0.145, max(xj) + 0.145, yj + 0.145)
        c.via(xj[-1], yj)
        c.box("M2", xj[-1] - 0.145, yj - 0.145, xj[-1] + 0.145, top)
        c.pin("M2", n, xj[-1] - 0.145, top - 0.4, xj[-1] + 0.145, top)
    for dv, n in rise + [(tg, "iref")]:
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
    c.info = "row: [TGN] | %s | [TDN]; ring" % " ".join(it[0] if it[0] != "dummy" else "D" for it in seq)
    return c


# ======================================================================================================
# C4, new: bypass_rb, the pad cload's capacitor arrayed
# ======================================================================================================
def bypass(name, ncm=4, ncr=8, rows=3, cols=4):
    """ncm capacitors on vcm and ncr on vref, each the pad's load capacitor (s2d_cload_c3's CLP: hv NMOS 12 x 12
    turned as there, S / D / B on vss, gate contacted over its full height by a column on one side), in rows x
    cols, filled column by column from the top left, vcm first (a column holding both nets has vcm on top; places
    beyond ncm + ncr stay empty). Columns in mirrored pairs facing their gate columns, as CLP | col .. col | CLN in
    the pad, without the tie pair between them: the fills Gat.b 0.18 apart; pairs 0.54 apart (endcaps Gat.c 0.18
    + Gat.b 0.18); rows Act.b 0.21 apart. S / D: top and bottom stripes plated into the ring as in the pad; the
    stripes of facing rows on one M1 vss bus into the ring's side legs (no tie between rows), M1.b 0.18 from the
    columns' ends. Gates: one Via1 per capacitor on its column as in the pad, M2 over the column; vcm runs up to an
    M2 bus on the top edge, vref down to one on the bottom edge (the fill order keeps them from crossing). Closed
    p+ ring 0.73 / 0.51 outside the Activ, as the pad's cload (pSD.j1 0.40 from the gates). LU.b (20 um, no tie
    inside) limits the shorter side to 3 capacitors (measured: 3 rows 19.44 um, 4 x 3 19.70 um, 4 x 4 25.78 um); an
    even cols keeps the array mirror-symmetric."""
    assert ncm >= 0 and ncr >= 0 and 0 < ncm + ncr <= rows * cols
    c = Cell(name)
    H = 12.68
    PY = g5(H + 0.21)
    xs, x = [], 0.0
    for j in range(cols):                                # (Activ x0, mirrored, column center, fill)
        if j % 2 == 0:
            xs.append((x, False, x + 12.33, (x + 12.10, x + 12.60)))
        else:
            xs.append((x + 13.38, True, x + 13.05, (x + 12.78, x + 13.28)))
            x = g5(x + 25.38 + 0.54)
    xr = max(xs[-1][0] + 12, xs[-1][3][1]) + 0.73
    yr = (rows - 1) * PY + H + 0.51
    c.ring(-0.73, -0.51, xr, yr)
    yt, yb0 = yr + 0.03, -0.54                           # top / bottom edge (ring pSD)
    seg = {}
    for j, (x0, mx, xc, fill) in enumerate(xs):
        for i in range(rows):
            k = j * rows + i
            if k >= ncm + ncr:
                continue
            net, lab = ("vcm", "CBM") if k < ncm else ("vref", "CBR")
            yb = g5((rows - 1 - i) * PY)
            dv = c.mos(lab, 12, 12, x0, yb, "vss", net, "vss", mx=mx)
            c.gate_col(xc, [dv["gate"]], yb + 0.36, yb + 12.32, fill)
            yv = yb + 12.1 if net == "vcm" else yb + H - 12.1
            c.via(xc, yv)
            seg.setdefault((xc, net), []).append(yv)
            if i == 0:
                c.plate(dv, "top")
            if i == rows - 1:
                c.plate(dv, "bot")
    for r in range(rows - 1):                            # vss bus between row r and row r + 1 (from the bottom)
        c.box("M1", -0.71, r * PY + 12.50, xr - 0.02, r * PY + PY + 0.36 - 0.18)
    for net, yedge in (("vcm", yt), ("vref", yb0)):
        xn = sorted(xc for xc, n in seg if n == net)
        if not xn:
            continue
        for xc in xn:
            yv = seg[(xc, net)]
            c.box("M2", xc - 0.145, min(yv) - 0.145 if net == "vcm" else yedge,
                  xc + 0.145, yedge if net == "vcm" else max(yv) + 0.145)
        y0 = yedge - 0.29 if net == "vcm" else yedge
        c.box("M2", xn[0] - 0.145, y0, xn[-1] + 0.145, y0 + 0.29)
        c.pin("M2", net, xn[0] - 0.145, y0, min(xn[0] + 0.355, xn[-1] + 0.145), y0 + 0.29)
    c.pin("M1", "vss", -0.71, -0.49, -0.21, -0.23)
    c.tgo()
    c.info = "%d x CBM (vcm) + %d x CBR (vref), %d rows x %d columns, columns in facing pairs; ring" % (
        ncm, ncr, rows, cols)
    return c


# ======================================================================================================
# The cells
# ======================================================================================================
RB_TREE = [("SH2", 2.4, 6, "gh", "ni", "vss"), ("SF", 2, 6, "vref", "ni", "vss"), ("NBP", 2.4, 6, "vbp", "ni", "vss"),
           ("SY", 6, 6, "xp", "ni", "vss"), ("NI", 6, 6, "ni", "ni", "vss"), ("SH1", 2.4, 6, "gh", "ni", "vss"),
           ("dummy", 2, 6, "vss", "ni", "vss"), ("dummy", 2.4, 6, "vss", "ni", "vss")]
RB_CASC = dict(dev={"CY": ("CY", 15, 3, "vdd", "vbnc", "xp"), "F1": ("F1", 15, 3, "vdd", "vbnc", "vref"),
                    "F2": ("F2", 15, 3, "vdd", "vbnc", "vref"), "F3": ("F3", 15, 3, "vdd", "vbnc", "vref"),
                    "F4": ("F4", 15, 3, "vdd", "vbnc", "vref"), "X": ("dummy", 15, 3, "vss", "vbnc", "vss")},
               m1=("F1", "F2", "CY", "X"), m2=("X", "X", "F3", "F4"), band=(None, None, "vbnc", None, "vdd"),
               lev={"vref": (0, 0), "xp": (0, None)}, side={"vref": "L0", "xp": "R0"}, tie="vdd")
RB_MIRROR = dict(m1=["BD", "BM"], m2=None, band=["vcm", "bd"], gn="bd",
                 f={"BD": ("BD", 6, 6, "bd", "bd", "vss"), "BM": ("BM", 6, 6, "vcm", "bd", "vss")})
RB_CLOAD = dict(nets=("vcm", "vref"), labs=("CB", "CBR"), pd=(("SPDC", "vcm"), ("SPDR", "vref")), mid="vss")


def name_dummies(cell, names):
    """C4: the dummies' CDL names for backannotation, MD + row + position, in drawing order."""
    it = iter(names)
    cell.cdl = ["M%s %s" % (next(it), ln.split(" ", 1)[1]) if ln.startswith("Mdummy_") else ln for ln in cell.cdl]
    assert next(it, None) is None
    return cell


def write(cells, stem, title):
    opt = pya.SaveLayoutOptions()
    opt.gds2_write_timestamps = False
    ly.write(stem + ".gds", opt)
    with open(stem + ".cdl", "w") as f:
        f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
                "* %s.cdl: reference netlists of %s.gds (%s).\n"
                "* One line per finger as drawn, every dummy a device; bulk = vss (substrate).\n" % (stem, stem, title))
        for k in cells:
            nets = sorted({p[0] for p in k.pins})
            f.write("\n.SUBCKT %s %s\n%s\n.ENDS %s\n" % (k.name, " ".join(nets), "\n".join(k.cdl), k.name))
    for k in cells:
        b = k.c.dbbox()
        print("%-24s %6.2f x %6.2f um  %7.1f um2  %s" % (k.name, b.width(), b.height(), b.width() * b.height(), k.info))
        for n, m, x, y in sorted(k.pins):
            print("    pin %-9s %s (%.3f, %.3f)" % (n, m, x, y))


if "--pad" in sys.argv:                                  # regression: the pad's rows, C3's names and device lists
    write([bias_tree("bias_tree_noab_n_c3"), casc_n("s2d_casc_n_c3"), sinks("sinks_6x6_s2d_c3_core"),
           cload("s2d_cload_c3")], "pad_regress", "the S2D pad's rows rebuilt by build_rb_n.py --pad")
elif "--bypass" in sys.argv:
    p = [int(v) for v in sys.argv[sys.argv.index("--bypass") + 1:][:4]]
    stem = "bypass_rb_%d_%d_%dx%d" % tuple(p)
    write([bypass(stem, *p)], stem, "build_rb_n.py --bypass %d %d %d %d" % tuple(p))
else:
    cells = [name_dummies(bias_tree("rb_tree_n", RB_TREE), ["DTN6", "DTN7"]),
             name_dummies(casc_n("rb_casc", **RB_CASC), ["DC10", "DC14", "DC15", "DC20", "DC21", "DC22", "DC25"]),
             name_dummies(sink_block("rb_mirror", **RB_MIRROR), ["DM0", "DM3"]),
             cload("rb_cload", **RB_CLOAD), bypass("bypass_rb")]
    topc, x = ly.create_cell("rb_n_cells"), 0.0
    for k in cells:                                      # side by side, 5 um apart, bottom edges aligned
        b = k.c.dbbox()
        topc.insert(pya.DCellInstArray(k.c.cell_index(), pya.DTrans(pya.DVector(g5(x - b.left), g5(-b.bottom)))))
        topc.shapes(LI["TEXT"]).insert(pya.DText(k.name, g5(x), -2.0))
        x += b.width() + 5.0
    write(cells, "rb_n_cells", "build_rb_n.py, agent N, C4 2026-11-07")
