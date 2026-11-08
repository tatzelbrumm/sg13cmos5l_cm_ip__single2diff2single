# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_rb_avg_v3.py: rb_avg (the averaging diodes SU, SL1, SL2 of vcm_rb) with abutted gate poly, pad_ref_rb
(IHP sg13cmos5l), C4, agent P3, 2026-11-07, Claude.

    python3 build_rb_avg_v3.py [--no-png]    (needs the PDK: PDK_ROOT, default /foss/pdks; writes next to this file)

Christoph: "rb_avg: why can't you abut by gate poly? there's PLENTY of precedent in the bias generators and pads".
Built with the pads' row code: C3's build_s2d_p3.py (imported unchanged from ../../P/out, sha256 874063e7aff4)
rows() / gate_cols() / tap() / well(), i.e. the construction of the pad's s2d_loads / s2d_casc_p rows, whose row
ends already hold this very finger (hv PMOS 1/4, the "X" end dummies) with gate poly abutted to the row's gate.

Two wells, one per bulk net, one row each, the same construction and orientation (translated, not mirrored, so
all three active fingers carry current in the same direction):
  upper row, well gh :  DU0 | SU  | DU1          gate strip m  (SU  m m gh gh;  dummies gh m gh gh)
  lower row, well m  :  DL0 | SL1 SL2 | DL1      gate strip xp (SLi xp xp m m;  dummies m xp m m)
Per row: fingers rotated (W along x), Activ 0.25 apart (Gat.b1), end caps merged into one gate strip, contacted
only by the two gate columns at the row ends (gate_cols: full-width tab, no center contact); sources up, under one
Metal1 plate into the tie; the tie is a ring open on the drain side (top strip 0.21 from the source Activ =
pSD.c 0.18 + pSD.d1 0.03, side strips at RG 0.80 as the pads' rings); dummy drains straight up over their own
channel into the source plate (source and drain on the well's rail, gate by abutment); active drains down onto
a Metal1 bar (M1.e 0.22 below the dummies' drain boxes) that runs into both gate columns (the diode).
Upper bar (m) drops straight onto the lower row's tie strip (m) across the NWell gap (NW.b1 1.80).
Writes rb_avg_v3.gds (top cell rb_avg), rb_avg_v3.cdl, PNGs.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True                         # no __pycache__ in P's folder
sys.path.insert(0, os.path.join(HERE, "..", "..", "P", "out"))
import build_s2d_p3 as P     # noqa: E402  C3's generator, unchanged
import pya                   # noqa: E402

P.OUT = HERE
ly, box, note, pin, RG = P.ly, P.box, P.note, P.pin, P.RG
K = P.mos(1, 4)              # the pad's pmosHV_w1_l4 finger: Activ 1.0 x 4.68, gate 4.0, S / D stripes 0.34
H = 4.68                     # Activ length (L + 2 x 0.34)
YB = (-5.09, -4.83)          # drain bar: M1.e 0.22 below the dummies' drain boxes (-4.61), 0.26 wide
WT = 0.51 + 0.62             # well top above the row's source Activ edge: tie 0.21 ... 0.51, NW.e1 0.62
WB = -H - 0.62               # well bottom: NW.c1 0.62 below the drain Activ


def diode_row(name, labels):
    """one row of 1/4 fingers, labels with a leading 'D' are dummies; returns (cell, Activ x0, x1, xc)"""
    c = ly.create_cell(name)
    (row,), xc = P.rows(c, [K] * len(labels), [labels], False)    # src_out False: sources at y = 0, drains below
    x0, x1 = row[0]["act"].left, row[-1]["act"].right
    cols = P.gate_cols(c, row)
    box(c, "M1", x0, -0.23, x1, 0.51)                             # source plate into the tie strip
    # tie: top strip, contacts per finger (3 over each finger's Activ, so every finger sees the same contacts
    # whatever the row length) and over the strip ends beyond the gate columns ...
    box(c, "Activ", x0 - RG - 0.30, 0.21, x1 + RG + 0.30, 0.51)
    box(c, "M1", x0 - RG - 0.30, 0.21, x1 + RG + 0.30, 0.51)
    for dv in row:
        P.fill(c, "Cont", dv["act"].left, 0.28, dv["act"].right, 0.44)
    for xa, xb in ((x0 - RG - 0.23, x0 - 0.25), (x1 + 0.25, x1 + RG + 0.23)):
        P.fill(c, "Cont", xa, 0.28, xb, 0.44)
    for xa in (x0 - RG - 0.30, x1 + RG):                          # ... and side strips (open on the drain side)
        P.tap(c, xa, -H, xa + 0.30, 0.21, (xa + 0.07, -H + 0.07, xa + 0.23, 0.10))
    for dv, n in zip(row, labels):
        a = dv["act"]
        if n.startswith("D"):                                     # dummy drain over its channel into the plate
            box(c, "M1", a.left, -4.61, a.right, -0.07)
        else:                                                     # active drain down onto the bar
            box(c, "M1", a.left, YB[1], a.right, -4.45)
    box(c, "M1", x0 - 0.51, YB[0], x1 + 0.51, YB[1])              # bar into both gate columns (diode)
    for g in cols:
        box(c, "M1", g.left, YB[0], g.right, g.bottom + 0.01)
    P.well(c, pya.DBox(x0 - RG - 0.92, WB, x1 + RG + 0.92, WT))
    return c, x0, x1, xc


def avg():
    up_n, lo_n = ["DU0", "SU", "DU1"], ["DL0", "SL1", "SL2", "DL1"]
    cu, ux0, ux1, uxc = diode_row("rb_avg_u", up_n)
    cl, lx0, lx1, lxc = diode_row("rb_avg_l", lo_n)
    c = ly.create_cell("rb_avg")
    dy = WB - 1.80 - WT                                           # lower row frame: NW.b1 1.80 between the wells
    c.insert(pya.DCellInstArray(cu.cell_index(), pya.DTrans(pya.DVector(lxc - uxc, 0))))
    c.insert(pya.DCellInstArray(cl.cell_index(), pya.DTrans(pya.DVector(0, dy))))
    for n, d, g, s in (("DU0", "gh", "m", "gh"), ("SU", "m", "m", "gh"), ("DU1", "gh", "m", "gh"),
                       ("DL0", "m", "xp", "m"), ("SL1", "xp", "xp", "m"), ("SL2", "xp", "xp", "m"),
                       ("DL1", "m", "xp", "m")):
        P.dev(c, n, d, g, s, K, s)
    ax = lxc                                                      # common axis of both rows
    box(c, "M1", ax - 0.5, dy + 0.21, ax + 0.5, YB[0])            # m: SU's bar straight down onto the lower tie
    xl, xr = lx0 - RG - 0.92, lx1 + RG + 0.92                     # cell edges (lower well)
    for xe, xs in ((xl, lx0 - RG - 0.30), (xr, lx1 + RG + 0.30)):  # m pins: lower tie strip to both side edges
        box(c, "M1", xe, dy + 0.21, xs, dy + 0.51)
        pin(c, "M1", "m", xe, dy + 0.21, xe + (0.30 if xe == xl else -0.30), dy + 0.51)
    box(c, "M1", ax - 0.5, 0.51, ax + 0.5, WT)                    # gh: upper tie strip to the top edge
    pin(c, "M1", "gh", ax - 0.5, WT - 0.30, ax + 0.5, WT)
    box(c, "M1", ax - 0.5, dy + WB, ax + 0.5, dy + YB[0])         # xp: lower bar to the bottom edge
    pin(c, "M1", "xp", ax - 0.5, dy + WB, ax + 0.5, dy + YB[0])
    return P.finish(c, ["gh", "m", "xp"])


def write():
    c = avg()
    for d in list(ly.each_cell()):
        if d.name.startswith("pmosHV"):
            d.name = "rb_" + d.name
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(os.path.join(HERE, "rb_avg_v3.gds"), opt)
    ports, lines = P.CDL[c.name]
    txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* rb_avg_v3.cdl: reference netlist of rb_avg_v3.gds, written by build_rb_avg_v3.py (C4, agent P3, "
           "2026-11-07, Claude).", "* SU, SL1, SL2 as vcm_rb.spice; dummies D = S = B on the well's net, gate by "
           "abutment.", "", ".SUBCKT %s %s" % (c.name, " ".join(ports))] + lines + [".ENDS %s" % c.name, ""]
    open(os.path.join(HERE, "rb_avg_v3.cdl"), "w").write("\n".join(txt))
    b = c.dbbox()
    print("%-10s %7.3f x %7.3f um" % (c.name, b.width(), b.height()))
    for n, m, pb in P.PINS[c.name]:
        print("    %-9s %s  (%.3f, %.3f; %.3f, %.3f)" % (n, m, pb.left, pb.bottom, pb.right, pb.top))
    if "--no-png" not in sys.argv:
        P.render(c, "rb_avg_v3.png")
        P.render(c, "rb_avg_v3_lower_end.png", (0, 0, 4.5, 7.0))


if __name__ == "__main__":
    write()
