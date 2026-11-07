#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""make_slot_7.py --- slot_7.gds of the slot-7 test platform (stage A), docs/slot7_testplatform/PLAN.md.

Usage (design repository root, after `export PDK_ROOT=/foss/pdks; source .designinit`):
    python3 macros/slot7_testplatform/layout/scripts/make_slot_7.py <base slot_7.gds> <out slot_7.gds> [--pads custom|foundry]

<base>: the current delivery slot_7.gds (frame + the 13 custom-pad pins and stubs, tatzelbrumm/sg13cmos5l_cm_slot7 main
40ba9b0). Its shapes are kept unchanged. --pads foundry instead starts from macros/slot/layout/klayout/slot.klay.gds
of `harness-test` given as <base> (the frame with the IOPadAnalog pins s7_an[0], s7_an[1], s7_an_0_esd); the platform
is the same, it never comes near x >= 520.

Placed: tp_en_ctrl (built here by tp_en_ctrl.py, mirrored so its pins face up), oa_core_pd and bg_core_pd
(macros/*/layout/gds, unchanged), two xgate (macros/ocd_analog_switches/layout/klayout/xgate.klay.gds, unchanged).
Every sub-cell name gets the prefix `slot7_` so nothing collides with other slots' cells in the harness.
Routing: Metal3 horizontal, Metal4 vertical, TopMetal1 bands from the four supply stubs at the left edge.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tp_en_ctrl as T                         # noqa: E402  (builds into pbc_row.ly)
from pbc_row import ly, LI, box, g5            # noqa: E402
import pya                                     # noqa: E402

MAC = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
for k, v in {"TM1": (126, 0), "TV1": (125, 0), "M1txt": (8, 25)}.items():
    LI[k] = ly.layer(*v)


def import_cell(path, name, src_name=None):
    """Copy the cell src_name (default: the file's only top cell) of a GDS into ly as `name`."""
    src = pya.Layout()
    src.read(path)
    top = src.cell(src_name) if src_name else src.top_cell()
    dst = ly.create_cell(name)
    dst.copy_tree(top)
    return dst


def via(lay, x, y, c=None):
    box(c or TOP, lay, x - 0.095, y - 0.095, x + 0.095, y + 0.095)


def m3h(y, x0, x1, w=0.29):
    box(TOP, "M3", min(x0, x1) - 0.15, y - w / 2, max(x0, x1) + 0.15, y + w / 2)


def m4v(x, y0, y1, w=0.3):
    box(TOP, "M4", x - w / 2, min(y0, y1) - 0.15, x + w / 2, max(y0, y1) + 0.15)


def v3(x, y):
    """Via3 with 0.29 landing pads on M3 and M4."""
    box(TOP, "M3", x - 0.145, y - 0.145, x + 0.145, y + 0.145)
    box(TOP, "M4", x - 0.15, y - 0.15, x + 0.15, y + 0.15)
    via("Via3", x, y)


def v2_on_m2pin(x, y, xm0, xm1, pad=True):
    """Via2 on an M2 pin row y; pad=True extends the pin row (0.29 tall) over xm0..xm1 (core pins at the cell edge),
    pad=False lands on the pin itself (xgate pins are 0.20 .. 0.45 tall and only 0.24 apart: a wider pad would
    close the gap, M2.b)."""
    if pad:
        box(TOP, "M2", xm0, y - 0.145, xm1, y + 0.145)
    box(TOP, "M3", x - 0.145, y - 0.145, x + 0.145, y + 0.145)
    via("Via2", x, y)


def stack_m1_tm1(x, y):
    """M1 -> TopMetal1 at (x, y): pads 0.39 on M2 / M3, 0.62 on M4, TopVia1 0.42 (TV1.c 0.10)."""
    via("Via1", x, y)
    for lay in ("M2", "M3"):
        box(TOP, lay, x - 0.195, y - 0.195, x + 0.195, y + 0.195)
    via("Via2", x, y)
    via("Via3", x, y)
    box(TOP, "M4", x - 0.31, y - 0.31, x + 0.31, y + 0.31)
    box(TOP, "TV1", x - 0.21, y - 0.21, x + 0.21, y + 0.21)


def tv1_on_m4col(x, y):
    box(TOP, "M4", x - 0.31, y - 0.31, x + 0.31, y + 0.31)
    box(TOP, "TV1", x - 0.21, y - 0.21, x + 0.21, y + 0.21)


def stage_b(colA, xg, XP):
    """Stage B (2026-11-06, slot7_stage_b.spice): tp_en_ctrl_b, bias_tree_noab_pd, 8 xgates, all at x 145 .. 285 um.
    Stage A's geometry is not touched; only new shapes are added (the i_oa / i_bg Metal4 lines of stage A are
    extended downwards, the enable row is extended to the right, the TopMetal1 bands are extended to the right)."""
    import routed_cell as R
    bands, ext = R.tp_en_ctrl_b_spec()
    cb, colsb, ybb = R.build_routed("tp_en_ctrl_b", bands, ext)
    routed_tree = '--tree' in sys.argv and sys.argv[sys.argv.index('--tree') + 1] == 'routed'
    if routed_tree:                     # the first, naive tree (2026-11-06): one NMOS and one PMOS row, routed
        bands, ext = R.tree_spec()
        ct, colst, ybt = R.build_routed("bias_tree_noab_pd", bands, ext)
    else:                               # the matched tree (2026-11-07): layout/tree/assembly, pins on its right edge
        ct = import_cell(os.path.join(MAC, 'slot7_testplatform', 'layout', 'tree', 'assembly', 'bias_tree_noab_pd.gds'),
                         'bias_tree_noab_pd')
    # tp_en_ctrl_b: not mirrored, pins at its bottom edge at y = 100
    BX, YB = 187.0, 100.0
    BY = g5(YB - (ybb - 0.15))
    TOP.insert(pya.DCellInstArray(cb.cell_index(), pya.DTrans(pya.DVector(BX, BY))))
    cB = {n: g5(BX + x) for n, x in colsb.items()}
    ytopB = g5(BY + cb.dbbox().top)
    if routed_tree:
        # tree: pins at its bottom edge at y = 7
        TX, YT = 232.0, 7.0
        TY = g5(YT - (ybt - 0.15))
        TOP.insert(pya.DCellInstArray(ct.cell_index(), pya.DTrans(pya.DVector(TX, TY))))
        cT = {n: g5(TX + x) for n, x in colst.items()}
    else:
        # matched tree, mirrored about the y axis (x -> TX - x) so that its right-edge Metal2 pins face left;
        # cell 32.21 x 18.68: x 229.79 .. 262.00, y 1.0 .. 19.68 (below the lowest xgate, whose pins start at y 20.16)
        TX, TY = 262.0, 1.0
        TOP.insert(pya.DCellInstArray(ct.cell_index(), pya.DTrans(pya.DTrans.M90, pya.DVector(TX, TY))))
        TPIN = {"en_3v3_b": 16.59, "iref": 15.69, "vbpc": 14.79, "vbp": 13.89, "vbn": 12.99, "vbnc": 12.09,
                "en_3v3": 10.86}          # pin centres (cell y), pins at cell x 31.78 .. 32.21
        xpin = g5(TX - 32.0)             # 230.0, inside the mirrored pin boxes (229.79 .. 230.22)
    # Metal4 lanes between stage A and tp_en_ctrl_b (inputs of the xgates) and right of the xgates (outputs)
    LANE = {"i_oa": 147.5, "i_bg": 148.5, "ibias0": 149.5, "ibias1": 150.5,
            "vbp": 151.5, "vbn": 152.5, "vbpc": 153.5, "vbnc": 154.5, "iref": 214.0, "bus2": 215.5, "bus3": 217.0}
    span = {}                                   # lane -> [ymin, ymax] to draw at the end

    def lane_at(n, y):
        v3(LANE[n], y)
        s = span.setdefault(n, [y, y])
        s[0], s[1] = min(s[0], y), max(s[1], y)

    # inputs: dig_in[4..12] and enable (Metal3 rows at the pin height, Via3, column down from the cell)
    rows = {f"en{k}_1v2": round(80.22 + 0.44 * k, 2) for k in range(9)}
    for n, y in rows.items():
        box(TOP, "M3", 1.0, y - 0.11, cB[n] + 0.15, y + 0.11)
        box(TOP, "M4", cB[n] - 0.15, y - 0.15, cB[n] + 0.15, YB + 0.3)
        via("Via3", cB[n], y)
    y = 89.47
    box(TOP, "M3", colA["enable"], y - 0.11, cB["enable"] + 0.15, y + 0.11)
    box(TOP, "M4", cB["enable"] - 0.15, y - 0.15, cB["enable"] + 0.15, YB + 0.3)
    via("Via3", cB["enable"], y)
    # supplies: columns over the cell height and down to the tree lines; TopMetal1 bands extended
    for n in ("vdd_3v3", "vss_3v3"):
        m4v(cB[n], 0.9, ytopB - 0.3)
    m4v(cB["vdd_1v2"], 44.5, ytopB - 0.3)
    box(TOP, "TM1", 140.0, 116.0, 200.0, 125.0)
    tv1_on_m4col(cB["vss_3v3"], 120.5)
    box(TOP, "TM1", 140.0, 190.0, 200.0, 200.0)
    tv1_on_m4col(cB["vdd_3v3"], 195.0)
    box(TOP, "TM1", 30.0, 40.0, 190.0, 50.0)
    tv1_on_m4col(cB["vdd_1v2"], 45.0)
    # sources: i_oa, i_bg (stage A's Metal4 lines extended down), ibias0, ibias1 (rows from the left-edge pins)
    m4v(88.0, 95.5, 114.0)
    v3(88.0, 95.5)
    m3h(95.5, 88.0, LANE["i_oa"])
    lane_at("i_oa", 95.5)
    m4v(145.5, 96.5, 105.0)
    v3(145.5, 96.5)
    m3h(96.5, 145.5, LANE["i_bg"])
    lane_at("i_bg", 96.5)
    for n, y in (("ibias0", 98.155), ("ibias1", 101.095)):
        box(TOP, "M3", 1.0, y - 0.15, LANE[n] + 0.15, y + 0.15)
        lane_at(n, y)
    # analog_bus2 / analog_bus3: stub, Metal4 jog down, Metal3 along y 93.5 / 92.5 to the output lanes
    for n, yp, xj, yl in (("bus2", 106.975, 4.5, 93.5), ("bus3", 104.035, 5.5, 92.5)):
        box(TOP, "M3", 1.0, yp - 0.15, xj + 0.15, yp + 0.15)
        v3(xj, yp)
        m4v(xj, yl, yp)
        v3(xj, yl)
        m3h(yl, xj, LANE[n])
        lane_at(n, yl)
    # the eight xgates: one column at x = 200, out pins to the right lanes, the rest to the left
    XGB = [("i_oa", "iref", 0), ("i_bg", "iref", 1), ("ibias0", "iref", 2), ("ibias1", "bus3", 8),
           ("vbp", "bus2", 4), ("vbn", "bus2", 5), ("vbpc", "bus2", 6), ("vbnc", "bus2", 7)]
    for i, (nin, nout, k) in enumerate(XGB):
        gx, gy = 200.0, g5(74.0 - 7.0 * i)
        TOP.insert(pya.DCellInstArray(xg.cell_index(), pya.DTrans(pya.DVector(gx, gy))))
        xp = g5(gx + 3.04)
        for pin, net in (("vdd", "vdd_3v3"), ("vss", "vss_3v3"), ("ena", f"en{k}"), ("ena_b", f"en{k}_b")):
            yy = g5(gy + XP[pin][0])
            v2_on_m2pin(xp, yy, 0, 0, pad=False)
            m3h(yy, cB[net], xp)
            v3(cB[net], yy)
            if net.startswith("en"):
                m4v(cB[net], yy, YB + 0.3)
        yy = g5(gy + XP["in"][0])
        v2_on_m2pin(xp, yy, 0, 0, pad=False)
        m3h(yy, LANE[nin], xp)
        lane_at(nin, yy)
        yo, xo = g5(gy + XP["out"][0]), g5(gx + 8.055)
        v2_on_m2pin(xo, yo, 0, 0, pad=False)
        m3h(yo, xo, LANE[nout])
        lane_at(nout, yo)
    TGT = {"vdd": ("col", "vdd_3v3"), "vss": ("col", "vss_3v3"), "iref": ("lane", "iref"),
           "vbp": ("lane", "vbp"), "vbn": ("lane", "vbn"), "vbpc": ("lane", "vbpc"), "vbnc": ("lane", "vbnc"),
           "en_3v3": ("col", "en3"), "en_3v3_b": ("col", "en3_b")}

    def to_target(n, y, x_from):
        kind, tgt = TGT[n]
        xt = cB[tgt] if kind == "col" else LANE[tgt]
        m3h(y, xt, x_from)
        if kind == "col":
            v3(xt, y)
            if tgt.startswith("en"):
                m4v(xt, y, YB + 0.3)
        else:
            lane_at(tgt, y)

    if routed_tree:
        # tree pins: Metal4 down from the tree's bottom edge to one Metal3 line each (y 0.9 .. 5.7), then left
        for k, n in enumerate(TGT):
            y = g5(0.9 + 0.6 * k)
            m4v(cT[n], y, YT + 0.3)
            v3(cT[n], y)
            to_target(n, y, cT[n])
    else:
        # signal pins: Via2 on the Metal2 pin, Metal3 to the left at the pin height
        for n, yc in TPIN.items():
            y = g5(TY + yc)
            v2_on_m2pin(xpin, y, 0, 0, pad=False)
            to_target(n, y, xpin)
        # rails: Metal1 extended 2.3 um left of the cell, then Via1 / Via2 to a Metal3 line to the supply column
        for n, (r0, r1) in (("vss", (0.0, 1.01)), ("vdd", (17.32, 18.68))):
            y0, y1 = g5(TY + r0), g5(TY + r1)
            box(TOP, "M1", TX - 32.21 - 2.3, y0, TX - 32.21 + 0.1, y1)
            xs, ys = g5(TX - 32.21 - 1.5), g5((y0 + y1) / 2)
            via("Via1", xs, ys)
            for lay in ("M2", "M3"):
                box(TOP, lay, xs - 0.195, ys - 0.195, xs + 0.195, ys + 0.195)
            via("Via2", xs, ys)
            to_target(n, ys, xs)
    for n, (y0, y1) in span.items():
        m4v(LANE[n], y0, y1)
    return cB


def main():
    global TOP
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    base, out = args[0], args[1]
    # --- tp_en_ctrl ---------------------------------------------------------------------------------------------
    ctl, cols, y_bot = T.build_tp_en_ctrl()
    for c in list(ly.top_cells()):
        if c.name != "tp_en_ctrl":
            ly.delete_cell_rec(c.cell_index())
    oa = import_cell(os.path.join(MAC, 'oa_core_pd', 'layout', 'gds', 'oa_core_pd.gds'), 'oa_core_pd')
    bg = import_cell(os.path.join(MAC, 'bg_core_pd', 'layout', 'gds', 'bg_core_pd.gds'), 'bg_core_pd')
    xg = import_cell(os.path.join(MAC, 'ocd_analog_switches', 'layout', 'klayout', 'xgate.klay.gds'), 'xgate')
    TOP = import_cell(base, 'slot_7')

    # --- placement ----------------------------------------------------------------------------------------------
    CX, CY = 32.0, 2.2                       # tp_en_ctrl mirrored about x (M0): y' = CY - y
    TOP.insert(pya.DCellInstArray(ctl.cell_index(), pya.DTrans(pya.DTrans.M0, pya.DVector(CX, CY))))
    col = {n: g5(CX + x) for n, x in cols.items()}
    y_ctl_top = g5(CY - (y_bot - 0.15))      # cell top edge (pins)
    OAX, OAY, BGX, BGY = 45.0, 128.0, 95.0, 128.0
    TOP.insert(pya.DCellInstArray(oa.cell_index(), pya.DTrans(pya.DVector(OAX, OAY))))
    TOP.insert(pya.DCellInstArray(bg.cell_index(), pya.DTrans(pya.DVector(BGX, BGY))))
    # xgate pins (cell coordinates, Metal2): name -> (y centre, x0, x1)
    XP = {"vdd": (-1.2325, 2.53, 3.53), "ena_b": (-1.795, 2.54, 3.54), "in": (-2.42, 2.54, 3.54),
          "ena": (-4.225, 2.55, 3.55), "vss": (-4.8375, 2.55, 3.55), "out": (-3.6575, 7.555, 8.555)}
    BUS0, BUS1 = 112.855, 109.915
    XG0 = (34.0, g5(BUS0 - XP["out"][0]))    # out pin at the analog_bus0 height
    XG1 = (34.0, g5(104.0 - XP["out"][0]))   # out pin at y 104.0, jog to analog_bus1
    for (x, y) in (XG0, XG1):
        TOP.insert(pya.DCellInstArray(xg.cell_index(), pya.DTrans(pya.DVector(x, y))))

    # --- tp_en_ctrl pins to the frame's left-edge pins (Metal3 rows at the pin height, Via3, Metal4 column up) -------
    FRAME = {"dig_in[0]": 78.46, "dig_in[1]": 78.90, "dig_in[2]": 79.34, "dig_in[3]": 79.78, "enable": 89.47}
    FRAME.update({f"dig_out[{k}]": round(72.30 + 0.44 * k, 2) for k in range(12)})
    CTLPIN = {"dig_in[0]": "en0_1v2", "dig_in[1]": "en1_1v2", "dig_in[2]": "en2_1v2", "dig_in[3]": "en3_1v2",
              "enable": "enable"}
    CTLPIN.update({f"dig_out[{k}]": f"rb{k}" for k in range(4)})
    CTLPIN.update({f"dig_out[{k}]": f"lo{k}" for k in range(4, 12)})
    for pin, y in FRAME.items():
        x = col[CTLPIN[pin]]
        box(TOP, "M3", 1.0, y - 0.11, x + 0.15, y + 0.11)      # 0.22 tall like the frame stub, overlapping it
        box(TOP, "M4", x - 0.15, y_ctl_top - 0.3, x + 0.15, y + 0.15)
        via("Via3", x, y)

    # --- supplies -------------------------------------------------------------------------------------------------
    # the four supply columns of tp_en_ctrl, extended over the whole cell height (only columns use M4 there)
    for n in ("vdd_3v3", "vss_3v3", "vdd_1v2", "vss_1v2"):
        m4v(col[n], CY + 0.5, y_ctl_top)
    box(TOP, "TM1", 0.0, 40.0, 35.0, 50.0)                    # vdd_1v2 band (stub y 2.0 .. 56.8)
    tv1_on_m4col(col["vdd_1v2"], 45.0)
    box(TOP, "TM1", 3.0, 61.0, 35.0, 69.5)                    # vss_1v2 band (stub y 66.4 .. 96.4), and its
    box(TOP, "TM1", 0.0, 66.365, 3.2, 69.5)                   # connector inside the stub's y range at the edge
    tv1_on_m4col(col["vss_1v2"], 65.0)
    box(TOP, "TM1", 0.0, 116.0, 150.0, 125.0)                 # vss_3v3 band (stub y 113.5 .. 143.5)
    m4v(col["vss_3v3"], y_ctl_top, 120.5)
    tv1_on_m4col(col["vss_3v3"], 120.5)
    box(TOP, "TM1", 0.0, 190.0, 150.0, 200.0)                 # vdd_3v3 band (stub y 151.1 .. 256.1)
    m4v(col["vdd_3v3"], y_ctl_top, 195.0)
    tv1_on_m4col(col["vdd_3v3"], 195.0)
    # core rails: one 2 um wide Metal1 finger per stack, from the rail out to the TM1 band (fingers, not a plate:
    # a plate would make the rail "wide" metal, >= 10 um, and pull in the 0.6 um spacing rule M1.f inside the core)
    for (cx, cy, w, h, rail_b, rail_t) in ((OAX, OAY, 40.51, 58.135, 1.42, 56.635), (BGX, BGY, 47.55, 50.05, 0.80, 49.05)):
        x = cx + 1.5
        while x < cx + w - 1.0:
            box(TOP, "M1", x - 1.0, 121.5, x + 1.0, cy + rail_b)      # vss: down to the vss_3v3 band
            box(TOP, "M1", x - 1.0, cy + rail_t, x + 1.0, 197.0)      # vdd: up to the vdd_3v3 band
            stack_m1_tm1(g5(x), 122.5)
            stack_m1_tm1(g5(x), 195.5)
            x += 3.0

    # --- enables to the cores (Metal4 column up, Metal3 across, Via2 on the core's M2 pin) ---------------------------
    CORE_PINS = [  # (net column, core x0, core y0, width, pin y)
        ("en0", OAX, OAY, 40.51, 34.125), ("en0_b", OAX, OAY, 40.51, 29.695),
        ("en1", BGX, BGY, 47.55, 49.135), ("en1_b", BGX, BGY, 47.55, 25.375)]
    for n, cx, cy, w, py in CORE_PINS:
        y = g5(cy + py)
        xe = cx + w
        m4v(col[n], y_ctl_top, y)
        v3(col[n], y)
        m3h(y, col[n], xe + 0.45)
        v2_on_m2pin(g5(xe + 0.45), y, xe - 0.4, xe + 0.65)
    # iout -> xgate in
    I_OUT = [("i_oa", OAX + 40.51, OAY + 31.77, XG0, 88.0), ("i_bg", BGX + 47.55, BGY + 36.715, XG1, 145.5)]
    for n, xe, yp, (gx, gy), xv in I_OUT:
        yp = g5(yp)
        v2_on_m2pin(g5(xe + 0.45), yp, xe - 0.4, xe + 0.65)
        m3h(yp, xe + 0.45, xv)
        v3(xv, yp)
        yin = g5(gy + XP["in"][0])
        m4v(xv, yp, yin)
        v3(xv, yin)
        m3h(yin, gx + 3.04, xv)
        v2_on_m2pin(g5(gx + 3.04), yin, gx + XP["in"][1], gx + XP["in"][2], pad=False)
    # xgate controls and supplies: Metal3 left to the tp_en_ctrl columns
    for (gx, gy), ena, enb in ((XG0, "en2", "en2_b"), (XG1, "en3", "en3_b")):
        for pin, net in (("vdd", "vdd_3v3"), ("vss", "vss_3v3"), ("ena", ena), ("ena_b", enb)):
            yy, x0, x1 = XP[pin]
            y = g5(gy + yy)
            xp = g5(gx + 3.04)
            v2_on_m2pin(xp, y, gx + x0, gx + x1, pad=False)
            m3h(y, col[net], xp)
            v3(col[net], y)
            if net in ("en2", "en2_b", "en3", "en3_b"):
                m4v(col[net], y_ctl_top, y)
    # xgate out -> analog_bus0 / analog_bus1
    gx, gy = XG0
    xo = g5(gx + 8.055)
    v2_on_m2pin(xo, BUS0, gx + XP["out"][1], gx + XP["out"][2], pad=False)
    box(TOP, "M3", 1.0, BUS0 - 0.15, xo + 0.15, BUS0 + 0.15)
    gx, gy = XG1
    xo = g5(gx + 8.055)
    yo = g5(gy + XP["out"][0])
    v2_on_m2pin(xo, yo, gx + XP["out"][1], gx + XP["out"][2], pad=False)
    xj = g5(gx + 10.0)
    m3h(yo, xo, xj)
    v3(xj, yo)
    m4v(xj, yo, BUS1)
    v3(xj, BUS1)
    box(TOP, "M3", 1.0, BUS1 - 0.15, xj + 0.15, BUS1 + 0.15)

    if '--stage-b' in sys.argv:
        stage_b(col, xg, XP)

    # --- the PDK ptap1 PCell carries a text "sub!" (layer 40/0); magic makes a name ending in "!" a GLOBAL net, which
    # in the harness could join this tie (vss_3v3) to every other "sub!" of the chip. The tie is vss_3v3 by its metal.
    li40 = ly.find_layer(40, 0)
    if li40 is not None:
        for c in ly.each_cell():
            for sh in list(c.shapes(li40).each()):
                if sh.is_text() and sh.text_string.endswith("!"):
                    c.shapes(li40).erase(sh)
    # --- sub-cell names: prefix slot7_ ------------------------------------------------------------------------------
    for c in ly.each_cell():
        if c.cell_index() != TOP.cell_index() and not c.name.startswith("slot7_"):
            c.name = "slot7_" + c.name.replace("$", "_")
    for c in list(ly.top_cells()):
        if c.cell_index() != TOP.cell_index():
            ly.delete_cell_rec(c.cell_index())
    # sanity: nothing of the platform at x >= 520
    plat = pya.Region()
    for inst in TOP.each_inst():
        plat.insert(inst.bbox())
    assert plat.bbox().right * ly.dbu < 520.0, plat.bbox()
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    ly.write(out, opt)
    print(f"wrote {out}; instances bbox {plat.bbox().to_dtype(ly.dbu)}; tp_en_ctrl top edge {y_ctl_top}")


if __name__ == "__main__":
    main()
