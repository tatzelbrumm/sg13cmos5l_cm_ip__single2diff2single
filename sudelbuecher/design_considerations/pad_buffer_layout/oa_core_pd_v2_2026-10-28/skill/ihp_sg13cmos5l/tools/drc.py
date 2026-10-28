# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Python DRC on klayout.db for oa_core_pd and its primitives (IHP sg13cmos5l), written 2026-10-28 by Claude.

Why not IHP's deck: it needs KLayout >= 0.29.11 with Ruby; the cloud container has klayout.db 0.30.12 (no
Ruby) and KLayout 0.28.16, the source build was blocked by the network policy, and the uploaded PDK copy lacks
include files of the main deck (layers_def.drc, 5_5_activ, 5_8_gatpoly, 5_16_metal1, 7_2_latchup, ...).

Every value is read from libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json (key in the
report); the check semantics follow the deck file named in the report. "json only" = the file implementing
the rule is not in the uploaded deck; the check is the rule's plain reading (width / space / area).
Flat checks on the merged layout of one cell. Not covered: density, fillers, slits, seal ring, pads, rules for
devices that are not in these cells (resistors, BJT, varicap, ESD), Cnt.b1 / V1.b1 (contact / via arrays).

    python3 drc.py <gds> <cell> [report.txt]      (or run(layout_object, cellname) from Python)
"""
import json
import sys
import klayout.db as db

DECK = "/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/"
R = json.load(open(DECK + "sg13cmos5l_tech_default.json"))["drc_rules"]
J = "sg13cmos5l_tech_default.json"
MAX = "sg13cmos5l_maximal.drc"
EUC, PROJ = db.Metrics.Euclidian, db.Metrics.Projection


def _layout(gds):
    if isinstance(gds, db.Layout):          # in-memory layout (generator.py gap search)
        return gds
    ly = db.Layout()
    ly.read(gds)
    return ly


def run(gds, cellname, skip=()):
    ly = _layout(gds)
    cell = ly.cell(cellname)
    dbu = ly.dbu
    u = lambda v: int(round(float(v) / dbu))

    def Lraw(l, d=0):
        li = ly.find_layer(l, d)
        return db.Region(cell.begin_shapes_rec(li)) if li is not None else db.Region()

    L = lambda l, d=0: Lraw(l, d).merged()
    act, poly, cont, nsd, m1, m1p, m2, m2p, psd, v1, nw, tgo = (L(1), L(5), L(6), L(7), L(8), L(8, 2), L(10),
                                                                L(10, 2), L(14), L(19), L(31), L(44))
    nsdb, pwb = L(7, 21), L(46, 21)
    chip = db.Region(cell.bbox()).sized(u(30.0))
    # derivations as in ihp-sg13cmos5l.drc and sg13cmos5l_maximal.drc (nSD_drv, NAct, PAct, X1, Gate)
    nact = act & (nsd + (act - (nsdb + psd)))
    pact = act - nact
    x1 = nw + pwb
    gate = act & poly
    ngate = gate & nact
    pgate = gate - ngate
    nact_nw, pact_nw, nact_pw, pact_pw = nact & x1, pact & x1, nact - x1, pact - x1
    ntap, ptap = nact_nw - poly, pact_pw - poly
    hv = lambda r: r & tgo
    lv = lambda r: r - tgo
    res = []

    def rep(rule, desc, src, r):
        if isinstance(r, db.EdgePairs):
            boxes = [ep.bbox() for ep in r.each()]
        elif isinstance(r, db.Edges):
            boxes = [e.bbox() for e in r.each()]
        else:
            boxes = [p.bbox() for p in r.each()]
        res.append((rule, desc, src, len(boxes), [b.to_dtype(dbu) for b in boxes[:4]]))

    width = lambda r, v: r.width_check(u(v), False, EUC)
    space = lambda r, v: r.space_check(u(v), False, EUC)
    sep = lambda a, b, v: a.separation_check(b, u(v), False, EUC)
    enc = lambda outer, inner, v: outer.enclosing_check(inner, u(v), False, EUC)
    small = lambda r, a: r.with_area(0, int(round(a / dbu / dbu)), False)
    partial = lambda inner, outer: inner.interacting(outer) - inner.inside(outer)

    def wide_space(m, w, s, run_):
        """as Mn.e in beol/5_17_metaln.drc: space < s next to the parts of m wider than w, parallel run > run_.
        Pairs inside one merged polygon (notches) are left to the plain space rule."""
        wide = m.sized(-u(w / 2)).sized(u(w / 2))
        ep = db.EdgePairs()
        for p in m.each():
            wp = wide & db.Region(p)
            if not wp.is_empty():
                ep += wp.separation_check(m - db.Region(p), u(s), False, PROJ, None, u(run_) + 1, None)
        return ep

    def endcap(cuts, metal, e):
        """M1.c1 / V1.c1 / M2.c1 (maximal): metal reaches >= e beyond the cut on two opposite sides."""
        bad = db.Region()
        for c in cuts.each():
            b = c.bbox()
            bx = db.Region(db.Box(b.left - u(e), b.bottom, b.right + u(e), b.top))
            by = db.Region(db.Box(b.left, b.bottom - u(e), b.right, b.top + u(e)))
            if not (bx - metal).is_empty() and not (by - metal).is_empty():
                bad.insert(c)
        return bad

    # ---- geometry, forbidden layers
    off = db.EdgePairs()
    for li in ly.layer_indexes():
        i = ly.get_info(li)
        off += Lraw(i.layer, i.datatype).grid_check(u(R["grid"]), u(R["grid"]))
    rep("OffGrid", "all shapes on the %g um grid" % R["grid"], "geometry/3_1_offgrid.drc; %s grid" % J, off)
    bad_ang = db.Edges()
    for l, d in ((6, 0), (19, 0)):
        bad_ang += L(l, d).edges().with_angle(db.Edges.OrthoEdges, True)
    for l, d in ((1, 0), (5, 0), (8, 0), (10, 0), (30, 0)):
        bad_ang += L(l, d).edges().with_angle(db.Edges.OrthoDiagonalEdges, True)
    rep("Angle", "Cont/Via1 orthogonal; Activ/GatPoly/M1-M3 0/45/90 deg", "geometry/3_2_angle.drc", bad_ang)
    forb = db.Region()
    for l, d in ((67, 0), (67, 22), (66, 0), (134, 0), (134, 22), (133, 0), (26, 0), (32, 0), (36, 0), (129, 0)):
        forb += L(l, d)
    rep("CMOS5L.FORB", "no Metal5/Via4/TM2/TV2/TRANS/nBuLay/MIM/Vmim", "forbidden/3_2_forbidden_cmos5l.drc", forb)

    # ---- NWell; net of each NWell polygon from NWell - ntap - Cont - M1 - Via1 - M2 connectivity
    rep("NW.a", "NWell width >= %g" % R["NW_a"], MAX + " NW.a", width(nw, R["NW_a"]))
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, cell, []))
    g = {k: l2n.make_layer(ly.layer(*v), k) for k, v in (("nw", (31, 0)), ("act", (1, 0)), ("cont", (6, 0)),
                                                        ("m1", (8, 0)), ("v1", (19, 0)), ("m2", (10, 0)), ("psd", (14, 0)))}
    nt = (g["act"] & g["nw"]) - g["psd"]
    l2n.register(nt, "ntap")
    for k in ("nw", "m1", "m2"):
        l2n.connect(g[k])
    for a, b in ((g["nw"], nt), (nt, g["cont"]), (g["cont"], g["m1"]), (g["m1"], g["v1"]), (g["v1"], g["m2"])):
        l2n.connect(a, b)
    l2n.extract_netlist()
    nwp = list(nw.each())
    nid = []
    for k, p in enumerate(nwp):
        e = list(p.each_edge())[0]
        q = db.DPoint((e.p1.x + e.p2.x) / 2 * dbu, (e.p1.y + e.p2.y) / 2 * dbu)
        cand = [q + db.DVector(dx, dy) for dx in (-0.01, 0.01) for dy in (-0.01, 0.01)]
        net = None
        for c in cand:
            if p.inside(db.Point(round(c.x / dbu), round(c.y / dbu))):
                net = l2n.probe_net(g["nw"], c)
                break
        nid.append(net.cluster_id if net else -1 - k)
    nwb, nwb1 = nw.notch_check(u(R["NW_b"])), db.EdgePairs()
    for i in range(len(nwp)):
        for j in range(i + 1, len(nwp)):
            a, b = db.Region(nwp[i]), db.Region(nwp[j])
            if nid[i] == nid[j]:
                nwb += a.separation_check(b, u(R["NW_b"]))
            else:
                nwb1 += a.separation_check(b, u(R["NW_b1"]))
    rep("NW.b", "NWell space, same net >= %g" % R["NW_b"], "feol/5_1_nwell.drc NW.b", nwb)
    rep("NW.b1", "NWell space, different nets >= %g" % R["NW_b1"], "feol/5_1_nwell.drc NW.b1", nwb1)
    rep("NW.c", "NWell encl. of P+Activ, no TGO >= %g" % R["NW_c"], MAX + " NW.c", enc(nw, lv(pact_nw), R["NW_c"]))
    rep("NW.c1", "NWell encl. of P+Activ in TGO >= %g" % R["NW_c1"], MAX + " NW.c1", enc(nw, hv(pact_nw), R["NW_c1"]))
    rep("NW.c/x", "P+Activ crossing the NWell edge", MAX + " NW.c/c1 (overlap = error)", partial(pact.interacting(pgate), nw))
    rep("NW.d", "NWell space to N+Activ, no TGO >= %g" % R["NW_d"], MAX + " NW.d", sep(nw, lv(nact_pw), R["NW_d"]))
    rep("NW.d1", "NWell space to N+Activ in TGO >= %g" % R["NW_d1"], MAX + " NW.d1", sep(nw, hv(nact_pw), R["NW_d1"]))
    rep("NW.e", "NWell encl. of NWell tie, no TGO >= %g" % R["NW_e"], MAX + " NW.e", enc(nw, lv(ntap), R["NW_e"]))
    rep("NW.e1", "NWell encl. of NWell tie in TGO >= %g" % R["NW_e1"], MAX + " NW.e1", enc(nw, hv(ntap), R["NW_e1"]))
    rep("NW.f", "NWell space to substrate tie, no TGO >= %g" % R["NW_f"], MAX + " NW.f", sep(nw, lv(ptap), R["NW_f"]))
    rep("NW.f1", "NWell space to substrate tie in TGO >= %g" % R["NW_f1"], "feol/5_1_nwell.drc NW.f1", sep(nw, hv(ptap), R["NW_f1"]))

    # ---- Activ, ThickGateOx, GatPoly, pSD
    rep("Act.a", "Activ width >= %g" % R["Act_a"], J + " Act_a (json only)", width(act, R["Act_a"]))
    rep("Act.b", "Activ space >= %g" % R["Act_b"], J + " Act_b (json only)", space(act, R["Act_b"]))
    rep("Act.d", "Activ area >= %g" % R["Act_d"], MAX + " Act.d", small(act, R["Act_d"]))
    rep("TGO.a", "TGO extension over Activ >= %g" % R["TGO_a"], MAX + " TGO.a", enc(tgo, act & tgo, R["TGO_a"]))
    rep("TGO.b", "TGO space to Activ outside TGO >= %g" % R["TGO_b"], MAX + " TGO.b", sep(tgo, act.outside(tgo), R["TGO_b"]))
    rep("TGO.a/x", "Activ crossing the TGO edge", MAX + " TGO.a/b", partial(act, tgo))
    rep("TGO.c", "TGO extension over HV gate >= %g" % R["TGO_c"], MAX + " TGO.c", enc(tgo, hv(gate), R["TGO_c"]))
    rep("TGO.d", "TGO space to gate outside TGO >= %g" % R["TGO_d"], MAX + " TGO.d", sep(tgo, gate.outside(tgo), R["TGO_d"]))
    rep("TGO.e", "TGO space >= %g" % R["TGO_e"], MAX + " TGO.e", space(tgo, R["TGO_e"]))
    rep("TGO.f", "TGO width >= %g" % R["TGO_f"], J + " TGO_f (derivation ThickGateOx_TGO_f in maximal)", width(tgo, R["TGO_f"]))
    rep("Gat.a", "GatPoly width >= %g" % R["Gat_a"], J + " Gat_a (json only)", width(poly, R["Gat_a"]))
    sd = act - poly
    glen = lambda gt, v: (gt.edges() & sd.edges()).width_check(u(v), False, PROJ)   # gate edges on S/D = L
    rep("Gat.a3", "HV NFET gate length >= %g" % R["Gat_a3"], MAX + " Gat.a3", glen(hv(ngate), R["Gat_a3"]))
    rep("Gat.a4", "HV PFET gate length >= %g" % R["Gat_a4"], MAX + " Gat.a4", glen(hv(pgate), R["Gat_a4"]))
    rep("Gat.b", "GatPoly space >= %g" % R["Gat_b"], J + " Gat_b (json only)", space(poly, R["Gat_b"]))
    rep("Gat.b1", "space between HV gates over Activ >= %g" % R["Gat_b1"], MAX + " Gat.b1", space(hv(gate), R["Gat_b1"]))
    cap = db.Region()                       # Gat.c: poly must extend >= Gat_c beyond each Activ edge under it
    for e in act.edges().inside_part(poly).each():
        n = db.DVector(-e.dy(), e.dx())
        n = n * (u(R["Gat_c"]) / n.length())
        nv = db.Vector(round(n.x), round(n.y))
        for s in (1, -1):
            b = db.Region(db.Polygon([e.p1, e.p2, e.p2 + nv * s, e.p1 + nv * s]))
            if (b & act).area() == 0 and not (b - poly).is_empty():
                cap += b
    rep("Gat.c", "GatPoly end cap over Activ >= %g" % R["Gat_c"], MAX + " Gat.c", cap)
    rep("Gat.d", "GatPoly (field) space to Activ >= %g" % R["Gat_d"], J + " Gat_d (json only)", (poly - act).separation_check(act, u(R["Gat_d"]), zero_distance_mode=db.ZeroDistanceMode.NeverIncludeZeroDistance))
    rep("Gat.e", "GatPoly area >= %g" % R["Gat_e"], MAX + " Gat.e", small(poly, R["Gat_e"]))
    rep("pSD.a", "pSD width >= %g" % R["pSD_a"], MAX + " pSD.a", width(psd, R["pSD_a"]))
    rep("pSD.b", "pSD space >= %g" % R["pSD_b"], MAX + " pSD.b", space(psd, R["pSD_b"]))
    rep("pSD.c", "pSD encl. of P+Activ in NWell >= %g" % R["pSD_c"], MAX + " pSD.c", enc(psd, act & nw & psd, R["pSD_c"]))
    rep("pSD.d", "pSD space to N+Activ in PWell >= %g" % R["pSD_d"], MAX + " pSD.d", sep(psd, nact_pw, R["pSD_d"]))
    rep("pSD.i1", "pSD encl. of HV PFET gate >= %g" % R["pSD_i1"], MAX + " pSD.i1", enc(psd, hv(pgate), R["pSD_i1"]))
    rep("pSD.j1", "pSD space to HV NFET gate >= %g" % R["pSD_j1"], MAX + " pSD.j1", sep(psd, hv(ngate), R["pSD_j1"]))

    # ---- Cont
    cr = Lraw(6).merged()
    rep("Cnt.a", "Cont size = %g" % R["Cnt_a"], "feol/5_14_cont.drc Cnt.a",
        cr.non_squares() + cr.with_bbox_width(u(R["Cnt_a"]), u(R["Cnt_a"]) + 1, True))
    rep("Cnt.b", "Cont space >= %g" % R["Cnt_b"], "feol/5_14_cont.drc Cnt.b", space(cont, R["Cnt_b"]))
    rep("Cnt.c", "Activ encl. of Cont >= %g" % R["Cnt_c"], "feol/5_14_cont.drc Cnt.c", enc(act, cont & act, R["Cnt_c"]))
    rep("Cnt.d", "GatPoly encl. of Cont >= %g" % R["Cnt_d"], "feol/5_14_cont.drc Cnt.d", enc(poly, cont & poly, R["Cnt_d"]))
    rep("Cnt.e", "Cont on GatPoly space to Activ >= %g" % R["Cnt_e"], "feol/5_14_cont.drc Cnt.e", sep(cont & poly, act, R["Cnt_e"]))
    rep("Cnt.f", "Cont on Activ space to GatPoly >= %g" % R["Cnt_f"], MAX + " Cnt.f", sep(cont & act, poly, R["Cnt_f"]))
    rep("Cnt.g", "Cont inside Activ or GatPoly", MAX + " Cnt.g", cont - act - poly)
    rep("Cnt.h", "Cont covered by Metal1 (M1.c, 0)", MAX + " Cnt.h / M1.c", cont - m1)
    rep("Cnt.j", "no Cont on gate", MAX + " Cnt.j", cont & gate)

    # ---- Metal1, Via1, Metal2
    rep("M1.a", "M1 width >= %g" % R["M1_a"], J + " M1_a (json only; as Mn.a in beol/5_17_metaln.drc)", width(m1, R["M1_a"]))
    rep("M1.b", "M1 space >= %g" % R["M1_b"], J + " M1_b (json only; as Mn.b)", space(m1, R["M1_b"]))
    rep("M1.c1", "M1 endcap encl. of Cont >= %g" % R["M1_c1"], MAX + " M1.c1", endcap(cont, m1, R["M1_c1"]))
    rep("M1.d", "M1 area >= %g" % R["M1_d"], MAX + " M1.d", small(m1, R["M1_d"]))
    rep("M1.e", "M1 space >= %g next to M1 wider than %g, run > %g" % (R["M1_e"], R["M1_e_w"], R["M1_e_cr"]),
        J + " M1_e (json only; as Mn.e)", wide_space(m1, R["M1_e_w"], R["M1_e"], R["M1_e_cr"]))
    rep("M1.f", "M1 space >= %g next to M1 wider than %g, run > %g" % (R["M1_f"], R["M1_f_w"], R["M1_f_cr"]),
        J + " M1_f (json only; as Mn.f)", wide_space(m1, R["M1_f_w"], R["M1_f"], R["M1_f_cr"]))
    vr = Lraw(19).merged()
    rep("V1.a", "Via1 size = %g" % R["V1_a"], "beol/5_19_via1.drc V1.a",
        vr.non_squares() + vr.with_bbox_width(u(R["V1_a"]), u(R["V1_a"]) + 1, True))
    rep("V1.b", "Via1 space >= %g" % R["V1_b"], "beol/5_19_via1.drc V1.b", space(v1, R["V1_b"]))
    rep("V1.c", "M1 encl. of Via1 >= %g" % R["V1_c"], "beol/5_19_via1.drc V1.c", enc(m1, v1, R["V1_c"]))
    rep("V1.c/x", "Via1 not covered by M1", "beol/5_19_via1.drc V1.c", v1 - m1)
    rep("V1.c1", "M1 endcap encl. of Via1 >= %g" % R["V1_c1"], MAX + " V1.c1", endcap(v1, m1, R["V1_c1"]))
    rep("M2.a", "M2 width >= %g" % R["Mn_a"], "beol/5_17_metaln.drc M2.a", width(m2, R["Mn_a"]))
    rep("M2.b", "M2 space >= %g" % R["Mn_b"], "beol/5_17_metaln.drc M2.b", space(m2, R["Mn_b"]))
    rep("M2.c", "M2 encl. of Via1 >= %g" % R["Mn_c"], MAX + " M2.c", enc(m2, v1, R["Mn_c"]))
    rep("M2.c/x", "Via1 not covered by M2", MAX + " M2.c", v1 - m2)
    M2_C1 = 0.05      # no json key: literal of rule M2.c1 in sg13cmos5l_maximal.drc ("... = 0.05")
    rep("M2.c1", "M2 endcap encl. of Via1 >= %g" % M2_C1, MAX + " M2.c1 (value from the deck text)", endcap(v1, m2, M2_C1))
    rep("M2.d", "M2 area >= %g" % R["Mn_d"], MAX + " M2.d", small(m2, R["Mn_d"]))
    rep("M2.e", "M2 space >= %g next to M2 wider than %g, run > %g" % (R["Mn_e"], R["Mn_e_w"], R["Mn_e_cr"]),
        "beol/5_17_metaln.drc M2.e", wide_space(m2, R["Mn_e_w"], R["Mn_e"], R["Mn_e_cr"]))
    rep("M2.f", "M2 space >= %g next to M2 wider than %g, run > %g" % (R["Mn_f"], R["Mn_f_w"], R["Mn_f_cr"]),
        "beol/5_17_metaln.drc M2.f", wide_space(m2, R["Mn_f_w"], R["Mn_f"], R["Mn_f_cr"]))
    rep("Pin.e", "Metal1.pin inside Metal1", "pin/7_4_pin.drc Pin.e", m1p - m1)
    rep("Pin.f_M2", "Metal2.pin inside Metal2", "pin/7_4_pin.drc Pin.f_M2", m2p - m2)
    rep("M3+", "no Via2 / Metal3 / Via3 / Metal4 / TopVia1 / TopMetal1 (slot keeps them)", "brief",
        L(29) + L(30) + L(49) + L(50) + L(125) + L(126))

    # ---- latch-up: every MOS S/D within LU_a / LU_b of a tie, measured inside the well (as LU.a in maximal)
    def lu(dev_sd, ties, well, dist):
        reach = ties.dup()
        step = u(0.5)
        for _ in range(int(round(dist / 0.5))):
            reach = (reach.sized(step) & well) | reach
        return dev_sd - reach
    pwell_r = chip - nw
    rep("LU.a", "P+Activ in NWell within %g um of an NWell tie" % R["LU_a"], MAX + " LU.a",
        lu(pact_nw - poly, ntap, nw, R["LU_a"]))
    rep("LU.b", "N+Activ in PWell within %g um of a substrate tie" % R["LU_b"],
        J + " LU_b (json only; implementation 7_2_latchup.drc not in the upload; read as LU.a for NMOS)",
        lu(nact_pw - poly, ptap, pwell_r, R["LU_b"]))
    return res


def antenna(gds, cellname):
    """Ant.b / Ant.d as in antenna.drc (full connectivity): per net without S/D diffusion, cumulative M1+M2 area
    and Via1 area relative to the connected gate area."""
    ly = _layout(gds)
    cell = ly.cell(cellname)
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, cell, []))
    g = {k: l2n.make_layer(ly.layer(*v), k) for k, v in (("act", (1, 0)), ("poly", (5, 0)), ("cont", (6, 0)),
                                                        ("m1", (8, 0)), ("v1", (19, 0)), ("m2", (10, 0)))}
    gate = g["act"] & g["poly"]
    sd = g["act"] - g["poly"]
    pol = g["poly"] - g["act"]
    for k in ("m1", "m2"):
        l2n.connect(g[k])
    l2n.register(gate, "gate"); l2n.register(sd, "sd"); l2n.register(pol, "pol")
    l2n.connect(gate); l2n.connect(sd); l2n.connect(pol)
    for a, b in ((pol, gate), (pol, g["cont"]), (sd, g["cont"]), (g["cont"], g["m1"]), (g["m1"], g["v1"]),
                 (g["v1"], g["m2"])):
        l2n.connect(a, b)
    for (l, d), m in (((8, 25), g["m1"]), ((10, 25), g["m2"])):
        if ly.find_layer(l, d) is not None:
            l2n.connect(m, l2n.make_text_layer(ly.find_layer(l, d), "t%d" % l))
    l2n.extract_netlist()
    worst = []
    circ = l2n.netlist().circuit_by_name(cellname)
    if circ is None:                           # nothing extracted (no nets in the cell)
        return worst
    for net in circ.each_net():
        area = {}
        for k, lay in (("gate", gate), ("sd", sd), ("m1", g["m1"]), ("m2", g["m2"]), ("v1", g["v1"])):
            area[k] = l2n.shapes_of_net(net, lay, True).merged().area() * ly.dbu ** 2
        if area["gate"] > 0 and area["sd"] == 0:
            worst.append((net.expanded_name(), area["gate"], (area["m1"] + area["m2"]) / area["gate"], area["v1"] / area["gate"]))
    return worst


if __name__ == "__main__":
    gds, cellname = sys.argv[1], sys.argv[2]
    out = open(sys.argv[3], "w") if len(sys.argv) > 3 else sys.stdout
    res = run(gds, cellname)
    nerr = sum(r[3] for r in res)
    out.write("# DRC (Python, klayout.db %s) of cell %s in %s\n# values: %s%s\n" % (db.__version__ if hasattr(db, "__version__") else "", cellname, gds, DECK, J))
    for rule, desc, src, n, boxes in res:
        out.write("%-11s %5d  %-62s [%s]%s\n" % (rule, n, desc, src, ("  e.g. " + " ".join(str(b) for b in boxes)) if n else ""))
    ant = antenna(gds, cellname)
    bad = [a for a in ant if a[2] >= R["Ant_b"] or a[3] >= R["Ant_d"]]
    for a in ant:
        out.write("antenna net %-12s gate %8.3f um2  (M1+M2)/gate %7.2f (Ant.b < %g)  Via1/gate %6.3f (Ant.d < %g)\n"
                  % (a[0], a[1], a[2], R["Ant_b"], a[3], R["Ant_d"]))
    out.write("TOTAL %d violations (%d rules checked), antenna violations %d\n" % (nerr, len(res), len(bad)))
    print("%s: %d violations in %d rules, antenna violations %d" % (cellname, nerr, len(res), len(bad)))
