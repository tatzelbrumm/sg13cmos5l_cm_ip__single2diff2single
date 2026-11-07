# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""compare_pad.py: rb_p_cells.gds against the drawn s2d pad (C4, agent P, 2026-11-07, Claude).

    python3 compare_pad.py <rb_p_cells.gds> <sg13cmos5l_IOPadSingle2Diff.klay.gds>

Flat XOR per layer (um2) of each replica row against the pad row it copies, the two placed so that their Activ
bounding boxes' lower left corners meet (the right-hand window of rb_tails: lower right corners). DEV = the device
layers (Activ, GatPoly, Cont, pSD, NWell, ThickGateOx); ALL = every layer, pins and metal included."""
import sys

import klayout.db as db

DEV = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "pSD": (14, 0), "NWell": (31, 0), "TGO": (44, 0)}
a, p = db.Layout(), db.Layout()
a.read(sys.argv[1])
p.read(sys.argv[2])
U = a.dbu


def reg(ly, c, ld):
    i = ly.find_layer(*ld)
    return db.Region(c.begin_shapes_rec(i)).merged() if i is not None else db.Region()


def xor(rb, pad, layers=None, win=None, right=False):
    """win: (x0, x1[, y0, y1]) in um of rb's Activ frame (Activ bbox lower left = 0); the pad cell likewise"""
    ca, cp = a.cell(rb), p.cell(pad)
    ba, bp = reg(a, ca, DEV["Activ"]).bbox(), reg(p, cp, DEV["Activ"]).bbox()
    ta = db.Trans(-(ba.right if right else ba.left), -ba.bottom)
    tp = db.Trans(-(bp.right if right else bp.left), -bp.bottom)
    lays = layers or sorted({(i.layer, i.datatype) for L in (a, p) for i in L.layer_infos()})
    w = None
    if win:
        x0, x1, y0, y1 = (tuple(win) + (-1e4, 1e4))[:4]
        w = db.Region(db.DBox(x0, y0, x1, y1).to_itype(U))
    out = []
    for ld in (layers.values() if isinstance(layers, dict) else lays):
        ra, rp = reg(a, ca, ld).transformed(ta), reg(p, cp, ld).transformed(tp)
        if w is not None:
            ra, rp = ra & w, rp & w
        x = ra ^ rp
        if not x.is_empty():
            out.append("%d/%d %.4f um2 in %s" % (ld[0], ld[1], x.area() * U * U, x.bbox().to_dtype(U)))
    tag = "%s vs pad %s%s%s" % (rb, pad, " window %s" % (win,) if win else "", " (right-aligned)" if right
                                else "")
    print("%-75s %s" % (tag, "XOR 0" if not out else "XOR:"))
    for o in out:
        print("      " + o)


# leaf devices and the tub: every layer
for rb, pad in (("rb_pmosHV_w2_l6", "pmosHV_w2_l6"), ("rb_pmosHV_w5_l6", "pmosHV_w5_l6"),
                ("rb_pmosHV_w1_l0p45", "pmosHV_w1_l0p45"), ("rb_pmosHV_w20_l1_ng2", "pmosHV_w20_l1_ng2"),
                ("rb_pmosHV_w1_l4", "pmosHV_w1_l4$1"), ("rb_tub_p20x1", "tub_p20x1_c3")):
    xor(rb, pad)
# rb_tree_p: the pad's tree row, every layer (expected: the rewiring only)
xor("rb_tree_p", "bias_tree_noab_p_c3")
xor("rb_tree_p", "bias_tree_noab_p_c3", DEV)
# rb_tails: left window (D TR) against s2d_tails_lo_f's left end (D A2b), right window (BT D) against its right
# end (M2a D) and against s2d_tails_hi_f's right end (M2b D); the window reaches 0.80 + 0.30 + 0.92 beyond the Activ
ha = (4 * 5.0 + 3 * 0.25) / 2                    # half the Activ width of the 4-device row: the TR / BT gap middle
for pad in ("s2d_tails_lo_f", "s2d_tails_hi_f"):
    xor("rb_tails", pad, DEV, (-2.02, ha))
    xor("rb_tails", pad, DEV, (-ha, 2.02), right=True)
    xor("rb_tails", pad, None, (-2.02, ha))
    xor("rb_tails", pad, None, (-ha, 2.02), right=True)
# the same, Cont only, without the ring's top and bottom strips (Activ frame: strips at y 0 .. 0.30, 7.62 .. 7.92)
for pad in ("s2d_tails_lo_f", "s2d_tails_hi_f"):
    xor("rb_tails", pad, {"Cont": (6, 0)}, (-2.02, ha, 0.30, 7.62))
    xor("rb_tails", pad, {"Cont": (6, 0)}, (-ha, 2.02, 0.30, 7.62), right=True)
# rb_tubs: the five tubs against the first five of s2d_inputs_c3's lower row, window = rb_tubs's NWell extent
# (Activ frame: the first tub's tie corner at 0, 0); device layers, then every layer
tw = (-0.62, 4 * 6.10 + 3.68, -1.35 + 0.73, 10.62 + 0.73)
xor("rb_tubs", "s2d_inputs_c3", DEV, tw)
xor("rb_tubs", "s2d_inputs_c3", None, tw)
