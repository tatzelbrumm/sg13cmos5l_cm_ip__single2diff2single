# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 (C2, 2026-11-03), stage A: F2's reworked copies of N2's NMOS primitives and R block.

    python3 build_f2_n.py <out.gds> <out.cdl>

Reuses N2's build script (agents_c2/N2/out/build_d2s_n2.py) as a library: its source up to the cell list is executed
here, so every device, tie, gate column and track is drawn by N2's code with N2's rule values. Changes (Christoph's
review of 2026-11-02 / 03, agents_c2/N2/out/d2s_n2_cells_human_review.txt):

  d2s_pd_n_f2     reworked completely, as the NMOS twin of P2's d2s_pd_p (which Christoph found workable): upright
                  fingers SB | SABN, mirror images, drains inside, sources outside; one Metal1 gate bar over both
                  gate heads (contacts on full-width heads); tie only as long as the row (was 2.4x longer); drains b /
                  vabn as Metal1 + 2 Via1 + a Metal2 pad on the drain itself (no stubs; were 0.6 um Metal1 stubs);
                  vsso on Metal1 to the left edge (was Metal2 over the tie).
  d2s_ab_n_f2     reworked completely, as the NMOS twin of P2's d2s_ab_p: upright fingers D FNL RN2 ABN D (4.4/1),
                  the same stripe order as d2s_ab_p (l2 l1 | vabn dabn | a b), pins on Metal1 at the bottom edge, so
                  the two cells sit side by side (or face to face) with l1 / l2 / a / b in one column order; vabn bar
                  over the heads, Metal2 out over the tie. Dummies tied as d2s_ab_p's (D = S = G = tie, here vss).
  bias_tree_n_f2  row unchanged; TGN and TDN moved together to the left end (were at both ends): TDN next to the
                  tie (source straight into it), TGN above it, the shared ni node bridged to the row's left gate
                  column; iref leaves on Metal2 past the tie to the tie edge (the edge that faces the core-side pins
                  when the cell is placed flipped), next to bias_tree_p_f2's TGP. Cell 2.9 um narrower.
  d2s_rhigh_f2, d2s_casc_n_f2, sinks_6x6_f2
                  N2's cells unchanged plus a closed p+ ring: the missing legs are drawn (rhigh: top / bottom legs
                  beyond the link levels; casc_n / sinks: Activ ties under the existing Metal1 joiners at both ends).
"""
import os
import sys

sys.dont_write_bytecode = True
N2 = "/home/user/sudel/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/N2/out/build_d2s_n2.py"
src = open(N2).read()
ns = {"__name__": "n2lib"}
exec(compile(src[:src.index("\ncells = [")], N2, "exec"), ns)
pya, ly, LI, g5, Cell, centered = ns["pya"], ns["ly"], ns["LI"], ns["g5"], ns["Cell"], ns["centred"]   # N2 spells it centred
TIEW = ns["TIEW"]


# ------------------------------------------------------------------------------------------------ helpers
def nup(c, label, w, l, x0, d, g, s):
    """one upright nmosHV finger (R0, W along y), Activ [x0, x0 + l + 0.68] x [0, w]. Measured PCell geometry
    (probe of 2026-11-03): stripes 0.07 .. 0.23 inside the left / right Activ edge, gate x 0.34 .. 0.34 + l,
    poly 0.18 beyond the Activ in y, contacts symmetric in x. Left stripe = 'L', right = 'R'."""
    dev = pya.Layout.create_cell(ly, "nmosHV", "SG13_dev", {"w": "%gu" % w, "l": "%gu" % l, "ng": "1"})
    c.c.insert(pya.DCellInstArray(dev.cell_index(), pya.DTrans(pya.DVector(g5(x0), 0))))
    c.cdl.append("M%s_%d %s %s %s vss sg13_hv_nmos w=%gu l=%gu ng=1 m=1" % (label, len(c.cdl), d, g, s, w, l))
    aw = l + 0.68
    c.note(label, x0 + aw / 2, w / 2)
    return dict(x0=x0, x1=x0 + aw, top=w, L=(x0 + 0.07, x0 + 0.23), R=(x0 + aw - 0.23, x0 + aw - 0.07),
                g=(x0 + 0.34, x0 + 0.34 + l), xc=x0 + aw / 2)


def head(c, dv):
    """gate head as wide as the gate, 0.56 beyond the Activ, contacts 0.18 .. 0.34 above it (as P2's upright rows)"""
    g0, g1 = dv["g"]
    c.box("GatPoly", g0, dv["top"], g1, dv["top"] + 0.56)
    for p in centered(g0 + 0.07, g1 - 0.07):
        c.cont(p, dv["top"] + 0.18)


def fill_v1(c, x0, y0, x1, y1):
    """Via1 (V1_a 0.19, V1_b 0.22: pitch 0.41) centered in the zone"""
    def pos(a, b):
        n = max(1, int((b - a - 0.19) / 0.41 + 1e-6) + 1)
        return [(a + b) / 2 - ((n - 1) * 0.41) / 2 + i * 0.41 for i in range(n)]
    for x in pos(x0, x1):
        for y in pos(y0, y1):
            c.via(x, y)


def ring_legs(c, x0, x1, y0, y1):
    """vertical p+ tie legs (Activ 0.30, pSD 0.03 around, one contact column, Metal1 over it) at x0 and x1 (left
    edges), from y0 to y1: they close the existing top / bottom tie strips into a ring"""
    for xa in (x0, x1):
        c.tie(xa, y0, xa + TIEW, y1)


# ------------------------------------------------------------------------------------------------ pd_n
def pd_n_f2(name):
    c = Cell(name)
    sb = nup(c, "SB", 1, 0.45, 0.0, "b", "en_3v3_b", "vsso")
    sa = nup(c, "SABN", 1, 0.45, 1.13 + 0.21, "vabn", "en_3v3_b", "vss")     # Act_b 0.21
    for dv in (sb, sa):
        head(c, dv)
    top = 1.0
    c.box("M1", sum(sb["g"]) / 2 - 0.13, top + 0.18, sum(sa["g"]) / 2 + 0.13, top + 0.40)   # gate bar
    xc = (sb["x0"] + sa["x1"]) / 2
    c.pin("M1", "en_3v3_b", xc - 0.15, top + 0.18, xc + 0.15, top + 0.40)
    # tie under the row, as long as the row: pSD_j1 0.40 from the NFET gate (+ pSD 0.03 around the Activ)
    tb = c.tie(sb["x0"], -0.73, sa["x1"], -0.43)
    c.pin("M1", "vss", xc - 0.5, tb[1], xc + 0.5, tb[3])
    c.box("M1", sa["R"][0], tb[1], sa["R"][1], 0.0)                         # SABN source into the tie
    xl = sb["x0"] - 0.30
    c.box("M1", xl, 0.35, sb["L"][1], 0.65)                                  # vsso out to the left edge
    c.pin("M1", "vsso", xl, 0.35, xl + 0.25, 0.65)
    for dv, st, net in ((sb, "R", "b"), (sa, "L", "vabn")):                 # drains: M1 0.21, 2 Via1, M2 pad
        xa, xb = (dv[st][1] - 0.21, dv[st][1]) if st == "R" else (dv[st][0], dv[st][0] + 0.21)
        c.box("M1", xa, 0.0, xb, top)
        fill_v1(c, xa, 0.145, xb, 0.855)
        c.box("M2", xa, 0.145, xb, 0.855)                                    # Mn_d 0.144 um2: 0.21 x 0.71
        c.pin("M2", net, xa, 0.30, xb, 0.70)
    c.tgo()
    c.info = "row: SB SABN (upright, no dummies)"
    return c


# ------------------------------------------------------------------------------------------------ ab_n
def ab_n_f2(name):
    c = Cell(name)
    L = 1.0
    aw, gap = L + 0.68, 0.21
    lab = [("dummy", "vss", "vss", "vss"), ("FNL", "l2", "vabn", "l1"), ("RN2", "vabn", "vabn", "dabn"),
           ("ABN", "a", "vabn", "b"), ("dummy", "vss", "vss", "vss")]
    row = [nup(c, n, 4.4, L, k * (aw + gap), d, g, s) for k, (n, d, g, s) in enumerate(lab)]
    top = 4.4
    for dv in row:
        head(c, dv)
    xc = (row[0]["x0"] + row[-1]["x1"]) / 2
    # vabn bar over all contacts of the three heads (3 per 1 um head; M1_c1 0.05 beyond the outer ones)
    bt = (row[1]["g"][0] + 0.07 - 0.05, top + 0.18, row[3]["g"][1] - 0.07 + 0.05, top + 0.40)
    c.box("M1", *bt)
    yt = top + 0.80                                                          # tie: as d2s_ab_p (pSD_j1 0.40)
    tt = c.tie(row[0]["x0"], yt, row[-1]["x1"], yt + 0.30)
    ybot, ytop = -0.62, yt + 0.30 + 0.62                                     # pin edges as d2s_ab_p's
    c.via(xc, (bt[1] + bt[3]) / 2)
    c.box("M2", xc - 0.15, bt[1] - 0.04, xc + 0.15, ytop)
    c.pin("M2", "vabn", xc - 0.15, ytop - 0.4, xc + 0.15, ytop)
    for (n, d, g, s), dv in zip(lab, row):
        if n == "dummy":                                                     # gate, drain, source into the tie
            c.box("M1", dv["x0"] + 0.07, top + 0.18, dv["x1"] - 0.07, tt[3])
            for st in ("L", "R"):
                c.box("M1", dv[st][0], top, dv[st][1], yt)
            continue
        for st, net in (("L", d), ("R", s)):                                 # left stripe = drain everywhere
            if net == "vabn":
                c.box("M1", dv[st][0], top, dv[st][1], bt[1])
            else:
                c.box("M1", dv[st][0], ybot, dv[st][1], 0.0)
                c.pin("M1", net, dv[st][0], ybot, dv[st][1], ybot + 0.4)
    c.pin("M1", "vss", xc - 1.0, tt[1], xc + 1.0, tt[3])
    c.tgo()
    c.info = "row: D | FNL RN2 ABN | D (upright, dummies on the tie)"
    return c


# ------------------------------------------------------------------------------------------------ bias_tree_n
def bias_tree_n_f2(name):
    """N2's bias_tree_n row, gate columns, ni track, drains and pins unchanged; TGN / TDN as one block at the left
    end (x as N2's TGN: Activ 0.96 left of the row, poly 0.18 from the row's column fill, Gat_b)."""
    c = Cell(name)
    seq = [("NBPC", 2.4, 6, "vbpc", "ni", "vss"), ("NBP", 6, 6, "vbp", "ni", "vss"), ("NI", 6, 6, "ni", "ni", "vss"),
           ("NABP", 6, 6, "vabp", "ni", "vss"), ("dummy", 2.4, 6, "ni", "ni", "ni")]
    X, H, devs = ns["one_row"](c, seq)
    TAB = ns["TAB"]
    tb = c.tie(-2.96, -0.21 - TIEW, X + 0.97, -0.21)
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
    # switch block: TDN on the tie (Act_b 0.21), TGN above it (Act_b 0.21); W along x as N2's switches
    td = c.mos("TDN", 1, 0.45, -1.96, 0.0, "ni", "en_3v3_b", "vss")
    tg = c.mos("TGN", 1, 0.45, -1.96, 1.34, "ni", "en_3v3", "iref")
    for dv in (td, tg):                                  # own gate column each, on a fill as tall as the gate
        c.gate_col(-2.29, [dv["gate"]], dv["gate"][0], dv["gate"][1], (-2.56, -2.06))
    c.pin("M1", "en_3v3_b", -2.42, td["gate"][0], -2.16, td["gate"][1])
    c.pin("M1", "en_3v3", -2.42, tg["gate"][0], -2.16, tg["gate"][1])
    c.box("M1", td["xc"] - 0.145, tb[1], td["xc"] + 0.145, td["bot"][1])       # TDN source into the tie
    c.box("M1", td["x0"] + 0.1, td["top"][0], td["x1"] - 0.1, tg["bot"][1])     # ni: TDN top + TGN bottom stripe
    c.box("M1", -0.33, td["top"][0], td["x1"] - 0.1, tg["bot"][1])               # ... bridged to the gate column
    c.pin("M1", "ni", td["xc"] - 0.25, td["top"][0], td["xc"] + 0.25, tg["bot"][1])
    # iref: Via1 on TGN's top stripe (Metal1 pad 0.29 x 0.29 over it) -> Metal2 straight down over the switch
    # block and the tie to the tie edge (Metal2 crosses only Metal1)
    yi = g5(tg["top"][1] - 0.08 - 0.07)
    c.box("M1", tg["xc"] - 0.145, yi - 0.145, tg["xc"] + 0.145, tg["top"][1])
    c.via(tg["xc"], yi)
    yb = tb[1] - 0.6
    c.box("M2", tg["xc"] - 0.15, yb, tg["xc"] + 0.15, yi + 0.145)
    c.pin("M2", "iref", tg["xc"] - 0.15, yb, tg["xc"] + 0.15, yb + 0.3)
    c.pin("M1", "vss", tb[0], tb[1], tb[0] + 0.5, tb[3])
    c.tgo()
    c.info = "row: [TGN / TDN] | NBPC NBP NI NABP D"
    return c


# ------------------------------------------------------------------------------------------------ rings
def shapes_of(c, lay):
    return [s.dbox for s in c.c.shapes(LI[lay]).each() if s.is_box()]


def sinks_f2(name):
    """legs one tie width outside N2's tie ends (under the joiners they would sit 0.07 = Gat_d from the end gate
    columns' poly fill, and sym_check's neck test would count the fill as necked by the tie); Metal1 from the leg
    contacts over to N2's joiners"""
    c = ns["sinks"](name)
    act = sorted(shapes_of(c, "Activ"), key=lambda b: b.bottom)          # the two tie strips (devices are instances)
    lo, hi = act[0], act[-1]
    xl, xr = lo.left - TIEW, lo.right
    ring_legs(c, xl, xr, lo.bottom, hi.top)
    c.box("M1", xl + 0.07, lo.bottom + 0.07, lo.left + 0.29, hi.top - 0.07)
    c.box("M1", xr - 0.29, lo.bottom + 0.07, xr + TIEW - 0.07, hi.top - 0.07)
    c.box("TGO", xl - 0.27, lo.bottom - 0.27, xr + TIEW + 0.27, hi.top + 0.27)   # TGO_a 0.27 over the legs too
    c.info += "; closed p+ ring"
    return c


def casc_n_f2(name):
    c = ns["casc_n"](name)
    act = sorted(shapes_of(c, "Activ"), key=lambda b: b.bottom)
    lo, hi = act[0], act[-1]
    ring_legs(c, lo.left, lo.right - TIEW, lo.top, hi.bottom)
    c.info += "; closed p+ ring"
    return c


def rhigh_f2(name):
    c = ns["rhigh"](name)
    act = sorted(shapes_of(c, "Activ"), key=lambda b: b.left)             # the two side strips
    l, r = act[0], act[-1]
    m1 = pya.Region(c.c.begin_shapes_rec(LI["M1"])).bbox().to_dtype(ly.dbu)
    m2 = pya.Region(c.c.begin_shapes_rec(LI["M2"])).bbox().to_dtype(ly.dbu)
    yt = g5(max(m1.top, m2.top) + 0.18 - 0.07)       # leg contact M1 (0.07 inside the Activ) M1_b 0.18 above all M1
    yb = g5(m1.bottom - 0.18 + 0.07 - TIEW)
    c.tie(l.left, yt, r.right, yt + TIEW)
    c.tie(l.left, yb, r.right, yb + TIEW)
    c.box("Activ", l.left, yb, l.right, yt + TIEW)                       # legs joined to the side strips
    c.box("Activ", r.left, yb, r.right, yt + TIEW)
    c.box("pSD", l.left - 0.03, yb - 0.03, l.right + 0.03, yt + TIEW + 0.03)
    c.box("pSD", r.left - 0.03, yb - 0.03, r.right + 0.03, yt + TIEW + 0.03)
    for x0, x1 in ((l.left, l.right), (r.left, r.right)):               # Metal1 corners: strip contacts to legs
        c.box("M1", (x0 + x1) / 2 - 0.08, yb + 0.07, (x0 + x1) / 2 + 0.08, yt + TIEW - 0.07)
    c.info += "; closed p+ ring"
    return c


if __name__ == "__main__":
    out_gds, out_cdl = sys.argv[1], sys.argv[2]
    cells = [pd_n_f2("d2s_pd_n_f2"), ab_n_f2("d2s_ab_n_f2"), bias_tree_n_f2("bias_tree_n_f2"),
             rhigh_f2("d2s_rhigh_f2"), casc_n_f2("d2s_casc_n_f2"), sinks_f2("sinks_6x6_f2")]
    keep = {k.c.cell_index() for k in cells}
    for ci in [c.cell_index() for c in ly.each_cell() if c.is_top() and c.cell_index() not in keep]:
        ly.delete_cell_rec(ci)
    opt = pya.SaveLayoutOptions()
    opt.gds2_write_timestamps = False
    ly.write(out_gds, opt)
    with open(out_cdl, "w") as f:
        f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
                "* F2 reworked NMOS / R cells (build_f2_n.py, C2 2026-11-03); one line per finger / segment, dummies"
                " included; bulk = vss.\n")
        for k in cells:
            nets = sorted({p[0] for p in k.pins})
            f.write("\n.SUBCKT %s %s\n%s\n.ENDS %s\n" % (k.name, " ".join(nets), "\n".join(k.cdl), k.name))
    for k in cells:
        b = k.c.dbbox()
        print("%-16s %6.2f x %6.2f um  %s" % (k.name, b.width(), b.height(), k.info))
        for n, m, x, y in sorted(k.pins):
            print("    pin %-9s %s (%.3f, %.3f)" % (n, m, x, y))
