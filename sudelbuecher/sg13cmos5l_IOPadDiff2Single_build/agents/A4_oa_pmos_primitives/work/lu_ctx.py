"""LU contexts for oa_pmir_c / oa_ms1 / oa_svpg with parent tap segments (generator.tap_path), DRC'd with the IHP-only
tool; minimal centred segment lengths by bisection (check.lu)."""
import sys, os, subprocess
sys.path.insert(0, "../out/skill")
import klayout.db as db, generator as G, check as K
import process.ihp_sg13cmos5l as P
src = sys.argv[1]
lib = db.Layout(); lib.read(src)
c = lib.cell("oa_pmir_c")
wa = 2 * P.rule("diff_encl_contact") + P.rule("contact_size")           # 0.30
row1_top, row4_bot = 38.25, 0.0
xend = 18.85
# tap diffusion in the top / bottom margin: diff_space from the rows, pimp_to_ntap from their pSD (pimp_encl_pdiff)
gapy = max(P.rule("diff_space"), P.rule("pimp_encl_pdiff") + P.rule("pimp_to_ntap"))
yt0 = row1_top + gapy; yb1 = row4_bot - gapy
def lu_with(rects):
    return K.lu(P, lib, c, rects)[0]
res = []
# (C) top + bottom segments, centred, in the margins
def tb(Ls):
    x0 = xend / 2 - Ls / 2; x1 = xend / 2 + Ls / 2
    return [(x0, yt0, x1, yt0 + wa), (x0, yb1 - wa, x1, yb1)]
lo, hi = 0.5, xend
for _ in range(30):
    m = (lo + hi) / 2
    if lu_with(tb(m)) <= 20.0: hi = m
    else: lo = m
Ltb = hi
res.append(("top+bottom segments in the margins, full width", lu_with(tb(xend))))
res.append(("top+bottom segments, minimum centred length %.2f each" % Ltb, lu_with(tb(Ltb))))
# (B) one left segment outside the cell edge (diffusion from the edge), centred
def left(Ls):
    y0 = 19.125 - Ls / 2; y1 = 19.125 + Ls / 2
    return [(-0.62 - wa, y0, -0.62, y1)]
lo, hi = 0.5, 39.49
for _ in range(30):
    m = (lo + hi) / 2
    if lu_with(left(m)) <= 20.0: hi = m
    else: lo = m
Ll = hi
res.append(("left edge, full height", lu_with(left(39.49))))
res.append(("left edge, minimum centred length %.2f" % Ll, lu_with(left(Ll))))
for r in res: print("%-55s farthest P diffusion %.2f um" % r)
# DRC contexts: pmir_c + parent taps (rounded-up segment lengths) and well extension above / below
ly = db.Layout(); ly.read(src)
pm = ly.cell("oa_pmir_c")
def ctx(name, paths):
    top = ly.create_cell(name)
    top.insert(db.CellInstArray(pm.cell_index(), db.Trans()))
    for k, pts in enumerate(paths):
        t = G.tap_path(ly, P, name + "_tap%d" % k, pts, "vdd")
        top.insert(db.CellInstArray(t.cell_index(), db.Trans()))
    return top
Lr = round(Ltb + 0.3, 1)
yc_t, yc_b = yt0 + wa / 2, yb1 - wa / 2
ctx("ctx_tb", [[(xend / 2 - Lr / 2, yc_t), (xend / 2 + Lr / 2, yc_t)], [(xend / 2 - Lr / 2, yc_b), (xend / 2 + Lr / 2, yc_b)]])
Lr2 = round(Ll + 0.3, 1)
ctx("ctx_left", [[(-0.62 - wa / 2, 19.125 - Lr2 / 2), (-0.62 - wa / 2, 19.125 + Lr2 / 2)]])
o = db.SaveLayoutOptions(); o.write_context_info = False
ly.write("lu_ctx.gds", o)
print("segments drawn: top/bottom %.1f um each at y %.3f / %.3f; left %.1f um" % (Lr, yc_t, yc_b, Lr2))
