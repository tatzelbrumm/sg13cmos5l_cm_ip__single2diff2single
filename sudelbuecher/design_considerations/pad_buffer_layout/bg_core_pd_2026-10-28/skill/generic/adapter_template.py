# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Process adapter TEMPLATE for generator.py / render_block.py / area_audit.py (process-agnostic), 2026-10-28.
Copy to <process>.py and fill every TODO from the new PDK; give the source of each value (deck file + rule name /
json key / model file). A filled example: ../ihp_sg13cmos5l/adapter.py.
"""

NAME = "TODO"

# generic layer name -> (layer, datatype). Source: the PDK's layer map / the DRC deck's layer definitions.
LAYERS = {
    "diff": None, "poly": None, "cont": None,          # diffusion, gate poly, contact
    "nimp": None, "pimp": None,                         # implants (None if the process derives one from the other)
    "nwell": None, "thickox": None,                     # well; thick gate oxide (None if no thick-oxide devices)
    "m1": None, "m1.pin": None, "m1.text": None,        # lower routing metal, its pin and text layers
    "via1": None,
    "m2": None, "m2.pin": None, "m2.text": None,        # upper routing metal
}

# generic rule name -> value source. rules() returns {name: value in um}. Every name below is used.
RULE_KEYS = {
    "grid": "TODO manufacturing grid",
    "m1.width": "", "m1.space": "", "m1.area": "", "m1.enc_cont": "", "m1.enc_cont_end": "",
    "m1.wide_width": "", "m1.wide_space": "", "m1.wide_run": "",          # wide-metal space, its width threshold, run
    "m2.width": "", "m2.space": "", "m2.area": "", "m2.wide_width": "", "m2.wide_space": "", "m2.wide_run": "",
    "via1.size": "", "via1.space": "", "via1.enc": "", "via1.enc_end": "",  # enclosure all round / on two opposite sides
    "diff.width": "", "diff.space": "", "diff.area": "",
    "cont.size": "", "cont.space": "", "cont.enc_diff": "",
    "nwell.width": "", "nwell.space_same": "", "nwell.space_diff": "",
    "nwell.enc_ntap": "", "nwell.enc_ntap_thick": "", "nwell.space_ptap": "", "nwell.space_ptap_thick": "",
    "nwell.enc_pdiff_thick": "", "nwell.space_ndiff_thick": "",
    "pimp.enc_pdiff": "", "pimp.space_ndiff": "", "pimp.space": "",
    "thickox.space_diff": "", "thickox.enc_diff": "", "thickox.space": "", "thickox.width": "",
    "lu.ntap_dist": "", "lu.ptap_dist": "", "lu.tap_cont_ext": "",       # latch-up distances
}


def rules():
    """TODO: read the values (e.g. from the deck's json / yaml, or literal numbers with a comment per value)."""
    raise NotImplementedError


WELL_OUTLINE = dict(any_angle=False, min_corner_deg=90.0, source="TODO the deck's angle checks for the well layer")
TAPS = {"n": dict(well="nwell", implant=None, well_enc="nwell.enc_ntap", well_enc_thick="nwell.enc_ntap_thick"),
        "p": dict(well=None, implant="pimp", implant_enc="pimp.enc_pdiff", well_space="nwell.space_ptap")}
THICK = dict(layer="thickox", enc="thickox.enc_diff")
MERGE_LAYERS = [("nwell", "nwell.space_same"), ("thickox", "thickox.space")]   # closed below their space rule
LU_STEP = 0.5    # TODO: the step in which the deck grows ties inside the well when it measures latch-up distance


def derive(R):
    """TODO: R = {"diff", "poly", "pimp", "nwell"} -> {"gate", "pdiff_dev", "ndiff_dev", "ntap", "ptap", "nwell"}
    with the deck's own derivations (which implant makes n / p diffusion)."""
    raise NotImplementedError


DEVICES = {"TODO": "recognition layers, terminals, bulk rule (from the LVS deck)"}
PEX = {"note": "TODO which layers carry R / C that matter (PEX rules)"}
MODELS = {"note": "TODO characterized W / L / nf ranges, finger width limits (model cards)"}


# ---- optional (bg_core_pd, 2026-10-28): blocks with resistor arrays and bipolars
# LAYERS["polyres"] = (TODO, TODO)   # the resistor body marker layer, if the PDK has one (drawn in pictures)


def device_core(R):
    """OPTIONAL. R = {"diff", "poly", "pimp", "nwell", "polyres", "dbu"} -> Region of all device bodies: MOS (gate +
    its diffusion), resistor bodies with their heads, bipolars including their own guard / collector structures
    (they are part of the device, not ties). Used by area_audit.py and render_block.py; without it only MOS count
    as devices. TODO from the PDK's device cells (measure the bipolar's extent on its own cell)."""
    raise NotImplementedError
