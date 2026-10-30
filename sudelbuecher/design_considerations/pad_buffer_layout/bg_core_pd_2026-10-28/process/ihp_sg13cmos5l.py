# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Process adapter: IHP SG13CMOS5L (IHP-Open-PDK, ihp-sg13cmos5l), for generator.py.
Written 2026-10-28 by Claude (Opus 5.5). Every value carries its source. The generator reads ONLY this file for
process facts: layer numbers, rule values, tap / well construction, latch-up, recognition of devices.

To port to another process: copy this file, fill every entry from that PDK (see "porting" in the generic
SKILL_draft.md), and run the self-test cell (generator.selftest) through that PDK's DRC and LVS.
"""
import json
import os

NAME = "ihp_sg13cmos5l"
PDK = "/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l"
DECK = PDK + "/libs.tech/klayout/tech/drc/rule_decks/"
JSON = DECK + "sg13cmos5l_tech_default.json"
MAXIMAL = DECK + "sg13cmos5l_maximal.drc"

# ---- layer map: generic name -> (layer, datatype); source: sg13cmos5l_maximal.drc layer definitions
# (activ_drw 1/0, gatpoly_drw 5/0, cont_drw 6/0, nsd_drw 7/0, metal1_drw 8/0, metal1_pin 8/2, metal1_text 8/25,
#  psd_drw 14/0, metal2_drw 10/0, metal2_pin 10/2, metal2_text 10/25, via1_drw 19/0, nwell_drw 31/0,
#  thickgateox_drw 44/0) and the pin / text convention of pad_buffer_cells.py (<metal>.pin + <metal>.text)
LAYERS = {
    "diff": (1, 0), "poly": (5, 0), "cont": (6, 0), "nimp": (7, 0), "pimp": (14, 0), "nwell": (31, 0),
    "thickox": (44, 0), "m1": (8, 0), "m1.pin": (8, 2), "m1.text": (8, 25), "via1": (19, 0), "m2": (10, 0),
    "m2.pin": (10, 2), "m2.text": (10, 25), "polyres": (128, 0),
    "forbidden_above": [(29, 0), (30, 0), (49, 0), (50, 0), (125, 0), (126, 0)],   # Via2..TopMetal1: kept free
}

# ---- rule values: generic name -> json key of sg13cmos5l_tech_default.json ("drc_rules"); semantics from the
# rule text in sg13cmos5l_maximal.drc (quoted in rules.md)
RULE_KEYS = {
    "grid": "grid",                                    # 3_1_offgrid.drc
    "m1.width": "M1_a", "m1.space": "M1_b", "m1.area": "M1_d", "m1.enc_cont": "M1_c", "m1.enc_cont_end": "M1_c1",
    "m1.wide_width": "M1_e_w", "m1.wide_space": "M1_e", "m1.wide_run": "M1_e_cr",
    "m2.width": "Mn_a", "m2.space": "Mn_b", "m2.area": "Mn_d", "m2.wide_width": "Mn_e_w", "m2.wide_space": "Mn_e",
    "m2.wide_run": "Mn_e_cr",
    "via1.size": "V1_a", "via1.space": "V1_b", "via1.enc": "V1_c", "via1.enc_end": "V1_c1",
    "diff.width": "Act_a", "diff.space": "Act_b", "diff.area": "Act_d",
    "cont.size": "Cnt_a", "cont.space": "Cnt_b", "cont.enc_diff": "Cnt_c",
    "nwell.width": "NW_a", "nwell.space_same": "NW_b", "nwell.space_diff": "NW_b1",
    "nwell.enc_ntap": "NW_e", "nwell.enc_ntap_thick": "NW_e1", "nwell.space_ptap": "NW_f",
    "nwell.space_ptap_thick": "NW_f1", "nwell.enc_pdiff_thick": "NW_c1", "nwell.space_ndiff_thick": "NW_d1",
    "pimp.enc_pdiff": "pSD_c", "pimp.space_ndiff": "pSD_d", "pimp.space": "pSD_b",
    "thickox.space_diff": "TGO_b", "thickox.enc_diff": "TGO_a", "thickox.space": "TGO_e", "thickox.width": "TGO_f",
    "lu.ntap_dist": "LU_a", "lu.ptap_dist": "LU_b", "lu.tap_cont_ext": "LU_d",
}
# NWell outline: 3_2_angle.drc puts nwell_drw only under the acute-corner check (ACUTE_LIMIT_DEG = 87.0), not in
# ORTHO_ONLY_LAYERS / ORTHO_45_LAYERS: any edge angle, no corner below 87 deg; grid 0.005 (3_1_offgrid.drc).
# Activ / GatPoly / Metal1..4: 0/45/90 (ORTHO_45_LAYERS); Cont / Via1: 0/90 (ORTHO_ONLY_LAYERS).
WELL_OUTLINE = dict(any_angle=True, min_corner_deg=87.0, source="geometry/3_2_angle.drc ACUTE_LIMIT_DEG")


def rules():
    R = json.load(open(JSON))["drc_rules"]
    return {k: float(R[v]) for k, v in RULE_KEYS.items()}


def rule_source(name):
    return "%s %s" % (os.path.basename(JSON), RULE_KEYS[name])


# ---- tap construction (a tie stripe: diffusion + one contact row; Metal1 comes from the rail it sits under)
# n tie: N+ diffusion = diff not under pimp (no nSD needed: maximal.drc derives nSD_drv = Activ - pSD), in NWell,
#        NWell enclosure NW.e (outside ThickGateOx).  p tie: diff under pimp outside NWell, pimp enclosure pSD.c
#        (0.18, written for P+Activ in NWell; used here as the conservative value), NWell space NW.f.
#        Both outside ThickGateOx: thickox.space_diff (TGO.b) to the devices' ThickGateOx.
TAPS = {
    "n": dict(well="nwell", implant=None, well_enc="nwell.enc_ntap", well_enc_thick="nwell.enc_ntap_thick"),
    "p": dict(well=None, implant="pimp", implant_enc="pimp.enc_pdiff", well_space="nwell.space_ptap"),
}
# thick-oxide ties (inside the devices' ThickGateOx, merging with it): ThickGateOx around the tie by TGO.a
# (thickox.enc_diff), NWell by NW.e1 (nwell.enc_ntap_thick, "NWell tie ... inside ThickGateOx = 0.62")
THICK = dict(layer="thickox", enc="thickox.enc_diff")
# layers whose same-kind gaps below their space rule are filled (closing) when MERGE is on: the merged vdd NWell
# (NW.b same net 0.62) and ThickGateOx (TGO.e 0.86; no net)
MERGE_LAYERS = [("nwell", "nwell.space_same"), ("thickox", "thickox.space")]

# ---- latch-up (maximal.drc LU.a: "Max. space from any portion of P+Activ inside NWell to an nSD-NWell tie =
# 20.00"; json LU_b 20.0 for N+Activ in PWell to a substrate tie: the implementing file 7_2_latchup.drc is not in
# the uploaded deck, read as LU.a for NMOS). LU.d: tie Activ may extend <= 6 um beyond a Cont.
LU_STEP = 0.5     # um: the maximal deck's LU.a grows the ties inside the well in 0.5 um steps (sg13cmos5l_maximal.drc)


def derive(R):
    """R: dict generic layer name -> klayout.db.Region (merged). Returns the derived regions the generator and the
    latch-up check need (derivations as in sg13cmos5l_maximal.drc: nSD_drv = Activ - pSD, gate = Activ & GatPoly)."""
    diff, poly, pimp, nw = R["diff"], R["poly"], R["pimp"], R["nwell"]
    gate = diff & poly
    pdiff = diff & pimp
    ndiff = diff - pimp
    dev = diff.interacting(gate)
    return dict(gate=gate, pdiff_dev=(pdiff & nw).interacting(gate) - poly, ndiff_dev=(ndiff - nw).interacting(gate) - poly,
                ntap=(ndiff & nw) - dev, ptap=(pdiff - nw) - dev, nwell=nw)


def device_core(R):
    """Device bodies for the area audit (bg_core_pd, 2026-10-28): MOS = gate + its diffusion; rhigh = GatPoly
    touching PolyRes 128/0 (body and heads); pnpMPA = the NWell holding a P+ emitter (P+Activ in NWell, no gate),
    grown by 1.05 um to the collector ring's outer edge (NWell +-2.70 x +-1.96, collector Activ +-3.75 x +-3.01 um,
    measured on the pnpMPA cell of pad_buffer_cells.gds). R: dict of merged regions diff, poly, pimp, nwell, polyres;
    lengths in database units of `dbu` (key "dbu")."""
    diff, poly, pimp, nw, pres = R["diff"], R["poly"], R["pimp"], R["nwell"], R["polyres"]
    gate = diff & poly
    mos = diff.interacting(gate) + gate
    res = poly.interacting(pres) + pres
    emit = (diff & pimp & nw).not_interacting(gate)
    bjt = nw.interacting(emit).sized(int(round(1.05 / R["dbu"])))
    return (mos + res + bjt).merged()


# ---- devices and LVS recognition (implemented in drc.py / lvs.py of this folder; IHP-only)
DEVICES = {
    "sg13_hv_pmos": "gate = Activ & GatPoly on P+Activ (pSD) in NWell under ThickGateOx; bulk = NWell",
    "sg13_hv_nmos": "gate = Activ & GatPoly on N+Activ outside NWell under ThickGateOx; bulk = substrate",
    "cells": "SG13_dev PCells pmosHV / nmosHV / ntap1 / ptap1 as placed in pad_buffer_cells.gds",
}

# ---- parasitic extraction / model facts that drive the layout (sources: model cards and PEX rules are NOT in the
# uploaded PDK copy; what is known from the project notes is marked so)
PEX = {"note": "no PEX rule file in the uploaded copy (libs.tech/klayout only); Metal1 / Metal2 sheet resistance "
               "and coupling not available here: route sensitive nets short and away from switching nets "
               "[project practice, not from a PEX deck]"}
MODELS = {"note": "model cards not in the uploaded copy; finger widths used: 2, 10 um (HV PMOS / NMOS) as in the "
                  "library cells [library practice]"}
