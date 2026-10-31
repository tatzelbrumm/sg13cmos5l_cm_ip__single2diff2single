# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""d2s_block: the amplifier d2s_mpdda_pd + bias_tree_pd of the pad cell sg13cmos5l_IOPadDiff2Single, assembled bottom up
from P's and N's checked cells (unchanged copies) and F's cells, in absolute pad coordinates (x 0..80, y 84..180).
Agent F, C2 stage 3, 2026-10-31.

    python3 build_block.py <out.gds> <out.cdl> [--place-only]

Layers: cells' own Metal1 / Metal2; routing Metal1 horizontal / Metal2 vertical in channels; Metal3 only in the
ring gaps 119..126 / 134..140 (vfb hop is pad level; vbpc / vabp hops here). Copies of pad-top shapes (a / b joins,
dabp / dabn pin stubs, M3 rails, the frame's p+ ring Metal1) are drawn inside the block only so that the block is
LVS-checkable alone; in the pad they coincide with the pad's own shapes.
Rule values (json): M1_b 0.18, Mn_b 0.21, V1_a 0.19, V1_c1 0.05 (wire 0.29), Vn_a 0.19, NW_b 0.62, NW_b1 1.80,
NW_d1 0.62, NW_f 0.24, Act_b 0.21.
"""
import os
import sys

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Drawer, g5  # noqa: E402

OUT, CDL = sys.argv[1], sys.argv[2]
PLACE_ONLY = "--place-only" in sys.argv
F = "/home/user/c2/F"
SRC = {"P": F + "/inputs_P/d2s_p_cells.gds", "N": F + "/inputs_N/d2s_n_cells.gds",
       "rh": F + "/out/cells/d2s_rhigh.gds", "tr": F + "/out/cells/bias_tree_pd.gds"}
ly = db.Layout()
ly.dbu = 0.001
top = ly.create_cell("d2s_block")
D = Drawer(ly, top)
W, H = 0.29, 0.145


def load(src, name):
    s = db.Layout()
    s.read(src)
    c = ly.create_cell(name)
    c.copy_tree(s.cell(name))
    return c


INST = {}


def place(key, cell, x, y, mirror=False):
    t = db.DTrans(db.DTrans.M90, db.DVector(x, y)) if mirror else db.DTrans(db.DVector(x, y))
    top.insert(db.DCellInstArray(cell.cell_index(), t))
    INST[key] = (cell, t)


def pins(key, net):
    """absolute pin boxes (layer name, DBox) of net on an instance (top-level pin boxes of the cell)"""
    cell, t = INST[key]
    out = []
    for pl, tl, nm in (((8, 2), (8, 25), "M1"), ((10, 2), (10, 25), "M2")):
        lp, lt = ly.find_layer(*pl), ly.find_layer(*tl)
        if lp is None or lt is None:
            continue
        txt = [s.dtext for s in cell.shapes(lt).each() if s.is_text() and s.dtext.string == net]
        for s in cell.shapes(lp).each():
            b = s.dbox
            if any(b.enlarged(0.001, 0.001).contains(db.DPoint(tx.x, tx.y)) for tx in txt):
                out.append((nm, b.transformed(t)))
    assert out, (key, net)
    return out


def pin(key, net, side=None):
    ps = pins(key, net)
    if side:
        f = {"b": lambda b: b.bottom, "t": lambda b: -b.top, "l": lambda b: b.left, "r": lambda b: -b.right}[side]
        ps = sorted(ps, key=lambda p: f(p[1]))
    return ps[0]


# ---------------------------------------------------------------- cells
C = {}
for n in ("d2s_inputs_c", "d2s_tails_c", "d2s_loads_c", "d2s_casc_p_c", "d2s_ab_p_c", "d2s_pd_p_c"):
    C[n] = load(SRC["P"], n)
for n in ("sinks_6x6_c", "d2s_casc_n_c", "d2s_ab_n_c", "d2s_pd_n_c"):
    C[n] = load(SRC["N"], n)
C["d2s_rhigh"] = load(SRC["rh"], "d2s_rhigh")
C["bias_tree_pd"] = load(SRC["tr"], "bias_tree_pd")

Y0 = 89.2                                  # block bottom: b join top 88.0 + room for one Metal2 track (88.25 .. 88.54)
X_IN = 15.6                                # inputs; the tails sit 2.47 right of them (P: same column x)
place("cascp", C["d2s_casc_p_c"], 2.5, Y0)
place("loads", C["d2s_loads_c"], 2.5, Y0 + 33.64 + 1.46)               # gap 1.46: pl / pr / l2 crossover tracks
place("rh", C["d2s_rhigh"], 16.13, Y0 + 1.38)                          # bbox 15.20 .. 29.12 x 89.2 .. 104.61
place("abn", C["d2s_ab_n_c"], 31.0, Y0)
place("abp", C["d2s_ab_p_c"], 38.6, Y0)
place("pdp", C["d2s_pd_p_c"], 45.3, Y0)
place("pdn", C["d2s_pd_n_c"], 49.7, Y0)
place("cascn", C["d2s_casc_n_c"], 67.5, Y0)
place("sinks", C["sinks_6x6_c"], 60.5, Y0 + 33.12)                     # abutted on casc_n: x / y pins meet (N)
Y_TL = 109.0
place("tails", C["d2s_tails_c"], X_IN + 2.47, Y_TL)
Y_IN = Y_TL + 14.81 + 1.80                                             # NW_b1 between the tails' and the tubs' wells
place("inputs", C["d2s_inputs_c"], X_IN, Y_IN)
Y_TR = 154.70                                                          # tree bbox bottom (mirrored M90)
place("tree", C["bias_tree_pd"], 2.6 + 52.36, Y_TR + 0.185, mirror=True)

for k, (c, t) in INST.items():
    print("%-7s %-15s %s" % (k, c.name, c.dbbox().transformed(t)))

# ---------------------------------------------------------------- helpers


def hseg(lay, x0, x1, y, w=W):
    D.box(lay, min(x0, x1) - w / 2, y - w / 2, max(x0, x1) + w / 2, y + w / 2)


def vseg(lay, x, y0, y1, w=W):
    D.box(lay, x - w / 2, min(y0, y1) - w / 2, x + w / 2, max(y0, y1) + w / 2)


def v1(x, y):
    D.via1(x, y)
    D.box("M1", x - H, y - H, x + H, y + H)
    D.box("M2", x - H, y - H, x + H, y + H)


def v2(x, y):
    D.via2(x, y)
    D.box("M2", x - H, y - H, x + H, y + H)
    D.box("M3", x - H, y - H, x + H, y + H)


def cx(b):
    return g5((b.left + b.right) / 2)


def cy(b):
    return g5((b.bottom + b.top) / 2)


def label(lay, net, x, y, w=0.29):
    D.pin(lay, net, x - w / 2, y - w / 2, x + w / 2, y + w / 2)


if not PLACE_ONLY:
    # ------------------------------------------------ copies of the pad top's shapes (block LVS only)
    D.box("M2", 3.2, 86.4, 77.5, 87.0)                     # a join
    D.box("M2", 0.5, 87.4, 79.5, 88.0)                     # b join
    D.box("M2", 38.15, 85.0, 38.45, 86.0)                  # dabn pin stub
    D.box("M2", 38.94, 85.0, 39.55, 86.0)                  # dabp pin stub
    D.box("M1", 0.5, 83.95, 79.5, 84.25)                   # P frame outer p+ ring Metal1 (iovss)
    for y0, y1, net in ((84.0, 91.5, "iovdd"), (93.5, 119.0, "iovdd"), (126.0, 134.0, "iovss")):
        D.box("M3", 0.0, y0, 80.0, y1)
        D.pin("M3", net, 40.0, y0 + 0.5, 40.5, y0 + 1.0) if False else None
    for net, x, y in (("a", 20.0, 86.7), ("b", 20.0, 87.7), ("dabn", 38.3, 85.2), ("dabp", 39.245, 85.2)):
        label("M2", net, x, y)
    label("M1", "iovss", 70.0, 84.1, 0.25)
    for net, y in (("iovdd", 90.5), ("iovdd", 110.0), ("iovss", 130.0)):
        D.box("M3pin", 40.0, y, 40.5, y + 0.5)
        top.shapes(ly.layer(30, 25)).insert(db.DText(net, 40.25, y + 0.25))

    # ------------------------------------------------ casc_p <-> loads: pr / pl / l2 crossover in the 1.46 gap
    yc0 = 89.2 + 33.64
    T1, T2, T3 = g5(yc0 + 0.37), g5(yc0 + 0.84), g5(yc0 + 1.31)
    for net, t in (("l2", T1), ("pl", T2), ("pr", T3)):
        a = pin("cascp", net, "t")[1]
        b = pin("loads", net, "b")[1]
        vseg("M2", cx(a), a.top, t)
        vseg("M2", cx(b), b.bottom, t)
        v1(cx(a), t)
        v1(cx(b), t)
        hseg("M1", cx(a), cx(b), t)
    D.box("NWell", 2.5, yc0, 13.82, yc0 + 1.46)              # one iovdd well: casc_p + loads
    # front-end vdd of loads / casc_p: their left vdd pins joined by Metal1 outside the cells (x 2.36 .. 2.65);
    # one tap at casc_p's pin: Via1, Metal2 pad, Via2 into M3 iovdd (93.5 .. 119)
    pc, pld = pin("cascp", "vdd")[1], pin("loads", "vdd")[1]
    D.box("M1", 2.36, pc.bottom, 2.65, 148.80)
    D.box("M1", 1.60, 148.35, 2.65, 148.65)        # the left iovdd edge stub (n+ 148.35) tied here (no current)
    D.box("M1", 2.36, pc.bottom, pc.right, pc.top)
    D.box("M1", 2.36, pld.bottom, pld.right, pld.top)
    D.box("M1", 2.36, cy(pc) - 0.3, 2.65, cy(pc) + 0.3)
    D.via1(2.56, cy(pc))
    D.box("M2", 2.46, cy(pc) - 0.3, 2.85, cy(pc) + 0.75)          # 0.26 from the vfb line (x .. 2.20)
    D.via2(2.655, cy(pc) + 0.45)
    # ------------------------------------------------ tails tap (single point) and NWell bridges
    tp = pin("tails", "vdd")[1]
    D.via1(cx(tp), cy(tp))
    D.box("M2", tp.left, tp.bottom, tp.right, tp.top)
    D.via2(cx(tp), cy(tp))
    D.box("NWell", 13.82, Y_TL, X_IN + 2.47, 122.84)          # casc_p <-> tails
    D.box("NWell", 17.85, 122.84, 18.47, Y_IN + 0.5)     # tails <-> inputs' left dummy wells (NW_a 0.62)
    D.box("NWell", X_IN + 0.3, Y_IN + 11.9, X_IN + 2.6, Y_IN + 13.85)
    D.box("NWell", X_IN + 29.4, Y_TL + 14.0, X_IN + 31.8, Y_IN + 0.5)   # tails <-> right dummy wells
    D.box("NWell", X_IN + 29.4, Y_IN + 11.9, X_IN + 31.8, Y_IN + 13.85)
    D.box("NWell", 38.6, 97.0, 44.61, Y_TL + 0.2)             # ab_p <-> tails
    D.box("NWell", 44.5, Y0, 45.4, 92.17)                     # ab_p <-> pd_p
    for x0, x1, y1 in ((37.86, 38.6, 94.64), (44.61, 45.3, 92.17), (49.01, 49.7, 91.24)):
        D.box("TGO", x0, Y0, x1, y1)                         # TGO_e 0.86: gaps filled
    # inputs' dummy tubs (vdd) to the tails' vdd strip (Metal1, no current)
    ip = pin("inputs", "vdd")[1]
    D.box("M1", ip.left, 123.0, ip.right, ip.top)
    D.box("M1", ip.left, 123.0, X_IN + 2.47 + 0.30, 123.29)
    D.box("M1", X_IN + 2.47, 122.9, X_IN + 2.47 + 0.30, 123.29)

    # ------------------------------------------------ sa / sb: tails <-> inputs (straight), rhigh <-> tails channel
    nets = ["sb_A", "sa_B", "sa_A", "sa_C2", "sb_B", "sb_C2", "sb_C1", "sa_C1"]   # bottom track first
    for net in nets:
        a = pin("tails", net, "t")[1]
        b = pin("inputs", net, "b")[1]
        D.box("M2", a.left, a.top - 0.1, a.right, b.bottom + 0.1)
    rtop = 89.2 + 15.41
    for k, net in enumerate(nets):
        t = g5(rtop + 0.40 + 0.47 * k)
        r = pin("rh", net, "t")[1]
        s = pin("tails", net, "b")[1]
        vseg("M2", cx(r), r.top, t)
        vseg("M2", cx(s), s.bottom, t)
        v1(cx(r), t)
        v1(cx(s), t)
        hseg("M1", cx(r), cx(s), t)

    # ------------------------------------------------ x / y: inputs (right edge) -> sinks (left edge)
    xi, yi = pin("inputs", "x")[1], pin("inputs", "y")[1]
    xs, ys = pin("sinks", "x", "l")[1], pin("sinks", "y", "l")[1]
    D.box("M2", xi.left, cy(xi) - H, 48.45, cy(xi) + H)       # x: M2 out, Via1, M1 up, M1 east
    v1(48.30, cy(xi))
    vseg("M1", 48.30, cy(xi), cy(xs))
    hseg("M1", 48.30, 60.31, cy(xs))
    v1(60.31, cy(xs))
    hseg("M2", 60.31, xs.left + 0.35, cy(xs))
    D.box("M2", yi.left, cy(yi) - H, 49.15, cy(yi) + H)       # y: M2 out and down, M1 east
    vseg("M2", 49.0, cy(yi), cy(ys))
    v1(49.0, cy(ys))
    hseg("M1", 49.0, 60.31, cy(ys))
    v1(60.31, cy(ys))
    hseg("M2", 60.31, ys.left + 0.35, cy(ys))

    # ------------------------------------------------ sinks single tap (iovss M3), casc_n vss to the right stub
    sp = pin("sinks", "vss")[1]
    D.via1(cx(sp), cy(sp))
    D.box("M2", sp.left, sp.bottom, sp.right, sp.top)
    D.via2(cx(sp), cy(sp))
    cp = pin("cascn", "vss")[1]
    D.box("M1", cp.left, cp.bottom, 79.2, cp.top)
    label("M1", "iovss", 78.95, cy(cp), 0.29)

    # ------------------------------------------------ bottom: a / b drops, dabp / dabn hops, corridor taps
    def a_drop(key):
        p = pin(key, "a", "b")[1]
        D.box("M1", p.left, 86.55, p.right, p.top)
        D.via1(cx(p), 86.7)
    for k in ("cascp", "abn", "abp", "pdp"):
        a_drop(k)

    def b_drop_m2(key):
        p = pin(key, "b", "b")[1]
        D.box("M2", p.left, 87.5, p.right, p.top)
    for k in ("abn", "abp", "cascn"):
        b_drop_m2(k)
    p = pin("pdn", "b", "b")[1]
    D.box("M1", p.left, 87.55, p.right, p.top)
    D.via1(cx(p), 87.7)

    def hop_m1(p, xv, yv=85.55):
        """Metal1 from a bottom pin down to yv, jog to xv, Via1 there"""
        D.box("M1", p.left, yv - H, p.right, p.top)
        hseg("M1", cx(p), xv, yv)
        D.via1(xv, yv)
        D.box("M1", xv - H, yv - H, xv + H, yv + H)
    hop_m1(pin("abn", "dabn", "b")[1], 38.30)
    hop_m1(pin("abp", "dabp", "b")[1], 39.245)

    def tap_ring(p, xv, top_pin=False):
        """iovss tap: Metal1 down to 85.55, Via1, Metal2 down, Via1 onto the frame's p+ ring Metal1 (y 83.92 .. 84.26)"""
        if top_pin:
            return
        hop_m1(p, xv)
        D.box("M2", xv - H, 84.09 - H, xv + H, 85.55 + H)
        D.via1(xv, 84.09)

    def tap_iovdd(p, xv):
        """iovdd tap: Metal1 down to 85.55, Via1, Metal2 pad, Via2 into M3 iovdd (66 .. 91.5)"""
        hop_m1(p, xv)
        D.box("M2", xv - H, 85.55 - H, xv + H, 86.13)
        D.via2(xv, 85.95)
        D.box("M2", xv - H, 85.95 - H, xv + H, 86.13)
    tap_ring(pin("pdn", "vsso", "b")[1], 50.40)
    tap_iovdd(pin("pdp", "vddo", "b")[1], 46.90)
    # ab_n vss (left pin) and pd_n vss (top pin): Metal1 down to the corridor, ring taps
    p = pin("abn", "vss")[1]
    D.box("M1", p.left, 85.40, p.left + 0.29, p.top)
    D.via1(31.155, 85.55)
    D.box("M2", 31.155 - H, 84.09 - H, 31.155 + H, 85.55 + H)
    D.via1(31.155, 84.09)
    p = pin("pdn", "vss", "t")[1]                       # up, over pd_n's vabn pin (right of it), down its right side
    D.box("M1", p.left, p.bottom, p.right, 92.15)
    D.box("M1", p.left, 91.86, 53.55, 92.15)
    D.box("M1", 53.26, 85.40, 53.55, 92.15)
    D.via1(53.405, 85.55)
    D.box("M2", 53.405 - H, 84.09 - H, 53.405 + H, 85.55 + H)
    D.via1(53.405, 84.09)
    # pd_p vdd (top pin) -> iovdd tap between pd_p and pd_n
    p = pin("pdp", "vdd", "t")[1]
    D.box("M1", p.left, p.bottom, p.right, 93.10)
    D.box("M1", p.left, 92.81, 49.54, 93.10)
    D.box("M1", 49.25, 85.40, 49.54, 93.10)
    D.via1(49.395, 85.55)
    D.box("M2", 49.395 - H, 85.55 - H, 49.395 + H, 86.13)
    D.via2(49.395, 85.95)

    # ------------------------------------------------ l2 / l1 / vabp / vabn / en / en_b over the class-AB group
    TL2, TVABP, TL1, TVABN, TEN, TENB = 98.0, 98.5, 99.0, 99.5, 100.0, 100.5
    # l2: casc_p bottom pin -> M1 track y 88.765 east -> M2 riser x 30.3 -> track TL2
    p = pin("cascp", "l2", "b")[1]
    vseg("M2", cx(p), 88.765, p.bottom + 0.2)
    v1(cx(p), 88.765)
    hseg("M1", cx(p), 30.30, 88.765)
    v1(30.30, 88.765)
    vseg("M2", 30.30, 88.765, TL2)
    v1(30.30, TL2)
    for k in ("abn", "abp"):
        q = pin(k, "l2", "t")[1]
        vseg("M2", cx(q), q.top, TL2)
        v1(cx(q), TL2)
    hseg("M1", 30.30, cx(pin("abp", "l2", "t")[1]), TL2)
    # l1: casc_n bottom pin -> M1 y 88.80 west -> M2 riser x 67.0 (beside casc_n, keeping x 54 .. 66.6 x y 89.3 .. 98.6
    # free: CMB-stage reserve) -> track TL1 west
    XL1 = 67.0
    p = pin("cascn", "l1", "b")[1]
    D.box("M2", p.left, 88.655, p.right, p.top)
    v1(cx(p), 88.80)
    hseg("M1", XL1, cx(p), 88.80)
    v1(XL1, 88.80)
    vseg("M2", XL1, 88.80, TL1)
    v1(XL1, TL1)
    xs_l1 = []
    for k in ("abn", "abp"):
        q = pin(k, "l1", "t")[1]
        vseg("M2", cx(q), q.top, TL1)
        v1(cx(q), TL1)
        xs_l1.append(cx(q))
    hseg("M1", min(xs_l1), XL1, TL1)

    # ------------------------------------------------ right channel (Metal2 lines, x 55.3 .. 59.8)
    trp = lambda net: pin("tree", net, "r")[1]
    XCH = {"tvdd": 55.3, "vbp": 55.8, "vbn": 56.3, "vabn": 56.8, "vbnc": 57.3,
           "vinp": 57.8, "vref": 58.3, "vinn": 58.8, "en_3v3": 59.3, "en_3v3_b": 59.8}
    # tree bias outputs: trunk right ends (mirrored tree: tree_p's trunks on the right edge)
    ends = {}
    for net in ("vbp", "vbn", "vabn", "vbnc"):
        q = trp(net)
        hseg("M2", q.right - 0.2, XCH[net], cy(q))
        ends[net] = cy(q)
    # vbp -> tails right pin
    q = pin("tails", "vbp")[1]
    vseg("M2", XCH["vbp"], ends["vbp"], 110.40)
    v1(XCH["vbp"], 110.40)
    hseg("M1", 50.60, XCH["vbp"], 110.40)
    D.box("M2", q.right - 0.3, 110.40 - H, 50.75, 110.40 + H)
    v1(50.60, 110.40)
    # vbn -> sinks bottom pin
    q = pin("sinks", "vbn", "b")[1]
    vseg("M2", XCH["vbn"], ends["vbn"], 121.60)
    v1(XCH["vbn"], 121.60)
    hseg("M1", XCH["vbn"], cx(q), 121.60)
    v1(cx(q), 121.60)
    vseg("M2", cx(q), 121.60, q.bottom + 0.2)
    # vbnc -> casc_n left pin
    q = pin("cascn", "vbnc", "l")[1]
    vseg("M2", XCH["vbnc"], ends["vbnc"], cy(q))
    v1(XCH["vbnc"], cy(q))
    hseg("M1", XCH["vbnc"], q.left + 0.3, cy(q))
    v1(q.left + 0.3, cy(q))
    # vabn -> track TVABN -> ab_n top, pd_n top
    vseg("M2", XCH["vabn"], ends["vabn"], TVABN)
    v1(XCH["vabn"], TVABN)
    q1 = pin("abn", "vabn", "t")[1]
    q2 = pin("pdn", "vabn", "t")[1]
    hseg("M1", cx(q1), XCH["vabn"], TVABN)
    for q in (q1, q2):
        vseg("M2", cx(q), q.top - 0.15, TVABN)
        v1(cx(q), TVABN)
        if q is q2:
            D.via1(cx(q), cy(q))
            D.box("M2", cx(q) - H, cy(q) - H, cx(q) + H, cy(q) + H)
    # tree vdd: tree_p's ring (right edge of the mirrored tree) -> line -> Via2 into M3 iovdd
    D.box("M1", 54.40, Y_TR + 1.0, 54.90, Y_TR + 1.8)
    D.via1(54.65, Y_TR + 1.4)
    hseg("M2", 54.65, XCH["tvdd"], Y_TR + 1.4)
    vseg("M2", XCH["tvdd"], Y_TR + 1.4, 117.0)
    D.via2(XCH["tvdd"], 117.0)
    # core inputs: lines from the top edge down to M1 tracks above the tubs, west to the inputs' top pins
    TIN = {"vinn": 152.90, "vref": 153.37, "vinp": 153.84}
    for net, t in TIN.items():
        q = pin("inputs", net, "t")[1]
        vseg("M2", XCH[net], 180.0 - H, t)
        v1(XCH[net], t)
        hseg("M1", cx(q), XCH[net], t)
        v1(cx(q), t)
        vseg("M2", cx(q), q.top - 0.15, t)
        D.pin("M2", net, XCH[net] - H, 179.0, XCH[net] + H, 180.0)
    # iref / en_3v3 / en_3v3_b: tree top pins up to the top edge; en / en_b also east and down to pd_p / pd_n
    for net in ("iref", "en_3v3", "en_3v3_b"):
        q = pin("tree", net, "t")[1]
        D.box("M1", cx(q) - H, q.top - 0.3, cx(q) + H, 167.05)    # above the tree's en_b bar (M2, y .. 166.115)
        D.via1(cx(q), 166.90)
        D.box("M2", cx(q) - H, 166.755, cx(q) + H, 180.0)
        D.pin("M2", net, cx(q) - H, 179.0, cx(q) + H, 180.0)
    for net, t, tb in (("en_3v3", 167.85, TEN), ("en_3v3_b", 168.35, TENB)):
        q = pin("tree", net, "t")[1]
        v1(cx(q), t)
        hseg("M1", cx(q), XCH[net], t)
        v1(XCH[net], t)
        vseg("M2", XCH[net], t, tb)
        v1(XCH[net], tb)
        d = pin("pdp" if net == "en_3v3" else "pdn", net, "t")[1]
        hseg("M1", cx(d), XCH[net], tb)
        v1(cx(d), tb)
        vseg("M2", cx(d), cy(d), tb)
        D.via1(cx(d), cy(d))
    # tree vss: tree_n's ring bottom (left part) -> Via1 below the tree -> left strip track x 3.04 -> M3 iovss
    # (below the tree: its left-edge trunk ends are at x 2.6 .. 3.0 above)
    D.box("M1", 2.895, 154.31, 3.185, 155.10)
    D.via1(3.04, 154.455)
    vseg("M2", 3.04, 154.455, 133.0)
    D.via2(3.04, 133.0)
    # vbpc / vabp: tree_n trunk left ends -> left strip tracks x 2.00 / 2.52 -> M3 hop in the 134 .. 140 gap ->
    # left channel x 14.10 / 14.60
    for net, xt, yh, xc in (("vbpc", 1.50, 135.30, 13.96), ("vabp", 2.05, 136.30, 14.60)):
        q = pin("tree", net, "l")[1]
        hseg("M2", xt, q.left + 0.2, cy(q))
        vseg("M2", xt, cy(q), yh)
        D.via2(xt, yh)
        hseg("M3", xt, xc, yh, 0.40)
        D.via2(xc, yh)
        D.box("M2", xc - H, yh - H, xc + H, yh + H)
    q = pin("cascp", "vbpc")[1]
    vseg("M2", 13.96, 135.30, cy(q))          # touches casc_p's own vbpc lane (x .. 13.815): one polygon
    # vabp: down the left channel, M2 track under rhigh (y 88.395), riser x 29.6 to TVABP, ab_p / pd_p tops
    vseg("M2", 14.60, 136.30, 88.395)
    hseg("M2", 14.60, 29.60, 88.395)
    vseg("M2", 29.60, 88.395, TVABP)
    v1(29.60, TVABP)
    q1 = pin("abp", "vabp", "t")[1]
    q2 = pin("pdp", "vabp", "t")[1]
    hseg("M1", 29.60, cx(q2), TVABP)
    for q in (q1, q2):
        vseg("M2", cx(q), q.top - 0.15, TVABP)
        v1(cx(q), TVABP)
        if q is q2:
            D.via1(cx(q), cy(q))
            D.box("M2", cx(q) - H, cy(q) - H, cx(q) + H, cy(q) + H)
    # vfb: from the inputs' left pin to the M3 hop's landing (pad level draws the line from the junction)
    q = pin("inputs", "vfb")[1]
    D.box("M2", 15.10, 125.10, q.right, q.top)
    D.via2(15.25, 125.30)
    D.box("M3", 15.10, 125.0, 15.40, 125.60)
    label("M2", "vfb", 15.25, 125.45, 0.29)

top_bb = top.dbbox()
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
opt.write_context_info = False
ly.write(OUT, opt)
print("d2s_block bbox", top_bb)
with open(CDL, "w") as f:
    for src in (F + "/inputs_P/d2s_p_cells.cdl", F + "/inputs_N/d2s_n_cells.cdl", F + "/out/cells/d2s_rhigh.cdl",
                F + "/out/cells/bias_tree_pd.cdl"):
        f.write("".join(l for l in open(src) if not l.startswith("* SPDX")) + "\n")
    f.write("""* SPDX-FileCopyrightText: 2026 Christoph Maier
* SPDX-License-Identifier: Apache-2.0
* d2s_block (agent F, C2 stage 3): d2s_mpdda_pd + bias_tree_pd of the pad, composed from the cells' own CDLs.
* vdd = vddo = iovdd, vss = vsso = iovss (pad level); BP / BN / BPC / BNC are in the tails / sinks / cascode cells.
.SUBCKT d2s_block iovdd iovss vinp vinn vref vfb a b dabp dabn iref en_3v3 en_3v3_b
XIN vinp vref vinn vfb x y sa_A sa_B sa_C1 sa_C2 sb_A sb_B sb_C1 sb_C2 iovdd d2s_inputs_c
XTL sa_A sa_B sa_C1 sa_C2 sb_A sb_B sb_C1 sb_C2 vbp iovdd d2s_tails_c
XRH sa_A sa_B sa_C1 sa_C2 sb_A sb_B sb_C1 sb_C2 iovss d2s_rhigh
XLD l2 pl pr iovdd d2s_loads_c
XCP a l2 pl pr vbpc iovdd d2s_casc_p_c
XABP a b dabp l1 l2 vabp iovdd d2s_ab_p_c
XPDP a en_3v3 vabp iovdd iovdd d2s_pd_p_c
XSK vbn iovss x y sinks_6x6_c
XCN b l1 vbnc iovss x y d2s_casc_n_c
XABN a b dabn l1 l2 vabn iovss d2s_ab_n_c
XPDN b en_3v3_b vabn iovss iovss d2s_pd_n_c
XT iovdd iovss iref vbp vbn vbpc vbnc vabp vabn en_3v3 en_3v3_b bias_tree_pd
.ENDS d2s_block
""")
