# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage B4: P's s2d_inputs_c3 with the vfbp / vdd tracks swapped (lead, Christoph's go), fitted into stage B3's
# routed block.   python3 patch_b4.py <stage-B3 s2d_block.gds> <new p3_router.gds> <out s2d_block.gds>
# 1. s2d_inputs_c3's own shapes are replaced by the new cell's (its instances must be the same; every other P cell
#    that the block holds must be XOR-identical to the new library).
# 2. outp (vfbp): the router's one landing on the inputs band (Via1 + M2 pad at x 41.16..41.45 on its M1 riser
#    x 41.16..41.45, block y 107.58..111.65) moves from the old vfbp track (block y 110.19..110.45) to the new one
#    (109.71..109.97). vdd needs nothing: no block wiring lands on its track (it reaches iovdd through the cell's
#    own M1 at the tub ends), so the swap changes no outside connection of vdd.
import sys
import klayout.db as db
src, lib, dst = sys.argv[1:4]
ly = db.Layout(); ly.read(src); u = ly.dbu
nl = db.Layout(); nl.read(lib)
def li_of(L, info):
    i = L.find_layer(info)
    return i if i is not None else L.layer(info)
def own(c, L):
    return {L.get_info(i).to_s(): db.Region(c.shapes(i)) for i in L.layer_indexes() if not c.shapes(i).is_empty()}
# 0. the other P cells the block holds are unchanged
for c in nl.each_cell():
    if c.name == 's2d_inputs_c3' or ly.cell(c.name) is None:
        continue
    a, b = own(ly.cell(c.name), ly), own(c, nl)
    assert set(a) == set(b) and all((a[k] ^ b[k]).is_empty() for k in a), c.name
# 1. replace s2d_inputs_c3's own shapes
co, cn = ly.cell('s2d_inputs_c3'), nl.cell('s2d_inputs_c3')
io = sorted((i.cell.name, str(i.trans), i.na, i.nb) for i in co.each_inst())
inn = sorted((i.cell.name, str(i.trans), i.na, i.nb) for i in cn.each_inst())
assert io == inn, 'instances differ'
a, b = own(co, ly), own(cn, nl)
print('patch_b4: s2d_inputs_c3 layers differing:', sorted(k for k in set(a) | set(b)
      if not (a.get(k, db.Region()) ^ b.get(k, db.Region())).is_empty()))
for i in ly.layer_indexes():
    co.shapes(i).clear()
for i in nl.layer_indexes():
    if not cn.shapes(i).is_empty():
        co.shapes(li_of(ly, nl.get_info(i))).insert(cn.shapes(i))
# 2. move outp's landing
top = ly.cell('s2d_block')
M2, V1 = ly.find_layer(10, 0), ly.find_layer(19, 0)
for li, old, new in [(V1, (41.21, 110.225, 41.40, 110.415), (41.21, 109.745, 41.40, 109.935)),
                     (M2, (41.16, 110.19, 41.45, 110.45), (41.16, 109.71, 41.45, 109.97))]:
    ob = db.DBox(*old).to_itype(u)
    hit = [s for s in top.shapes(li).each() if s.bbox() == ob and (s.is_box() or s.polygon.num_points() == 4)]
    assert len(hit) == 1, (old, len(hit))
    top.shapes(li).erase(hit[0]); top.shapes(li).insert(db.DBox(*new).to_itype(u))
print('patch_b4: outp landing (Via1 + M2) moved from block y 110.19..110.45 to 109.71..109.97 at x 41.16..41.45')
opt = db.SaveLayoutOptions(); opt.gds2_write_timestamps = False
ly.write(dst, opt)
