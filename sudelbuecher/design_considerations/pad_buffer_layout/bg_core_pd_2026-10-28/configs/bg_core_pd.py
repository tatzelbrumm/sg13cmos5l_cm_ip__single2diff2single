# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# bg_core_pd (compact), config for ../generator.py, 2026-10-28, Claude (Opus 5.5).
#   cd configs && python3 ../generator.py bg_core_pd.py ../bg_core_pd.gds
# Primitives: PMOS from A4 (primP/out_bg/bg_p_cells.gds: bg_pmir_pcas_c, bg_ms1, bg_svpg; tap-less, bulk nw),
# NMOS from A3 (primN/out_bg/bg_n_cells.gds: bg_n4, dummies D = S = G = g, own p+ ties), and A2's bg_res_c
# (rhigh array, wired) and bg_pnp_c (pnp 3 x 3, wired) from ../.
# Floorplan (same conventions as oa_core_pd v2: vdd rail on top, vss rail at the bottom, ports on the right edge):
#   vdd rail (thick n tie)
#   [svpg][ bg_pmir_pcas_c                          ]   one merged vdd NWell
#   [ bg_res_c (MX: pins down)  ][ bg_ms1 (R270)  ]      ms1 hangs from the pmir well (well closing), its n tie in
#   [ bg_pnp_c ][ e-channel ]    [ bg_n4 (MY)     ]      pmir's bottom margin; n4 MY: g / vpc under pmir's g / vpc
#   vss rail
# ea / eb / e2 stay in the lower left: res pins down to the strip beside the pnp array and to its top row; n4's
# ea / eb buses (bottom edge) along the channel under n4.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.dirname(HERE)
S = "/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad"
sys.path.insert(0, os.path.join(BG, "tools"))
import drc as _drc  # noqa: E402

NAME = "bg_core_pd"
PROCESS = os.path.join(BG, "process", "ihp_sg13cmos5l.py")
SOURCES = {"P": S + "/primP/out_bg/bg_p_cells.gds", "N": S + "/primN/out_bg/bg_n_cells.gds",
           "R": os.path.join(BG, "bg_res_c.gds"), "Q": os.path.join(BG, "bg_pnp_c.gds")}
CDLS = [S + "/primP/out_bg/bg_p_cells.cdl", S + "/primN/out_bg/bg_n_cells.cdl", os.path.join(BG, "bg_res_c.cdl"),
        os.path.join(BG, "bg_pnp_c.cdl")]
INSTANCES = {
    "pmir": dict(cell="bg_pmir_pcas_c", o="R0"),
    "svpg": dict(cell="bg_svpg", o="R0"),
    "ms1": dict(cell="bg_ms1", o="R270"),      # vdd pin top right (under pmir's bottom plate), ks / en_3v3_b left
    "n4": dict(cell="bg_n4", o="M90"),         # MY: g / vpc top right, ks / en_3v3_b top left, ea / eb bottom
    "res": dict(cell="bg_res_c", o="M0"),      # MX: e2 / ea / eb pins on the bottom edge, vss bus on top
    "pnp": dict(cell="bg_pnp_c", o="R0"),      # e2 / ea on the right edge, e2 frame's top row under res's e2
}
FLOORPLAN = """
V gap=auto
  rail vdd h=1.00 tap=n thick=1
  H align=top gap=auto
    cell svpg
    cell pmir
  H align=top gap=auto
    V align=left gap=auto
      cell res
      cell pnp
    V align=left gap=1.35
      cell ms1
      cell n4
  rail vss h=0.80
"""
NETS = ["vdd", "vss", "iout", "en_3v3", "en_3v3_b", "vpg", "vpc", "g", "ks", "ea", "eb", "e2"]
# ports on the right edge; en_3v3_b leaves through the channel between bg_ms1 and bg_n4 (y range in block
# coordinates of this placement), so the strip right of bg_ms1 stays free for g / vpc
PORTS = {"iout": ("right", None), "en_3v3": ("right", None), "en_3v3_b": ("right", (24.40, 25.60))}
# bandgap core nets first; en_3v3_b before g / vpc: it must cross their drop from pmir to n4 to reach the port
# edge, on Metal2 in the channel (g / vpc hop under it on Metal1)
ROUTE_ORDER = ["e2", "ea", "eb", "vpg", "ks", "en_3v3_b", "g", "vpc", "en_3v3", "iout", "vdd", "vss"]
# bg_ms1 hangs below bg_pmir_pcas_c (its farthest P+ is 23 um from the vdd rail tie): one-contact-row n tie in
# pmir's bottom 0.62 um margin over ms1's width (pmir cell coordinates; Activ y -0.51...-0.21 = 0.21 Act_b from the
# bottom row, as A4's top-margin tie mirrored), under pmir's bottom vdd plate; well / oxide by NW.e1 0.62 inside
# ms1's well (ms1 spans pmir x 24.45 ... 38.87 in this placement)
TAP_SEGMENTS = [dict(inst="pmir", kind="n", net="vdd", box=(25.10, -0.51, 38.20, -0.21), thick=True)]
MERGE_WELLS = True
TIES = {"nw": "vdd"}
ROUTER = dict(pitch=0.27, width=0.29, margin=0.12, keepout=[
    dict(metal=("M1", "M2"), inst="pmir", box=(-1.66, -0.62, 43.51, 15.53)),  # matched PMOS mirror (whole cell)
    dict(metal=("M1", "M2"), inst="ms1", box=(-0.62, -0.62, 6.37, 13.8)),     # MS1 (whole cell)
    dict(metal=("M1", "M2"), inst="n4", box=(-1.33, -0.78, 16.79, 22.02)),    # NMOS block (whole cell)
    dict(metal=("M1", "M2"), inst="res", box=(-0.395, -2.32, 28.095, 11.76)),  # rhigh array
    dict(metal=("M1", "M2"), inst="pnp", box=(0.0, -14.84, 22.2, 2.92)),       # pnp array
])
DRC = lambda ly, cell: [(r[0], r[3]) for r in _drc.run(ly, cell)]
