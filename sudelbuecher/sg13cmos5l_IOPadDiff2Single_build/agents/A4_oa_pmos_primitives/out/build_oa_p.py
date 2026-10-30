# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""build_oa_p.py: compact PMOS primitives of oa_core_pd (IHP sg13cmos5l), 2026-10-28, Claude.

    python3 build_oa_p.py <pad_buffer_cells.gds> [out_dir]

The cells come from the scores in skill/generic/patterns.md, built by skill/generic/generator.py with the process
adapter skill/ihp_sg13cmos5l/adapter.py (every rule value from sg13cmos5l_tech_default.json, keys cited there). The 2/8,
0.5/12.5 and 1/0.45 fingers are the library's unmodified PCell cells (pmosHV$9, $13, $7, copied from
pad_buffer_cells.gds, read-only); the 0.3/8 end dummy is drawn by the adapter's pmos_hv(), which reproduces all 15
single-finger pmosHV cells of the library exactly. Writes oa_p_cells.gds and oa_p_cells.cdl.

Cells (tap-less, one well polygon to the cell edge, bulk = internal net nw, tied by the parent's periphery tap):
  oa_pmir_c  P0 / P2 / P8 / PO mirror, 4 x 8 point-symmetric 2/8 fingers, end dummies 0.3/8 (were 2/8)
  oa_ms1     MS1, 8 x 0.5/12.5 in series, one R270 row, merged en_3v3_b gate strip
  oa_svpg    SVPG 1/0.45
"""
import os
import sys
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "skill", "generic"))
import generator as G                    # noqa: E402
P = G.load_adapter(os.path.join(HERE, "skill", "ihp_sg13cmos5l", "adapter.py"))

LIB_CELLS = {"oa_pmir_c": {"o": "pmosHV$9", "8": "pmosHV$9", "2": "pmosHV$9", "1": "pmosHV$9", "x": "pmosHV$9"},
             "oa_ms1": {"S": "pmosHV$13"}, "oa_svpg": {"W": "pmosHV$7"}}
PINS = {"oa_pmir_c": ["c2", "c8", "co", "vdd", "vpg"], "oa_ms1": ["en_3v3_b", "ks", "vdd"],
        "oa_svpg": ["en_3v3", "vdd", "vpg"]}
NOTES = {"oa_pmir_c": ["4 x 8 point-symmetric 2/8 map of oa_pmir (PO 20, P8 8, P2 2, P0 1, inner dummy 1 = P0's point",
                       "image); end dummies 0.3/8 (were 2/8), D = S = vdd, G = vpg"],
         "oa_ms1": ["MS1 0.5/100 as 8 x 0.5/12.5 in series (ms1 ... ms7)"], "oa_svpg": ["SVPG 1/0.45"]}


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

    scores = G.parse_scores(open(os.path.join(HERE, "skill", "generic", "patterns.md")).read())
    info, txt = {}, ["* SPDX-FileCopyrightText: 2026 Christoph Maier", "* SPDX-License-Identifier: Apache-2.0",
                     "* oa_p_cells.cdl: reference netlists of oa_p_cells.gds, written by build_oa_p.py (2026-10-28, "
                     "Claude).", "* Devices as drawn, dummies included (S = D). All cells are tap-less: bulk on the "
                     "internal net nw (the cell's", "* one NWell), tied to vdd by the parent's periphery tap of the "
                     "merged vdd well.", ""]
    for s in scores:
        if s["name"] not in LIB_CELLS:                 # patterns.md also holds other blocks' scores
            continue
        cells = {k: libcell(v) for k, v in LIB_CELLS[s["name"]].items()}
        cell, devs, inf = G.build(ly, P, s, cells)
        info[s["name"]] = inf
        txt.append(G.cdl(s["name"], PINS[s["name"]], devs, NOTES[s["name"]]))
    for c in ly.each_cell():                       # the adapter's dummy cell gets a stable, unique name
        if c.name.startswith("pmosHV_w0p3_l8"):
            c.name = "pmosHV_w0p3_l8"
    opt = db.SaveLayoutOptions()
    opt.write_context_info = False
    opt.gds2_write_timestamps = False              # byte-reproducible output
    ly.write(os.path.join(out_dir, "oa_p_cells.gds"), opt)
    open(os.path.join(out_dir, "oa_p_cells.cdl"), "w").write("\n".join(txt))
    return ly, info


if __name__ == "__main__":
    lib = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else HERE
    ly, info = build(lib, out)
    for n, i in info.items():
        b = [v * G.DBU for v in i["bbox"]]
        print("%-10s %.3f x %.3f um  bbox %s  well polygon: %d vertices" % (
            n, b[2] - b[0], b[3] - b[1], b, sum(p.num_points() for p in i["well"].each())))
