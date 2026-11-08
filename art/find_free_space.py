#!/usr/bin/env python3
"""Free region per metal layer in the slot7 layout, and the largest free rectangles.

usage: find_free_space.py [slot_7.gds] [out_dir]
Read-only on the slot7 GDS. Writes <out_dir>/free_space.json and free_space.md.

free(layer) = (slot boundary shrunk by EDGE_MARGIN) minus (every shape on that layer, all datatypes
              drawing/pin/nofill/boundary/..., grown by MARGIN[layer]).
"""
import sys, json, os
import numpy as np
import klayout.db as db
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdk_layers as pl

GDS = sys.argv[1] if len(sys.argv) > 1 else "/home/user/sg13cmos5l_cm_slot7/final/gds/slot_7.gds"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
TOP = "slot_7"
# Safety margins (um), see ART_NOTES.md section "Margins"
MARGIN = {"Metal1": 1.0, "Metal2": 1.0, "Metal3": 1.0, "Metal4": 1.0, "TopMetal1": 3.0}
EDGE_MARGIN = 5.0
RES = 0.25  # raster pitch (um) for the rectangle search


def largest_rects(free, res, ox, oy, n=5, min_cells=4):
    """Greedy: n largest axis-parallel all-free rectangles (disjoint after each pick); um coordinates."""
    f = free.copy()
    out = []
    for _ in range(n):
        h, w = f.shape
        heights = np.zeros(w, int)
        best = (0, None)
        for y in range(h):
            heights = np.where(f[y], heights + 1, 0)
            st = []
            for x in range(w + 1):
                cur = heights[x] if x < w else 0
                start = x
                while st and st[-1][1] >= cur:
                    sx, sh = st.pop()
                    area = sh * (x - sx)
                    if area > best[0]:
                        best = (area, (sx, y - sh + 1, x, y + 1))
                    start = sx
                st.append((start, cur))
        if best[1] is None or best[0] < min_cells:
            break
        x0, y0, x1, y1 = best[1]
        out.append((ox + x0 * res, oy + y0 * res, ox + x1 * res, oy + y1 * res))
        f[y0:y1, x0:x1] = False
    return out


def main():
    ly = db.Layout()
    ly.read(GDS)
    top = ly.cell(TOP)
    dbu = ly.dbu
    ln = pl.layer_numbers()
    # slot boundary: prBoundary (189/4) of the top cell, else bbox
    pr = ly.find_layer(*ln["prBoundary.boundary"])
    bbox = top.bbox()
    if pr is not None:
        r = db.Region(top.begin_shapes_rec(pr)).merged()
        if not r.is_empty():
            bbox = r.bbox()
    slot = db.Region(bbox)
    res = {"gds": GDS, "top": TOP, "slot_um": [bbox.left * dbu, bbox.bottom * dbu, bbox.right * dbu, bbox.top * dbu],
           "margin_um": MARGIN, "edge_margin_um": EDGE_MARGIN, "layers": {}}
    inner = slot.sized(-int(EDGE_MARGIN / dbu))
    free_all = inner.dup()
    for m in pl.METALS:
        lnum = ln[m + ".drawing"][0]
        occ = db.Region()
        n_sh = 0
        for li in ly.layer_indexes():
            info = ly.get_info(li)
            if info.layer == lnum and info.datatype not in (1, 25):   # skip label / text datatypes
                rr = db.Region(top.begin_shapes_rec(li))
                n_sh += rr.count()
                occ += rr
        occ = occ.merged()
        grown = occ.sized(int(MARGIN[m] / dbu))
        free = inner - grown
        free_all -= grown
        # raster for the largest rectangles
        ox, oy = bbox.left * dbu, bbox.bottom * dbu
        W = int(round((bbox.right - bbox.left) * dbu / RES))
        H = int(round((bbox.top - bbox.bottom) * dbu / RES))
        mask = np.zeros((H, W), bool)
        # a cell is free only if the full cell is inside the free region
        step = int(RES / dbu)
        fr = free
        for p in fr.each():
            pass
        # rasterise through box tests per row band (fast enough with region AND on strips)
        for j in range(H):
            strip = db.Region(db.Box(bbox.left, bbox.bottom + j * step, bbox.right, bbox.bottom + (j + 1) * step))
            inter = (strip & fr).merged()
            if inter.is_empty():
                continue
            # cell x-intervals fully covered: strip == cell width pieces
            for pg in inter.each():
                b = pg.bbox()
                if b.height() < step:
                    continue
                i0 = -(-(b.left - bbox.left) // step)
                i1 = (b.right - bbox.left) // step
                if i1 > i0:
                    mask[j, i0:i1] = True
        rects = largest_rects(mask, RES, ox, oy, n=6)
        res["layers"][m] = {
            "gds": ln[m + ".drawing"], "shapes": n_sh, "occupied_um2": occ.area() * dbu * dbu,
            "free_um2": free.area() * dbu * dbu,
            "free_fraction": free.area() / inner.area(),
            "rects_um": [[round(v, 3) for v in r] for r in rects],
        }
    # common region: free on all five metals (also guarantees nothing underneath/above on any metal)
    res["common_free_um2"] = free_all.area() * dbu * dbu
    ox, oy = bbox.left * dbu, bbox.bottom * dbu
    W = int(round((bbox.right - bbox.left) * dbu / RES)); H = int(round((bbox.top - bbox.bottom) * dbu / RES))
    mask = np.zeros((H, W), bool); step = int(RES / dbu)
    for j in range(H):
        strip = db.Region(db.Box(bbox.left, bbox.bottom + j * step, bbox.right, bbox.bottom + (j + 1) * step))
        for pg in (strip & free_all).merged().each():
            b = pg.bbox()
            if b.height() < step:
                continue
            i0 = -(-(b.left - bbox.left) // step); i1 = (b.right - bbox.left) // step
            if i1 > i0:
                mask[j, i0:i1] = True
    res["common_rects_um"] = [[round(v, 3) for v in r] for r in largest_rects(mask, RES, ox, oy, n=6)]
    # art region for Metal1-Metal4 only: free on those four layers and clear of the TopMetal1 shapes (grown by the
    # Metal margin) so that nothing is hidden under a TopMetal1 strap when seen from above
    free_vis = inner.dup()
    tm = db.Region()
    for m_ in ("Metal1", "Metal2", "Metal3", "Metal4"):
        lnum_ = ln[m_ + ".drawing"][0]
        occ_ = db.Region()
        for li in ly.layer_indexes():
            info = ly.get_info(li)
            if info.layer == lnum_ and info.datatype not in (1, 25):
                occ_ += db.Region(top.begin_shapes_rec(li))
        free_vis -= occ_.merged().sized(int(MARGIN[m_] / dbu))
    for li in ly.layer_indexes():
        info = ly.get_info(li)
        if info.layer == ln["TopMetal1.drawing"][0] and info.datatype not in (1, 25):
            tm += db.Region(top.begin_shapes_rec(li))
    free_vis -= tm.merged().sized(int(MARGIN["Metal1"] / dbu))
    mask = np.zeros((H, W), bool)
    for j in range(H):
        strip = db.Region(db.Box(bbox.left, bbox.bottom + j * step, bbox.right, bbox.bottom + (j + 1) * step))
        for pg in (strip & free_vis).merged().each():
            b = pg.bbox()
            if b.height() < step:
                continue
            i0 = -(-(b.left - bbox.left) // step); i1 = (b.right - bbox.left) // step
            if i1 > i0:
                mask[j, i0:i1] = True
    res["m1_m4_visible_free_um2"] = free_vis.area() * dbu * dbu
    res["m1_m4_visible_rects_um"] = [[round(v, 3) for v in r] for r in largest_rects(mask, RES, ox, oy, n=6)]
    json.dump(res, open(os.path.join(OUT, "free_space.json"), "w"), indent=1)
    # markdown
    L = ["# Free space in slot_7 (generated by find_free_space.py)", "",
         f"Slot boundary (um): {res['slot_um']}; art keep-away from the slot edge: {EDGE_MARGIN} um.", "",
         "| layer | GDS l/d | shapes | free area (um^2) | free of slot | margin (um) |", "|---|---|---|---|---|---|"]
    for m, v in res["layers"].items():
        L.append(f"| {m} | {v['gds'][0]}/{v['gds'][1]} | {v['shapes']} | {v['free_um2']:.0f} | {100*v['free_fraction']:.1f} % | {MARGIN[m]} |")
    L += ["", "Largest free rectangles (x0, y0, x1, y1 in um, slot coordinates; successive, disjoint):", ""]
    for m, v in res["layers"].items():
        L.append(f"- **{m}**: " + "; ".join(f"({r[0]}, {r[1]}) - ({r[2]}, {r[3]}) = {r[2]-r[0]:.1f} x {r[3]-r[1]:.1f}" for r in v["rects_um"][:4]))
    L.append(f"- **free on all five layers (common)**: area {res['common_free_um2']:.0f} um^2: " +
             "; ".join(f"({r[0]}, {r[1]}) - ({r[2]}, {r[3]}) = {r[2]-r[0]:.1f} x {r[3]-r[1]:.1f}" for r in res["common_rects_um"][:4]))
    L.append(f"- **art region for Metal1-Metal4 (free on those four layers, clear of the TopMetal1 shapes by {MARGIN['Metal1']} um)**: area {res['m1_m4_visible_free_um2']:.0f} um^2: " +
             "; ".join(f"({r[0]}, {r[1]}) - ({r[2]}, {r[3]}) = {r[2]-r[0]:.1f} x {r[3]-r[1]:.1f}" for r in res["m1_m4_visible_rects_um"][:4]))
    open(os.path.join(OUT, "free_space.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


main()
