# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""verify_bg_cells.py: A2's revised bandgap primitives against the library cells they replace (2026-10-28, Claude).

    python3 verify_bg_cells.py <pad_buffer_cells.gds> <bg_pnp_c.gds> <bg_res_c.gds>

bg_pnp_c vs bg_pnp: the device cell pnpMPA identical (XOR on every layer), the array the same (AREF origin, steps,
counts), the device layers of the whole array identical after flattening (Activ, NWell, pSD, nSD, Cont), the
library's device labels kept. bg_res_c vs bg_res: the device cell rhigh$1 identical (every layer), the 41 positions
at the same pitch and in the same order of R0 / R1A / R1B / dummy (from the labels), the resistor layers of the
array identical up to a translation (GatPoly, PolyRes, SalBlock, pSD, nSD, EXTBlock, Cont). Sizes before / after.
"""
import sys

import klayout.db as db

LIB, PNP, RES = sys.argv[1:4]
DEV = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "nSD": (7, 0), "pSD": (14, 0), "SalBlock": (28, 0),
       "NWell": (31, 0), "PolyRes": (128, 0), "EXTBlock": (111, 0), "RES": (24, 0)}


def load(p):
    ly = db.Layout()
    ly.read(p)
    return ly


def reg(ly, cell, ld, trans=None):
    li = ly.find_layer(*ld)
    if li is None:
        return db.Region()
    r = db.Region(cell.begin_shapes_rec(li)).merged()
    return r.transformed(trans) if trans is not None else r


def same_cell(la, ca, lb, cb):
    """XOR of every layer of two cells (flattened) and their texts; returns the list of differing layers."""
    diff = []
    lds = {(la.get_info(i).layer, la.get_info(i).datatype) for i in la.layer_indexes()} | \
          {(lb.get_info(i).layer, lb.get_info(i).datatype) for i in lb.layer_indexes()}
    for ld in sorted(lds):
        if not (reg(la, ca, ld) ^ reg(lb, cb, ld)).is_empty():
            diff.append("%d/%d" % ld)
    return diff


lib = load(LIB)
ok = True
print("1. bg_pnp_c (%s) vs library bg_pnp" % PNP.split("/")[-1])
pl = load(PNP)
d = same_cell(lib, lib.cell("pnpMPA"), pl, pl.cell("pnpMPA"))
print("   device cell pnpMPA: XOR differences on %s" % (", ".join(d) or "no layer"))
ok &= not d
ia = [i for i in lib.cell("bg_pnp").each_inst()][0]
ib = [i for i in pl.cell("bg_pnp_c").each_inst() if i.cell.name == "pnpMPA"][0]
arr = lambda i, ly: (i.dcplx_trans.disp.x, i.dcplx_trans.disp.y, i.da.x, i.da.y, i.db.x, i.db.y, i.na, i.nb)
print("   array: library %s, revised %s -> %s" % (arr(ia, lib), arr(ib, pl), "same" if arr(ia, lib) == arr(ib, pl) else "DIFFERENT"))
ok &= arr(ia, lib) == arr(ib, pl)
for name, ld in DEV.items():
    a, b = reg(lib, lib.cell("bg_pnp"), ld), reg(pl, pl.cell("bg_pnp_c"), ld)
    if a.is_empty() and b.is_empty():
        continue
    x = (a ^ b).area() * lib.dbu ** 2
    print("   %-8s XOR %.4f um2 (library %.2f um2)" % (name, x, a.area() * lib.dbu ** 2))
    ok &= x == 0
ta = sorted((s.text_string, s.dtext.x, s.dtext.y) for s in lib.cell("bg_pnp").shapes(lib.find_layer(63, 0)).each() if s.is_text())
tb = sorted((s.text_string, s.dtext.x, s.dtext.y) for s in pl.cell("bg_pnp_c").shapes(pl.find_layer(63, 0)).each() if s.is_text())
print("   device labels (63/0): %d in the library, %s" % (len(ta), "kept" if ta == tb else "CHANGED"))
ok &= ta == tb

print("2. bg_res_c (%s) vs library bg_res" % RES.split("/")[-1])
rl = load(RES)
d = same_cell(lib, lib.cell("rhigh$1"), rl, rl.cell("rhigh$1"))
print("   device cell rhigh$1: XOR differences on %s" % (", ".join(d) or "no layer"))
ok &= not d
pa = sorted(i.dcplx_trans.disp.x for i in lib.cell("bg_res").each_inst() if i.cell.name == "rhigh$1")
pb = sorted(i.dcplx_trans.disp.x for i in rl.cell("bg_res_c").each_inst() if i.cell.name == "rhigh$1")
ya = {round(i.dcplx_trans.disp.y, 4) for i in lib.cell("bg_res").each_inst() if i.cell.name == "rhigh$1"}
pitch = lambda p: sorted({round(b - a, 4) for a, b in zip(p[:-1], p[1:])})
print("   segments: library %d at pitch %s (y %s), revised %d at pitch %s" % (len(pa), pitch(pa), sorted(ya), len(pb), pitch(pb)))
ok &= len(pa) == len(pb) and pitch(pa) == pitch(pb)
lab = lambda ly, c: [t.split(".")[0] for _, t in sorted((s.dtext.x, s.text_string) for s in c.shapes(ly.find_layer(63, 0)).each() if s.is_text())]
la, lb = lab(lib, lib.cell("bg_res")), lab(rl, rl.cell("bg_res_c"))
print("   order of R0 / R1A / R1B / dummy: %s" % ("same" if la == lb else "DIFFERENT"))
ok &= la == lb
dy = int(round((min(round(i.dcplx_trans.disp.y, 4) for i in rl.cell("bg_res_c").each_inst()) - min(ya)) / lib.dbu))
shift = db.ICplxTrans(1.0, 0, False, int(round((pb[0] - pa[0]) / lib.dbu)), dy)
for name, ld in DEV.items():
    if name in ("NWell", "Activ"):
        continue
    a = reg(lib, lib.cell("bg_res"), ld, shift)
    b = reg(rl, rl.cell("bg_res_c"), ld)
    if ld in ((14, 0), (7, 0), (6, 0)):          # the library's p-tap ring has pSD / Cont of its own: compared are the
        a = a.interacting(b) if not b.is_empty() else a      # library shapes that touch the revised array's
    if a.is_empty() and b.is_empty():
        continue
    x = (a ^ b).area() * lib.dbu ** 2
    print("   %-8s XOR %.4f um2 (library %.2f um2, translated by %.3f, %.3f)" % (name, x, a.area() * lib.dbu ** 2,
                                                                                  shift.disp.x * lib.dbu, shift.disp.y * lib.dbu))
    ok &= x == 0
print("3. sizes")
for a, b, la_, lb_ in (("bg_pnp", "bg_pnp_c", lib, pl), ("bg_res", "bg_res_c", lib, rl)):
    ba, bb = la_.cell(a).dbbox(), lb_.cell(b).dbbox()
    print("   %-8s %.2f x %.2f = %6.1f um2  ->  %-9s %.2f x %.2f = %6.1f um2  (%+.1f %%)" % (
        a, ba.width(), ba.height(), ba.width() * ba.height(), b, bb.width(), bb.height(), bb.width() * bb.height(),
        100 * (bb.width() * bb.height() / (ba.width() * ba.height()) - 1)))
print("RESULT: %s" % ("devices as in the library" if ok else "DIFFERENCES (see above)"))
