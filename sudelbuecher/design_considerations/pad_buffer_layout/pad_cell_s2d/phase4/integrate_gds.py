# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""C3 phase 4 (lead): F's pad candidate -> the macro's sg13cmos5l_IOPadSingle2Diff.klay.gds.

usage: python3 integrate_gds.py <pad_candidate.gds> <out.klay.gds>

1. The iovdd rail tie (Christoph 2026-11-04: "keep the strap for now, maybe annotate with TEXT.drawing so it can be
   manually removed if necessary") moves out of F's pwr_f into a cell of its own, iovdd_rail_tie, placed in the top
   cell at the same coordinates: one Metal2 strap, two Metal3 landings, four Via2. Its outline and a note are drawn on
   TEXT.drawing 63/0. To remove the tie, delete the one instance of iovdd_rail_tie.
2. Every port text of the top cell (datatype 25) is copied to the pin datatype 2, as C2 did (commit 2abcca1), so magic
   sees the ports too. No text is added for vss (substrate merge with iovss, C2 report 4.3).
No other shape changes; the script checks that by XOR of every drawing layer, flattened, against the input.
"""
import sys
import klayout.db as db

src, dst = sys.argv[1:3]
ly = db.Layout(); ly.read(src)
top = ly.top_cell()
assert top.name == 'sg13cmos5l_IOPadSingle2Diff', top.name
um = lambda v: int(round(v / ly.dbu))
B = lambda x0, y0, x1, y1: db.Box(um(x0), um(y0), um(x1), um(y1))

# --- 1. the rail tie (src/make_pwr.py of agent F: pwr_f sits at the global origin)
pwr = ly.cell('pwr_f')
tie_shapes = {(10, 0): [B(76.55, 90.20, 77.35, 95.20)],
              (30, 0): [B(76.55, 90.50, 77.35, 91.10), B(76.55, 94.30, 77.35, 94.90)],
              (29, 0): [B(76.95 + dx - 0.095, y - 0.095, 76.95 + dx + 0.095, y + 0.095)
                        for y in (90.80, 94.60) for dx in (-0.205, 0.205)]}
tie = ly.create_cell('iovdd_rail_tie')
for (ln, dt), boxes in tie_shapes.items():
    li = ly.layer(ln, dt)
    for b in boxes:
        hits = [s for s in pwr.shapes(li).each_overlapping(b) if s.is_box() and s.box == b]
        assert len(hits) == 1, ((ln, dt), b, len(hits))
        pwr.shapes(li).erase(hits[0])
        tie.shapes(li).insert(b)
txt = ly.layer(63, 0)
tie.shapes(txt).insert(B(76.35, 90.00, 77.55, 95.40))
tie.shapes(txt).insert(db.Text('iovdd_rail_tie: removable, delete this instance (C3 2026-11-04)',
                               db.Trans(um(76.95), um(92.50))))
top.insert(db.CellInstArray(tie.cell_index(), db.Trans()))

# --- 2. port texts on the pin datatype
for li in list(ly.layer_indexes()):
    info = ly.get_info(li)
    if info.datatype != 25:
        continue
    pin = ly.layer(info.layer, 2)
    for s in top.shapes(li).each():
        if s.is_text():
            assert s.text.string != 'vss'
            top.shapes(pin).insert(s.text)

opt = db.SaveLayoutOptions(); opt.gds2_write_timestamps = False
ly.write(dst, opt)

# --- XOR check against the input, every layer, flattened (texts aside)
a = db.Layout(); a.read(src)
b = db.Layout(); b.read(dst)
bad = 0
for li in a.layer_indexes():
    info = a.get_info(li)
    if (info.layer, info.datatype) == (63, 0):
        continue    # the tie's note, checked below
    lb = b.find_layer(info)
    ra = db.Region(a.top_cell().begin_shapes_rec(li))
    rb = db.Region(b.top_cell().begin_shapes_rec(lb)) if lb is not None else db.Region()
    x = ra ^ rb
    if not x.is_empty():
        bad += 1; print('XOR', info, x.area() * a.dbu ** 2)
new = [b.get_info(li) for li in b.layer_indexes() if a.find_layer(b.get_info(li)) is None]
print('layers new in the output:', [str(i) for i in new])
for li in b.layer_indexes():
    if str(b.get_info(li)) == '63/0':
        print('63/0 area um2', db.Region(b.top_cell().begin_shapes_rec(li)).area() * b.dbu ** 2)
ntxt = sum(1 for li in b.layer_indexes() if b.get_info(li).datatype == 2
           for sh in b.top_cell().shapes(li).each() if sh.is_text())
print('port texts on datatype 2:', ntxt)
print('XOR layers differing (63/0 aside):', bad)
sys.exit(1 if bad else 0)
