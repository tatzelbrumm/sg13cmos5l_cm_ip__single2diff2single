# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""check.py: process-free geometric checks for generated primitives (layers and LU distance from the adapter),
2026-10-28, Claude. They complement the target PDK's own DRC / LVS, which they do not replace.

    python3 check.py sym  <gds> <cell> <adapter.py>            point symmetry: per-layer XOR with the R180 image
    python3 check.py lu   <gds> <cell> <tap spec> <adapter.py> farthest P diffusion from the given taps
    python3 check.py pins <gds> <cell> <adapter.py>            pin texts and which cell edge they touch

tap spec: ';'-separated rectangles x1,y1,x2,y2 (um, tap diffusion, e.g. a parent's tap_path), or 'L', 'R', 'T',
'B' for a one-contact tap abutting that cell edge (its diffusion starts at the edge).
The LU distance is the Euclidean distance inside the well (here every well is convex: one polygon around the
taps and devices), sampled every 0.05 um over all P diffusion under the well. adapter.py: the process adapter
file (e.g. ../ihp_sg13cmos5l/adapter.py).
"""
import math
import os
import sys
import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generator import load_adapter   # noqa: E402


def load(gds, cell, adapter):
    P = load_adapter(adapter)
    ly = db.Layout()
    ly.read(gds)
    return P, ly, ly.cell(cell)


def reg(ly, c, P, k):
    li = ly.find_layer(*P.layer(k))
    return db.Region(c.begin_shapes_rec(li)).merged() if li is not None else db.Region()


def sym(P, ly, c):
    b = c.bbox()
    img = db.ICplxTrans(1, 180, False, b.left + b.right, b.bottom + b.top)
    out = []
    for k in ("diff", "poly", "contact", "pimp", "well", "hvox", "m1", "via1", "m2"):
        r = reg(ly, c, P, k)
        out.append((k, r.area() * ly.dbu ** 2, (r ^ r.transformed(img)).area() * ly.dbu ** 2))
    return (b.left + b.right) / 2 * ly.dbu, (b.bottom + b.top) / 2 * ly.dbu, out


def taps_from_spec(P, c, ly, spec):
    b = c.dbbox()
    wa = 2 * P.rule("diff_encl_contact") + P.rule("contact_size")
    edge = dict(L=(b.left - wa, b.bottom, b.left, b.top), R=(b.right, b.bottom, b.right + wa, b.top),
                B=(b.left, b.bottom - wa, b.right, b.bottom), T=(b.left, b.top, b.right, b.top + wa))
    out = []
    for s in spec.split(";"):
        s = s.strip()
        out.append(edge[s] if s in edge else tuple(float(v) for v in s.split(",")))
    return out


def lu(P, ly, c, taps, step=0.05):
    """max over P diffusion (in the well) of the distance to the nearest tap rectangle"""
    pd = reg(ly, c, P, "diff") & reg(ly, c, P, "pimp") & reg(ly, c, P, "well")
    worst, at = 0.0, None
    for p in pd.each():
        bb = p.bbox().to_dtype(ly.dbu)
        nx, ny = max(1, int(bb.width() / step)), max(1, int(bb.height() / step))
        for i in range(nx + 1):
            for j in range(ny + 1):
                x, y = bb.left + bb.width() * i / nx, bb.bottom + bb.height() * j / ny
                d = min(math.hypot(max(t[0] - x, 0, x - t[2]), max(t[1] - y, 0, y - t[3])) for t in taps)
                if d > worst:
                    worst, at = d, (round(x, 3), round(y, 3))
    return worst, at


def pins(P, ly, c):
    b = c.bbox()
    out = []
    for m in ("m1", "m2"):
        lt = ly.find_layer(*P.layer(m + "_text"))
        lp = ly.find_layer(*P.layer(m + "_pin"))
        if lt is None:
            continue
        boxes = [s.bbox() for s in c.shapes(lp).each()] if lp is not None else []
        for s in c.shapes(lt).each():
            if not s.is_text():
                continue
            pt = s.text_trans.disp
            bx = [q for q in boxes if q.contains(db.Point(pt.x, pt.y))]
            e = ""
            if bx:
                q = bx[0]
                e = "".join(n for n, v in (("L", q.left == b.left), ("R", q.right == b.right), ("B", q.bottom == b.bottom),
                                           ("T", q.top == b.top)) if v)
            out.append((s.text_string, m, bx[0].to_dtype(ly.dbu) if bx else None, e or "inside"))
    return out


if __name__ == "__main__":
    mode, gds, cell = sys.argv[1:4]
    if mode == "lu":
        spec, ad = sys.argv[4], sys.argv[5]
    else:
        ad = sys.argv[4]
    P, ly, c = load(gds, cell, ad)
    if mode == "sym":
        cx, cy, out = sym(P, ly, c)
        print("%s: R180 about (%.3f, %.3f) um" % (cell, cx, cy))
        for k, a, x in out:
            print("  %-8s area %9.3f um2   XOR with image %8.3f um2" % (k, a, x))
    elif mode == "lu":
        taps = taps_from_spec(P, c, ly, spec)
        d, at = lu(P, ly, c, taps)
        lim = P.rule("lu_tap_dist")
        print("%s taps %s: farthest P diffusion %.2f um at %s; limit %g (%s) -> %s"
              % (cell, spec, d, at, lim, P.RULES["lu_tap_dist"][0], "pass" if d <= lim else "FAIL"))
    else:
        for p in pins(P, ly, c):
            print("  %-10s %s  %s  edge %s" % p)
