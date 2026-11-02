# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_d2s_p.py: compact PMOS cells of d2s_mpdda_pd (IHP sg13cmos5l), C2 2026-10-31, agent P.

    python3 build_d2s_p.py [out_dir]        (reads ../inputs/pad_buffer_klayout/pad_buffer_cells.gds)

Device cells: the library's PCell copies (pmosHV, $14 = 10/1, $1 = 5/6, $2 = 6/4, $15 = 2/4, $3 = 15/3, $4 = 1/4,
$5 = 6.66/0.6, $7 = 1/0.45), plus the narrow 0.3/6 tail dummy from A4's adapter pmos_hv() (XOR 0 against the PCell).
Everything else is drawn here from rule values of sg13cmos5l_tech_default.json (names in comments).
Writes d2s_p_cells.gds and d2s_p_cells.cdl; pin table -> pins.txt.
"""
import os, sys, importlib.util
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("PDK_DRC_DECKS", "/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/")
_sp = importlib.util.spec_from_file_location("adapter", os.path.join(HERE, "..", "inputs", "A4", "out", "skill",
                                                                    "ihp_sg13cmos5l", "adapter.py"))
AD = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(AD)
R = AD.rule                                       # R("m1_space") = json M1_b ...

LIB = os.path.join(HERE, "..", "inputs", "pad_buffer_klayout", "pad_buffer_cells.gds")
LAY = dict(act=(1, 0), poly=(5, 0), cont=(6, 0), m1=(8, 0), m1p=(8, 2), m1t=(8, 25), m2=(10, 0), m2p=(10, 2),
           m2t=(10, 25), psd=(14, 0), v1=(19, 0), nw=(31, 0), tgo=(44, 0))
DEV = {"p10x1x2": "pmosHV", "p10x1": "pmosHV$14", "p5x6": "pmosHV$1", "p6x4": "pmosHV$2", "p2x4": "pmosHV$15",
       "p15x3": "pmosHV$3", "p1x4": "pmosHV$4", "p6p66x0p6": "pmosHV$5", "p1x0p45": "pmosHV$7"}

ly = db.Layout()
ly.dbu = 0.001
lib = db.Layout()
lib.read(LIB)
_copied = {}
N = lambda v: int(round(v * 1000))


def L(k):
    return ly.layer(*LAY[k])


def devcell(key):
    """library PCell copy (or the adapter's drawing for the 0.3/6 dummy)"""
    if key not in _copied:
        if key == "p0p3x6":
            c = AD.pmos_hv(ly, 0.3, 6.0, "pmosHV_w0p3_l6")
        else:
            s = lib.cell(DEV[key])
            c = ly.create_cell(DEV[key])
            for li in lib.layer_indexes():
                i = lib.get_info(li)
                c.shapes(ly.layer(i.layer, i.datatype)).insert(s.shapes(li))
        _copied[key] = c
    return _copied[key]


def act_len(l):
    return 2 * (R("diff_encl_contact") + R("contact_size") + R("diff_contact_to_gate")) + l


class Cell:
    def __init__(self, name):
        self.c = ly.create_cell(name)
        self.name = name
        self.pins = []                      # (name, layer, x1, y1, x2, y2)
        self.devs = []                      # CDL lines

    def box(self, k, x1, y1, x2, y2):
        self.c.shapes(L(k)).insert(db.Box(N(x1), N(y1), N(x2), N(y2)))

    def dev(self, key, x, y, rot=0, mirror=False):
        """place a device; (x, y) = lower-left of its Activ in the final frame (before the cell is moved to 0,0).
        rot 0: L along x, W along y (S left); 270: L along y, W along x, S on top; 90: W along x, S at the bottom."""
        d = devcell(key)
        b = d.bbox()
        wl = {"p10x1x2": (10, 3.06), "p10x1": (10, 1.68), "p5x6": (5, 6.68), "p6x4": (6, 4.68), "p2x4": (2, 4.68),
              "p15x3": (15, 3.68), "p1x4": (1, 4.68), "p6p66x0p6": (6.66, 1.28), "p1x0p45": (1, 1.13),
              "p0p3x6": (0.3, 6.68)}[key]
        W, A = wl
        if rot == 0:
            t = db.Trans(db.Trans.M0 if mirror else db.Trans.R0, N(x + (A if mirror else 0)), N(y))
        elif rot == 270:
            t = db.Trans(db.Trans.R270, N(x), N(y + A))
        elif rot == 90:
            t = db.Trans(db.Trans.R90, N(x + W), N(y))
        else:
            raise ValueError(rot)
        self.c.insert(db.CellInstArray(d.cell_index(), t))

    def pin(self, k, x1, y1, x2, y2, name):
        """pin box (<metal>p) and text (<metal>t) at its centre; the shape itself must be drawn by the caller"""
        self.box(k + "p", x1, y1, x2, y2)
        t = db.Text(name, db.Trans(N((x1 + x2) / 2), N((y1 + y2) / 2)))
        t.size = 100
        self.c.shapes(L(k + "t")).insert(t)
        self.pins.append((name, k, x1, y1, x2, y2))

    def finish(self, textbox=None):
        """move the cell so the bounding box of all shapes (no texts) has its lower-left at 0,0"""
        bb = db.Region()
        for k in LAY:
            if not k.endswith("t"):
                bb += db.Region(self.c.begin_shapes_rec(L(k)))
        b = bb.bbox()
        self.c.transform(db.Trans(-b.left, -b.bottom))
        self.off = (b.left / 1000, b.bottom / 1000)
        self.size = (b.width() / 1000, b.height() / 1000)
        self.pins = [(n, k, x1 - self.off[0], y1 - self.off[1], x2 - self.off[0], y2 - self.off[1])
                     for (n, k, x1, y1, x2, y2) in self.pins]


def ntie(cell, x1, y1, x2, y2, net=None, pitch=0.36):
    """N+ tie strip (Activ, one contact row or column, Metal1 over it); returns nothing, caller connects the Metal1.
    Activ >= 0.30 wide (Cnt_a + 2 Cnt_c); contacts every `pitch` (Cnt_b 0.18 -> 0.34; 0.36 keeps Cnt_b1 0.20)."""
    cell.box("act", x1, y1, x2, y2)
    cs, ce = R("contact_size"), R("diff_encl_contact")
    if (x2 - x1) <= (y2 - y1):                      # vertical strip
        n = int((y2 - y1 - 2 * ce + R("contact_space") + 1e-6) // (cs + R("contact_space")))
        n = max(1, int((y2 - y1 - 2 * ce - cs) // pitch) + 1)
        y0 = y1 + (y2 - y1 - cs - (n - 1) * pitch) / 2
        for i in range(n):
            cell.box("cont", (x1 + x2) / 2 - cs / 2, y0 + i * pitch, (x1 + x2) / 2 + cs / 2, y0 + i * pitch + cs)
        return ((x1 + x2) / 2 - cs / 2, y0, (x1 + x2) / 2 + cs / 2, y0 + (n - 1) * pitch + cs)
    n = max(1, int((x2 - x1 - 2 * ce - cs) // pitch) + 1)
    x0 = x1 + (x2 - x1 - cs - (n - 1) * pitch) / 2
    for i in range(n):
        cell.box("cont", x0 + i * pitch, (y1 + y2) / 2 - cs / 2, x0 + i * pitch + cs, (y1 + y2) / 2 + cs / 2)
    return (x0, (y1 + y2) / 2 - cs / 2, x0 + (n - 1) * pitch + cs, (y1 + y2) / 2 + cs / 2)


def well(cell, x1, y1, x2, y2):
    cell.box("nw", x1, y1, x2, y2)
    cell.box("tgo", x1, y1, x2, y2)             # ThickGateOx = NWell box, as the pmosHV PCell draws it (NW_c1 > TGO_a)


def cdl(name, pins, devs, notes=()):
    out = ["* " + n for n in notes]
    out.append(".SUBCKT %s %s" % (name, " ".join(pins)))
    out += devs
    out.append(".ENDS %s\n" % name)
    return "\n".join(out)


def M(name, d, g, s, b, w, l, ng=1):
    return "M%s %s %s %s %s sg13_hv_pmos w=%gu l=%gu ng=%d m=1" % (name, d, g, s, b, w, l, ng)


CELLS = []        # (Cell, pin list in CDL order, devices)
VH, VE = R("via1_size") / 2, R("m1_endcap_via1")      # Via1 0.19 (V1_a), Metal1 / Metal2 endcap 0.05 (V1_c1, M2.c1)


def v1(cell, xc, yc, m1="y", m2="y"):
    """Via1 at (xc, yc) with its Metal1 pad (0.21 wide, 0.29 long along m1) and Metal2 pad (0.20 wide, 0.29 long along m2)"""
    cell.box("v1", xc - VH, yc - VH, xc + VH, yc + VH)
    e, w = VH + VE, VH + R("m1_encl_via1")
    cell.box("m1", xc - (w if m1 == "y" else e), yc - (e if m1 == "y" else w), xc + (w if m1 == "y" else e),
             yc + (e if m1 == "y" else w))
    w2 = R("m2_width") / 2
    cell.box("m2", xc - (w2 if m2 == "y" else e), yc - (e if m2 == "y" else w2), xc + (w2 if m2 == "y" else e),
             yc + (e if m2 == "y" else w2))


def pad(cell, k, xc, y1, y2, name, w=0.29):
    """pin pad of width w centred on xc between y1 and y2 (Metal1 or Metal2), as pin"""
    cell.box(k, xc - w / 2, y1, xc + w / 2, y2)
    cell.pin(k, xc - w / 2, y1, xc + w / 2, y2, name)


def d2s_pd_p():
    """SA (a, en_3v3, vddo) and SABP (vabp, en_3v3, vdd) side by side, own source columns; gates by one poly bridge;
    N+ tie on the vdd column at the top edge (bulk = vdd for both, see report)."""
    c = Cell("d2s_pd_p_c")
    c.dev("p1x0p45", 0, 0)
    c.dev("p1x0p45", 1.34, 0)
    cw = R("m1_width")
    # bottom pins: a, vddo (Metal1 columns of SA down to the edge)
    for xc, nm in ((0.15, "a"), (0.98, "vddo")):
        c.box("m1", xc - 0.08, -0.62, xc + 0.08, 0)
        pad(c, "m1", xc, -0.62, -0.33, nm)
    # gate: poly bridge over the field above the Activ (Gat_d 0.07), contact on a pad above SA, Metal1 up to the top edge
    c.box("poly", 0.34, 1.08, 2.13, 1.21)
    c.box("poly", 0.34, 1.08, 0.79, 1.45)
    c.box("cont", 0.485, 1.22, 0.645, 1.38)
    c.box("m1", 0.485, 1.17, 0.645, 2.35)
    pad(c, "m1", 0.565, 2.06, 2.35, "en_3v3")
    # SABP: vdd column (with the N+ tie on top, pSD ends at 1.40, pSD_d1 0.03) and vabp column up to the top edge
    c.box("m1", 1.41, 1.0, 1.57, 2.35)
    c.box("act", 1.34, 1.43, 1.79, 1.73)         # 0.45 x 0.30 = 0.135 >= Act_d 0.122
    c.box("cont", 1.41, 1.50, 1.57, 1.66)
    pad(c, "m1", 1.49, 2.06, 2.35, "vdd")
    c.box("m1", 2.24, 1.0, 2.40, 2.35)
    pad(c, "m1", 2.32, 2.06, 2.35, "vabp")
    well(c, -0.62, -0.62, 3.09, 2.35)
    devs = [M("SA", "a", "en_3v3", "vddo", "vdd", 1, 0.45), M("SABP", "vabp", "en_3v3", "vdd", "vdd", 1, 0.45)]
    CELLS.append((c, ["a", "en_3v3", "vabp", "vddo", "vdd"], devs,
                  ["SA bulk = vdd here (one NWell with the tie on vdd); the circuit has vddo"]))


def d2s_ab_p():
    """RP2 | FPL | ABP, one row, W (6.66) vertical, own Activ each; poly bridge over the top joins the gates (vabp);
    N+ tie strip on the left edge (vdd). Pins: bottom dabp (M1), a (M1), b (M2); top vabp, l2, l1 (M2); left vdd (M1)."""
    c = Cell("d2s_ab_p_c")
    W, A = 6.66, 1.28
    xr, xf, xa = 0.0, A + 0.21, 2 * (A + 0.21)
    for x in (xr, xf, xa):
        c.dev("p6p66x0p6", x, 0)
    # bottom: dabp (RP2 S) and a (ABP S) on Metal1 down to the edge, b (ABP D) Via1 + Metal2
    for xc, nm in ((xr + 0.15, "dabp"), (xa + 0.15, "a")):
        c.box("m1", xc - 0.08, -0.62, xc + 0.08, 0)
        pad(c, "m1", xc, -0.62, -0.33, nm)
    xb = xa + 1.13
    c.box("m1", xb - 0.08, -0.38, xb + 0.08, 0)
    v1(c, xb, -0.235)
    c.box("m2", xb - 0.1, -0.62, xb + 0.1, 0.15)                 # Mn_d: Metal2 area 0.144 -> 0.2 x >= 0.72
    c.pin("m2", xb - 0.1, -0.62, xb + 0.1, -0.22, "b")
    # top: gate bridge (Gat_d 0.07 above the Activ), contact on a pad above RP2's gate, Metal1 link to RP2's D column
    c.box("poly", 0.34, W + 0.08, xa + 0.94, W + 0.21)
    c.box("poly", 0.34, W + 0.08, 0.94, W + 0.45)
    c.box("cont", 0.56, W + 0.22, 0.72, W + 0.38)
    c.box("m1", 0.56, W + 0.17, 0.72, W + 0.43)
    c.box("m1", 0.56, W + 0.27, xr + 1.21, W + 0.43)
    ytop = W + 0.62
    for xc, nm in ((xr + 1.13, "vabp"), (xf + 0.15, "l2"), (xf + 1.13, "l1")):
        c.box("m1", xc - 0.08, W, xc + 0.08, W + 0.53)
        v1(c, xc, W + 0.405)
        c.box("m2", xc - 0.1, W - 0.2, xc + 0.1, ytop)
        c.pin("m2", xc - 0.1, ytop - 0.4, xc + 0.1, ytop, nm)
    # left edge: N+ tie strip (pSD ends 0.18 left of the Activ, pSD_d1 0.03), Metal1 stub to the edge = vdd pin
    ntie(c, -0.51, 0.0, -0.21, W)
    c.box("m1", -0.44, 0.0, -0.28, W)
    c.box("m1", -1.13, 3.0, -0.28, 3.16)
    pad(c, "m1", -0.985, 2.87, 3.16, "vdd")
    well(c, -1.13, -0.62, xa + A + 0.62, ytop)
    devs = [M("RP2", "vabp", "vabp", "dabp", "vdd", 6.66, 0.6), M("FPL", "l1", "vabp", "l2", "vdd", 6.66, 0.6),
            M("ABP", "b", "vabp", "a", "vdd", 6.66, 0.6)]
    CELLS.append((c, ["a", "b", "dabp", "l1", "l2", "vabp", "vdd"], devs, ["RP1 is in the clamp frame (not here)"]))


def d2s_casc_p():
    """upright: two groups of two stacked 15/3 fingers, [a | pr] and [pl | l2], one 30.25 tall Metal1 line per column;
    BPC + dummy (1/4) in a row above; gates by contacts at the top ends + one Metal1 bar (vbpc); N+ tie strip on the left."""
    c = Cell("d2s_casc_p_c")
    W, A, G = 15.0, 3.68, 0.25
    X1 = 1.13
    X2 = X1 + A + 0.21
    ytop = 2 * W + G                                            # 30.25 top of the upper Activ
    for x in (X1, X2):
        c.dev("p15x3", x, 0)
        c.dev("p15x3", x, W + G)
    cols = {"a": X1 + 0.15, "pr": X1 + 3.53, "pl": X2 + 0.15, "l2": X2 + 3.53}
    for nm, xc in cols.items():                                  # one line per column: bridge the 0.25 gap
        c.box("m1", xc - 0.08, W - 0.05, xc + 0.08, W + G + 0.05)
    # pins: a (Metal1, bottom), l2 (Metal2 bottom and top), pl / pr (Metal2 top)
    c.box("m1", cols["a"] - 0.08, -0.62, cols["a"] + 0.08, 0)
    pad(c, "m1", cols["a"], -0.62, -0.33, "a")
    xb = cols["l2"]
    c.box("m1", xb - 0.08, -0.38, xb + 0.08, 0)
    v1(c, xb, -0.235)
    c.box("m2", xb - 0.1, -0.62, xb + 0.1, 0.15)
    c.pin("m2", xb - 0.1, -0.62, xb + 0.1, -0.22, "l2")
    Ytop = 33.02
    for nm in ("pr", "pl", "l2"):
        xc = cols[nm]
        v1(c, xc, ytop - 0.4)
        c.box("m2", xc - 0.1, ytop - 0.55, xc + 0.1, Ytop)
        c.pin("m2", xc - 0.1, Ytop - 0.4, xc + 0.1, Ytop, nm)
    # gates: poly pad above each group (contacts 0.14 from the Activ, M1 bar 0.18 above the column tops)
    yb0 = ytop + 0.18
    for x in (X1, X2):
        xg = x + 1.84
        c.box("poly", x + 0.34, ytop, x + 3.34, ytop + 0.46)
        for dx in (-0.28, 0.12):
            c.box("cont", xg + dx, ytop + 0.23, xg + dx + 0.16, ytop + 0.39)
    c.box("m1", X1 + 1.84 - 0.28, yb0 + 0.0, 11.215 + 0.105, yb0 + 0.26)
    # BPC row (pSD gap 0.31 to the fingers' pSD) with the dummy on its left
    Yb = 31.4
    Xd, Xb = X1, X1 + 4.68 + 0.21
    c.dev("p1x4", Xd, Yb)
    c.dev("p1x4", Xb, Yb)
    c.box("m1", Xb + 4.45, yb0, Xb + 4.61, Yb + 0.37)         # BPC drain column down to the bar and up to the gate link
    c.box("poly", Xb + 0.34, Yb + 1.0, Xb + 4.34, Yb + 1.39)
    c.box("cont", Xb + 4.0, Yb + 1.16, Xb + 4.16, Yb + 1.32)
    c.box("m1", Xb + 4.0, Yb + 1.11, Xb + 4.61, Yb + 1.37)
    c.box("m1", Xb + 4.45, Yb, Xb + 4.61, Yb + 1.37)
    c.box("m1", Xd + 4.45, Yb + 0.3, Xb + 0.23, Yb + 0.7)     # dummy's right column to BPC's source column (both vdd)
    c.box("m1", Xd + 0.07, Yb, Xd + 0.23, Yb + 1.28)           # dummy: D = S = vdd, columns joined above the Activ
    c.box("m1", Xd + 4.45, Yb, Xd + 4.61, Yb + 1.28)
    c.box("m1", Xd + 0.07, Yb + 1.12, Xd + 4.61, Yb + 1.28)
    c.box("poly", Xd + 0.34, 30.92, Xd + 4.34, Yb)             # dummy gate: contact below, Metal1 down to the bar (vbpc)
    c.box("cont", Xd + 2.0, 31.05, Xd + 2.16, 31.21)
    c.box("m1", Xd + 2.0, yb0, Xd + 2.16, 31.26)
    # vbpc to the right edge: Via1 on the bar's end, Metal2 down the right margin to the pin (<= 3 um from the bottom)
    xv = 11.215
    v1(c, xv, yb0 + 0.13)
    c.box("m2", xv - 0.1, 0.5, xv + 0.1, yb0 + 0.13)
    c.pin("m2", xv - 0.1, 0.5, xv + 0.1, 0.9, "vbpc")
    # left edge: N+ tie strip over the full height, Metal1 column, vdd links to the dummy and a pin stub on the edge
    ntie(c, 0.62, 0.0, 0.92, Yb + 1.0)
    c.box("m1", 0.69, 0.0, 0.85, Yb + 1.0)
    c.box("m1", 0.85, Yb + 0.3, Xd + 0.23, Yb + 0.7)
    c.box("m1", 0.0, 15.0, 0.85, 15.16)
    pad(c, "m1", 0.145, 14.87, 15.16, "vdd")
    well(c, 0.0, -0.62, 11.32, Yb + 1.0 + 0.62)
    dev = [M("PCL1", "l2", "vbpc", "pl", "vdd", 15, 3), M("PCL2", "l2", "vbpc", "pl", "vdd", 15, 3),
           M("PCR1", "a", "vbpc", "pr", "vdd", 15, 3), M("PCR2", "a", "vbpc", "pr", "vdd", 15, 3),
           M("BPC", "vbpc", "vbpc", "vdd", "vdd", 1, 4), M("DUM", "vdd", "vbpc", "vdd", "vdd", 1, 4)]
    CELLS.append((c, ["a", "l2", "pl", "pr", "vbpc", "vdd"], dev, []))


def d2s_loads():
    """upright: two columns of 5 stacked fingers (6/4, dummies 2/4), col 1 d L R R L, col 2 L R R L d (point symmetric,
    reading col 1 then col 2 bottom to top = L R R L L R R L). One continuous poly gate per column (l2, contacts below),
    S column (vdd) left, D column right. Metal2 lanes pl / pr per column, joined by Metal1 bars below the cell's devices.
    N+ tie strip on the left edge."""
    c = Cell("d2s_loads_c")
    X1 = 1.13
    X2 = X1 + 4.68 + 0.21
    G = 0.25
    stack = {X1: [("d", 2), ("L", 6), ("R", 6), ("R", 6), ("L", 6)], X2: [("L", 6), ("R", 6), ("R", 6), ("L", 6), ("d", 2)]}
    ytop = 27.0
    devs, pieces = [], []
    for X, st in stack.items():
        y = 0.0
        for k, (t, w) in enumerate(st):
            c.dev("p2x4" if t == "d" else "p6x4", X, y)
            pieces.append((X, t, y, y + w))
            devs.append(M("%s%d" % (t, len(devs)), {"L": "pl", "R": "pr", "d": "vdd"}[t], "l2", "vdd", "vdd", w, 4))
            if k:
                for xo in (0.07, 4.45):
                    nt = st[k - 1][0]
                    if xo == 0.07 or nt == t:
                        c.box("m1", X + xo, y - G - 0.05, X + xo + 0.16, y + 0.05)     # bridge equal-net columns
            y += w + G
    # vdd: S columns (left), dummies' D = S links
    for X in (X1, X2):
        c.box("m1", X + 0.07, 0, X + 0.23, ytop + 0.36)
    for X, t, y0, y1 in pieces:
        if t == "d":
            c.box("m1", X + 0.07, (y0 + y1) / 2 - 0.08, X + 4.61, (y0 + y1) / 2 + 0.08)
    c.box("m1", 0.69, ytop + 0.2, X2 + 0.23, ytop + 0.36)
    ntie(c, 0.62, 0.0, 0.92, ytop)
    c.box("m1", 0.69, 0.0, 0.85, ytop + 0.36)
    c.box("m1", 0.0, 13.0, 0.85, 13.16)
    pad(c, "m1", 0.145, 12.87, 13.16, "vdd")
    # gates: contacts below the columns (outside pSD), Metal1 bar
    for X in (X1, X2):
        xg = X + 2.34
        c.box("poly", X + 0.34, -0.65, X + 4.34, 0.0)
        for dx in (-0.28, 0.12):
            c.box("cont", xg + dx, -0.58, xg + dx + 0.16, -0.42)
    c.box("m1", X1 + 2.34 - 0.28, -0.63, X2 + 2.34 + 0.28, -0.37)
    # drain lanes: pl / pr; col 1: pl on the D column, pr on a stub 0.41 left; col 2: pr on the D column, pl on the stub
    xd1, xd2 = X1 + 4.53, X2 + 4.53
    lane = {("L", X1): xd1, ("R", X1): xd1 - 0.41, ("L", X2): xd2 - 0.41, ("R", X2): xd2}
    ext = {}
    for X, t, y0, y1 in pieces:
        if t == "d":
            continue
        xl = lane[(t, X)]
        xd = X + 4.53
        ym = (y0 + y1) / 2
        if (t == "R"):
            ym = {X1: 14.6, X2: 12.4}[X]
            if y0 not in (8.5, 14.75, 6.25, 12.5) or (X == X1 and y0 == 14.75) or (X == X2 and y0 == 12.5):
                continue
        if xl != xd:
            c.box("m1", xl - 0.105, ym - 0.08, xd + 0.08, ym + 0.08)
        v1(c, xl, ym)
        ext.setdefault((t, X), []).append(ym)
    nets = {}
    for (t, X), ys in ext.items():
        nets.setdefault(t, []).append((lane[(t, X)], min(ys), max(ys)))
    ybar = {"L": -1.0, "R": -1.6}                         # Metal1 bars (pl above pr), pitch 0.60
    ybot = -2.4
    for t, nm in (("L", "pl"), ("R", "pr")):
        xs = sorted(n[0] for n in nets[t])
        for xl, y0, y1 in nets[t]:
            c.box("m2", xl - 0.1, ybar[t] - 0.145, xl + 0.1, y1 + 0.145)
            v1(c, xl, ybar[t])
        c.box("m1", xs[0] - 0.105, ybar[t] - 0.105, xs[1] + 0.105, ybar[t] + 0.105)
        xp = {"L": 7.3, "R": 8.3}[t]
        c.box("m1", xp - 0.145, ybar[t] - 0.105, xp + 0.145, ybar[t] + 0.105)
        v1(c, xp, ybar[t])
        c.box("m2", xp - 0.1, ybot, xp + 0.1, ybar[t] + 0.145)
        c.pin("m2", xp - 0.1, ybot, xp + 0.1, ybot + 0.4, nm)
    xp = 4.0                                              # l2: via on the gate bar, Metal2 down to the edge
    v1(c, xp, -0.5)
    c.box("m2", xp - 0.1, ybot, xp + 0.1, -0.5 + 0.145)
    c.pin("m2", xp - 0.1, ybot, xp + 0.1, ybot + 0.4, "l2")
    well(c, 0.0, ybot, X2 + 4.68 + 0.62, ytop + 0.62)
    CELLS.append((c, ["l2", "pl", "pr", "vdd"], devs, []))


X0, PITCH = 5.34, 6.1                    # tub column origins (d2s_inputs): tub k Activ starts at X0 + k PITCH
COLC = [X0 + PITCH * k + 1.53 for k in range(4)]      # column centres (tub centre line)
LANE = (+1.38, -1.38)                                   # M2 lane offsets from the column centre: top row, bottom row


def d2s_tails():
    """two rows of 5/6 tails on the tub column pitch: row 1 (top) S up (R270), row 2 (bottom) S down (R90), the point image.
    Narrow 0.3/6 dummies at the left ends, a full 5/6 dummy (row 1) and BP (row 2) at the right ends. One poly gate strip per
    row (vbp, contacts at the right end), source bars top and bottom (vdd) joined on the left with the N+ tie strip,
    Metal2 through-lanes per drain net from the top to the bottom edge."""
    c = Cell("d2s_tails_c")
    ya2, ya1, A = 0.62, 7.51, 6.68
    rows = [("1", ya1, 270, ["sa_A", "sb_C2", "sb_C1", "sa_B"], ["Aa", "C2b", "C1b", "Ba"]),
            ("2", ya2, 90, ["sb_B", "sa_C1", "sa_C2", "sb_A"], ["Bb", "C1a", "C2a", "Ab"])]
    xl = COLC[0] - 2.5 - 0.25 - 0.3
    xR = COLC[3] + 2.75 + 5.0                              # right end of the full end device
    devs = []
    for r, ya, rot, nets, names in rows:
        c.dev("p0p3x6", xl, ya, rot)
        devs.append(M("Td" + r, "vdd", "vbp", "vdd", "vdd", 0.3, 6))
        for k in range(4):
            c.dev("p5x6", COLC[k] - 2.5, ya, rot)
            devs.append(M("T" + names[k], nets[k], "vbp", "vdd", "vdd", 5, 6))
        c.dev("p5x6", COLC[3] + 2.75, ya, rot)
        devs.append(M("BP", "vbp", "vbp", "vdd", "vdd", 5, 6) if r == "2" else M("Td5", "vdd", "vbp", "vdd", "vdd", 5, 6))
        gy = (ya + 0.34, ya + 0.34 + 6) if rot == 90 else (ya + A - 0.34 - 6, ya + A - 0.34)
        c.box("poly", xl, gy[0], xR + 0.68, gy[1])                         # one gate strip per row
        c.box("psd", xl - 0.4, ya - 0.18, xR + 0.4, ya + A + 0.18)         # fills the 0.30 gaps between the fingers' pSD
        gm = (gy[0] + gy[1]) / 2
        for dy in (-0.34, 0, 0.34):
            c.box("cont", xR + 0.45, gm + dy - 0.08, xR + 0.61, gm + dy + 0.08)
        # drain stripes: D side is the middle (row 1 bottom, row 2 top)
        yd = 7.58 if rot == 270 else 7.07
        for k in range(4):
            xc = COLC[k] + LANE[0 if r == "1" else 1]
            v1(c, xc, yd + 0.08)
            c.box("m2", xc - 0.1, 0, xc + 0.1, 14.81)
            c.pin("m2", xc - 0.1, 0, xc + 0.1, 0.4, nets[k])
            c.pin("m2", xc - 0.1, 14.41, xc + 0.1, 14.81, nets[k])
        xt = xl - 0.73
        c.box("m1", xt + 0.07, yd, xl + 0.3, yd + 0.16)                   # dummy's D stripe to the vdd column
        ys = 13.96 if rot == 270 else 0.69                               # S bar (M1 over the S contact column)
        xe = xR if rot == 270 else xR
        c.box("m1", xt + 0.07, ys, xe, ys + 0.16)
    # vdd: tie strip + column on the left, tap pad bottom-left; row 1 end dummy D + S joined at the right
    xt = xl - 0.73
    ntie(c, xt, ya2, xt + 0.3, ya1 + A)
    c.box("m1", xt + 0.07, 0.3, xt + 0.23, 14.12)
    wl = xt - 0.62
    c.box("m1", wl, 0, xt + 0.23, 0.6)                                  # tap pad (0.6 x 0.6 at the corner, merged with the column)
    c.pin("m1", wl, 0, wl + 0.6, 0.6, "vdd")
    c.box("m1", xR - 0.05, 7.58, xR + 0.21, 14.12)
    # vbp: Metal1 bar over the gate contacts, BP's D stripe link, Via1 + Metal2 pin on the right edge (low)
    c.box("m1", xR + 0.45, 0.9, xR + 0.61, 13.0)
    c.box("m1", xR - 0.05, 7.07, xR + 0.61, 7.23)
    xv = xR + 0.61
    wr = xR + 1.82
    ntie(c, xR + 0.9, ya2, xR + 1.2, ya1 + A)                          # second N+ strip (LU.a: 31 um wide cell)
    c.box("m1", xR + 0.97, 0.62, xR + 1.13, 14.12)
    c.box("m1", xR - 0.05, 13.96, xR + 1.13, 14.12)
    c.box("v1", xv - VH, 1.4 - VH, xv + VH, 1.4 + VH)
    c.box("m1", xv - 0.105, 1.4 - 0.145, xv + 0.105, 1.4 + 0.145)
    c.box("m2", xv - 0.105, 0.9, xv + 0.105, 1.7)
    c.box("m2", xv - 0.105, 1.3, wr, 1.5)
    c.pin("m2", wr - 0.8, 1.3, wr, 1.5, "vbp")
    well(c, wl, 0, wr, 14.81)
    pl = [n for r in rows for n in r[3]]
    CELLS.append((c, sorted(pl) + ["vbp", "vdd"], devs, ["tail rows: row 1 Aa C2b C1b Ba, row 2 Bb C1a C2a Ab; BP at the right end of row 2"]))


def d2s_inputs():
    """4 x 2 tubs (each 2 x 10/1 in its own NWell, well = source via an N+ tie strip below the device) on the tail pitch,
    one narrow 10/1 dummy tub (all vdd) at each row end. Metal2 lanes: sources straight to the bottom edge (the top row's
    pass the lower tub), drains up / down to Metal1 tracks in the row gap (x, y, crossing by the order of the tracks) and on to
    the right edge; gates on Metal1 pads, vref / vfb / vinn / vinp on Metal2 to the top and left edges."""
    c = Cell("d2s_inputs_c")
    Ry = 13.77
    RIGHT, TOP = 32.05, 25.36
    tubs = [[("Aa", "vinp", "y", "sa_A"), ("C2b", "vfb", "x", "sb_C2"), ("C1b", "vfb", "x", "sb_C1"), ("Ba", "vref", "y", "sa_B")],
            [("Bb", "vinn", "x", "sb_B"), ("C1a", "vref", "y", "sa_C1"), ("C2a", "vref", "y", "sa_C2"), ("Ab", "vref", "x", "sb_A")]]
    ydev = [Ry, 0.0]
    devs, pins = [], []
    xdl, xdr = 0.62, 29.74                                      # dummy Activ left edges
    T = {1: 10.95, 2: 11.34, 3: 11.73, 4: 12.12}               # Metal1 track bottoms in the row gap (0.21 high)
    tc = lambda n: T[n] + 0.105
    trk = {("Aa", 0): 4, ("Ba", 0): 4, ("Bb", 1): 2, ("Ab", 1): 2, ("C2b", 0): 3, ("C1b", 0): 3, ("C1a", 1): 1, ("C2a", 1): 1}
    for r in (0, 1):
        y0 = ydev[r]
        for k in range(4):
            nm, g, d, sn = tubs[r][k]
            x0 = X0 + PITCH * k
            c.dev("p10x1x2", x0, y0)
            devs.append(M(nm, d, g, sn, sn, 20, 1, 2))
            well(c, x0 - 0.62, y0 - 1.35, x0 + 3.68, y0 + 10.62)
            # tie strip below the device, bar, source columns down to it
            c.box("act", x0, y0 - 0.73, x0 + 3.06, y0 - 0.43)
            for i in range(9):
                c.box("cont", x0 + 0.09 + 0.34 * i, y0 - 0.66, x0 + 0.25 + 0.34 * i, y0 - 0.50)
            c.box("m1", x0 + 0.04, y0 - 0.66, x0 + 3.02, y0 - 0.50)
            for xo in (0.07, 2.83):
                c.box("m1", x0 + xo, y0 - 0.66, x0 + xo + 0.16, y0)
            # gate: the library's strap over the tops of both gates
            c.box("poly", x0 + 0.59, y0 + 10.0, x0 + 1.09, y0 + 10.43)
            c.box("poly", x0 + 1.97, y0 + 10.0, x0 + 2.47, y0 + 10.43)
            c.box("poly", x0 + 0.34, y0 + 10.42, x0 + 2.72, y0 + 10.78)
            c.box("cont", x0 + 0.76, y0 + 10.52, x0 + 0.92, y0 + 10.68)
            c.box("cont", x0 + 2.14, y0 + 10.52, x0 + 2.30, y0 + 10.68)
            c.box("m1", x0 + 0.71, y0 + 10.47, x0 + 2.35, y0 + 10.73)
            # source lane (Metal2 to the bottom edge)
            xs = x0 + (2.91 if r == 0 else 0.15)
            v1(c, xs, y0 - 0.58)
            c.box("m2", xs - 0.1, -1.35, xs + 0.1, y0 - 0.58 + 0.145)
            c.pin("m2", xs - 0.1, -1.35, xs + 0.1, -0.95, sn)
            # drain lane to its track
            xd = x0 + 1.53
            yt = tc(trk[(nm, r)])
            if r == 1:
                v1(c, xd, y0 + 9.6)
                c.box("m2", xd - 0.1, y0 + 9.6 - 0.145, xd + 0.1, yt + 0.145)
            else:
                v1(c, xd, y0 + 0.4)
                c.box("m2", xd - 0.1, yt - 0.145, xd + 0.1, y0 + 0.4 + 0.145)
            v1(c, xd, yt, m1="x")
            ext = {"x": 31.835, "y": 31.0}[d] if False else None
    # tracks (Metal1, 0.21 high): x = T2 + T3 (joined), y = T4 + T1 (joined by the Metal2 pin line)
    cx = [X0 + PITCH * k + 1.53 for k in range(4)]
    def trkbox(n, xa, xb):
        c.box("m1", xa, T[n], xb, T[n] + 0.21)
    trkbox(4, cx[0] - 0.145, 31.0 + 0.105)
    trkbox(1, cx[1] - 0.145, 31.0 + 0.105)
    trkbox(2, cx[0] - 0.145, 31.945)
    trkbox(3, cx[1] - 0.145, 31.945)
    xj = X0 + PITCH + 4.6
    c.box("m1", xj, T[2], xj + 0.21, T[3] + 0.21)              # joins T2 / T3 (adjacent)
    c.box("m1", 31.84, T[2], 32.05, T[3] + 0.21)
    xm = 31.945
    c.box("v1", xm - VH, 11.64 - VH, xm + VH, 11.64 + VH)
    c.box("m2", xm - 0.1, 11.13, xm + 0.1, 11.85)
    c.pin("m2", xm - 0.1, 11.13, xm + 0.1, 11.85, "x")
    v1(c, 31.0, tc(4), m1="x")
    v1(c, 31.0, tc(1), m1="x")
    c.box("m2", 30.9, tc(1) - 0.145, 31.1, tc(4) + 0.145)
    c.box("m2", 31.0, tc(4) - 0.1, 32.05, tc(4) + 0.1)
    c.pin("m2", 31.65, tc(4) - 0.1, 32.05, tc(4) + 0.1, "y")
    # row-2 gate pads: vref bar over c1..c3, vinn pad at c0; row-1 pads: vinp at c0, vfb bar c1..c2, vref at c3
    x0s = [X0 + PITCH * k for k in range(4)]
    c.box("m1", x0s[1] + 0.71, 10.47, x0s[3] + 2.35, 10.73)
    c.box("m1", x0s[1] + 0.71, Ry + 10.47, x0s[2] + 2.35, Ry + 10.73)
    xv = x0s[3] + 0.85
    v1(c, xv, 10.6)
    v1(c, xv, Ry + 10.6)
    c.box("m2", xv - 0.1, 10.6 - 0.145, xv + 0.1, TOP)
    c.pin("m2", xv - 0.1, TOP - 0.4, xv + 0.1, TOP, "vref")
    xa = x0s[0] + 2.0
    v1(c, xa, Ry + 10.6)
    c.box("m2", xa - 0.1, Ry + 10.6 - 0.145, xa + 0.1, TOP)
    c.pin("m2", xa - 0.1, TOP - 0.4, xa + 0.1, TOP, "vinp")
    xn = x0s[0] + 0.85
    Tn, Tv = Ry + 10.97 + 0.0, 0
    ytv, ytn = Ry + 10.95 - 0.0, Ry + 11.34
    ytv, ytn = 24.72, 25.11                                     # Metal1 tracks above the row-1 pads (0.21 high)
    v1(c, xn, 10.6)
    v1(c, xn, ytn + 0.105, m1="x")
    c.box("m2", xn - 0.1, 10.6 - 0.145, xn + 0.1, ytn + 0.105 + 0.145)
    xp = 30.0
    c.box("m1", xn - 0.145, ytn, xp + 0.145, ytn + 0.21)
    v1(c, xp, ytn + 0.105, m1="x")
    c.box("m2", xp - 0.4, TOP - 0.2, xp + 0.4, TOP)
    c.box("m2", xp - 0.1, ytn + 0.105 - 0.145, xp + 0.1, TOP)
    c.pin("m2", xp - 0.4, TOP - 0.2, xp + 0.4, TOP, "vinn")
    xf = x0s[1] + 0.8
    c.box("m1", xf, Ry + 10.47, xf + 0.2, ytv + 0.21)
    c.box("m1", 0.2 - 0.105, ytv, xf + 0.2, ytv + 0.21)
    v1(c, 0.2, ytv + 0.105, m1="x")
    c.box("m2", 0.1, -0.8, 0.3, ytv + 0.105 + 0.145)
    c.box("m2", 0.0, -0.8, 0.3, -0.55)
    c.pin("m2", 0.0, -0.8, 0.3, -0.55, "vfb")
    # dummy tubs (all vdd): Metal1 columns joined top and bottom, vdd bar along the bottom edge, Metal2 down for row 1
    for xd in (xdl, xdr):
        for r in (0, 1):
            y0 = ydev[r]
            c.dev("p10x1", xd, y0)
            devs.append(M("Dm%d%d" % (r, int(xd > 10)), "vdd", "vdd", "vdd", "vdd", 10, 1))
            well(c, xd - 0.62, y0 - 1.35, xd + 2.30 + (0.01 if xd > 10 else 0), y0 + 10.62)
            c.box("act", xd, y0 - 0.73, xd + 1.68, y0 - 0.43)
            for i in range(4):
                c.box("cont", xd + 0.09 + 0.34 * i, y0 - 0.66, xd + 0.25 + 0.34 * i, y0 - 0.50)
            c.box("m1", xd + 0.04, y0 - 0.66, xd + 1.64, y0 - 0.50)
            c.box("m1", xd + 0.07, y0 - 0.66, xd + 0.23, y0 + 10.51)
            c.box("m1", xd + 1.45, y0, xd + 1.61, y0 + 10.51)
            c.box("m1", xd + 0.07, y0 + 10.25, xd + 1.61, y0 + 10.51)
            c.box("poly", xd + 0.34, y0 + 10.0, xd + 1.34, y0 + 10.62)
            c.box("cont", xd + 0.59, y0 + 10.30, xd + 0.75, y0 + 10.46)
            if r == 1:
                c.box("m1", xd + 0.07, -1.06, xd + 0.23, -0.66)
            else:
                xl_ = xd + 0.3
                v1(c, xl_, y0 - 0.58)
                v1(c, xl_, -1.2)
                c.box("m2", xl_ - 0.1, -1.2 - 0.145, xl_ + 0.1, y0 - 0.58 + 0.145)
    c.box("m1", xdl + 0.07, -1.35, xdr + 0.23, -1.06)
    c.pin("m1", xdl + 0.07, -1.35, xdl + 0.36, -1.06, "vdd")
    CELLS.append((c, ["vinp", "vref", "vinn", "vfb", "x", "y"] + sorted(set(t[3] for row in tubs for t in row)) + ["vdd"], devs,
                  ["tubs: ng = 2, w = 20u (2 x 10/1), bulk = source; dummies 10/1 ng=1 on vdd"]))


def main(out):
    d2s_pd_p()
    d2s_ab_p()
    d2s_casc_p()
    d2s_loads()
    d2s_tails()
    d2s_inputs()
    txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* d2s_p_cells.cdl: reference netlists of d2s_p_cells.gds (build_d2s_p.py, agent P, 2026-10-31).",
           "* Devices as drawn, dummies included (D = S for a dummy).", ""]
    pins = []
    for c, pl, devs, notes in CELLS:
        c.finish()
        txt.append(cdl(c.name, pl, devs, notes))
        pins.append("== %s  %.3f x %.3f um  (cell origin was %.3f, %.3f)" % (c.name, c.size[0], c.size[1], *c.off))
        for n, k, x1, y1, x2, y2 in c.pins:
            pins.append("  %-8s %s  x %.3f-%.3f  y %.3f-%.3f" % (n, k, x1, x2, y1, y2))
    for c in list(ly.each_cell()):
        pass
    o = db.SaveLayoutOptions()
    o.write_context_info = False
    o.gds2_write_timestamps = False
    ly.write(os.path.join(out, "d2s_p_cells.gds"), o)
    open(os.path.join(out, "d2s_p_cells.cdl"), "w").write("\n".join(txt))
    open(os.path.join(out, "pins.txt"), "w").write("\n".join(pins) + "\n")
    print("\n".join(pins))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE)
