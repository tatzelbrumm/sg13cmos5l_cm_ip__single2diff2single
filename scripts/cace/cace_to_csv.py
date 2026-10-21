#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Collect the per-run results of one CACE parameter group into a CSV file.

Usage: cace_to_csv.py <cell.yaml> <group> <run_dir> <out.csv>
  <run_dir> is verification/cace/_runs/RUN_<date>/ ; every parameters/<group>/run_*/ holds conditions.yaml and
  a <testbench>_<N>.data file whose columns follow `variables:` of the group in the cell yaml.
CSV columns: the conditions of the group, then the variables (SI units: s, V, A, C, J).
"""
import csv, glob, os, re, sys
import yaml

def main(ycell, group, rundir, out):
    d = yaml.safe_load(open(ycell))
    g = d['parameters'][group]
    variables = g['tool']['ngspice']['variables']
    conds = [c for c in g['conditions']]
    # the testbench writes SI values; the yaml units are display units, so label the columns with the SI unit
    si = {'ns': 's', 'ps': 's', 'pA': 'A', 'nA': 'A', 'uA': 'A', 'fC': 'C', 'pC': 'C', 'fW\u22c5s': 'J', 'pW\u22c5s': 'J'}
    units = {k: si.get(v.get('unit', ''), v.get('unit', '')) for k, v in g['spec'].items()}
    runs = sorted(glob.glob(os.path.join(rundir, 'parameters', group, 'run_*')), key=lambda p: int(re.search(r'run_(\d+)', p).group(1)))
    rows = []
    for r in runs:
        files = glob.glob(os.path.join(r, '*.data'))
        if not files: continue
        c = yaml.safe_load(open(os.path.join(r, 'conditions.yaml')))
        vals = open(files[0]).read().split()
        if len(vals) != len(variables): continue
        row = {k: c.get(k) for k in conds}
        row.update({v: x for v, x in zip(variables, vals)})
        rows.append(row)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(conds + ['%s[%s]' % (v, units.get(v, '')) for v in variables])
        for row in rows: w.writerow([row[k] for k in conds + variables])
    print('%s: %d of %d runs -> %s' % (group, len(rows), len(runs), out))

if __name__ == '__main__':
    if len(sys.argv) != 5: sys.exit(__doc__)
    main(*sys.argv[1:])
