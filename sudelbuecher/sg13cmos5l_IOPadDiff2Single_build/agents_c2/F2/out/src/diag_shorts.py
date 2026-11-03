import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/sudel/sudelbuecher/design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/v2")
import generator as G
import klayout.db as db
cfg = G.load_config(sys.argv[1]); proc = G.load_process(cfg["PROCESS"])
blk = G.Block(cfg["NAME"], cfg["SOURCES"], cfg["INSTANCES"], cfg["FLOORPLAN"], proc, cfg["NETS"], cfg.get("PORTS"), None, cfg.get("ROUTER"), None, True, (), lambda *a: None)
blk.place(); blk._well_fill(blk.top)
cell = blk.top
for metal in ("M1", "M2"):
    texts = []
    it = cell.begin_shapes_rec(blk.LI[metal + "txt"])
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            texts.append((s.text_string, s.text.transformed(it.trans()).position(), it.cell().name))
        it.next()
    reg = db.Region(cell.begin_shapes_rec(blk.LI[metal]))
    for poly in reg.merged().each():
        names = {(t, cn) for t, p, cn in texts if poly.inside(p)}
        if len({t for t, _ in names}) > 1:
            print(metal, poly.bbox().to_dtype(0.001).moved(db.DVector(0, 84)), sorted(names)[:8])
