"""Area audit of the v1 oa_core_pd (out/oa_core_pd.gds, read only): where do the 3856 um2 go?"""
import sys
import klayout.db as db

GDS = sys.argv[1]
ly = db.Layout()
ly.read(GDS)
top = ly.cell("oa_core_pd")
dbu = ly.dbu
A = lambda r: r.area() * dbu * dbu


def L(cell, l, d=0):
    li = ly.find_layer(l, d)
    return db.Region(cell.begin_shapes_rec(li)).merged() if li is not None else db.Region()


def dev_regions(cell):
    act, poly, psd, nw, tgo, m1, cont = (L(cell, 1), L(cell, 5), L(cell, 14), L(cell, 31), L(cell, 44),
                                         L(cell, 8), L(cell, 6))
    gate = act & poly
    mos_act = act.interacting(gate)         # S/D + channel of the transistors
    tap = act - mos_act                      # everything else on Activ: well / substrate ties, rings
    return dict(act=act, gate=gate, mos=mos_act, tap=tap, nw=nw, tgo=tgo, poly=poly, m1=m1, cont=cont)


bb = top.dbbox()
blk = bb.width() * bb.height()
print("block %.2f x %.2f = %.1f um2" % (bb.width(), bb.height(), blk))
rows = []
union = db.Region()
for inst in top.each_inst():
    c = inst.cell
    if not c.name.startswith("oa_") or c.name == "oa_pmir_image_jumpers":
        continue
    ib = inst.dbbox()
    r = dev_regions(c)
    core = (r["mos"] + r["gate"]).bbox()
    corea = core.width() * core.height() * dbu * dbu
    cb = c.dbbox()
    rows.append((c.name, ib, cb.width() * cb.height(), A(r["gate"]), A(r["mos"]), A(r["tap"]), corea))
    union += db.Region(inst.bbox())
print("%-10s %-30s %8s %8s %8s %8s %8s %8s" % ("cell", "placed bbox", "bbox", "gate", "MOSact", "tapAct",
                                               "devcore", "ring+"))
tot = [0] * 6
for n, ib, a, g, m, t, core in rows:
    print("%-10s %-30s %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f" % (n, "(%.2f,%.2f;%.2f,%.2f)" % (ib.left, ib.bottom,
          ib.right, ib.top), a, g, m, t, core, a - core))
    for i, v in enumerate((a, g, m, t, core, a - core)):
        tot[i] += v
print("%-10s %-30s %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f" % ("sum", "", *tot))
ua = A(union.merged())
print("union of placed cell bboxes %.1f um2; outside cells (rails + wiring + empty) %.1f um2 (%.0f %%)"
      % (ua, blk - ua, 100 * (blk - ua) / blk))
li = ly.find_layer(8, 0)
rails = db.Region()
for s in top.shapes(li).each():
    b = s.dbbox()
    if b.width() > 70:
        rails += db.Region(s.bbox())
print("rails %.1f um2" % A(rails))
free = (db.Region(top.bbox()) - union - rails).merged()
print("free (no cell bbox, no rail) %.1f um2; largest free rectangles:" % A(free))
boxes = []
for p in free.decompose_convex_to_region().each() if hasattr(free, "decompose_convex_to_region") else free.each():
    b = p.bbox()
    boxes.append((b.width() * b.height() * dbu * dbu, b))
for a, b in sorted(boxes, key=lambda t: -t[0])[:8]:
    print("   %.1f um2  (%.2f,%.2f;%.2f,%.2f)" % (a, b.left * dbu, b.bottom * dbu, b.right * dbu, b.top * dbu))
# gaps between neighbouring placed cells
print("gaps between placed cell bboxes (x-gap where y ranges overlap, y-gap where x ranges overlap):")
ins = [(c.name, c.dbbox) for c in []]
pl = [(n, ib) for n, ib, *_ in rows]
for i in range(len(pl)):
    for j in range(i + 1, len(pl)):
        (na, a), (nb, b) = pl[i], pl[j]
        yo = min(a.top, b.top) - max(a.bottom, b.bottom)
        xo = min(a.right, b.right) - max(a.left, b.left)
        if yo > 0:
            g = max(b.left - a.right, a.left - b.right)
            if g < 15:
                print("   %-9s | %-9s x-gap %6.2f (y overlap %.2f)" % (na, nb, g, yo))
        if xo > 0:
            g = max(b.bottom - a.top, a.bottom - b.top)
            if g < 15:
                print("   %-9s / %-9s y-gap %6.2f (x overlap %.2f)" % (na, nb, g, xo))
dv = dev_regions(top)
print("whole block: gate %.1f, MOS Activ %.1f, tap Activ %.1f, NWell %.1f, TGO %.1f um2"
      % (A(dv["gate"]), A(dv["mos"]), A(dv["tap"]), A(dv["nw"]), A(dv["tgo"])))
print("utilization: gate/block %.1f %%, MOS Activ/block %.1f %%"
      % (100 * A(dv["gate"]) / blk, 100 * A(dv["mos"]) / blk))
