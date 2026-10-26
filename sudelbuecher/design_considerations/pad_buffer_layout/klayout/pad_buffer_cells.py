# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Layout cells for the two pad buffers (d2s_mpdda in sg13cmos5l_IOPadDiff2Single, s2d_mpdda in
sg13cmos5l_IOPadSingle2Diff) and for their bias (d2s_bias_sel_pd: tree, Oguey-Aebischer core,
bandgap core). Proposal of design_considerations/pad_buffer_layout/layout_primitives.md, drawn.

Written 2026-10-26 by Claude (Opus 5.5) for Christoph Maier. Static cells, not PCells: every device
is an IHP SG13_dev PCell (pmosHV, nmosHV, rhigh, pnpMPA, ntap1, ptap1); what this script adds is drawn
geometry around them. The rules used are the PDK's (sg13cmos5l_tech_default.json); the values are
written where they are used.

How a row is built (row()):
  - every matched device is a single PCell finger (ng=1) or one PCell, placed left to right with
    0.6 um between Activ edges, all in the same orientation (left stripe first);
  - a poly bar 0.42 um above the tallest Activ joins the gates of consecutive devices on the same
    gate net, with one contact per gate and an M1 bar over the contacts;
  - a tie (ntap1 for PMOS, ptap1 for NMOS) runs under the row; stripes on the tie's net drop to it
    in M1, stripes on the device's own gate net (diodes) rise to the gate bar in M1;
  - nets that occur on two or more other stripes get an M2 trunk across the row (Via1 on an M1 pad
    0.29 x 0.29, trunks 0.29 wide on a 0.7 pitch); everything else gets an M1 pin;
  - one NWell + ThickGateOx + pSD rectangle over a PMOS row (and its tie), one ThickGateOx rectangle
    over an NMOS row (not over its tie).
block() puts two rows on one tie, the second mirrored about the tie's centre line, and joins their
M2 trunks and gate bars with M1 tracks left of the rows (M3 is the IO ring in the pad cell, so the
cells use Metal1 / Metal2 only).

Inside IIC-OSIC-TOOLS, after `source .designinit` (sets PDK_ROOT and PDK):
    python3 pad_buffer_cells.py   (or klayout -b -r pad_buffer_cells.py)
writes pad_buffer_cells.gds in the current directory.
"""
import os
import sys

pdk = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "ihp-sg13cmos5l"))
sys.path += [pdk + "/libs.tech/klayout/python",
             pdk + "/libs.tech/klayout/python/pycell4klayout-api/source/python"]
import pya
import sg13cmos5l_pycell_lib            # registers PCell library SG13_dev

ly = pya.Layout()
ly.dbu = 0.001
ly.technology_name = "sg13cmos5l"
LAY = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25),
       "Via1": (19, 0), "M2": (10, 0), "M2pin": (10, 2), "M2txt": (10, 25), "pSD": (14, 0), "NWell": (31, 0),
       "TGO": (44, 0), "TEXT": (63, 0)}
LI = {k: ly.layer(*v) for k, v in LAY.items()}


def g5(v):
    """IHP grid is 5 nm."""
    return round(v / 0.005) * 0.005


def box(c, lay, x0, y0, x1, y1):
    c.shapes(LI[lay]).insert(pya.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


def pin(c, metal, net, x0, y0, x1, y1):
    box(c, metal + "pin", x0, y0, x1, y1)
    c.shapes(LI[metal + "txt"]).insert(pya.DText(net, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))


def note(c, text, x, y):
    c.shapes(LI["TEXT"]).insert(pya.DText(text, g5(x), g5(y)))


_pc = {}
NETLIST = {}               # cell name -> CDL device lines (reference netlist for LVS)
MODEL = {"pmosHV": "sg13_hv_pmos", "nmosHV": "sg13_hv_nmos"}


def pcell(kind, **par):
    key = (kind, tuple(sorted(par.items())))
    if key not in _pc:
        _pc[key] = ly.create_cell(kind, "SG13_dev", par)
    return _pc[key]


def region(cell, lay):
    return pya.Region(cell.begin_shapes_rec(LI[lay])).merged()


def geom(cell):
    """Activ box, gate x ranges, S/D stripe x centres of a MOS PCell (um, cell coordinates)."""
    d = ly.dbu
    act = region(cell, "Activ").bbox()
    gates = sorted((p.bbox().left * d, p.bbox().right * d) for p in region(cell, "GatPoly").each())
    stripes = sorted((p.bbox().center().x * d) for p in region(cell, "M1").each()
                     if p.bbox().height() >= 0.9 * act.height())
    return pya.DBox(act.left * d, act.bottom * d, act.right * d, act.top * d), gates, stripes


GAP = 0.6                 # Activ to Activ inside a row (Act.b 0.21; pSD / TGO / NWell merged over the row)
TIE_P = (-1.60, -0.82)    # ntap Activ under a PMOS row: 0.42 from pSD (pSD.d 0.18)
TIE_N = (-1.80, -1.02)    # ptap Activ under an NMOS row: 0.50 from ThickGateOx (TGO.b 0.27)


def row(name, kind, devs, tie, tie_len=None):
    """devs: [(label, w, l, ng, gate_net, [stripe nets left to right])], w per finger * ng = total w.
    Returns (cell, info) with info = {'trunk': {net: y}, 'bar': {net: (x0, x1, y)}, 'x1': right end}."""
    c = ly.create_cell(name)
    parts = []
    for lab, w, l, ng, gnet, nets in devs:
        d = pcell(kind, w="%gu" % w, l="%gu" % l, ng=str(ng))
        parts.append((lab, d, gnet, nets) + geom(d))
    wmax = max(p[4].height() for p in parts)
    x = 0.0
    stripes, gates = [], []      # (x, y0, y1, net, dev index), (x0, x1, y1, gate net, dev index)
    for i, (lab, d, gnet, nets, act, gx, sx) in enumerate(parts):
        assert len(sx) == len(nets), (name, lab, sx, nets)
        tx, ty = x - act.left, wmax - act.top       # devices hang from the top: short gates stay short
        c.insert(pya.DCellInstArray(d.cell_index(), pya.DTrans(pya.DVector(g5(tx), g5(ty)))))
        stripes += [(tx + s_, ty + act.bottom, ty + act.top, n, i) for s_, n in zip(sx, nets)]
        gates += [(tx + a, tx + b, ty + act.top, gnet, i) for a, b in gx]
        note(c, lab, tx + act.left, wmax - act.height() / 2)
        x = tx + act.right + GAP
    x1 = x - GAP
    yb0, yb1 = wmax + 0.42, wmax + 0.78          # poly bar: 0.24 above the gate ends (Gat.b 0.18), 0.36 tall
    yc = (yb0 + yb1) / 2                         # contact 0.16, 0.10 poly around it (Cnt.d 0.07)
    info = {"trunk": {}, "bar": {}, "x1": x1}
    lines = []
    for i, (lab, d, gnet, nets, act, gx, sx) in enumerate(parts):
        w, l, ng = devs[i][1], devs[i][2], devs[i][3]
        sn, dn = nets[0], nets[1]
        lines.append("M%s_%s_%d %s %s %s %s %s w=%gu l=%gu ng=%d m=1" % (name, lab, i, dn, gnet, sn, tie, MODEL[kind], w, l, ng))
    NETLIST[name] = lines

    # gate bars: one per run of consecutive devices on the same gate net
    runs = []
    for g in gates:
        if runs and runs[-1][0] == g[3] and runs[-1][-1][4] in (g[4], g[4] - 1):
            runs[-1].append(g)
        else:
            runs.append([g[3], g])
    for r in runs:
        net, gs = r[0], r[1:]
        for a, b, W, _, _ in gs:
            m, h = (a + b) / 2, min(b - a, 0.5) / 2
            box(c, "GatPoly", m - h, W, m + h, yb0 + 0.01)
            box(c, "Cont", (a + b) / 2 - 0.08, yc - 0.08, (a + b) / 2 + 0.08, yc + 0.08)
        box(c, "GatPoly", gs[0][0], yb0, gs[-1][1], yb1)
        mx0, mx1 = (gs[0][0] + gs[0][1]) / 2 - 0.13, (gs[-1][0] + gs[-1][1]) / 2 + 0.13
        devidx = {g[4] for g in gs}
        for sxp, y0, y1, n, i in stripes:     # diodes: drain stripe up to the bar
            if n == net and i in devidx:
                box(c, "M1", sxp - 0.08, y1 - 0.05, sxp + 0.08, yc)
                mx0, mx1 = min(mx0, sxp - 0.13), max(mx1, sxp + 0.13)
        if mx1 - mx0 < 0.5:                  # M1.d: area >= 0.09 um2 (a one-gate bar would be 0.26 x 0.26)
            mx0, mx1 = (mx0 + mx1) / 2 - 0.25, (mx0 + mx1) / 2 + 0.25
        box(c, "M1", mx0, yc - 0.13, mx1, yc + 0.13)
        pin(c, "M1", net, mx0, yc - 0.13, mx0 + 0.3, yc + 0.13)
        info["bar"].setdefault(net, (mx0, mx1, yc))

    # tie under the row
    ty0, ty1 = TIE_P if kind == "pmosHV" else TIE_N
    t = pcell("ntap1" if kind == "pmosHV" else "ptap1", w="%gu" % g5(tie_len or x1), l="0.78u")
    c.insert(pya.DCellInstArray(t.cell_index(), pya.DTrans(pya.DVector(0, ty0))))
    tm = region(t, "M1").bbox()
    tm_top = ty0 + tm.top * ly.dbu
    pin(c, "M1", tie, tm.left * ly.dbu, ty0 + tm.bottom * ly.dbu, tm.left * ly.dbu + 0.4, tm_top)

    # stripes: to the tie, to a trunk, or a pin
    gate_of = {(i): g[3] for g in gates for i in [g[4]]}
    count = {}
    for sxp, y0, y1, n, i in stripes:
        if n != tie and n != gate_of[i]:
            count[n] = count.get(n, 0) + 1
    many = [n for n, k in sorted(count.items(), key=lambda kv: (-kv[1], kv[0])) if k >= 2]
    wtr = min([s[2] - s[1] for s in stripes if s[3] in many] or [0])
    ys = [wmax - wtr + 0.5 + 0.7 * k for k in range(40) if 0.5 + 0.7 * k <= wtr - 0.5]
    trunked = many[:len(ys)]
    for n, y in zip(trunked, ys):
        info["trunk"][n] = y
    xt = [sxp for sxp, y0, y1, n, i in stripes if n == tie]
    if xt:
        box(c, "M1", min(xt) - 0.08, ty0 + tm.bottom * ly.dbu, max(xt) + 0.08, tm_top)
    for sxp, y0, y1, n, i in stripes:        # M1.d: the PCell's stripes on a 0.5 um finger are 0.08 um2
        if y1 - y0 < 0.6:
            box(c, "M1", sxp - 0.08, y0 - 0.15, sxp + 0.08, y1)
    vias = {}
    for sxp, y0, y1, n, i in stripes:
        if n == tie:
            box(c, "M1", sxp - 0.08, tm_top - 0.1, sxp + 0.08, y0 + 0.05)
        elif n == gate_of[i]:
            pass
        elif n in info["trunk"]:
            y = info["trunk"][n]
            box(c, "M1", sxp - 0.145, y - 0.145, sxp + 0.145, y + 0.145)
            box(c, "Via1", sxp - 0.095, y - 0.095, sxp + 0.095, y + 0.095)
            vias.setdefault(n, []).append(sxp)
        else:
            pin(c, "M1", n, sxp - 0.08, (y0 + y1) / 2 - 0.25, sxp + 0.08, (y0 + y1) / 2 + 0.25)
    for n, xs in vias.items():
        y = info["trunk"][n]
        box(c, "M2", min(xs) - 0.145, y - 0.145, max(xs) + 0.145, y + 0.145)
        pin(c, "M2", n, min(xs) - 0.145, y - 0.145, min(xs) + 0.25, y + 0.145)
        info["trunk"][n] = (y, min(xs))

    # wells and implants (merged over the row)
    if kind == "pmosHV":
        box(c, "NWell", -0.62, ty0 - 0.62, x1 + 0.62, wmax + 0.62)     # NW.c1 / NW.e1 0.62 in TGO
        box(c, "TGO", -0.62, ty0 - 0.62, x1 + 0.62, wmax + 0.62)
        box(c, "pSD", -0.18, -0.40, x1 + 0.18, wmax + 0.40)
    else:
        box(c, "TGO", -0.27, -0.52, x1 + 0.27, wmax + 0.52)
    return c, info


def row_len(kind, devs):
    """Length of a row as row() lays it out (Activ of the first device to Activ of the last)."""
    acts = [geom(pcell(kind, w="%gu" % w, l="%gu" % l, ng=str(ng)))[0] for _, w, l, ng, _, _ in devs]
    return g5(sum(a.width() for a in acts) + GAP * (len(acts) - 1))


def block(name, kind, devs1, devs2, tie):
    """Two rows on one tie, the second mirrored about the tie centre; M2 trunks and gate bars of the
    same net joined by M1 tracks left of the rows (0.6 pitch)."""
    c = ly.create_cell(name)
    tl = max(row_len(kind, devs1), row_len(kind, devs2))
    r1, i1 = row(name + "_r1", kind, devs1, tie, tl)
    r2, i2 = row(name + "_r2", kind, devs2, tie, tl)
    ty0, ty1 = TIE_P if kind == "pmosHV" else TIE_N
    ym = ty0 + ty1                                   # mirror: y -> ym - y
    c.insert(pya.DCellInstArray(r1.cell_index(), pya.DTrans()))
    c.insert(pya.DCellInstArray(r2.cell_index(), pya.DTrans(pya.DTrans.M0, pya.DVector(0, ym))))
    NETLIST[name] = NETLIST[name + "_r1"] + NETLIST[name + "_r2"]
    k = 0
    for n in sorted(set(i1["trunk"]) & set(i2["trunk"])):
        (ya, xa), (yb, xb) = i1["trunk"][n], i2["trunk"][n]
        yb = ym - yb
        xt = -1.2 - 0.6 * k
        k += 1
        for y, xs in ((ya, xa), (yb, xb)):
            box(c, "M2", xt - 0.145, y - 0.145, xs, y + 0.145)
            box(c, "Via1", xt - 0.095, y - 0.095, xt + 0.095, y + 0.095)
            box(c, "M1", xt - 0.145, y - 0.145, xt + 0.145, y + 0.145)
        box(c, "M1", xt - 0.08, min(ya, yb), xt + 0.08, max(ya, yb))
    for n in sorted(set(i1["bar"]) & set(i2["bar"])):
        (a0, a1, ya), (b0, b1, yb) = i1["bar"][n], i2["bar"][n]
        yb = ym - yb
        xt = -1.2 - 0.6 * k
        k += 1
        box(c, "M1", xt - 0.13, ya - 0.13, a0 + 0.01, ya + 0.13)
        box(c, "M1", xt - 0.13, yb - 0.13, b0 + 0.01, yb + 0.13)
        box(c, "M1", xt - 0.13, min(ya, yb), xt + 0.13, max(ya, yb))
    return c


def mirror_map(rows, cols, pairs):
    """Positions of a rows x cols array, filled from the centre outward with pairs of devices at
    point-reflected positions: every group's centroid is the array centre. pairs: [(a, b)], one per
    reflected pair, a and b usually the same device (a group of odd size pairs once with 'dummy')."""
    pos = [(r, c) for r in range(rows) for c in range(cols)]
    rc, cc = (rows - 1) / 2, (cols - 1) / 2
    pos.sort(key=lambda p: ((p[0] - rc) ** 2 + (p[1] - cc) ** 2, p))
    grid = [[None] * cols for _ in range(rows)]
    k = 0
    for r, c in pos:
        if grid[r][c] is None:
            grid[r][c], grid[rows - 1 - r][cols - 1 - c] = pairs[k]
            k += 1
    assert k == len(pairs) and all(all(line) for line in grid), (k, len(pairs))
    return grid


cells = {}

# ======================================================================================
# 1. Input device in its own well (P1): hv PMOS 2 x 10/1, well = source, used by every unit_r2
# ======================================================================================
tub, tub_i = row("tub_p20x1", "pmosHV", [("M", 20, 1, 2, "g", ["s", "d", "s"])], "s")
tubd, _ = row("tub_p20x1_dummy", "pmosHV", [("Mdummy", 20, 1, 2, "s", ["s", "s", "s"])], "s")
# dummy: gate, drains and sources on the well net (diode rule and tie rule of row() do it)

TUB_PX, TUB_PY = 4.30 + 1.8, 13.0 + 1.8      # tub NWell 4.30 x (10.62 + 2.22); NW.b1 1.8 between wells


def tub_array(name, grid, nets):
    """grid[r][c] = device name ('dummy' = dummy tub); nets[name] = (g, d, s). Labels the nets of
    every tub on M1 (TEXT copy on 63/0) so the array documents the netlist."""
    c = ly.create_cell(name)
    for r, line in enumerate(grid):
        for k, dev in enumerate(line):
            x, y = k * TUB_PX, -r * TUB_PY
            cc = tubd if dev == "dummy" else tub
            c.insert(pya.DCellInstArray(cc.cell_index(), pya.DTrans(pya.DVector(x, y))))
            note(c, dev, x, y + 11.2)
            if dev != "dummy":
                g, d, s = nets[dev]
                note(c, "g=%s d=%s s=%s" % (g, d, s), x, y - 2.8)
    return c


# unit half 'a' = device on gp (drains to y), 'b' = device on gn (drains to x); s = sa / sb of the unit
d2s_units = {"A": ("vinp", "vref"), "B": ("vref", "vinn"), "C1": ("vref", "vfb"), "C2": ("vref", "vfb")}
s2d_units = {"A1": ("vin", "vref"), "A2": ("vin", "vref"), "F1": ("vcm", "vfbp"), "F2": ("vfbn", "vcm")}
s2d_cmfb = {"M1": ("vfbp", "vcm"), "M2": ("vfbn", "vcm")}


def unit_nets(units, x="x", y="y"):
    n = {}
    for u, (gp, gn) in units.items():
        n[u + "a"] = (gp, y, "sa_" + u)
        n[u + "b"] = (gn, x, "sb_" + u)
    return n


# 2 x 4 cross-coupled map of layout_primitives.md section 5, with dummies at both ends
d2s_map = [["dummy", "Aa", "C2b", "C1b", "Ba", "dummy"],
           ["dummy", "Bb", "C1a", "C2a", "Ab", "dummy"]]
cells["d2s_inputs"] = tub_array("d2s_inputs", d2s_map, unit_nets(d2s_units))
s2d_map = [["dummy", "A1a", "F2b", "F1b", "A2a", "M1a", "M2b", "dummy"],
           ["dummy", "A2b", "F1a", "F2a", "A1b", "M1b", "M2a", "dummy"]]
s2d_nets = unit_nets(s2d_units)
s2d_nets.update(unit_nets(s2d_cmfb, x="xc", y="yc"))
cells["s2d_inputs"] = tub_array("s2d_inputs", s2d_map, s2d_nets)

# ======================================================================================
# 2. Tails (P2): hv PMOS 5/6 in one well on vdd, gate vbp; BP (bias diode, same device) at an end
# ======================================================================================


def tails(name, grid):
    devs = []
    for line in grid:
        d = []
        for dev in line:
            if dev == "dummy":
                d.append(("Tdummy", 5, 6, 1, "vbp", ["vdd", "vdd"]))
            elif dev == "BP":
                d.append(("BP", 5, 6, 1, "vbp", ["vdd", "vbp"]))
            else:
                d.append(("T" + dev, 5, 6, 1, "vbp", ["vdd", ("sa_" if dev[-1] == "a" else "sb_") + dev[:-1]]))
        devs.append(d)
    return block(name, "pmosHV", devs[0], devs[1], "vdd")


cells["d2s_tails"] = tails("d2s_tails", [["dummy", "Aa", "C2b", "C1b", "Ba", "BP"],
                                         ["dummy", "Bb", "C1a", "C2a", "Ab", "dummy"]])
cells["s2d_tails"] = tails("s2d_tails", [["dummy", "A1a", "F2b", "F1b", "A2a", "M1a", "M2b", "BP"],
                                         ["dummy", "A2b", "F1a", "F2a", "A1b", "M1b", "M2a", "dummy"]])

# ======================================================================================
# 3. Degeneration resistors (P3): each 150 kOhm as 4 series rhigh segments 0.5 x 12.65 um,
#    interleaved mirror-symmetric, nested M2 jumpers above (top heads) and below (bottom heads)
# ======================================================================================
RSEG = 12.65
RPITCH = 1.4               # rhigh body 0.5, SalBlock 0.2 around it (Sal.b 0.42 between)


def rblock(name, units):
    """units u_0 .. u_{n-1}: sequence (u_0..u_{n-1} u_{n-1}..u_0) twice, dummies at both ends. Unit j sits
    at j, 2n-1-j, 2n+j, 4n-1-j; its chain is top(j, 2n-1-j), bottom(2n-1-j, 2n+j), top(2n+j, 4n-1-j),
    ends at the bottom heads of j and 4n-1-j. Jumpers are nested, innermost lowest: top track
    n-2-j, bottom track j-1; neighbours are joined in M1. The ends drop below all bottom tracks."""
    c = ly.create_cell(name)
    n = len(units)
    seq = ["dummy"] + units + units[::-1] + units + units[::-1] + ["dummy"]
    seg = pcell("rhigh", w="0.5u", l="%gu" % RSEG, b="0")
    heads = sorted((p.bbox().center().y * ly.dbu, p.bbox().center().x * ly.dbu) for p in region(seg, "M1").each())
    (hb, hx), (ht, _) = heads[0], heads[-1]
    for k, u in enumerate(seq):
        c.insert(pya.DCellInstArray(seg.cell_index(), pya.DTrans(pya.DVector(k * RPITCH, 0))))
        note(c, u, k * RPITCH, RSEG / 2)
    X = lambda k: (k + 1) * RPITCH + hx           # position k of the 4n (dummy at -1)

    def jumper(ka, kb, yh, sgn, lvl):
        xa, xb = X(ka), X(kb)
        if kb - ka == 1:
            box(c, "M1", xa - 0.23, yh - 0.13, xb + 0.23, yh + 0.13)
            return
        yt = yh + sgn * (0.8 + 0.6 * lvl)
        for xx in (xa, xb):
            box(c, "Via1", xx - 0.095, yh - 0.095, xx + 0.095, yh + 0.095)
            box(c, "M2", xx - 0.145, min(yh, yt) - 0.145, xx + 0.145, max(yh, yt) + 0.145)
        box(c, "M2", xa - 0.145, yt - 0.145, xb + 0.145, yt + 0.145)

    yend = hb - 0.8 - 0.6 * n
    for j, u in enumerate(units):
        jumper(j, 2 * n - 1 - j, ht, 1, n - 2 - j)
        jumper(2 * n + j, 4 * n - 1 - j, ht, 1, n - 2 - j)
        jumper(2 * n - 1 - j, 2 * n + j, hb, -1, j - 1)
        for k, s_ in ((j, "sa_"), (4 * n - 1 - j, "sb_")):
            xx = X(k)
            box(c, "Via1", xx - 0.095, hb - 0.095, xx + 0.095, hb + 0.095)
            box(c, "M2", xx - 0.145, yend, xx + 0.145, hb + 0.145)
            pin(c, "M2", s_ + u, xx - 0.145, yend, xx + 0.145, yend + 0.4)
    # substrate tie (vss) under the block, below the end pins; the rhigh bulk is the substrate
    yt1 = yend - 0.6
    t = pcell("ptap1", w="%gu" % g5((4 * n + 2) * RPITCH + 2.4), l="0.78u")    # under both dummy straps
    c.insert(pya.DCellInstArray(t.cell_index(), pya.DTrans(pya.DVector(-1.2, g5(yt1 - 0.78)))))
    tm = region(t, "M1").bbox()
    ytm = yt1 - 0.78 + tm.top * ly.dbu
    pin(c, "M1", "vss", -1.2 + tm.left * ly.dbu, yt1 - 0.78 + tm.bottom * ly.dbu, -1.2 + tm.left * ly.dbu + 0.4, ytm)
    for k, side in ((-1, -1), (4 * n, 1)):           # dummies: both heads shorted, down to the tie
        xo = X(k) + side * 0.55
        box(c, "M1", min(X(k), xo) - 0.08, hb - 0.13, max(X(k), xo) + 0.08, hb + 0.13)
        box(c, "M1", min(X(k), xo) - 0.08, ht - 0.13, max(X(k), xo) + 0.08, ht + 0.13)
        box(c, "M1", xo - 0.08, ytm - 0.1, xo + 0.08, ht + 0.13)
    lines = []
    for j, u in enumerate(units):
        ks = [j, 2 * n - 1 - j, 2 * n + j, 4 * n - 1 - j]
        nodes = ["sa_" + u, u + "_t1", u + "_b2", u + "_t3", "sb_" + u]
        for q in range(4):
            lines.append("R%s_%s_%d %s %s vss rhigh w=0.5u l=%gu m=1 b=0" % (name, u, q, nodes[q], nodes[q + 1], RSEG))
    lines += ["R%s_dummy_%d vss vss vss rhigh w=0.5u l=%gu m=1 b=0" % (name, q, RSEG) for q in range(2)]
    NETLIST[name] = lines
    return c


cells["d2s_rhigh"] = rblock("d2s_rhigh", ["A", "B", "C1", "C2"])
cells["s2d_rhigh"] = rblock("s2d_rhigh", ["A1", "A2", "F1", "F2", "M1", "M2"])

# ======================================================================================
# 4. Fold sinks (P4): hv NMOS 6/6 single fingers, gate vbn, BN (bias diode, same finger) at an end.
#    SX / SY 6 + 6 fingers: X Y Y X X Y / Y X X Y Y X. Shared by both pads (d2s at ng=6, see
#    sink_6x6/results_sink_6x6.md); s2d's CMFB sinks SXC / SYC 4 + 4 in their own block.
# ======================================================================================


def nfing(lab, net, gate="vbn", w=6, l=6):
    return (lab, w, l, 1, gate, ["vss", net])


def sinks(name, r1, r2):
    tr = {"X": "x", "Y": "y", "XC": "xc", "YC": "yc"}
    mk = lambda line: [nfing("dummy", "vss") if d == "dummy" else nfing("BN", "vbn") if d == "BN"
                       else nfing("S" + d, tr[d]) for d in line]
    return block(name, "nmosHV", mk(r1), mk(r2), "vss")


cells["sinks_6x6"] = sinks("sinks_6x6", ["dummy", "X", "Y", "Y", "X", "X", "Y", "BN"],
                           ["dummy", "Y", "X", "X", "Y", "Y", "X", "dummy"])
cells["s2d_sinks_cmfb"] = sinks("s2d_sinks_cmfb", ["dummy", "XC", "YC", "YC", "XC", "dummy"],
                                ["dummy", "YC", "XC", "XC", "YC", "dummy"])

# ======================================================================================
# 5. PMOS loads (P5): hv PMOS 6/4 fingers in one well on vdd
# ======================================================================================
pf = lambda lab, net, gate: (lab, 6, 4, 1, gate, ["vdd", net])
pd = lambda gate: ("dummy", 6, 4, 1, gate, ["vdd", "vdd"])
d2s_l = {"L": ("PL", "pl"), "R": ("PR", "pr")}
cells["d2s_loads"], _ = row("d2s_loads", "pmosHV",
                            [pd("l2")] + [pf(d2s_l[k][0], d2s_l[k][1], "l2") for k in "LRRLLRRL"] + [pd("l2")], "vdd")
s2d_l = {"P": ("LP", "lp"), "N": ("LN", "ln"), "D": ("D", "dd")}
cells["s2d_loads"], _ = row("s2d_loads", "pmosHV",
                            [pd("vcmfb")] + [pf(s2d_l[k][0], s2d_l[k][1], "vcmfb") for k in "PNDDNPPNDDNP"] + [pd("vcmfb")], "vdd")

# ======================================================================================
# 6. Cascodes (P6): 15/3 fingers (lcas = 3), next to the device they cascode. BNC (1/8, diode
#    vbnc) and BPC (1/4, diode vbpc) sit in the cascode rows, on the same gate line.
# ======================================================================================
cn = lambda lab, s, d: (lab, 15, 3, 1, "vbnc", [s, d])
cp = lambda lab, s, d: (lab, 15, 3, 1, "vbpc", [s, d])
cells["d2s_casc_n"], _ = row("d2s_casc_n", "nmosHV",
                             [cn("CX", "x", "l1"), cn("CY", "y", "b"), cn("CY", "y", "b"), cn("CX", "x", "l1"),
                              ("BNC", 1, 8, 1, "vbnc", ["vss", "vbnc"])], "vss")
cells["d2s_casc_p"], _ = row("d2s_casc_p", "pmosHV",
                             [cp("PCL", "pl", "l2"), cp("PCR", "pr", "a"), cp("PCR", "pr", "a"), cp("PCL", "pl", "l2"),
                              ("BPC", 1, 4, 1, "vbpc", ["vdd", "vbpc"])], "vdd")
cells["s2d_casc_n"], _ = row("s2d_casc_n", "nmosHV",
                             [cn("CX", "x", "voutp"), cn("CY", "y", "voutn"), cn("CY", "y", "voutn"), cn("CX", "x", "voutp"),
                              cn("CXC", "xc", "vcmfb"), cn("CYC", "yc", "vdd"), cn("CYC", "yc", "vdd"), cn("CXC", "xc", "vcmfb"),
                              ("BNC", 1, 8, 1, "vbnc", ["vss", "vbnc"])], "vss")
cells["s2d_casc_p"], _ = row("s2d_casc_p", "pmosHV",
                             [cp("LPC", "lp", "voutp"), cp("LNC", "ln", "voutn"), cp("DC", "dd", "vcmfb"),
                              cp("DC", "dd", "vcmfb"), cp("LNC", "ln", "voutn"), cp("LPC", "lp", "voutp"),
                              ("BPC", 1, 4, 1, "vbpc", ["vdd", "vbpc"])], "vdd")

# ======================================================================================
# 7. Class-AB groups (P7, d2s only): the output-device finger. RP1 / RN1 belong into the clamp
#    frames (proposal); here they stand next to RP2 / RN2 as the fall-back.
# ======================================================================================
cells["d2s_ab_p"], _ = row("d2s_ab_p", "pmosHV",
                           [("RP1", 6.66, 0.6, 1, "n1", ["vdd", "n1"]), ("RP1", 6.66, 0.6, 1, "n1", ["vdd", "n1"]),
                            ("RP2", 6.66, 0.6, 1, "vabp", ["n1", "vabp"]), ("FPL", 6.66, 0.6, 1, "vabp", ["l2", "l1"]),
                            ("ABP", 6.66, 0.6, 1, "vabp", ["a", "b"])], "vdd")
cells["d2s_ab_n"], _ = row("d2s_ab_n", "nmosHV",
                           [("RN1", 4.4, 1, 1, "n2", ["vss", "n2"]), ("RN1", 4.4, 1, 1, "n2", ["vss", "n2"]),
                            ("RN2", 4.4, 1, 1, "vabn", ["n2", "vabn"]), ("FNL", 4.4, 1, 1, "vabn", ["l1", "l2"]),
                            ("ABN", 4.4, 1, 1, "vabn", ["b", "a"])], "vss")

# ======================================================================================
# 8. MOS capacitors (P9) and power-down switches
# ======================================================================================
cells["d2s_cma"], _ = row("d2s_cma", "pmosHV", [("CMA", 16, 16, 1, "a", ["vout", "vout"])], "vout")
cells["d2s_cmb"], _ = row("d2s_cmb", "pmosHV", [("CMB", 16, 16, 1, "vout", ["b", "b"])], "b")
cells["s2d_cload"], _ = row("s2d_cload", "nmosHV", [("CLP", 12, 12, 1, "voutp", ["vss", "vss"]),
                                                    ("CLN", 12, 12, 1, "voutn", ["vss", "vss"])], "vss")
cells["d2s_pd_p"], _ = row("d2s_pd_p", "pmosHV", [("SA", 1, 0.45, 1, "en_3v3", ["vdd", "a"]),
                                                  ("SABP", 1, 0.45, 1, "en_3v3", ["vdd", "vabp"])], "vdd")
cells["d2s_pd_n"], _ = row("d2s_pd_n", "nmosHV", [("SB", 1, 0.45, 1, "en_3v3_b", ["vss", "b"]),
                                                  ("SABN", 1, 0.45, 1, "en_3v3_b", ["vss", "vabn"])], "vss")
cells["s2d_pd_n"], _ = row("s2d_pd_n", "nmosHV", [("TPN", 1, 0.45, 1, "en_3v3_b", ["voutp", "vcm"]),
                                                  ("TNN", 1, 0.45, 1, "en_3v3_b", ["voutn", "vcm"])], "vss")
cells["s2d_pd_p"], _ = row("s2d_pd_p", "pmosHV", [("TPP", 1, 0.45, 1, "en_3v3", ["voutp", "vcm"]),
                                                  ("TNP", 1, 0.45, 1, "en_3v3", ["voutn", "vcm"])], "vdd")

# ======================================================================================
# 9. Bias tree (d2s_bias_in_tree_pd without BP / BN, which live in the tail and sink rows)
# ======================================================================================
cells["bias_tree_n"], _ = row("bias_tree_n", "nmosHV",
                              [("dummy", 6, 6, 1, "ni", ["vss", "vss"]), ("NBP", 6, 6, 1, "ni", ["vss", "vbp"]),
                               ("NI", 6, 6, 1, "ni", ["vss", "ni"]), ("NABP", 6, 6, 1, "ni", ["vss", "vabp"]),
                               ("dummy", 6, 6, 1, "ni", ["vss", "vss"]), ("NBPC", 2.4, 6, 1, "ni", ["vss", "vbpc"])], "vss")
cells["bias_tree_p"], _ = row("bias_tree_p", "pmosHV",
                              [("dummy", 5, 6, 1, "vbp", ["vdd", "vdd"]), ("PBN", 5, 6, 1, "vbp", ["vdd", "vbn"]),
                               ("PABN", 5, 6, 1, "vbp", ["vdd", "vabn"]), ("dummy", 5, 6, 1, "vbp", ["vdd", "vdd"]),
                               ("PBNC", 2, 6, 1, "vbp", ["vdd", "vbnc"])], "vdd")
cells["bias_tree_sw"], _ = row("bias_tree_sw", "nmosHV",
                               [("TGN", 1, 0.45, 1, "en_3v3", ["iref", "ni"]), ("TDN", 1, 0.45, 1, "en_3v3_b", ["vss", "ni"])], "vss")
cells["bias_tree_swp"], _ = row("bias_tree_swp", "pmosHV", [("TGP", 1, 0.45, 1, "en_3v3_b", ["iref", "ni"])], "vdd")

# ======================================================================================
# 10. Oguey-Aebischer core (oa_core_pd). Matched groups wired; start-up / power-down devices placed.
#     M10 / M11 as 10 um fingers (PCell finger limit 10 um): netlist ng 8 -> 18 and 4 -> 9.
# ======================================================================================


def grid_rows(grid, mk):
    return [[mk(d) for d in line] for line in grid]


P8, PO = ("P8", "P8"), ("PO", "PO")
oa_g = mirror_map(4, 8, [("P0", "dummy"), ("P2", "P2"), P8, PO, PO, P8, PO, PO, P8, PO, PO, P8, PO, PO, PO, PO])
oa_net = {"P0": "vpg", "P2": "c2", "P8": "c8", "PO": "co", "dummy": "vdd"}
mkp = lambda d: (d, 2, 8, 1, "vpg", ["vdd", oa_net[d]])
rows_ = grid_rows(oa_g, mkp)
cells["oa_pmir_a"] = block("oa_pmir_a", "pmosHV", rows_[0], rows_[1], "vdd")
cells["oa_pmir_b"] = block("oa_pmir_b", "pmosHV", rows_[2], rows_[3], "vdd")
cells["oa_pcas"], _ = row("oa_pcas", "pmosHV",
                          [("POC", 2, 2, 1, "vpc", ["co", "iout"])] * 2 + [("P8C", 2, 2, 1, "vpc", ["c8", "vnc"])] +
                          [("POC", 2, 2, 1, "vpc", ["co", "iout"])] + [("P0C", 0.5, 2, 1, "vpc", ["vpg", "vpc"])] +
                          [("P2C", 1, 2, 1, "vpc", ["c2", "vbr"])] + [("POC", 2, 2, 1, "vpc", ["co", "iout"])] +
                          [("P8C", 2, 2, 1, "vpc", ["c8", "vnc"])] + [("POC", 2, 2, 1, "vpc", ["co", "iout"])], "vdd")
M10, M11 = ("M10", "M10"), ("M11", "M11")
oa_n = mirror_map(2, 14, [("M11", "dummy"), M10, M10, M11, M10, M10, M11, M10, M10, M11, M10, M10, M11, M10])
mkn = lambda d: {"M11": ("M11", 10, 1, 1, "vnc", ["vss", "vnc"]), "M10": ("M10", 10, 1, 1, "vnc", ["vres", "d10"]),
                 "dummy": ("dummy", 10, 1, 1, "vnc", ["vss", "vss"])}[d]
rows_ = grid_rows(oa_n, mkn)
cells["oa_nmir"] = block("oa_nmir", "nmosHV", rows_[0], rows_[1], "vss")
cells["oa_mcs"], _ = row("oa_mcs", "nmosHV", [("MCS", 3.4, 30, 1, "vbr", ["vss", "vbr"]),
                                             ("MCL", 3.4, 30, 1, "vbr", ["vss", "vres"])], "vss")
cells["oa_misc_n"], _ = row("oa_misc_n", "nmosHV",
                            [("MC10", 10, 1, 1, "vbr", ["d10", "vpc"]), ("MS2", 10, 1, 1, "vbr", ["vss", "ks"]),
                             ("MS3", 0.5, 2, 1, "ks", ["vss", "vpc"]), ("SKS", 1, 0.45, 1, "en_3v3_b", ["vss", "ks"])], "vss")
# MS1 0.5/100 does not fit an 80 um cell as one device: 8 x 0.5/12.5 in series (netlist change)
ms1 = [("MS1_%d" % k, 0.5, 12.5, 1, "en_3v3_b", ["vdd" if k == 0 else "ms%d" % k, "ks" if k == 7 else "ms%d" % (k + 1)])
       for k in range(8)]
cells["oa_misc_p"] = block("oa_misc_p", "pmosHV", ms1[:4], ms1[4:] + [("SVPG", 1, 0.45, 1, "en_3v3", ["vdd", "vpg"])], "vdd")

# ======================================================================================
# 11. Bandgap core (bg_core_pd). PMOS mirror and cascodes 10/1 fingers, NA / NB 2 x 10/4,
#     Q1 in the middle of 8 Q2, R1A / R1B / R0 as 9.94 um segments, interleaved.
# ======================================================================================
PB, PA, PO = ("PB", "PB"), ("PA", "PA"), ("PO", "PO")
bg_g = mirror_map(2, 9, [PB, PA, PO, PO, PB, PA, PO, PO, ("dummy", "dummy")])
bg_net = {"PB": "vpg", "PA": "ca", "PO": "co", "dummy": "vdd"}
rows_ = grid_rows(bg_g, lambda d: (d, 10, 1, 1, "vpg", ["vdd", bg_net[d]]))
cells["bg_pmir"] = block("bg_pmir", "pmosHV", rows_[0], rows_[1], "vdd")
bc_net = {"PB": ("vpg", "vpc"), "PA": ("ca", "g"), "PO": ("co", "iout"), "dummy": ("vdd", "vdd")}
rows_ = grid_rows(bg_g, lambda d: (d.replace("P", "P") + "C" if d != "dummy" else d, 10, 1, 1, "vpc", list(bc_net[d])))
cells["bg_pcas"] = block("bg_pcas", "pmosHV", rows_[0], rows_[1], "vdd")
cells["bg_nab"], _ = row("bg_nab", "nmosHV",
                         [("dummy", 10, 4, 1, "g", ["vss", "vss"]), ("NA", 10, 4, 1, "g", ["ea", "g"]),
                          ("NB", 10, 4, 1, "g", ["eb", "vpc"]), ("NB", 10, 4, 1, "g", ["eb", "vpc"]),
                          ("NA", 10, 4, 1, "g", ["ea", "g"]), ("dummy", 10, 4, 1, "g", ["vss", "vss"])], "vss")
cells["bg_misc_n"], _ = row("bg_misc_n", "nmosHV",
                            [("MS2", 10, 1, 1, "g", ["vss", "ks"]), ("MS3", 0.5, 2, 1, "ks", ["vss", "vpc"]),
                             ("SKS", 1, 0.45, 1, "en_3v3_b", ["vss", "ks"])], "vss")
cells["bg_misc_p"] = block("bg_misc_p", "pmosHV", ms1[:4], ms1[4:] + [("SVPG", 1, 0.45, 1, "en_3v3", ["vdd", "vpg"])], "vdd")

# PNPs: 3 x 3, Q1 in the middle (placed, not wired: emitters ea (Q1) / e2 (Q2), base and collector vss)
pnp = pcell("pnpMPA", w="2u", l="2u")
pb = pnp.dbbox()
c = ly.create_cell("bg_pnp")
for r in range(3):
    for k in range(3):
        x, y = k * (pb.width() + 1.0) - pb.left, -r * (pb.height() + 1.0) - pb.bottom
        c.insert(pya.DCellInstArray(pnp.cell_index(), pya.DTrans(pya.DVector(g5(x), g5(y)))))
        note(c, "Q1 (ea)" if (r, k) == (1, 1) else "Q2 (e2)", x + pb.left, y + pb.top + 0.3)
cells["bg_pnp"] = c

# Resistors: R1A 11, R1B 10, R0 18 segments of 9.94 um (R0 178.9 um instead of 179.5, -0.33 %),
# mirror-symmetric sequence, dummies at the ends; placed with head labels, series wiring not drawn.
seg = pcell("rhigh", w="0.5u", l="9.94u", b="0")
half = ["R0", "R1A", "R0", "R1B", "R0", "R1A", "R0", "R1B", "R0", "R1A", "R1B", "R0", "R1A", "R0", "R1B", "R0", "R1A", "R0", "R1B"]
seq = half + ["R1A"] + half[::-1]
assert (seq.count("R1A"), seq.count("R1B"), seq.count("R0")) == (11, 10, 18), (seq.count("R1A"), seq.count("R1B"), seq.count("R0"))
seq = ["dummy"] + seq + ["dummy"]
c = ly.create_cell("bg_res")
cnt = {}
for k, u in enumerate(seq):
    c.insert(pya.DCellInstArray(seg.cell_index(), pya.DTrans(pya.DVector(k * RPITCH, 0))))
    cnt[u] = cnt.get(u, 0) + 1
    note(c, "%s.%d" % (u, cnt[u]), k * RPITCH, 5.0)
cells["bg_res"] = c

# ======================================================================================
# Library top: every cell, in three columns (d2s / shared / s2d) with titles; outline of the
# 80 x 94 um zone above the clamp frames (y = 84 ... 178 in the pad cell) for scale.
# ======================================================================================
top = ly.create_cell("pad_buffer_cells")
cols = [("d2s (sg13cmos5l_IOPadDiff2Single)", ["d2s_inputs", "d2s_tails", "d2s_rhigh", "sinks_6x6", "d2s_loads",
                                               "d2s_casc_n", "d2s_casc_p", "d2s_ab_p", "d2s_ab_n", "d2s_cma", "d2s_cmb",
                                               "d2s_pd_p", "d2s_pd_n"]),
        ("s2d (sg13cmos5l_IOPadSingle2Diff)", ["s2d_inputs", "s2d_tails", "s2d_rhigh", "sinks_6x6", "s2d_sinks_cmfb",
                                               "s2d_loads", "s2d_casc_n", "s2d_casc_p", "s2d_cload", "s2d_pd_n", "s2d_pd_p"]),
        ("bias (d2s_bias_sel_pd)", ["bias_tree_n", "bias_tree_p", "bias_tree_sw", "bias_tree_swp", "oa_pmir_a", "oa_pmir_b",
                                    "oa_pcas", "oa_nmir", "oa_mcs", "oa_misc_n", "oa_misc_p", "bg_pmir", "bg_pcas",
                                    "bg_nab", "bg_misc_n", "bg_misc_p", "bg_pnp", "bg_res"])]
X = 0.0
for title, names in cols:
    Y = 0.0
    note(top, title, X, 6.0)
    w = 0.0
    for n in names:
        cc = cells[n]
        b = cc.dbbox()
        top.insert(pya.DCellInstArray(cc.cell_index(), pya.DTrans(pya.DVector(g5(X - b.left), g5(Y - b.top)))))
        note(top, n, X, Y + 1.0)
        Y -= b.height() + 8.0
        w = max(w, b.width())
    X += w + 30.0
z = ly.create_cell("zone_80x94")
for x0, y0, x1, y1 in ((0, 0, 80, 0.2), (0, 93.8, 80, 94), (0, 0, 0.2, 94), (79.8, 0, 80, 94)):
    box(z, "TEXT", x0, y0, x1, y1)
note(z, "pad cell above the clamp frames: 80 x 94 um (y 84 ... 178)", 1, 95)
top.insert(pya.DCellInstArray(z.cell_index(), pya.DTrans(pya.DVector(g5(X), -94))))

def pack(name, names, width=80.0, gap=2.0):
    """First-fit-decreasing shelf packing of cells into a strip 'width' wide, 'gap' between bounding
    boxes (bounding boxes include wells and ThickGateOx). A fit check, not a floorplan: no wiring."""
    c = ly.create_cell(name)
    items = sorted(names, key=lambda n: -cells[n].dbbox().height())
    shelves = []                                      # [y_top, height, x_used]
    y = 0.0
    for n in items:
        b = cells[n].dbbox()
        sh = next((s_ for s_ in shelves if s_[2] + gap + b.width() <= width), None)
        if sh is None:
            sh = [y, b.height(), -gap]
            shelves.append(sh)
            y -= b.height() + gap
        x = sh[2] + gap
        c.insert(pya.DCellInstArray(cells[n].cell_index(), pya.DTrans(pya.DVector(g5(x - b.left), g5(sh[0] - b.top)))))
        note(c, n, x, sh[0] - 0.5)
        sh[2] = x + b.width()
    h = -y - gap
    for x0, y0, x1, y1 in ((0, 0, width, 0.2), (0, -94, width, -93.8), (0, -94, 0.2, 0), (width - 0.2, -94, width, 0)):
        box(c, "TEXT", x0, y0, x1, y1)
    note(c, "%s: %.1f um tall in %.0f um width (zone: 94 um)" % (name, h, width), 0, 1.5)
    print("%-22s %5.1f um tall in %.0f um (zone above the frames: 94 um)" % (name, h, width))
    return c


d2s_front = ["d2s_inputs", "d2s_tails", "d2s_rhigh", "sinks_6x6", "d2s_loads", "d2s_casc_n", "d2s_casc_p",
             "d2s_ab_p", "d2s_ab_n", "d2s_pd_p", "d2s_pd_n"]
s2d_front = ["s2d_inputs", "s2d_tails", "s2d_rhigh", "sinks_6x6", "s2d_sinks_cmfb", "s2d_loads", "s2d_casc_n",
             "s2d_casc_p", "s2d_pd_n", "s2d_pd_p"]
fits = [pack("fit_d2s_front", d2s_front), pack("fit_d2s_front_caps", d2s_front + ["d2s_cma", "d2s_cmb"]),
        pack("fit_s2d_front", s2d_front), pack("fit_s2d_front_caps", s2d_front + ["s2d_cload"]),
        pack("fit_bias_tree_oa_bg", ["bias_tree_n", "bias_tree_p", "bias_tree_sw", "bias_tree_swp", "oa_pmir_a",
                                     "oa_pmir_b", "oa_pcas", "oa_nmir", "oa_mcs", "oa_misc_n", "oa_misc_p", "bg_pmir",
                                     "bg_pcas", "bg_nab", "bg_misc_n", "bg_misc_p", "bg_pnp", "bg_res"])]
x = top.dbbox().right + 40
for f_ in fits:
    top.insert(pya.DCellInstArray(f_.cell_index(), pya.DTrans(pya.DVector(g5(x), 0))))
    x += 120

for n in ["d2s_inputs", "s2d_inputs", "d2s_tails", "s2d_tails", "d2s_rhigh", "s2d_rhigh", "sinks_6x6", "s2d_sinks_cmfb",
          "d2s_loads", "s2d_loads", "d2s_casc_n", "d2s_casc_p", "s2d_casc_n", "s2d_casc_p", "d2s_ab_p", "d2s_ab_n",
          "bias_tree_n", "bias_tree_p", "oa_pmir_a", "oa_nmir", "bg_pmir", "bg_pcas", "bg_pnp", "bg_res"]:
    b = cells[n].dbbox()
    print("%-16s %6.1f x %6.1f um" % (n, b.width(), b.height()))
ly.write("pad_buffer_cells.gds")
with open("pad_buffer_cells.cdl", "w") as f:
    f.write("* Reference netlists of the wired cells in pad_buffer_cells.gds, written by pad_buffer_cells.py.\n"
            "* One .SUBCKT per cell; pins are the labelled nets. Dummies are listed (S = D or shorted).\n")
    for n, lines in sorted(NETLIST.items()):
        if n.endswith(("_r1", "_r2")):
            continue
        nets = set()
        for l_ in lines:
            t_ = l_.split()
            nets.update(t_[1:5] if l_.startswith("M") else t_[1:4])
        pins = sorted(x_ for x_ in nets if not (("_t1" in x_) or ("_b2" in x_) or ("_t3" in x_)))
        f.write("\n.SUBCKT %s %s\n%s\n.ENDS %s\n" % (n, " ".join(pins), "\n".join(lines), n))
