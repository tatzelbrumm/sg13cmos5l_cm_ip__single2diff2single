# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 stage B: the pad candidate sg13cmos5l_IOPadDiff2Single.

    python3 build_pad_B.py <pad_ctx.gds> <d2s_block.gds> <out_pad.gds>

pad_ctx.gds: the pad as drawn + rejected F's stage-2 pad-top cells (build_pad.py, F's code, only its input path
changed). d2s_block.gds: the routed block (route_block.py); placed at (0, 84) without its padtop_ctx_f2 copy.
Pad-level changes, all in the new cell pad_wiring_f2 except where named:
  - top cell: the 63/0 TEXT.drawing box deleted (Christoph 2026-10-31 16:50);
  - CMA (cell d2s_cma, F's): its source / drain / well columns off the pad (the 88 Via1 onto the junction's Metal2
    tabs removed, the left tab removed) and onto pa, the node behind CMA's 2 kOhm stage: a new Metal2 tab with Via1
    on the left column, a Metal1 strap across CMA to the right column, a Metal2 line up the left edge channel
    (x 2.55 .. 2.85, beside F's vfb Kelvin line), Metal1 under the a / b joins, into the stage's core node;
  - CMB (cell m2_comb_p): its gate's last feed from the pad (the 2 Via1 at x 72.2 .. 72.8, y 50.6) removed; the
    gate head onto pb, the node behind CMB's stage: Via1 at its right end, Metal2 east and up the right edge channel
    (x 78.0 .. 78.3), Metal1 under the joins, into the stage's core node;
  - the stages' pad pins down to the pad: Metal1 (0.84 wide, 2 Via1 at each end) under the joins, Metal2 over the
    NWell isolator onto the P frame's 0.61 um pad lines (x 8.74 .. 9.35 / 72.16 .. 72.77, ending at y 81.45);
  - the stages' p+ rings (iovss) onto the edge stubs' iovss p+ (Metal1, x 0 .. 1.2 / 78.8 .. 80);
  - vsso (SB's source) on its own path to the P frame's p+ ring (iovss): Metal1 under the joins, Metal2 over the
    isolator, Via1 onto the ring's Metal1;
  - vfb: F's Kelvin line from the junction's left end up the left edge channel (vfb_kelvin), unchanged.
"""
import sys

import klayout.db as db

PAD, BLK, OUT = sys.argv[1:4]
ly = db.Layout()
ly.read(PAD)
top = ly.top_cell()
LI = {k: ly.layer(*v) for k, v in {"M1": (8, 0), "V1": (19, 0), "M2": (10, 0), "T63": (63, 0)}.items()}
top.shapes(LI["T63"]).clear()

# ---- the routed block, without its context copy
b = db.Layout()
b.read(BLK)
blk = ly.create_cell("d2s_block")
blk.copy_tree(b.cell("d2s_block"))
for inst in list(blk.each_inst()):
    if inst.cell.name.startswith("padtop_ctx_f2"):
        ci = inst.cell.cell_index()
        inst.delete()
        ly.delete_cell(ci)
top.insert(db.DCellInstArray(blk.cell_index(), db.DTrans(db.DVector(0, 84.0))))

# ---- CMA off the pad
cma = ly.cell("d2s_cma")
cma.shapes(LI["V1"]).clear()
for s in list(cma.shapes(LI["M2"]).each()):
    if s.is_box() and abs(s.dbox.left - 3.24) < 1e-6 and abs(s.dbox.right - 4.08) < 1e-6:
        cma.shapes(LI["M2"]).erase(s)
# ---- CMB's gate off the pad
cp = ly.cell("m2_comb_p")
gone = [s for s in cp.shapes(LI["V1"]).each() if 50.4 < s.dbox.center().y < 50.9 and 72.0 < s.dbox.center().x < 73.0]
assert len(gone) == 2, len(gone)
for s in gone:
    cp.shapes(LI["V1"]).erase(s)

# F's standalone pin labels "pad" on CMA's column and CMB's gate head now sit on pa / pb: removed
for name in ("d2s_cma", "d2s_cmb"):
    cl = ly.cell(name)
    for k in ((8, 25), (8, 2), (10, 25), (10, 2)):
        li = ly.find_layer(*k)
        if li is None:
            continue
        for s in list(cl.shapes(li).each()):
            if s.is_text() and s.text_string == "pad":
                p = s.text.position()
                cl.shapes(li).erase(s)
                for q in list(cl.shapes(ly.find_layer(k[0], 2)).each()):
                    if q.is_box() and q.box.contains(p):
                        cl.shapes(ly.find_layer(k[0], 2)).erase(q)
# NWell isolator (F's nw_isolator): its tap at x 9.045 (Metal2 over the P frame's pad line x 8.74 .. 9.35) removed so
# that CMA's stage reaches that pad line; 18 taps remain
iso = ly.cell("nw_isolator")
for k in ((10, 0), (19, 0), (29, 0)):
    li = ly.find_layer(*k)
    for s in list(iso.shapes(li).each()):
        if 8.70 < s.dbox.center().x < 9.40:
            iso.shapes(li).erase(s)
w = ly.create_cell("pad_wiring_f2")
top.insert(db.DCellInstArray(w.cell_index(), db.DTrans()))


def box(k, x0, y0, x1, y1):
    w.shapes(LI[k]).insert(db.DBox(round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)))


def via(x, y):
    box("V1", x - 0.095, y - 0.095, x + 0.095, y + 0.095)


def hop(x0, x1, y_hi, y_lo, xs):
    """Metal1 under the a / b joins from a Via1 row at y_hi down to one at y_lo (vias at xs)"""
    box("M1", x0, y_lo - 0.145, x1, y_hi + 0.145)
    for x in xs:
        via(x, y_hi)
        via(x, y_lo)


# vfb: rejected F's vfb_kelvin (junction's left end, up the left edge channel, Metal1 under the joins)
box("M2", 1.90, 39.80, 3.40, 40.40)
box("M2", 1.90, 39.80, 2.20, 87.10)
via(2.05, 86.95)
box("M1", 1.90, 86.80, 2.20, 88.55)
via(2.05, 88.40)
box("M2", 1.90, 88.25, 2.20, 88.85)
# pa: CMA's left column (x 3.24 .. 4.13, y 40.85 .. 49.93) -> left edge channel -> stage core (x 8.35 .. 8.85)
box("M2", 3.24, 41.60, 4.08, 49.80)
for k in range(19):
    y = 41.85 + 0.41 * k
    via(3.44, y)
    via(3.85, y)
box("M1", 4.13, 45.00, 36.41, 45.60)             # right column (x 36.41 .. 37.30) joined across CMA in Metal1
box("M2", 2.55, 45.85, 3.24, 46.15)
box("M2", 2.55, 45.85, 2.85, 86.20)
hop(2.55, 2.85, 88.40, 86.05, (2.70,))
box("M2", 2.55, 88.25, 2.85, 93.42)
box("M2", 2.55, 93.12, 8.85, 93.42)
# pb: CMB's gate head (M1 y 50.46 .. 50.82, right end x 73.41) -> right edge channel -> stage core (x 71.5 .. 72.0)
via(73.25, 50.64)
box("M2", 73.10, 50.49, 78.30, 50.79)
box("M2", 78.00, 50.49, 78.30, 86.20)
hop(78.00, 78.30, 88.40, 86.05, (78.15,))
box("M2", 78.00, 88.25, 78.30, 93.42)
box("M2", 71.50, 93.12, 78.30, 93.42)
# stage pad pins (stage pad Metal2 x 4.14 .. 4.98 / 75.37 .. 76.21 from y 88.78) -> the P frame's pad lines
# (Metal2 0.61 wide, x 8.74 .. 9.35 / 72.16 .. 72.77, ending at y 81.45 under the frame's top ring)
for x0, x1, px0, px1 in ((4.14, 4.98, 8.74, 9.35), (75.37, 76.21, 72.16, 72.77)):
    box("M2", x0, 88.22, x1, 88.78)
    hop(x0, x1, 88.40, 85.90, (x0 + 0.21, x1 - 0.21))
    box("M2", min(x0, px0), 85.75, max(x1, px1), 86.15)
    box("M2", px0, 81.00, px1, 86.15)
# stage p+ rings (iovss) -> edge stubs' iovss p+ (Metal1, 1.0 wide: the stage's whole iovss path)
box("M1", 0.60, 95.50, 3.40, 96.50)
box("M1", 76.95, 95.50, 79.40, 96.50)
# vsso -> P frame's p+ ring (M1 y 83.95 .. 84.25)
box("M2", 63.95, 88.25, 65.00, 88.85)
hop(63.95, 64.25, 88.40, 85.90, (64.10,))
box("M2", 63.95, 83.94, 64.25, 86.05)
via(64.10, 84.10)

opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
opt.write_context_info = True
ly.write(OUT, opt)
print("pad candidate written:", OUT, top.name, top.dbbox())
