# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Metal connectivity probe of the pad candidate (flat): Activ minus GatPoly, Cont, Metal1 .. Metal4 with vias.
Each probe names the net it should be on; probes of one expected net must share a net, different ones must not.
    python3 probe_nets.py <gds> <cell> <probe file: lines 'expected layer x y comment'>"""
import sys

import klayout.db as db

gds, cell, pf = sys.argv[1:4]
ly = db.Layout()
ly.read(gds)
c = ly.cell(cell)
l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, c, []))
L = {}
for n, (a, b) in {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "M1": (8, 0), "Via1": (19, 0), "M2": (10, 0),
                  "Via2": (29, 0), "M3": (30, 0), "Via3": (49, 0), "M4": (50, 0)}.items():
    L[n] = l2n.make_layer(ly.layer(a, b), n)
diff = l2n.make_layer("diff")
diff.insert(L["Activ"] - L["GatPoly"])
chain = [diff, L["Cont"], L["M1"], L["Via1"], L["M2"], L["Via2"], L["M3"], L["Via3"], L["M4"]]
for a, b in zip(chain, chain[1:]):
    l2n.connect(a, b)
for x in chain:
    l2n.connect(x)
l2n.connect(L["GatPoly"])
l2n.connect(L["GatPoly"], L["Cont"])
l2n.extract_netlist()
groups, ok = {}, True
for ln in open(pf):
    ln = ln.split("#")[0].split()
    if not ln:
        continue
    exp, lay, x, y = ln[0], ln[1], float(ln[2]), float(ln[3])
    net = l2n.probe_net(L[lay] if lay in L else diff, db.DPoint(x, y))
    nid = net.cluster_id if net else None
    groups.setdefault(exp, set()).add(nid)
    print("%-8s %-4s (%7.3f, %7.3f) -> %s" % (exp, lay, x, y, nid))
for e, s in groups.items():
    if None in s or len(s) != 1:
        ok = False
        print("FAIL: %s probes on %s" % (e, s))
ids = [next(iter(s)) for s in groups.values() if len(s) == 1]
if len(ids) != len(set(ids)):
    ok = False
    print("FAIL: two expected nets share one net (short)")
print("PROBES:", "PASS" if ok else "FAIL", "(%d nets, %d probes)" % (len(groups), sum(len(s) for s in groups.values())))
