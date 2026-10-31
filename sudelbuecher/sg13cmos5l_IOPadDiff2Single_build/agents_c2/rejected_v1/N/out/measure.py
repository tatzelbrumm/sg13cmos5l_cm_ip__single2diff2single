"""measure.py: pin table, outline, tie / TGO positions and the LU.b distance of each cell of d2s_n_cells.gds (measured from the GDS)"""
import sys, math
import klayout.db as db
l = db.Layout(); l.read(sys.argv[1] if len(sys.argv) > 1 else "d2s_n_cells.gds")
u = l.dbu
L = lambda a, b: l.layer(a, b)
CELLS = ["sinks_6x6_c", "sinks_6x6_s2d_c", "d2s_casc_n_c", "d2s_ab_n_c", "d2s_pd_n_c"]
def reg(c, a, b): return db.Region(c.begin_shapes_rec(L(a, b)))
for n in CELLS:
    c = l.cell(n); bb = c.dbbox()
    print("== %s  bbox (%.3f, %.3f) .. (%.3f, %.3f)  size %.3f x %.3f = %.1f um2" % (n, bb.left, bb.bottom, bb.right, bb.top, bb.width(), bb.height(), bb.width() * bb.height()))
    lay = sorted({(l.get_info(i).layer, l.get_info(i).datatype) for i in l.layer_indexes() if not db.Region(c.begin_shapes_rec(i)).is_empty()})
    print("   layers:", " ".join("%d/%d" % x for x in lay))
    labels = {}
    for (pl, tl, nm) in ((8, 25, "M1"), (10, 25, "M2")):
        for t in c.begin_shapes_rec(L(pl, tl)):
            s = t.shape()
            if s.is_text(): labels.setdefault(nm, []).append((s.text.string, t.trans() * s.text.trans.disp))
    for (pl, nm) in ((2, "M1"), (2, "M2")):
        pass
    for nm, pin_l, txt_l in (("Metal1", 8, 25), ("Metal2", 10, 25)):
        for sh in c.begin_shapes_rec(L(pin_l, 2)):
            b = sh.shape().bbox().transformed(sh.trans()).to_dtype(u)
            txt = [s for (s, p) in labels.get("M1" if pin_l == 8 else "M2", []) if b.contains(db.DPoint(p.x * u, p.y * u))] if False else []
            # label inside the box
            for t in c.begin_shapes_rec(L(pin_l, 25)):
                s = t.shape()
                if s.is_text():
                    p = (t.trans() * s.text.trans).disp
                    if b.contains(db.DPoint(p.x * u, p.y * u)): txt.append(s.text.string)
            side = [k for k, v in (("left", abs(b.left - bb.left) < 1e-6), ("right", abs(b.right - bb.right) < 1e-6), ("bottom", abs(b.bottom - bb.bottom) < 1e-6), ("top", abs(b.top - bb.top) < 1e-6)) if v]
            if not txt: continue
            print("   pin %-9s %-6s edge=%-12s box x %.3f..%.3f y %.3f..%.3f (w %.3f h %.3f) centre (%.3f, %.3f)" % (txt[0], nm, "+".join(side) or "inside", b.left, b.right, b.bottom, b.top, b.width(), b.height(), b.center().x, b.center().y))
    act = reg(c, 1, 0); psd = reg(c, 14, 0); cont = reg(c, 6, 0)
    tie = act & psd
    tie = tie.merged()
    nplus = (act - psd).merged()
    ties = [p.bbox().to_dtype(u) for p in tie.each()]
    print("   tie Activ boxes:", ["x %.3f..%.3f y %.3f..%.3f" % (t.left, t.right, t.bottom, t.top) for t in ties])
    tgo = reg(c, 44, 0).merged()
    print("   TGO: %d polygon(s), bbox %s" % (tgo.count(), tgo.bbox().to_dtype(u)))
    dmax = 0
    for p in nplus.each():
        for pt in p.each_point_hull():
            q = pt.to_dtype(u)
            d = min(math.hypot(max(t.left - q.x, 0, q.x - t.right), max(t.bottom - q.y, 0, q.y - t.top)) for t in ties)
            dmax = max(dmax, d)
    print("   LU.b: farthest N+Activ vertex to the nearest tie Activ: %.2f um (limit 20)" % dmax)
    print("   NWell shapes: %d" % reg(c, 31, 0).count())
