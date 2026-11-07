# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""bias_tree_noab_pd: the slot-7 bias tree assembled from its two verified halves (IHP sg13cmos5l, hv devices).

2026-11-07, claude, in the role of A2 (oa_core_pd / bg_core_pd assembly, 2026-10-28).
Circuit (source of truth, not edited): macros/bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice
(+ bias_diodes in macros/bias_tree_pd/netlist/source/bias_ref_pd.spice).

Halves (instantiated unchanged, read from their GDS):
  ../pmos/tree_pmos.gds  20.985 x 8.430  vdd plate + N tie on top, signal pins Metal1 on its bottom edge
  ../nmos/tree_nmos.gds  32.210 x 9.730  vss plate + p+ tie at the bottom, signal pins on its top edge

Floorplan (score, top to bottom; P = prime, no mirror):

    rail vdd  M1 1.36 (= tree_pmos's vdd plate, extended over the full width)
    [ tree_pmos  P  dx = +0.405 ][ fan-out: M1 risers + M2 pin stubs -> right edge ]
    channel 0.52 (3 M2 tracks above the NMOS edge, 2 of them inside tree_pmos's bottom margin)
    [ tree_nmos  P  (3 M2 tracks inside its top margin)                           ]
    rail vss  M1 1.01 (= tree_nmos's vss plate)

The PMOS x offset puts its ni pin over the NMOS ni pin (one straight Metal1 bridge) and its iref pin over the
NMOS iref riser (one Via1). Every other joining net is one Metal2 track (horizontal) with Metal1 drops
(vertical); the six tracks end in the fan-out bay right of tree_pmos, where Metal1 risers lift them to the
Metal2 pin stubs on the right edge. Metal1 / Metal2 only.

Usage: python3 build_tree.py [out.gds]      (default: bias_tree_noab_pd.gds next to this script)
Rule values: libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json, key in the comment.
"""
import os
import sys

import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = "bias_tree_noab_pd"
PMOS_GDS = os.path.join(HERE, "..", "pmos", "tree_pmos.gds")
NMOS_GDS = os.path.join(HERE, "..", "nmos", "tree_nmos.gds")

# ---------------------------------------------------------------- rules (json key)
V1_A = 0.19       # V1_a   Via1 size
V1_C1 = 0.05      # V1_c1  Metal1 enclosure of Via1 on two opposite sides (V1_c 0.01 on the others)
M2_C1 = 0.05      # Mn_c1  Metal2 enclosure of Via1 on two opposite sides (Mn_c 0.005 on the others)
MN_A = 0.20       # Mn_a   Metal2 width: router tracks
MN_B = 0.21       # Mn_b   Metal2 space: track pitch 0.41
M1_B = 0.18       # M1_b   Metal1 space
M1_E = 0.22       # M1_e   Metal1 space to wide (> 0.30) Metal1 (the vdd rail)
NW_D1 = 0.62      # NW_d1  NWell space to N+Activ in ThickGateOx (tree_nmos's row tops out at y 6.68)
TGO_E = 0.86      # TGO_e  ThickGateOx space: the 0.52 gap between the halves is filled
RISER = 0.26      # Metal1 riser width: Via1 + 2 x 0.035 (>= V1_c 0.01)
PIN_W = 0.29      # Metal2 pin stub height, as oa_core_pd / bg_core_pd (Via2 0.19 + 2 x 0.05)
PIN_L = 0.43      # pin shape length at the right edge, as oa_core_pd / bg_core_pd
PIN_GAP = 0.60    # space between pin stubs (brief: >= 0.6, the top level lands Via2 on them)

# ---------------------------------------------------------------- placement, in tree_nmos's own frame (um)
N_BOX = (-2.31, -0.78, 29.90, 8.95)       # tree_nmos bbox
P_W, P_H = 20.985, 8.43                    # tree_pmos bbox (0, 0; P_W, P_H)
PDX = -1.905      # tree_pmos x: its ni pin (0.21 wide) lies inside the NMOS ni stub (-0.46..-0.20), its vbn
                  #   pin 0.18 (M1_b) right of that stub, its iref pin over the NMOS iref riser
PDY = 9.47        # tree_pmos y: the top channel track (9.98..10.18) ends 0.21 (Mn_b) below its first Metal2
                  #   lane (PMOS y 0.92); NWell 2.79 above the NMOS row's N+ (>= NW_d1 0.62)
OX, OY = 2.31, 0.78                        # final shift: cell origin at its lower-left corner
X0, X1 = N_BOX[0], N_BOX[2]                # cell edges (frame of tree_nmos)
Y0, Y1 = N_BOX[1], PDY + P_H

# Metal2 tracks: (net, y bottom). The three below 8.95 sit in tree_nmos's free top margin (its Metal2 ends at 7.60);
# the three above must clear the NMOS iref riser / pad top 8.95 (en_3v3_b and vbpc start left of it).
TRK = {"iref": 7.81, "vbn": 8.22, "vbp": 8.63, "en_3v3_b": 9.16, "vbpc": 9.57, "en_3v3": 9.98}
# fan-out risers right of tree_pmos (x centre) and the pin stub centres on the right edge (y)
RISE_X = {"iref": 25.90, "vbp": 26.40, "en_3v3_b": 26.90, "vbpc": 27.40, "vbn": 27.92, "vbnc": 28.53}
PIN_Y = {"en_3v3": 10.08, "vbnc": 11.31, "vbn": 12.21, "vbp": 13.11, "vbpc": 14.01, "iref": 14.91,
         "en_3v3_b": 15.81}

LAY = {"M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25), "Via1": (19, 0), "M2": (10, 0), "M2pin": (10, 2),
       "M2txt": (10, 25), "TGO": (44, 0)}


def g5(v):
    return round(round(v / 0.005) * 0.005, 3)


class Top:
    def __init__(self, ly, cell):
        self.ly, self.cell = ly, cell
        self.li = {k: ly.layer(*v) for k, v in LAY.items()}
        self.wire = {}                        # net -> {layer: drawn length (um)}
        self.vias = {}

    def box(self, lay, x0, y0, x1, y1, net=None):
        b = db.DBox(g5(min(x0, x1) + OX), g5(min(y0, y1) + OY), g5(max(x0, x1) + OX), g5(max(y0, y1) + OY))
        self.cell.shapes(self.li[lay]).insert(b)
        if net and lay in ("M1", "M2"):
            d = self.wire.setdefault(net, {})
            d[lay] = d.get(lay, 0.0) + max(b.width(), b.height())

    def via1(self, net, x, y):
        h = V1_A / 2
        self.box("Via1", x - h, y - h, x + h, y + h)
        self.vias[net] = self.vias.get(net, 0) + 1

    def text(self, lay, s, x, y):
        self.cell.shapes(self.li[lay]).insert(db.DText(s, g5(x + OX), g5(y + OY)))

    # a Metal2 track [xa, xb] at y bottom yb, 0.20 wide; vias on it get the 0.05 endcap from xa / xb
    def track(self, net, xa, xb, yb):
        self.box("M2", xa, yb, xb, yb + MN_A, net)

    # a Metal1 riser of width RISER centred at x, from ya to yb (endcaps over vias are the caller's job)
    def riser(self, net, x, ya, yb, w=RISER):
        self.box("M1", x - w / 2, ya, x + w / 2, yb, net)

    def pin(self, net, y, xa):
        """Metal2 stub from xa to the right edge, centred at y, with the pin shape and its text at the edge."""
        h = PIN_W / 2
        self.box("M2", xa, y - h, X1, y + h, net)
        self.box("M2pin", X1 - PIN_L, y - h, X1, y + h)
        self.text("M2txt", net, X1 - PIN_L / 2, y)


def build(out):
    ly = db.Layout()
    ly.dbu = 0.001
    ly.read(PMOS_GDS)
    ly.read(NMOS_GDS)
    pm, nm = ly.cell("tree_pmos"), ly.cell("tree_nmos")
    assert pm and nm, "halves not found"
    top = ly.create_cell(TOP)
    top.insert(db.DCellInstArray(nm.cell_index(), db.DTrans(OX, OY)))
    top.insert(db.DCellInstArray(pm.cell_index(), db.DTrans(g5(PDX + OX), g5(PDY + OY))))
    T = Top(ly, top)
    h = V1_A / 2
    e = h + V1_C1                     # via half size + endcap = 0.145

    def px(x):                        # tree_pmos x -> frame of tree_nmos
        return PDX + x

    # ---- rails: vdd = tree_pmos's plate (PMOS y 7.07..8.43) over the full width; vss = tree_nmos's plate
    T.box("M1", X0, PDY + 7.07, X1, Y1, "vdd")
    T.box("M1pin", X0, PDY + 7.07, X1, Y1)
    T.text("M1txt", "vdd", (X0 + X1) / 2, (PDY + 7.07 + Y1) / 2)
    T.box("M1pin", X0, -0.78, X1, 0.23)
    T.text("M1txt", "vss", (X0 + X1) / 2, (-0.78 + 0.23) / 2)
    # ---- ThickGateOx: fill the 0.52 gap between the halves (< TGO_e 0.86) over tree_pmos's width
    T.box("TGO", px(0), N_BOX[3], px(P_W), PDY)

    # ---- ni (internal): straight Metal1 bridge, PMOS ni pin (0.21) inside the NMOS ni stub (-0.46..-0.20)
    T.box("M1", px(1.495), N_BOX[3], px(1.705), PDY, "ni")

    # ---- iref: PMOS iref Metal1 down to a Metal2 pad on the NMOS iref riser (-1.43..-1.15, top 8.95)
    xi = px(0.77)                                       # PMOS iref pin centre (-1.135)
    yv = N_BOX[3] - M2_C1 - h                           # via centre 8.805
    T.box("M1", px(0.665), yv - e, px(0.875), PDY, "iref")
    T.box("M2", -1.43, yv - e, xi + e, N_BOX[3], "iref")
    T.via1("iref", xi, yv)
    T.track("iref", -1.43, RISE_X["iref"] + e, TRK["iref"])       # leaves the riser to the right

    # ---- en_3v3_b: NMOS Metal2 riser (-2.27..-1.99) up to its track; PMOS en_3v3_b drops onto it
    T.box("M2", -2.27, N_BOX[3], -1.99, TRK["en_3v3_b"] + MN_A, "en_3v3_b")
    T.track("en_3v3_b", -2.27, RISE_X["en_3v3_b"] + e, TRK["en_3v3_b"])
    yc = TRK["en_3v3_b"] + MN_A / 2
    T.box("M1", px(1.08), yc - e, px(1.29), PDY, "en_3v3_b")
    T.via1("en_3v3_b", px(1.185), yc)

    # ---- en_3v3: NMOS Metal1 stub (under the en_3v3_b riser) up past it to the top track, which runs to the edge
    yc = TRK["en_3v3"] + MN_A / 2
    T.box("M1", -2.25, N_BOX[3], -1.99, yc + e, "en_3v3")
    T.via1("en_3v3", -2.12, yc)
    T.track("en_3v3", -2.12 - e, X1, TRK["en_3v3"])

    # ---- vbpc: PMOS vbpc pin (via inside its existing stub) and NMOS vbpc stub (raised) on one track
    yc = TRK["vbpc"] + MN_A / 2
    T.via1("vbpc", px(0.335), yc)
    T.track("vbpc", px(0.335) - e, RISE_X["vbpc"] + e, TRK["vbpc"])
    T.box("M1", 4.82, N_BOX[3], 5.08, yc + e, "vbpc")
    T.via1("vbpc", 4.95, yc)

    # ---- vbn: PMOS vbn pin dropped onto its track; NMOS vbn stub (27.79..28.05) takes the via in its top part
    yc = TRK["vbn"] + MN_A / 2
    T.box("M1", px(1.885), yc - e, px(2.095), PDY, "vbn")
    T.via1("vbn", px(1.99), yc)
    T.track("vbn", px(1.99) - e, RISE_X["vbn"] + e, TRK["vbn"])
    T.via1("vbn", RISE_X["vbn"], yc)

    # ---- vbp: NMOS vbp stub (via inside it) and tree_pmos's second vbp gate column (20.345..20.555), dropped
    yc = TRK["vbp"] + MN_A / 2
    T.via1("vbp", 9.30, yc)
    T.track("vbp", 9.30 - e, RISE_X["vbp"] + e, TRK["vbp"])
    T.box("M1", px(20.345), yc - e, px(20.555), PDY, "vbp")
    T.via1("vbp", px(20.45), yc)

    # ---- fan-out: Metal1 risers from the track ends up to the pin stubs
    for net in ("iref", "vbp", "en_3v3_b", "vbpc"):
        yc, yp = TRK[net] + MN_A / 2, PIN_Y[net]
        T.riser(net, RISE_X[net], yc - e, yp + e)
        T.via1(net, RISE_X[net], yc)
        T.via1(net, RISE_X[net], yp)
        T.pin(net, yp, RISE_X[net] - e)
    # vbn: the NMOS vbn stub itself rises (same x, same width) to its pin
    T.riser("vbn", RISE_X["vbn"], N_BOX[3], PIN_Y["vbn"] + e)
    T.via1("vbn", RISE_X["vbn"], PIN_Y["vbn"])
    T.pin("vbn", PIN_Y["vbn"], RISE_X["vbn"] - e)
    # vbnc: tree_pmos's vbnc Metal2 lane (PMOS y 1.74..1.94) reaches its right edge; extend it to a riser on the
    #   NMOS vbnc bar (28.38..29.84, top 8.95); the pin continues from there
    yl = PDY + 1.74
    T.box("M2", px(P_W) - 0.05, yl, RISE_X["vbnc"] + e, yl + MN_A, "vbnc")
    T.riser("vbnc", RISE_X["vbnc"], N_BOX[3], PIN_Y["vbnc"] + e, w=0.30)
    T.via1("vbnc", RISE_X["vbnc"], PIN_Y["vbnc"])
    T.pin("vbnc", PIN_Y["vbnc"], RISE_X["vbnc"] - e)
    # en_3v3: its track is the stub; the pin part is widened to PIN_W
    T.pin("en_3v3", PIN_Y["en_3v3"], X1 - 1.0)

    # ---- checks on the floorplan numbers
    ys = sorted(PIN_Y.values())
    assert all(b - a - PIN_W >= PIN_GAP - 1e-9 for a, b in zip(ys, ys[1:])), "pins closer than 0.6"
    assert ys[-1] + e + M1_E <= PDY + 7.07, "pin riser too close to the vdd rail"
    assert TRK["en_3v3"] + MN_A + MN_B <= PDY + 0.92 + 1e-9, "top track too close to tree_pmos's lanes"
    assert PDY - 6.68 >= NW_D1, "NWell too close to the NMOS row"

    opt = db.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(out, opt)
    return T, top


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, TOP + ".gds")
    T, top = build(out)
    bb = top.dbbox()
    print(f"wrote {out}: {TOP} {bb}  {bb.width():.3f} x {bb.height():.3f} = {bb.width() * bb.height():.1f} um2")
    for net in sorted(T.wire):
        print("  %-9s" % net, "  ".join("%s %.2f" % (k, v) for k, v in sorted(T.wire[net].items())),
              " vias %d" % T.vias.get(net, 0))
