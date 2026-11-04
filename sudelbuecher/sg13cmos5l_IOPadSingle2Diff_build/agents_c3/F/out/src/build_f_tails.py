# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_f_tails.py (F, C3, 2026-11-03): s2d_tails_c3 split into its two rows, one above and one below the input
tubs, so that every tail drain faces its own tub's source pin (brief rule 2: each tail under its tub's column; short
sa / sb wires of equal length).

    python3 build_f_tails.py <out.gds> <out.cdl> [png dir]    (needs the PDK; uses P's helpers, p3lib.py = build_s2d_p3.py)

s2d_tails_hi_f  BP | A1a F2b F1b A2a M1a M2b | D    P's upper row, placed above the inputs (drains face down)
s2d_tails_lo_f  D  | A2b F1a F2a A1b M1b M2a | D    P's lower row, placed below the inputs with M0 (drains face up)

Each row is built exactly as in P's tails() (same PCells, positions, gate columns, drain pads, BP lane, dummy ties),
in P's lower-row frame (sources at y = 0, drains at the bottom). Changes against s2d_tails_c3:
  - one row per cell; the shared vdd plate between the rows becomes the row's own source plate, joined directly to
    the ring's top strip, which sits 0.43 above the source Activ (pSD_i1 0.40 + pSD_d1 0.03, as P's tub tie);
  - the poly bridge between the two rows' gate tabs goes (one row); each cell gets its own vbp edge stub, at the
    right row end (P's cell had one, at the left; stage A had both ends, stage B2 drops the left one);
  - closed N+ ring and one NWell per cell (NW_c1 / NW_e1 0.62, as P).
The two cells are mirror images of each other in the device layers (BP is the same 5/6 device as D).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3lib as P  # noqa: E402
import pya         # noqa: E402

OUT_GDS, OUT_CDL = sys.argv[1], sys.argv[2]


def tails_row(name, names):
    c = P.ly.create_cell(name)
    T = P.mos(5, 6)
    (lo,), xc = P.rows(c, [T] * 8, [names], False)
    h = 6.68
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    top_in = 0.43                                            # ring top strip, inner edge (pSD_i1 + pSD_d1)
    b = pya.DBox(x0 - (P.RG + 0.92), -h - 1.13, x1 + (P.RG + 0.92), top_in + 0.30 + 0.62)
    gl, gr = P.gate_cols(c, lo)
    P.box(c, "M1", x0, -0.23, x1, top_in + 0.30)             # source plate over the source stripes, into the ring
    P.ring(c, x0 - P.RG, -h - 0.51, x1 + P.RG, top_in + 0.30)
    for i, (dv, n) in enumerate(zip(lo, names)):
        a, cx = dv["act"], dv["act"].center().x
        if n == "D":                                         # dummy drain straight into the ring strip
            P.dev(c, "D%d" % i, "vdd", "vbp", "vdd", T)
            P.box(c, "M1", a.left, -h - 0.21, a.right, -6.45)
            continue
        if n == "BP":                                        # diode: drain lane into its own gate column
            P.dev(c, "BP", "vbp", "vbp", "vdd", T)
            P.box(c, "M1", gl.left, -6.65, gl.right, gl.bottom + 0.01)   # 0.24 (M1_e) above the ring strip
            P.box(c, "M1", gl.left, -6.65, a.left + 1.0, -6.39)          # beyond BP's gate
            continue
        net = ("sa_" if n[-1] == "a" else "sb_") + n[:-1]
        P.dev(c, "T" + n, net, "vbp", "vdd", T)
        P.box(c, "M1", cx - 0.555, -6.67, cx + 0.555, -6.38)
        P.fill(c, "Via1", cx - 0.505, -6.62, cx + 0.505, -6.43)
        P.box(c, "M2", cx - 0.555, -6.38, cx + 0.555, b.bottom)
        P.pin(c, "M2", net, cx - 0.555, b.bottom, cx + 0.555, b.bottom + 0.30)
    # vbp leaves at the right row end only (stage B2, Christoph: no vbp on the left; the bias tree sits on the right).
    # P's cell had its stub at the left end.
    P.edge_stub(c, gr, gr.center().y, b.right, "vbp")
    P.pin(c, "M1", "vdd", x0 - P.RG - 0.30, -h + 0.5, x0 - P.RG, -h + 2.5)
    P.well(c, b)
    nets = sorted({("sa_" if n[-1] == "a" else "sb_") + n[:-1] for n in names if n not in ("D", "BP")})
    return P.finish(c, nets + ["vbp", "vdd"])


cells = [tails_row("s2d_tails_hi_f", ["BP", "A1a", "F2b", "F1b", "A2a", "M1a", "M2b", "D"]),
         tails_row("s2d_tails_lo_f", ["D", "A2b", "F1a", "F2a", "A1b", "M1b", "M2a", "D"])]
keep = {c.cell_index() for c in cells}
for c in cells:
    keep |= set(c.called_cells())
for ci in [c.cell_index() for c in P.ly.each_cell() if c.cell_index() not in keep]:
    P.ly.delete_cell(ci)
opt = pya.SaveLayoutOptions()
opt.write_context_info = False
opt.gds2_write_timestamps = False
P.ly.write(OUT_GDS, opt)
txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
       "* reference netlists of F's split tails rows (build_f_tails.py, C3, 2026-11-03); dummies D = S = vdd", ""]
for c in cells:
    ports, lines = P.CDL[c.name]
    txt += [".SUBCKT %s %s" % (c.name, " ".join(ports))] + lines + [".ENDS %s" % c.name, ""]
open(OUT_CDL, "w").write("\n".join(txt))
for c in cells:
    bb = c.dbbox()
    print("%-16s %7.3f x %7.3f um" % (c.name, bb.width(), bb.height()))
    for n, m, pb in P.PINS[c.name]:
        print("    %-6s %s  (%.3f, %.3f; %.3f, %.3f)" % (n, m, pb.left, pb.bottom, pb.right, pb.top))
if len(sys.argv) > 3:                                        # cell pictures (P's render) into the given directory
    P.OUT = sys.argv[3]
    for c in cells:
        P.render(c, c.name + ".png")
        P.render(c, c.name + "_row_end.png", (0, 0, 9.0, 9.16))
