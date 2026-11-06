# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Row builder for hv MOS rows of IHP SG13_dev PCells.

Copied unchanged (lines 31..207) from sudel_buecher
`sudelbuecher/design_considerations/pad_buffer_layout/klayout/pad_buffer_cells.py`
(sha256 c3361d8d048cc166e694afabcef15136ed2d2dea2f89021116b1cf6b3a22ea43, written 2026-10-26 by Claude for
Christoph Maier; its cells are DRC clean and LVS matched with IHP's decks, see its verification.md).
Only this docstring is new. Import it; `ly` is the shared layout.
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

