# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Geometric checks of bias_tree_noab_pd beyond DRC / LVS (2026-11-07, Claude).

1. Layers: nothing above Metal2 (Via2 and up empty).
2. Pins: every signal pin is Metal2 (10/2 + 10/25) touching the right edge, >= 0.6 um from the next one;
   vdd / vss Metal1 pins span the full top / bottom edge.
3. Latch-up (LU_a = LU_b = 20 um, json keys LU_a, LU_b): every P+Activ in NWell within 20 um of an N tie
   (N+Activ in NWell), every N+Activ outside NWell within 20 um of a p+ tie (P+Activ outside NWell). Exact farthest
   distance over all diffusion corners and edge samples (0.05 um), Euclidean to the nearest tie box.
4. Area against the naive cell macros/slot7_testplatform/layout/gds/bias_tree_noab_pd.gds.
Usage: python3 check_tree.py [gds]
"""
import math
import os
import sys

import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../../../.."))
GDS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "bias_tree_noab_pd.gds")
NAIVE = os.path.join(REPO, "macros/slot7_testplatform/layout/gds/bias_tree_noab_pd.gds")
LU = 20.0

ly = db.Layout()
ly.read(GDS)
top = ly.cell("bias_tree_noab_pd")
dbu = ly.dbu
bb = top.bbox()


def R(l, d=0):
    li = ly.find_layer(l, d)
    return db.Region() if li is None else db.Region(top.begin_shapes_rec(li)).merged()


ok = True
print("== cell", top.name, bb.to_dtype(dbu), "%.3f x %.3f = %.1f um2" % (bb.width() * dbu, bb.height() * dbu,
                                                                      bb.width() * bb.height() * dbu * dbu))
print("== layers above Metal2")
for name, ld in [("Via2", (29, 0)), ("Metal3", (30, 0)), ("Via3", (49, 0)), ("Metal4", (50, 0)),
                 ("Via4", (66, 0)), ("Metal5", (67, 0)), ("TopVia1", (125, 0)), ("TopMetal1", (126, 0))]:
    n = R(*ld).count()
    ok &= n == 0
    print("  %-9s %d shapes" % (name, n))

print("== pins (top-level shapes)")
pins = []
for ld, kind in [((10, 2), "M2"), ((8, 2), "M1")]:
    li = ly.find_layer(*ld)
    tl = ly.find_layer(ld[0], 25)
    texts = [(s.text_string, s.text_pos) for s in top.shapes(tl).each() if s.is_text()]
    for s in top.shapes(li).each():
        b = s.bbox()
        names = [t for t, p in texts if b.contains(p)]
        pins.append((kind, names[0] if names else "?", b))
for kind, n, b in sorted(pins, key=lambda p: (p[0], -p[2].bottom)):
    edge = ("right" if b.right == bb.right else "") + (" top" if b.top == bb.top else "") + \
           (" bottom" if b.bottom == bb.bottom else "")
    print("  %-9s %s %-30s %s" % (n, kind, b.to_dtype(dbu), edge))
sig = sorted([p for p in pins if p[0] == "M2"], key=lambda p: p[2].bottom)
for a, b in zip(sig, sig[1:]):
    gap = (b[2].bottom - a[2].top) * dbu
    ok &= gap >= 0.6 - 1e-9
print("  signal pins on the right edge: %d, min gap %.2f um" % (
    sum(1 for p in sig if p[2].right == bb.right),
    min((b[2].bottom - a[2].top) * dbu for a, b in zip(sig, sig[1:]))))
ok &= all(p[2].right == bb.right for p in sig) and len(sig) == 7
for kind, n, b in pins:
    if kind == "M1":
        ok &= b.left == bb.left and b.right == bb.right

print("== latch-up (LU_a / LU_b = %.0f um)" % LU)
act, psd, nw = R(1), R(14), R(31)
gat = R(5)
ntie = (act - psd) & nw
ptie = (act & psd) - nw
pdiff = ((act & psd) & nw) - gat
ndiff = ((act - psd) - nw) - gat


def farthest(diff, ties):
    tb = [t.bbox() for t in ties.each()]
    far, where = 0.0, None
    for p in diff.each():
        pts = list(p.each_point_hull())
        samp = []
        for a, b in zip(pts, pts[1:] + pts[:1]):
            n = max(1, int(math.hypot(b.x - a.x, b.y - a.y) / 50))
            samp += [(a.x + (b.x - a.x) * k / n, a.y + (b.y - a.y) * k / n) for k in range(n)]
        for x, y in samp:
            d = min(math.hypot(max(t.left - x, 0, x - t.right), max(t.bottom - y, 0, y - t.top)) for t in tb)
            if d > far:
                far, where = d, (x * dbu, y * dbu)
    return far * dbu, where


for name, diff, ties in [("P+Activ in NWell -> N tie", pdiff, ntie), ("N+Activ -> p+ tie", ndiff, ptie)]:
    far, where = farthest(diff, ties)
    ok &= far <= LU
    print("  %-26s diffusion shapes %3d, ties %d (%s), farthest %.2f um at %s" % (
        name, diff.count(), ties.count(), ", ".join(str(t.bbox().to_dtype(dbu)) for t in ties.each()), far,
        "(%.2f, %.2f)" % where))

print("== area")
nl = db.Layout()
nl.read(NAIVE)
nb = nl.top_cell().dbbox()
a_new = bb.width() * bb.height() * dbu * dbu
print("  naive %s %.2f x %.2f = %.1f um2; assembled %.1f um2 (%.1f %%)" % (
    nl.top_cell().name, nb.width(), nb.height(), nb.width() * nb.height(), a_new,
    100 * (a_new / (nb.width() * nb.height()) - 1)))
halves = 20.985 * 8.43 + 32.21 * 9.73
print("  halves' boxes %.1f um2 (%.1f %% of the cell); rest = channel + fan-out bay beside tree_pmos" % (
    halves, 100 * halves / a_new))
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
