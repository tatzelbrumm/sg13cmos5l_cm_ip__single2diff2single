# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 (C2, 2026-11-03), stage A: F2's reworked copies of P2's PMOS primitives.

    python3 build_f2_p.py <out.gds> <out.cdl>

Imports P2's build script (agents_c2/P2/out/build_d2s_p2.py) as a library (it only writes files in write()), so the
devices, gate columns, ties, wells and tabs are P2's code and rule values. Changes (Christoph's review,
agents_c2/P2/out/d2s_p2_cells_human_review.txt):

  d2s_ab_p_f2     "workable if F revises well tap": the single N+ strip above the heads becomes a U, the strip plus
                  two legs beside the end dummies down to the pin edge (Act_b 0.21 from the dummies), so the whole
                  well edge except the pin side is tied. Devices, heads, vabp bar, pins unchanged.
  bias_tree_p_f2  "workable if TGP is moved by F as pad layout requires": TGP moved from under the middle of the row
                  to the right end, outside the right tie (Act_b 0.21), gate head pointing down as before; iref,
                  en_3v3_b, ni leave on Metal1 at the bottom edge as before. In the pad the cell is placed flipped
                  (drains down to their loads), so TGP sits at the top right, next to bias_tree_n_f2's TGN / TDN.
                  Cell 1.18 um lower, 1.34 um wider.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/sudel/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/P2/out")
import build_d2s_p2 as p2                     # noqa: E402

pya, ly, box, fill, pin, tap, well = p2.pya, p2.ly, p2.box, p2.fill, p2.pin, p2.tap, p2.well
mos, place, dev, rows, gate_cols, tab3, ring, upright, finish = (p2.mos, p2.place, p2.dev, p2.rows, p2.gate_cols,
                                                                 p2.tab3, p2.ring, p2.upright, p2.finish)
RG = p2.RG


def ab_p_f2():
    c = ly.create_cell("d2s_ab_p_f2")
    A = mos(6.66, 0.6)
    lab = ["D", "FPL", "RP2", "ABP", "D"]
    row, xc = upright(c, [A] * 5, lab, 0.21)
    top = row[0]["act"].top
    bt = pya.DBox(row[1]["gate"].center().x - 0.13, top + 0.18, row[3]["gate"].center().x + 0.13, top + 0.40)
    box(c, "M1", bt.left, bt.bottom, bt.right, bt.top)
    yt = top + 0.80
    xl, xr = row[0]["act"].left - 0.21 - 0.30, row[-1]["act"].right + 0.21     # U legs: Act_b 0.21 from the dummies
    tap(c, xl, yt, xr + 0.30, yt + 0.30)                                        # top strip, now over the legs too
    for x0 in (xl, xr):                                                         # contacts Cnt_b 0.18 below the strip's
        tap(c, x0, 0.0, x0 + 0.30, yt, (x0 + 0.07, 0.07, x0 + 0.23, yt - 0.11))
    b = pya.DBox(xl - 0.62, -0.62, xr + 0.30 + 0.62, yt + 0.92)                 # NW_e1 0.62 around the N+ tie
    fill(c, "Via1", xc - 0.095, bt.bottom + 0.015, xc + 0.095, bt.top - 0.015)
    box(c, "M2", xc - 0.15, bt.bottom - 0.04, xc + 0.15, b.top)
    pin(c, "M2", "vabp", xc - 0.15, b.top - 0.4, xc + 0.15, b.top)
    nets = {"FPL": ("l1", "l2"), "RP2": ("vabp", "dabp"), "ABP": ("b", "a")}
    for i, (dv, n) in enumerate(zip(row, lab)):
        if n == "D":
            dev(c, "D%d" % i, "vdd", "vdd", "vdd", A)
            box(c, "M1", dv["act"].left + 0.07, top + 0.18, dv["act"].right - 0.07, yt + 0.30)
            for st in (dv["s"], dv["d"]):
                box(c, "M1", st.left, top, st.right, yt)
            continue
        d, s = nets[n]
        dev(c, n, d, "vabp", s, A)
        sd = {"FPL": (dv["d"], dv["s"]), "RP2": (dv["s"], dv["d"]), "ABP": (dv["s"], dv["d"])}[n]
        for st, net in zip(sd, (d, s)):
            if net == "vabp":
                box(c, "M1", st.left, top, st.right, bt.bottom)
            else:
                box(c, "M1", st.left, b.bottom, st.right, 0)
                pin(c, "M1", net, st.left, b.bottom, st.right, b.bottom + 0.4)
    pin(c, "M1", "vdd", xc - 1.0, yt, xc + 1.0, yt + 0.30)
    well(c, b)
    return finish(c, ["a", "b", "dabp", "l1", "l2", "vabp", "vdd"])


def bias_tree_p_f2():
    c = ly.create_cell("bias_tree_p_f2")
    N, P, S = mos(2, 6), mos(5, 6), mos(1, 0.45)
    lab = ["PBNC", "PBN", "PABN", "D"]
    (row,), xc = rows(c, [N, P, P, N], [lab], True)
    h = 6.68
    x0, x1 = row[0]["act"].left, row[-1]["act"].right
    # TGP right of the right tie (tie Activ x1 + RG .. + 0.30), Act_b 0.21; Activ y -h - 0.22 .. -h + 0.78
    xt = x1 + RG + 0.30 + 0.21
    ya = -h - 0.22 + 1.0
    t = pya.DTrans(pya.DTrans.M0, pya.DVector(xt, ya))
    tg = place(c, S, t, "TGP")
    dev(c, "TGP", "iref", "en_3v3_b", "ni", S)
    a = tg["act"]
    b = pya.DBox(x0 - (RG + 0.92), a.bottom - 0.62, a.right + 0.62, 0.62)       # NW_c1 0.62 around TGP's P+
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
    gx = a.center().x
    box(c, "GatPoly", gx - 0.225, a.bottom - 0.56, gx + 0.225, a.bottom)
    fill(c, "Cont", gx - 0.08, a.bottom - 0.34, gx + 0.08, a.bottom - 0.18)
    box(c, "M1", gx - 0.13, b.bottom, gx + 0.13, a.bottom - 0.18)
    pin(c, "M1", "en_3v3_b", gx - 0.13, b.bottom, gx + 0.13, b.bottom + 0.3)
    for st, net, sg in ((tg["s"], "iref", -1), (tg["d"], "ni", 1)):
        xo = st.left - 0.10 if sg < 0 else st.right + 0.10
        box(c, "M1", min(xo, st.left), b.bottom, max(xo, st.right), st.top)
        pin(c, "M1", net, min(xo, st.left), b.bottom, max(xo, st.right), b.bottom + 0.3)
    well(c, b)
    return finish(c, ["en_3v3_b", "iref", "ni", "vabn", "vbn", "vbnc", "vbp", "vdd"])


if __name__ == "__main__":
    out_gds, out_cdl = sys.argv[1], sys.argv[2]
    cells = [ab_p_f2(), bias_tree_p_f2()]
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(out_gds, opt)
    txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* F2 reworked PMOS cells (build_f2_p.py, C2 2026-11-03); one line per finger, dummies included.", ""]
    for c in cells:
        ports, lines = p2.CDL[c.name]
        txt += [".SUBCKT %s %s" % (c.name, " ".join(ports))] + lines + [".ENDS %s" % c.name, ""]
    open(out_cdl, "w").write("\n".join(txt))
    for c in cells:
        bb = c.dbbox()
        print("%-16s %7.3f x %7.3f um" % (c.name, bb.width(), bb.height()))
        for n, m, pb in p2.PINS[c.name]:
            print("    %-9s %s  (%.3f, %.3f; %.3f, %.3f)" % (n, m, pb.left, pb.bottom, pb.right, pb.top))
