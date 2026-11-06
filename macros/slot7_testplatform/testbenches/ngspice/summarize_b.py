#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Summary tables of results_b/*.csv (run_tb_b.py), markdown on stdout. `--layout` reads results_b_layout/."""
import csv, collections, os, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_b_layout' if '--layout' in sys.argv else 'results_b')
f = float
rows = list(csv.DictReader(open(os.path.join(R, 'ref.csv'))))
print('## Tree bias voltages on analog_bus2 (V), min .. max over corners x temperatures x supplies\n')
print('| reference | vbp | vbn | vbpc | vbnc | tree off, vbp selected |')
print('|---|---|---|---|---|---|')
for ref in ('oa', 'bg', 'ib0'):
    rs = [r for r in rows if r['ref'] == ref]
    cells = [f"{min(f(r[m]) for r in rs):.3f} .. {max(f(r[m]) for r in rs):.3f}" for m in ('vbp', 'vbn', 'vbpc', 'vbnc', 'bus2_tree_off')]
    print(f"| {ref} | " + ' | '.join(cells) + ' |')
print('\n| corner | T | supply | vbn with OA / BG / ibias0 (V) | vbp with OA / BG / ibias0 (V) |')
print('|---|---|---|---|---|')
g = collections.OrderedDict()
for r in rows:
    g.setdefault((r['corner'], r['temp'], r['supply']), {})[r['ref']] = r
for (c, t, s), d in g.items():
    if s != 'nom':
        continue
    print(f"| {c} | {t} | {s} | {' / '.join('%.3f' % f(d[x]['vbn']) for x in ('oa','bg','ib0'))} | {' / '.join('%.3f' % f(d[x]['vbp']) for x in ('oa','bg','ib0'))} |")
ib = list(csv.DictReader(open(os.path.join(R, 'ib1.csv'))))
print(f"\n## ibias1 -> analog_bus3 (bus at 0.7 V, harness source 5 uA)\n\non: {min(f(r['i_bus3_on']) for r in ib)*1e6:.4f} .. {max(f(r['i_bus3_on']) for r in ib)*1e6:.4f} uA; "
      f"off: max {max(abs(f(r['i_bus3_off'])) for r in ib):.3g} A")
p = os.path.join(R, 'failsafe.csv')
if os.path.exists(p):
    fs = list(csv.DictReader(open(p)))
    print('\n## Fail-safe (every dig_in = 1)\n')
    print('| case | max V(bus2) into 1 Gohm | max |I(bus0)| | max |I(bus1)| | max |I(bus3)| |')
    print('|---|---|---|---|---|')
    for case in ('vdd1v2_off', 'vdd1v2_off_1uA', 'enable_low'):
        rs = [r for r in fs if r['case'] == case]
        print(f"| {case} | {max(abs(f(r['v_bus2'])) for r in rs)*1e3:.1f} mV | {max(abs(f(r['i_bus0'])) for r in rs):.3g} A | "
              f"{max(abs(f(r['i_bus1'])) for r in rs):.3g} A | {max(abs(f(r['i_bus3'])) for r in rs):.3g} A |")
