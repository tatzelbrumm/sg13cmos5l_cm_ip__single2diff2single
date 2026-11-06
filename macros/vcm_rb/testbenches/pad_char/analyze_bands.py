# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Bands from the DC sweeps of run_pad_char.py: per PVT point, the range of the swept reference over which INL <= limit
(linear interpolation between sweep points; an edge that the sweep does not reach is reported as the sweep end with
'<' / '>'), its centre, and per iovdd the band common to all corners and temperatures.

usage: python3 -I analyze_bands.py <experiment> <swept column> <limit in V> [group-by columns ...]
"""
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

RES = Path(__file__).resolve().parent / "results"


def load(name):
    rows = [l for l in open(RES / f"{name}.tsv") if not l.startswith("#")]
    rd = csv.DictReader(rows, delimiter="\t")
    return list(rd)


def band(points, lim):
    """points: sorted [(x, inl)]. Returns (lo, hi, lo_open, hi_open) around the best point, or None."""
    pts = [(x, y) for x, y in points if not math.isnan(y)]
    if not pts:
        return None
    i0 = min(range(len(pts)), key=lambda i: pts[i][1])
    if pts[i0][1] > lim:
        return None
    lo, lo_open = pts[0][0], True
    for i in range(i0, 0, -1):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        if y0 > lim:
            lo, lo_open = x0 + (x1 - x0) * (y0 - lim) / (y0 - y1), False
            break
    hi, hi_open = pts[-1][0], True
    for i in range(i0, len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        if y1 > lim:
            hi, hi_open = x0 + (x1 - x0) * (lim - y0) / (y1 - y0), False
            break
    return lo, hi, lo_open, hi_open


def main():
    name, xcol, lim = sys.argv[1], sys.argv[2], float(sys.argv[3])
    group = sys.argv[4:] or ["vdd", "corner_mos", "temp"]
    rows = load(name)
    by = defaultdict(list)
    for r in rows:
        inl = r.get("INL")
        by[tuple(r[g] for g in group)].append((float(r[xcol]), float(inl) if inl not in (None, "", "nan") else math.nan))
    print(f"# {name}: band of {xcol} where INL <= {lim * 1e3:g} mV; '<' / '>' = edge beyond the sweep")
    print("\t".join(group + ["lo", "hi", "centre", "width"]))
    common = defaultdict(lambda: [-1e9, 1e9, False, False])
    for k in sorted(by, key=lambda k: [float(v) if v.replace('.', '').replace('-', '').isdigit() else v for v in k]):
        if any(math.isnan(y) for x, y in by[k]):
            print("\t".join(list(k) + ["lost-points", "", "", ""]))
            continue
        b = band(sorted(by[k]), lim)
        if b is None:
            print("\t".join(list(k) + ["none", "none", "", ""]))
            continue
        lo, hi, lo_o, hi_o = b
        print("\t".join(list(k) + [("<" if lo_o else "") + f"{lo:.3f}", (">" if hi_o else "") + f"{hi:.3f}",
                                   f"{(lo + hi) / 2:.3f}", f"{hi - lo:.3f}"]))
        c = common[k[0]]
        if lo > c[0]:
            c[0], c[2] = lo, lo_o
        if hi < c[1]:
            c[1], c[3] = hi, hi_o
    print(f"# band common to every other key, per {group[0]}:")
    for v, (lo, hi, lo_o, hi_o) in sorted(common.items()):
        print(f"# {group[0]} {v}: {('<' if lo_o else '')}{lo:.3f} ... {('>' if hi_o else '')}{hi:.3f}  "
              f"(centre {(lo + hi) / 2:.3f}, width {hi - lo:.3f})")


if __name__ == "__main__":
    main()
