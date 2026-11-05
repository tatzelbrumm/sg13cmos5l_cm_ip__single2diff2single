# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Schematic vs post-layout CACE results of the s2d pad (C3, lead, 2026-11-05).

usage: python3 cace_compare.py <results/TOP> <results/TOP_pex> <group> [<group> ...] > compare.md

For each group and result quantity of the CSVs that cace_to_csv.py wrote: the range on the schematic, the range on
the PEX netlist, and the largest change between runs of the same conditions (rows matched by every condition column),
absolute and relative to the schematic value. Rows present on one side only are counted."""
import csv, os, sys

sch, pex, groups = sys.argv[1], sys.argv[2], sys.argv[3:]
print('| group | quantity | schematic | pex | max abs change | max rel change | rows matched |')
print('|---|---|---:|---:|---:|---:|---:|')
for g in groups:
    a = list(csv.DictReader(open(os.path.join(sch, g + '.csv'))))
    b = list(csv.DictReader(open(os.path.join(pex, g + '.csv'))))
    cols = list(a[0].keys())
    res = [c for c in cols if '[' in c]          # results carry a unit in brackets; conditions do not
    cond = [c for c in cols if c not in res]
    key = lambda r: tuple(r[c] for c in cond)
    bb = {key(r): r for r in b}
    pairs = [(r, bb[key(r)]) for r in a if key(r) in bb]
    for q in res:
        def num(rows):
            out = []
            for r in rows:
                try:
                    out.append(float(r[q]))
                except (ValueError, TypeError):
                    pass
            return out
        va, vb = num(a), num(b)
        if not va or not vb:
            continue
        d, rel = 0.0, 0.0
        for ra, rb in pairs:
            try:
                x, y = float(ra[q]), float(rb[q])
            except (ValueError, TypeError):
                continue
            d = max(d, abs(y - x))
            if x != 0:
                rel = max(rel, abs(y - x) / abs(x))
        print(f'| {g} | {q} | {min(va):.4g} .. {max(va):.4g} | {min(vb):.4g} .. {max(vb):.4g} | {d:.3g} | '
              f'{100 * rel:.2f} % | {len(pairs)} of {len(a)} / {len(b)} |')
