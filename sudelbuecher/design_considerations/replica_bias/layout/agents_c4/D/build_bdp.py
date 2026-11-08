# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_bdp.py: layout of bias_dist_pd (4 inputs, 4 outputs), IHP sg13cmos5l. C4, Claude, agent D, 2026-11-07.

    python3 build_bdp.py <out dir> [--no-png]      (PDK_ROOT, default /foss/pdks; inputs/ next to work/)

Rows (each built with the code that built its precedent):
  bdp_mirror_n  D | NI NM | D, 6u/6u, 2u/6u end dummies: N's sink_block() (build_rb_n.py, unchanged, as rb_mirror)
                with the gate net ni and band tracks vpd / ni; placed mirrored (band down, toward the switches)
  bdp_mirror_p  D | PO0 PO1 PD PO2 PO3 | D, 5u/6u: the tail row (build_rb_p.tails() = F's tails_row(), C3's P
                helpers unchanged) with PD, the diode, in the middle; drains down as M2 pads; PD's drain joins the
                left gate column through an M1 lane under the ring and an M2 riser to the column's edge stub
Switch row (bdp_cells.py): one standard-cell row under both mirrors, en_3v3 line at its bottom:
  under NI / NM:  bdp_slice x 4 (inputs 0..3, abutted) | bdp_tdn
  under PO / PD:  bdp_slice under PO0, PO1 | bdp_svpd under PD | bdp_slice under PO2, PO3 (each slice's io_a riser
                  under its PO's drain pad), fillers between
Channel between the mirrors and the switch row: Metal1 tracks T0 (ni left, vpd lane right), T1..T4 (iin0..3 to the
left edge, iout0..3 to the right edge); Metal2 vertical only (risers, po lines, supply straps). M1 / M2 only.
"""
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
INP = os.environ.get("BDP_INPUTS", os.path.join(HERE, "..", "inputs"))
REPO = "/home/user/sg13cmos5l_cm_ip__single2diff2single"
sys.path.insert(0, HERE)
import bdp_cells as B        # noqa: E402
import pya                   # noqa: E402

P, ly, box, pin = B.P, B.ly, B.box, B.pin
g5 = P.g5


# ---------------------------------------------------------------- N row: N's generator, unchanged
def n_lib():
    """build_rb_n.py up to its write() (library part, C3's and N's code unchanged), executed in its own namespace
    and layout (its module end would write files)"""
    src = open(os.path.join(INP, "N", "build_rb_n.py")).read()
    ns = {"__name__": "build_rb_n_lib"}
    exec(compile(src[:src.index("\ndef write(")], "build_rb_n.py", "exec"), ns)
    return ns


def mirror_n(N):
    c = N["sink_block"]("bdp_mirror_n", m1=["NI", "NM"], m2=None, band=["vpd", "ni"], gn="ni",
                        f={"NI": ("NI", 6, 6, "ni", "ni", "vss"), "NM": ("NM", 6, 6, "vpd", "ni", "vss")})
    N["name_dummies"](c, ["DN0", "DN3"])
    t = ly.create_cell("bdp_mirror_n")
    t.copy_tree(c.c)
    ports = sorted({p[0] for p in c.pins})
    B.CDL["bdp_mirror_n"] = (ports, c.cdl)
    return t


# ---------------------------------------------------------------- P row: the tail row with PD in the middle
def mirror_p():
    """build_rb_p.tails() (F's tails_row(), C3's helpers) with seven 5/6 devices D PO0 PO1 PD PO2 PO3 D. Changed:
    gate net vpd, edge stub on the left; PD (diode) drain -> M1 lane 0.18 (M1_b) under the ring strip -> M2 riser
    beside the ring -> the stub (no gate contact in the middle of the bar)."""
    c = ly.create_cell("bdp_mirror_p")
    T = P.mos(5, 6)
    names = ["D", "PO0", "PO1", "PD", "PO2", "PO3", "D"]
    nets = {"PO0": "po0", "PO1": "po1", "PD": "vpd", "PO2": "po2", "PO3": "po3"}
    (lo,), xc = P.rows(c, [T] * 7, [names], False)
    h = 6.68
    x0, x1 = lo[0]["act"].left, lo[-1]["act"].right
    top_in = 0.43
    b = pya.DBox(x0 - (P.RG + 0.92), -h - 1.13, x1 + (P.RG + 0.92), top_in + 0.30 + 0.62)
    gl, gr = P.gate_cols(c, lo)
    box(c, "M1", x0, -0.23, x1, top_in + 0.30)
    P.ring(c, x0 - P.RG, -h - 0.51, x1 + P.RG, top_in + 0.30)
    cx = {}
    for i, (dv, n) in enumerate(zip(lo, names)):
        a, x = dv["act"], dv["act"].center().x
        if n == "D":
            P.dev(c, "DP%d" % i, "vdd", "vpd", "vdd", T)
            box(c, "M1", a.left, -h - 0.21, a.right, -6.45)
            continue
        P.dev(c, n, nets[n], "vpd", "vdd", T)
        cx[n] = x
        box(c, "M1", x - 0.555, -6.67, x + 0.555, -6.38)
        P.fill(c, "Via1", x - 0.505, -6.62, x + 0.505, -6.43)
        box(c, "M2", x - 0.555, -6.38, x + 0.555, b.bottom)
        pin(c, "M2", nets[n], x - 0.555, b.bottom, x + 0.555, b.bottom + 0.30)
    yl = b.bottom + 0.295                                     # lane (T0), 0.21 wide, 0.22 (M1_e) under the ring
    ys = gl.center().y
    box(c, "M1", b.left, yl - 0.105, cx["PD"] + 0.15, yl + 0.105)
    for x in (cx["PD"], b.left + 0.145):
        B.via(c, x, yl)
    box(c, "M2", b.left, yl - 0.145, b.left + 0.29, ys + 0.15)
    P.edge_stub(c, gl, ys, b.left, "vpd")
    pin(c, "M1", "vdd", x0 - P.RG - 0.30, -h + 0.5, x0 - P.RG, -h + 2.5)
    P.well(c, b)
    P.finish(c, ["po0", "po1", "po2", "po3", "vdd", "vpd"])
    c.cx = {k: v - b.left for k, v in cx.items()}             # device centers in the finished frame
    c.ring = (P.RG + 0.92 - P.RG - 0.30, -h - 0.51 - b.bottom)   # ring Activ outer left x, bottom y
    B.CDL["bdp_mirror_p"] = P.CDL["bdp_mirror_p"]
    return c


# ---------------------------------------------------------------- top level
T = {k: g5(B.TD[1] + 0.285 + 0.39 * (4 - k)) for k in range(5)}   # track centers: T4 (M1_b over the vdd strip) .. T0
TW = 0.105                                                 # M1 track half width (Via1 + V1_c 0.01)
YR = g5(T[0] + 0.105 + 0.22)                               # ring Activ bottom of both mirrors (T0 top + M1_e 0.22)


def track(c, x0, x1, k):
    box(c, "M1", x0, T[k] - TW, x1, T[k] + TW)


def riser_up(c, x, k, y0=B.NW[1] - 0.30):
    """M2 from a slice's riser pin (top edge 5.32) up to track k, Via1 there"""
    box(c, "M2", x - 0.145, y0, x + 0.145, T[k] + 0.145)
    B.via(c, x, T[k])


def top(cells):
    nd, iv, tg, sl, tn, sp, mn, mp = cells
    c = ly.create_cell("bias_dist_pd")
    ins = lambda cc, x, y=0.0, t=pya.DTrans.R0: c.insert(pya.DCellInstArray(cc.cell_index(),
                                                                          pya.DTrans(t, pya.DVector(x, y))))
    # N mirror: bbox left at x = 0, mirrored (band down), ring Activ bottom at YR
    act = pya.Region(mn.begin_shapes_rec(P.LI["Activ"])).bbox().to_dtype(ly.dbu)
    nb = mn.dbbox()
    dxn, dyn = -nb.left, YR + act.top
    ins(mn, dxn, dyn, pya.DTrans.M0)
    nring = (act.left + dxn, act.right + dxn)                  # N ring Activ x range
    ni_y, vpd_y = dyn - 7.475, dyn - 6.975                     # band tracks (sink_block: A + TM + TP k)
    # P mirror: left edge 0.72 (NW_f1 0.62 + 0.10) right of the N ring, ring Activ bottom at YR
    xp = g5(nring[1] + 0.72)
    yp = YR - mp.ring[1]
    ins(mp, xp, yp)
    cx = {k: xp + v for k, v in mp.cx.items()}
    pw = mp.dbbox().width()
    # switch row
    xl = nring[0]                                              # row starts under the N ring's left leg
    xr = xp + pw - 0.62                                        # and ends 0.62 inside the P mirror's NWell edge
    place = []                                                 # (cell, origin x, kind, index)
    o = xl + 0.90 + 0.105                                      # left filler 0.90 (holds the vss strap)
    for k in range(4):
        place.append((sl, o + 4.38 * k, "in", k))
    place.append((tn, o + 3 * 4.38 + 4.275 + 0.125, "tdn", 0))
    for j, n in enumerate(["PO0", "PO1", "PO2", "PO3"]):
        place.append((sl, cx[n] + 0.27 - (B.XT + 0.15), "out", j))   # io_a riser 0.27 right of the pad center
    place.append((sp, cx["PD"] - 0.98, "svpd", 0))
    place.sort(key=lambda p: p[1])
    edge = xl
    nf = 0
    for cc, x, kind, k in place:
        bl, br = B.BND[cc.name]
        assert x + bl >= edge - 1e-6, (kind, k, x + bl, edge)
        if x + bl - edge > 1e-6:
            f = B.filler("bdp_fill%d" % nf, g5(x + bl - edge))
            ins(f, edge)
            nf += 1
        ins(cc, x)
        edge = x + br
    f = B.filler("bdp_fill%d" % nf, g5(xr - edge))
    ins(f, edge)
    # channel: tracks, risers, po lines
    xL, xR = min(0.0, xl - 0.62), xp + pw
    ni_x = []
    for cc, x, kind, k in place:
        if kind == "in":
            xa, xb = x + B.XT + 0.15, x + B.XT + 0.98
            riser_up(c, xa, k + 1)
            track(c, xL, xa + 0.15, k + 1)
            pin(c, "M1", "iin%d" % k, xL, T[k + 1] - TW, xL + 0.5, T[k + 1] + TW)
            riser_up(c, xb, 0)
            ni_x.append(xb)
            pin(c, "M2", "en_in%d" % k, x + 1.25, B.EN[0], x + 1.54, B.EN[0] + 0.30)
        elif kind == "out":
            xa, xb = x + B.XT + 0.15, x + B.XT + 0.98
            riser_up(c, xb, k + 1)
            track(c, xb - 0.15, xR, k + 1)
            pin(c, "M1", "iout%d" % k, xR - 0.5, T[k + 1] - TW, xR, T[k + 1] + TW)
            box(c, "M2", xa - 0.145, B.NW[1] - 0.30, xa + 0.145, yp + 0.30)   # po: into the PO drain pad
            pin(c, "M2", "en_out%d" % k, x + 1.25, B.EN[0], x + 1.54, B.EN[0] + 0.30)
        elif kind == "tdn":
            riser_up(c, x + 0.98, 0)
            ni_x.append(x + 0.98)
            pin(c, "M2", "en_3v3_b", x + 0.42, B.EN[0], x + 0.71, B.EN[0] + 0.30)
        else:                                                  # SVPD drain riser straight up into PD's drain pad
            box(c, "M2", x + 0.835, B.NW[1] - 0.30, x + 1.125, yp + 0.30)
    track(c, min(ni_x) - 0.15, max(ni_x) + 0.15, 0)            # ni (T0), the vpd lane is in bdp_mirror_p
    xd = ni_x[1]                                               # N band's ni track down onto T0 over slice 1's riser
    box(c, "M2", xd - 0.145, T[0] - 0.145, xd + 0.145, ni_y + 0.145)
    box(c, "M2", nring[1] - 0.5, vpd_y - 0.145, xp + 0.29, vpd_y + 0.145)   # vpd: N band track -> P mirror riser
    # supplies: M2 straps, Via1 on both strips / ring legs
    xs = xl + 0.45                                             # vss: N ring bottom leg -> row vss strip
    box(c, "M2", xs - 0.145, B.TS[0] + 0.005, xs + 0.145, YR + 0.255)   # Mn_c 0.005 on top: 0.245 to the band
    B.via(c, xs, 0.15)
    B.via(c, xs, YR + 0.15)
    xv = xp + 2.8                                              # vdd: P ring bottom leg -> row vdd strip
    box(c, "M2", xv - 0.145, B.TD[0] + 0.005, xv + 0.145, YR + 0.255)
    B.via(c, xv, (B.TD[0] + B.TD[1]) / 2)
    B.via(c, xv, YR + 0.15)
    # one NWell for the vdd rail (row strip + P mirror), one ThickGateOx over everything
    box(c, "NWell", xp, B.NW[1] - 0.10, xp + pw, yp + 0.10)
    a = pya.Region(c.begin_shapes_rec(P.LI["Activ"])).bbox().to_dtype(ly.dbu)
    box(c, "TGO", a.left - 0.27, a.bottom - 0.27, a.right + 0.27, a.top + 0.27)
    # pins: en_3v3 on its line (left filler), supplies on the top legs of the rings
    pin(c, "M1", "en_3v3", xl, B.EN[0], xl + 0.5, B.EN[1])
    ytop_n = YR + act.height()
    pin(c, "M1", "vssh", nring[0] + 1.0, ytop_n - 0.28, nring[0] + 3.0, ytop_n - 0.02)
    pr = pya.Region(mp.begin_shapes_rec(P.LI["Activ"])).bbox().to_dtype(ly.dbu)
    pin(c, "M1", "vddh", xp + pr.right - 3.0, yp + pr.top - 0.30, xp + pr.right - 1.0, yp + pr.top)
    c.geo = dict(cx=cx, xp=xp, yp=yp, nring=nring, ni_y=ni_y, vpd_y=vpd_y, place=place)
    return c


# ---------------------------------------------------------------- flat CDL from the circuit files
def compose_cdl():
    """bias_dist_pd.spice + hv_logic.spice, subcircuits nand2_hv / inv_hv expanded (instance prefix + '_'),
    X... sg13_hv_* lines as M devices, vdd / vss -> vddh / vssh, plus the drawn dummies."""
    def read(path):
        sub, cur = {}, None
        for ln in open(path):
            ln = ln.strip()
            if ln.lower().startswith(".subckt"):
                f = ln.split()
                cur = f[1]
                sub[cur] = (f[2:], [])
            elif ln.lower().startswith(".ends"):
                cur = None
            elif cur and ln and ln[0] in "XxMm":
                sub[cur][1].append(ln.split())
        return sub
    src = read(os.path.join(REPO, "macros/bias_dist_pd/netlist/source/bias_dist_pd.spice"))
    lib = read(os.path.join(REPO, "macros/hv_logic/netlist/source/hv_logic.spice"))
    ports, body = src["bias_dist_pd"]
    ren = {"vdd": "vddh", "vss": "vssh"}
    out = []

    def mos(name, nets, params):
        out.append("M%s %s %s m=1" % (name, " ".join(ren.get(n, n) for n in nets), " ".join(params)))
    for f in body:
        model = [i for i, t in enumerate(f) if t.startswith("sg13_hv_")]
        if model:
            mos(f[0][1:], f[1:5], f[5:])
            continue
        sp, sb = f[-1], lib[f[-1]]
        m = dict(zip(sb[0], f[1:-1]))
        for g in sb[1]:
            nets = [m.get(n, "%s_%s" % (f[0], n)) for n in g[1:5]]
            mos("%s_%s" % (f[0][1:], g[0][1:]), nets, g[5:])
    dummies = ["MDN0 vssh ni vssh vssh sg13_hv_nmos w=2u l=6u ng=1 m=1",
               "MDN3 vssh ni vssh vssh sg13_hv_nmos w=2u l=6u ng=1 m=1",
               "MDP0 vddh vpd vddh vddh sg13_hv_pmos w=5u l=6u ng=1 m=1",
               "MDP6 vddh vpd vddh vddh sg13_hv_pmos w=5u l=6u ng=1 m=1"]
    src_d = [ln for ln in out if ln.startswith("MMD")]          # round 2: the lead backannotated the dummies into
    if src_d:                                                   # the source netlist (XMDN[k], XMDP[k]): use those
        out = [ln for ln in out if not ln.startswith("MMD")]
        dummies = src_d
    head = ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
            "* bias_dist_pd.cdl: flat reference netlist of bias_dist_pd.gds, composed by build_bdp.py (Claude, "
            "agent D, C4 2026-11-07)",
            "* from macros/bias_dist_pd/netlist/source/bias_dist_pd.spice + macros/hv_logic/netlist/source/"
            "hv_logic.spice", "* (gates expanded, vdd / vss -> vddh / vssh); the dummies of bdp_mirror_n / bdp_mirror_p "
            "as backannotated in the source (else drawn names MDN0 / MDN3, MDP0 / MDP6).", ""]
    txt = head + [".SUBCKT bias_dist_pd " + " ".join(ren.get(p, p) for p in ports)] + out + \
        ["* dummies (D = S = B on the rail, gate by abutment)"] + dummies + [".ENDS bias_dist_pd", ""]
    return "\n".join(txt), len(out), len(dummies)


# ---------------------------------------------------------------- main
def main(out, png=True):
    os.makedirs(os.path.join(out, "cells"), exist_ok=True)
    P.OUT = os.path.join(out, "previews")
    os.makedirs(P.OUT, exist_ok=True)
    std = lambda c: B.standalone(c, os.path.join(out, "cells", c.name + ".gds"), B.cdl_text([c], c.name))
    g = [B.nand2_hv(), B.inv_hv(), B.tg_hv()]
    for c in g:
        std(c)
    for c in g:
        B.strip_labels(c)
    sl = B.slice_(*g)
    tn, sp = B.single("bdp_tdn", "n"), B.single("bdp_svpd", "p")
    N = n_lib()
    mn, mp = mirror_n(N), mirror_p()
    for c in (sl, tn, sp, mn, mp):
        std(c)
        B.strip_labels(c)
    t = top([*g, sl, tn, sp, mn, mp])
    for c in list(ly.each_cell()):
        if c.name.startswith(("pmosHV", "nmosHV")):
            c.name = "bdp_" + c.name.replace("$", "_")
    opt = pya.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    l2 = pya.Layout()
    l2.dbu = ly.dbu
    l2.create_cell("bias_dist_pd").copy_tree(t)
    l2.write(os.path.join(out, "bias_dist_pd.gds"), opt)
    txt, n, d = compose_cdl()
    open(os.path.join(out, "bias_dist_pd.cdl"), "w").write(txt)
    b = t.dbbox()
    print("bias_dist_pd %.3f x %.3f um = %.1f um2; CDL %d devices + %d dummies" % (b.width(), b.height(),
                                                                                  b.width() * b.height(), n, d))
    for k in ("nand2_hv", "inv_hv", "tg_hv", "bdp_slice", "bdp_tdn", "bdp_svpd", "bdp_mirror_n", "bdp_mirror_p"):
        cb = ly.cell(k).dbbox()
        print("  %-13s %6.2f x %5.2f um  %6.1f um2" % (k, cb.width(), cb.height(), cb.width() * cb.height()))
    print("  geometry:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in t.geo.items() if k != "place"})
    if png:
        previews(t)
    return t



# ---------------------------------------------------------------- previews
def render(c, fn, win=None, notes=()):
    """P.render() with two changes: subcell TEXT notes placed at their transformed positions (DPoint, not DVector,
    so the instance displacement applies), and extra net notes (x, y, text) for the unlabeled inner nets."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon
    b = c.dbbox() if win is None else pya.DBox(*win)
    s = min(30.0 / b.width(), 17.0 / b.height())
    fig, ax = plt.subplots(figsize=(max(5.0, b.width() * s) + 1, max(4.0, b.height() * s) + 1.2))
    for lay, fc, a, ec in P.STYLE:
        ps = [Polygon([(q.x * ly.dbu, q.y * ly.dbu) for q in p.to_simple_polygon().each_point()])
              for p in pya.Region(c.begin_shapes_rec(P.LI[lay])).merged().each()]
        ax.add_collection(PatchCollection(ps, facecolor=fc, alpha=a, edgecolor=ec or fc, linewidth=0.7 if ec else 0))
    fs = 8 if win else 6
    for lay, col in (("M1txt", "#0b3d91"), ("M2txt", "#3b2a70")):
        for t in c.shapes(P.LI[lay]).each():
            p = t.dtext.trans.disp
            ax.text(p.x, p.y, t.dtext.string, fontsize=fs, color=col, weight="bold", ha="center", va="center",
                    clip_on=True, bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    it = c.begin_shapes_rec(P.LI["TEXT"])
    while not it.at_end():
        t = it.shape()
        if t.is_text() and t.text_string not in ("pmosHV", "nmosHV", "well"):
            p = it.dtrans() * pya.DPoint(t.dtext.trans.disp.x, t.dtext.trans.disp.y)
            ax.text(p.x, p.y, t.text_string, fontsize=fs + 1, color="#5a1a5a", weight="bold", ha="center",
                    va="center", clip_on=True)
        it.next()
    for x, y, txt in notes:
        ax.text(x, y, txt, fontsize=fs, color="#b03000", weight="bold", ha="center", va="center", clip_on=True,
                bbox=dict(boxstyle="round,pad=0.1", fc="#fff3e0", ec="#b03000", lw=0.5, alpha=0.9))
    ax.set_xlim(b.left, b.right)
    ax.set_ylim(b.bottom, b.top)
    ax.set_aspect("equal")
    ax.set_xlabel("um")
    w = c.dbbox()
    ax.set_title("%s%s  (cell %.2f x %.2f um). NWell green, ThickGateOx olive, pSD tan, Activ green, GatPoly red, "
                 "Cont black, Metal1 blue, Via1 red, Metal2 violet; pins blue / violet, inner nets orange" % (
                     c.name, "  close-up" if win else "", w.width(), w.height()), fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(P.OUT, fn), dpi=110)
    plt.close(fig)


def previews(t):
    g = t.geo
    cx, xp = g["cx"], g["xp"]
    notes = [((g["place"][0][1] + 14.0), T[0], "ni"), (xp + 5.0, T[0], "vpd lane"), (3.0, g["ni_y"], "ni (band)"),
             (3.0, g["vpd_y"], "vpd (band)"), (cx["PD"], T[2], "vpd")]
    for j, n in enumerate(["PO0", "PO1", "PO2", "PO3"]):
        notes.append((cx[n] + 0.27, T[0] + 0.3, "po%d" % j))
    for cc, x, kind, k in g["place"]:
        if kind in ("in", "out"):
            notes += [(x + 0.8, B.LINE[0] - 0.15, "e_b"), (x + 2.64, 1.45, "e")]
    render(t, "bias_dist_pd.png", notes=notes)
    xs = g["place"][1][1]
    render(t, "closeup_input_slice.png", (xs - 0.9, -0.6, xs + 5.4, 7.6), notes)
    render(t, "closeup_pd_svpd.png", (cx["PD"] - 6.5, -0.6, cx["PD"] + 6.5, 9.5), notes)
    render(t, "closeup_left_edge.png", (-0.5, -0.6, 11.0, 9.5), notes)
    render(t, "closeup_n_p_junction.png", (14.0, -0.6, 27.0, 11.5), notes)
    for k in ("nand2_hv", "inv_hv", "tg_hv", "bdp_slice", "bdp_mirror_n", "bdp_mirror_p"):
        render(ly.cell(k), k + ".png")


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]), "--no-png" not in sys.argv)
