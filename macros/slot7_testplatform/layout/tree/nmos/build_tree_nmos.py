# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""tree_nmos: the NMOS half of bias_tree_noab_pd (slot 7, IHP sg13cmos5l, hv devices), compact and matched.

Written 2026-11-07 by claude for Christoph Maier, after the OA / BG core primitives of 2026-10-28
(agent A3): rotated fingers (W along x, L along y), one row, one gate-poly plate per gate net, end dummies, one
p+ tie strip along the bottom (no ring, no NWell), drain tracks on Metal2 above the row, pins on the top edge.

Run (design repo root or anywhere; PDK_ROOT / PDK default to /foss/pdks, ihp-sg13cmos5l):
    python3 build_tree_nmos.py [out.gds]          -> tree_nmos.gds (default: next to this script)
It also writes tree_nmos.spice (devices as drawn, one line per finger). Rerunning gives the same bytes.

Row, left to right ("score"; one letter per finger of W = 1.2 um, L = 6 um unless noted):
    s | d A B C B A B A B A C A B d | N N N N N | c
    s = TDN + TGN as one two-gate Activ stack (1/0.45 each: vss | en_3v3_b | ni | en_3v3 | iref, bottom to top)
    d = MDBN (vss ni vss), A = NI (ni ni vss), B = NBP (vbp ni vss), C = NBPC (vbpc ni vss)   -- one poly plate on ni
    N = BN (vbn vbn vss), one poly plate on vbn;  c = BNC (vbnc vbnc vss) 1/8, its own plate
"""
import os
import sys

pdk = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "ihp-sg13cmos5l"))
sys.path += [pdk + "/libs.tech/klayout/python",
             pdk + "/libs.tech/klayout/python/pycell4klayout-api/source/python"]
import pya                               # noqa: E402
import sg13cmos5l_pycell_lib             # noqa: E402,F401  registers PCell library SG13_dev

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = "tree_nmos"

# ---------------------------------------------------------------------------------------------------------------
# floorplan parameters (um). Rule values from sg13cmos5l_tech_default.json (key in brackets).
PATTERN = "dABCBABABACABd"        # the ni plate: d = MDBN half, A = NI, B = NBP, C = NBPC (one finger 1.2/6 each)
NBN = 5                           # BN fingers 1.2/6 (6/6 total)
WU, LU = 1.2, 6.0                 # unit finger
PITCH = WU + 0.25                 # Gat.b1 0.25 [Gat_b1]: gates of neighbouring fingers (Act.b 0.21 is then met)
LACT = LU + 0.68                  # Activ length of a finger: 0.34 S/D on each side (PCell)
PLATE_GAP = 0.54                  # Activ gap between two plates: 0.18 end cap + Gat.b 0.18 [Gat_b] + 0.18 end cap
GC_CNT = (0.20, 0.36)             # gate-contact column: contact 0.20..0.36 from the plate's Activ edge
                                  #   (Cnt.e 0.14 [Cnt_e] would allow 0.14; 0.20 keeps M1.b 0.18 [M1_b] to the
                                  #    finger's S/D Metal1, which starts at the Activ edge)
GC_POLY = 0.43                    # poly extension for it: contact + Cnt.d 0.07 [Cnt_d]
GC_M1 = (0.20, 0.46)              # Metal1 of the column (contact enclosure 0 on the sides, M1.c 0.0 [M1_c])
CPITCH = 0.34                     # Cont 0.16 [Cnt_a] + Cnt.b 0.18 [Cnt_b]
TIE = (-0.51, -0.21)              # p+ tie Activ: Act.b 0.21 [Act_b] below the row, 0.30 tall (one contact row)
PSD_ENC = 0.03                    # pSD.c1 0.03 [pSD_c1]; pSD then 0.18 from N+ Activ = pSD.d 0.18 [pSD_d]
TGO_X, TGO_Y = 0.52, 0.27         # ThickGateOx beyond Activ: TGO.c 0.34 [TGO_c] over the gate (W side, PCell uses
                                  #   0.52), TGO.a 0.27 [TGO_a] (L side)
VSS_PLATE_TOP = 0.23              # Metal1 vss plate: tie contacts and every source strip (S strips at 0.07..0.23)
COL_BOT = 0.45                    # gate columns start 0.22 above the plate: M1.e 0.22 [M1_e] (plate is wide)
PAD = (LACT - 0.28, LACT - 0.02)  # Metal1 drain pad over the top S/D strip (strip 6.45..6.61), 0.26 tall
TRK_W, TRK_P = 0.26, 0.47         # Metal2 tracks: 0.26 wide (Via1 0.19 [V1_a] + Mn.c 0.005 [Mn_c]), space 0.21 [Mn_b]
STUB = 0.26                       # Metal1 stub width (Via1 + V1.c 0.01 [V1_c]; V1.c1 0.05 [V1_c1] along the stub)
V1 = 0.19
# drain tracks above the row: track 1 lies over the drain pads, tracks 2, 3 above it
TRACK_NET = {"B": 0, "A": 1, "C": 2}           # vbp on track 1 (pads), ni on track 2, vbpc on track 3
NET = {"A": "ni", "B": "vbp", "C": "vbpc", "d": "vss"}
PIN_SLOT = {"vbp": 6, "vbpc": 3}               # finger index (in PATTERN) whose stub carries the top-edge pin

LAY = {"Activ": (1, 0), "GatPoly": (5, 0), "Cont": (6, 0), "M1": (8, 0), "M1pin": (8, 2), "M1txt": (8, 25),
       "Via1": (19, 0), "M2": (10, 0), "M2pin": (10, 2), "M2txt": (10, 25), "pSD": (14, 0), "TGO": (44, 0),
       "TEXT": (63, 0)}

ly = pya.Layout()
ly.dbu = 0.001
ly.technology_name = "sg13cmos5l"
LI = {k: ly.layer(*v) for k, v in LAY.items()}


def g5(v):
    return round(v / 0.005) * 0.005


def box(c, lay, x0, y0, x1, y1):
    c.shapes(LI[lay]).insert(pya.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


def via1(c, xc, yc):
    box(c, "Via1", xc - V1 / 2, yc - V1 / 2, xc + V1 / 2, yc + V1 / 2)


PINS = []


def pin(c, metal, net, x0, y0, x1, y1):
    box(c, metal + "pin", x0, y0, x1, y1)
    c.shapes(LI[metal + "txt"]).insert(pya.DText(net, g5((x0 + x1) / 2), g5((y0 + y1) / 2)))
    PINS.append((net, metal, g5(x0), g5(y0), g5(x1), g5(y1)))


def note(c, text, x, y):
    c.shapes(LI["TEXT"]).insert(pya.DText(text, g5(x), g5(y)))


_dev = {}


def device(name, **par):
    """Static copy (cell `tree_nmos_<name>`) of an SG13_dev nmosHV PCell variant."""
    if name not in _dev:
        proxy = ly.create_cell("nmosHV", "SG13_dev", par)
        assert proxy is not None, par
        st = ly.create_cell("tree_nmos_" + name)
        st.copy_tree(proxy)
        ly.delete_cell(proxy.cell_index())
        _dev[name] = st
    return _dev[name]


def place(top, cell, x, y):
    """Rotated placement (M45: PCell x = L -> y, PCell y = W -> x); (x, y) = Activ lower left."""
    top.insert(pya.DCellInstArray(cell.cell_index(), pya.DTrans(pya.DTrans.M45, pya.DVector(g5(x), g5(y)))))


def gate_column(top, side, xa, y0, y1, ycon1):
    """Poly extension + contact column + Metal1 column beside a plate whose Activ edge is at xa.
    side = -1: column left of xa, +1: right. Contacts from COL_BOT + 0.05 up to ycon1. Returns the M1 x range."""
    s = side
    box(top, "GatPoly", xa + s * 0.18, y0, xa + s * GC_POLY, y1)
    cx0, cx1 = sorted((xa + s * GC_CNT[0], xa + s * GC_CNT[1]))
    y = COL_BOT + 0.05
    while y + 0.16 <= ycon1 + 1e-9:
        box(top, "Cont", cx0, y, cx1, y + 0.16)
        y += CPITCH
    mx0, mx1 = sorted((xa + s * GC_M1[0], xa + s * GC_M1[1]))
    return mx0, mx1


def build():
    top = ly.create_cell(TOP)
    unit = device("nmosHV_w1p2_l6", w="1.2u", l="6u", ng="1")
    bnc = device("nmosHV_w1_l8", w="1u", l="8u", ng="1")
    stack = device("nmosHV_w2_l0p45_ng2", w="2u", l="0.45u", ng="2")     # 2 fingers 1/0.45, gates kept separate

    lines = []          # CDL lines, one per finger
    # ---------------------------------------------------------------- the ni plate: d A B C ... d
    xs = [i * PITCH for i in range(len(PATTERN))]
    for i, (x, ch) in enumerate(zip(xs, PATTERN)):
        place(top, unit, x, 0.0)
        note(top, ch, x + WU / 2, LACT / 2)
        dn = NET[ch]
        nm = {"d": "MDBN", "A": "NI", "B": "NBP", "C": "NBPC"}[ch]
        lines.append(f"X{nm}_f{i} {dn} ni vss vss sg13_hv_nmos w=1.2u l=6u ng=1")
    x_ni0, x_ni1 = xs[0], xs[-1] + WU
    # ---------------------------------------------------------------- BN plate
    xb = [x_ni1 + PLATE_GAP + j * PITCH for j in range(NBN)]
    for j, x in enumerate(xb):
        place(top, unit, x, 0.0)
        note(top, "N", x + WU / 2, LACT / 2)
        lines.append(f"XBN_f{j} vbn vbn vss vss sg13_hv_nmos w=1.2u l=6u ng=1")
    x_bn1 = xb[-1] + WU
    # ---------------------------------------------------------------- BNC (1/8)
    x_c = x_bn1 + GC_POLY + 0.18 + 0.18          # vbn contact column, Gat.b 0.18, BNC end cap 0.18
    place(top, bnc, x_c, 0.0)
    note(top, "c", x_c + 0.5, 4.34)
    lines.append("XBNC vbnc vbnc vss vss sg13_hv_nmos w=1u l=8u ng=1")
    x_c1 = x_c + 1.0
    lact_c = 8.0 + 0.68
    # ---------------------------------------------------------------- TDN / TGN stack (left)
    x_s1 = x_ni0 - GC_POLY - 0.18 - 0.18          # stack Activ right edge: ni column, Gat.b, stack end cap
    x_s0 = x_s1 - 1.0
    place(top, stack, x_s0, 0.0)
    note(top, "s", x_s0 + 0.5, 1.0)
    lines.append("XTDN ni en_3v3_b vss vss sg13_hv_nmos w=1u l=0.45u ng=1")
    lines.append("XTGN iref en_3v3 ni vss sg13_hv_nmos w=1u l=0.45u ng=1")
    # stack: Activ y 0..1.96; gates 0.34..0.79 (TDN, en_3v3_b), 1.17..1.62 (TGN, en_3v3); strips 0.07 / 0.90 / 1.73

    # ---------------------------------------------------------------- outline
    X0 = x_s0 - TGO_X
    X1 = x_c1 + TGO_X
    Y0 = TIE[0] - TGO_Y
    Y1 = lact_c + TGO_Y
    box(top, "TGO", X0, Y0, X1, Y1)

    # ---------------------------------------------------------------- p+ tie + vss plate (bottom)
    tx0, tx1 = x_s0, x_c1
    box(top, "Activ", tx0, TIE[0], tx1, TIE[1])
    box(top, "pSD", tx0 - PSD_ENC, TIE[0] - PSD_ENC, tx1 + PSD_ENC, TIE[1] + PSD_ENC)
    n = int((tx1 - tx0 - 0.16 - 0.14) / CPITCH) + 1
    cx = tx0 + ((tx1 - tx0) - ((n - 1) * CPITCH + 0.16)) / 2
    for k in range(n):
        box(top, "Cont", cx + k * CPITCH, TIE[0] + 0.07, cx + k * CPITCH + 0.16, TIE[1] - 0.07)
    box(top, "M1", X0, Y0, X1, VSS_PLATE_TOP)
    pin(top, "M1", "vss", X0, Y0, X0 + 1.0, Y0 + 0.3)

    # ---------------------------------------------------------------- gate columns
    # ni: left of the left dummy
    m_ni = gate_column(top, -1, x_ni0, 0.34, LU + 0.34, LU + 0.34 - 0.07)
    box(top, "M1", m_ni[0], COL_BOT, m_ni[1], Y1)
    pin(top, "M1", "ni", m_ni[0], Y1 - 0.29, m_ni[1], Y1)
    # vbn: right of BN
    m_bn = gate_column(top, +1, x_bn1, 0.34, LU + 0.34, LU + 0.34 - 0.07)
    box(top, "M1", m_bn[0], COL_BOT, m_bn[1], Y1)
    pin(top, "M1", "vbn", m_bn[0], Y1 - 0.29, m_bn[1], Y1)
    # vbnc: right of BNC
    m_c = gate_column(top, +1, x_c1, 0.34, 8.34, 8.34 - 0.07)
    box(top, "M1", m_c[0], COL_BOT, m_c[1], lact_c - 0.02)

    # ---------------------------------------------------------------- drain pads, tracks, stubs (ni plate)
    ytrk = [PAD[0] + k * TRK_P for k in range(3)]          # bottom edges of tracks 1..3
    yc = [y + TRK_W / 2 for y in ytrk]
    span = {0: [], 1: [], 2: []}
    for i, (x, ch) in enumerate(zip(xs, PATTERN)):
        xc = x + WU / 2
        box(top, "M1", x, PAD[0], x + WU, PAD[1])            # pad over the top strip
        if ch == "d":                                        # dummy drain -> vss: Metal2 strap over the dummy
            via1(top, xc, (PAD[0] + PAD[1]) / 2)
            via1(top, xc, 0.0)
            box(top, "M2", xc - 0.145, -0.15, xc + 0.145, PAD[1] - 0.015)
            continue
        t = TRACK_NET[ch]
        span[t].append(xc)
        if t == 0:
            via1(top, xc, yc[0])
            ytop = yc[0]
        else:
            via1(top, xc, yc[t])
            ytop = yc[t] + V1 / 2 + 0.05
        if NET[ch] in PIN_SLOT and PIN_SLOT[NET[ch]] == i:
            ytop = Y1
            pin(top, "M1", NET[ch], xc - STUB / 2, Y1 - 0.29, xc + STUB / 2, Y1)
        if ytop > PAD[1]:
            box(top, "M1", xc - STUB / 2, PAD[0], xc + STUB / 2, ytop)
    # ni track also lands on the ni gate column
    span[1].append((m_ni[0] + m_ni[1]) / 2)
    via1(top, (m_ni[0] + m_ni[1]) / 2, yc[1])
    for t, xl in span.items():
        box(top, "M2", min(xl) - V1 / 2 - 0.05, ytrk[t], max(xl) + V1 / 2 + 0.05, ytrk[t] + TRK_W)

    # ---------------------------------------------------------------- BN drains: Metal1 bar into the vbn column
    box(top, "M1", xb[0], PAD[0], m_bn[1], PAD[1])
    # ---------------------------------------------------------------- BNC drain pad into the vbnc column, pin
    box(top, "M1", x_c, lact_c - 0.28, m_c[1], Y1)
    pin(top, "M1", "vbnc", x_c, Y1 - 0.29, m_c[1], Y1)

    # ---------------------------------------------------------------- stack wiring
    # gate contacts left of the stack Activ (x_s0): Cnt.e 0.14 [Cnt_e] -> 0.20 used
    for (g0, g1) in ((0.34, 0.79), (1.17, 1.62)):
        box(top, "GatPoly", x_s0 - GC_POLY, g0, x_s0 - 0.18, g1)
        ym = (g0 + g1) / 2
        box(top, "Cont", x_s0 - GC_CNT[1], ym - 0.08, x_s0 - GC_CNT[0], ym + 0.08)
    # en_3v3_b (TDN gate, lower): Metal1 pad, Via1, Metal2 riser to the top edge
    xe = x_s0 - 0.34
    ym = (0.34 + 0.79) / 2
    box(top, "M1", x_s0 - 0.48, ym - 0.145, x_s0 - GC_CNT[0], ym + 0.18)
    via1(top, xe, ym + 0.02)
    box(top, "M2", xe - 0.14, ym + 0.02 - 0.145, xe + 0.14, Y1)
    pin(top, "M2", "en_3v3_b", xe - 0.14, Y1 - 0.29, xe + 0.14, Y1)
    # en_3v3 (TGN gate, upper): Metal1 riser to the top edge
    ym = (1.17 + 1.62) / 2
    box(top, "M1", x_s0 - GC_M1[1], ym - 0.13, x_s0 - GC_M1[0], Y1)
    pin(top, "M1", "en_3v3", x_s0 - GC_M1[1], Y1 - 0.29, x_s0 - GC_M1[0], Y1)
    # ni (middle strip 0.90..1.06): Metal1 bar into the ni gate column
    box(top, "M1", x_s0, 0.85, m_ni[1], 1.11)
    # iref (top strip 1.73..1.89): Metal1 pad, Via1, Metal2 riser to the top edge
    box(top, "M1", x_s0, 1.665, x_s1, 1.955)
    xi = x_s0 + 0.5
    via1(top, xi, 1.81)
    box(top, "M2", xi - 0.14, 1.665, xi + 0.14, Y1)
    pin(top, "M2", "iref", xi - 0.14, Y1 - 0.29, xi + 0.14, Y1)

    # ---------------------------------------------------------------- matching check of the ni plate
    pos = {ch: [i for i, c in enumerate(PATTERN) if c == ch] for ch in "ABCd"}
    cen = {ch: sum(xs[i] + WU / 2 for i in p) / len(p) for ch, p in pos.items()}
    return top, lines, (X0, Y0, X1, Y1), cen, pos


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "tree_nmos.gds")
    top, lines, bb, cen, pos = build()
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(out, opt)
    ports = "vss ni iref vbp vbpc vbn vbnc en_3v3 en_3v3_b"
    sp = os.path.splitext(out)[0] + ".spice"
    with open(sp, "w") as f:
        f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n")
        f.write("* tree_nmos: NMOS half of bias_tree_noab_pd (+ bias_diodes BN, BNC) as drawn in tree_nmos.gds,\n")
        f.write("* one line per finger; generated by build_tree_nmos.py. Parallel fingers sum to the source W:\n")
        f.write("* NI 5 x 1.2 = 6u, NBP 5 x 1.2 = 6u, NBPC 2 x 1.2 = 2.4u, MDBN 2 x 1.2 = 2.4u, BN 5 x 1.2 = 6u.\n")
        f.write(f".subckt {TOP} {ports}\n")
        f.write("\n".join(lines) + "\n.ends " + TOP + "\n")
    X0, Y0, X1, Y1 = bb
    print(f"wrote {out} and {sp}")
    print(f"bbox x {X0:.3f}..{X1:.3f} y {Y0:.3f}..{Y1:.3f} = {X1 - X0:.3f} x {Y1 - Y0:.3f} = {(X1 - X0) * (Y1 - Y0):.1f} um2")
    print("pattern", PATTERN, "centroids (x, um):", {k: round(v, 4) for k, v in cen.items()})
    for p in PINS:
        print("pin %-9s %s (%.3f, %.3f; %.3f, %.3f)" % p)


if __name__ == "__main__":
    main()
