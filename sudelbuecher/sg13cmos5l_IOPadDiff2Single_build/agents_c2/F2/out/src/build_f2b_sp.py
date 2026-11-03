# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 (C2, 2026-11-03), stage B (one p+ ring instead of IHP's two, see below): d2s_sp2k_f2, the 2 kOhm secondary stage in front of CMA and of CMB (Christoph:
"CMA and CMB, symmetric with 2kOhm stage"). One cell, placed twice (CMB's copy mirrored).

    python3 build_f2b_sp.py <out.gds> <out.cdl>

Circuit (as IHP's sg13cmos5l_SecondaryProtection, libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl, with the resistor
2 kOhm instead of 587 Ohm): rppd w 1 / l 7.435 um from pad to core (agent K: 1991.6 Ohm), dantenna 0.64 x 3.1 um
core -> substrate (iovss), dpantenna 0.64 x 4.98 um core -> NWell (iovdd).
Layout: IHP's cell (sg13cmos5l_io.gds, sg13cmos5l_SecondaryProtection) redrawn with SG13_dev PCells and its
distances, stretched by 5.435 um (= 7.435 - 2) along the resistor:
  - rppd vertical, pad head at the bottom (Metal2 pad pin to the bottom edge), core head at the top;
  - dantenna beside it, centered on the resistor;
  - ONE p+ ring (iovss, Activ / Metal1 0.34) around both (stage B; IHP draws one ring per device and joins them by a
    narrow Metal2 strap): poly 0.60 and the diode 0.48 from the ring, as IHP. The ring is the guard of the
    pad-connected resistor and the substrate (anode) contact of dantenna; it is also the cell's iovss terminal;
  - dpantenna (turned, along x) above, in an NWell with an n+ ring (iovdd), NWell 0.62 around the ring (as IHP);
  - core: Metal2 from the top resistor head to the dantenna column and the dpantenna row (as IHP's polygon).
"""
import os
import sys

sys.dont_write_bytecode = True
pdk = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), "ihp-sg13cmos5l")
sys.path += [pdk + "/libs.tech/klayout/python", pdk + "/libs.tech/klayout/python/pycell4klayout-api/source/python"]
import pya                              # noqa: E402
import sg13cmos5l_pycell_lib            # noqa: E402,F401

ly = pya.Layout()
ly.dbu = 0.001
ly.technology_name = "sg13cmos5l"
L = {"Activ": (1, 0), "Cont": (6, 0), "M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25), "Via1": (19, 0), "M2": (10, 0),
     "M2pin": (10, 2), "M2txt": (10, 25), "pSD": (14, 0), "NWell": (31, 0), "TEXT": (63, 0)}
LI = {k: ly.layer(*v) for k, v in L.items()}
D = 7.435 - 2.0                          # stretch against IHP's 2 um resistor


def g5(v):
    return round(round(v / 0.005) * 0.005, 4)


def box(c, lay, x0, y0, x1, y1):
    c.shapes(LI[lay]).insert(pya.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


def pin(c, m, net, x0, y0, x1, y1):
    box(c, m + "pin", x0, y0, x1, y1)
    c.shapes(LI[m + "txt"]).insert(pya.DText(net, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))


def pos(a, b, s, p):
    n = max(1, int((b - a - s) / p + 1e-6) + 1)
    return [g5((a + b) / 2 - ((n - 1) * p + s) / 2 + i * p) for i in range(n)]


def conts(c, x0, y0, x1, y1):            # Cnt_a 0.16, pitch 0.36 (Cnt_b 0.18 + margin), Cnt_c 0.07 inside
    for x in pos(x0 + 0.07, x1 - 0.07, 0.16, 0.36):
        for y in pos(y0 + 0.07, y1 - 0.07, 0.16, 0.36):
            box(c, "Cont", x, y, x + 0.16, y + 0.16)


def vias(c, x0, y0, x1, y1):             # V1_a 0.19, pitch 0.41
    for x in pos(x0, x1, 0.19, 0.41):
        for y in pos(y0, y1, 0.19, 0.41):
            box(c, "Via1", x, y, x + 0.19, y + 0.19)


def ring(c, x0, y0, x1, y1, w=0.34, p=True):
    """tie ring (Activ = Metal1, contacts on every leg; p: pSD 0.18 around both edges as IHP's ptap rings)"""
    legs = [(x0, y0, x1, y0 + w), (x0, y1 - w, x1, y1), (x0, y0 + w, x0 + w, y1 - w), (x1 - w, y0 + w, x1, y1 - w)]
    for b in legs:
        box(c, "Activ", *b)
        box(c, "M1", *b)
    for b in legs[:2]:
        conts(c, b[0] + 0.05, b[1], b[2] - 0.05, b[3])
    for b in legs[2:]:
        conts(c, b[0], b[1] + 0.15, b[2], b[3] - 0.15)
    if p:
        for b in legs:
            box(c, "pSD", b[0] - 0.18, b[1] - 0.18, b[2] + 0.18, b[3] + 0.18)


def pcell(c, name, params, t):
    d = pya.Layout.create_cell(ly, name, "SG13_dev", params)
    c.insert(pya.DCellInstArray(d.cell_index(), t))


def sp2k(name):
    c = ly.create_cell(name)
    # resistor: body x 0.94 .. 1.94, y 1.37 .. 1.37 + 7.435 (heads 0.43 beyond, IHP's position)
    pcell(c, "rppd", {"w": "1u", "l": "7.435u", "b": "0"}, pya.DTrans(pya.DVector(0.94, 1.37)))
    yt = 4.74 + D                                          # ring top (IHP 4.74)
    ring(c, 0.0, 0.0, 6.62, yt)                           # one p+ ring around rppd and dantenna
    box(c, "pSD", 0.0, 0.0, 4.80, yt)                     # pSD over the resistor part (IHP: over its ring), 0.36 from
    #                                                       the dantenna's N+ Activ (pSD_d 0.18)
    # dantenna: Activ 5.16 .. 5.80, centered beside the resistor (IHP 0.82 .. 3.92 in 0 .. 4.74)
    yd = g5((yt - 3.1) / 2)
    pcell(c, "dantenna", {"w": "0.64u", "l": "3.1u"}, pya.DTrans(pya.DVector(5.16, yd)))
    box(c, "M1", 5.23, yd + 0.03, 5.73, yd + 3.07)        # M1_c1 0.05 beyond the end contacts (as IHP's cell)
    # NWell part, IHP's y + D: NWell -0.62 .. 7.24 x 5.58 .. 9.1, n+ ring 0 .. 6.62 x 6.2 .. 8.48
    ring(c, 0.0, 6.2 + D, 6.62, 8.48 + D, p=False)
    box(c, "NWell", -0.62, 5.58 + D, 7.24, 9.1 + D)
    # dpantenna turned (along x): Activ 0.82 .. 5.80, y 7.02 .. 7.66 (+ D)
    pcell(c, "dpantenna", {"w": "0.64u", "l": "4.98u"}, pya.DTrans(pya.DTrans.R90, pya.DVector(5.80, 7.02 + D)))
    box(c, "M1", 5.80 - 4.86, 7.09 + D, 5.80 - 0.12, 7.59 + D)  # M1_c1 0.05 beyond the end contacts
    # pad: Metal2 from the bottom resistor head (M1 y 0.94 .. 1.24) to the bottom edge
    vias(c, 1.02, 0.94, 1.86, 1.24)
    box(c, "M2", 1.02, 0.0, 1.86, 1.29)
    pin(c, "M2", "pad", 1.02, 0.0, 1.86, 0.4)
    # core: top head M1 y 8.935 .. 9.235 -> Metal2 bar to the dantenna column and up to the dpantenna row
    yh0, yh1 = 1.37 + 7.435 + 0.13, 1.37 + 7.435 + 0.43
    vias(c, 1.02, yh0, 1.86, yh1)
    box(c, "M2", 1.02, yh0 - 0.05, 5.73, yh1 + 0.05)
    box(c, "M2", 5.23, yd + 0.11, 5.73, yh1 + 0.05)      # over the dantenna Metal1 (PCell 0.07 .. 0.57)
    vias(c, 5.23, yd + 0.11, 5.73, yd + 2.99)
    yp0, yp1 = 7.02 + D + 0.07, 7.02 + D + 0.57           # dpantenna Metal1 (PCell, turned)
    box(c, "M2", 1.02, yh0 - 0.05, 1.86, yp1 + 0.05)
    box(c, "M2", 1.02, yp0 - 0.05, 5.60, yp1 + 0.05)
    vias(c, 1.02, yp0, 5.60, yp1)
    pin(c, "M2", "core", 5.23, yd + 1.0, 5.73, yd + 1.5)
    pin(c, "M1", "iovss", 3.0, 0.0, 6.62, 0.34)               # the ring's bottom leg
    pin(c, "M1", "iovdd", 2.0, 8.14 + D, 4.6, 8.48 + D)
    for t, x, y in (("rppd 2k", 1.44, 5.0), ("dant", 5.48, 5.0), ("dpant", 3.3, 7.34 + D)):
        c.shapes(LI["TEXT"]).insert(pya.DText(t, x, y))
    cdl = [".SUBCKT %s core iovdd iovss pad" % name,
           "R0 pad core iovss rppd w=1u l=7.435u m=1 b=0",
           "D1 iovss core dantenna w=0.64u l=3.1u a=1.984p p=7.48u m=1",
           "D0 core iovdd dpantenna w=0.64u l=4.98u a=3.187p p=11.24u m=1",
           ".ENDS %s" % name]
    return c, cdl


if __name__ == "__main__":
    c, cdl = sp2k("d2s_sp2k_f2")
    opt = pya.SaveLayoutOptions()
    opt.gds2_write_timestamps = False
    ly.write(sys.argv[1], opt)
    open(sys.argv[2], "w").write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: "
                                 "Apache-2.0\n* d2s_sp2k_f2 (build_f2_sp.py, F2, C2 2026-11-03): 2 kOhm secondary stage"
                                 " for CMA / CMB.\n" + "\n".join(cdl) + "\n")
    b = c.dbbox()
    print("%s %.2f x %.2f um, bbox %s" % (c.name, b.width(), b.height(), b))
