# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B: place and route s2d_block with generator.py (C2's router, copied unchanged).
    python3 route_block.py <block_cfg.py> <out.gds>"""
import os
import sys
import time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generator as G  # noqa: E402
t0 = time.time()
cfg = G.load_config(sys.argv[1])
# rip-up by reordering: nets that fail go to the front of the order and everything is routed again (at most 8
# rounds); the order that routes everything is printed (to be written back into block_cfg.py's ROUTE_ORDER)
order = list(cfg.get("ROUTE_ORDER") or [])
for rnd in range(8):
    cfg["ROUTE_ORDER"] = order
    blk, rep = G.build(cfg, sys.argv[2], log=(print if rnd == 0 else (lambda *a: None)))
    bad = [n for n, _ in rep["failed"] or []]
    print("round %d: failed %s" % (rnd, bad))
    if not bad:
        break
    order = bad + [n for n in order if n not in bad]
print("ROUTE_ORDER used:", order)
blk, rep = blk, rep
G.build.__doc__  # noqa: B018
print("failed:", rep["failed"], "time %.0f s" % (time.time() - t0))
# diagnostics of failed nets: the terminal groups (instance.pin, access nodes) and a flood fill of each group's free
# region on its own net's mask (how far it can get)
import numpy as np  # noqa: E402
gr = blk.router
names = [None] + blk.nets
for net, why in rep["failed"] or []:
    k = names.index(net)
    f = gr.free(k)
    groups = {}
    for p in blk.pins:
        if p["net"] == net:
            groups.setdefault(p["group"], []).append(p)
    for gid, ps in groups.items():
        nodes = set()
        for p in ps:
            for m, reg in p["terms"].items():
                nodes |= gr.terminal_nodes(m, reg, k) | gr.via_access_nodes(m, reg, k)
        # flood fill over free nodes of both layers (vias allowed where not blocked)
        seen, stack = set(nodes), list(nodes)
        while stack and len(seen) < 4000:
            n = stack.pop()
            L, rem = divmod(n, gr.NX * gr.NY)
            i, j = divmod(rem, gr.NY)
            for L2, i2, j2 in ((L, i + 1, j), (L, i - 1, j), (L, i, j + 1), (L, i, j - 1), (1 - L, i, j)):
                if 0 <= i2 < gr.NX and 0 <= j2 < gr.NY and f[L2, i2, j2]:
                    m2 = gr.nid(L2, i2, j2)
                    if m2 not in seen:
                        seen.add(m2)
                        stack.append(m2)
        print("  %s group %s: %s, %d access nodes, reach %s" % (net, gid, sorted({"%s.%s" % (p["inst"], p["cellpin"])
              for p in ps}), len(nodes), ">4000" if len(seen) >= 4000 else len(seen)))
for net in os.environ.get('FDEBUG', '').split():
    gs = {}
    for p in blk.pins:
        if p['net'] == net:
            gs.setdefault(p['group'], []).append('%s.%s %s' % (p['inst'], p['cellpin'], p['box']))
    print('DEBUG', net, gs)
for net in os.environ.get('FPATHS', '').split():
    k = names.index(net)
    for path in gr.paths.get(k, []):
        pts = []
        for n in path:
            L, b = gr.node_box(n)
            pts.append('%s(%.2f,%.2f)' % ('ab'[L], b.center().x * 0.001, b.center().y * 0.001 + 26))
        print('PATH', net, ' '.join(pts[:3]), '...', ' '.join(pts[-4:]))
    print('VIAS', net, [(round(gr.xl[r // gr.NY] * 0.001, 2), round(gr.yl[r % gr.NY] * 0.001 + 26, 2)) for r in gr.vias.get(k, [])])
for net in os.environ.get('FTERMS', '').split():
    for p in blk.pins:
        if p['net'] == net:
            for m, r in p['terms'].items():
                for q in r.each():
                    b = q.bbox().to_dtype(0.001)
                    print('TERM', net, p['inst'], p['cellpin'], m, '(%.3f,%.3f;%.3f,%.3f)' % (b.left, b.bottom + 26, b.right, b.top + 26))
