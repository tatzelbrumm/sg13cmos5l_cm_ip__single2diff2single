# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""lu_context.py: latch-up of a tap-less cell against the parent's tap segments (IHP sg13cmos5l), 2026-10-28, Claude.

    python3 lu_context.py <gds> <cell> <sides> [out.gds]
      sides: comma-separated set of T, B (segment in the cell's top / bottom margin, under the source plate) and
             L, R (segment abutting the left / right cell edge, outside the cell)
    e.g. python3 lu_context.py examples/oa_p_cells.gds oa_pmir_c T,B
         python3 lu_context.py ../../../out_bg/bg_p_cells.gds bg_pmir_pcas_c T

Prints the farthest P+ Activ for full-length segments and the minimum centred segment length (same for every side
in the set, bisection on ../generic/check.py lu), then draws the context cell (cell + segments from
../generic/generator.py tap_path, length rounded up by 0.3 um) and runs the rule part of tools/oa_core_pd_drc.py.
Margin position of T / B: diff_space from the outer rows' Activ and pimp_encl_pdiff + pimp_to_ntap from their pSD.
"""
import importlib.util
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "generic"))
import klayout.db as db             # noqa: E402
import generator as G               # noqa: E402
import check as K                   # noqa: E402
P = G.load_adapter(os.path.join(HERE, "adapter.py"))


def run(gds, cn, sides, out=None):
    ly = db.Layout()
    ly.read(gds)
    c = ly.cell(cn)
    cb = c.dbbox()
    arr = db.Region(c.begin_shapes_rec(ly.find_layer(*P.layer("diff")))).bbox().to_dtype(ly.dbu)
    wa = 2 * P.rule("diff_encl_contact") + P.rule("contact_size")
    gy = max(P.rule("diff_space"), P.rule("pimp_encl_pdiff") + P.rule("pimp_to_ntap"))
    cx, cy = (arr.left + arr.right) / 2, (arr.bottom + arr.top) / 2

    def rects(L):
        out_ = []
        for s in sides:
            if s == "T":
                out_.append((cx - L / 2, arr.top + gy, cx + L / 2, arr.top + gy + wa))
            elif s == "B":
                out_.append((cx - L / 2, arr.bottom - gy - wa, cx + L / 2, arr.bottom - gy))
            elif s == "L":
                out_.append((cb.left - wa, cy - L / 2, cb.left, cy + L / 2))
            elif s == "R":
                out_.append((cb.right, cy - L / 2, cb.right + wa, cy + L / 2))
        return out_
    full = cb.height() if all(s in "LR" for s in sides) else arr.width()
    dfull = K.lu(P, ly, c, rects(full))[0]
    lo, hi = 0.5, full
    if dfull > P.rule("lu_tap_dist"):
        print("%s %s: full-length segments leave %.2f um > %g: not enough" % (cn, ",".join(sides), dfull,
                                                                               P.rule("lu_tap_dist")))
        return None
    for _ in range(30):
        m = (lo + hi) / 2
        if K.lu(P, ly, c, rects(m))[0] <= P.rule("lu_tap_dist"):
            hi = m
        else:
            lo = m
    Lmin = hi
    Ld = min(full, round(Lmin + 0.3, 1))
    top = ly.create_cell("ctx_%s_%s" % (cn, "".join(sides)))
    top.insert(db.CellInstArray(c.cell_index(), db.Trans()))
    for k, (x1, y1, x2, y2) in enumerate(rects(Ld)):
        if x2 - x1 > y2 - y1:
            pts = [(x1, (y1 + y2) / 2), (x2, (y1 + y2) / 2)]
        else:
            pts = [((x1 + x2) / 2, y1), ((x1 + x2) / 2, y2)]
        t = G.tap_path(ly, P, top.name + "_tap%d" % k, pts, "vdd")
        top.insert(db.CellInstArray(t.cell_index(), db.Trans()))
    out = out or os.path.splitext(gds)[0] + "_lu_" + cn + ".gds"
    o = db.SaveLayoutOptions()
    o.write_context_info = False
    o.gds2_write_timestamps = False
    ly.write(out, o)
    spec = importlib.util.spec_from_file_location("drc", os.path.join(HERE, "tools", "oa_core_pd_drc.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    res = m.run(out, top.name)
    nv = sum(r_[3] for r_ in res)
    seg = rects(Ld)
    print("%s %s: full-length segments %.2f um; minimum centred length %.2f um (farthest P+ %.2f); drawn %.1f um "
          "at %s; DRC rules on %s: %d violations%s" % (
              cn, ",".join(sides), dfull, Lmin, K.lu(P, ly, c, rects(Lmin))[0], Ld,
              "; ".join("(%.2f, %.2f; %.2f, %.2f)" % s for s in seg), top.name, nv,
              "" if not nv else " " + str([(r_[0], r_[3]) for r_ in res if r_[3]])))
    return Lmin, Ld, nv


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4] if len(sys.argv) > 4 else None)
