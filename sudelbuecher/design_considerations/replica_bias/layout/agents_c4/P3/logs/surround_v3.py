"""surround_v3.py <gds>: device layers of rb_avg in a window of +- one finger pitch (1.25 um) in x around each active
finger (SU, SL1, SL2), over the full height of its row (well bottom - 0.5 ... well top + 0.5); each window moved onto
SU's; XOR against SU's window (um2). A second pass with +- two pitches shows where the surroundings first differ."""
import sys
import klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1]); top = ly.cell("rb_avg"); u = ly.dbu
DEV = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "pSD": (14, 0), "NWell": (31, 0), "TGO": (44, 0)}
# finger Activ boxes: each row cell's PCell instances, in the top cell's frame
fing = {}
for inst in top.each_inst():
    sub = inst.cell
    names = {"rb_avg_u": ["DU0", "SU", "DU1"], "rb_avg_l": ["DL0", "SL1", "SL2", "DL1"]}[sub.name]
    boxes = []
    for i in sub.each_inst():
        if i.cell.name.startswith("rb_pmosHV"):
            b = (inst.dcplx_trans * i.dcplx_trans) * i.cell.dbbox_per_layer(ly.find_layer(1, 0))
            boxes.append(b)
    for n, b in zip(names, sorted(boxes, key=lambda b: b.left)):
        fing[n] = b
def win(n, ld, k):
    a = fing[n]
    r = db.Region(top.begin_shapes_rec(ly.find_layer(*ld))).merged()
    w = db.Region(db.DBox(a.left - k * 1.25, a.bottom - 0.62 - 0.5, a.right + k * 1.25, a.top + 1.13 + 0.5).to_itype(u))
    d = fing["SU"].p1 - a.p1
    return (r & w).moved(db.Vector(int(round(d.x / u)), int(round(d.y / u))))
for k in (1, 2):
    for n in ("SL1", "SL2"):
        tot, per = 0.0, []
        for ln, ld in DEV.items():
            x = (win(n, ld, k) ^ win("SU", ld, k)).area() * u * u
            tot += x
            if x: per.append("%s %.4f" % (ln, x))
        print("+-%d pitch: %s window vs SU window, device layers: XOR %.4f um2 %s" % (k, n, tot, " ".join(per)))
print("finger Activ boxes:", {n: str(b) for n, b in fing.items()})
