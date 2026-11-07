# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): route pad_ref_rb with generator.py (C3 F's route_block.py loop: nets that fail move to the
front, at most 8 rounds), then write a net map for the pictures.
    python3 route_rb.py <rb_cfg.py> <out.gds> <netmap.gds>
netmap.gds: per routed net its router wires, Metal1 on layer 1000 + k / 0, Metal2 on 1000 + k / 1, vias on
1000 + k / 2, with the net name as a text on 999/0 (k = index in NETS + 1)."""
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generator as G  # noqa: E402
import klayout.db as db  # noqa: E402

t0 = time.time()
cfg = G.load_config(sys.argv[1])
order = list(cfg.get("ROUTE_ORDER") or [])
for rnd in range(int(os.environ.get("FROUNDS", 8))):
    cfg["ROUTE_ORDER"] = order
    blk, rep = G.build(cfg, sys.argv[2], log=(print if rnd == 0 else (lambda *a: None)))
    bad = [n for n, _ in rep["failed"] or []]
    print("round %d: failed %s" % (rnd, bad))
    if not bad:
        break
    order = bad + [n for n in order if n not in bad]
print("ROUTE_ORDER used:", order)
print("failed:", rep["failed"], "time %.0f s" % (time.time() - t0))
for net, st in rep["wires"].items():
    print("  %-10s M1 %6.2f um  M2 %6.2f um  vias %d" % (net, st["M1"], st["M2"], st["vias"]))
print("ports:", {n: (round(b.left, 3), round(b.bottom, 3), round(b.right, 3), round(b.top, 3))
                 for n, b in blk.port_pins.items()})
gr = blk.router
ly = db.Layout()
ly.dbu = blk.dbu
c = ly.create_cell("netmap")
for k, net in enumerate(blk.nets, 1):
    for L, m in ((0, "M1"), (1, "M2")):
        r = gr.wire_region(m, k)
        if not r.is_empty():
            c.shapes(ly.layer(1000 + k, L)).insert(r)
    v = gr.via_region(k)
    if not v.is_empty():
        c.shapes(ly.layer(1000 + k, 2)).insert(v)
    c.shapes(ly.layer(999, 0)).insert(db.Text(net, 0, 0))
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[3], opt)
for net in os.environ.get("FEDGE", "").split():   # who holds the right-edge column near a port
    k = blk.nets.index(net) + 1
    f = gr.free(k)[1]
    i = gr.NX - 1
    print("EDGE", net, [(round(gr.yl[j] * blk.dbu, 2), [blk.nets[q - 1] for q in range(1, len(blk.nets) + 1)
                         if gr.mask[q, 1, i, j]]) for j in range(gr.NY)
                        if abs(gr.yl[j] * blk.dbu - cfg["PORTS"][net][1][0] - 0.45) < 1.2])
