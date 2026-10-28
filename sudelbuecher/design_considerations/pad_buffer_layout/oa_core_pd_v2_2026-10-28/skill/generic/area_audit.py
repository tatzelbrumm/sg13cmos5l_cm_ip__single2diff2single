# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""area_audit.py: where the area of an assembled block goes (layers from the process adapter), 2026-10-28, Claude.

    python3 area_audit.py <adapter.py> <gds> <cell> [<gds> <cell> ...]

Per primitive instance: bbox, device core (bbox of the device diffusion and gates), band = bbox - core (rings,
enclosures, track bands, the space a ring encloses), tie diffusion; per block: wells (count, area), union of the
primitive boxes, free area (no primitive, no rail), utilization (gate area / block, device diffusion / block).
"""
import importlib.util
import sys

import klayout.db as db

spec = importlib.util.spec_from_file_location("adapter", sys.argv[1])
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)


def audit(gds, cellname):
    ly = db.Layout()
    ly.read(gds)
    top = ly.cell(cellname)
    dbu = ly.dbu
    A = lambda r: r.area() * dbu * dbu

    def L(cell, key, own=False):
        li = ly.find_layer(*P.LAYERS[key])
        if li is None:
            return db.Region()
        return (db.Region(cell.shapes(li)) if own else db.Region(cell.begin_shapes_rec(li))).merged()
    bb = top.dbbox()
    blk = bb.width() * bb.height()
    print("== %s in %s: %.2f x %.2f = %.1f um2" % (cellname, gds.split("/")[-1], bb.width(), bb.height(), blk))
    tot = dict(bbox=0, core=0, band=0, tie=0)
    union = db.Region()
    print("   %-24s %8s %8s %8s %8s  %s" % ("instance", "bbox", "core", "band", "tie", "wells"))
    for inst in top.each_inst():
        c = inst.cell
        if c.name.endswith("image_jumpers"):
            continue
        diff, poly = L(c, "diff"), L(c, "poly")
        gate = diff & poly
        dev = diff.interacting(gate)
        tie = diff - dev
        cb = c.bbox()
        core = (dev + gate).bbox()
        a_bb = cb.width() * cb.height() * dbu * dbu
        a_core = core.width() * core.height() * dbu * dbu
        nw = L(c, "nwell")
        print("   %-24s %8.1f %8.1f %8.1f %8.1f  %d well(s) %.1f um2"
              % (c.name, a_bb, a_core, a_bb - a_core, A(tie), nw.count(), A(nw)))
        for k, v in (("bbox", a_bb), ("core", a_core), ("band", a_bb - a_core), ("tie", A(tie))):
            tot[k] += v
        union += db.Region(inst.bbox())
    print("   %-24s %8.1f %8.1f %8.1f %8.1f" % ("sum", tot["bbox"], tot["core"], tot["band"], tot["tie"]))
    m1 = db.Region(top.shapes(ly.find_layer(*P.LAYERS["m1"])))
    rails = db.Region([p for p in m1.merged().each() if p.bbox().width() * dbu > 0.8 * bb.width()])
    free = db.Region(top.bbox()) - union.merged() - rails
    diff, poly = L(top, "diff"), L(top, "poly")
    gate = diff & poly
    dev = diff.interacting(gate)
    nw = L(top, "nwell")
    tie_top = L(top, "diff", own=True)
    print("   block: wells %d (%.1f um2); top-level ties %.1f um2; rails %.1f um2; union of primitives %.1f um2;"
          " free (no primitive, no rail) %.1f um2 = %.1f %%"
          % (nw.count(), A(nw), A(tie_top), A(rails), A(union.merged()), A(free), 100 * A(free) / blk))
    print("   gate area %.1f um2 = %.1f %% of the block; device diffusion %.1f um2 = %.1f %%"
          % (A(gate), 100 * A(gate) / blk, A(dev), 100 * A(dev) / blk))
    return dict(block=blk, band=tot["band"], tie=tot["tie"], free=A(free), wells=nw.count(), gate=A(gate), dev=A(dev))


res = [audit(sys.argv[i], sys.argv[i + 1]) for i in range(2, len(sys.argv), 2)]
if len(res) == 2:
    a, b = res
    print("== change: block %.1f -> %.1f um2 (%.0f %%); bands %.1f -> %.1f; free %.1f -> %.1f; wells %d -> %d"
          % (a["block"], b["block"], 100 * (b["block"] - a["block"]) / a["block"], a["band"], b["band"], a["free"],
             b["free"], a["wells"], b["wells"]))
