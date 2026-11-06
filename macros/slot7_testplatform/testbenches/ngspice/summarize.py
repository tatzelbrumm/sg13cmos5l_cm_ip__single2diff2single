#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Summaries of results/*.csv written by run_tb.py (prints markdown tables)."""
import csv, collections, os, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_layout' if '--layout' in sys.argv else 'results')
f = lambda v: float(v) if v not in ('', None) else float('nan')

def static():
    rows = list(csv.DictReader(open(os.path.join(R, 'static.csv'))))
    by = collections.OrderedDict()
    for r in rows:
        by.setdefault(r['state'], []).append(r)
    print('| state | I(bus0) min .. max | I(bus1) min .. max | en_oa / en_bg / read-back as expected | worst point |')
    print('|---|---|---|---|---|')
    bad_total = 0
    for st, rs in by.items():
        i0 = [f(r['i(vbus0)']) for r in rs]; i1 = [f(r['i(vbus1)']) for r in rs]
        d = rs[0]['dig_in']; en = rs[0]['enable'] == '1'
        on1 = rs[0]['vdd_1v2_on'] == '1'; on3 = rs[0]['vdd_3v3_on'] == '1'
        bad = []
        for r in rs:
            v3, v1 = f(r['v3']), f(r['v1'])
            if not on3:
                continue                       # 3.3 V logic unpowered: levels meaningless
            for c, k in ((0, 'oa'), (1, 'bg'), (2, 'tg0'), (3, 'tg1')):
                want = en and on1 and d[c] == '1'
                e, eb = f(r[f'v(x1.en_{k})']), f(r[f'v(x1.en_{k}_b)'])
                if e != e:                      # layout netlist: no internal nodes, judge by the read-back only
                    ok = True
                else:
                    ok = (e > 0.9 * v3 and eb < 0.1 * v3) if want else (e < 0.1 * v3 and eb > 0.9 * v3)
                if on1:
                    rb = f(r[f'v(dout{c})'])
                    ok = ok and ((rb > 0.9 * v1) if want else (rb < 0.1 * v1))
                if not ok:
                    bad.append(f"{r['corner']}/{r['temp']}/{r['supply']}/{k}")
        bad_total += len(bad)
        worst = max(rs, key=lambda r: abs(f(r['i(vbus0)'])) + abs(f(r['i(vbus1)'])))
        print(f"| {st} (dig_in {d}, en {int(en)}, 3v3 {int(on3)}, 1v2 {int(on1)}) | {min(i0):.3g} .. {max(i0):.3g} A | "
              f"{min(i1):.3g} .. {max(i1):.3g} A | {'yes' if not bad else 'NO: ' + ', '.join(bad[:6])} | "
              f"{worst['corner']} {worst['temp']} C {worst['supply']} |")
    # tie-lows and supply currents
    lo = max(f(r['v(dout4)']) for r in rows if r['vdd_1v2_on'] == '1')
    lo11 = max(f(r['v(dout11)']) for r in rows if r['vdd_1v2_on'] == '1')
    print(f'\ntie-lows dig_out[4] / dig_out[11], vdd_1v2 on: max {lo:.3g} / {lo11:.3g} V (into 1 Tohm)')
    for st in ('all_off', 'both_on'):
        rs = by[st]
        print(f"supply currents, {st}: I(vdd_3v3) {min(-f(r['i(v3)']) for r in rs):.3g} .. {max(-f(r['i(v3)']) for r in rs):.3g} A, "
              f"I(vdd_1v2) {min(-f(r['i(v1)']) for r in rs):.3g} .. {max(-f(r['i(v1)']) for r in rs):.3g} A")
    for st in ('vdd1v2_off',):
        print(f"floating vdd_1v2 when gated off: {min(f(r['v(vdd_1v2)']) for r in by[st]):.3g} .. {max(f(r['v(vdd_1v2)']) for r in by[st]):.3g} V")
    for st in ('vdd3v3_off', 'both_supplies_off'):
        print(f"floating vdd_3v3, {st}: {min(f(r['v(vdd_3v3)']) for r in by[st]):.3g} .. {max(f(r['v(vdd_3v3)']) for r in by[st]):.3g} V")
    # on-current table per corner/temp (nominal supply)
    print('\n| corner | T (C) | I_OA (uA) low / nom / high supply | I_BG (uA) low / nom / high |')
    print('|---|---|---|---|')
    tab = collections.OrderedDict()
    for r in by['both_on']:
        tab.setdefault((r['corner'], r['temp']), {})[r['supply']] = (f(r['i(vbus0)']) * 1e6, f(r['i(vbus1)']) * 1e6)
    for (c, t), d in tab.items():
        g = lambda s, i: ('%.3f' % d[s][i]) if s in d else '-'
        print(f"| {c} | {t} | {g('low', 0)} / {g('nom', 0)} / {g('high', 0)} | {g('low', 1)} / {g('nom', 1)} / {g('high', 1)} |")
    print(f'\nlogic-level failures: {bad_total}')

def sweep():
    rows = list(csv.DictReader(open(os.path.join(R, 'sweep.csv'))))
    print('| corner | T | I_OA at 0 / 0.7 / 1.5 / 2.0 / 2.5 V (uA) | I_BG at 0 / 0.7 / 1.5 / 2.0 / 2.5 V (uA) |')
    print('|---|---|---|---|')
    g = collections.OrderedDict()
    for r in rows:
        g.setdefault((r['corner'], r['temp']), {})[round(f(r['v_bus']), 2)] = (f(r['i_oa']) * 1e6, f(r['i_bg']) * 1e6)
    for (c, t), d in g.items():
        pts = [0.0, 0.7, 1.5, 2.0, 2.5]
        print(f"| {c} | {t} | {' / '.join('%.3f' % d[p][0] for p in pts)} | {' / '.join('%.3f' % d[p][1] for p in pts)} |")

def tran():
    rows = list(csv.DictReader(open(os.path.join(R, 'tran.csv'))))
    print('| corner | T | I_OA on (uA) | t_on OA (us) | t_off OA | I_BG on (uA) | t_on BG (us) | t_off BG | I after off (OA / BG) |')
    print('|---|---|---|---|---|---|---|---|---|')
    for r in rows:
        print(f"| {r['corner']} | {r['temp']} | {f(r['i0_on'])*1e6:.3f} | {(f(r['t0_on'])-1e-6)*1e6:.2f} | {(f(r['t0_off'])-101e-6)*1e9:.0f} ns | "
              f"{f(r['i1_on'])*1e6:.3f} | {(f(r['t1_on'])-1e-6)*1e6:.2f} | {(f(r['t1_off'])-101e-6)*1e9:.0f} ns | {f(r['i0_off']):.2g} / {f(r['i1_off']):.2g} A |")

def leak():
    rows = list(csv.DictReader(open(os.path.join(R, 'leak.csv'))))
    print('| corner | T | I(bus0) at 0 / 0.7 / 1.65 / 2.5 / 3.3 V | I(bus1) same |')
    print('|---|---|---|---|')
    g = collections.OrderedDict()
    for r in rows:
        g.setdefault((r['corner'], r['temp']), []).append((f(r['i_bus0']), f(r['i_bus1'])))
    for (c, t), v in g.items():
        print(f"| {c} | {t} | {' / '.join('%.2g' % a for a, b in v)} | {' / '.join('%.2g' % b for a, b in v)} |")

for w in ([a for a in sys.argv[1:] if not a.startswith('--')] or ['static', 'sweep', 'tran', 'leak']):
    if os.path.exists(os.path.join(R, w + '.csv')):
        print(f'\n## {w}\n'); globals()[w]()
