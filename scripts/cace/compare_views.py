#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Compare the CACE results of one cell between netlist views (results/<cell>/ against results/<cell>_cores_<view>/), as markdown.

Usage: compare_views.py <cell.yaml> <ref_dir> <view_dir> [<view_dir> ...] [-g <group> ...]
  Per group (default: every group with a CSV in ref_dir) and quantity: the limits, min and max over the group's runs
  in the reference and in each view, the change of min and max in %, and the largest change of a single run in %
  (runs matched by their conditions). A run outside the limits is marked **min** / **max** at its view.
Added 2026-10-30 (cloud session C1): bias_sel_pd with the cores as schematic, magic PEX 2 and magic PEX 3.
"""
import csv, os, sys
import yaml
from spec_table import scale

def load(d, g):
    p = os.path.join(d, g + '.csv')
    if not os.path.exists(p):
        return None
    rows = list(csv.reader(open(p)))
    return rows[0], rows[1:]

def lim(spec, key):
    v = spec.get(key, {}).get('value', 'any')
    return None if v in (None, 'any') else float(v)

def pct(a, b):
    return 100.0 * (b - a) / abs(a) if a else float('nan')

def main(argv):
    groups = []
    if '-g' in argv:
        i = argv.index('-g')
        groups, argv = argv[i + 1:], argv[:i]
    if len(argv) < 3:
        sys.exit(__doc__)
    ycell, ref, views = argv[0], argv[1], argv[2:]
    params = yaml.safe_load(open(ycell))['parameters']
    groups = groups or [g for g in params if os.path.exists(os.path.join(ref, g + '.csv'))]
    names = [os.path.basename(os.path.normpath(v)) for v in views]
    print('| group | quantity | unit | limits | %s |' % ' | '.join(
        ['%s min .. max' % os.path.basename(os.path.normpath(ref))] +
        ['%s min .. max (change %%) | %s largest run change %%' % (n, n) for n in names]))
    print('|---|---|---|---|---|%s' % ('---|---|' * len(views)))
    for g in groups:
        r = load(ref, g)
        if not r:
            continue
        head, data = r
        ncond = min(i for i, h in enumerate(head) if '[' in h)
        others = [load(v, g) for v in views]
        for name, s in params[g]['spec'].items():
            col = [i for i, h in enumerate(head) if h.startswith(name + '[')]
            if not col or not data:
                continue
            c, unit = col[0], s.get('unit', '')
            f = scale(unit)
            lo, hi = lim(s, 'minimum'), lim(s, 'maximum')
            lims = 'any' if lo is None and hi is None else '%s .. %s' % ('-' if lo is None else '%g' % lo, '-' if hi is None else '%g' % hi)
            def mark(xs):
                m = []
                if lo is not None and min(xs) < lo: m.append('**min**')
                if hi is not None and max(xs) > hi: m.append('**max**')
                return (' ' + ' '.join(m)) if m else ''
            xr = {tuple(row[:ncond]): float(row[c]) * f for row in data}
            cells = ['%.4g .. %.4g%s' % (min(xr.values()), max(xr.values()), mark(list(xr.values())))]
            for o in others:
                if not o:
                    cells += ['-', '-']
                    continue
                oh, od = o
                oc = [i for i, h in enumerate(oh) if h.startswith(name + '[')][0]
                xv = {tuple(row[:ncond]): float(row[oc]) * f for row in od}
                common = [k for k in xr if k in xv]
                big = max((abs(pct(xr[k], xv[k])) for k in common if xr[k]), default=float('nan'))
                vals = list(xv.values())
                cells += ['%.4g .. %.4g (%+.2f / %+.2f)%s' % (min(vals), max(vals), pct(min(xr.values()), min(vals)),
                          pct(max(xr.values()), max(vals)), mark(vals)), '%.2f' % big]
            print('| %s | %s | %s | %s | %s |' % (g, name, unit, lims, ' | '.join(cells)))

if __name__ == '__main__':
    main(sys.argv[1:])
