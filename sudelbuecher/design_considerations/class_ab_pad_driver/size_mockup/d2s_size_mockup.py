# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Size mockup of the class-AB pad driver, topology A (d2s_miller.spice + d2s_bias.spice).

Every device is a real SG13_dev PCell with the netlist's w/l/ng (output devices: IHP's IO clamp
frames), placed on a grid that keeps the arrangement of xschem/d2s_miller.sch and
xschem/d2s_bias.sch. Each grid row/column is as large as its largest device, so the picture
reads like the schematic but every device is drawn at its true size.
Not a layout: no wiring, no guard rings, no DRC. Labels are polygons on TEXT.drawing (63/0).

Inside IIC-OSIC-TOOLS, after `source .designinit` (sets PDK_ROOT and PDK):
    klayout -b -r d2s_size_mockup.py         -> d2s_size_mockup.gds in the current directory
"""
import os
import sys

pdk = os.path.join(os.environ["PDK_ROOT"], os.environ["PDK"])
sys.path += [pdk + "/libs.tech/klayout/python",
             pdk + "/libs.tech/klayout/python/pycell4klayout-api/source/python"]
import pya
import sg13cmos5l_pycell_lib            # registers PCell library SG13_dev, as the PDK's autorun.lym does

ly = pya.Layout()
ly.technology_name = "sg13cmos5l"       # SG13_dev is registered for this technology only
TEXT = ly.layer(63, 0)
top = ly.create_cell("d2s_size_mockup")
tg = pya.TextGenerator.default_generator()   # mag 1.0 -> 0.7 um tall letters

# --- IHP IO cell (scale reference) and its clamp frames (output devices) --------------------
io = pya.Layout()
io.read(pdk + "/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds")
pad = ly.create_cell("sg13cmos5l_IOPadInOut30mA")
pad.copy_tree(io.cell("sg13cmos5l_IOPadInOut30mA"))     # brings its sub-cells along, same names
clampP = ly.cell("sg13cmos5l_Clamp_P15N15D")
clampN = ly.cell("sg13cmos5l_Clamp_N15N15D")
clampN2 = ly.create_cell("ON_2x_Clamp_N15N15D")          # XON = two N frames, stacked
for k in range(2):
    clampN2.insert(pya.DCellInstArray(clampN.cell_index(), pya.DTrans(0, k * clampN.dbbox().height())))


def mos(kind, w, l, ng):
    """SPICE w is the total width; so is the PCell's w (finger width = w/ng)."""
    return ly.create_cell(kind, "SG13_dev", {"w": w, "l": l, "ng": str(ng)})


def turned(cell):
    """The rhigh PCell is drawn vertically; the schematic has R1, R2 horizontal."""
    c = ly.create_cell(cell.name + "_r90")
    c.insert(pya.DCellInstArray(cell.cell_index(), pya.DTrans(pya.DTrans.R90)))
    return c


def text(lines, x, y, mag):
    """Polygon text, first line on top, lower left corner at (x, y). Returns its height."""
    h = 0.0
    for line in reversed(lines):
        top.shapes(TEXT).insert(tg.text(line, ly.dbu, mag).moved(pya.DVector(x, y + h).to_itype(ly.dbu)))
        h += 1.3 * 0.7 * mag
    return h


P, N = "pmosHV", "nmosHV"
rhigh = lambda l: turned(ly.create_cell("rhigh", "SG13_dev", {"w": "0.5u", "l": l, "b": "0"}))
cmom = ly.create_cell("cap_cmomi", "SG13_dev", {"w": "31u", "l": "31u"})

# name: (row, column, cell, label)  -- rows top to bottom, columns left to right, as in the .sch
miller = {
    "T1a": (0, 0, mos(P, "20u", "2u", 2), "20/2 x2"),       "T1b": (0, 2, mos(P, "20u", "2u", 2), "20/2 x2"),
    "T2a": (0, 3, mos(P, "20u", "2u", 2), "20/2 x2"),       "T2b": (0, 5, mos(P, "20u", "2u", 2), "20/2 x2"),
    "PL":  (0, 7, mos(P, "10u", "2u", 1), "10/2"),          "PR":  (0, 8, mos(P, "10u", "2u", 1), "10/2"),
    "OP":  (0, 11, clampP, "546/0.6 x82: IHP Clamp_P15N15D frame"),
    "PCL": (1, 7, mos(P, "10u", "1u", 1), "10/1"),          "PCR": (1, 8, mos(P, "10u", "1u", 1), "10/1"),
    "R1":  (2, 1, rhigh("39u"), "rhigh 0.5/39 116k"),       "R2":  (2, 4, rhigh("17u"), "rhigh 0.5/17 51k"),
    "CMA": (2, 10, cmom, "cmomi 31x31 1pF"),
    "M1a": (3, 0, mos(P, "20u", "1u", 2), "20/1 x2"),       "M1b": (3, 2, mos(P, "20u", "1u", 2), "20/1 x2"),
    "M2a": (3, 3, mos(P, "20u", "1u", 2), "20/1 x2"),       "M2b": (3, 5, mos(P, "20u", "1u", 2), "20/1 x2"),
    "FNL": (3, 6, mos(N, "4.4u", "1u", 1), "4.4/1"),        "FPL": (3, 7, mos(P, "6.66u", "0.6u", 1), "6.66/0.6"),
    "ABP": (3, 8, mos(P, "6.66u", "0.6u", 1), "6.66/0.6"),  "ABN": (3, 9, mos(N, "4.4u", "1u", 1), "4.4/1"),
    "CMB": (4, 10, cmom, "cmomi 31x31 1pF"),
    "CX":  (5, 6, mos(N, "10u", "1u", 1), "10/1"),          "CY":  (5, 9, mos(N, "10u", "1u", 1), "10/1"),
    "SX":  (6, 6, mos(N, "25u", "2u", 2), "25/2 x2"),       "SY":  (6, 9, mos(N, "25u", "2u", 2), "25/2 x2"),
    "ON":  (6, 11, clampN2, "290/1 x66: 2 x IHP Clamp_N15N15D frame (L=0.6 stand-in)"),
}
bias = {   # ideal reference current sources IBP ... IABN are not drawn
    "RP1": (0, 3, mos(P, "13.32u", "0.6u", 2), "13.32/0.6 x2"),
    "BPC": (0, 4, mos(P, "2u", "4u", 1), "2/4"),            "BP":  (0, 5, mos(P, "20u", "2u", 2), "20/2 x2"),
    "RP2": (1, 3, mos(P, "6.66u", "0.6u", 1), "6.66/0.6"),
    "RN2": (2, 0, mos(N, "4.4u", "1u", 1), "4.4/1"),
    "RN1": (3, 0, mos(N, "8.8u", "1u", 2), "8.8/1 x2"),
    "BNC": (3, 1, mos(N, "1u", "4u", 1), "1/4"),            "BN":  (3, 2, mos(N, "25u", "2u", 2), "25/2 x2"),
}

GAP, MAG = 3.0, 1.5          # um between grid cells; label size (1.5 -> ~1 um letters)
LINE = 1.3 * 0.7 * MAG


def place(devices, x0, y0, title):
    """Grid placement; (x0, y0) is the upper left corner. Returns the group's lower edge."""
    colw, rowh = {}, {}
    for name, (r, c, cell, lab) in devices.items():
        b = cell.dbbox()
        lw = max(len(name), len(lab)) * 0.6 * MAG                  # std_font letter: 0.6 x 0.7 um at mag 1
        colw[c] = max(colw.get(c, 0.0), b.width(), lw)
        rowh[r] = max(rowh.get(r, 0.0), b.height() + 2 * LINE + 0.5)
    y0 -= text([title], x0, y0 - 0.7 * 4, 4) + GAP
    xs, x = {}, x0
    for c in sorted(colw):
        xs[c], x = x, x + colw[c] + GAP
    ys, y = {}, y0
    for r in sorted(rowh):
        y -= rowh[r]
        ys[r], y = y, y - GAP
    for name, (r, c, cell, lab) in devices.items():
        b = cell.dbbox()
        top.insert(pya.DCellInstArray(cell.cell_index(), pya.DTrans(xs[c] - b.left, ys[r] - b.bottom)))
        text([name, lab], xs[c], ys[r] + b.height() + 0.5, MAG)
    return y


y = place(miller, 0, 0, "d2s_miller (topology A), arranged as xschem/d2s_miller.sch")
place(bias, 0, y - 10, "d2s_bias, arranged as xschem/d2s_bias.sch")

# IO cell for scale, to the right, with what occupies the part above its P frame outlined:
# from the P frame's top edge up to the top of the cell's own (top-level) Activ polygons, a solid
# p+ substrate tap (Activ/pSD/Cont/Metal1) under the iovdd/iovss rails; above it GateDecode and
# LevelDown under the vdd/vss rails.
bb = top.dbbox()
at = pya.DVector(bb.right + 30, bb.top - pad.dbbox().top)
top.insert(pya.DCellInstArray(pad.cell_index(), pya.DTrans(at)))
p_top = max(i.dbbox().top for i in pad.each_inst() if i.cell_index == clampP.cell_index())
a_top = max(s.dbbox().top for s in pad.shapes(ly.layer(1, 0)).each() if s.dbbox().height() > 1)
tap = pya.DBox(0, p_top, 80, a_top)
logic = pya.DBox(0, a_top, 80, pad.dbbox().top)
for box, what in [(tap, "p+ substrate tap under iovdd/iovss rails"),
                  (logic, "GateDecode + LevelDown under vdd/vss rails")]:
    b = box.moved(at)
    top.shapes(TEXT).insert(pya.DPath([b.p1, pya.DPoint(b.left, b.top), b.p2,
                                       pya.DPoint(b.right, b.bottom), b.p1], 0.5))
    text([what, "%.0f x %.0f um" % (b.width(), b.height())], b.right + 3, b.center().y, 2.5)
text(["sg13cmos5l_IOPadInOut30mA, for scale"], at.x, bb.top + 2, 2.5)


def area(devs, skip=()):
    return sum(c.dbbox().area() for n, (_, _, c, _) in devs.items() if n not in skip)


print("device bounding-box areas, um2:")
print("  d2s_miller front end (w/o OP, ON, CMA, CMB): %6.0f" % area(miller, skip=("OP", "ON", "CMA", "CMB")))
print("  d2s_bias transistors:                        %6.0f" % area(bias))
print("  CMA + CMB:                                   %6.0f" % (2 * cmom.dbbox().area()))
print("  one Clamp_N frame:                           %6.0f" % clampN.dbbox().area())
print("  IO cell, substrate tap above the P frame:    %6.0f" % tap.area())
print("  IO cell, GateDecode/LevelDown band:          %6.0f" % logic.area())

ly.write("d2s_size_mockup.gds")
