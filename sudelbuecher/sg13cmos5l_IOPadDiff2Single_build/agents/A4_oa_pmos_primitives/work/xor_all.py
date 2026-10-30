import sys, klayout.db as db
sys.path.insert(0, "../out/skill"); import generator as G
R = G.load_rules("/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json")
lib = db.Layout(); lib.read("../inputs/pad_buffer_cells.gds")
ly = db.Layout(); ly.dbu = 0.001
ok = 0; res = []
for a in lib.each_cell():
    if not a.name.startswith("pmosHV"): continue
    act = db.Region(a.shapes(lib.find_layer(1, 0))).merged()
    pol = db.Region(a.shapes(lib.find_layer(5, 0))).merged()
    if pol.count() != 1: res.append((a.name, "ng>1 skipped")); continue
    w = act.bbox().height() * lib.dbu; l = pol.bbox().width() * lib.dbu
    g = G.pmos_hv(ly, R, w, l, "g_" + a.name)
    bad = 0
    for li in lib.layer_indexes():
        i = lib.get_info(li); lg = ly.find_layer(i.layer, i.datatype)
        ra = db.Region(a.shapes(li)); rg = db.Region(g.shapes(lg)) if lg is not None else db.Region()
        if not (ra ^ rg).is_empty(): bad += 1
    res.append((a.name, "w=%g l=%g" % (w, l), "XOR 0" if not bad else "%d layers differ" % bad))
for r in res: print(*r)
