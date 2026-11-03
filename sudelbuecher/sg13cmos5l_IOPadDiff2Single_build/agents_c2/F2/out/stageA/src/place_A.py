# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 (C2, 2026-11-03), stage A: place the reviewed primitives and F2's reworked copies in the pad top, unrouted.

    python3 place_A.py <pad_ctx.gds> <p2.gds> <f2_p.gds> <f2_n.gds> <f2_sp.gds> <out_dir>

pad_ctx.gds = the pad cell as drawn + rejected F's stage-2 pad-top cells (d2s_cma / d2s_cmb, cm_rings, guard_tie,
nw_isolator, edge_stubs), rebuilt by F's build_pad.py from the design checkout (re-checked in stage B).
Writes <out_dir>/placement_A.gds (top sg13cmos5l_IOPadDiff2Single, the cells placed as instances, no routing) and
<out_dir>/placement_A.tsv (cell, orientation, bbox). The 63/0 TEXT.drawing box of the top cell is deleted
(Christoph, 2026-10-31 16:50).

Placement (bottom up, from the drawn cells; the floorplan follows them):
  bottom row, on the a / b joins (y 88.3), left to right: CMA's 2 kOhm stage d2s_sp2k_f2 | loads | ab_p_f2 (+ pd_p
    on it) | ab_n_f2 | pd_n_f2 | CMB's 2 kOhm stage (the same cell, M90): the two stages mirror images at the pad edges
  column A (P, one iovdd well), x 2.5 .. 43.42, the width of d2s_inputs:
    casc_p  ->  tails (M0)  ->  inputs  ->  bias_tree_p_f2 (M0, right-aligned)
  column B (N, substrate), x 43.8 .. 77.85:
    B1 (x 46.0 .. 59.8): casc_n_f2 (R90) -> rhigh_f2 (M0, terminals down) -> spare
    B2 (x 61.3 .. 77.81): sinks_6x6_f2 (R90) -> spare
    top: bias_tree_n_f2 (M0), its TGN / TDN block next to bias_tree_p_f2's TGP
  The stages' NWells (iovdd, n+ guard ring) stay 1.8 um (NW_b1) from the circuit's wells: own guard, own well.
Spacings (sg13cmos5l_tech_default.json): P cells' bbox = their NWell; N cells' bbox = ThickGateOx (Activ + 0.27) or
pins. N+ / P+ tie in ThickGateOx to NWell 0.62 (NW_d1 / NW_f1) -> >= 0.35 between a P and an N bbox; NWells of the
same net >= 0.62 (NW_b) or merged; right edge stub NWell at x 78.2 (y 147.73 .. 149.27) -> N Activ <= 77.58.
"""
import csv
import sys

import klayout.db as db

PAD, P2, F2P, F2N, F2SP, OUT = sys.argv[1:7]
ly = db.Layout()
ly.read(PAD)
top = ly.top_cell()
src = {}
for f in (P2, F2P, F2N, F2SP):
    s = db.Layout()
    s.read(f)
    for c in s.each_cell():
        src.setdefault(c.name, (s, c))

T = {"R0": db.DTrans(), "M0": db.DTrans(db.DTrans.M0, 0, 0), "R90": db.DTrans(db.DTrans.R90, 0, 0),
     "M90": db.DTrans(db.DTrans.M90, 0, 0)}
# (cell, orientation, x of the placed bbox's left edge, y of its bottom edge, block)
PLACE = [
    ("d2s_sp2k_f2", "R0", 2.50, 88.30, "S", "sp2k_cma"),     # CMA's stage; pad pin x 4.14 .. 4.98 at the bottom
    ("d2s_loads_c2", "R0", 12.16, 88.30, "P", None),         # NW_b1 1.80 from the stage's NWell
    ("d2s_ab_p_f2", "R0", 42.85, 88.30, "P", None),          # abuts loads: one NWell / ThickGateOx (NW_b1, TGO_e)
    ("d2s_pd_p_c2", "R0", 45.42, 97.30, "P", None),          # on ab_p, its vabp drain pad on ab_p's vabp pin (M2_b)
    ("d2s_ab_n_f2", "R0", 53.46, 88.30, "N", None),          # TGO_e 0.86 / NW_d1 from ab_p
    ("d2s_pd_n_f2", "R0", 64.10, 88.30, "N", None),          # TGO_e 0.86 from ab_n
    ("d2s_sp2k_f2", "M90", 69.99, 88.30, "S", "sp2k_cmb"),   # CMB's stage, mirror image; NWell edge at 77.85
    ("d2s_casc_p_c2", "R0", 2.50, 104.85, "P", None),        # NW_b1 1.80 above the CMA stage's NWell
    ("d2s_tails_c2", "M0", 4.13, 121.00, "P", None),
    ("d2s_inputs_c2", "R0", 2.50, 138.60, "P", None),
    ("bias_tree_p_f2", "M0", 23.89, 169.80, "P", None),
    ("d2s_casc_n_f2", "R90", 46.695, 101.15, "N", None),     # TGO_e 0.86 above pd_p (also NW_d1 0.62)
    ("d2s_rhigh_f2", "M0", 46.00, 142.55, "N", None),
    ("sinks_6x6_f2", "R90", 61.30, 103.40, "N", None),        # above the CMB stage's NWell
    ("bias_tree_n_f2", "M0", 46.00, 169.50, "N", None),
]
# well bridge (not routing): the inputs' lower-left dummy tub well (vdd = iovdd) joined to the left edge stub's
# iovdd NWell (147.73 .. 149.27, x .. 1.80); otherwise NW_b1 1.80 between them until both are tied
FILLS = [((31, 0), db.DBox(1.80, 147.73, 2.50, 149.27))]

if __name__ == "__main__":
    t63 = ly.find_layer(63, 0)
    if t63 is not None:
        top.shapes(t63).clear()
    rows = []
    for (l, d), b in FILLS:
        top.shapes(ly.layer(l, d)).insert(b)
    made = {}
    for name, o, x, y, blk, label in PLACE:
        s, sc = src[name]
        if name not in made:
            made[name] = ly.create_cell(name)
            made[name].copy_tree(sc)
        c = made[name]
        b = c.dbbox().transformed(T[o])
        t = db.DTrans(db.DVector(round(x - b.left, 3), round(y - b.bottom, 3))) * T[o]
        top.insert(db.DCellInstArray(c.cell_index(), t))
        pb = c.dbbox().transformed(t)
        rows.append((label or name, o, blk, round(pb.left, 3), round(pb.bottom, 3), round(pb.right, 3), round(pb.top, 3),
                     round(pb.width() * pb.height(), 1)))
    # overlap check of the placed bboxes
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a = db.DBox(*rows[i][3:7])
            b = db.DBox(*rows[j][3:7])
            if a.overlaps(b):
                print("OVERLAP", rows[i][0], rows[j][0])
    opt = db.SaveLayoutOptions()
    opt.gds2_write_timestamps = False
    opt.write_context_info = True
    ly.write(OUT + "/placement_A.gds", opt)
    with open(OUT + "/placement_A.tsv", "w") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["cell", "orientation", "block", "x0", "y0", "x1", "y1", "area_um2"])
        w.writerows(rows)
    for r in rows:
        print("%-16s %-3s %s  x %7.3f .. %7.3f  y %7.3f .. %7.3f  %7.1f um2" % (r[0], r[1], r[2], r[3], r[5], r[4],
                                                                              r[6], r[7]))
