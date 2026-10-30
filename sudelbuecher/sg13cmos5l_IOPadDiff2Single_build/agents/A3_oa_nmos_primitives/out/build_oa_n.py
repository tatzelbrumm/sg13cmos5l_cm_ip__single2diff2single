# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Build the compact NMOS primitives of oa_core_pd (IHP sg13cmos5l), 2026-10-28, Claude (Opus 5.5).

    python3 build_oa_n.py [path/to/pad_buffer_cells.gds] [out_dir]

Cells (all in oa_n_cells.gds, each standalone-checkable; reference netlist oa_n_cells.cdl):
  oa_n10    M10 (18 x 10/1), M11 (9 x 10/1), MC10, MS2 (10/1 each) as one rotated array of 3-finger rows,
            interdigitated by rows; MS3 (0.5/2) and SKS (1/0.45) in the free end of the MC10 / MS2 row;
            2/1 end dummies; one p+ tie segment at the bottom; pins on the top / bottom edges.
  oa_mcs_c  MCS / MCL (3.4/30) as a 1 x 2 AREF at the Gat.b1 pitch (30 um gates horizontal, merged poly);
            gate contact row below, one p+ tie segment on top that can overlap oa_n10's.
  oa_n_pair (check cell, written to logs/oa_n_pair_check.gds only) oa_n10 + oa_mcs_c at (4.91, -7.99) with
            the shared tie, to prove the overlap is DRC clean.
Device cells are copied unmodified from the library; the 2/1 dummy is derived from two library variants
(generator.derive_mos checks the PCell's separability). Process-agnostic code: skill/generic/generator.py;
IHP values: skill/ihp_sg13cmos5l/adapter.py (every rule value from sg13cmos5l_tech_default.json, keys cited).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "skill", "generic"))
sys.path.insert(0, os.path.join(HERE, "skill", "ihp_sg13cmos5l"))
import klayout.db as db                      # noqa: E402
import generator as g                        # noqa: E402  (process-agnostic)
import adapter as proc                       # noqa: E402  (IHP sg13cmos5l process adapter)

LIB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "inputs", "pad_buffer_cells.gds")
OUT = sys.argv[2] if len(sys.argv) > 2 else HERE

# ------------------------------------------------------------------ the score (bottom row first)
# same text as skill/generic/patterns.md, section "oa_n10"; check_score() verifies the sym / cc claims
SCORE_N10 = """
row X0 : d A A A d      # A = M10, B = M11: alternation by rows A B A A B A A B A
row X1 : d B B B d
row X2 : d A A A d
row X3 : d A A A d
row X4 : d B B B d
row X5 : d A A A d
row X6 : d A A A d
row X7 : d B B B d
row X8 : d A A A d
row Y  : e C S e        # MS3, SKS follow in the free end of this row (extras, drawn by hand below)
voice A = M10   D=d10 G=vnc S=vres B=vss
voice B = M11   D=vnc G=vnc S=vss  B=vss
voice C = MC10  D=vpc G=vbr S=d10  B=vss
voice S = MS2   D=ks  G=vbr S=vss  B=vss
voice d = dummy D=vss G=vnc S=vss  B=vss
voice e = dummy D=vss G=vbr S=vss  B=vss
sym mirror_y rows=X0-X8   # retrogradation of the rows
sym mirror_x rows=X0-X8   # every row is its own retrograde (end rests d ... d)
sym point    rows=X0-X8   # hence retrograde inversion too
cc  A,B      rows=X0-X8   # M10 and M11 share one centroid
"""
SCORE = None
PORTS_N10 = ["vss", "vnc", "vres", "vbr", "vpc", "ks", "en_3v3_b"]
PORTS_MCS = ["vss", "vbr", "vres"]


def build():
    P = proc.Process()
    lib = db.Layout()
    lib.read(LIB)
    ly = db.Layout()
    ly.dbu = lib.dbu
    cx = g.Ctx(P, ly)
    model = "sg13_hv_nmos"
    c10 = g.copy_cell(lib, proc.DEVICES["nhv_10_1"][0], ly)
    cdum = g.derive_mos(cx, lib, proc.DEVICES["nhv_10_1"][0], proc.DEVICES["nhv_2_4"][0], "nmosHV_w2_l1")
    c_ms3 = g.copy_cell(lib, proc.DEVICES["nhv_0p5_2"][0], ly)
    c_sks = g.copy_cell(lib, proc.DEVICES["nhv_1_0p45"][0], ly)
    c_mcs = g.copy_cell(lib, proc.DEVICES["nhv_3p4_30"][0], ly)
    m10, mdum = g.Mos(cx, c10, model), g.Mos(cx, cdum, model)
    mm = g.Mos(cx, c_mcs, model)
    global RISER_OFF
    RISER_OFF = g.snap(cx.r("thickox_over_active") + (mm.lact - mm.stripe_c[1]) + cx.track_w() / 2)
    devs = {"A": m10, "B": m10, "C": m10, "S": m10, "d": mdum, "e": mdum}
    global SCORE
    SCORE = g.parse_score(SCORE_N10)
    bad = [c for c in g.check_score(SCORE) if not c[1]]
    if bad:
        raise ValueError("score claims fail: %s" % bad)
    VO = {k: (v["device"], v["D"], v["G"], v["S"]) for k, v in SCORE["voices"].items()}

    # ================================================================ oa_n10
    top = ly.create_cell("oa_n10")
    blk = g.Block(cx, top)
    rows = SCORE["rows"]
    pitch_y = m10.lact + cx.r("active_space")
    R = {}
    for k, (name, letters) in enumerate(rows):
        R[name] = blk.add_row(name, letters, devs, 0.0, g.snap(k * pitch_y))
    X = [R["X%d" % i] for i in range(9)]
    Y = R["Y"]
    tw = cx.track_w()
    m1s = cx.r("m1_space")

    # vertical structures: dummy straps, gate bars, joiners
    tie_h = cx.tap_h()
    tie_y0 = g.snap(X[0][0].y0 - cx.r("active_space") - tie_h)       # tie Activ below row X0 (Act.b)
    tie_m1 = (tie_y0 + cx.r("cont_in_active") - cx.r("m1_cont_endcap"),
              tie_y0 + cx.r("cont_in_active") + cx.r("cont") + cx.r("m1_cont_endcap"))
    sL = g.strap(cx, top, [r[0] for r in X] + [Y[0]], tie_m1[0], Y[0].yT + cx.pad_h() / 2)
    sR = g.strap(cx, top, [r[-1] for r in X], tie_m1[0], Y[-1].yB + tw / 2)        # up to Y's vss line
    sY = g.strap(cx, top, [Y[-1]], Y[-1].yB - cx.pad_h() / 2, Y[-1].yT + cx.pad_h() / 2)
    blk.vertical("vss", sL[0], sL[1], tie_m1[0], Y[0].yT + cx.pad_h() / 2, nvia=3, draw=False)
    blk.vertical("vss", sR[0], sR[1], tie_m1[0], Y[-1].yB + tw / 2, nvia=3, draw=False)
    blk.vertical("vss", sY[0], sY[1], Y[-1].yB - cx.pad_h() / 2, Y[-1].yT + cx.pad_h() / 2, nvia=3, draw=False)
    bars = {}
    top_edge = None
    for side in ("L", "R"):
        ys = []
        for r in X:
            bar, cy = g.gate_contacts(cx, top, r, side)
            ys.append(cy)
        bars[side] = bar
    yb0 = ys[0][0] - cx.r("m1_cont_endcap")
    yb1 = ys[-1][1] + cx.r("m1_cont_endcap")
    jL = (g.snap(bars["L"][0] - m1s - tw), g.snap(bars["L"][0] - m1s))
    jR = (g.snap(bars["R"][1] + m1s), g.snap(bars["R"][1] + m1s + tw))
    # Y row gate (vbr): left contact column only
    barY, cyY = g.gate_contacts(cx, top, Y, "L")

    # tracks over the stripes
    # each finger: S on its bottom line (B), D on its top line (T), nets from the voices; dummies are strapped
    def nets(r, term, skip=()):
        return [None if (VO[f.letter][0] == "dummy" or VO[f.letter][term] in skip) else VO[f.letter][term] for f in r]
    # where each net's tracks end: at the vertical structure that carries the net (joiner / strap / gate bar)
    EXT = {"vres": lambda r: (r[1].x0, jR[1]), "d10": lambda r: (jL[0], r[-2].x1),
           "vss": lambda r: (sL[0], sR[1]), "vnc": lambda r: (bars["L"][0], bars["R"][1])}
    for r in X:
        for line, term in (("B", 3), ("T", 1)):
            nl = nets(r, term)
            n0 = [n for n in nl if n][0]
            blk.line_tracks(r, line, nl, ext={n0: EXT[n0](r)})
    blk.line_tracks(Y, "B", nets(Y, 3), ext={"d10": (jL[0], None), "vss": (None, sR[1])})
    # extras in the free end of row Y: MS3 (0.5/2) and SKS (1/0.45), R0 (gate vertical, contact above)
    m3, mk = g.Mos(cx, c_ms3, model), g.Mos(cx, c_sks, model)
    # extras' Activ bottom: row Y's baseline, raised so their poly endcap keeps Gat.d from row X8's Activ
    yE = g.snap(max(Y[0].y0, X[8][0].y1 + cx.r("poly_to_active") + cx.r("poly_endcap")))
    # MS3 Activ left edge: Act.b / Gat.d from row Y's last finger and its poly end, M1 space of the S tab
    x3 = g.snap(max(Y[-1].x1 + cx.r("active_space"), Y[-1].x1 + cx.r("poly_endcap") + cx.r("poly_to_active"),
                    Y[-1].x1 + m1s + tw / 2 - (m3.stripe_c[0])))
    top.insert(db.DCellInstArray(c_ms3.cell_index(), db.DTrans(x3, yE)))
    sw = tw                                                   # S / D tabs of the extras: via-ready width
    s3 = x3 + m3.stripe_c[0]                                  # MS3 S stripe centre (vss)
    d3 = x3 + m3.stripe_c[1]                                  # MS3 D stripe centre (vpc)
    x4 = g.snap(max(x3 + m3.lact + cx.r("active_space"), d3 + sw / 2 + m1s + sw / 2 - mk.stripe_c[0]))
    top.insert(db.DCellInstArray(c_sks.cell_index(), db.DTrans(x4, yE)))
    s4 = x4 + mk.stripe_c[0]
    d4 = x4 + mk.stripe_c[1]
    # lines above row Y: T line = ks (from MS2 to the ks riser); vpc line one track pitch higher
    yT, yB = Y[0].yT, Y[0].yB
    y_vpc = g.snap(yT + tw + cx.r("m2_space"))
    top_edge = g.snap(y_vpc + tw / 2)
    x_ks = g.snap(d4 - tw / 2)                                  # ks riser: straight above SKS's drain via
    blk.line_tracks(Y, "T", nets(Y, 1, skip=("vpc",)), ext={"ks": (None, x_ks + tw)})   # vpc: tab up, below
    # gate contacts of the extras (above their Activ): contact Cnt.e above Activ; poly tab Cnt.d around it
    c, cd, ce = cx.r("cont"), cx.r("cont_in_poly"), max(cx.r("polycont_to_active"), 0)
    for (xx, m, net) in ((x3, m3, "ks"), (x4, mk, "en_3v3_b")):
        gx0, gx1 = xx + m.sd, xx + m.sd + m.L
        ya = yE + m.W
        cy0 = g.snap(ya + ce)
        cx.box(top, "poly", gx0, ya, gx1, cy0 + c + cd)
        ccx = g.snap((gx0 + gx1) / 2 - c / 2)
        cx.box(top, "contact", ccx, cy0, ccx + c, cy0 + c)
        if net == "ks":       # MS3 gate: M1 up to the ks line (via-ready width), Via1
            cx.box(top, "metal1", ccx + c / 2 - tw / 2, cy0 - cx.r("m1_cont_endcap"), ccx + c / 2 + tw / 2,
                   yT + cx.r("via1") / 2 + cx.r("via1_m1_enc"))
            blk.vertical("ks", ccx + c / 2 - tw / 2, ccx + c / 2 + tw / 2, cy0, yT + cx.r("via1") / 2 + cx.r("via1_m1_enc"), draw=False)
        else:                 # SKS gate: M1 riser (contact width) to the top edge = en_3v3_b pin
            cx.box(top, "metal1", ccx, cy0 - cx.r("m1_cont_endcap"), ccx + c, top_edge)
            cx.pin(top, 1, "en_3v3_b", ccx, top_edge - tw, ccx + c, top_edge)
    # S tabs (vss) down to the vss line, D tabs up: MS3 D -> vpc line, SKS D -> ks line
    vend = cx.r("via1") / 2 + cx.r("via1_m1_enc")
    for sc, m in ((s3, m3), (s4, mk)):
        cx.box(top, "metal1", sc - sw / 2, yB - vend, sc + sw / 2, yE + m.W)
        blk.vertical("vss", sc - sw / 2, sc + sw / 2, yB - vend, yE + m.W, draw=False)
    cx.box(top, "metal1", d3 - sw / 2, yE, d3 + sw / 2, y_vpc + vend)
    blk.vertical("vpc", d3 - sw / 2, d3 + sw / 2, yE, y_vpc + vend, draw=False)
    cx.box(top, "metal1", d4 - sw / 2, yE, d4 + sw / 2, yT + vend)
    blk.vertical("ks", d4 - sw / 2, d4 + sw / 2, yE, yT + vend, draw=False)
    # MC10 drain (vpc): 3-via tab from its top stripe up to the vpc line
    fC = Y[1]
    xc, ln = (fC.x0 + fC.x1) / 2, cx.pad_len(3)
    cx.box(top, "metal1", xc - ln / 2, yT - cx.pad_h() / 2, xc + ln / 2, y_vpc + vend)
    blk.vertical("vpc", xc - ln / 2, xc + ln / 2, yT, y_vpc + vend, nvia=3, draw=False)
    blk.track("vpc", xc - ln / 2, d3 + sw / 2, y_vpc)
    # ks riser to the top edge
    cx.box(top, "metal2", x_ks, yT - tw / 2, x_ks + tw, top_edge)
    cx.pin(top, 2, "ks", x_ks, top_edge - tw, x_ks + tw, top_edge)
    cx.pin(top, 2, "vpc", xc - ln / 2, top_edge - tw, xc - ln / 2 + tw, top_edge)

    # gate bars (vnc both sides, up to the top edge on the right = vnc pin), Y's vbr riser (left) = vbr pin
    blk.vertical("vnc", bars["L"][0], bars["L"][1], yb0, yb1)
    blk.vertical("vnc", bars["R"][0], bars["R"][1], yb0, top_edge)
    cx.pin(top, 1, "vnc", bars["R"][0], top_edge - tw, bars["R"][1], top_edge)
    cx.box(top, "metal1", barY[0], cyY[0] - cx.r("m1_cont_endcap"), barY[1], top_edge)
    cx.pin(top, 1, "vbr", barY[0], top_edge - tw, barY[1], top_edge)
    # joiners
    d10y = [t["y"] for t in blk.tracks if t["net"] == "d10"]
    vresy = [t["y"] for t in blk.tracks if t["net"] == "vres"]
    blk.vertical("d10", jL[0], jL[1], min(d10y) - tw / 2, max(d10y) + tw / 2)
    blk.vertical("vres", jR[0], jR[1], min(vresy) - tw / 2, max(vresy) + tw / 2)
    # p+ substrate tie: one segment under row X0 (LU distance to the top row checked by DRC), contacts on a
    # grid anchored at the array's right Activ edge (oa_mcs_c uses the same grid)
    x_act0, x_act1 = X[0][0].x0, X[0][-1].x1
    grid = g.snap(x_act1 - cx.r("cont_in_active") - cx.r("cont"))
    tm = g.tie(cx, top, x_act0, x_act1, tie_y0, grid)
    # vss pin: the tie's M1 carried out to the left cell edge (= the d10 joiner's outer edge)
    cx.box(top, "metal1", jL[0], tm[1], tm[0], tm[3])
    cx.pin(top, 1, "vss", jL[0], tm[1], jL[0] + tw, tm[3])
    # thick-oxide outline following the devices and the tie
    tox = g.outline(cx, top, "thickox", [("active", cx.r("thickox_over_active")), ("thickox", 0.0)],
                    cx.r("thickox_space"))
    bot_edge = g.snap(tox.bbox().bottom * ly.dbu)
    # vres riser: from the X0 vres track down to the bottom edge, at the offset from the cell's right edge that
    # oa_mcs_c's vres riser has from its right edge (TGO.a + MCL drain stripe centre + half a track)
    right_edge = jR[1]
    xr = g.snap(right_edge - RISER_OFF)
    cx.box(top, "metal2", xr, bot_edge, xr + tw, X[0][0].yB + tw / 2)
    cx.pin(top, 2, "vres", xr, bot_edge, xr + tw, bot_edge + tw)
    blk.wire()
    # device names (TEXT layer) at finger centres
    names = {}
    for name, r in blk.rows:
        for f in r:
            nm = VO[f.letter][0]
            cx.text(top, "note", nm, (f.x0 + f.x1) / 2, (f.y0 + f.y1) / 2)
    cx.text(top, "note", "MS3", x3 + m3.lact / 2, yE + m3.W / 2)
    cx.text(top, "note", "SKS", x4 + mk.lact / 2, yE + mk.W / 2)

    # reference netlist, devices as drawn
    devlist = []
    for name, r in blk.rows:
        for f in r:
            nm, D, G, S = VO[f.letter]
            devlist.append(("%s_%s_%d" % (nm, name, f.idx), D, G, S, "vss", model, f.mos.W, f.mos.L))
    devlist.append(("MS3", "vpc", "ks", "vss", "vss", model, m3.W, m3.L))
    devlist.append(("SKS", "ks", "en_3v3_b", "vss", "vss", model, mk.W, mk.L))
    geo_n10 = dict(tie_y=(tie_y0, tie_y0 + tie_h), tie_x=(x_act0, x_act1), grid=grid, right=right_edge, xr=xr,
                   top=top_edge, bottom=bot_edge, rows=blk.rows, x3=x3, x4=x4, yE=yE)

    # ================================================================ oa_mcs_c
    mc = ly.create_cell("oa_mcs_c")
    mm = g.Mos(cx, c_mcs, model)
    gap = cx.r("finger_gap")
    pit = g.snap(mm.W + gap)
    mc.insert(db.DCellInstArray(c_mcs.cell_index(), db.DTrans(0, 0), db.DVector(0, 0), db.DVector(0, pit), 1, 2))
    # in R0 the gate runs along x (L = 30 horizontal): stripes are vertical, S left, D right
    sx, dx_ = mm.stripe_c[0], mm.stripe_c[1]
    gx0, gx1 = mm.sd, mm.sd + mm.L
    # gate contact row below MCS: contacts M1 space below the stripes' ends (and Cnt.e from Activ)
    c, cd, cs = cx.r("cont"), cx.r("cont_in_poly"), cx.r("cont_space")
    gy1 = -max(m1s, cx.r("polycont_to_active"))
    gy0 = gy1 - c
    cx.box(mc, "poly", gx0, gy0 - cd, gx1, 0)
    p = cx.cont_pitch()
    n = int((gx1 - gx0 - 2 * cd + cs) // p)
    span = n * c + (n - 1) * cs
    xs0 = gx0 + (gx1 - gx0 - span) / 2
    for k in range(n):
        x = g.snap(xs0 + k * p)
        cx.box(mc, "contact", x, gy0, x + c, gy1)
    enc = cx.r("m1_cont_endcap")
    row_m1 = (g.snap(xs0 - enc), g.snap(gy1 - cx.pad_h()), g.snap(dx_ + tw / 2), g.snap(gy1))
    cx.box(mc, "metal1", *row_m1)                                   # gate row, joined to MCS drain (diode)
    cx.box(mc, "metal1", dx_ - tw / 2, row_m1[1], dx_ + tw / 2, mm.W)  # MCS drain stripe widened = vbr
    # MCL drain (vres): widened stripe, 3 Via1 in a column, M2 riser up to the top edge
    y_mcl0, y_mcl1 = pit, pit + mm.W
    cx.box(mc, "metal1", dx_ - tw / 2, y_mcl0, dx_ + tw / 2, y_mcl1)
    cx.vias(mc, dx_, (y_mcl0 + y_mcl1) / 2, 3, vertical=True)
    # sources (vss): strap over both S stripes up to the tie
    tie_y0m = g.snap(y_mcl1 + max(cx.r("active_space"), cx.r("impl_to_ngate_hv") + cx.r("tie_impl_enc"),
                                  cx.r("poly_endcap") + cx.r("poly_to_active")))
    tie_m1m = tie_y0m + cx.r("cont_in_active") - enc
    cx.box(mc, "metal1", sx - tw / 2, 0, sx + tw / 2, tie_m1m + cx.pad_h())
    # tie: same contact grid as oa_n10 when the right edges are aligned (offset = n10 right edge - mcs right edge)
    mcs_right_guess = mm.lact + cx.r("thickox_over_active")      # PCell TGO / grown Activ right edge
    off = g.snap(geo_n10["right"] - mcs_right_guess)
    grid_m = g.snap(geo_n10["grid"] - off)
    tmm = g.tie(cx, mc, 0.0, mm.lact, tie_y0m, grid_m)
    tox_m = g.outline(cx, mc, "thickox", [("active", cx.r("thickox_over_active")), ("thickox", 0.0)],
                      cx.r("thickox_space"))
    bb = tox_m.bbox().to_dtype(ly.dbu)
    assert abs(bb.right - mcs_right_guess) < 1e-6, bb
    top_m = g.snap(bb.top)
    xrm = g.snap(bb.right - RISER_OFF)
    cx.box(mc, "metal2", xrm, (y_mcl0 + y_mcl1) / 2 - cx.via_pitch() - tw / 2, xrm + tw, top_m)
    assert abs(xrm + tw / 2 - dx_) < 0.05, (xrm, dx_)
    cx.pin(mc, 2, "vres", xrm, top_m - tw, xrm + tw, top_m)
    cx.box(mc, "metal1", bb.left, tmm[1], tmm[0], tmm[3])               # tie M1 out to the left cell edge
    cx.pin(mc, 1, "vss", bb.left, tmm[1], bb.left + tw, tmm[3])
    yv = (row_m1[1] + row_m1[3]) / 2
    xv = row_m1[0] + cx.r("via1_m1_endcap") + cx.r("via1") / 2
    cx.vias(mc, xv, yv, 1)
    cx.hpath(mc, "metal2", bb.left, xv + cx.r("via1") / 2 + cx.r("m2_via1_endcap"), yv, tw)
    cx.pin(mc, 2, "vbr", bb.left, yv - tw / 2, bb.left + tw, yv + tw / 2)
    cx.text(mc, "note", "MCS", mm.lact / 2, mm.W / 2)
    cx.text(mc, "note", "MCL", mm.lact / 2, pit + mm.W / 2)
    dev_mcs = [("MCS", "vbr", "vbr", "vss", "vss", model, mm.W, mm.L), ("MCL", "vres", "vbr", "vss", "vss", model, mm.W, mm.L)]
    geo_mcs = dict(right=bb.right, top=top_m, bottom=bb.bottom, left=bb.left, tie_y=(tie_y0m, tie_y0m + tie_h), off=off)

    opt = db.SaveLayoutOptions()
    opt.gds2_write_timestamps = False                          # reproducible bytes
    ly.write(os.path.join(OUT, "oa_n_cells.gds"), opt)
    # ================================================================ pair check (separate file): shared tie
    pr = ly.create_cell("oa_n_pair")
    pr.insert(db.DCellInstArray(top.cell_index(), db.DTrans(0, 0)))
    dy = g.snap(geo_n10["tie_y"][0] - geo_mcs["tie_y"][0])
    pr.insert(db.DCellInstArray(mc.cell_index(), db.DTrans(off, dy)))
    geo_mcs["pair_at"] = (off, dy)
    os.makedirs(os.path.join(OUT, "logs"), exist_ok=True)
    ly.write(os.path.join(OUT, "logs", "oa_n_pair_check.gds"), opt)
    hdr = ("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
           "* oa_n_cells.cdl: reference netlists of oa_n_cells.gds, devices as drawn (one line per finger,\n"
           "* dummies included), generated by build_oa_n.py 2026-10-28 (Claude, Opus 5.5).\n"
           "* Internal net of oa_n10: d10 (M10 drain = MC10 source).\n\n")
    g.write_cdl(os.path.join(OUT, "oa_n_cells.cdl"),
                [("oa_n10", PORTS_N10, devlist), ("oa_mcs_c", PORTS_MCS, dev_mcs)], hdr)
    return P, geo_n10, geo_mcs


if __name__ == "__main__":
    P, gn, gm = build()
    print("oa_n10: top %.3f bottom %.3f right %.3f; oa_mcs_c: %s" % (gn["top"], gn["bottom"], gn["right"], gm))
    print("rules used:")
    for k, (v, why) in P.citations().items():
        print("  %-20s %-7g %s" % (k, v, why))
