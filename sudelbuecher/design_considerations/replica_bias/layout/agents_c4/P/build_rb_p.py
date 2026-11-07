# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_rb_p.py: PMOS rows of the replica bias pad_ref_rb (IHP sg13cmos5l), C4, agent P, 2026-11-07, Claude.

    python3 build_rb_p.py [--no-png]    (needs the PDK: PDK_ROOT, default /foss/pdks; writes next to this file)

Christoph: "the replica bias must match their layout structures". Every row is drawn with the code that drew the s2d
pad's row: build_s2d_p3.py (C3, agent P; next to this file, unchanged, sha256 874063e7aff4) is imported as P and its
helpers (mos, rows, gate_cols, ring, well, fill, edge_stub, tub, finish, render) build the rows unchanged; only the
device lists and the nets differ.
  rb_tree_p  = P.bias_tree() (pad cell bias_tree_noab_p_c3), rewired: PBNC | MDPBN (dummy in PBN's 5/6 slot) | BP
               (diode in the dummy's 2/6 slot), TGP as drawn
  rb_tails   = F's tails_row() (pad cell s2d_tails_hi_f / _lo_f, built from P's tails()), cut to D | TR BT | D
  rb_tubs    = P.tub() (pad cell tub_p20x1_c3) in a row at the pitch of s2d_inputs_c3: D | MR BA BB | D
  rb_avg     = new: D | SL1 | SU | SL2 | D, 1/4 "small tubs" built as P.tub(); SL1 = M90 image of SL2 about SU's
               axis; dummy small tubs at both ends built as the pad's dummy tubs (round 2)
Writes rb_p_cells.gds (top cell rb_p_cells), rb_p_cells.cdl (one .SUBCKT per cell, every dummy a device) and PNGs.
Rule values: sg13cmos5l_tech_default.json / SG13CMOS5L_os_layout_rules.txt (names in the comments).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_s2d_p3 as P     # noqa: E402  C3's generator, unchanged
import pya                   # noqa: E402

P.OUT = HERE
ly, box, fill, pin, note, RG = P.ly, P.box, P.fill, P.pin, P.note, P.RG


# ---------------------------------------------------------------- rb_tree_p: the pad's bias_tree_noab_p_c3, rewired
def tree_p():
    """P.bias_tree() line by line; changed: the row's nets (PBN slot -> dummy MDPBN, drain into the ring strip as the
    pad's dummy; dummy slot -> BP, drain lane into its own gate column as the pad's tails BP, mirrored) and TGP's
    CDL terminals (drain ni, source iref, as in pad_ref_rb.spice; the drawn transistor is the pad's)."""
    c = ly.create_cell("rb_tree_p")
    N, Pm, S = P.mos(2, 6), P.mos(5, 6), P.mos(1, 0.45)
    lab = ["PBNC", "DPBN", "BP"]
    (row,), xc = P.rows(c, [N, Pm, N], [["PBNC", "MDPBN", "BP"]], True)
    h = 6.68
    x0, x1 = row[0]["act"].left, row[-1]["act"].right
    ta = -h - 0.51 - 0.43
    b = pya.DBox(x0 - (RG + 0.92), ta - 1.0 - 0.62, x1 + (RG + 0.92), 0.51 + 0.62)
    gl, gr = P.gate_cols(c, row)
    for dv, n, net in zip(row, lab, ["vbnc", "vdd", "vbp"]):
        a, cx = dv["act"], dv["act"].center().x
        P.dev(c, n, net, "vbp", "vdd", dv["key"])
        if n == "DPBN":                                      # dummy drain straight into the ring strip (pad's D)
            box(c, "M1", a.left, -0.23, a.right, 0.21)
            continue
        if n == "BP":                                        # diode: drain lane into its gate column, 0.24 below
            box(c, "M1", gr.left, gr.top - 0.01, gr.right, -0.03)        # the ring strip (pad tails' BP, mirrored)
            box(c, "M1", a.right - 1.0, -0.29, gr.right, -0.03)
            continue
        box(c, "M1", cx - 0.555, -0.30, cx + 0.555, -0.01)
        fill(c, "Via1", cx - 0.505, -0.25, cx + 0.505, -0.06)
        box(c, "M2", cx - 0.555, -0.30, cx + 0.555, b.top)
        pin(c, "M2", net, cx - 0.555, b.top - 0.30, cx + 0.555, b.top)
    box(c, "M1", x0, -h - 0.51, x1, -h + 0.23)
    P.ring(c, x0 - RG, -h - 0.51, x1 + RG, 0.51)
    P.edge_stub(c, gl, gl.center().y, b.left, "vbp")
    pin(c, "M1", "vdd", x0 - RG - 0.30, -h + 0.5, x0 - RG, -h + 2.5)
    tg = P.place(c, S, pya.DTrans(pya.DTrans.M0, pya.DVector(xc - 0.565, ta)), "TGP")
    P.dev(c, "TGP", "ni", "en_3v3_b", "iref", S)
    a = tg["act"]
    box(c, "GatPoly", xc - 0.225, a.bottom - 0.56, xc + 0.225, a.bottom)
    fill(c, "Cont", xc - 0.08, a.bottom - 0.34, xc + 0.08, a.bottom - 0.18)
    box(c, "M1", xc - 0.13, b.bottom, xc + 0.13, a.bottom - 0.18)
    pin(c, "M1", "en_3v3_b", xc - 0.13, b.bottom, xc + 0.13, b.bottom + 0.3)
    for st, net, sg in ((tg["s"], "iref", -1), (tg["d"], "ni", 1)):
        xo = st.left - 0.10 if sg < 0 else st.right + 0.10
        box(c, "M1", min(xo, st.left), b.bottom, max(xo, st.right), st.top)
        pin(c, "M1", net, min(xo, st.left), b.bottom, max(xo, st.right), b.bottom + 0.3)
    P.well(c, b)
    return P.finish(c, ["en_3v3_b", "iref", "ni", "vbnc", "vbp", "vdd"])


# ---------------------------------------------------------------- rb_tails: the pad's tail row cut to D TR BT D
def tails():
    """F's tails_row() (build_f_tails.py, C3) line by line with four 5/6 devices: the row ends of s2d_tails_lo_f
    (D at both ends) around two unit tails. Sources under one plate into the ring's top strip, drains out over the
    closed ring as M2 pads, vbp edge stub at the right row end (as s2d_tails_hi_f / _lo_f)."""
    c = ly.create_cell("rb_tails")
    T = P.mos(5, 6)
    names = ["D", "TR", "BT", "D"]
    nets = {"TR": "ts", "BT": "bt"}
    (lo,), xc = P.rows(c, [T] * 4, [names], False)
    h = 6.68
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    top_in = 0.43
    b = pya.DBox(x0 - (RG + 0.92), -h - 1.13, x1 + (RG + 0.92), top_in + 0.30 + 0.62)
    gl, gr = P.gate_cols(c, lo)
    box(c, "M1", x0, -0.23, x1, top_in + 0.30)
    P.ring(c, x0 - RG, -h - 0.51, x1 + RG, top_in + 0.30)
    for i, (dv, n) in enumerate(zip(lo, names)):
        a, cx = dv["act"], dv["act"].center().x
        if n == "D":
            P.dev(c, "DT%d" % i, "vdd", "vbp", "vdd", T)
            box(c, "M1", a.left, -h - 0.21, a.right, -6.45)
            continue
        P.dev(c, n, nets[n], "vbp", "vdd", T)
        box(c, "M1", cx - 0.555, -6.67, cx + 0.555, -6.38)
        fill(c, "Via1", cx - 0.505, -6.62, cx + 0.505, -6.43)
        box(c, "M2", cx - 0.555, -6.38, cx + 0.555, b.bottom)
        pin(c, "M2", nets[n], cx - 0.555, b.bottom, cx + 0.555, b.bottom + 0.30)
    P.edge_stub(c, gr, gr.center().y, b.right, "vbp")
    pin(c, "M1", "vdd", x0 - RG - 0.30, -h + 0.5, x0 - RG, -h + 2.5)
    P.well(c, b)
    return P.finish(c, ["bt", "ts", "vbp", "vdd"])


# ---------------------------------------------------------------- rb_tubs: the pad's tub in a row of five
def tub():
    """P.tub() unchanged, with its g / d / s labels removed as in the pad's copy (rbsrc_tub_p20x1_c3)."""
    c = P.tub()
    del P.CDL[c.name]
    for lay in ("M1pin", "M1txt", "TEXT"):
        c.shapes(P.LI[lay]).clear()
    c.name = "rb_tub_p20x1"
    return c


def tubs(tc):
    """one row of s2d_inputs_c3 at its pitch (tub 4.30 + NW.b1 1.80): D | MR BA BB | D, gate heads up, the pad's
    lower-row construction: gate tab on the right head, source plates and drain tab down. Changes: the band holds
    only vdd (the dummies' gates, the pad's Via1 scheme), the three gate tabs go straight up to pins on the top edge;
    the diodes MR / BB join their drain stripe end to both gate pads (M1 over the poly bridge); BA's drain tab runs
    on to the bottom edge; bt joins BA's right and BB's left source plate on the pad's first under-row track."""
    c = ly.create_cell("rb_tubs")
    pt, yv, top, bot = 4.30 + 1.80, 10.30, 10.62, -1.35
    names = ["D", "MR", "BA", "BB", "D"]
    term = {"MR": ("gh", "gh", "ts"), "BA": ("bd", "m", "bt"), "BB": ("vcm", "vcm", "bt")}
    for i, n in enumerate(names):
        ox = i * pt
        c.insert(pya.DCellInstArray(tc.cell_index(), pya.DTrans(pya.DVector(ox, 0))))
        note(c, n, pya.DBox(ox, 4.0, ox + 3.06, 6.0))
        if n == "D":
            P.dev(c, "DU%d" % i, "vdd", "vdd", "vdd", (20, 1, 2))
            box(c, "M1", ox + 0.07, -0.62, ox + 2.99, -0.30)           # drain tab into both plates (pad)
            box(c, "M1", ox + 0.07, 10.0, ox + 2.99, yv + 0.145)        # gate pads and stripe ends, Via1 on vdd (pad)
            fill(c, "Via1", ox + 0.5, yv - 0.095, ox + 2.56, yv + 0.095)
            continue
        d, g, s = term[n]
        P.dev(c, n, d, g, s, (20, 1, 2), s)
        if d == g:
            box(c, "M1", ox + 1.31, 10.0, ox + 1.75, 10.40)            # diode: drain stripe end to both gate pads
        else:
            box(c, "M1", ox + 0.975, bot, ox + 2.085, -0.62)            # drain tab on to the edge (no tie contact)
            pin(c, "M1", d, ox + 0.975, bot, ox + 2.085, bot + 0.30)
        box(c, "M1", ox + 1.82, 10.18, ox + 2.52, top)                  # gate tab on the right head (pad)
        pin(c, "M1", g, ox + 1.82, top - 0.30, ox + 2.52, top)
        pin(c, "M1", s, ox + 0.07, bot, ox + 0.74, bot + 0.30)
    xa, xb = 2 * pt + 2.32, 3 * pt + 0.07                              # BA's right, BB's left source plate
    for x in (xa, xb):
        fill(c, "Via1", x + 0.05, -0.95 - 0.095, x + 0.62, -0.95 + 0.095)
    P.track(c, xa, xb + 0.67, -0.95)
    x0, x1 = -0.62, 4 * pt + 3.68
    P.track(c, x0, x1, yv)
    pin(c, "M2", "vdd", x0, yv - P.TW, x0 + 0.5, yv + P.TW)
    return P.finish(c, ["bd", "bt", "gh", "m", "ts", "vcm", "vdd"])


# ---------------------------------------------------------------- rb_avg: 1/4 small tubs, D | SL1 | SU | SL2 | D
def small_tub():
    """hv PMOS 1/4 (the pad's pmosHV_w1_l4 finger) in its own NWell, bulk = source, as a diode; built as P.tub():
    upright, gate head as wide as the gate (L = 4) above the Activ with one contact row (Cnt.e 0.14, M1.b 0.18 to the
    stripe ends), N+ tie 0.43 below the Activ (pSD.i1 0.40 + pSD.d1 0.03), source plate down over it, NWell / TGO
    0.62 beyond Activ and tie (NW.c1, NW.e1). One finger: no poly bridge. No drain crosses the tie, so the tie is
    contacted along its length. The drain stripe end joins the gate pad (diode)."""
    c = ly.create_cell("rb_tub_p1x4")
    P.place(c, P.mos(1, 4), pya.DTrans())                 # Activ 0 .. 4.68 x 0 .. 1, gate 0.34 .. 4.34
    box(c, "GatPoly", 0.34, 1.0, 4.34, 1.56)
    fill(c, "Cont", 0.41, 1.18, 4.27, 1.34)
    box(c, "M1", 0.37, 1.18, 4.31, 1.40)                  # gate pad
    box(c, "M1", 4.31, 1.0, 4.61, 1.40)                   # diode: drain stripe end to the gate pad
    P.tap(c, 0.0, -0.73, 4.68, -0.43)                     # tie, contacted along its length
    box(c, "M1", 0.07, -1.35, 0.74, 0.0)                  # source plate over the tie (the tub's plate)
    P.well(c, pya.DBox(-0.62, -1.35, 5.30, 1.62))
    return c


def avg(sc):
    """D | SL1 | SU | SL2 | D at the small-tub pitch (5.92 + NW.b1 1.80); SU R0 in the middle, SL2 R0, SL1 = M90 image
    of SL2 about SU's axis (x = 2.34), so the sources of SL1 / SL2 face SU. Round 2 (Christoph: "apply dummies ...
    reproduce the dummy structures in the pads"): a dummy small tub at both ends, the same cell at the same pitch and
    in its neighbor's orientation (right R0 as SL2, left M90 as SL1), built as the pad's dummy tubs: one M1 box over the
    gate pad and the stripe ends (g = d = s), Via1 on the vdd M2 track that crosses the row (the pad's band track).
    m: SU's gate pad out to both NWell gaps and down them onto SL1's / SL2's ties; xp: SL1's and SL2's gate pads
    joined over SU, 0.22 (M1.e) above."""
    c = ly.create_cell("rb_avg")
    pt, ax, top, bot, yv = 5.92 + 1.80, 2.34, 1.88, -1.35, 1.30
    for n, t in (("SU", pya.DTrans()), ("SL2", pya.DTrans(pya.DVector(pt, 0))),
                 ("SL1", pya.DTrans(pya.DTrans.M90, pya.DVector(2 * ax - pt, 0))),
                 ("D", pya.DTrans(pya.DVector(2 * pt, 0))),
                 ("D", pya.DTrans(pya.DTrans.M90, pya.DVector(2 * ax - 2 * pt, 0)))):
        c.insert(pya.DCellInstArray(sc.cell_index(), t))
        note(c, n, t * pya.DBox(0.34, 0.0, 4.34, 1.0))
    P.dev(c, "DA0", "vdd", "vdd", "vdd", (1, 4, 1))
    P.dev(c, "SL1", "xp", "xp", "m", (1, 4, 1), "m")
    P.dev(c, "SU", "m", "m", "gh", (1, 4, 1), "gh")
    P.dev(c, "SL2", "xp", "xp", "m", (1, 4, 1), "m")
    P.dev(c, "DA1", "vdd", "vdd", "vdd", (1, 4, 1))
    for sg in (-1, 1):
        X = (lambda x: x) if sg > 0 else (lambda x: 2 * ax - x)
        gx = 5.30 + 0.90                                  # middle of the NWell gap
        box(c, "M1", X(4.31), 1.18, X(gx + 0.13), 1.40)  # m: SU's gate pad out to the gap
        box(c, "M1", X(gx - 0.13), bot, X(gx + 0.13), 1.40)
        box(c, "M1", X(gx - 0.13), -0.73, X(pt), -0.43)  # onto SL's tie (= SL's source, m)
        pin(c, "M1", "m", X(gx - 0.13), bot, X(gx + 0.13), bot + 0.30)
        box(c, "M1", X(pt + 0.37), 1.18, X(pt + 0.63), top)   # xp riser on SL's gate pad
        box(c, "M1", X(2 * pt + 0.07), 1.0, X(2 * pt + 4.61), yv + 0.145)   # dummy: gate pad and stripe ends (pad)
        fill(c, "Via1", X(2 * pt + 0.5), yv - 0.095, X(2 * pt + 4.18), yv + 0.095)
    box(c, "M1", 2 * ax - pt - 0.63, top - 0.26, pt + 0.63, top)  # xp over SU
    pin(c, "M1", "xp", ax - 0.5, top - 0.26, ax + 0.5, top)
    pin(c, "M1", "gh", 0.07, bot, 0.74, bot + 0.30)
    x0, x1 = 2 * ax - 2 * pt - 5.30, 2 * pt + 5.30         # the dummies' NWell edges
    P.track(c, x0, x1, yv)
    pin(c, "M2", "vdd", x0, yv - P.TW, x0 + 0.5, yv + P.TW)
    return P.finish(c, ["gh", "m", "vdd", "xp"])


# ---------------------------------------------------------------- output
VIEWS = {"rb_tree_p": [("bp_lane", (8.0, 3.0, 12.94, 10.37))], "rb_tails": [("row_end", (0, 0, 9.0, 9.16))],
         "rb_tubs": [("diode_head", (5.5, 10.6, 16.0, 11.97)), ("bottom", (5.5, 0, 22.0, 2.4))],
         "rb_avg": [("su_sl2_dummy", (15.2, 0, 36.80, 3.23))]}


def write():
    cells = [tree_p(), tails()]
    tc = tub()
    cells.append(tubs(tc))
    cells.append(avg(small_tub()))
    for c in list(ly.each_cell()):                           # leaf names: no clash with the pad's cells
        if c.name.startswith("pmosHV"):
            c.name = "rb_" + c.name
    top = ly.create_cell("rb_p_cells")
    x = 0.0
    for c in cells:
        top.insert(pya.DCellInstArray(c.cell_index(), pya.DTrans(pya.DVector(x, 0))))
        top.shapes(P.LI["TEXT"]).insert(pya.DText(c.name, x, -2.0))
        x += c.dbbox().width() + 5.0
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(os.path.join(HERE, "rb_p_cells.gds"), opt)
    txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* rb_p_cells.cdl: reference netlists of rb_p_cells.gds, written by build_rb_p.py (C4, agent P, 2026-11-07).",
           "* Devices as drawn (netlists pad_ref_rb / vcm_rb), dummies included (D = S = B on vdd).", ""]
    for c in cells:
        ports, lines = P.CDL[c.name]
        txt += [".SUBCKT %s %s" % (c.name, " ".join(ports))] + lines + [".ENDS %s" % c.name, ""]
    open(os.path.join(HERE, "rb_p_cells.cdl"), "w").write("\n".join(txt))
    for c in cells:
        b = c.dbbox()
        print("%-10s %7.3f x %7.3f um" % (c.name, b.width(), b.height()))
        for n, m, pb in P.PINS[c.name]:
            print("    %-9s %s  (%.3f, %.3f; %.3f, %.3f)" % (n, m, pb.left, pb.bottom, pb.right, pb.top))
    if "--no-png" not in sys.argv:
        for c in cells:
            P.render(c, c.name + ".png")
            for tag, win in VIEWS.get(c.name, []):
                P.render(c, "%s_%s.png" % (c.name, tag), win)


if __name__ == "__main__":
    write()
