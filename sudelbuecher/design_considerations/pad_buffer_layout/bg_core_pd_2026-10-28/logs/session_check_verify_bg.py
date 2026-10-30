"""Independent flat extraction (session's own check, not the agents' tools): HV MOS, rhigh (PolyRes 128/0 body, squares),
pnp emitters (P+ Activ in NWell outside ThickGateOx and GatPoly) with their emitter and base nets. usage: verify_bg.py <gds>"""
import klayout.db as db, sys, collections
ly = db.Layout(); ly.read(sys.argv[1]); top = ly.top_cell(); top.flatten(-1, True); dbu = ly.dbu
li = lambda l, d: ly.find_layer(l, d) if ly.find_layer(l, d) is not None else ly.layer(l, d)
l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, top, []))
mk = lambda l, d: l2n.make_layer(li(l, d), "L%d_%d" % (l, d))
A, Pl, PS, NW, C, M1, V1, M2, TGO, PR = mk(1, 0), mk(5, 0), mk(14, 0), mk(31, 0), mk(6, 0), mk(8, 0), mk(19, 0), mk(10, 0), mk(44, 0), mk(128, 0)
pc = Pl - PR                                          # conducting poly (heads, gates)
gate = A & pc
ng = (gate - PS) - NW; pg = (gate & PS) & NW
nsd = (A - PS) - pc; psd_ = (A & PS) - pc
emit = (psd_ & NW) - TGO                              # pnp emitters (PMOS S/D are under ThickGateOx)
psd_mos = psd_ - emit
ntie = nsd & NW; nsd_mos = nsd - NW
for r, n in ((ng, "ng"), (pg, "pg"), (nsd_mos, "nsd"), (psd_mos, "psd"), (emit, "emit"), (ntie, "ntie"), (pc, "pc")): l2n.register(r, n)
l2n.extract_devices(db.DeviceExtractorMOS3Transistor("NMOS"), {"SD": nsd_mos, "G": ng, "P": pc})
l2n.extract_devices(db.DeviceExtractorMOS3Transistor("PMOS"), {"SD": psd_mos, "G": pg, "P": pc})
l2n.extract_devices(db.DeviceExtractorResistor("RES", 1.0), {"R": PR, "C": pc})
for a in (nsd_mos, psd_mos, emit, ntie, pc, M1, M2, NW): l2n.connect(a)
for a in (nsd_mos, psd_mos, emit, ntie, pc): l2n.connect(a, C)
l2n.connect(ntie, NW); l2n.connect(C, M1); l2n.connect(M1, V1); l2n.connect(V1, M2)
for (l, d), m in [((8, 25), M1), ((10, 25), M2)]:
    t = l2n.make_text_layer(li(l, d), "T%d_%d" % (l, d)); l2n.connect(m, t)
l2n.extract_netlist(); nl = l2n.netlist(); nl.combine_devices()
c = nl.circuit_by_name(top.name); nm = lambda n: (n.name if n and n.name else "#")
agg = collections.defaultdict(float); cnt = collections.Counter()
for d in c.each_device():
    cl = d.device_class().name
    if cl == "RES":
        print("  RES  %-6s - %-6s  %.2f squares" % (nm(d.net_for_terminal('A')), nm(d.net_for_terminal('B')), d.parameter('R'))); continue
    sd = tuple(sorted((nm(d.net_for_terminal('S')), nm(d.net_for_terminal('D')))))
    k = (cl, round(d.parameter('L'), 2), nm(d.net_for_terminal('G')), sd); agg[k] += d.parameter('W'); cnt[k] += 1
for k in sorted(agg): print('  %s L=%.2f G=%-8s S/D=%-20s W=%8.2f  (%d)' % (k[0], k[1], k[2], '/'.join(k[3]), agg[k], cnt[k]))
# pnp emitters: net of each emitter polygon, and of the NWell (base) it sits in
er = db.Region(top.shapes(li(1, 0))) & db.Region(top.shapes(li(14, 0))) & db.Region(top.shapes(li(31, 0))) - db.Region(top.shapes(li(44, 0))) - db.Region(top.shapes(li(5, 0)))
ec = collections.Counter()
for p in er.merged().each():
    pt = p.bbox().center()
    en = l2n.probe_net(emit, db.DPoint(pt.x * dbu, pt.y * dbu)); bn = l2n.probe_net(NW, db.DPoint(pt.x * dbu, pt.y * dbu))
    ec[(nm(en), nm(bn), round(p.area() * dbu * dbu, 2))] += 1
for k, v in sorted(ec.items()): print('  pnp emitter net=%-6s base(NWell) net=%-6s area %.2f um2  x%d' % (k[0], k[1], k[2], v))
print('named nets:', sorted(n.name for n in c.each_net() if n.name))
print('nets with more than one label name:', [n.name for n in c.each_net() if n.name and ',' in n.name])
