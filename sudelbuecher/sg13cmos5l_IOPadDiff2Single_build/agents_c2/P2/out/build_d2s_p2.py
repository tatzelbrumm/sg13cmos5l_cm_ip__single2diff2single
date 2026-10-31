# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_d2s_p2.py: PMOS layout primitives of d2s_mpdda_pd / bias_tree_pd (IHP sg13cmos5l), rebuild C2, agent P2,
2026-10-31, Claude.

    python3 build_d2s_p2.py        (needs the PDK: PDK_ROOT, default /foss/pdks; writes next to this file)

Writes d2s_p2_cells.gds (cells <name>_c2), d2s_p2_cells.cdl (reference netlists, every dummy a device) and the PNGs.

Layout rules (Christoph, 2026-10-31 18:55, and the brief):
- device layers mirror-symmetric: the right half of every row is the mirror image (M90) of its left half, the upper
  row the mirror image (M0) of the lower one, so the symmetry is exact by construction, PCell grid rounding included;
- dummies only in pairs of the same device at both ends of a row (BP's twin is a full 5/6 dummy);
- gate contacts on full-width poly: on a tab as long as the gate at both row ends (rotated rows), or on the gate heads
  themselves (upright fingers), never through a narrowed link;
- unmodified IHP SG13_dev pmosHV PCells (copied flat, unchanged); taps only at the periphery.
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
TP = 0.48          # M2 track pitch: 0.26 track (Via1 0.19 + 2 x Mn_c 0.005 and margin) + 0.22 (Mn_b 0.21)
TW = 0.13          # half track width
RG = 0.80          # end Activ to tie ring: poly tab 0.60, and the tab beyond both Activ grown by 0.25 stays >= 0.30 wide


def g5(v):
    """5 nm drawing grid (geometry/3_1_offgrid.drc)"""
    return round(v / 0.005) * 0.005


def box(c, lay, x0, y0, x1, y1):
    c.shapes(LI[lay]).insert(pya.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


def fill(c, lay, x0, y0, x1, y1):
    """Cont (Cnt_a 0.16, pitch + Cnt_b 0.18) or Via1 (V1_a 0.19, pitch + V1_b 0.22), centred in the zone"""
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


def well(c, b):
    """one NWell and one ThickGateOx over the whole cell (NW_c1 / NW_e1 0.62 beyond all Activ, TGO_a 0.27)"""
    box(c, "NWell", b.left, b.bottom, b.right, b.top)
    box(c, "TGO", b.left, b.bottom, b.right, b.top)


# ---------------------------------------------------------------- devices: IHP PCells, copied flat and unchanged
_pcl = pya.Layout()
_pcl.technology_name = "sg13cmos5l"
DEV = {}


def mos(w, l, ng=1):
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


def tab3(c, cx, ys, yt, m2=None):
    """drain / source tab: Metal1 1.11 wide (3 Via1 + 2 V1_b + 2 x 0.05) from a stripe edge ys to a track at yt,
    3 Via1 centred on yt; m2 = (y0, y1) draws a Metal2 pad there instead of using a track"""
    box(c, "M1", cx - 0.555, ys, cx + 0.555, yt + (0.145 if yt > ys else -0.145))
    fill(c, "Via1", cx - 0.505, yt - 0.095, cx + 0.505, yt + 0.095)
    if m2:
        box(c, "M2", cx - 0.555, m2[0], cx + 0.555, m2[1])


def tab1(c, cx, ys, yt):
    """one-via tab, 0.29 wide (V1_a + 2 x 0.05)"""
    box(c, "M1", cx - 0.145, ys, cx + 0.145, yt + (0.145 if yt > ys else -0.145))
    fill(c, "Via1", cx - 0.095, yt - 0.095, cx + 0.095, yt + 0.095)


def track(c, x0, x1, y):
    box(c, "M2", x0, y - TW, x1, y + TW)


def finish(c, pins_of):
    """move the cell's lower left corner to (0, 0); record the port order"""
    b = c.dbbox()
    c.transform(pya.DTrans(pya.DVector(-b.left, -b.bottom)))
    PINS[c.name] = [(n, m, pb.moved(pya.DVector(-b.left, -b.bottom))) for n, m, pb in PINS.get(c.name, [])]
    CDL[c.name] = (pins_of, CDL.get(c.name, []))
    return c


# ---------------------------------------------------------------- d2s_loads: PL / PR 4 + 4 fingers 6/4, gate l2
def loads():
    c = ly.create_cell("d2s_loads_c2")
    P, D = mos(6, 4), mos(1, 4)                  # narrow end dummies, the same at all four row ends
    G = 2.05                                     # band: 4 tracks, tab ends M1_e 0.22 from the far row's stripes
    lo_n, up_n = ["D", "R", "L", "L", "R", "D"], ["D", "L", "R", "R", "L", "D"]
    (lo, up), xc = rows(c, [D, P, P, P, P, D], [lo_n, up_n], True, G)
    ty = {n: (G - 3 * TP) / 2 + i * TP for i, n in enumerate(["pl", "vdd", "l2", "pr"])}
    net = {"L": "pl", "R": "pr"}
    for rw, nm, sg in ((lo, lo_n, -1), (up, up_n, 1)):
        for i, (dv, n) in enumerate(zip(rw, nm)):
            cx = dv["act"].center().x
            if n == "D":
                dev(c, "D%s%d" % ("lu"[sg > 0], i), "vdd", "l2", "vdd", D)
                if sg < 0:                       # dummy drains of both rows: one strap through the band, Via1 on vdd
                    box(c, "M1", cx - 0.145, lo[i]["d"].bottom, cx + 0.145, up[i]["d"].top)
                    fill(c, "Via1", cx - 0.095, ty["vdd"] - 0.095, cx + 0.095, ty["vdd"] + 0.095)
                continue
            dev(c, "%s%d%s" % (n, i, "lu"[sg > 0]), net[n], "l2", "vdd", P)
            tab3(c, cx + sg * 0.9, dv["d"].bottom if sg < 0 else dv["d"].top, ty[net[n]])
    gl, gr = gate_cols(c, lo)
    hl, hr = gate_cols(c, up)
    for a, b in ((gl, hl), (gr, hr)):            # gate columns of both rows joined through the band, Via1 on l2
        box(c, "M1", a.left, a.bottom, a.right, b.top)
        fill(c, "Via1", a.left, ty["l2"] - 0.095, a.right, ty["l2"] + 0.095)
    h = 4.68
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    for sg in (-1, 1):                           # source plates out to the ring strips (0.21 = pSD_c 0.18 + pSD_d1)
        yb = -h - 0.21 if sg < 0 else G + h + 0.21
        box(c, "M1", x0, yb + sg * 0.30, x1, (-h + 0.23) if sg < 0 else (G + h - 0.23))
    ring(c, x0 - RG, -h - 0.51, x1 + RG, G + h + 0.51, strips=True)
    for x in (x0 - RG - 0.15, x1 + RG + 0.15):  # vdd track onto both ring sides
        fill(c, "Via1", x - 0.095, ty["vdd"] - 0.095, x + 0.095, ty["vdd"] + 0.095)
    b = pya.DBox(x0 - (RG + 0.92), -h - 1.13, x1 + (RG + 0.92), G + h + 1.13)
    well(c, b)
    for n, y in ty.items():
        track(c, b.left, b.right, y)
        if n != "vdd":
            pin(c, "M2", n, b.left, y - TW, b.left + 0.5, y + TW)
    pin(c, "M1", "vdd", xc - 1.0, -h - 0.51, xc + 1.0, -h - 0.21)
    return finish(c, ["l2", "pl", "pr", "vdd"])


def ring(c, x0, y0, x1, y1, strips):
    """N+ tie ring (or only its two sides): Activ 0.30 (Cnt_a + 2 Cnt_c), Metal1 0.30; inner box given"""
    tap(c, x0 - 0.30, y0 + (0.30 if strips else 0), x0, y1 - (0.30 if strips else 0),
        (x0 - 0.23, y0 + (0.41 if strips else 0.07), x0 - 0.07, y1 - (0.41 if strips else 0.07)))
    tap(c, x1, y0 + (0.30 if strips else 0), x1 + 0.30, y1 - (0.30 if strips else 0),
        (x1 + 0.07, y0 + (0.41 if strips else 0.07), x1 + 0.23, y1 - (0.41 if strips else 0.07)))
    if strips:
        tap(c, x0 - 0.30, y0, x1 + 0.30, y0 + 0.30)
        tap(c, x0 - 0.30, y1 - 0.30, x1 + 0.30, y1)


# ---------------------------------------------------------------- d2s_casc_p: PCL / PCR 2 + 2 fingers 15/3, BPC 1/4
def casc_p():
    c = ly.create_cell("d2s_casc_p_c2")
    C, T = mos(15, 3), mos(1, 4)                 # BPC in the middle of the upper row, its twin (dummy) below it
    G = 2.05
    lo_n, up_n = ["PCR", "D", "PCL"], ["PCL", "BPC", "PCR"]
    (lo, up), xc = rows(c, [C, T, C], [lo_n, up_n], True, G)
    ty = {n: (G - 3 * TP) / 2 + i * TP for i, n in enumerate(["l2", "vdd", "vbpc", "a"])}
    h = 3.68
    yo = {"lo": {"pr": -h - 0.27, "pl": -h - 0.27 - TP}, "up": {"pl": G + h + 0.27, "pr": G + h + 0.27 + TP}}
    nets = {"PCL": ("l2", "pl"), "PCR": ("a", "pr")}
    for rw, nm, sg, r in ((lo, lo_n, -1, "lo"), (up, up_n, 1, "up")):
        for i, (dv, n) in enumerate(zip(rw, nm)):
            cx = dv["act"].center().x
            ds = dv["d"].bottom if sg < 0 else dv["d"].top
            ss = dv["s"].top if sg < 0 else dv["s"].bottom
            if n in nets:
                d, s = nets[n]
                dev(c, "%s%s" % (n, r), d, "vbpc", s, C)
                tab3(c, cx + sg * 1.5, ds, ty[d])
                tab3(c, cx, ss, yo[r][s])
                continue
            dev(c, "BPC" if n == "BPC" else "DUM", "vbpc" if n == "BPC" else "vdd", "vbpc", "vdd", T)
            tab1(c, cx, ds, ty["vbpc" if n == "BPC" else "vdd"])
            yr = -h - 1.51 if sg < 0 else G + h + 1.51  # source straight out to the ring strip
            box(c, "M1", dv["act"].left, yr, dv["act"].right, dv["s"].bottom if sg < 0 else dv["s"].top)
    gl, gr = gate_cols(c, lo)
    hl, hr = gate_cols(c, up)
    for a, b in ((gl, hl), (gr, hr)):
        box(c, "M1", a.left, a.bottom, a.right, b.top)
        fill(c, "Via1", a.left, ty["vbpc"] - 0.095, a.right, ty["vbpc"] + 0.095)
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    for xl, n in ((x0 - 0.835, "pl"), (x1 + 0.835, "pr")):  # pl / pr of both rows joined by one M1 line per side
        ya, yb = yo["lo"][n], yo["up"][n]
        box(c, "M1", xl - 0.145, ya - 0.145, xl + 0.145, yb + 0.145)
        for y in (ya, yb):
            fill(c, "Via1", xl - 0.095, y - 0.095, xl + 0.095, y + 0.095)
    ring(c, x0 - 1.16, -h - 1.51, x1 + 1.16, G + h + 1.51, strips=True)
    for x in (x0 - 1.31, x1 + 1.31):
        fill(c, "Via1", x - 0.095, ty["vdd"] - 0.095, x + 0.095, ty["vdd"] + 0.095)
    b = pya.DBox(x0 - 2.08, -h - 2.13, x1 + 2.08, G + h + 2.13)
    well(c, b)
    for n, y in list(ty.items()) + list(yo["lo"].items()) + list(yo["up"].items()):
        track(c, b.left, b.right, y)
    for n, y in list(ty.items()) + list(yo["lo"].items()):
        if n != "vdd":
            pin(c, "M2", n, b.left, y - TW, b.left + 0.5, y + TW)
    pin(c, "M1", "vdd", xc - 1.0, -h - 1.51, xc + 1.0, -h - 1.21)
    return finish(c, ["a", "l2", "pl", "pr", "vbpc", "vdd"])


# ---------------------------------------------------------------- d2s_tails: 8 tails + BP + 3 dummies, 5/6, vbp
def tails():
    c = ly.create_cell("d2s_tails_c2")
    T = mos(5, 6)
    G = 0.21                                     # sources face each other (Act_b); one vdd plate between the rows
    lo_n = ["D", "Bb", "C1a", "C2a", "Ab", "D"]
    up_n = ["BP", "Aa", "C2b", "C1b", "Ba", "D"]
    (lo, up), xc = rows(c, [T] * 6, [lo_n, up_n], False, G)
    h = 6.68
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    b = pya.DBox(x0 - (RG + 0.92), -h - 0.62, x1 + (RG + 0.92), G + h + 0.62)
    gl, gr = gate_cols(c, lo)
    hl, hr = gate_cols(c, up)
    for a, u in ((gl, hl), (gr, hr)):            # vbp: the two rows' columns bridged in Metal2 over the vdd plate
        fill(c, "Via1", a.left, a.top - 0.60, a.right, a.top - 0.19)
        fill(c, "Via1", u.left, u.bottom + 0.19, u.right, u.bottom + 0.60)
        box(c, "M2", a.left, a.top - 0.65, a.right, u.bottom + 0.65)
    box(c, "M2", b.left, G / 2 - 0.15, gl.right, G / 2 + 0.15)
    pin(c, "M2", "vbp", b.left, G / 2 - 0.15, b.left + 0.5, G / 2 + 0.15)
    box(c, "M1", x0, -0.23, x1, G + 0.23)        # vdd plate over both rows' source stripes
    box(c, "M1", x0 - (RG + 0.30), -0.14, x1 + (RG + 0.30), G + 0.14)  # out between the columns
    ring(c, x0 - RG, -h, x1 + RG, G + h, strips=False)
    for rw, nm, sg in ((lo, lo_n, -1), (up, up_n, 1)):
        for i, (dv, n) in enumerate(zip(rw, nm)):
            cx = dv["act"].center().x
            ye = b.bottom if sg < 0 else b.top
            if n == "D":
                dev(c, "D%s%d" % ("lu"[sg > 0], i), "vdd", "vbp", "vdd", T)
            elif n == "BP":
                dev(c, "BP", "vbp", "vbp", "vdd", T)
            else:
                net = ("sa_" if n[-1] == "a" else "sb_") + n[:-1]
                dev(c, "T" + n, net, "vbp", "vdd", T)
                yv = ye - sg * 0.30
                tab3(c, cx, dv["d"].bottom if sg > 0 else dv["d"].top, yv, (ye, yv - sg * 0.145))
                pin(c, "M2", net, cx - 0.555, ye, cx + 0.555, yv - sg * 0.145)
                continue
            # dummy / BP drain at the outer edge: a lane above the gate column's end (M1_b) to the ring (dummy)
            # or into its own gate column (BP)
            yl = dv["d"].top - 0.11 if sg < 0 else dv["d"].bottom + 0.11
            left = cx < xc
            xr = (x0 - (RG + 0.30)) if left else (x1 + (RG + 0.30))
            if n == "BP":
                xr = hl.left
                box(c, "M1", hl.left, hl.top, hl.right, yl + 0.29)
            box(c, "M1", min(cx, xr), yl - sg * 0.0, max(cx, xr), yl + sg * 0.29)
    pin(c, "M1", "vdd", x0 - RG - 0.30, -h + 0.5, x0 - RG, -h + 2.5)
    well(c, b)
    return finish(c, ["sa_A", "sa_B", "sa_C1", "sa_C2", "sb_A", "sb_B", "sb_C1", "sb_C2", "vbp", "vdd"])


# ---------------------------------------------------------------- bias_tree_p: PBNC PBN PABN + 2/6 dummy, TGP
def bias_tree_p():
    c = ly.create_cell("bias_tree_p_c2")
    N, P, S = mos(2, 6), mos(5, 6), mos(1, 0.45)
    lab = ["PBNC", "PBN", "PABN", "D"]
    (row,), xc = rows(c, [N, P, P, N], [lab], True)
    h = 6.68
    x0, x1 = row[0]["act"].left, row[-1]["act"].right
    b = pya.DBox(x0 - (RG + 0.92), -8.70, x1 + (RG + 0.92), 0.62)
    gl, gr = gate_cols(c, row)
    box(c, "M1", gl.left, gl.top, gl.right, b.top)        # vbp out of the left column to the top edge
    pin(c, "M1", "vbp", gl.left, b.top - 0.4, gl.right, b.top)
    for dv, n, net in zip(row, lab, ["vbnc", "vbn", "vabn", "vdd"]):
        cx = dv["act"].center().x
        dev(c, n, net, "vbp", "vdd", dv["key"])
        if n == "D":                             # dummy drain: lane above the column end to the ring side
            box(c, "M1", cx, dv["d"].top - 0.11, x1 + (RG + 0.30), dv["d"].top + 0.18)
            continue
        tab3(c, cx, dv["d"].bottom, 0.32, (0.12, b.top))
        pin(c, "M2", net, cx - 0.555, 0.12, cx + 0.555, b.top)
    box(c, "M1", x0, -h - 0.22, x1, -h + 0.23)           # vdd plate under the sources
    box(c, "M1", x0 - (RG + 0.30), -h - 0.22, x1 + (RG + 0.30), -h + 0.14)
    ring(c, x0 - RG, -h - 0.22, x1 + RG, 0, strips=False)
    pin(c, "M1", "vdd", x0 - RG - 0.30, -h + 0.5, x0 - RG, -h + 2.5)
    # TGP (iref <-> ni, gate en_3v3_b) centred under the row, gate head pointing down, contact on the head
    t = pya.DTrans(pya.DTrans.M0, pya.DVector(xc - 0.565, -7.08))
    tg = place(c, S, t, "TGP")
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
    return finish(c, ["en_3v3_b", "iref", "ni", "vabn", "vbn", "vbnc", "vbp", "vdd"])


# ---------------------------------------------------------------- upright single rows: d2s_ab_p, d2s_pd_p
def upright(c, keys, labels, gap):
    """upright fingers (R0), Activ `gap` apart; right half = M90 image of the left half. Gate heads 0.56 above the
    Activ, full gate width (L >= 0.45 > 0.30), contact 0.18 above the Activ (Cnt_e 0.14; M1_b to the stripe ends)."""
    xs, x = [], 0.0
    for k in keys:
        xs.append(x)
        x += DEV[k][1]["act"].width() + gap
    xc = (x - gap) / 2
    ts = mirror_row(keys, [pya.DTrans(pya.DVector(xi, 0)) for xi in xs], xc)
    out = [place(c, k, t, lb) for k, t, lb in zip(keys, ts, labels)]
    for dv in out:
        gt, top = dv["gate"], dv["act"].top
        box(c, "GatPoly", gt.left, top, gt.right, top + 0.56)
        fill(c, "Cont", gt.left + 0.07, top + 0.18, gt.right - 0.07, top + 0.34)
    return out, xc


def ab_p():
    c = ly.create_cell("d2s_ab_p_c2")
    A = mos(6.66, 0.6)
    lab = ["D", "FPL", "RP2", "ABP", "D"]
    row, xc = upright(c, [A] * 5, lab, 0.21)
    top = row[0]["act"].top
    bt = pya.DBox(row[1]["gate"].center().x - 0.13, top + 0.18, row[3]["gate"].center().x + 0.13, top + 0.40)
    box(c, "M1", bt.left, bt.bottom, bt.right, bt.top)     # vabp bar over the three gate-head contacts
    yt = top + 0.80                                          # tie: pSD_i1 0.40 + pSD_d1; 0.25 + 0.30 past the heads
    tap(c, row[0]["act"].left, yt, row[-1]["act"].right, yt + 0.30)
    b = pya.DBox(row[0]["act"].left - 0.62, -0.62, row[-1]["act"].right + 0.62, yt + 0.92)
    fill(c, "Via1", xc - 0.095, bt.bottom + 0.015, xc + 0.095, bt.top - 0.015)
    box(c, "M2", xc - 0.15, bt.bottom - 0.04, xc + 0.15, b.top)
    pin(c, "M2", "vabp", xc - 0.15, b.top - 0.4, xc + 0.15, b.top)
    nets = {"FPL": ("l1", "l2"), "RP2": ("vabp", "dabp"), "ABP": ("b", "a")}
    for i, (dv, n) in enumerate(zip(row, lab)):
        if n == "D":                                         # dummy: gate, drain, source on vdd (the tie)
            dev(c, "D%d" % i, "vdd", "vdd", "vdd", A)
            box(c, "M1", dv["act"].left + 0.07, top + 0.18, dv["act"].right - 0.07, yt + 0.30)
            for st in (dv["s"], dv["d"]):
                box(c, "M1", st.left, top, st.right, yt)
            continue
        d, s = nets[n]
        dev(c, n, d, "vabp", s, A)
        sd = {"FPL": (dv["d"], dv["s"]), "RP2": (dv["s"], dv["d"]), "ABP": (dv["s"], dv["d"])}[n]
        # FPL native, ABP its mirror image: native left = s (l2 / a); RP2: native left = d (vabp, up to the bar)
        for st, net in zip(sd, (d, s)):
            if net == "vabp":
                box(c, "M1", st.left, top, st.right, bt.bottom)
            else:
                box(c, "M1", st.left, b.bottom, st.right, 0)
                pin(c, "M1", net, st.left, b.bottom, st.right, b.bottom + 0.4)
    pin(c, "M1", "vdd", xc - 1.0, yt, xc + 1.0, yt + 0.30)
    well(c, b)
    return finish(c, ["a", "b", "dabp", "l1", "l2", "vabp", "vdd"])


def pd_p():
    c = ly.create_cell("d2s_pd_p_c2")
    S = mos(1, 0.45)
    (sa, sb), xc = upright(c, [S, S], ["SA", "SABP"], 0.21)
    top = sa["act"].top
    box(c, "M1", sa["gate"].center().x - 0.13, top + 0.18, sb["gate"].center().x + 0.13, top + 0.40)
    yt = -0.73                                               # tie under both: pSD_i1 0.40 + pSD_d1 0.03
    tap(c, sa["act"].left, yt, sb["act"].right, yt + 0.30)
    b = pya.DBox(sa["act"].left - 0.62, yt - 0.62, sb["act"].right + 0.62, top + 0.62)
    fill(c, "Via1", xc - 0.095, top + 0.195, xc + 0.095, top + 0.385)
    box(c, "M2", xc - 0.20, top + 0.145, xc + 0.20, b.top)  # Mn_d 0.144 um2
    pin(c, "M2", "en_3v3", xc - 0.15, b.top - 0.3, xc + 0.15, b.top)
    dev(c, "SA", "a", "en_3v3", "vddo", S)                  # bulk vdd (brief; the circuit has vddo)
    dev(c, "SABP", "vabp", "en_3v3", "vdd", S)
    box(c, "M1", b.left, 0.35, sa["s"].right, 0.65)          # vddo out to the left edge
    pin(c, "M1", "vddo", b.left, 0.35, b.left + 0.3, 0.65)
    box(c, "M1", sb["s"].left, yt, sb["s"].right, 0)         # SABP source into the tie (vdd)
    pin(c, "M1", "vdd", xc - 0.5, yt, xc + 0.5, yt + 0.30)
    for st, net, sg in ((sa["d"], "a", -1), (sb["d"], "vabp", 1)):   # drains: Via1 x 2, Metal2 down over the tie
        xa, xb = (st.right - 0.21, st.right) if sg < 0 else (st.left, st.left + 0.21)
        box(c, "M1", xa, 0, xb, top)
        fill(c, "Via1", xa + 0.01, 0.195, xb - 0.01, 0.805)
        box(c, "M2", xa, b.bottom, xb, 0.855)
        pin(c, "M2", net, xa, b.bottom, xb, b.bottom + 0.3)
    well(c, b)
    return finish(c, ["a", "en_3v3", "vabp", "vdd", "vddo"])


# ---------------------------------------------------------------- input device (tub) and d2s_inputs
def tub():
    """one input device hv PMOS 2 x 10/1 in its own NWell, bulk = source: N+ ties left and right of the two source
    stripes (0.21 from the Activ: Act_b, pSD_c 0.18 + pSD_d1 0.03), joined to them in Metal1 and to each other by a
    Metal2 strap below the device; gate contacts on the two 1 um gate heads (2 each), one Metal1 bar; drain tab down."""
    c = ly.create_cell("tub_p20x1_c2")
    M = mos(20, 1, 2)
    d = place(c, M, pya.DTrans(), "M")
    for x0 in (0.34, 1.72):                       # gate heads: full gate width 1.0, 0.56 beyond the Activ
        box(c, "GatPoly", x0, 10.0, x0 + 1.0, 10.56)
        fill(c, "Cont", x0 + 0.07, 10.18, x0 + 0.93, 10.34)
    box(c, "M1", 0.37, 10.18, 2.69, 10.40)
    pin(c, "M1", "g", 1.33, 10.18, 1.73, 10.40)
    for x0 in (-0.51, 3.27):
        tap(c, x0, 0, x0 + 0.30, 10.0)
    box(c, "M1", -0.51, -0.62, 0.23, 10.0)        # source plates = tie + source stripe, down to the cell edge
    box(c, "M1", 2.83, -0.62, 3.57, 10.0)
    pin(c, "M1", "s", -0.51, -0.62, 0.23, -0.32)
    for x in (-0.14, 3.20):
        fill(c, "Via1", x - 0.095, -0.425, x + 0.095, -0.235)
    box(c, "M2", -0.285, -0.475, 3.345, -0.185)
    box(c, "M1", 0.975, -0.62, 2.085, 0.0)        # drain tab (3 Via1 wide) under the middle stripe
    pin(c, "M1", "d", 0.975, -0.62, 2.085, -0.32)
    well(c, pya.DBox(-1.13, -0.62, 4.19, 10.62))
    CDL[c.name] = (["d", "g", "s"], ["M0 d g s s sg13_hv_pmos w=20u l=1u ng=2 m=1"])
    return c


def inputs(tc):
    """2 x 6 tubs: D | Aa C2b C1b Ba | D over D | Bb C1a C2a Ab | D (upper row = M0 image of the lower one).
    Gate heads face the band between the rows (gate tracks); drains and source plates face outwards."""
    c = ly.create_cell("d2s_inputs_c2")
    P = 5.32 + 1.80                                          # tub NWell width + NW_b1 (different nets)
    yc = 10.0 + (0.62 + 1.80 + 0.62) / 2                     # Activ gap 3.04 between the rows
    lo_n = ["D", "Bb", "C1a", "C2a", "Ab", "D"]
    up_n = ["D", "Aa", "C2b", "C1b", "Ba", "D"]
    gate = {"Aa": "vinp", "Ab": "vref", "Ba": "vref", "Bb": "vinn", "C1a": "vref", "C1b": "vfb", "C2a": "vref",
            "C2b": "vfb"}
    yb = {n: 10.0 + 0.55 + i * 0.48 + (0.01 if i > 1 else 0) for i, n in enumerate(["vinn", "vref", "vdd", "vfb",
                                                                                     "vinp"])}
    yo = {"lo": {"y": -0.95, "x": -1.43}, "up": {"x": 2 * yc + 0.95, "y": 2 * yc + 1.43}}
    ye = (-1.70, 2 * yc + 1.70)
    for r, nm, sg in (("lo", lo_n, 1), ("up", up_n, -1)):
        for i, n in enumerate(nm):
            ox = i * P
            t = pya.DTrans(pya.DVector(ox, 0)) if sg > 0 else pya.DTrans(pya.DTrans.M0, pya.DVector(ox, 2 * yc))
            c.insert(pya.DCellInstArray(tc.cell_index(), t))
            note(c, n, pya.DBox(ox, 4.0, ox + 3.06, 6.0) if sg > 0 else pya.DBox(ox, 2 * yc - 6.0, ox + 3.06,
                                                                                 2 * yc - 4.0))
            Y = (lambda y: y) if sg > 0 else (lambda y, _y=2 * yc: _y - y)
            if n == "D":
                CDL.setdefault(c.name, []).append("XD%s%d vdd vdd vdd tub_p20x1_c2" % (r, i))
                box(c, "M1", ox - 0.51, Y(10.18), ox + 3.57, Y(10.40))   # gate bar into both plates
                box(c, "M1", ox - 0.51, Y(-0.62), ox + 3.57, Y(-0.30))   # drain tab into both plates
                if sg > 0:                                             # plates through the band, Via1 on vdd
                    for x0 in (ox - 0.51, ox + 2.83):
                        box(c, "M1", x0, 10.0, x0 + 0.74, 2 * yc - 10.0)
                        fill(c, "Via1", x0 + 0.275, yb["vdd"] - 0.095, x0 + 0.465, yb["vdd"] + 0.095)
                continue
            g = gate[n]
            d = "y" if n[-1] == "a" else "x"
            s = ("sa_" if n[-1] == "a" else "sb_") + n[:-1]
            CDL.setdefault(c.name, []).append("X%s %s %s %s tub_p20x1_c2" % (n, d, g, s))
            gx = ox + (1.82 if sg > 0 else 0.54)                     # lower row: right end of the bar, upper: left
            box(c, "M1", gx, Y(10.40), gx + 0.70, Y(yb[g] if sg > 0 else 2 * yc - yb[g]) + sg * 0.145)
            fill(c, "Via1", gx + 0.05, yb[g] - 0.095, gx + 0.65, yb[g] + 0.095)
            tab3(c, ox + 1.53, Y(-0.62), yo[r][d])
            for x0 in (ox - 0.51, ox + 2.83):                        # source plates out to the edge
                box(c, "M1", x0, Y(-0.62), x0 + 0.74, ye[0] if sg > 0 else ye[1])
            pin(c, "M1", s, ox - 0.51, ye[0] if sg > 0 else ye[1] - 0.3, ox + 0.23, ye[0] + 0.3 if sg > 0 else ye[1])
    x0, x1 = -1.13, 5 * P + 4.19
    for n, y in yb.items():
        track(c, x0, x1, y)
        pin(c, "M2", n, x0, y - TW, x0 + 0.5, y + TW)
    for r in ("lo", "up"):
        for n, y in yo[r].items():
            track(c, x0, x1, y)
    for xa, n in ((-1.02, "x"), (5 * P + 3.79, "y")):     # x / y join lines, M1_e 0.22 from the dummies' plates
        ya, yb2 = yo["lo"][n], yo["up"][n]
        box(c, "M1", xa, ya - 0.145, xa + 0.29, yb2 + 0.145)
        for y in (ya, yb2):
            fill(c, "Via1", xa + 0.05, y - 0.095, xa + 0.24, y + 0.095)
        pin(c, "M2", n, x0 if n == "x" else x1 - 0.5, yo["lo"][n] - TW, x0 + 0.5 if n == "x" else x1,
            yo["lo"][n] + TW)
    return finish(c, ["sa_A", "sa_B", "sa_C1", "sa_C2", "sb_A", "sb_B", "sb_C1", "sb_C2", "vdd", "vfb", "vinn", "vinp",
                      "vref", "x", "y"])


# ---------------------------------------------------------------- pictures
STYLE = [("NWell", "#2e8b57", 0.07, "#2e8b57"), ("TGO", "#b8b860", 0.0, "#8a8a30"), ("pSD", "#d2b48c", 0.18, None),
         ("Activ", "#22aa22", 0.50, None), ("GatPoly", "#c0392b", 0.55, None), ("Cont", "#111111", 0.90, None),
         ("M1", "#3a8fd9", 0.35, "#1a5f99"), ("Via1", "#ff2a2a", 0.90, None), ("M2", "#8e7cc3", 0.40, "#4b3c80")]
VIEWS = {"d2s_tails_c2": [("row_end", (0, 3.0, 5.5, 14.81))], "d2s_loads_c2": [("row_end", (0, 3.5, 5.5, 10.2))],
         "d2s_casc_p_c2": [("row_end", (0, 0, 6.0, 13.67))], "d2s_inputs_c2": [("row_end", (0, 8.5, 13.0, 17.9))],
         "tub_p20x1_c2": [("gate", (0, 9.0, 5.32, 11.24))], "d2s_ab_p_c2": [("gate", (0, 5.5, 8.48, 8.83))],
         "bias_tree_p_c2": [("row_end", (0, 0, 4.5, 9.32)), ("tgp", (7.0, 0, 11.2, 3.0))]}


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
    cells += [tails(), loads(), casc_p(), ab_p(), pd_p(), bias_tree_p()]
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(os.path.join(OUT, "d2s_p2_cells.gds"), opt)
    txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* d2s_p2_cells.cdl: reference netlists of d2s_p2_cells.gds, written by build_d2s_p2.py (C2, agent P2, "
           "2026-10-31).", "* Devices as drawn, one line per finger, dummies included (D = S = vdd).", ""]
    for c in cells:
        ports, lines = CDL[c.name]
        txt += [".SUBCKT %s %s" % (c.name, " ".join(ports))] + lines + [".ENDS %s" % c.name, ""]
    open(os.path.join(OUT, "d2s_p2_cells.cdl"), "w").write("\n".join(txt))
    for c in cells:
        b = c.dbbox()
        print("%-16s %7.3f x %7.3f um" % (c.name, b.width(), b.height()))
        for n, m, pb in PINS[c.name]:
            print("    %-9s %s  (%.3f, %.3f; %.3f, %.3f)" % (n, m, pb.left, pb.bottom, pb.right, pb.top))
    for c in cells:
        render(c, c.name + ".png")
        for tag, win in VIEWS.get(c.name, []):
            render(c, "%s_%s.png" % (c.name, tag), win)
    return cells


if __name__ == "__main__":
    write()
