# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_s2d_p3.py: PMOS layout primitives of s2d_mpdda_pd / bias_tree_noab_pd (IHP sg13cmos5l), C3, agent P,
2026-11-03, Claude. Built on C2's build_d2s_p2.py (agent P2): same helpers, same row / gate-column scheme.

    python3 build_s2d_p3.py        (needs the PDK: PDK_ROOT, default /foss/pdks; writes next to this file)

Writes s2d_p3_cells.gds (cells <name>_c3), s2d_p3_cells.cdl (reference netlists, every dummy a device) and the PNGs.

Layout rules (Christoph; brief P of C3):
- device layers mirror-symmetric: the right half of every row is the M90 image of its left half, the upper row the
  M0 image of the lower one (exact by construction, PCell grid rounding included);
- dummies only in pairs of the same device at both ends of a row; a bias diode at a row end has its twin at the other;
- gate contacts on full-width poly (tabs as long as the gate, or the gate heads), never through a narrowed link;
  two-row cells join the two rows' gate tabs by a poly bridge at both row ends (gates joined in poly, no M2);
- dummies: source and drain to the rail (vdd), gate by abutment;
- unmodified IHP SG13_dev pmosHV PCells (copied flat, unchanged); taps as closed rings at the periphery;
- no M2 unless the cell needs it (crossing a ring, joining across rows, edge pins of inner nets).
Rule values: sg13cmos5l_tech_default.json (keys in the comments), SG13CMOS5L_os_layout_rules.txt.
"""
import os
import sys

PDK = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "ihp-sg13cmos5l"))
sys.path += [PDK + "/libs.tech/klayout/python", PDK + "/libs.tech/klayout/python/pycell4klayout-api/source/python"]
import pya                                   # noqa: E402
import sg13cmos5l_pycell_lib                 # noqa: E402,F401  registers the PCell library SG13_dev

OUT = os.path.dirname(os.path.abspath(__file__))
ly = pya.Layout()
ly.dbu = 0.001
LAY = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25),
       "Via1": (19, 0), "M2": (10, 0), "M2pin": (10, 2), "M2txt": (10, 25), "pSD": (14, 0), "NWell": (31, 0),
       "TGO": (44, 0), "TEXT": (63, 0)}
LI = {k: ly.layer(*v) for k, v in LAY.items()}
CDL, PINS = {}, {}
TP = 0.48          # wide M2 track pitch: 0.26 track + Mn_b 0.21 (+0.01)
TN = 0.41          # narrow M2 track pitch: 0.20 track (V1_a 0.19 + 2 Mn_c 0.005) + Mn_b 0.21; vias V1_b 0.22 apart
TW = 0.13          # half width of a wide track
RG = 0.80          # end Activ to tie ring: poly tab 0.60, ring Activ 0.20 beyond it (Gat_d 0.07), pSD 0.40 inside


def g5(v):
    """5 nm drawing grid (geometry/3_1_offgrid.drc)"""
    return round(v / 0.005) * 0.005


def box(c, lay, x0, y0, x1, y1):
    c.shapes(LI[lay]).insert(pya.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


def fill(c, lay, x0, y0, x1, y1):
    """Cont (Cnt_a 0.16, pitch + Cnt_b 0.18) or Via1 (V1_a 0.19, pitch + V1_b 0.22), centered in the zone"""
    s, p = (0.16, 0.34) if lay == "Cont" else (0.19, 0.41)

    def pos(a, b):
        a, b = min(a, b), max(a, b)
        n = max(1, int((b - a - s) / p + 1e-6) + 1)
        return [g5((a + b) / 2 - ((n - 1) * p + s) / 2 + i * p) for i in range(n)]
    for x in pos(x0, x1):
        for y in pos(y0, y1):
            box(c, lay, x, y, x + s, y + s)


def pin(c, m, net, x0, y0, x1, y1):
    box(c, m + "pin", x0, y0, x1, y1)
    c.shapes(LI[m + "txt"]).insert(pya.DText(net, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))
    PINS.setdefault(c.name, []).append((net, m, pya.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)),
                                                         g5(max(y0, y1)))))


def note(c, text, b):
    c.shapes(LI["TEXT"]).insert(pya.DText(text, g5(b.center().x), g5(b.center().y)))


def tap(c, x0, y0, x1, y1, cut=None):
    """N+ tie in the NWell: Activ, one contact row / column (Cnt_c 0.07), Metal1; cut = contact zone if not all"""
    box(c, "Activ", x0, y0, x1, y1)
    box(c, "M1", x0, y0, x1, y1)
    fill(c, "Cont", *(cut or (min(x0, x1) + 0.07, min(y0, y1) + 0.07, max(x0, x1) - 0.07, max(y0, y1) - 0.07)))


def ring(c, x0, y0, x1, y1):
    """closed N+ tie ring, Activ / Metal1 0.30 wide (Cnt_a + 2 Cnt_c); x0..x1 inner, y0..y1 outer edges of the strips"""
    tap(c, x0 - 0.30, y0 + 0.30, x0, y1 - 0.30, (x0 - 0.23, y0 + 0.41, x0 - 0.07, y1 - 0.41))
    tap(c, x1, y0 + 0.30, x1 + 0.30, y1 - 0.30, (x1 + 0.07, y0 + 0.41, x1 + 0.23, y1 - 0.41))
    tap(c, x0 - 0.30, y0, x1 + 0.30, y0 + 0.30)
    tap(c, x0 - 0.30, y1 - 0.30, x1 + 0.30, y1)


def well(c, b):
    """one NWell and one ThickGateOx over the whole cell (NW_c1 / NW_e1 0.62 beyond all Activ, TGO_a 0.27)"""
    box(c, "NWell", b.left, b.bottom, b.right, b.top)
    box(c, "TGO", b.left, b.bottom, b.right, b.top)


# ---------------------------------------------------------------- devices: IHP PCells, copied flat and unchanged
_pcl = pya.Layout()
_pcl.technology_name = "sg13cmos5l"
DEV = {}


def mos(w, l, ng=1):
    """pmosHV, w = total width. Native: fingers upright (W along y), stripes left to right."""
    key = (w, l, ng)
    if key not in DEV:
        p = _pcl.create_cell("pmosHV", "SG13_dev", {"w": "%gu" % w, "l": "%gu" % l, "ng": str(ng)})
        d = ly.create_cell(("pmosHV_w%g_l%g" % (w, l) + ("_ng%d" % ng if ng > 1 else "")).replace(".", "p"))
        for li in _pcl.layer_indexes():
            i = _pcl.get_info(li)
            d.shapes(ly.layer(i.layer, i.datatype)).insert(p.begin_shapes_rec(li))

        def bx(lay):
            return sorted((q.bbox().to_dtype(ly.dbu) for q in pya.Region(d.begin_shapes_rec(LI[lay])).merged()
                           .each()), key=lambda b: b.left)
        m1 = bx("M1")
        DEV[key] = (d, {"act": bx("Activ")[0], "s": m1[0], "d": m1[1], "gate": bx("GatPoly")[0]})
    return key


def place(c, key, t, label=None):
    d, g = DEV[key]
    c.insert(pya.DCellInstArray(d.cell_index(), t))
    r = {k: t * v for k, v in g.items()}
    r["key"] = key
    if label:
        note(c, label, r["act"])
    return r


def dev(c, name, d, g, s, key, b="vdd"):
    w, l, ng = key
    CDL.setdefault(c.name, []).append("M%s %s %s %s %s sg13_hv_pmos w=%gu l=%gu ng=%d m=1" % (name, d, g, s, b, w, l, ng))


def mirror_row(keys, ts, xc):
    """right half of a row = M90 image of its left half about x = xc"""
    n = len(keys)
    for i in range(n - n // 2, n):
        assert keys[i] == keys[n - 1 - i]
        ts[i] = pya.DTrans(pya.DTrans.M90, pya.DVector(2 * xc, 0)) * ts[n - 1 - i]
    return ts


def rows(c, keys, labels, src_out, G=None):
    """Rotated fingers (W along x, L along y), Activ 0.25 apart (Gat_b1: the end caps merge into one gate strip).
    Lower row: inner line y = 0, devices below it; inner side = drain (src_out) or source. Upper row (if G) = M0
    image about y = G / 2. labels: [lower, upper]. Returns ([lower, upper] geometry, xc)."""
    xs, x = [], 0.0
    for k in keys:
        xs.append(x)
        x += k[0] + 0.25
    xc = (x - 0.25) / 2
    ts = [pya.DTrans(pya.DTrans.R90, pya.DVector(xs[i] + k[0], -(k[1] + 0.68))) if src_out else
          pya.DTrans(pya.DTrans.R270, pya.DVector(xs[i], 0)) for i, k in enumerate(keys)]
    ts = mirror_row(keys, ts, xc)
    out = [[place(c, k, t, lb) for k, t, lb in zip(keys, ts, labels[0])]]
    if G is not None:
        my = pya.DTrans(pya.DTrans.M0, pya.DVector(0, G))
        out.append([place(c, k, my * t, lb) for k, t, lb in zip(keys, ts, labels[1])])
    return out, xc


def gate_cols(c, row):
    """gate contact column at both row ends: poly tab as long as the gate (no neck), 0.60 beyond the Activ (so the
    poly beyond the 0.25 end-cap zone is 0.35 > 0.30 wide), contacts 0.30 ... 0.46 from the Activ (Cnt_e 0.14),
    Metal1 0.26 wide (Via1 0.19 + 2 V1_c), 0.25 from the Activ, i.e. >= M1_b from the S/D stripes. Returns M1 boxes."""
    out = []
    for dv, sg in ((row[0], -1), (row[-1], 1)):
        e = dv["act"].left if sg < 0 else dv["act"].right
        y0, y1 = dv["gate"].bottom, dv["gate"].top
        box(c, "GatPoly", e, y0, e + sg * 0.60, y1)
        fill(c, "Cont", e + sg * 0.30, y0 + 0.07, e + sg * 0.46, y1 - 0.07)
        b = pya.DBox(min(e + sg * 0.25, e + sg * 0.51), y0 + 0.02, max(e + sg * 0.25, e + sg * 0.51), y1 - 0.02)
        box(c, "M1", b.left, b.bottom, b.right, b.top)
        out.append(b)
    return out


def bridge(c, lo, up):
    """poly bridge joining the two rows' gate tabs at both row ends, 0.25 ... 0.60 from the end Activ (outside the
    end-cap zone, 0.35 wide, so no narrow tongue): the gates of both rows are one poly net, no Metal2 needed"""
    for i, sg in ((0, -1), (-1, 1)):
        e = lo[i]["act"].left if sg < 0 else lo[i]["act"].right
        box(c, "GatPoly", e + sg * 0.25, lo[i]["gate"].top, e + sg * 0.60, up[i]["gate"].bottom)


def tab3(c, cx, ys, yt):
    """drain / source tab: Metal1 1.11 wide (3 Via1 + 2 V1_b + 2 x 0.05) from a stripe edge ys to a track at yt"""
    box(c, "M1", cx - 0.555, ys, cx + 0.555, yt + (0.145 if yt > ys else -0.145))
    fill(c, "Via1", cx - 0.505, yt - 0.095, cx + 0.505, yt + 0.095)


def track(c, x0, x1, y, hw=TW):
    box(c, "M2", x0, y - hw, x1, y + hw)


def edge_stub(c, col, y, x_edge, net):
    """inner M1 net (gate column) to an M2 pin at the cell edge: one Via1 on the column, a 0.30 M2 stub"""
    fill(c, "Via1", col.left, y - 0.095, col.right, y + 0.095)
    box(c, "M2", x_edge, y - 0.15, col.right if x_edge < col.left else col.left, y + 0.15)
    xa = x_edge + (0.5 if x_edge < col.left else -0.5)
    pin(c, "M2", net, x_edge, y - 0.15, xa, y + 0.15)


def finish(c, pins_of):
    """move the cell's lower left corner to (0, 0); record the port order"""
    b = c.dbbox()
    c.transform(pya.DTrans(pya.DVector(-b.left, -b.bottom)))
    PINS[c.name] = [(n, m, pb.moved(pya.DVector(-b.left, -b.bottom))) for n, m, pb in PINS.get(c.name, [])]
    CDL[c.name] = (pins_of, CDL.get(c.name, []))
    return c


def end_plate(c, a, xr, G):
    """dummy drains of both rows (they face the band): one Metal1 plate, out over the poly bridge to the ring side;
    0.22 (M1_e) from both rows' gate columns, which end 0.02 inside the gate"""
    box(c, "M1", a.left, -0.23, a.right, G + 0.23)
    box(c, "M1", min(xr, a.left), -0.14, max(xr, a.right), G + 0.14)


# ---------------------------------------------------------------- s2d_tails: 12 tails + BP + twin + 2 dummies, 5/6
def tails():
    """rows D | A2b F1a F2a A1b M1b M2a | D (lower) and BP | A1a F2b F1b A2a M1a M2b | D (upper); sources face
    each other under one vdd plate (Act_b 0.21); drains straight out over the closed ring as Metal2 pads."""
    c = ly.create_cell("s2d_tails_c3")
    T = mos(5, 6)
    G = 0.21
    lo_n = ["D", "A2b", "F1a", "F2a", "A1b", "M1b", "M2a", "D"]
    up_n = ["BP", "A1a", "F2b", "F1b", "A2a", "M1a", "M2b", "D"]
    (lo, up), xc = rows(c, [T] * 8, [lo_n, up_n], False, G)
    h = 6.68
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    b = pya.DBox(x0 - (RG + 0.92), -h - 1.13, x1 + (RG + 0.92), G + h + 1.13)
    gl, gr = gate_cols(c, lo)
    hl, hr = gate_cols(c, up)
    bridge(c, lo, up)
    box(c, "M1", x0, -0.23, x1, G + 0.23)                    # vdd plate over both rows' source stripes
    box(c, "M1", x0 - RG, -0.14, x1 + RG, G + 0.14)          # out between the gate columns to the ring sides
    ring(c, x0 - RG, -h - 0.51, x1 + RG, G + h + 0.51)
    for rw, nm, sg in ((lo, lo_n, -1), (up, up_n, 1)):
        Y = (lambda y: y) if sg < 0 else (lambda y: G - y)
        for i, (dv, n) in enumerate(zip(rw, nm)):
            a, cx = dv["act"], dv["act"].center().x
            if n == "D":                                     # dummy drain straight into the ring strip
                dev(c, "D%s%d" % ("lu"[sg > 0], i), "vdd", "vbp", "vdd", T)
                box(c, "M1", a.left, Y(-h - 0.21), a.right, Y(-6.45))
                continue
            if n == "BP":                                    # diode: drain lane into its own gate column
                dev(c, "BP", "vbp", "vbp", "vdd", T)
                box(c, "M1", hl.left, hl.top - 0.01, hl.right, Y(-6.65))   # 0.24 (M1_e) below the ring strip
                box(c, "M1", hl.left, Y(-6.39), a.left + 1.0, Y(-6.65))    # beyond BP's gate (6.55)
                continue
            net = ("sa_" if n[-1] == "a" else "sb_") + n[:-1]
            dev(c, "T" + n, net, "vbp", "vdd", T)
            # drain pad: M1 0.22 (M1_e) from the ring strip, inside the drain diffusion; 3 Via1; M2 out to the edge
            box(c, "M1", cx - 0.555, Y(-6.67), cx + 0.555, Y(-6.38))
            fill(c, "Via1", cx - 0.505, Y(-6.62), cx + 0.505, Y(-6.43))
            ye = b.bottom if sg < 0 else b.top
            box(c, "M2", cx - 0.555, Y(-6.38), cx + 0.555, ye)
            pin(c, "M2", net, cx - 0.555, ye, cx + 0.555, ye - sg * 0.30)
    edge_stub(c, gl, gl.center().y, b.left, "vbp")
    pin(c, "M1", "vdd", x0 - RG - 0.30, -h + 0.5, x0 - RG, -h + 2.5)
    well(c, b)
    return finish(c, ["sa_A1", "sa_A2", "sa_F1", "sa_F2", "sa_M1", "sa_M2", "sb_A1", "sb_A2", "sb_F1", "sb_F2",
                      "sb_M1", "sb_M2", "vbp", "vdd"])


# ---------------------------------------------------------------- s2d_loads: LP / LN / D 4 + 4 + 4 fingers 6/4
def loads():
    """both rows X LP LN DD DD LN LP X (the library's 1-D map P N D D N P P N D D N P folded; each column holds two
    fingers of one device). Drains face the band: one Metal1 plate per column joins both rows' drains; three M2
    tracks lp dd ln join the columns and run to the left edge. Sources into the ring strips."""
    c = ly.create_cell("s2d_loads_c3")
    P, X = mos(6, 4), mos(1, 4)                  # narrow end dummies, the same at all four row ends
    G = 0.70                                     # pSD_b 0.31 between the rows' pSD (0.18 beyond each Activ)
    nm = ["X", "LP", "LN", "DD", "DD", "LN", "LP", "X"]
    (lo, up), xc = rows(c, [X, P, P, P, P, P, P, X], [nm, nm], True, G)
    h = 4.68
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    b = pya.DBox(x0 - (RG + 0.92), -h - 1.13, x1 + (RG + 0.92), G + h + 1.13)
    net = {"LP": "lp", "LN": "ln", "DD": "dd"}
    ty = {"lp": G / 2 - TN, "dd": G / 2, "ln": G / 2 + TN}
    xe = {}
    for rw, sg in ((lo, -1), (up, 1)):
        for i, (dv, n) in enumerate(zip(rw, nm)):
            if n == "X":
                dev(c, "X%s%d" % ("lu"[sg > 0], i), "vdd", "vcmfb", "vdd", X)
            else:
                dev(c, "%s%d%s" % (n, i, "lu"[sg > 0]), net[n], "vcmfb", "vdd", P)
    for i, n in enumerate(nm):
        a = lo[i]["act"]
        if n == "X":
            end_plate(c, a, x0 - RG if i == 0 else x1 + RG, G)
            continue
        if n == "DD" and i == 4:
            continue
        xr = lo[4]["act"].right if n == "DD" else a.right
        box(c, "M1", a.left, -0.23, xr, G + 0.23)
        cx = (a.left + xr) / 2
        fill(c, "Via1", cx - 0.505, ty[net[n]] - 0.095, cx + 0.505, ty[net[n]] + 0.095)
        xe[net[n]] = max(xe.get(net[n], 0), cx + 0.555)
    for n, y in ty.items():
        track(c, b.left, xe[n], y, 0.10)
        pin(c, "M2", n, b.left, y - 0.10, b.left + 0.5, y + 0.10)
    gl, gr = gate_cols(c, lo)
    gate_cols(c, up)
    bridge(c, lo, up)
    for sg in (-1, 1):                           # source plates into the ring strips (0.21 = pSD_c 0.18 + pSD_d1)
        yb = -h - 0.51 if sg < 0 else G + h + 0.51
        box(c, "M1", x0, yb, x1, (-h + 0.23) if sg < 0 else (G + h - 0.23))
    ring(c, x0 - RG, -h - 0.51, x1 + RG, G + h + 0.51)
    edge_stub(c, gl, gl.center().y, b.left, "vcmfb")
    pin(c, "M1", "vdd", xc - 1.0, -h - 0.51, xc + 1.0, -h - 0.21)
    well(c, b)
    return finish(c, ["dd", "ln", "lp", "vcmfb", "vdd"])


# ---------------------------------------------------------------- s2d_casc_p: LPC / LNC / DC 2 fingers 15/3, BPC 1/4
def casc_p():
    """rows X LPC LNC DC X (lower) and BPC LPC LNC DC X (upper): BPC at one end, its twin at the other, 1/4
    dummies at the lower row's ends. Drains face the band (one plate per column, M2 tracks voutp vcmfb voutn to the
    left edge); sources out to M2 tracks lp ln dd inside the ring, joined by three equal M1 lines outside the ring."""
    c = ly.create_cell("s2d_casc_p_c3")
    C, S = mos(15, 3), mos(1, 4)
    G = 0.70
    lo_n = ["X", "LPC", "LNC", "DC", "X"]
    up_n = ["BPC", "LPC", "LNC", "DC", "X"]
    (lo, up), xc = rows(c, [S, C, C, C, S], [lo_n, up_n], True, G)
    nets = {"LPC": ("voutp", "lp"), "LNC": ("voutn", "ln"), "DC": ("vcmfb", "dd")}
    ty = {"voutp": G / 2 - TN, "vcmfb": G / 2, "voutn": G / 2 + TN}
    ts = {"lp": -3.95, "ln": -3.95 - TN, "dd": -3.95 - 2 * TN}      # source tracks under the lower row
    yr = -3.95 - 2 * TN - 0.145 - 0.22                               # ring strip: M1_e 0.22 from the lowest tab end
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    xj = [x0 - RG - 0.30 - 0.18 - 0.145 - k * 0.47 for k in range(3)]  # join line centers, outside the ring
    b = pya.DBox(xj[2] - 0.145, yr - 0.30 - 0.62, x1 + (RG + 0.92), G - yr + 0.30 + 0.62)
    for rw, nm, sg in ((lo, lo_n, -1), (up, up_n, 1)):
        Y = (lambda y: y) if sg < 0 else (lambda y: G - y)
        for i, (dv, n) in enumerate(zip(rw, nm)):
            a, cx = dv["act"], dv["act"].center().x
            if n in nets:
                d, s = nets[n]
                dev(c, "%s%s" % (n, "lu"[sg > 0]), d, "vbpc", s, C)
                tab3(c, cx, Y(-3.45), Y(ts[s]))
                continue
            dev(c, "BPC" if n == "BPC" else "X%s%d" % ("lu"[sg > 0], i), "vbpc" if n == "BPC" else "vdd", "vbpc",
                "vdd", S)
            box(c, "M1", a.left, Y(yr), a.right, Y(-4.45))            # source straight into the ring strip
    for i, n in enumerate(lo_n[1:4], 1):                              # drain plates, one per column
        a = lo[i]["act"]
        box(c, "M1", a.left, -0.23, a.right, G + 0.23)
        y = ty[nets[n][0]]
        fill(c, "Via1", a.center().x - 0.505, y - 0.095, a.center().x + 0.505, y + 0.095)
        track(c, b.left, a.center().x + 0.555, y, 0.10)
        pin(c, "M2", nets[n][0], b.left, y - 0.10, b.left + 0.5, y + 0.10)
    gl, gr = gate_cols(c, lo)
    hl, hr = gate_cols(c, up)
    bridge(c, lo, up)
    end_plate(c, lo[-1]["act"], x1 + RG, G)                           # right end: both dummies to the ring side
    a = lo[0]["act"]                         # left end: lower dummy drain out to the ring side, 0.22 (M1_e) below
    yt = G + 0.07 - 0.22                     # BPC's drain lane, which runs into BPC's own gate column
    box(c, "M1", a.left, -0.23, a.right, yt)
    box(c, "M1", x0 - RG, -0.14, a.right, yt)
    box(c, "M1", hl.left, G + 0.07, a.right, G + 0.29)
    box(c, "M1", hl.left, G + 0.07, hl.right, hl.bottom + 0.01)
    for k, (s, y) in enumerate(ts.items()):                           # source tracks and their join lines
        for yy in (y, G - y):
            track(c, xj[k] - 0.145, lo[1 + k]["act"].center().x + 0.555, yy, 0.10)
            fill(c, "Via1", xj[k] - 0.095, yy - 0.095, xj[k] + 0.095, yy + 0.095)
        box(c, "M1", xj[k] - 0.145, ts["dd"] - 0.145, xj[k] + 0.145, G - ts["dd"] + 0.145)
        box(c, "M2", b.left, y - 0.10, xj[k], y + 0.10)
        pin(c, "M2", s, b.left, y - 0.10, b.left + 0.5, y + 0.10)
    ring(c, x0 - RG, yr - 0.30, x1 + RG, G - yr + 0.30)
    edge_stub(c, gl, -2.0, b.left, "vbpc")
    pin(c, "M1", "vdd", xc - 1.0, yr - 0.30, xc + 1.0, yr)
    well(c, pya.DBox(x0 - (RG + 0.92), b.bottom, b.right, b.top))
    return finish(c, ["dd", "ln", "lp", "vbpc", "vcmfb", "vdd", "voutn", "voutp"])


# ---------------------------------------------------------------- bias_tree_noab_p: PBNC PBN + 2/6 dummy, TGP
def bias_tree():
    """row PBNC PBN D (2/6, 5/6, 2/6: the narrow device and its narrow twin), drains up over the closed ring as M2
    pads, sources into the lower ring strip; TGP (1/0.45) centered below the ring in the same NWell."""
    c = ly.create_cell("bias_tree_noab_p_c3")
    N, P, S = mos(2, 6), mos(5, 6), mos(1, 0.45)
    lab = ["PBNC", "PBN", "D"]
    (row,), xc = rows(c, [N, P, N], [lab], True)
    h = 6.68
    x0, x1 = row[0]["act"].left, row[-1]["act"].right
    ta = -h - 0.51 - 0.43                                    # TGP Activ top: pSD_i1 0.40 + pSD_d1 0.03 below the ring
    b = pya.DBox(x0 - (RG + 0.92), ta - 1.0 - 0.62, x1 + (RG + 0.92), 0.51 + 0.62)
    gl, gr = gate_cols(c, row)
    for dv, n, net in zip(row, lab, ["vbnc", "vbn", "vdd"]):
        a, cx = dv["act"], dv["act"].center().x
        dev(c, n, net, "vbp", "vdd", dv["key"])
        if n == "D":                                         # dummy drain straight into the ring strip
            box(c, "M1", a.left, -0.23, a.right, 0.21)
            continue
        box(c, "M1", cx - 0.555, -0.30, cx + 0.555, -0.01)   # drain pad, M1_e 0.22 from the ring strip
        fill(c, "Via1", cx - 0.505, -0.25, cx + 0.505, -0.06)
        box(c, "M2", cx - 0.555, -0.30, cx + 0.555, b.top)
        pin(c, "M2", net, cx - 0.555, b.top - 0.30, cx + 0.555, b.top)
    box(c, "M1", x0, -h - 0.51, x1, -h + 0.23)               # sources into the lower ring strip
    ring(c, x0 - RG, -h - 0.51, x1 + RG, 0.51)
    edge_stub(c, gl, gl.center().y, b.left, "vbp")
    pin(c, "M1", "vdd", x0 - RG - 0.30, -h + 0.5, x0 - RG, -h + 2.5)
    # TGP (iref <-> ni, gate en_3v3_b) centered under the ring, gate head down, contact on the head (Cnt_e 0.14)
    tg = place(c, S, pya.DTrans(pya.DTrans.M0, pya.DVector(xc - 0.565, ta)), "TGP")
    dev(c, "TGP", "iref", "en_3v3_b", "ni", S)
    a = tg["act"]
    box(c, "GatPoly", xc - 0.225, a.bottom - 0.56, xc + 0.225, a.bottom)
    fill(c, "Cont", xc - 0.08, a.bottom - 0.34, xc + 0.08, a.bottom - 0.18)
    box(c, "M1", xc - 0.13, b.bottom, xc + 0.13, a.bottom - 0.18)
    pin(c, "M1", "en_3v3_b", xc - 0.13, b.bottom, xc + 0.13, b.bottom + 0.3)
    for st, net, sg in ((tg["s"], "iref", -1), (tg["d"], "ni", 1)):
        xo = st.left - 0.10 if sg < 0 else st.right + 0.10
        box(c, "M1", min(xo, st.left), b.bottom, max(xo, st.right), st.top)
        pin(c, "M1", net, min(xo, st.left), b.bottom, max(xo, st.right), b.bottom + 0.3)
    well(c, b)
    return finish(c, ["en_3v3_b", "iref", "ni", "vbn", "vbnc", "vbp", "vdd"])


# ---------------------------------------------------------------- s2d_pd_p: TPP / TNP, one ng=2 PCell sharing vcm
def pd_p():
    """voutp | G | vcm | G | voutn: one pmosHV w=2 ng=2 (two 1/0.45 fingers sharing the vcm stripe). Gates joined
    in poly over the vcm stripe end, one contact row on the heads and the bridge, en_3v3 in M1 to the top edge.
    N+ tie (bulk vdd) under the device, vcm in M1 straight down across it (no contact there)."""
    c = ly.create_cell("s2d_pd_p_c3")
    place(c, mos(2, 0.45, 2), pya.DTrans(), "TPP  TNP")
    dev_lines = ["MTPP voutp en_3v3 vcm vdd sg13_hv_pmos w=1u l=0.45u ng=1 m=1",
                 "MTNP voutn en_3v3 vcm vdd sg13_hv_pmos w=1u l=0.45u ng=1 m=1"]
    CDL.setdefault(c.name, []).extend(dev_lines)
    for x0 in (0.34, 1.17):                                  # gate heads, full gate width 0.45
        box(c, "GatPoly", x0, 1.0, x0 + 0.45, 1.56)
    box(c, "GatPoly", 0.79, 1.07, 1.17, 1.56)                # bridge over the vcm stripe end (Gat_d 0.07)
    fill(c, "Cont", 0.41, 1.18, 1.55, 1.34)
    b = pya.DBox(-0.62, -0.73 - 0.62, 2.58, 1.62)
    box(c, "M1", 0.51, 1.18, 1.45, 1.40)                     # gate pad (M1_b 0.18 above the stripe ends)
    box(c, "M1", 0.85, 1.18, 1.11, b.top)
    pin(c, "M1", "en_3v3", 0.85, b.top - 0.30, 1.11, b.top)
    box(c, "Activ", 0.0, -0.73, 1.96, -0.43)                 # tie: pSD_i1 0.40 + pSD_d1 0.03 below the Activ
    for xa, xb in ((0.0, 0.67), (1.29, 1.96)):
        box(c, "M1", xa, -0.73, xb, -0.43)
        fill(c, "Cont", xa + 0.07, -0.66, xb - 0.07, -0.50)
    pin(c, "M1", "vdd", 0.0, -0.73, 0.67, -0.43)
    box(c, "M1", 0.90, b.bottom, 1.06, 0.0)                  # vcm down across the tie Activ
    pin(c, "M1", "vcm", 0.90, b.bottom, 1.06, b.bottom + 0.30)
    box(c, "M1", b.left, 0.35, 0.23, 0.65)                   # voutp out to the left edge
    pin(c, "M1", "voutp", b.left, 0.35, b.left + 0.30, 0.65)
    box(c, "M1", 1.73, 0.35, b.right, 0.65)                  # voutn out to the right edge
    pin(c, "M1", "voutn", b.right - 0.30, 0.35, b.right, 0.65)
    well(c, b)
    return finish(c, ["en_3v3", "vcm", "vdd", "voutn", "voutp"])


# ---------------------------------------------------------------- input device (tub) and s2d_inputs
def tub():
    """one input device hv PMOS 2 x 10/1 (w=20 ng=2) in its own NWell, bulk = source. The N+ tie runs under the
    device (pSD_i1 0.40 + pSD_d1 0.03 below the Activ), contacted only under the two source plates; the drain tab
    crosses it in Metal1 without a contact. Source plates joined by a Metal2 strap. Gate heads full width (1.0),
    joined in poly over the drain stripe end, contacts on both heads (Cnt_e 0.14; M1_b 0.18 to the stripe ends)."""
    c = ly.create_cell("tub_p20x1_c3")
    place(c, mos(20, 1, 2), pya.DTrans(), "M")
    for x0 in (0.34, 1.72):
        box(c, "GatPoly", x0, 10.0, x0 + 1.0, 10.56)
        fill(c, "Cont", x0 + 0.07, 10.18, x0 + 0.93, 10.34)
        box(c, "M1", x0 + 0.03, 10.18, x0 + 0.97, 10.40)
    box(c, "GatPoly", 1.34, 10.07, 1.72, 10.56)             # poly bridge, Gat_d 0.07 above the Activ
    pin(c, "M1", "g", 1.75, 10.18, 2.69, 10.40)
    box(c, "Activ", 0.0, -0.73, 3.06, -0.43)                # tie
    for xa, xb in ((0.07, 0.74), (2.32, 2.99)):             # source plates over the tie contacts
        box(c, "M1", xa, -1.35, xb, 0.0)
    for xa, xb in ((0.07, 0.67), (2.39, 2.99)):             # tie contacts only under the plates (mirror images)
        fill(c, "Cont", xa, -0.66, xb, -0.50)
    for xa in (0.31, 2.56):
        box(c, "Via1", xa, -0.36, xa + 0.19, -0.17)
    box(c, "M2", 0.26, -0.41, 2.80, -0.12)                  # source strap (Mn_c1 0.05 at the ends)
    box(c, "M1", 0.975, -0.62, 2.085, 0.0)                  # drain tab (3 Via1 wide) under the middle stripe
    pin(c, "M1", "s", 0.07, -1.35, 0.74, -1.05)
    pin(c, "M1", "d", 0.975, -0.62, 2.085, -0.32)
    well(c, pya.DBox(-0.62, -1.35, 3.68, 10.62))
    CDL[c.name] = (["d", "g", "s"], ["M0 d g s s sg13_hv_pmos w=20u l=1u ng=2 m=1"])
    return c


def inputs(tc):
    """2 x 8 tubs: D | A1a F2b F1b A2a | M1a M2b | D over D | A2b F1a F2a A1b | M1b M2a | D (upper row = M0 image of
    the lower one). Gate heads face the band between the rows (6 gate tracks); drains and source plates face
    outwards. x / y run left of the CMFB columns, xc / yc right of them, so each pair shares a track slot."""
    c = ly.create_cell("s2d_inputs_c3")
    P = 4.30 + 1.80                                          # tub NWell width + NW_b1 (different nets)
    yc = 10.0 + (0.62 + 1.80 + 0.62) / 2                     # Activ gap 3.04 between the rows (NW_b1)
    lo_n = ["D", "A2b", "F1a", "F2a", "A1b", "M1b", "M2a", "D"]
    up_n = ["D", "A1a", "F2b", "F1b", "A2a", "M1a", "M2b", "D"]
    gate = {"A1a": "vin", "A2a": "vin", "A1b": "vref", "A2b": "vref", "F1a": "vcm", "F1b": "vfbp", "F2a": "vfbn",
            "F2b": "vcm", "M1a": "vfbp", "M1b": "vcm", "M2a": "vfbn", "M2b": "vcm"}
    # vias between the two rows' gate pads (10.19 ... 2 yc - 10.19); vcm reached by both rows' tabs
    yb = {n: 10.30 + i * TP for i, n in enumerate(["vref", "vfbn", "vcm", "vdd", "vfbp", "vin"])}
    yo = {"lo": {"y": -0.95, "x": -1.43}, "up": {"x": 2 * yc + 0.95, "y": 2 * yc + 1.43}}
    ye = (-1.70, 2 * yc + 1.70)
    x0, x1 = -0.91, 7 * P + 3.06 + 0.91
    xe = {"lo": 4 * P + 2.085, "hi": 5 * P + 0.975}         # x / y tracks end, xc / yc tracks begin
    for r, nm, sg in (("lo", lo_n, 1), ("up", up_n, -1)):
        for i, n in enumerate(nm):
            ox = i * P
            t = pya.DTrans(pya.DVector(ox, 0)) if sg > 0 else pya.DTrans(pya.DTrans.M0, pya.DVector(ox, 2 * yc))
            c.insert(pya.DCellInstArray(tc.cell_index(), t))
            note(c, n, pya.DBox(ox, 4.0, ox + 3.06, 6.0) if sg > 0 else pya.DBox(ox, 2 * yc - 6.0, ox + 3.06,
                                                                                 2 * yc - 4.0))
            Y = (lambda y: y) if sg > 0 else (lambda y, _y=2 * yc: _y - y)
            if n == "D":
                CDL.setdefault(c.name, []).append("XD%s%d vdd vdd vdd tub_p20x1_c3" % (r, i))
                box(c, "M1", ox + 0.07, Y(-0.62), ox + 2.99, Y(-0.30))     # drain tab into both plates
                if sg > 0:                                   # gate pads and stripe ends of both dummies, Via1 on vdd
                    box(c, "M1", ox + 0.07, 10.0, ox + 2.99, 2 * yc - 10.0)
                    fill(c, "Via1", ox + 0.5, yb["vdd"] - 0.095, ox + 2.56, yb["vdd"] + 0.095)
                continue
            g = gate[n]
            d = ("y" if n[-1] == "a" else "x") + ("c" if n[0] == "M" else "")
            s = ("sa_" if n[-1] == "a" else "sb_") + n[:-1]
            CDL.setdefault(c.name, []).append("X%s %s %s %s tub_p20x1_c3" % (n, d, g, s))
            gx = ox + (1.82 if sg > 0 else 0.54)             # lower row: tab on the right head, upper: left head
            box(c, "M1", gx, Y(10.18), gx + 0.70, Y(yb[g] if sg > 0 else 2 * yc - yb[g]) + sg * 0.145)
            fill(c, "Via1", gx + 0.05, yb[g] - 0.095, gx + 0.65, yb[g] + 0.095)
            tab3(c, ox + 1.53, Y(-0.62), yo[r][d[0]])
            for xa in (ox + 0.07, ox + 2.32):                # source plates out to the edge
                box(c, "M1", xa, Y(-1.35), xa + 0.67, ye[0] if sg > 0 else ye[1])
            pin(c, "M1", s, ox + 0.07, ye[0] if sg > 0 else ye[1] - 0.3, ox + 0.74, ye[0] + 0.3 if sg > 0 else ye[1])
    for n, y in yb.items():
        track(c, x0, x1, y)
        pin(c, "M2", n, x0, y - TW, x0 + 0.5, y + TW)
    for r in ("lo", "up"):
        for n, y in yo[r].items():
            track(c, x0, xe["lo"], y)
            track(c, xe["hi"], x1, y)
    for xa, n, edge in ((-0.44, "y", x0), (-0.91, "x", x0), (7 * P + 3.06 + 0.15, "yc", x1),
                        (7 * P + 3.06 + 0.62, "xc", x1)):    # join lines, M1_e 0.22 from the dummies' plates
        ya, yb2 = yo["lo"][n[0]], yo["up"][n[0]]
        box(c, "M1", xa, -1.43 - 0.145, xa + 0.29, 2 * yc + 1.43 + 0.145)
        for y in (ya, yb2):
            fill(c, "Via1", xa + 0.05, y - 0.095, xa + 0.24, y + 0.095)
        pin(c, "M2", n, edge if edge == x0 else edge - 0.5, ya - TW, edge + 0.5 if edge == x0 else edge, ya + TW)
    return finish(c, ["sa_A1", "sa_A2", "sa_F1", "sa_F2", "sa_M1", "sa_M2", "sb_A1", "sb_A2", "sb_F1", "sb_F2",
                      "sb_M1", "sb_M2", "vcm", "vdd", "vfbn", "vfbp", "vin", "vref", "x", "xc", "y", "yc"])


# ---------------------------------------------------------------- pictures
STYLE = [("NWell", "#2e8b57", 0.07, "#2e8b57"), ("TGO", "#b8b860", 0.0, "#8a8a30"), ("pSD", "#d2b48c", 0.18, None),
         ("Activ", "#22aa22", 0.50, None), ("GatPoly", "#c0392b", 0.55, None), ("Cont", "#111111", 0.90, None),
         ("M1", "#3a8fd9", 0.35, "#1a5f99"), ("Via1", "#ff2a2a", 0.90, None), ("M2", "#8e7cc3", 0.40, "#4b3c80")]
VIEWS = {"tub_p20x1_c3": [("gate", (0, 10.6, 4.30, 11.97)), ("tie", (0, 0, 4.30, 2.4))],
         "s2d_inputs_c3": [("row_end", (0, 9.0, 14.0, 17.5))],
         "s2d_tails_c3": [("row_end", (0, 3.0, 9.0, 15.83))], "s2d_loads_c3": [("row_end", (0, 2.0, 9.0, 10.5))],
         "s2d_casc_p_c3": [("row_end", (0, 0, 9.0, 12.81))], "s2d_pd_p_c3": [("gate", (0, 1.0, 3.2, 2.97))],
         "bias_tree_noab_p_c3": [("row_end", (0, 1.0, 5.0, 10.37)), ("tgp", (3.5, 0, 9.5, 3.0))]}


def render(c, fn, win=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon
    b = c.dbbox() if win is None else pya.DBox(*win)
    s = min(26.0 / b.width(), 17.0 / b.height())
    fig, ax = plt.subplots(figsize=(max(5.0, b.width() * s) + 1, max(4.0, b.height() * s) + 1))
    for lay, fc, a, ec in STYLE:
        ps = [Polygon([(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()])
              for p in pya.Region(c.begin_shapes_rec(LI[lay])).merged().each()]
        ax.add_collection(PatchCollection(ps, facecolor=fc, alpha=a, edgecolor=ec or fc, linewidth=0.7 if ec else 0))
    fs = 8 if win else 7
    for lay, col in (("M1txt", "#0b3d91"), ("M2txt", "#3b2a70")):
        for t in c.shapes(LI[lay]).each():
            p = t.dtext.trans.disp
            ax.text(p.x, p.y, t.dtext.string, fontsize=fs, color=col, weight="bold", ha="center", va="center",
                    clip_on=True, bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.8))
    it = c.begin_shapes_rec(LI["TEXT"])
    while not it.at_end():
        t = it.shape()
        if t.is_text() and t.text_string not in ("pmosHV", "well"):
            p = it.dtrans() * t.dtext.trans.disp
            ax.text(p.x, p.y, t.text_string, fontsize=fs + 2, color="#5a1a5a", weight="bold", ha="center",
                    va="center", clip_on=True)
        it.next()
    ax.set_xlim(b.left, b.right)
    ax.set_ylim(b.bottom, b.top)
    ax.set_aspect("equal")
    ax.set_xlabel("um")
    w = c.dbbox()
    ax.set_title("%s%s  (cell %.2f x %.2f um)   NWell green, ThickGateOx olive, pSD tan, Activ green, GatPoly red, "
                 "Cont black, Metal1 blue, Via1 red, Metal2 violet" % (c.name, "  close-up" if win else "",
                                                                        w.width(), w.height()), fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fn), dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------- output
def write():
    cells = [tub()]
    cells.append(inputs(cells[0]))
    cells += [tails(), loads(), casc_p(), pd_p(), bias_tree()]
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(os.path.join(OUT, "s2d_p3_cells.gds"), opt)
    txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* s2d_p3_cells.cdl: reference netlists of s2d_p3_cells.gds, written by build_s2d_p3.py (C3, agent P, "
           "2026-11-03).", "* Devices as drawn, one line per finger, dummies included (D = S = vdd).", ""]
    for c in cells:
        ports, lines = CDL[c.name]
        txt += [".SUBCKT %s %s" % (c.name, " ".join(ports))] + lines + [".ENDS %s" % c.name, ""]
    open(os.path.join(OUT, "s2d_p3_cells.cdl"), "w").write("\n".join(txt))
    for c in cells:
        b = c.dbbox()
        print("%-20s %7.3f x %7.3f um" % (c.name, b.width(), b.height()))
        for n, m, pb in PINS[c.name]:
            print("    %-9s %s  (%.3f, %.3f; %.3f, %.3f)" % (n, m, pb.left, pb.bottom, pb.right, pb.top))
    if "--no-png" not in sys.argv:
        for c in cells:
            render(c, c.name + ".png")
            for tag, win in VIEWS.get(c.name, []):
                render(c, "%s_%s.png" % (c.name, tag), win)
    return cells


if __name__ == "__main__":
    write()
