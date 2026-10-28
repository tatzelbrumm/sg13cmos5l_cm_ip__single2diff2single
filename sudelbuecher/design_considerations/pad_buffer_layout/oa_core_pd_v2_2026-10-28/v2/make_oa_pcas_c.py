# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""oa_pcas_c: oa_pcas without its own ntap ring, NWell drawn to the cell edge, so that it merges with the
neighbouring PMOS cells' NWell (all bulk = vdd) and is tapped by the parent's tap segments.
Written 2026-10-28 by Claude (Opus 5.5) on the coordinator's instruction of 02:58 (user: "separate nwells
connected to the same voltage rail are EXTREMELY wasteful").

    python3 make_oa_pcas_c.py <pad_buffer_cells.gds> <out.gds>

What changes (nothing else; checked by XOR in the self-check at the end):
  - the four ntap1 ring instances (ntap1$33 x 2, ntap1$34 x 2) are removed;
  - the cell's own Metal1 shapes lying on the ring (the vdd bar) and the vdd pin box / text are removed;
  - NWell becomes the bounding box of everything that is left (the cell edge).
Devices, Cont, Via1, Metal2 tracks, pins of the signal nets, pSD, ThickGateOx: unchanged. Electrically no device
changes; the PMOS bulk is the NWell, tied to vdd by the parent (no vdd pin in the cell any more).
"""
import sys
import klayout.db as db

LIB = sys.argv[1]
OUT = sys.argv[2]
ly = db.Layout()
ly.read(LIB)
src = ly.cell("oa_pcas")
keep = {src.cell_index()} | set(src.called_cells())
for ci in [c.cell_index() for c in ly.each_cell()]:
    if ci not in keep:
        ly.delete_cell(ci)
dbu = ly.dbu
new = ly.create_cell("oa_pcas_c")
li = {k: ly.find_layer(*v) for k, v in {"act": (1, 0), "m1": (8, 0), "m1p": (8, 2), "m1t": (8, 25),
                                         "nw": (31, 0)}.items()}
ring_cells = [i for i in src.each_inst() if i.cell.name.startswith("ntap1")]
ring_act = db.Region()
for i in ring_cells:
    ring_act += db.Region(i.cell.begin_shapes_rec(li["act"])).transformed(i.cplx_trans)
ring_band = ring_act.merged().sized(int(0.2 / dbu))
for i in src.each_inst():
    if not i.cell.name.startswith("ntap1"):
        new.insert(i.cell_inst)
removed = {"m1": 0, "pin": 0, "text": 0}
for lidx in ly.layer_indexes():
    for s in src.shapes(lidx).each():
        if lidx == li["nw"]:
            continue
        if lidx == li["m1"] and not s.is_text() and (db.Region(s.polygon) - ring_band).is_empty():
            removed["m1"] += 1
            continue
        if lidx == li["m1p"] and not s.is_text() and (db.Region(s.polygon) - ring_band).is_empty():
            removed["pin"] += 1
            continue
        if lidx in (li["m1t"], li["m1p"]) and s.is_text() and s.text_string == "vdd":
            removed["text"] += 1
            continue
        new.shapes(lidx).insert(s)
bb = new.bbox()
new.shapes(li["nw"]).insert(bb)
src_name = src.cell_index()
ly.delete_cell(src.cell_index())
for c in [c for c in ly.each_cell() if c.name.startswith("ntap1")]:
    if c.parent_cells() == 0:
        ly.delete_cell(c.cell_index())
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(OUT, opt)
print("oa_pcas_c: removed %d ring instances, %d M1 shapes, %d pin boxes, %d vdd texts; NWell = cell bbox %s "
      "(%.2f x %.2f um = %.1f um2; oa_pcas %.2f x %.2f = %.1f um2)"
      % (len(ring_cells), removed["m1"], removed["pin"], removed["text"], bb.to_dtype(dbu), bb.width() * dbu,
         bb.height() * dbu, bb.area() * dbu * dbu, 21.46, 8.54, 21.46 * 8.54))

# self-check: oa_pcas_c equals oa_pcas minus (ring instances, ring M1, vdd pin) on every layer except NWell
ref = db.Layout()
ref.read(LIB)
rc = ref.cell("oa_pcas")
chk = db.Layout()
chk.read(OUT)
cc = chk.cell("oa_pcas_c")
bad = []
for lidx in ref.layer_indexes():
    inf = ref.get_info(lidx)
    if (inf.layer, inf.datatype) == (31, 0):
        continue
    a = db.Region()
    for s in rc.shapes(lidx).each():
        if not s.is_text():
            a.insert(s.polygon)
    for i in rc.each_inst():
        if not i.cell.name.startswith("ntap1"):
            a += db.Region(i.cell.begin_shapes_rec(lidx)).transformed(i.cplx_trans)
    if (inf.layer, inf.datatype) in ((8, 0), (8, 2)):
        a = a - db.Region([p for p in a.each() if (db.Region(p) - ring_band).is_empty()])
    j = chk.find_layer(inf.layer, inf.datatype)
    b = db.Region()
    if j is not None:
        it = cc.begin_shapes_rec(j)
        it.shape_flags = db.Shapes.SPolygons | db.Shapes.SBoxes | db.Shapes.SPaths
        b = db.Region(it)
    x = a ^ b
    if not x.is_empty():
        bad.append(("%d/%d" % (inf.layer, inf.datatype), x.area() * dbu * dbu))
    ta = sorted((s.text_string, s.text.x, s.text.y) for s in rc.shapes(lidx).each() if s.is_text()
                and not (s.text_string == "vdd" and (inf.layer, inf.datatype) in ((8, 25), (8, 2))))
    tb = sorted((s.text_string, s.text.x, s.text.y) for s in cc.shapes(j).each() if s.is_text()) if j is not None else []
    if ta != tb:
        bad.append(("%d/%d texts" % (inf.layer, inf.datatype), sorted(set(ta) ^ set(tb))))
print("XOR oa_pcas (minus ring) vs oa_pcas_c, all layers but NWell: %s" % (bad or "none differing"))
