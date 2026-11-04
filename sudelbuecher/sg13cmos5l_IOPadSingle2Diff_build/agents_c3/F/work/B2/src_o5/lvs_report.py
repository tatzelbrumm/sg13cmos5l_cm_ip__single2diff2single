# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Summary of a KLayout .lvsdb: per circuit pair the match status, and the nets / devices / pins that do not match.
    python3 lvs_report.py <file.lvsdb> [max lines per circuit]"""
import sys

import klayout.db as db

lvs = db.LayoutVsSchematic()
lvs.read(sys.argv[1])
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 30
xr = lvs.xref()
ST = {db.NetlistCrossReference.Match: 'match', db.NetlistCrossReference.NoMatch: 'NOMATCH',
      db.NetlistCrossReference.Skipped: 'skipped', db.NetlistCrossReference.MatchWithWarning: 'match(warn)',
      db.NetlistCrossReference.Mismatch: 'MISMATCH', db.NetlistCrossReference.None_: '-'}
for cp in xr.each_circuit_pair():
    a, b = cp.first(), cp.second()
    st = ST.get(cp.status(), str(cp.status()))
    print('circuit %s <-> %s: %s' % (a.name if a else None, b.name if b else None, st))
    if st in ('match', 'skipped'):
        continue
    n = 0
    for np_ in xr.each_net_pair(cp):
        s = ST.get(np_.status(), str(np_.status()))
        if s not in ('match',):
            la, sb = np_.first(), np_.second()
            print('   net %-9s L %-30s S %s' % (s, la.expanded_name() if la else None, sb.expanded_name() if sb else None))
            n += 1
            if n > mx:
                break
    n = 0
    for dp in xr.each_device_pair(cp):
        s = ST.get(dp.status(), str(dp.status()))
        if s != 'match':
            la, sb = dp.first(), dp.second()
            print('   dev %-9s L %s S %s' % (s, la.expanded_name() if la else None, sb.expanded_name() if sb else None))
            n += 1
            if n > mx:
                break
    for pp in xr.each_pin_pair(cp):
        s = ST.get(pp.status(), str(pp.status()))
        if s != 'match':
            la, sb = pp.first(), pp.second()
            print('   pin %-9s L %s S %s' % (s, la.expanded_name() if la else None, sb.expanded_name() if sb else None))
    for sp in xr.each_subcircuit_pair(cp):
        s = ST.get(sp.status(), str(sp.status()))
        if s != 'match':
            la, sb = sp.first(), sp.second()
            print('   sub %-9s L %s S %s' % (s, la.expanded_name() if la else None, sb.expanded_name() if sb else None))
