#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Print the statistics of Monte Carlo groups (CSV files of `make sim-cace`) against the limits of another group, as markdown.

Usage: mc_stats.py <cell.yaml> <results_dir> <mc_group>=<limit_group> ... [--nolimit <cond>=<value>] ...
  Per mc_group, per combination of its enumerated conditions other than `iterations` (e.g. sel x vdd), and per
  quantity with a unit: runs, mean, sigma (sample), min, max, and the limits of <limit_group> for that quantity, with
  two verdicts: min / max inside the limits, and mean -/+ 3 sigma inside the limits.
  --nolimit sel=3 shows the rows with sel = 3 without limits (sel 3 runs both cores, about twice every current).
Added 2026-10-30 (cloud session C1) for the mismatch groups of bias_sel_pd (make mc-table).
"""
import csv, os, statistics, sys
import yaml
from spec_table import scale

def lim(spec, key):
    v = spec.get(key, {}).get('value', 'any')
    return None if v in (None, 'any') else float(v)

def fmt(x):
    return '%.4g' % x

def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    ycell, resdir, rest = argv[0], argv[1], argv[2:]
    nolimit, pairs = [], []
    i = 0
    while i < len(rest):
        if rest[i] == '--nolimit':
            nolimit.append(tuple(rest[i + 1].split('=', 1)))
            i += 2
        else:
            pairs.append(tuple(rest[i].split('=', 1)))
            i += 1
    params = yaml.safe_load(open(ycell))['parameters']
    for mc, lg in pairs:
        path = os.path.join(resdir, mc + '.csv')
        if not os.path.exists(path):
            print('%s: no %s\n' % (mc, path))
            continue
        rows = list(csv.DictReader(open(path)))
        conds = params[mc]['conditions']
        keys = [c for c, v in conds.items() if c != 'iterations' and 'enumerate' in v]
        fixed = ', '.join('%s %s' % (c, v.get('typical')) for c, v in conds.items() if 'typical' in v)
        print('### %s (%s), limits of %s\n' % (mc, fixed, lg))
        print('| %s | quantity | unit | runs | mean | sigma | min | max | limits | min / max | mean -/+ 3 sigma |' % ' | '.join(keys))
        print('|%s---|---|---:|---:|---:|---:|---:|---|---|---|' % ('---|' * len(keys)))
        combos = []
        for r in rows:
            k = tuple(r[c] for c in keys)
            if k not in combos:
                combos.append(k)
        for k in combos:
            sub = [r for r in rows if tuple(r[c] for c in keys) == k]
            free = any(dict(zip(keys, k)).get(c) == v for c, v in nolimit)
            for name, s in params[mc]['spec'].items():
                unit = s.get('unit', '')
                col = [h for h in sub[0] if h.startswith(name + '[')]
                if not col:
                    continue
                f = scale(unit)
                x = [float(r[col[0]]) * f for r in sub]
                m, sd = statistics.fmean(x), (statistics.stdev(x) if len(x) > 1 else 0.0)
                ls = params[lg]['spec'].get(name, {})
                lo, hi = (None, None) if free else (lim(ls, 'minimum'), lim(ls, 'maximum'))
                if lo is None and hi is None:
                    lims, v1, v3 = ('none (%s)' % ', '.join('%s=%s' % c for c in nolimit) if free else 'any'), '', ''
                else:
                    lims = '%s .. %s' % ('-' if lo is None else fmt(lo), '-' if hi is None else fmt(hi))
                    ok1 = (lo is None or min(x) >= lo) and (hi is None or max(x) <= hi)
                    ok3 = (lo is None or m - 3 * sd >= lo) and (hi is None or m + 3 * sd <= hi)
                    v1, v3 = ('pass' if ok1 else '**FAIL**'), ('pass' if ok3 else '**FAIL**')
                print('| %s | %s | %s | %d | %s | %s | %s | %s | %s | %s | %s |' % (
                    ' | '.join(k), name, unit, len(x), fmt(m), fmt(sd), fmt(min(x)), fmt(max(x)), lims, v1, v3))
        print()

if __name__ == '__main__':
    main(sys.argv[1:])
