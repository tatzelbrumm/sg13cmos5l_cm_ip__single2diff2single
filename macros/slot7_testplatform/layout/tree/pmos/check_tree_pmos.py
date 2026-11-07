# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Geometric checks of tree_pmos.gds that the PDK decks do not make (2026-11-07, Claude).

1. LU.a (PMOS latch-up): the ihp-sg13cmos5l.drc run deck implements only LU.b (rule_decks/feol/7_2_latchup.drc);
   LU.a of sg13cmos5l_maximal.drc: P+Activ in NWell within LU_a = 20 um of an N tie (N+Activ in NWell), grown inside
   the NWell. Here: the tie grown in 0.5 um steps inside the NWell (as the deck does), plus the exact farthest
   Euclidean distance.
2. Matching of the mirror row: the device centroids per drain net (from the Via1 on each finger's tab), and the XOR of
   the row's device layers with their mirror image about the row centre.
Usage: python3 check_tree_pmos.py [tree_pmos.gds]
"""
import os
import sys
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
gds = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "tree_pmos.gds")
ly = db.Layout()
ly.read(gds)
top = ly.cell("tree_pmos")
dbu = ly.dbu
L = {n: ly.layer(*v) for n, v in {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "M1": (8, 0), "Via1": (19, 0),
                                   "M2": (10, 0), "pSD": (14, 0), "NWell": (31, 0), "TGO": (44, 0)}.items()}


def R(n):
    return db.Region(top.begin_shapes_rec(L[n])).merged()


act, psd, nw = R("Activ"), R("pSD"), R("NWell")
pact = (act & psd) & nw
ntie = (act - psd) & nw
print("== LU.a (LU_a = 20.0 um, json key LU_a)")
grown = ntie.dup()
for _ in range(40):                       # 40 x 0.5 um = 20 um, grown inside the NWell
    grown = (grown.sized(int(0.5 / dbu)) & nw)
uncov = pact - grown
print("  P+Activ shapes: %d, not within 20 um of a tie: %d" % (pact.count(), uncov.count()))
far = 0.0


def box_dist(pt, b):
    dx = max(b.left - pt.x, 0, pt.x - b.right)
    dy = max(b.bottom - pt.y, 0, pt.y - b.top)
    return (dx * dx + dy * dy) ** 0.5


for p in pact.each():
    for pt in p.each_point_hull():
        far = max(far, min(box_dist(pt, t.bbox()) for t in ntie.each()) * dbu)
print("  farthest P+Activ corner from the tie: %.2f um (tie: %s)" % (far, ntie.bbox().to_dtype(dbu)))

print("== mirror row: centroids per drain net (finger pitch units from the row centre)")
vias = R("Via1")
m2 = db.Region(top.begin_shapes_rec(L["M2"]))
gate = R("GatPoly") & act
fingers = sorted((g.bbox() for g in gate.each() if g.bbox().height() * dbu > 5.9), key=lambda b: b.left)
x0 = fingers[0].left
x1 = fingers[-1].right
xc = (x0 + x1) / 2
pitch = 1.25
# lanes by y (from the generator: vbp lowest, then vbn, vbnc)
lanes = sorted({round(v.bbox().center().y * dbu, 3) for v in vias.each()
                if x0 <= v.bbox().center().x <= x1})
names = dict(zip(lanes, ["vbp", "vbn", "vbnc"]))
cen = {}
for v in vias.each():
    c = v.bbox().center()
    if x0 <= c.x <= x1:
        n = names[round(c.y * dbu, 3)]
        cen.setdefault(n, []).append((c.x - xc) * dbu / pitch)
for n, xs in cen.items():
    m1 = sum(xs) / len(xs)
    m2_ = sum(x * x for x in xs) / len(xs)
    print("  %-5s %d fingers: positions %s, centroid %+.3f, mean square %.2f" %
          (n, len(xs), " ".join("%+.0f" % x for x in sorted(xs)), m1, m2_))
print("== mirror row: XOR with its mirror image about x = %.3f um" % (xc * dbu))
ya0, ya1 = fingers[0].bottom - int(0.34 / dbu), fingers[0].top + int(0.34 / dbu)    # the row's Activ in y
print("  (window: the row's Activ x %.3f .. %.3f, y %.3f .. %.3f; the tie above is excluded)"
      % (x0 * dbu, x1 * dbu, ya0 * dbu, ya1 * dbu))
win = db.Region(db.Box(x0 - int(1.0 / dbu), ya0, x1 + int(1.0 / dbu), ya1))
mir = db.Trans(db.Trans.M90, db.Vector(int(2 * xc), 0))
for n in ("Activ", "GatPoly", "Cont", "pSD", "M1", "Via1", "M2"):
    r = R(n) & win
    x = (r ^ r.transformed(mir)) & db.Region(db.Box(x0, ya0, x1, ya1))
    print("  %-7s XOR area %.4f um2  (%d shapes)" % (n, x.area() * dbu * dbu, x.count()))
