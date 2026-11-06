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
