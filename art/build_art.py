#!/usr/bin/env python3
"""Build the tughra metal art for slot_7: image -> octilinear polygons on five metal layers -> GDS.

usage: build_art.py [--slot SLOT_GDS] [--scale UM_PER_PX] [--out DIR]

Pipeline (all lengths in um, grid G = 0.05 um):
 1. segment.py splits the source image (legend row excluded) into six colour masks (soft coverage).
 2. The soft coverage is resampled to the 0.05 um grid at the chosen scale and cut at 0.5.
 3. Per layer (mapping in LAYER_OF): every stroke is widened along its centreline to the design minimum width
    (skeleton + disk of the minimum radius where the stroke is thinner), gaps below the design minimum space are
    closed.  Strokes are never narrowed, so thick strokes keep their shape.
 4. The binary image is contoured with marching squares on the grid (vertices at edge midpoints), which gives only
    0 / 45 / 90 degree edges, as the deck's angle rule requires; all vertices are multiples of 0.025 um (5 nm grid).
 5. Written as cell "tughra_art" (art/tughra_art.gds) and as a copy of slot_7 with the art placed in the common
    free region (art/slot7_with_art.gds).  The slot7 source file is only read.
The script re-runs deterministically.
"""
import argparse, json, os, sys
import numpy as np
import cv2
from skimage.morphology import skeletonize
from skimage.measure import find_contours
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import segment as S
import pdk_layers as pl

G = 0.05                                   # raster grid (um); contour vertices land on multiples of G/2
LAYER_OF = {"purple": "TopMetal1", "green": "Metal4", "red": "Metal3", "blue": "Metal2",
            "orange": "Metal1", "gold": "Metal1"}
DESIGN = {                                 # design minimum width / space (um); PDK minimum is in pdk_layers
    "Metal1": (0.30, 0.30), "Metal2": (0.30, 0.30), "Metal3": (0.30, 0.30), "Metal4": (0.30, 0.30),
    "TopMetal1": (1.70, 1.70),
}
SLOT_DEFAULT = os.environ.get("SLOT7_GDS", "/home/user/sg13cmos5l_cm_slot7/final/gds/slot_7.gds")
CELL = "tughra_art"


def disk(r_cells):
    r = max(1, int(round(r_cells)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def widen_to_min(mask, w_um):
    """Every stroke at least w_um wide: disk of radius w/2 on each skeleton pixel whose local radius is smaller."""
    r_min = w_um / 2 / G
    dt = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 5)
    sk = skeletonize(mask)
    ys, xs = np.where(sk & (dt < r_min - 0.5))
    out = mask.astype(np.uint8).copy()
    ri = int(round(r_min))
    for y, x in zip(ys, xs):
        cv2.circle(out, (int(x), int(y)), ri, 1, -1)
    return out.astype(bool)


def conform(mask, w_um, s_um):
    m = widen_to_min(mask, w_um)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, disk(s_um / 2 / G)).astype(bool)
    # closing can leave pinches; one more floor pass and close for stability
    m = widen_to_min(m, w_um)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, disk(s_um / 2 / G)).astype(bool)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=4)
    keep = np.zeros_like(m)
    for i in range(1, n):
        if st[i, 4] * G * G >= 1.0 * w_um * w_um:      # drop specks smaller than one minimum-width square
            keep |= lab == i
    return keep


def class_masks(path, scale):
    """Soft coverage -> binary masks on the G grid, plus the source crop box and the raw (unprocessed) masks."""
    rgb, refs, lab, cov = S.load(path)
    ys, xs = np.where(lab >= 0)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1      # ink bounding box in source px
    f = scale / G                                                          # grid cells per source pixel
    W = int(np.ceil((x1 - x0) * f)); H = int(np.ceil((y1 - y0) * f))
    out = {}
    for i, c in enumerate(S.COLORS):
        crop = cov[i][y0:y1, x0:x1]
        up = cv2.resize(crop, (W, H), interpolation=cv2.INTER_CUBIC)
        out[c] = up >= 0.5
    return out, (x0, y0, x1, y1), (rgb, lab)


def rings_to_region(mask_u8, dbu_um=0.001):
    """Binary mask (row 0 = top of the art) -> klayout Region in the art cell frame (origin = lower-left)."""
    H, W = mask_u8.shape
    pad = np.pad(mask_u8.astype(float), 1)
    cont = find_contours(pad, 0.5)
    rings = []
    for c in cont:
        # c: (row, col) in padded coordinates, vertices at edge midpoints; closed
        if len(c) < 4:
            continue
        x = (c[:, 1] - 1 + 0.5) * G                 # cell centre of col j is at (j+0.5)*G
        y = (H - (c[:, 0] - 1 + 0.5)) * G
        pts = np.round(np.stack([x, y], 1) / 0.025).astype(np.int64) * 25      # nm, multiples of 25 nm
        # drop repeated and collinear vertices
        keep = [pts[0]]
        for p in pts[1:-1]:
            if (p != keep[-1]).any():
                keep.append(p)
        pts = np.array(keep)
        if len(pts) > 2:
            a, b, cc = np.roll(pts, 1, 0), pts, np.roll(pts, -1, 0)
            cross = (b[:, 0] - a[:, 0]) * (cc[:, 1] - b[:, 1]) - (b[:, 1] - a[:, 1]) * (cc[:, 0] - b[:, 0])
            pts = pts[cross != 0]
        if len(pts) < 3:
            continue
        area2 = float(np.sum(pts[:, 0] * np.roll(pts[:, 1], -1) - np.roll(pts[:, 0], -1) * pts[:, 1]))
        rings.append((area2, pts))
    # nesting by even-odd: outer rings and holes via polygon containment using a Region XOR chain per top-level group
    # skimage returns holes with the opposite orientation of outer rings: sign of area separates them.
    if not rings:
        return db.Region()
    sgn = np.sign(max(rings, key=lambda t: abs(t[0]))[0])      # the largest ring is always an outer ring
    outers = [(a, p) for a, p in rings if np.sign(a) == sgn]
    holes = [(a, p) for a, p in rings if np.sign(a) != sgn]
    # assign each hole to the smallest outer ring that contains one of its points
    import shapely.geometry as sg
    from shapely.strtree import STRtree
    outer_polys = [sg.Polygon(p) for _, p in outers]
    tree = STRtree(outer_polys)
    hole_of = {i: [] for i in range(len(outers))}
    for _, hp in holes:
        pt = sg.Point(hp[0])
        cand = [i for i in tree.query(pt) if outer_polys[i].contains(pt)]
        if not cand:       # point exactly on the outer ring: try another vertex
            for q in hp[1:]:
                pt = sg.Point(q)
                cand = [i for i in tree.query(pt) if outer_polys[i].contains(pt)]
                if cand:
                    break
        if cand:
            hole_of[min(cand, key=lambda i: outer_polys[i].area)].append(hp)
    region = db.Region()
    for i, (_, p) in enumerate(outers):
        poly = db.Polygon([db.Point(int(x), int(y)) for x, y in p])
        for hp in hole_of[i]:
            poly.insert_hole([db.Point(int(x), int(y)) for x, y in hp])
        region.insert(poly)
    return region.merged()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", default=SLOT_DEFAULT)
    ap.add_argument("--scale", type=float, default=0.0975, help="um per source pixel (0.098 just fits the 86 um tall free region with no slack)")
    ap.add_argument("--out", default=HERE)
    ap.add_argument("--region", default=None, help="x0,y0,x1,y1 (um) free rectangle to centre the art in; default: from free_space.json")
    a = ap.parse_args()

    ln = pl.layer_numbers()
    metal_rules = pl.metal_rules()
    masks, box, (rgb, lab) = class_masks(os.path.join(HERE, "source/tughra_source.webp"), a.scale)
    # group per layer
    per_layer = {}
    for c, m in masks.items():
        L = LAYER_OF[c]
        per_layer[L] = per_layer.get(L, np.zeros_like(m)) | m
    cells_h, cells_w = next(iter(masks.values())).shape
    # pad the raster so growth at the border is not clipped
    PADC = int(round(2.5 / G))
    stats = {"scale_um_per_px": a.scale, "grid_um": G, "layers": {}}
    regions = {}
    proc = {}
    for L, m in per_layer.items():
        w, s = DESIGN[L]
        assert w >= metal_rules[L]["w"] and s >= metal_rules[L]["s"], (L, w, s)
        mp = np.pad(m, PADC)
        res = conform(mp, w, s)
        proc[L] = res
        regions[L] = res
    # common bounding box of everything after processing (cells, padded frame)
    allm = np.zeros_like(next(iter(proc.values())))
    for r in proc.values():
        allm |= r
    ys, xs = np.where(allm)
    cy0, cy1, cx0, cx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    for L in proc:
        proc[L] = proc[L][cy0:cy1, cx0:cx1]
    Hc, Wc = proc[next(iter(proc))].shape
    art_w, art_h = Wc * G, Hc * G
    # placement
    free_json = os.path.join(HERE, "free_space.json")
    j = json.load(open(free_json))
    if a.region:
        rect = [float(v) for v in a.region.split(",")]
    else:
        cand = [r for r in j["common_rects_um"] if (r[2] - r[0]) >= art_w and (r[3] - r[1]) >= art_h]
        if not cand:
            sys.exit(f"art {art_w:.2f} x {art_h:.2f} um does not fit any common free rectangle; lower --scale")
        rect = max(cand, key=lambda r: (r[2] - r[0]) * (r[3] - r[1]))
    rx0, ry0, rx1, ry1 = rect
    px = round((rx0 + rx1) / 2 - art_w / 2, 1)
    py = round((ry0 + ry1) / 2 - art_h / 2, 1)
    px = round(px / 0.05) * 0.05; py = round(py / 0.05) * 0.05
    stats["art_size_um"] = [art_w, art_h]
    stats["free_rect_um"] = rect
    stats["origin_um"] = [round(px, 3), round(py, 3)]

    # ---- cell + GDS
    ly = db.Layout(); ly.dbu = 0.001
    cell = ly.create_cell(CELL)
    layer_idx = {}
    for L in pl.METALS:
        if L in proc:
            layer_idx[L] = ly.layer(*ln[L + ".drawing"])
            reg = rings_to_region(proc[L])
            cell.shapes(layer_idx[L]).insert(reg)
            stats["layers"][L] = {"gds": list(ln[L + ".drawing"]), "polygons": reg.count(),
                                  "vertices": sum(p.num_points() for p in reg.each()), "area_um2": reg.area() * 1e-6,
                                  "colours": [c for c, v in LAYER_OF.items() if v == L]}
    art_path = os.path.join(a.out, "tughra_art.gds")
    ly.write(art_path)

    # ---- merged copy of slot_7
    m = db.Layout(); m.read(a.slot)
    if m.cell(CELL) is not None:
        sys.exit(f"cell {CELL} already exists in {a.slot}")
    top = m.cell("slot_7")
    art_cell = m.create_cell(CELL)
    for L in layer_idx:
        li = m.layer(*ln[L + ".drawing"])
        art_cell.shapes(li).insert(cell.shapes(layer_idx[L]))
    top.insert(db.CellInstArray(art_cell.cell_index(), db.Trans(int(round(px / m.dbu)), int(round(py / m.dbu)))))
    merged_path = os.path.join(a.out, "slot7_with_art.gds")
    m.write(merged_path)
    stats["files"] = {"art": "tughra_art.gds", "merged": "slot7_with_art.gds"}
    json.dump(stats, open(os.path.join(a.out, "build_stats.json"), "w"), indent=1)
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
