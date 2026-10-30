# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Process adapter: IHP sg13cmos5l (3.3 V HV PMOS primitives), 2026-10-28, Claude.

Everything process-specific that ../generator.py needs, each item with its source. The generator only uses the
generic names on the left; to port, write another file with the same names (SKILL_draft.md, "porting").

    import process.ihp_sg13cmos5l as P
    P.rule("m1_space") -> 0.18 (um);  P.src("m1_space") -> "json M1_b (Min. Metal1 space)"
    P.layer("m1") -> (8, 0);  P.device(layout, "pmos_hv", w, l) -> cell;  P.model("pmos_hv") -> "sg13_hv_pmos"

The DRC deck folder is read from $PDK_DRC_DECKS, default the uploaded IHP-Open-PDK copy.
"""
import json
import math
import os

NAME = "ihp_sg13cmos5l"
DECKS = os.environ.get("PDK_DRC_DECKS",
                       "/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/")
JSON = "sg13cmos5l_tech_default.json"
_R = json.load(open(os.path.join(DECKS, JSON)))["drc_rules"]
MAX = "sg13cmos5l_maximal.drc"

# ------------------------------------------------------------------------------------------------ layers
# generic name: ((layer, datatype), source)
LAYERS = {
    "diff":     ((1, 0), MAX + ":1455 Activ"),
    "poly":     ((5, 0), MAX + ":1460 GatPoly"),
    "poly_pin": ((5, 2), MAX + ":1461 GatPoly_pin (drawn by the PCell)"),
    "contact":  ((6, 0), MAX + ":1464 Cont"),
    "m1":       ((8, 0), MAX + ":1467 Metal1"),
    "m1_pin":   ((8, 2), MAX + ":1468 Metal1_pin"),
    "m1_text":  ((8, 25), "Metal1 text: the library's pin convention (pad_buffer_cells.gds); LVS labels"),
    "m2":       ((10, 0), MAX + ":1473 Metal2"),
    "m2_pin":   ((10, 2), MAX + ":1474 Metal2_pin"),
    "m2_text":  ((10, 25), "Metal2 text: as m1_text"),
    "pimp":     ((14, 0), MAX + ":1478 pSD"),
    "via1":     ((19, 0), MAX + ":1480 Via1"),
    "well":     ((31, 0), MAX + ":1490 NWell"),
    "hvox":     ((44, 0), MAX + ":1498 ThickGateOx"),
    "heat":     ((51, 0), "drawn by the pmosHV PCell (thermal marker); not read by the DRC deck"),
    "text":     ((63, 0), MAX + ":1508 TEXT (device tags)"),
}

# ------------------------------------------------------------------------------------------------ rules
# generic name: (json key, or None with a literal, description / source)
RULES = {
    "grid":               ("grid", "drawing grid (geometry/3_1_offgrid.drc)"),
    "diff_width":         ("Act_a", "Min. Activ width"),
    "diff_space":         ("Act_b", "Min. Activ space"),
    "finger_gap":         ("Gat_b1", "Min. space between unrelated 3.3 V GatPoly over Activ; with end caps Gat_c the "
                                     "poly merges into one gate strip"),
    "gate_len_min":       ("Gat_a4", "Min. GatPoly width = channel length, 3.3 V PFET"),
    "poly_endcap":        ("Gat_c", "Min. GatPoly extension over Activ (end cap)"),
    "poly_to_diff":       ("Gat_d", "Min. GatPoly (field) space to Activ"),
    "contact_size":       ("Cnt_a", "Cont size"),
    "contact_space":      ("Cnt_b", "Min. Cont space"),
    "diff_encl_contact":  ("Cnt_c", "Min. Activ enclosure of Cont"),
    "poly_encl_contact":  ("Cnt_d", "Min. GatPoly enclosure of Cont"),
    "poly_contact_to_diff": ("Cnt_e", "Min. Cont on GatPoly space to Activ"),
    "diff_contact_to_gate": ("Cnt_f", "Min. Cont on Activ space to GatPoly"),
    "m1_width":           ("M1_a", "Min. Metal1 width"),
    "m1_space":           ("M1_b", "Min. Metal1 space"),
    "m1_encl_contact":    ("M1_c", "Min. Metal1 enclosure of Cont"),
    "m1_endcap_contact":  ("M1_c1", "Min. Metal1 endcap enclosure of Cont"),
    "m1_area":            ("M1_d", "Min. Metal1 area (um2)"),
    "m1_wide_space":      ("M1_e", "Min. Metal1 space next to Metal1 wider than M1_e_w, parallel run > M1_e_cr"),
    "m1_wide_width":      ("M1_e_w", "Metal1 counts as wide for M1_e above this width"),
    "m1_wide_run":        ("M1_e_cr", "M1_e applies above this parallel run"),
    "via1_size":          ("V1_a", "Via1 size"),
    "via1_space":         ("V1_b", "Min. Via1 space"),
    "m1_encl_via1":       ("V1_c", "Min. Metal1 enclosure of Via1"),
    "m1_endcap_via1":     ("V1_c1", "Min. Metal1 endcap enclosure of Via1"),
    "m2_width":           ("Mn_a", "Min. Metal2 width"),
    "m2_space":           ("Mn_b", "Min. Metal2 space"),
    "m2_encl_via1":       ("Mn_c", "Min. Metal2 enclosure of Via1"),
    "m2_endcap_via1":     (None, 0.05, MAX + " rule text M2.c1 'Min. Metal2 endcap enclosure of Via1 = 0.05' (no json key)"),
    "well_width":         ("NW_a", "Min. NWell width"),
    "well_space_same":    ("NW_b", "Min. NWell space or notch, same net (merged below this)"),
    "well_space_diff":    ("NW_b1", "Min. PWell width between NWell regions, different nets"),
    "well_encl_pdiff":    ("NW_c1", "Min. NWell enclosure of P+Activ inside ThickGateOx"),
    "well_encl_tap":      ("NW_e1", "Min. NWell enclosure of an NWell tie in N+Activ inside ThickGateOx"),
    "well_to_ndiff":      ("NW_d1", "Min. NWell space to external N+Activ inside ThickGateOx"),
    "pimp_encl_pdiff":    ("pSD_c", "Min. pSD enclosure of P+Activ in NWell"),
    "pimp_encl_gate":     ("pSD_i1", "Min. pSD enclosure of PFET gate inside ThickGateOx"),
    "pimp_to_ntap":       ("pSD_d1", "Min. pSD space to N+Activ in NWell"),
    "hvox_encl_diff":     ("TGO_a", "Min. ThickGateOx extension over Activ"),
    "hvox_encl_gate":     ("TGO_c", "Min. ThickGateOx extension over GatPoly over Activ"),
    "hvox_space":         ("TGO_e", "Min. ThickGateOx space (merged below this)"),
    "lu_tap_dist":        ("LU_a", MAX + " LU.a: Max. space from any portion of P+Activ inside NWell to an nSD-NWell "
                                   "tie (grown inside NWell)"),
    "lu_tap_cont_ext":    ("LU_d", MAX + " LU.d: Max. extension of NWell tie Activ beyond Cont"),
}
# deck facts that are not numbers
WELL_45 = True        # geometry/3_2_angle.drc: NWell is only in ACUTE_SCOPE_LAYERS (no corner < 87 deg); it is in
                      # neither ORTHO_ONLY_LAYERS nor ORTHO_45_LAYERS, so 45-degree well edges are legal (on grid)
HVOX_LIKE_WELL = True  # the pmosHV PCell draws ThickGateOx = its NWell box (NW_c1 > TGO_a); merged regions keep TGO.e
TAP_COUNTS = "N+Activ in NWell, not under pSD (ntap); the deck's all_ntie = ntap + soft_n_tie (" + MAX + ":1864)"


def rule(name):
    e = RULES[name]
    return float(e[1]) if e[0] is None else float(_R[e[0]])


def src(name):
    e = RULES[name]
    return ("%s literal %g: %s" % (NAME, e[1], e[2])) if e[0] is None else "%s %s = %g (%s)" % (JSON, e[0], _R[e[0]], e[1])


def layer(name):
    return LAYERS[name][0]


# ------------------------------------------------------------------------------------------------ devices
DEVICES = {
    "pmos_hv": dict(
        model="sg13_hv_pmos",
        builder="pmos_hv (below): geometry of the SG13 pmosHV PCell, ng = 1, from json keys; checked XOR 0 against "
                "all 15 single-finger pmosHV cells of pad_buffer_cells.gds (w 0.5 ... 16, l 0.45 ... 16)",
        lvs="gate = Activ & GatPoly on P+Activ (Activ & pSD) in NWell under ThickGateOx; S/D = Activ - GatPoly; "
            "bulk = the NWell polygon (derivations of ihp-sg13cmos5l.drc / " + MAX + "; IHP's run_lvs.py with "
            "--disable_tap_extraction treats the tie as a plain connection)",
        min_w="2 Cnt_c + Cnt_a = 0.30 (one S/D contact); narrower = PCell dog-bone, not reproduced",
        min_l="Gat_a4 = 0.40",
        max_finger_w="10 um: SG13_dev PCell finger limit (pad_buffer_cells klayout/README.md, netlist change 4)",
        mismatch="sg13 models carry mm_ok; Monte-Carlo mismatch is vacuous on an extracted netlist (project CLAUDE.md)",
    ),
}
PEX = ("no PEX rule files in the uploaded PDK copy: nothing in these generators depends on R / C values. Project "
       "facts (CLAUDE.md): Magic full-RC PEX not reproducible (R 574 / 833 / 376 for one geometry), use EXT_MODE=2; "
       "Magic splits ng = 20 into 20 fingers; mismatch MC must run on the schematic.")


def model(kind):
    return DEVICES[kind]["model"]


def device(ly, kind, w, l, name=None):
    if kind != "pmos_hv":
        raise KeyError(kind)
    return pmos_hv(ly, w, l, name)


def pmos_hv(ly, w, l, name=None):
    """SG13 pmosHV PCell geometry (pmosHV_code.py construction), ng = 1. Frame: x along L (S at x = 0), y along W.
    Contacts Cnt_a at Cnt_c from the S/D ends, spread over W at >= Cnt_b, each position floored to the grid;
    gate Cnt_f from the contacts; Metal1 over each column (M1_c, endcap M1_c1); pSD pSD_c around Activ and pSD_i1
    around the gate; NWell NW_c1; ThickGateOx max(NW_c1, TGO_a / TGO_c); poly end caps Gat_c."""
    import klayout.db as db
    U = lambda v: int(round(v * 1000))
    gr = U(_R["grid"])
    cs, cd, cao = U(_R["Cnt_a"]), U(_R["Cnt_b"]), U(_R["Cnt_c"])
    cmo, endcap, gc = U(_R["M1_c"]), U(_R["M1_c1"]), U(_R["Cnt_f"])
    psd_o, psd_g, nw_o = U(_R["pSD_c"]), U(_R["pSD_i1"]), U(_R["NW_c1"])
    gat_o, tgo_g, tgo_a = U(_R["Gat_c"]), U(_R["TGO_c"]), U(_R["TGO_a"])
    W, Lg = U(w), U(l)
    if W < 2 * cao + cs:
        raise ValueError("w below one S/D contact (2 Cnt_c + Cnt_a)")
    c = ly.create_cell(name or "pmosHV_w%s_l%s" % (("%g" % w).replace(".", "p"), ("%g" % l).replace(".", "p")))
    L_ = lambda k: ly.layer(*LAYERS[k][0])
    bx = lambda k, x1, y1, x2, y2: c.shapes(L_(k)).insert(db.Box(x1, y1, x2, y2))
    ny = int(math.floor((W - 2 * cao + cd) / (cs + cd) + 1e-6))
    if ny == 1:
        ys = [(W - cs) // 2]
    else:
        ds = (W - 2 * cao - cs * ny) / (ny - 1)
        ys = [int(math.floor((cao + i * (cs + ds)) / gr + 1e-6)) * gr for i in range(ny)]
    ncont = max(1, int(math.floor((W - 2 * cao + cd - 2 * endcap) / (cs + cd) + 1e-6)))
    off = (W - 2 * cao - ncont * cs - (ncont - 1) * cd) // 2
    off -= off % gr
    ym1, ym2 = min(cao + off - endcap, 0), max(cao + off + cs + (ncont - 1) * (cs + cd) + endcap, W)
    x1c = cao
    xp1 = x1c + cs + gc
    xp2 = xp1 + Lg
    x2c = xp2 + gc
    xd = x2c + cs + cao
    for xc in (x1c, x2c):
        for y in ys:
            bx("contact", xc, y, xc + cs, y + cs)
        bx("m1", xc - cmo, ym1, xc + cs + cmo, ym2)
        bx("m1_pin", xc - cmo, ym1, xc + cs + cmo, ym2)
        bx("diff", xc - cao, 0, xc + cs + cao, cao + cs + cao)
    for k in ("poly", "poly_pin", "heat"):
        bx(k, xp1, -gat_o, xp2, W + gat_o)
    t = db.Text("pmos", db.Trans(db.Vector((xp1 + xp2) // 2, W // 2)))
    t.size = 1
    c.shapes(L_("heat")).insert(t)
    t = db.Text("pmosHV", db.Trans(db.Trans.R90, db.Vector((xp1 + xp2) // 2, W // 2)))
    t.size = 100
    c.shapes(L_("text")).insert(t)
    bx("diff", 0, 0, xd, W)
    bx("pimp", -psd_o, -psd_g, xd + psd_o, W + psd_g)
    bx("well", -nw_o, -nw_o, xd + nw_o, W + nw_o)
    tx = nw_o if nw_o > tgo_a else tgo_a
    ty = nw_o if nw_o > gat_o - tgo_g else gat_o + tgo_g
    bx("hvox", -tx, -ty, xd + tx, W + ty)
    return c


def act_len(l):
    """Activ length of one finger along L: 2 (Cnt_c + Cnt_a + Cnt_f) + l (PCell construction)"""
    return 2 * (rule("diff_encl_contact") + rule("contact_size") + rule("diff_contact_to_gate")) + l


def table():
    """every adapter item with its source, for rules.md"""
    out = ["| generic name | value | source |", "|---|---:|---|"]
    for k in RULES:
        out.append("| `%s` | %g | %s |" % (k, rule(k), src(k)))
    out += ["", "| layer | GDS | source |", "|---|---|---|"]
    for k, (ld, s) in LAYERS.items():
        out.append("| `%s` | %d/%d | %s |" % (k, ld[0], ld[1], s))
    return "\n".join(out)
