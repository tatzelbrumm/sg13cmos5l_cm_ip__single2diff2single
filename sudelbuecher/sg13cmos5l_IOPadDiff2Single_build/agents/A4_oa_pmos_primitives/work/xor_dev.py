import sys, klayout.db as db
sys.path.insert(0, "../out/skill"); import generator as G
R = G.load_rules(G.__dict__.get("DECK", "/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json"))
lib = db.Layout(); lib.read("../inputs/pad_buffer_cells.gds")
ly = db.Layout(); ly.dbu = 0.001
for cn, w, l in (("pmosHV$9", 2, 8), ("pmosHV$13", 0.5, 12.5), ("pmosHV$7", 1, 0.45), ("pmosHV$15", None, None), ("pmosHV$3", None, None)):
    if w is None:
        continue
    g = G.pmos_hv(ly, R, w, l, "g_" + cn)
    a = lib.cell(cn)
    bad = []
    layers = set()
    for li in lib.layer_indexes():
        i = lib.get_info(li); layers.add((i.layer, i.datatype))
    for li in ly.layer_indexes():
        i = ly.get_info(li); layers.add((i.layer, i.datatype))
    for (L, D) in sorted(layers):
        la, lg = lib.find_layer(L, D), ly.find_layer(L, D)
        ra = db.Region(a.shapes(la)) if la is not None else db.Region()
        rg = db.Region(g.shapes(lg)) if lg is not None else db.Region()
        x = (ra ^ rg)
        if not x.is_empty(): bad.append((L, D, x.area()))
        ta = sorted((s.text_string, str(s.text_trans), s.text_size) for s in a.shapes(la).each() if s.is_text()) if la is not None else []
        tg = sorted((s.text_string, str(s.text_trans), s.text_size) for s in g.shapes(lg).each() if s.is_text()) if lg is not None else []
        if ta != tg: bad.append((L, D, "texts", ta, tg))
    print("%-10s w=%g l=%g: %s" % (cn, w, l, "XOR 0 on all layers, texts equal" if not bad else bad))
