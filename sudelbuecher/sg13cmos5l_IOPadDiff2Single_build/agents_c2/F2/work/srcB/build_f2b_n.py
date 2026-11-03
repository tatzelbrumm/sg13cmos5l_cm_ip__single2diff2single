# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 (C2, 2026-11-03), stage B: the NMOS / R cells after Christoph's review of the stage-A placement.

    python3 build_f2b_n.py <out.gds> <out.cdl>

Builds on build_f2_n.py (stage A, which executes N2's build script as a library). Changes against stage A:
  sinks_6x6_f2    no center gate-contact columns: the 0.85 um gaps beside BN / its twin T closed to 0.25 (Gat_b1),
                  rows still mirror images, the same end dummies; BN's drain tabbed onto the vbn track like SX / SY
                  onto x / y; T (D = S = G = vbn): band-side stripe tabbed onto the vbn track, outer stripe joined to
                  it by a Metal1 strap across T's own (dummy) channel; gate contacts only at the row ends.
  d2s_ab_n_f2     d2s_pd_n's switches folded in: SABN and SB above the tie (sharing it; no tap of their own), mirror
                  images about the cell axis, gates joined in poly (one poly bridge, a contact on each head); SABN's
                  drain on the vabn riser, SB's drain b joined to ABN's b pin by Metal2 down the right side.
  bias_tree_n_f2  the row only (TGN / TDN moved out into d2s_tgsw_f2); tie as long as the row.
  d2s_tgsw_f2     new: TGP, TGN, TDN (1 / 0.45) in one small block placed under NI on the ni track: TGP in an NWell
                  that joins bias_tree_p's well in the assembly (no tap of its own), TGN / TDN beside it; ni straight up
                  into the ni track, iref / en_3v3 / en_3v3_b in from the left edge, TDN's source as a vss pin.
  d2s_rhigh_f2, d2s_casc_n_f2   unchanged from stage A.
"""
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import build_f2_n as A                   # noqa: E402

ns, pya, ly, LI, g5, Cell, centered = A.ns, A.pya, A.ly, A.LI, A.g5, A.Cell, A.centered
TIEW, VOFF = ns["TIEW"], ns["VOFF"]
LI["NWell"] = ly.layer(31, 0)


# ------------------------------------------------------------------------------------------------ sinks
def sinks_f2(name, nf=6):
    c = Cell(name)
    half = ("XYYX" * nf)[:nf // 2]
    sw = {"X": "Y", "Y": "X"}
    right = "".join(sw[ch] for ch in half[::-1])
    m1 = list(half) + ["BN"] + list(right)
    m2 = [sw[ch] if ch in sw else "T" for ch in m1]
    f = {"X": ("SX", 6, 6, "x", "vbn", "vss"), "Y": ("SY", 6, 6, "y", "vbn", "vss"),
         "BN": ("BN", 6, 6, "vbn", "vbn", "vss"), "T": ("BNtwin", 6, 6, "vbn", "vbn", "vbn")}
    dn = ("dummy", 2, 6, "vbn", "vbn", "vbn")
    seq = lambda m: [dn] + [f[k] for k in m] + [dn]
    g = ns["two_rows"](c, seq(m1), seq(m2), ["x", "vbn", "y"], gcols_mid=False)
    X, top, tr = g["X"], g["top"], g["tr"]
    xl, xr = -0.97, X + 0.97
    tb = c.tie(xl, -0.21 - TIEW, xr, -0.21)
    tt = c.tie(xl, top + 0.21, xr, top + 0.21 + TIEW)
    for x0 in (xl, X + 0.68):
        c.box("M1", x0, tb[1], x0 + 0.29, tt[3])
    for row, devs in ((1, g["d1"]), (2, g["d2"])):
        for dv, it in zip(devs, seq(m1 if row == 1 else m2)):
            lab, w, l, d, gn, s = it
            inner, outer = ("top", "bot") if row == 1 else ("bot", "top")
            if s == "vss":
                c.box("M1", dv["x0"], tb[1], dv["x1"], dv["bot"][1]) if row == 1 else \
                    c.box("M1", dv["x0"], dv["top"][0], dv["x1"], tt[3])
            elif lab == "BNtwin":                        # outer stripe -> inner stripe across T's own channel
                c.box("M1", dv["xc"] - 0.25, dv["bot"][0], dv["xc"] + 0.25, dv["top"][1])
            else:
                c.bridge(dv, outer, ns["nearest_col"](g, dv))
            if d in ("x", "y") or lab in ("BN", "BNtwin"):
                ns["drains"](c, g, dv, row, d)
            else:
                c.bridge(dv, inner, ns["nearest_col"](g, dv))
    for n, t in tr.items():
        c.track(xl, X + 0.33 + 0.145, t)
        c.pin("M2", n, xl, t - 0.145, xl + 0.5, t + 0.145)
    for xc in g["cols"]:
        c.via(xc, tr["vbn"])
    c.pin("M1", "vss", tb[0], tb[1], tb[0] + 0.5, tb[3])
    c.tgo()
    # closed p+ ring (stage A): legs one tie width outside the tie ends, Metal1 over to the joiners, TGO over them
    act = sorted([s.dbox for s in c.c.shapes(LI["Activ"]).each()], key=lambda b: b.bottom)
    lo, hi = act[0], act[-1]
    xa, xb = lo.left - TIEW, lo.right
    A.ring_legs(c, xa, xb, lo.top, hi.bottom)            # contacts only between the strips (Cnt_b to theirs)
    for x0 in (xa, xb):                                  # Activ / pSD of the legs over the strips' ends too
        c.box("Activ", x0, lo.bottom, x0 + TIEW, hi.top)
        c.box("pSD", x0 - 0.03, lo.bottom - 0.03, x0 + TIEW + 0.03, hi.top + 0.03)
    c.box("M1", xa + 0.07, lo.bottom + 0.07, lo.left + 0.29, hi.top - 0.07)
    c.box("M1", xb - 0.29, lo.bottom + 0.07, xb + TIEW - 0.07, hi.top - 0.07)
    c.box("TGO", xa - 0.27, lo.bottom - 0.27, xb + TIEW + 0.27, hi.top + 0.27)
    c.info = "rows: D | %s | D  /  D | %s | D; no center columns; closed p+ ring" % (" ".join(m1), " ".join(m2))
    return c


# ------------------------------------------------------------------------------------------------ ab_n (+ SB, SABN)
def nup_at(c, label, w, l, x0, y0, d, g, s):
    """upright nmosHV finger (as build_f2_n.nup) with its Activ bottom at y0"""
    dev = pya.Layout.create_cell(ly, "nmosHV", "SG13_dev", {"w": "%gu" % w, "l": "%gu" % l, "ng": "1"})
    c.c.insert(pya.DCellInstArray(dev.cell_index(), pya.DTrans(pya.DVector(g5(x0), g5(y0)))))
    c.cdl.append("M%s_%d %s %s %s vss sg13_hv_nmos w=%gu l=%gu ng=1 m=1" % (label, len(c.cdl), d, g, s, w, l))
    aw = l + 0.68
    c.note(label, x0 + aw / 2, y0 + w / 2)
    return dict(x0=x0, x1=x0 + aw, top=y0 + w, L=(x0 + 0.07, x0 + 0.23), R=(x0 + aw - 0.23, x0 + aw - 0.07),
                g=(x0 + 0.34, x0 + 0.34 + l), xc=x0 + aw / 2)


def ab_n_f2(name):
    c = A.ab_n_f2(name)                                 # stage-A cell: row, heads, vabn bar + riser, tie, pins
    xc, top = 4.62, 4.4                                 # cell axis, row Activ top (stage A geometry)
    tie_top = top + 0.80 + TIEW                         # 5.50
    ys = g5(tie_top + 0.43)                             # pSD_j1 0.40 from the switches' channel to the tie's pSD
    sab = nup_at(c, "SABN", 1, 0.45, xc - 0.5 - 1.13, ys, "vabn", "en_3v3_b", "vss")
    sb = nup_at(c, "SB", 1, 0.45, xc + 0.5, ys, "b", "en_3v3_b", "vsso")
    yt = ys + 1.0                                       # switches' Activ top
    for dv in (sab, sb):                                # heads up, contact on each head
        g0, g1 = dv["g"]
        c.box("GatPoly", g0, yt, g1, yt + 0.56)
        for p in centered(g0 + 0.07, g1 - 0.07):
            c.cont(p, yt + 0.18)
        c.box("M1", (g0 + g1) / 2 - 0.13, yt + 0.12, (g0 + g1) / 2 + 0.13, yt + 0.47)
    c.box("GatPoly", sab["g"][0], yt + 0.16, sb["g"][1], yt + 0.56)          # poly bridge between the heads
    c.pin("M1", "en_3v3_b", sum(sb["g"]) / 2 - 0.13, yt + 0.12, sum(sb["g"]) / 2 + 0.13, yt + 0.47)
    ytop = g5(yt + 0.56 + 0.62)
    # SABN: outer (left) stripe vss into the tie, inner (right) stripe vabn onto the vabn riser (Via1)
    c.box("M1", sab["L"][0], tie_top - 0.23, sab["L"][1], ys)
    yv = ys + 0.5
    c.box("M1", sab["R"][0], yv - 0.145, xc + 0.145, yv + 0.145)
    c.via(xc, yv)
    c.box("M2", xc - 0.15, tie_top, xc + 0.15, ytop)                       # riser on up to the new top edge
    c.pin("M2", "vabn", xc - 0.15, ytop - 0.4, xc + 0.15, ytop)
    # SB: outer (right) stripe vsso up to the top edge, inner (left) stripe b: Via1, Metal2 east and down the right
    # side to ABN's b pin at the bottom edge
    c.box("M1", sb["R"][0], yt, sb["R"][1], ytop)
    c.pin("M1", "vsso", sb["R"][0], ytop - 0.4, sb["R"][1], ytop)
    yb = yv                                              # Via1 on the stripe, clear of the head's Metal1
    c.box("M1", sb["L"][0] - 0.065, yb - 0.145, sb["L"][1] + 0.065, yb + 0.145)
    xbv = (sb["L"][0] + sb["L"][1]) / 2
    c.via(xbv, yb)
    xs = 9.24 + 0.27 + 0.10                              # beyond the right dummy's ThickGateOx
    c.box("M2", xbv - 0.145, yb - 0.145, xs + 0.30, yb + 0.145)
    c.box("M2", xs, -0.545, xs + 0.30, yb + 0.145)
    tg = pya.Region(c.c.begin_shapes_rec(LI["TGO"])).bbox().to_dtype(ly.dbu)
    c.box("TGO", tg.left, tg.bottom, tg.right, tg.top)  # one ThickGateOx rectangle (TGO_e: no notches)
    xab = 7.20                                           # ABN's b stripe center (pin x 7.12 .. 7.28)
    c.box("M2", xab - 0.145, -0.545, xs + 0.30, -0.255)
    c.box("M1", xab - 0.145, -0.545, xab + 0.145, -0.255)
    c.via(xab, -0.40)
    c.tgo()
    c.info += "; SABN | SB above the tie"
    return c


# ------------------------------------------------------------------------------------------------ bias_tree_n (row)
def bias_tree_n_f2(name):
    c = Cell(name)
    seq = [("NBPC", 2.4, 6, "vbpc", "ni", "vss"), ("NBP", 6, 6, "vbp", "ni", "vss"), ("NI", 6, 6, "ni", "ni", "vss"),
           ("NABP", 6, 6, "vabp", "ni", "vss"), ("dummy", 2.4, 6, "ni", "ni", "ni")]
    X, H, devs = ns["one_row"](c, seq)
    TAB = ns["TAB"]
    tb = c.tie(-0.97, -0.21 - TIEW, X + 0.97, -0.21)
    for dv in devs[:-1]:
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
    c.pin("M2", "ni", X / 2 - 0.25, tn - 0.145, X / 2 + 0.25, tn + 0.145)
    for dv in devs[:-1]:
        if dv is devs[2]:
            c.tab(dv["xc"], dv["top"][0], tn + 0.145, tn)
        else:
            wt = min(TAB, dv["w"] - 0.4)
            c.box("M1", dv["xc"] - wt / 2, dv["top"][0], dv["xc"] + wt / 2, ytop)
    for dv, n in zip((devs[0], devs[1], devs[3]), ("vbpc", "vbp", "vabp")):
        wt = min(TAB, dv["w"] - 0.4)
        c.pin("M1", n, dv["xc"] - wt / 2, ytop - 0.3, dv["xc"] + wt / 2, ytop)
    c.pin("M1", "vss", tb[0], tb[1], tb[0] + 0.5, tb[3])
    c.tgo()
    c.info = "row: NBPC NBP NI NABP D (switches in d2s_tgsw_f2)"
    return c


# ------------------------------------------------------------------------------------------------ switches
def mos270(c, kind, label, w, l, x0, yb, d, g, s, bulk):
    """one hv MOS finger, W along x (as N2's Cell.mos): Activ [x0, x0 + w] x [yb, yb + l + 0.68]"""
    dev = pya.Layout.create_cell(ly, kind + "HV", "SG13_dev", {"w": "%gu" % w, "l": "%gu" % l, "ng": "1"})
    h = l + 0.68
    c.c.insert(pya.DCellInstArray(dev.cell_index(), pya.DTrans(pya.DVector(g5(x0), g5(yb))) *
                                  pya.DTrans(pya.DTrans.R270, pya.DVector(0, h))))
    c.cdl.append("M%s_%d %s %s %s %s sg13_hv_%s w=%gu l=%gu ng=1 m=1" % (label, len(c.cdl), d, g, s, bulk, kind, w, l))
    c.note(label, x0 + w / 2, yb + h / 2)
    return dict(x0=x0, x1=x0 + w, bot=(yb + 0.07, yb + 0.23), top=(yb + h - 0.23, yb + h - 0.07),
                gate=(yb + 0.34, yb + 0.34 + l), xc=x0 + w / 2)


def tgsw_f2(name):
    """TGP | TGN | TDN, W along x, side by side (Activ 1.96 apart: each gate column's fill 0.18 (Gat_b) from the
    neighbor's poly end; TGN 0.62 (NW_d1) from TGP's NWell). Top stripes = ni (one Metal1 strap above all three,
    clear of the gate columns), bottom stripes: TGP / TGN = iref (Metal1 strap below), TDN = vss (pin below).
    Gate columns on the left of each device: en_3v3_b (TGP, TDN; joined in Metal2 below), en_3v3 (TGN)."""
    c = Cell(name)
    tgp = mos270(c, "pmos", "TGP", 1, 0.45, 0.0, 0.0, "ni", "en_3v3_b", "iref", "vdd")
    tgn = mos270(c, "nmos", "TGN", 1, 0.45, 2.24, 0.0, "ni", "en_3v3", "iref", "vss")
    tdn = mos270(c, "nmos", "TDN", 1, 0.45, 4.20, 0.0, "ni", "en_3v3_b", "vss", "vss")
    cols = []
    for dv in (tgp, tgn, tdn):
        g0, g1 = dv["gate"]
        xc = dv["x0"] - 0.35
        c.gate_col(xc, [dv["gate"]], (g0 + g1) / 2 - 0.155, (g0 + g1) / 2 + 0.155, (dv["x0"] - 0.60, dv["x0"] - 0.10))
        c.box("M1", xc - 0.15, (g0 + g1) / 2 - 0.155, xc + 0.15, (g0 + g1) / 2 + 0.155)     # 0.30 x 0.31 (M1_d)
        cols.append(xc)
    c.box("NWell", -1.30, -0.62, 1.62, 1.75)              # NW_c1 0.62 around TGP's Activ; joins bias_tree_p's well
    # ni: the three top stripes into one strap above
    c.box("M1", tgp["x0"], tgp["top"][0], tdn["x1"], 1.42)
    xn = tdn["xc"]
    c.via(xn, 1.27)
    c.box("M2", xn - 0.15, 1.12, xn + 0.15, 2.30)                  # up into bias_tree_n's ni track
    c.pin("M2", "ni", xn - 0.15, 1.90, xn + 0.15, 2.30)
    # iref: risers from TGP's / TGN's bottom stripes to a strap below, out to the left edge
    for dv in (tgp, tgn):
        c.box("M1", dv["xc"] - 0.25, -0.60, dv["xc"] + 0.25, dv["bot"][1])
    c.box("M1", -1.30, -0.60, tgn["xc"] + 0.25, -0.31)
    c.pin("M1", "iref", -1.30, -0.60, -1.00, -0.31)
    # vss: TDN's bottom stripe down to a pin
    c.box("M1", tdn["xc"] - 0.25, -0.80, tdn["xc"] + 0.25, tdn["bot"][1])
    c.pin("M1", "vss", tdn["xc"] - 0.25, -0.80, tdn["xc"] + 0.25, -0.50)
    # gates: en_3v3_b (TGP, TDN columns) joined in Metal2 below, out to the left; en_3v3 (TGN) in Metal2 above
    yg = (tgp["gate"][0] + tgp["gate"][1]) / 2
    for xc in (cols[0], cols[2]):
        c.via(xc, yg)
        c.box("M2", xc - 0.145, -1.35, xc + 0.145, yg + 0.145)
    c.box("M2", -1.30, -1.35, cols[2] + 0.145, -1.06)
    c.pin("M2", "en_3v3_b", -1.30, -1.35, -1.00, -1.06)
    c.via(cols[1], yg)
    c.box("M2", cols[1] - 0.145, yg - 0.145, cols[1] + 0.145, 1.79)
    c.box("M2", -1.30, 1.50, cols[1] + 0.145, 1.79)
    c.pin("M2", "en_3v3", -1.30, 1.50, -1.00, 1.79)
    c.tgo()
    c.info = "TGP | TGN | TDN"
    return c


if __name__ == "__main__":
    out_gds, out_cdl = sys.argv[1], sys.argv[2]
    cells = [ab_n_f2("d2s_ab_n_f2"), bias_tree_n_f2("bias_tree_n_f2"), tgsw_f2("d2s_tgsw_f2"),
             A.rhigh_f2("d2s_rhigh_f2"), A.casc_n_f2("d2s_casc_n_f2"), sinks_f2("sinks_6x6_f2")]
    keep = {k.c.cell_index() for k in cells}
    for ci in [c.cell_index() for c in ly.each_cell() if c.is_top() and c.cell_index() not in keep]:
        ly.delete_cell_rec(ci)
    opt = pya.SaveLayoutOptions()
    opt.gds2_write_timestamps = False
    ly.write(out_gds, opt)
    with open(out_cdl, "w") as f:
        f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
                "* F2 NMOS / R cells, stage B (build_f2b_n.py, C2 2026-11-03); one line per finger / segment,"
                " dummies included.\n")
        for k in cells:
            nets = sorted({p[0] for p in k.pins})
            f.write("\n.SUBCKT %s %s\n%s\n.ENDS %s\n" % (k.name, " ".join(nets), "\n".join(k.cdl), k.name))
    for k in cells:
        b = k.c.dbbox()
        print("%-16s %6.2f x %6.2f um  bbox %s  %s" % (k.name, b.width(), b.height(), b, k.info))
        for n, m, x, y in sorted(k.pins):
            print("    pin %-9s %s (%.3f, %.3f)" % (n, m, x, y))
