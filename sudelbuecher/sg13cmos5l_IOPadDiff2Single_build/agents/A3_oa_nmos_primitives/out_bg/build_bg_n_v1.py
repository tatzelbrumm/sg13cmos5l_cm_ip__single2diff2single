# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""VERSION 1 (dummies on vss), kept for reference; writes bg_n_cells_v1.gds / .cdl. Current: build_bg_n.py.
Build the compact NMOS block of bg_core_pd (IHP sg13cmos5l), 2026-10-28, Claude (Opus 5.5).

    python3 build_bg_n.py [path/to/pad_buffer_cells.gds] [out_dir]

Cell bg_n4 (in bg_n_cells.gds; reference netlist bg_n_cells.cdl):
  NA, NB (20/4 each) as 2 + 2 fingers of 10/4 in four rotated rows A B B A, rows 2-3 flipped (S on top), so the
  array is mirror-symmetric in y including the current direction; 2/4 end dummies; MS2 (10/1) as the top row with a
  2/1 dummy on the left, MS3 (0.5/2) and SKS (1/0.45) in that row's free end; p+ tie segments: one under row R0,
  one over row Y (latch-up needs it: 21.45 um from the bottom tie otherwise).
  Pins (A2's request, 2026-10-28): g, vpc, ks, en_3v3_b on the top edge (PMOS side); ea, eb next to each other on
  the bottom edge, symmetric about the array's centre line; vss on the bottom tie.
Process-agnostic code: ../out/skill/generic/generator.py; IHP values: ../out/skill/ihp_sg13cmos5l/adapter.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, "..", "out", "skill")
sys.path.insert(0, os.path.join(SKILL, "generic"))
sys.path.insert(0, os.path.join(SKILL, "ihp_sg13cmos5l"))
import klayout.db as db                      # noqa: E402
import generator as g                        # noqa: E402  (process-agnostic)
import adapter as proc                       # noqa: E402  (IHP sg13cmos5l process adapter)

LIB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "inputs", "pad_buffer_cells.gds")
OUT = sys.argv[2] if len(sys.argv) > 2 else HERE

# same text as ../out/skill/generic/patterns.md, section P4; check_score() verifies the claims
SCORE_BG = """
row R0      : d A d       # A = NA (2 x 10/4), B = NB (2 x 10/4): A B B A in y
row R1      : d B d
row R2 flip : d B d       # flip: S on the top line; rows R2, R3 are the mirror images of R1, R0
row R3 flip : d A d
row Y  flip : e S         # MS2 (10/1), S (vss) on top towards the top tie; coda MS3, SKS in the free end
voice A = NA    D=g   G=g S=ea  B=vss
voice B = NB    D=vpc G=g S=eb  B=vss
voice S = MS2   D=ks  G=g S=vss B=vss
voice d = dummy D=vss G=g S=vss B=vss
voice e = dummy D=vss G=g S=vss B=vss
sym mirror_y_orient rows=R0-R3   # retrogradation of the rows with inversion of the current direction
sym mirror_x        rows=R0-R3
cc  A,B             rows=R0-R3
"""
PORTS = ["vss", "g", "vpc", "ea", "eb", "ks", "en_3v3_b"]


def build():
    P = proc.Process()
    lib = db.Layout()
    lib.read(LIB)
    ly = db.Layout()
    ly.dbu = lib.dbu
    cx = g.Ctx(P, ly)
    model = proc.DEVICES["nhv_10_4"][3]
    c104 = g.copy_cell(lib, proc.DEVICES["nhv_10_4"][0], ly)
    c24 = g.copy_cell(lib, proc.DEVICES["nhv_2_4"][0], ly)
    c101 = g.copy_cell(lib, proc.DEVICES["nhv_10_1"][0], ly)
    c21 = g.derive_mos(cx, lib, proc.DEVICES["nhv_10_1"][0], proc.DEVICES["nhv_2_4"][0], "nmosHV_w2_l1")
    c_ms3 = g.copy_cell(lib, proc.DEVICES["nhv_0p5_2"][0], ly)
    c_sks = g.copy_cell(lib, proc.DEVICES["nhv_1_0p45"][0], ly)
    m104, m24, m101, m21 = (g.Mos(cx, c, model) for c in (c104, c24, c101, c21))
    m3, mk = g.Mos(cx, c_ms3, model), g.Mos(cx, c_sks, model)
    devs = {"A": m104, "B": m104, "d": m24, "S": m101, "e": m21}
    score = g.parse_score(SCORE_BG)
    bad = [c for c in g.check_score(score) if not c[1]]
    if bad:
        raise ValueError("score claims fail: %s" % bad)
    VO = {k: (v["device"], v["D"], v["G"], v["S"]) for k, v in score["voices"].items()}
    tw, m1s, sp2 = cx.track_w(), cx.r("m1_space"), cx.r("m2_space")
    vend = cx.r("via1") / 2 + cx.r("via1_m1_enc")      # M1 end beyond a via centre (V1.c; endcap along the tab)
    asp = cx.r("active_space")

    top = ly.create_cell("bg_n4")
    blk = g.Block(cx, top)
    y = 0.0
    R = {}
    for name, letters in score["rows"]:
        R[name] = blk.add_row(name, letters, devs, 0.0, g.snap(y))
        y += devs[letters[0]].lact + asp
    X = [R["R0"], R["R1"], R["R2"], R["R3"]]
    Y = R["Y"]

    def nets(r, line):
        """net on line 'B' / 'T' per finger; S on B unless the row is flipped; dummies strapped (None)"""
        flipped = [n for n, rr in blk.rows if rr is r][0] in score["flip"]
        term = (3 if line == "B" else 1) if not flipped else (1 if line == "B" else 3)
        return [None if VO[f.letter][0] == "dummy" else VO[f.letter][term] for f in r]

    # ---- ties: bottom (under R0) and top (over Y, MS2 / dummy width only)
    th = cx.tap_h()
    enc_m = cx.r("cont_in_active") - cx.r("m1_cont_endcap")         # tie Activ edge to its M1 edge
    yt0 = g.snap(X[0][0].y0 - asp - th)
    yt1 = g.snap(Y[0].y1 + asp)
    x_act0, x_act1 = X[0][0].x0, X[0][-1].x1
    grid = g.snap(x_act1 - cx.r("cont_in_active") - cx.r("cont"))
    tb = g.tie(cx, top, x_act0, x_act1, yt0, grid)
    tt = g.tie(cx, top, Y[0].x0, Y[-1].x1, yt1, grid)
    # ---- dummy straps (vss): left column through R0-R3 and Y up to the top tie; right column R0-R3
    sL = g.strap(cx, top, [r[0] for r in X] + [Y[0]], tb[1], tt[3])
    sR = g.strap(cx, top, [r[-1] for r in X], tb[1], X[3][0].yT + cx.pad_h() / 2)
    blk.vertical("vss", sL[0], sL[1], tb[1], tt[3], nvia=3, draw=False)
    # ---- gate bars (g): left over R0-R3 and Y, up to the top edge (g pin); right over R0-R3
    cys = {}
    for side in ("L", "R"):
        for r in X + ([Y] if side == "L" else []):
            bar, cy = g.gate_contacts(cx, top, r, side)
            cys.setdefault(side, []).append(cy)
            if side == "L":
                barL = bar
            else:
                barR = bar
    jA = (g.snap(barL[0] - m1s - tw), g.snap(barL[0] - m1s))          # left inner: ea joiner
    jV = (g.snap(jA[0] - m1s - tw), g.snap(jA[0] - m1s))              # left outer: vpc column
    jB = (g.snap(barR[1] + m1s), g.snap(barR[1] + m1s + tw))          # right: eb joiner
    # ---- row tracks over the stripes (NA / NB rows)
    EXT = {"ea": lambda r: (jA[0], r[-2].x1), "eb": lambda r: (r[1].x0, jB[1]),
           "g": lambda r: (barL[0], barR[1]), "vpc": lambda r: (jV[0], r[-2].x1)}
    for r in X:
        for line in ("B", "T"):
            nl = nets(r, line)
            n0 = [n for n in nl if n][0]
            blk.line_tracks(r, line, nl, ext={n0: EXT[n0](r)})
    # ---- row Y: MS2 flipped (S = vss on the top stripe -> M1 plate up to the top tie), D = ks on the bottom line
    fS = Y[1]
    yE = g.snap(max(Y[0].y0, X[3][0].y1 + cx.r("poly_to_active") + cx.r("poly_endcap")))
    sw = tw
    x3 = g.snap(max(fS.x1 + asp, fS.x1 + cx.r("poly_endcap") + cx.r("poly_to_active"),
                    fS.x1 + m1s + sw / 2 - m3.stripe_c[0]))
    top.insert(db.DCellInstArray(c_ms3.cell_index(), db.DTrans(x3, yE)))
    s3, d3 = x3 + m3.stripe_c[0], x3 + m3.stripe_c[1]
    x4 = g.snap(max(x3 + m3.lact + asp, d3 + sw / 2 + m1s + sw / 2 - mk.stripe_c[0]))
    top.insert(db.DCellInstArray(c_sks.cell_index(), db.DTrans(x4, yE)))
    s4, d4 = x4 + mk.stripe_c[0], x4 + mk.stripe_c[1]
    yB, yT = Y[0].yB, Y[0].yT
    # MS2's vss plate: from row Y's top stripes up to the top tie's M1, extended right over MS3's S tab
    plate_r = g.snap(s3 + sw / 2)
    cx.box(top, "metal1", sL[0], yT - cx.r("cont") / 2, plate_r, tt[3])
    # ks: track over row Y's bottom line from MS2 to SKS's drain
    blk.line_tracks(Y, "B", nets(Y, "B"), ext={"ks": (None, d4 + sw / 2)})
    # top lanes: vss bridge (SKS source -> plate), vpc lane at the top edge
    y_top_tox = g.snap(yt1 + th + cx.r("thickox_over_active"))
    y_vpc = g.snap(y_top_tox - tw / 2)
    y_br = g.snap(y_vpc - tw - sp2)
    top_edge = y_top_tox
    # extras: gate contacts above their Activ
    c, cd = cx.r("cont"), cx.r("cont_in_poly")
    ce = max(cx.r("polycont_to_active"), 0)
    gc = {}
    for (xx, m, key) in ((x3, m3, "ms3"), (x4, mk, "sks")):
        gx0, gx1 = xx + m.sd, xx + m.sd + m.L
        ya = yE + m.W
        cy0 = g.snap(ya + ce)
        cx.box(top, "poly", gx0, ya, gx1, cy0 + c + cd)
        ccx = g.snap((gx0 + gx1) / 2 - c / 2)
        cx.box(top, "contact", ccx, cy0, ccx + c, cy0 + c)
        gc[key] = (ccx, cy0)
    # MS3 gate (ks): M1 pad on the contact, Via1, M2 stub down into the ks track (over MS3's own gate: same net)
    ccx, cy0 = gc["ms3"]
    xc3, yc3 = ccx + c / 2, cy0 + c / 2
    ph = max(tw, g.snap(cx.r("m1_area") / tw + 0.0049))          # pad height: M1 area rule on a via-ready width
    cx.box(top, "metal1", xc3 - tw / 2, yc3 - tw / 2, xc3 + tw / 2, yc3 - tw / 2 + ph)
    cx.vias(top, xc3, yc3, 1)
    cx.box(top, "metal2", xc3 - tw / 2, yB - tw / 2, xc3 + tw / 2, yc3 + tw / 2)
    # SKS gate (en_3v3_b): M1 riser (contact width) to the top edge
    ccx, cy0 = gc["sks"]
    cx.box(top, "metal1", ccx, cy0 - cx.r("m1_cont_endcap"), ccx + c, top_edge)
    cx.pin(top, 1, "en_3v3_b", ccx, top_edge - tw, ccx + c, top_edge)
    # MS3 S (vss): tab up into the plate; MS3 D (vpc): tab up to the vpc lane
    cx.box(top, "metal1", s3 - sw / 2, yE, s3 + sw / 2, yT)
    cx.box(top, "metal1", d3 - sw / 2, yE, d3 + sw / 2, y_vpc + vend)
    blk.vertical("vpc", d3 - sw / 2, d3 + sw / 2, yE, y_vpc + vend, draw=False)
    # SKS S (vss): tab up to the vss bridge; SKS D (ks): tab from the ks track up to the top edge (ks pin)
    cx.box(top, "metal1", s4 - sw / 2, yE, s4 + sw / 2, y_br + vend)
    blk.vertical("vss", s4 - sw / 2, s4 + sw / 2, yE, y_br + vend, draw=False)
    cx.box(top, "metal1", d4 - sw / 2, yE, d4 + sw / 2, top_edge)
    blk.vertical("ks", d4 - sw / 2, d4 + sw / 2, yE, top_edge, draw=False)
    cx.pin(top, 1, "ks", d4 - sw / 2, top_edge - tw, d4 + sw / 2, top_edge)
    blk.vertical("vss", s3 - sw / 2, s3 + sw / 2, yT - cx.r("cont") / 2, tt[3], draw=False)   # plate column
    blk.track("vss", s3 - sw / 2, s4 + sw / 2, y_br)
    blk.track("vpc", jV[0], d3 + sw / 2, y_vpc)
    cx.pin(top, 2, "vpc", jV[0], top_edge - tw, jV[1], top_edge)
    # ---- verticals: gate bars, joiners
    yb0 = cys["L"][0][0] - cx.r("m1_cont_endcap")
    blk.vertical("g", barL[0], barL[1], yb0, top_edge)
    cx.pin(top, 1, "g", barL[0], top_edge - tw, barL[1], top_edge)
    blk.vertical("g", barR[0], barR[1], yb0, cys["R"][-1][1] + cx.r("m1_cont_endcap"))
    # bottom lanes: ea from the left joiner, eb from the right joiner, meeting at the array's centre line
    bot_edge = g.snap(yt0 - cx.r("thickox_over_active"))
    y_lane = g.snap(bot_edge + tw / 2)
    xc = g.snap((x_act0 + x_act1) / 2)
    ea_r, eb_l = g.snap(xc - sp2 / 2), g.snap(xc + sp2 / 2)
    blk.track("ea", jA[0], ea_r, y_lane)
    blk.track("eb", eb_l, jB[1], y_lane)
    cx.pin(top, 2, "ea", ea_r - tw, bot_edge, ea_r, bot_edge + tw)
    cx.pin(top, 2, "eb", eb_l, bot_edge, eb_l + tw, bot_edge + tw)
    ty = {n: [t["y"] for t in blk.tracks if t["net"] == n] for n in ("ea", "eb", "vpc")}
    blk.vertical("ea", jA[0], jA[1], bot_edge, max(ty["ea"]) + tw / 2)
    blk.vertical("eb", jB[0], jB[1], bot_edge, max(ty["eb"]) + tw / 2)
    blk.vertical("vpc", jV[0], jV[1], min(ty["vpc"]) - tw / 2, top_edge)
    cx.pin(top, 1, "vss", tb[0], tb[1], tb[0] + tw, tb[3])
    blk.wire()
    tox = g.outline(cx, top, "thickox", [("active", cx.r("thickox_over_active")), ("thickox", 0.0)],
                    cx.r("thickox_space"))
    # device names
    for name, r in blk.rows:
        for f in r:
            cx.text(top, "note", VO[f.letter][0], (f.x0 + f.x1) / 2, (f.y0 + f.y1) / 2)
    cx.text(top, "note", "MS3", x3 + m3.lact / 2, yE + m3.W / 2)
    cx.text(top, "note", "SKS", x4 + mk.lact / 2, yE + mk.W / 2)
    # reference netlist, devices as drawn
    devl = []
    for name, r in blk.rows:
        for f in r:
            nm, D, G, S = VO[f.letter]
            devl.append(("%s_%s_%d" % (nm, name, f.idx), D, G, S, "vss", model, f.mos.W, f.mos.L))
    devl.append(("MS3", "vpc", "ks", "vss", "vss", model, m3.W, m3.L))
    devl.append(("SKS", "ks", "en_3v3_b", "vss", "vss", model, mk.W, mk.L))
    opt = db.SaveLayoutOptions()
    opt.gds2_write_timestamps = False
    ly.write(os.path.join(OUT, "bg_n_cells_v1.gds"), opt)
    hdr = ("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
           "* bg_n_cells.cdl: reference netlist of bg_n_cells.gds, devices as drawn (one line per finger, dummies\n"
           "* included), generated by build_bg_n.py 2026-10-28 (Claude, Opus 5.5).\n\n")
    g.write_cdl(os.path.join(OUT, "bg_n_cells_v1.cdl"), [("bg_n4", PORTS, devl)], hdr)
    return P, dict(bbox=top.dbbox(), ties=(tb, tt), tie_y=(yt0, yt1), x3=x3, x4=x4, yE=yE, xc=xc)


if __name__ == "__main__":
    P, geo = build()
    print("bg_n4:", geo)
    print("rules used:")
    for k, (v, why) in P.citations().items():
        print("  %-20s %-7g %s" % (k, v, why))
