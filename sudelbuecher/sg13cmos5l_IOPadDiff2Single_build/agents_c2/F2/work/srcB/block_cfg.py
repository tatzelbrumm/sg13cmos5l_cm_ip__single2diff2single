# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F2 stage B: d2s_block (d2s_mpdda_pd + bias_tree_pd + the two 2 kOhm stages) for generator.py of
# oa_core_pd_v2_2026-10-28/v2 (two-metal grid router; read from the notes checkout, not copied).
# Coordinates below are pad coordinates of the cells' bounding boxes (lower left); the generator shifts the block
# so that padtop_ctx_f2 (0, 84) is its origin; the pad places the block back at (0, 84).
import os
import sys

import klayout.db as db

W = os.environ.get("F2W", "/home/user/c2/F2/work")
CB = os.environ.get("F2CELLS", W + "/cellsB")
P2GDS = "/home/user/sudel/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/P2/out/d2s_p2_cells.gds"
P2CDL = P2GDS[:-4] + ".cdl"
NAME = "d2s_block"
PROCESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ihp_sg13cmos5l_f2.py")
SOURCES = {"ctx": CB + "/ctx.gds", "P2": CB + "/p2_tubnolabel.gds", "fp": CB + "/f2b_p.gds", "fn": CB + "/f2b_n.gds",
           "sp": CB + "/f2b_sp.gds", "pw": CB + "/pwr.gds"}
CDLS = [P2CDL, CB + "/f2b_p.cdl", CB + "/f2b_n.cdl", CB + "/f2b_sp.cdl"]

# (instance, cell, orientation, x, y of the oriented bbox's lower left in pad coordinates, net map)
DV = {"vdd": "iovdd"}
PLACE = [
    ("ctx", "padtop_ctx_f2", "R0", 0.0, 84.0, {}),
    ("pwr", "pwr_f2", "R0", None, None, {}),                                  # at its own coordinates
    ("spa", "d2s_sp2k_f2", "R0", 2.50, 88.60, {"core": "pa"}),
    ("spb", "d2s_sp2k_f2", "M90", 69.99, 88.60, {"core": "pb"}),
    ("loads", "d2s_loads_c2", "M90", 12.16, 88.30, {"vdd": "iovdd_ld"}),
    ("abp", "d2s_ab_p_f2", "R0", 42.85, 89.70, {"vdd": "iovdd_ab", "vddo": "iovdd_o"}),
    ("abn", "d2s_ab_n_f2", "R0", 53.61, 89.70, {"vss": "iovss_m", "vsso": "iovss_o"}),
    ("cascp", "d2s_casc_p_c2", "M90", 7.19, 105.15, {"vdd": "iovdd_cp"}),
    ("inputs", "d2s_inputs_c2", "R0", 2.50, 121.00, {"vdd": "iovdd_up"}),
    ("tails", "d2s_tails_c2", "M0", 4.13, 150.20, {"vdd": "iovdd_up"}),
    ("biasp", "bias_tree_p_f2", "M0", 25.23, 169.80, {"vdd": "iovdd_up"}),
    ("cascn", "d2s_casc_n_f2", "R90", 46.695, 103.10, {"vss": "iovss_m"}),
    ("rhigh", "d2s_rhigh_f2", "M0", 46.00, 145.60, {"vss": "iovss_m"}),
    ("sinks", "sinks_6x6_f2", "R90", 61.30, 103.70, {"vss": "iovss_sk"}),
    ("biasn", "bias_tree_n_f2", "M0", 46.00, 169.50, {"vss": "iovss_m"}),
    ("tgsw", "d2s_tgsw_f2", "R0", 53.90, 166.55, {"vss": "iovss_m"}),
]


def _cell_bbox(name, orient):
    for f in SOURCES.values():
        if not os.path.exists(f):
            continue
        ly = db.Layout()
        ly.read(f)
        c = ly.cell(name)
        if c is not None:
            o = {"R0": db.DTrans.R0, "M0": db.DTrans.M0, "M90": db.DTrans.M90, "R90": db.DTrans.R90}[orient]
            return c.dbbox().transformed(db.DTrans(o, 0, 0))
    raise ValueError(name)


INSTANCES, lines = {}, ["FREE"]
for inst, cell, o, x, y, nets in PLACE:
    INSTANCES[inst] = dict(cell=cell, o=o, nets=nets)
    if x is None:
        lines.append("  cell %s o=%s at=0,0" % (inst, o))
        continue
    b = _cell_bbox(cell, o)
    lines.append("  cell %s o=%s at=%.4f,%.4f" % (inst, o, x - b.left, y - b.bottom))
FLOORPLAN = "\n".join(lines) + "\n"

SIGNAL = ["a", "b", "l1", "l2", "pl", "pr", "x", "y", "dabp", "dabn", "vbp", "vbn", "vbpc", "vbnc", "vabp", "vabn",
          "ni", "iref", "en_3v3", "en_3v3_b", "vinp", "vinn", "vref", "vfb"] + \
         ["s%s_%s" % (p, u) for p in "ab" for u in ("A", "B", "C1", "C2")]
POWER = ["iovdd_ld", "iovdd_ab", "iovdd_o", "iovdd_cp", "iovdd_up", "iovss_m", "iovss_sk", "iovss_o"]
NETS = SIGNAL + POWER
PORTS = {"vinp": ("top", (6.0, 12.0)), "vinn": ("top", (6.0, 12.0)), "vref": ("top", (6.0, 12.0)),
         "iref": ("top", (43.6, 45.8)), "en_3v3": ("top", (43.6, 45.8)), "en_3v3_b": ("top", (43.6, 45.8))}


def _ko(inst, box, metals=("M1", "M2")):
    return dict(metal=metals, inst=inst, box=box)


# no router metal over any channel: keep-outs over every gate (Activ & GatPoly, merged, 0.1 um around; cell
# coordinates), no net allowed; the cells' own source / drain metal and pins stay reachable
def _keepouts():
    out = []
    seen = {}
    for inst, cell, o, x, y, nets in PLACE:
        if inst in ("ctx", "pwr"):
            continue
        if cell not in seen:
            for f in SOURCES.values():
                if not os.path.exists(f):
                    continue
                ly = db.Layout()
                ly.read(f)
                c = ly.cell(cell)
                if c is None:
                    continue
                ra, rp = db.Region(), db.Region()
                if ly.find_layer(1, 0) is not None:
                    ra = db.Region(c.begin_shapes_rec(ly.find_layer(1, 0)))
                if ly.find_layer(5, 0) is not None:
                    rp = db.Region(c.begin_shapes_rec(ly.find_layer(5, 0)))
                r = (ra & rp).merged().sized(int(0.1 / ly.dbu))
                seen[cell] = [p.bbox().to_dtype(ly.dbu) for p in r.merged().each()]
                break
        for b in seen[cell]:
            out.append(dict(metal=("M1", "M2"), inst=inst, box=(b.left, b.bottom, b.right, b.top), nets=[]))
    return out


ROUTER = dict(pitch=0.27, width=0.29, margin=0.12, keepout=_keepouts())
ROUTE_ORDER = ["dabp", "dabn", "sb_C2", "sb_C1", "sb_B", "sb_A", "vabp", "vabn", "vbpc", "vbnc", "vbn", "en_3v3",
               "en_3v3_b", "sa_A", "sa_B", "sa_C1", "sa_C2", "x", "y", "l1", "l2", "pl", "pr", "a", "b", "ni", "iref",
               "vinp", "vinn", "vref", "vfb"]          # found by trying four orders (try_orders.py): this one routes all
MERGE_WELLS = True
