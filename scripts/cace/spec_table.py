#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Print the specification table (limit, worst case, verdict per quantity) of one cell as markdown,
from its CACE yaml and the CSV files that `make sim-cace` leaves in verification/cace/results/<cell>/.
Usage: spec_table.py <cell.yaml> <results_dir> [group ...]   (default: every group with a CSV)
Generalized 2026-10-20 from chipalooza2/levelshifters/ls_pair/scripts/spec_table.py (two fixed cells, pvt_params only)."""
import csv, os, sys, yaml
PFX = {'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'f': 1e-15, 'm': 1e-3, 'k': 1e3, 'M': 1e6, 'G': 1e9}
SI = ('V', 'A', 's', 'C', 'Hz', 'dB', '°', 'Ω', 'F', 'J', 'rtHz', '')

def scale(unit):            # SI value -> display unit ('V/us' = scale('V') / scale('us'), '%' = 100)
    if '/' in unit:
        num, den = unit.split('/', 1)
        return scale(num) / scale(den)
    if unit == '%': return 100.0
    if unit in SI or len(unit) < 2 or unit[0] not in PFX: return 1.0
    return 1.0 / PFX[unit[0]]

def table(ycell, resdir, groups):
    params = yaml.safe_load(open(ycell))['parameters']
    groups = groups or [g for g in params if os.path.exists(os.path.join(resdir, g + '.csv'))]
    print('| group | quantity | unit | limit | worst | runs | verdict |\n|---|---|---|---:|---:|---:|---|')
    for g in groups:
        rows = list(csv.reader(open(os.path.join(resdir, g + '.csv'))))
        head, data = rows[0], rows[1:]
        for name, s in params[g]['spec'].items():
            col = [i for i, h in enumerate(head) if h.startswith(name + '[')]
            if not col or not data: continue
            unit = s.get('unit', '')
            v = [float(r[col[0]]) * scale(unit) for r in data if r[col[0]] not in ('', 'nan')]
            if not v: continue
            lo = s.get('minimum', {}).get('value', 'any'); hi = s.get('maximum', {}).get('value', 'any')
            cells = []
            if lo != 'any': cells.append(('>=', lo, min(v), min(v) >= float(lo)))
            if hi != 'any': cells.append(('<=', hi, max(v), max(v) <= float(hi)))
            if not cells: cells.append(('', 'any', '%.4g .. %.4g' % (min(v), max(v)), None))
            for op, lim, worst, ok in cells:
                w = worst if isinstance(worst, str) else '%.4g' % worst
                print('| %s | %s | %s | %s %s | %s | %d | %s |' % (g, s.get('display', name), unit, op, lim, w, len(v),
                      'pass' if ok else ('FAIL' if ok is False else 'report')))

if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    table(sys.argv[1], sys.argv[2], sys.argv[3:])
