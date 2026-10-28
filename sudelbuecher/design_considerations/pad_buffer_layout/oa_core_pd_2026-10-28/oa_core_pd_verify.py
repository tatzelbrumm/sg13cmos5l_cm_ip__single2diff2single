# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Checks of oa_core_pd.gds that are not DRC / LVS (2026-10-28, Claude):
1. every cell below the top except oa_pmir_image_jumpers equals the library cell of the same name
   (XOR on every layer, texts, child instances);
2. point symmetry of oa_pmir's wiring: oa_pmir + oa_pmir_image_jumpers against their point image about the
   centre of oa_pmir (XOR per layer; texts / pins not included);
3. layers used by the new cells; 4. port pins and the block edge.
    python3 oa_core_pd_verify.py oa_core_pd.gds pad_buffer_cells.gds
"""
import sys
import klayout.db as db

out_gds, lib_gds = sys.argv[1], sys.argv[2]
o, lib = db.Layout(), db.Layout()
o.read(out_gds)
lib.read(lib_gds)
top = o.cell("oa_core_pd")


def texts(ly, c, li):
    r = []
    if li is None:
        return r
    it = c.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            t = s.text.transformed(it.trans())
            r.append((t.string, t.x, t.y))
        it.next()
    return sorted(r)


print("1. cells against the library")
bad = 0
n = 0
for c in o.each_cell():
    if c.name in ("oa_core_pd", "oa_pmir_image_jumpers"):
        continue
    lc = lib.cell(c.name)
    if lc is None:
        print("   %s: not in the library" % c.name)
        bad += 1
        continue
    n += 1
    layers = set((i.layer, i.datatype) for i in o.layer_infos()) | set((i.layer, i.datatype) for i in lib.layer_infos())
    diff = []
    for L in sorted(layers):
        a, b = o.find_layer(*L), lib.find_layer(*L)
        ra = db.Region(c.begin_shapes_rec(a)) if a is not None else db.Region()
        rb = db.Region(lc.begin_shapes_rec(b)) if b is not None else db.Region()
        if not (ra ^ rb).is_empty() or texts(o, c, a) != texts(lib, lc, b):
            diff.append(L)
    ia = sorted((o.cell(i.cell_index).name, str(i.trans), i.size()) for i in c.each_inst())
    ib = sorted((lib.cell(i.cell_index).name, str(i.trans), i.size()) for i in lc.each_inst())
    if diff or ia != ib:
        bad += 1
        print("   %s: layers differing %s, instances equal %s" % (c.name, diff, ia == ib))
print("   %d cells compared (6 primitives and all their sub-cells), %d differ" % (n, bad))

print("2. point symmetry of oa_pmir with oa_pmir_image_jumpers")
pm, im = o.cell("oa_pmir"), o.cell("oa_pmir_image_jumpers")
nb = db.Region(pm.begin_shapes_rec(o.find_layer(31, 0))).bbox()
R = db.Trans(db.Trans.R180, db.Vector(nb.left + nb.right, nb.bottom + nb.top))
print("   centre (%.3f, %.3f) um" % ((nb.left + nb.right) / 2 * o.dbu, (nb.bottom + nb.top) / 2 * o.dbu))
for name, L in (("Activ", (1, 0)), ("GatPoly", (5, 0)), ("Cont", (6, 0)), ("pSD", (14, 0)), ("NWell", (31, 0)),
                ("ThickGateOx", (44, 0)), ("Metal1", (8, 0)), ("Via1", (19, 0)), ("Metal2", (10, 0))):
    li = o.find_layer(*L)
    r = db.Region(pm.begin_shapes_rec(li)) + db.Region(im.begin_shapes_rec(li))
    r0 = db.Region(pm.begin_shapes_rec(li))
    x = r ^ r.transformed(R)
    x0 = r0 ^ r0.transformed(R)
    print("   %-11s XOR with image: %8.4f um2 (oa_pmir alone: %8.4f um2)" % (name, x.area() * o.dbu ** 2, x0.area() * o.dbu ** 2))

print("3. layers with shapes in the new cells")
for c in (top, im):
    used = sorted("%d/%d" % (o.get_info(li).layer, o.get_info(li).datatype) for li in o.layer_indexes()
                  if not c.shapes(li).is_empty())
    print("   %s: %s" % (c.name, " ".join(used)))
used_all = sorted("%d/%d" % (o.get_info(li).layer, o.get_info(li).datatype) for li in o.layer_indexes()
                  if not db.Region(top.begin_shapes_rec(li)).is_empty() or texts(o, top, li))
print("   whole hierarchy: %s" % " ".join(used_all))

print("4. ports (pin box layer, text layer, box, edge)")
bb = top.dbbox()
print("   block %.3f x %.3f um (x %.3f ... %.3f, y %.3f ... %.3f), %.1f um2" % (bb.width(), bb.height(), bb.left, bb.right,
                                                                           bb.bottom, bb.top, bb.width() * bb.height()))
for pl, tl in (((8, 2), (8, 25)), ((10, 2), (10, 25))):
    pi, ti = o.find_layer(*pl), o.find_layer(*tl)
    for s in top.shapes(ti).each():
        t = s.dtext
        box = [p.dbbox() for p in top.shapes(pi).each() if p.dbbox().contains(db.DPoint(t.x, t.y))]
        b = box[0] if box else None
        edges = [n for n, ok in (("left", b.left <= bb.left + 1e-6), ("right", b.right >= bb.right - 1e-6),
                                 ("bottom", b.bottom <= bb.bottom + 1e-6), ("top", b.top >= bb.top - 1e-6)) if ok] if b else []
        print("   %-9s %d/%d + %d/%d  %s  edge: %s" % (t.string, pl[0], pl[1], tl[0], tl[1], b, ",".join(edges) or "NONE"))
