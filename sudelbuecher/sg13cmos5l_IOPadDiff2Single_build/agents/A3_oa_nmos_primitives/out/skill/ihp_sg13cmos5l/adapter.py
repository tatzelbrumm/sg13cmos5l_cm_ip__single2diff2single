# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Process adapter: IHP sg13cmos5l (KLayout open PDK), for ../generic/generator.py. 2026-10-28, Claude (Opus 5.5).

Everything process-specific that ../generator.py needs lives here, each item with its source. The generator only
uses the semantic names below (P.rule("finger_gap"), P.layer("metal1"), ...).
To port: copy this file, fill every entry from the new PDK (see ../generic/SKILL_draft.md, "Porting to another process").

Sources (paths of the PDK copy this was written against):
  J   = libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json, key "drc_rules"
  MAX = libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_maximal.drc
  TOP = libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc
  ANG = libs.tech/klayout/tech/drc/rule_decks/geometry/3_2_angle.drc
  LYP = libs.tech/klayout/tech/sg13cmos5l.lyp
"""
import json
import os

NAME = "ihp_sg13cmos5l"
PDK_DRC = "/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/"
JSON = os.path.join(PDK_DRC, "rule_decks", "sg13cmos5l_tech_default.json")

# ---- layer map (LYP names)
LAYERS = {
    "active": ((1, 0), "LYP Activ.drawing"),
    "poly": ((5, 0), "LYP GatPoly.drawing"),
    "contact": ((6, 0), "LYP Cont.drawing"),
    "metal1": ((8, 0), "LYP Metal1.drawing"),
    "metal1_pin": ((8, 2), "LYP Metal1.pin"),
    "metal1_label": ((8, 25), "LYP Metal1.text"),
    "via1": ((19, 0), "LYP Via1.drawing"),
    "metal2": ((10, 0), "LYP Metal2.drawing"),
    "metal2_pin": ((10, 2), "LYP Metal2.pin"),
    "metal2_label": ((10, 25), "LYP Metal2.text"),
    "pimp": ((14, 0), "LYP pSD.drawing (P+ implant; N+ = Activ not under pSD, MAX nSD_drv)"),
    "well_n": ((31, 0), "LYP NWell.drawing"),
    "thickox": ((44, 0), "LYP ThickGateOx.drawing (3.3 V devices)"),
    "note": ((63, 0), "LYP TEXT.drawing (device names, not read by DRC / LVS)"),
}
# layers that may carry 45-degree edges / only orthogonal edges / only the acute-angle check (ANG)
ANGLES = {
    "ortho_only": ["contact", "via1"],
    "ortho_45": ["active", "poly", "metal1", "metal2"],
    "free_no_acute_below_87deg": ["pimp", "well_n", "thickox"],
}

# ---- rules: semantic name -> (json key or literal, meaning)
RULE_KEYS = {
    "grid": ("grid", "J grid: all coordinates on this grid"),
    "finger_gap": ("Gat_b1", "J Gat_b1 / MAX Gat.b1: space between unrelated 3.3 V gates over Activ; fingers of a "
                             "row at this gap merge their poly endcaps into one strip"),
    "poly_space": ("Gat_b", "J Gat_b: GatPoly space"),
    "poly_endcap": ("Gat_c", "J Gat_c / MAX Gat.c: GatPoly extension over Activ"),
    "poly_to_active": ("Gat_d", "J Gat_d: field GatPoly to Activ"),
    "active_space": ("Act_b", "J Act_b: Activ space (row-to-row gap)"),
    "cont": ("Cnt_a", "J Cnt_a: contact size"),
    "cont_space": ("Cnt_b", "J Cnt_b: contact space"),
    "cont_in_active": ("Cnt_c", "J Cnt_c: Activ enclosure of contact"),
    "cont_in_poly": ("Cnt_d", "J Cnt_d: GatPoly enclosure of contact"),
    "polycont_to_active": ("Cnt_e", "J Cnt_e: contact on GatPoly to Activ"),
    "m1_width": ("M1_a", "J M1_a"),
    "m1_space": ("M1_b", "J M1_b"),
    "m1_wide_space": ("M1_e", "J M1_e: M1 space next to M1 wider than M1_e_w with parallel run > M1_e_cr"),
    "m1_wide_w": ("M1_e_w", "J M1_e_w"),
    "m1_wide_run": ("M1_e_cr", "J M1_e_cr"),
    "m1_cont_endcap": ("M1_c1", "J M1_c1 / MAX M1.c1: M1 endcap enclosure of contact"),
    "m1_area": ("M1_d", "J M1_d / MAX M1.d: minimum Metal1 area (um2)"),
    "via1": ("V1_a", "J V1_a: Via1 size"),
    "via1_space": ("V1_b", "J V1_b: Via1 space"),
    "via1_m1_enc": ("V1_c", "J V1_c: M1 enclosure of Via1"),
    "via1_m1_endcap": ("V1_c1", "J V1_c1 / MAX V1.c1: M1 endcap enclosure of Via1"),
    "m2_width": ("Mn_a", "J Mn_a"),
    "m2_space": ("Mn_b", "J Mn_b"),
    "m2_via1_enc": ("Mn_c", "J Mn_c: M2 enclosure of Via1"),
    "m2_via1_endcap": (0.05, "MAX M2.c1 output text '= 0.05' (no json key)"),
    "tie_impl_enc": ("pSD_c1", "J pSD_c1: pSD enclosure of the P+ substrate tie (the ptap1 PCell uses it)"),
    "impl_to_nactive": ("pSD_d", "J pSD_d / MAX pSD.d: pSD space to unrelated N+Activ in PWell"),
    "impl_to_ngate_hv": ("pSD_j1", "J pSD_j1 / MAX pSD.j1: pSD space to NFET gate inside ThickGateOx"),
    "thickox_over_active": ("TGO_a", "J TGO_a / MAX TGO.a"),
    "thickox_over_gate": ("TGO_c", "J TGO_c / MAX TGO.c"),
    "thickox_space": ("TGO_e", "J TGO_e / MAX TGO.e: merge if closer"),
    "lu_ptie": ("LU_b", "J LU_b: max distance N+Activ (PWell) to a substrate tie; implementation 7_2_latchup.drc "
                        "not in this PDK copy (TOP line 463 includes it)"),
    "lu_ntie": ("LU_a", "J LU_a / MAX LU.a: max distance P+Activ (NWell) to an NWell tie"),
    "tie_cont_ext_max": ("LU_d", "J LU_d / MAX LU.d1: max tie Activ extension beyond a contact"),
    "well_space_same": ("NW_b", "J NW_b / 5_1_nwell.drc NW.b: same net (merged if closer)"),
    "well_space_diff": ("NW_b1", "J NW_b1 / 5_1_nwell.drc NW.b1: different nets"),
    "well_over_pact_hv": ("NW_c1", "J NW_c1 / MAX NW.c1: NWell enclosure of P+Activ in TGO"),
    "well_to_nact_hv": ("NW_d1", "J NW_d1 / MAX NW.d1: NWell space to N+Activ in TGO"),
    "well_over_ntie_hv": ("NW_e1", "J NW_e1 / MAX NW.e1: NWell enclosure of the NWell tie in TGO"),
    "well_to_ptie_hv": ("NW_f1", "J NW_f1 / 5_1_nwell.drc NW.f1: NWell space to substrate tie in TGO"),
}

# ---- devices: library cells (exported SG13_dev PCell variants) and how LVS sees them
DEVICE_LIBRARY = "pad_buffer_cells.gds"   # the block library the device cells are copied from (unmodified)
DEVICES = {
    # key: (library cell, W um, L um, model)
    "nhv_10_1": ("nmosHV$7", 10.0, 1.0, "sg13_hv_nmos"),
    "nhv_2_4": ("nmosHV$11", 2.0, 4.0, "sg13_hv_nmos"),
    "nhv_10_4": ("nmosHV$10", 10.0, 4.0, "sg13_hv_nmos"),
    "nhv_3p4_30": ("nmosHV$8", 3.4, 30.0, "sg13_hv_nmos"),
    "nhv_0p5_2": ("nmosHV$9", 0.5, 2.0, "sg13_hv_nmos"),
    "nhv_1_0p45": ("nmosHV$5", 1.0, 0.45, "sg13_hv_nmos"),
}
LVS = {
    "sg13_hv_nmos": "gate = Activ & GatPoly on N+Activ (Activ not under pSD) outside NWell, inside ThickGateOx; "
                    "S/D = N+Activ - GatPoly; bulk = substrate (TOP: pwell = not NWell; ptap = pactiv & pwell)",
    "sg13_hv_pmos": "gate on P+Activ (Activ & pSD) inside NWell and ThickGateOx; bulk = NWell",
    "substrate_tie": "P+Activ outside NWell (TOP ptap); the ptap1 PCell adds Substrate 40/0, which makes IHP's "
                     "run_lvs.py extract a tap resistor unless --disable_tap_extraction; plain ties here have no 40/0",
}
# ---- parasitic extraction / model facts that drive the layout (what this PDK copy states)
PEX = "No PEX rule files in this PDK copy (libs.tech/klayout/tech has drc/ and the .lyp only). Layout-driving " \
      "assumption, not a PDK fact: Metal1 / Metal2 tracks of a few 10 um carry uA bias currents, R negligible; " \
      "coupling between neighbouring tracks matters only for high-impedance nets."
MODEL = "HV MOS minimum L: Gat_a3 (NMOS) / Gat_a4 (PMOS) in J. Finger widths used: those of exported PCell " \
        "variants. Model cards are not in this PDK copy, so no W / nf binning limits are checked here."


class Process:
    def __init__(self, json_path=JSON):
        self.json_path = json_path
        self.R = json.load(open(json_path))["drc_rules"]
        self.used = {}

    def rule(self, name):
        key, why = RULE_KEYS[name]
        v = key if isinstance(key, float) else self.R[key]
        self.used[name] = (v, key if isinstance(key, str) else why)
        return v

    def layer(self, name):
        return LAYERS[name][0]

    def device(self, key):
        return DEVICES[key]

    def citations(self):
        return {n: (v, RULE_KEYS[n][1]) for n, (v, k) in sorted(self.used.items())}
