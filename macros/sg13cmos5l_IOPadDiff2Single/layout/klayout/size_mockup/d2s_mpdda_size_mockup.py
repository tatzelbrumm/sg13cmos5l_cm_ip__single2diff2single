# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Size mockup of the revised class-AB pad driver, Miller compensated
(improvements/sim: d2s_mpdda.spice with four unit_r2 from units.spice, + d2s_bias_lp.spice).
Made like ../../size_mockup/d2s_size_mockup.py (topology A, d2s_miller), so the two compare.

Every device is a real SG13_dev PCell with the netlist's w/l/ng at the .subckt defaults
(output devices: IHP's IO clamp frames, as in topology A; Miller capacitors CMA, CMB: hv PMOS
16 x 16 um in accumulation), placed on a grid that keeps the arrangement of
../xschem/d2s_mpdda_bias_flat.sch. Each grid row/column is as large as its largest device, so
the picture reads like the schematic but every device is drawn at its true size.
Not a layout: no wiring, no guard rings, no DRC. Labels are polygons on TEXT.drawing (63/0).

Inside IIC-OSIC-TOOLS, after `source .designinit` (sets PDK_ROOT and PDK):
    klayout -b -r d2s_mpdda_size_mockup.py   -> d2s_mpdda_size_mockup.gds in the current directory
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
top = ly.create_cell("d2s_mpdda_size_mockup")
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
    """The rhigh PCell is drawn vertically; the schematic has the R_* horizontal."""
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
mcap = mos(P, "16u", "16u", 1)        # CMA, CMB: wc = lc = 16u, ~0.8 pF each at the tt operating point
runit = rhigh("50.6u")                # R of unit_r2 at rl = 50.6u, ~150 kOhm

# name: (row, column, cell, label)  -- rows top to bottom, columns left to right, as in the .sch
mpdda = {}
for k, u in enumerate(("A", "B", "C1", "C2")):          # four unit_r2; columns Ta | R | Tb
    c = 6 + 3 * k
    mpdda.update({
        "Ta_" + u: (0, c, mos(P, "5u", "6u", 1), "5/6"),          "Tb_" + u: (0, c + 2, mos(P, "5u", "6u", 1), "5/6"),
        "R_" + u:  (1, c + 1, runit, "rhigh 0.5/50.6 150k"),
        "Ma_" + u: (2, c, mos(P, "20u", "1u", 2), "20/1 x2"),     "Mb_" + u: (2, c + 2, mos(P, "20u", "1u", 2), "20/1 x2"),
    })
mpdda.update({
    "PL":  (0, 19, mos(P, "24u", "4u", 4), "24/4 x4"),      "PR":  (0, 20, mos(P, "24u", "4u", 4), "24/4 x4"),
    "OP":  (0, 23, clampP, "546/0.6 x82: IHP Clamp_P15N15D frame"),
    "PCL": (1, 19, mos(P, "30u", "3u", 2), "30/3 x2"),      "PCR": (1, 20, mos(P, "30u", "3u", 2), "30/3 x2"),
    "CMA": (2, 22, mcap, "pmosHV 16/16 accum. 0.8pF"),
    "FNL": (3, 18, mos(N, "4.4u", "1u", 1), "4.4/1"),       "FPL": (3, 19, mos(P, "6.66u", "0.6u", 1), "6.66/0.6"),
    "ABP": (3, 20, mos(P, "6.66u", "0.6u", 1), "6.66/0.6"), "ABN": (3, 21, mos(N, "4.4u", "1u", 1), "4.4/1"),
    "CMB": (4, 22, mcap, "pmosHV 16/16 accum. 0.8pF"),
    "CX":  (5, 18, mos(N, "30u", "3u", 2), "30/3 x2"),      "CY":  (5, 21, mos(N, "30u", "3u", 2), "30/3 x2"),
    "SX":  (7, 18, mos(N, "36u", "6u", 4), "36/6 x4"),      "SY":  (7, 21, mos(N, "36u", "6u", 4), "36/6 x4"),
    "ON":  (7, 23, clampN2, "290/1 x66: 2 x IHP Clamp_N15N15D frame (L=0.6 stand-in)"),
})
bias = {   # d2s_bias_lp, at the left of the same sheet; ideal reference current sources not drawn
    "RP1": (0, 0, mos(P, "13.32u", "0.6u", 2), "13.32/0.6 x2"),
    "BPC": (0, 1, mos(P, "1u", "4u", 1), "1/4"),            "BP":  (0, 2, mos(P, "5u", "6u", 1), "5/6"),
    "RP2": (1, 0, mos(P, "6.66u", "0.6u", 1), "6.66/0.6"),
    "RN2": (6, 3, mos(N, "4.4u", "1u", 1), "4.4/1"),
    "RN1": (7, 3, mos(N, "8.8u", "1u", 2), "8.8/1 x2"),
    "BNC": (7, 4, mos(N, "1u", "8u", 1), "1/8"),            "BN":  (7, 5, mos(N, "6u", "6u", 1), "6/6"),
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


place({**bias, **mpdda}, 0, 0, "d2s_mpdda + d2s_bias_lp, Miller compensated, arranged as improvements/xschem/d2s_mpdda_bias_flat.sch")

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
print("  d2s_mpdda front end (w/o OP, ON, CMA, CMB):  %6.0f" % area(mpdda, skip=("OP", "ON", "CMA", "CMB")))
print("    of which the four DDA units:               %6.0f" % area({n: d for n, d in mpdda.items() if "_" in n}))
print("  d2s_bias_lp transistors:                     %6.0f" % area(bias))
print("  CMA + CMB:                                   %6.0f" % (2 * mcap.dbbox().area()))
print("  one Clamp_N frame:                           %6.0f" % clampN.dbbox().area())
print("  IO cell, substrate tap above the P frame:    %6.0f" % tap.area())
print("  IO cell, GateDecode/LevelDown band:          %6.0f" % logic.area())

ly.write("d2s_mpdda_size_mockup.gds")
