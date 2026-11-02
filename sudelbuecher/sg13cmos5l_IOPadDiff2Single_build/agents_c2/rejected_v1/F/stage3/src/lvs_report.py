# summarise an IHP run_lvs.py lvsdb: unmatched / mismatched nets, devices, pins per circuit. python3 lvs_report.py <lvsdb> [max]
import sys
import klayout.db as db
l = db.LayoutVsSchematic()
l.read(sys.argv[1])
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 40
xref = l.xref()
for cp in xref.each_circuit_pair():
    a, b = cp.first(), cp.second()
    st = cp.status()
    print("circuit", a.name if a else None, b.name if b else None, st)
    if st == db.NetlistCrossReference.Match:
        continue
    k = 0
    for np in xref.each_net_pair(cp):
        if np.status() != db.NetlistCrossReference.Match:
            print("  net", np.first().expanded_name() if np.first() else None, "<->",
                  np.second().expanded_name() if np.second() else None, np.status())
            k += 1
            if k > mx: break
    k = 0
    for dp in xref.each_device_pair(cp):
        if dp.status() != db.NetlistCrossReference.Match:
            d1, d2 = dp.first(), dp.second()
            f = lambda d: (d.expanded_name(), d.device_class().name, [(t.name, d.net_for_terminal(t.id()).expanded_name() if d.net_for_terminal(t.id()) else None) for t in d.device_class().terminal_definitions()], ["%s=%g" % (p.name, d.parameter(p.id())) for p in d.device_class().parameter_definitions() if p.name in ("W", "L")]) if d else None
            print("  dev", f(d1), "<->", f(d2), dp.status())
            k += 1
            if k > mx: break
