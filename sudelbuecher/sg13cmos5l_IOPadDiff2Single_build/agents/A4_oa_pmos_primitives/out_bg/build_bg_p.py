# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_bg_p.py: compact PMOS primitives of bg_core_pd (IHP sg13cmos5l), 2026-10-28, Claude.

    python3 build_bg_p.py <pad_buffer_cells.gds> [out_dir]

The scores bg_pmir_pcas_c, bg_ms1 and bg_svpg in ../out/skill/generic/patterns.md, built by
../out/skill/generic/generator.py with the adapter ../out/skill/ihp_sg13cmos5l/adapter.py (rule values from
sg13cmos5l_tech_default.json, keys cited there). The 10/1, 0.5/12.5 and 1/0.45 fingers are the library's unmodified
PCell cells (pmosHV$14, $13, $7 of pad_buffer_cells.gds, read-only); the 0.3/1 rest is drawn by the adapter (its
pmos_hv reproduces all single-finger pmosHV cells of the library, XOR 0). Writes bg_p_cells.gds / .cdl.

Cells (tap-less, one NWell = ThickGateOx polygon to every cell edge, bulk = internal net nw, tied by the parent):
  bg_pmir_pcas_c  PB / PA / PO (4 / 4 / 8 x 10/1) and PBC / PAC / POC in 8 R270 rows of 4, point-symmetric
  bg_ms1          MS1 = 8 x 0.5/12.5 in series; ks and en_3v3_b on the bottom edge, vdd on top
  bg_svpg         SVPG 1/0.45; vpg bottom, en_3v3 right, vdd top
"""
import os
import sys
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, "..", "out", "skill")
sys.path.insert(0, os.path.join(SKILL, "generic"))
import generator as G                    # noqa: E402
P = G.load_adapter(os.path.join(SKILL, "ihp_sg13cmos5l", "adapter.py"))

LIB_CELLS = {"bg_pmir_pcas_c": {"o": "pmosHV$14", "b": "pmosHV$14", "a": "pmosHV$14"},
             "bg_ms1": {"S": "pmosHV$13"}, "bg_svpg": {"W": "pmosHV$7"}}
PINS = {"bg_pmir_pcas_c": ["g", "iout", "vdd", "vpc", "vpg"], "bg_ms1": ["en_3v3_b", "ks", "vdd"],
        "bg_svpg": ["en_3v3", "vdd", "vpg"]}
NOTES = {"bg_pmir_pcas_c": ["PB / PA / PO = 4 / 4 / 8 fingers 10/1 (sheet: W 40 / 40 / 80, ng 4 / 4 / 8), cascodes",
                            "PBC / PAC / POC the same; ca, co internal; 16 rests 0.3/1 (D = S = vdd, G = row gate)"],
         "bg_ms1": ["MS1 0.5/100 as 8 x 0.5/12.5 in series (ms1 ... ms7)"], "bg_svpg": ["SVPG 1/0.45"]}


def build(lib_gds, out_dir):
    lib = db.Layout()
    lib.read(lib_gds)
    ly = db.Layout()
    ly.dbu = G.DBU
    copied = {}

    def libcell(n):
        if n not in copied:
            s = lib.cell(n)
            d = ly.create_cell(n)
            for li in lib.layer_indexes():
                i = lib.get_info(li)
                d.shapes(ly.layer(i.layer, i.datatype)).insert(s.shapes(li))
            copied[n] = d
        return copied[n]

    scores = G.parse_scores(open(os.path.join(SKILL, "generic", "patterns.md")).read())
    info, txt = {}, ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
                     "* bg_p_cells.cdl: reference netlists of bg_p_cells.gds, written by build_bg_p.py (2026-10-28, "
                     "Claude).", "* Devices as drawn, rests included (S = D). Tap-less cells: bulk on the internal "
                     "net nw, tied to vdd by", "* the parent's tap of the merged vdd well.", ""]
    for s in scores:
        if s["name"] not in LIB_CELLS:
            continue
        cells = {k: libcell(v) for k, v in LIB_CELLS[s["name"]].items()}
        cell, devs, inf = G.build(ly, P, s, cells)
        info[s["name"]] = inf
        txt.append(G.cdl(s["name"], PINS[s["name"]], devs, NOTES[s["name"]]))
    for c in ly.each_cell():
        if c.name.startswith("pmosHV_w0p3_l1"):
            c.name = "pmosHV_w0p3_l1"
    opt = db.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False
    ly.write(os.path.join(out_dir, "bg_p_cells.gds"), opt)
    open(os.path.join(out_dir, "bg_p_cells.cdl"), "w").write("\n".join(txt))
    return ly, info


if __name__ == "__main__":
    lib = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else HERE
    ly, info = build(lib, out)
    for n, i in info.items():
        b = [v * G.DBU for v in i["bbox"]]
        print("%-15s %.3f x %.3f um = %.1f um2  bbox %s" % (n, b[2] - b[0], b[3] - b[1], (b[2] - b[0]) * (b[3] - b[1]), b))
