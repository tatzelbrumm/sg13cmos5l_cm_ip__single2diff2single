# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""metal-only connectivity probe: python3 probe.py <gds> <cell> x,y[:layer] ... -> which probes share a net"""
import sys
import klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1]); c = ly.cell(sys.argv[2])
l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, c, []))
L = {}
for n, (l, d) in {"M1": (8, 0), "V1": (19, 0), "M2": (10, 0), "V2": (29, 0), "M3": (30, 0), "V3": (49, 0),
                  "M4": (50, 0), "TV1": (125, 0), "TM1": (126, 0)}.items():
    L[n] = l2n.make_layer(ly.layer(l, d), n)
for a in ("M1", "M2", "M3", "M4", "TM1"):
    l2n.connect(L[a])
for a, v, b in (("M1", "V1", "M2"), ("M2", "V2", "M3"), ("M3", "V3", "M4"), ("M4", "TV1", "TM1")):
    l2n.connect(L[a], L[v]); l2n.connect(L[v], L[b])
l2n.extract_netlist()
nets = []
for arg in sys.argv[3:]:
    p, lay = (arg.split(":") + ["M2"])[:2]
    x, y = (float(v) for v in p.split(","))
    n = l2n.probe_net(L[lay], db.DPoint(x, y))
    nets.append((arg, n.cluster_id if n else None))
    print(arg, n.cluster_id if n else None, n.expanded_name() if n else "")
