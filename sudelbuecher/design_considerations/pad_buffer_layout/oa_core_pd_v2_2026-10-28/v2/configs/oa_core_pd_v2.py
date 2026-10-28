# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# oa_core_pd v2 (compact), config for ../generator.py, 2026-10-28, Claude (Opus 5.5).
#   python3 ../generator.py oa_core_pd_v2.py ../oa_core_pd.gds          (FP=3 default; FP=1 / FP=2: candidates)
# Primitives: NMOS from A3 (primN/out/oa_n_cells.gds: oa_n10, oa_mcs_c), PMOS from A4 (primP/out/oa_p_cells.gds:
# oa_pmir_c, oa_ms1, oa_svpg), oa_pcas_c (../oa_pcas_c.gds: oa_pcas without its ring). All PMOS tap-less, one
# merged vdd NWell; ties: thick n tie under the vdd rail where free, A4's two segments in oa_pmir_c's margins;
# NMOS: A3's shared p+ tie of the oa_n10 / oa_mcs_c pair.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
S = "/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad"
sys.path.insert(0, V2)
import drc as _drc  # noqa: E402

NAME = "oa_core_pd"
PROCESS = os.path.join(V2, "process", "ihp_sg13cmos5l.py")
SOURCES = {"P": S + "/primP/out/oa_p_cells.gds", "N": S + "/primN/out/oa_n_cells.gds",
           "C": os.path.join(V2, "oa_pcas_c.gds")}
CDLS = [S + "/primP/out/oa_p_cells.cdl", S + "/primN/out/oa_n_cells.cdl", os.path.join(V2, "oa_pcas_c.cdl")]
FP = os.environ.get("FP", "3")      # 3 = the delivered floorplan (2355 um2); 1, 2 = the side-by-side candidates
INSTANCES = {
    "pmir": dict(cell="oa_pmir_c", o="M0"),     # inversion: band B (its Metal2 pins) moves up, next to oa_pcas_c
    "pcas": dict(cell="oa_pcas_c", o="M0"),     # sources up (towards pmir's pins), drains down (towards the NMOS)
    "ms1": dict(cell="oa_ms1", o="R270"),      # its vdd / ks pins on the right, its clean edge towards oa_pmir_c
    "svpg": dict(cell="oa_svpg", o="M90"),
    "n10": dict(cell="oa_n10", o="R0"),
    "mcs": dict(cell="oa_mcs_c", o="R0"),
}
FLOORPLANS = {
    # 1: pmir column | right column [ms1 svpg] / pcas / NMOS pair (shared tie)
    "1": """
V gap=auto,auto
  rail vdd h=1.50 tap=n thick=1
  H align=top gap=auto
    cell pmir
    V align=left gap=auto
      H align=top gap=auto
        cell ms1
        cell svpg
      cell pcas
      FREE
        cell n10 at=0,0
        cell mcs at=4.91,-7.99
  rail vss h=1.42
""",
    # 2: pmir column | right column [pcas ms1 svpg] / NMOS pair
    "2": """
V gap=auto,auto
  rail vdd h=1.50 tap=n thick=1
  H align=top gap=auto
    cell pmir
    V align=left gap=auto
      H align=top gap=auto
        cell pcas
        cell ms1
        cell svpg
      FREE
        cell n10 at=0,0
        cell mcs at=4.91,-7.99
  rail vss h=1.42
""",
    # 3: stacked rows: pmir (R270, pins down) / [pcas ms1 svpg] / NMOS pair
    "3": """
V gap=auto,auto,auto,auto
  rail vdd h=1.50 tap=n thick=1
  cell pmir o=R270
  H align=top gap=auto
    cell pcas
    cell ms1 o=R90
    cell svpg
  FREE
    cell n10 at=0,0
    cell mcs at=4.91,-7.99
  rail vss h=1.42
""",
}
FLOORPLAN = FLOORPLANS[FP]

NETS = ["vdd", "vss", "iout", "en_3v3", "en_3v3_b", "vpg", "vpc", "vnc", "vbr", "ks", "vres", "co", "c8", "c2"]
_side = "right" if FP == "3" else "top"   # FP3: all ports on the right edge (no route over the PMOS mirror)
PORTS = {"iout": (os.environ.get("IOUT", _side), None), "en_3v3": (os.environ.get("EN", _side), None),
         "en_3v3_b": (os.environ.get("ENB", "right"), None)}
# A4 (oa_p_report): one-contact n ties in oa_pmir_c's top / bottom 0.62 um margins under its vdd plates, centred,
# >= 7.86 um long (8.2 drawn as in A4's ctx_tb, DRC 0 there), Activ y 38.46-38.76 and -0.51...-0.21 (cell coords);
# inside ThickGateOx: well and oxide by NW.e1 0.62 around the tie.
TAP_SEGMENTS = [dict(inst="pmir", kind="n", net="vdd", box=(5.325, 38.46, 13.525, 38.76), thick=True),
                dict(inst="pmir", kind="n", net="vdd", box=(5.325, -0.51, 13.525, -0.21), thick=True)]
MERGE_WELLS = True
TIES = {"nw": "vdd"}
# no foreign net over the matched PMOS mirror: Metal1 / Metal2 keep-out over oa_pmir_c's device rows (cell coords:
# rows x 0 ... 18.85, y 0 ... 38.25; its own pins sit on the edge outside this box)
# router grid as built on 2026-10-28 (generator default would be pitch 0.265 = (0.29 + Mn_e 0.24) / 2): kept fixed so
# the delivered GDS is reproduced byte for byte
ROUTER = dict(pitch=0.27, width=0.29, margin=0.12, keepout=[dict(metal=("M1", "M2"), inst="pmir", box=(0.0, 0.0, 18.85, 38.25))])           # the tap-less PMOS cells' internal bulk = the merged vdd well
DRC = lambda ly, cell: [(r[0], r[3]) for r in _drc.run(ly, cell)]
