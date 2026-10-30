# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Process adapter TEMPLATE for generator.py / render.py (process-agnostic part), 2026-10-28, Claude (Opus 5.5).

Copy to <process>/adapter.py and fill every value from the new PDK. Keep the source of each value next to it
(deck file + rule name, json key, LVS deck line, model file). A worked instance is ../ihp_sg13cmos5l/adapter.py.
Where to find each item and how to verify it: SKILL_draft.md, section "Porting to another process".
"""
import json

NAME = "<process>"
JSON = None          # path of a machine-readable rule table if the PDK has one, else None (put values in RULE_KEYS)

# semantic layer name -> ((layer, datatype), source). All names below are used by generator.py / render.py.
LAYERS = {
    "active": (None, "diffusion / active area drawing layer"),
    "poly": (None, "gate poly"),
    "contact": (None, "contact to active / poly"),
    "metal1": (None, ""), "metal1_pin": (None, "pin purpose"), "metal1_label": (None, "text purpose"),
    "via1": (None, ""),
    "metal2": (None, ""), "metal2_pin": (None, ""), "metal2_label": (None, ""),
    "pimp": (None, "P+ implant (selects P+ active; ties to the substrate)"),
    "well_n": (None, "N-well"),
    "thickox": (None, "thick gate oxide marker for the high-voltage devices (if the process has one)"),
    "note": (None, "a text layer that DRC / LVS ignore (device names)"),
}
# which layers may have 45-degree edges, which only orthogonal ones (deck: angle / grid rules)
ANGLES = {"ortho_only": [], "ortho_45": [], "free_no_acute_below_deg": []}

# semantic rule name -> (value or rule-table key, source and meaning). Every name is read by the generator.
RULE_KEYS = {
    "grid": (None, "manufacturing grid"),
    "finger_gap": (None, "space between unrelated gates over active for the device class used; fingers of a row "
                         "at this gap merge their poly endcaps"),
    "poly_space": (None, "poly space"), "poly_endcap": (None, "poly extension over active"),
    "poly_to_active": (None, "field poly to active"),
    "active_space": (None, "active space (row-to-row gap)"),
    "cont": (None, "contact size"), "cont_space": (None, "contact space"),
    "cont_in_active": (None, "active enclosure of contact"), "cont_in_poly": (None, "poly enclosure of contact"),
    "polycont_to_active": (None, "contact on poly to active"),
    "m1_width": (None, ""), "m1_space": (None, ""),
    "m1_wide_space": (None, "M1 space next to wide M1"), "m1_wide_w": (None, ""), "m1_wide_run": (None, ""),
    "m1_cont_endcap": (None, "M1 endcap enclosure of contact"),
    "m1_area": (None, "minimum M1 area"),
    "via1": (None, "via1 size"), "via1_space": (None, ""), "via1_m1_enc": (None, "M1 enclosure of via1"),
    "via1_m1_endcap": (None, "M1 endcap enclosure of via1"),
    "m2_width": (None, ""), "m2_space": (None, ""), "m2_via1_enc": (None, ""), "m2_via1_endcap": (None, ""),
    "tie_impl_enc": (None, "implant enclosure of the substrate tie active"),
    "impl_to_nactive": (None, "P+ implant to unrelated N+ active"),
    "impl_to_ngate_hv": (None, "P+ implant to NMOS gate (device class used)"),
    "thickox_over_active": (None, ""), "thickox_over_gate": (None, ""), "thickox_space": (None, "merge distance"),
    "lu_ptie": (None, "max distance N+ active (substrate) to a substrate tie"),
    "lu_ntie": (None, "max distance P+ active (well) to a well tie"),
    "tie_cont_ext_max": (None, "max tie active extension beyond a contact"),
    "well_space_same": (None, "well space, same net (merge below)"), "well_space_diff": (None, "different nets"),
    "well_over_pact_hv": (None, ""), "well_to_nact_hv": (None, ""), "well_over_ntie_hv": (None, ""),
    "well_to_ptie_hv": (None, ""),
}
# device key -> (cell name in the device library, W, L, LVS model name); cells must have the gate vertical
# (L along x) in their own frame, two S/D stripes on Metal1
DEVICES = {}
LVS = {}      # model -> how the LVS deck recognizes it (layers, terminals, bulk); "substrate_tie" -> how ties connect
PEX = ""      # which layers carry significant R / C per the PEX rules; what that means for track widths
MODEL = ""    # characterized W / L / nf ranges, finger-width limits, minimum L per device class


class Process:
    def __init__(self, json_path=JSON):
        self.R = json.load(open(json_path))["drc_rules"] if json_path else {}
        self.used = {}

    def rule(self, name):
        key, why = RULE_KEYS[name]
        v = key if isinstance(key, (int, float)) else self.R[key]
        self.used[name] = (v, key)
        return v

    def layer(self, name):
        return LAYERS[name][0]

    def device(self, key):
        return DEVICES[key]

    def citations(self):
        return {n: (v, RULE_KEYS[n][1]) for n, (v, k) in sorted(self.used.items())}
