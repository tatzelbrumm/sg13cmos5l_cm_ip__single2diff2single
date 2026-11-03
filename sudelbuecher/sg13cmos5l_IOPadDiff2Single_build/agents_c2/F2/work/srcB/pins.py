# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""list every instance pin of the block in pad coordinates: python3 pins.py <block_cfg.py>"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/sudel/sudelbuecher/design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/v2")
import generator as G
cfg = G.load_config(sys.argv[1])
proc = G.load_process(cfg["PROCESS"])
blk = G.Block(cfg["NAME"], cfg["SOURCES"], cfg["INSTANCES"], cfg["FLOORPLAN"], proc, cfg["NETS"], cfg.get("PORTS"),
              None, cfg.get("ROUTER"), None, False, (), lambda *a: None)
blk.place()
off = -blk.bbox.left, 84.0 - blk.bbox.bottom
for inst, t in blk.leaves.items():
    b = blk.ly.cell(cfg["INSTANCES"][inst]["cell"]).dbbox().transformed(t).moved(db.DVector(*off)) if False else None
import klayout.db as db
for inst, t in sorted(blk.leaves.items()):
    c = blk.ly.cell(cfg["INSTANCES"][inst]["cell"])
    bb = c.dbbox().transformed(t).moved(db.DVector(*off))
    print("%-7s %-16s %s" % (inst, c.name, bb))
    if inst in ("ctx", "pwr"):
        continue
    for m, n, b in blk.cell_pins(c.name):
        nb = b.transformed(t).moved(db.DVector(*off))
        print("    %-9s -> %-9s %s %s" % (n, cfg["INSTANCES"][inst]["nets"].get(n, n), m, nb))
