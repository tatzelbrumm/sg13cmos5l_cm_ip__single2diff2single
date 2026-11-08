# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""bdp_cells.py: the logic and switch cells of bias_dist_pd (IHP sg13cmos5l), C4, Claude, agent D, 2026-11-07.

Library module, imported by build_bdp.py. Draws into the layout of C3's build_s2d_p3.py (imported as P, unchanged),
with its helpers (box, fill, pin, note, place, mos) and its NMOS twin nmos() below.

Cells (all hv devices 1u / 0.45u, unmodified SG13_dev PCells in their native orientation, gates vertical):
  nand2_hv  PMOS ng=2 (vdd |a| y |b| vdd) over NMOS ng=2 (y |a| n1 |b| vss), gates a / b continuous poly
  inv_hv    PMOS ng=1 (vdd |a| y) over NMOS ng=1 (vss |a| y); abuts nand2_hv on the shared vdd / vss stripe
  tg_hv     TGP (io_a |en_b| io_b) over TGN (io_a |en| io_b), the project's standard 1u / 0.45u pair, one well / tie
  bdp_slice nand2_hv | inv_hv | tg_hv (option B of the README): a = en_3v3, b = en, y = e_b -> inverter -> e;
            e_b reaches TGP's gate by a poly bridge, e reaches TGN's gate by a poly bar (gates contacted with poly)
  bdp_tdn   TDN (ni -> vss, gate en_3v3_b);  bdp_svpd  SVPD (vpd -> vdd, gate en_3v3);  bdp_fill  tie / well filler
Every cell is a full-height piece of one standard-cell row: p+ substrate tie strip (vss) at the bottom, N+ well tie
strip (vdd) at the top, one NWell, en_3v3 Metal1 line under the vss strip (slice-level cells); cells abut at
their boundary boxes (BND) and the strips merge into the row's periphery ties.

Vertical stack (um): en_3v3 line -0.47..-0.18 (M1_b 0.18 to the strip); vss tie 0..0.30 (Cnt_a 0.16 + 2 Cnt_c);
NMOS Activ 0.73..1.73 (pSD_j1 0.40 + pSD_c1 0.03 from the tie); NWell from 2.55; PMOS Activ 3.17..4.17 (NW_c1
0.62); vdd tie 4.60..4.90 (pSD_i1 0.40 + pSD_d1 0.03); NWell to 5.52 (NW_e1 0.62).
Gap 1.73..3.17 (round 2: 0.20 taller than the NW_c1 + NW_d1 minimum, Christoph: "we're not short of area, so move the
pads away from the channels"): every contacted gate pad / bar / bridge reaches >= 0.30 beyond the 0.25 endcap zone
around the Activ (sym_check's N check): TGN / TDN pads and the bar 1.80 (Gat_d)..2.30, L2 contacts 2.04..2.20;
TGP / SVPD pads and the bridge 2.55..3.10 (Gat_d), L1 contacts 2.66..2.82; poly 0.25 apart (Gat_b 0.18).
Rule values: sg13cmos5l_tech_default.json (keys in the comments).
"""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("BDP_P_DIR", os.path.join(HERE, "..", "inputs", "P")))
import build_s2d_p3 as P     # noqa: E402  C3's generator, unchanged
import pya                   # noqa: E402

ly, box, fill, pin, note = P.ly, P.box, P.fill, P.pin, P.note
CDL = {}                     # cell name -> (ports, device lines)

YN, YP = 0.73, 3.17          # NMOS / PMOS Activ bottom (W = 1.0)
TS, TD = (0.0, 0.30), (4.60, 4.90)     # vss / vdd tie strips
NW = (2.55, 5.52)
EN = (-0.47, -0.18)          # en_3v3 Metal1 line
L2, L1 = 2.04, 2.66          # contact bottom edges in the gap
PN, PP = 2.30, 2.55          # top of the lower pads (TGN, TDN, bar), bottom of the upper ones (TGP, SVPD, bridge)
LINE = (L1 - 0.05, L1 + 0.21)          # the e_b Metal1 line at L1
VP = (4.13, 4.42)            # Via1 pads on top of a stripe (0.18 = M1_b below the vdd strip)


def nmos(w, l, ng=1):
    """nmosHV PCell copied flat, as P.mos() does for pmosHV."""
    key = ("n", w, l, ng)
    if key not in P.DEV:
        p = P._pcl.create_cell("nmosHV", "SG13_dev", {"w": "%gu" % w, "l": "%gu" % l, "ng": str(ng)})
        d = ly.create_cell(("nmosHV_w%g_l%g" % (w, l) + ("_ng%d" % ng if ng > 1 else "")).replace(".", "p"))
        for li in P._pcl.layer_indexes():
            i = P._pcl.get_info(li)
            d.shapes(ly.layer(i.layer, i.datatype)).insert(p.begin_shapes_rec(li))

        def bx(lay):
            return sorted((q.bbox().to_dtype(ly.dbu) for q in pya.Region(d.begin_shapes_rec(P.LI[lay])).merged()
                           .each()), key=lambda b: b.left)
        m1 = bx("M1")
        P.DEV[key] = (d, {"act": bx("Activ")[0], "s": m1[0], "d": m1[1], "gate": bx("GatPoly")[0]})
    return key


def dev(c, name, d, g, s, b, typ, w=1, l=0.45):
    CDL.setdefault(c.name, []).append("M%s %s %s %s %s sg13_hv_%s w=%gu l=%gu ng=1 m=1" % (name, d, g, s, b, typ, w, l))


def cont(c, x, y):
    box(c, "Cont", x, y, x + 0.16, y + 0.16)


def via(c, xc, yc):
    box(c, "Via1", xc - 0.095, yc - 0.095, xc + 0.095, yc + 0.095)


def gate_pad(c, xg, y, viapad=False):
    """contact on a 0.45 gate (center xg) at contact bottom y; Metal1 0.26 x 0.26 (M1_c1 0.05 at the ends), or
    0.21 x 0.29 ready for a Via1 (V1_c 0.01, V1_c1 0.05)"""
    cont(c, xg - 0.08, y)                                     # Metal1 0.26 x 0.35 >= M1_d 0.09 um2, Via1-ready
    if viapad:                                                # (V1_c 0.01 / V1_c1 0.05)
        box(c, "M1", xg - 0.13, y - 0.07, xg + 0.13, y + 0.28)
    else:
        box(c, "M1", xg - 0.13, y - 0.10, xg + 0.13, y + 0.25)


def cont_row(c, x0, x1, y):
    """one row of contacts (Cnt_a 0.16, pitch 0.34 = Cnt_b 0.18 exactly) centered in [x0, x1], start rounded once
    to the 5 nm grid so that every gap is exactly 0.18"""
    n = int((x1 - x0 - 0.16) / 0.34 + 1e-6) + 1
    s = P.g5(x0 + (x1 - x0 - (n - 1) * 0.34 - 0.16) / 2)
    for i in range(n):
        cont(c, s + i * 0.34, y)


def strips(c, bl, br, contacts=True, ext=None):
    """the row's tie strips over the boundary [bl, br]: p+ vss strip (pSD_c1 0.03) and N+ vdd strip, Activ and Metal1
    0.30, contacts 0.09 inside the boundary (two abutted cells keep Cnt_b 0.18); LU_d1 / LU_d 6 um without contacts"""
    xa, xb = ext or (bl, br)                                   # strips may run on over a device's own Activ
    for (y0, y1), p in ((TS, True), (TD, False)):
        box(c, "Activ", xa, y0, xb, y1)
        box(c, "M1", xa, y0, xb, y1)
        if p:
            box(c, "pSD", xa - 0.03, y0 - 0.03, xb + 0.03, y1 + 0.03)
        if contacts and br - bl >= 0.34:
            cont_row(c, bl + 0.09, br - 0.09, y0 + 0.07)


def frame(c, bl, br, en_line=False):
    """strips, one NWell (NW_c1 / NW_e1 0.62 beyond every P+ Activ and the vdd strip) and one ThickGateOx (TGO_a
    0.27 beyond every Activ) over the cell; the boundary box on layer TEXT as a note"""
    act = pya.Region(c.begin_shapes_rec(P.LI["Activ"])).bbox().to_dtype(ly.dbu)
    xa, xb = min(act.left, bl), max(act.right, br)
    strips(c, bl, br, ext=(xa, xb))
    box(c, "NWell", xa - 0.62, NW[0], xb + 0.62, NW[1])
    box(c, "TGO", xa - 0.27, TS[0] - 0.27, xb + 0.27, TD[1] + 0.27)
    if en_line:
        box(c, "M1", bl, EN[0], br, EN[1])
    BND[c.name] = (bl, br)


BND = {}


# ---------------------------------------------------------------- gate cells (Metal1 only)
def nand2_hv():
    c = ly.create_cell("nand2_hv")
    P.place(c, P.mos(2, 0.45, 2), pya.DTrans(pya.DVector(0, YP)), "PA PB")
    P.place(c, nmos(2, 0.45, 2), pya.DTrans(pya.DVector(0, YN)), "NA NB")
    dev(c, "PA", "y", "a", "vdd", "vdd", "pmos")
    dev(c, "PB", "y", "b", "vdd", "vdd", "pmos")
    dev(c, "NA", "y", "a", "n1", "vss", "nmos")
    dev(c, "NB", "n1", "b", "vss", "vss", "nmos")
    for xg in (0.34, 1.17):                                   # gates a, b: one poly from NMOS to PMOS
        box(c, "GatPoly", xg, YN + 1.18, xg + 0.45, YP - 0.18)
        gate_pad(c, xg + 0.225, L2, viapad=True)
    box(c, "M1", 0.07, YN + 1.0, 0.23, LINE[1])              # y: NMOS stripe 0 up to L1
    box(c, "M1", 0.07, LINE[0], 1.06, LINE[1])                # L1 line
    box(c, "M1", 0.90, LINE[0], 1.06, YP)                     # PMOS stripe 1 down to L1
    for x in (0.07, 1.73):                                    # vdd stripes up into the vdd strip
        box(c, "M1", x, YP + 1.0, x + 0.16, TD[0])
    box(c, "M1", 1.73, TS[1], 1.89, YN)                       # vss stripe down into the vss strip
    frame(c, -0.105, 1.81)
    pin(c, "M1", "a", 0.435, L2 - 0.07, 0.695, L2 + 0.22)
    pin(c, "M1", "b", 1.265, L2 - 0.07, 1.525, L2 + 0.22)
    pin(c, "M1", "y", 0.30, LINE[0], 0.80, LINE[1])
    pin(c, "M1", "vdd", 0.20, TD[0], 0.70, TD[1])
    pin(c, "M1", "vss", 0.20, TS[0], 0.70, TS[1])
    CDL[c.name] = (["a", "b", "vdd", "vss", "y"], CDL[c.name])
    return c


def inv_hv():
    c = ly.create_cell("inv_hv")
    P.place(c, P.mos(1, 0.45), pya.DTrans(pya.DVector(0, YP)), "P")
    P.place(c, nmos(1, 0.45), pya.DTrans(pya.DVector(0, YN)), "N")
    dev(c, "P", "y", "a", "vdd", "vdd", "pmos")
    dev(c, "N", "y", "a", "vss", "vss", "nmos")
    box(c, "GatPoly", 0.34, YN + 1.18, 0.79, YP - 0.18)
    gate_pad(c, 0.565, L1)                                    # L1: the nand's y line ends here
    box(c, "M1", 0.90, YN + 1.0, 1.06, YP)                    # y: both drain stripes
    box(c, "M1", 0.07, YP + 1.0, 0.23, TD[0])
    box(c, "M1", 0.07, TS[1], 0.23, YN)
    frame(c, 0.15, 1.255)
    pin(c, "M1", "a", 0.435, LINE[0], 0.695, LINE[1])
    pin(c, "M1", "y", 0.90, 2.0, 1.06, 2.5)
    pin(c, "M1", "vdd", 0.40, TD[0], 0.90, TD[1])
    pin(c, "M1", "vss", 0.40, TS[0], 0.90, TS[1])
    CDL[c.name] = (["a", "vdd", "vss", "y"], CDL[c.name])
    return c


def tg_hv():
    c = ly.create_cell("tg_hv")
    P.place(c, P.mos(1, 0.45), pya.DTrans(pya.DVector(0, YP)), "TGP")
    P.place(c, nmos(1, 0.45), pya.DTrans(pya.DVector(0, YN)), "TGN")
    dev(c, "TGP", "io_a", "en_b", "io_b", "vdd", "pmos")
    dev(c, "TGN", "io_a", "en", "io_b", "vss", "nmos")
    box(c, "GatPoly", 0.34, PP, 0.79, YP - 0.18)              # TGP gate down to its pad (0.37 beyond the zone)
    gate_pad(c, 0.565, L1)
    box(c, "GatPoly", 0.34, YN + 1.18, 0.79, PN)              # TGN gate up to its pad (0.32 beyond the zone)
    gate_pad(c, 0.565, L2)
    for x in (0.07, 0.90):                                    # io_a, io_b: both stripes through the gap
        box(c, "M1", x, YN + 1.0, x + 0.16, YP)
    frame(c, -0.125, 1.235)
    pin(c, "M1", "en_b", 0.435, LINE[0], 0.695, LINE[1])
    pin(c, "M1", "en", 0.435, L2 - 0.05, 0.695, L2 + 0.21)
    pin(c, "M1", "io_a", 0.07, 2.0, 0.23, 2.5)
    pin(c, "M1", "io_b", 0.90, 2.0, 1.06, 2.5)
    pin(c, "M1", "vdd", 0.30, TD[0], 0.80, TD[1])
    pin(c, "M1", "vss", 0.30, TS[0], 0.80, TS[1])
    CDL[c.name] = (["en", "en_b", "io_a", "io_b", "vdd", "vss"], CDL[c.name])
    return c


# ---------------------------------------------------------------- slice and single switches (M1 + M2)
XI, XT = 1.66, 3.04          # inv_hv / tg_hv origins in the slice (inv shares the nand's stripe 2 at 1.73)
PITCH = 4.38                 # slice boundary [-0.105, 4.275]


def riser(c, x, net, top=NW[1]):
    """Via1 pad on top of a stripe (x = stripe left edge) and a Metal2 riser to the cell's top edge"""
    box(c, "M1", x - 0.025, VP[0], x + 0.185, VP[1])
    via(c, x + 0.08, (VP[0] + VP[1]) / 2)
    box(c, "M2", x + 0.08 - 0.145, VP[0], x + 0.08 + 0.145, top)
    pin(c, "M2", net, x + 0.08 - 0.145, top - 0.30, x + 0.08 + 0.145, top)


def drop(c, xg, ypad, net=None, on_line=False):
    """Via1 on a gate pad (center xg, pad bottom ypad) and a Metal2 line down to the cell's bottom edge; on_line:
    Via1 onto the en_3v3 line instead of a pin"""
    via(c, xg, ypad + 0.145)
    box(c, "M2", xg - 0.145, EN[0], xg + 0.145, ypad + 0.29)
    if on_line:
        via(c, xg, (EN[0] + EN[1]) / 2)
    else:
        pin(c, "M2", net, xg - 0.145, EN[0], xg + 0.145, EN[0] + 0.30)


def slice_(nd, iv, tg):
    c = ly.create_cell("bdp_slice")
    for cc, x in ((nd, 0.0), (iv, XI), (tg, XT)):
        c.insert(pya.DCellInstArray(cc.cell_index(), pya.DTrans(pya.DVector(x, 0))))
    box(c, "M1", 1.06, LINE[0], XI + 0.435, LINE[1])          # e_b: the nand's L1 line on to the inverter's gate
    box(c, "GatPoly", XI + 0.34, PP, XT + 0.79, YP - 0.07)    # e_b: poly bridge inverter gate -> TGP gate
    box(c, "GatPoly", 2.63, YN + 1.07, XT + 0.79, PN)         # e: poly bar from TGN's gate (Gat_b 0.18 to the
    cont(c, 2.70, L2)                                         #    inverter's gate), contacted beside the e stripe
    box(c, "M1", XI + 0.90, L2 - 0.05, 2.91, L2 + 0.21)
    drop(c, 0.565, L2 - 0.07, on_line=True)                   # a = en_3v3
    drop(c, 1.395, L2 - 0.07, "en")                           # b = en
    riser(c, XT + 0.07, "io_a")
    riser(c, XT + 0.90, "io_b")
    box(c, "M1", -0.105, EN[0], 4.275, EN[1])
    BND[c.name] = (-0.105, 4.275)
    pin(c, "M1", "en_3v3", -0.105, EN[0], 0.395, EN[1])
    pin(c, "M1", "vdd", 2.0, TD[0], 2.5, TD[1])
    pin(c, "M1", "vss", 2.0, TS[0], 2.5, TS[1])
    CDL[c.name] = (["en", "en_3v3", "io_a", "io_b", "vdd", "vss"],
                   ["MPA e_b en_3v3 vdd vdd sg13_hv_pmos w=1u l=0.45u ng=1 m=1",
                    "MPB e_b en vdd vdd sg13_hv_pmos w=1u l=0.45u ng=1 m=1",
                    "MNA e_b en_3v3 n1 vss sg13_hv_nmos w=1u l=0.45u ng=1 m=1",
                    "MNB n1 en vss vss sg13_hv_nmos w=1u l=0.45u ng=1 m=1",
                    "MP e e_b vdd vdd sg13_hv_pmos w=1u l=0.45u ng=1 m=1",
                    "MN e e_b vss vss sg13_hv_nmos w=1u l=0.45u ng=1 m=1",
                    "MTGP io_a e_b io_b vdd sg13_hv_pmos w=1u l=0.45u ng=1 m=1",
                    "MTGN io_a e io_b vss sg13_hv_nmos w=1u l=0.45u ng=1 m=1"])
    return c


def single(name, typ):
    """TDN (n: ni -> vss, gate en_3v3_b, gate to a pin at the bottom edge) or SVPD (p: vpd -> vdd, gate en_3v3,
    onto the en_3v3 line); the switched stripe rises to a Metal2 pin at the top edge."""
    c = ly.create_cell(name)
    if typ == "n":
        P.place(c, nmos(1, 0.45), pya.DTrans(pya.DVector(0, YN)), "TDN")
        dev(c, "TDN", "ni", "en_3v3_b", "vss", "vss", "nmos")
        box(c, "GatPoly", 0.34, YN + 1.18, 0.79, PN)
        gate_pad(c, 0.565, L2, viapad=True)
        drop(c, 0.565, L2 - 0.07, "en_3v3_b")
        box(c, "M1", 0.07, TS[1], 0.23, YN)                   # source down into the vss strip
        box(c, "M1", 0.90, YN + 1.0, 1.06, VP[0])             # drain up to its Via1 pad
        riser(c, 0.90, "ni")
        ports = ["en_3v3", "en_3v3_b", "ni", "vdd", "vss"]
    else:
        P.place(c, P.mos(1, 0.45), pya.DTrans(pya.DVector(0, YP)), "SVPD")
        dev(c, "SVPD", "vpd", "en_3v3", "vdd", "vdd", "pmos")
        box(c, "GatPoly", 0.34, PP, 0.79, YP - 0.18)
        gate_pad(c, 0.565, L1, viapad=True)
        drop(c, 0.565, L1 - 0.07, on_line=True)
        box(c, "M1", 0.07, YP + 1.0, 0.23, TD[0])             # source up into the vdd strip
        riser(c, 0.90, "vpd")
        ports = ["en_3v3", "vdd", "vpd", "vss"]
    frame(c, -0.125, 1.235, en_line=True)
    pin(c, "M1", "en_3v3", -0.125, EN[0], 0.375, EN[1])
    pin(c, "M1", "vdd", 0.30, TD[0], 0.80, TD[1])
    pin(c, "M1", "vss", 0.30, TS[0], 0.80, TS[1])
    CDL[c.name] = (ports, CDL[c.name])
    return c


def filler(name, w):
    """tie strips, NWell, TGO and the en_3v3 line over a gap of width w (no devices)"""
    c = ly.create_cell(name)
    strips(c, 0.0, w)
    box(c, "NWell", -0.62, NW[0], w + 0.62, NW[1])
    box(c, "TGO", -0.27, TS[0] - 0.27, w + 0.27, TD[1] + 0.27)
    box(c, "M1", 0.0, EN[0], w, EN[1])
    BND[c.name] = (0.0, w)
    return c


def cdl_text(cells, title):
    txt = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
           "* %s (Claude, agent D, C4 2026-11-07). hv devices 1u/0.45u; every device as drawn." % title, ""]
    for c in cells:
        ports, lines = CDL[c.name]
        txt += [".SUBCKT %s %s" % (c.name, " ".join(ports))] + lines + [".ENDS %s" % c.name, ""]
    return "\n".join(txt)


def strip_labels(c):
    """remove a cell's own pin shapes and texts once its standalone copy is written: inside a larger cell the
    parent's labels name the nets (as the pad's copy of the tub, rbsrc_tub_p20x1_c3)"""
    for lay in ("M1pin", "M1txt", "M2pin", "M2txt"):
        c.shapes(P.LI[lay]).clear()


def standalone(c, path, cdl):
    """write cell c (and its tree) alone to path with its CDL next to it"""
    l2 = pya.Layout()
    l2.dbu = ly.dbu
    l2.create_cell(c.name).copy_tree(c)
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    l2.write(path, opt)
    open(path[:-4] + ".cdl", "w").write(cdl)
