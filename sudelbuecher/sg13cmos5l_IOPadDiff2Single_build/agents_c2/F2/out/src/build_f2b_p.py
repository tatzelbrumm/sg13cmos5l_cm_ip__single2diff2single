# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 (C2, 2026-11-03), stage B: the PMOS cells after Christoph's review of the stage-A placement.

    python3 build_f2b_p.py <out.gds> <out.cdl>

Imports P2's build script as a library (as stage A). Changes against stage A:
  d2s_ab_p_f2     d2s_pd_p's switches folded in: SABP and SA above the U tap's top strip, in the same NWell rectangle
                  (no notch, no tap of their own: the U tap serves them), mirror images about the cell axis, gates
                  joined in poly (one poly bridge, a contact on each head); SABP's drain on the vabp riser, SA's drain
                  a joined to ABP's a pin by Metal2 down the right side; vddo (SA's source) as a pin at the top.
  bias_tree_p_f2  the row only (TGP moved out into d2s_tgsw_f2); NWell 0.62 around the ring.
"""
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/sudel/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/P2/out")
import build_d2s_p2 as p2                     # noqa: E402

pya, ly, box, fill, pin, tap, well, g5 = p2.pya, p2.ly, p2.box, p2.fill, p2.pin, p2.tap, p2.well, p2.g5
mos, place, dev, rows, gate_cols, tab3, ring, upright, finish = (p2.mos, p2.place, p2.dev, p2.rows, p2.gate_cols,
                                                                 p2.tab3, p2.ring, p2.upright, p2.finish)
RG = p2.RG


def ab_p_f2():
    c = ly.create_cell("d2s_ab_p_f2")
    A, S = mos(6.66, 0.6), mos(1, 0.45)
    lab = ["D", "FPL", "RP2", "ABP", "D"]
    row, xc = upright(c, [A] * 5, lab, 0.21)
    top = row[0]["act"].top
    bt = pya.DBox(row[1]["gate"].center().x - 0.13, top + 0.18, row[3]["gate"].center().x + 0.13, top + 0.40)
    box(c, "M1", bt.left, bt.bottom, bt.right, bt.top)
    yt = top + 0.80
    xl, xr = row[0]["act"].left - 0.21 - 0.30, row[-1]["act"].right + 0.21
    tap(c, xl, yt, xr + 0.30, yt + 0.30)
    for x0 in (xl, xr):
        tap(c, x0, 0.0, x0 + 0.30, yt, (x0 + 0.07, 0.07, x0 + 0.23, yt - 0.11))
    # switches above the tap: Activ bottom pSD_i1 0.40 + 0.03 above the N+ strip; 1.0 apart for the vabp riser
    ys = yt + 0.30 + 0.43
    ts = [pya.DTrans(pya.DVector(xc - 0.5 - 1.13, ys)), pya.DTrans(pya.DVector(xc + 0.5, ys))]
    sabp, sa = place(c, S, ts[0], "SABP"), place(c, S, ts[1], "SA")
    dev(c, "SABP", "vabp", "en_3v3", "vdd", S)
    dev(c, "SA", "a", "en_3v3", "vddo", S)
    st = ys + 1.0
    for dv in (sabp, sa):
        gt = dv["gate"]
        box(c, "GatPoly", gt.left, st, gt.right, st + 0.56)
        fill(c, "Cont", gt.left + 0.07, st + 0.18, gt.right - 0.07, st + 0.34)
        box(c, "M1", gt.center().x - 0.13, st + 0.12, gt.center().x + 0.13, st + 0.47)
    box(c, "GatPoly", sabp["gate"].left, st + 0.16, sa["gate"].right, st + 0.56)       # poly bridge
    ytop = st + 0.56 + 0.62
    b = pya.DBox(xl - 0.62, -0.62, xr + 0.30 + 0.62, ytop)                            # NW_e1 / NW_c1 0.62
    pin(c, "M1", "en_3v3", sa["gate"].center().x - 0.13, st + 0.12, sa["gate"].center().x + 0.13, st + 0.47)
    # left / right stripes of the switches (upright PCell: s = left, d = right)
    L = lambda dv: dv["s"]
    R = lambda dv: dv["d"]
    box(c, "M1", L(sabp).left, yt + 0.07, L(sabp).right, ys)                          # SABP source into the tap
    yv = ys + 0.5
    box(c, "M1", R(sabp).left, yv - 0.145, xc + 0.145, yv + 0.145)                    # SABP drain -> vabp riser
    fill(c, "Via1", xc - 0.095, yv - 0.095, xc + 0.095, yv + 0.095)
    fill(c, "Via1", xc - 0.095, bt.bottom + 0.015, xc + 0.095, bt.top - 0.015)        # riser on the vabp bar
    box(c, "M2", xc - 0.15, bt.bottom - 0.04, xc + 0.15, ytop)
    pin(c, "M2", "vabp", xc - 0.15, ytop - 0.4, xc + 0.15, ytop)
    box(c, "M1", R(sa).left, st, R(sa).right, ytop)                                   # vddo up to the top edge
    pin(c, "M1", "vddo", R(sa).left, ytop - 0.4, R(sa).right, ytop)
    xa = L(sa).center().x                                                               # a: Via1, M2 east, down
    box(c, "M1", xa - 0.145, yv - 0.145, xa + 0.145, yv + 0.145)
    fill(c, "Via1", xa - 0.095, yv - 0.095, xa + 0.095, yv + 0.095)
    xs = xr + 0.30 + 0.62 + 0.10
    box(c, "M2", xa - 0.145, yv - 0.145, xs + 0.30, yv + 0.145)
    box(c, "M2", xs, -0.545, xs + 0.30, yv + 0.145)
    nets = {"FPL": ("l1", "l2"), "RP2": ("vabp", "dabp"), "ABP": ("b", "a")}
    xa_pin = None
    for i, (dv, n) in enumerate(zip(row, lab)):
        if n == "D":
            dev(c, "D%d" % i, "vdd", "vdd", "vdd", A)
            box(c, "M1", dv["act"].left + 0.07, top + 0.18, dv["act"].right - 0.07, yt + 0.30)
            for s_ in (dv["s"], dv["d"]):
                box(c, "M1", s_.left, top, s_.right, yt)
            continue
        d, s = nets[n]
        dev(c, n, d, "vabp", s, A)
        sd = {"FPL": (dv["d"], dv["s"]), "RP2": (dv["s"], dv["d"]), "ABP": (dv["s"], dv["d"])}[n]
        for s_, net in zip(sd, (d, s)):
            if net == "vabp":
                box(c, "M1", s_.left, top, s_.right, bt.bottom)
            else:
                box(c, "M1", s_.left, b.bottom, s_.right, 0)
                pin(c, "M1", net, s_.left, b.bottom, s_.right, b.bottom + 0.4)
                if net == "a":
                    xa_pin = s_.center().x
    box(c, "M2", xa_pin - 0.145, -0.545, xs + 0.30, -0.255)
    box(c, "M1", xa_pin - 0.145, -0.545, xa_pin + 0.145, -0.255)
    fill(c, "Via1", xa_pin - 0.095, -0.495, xa_pin + 0.095, -0.305)
    pin(c, "M1", "vdd", xc - 1.0, yt, xc + 1.0, yt + 0.30)
    well(c, b)
    return finish(c, ["a", "b", "dabp", "en_3v3", "l1", "l2", "vabp", "vdd", "vddo"])


def bias_tree_p_f2():
    c = ly.create_cell("bias_tree_p_f2")
    N, P = mos(2, 6), mos(5, 6)
    lab = ["PBNC", "PBN", "PABN", "D"]
    (row,), xc = rows(c, [N, P, P, N], [lab], True)
    h = 6.68
    x0, x1 = row[0]["act"].left, row[-1]["act"].right
    b = pya.DBox(x0 - (RG + 0.92), -h - 0.22 - 0.62, x1 + (RG + 0.92), 0.62)
    gl, gr = gate_cols(c, row)
    box(c, "M1", gl.left, gl.top, gl.right, b.top)
    pin(c, "M1", "vbp", gl.left, b.top - 0.4, gl.right, b.top)
    for dv, n, net in zip(row, lab, ["vbnc", "vbn", "vabn", "vdd"]):
        cx = dv["act"].center().x
        dev(c, n, net, "vbp", "vdd", dv["key"])
        if n == "D":
            box(c, "M1", cx, dv["d"].top - 0.11, x1 + (RG + 0.30), dv["d"].top + 0.18)
            continue
        tab3(c, cx, dv["d"].bottom, 0.32, (0.12, b.top))
        pin(c, "M2", net, cx - 0.555, 0.12, cx + 0.555, b.top)
    box(c, "M1", x0, -h - 0.22, x1, -h + 0.23)
    box(c, "M1", x0 - (RG + 0.30), -h - 0.22, x1 + (RG + 0.30), -h + 0.14)
    ring(c, x0 - RG, -h - 0.22, x1 + RG, 0, strips=False)
    pin(c, "M1", "vdd", x0 - RG - 0.30, -h + 0.5, x0 - RG, -h + 2.5)
    well(c, b)
    return finish(c, ["vabn", "vbn", "vbnc", "vbp", "vdd"])


if __name__ == "__main__":
    out_gds, out_cdl = sys.argv[1], sys.argv[2]
    cells = [ab_p_f2(), bias_tree_p_f2()]
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(out_gds, opt)
    txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* F2 PMOS cells, stage B (build_f2b_p.py, C2 2026-11-03); one line per finger, dummies included.", ""]
    for c in cells:
        ports, lines = p2.CDL[c.name]
        txt += [".SUBCKT %s %s" % (c.name, " ".join(ports))] + lines + [".ENDS %s" % c.name, ""]
    open(out_cdl, "w").write("\n".join(txt))
    for c in cells:
        bb = c.dbbox()
        print("%-16s %7.3f x %7.3f um" % (c.name, bb.width(), bb.height()))
        for n, m, pb in p2.PINS[c.name]:
            print("    %-9s %s  (%.3f, %.3f; %.3f, %.3f)" % (n, m, pb.left, pb.bottom, pb.right, pb.top))
