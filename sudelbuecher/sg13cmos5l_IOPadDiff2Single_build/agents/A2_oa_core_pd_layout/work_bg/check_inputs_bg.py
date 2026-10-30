import re, os, klayout.db as db
H = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(H, "..")
lib = db.Layout(); lib.read(A + "/inputs/pad_buffer_cells.gds")
def texts(c, li):
    r = []
    if li is None: return r
    it = c.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            t = s.text.transformed(it.trans()); r.append((t.string, t.x, t.y))
        it.next()
    return sorted(r)
for f in ("bg_misc_p", "bg_nab", "bg_pmir_pcas", "bg_pnp", "bg_res"):
    ex = db.Layout(); ex.read(A + "/inputs_bg/%s.gds" % f)
    c1, c2 = lib.cell(f), ex.cell(f)
    layers = set((i.layer, i.datatype) for i in lib.layer_infos()) | set((i.layer, i.datatype) for i in ex.layer_infos())
    nd = []
    for L in sorted(layers):
        l1, l2 = lib.find_layer(*L), ex.find_layer(*L)
        r1 = db.Region(c1.begin_shapes_rec(l1)) if l1 is not None else db.Region()
        r2 = db.Region(c2.begin_shapes_rec(l2)) if l2 is not None else db.Region()
        if not (r1 ^ r2).is_empty() or texts(c1, l1) != texts(c2, l2):
            nd.append(L)
    n1 = sorted(lib.cell(i).name for i in c1.called_cells()); n2 = sorted(ex.cell(i).name for i in c2.called_cells())
    print("%-14s tops %s; layers differing: %s; subcell names lib %s / export %s" % (f, [c.name for c in ex.top_cells()], nd or "none", n1, n2))
