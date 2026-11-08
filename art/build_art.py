#!/usr/bin/env python3
"""Build the tughra metal art for slot_7: image -> staircase polygons on five metal layers -> GDS.

usage: build_art.py [--slot SLOT_GDS] [--scale UM_PER_PX] [--out DIR]

Pipeline (all lengths in um, grid G = 0.05 um):
 1. segment.py splits the source image (legend row excluded) into six colour masks (soft coverage).
 2. The soft coverage is resampled to the 0.05 um grid at the chosen scale and cut at 0.5.
 3. Per layer (mapping in LAYER_OF): every stroke is widened along its centreline to the design minimum width
    (skeleton + disk of the minimum radius where the stroke is thinner), gaps below the design minimum space are
    closed.  Strokes are never narrowed, so thick strokes keep their shape.
 4. The binary image becomes a staircase polygon (runs of 0.05 um cells merged): only 0 / 90 degree edges, as the deck's
    angle rule allows, all vertices multiples of 0.05 um (on the 5 nm grid), and no 45-degree chamfers (see mask_to_region).
 5. Written as cell "tughra_art" (art/tughra_art.gds) and as a copy of slot_7 with the art placed in the common
    free region (art/slot7_with_art.gds).  The slot7 source file is only read.
The script re-runs deterministically.
"""
import argparse, json, os, sys
import numpy as np
import cv2
from skimage.morphology import skeletonize
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import segment as S
import pdk_layers as pl

G = 0.05                                   # raster grid (um); contour vertices land on multiples of G/2
LAYER_OF = {"red": "Metal1", "orange": "Metal1", "gold": "Metal1", "purple": "Metal2", "blue": "Metal3",
            "green": "Metal4"}
DESIGN = {                                 # (kernel cells n, chamfer cells c); flat = (n - 2c) * G, body = n * G
    "Metal1": (7, 1), "Metal2": (7, 1), "Metal3": (7, 1), "Metal4": (7, 1),    # 0.35 um body, 0.25 um flat
}
SLOT_DEFAULT = os.environ.get("SLOT7_GDS", "/home/user/sg13cmos5l_cm_slot7/final/gds/slot_7.gds")
CELL = "tughra_art"


def kernel(n, c):
    """n x n square with 45-degree corner chamfers of c cells: every row and column keeps a flat of n - 2c cells."""
    k = np.ones((n, n), np.uint8)
    for a in range(c):
        for b in range(c - a):
            k[a, b] = k[a, n - 1 - b] = k[n - 1 - a, b] = k[n - 1 - a, n - 1 - b] = 0
    return k


def widen_to_min(mask, K):
    """Every stroke at least as wide as K: stamp K on each skeleton pixel whose local half-width is smaller."""
    n = K.shape[0]
    dt = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 5)
    sk = skeletonize(mask)
    pts = np.zeros(mask.shape, np.uint8)
    pts[sk & (dt < n / 2 - 0.5)] = 1
    return mask | (cv2.dilate(pts, K) > 0)


def conform(mask, K):
    """Width floor along the centreline, then alternate closing (space) and opening (width) with the same kernel.

    The kernel is a chamfered square, not a disk: with a disk, the end of a stroke and every tight bend has rows only
    one or two cells wide, and the deck's Euclidean width / space check reports those (Mn.a, Mn.b). With the square,
    every flat extremity is at least n - 2c cells long, so it passes.
    """
    m = widen_to_min(mask, K)
    for _ in range(4):
        prev = m
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, K)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, K).astype(bool)
        if (m == prev).all():
            break
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, K)
    n_, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
    keep = np.zeros(m.shape, bool)
    for i in range(1, n_):
        if st[i, 4] >= 2 * K.shape[0] ** 2:           # drop specks smaller than two kernel squares
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


def mask_to_region(mask):
    """Binary mask (row 0 = top of the art) -> klayout Region in the art cell frame (origin = lower-left, dbu 1 nm).

    Every run of set cells in a row becomes a box of G x G cells; the union is a pure staircase (0 / 90 degree edges,
    all vertices multiples of G = 50 nm).  A 45-degree chamfer outline was tried first and rejected: two convex 45-degree
    turns over a short edge (every round end and tight bend) are reported by the deck as Mn.a / Mn.b / Mn.i violations,
    whereas a staircase has no chamfers.
    """
    H, W = mask.shape
    step = int(round(G / 0.001))
    region = db.Region()
    m = np.pad(mask.astype(np.int8), ((0, 0), (1, 1)))
    d = np.diff(m, axis=1)
    for r in range(H):
        starts = np.where(d[r] == 1)[0]
        ends = np.where(d[r] == -1)[0]
        y1 = (H - r) * step
        for a, b in zip(starts, ends):
            region.insert(db.Box(int(a) * step, y1 - step, int(b) * step, y1))
    return region.merged()


def repair(reg, w_um, s_um, margin_um=0.01, tries=20):
    """Patch what the raster morphology leaves: diagonal necks and tips that are narrower than the rule when measured
    Euclidean.  Runs the same width / space check as the deck on the Region; every marker is covered with a box
    (marker bbox + 75 nm, snapped outward to the 50 nm grid) and merged.  Repeats until the checks are empty."""
    dbu = 0.001
    w = int(round((w_um + margin_um) / dbu)); sp = int(round((s_um + margin_um) / dbu))
    grid = int(round(G / dbu)); pad = 75
    log = []
    for it in range(tries):
        bad = reg.width_check(w, False, db.Region.Euclidian)
        gap = reg.space_check(sp, False, db.Region.Euclidian)
        n = bad.count() + gap.count()
        log.append(n)
        if n == 0:
            break
        fill = db.Region()
        for ep in list(bad.each()) + list(gap.each()):
            b = ep.bbox().enlarged(pad, pad)
            fill.insert(db.Box((b.left // grid) * grid, (b.bottom // grid) * grid,
                               -((-b.right) // grid) * grid, -((-b.top) // grid) * grid))
        reg = (reg + fill).merged()
    return reg, log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", default=SLOT_DEFAULT)
    ap.add_argument("--scale", type=float, default=0.102, help="um per source pixel (largest that fits the 90 um tall region with slack)")
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
        n, c = DESIGN[L]
        flat = (n - 2 * c) * G
        assert flat >= metal_rules[L]["w"] and flat >= metal_rules[L]["s"], (L, flat)
        mp = np.pad(m, PADC)
        res = conform(mp, kernel(n, c))
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
    # shape fidelity: per layer, intersection-over-union of the final mask with the union of its source colours, and
    # per colour the share of the source colour area that the layer covers (same G grid, same crop)
    fid = {}
    for L, r in proc.items():
        cols = [c for c, v in LAYER_OF.items() if v == L]
        src = np.zeros_like(r)
        for c in cols:
            src |= np.pad(masks[c], PADC)[cy0:cy1, cx0:cx1]
        fid[L] = {"colours": cols, "iou": float((r & src).sum() / max(1, (r | src).sum())),
                  "area_ratio_final_over_source": float(r.sum() / max(1, src.sum())),
                  "source_area_covered": {c: float((r & np.pad(masks[c], PADC)[cy0:cy1, cx0:cx1]).sum() /
                                                   max(1, np.pad(masks[c], PADC)[cy0:cy1, cx0:cx1].sum())) for c in cols}}
    stats["fidelity"] = fid
    # colours that share a layer: which source colours end up in one connected polygon, and a per-cell colour map
    # (nearest source colour) so that previews can draw the shared layer in the artist's colours
    fused, cmap = {}, {}
    for L, r in proc.items():
        cols = [c for c, v in LAYER_OF.items() if v == L]
        if len(cols) < 2:
            continue
        raw = {c: np.pad(masks[c], PADC)[cy0:cy1, cx0:cx1] for c in cols}
        n_, lab_, st_, _ = cv2.connectedComponentsWithStats(r.astype(np.uint8), connectivity=4)
        fl = []
        for i in range(1, n_):
            comp = lab_ == i
            present = [c for c in cols if (comp & raw[c]).any()]
            if len(present) > 1:
                x_, y_, w_, h_, _a = st_[i]
                fl.append({"colours": present, "bbox_art_um": [round(x_ * G, 2), round((r.shape[0] - y_ - h_) * G, 2), round((x_ + w_) * G, 2), round((r.shape[0] - y_) * G, 2)],
                           "area_um2": round(float(_a) * G * G, 1)})
        fused[L] = fl
        dts = np.stack([cv2.distanceTransform((~raw[c]).astype(np.uint8), cv2.DIST_L2, 5) for c in cols])
        cmap[L] = (np.array([S.COLORS.index(c) for c in cols], np.uint8)[dts.argmin(0)])
    stats["fused_components"] = fused
    np.savez_compressed(os.path.join(a.out, "layer_colour_map.npz"), grid_um=G, **cmap)
    art_w, art_h = Wc * G, Hc * G
    # placement
    free_json = os.path.join(HERE, "free_space.json")
    j = json.load(open(free_json))
    if a.region:
        rect = [float(v) for v in a.region.split(",")]
    else:
        cand = [r for r in j["m1_m4_visible_rects_um"] if (r[2] - r[0]) >= art_w and (r[3] - r[1]) >= art_h]
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
            reg = mask_to_region(proc[L])
            r = metal_rules[L]
            reg, log = repair(reg, r["w"], r["s"])
            assert log[-1] == 0, (L, log)
            cell.shapes(layer_idx[L]).insert(reg)
            stats["layers"][L] = {"gds": list(ln[L + ".drawing"]), "polygons": reg.count(),
                                  "vertices": sum(p.num_points() for p in reg.each()), "area_um2": reg.area() * 1e-6, "repair_marker_counts": log,
                                  "colours": [c for c, v in LAYER_OF.items() if v == L]}
    art_path = os.path.join(a.out, "tughra_art.gds")
    opt = db.SaveLayoutOptions(); opt.format = 'GDS2'; opt.gds2_max_vertex_count = 4000
    ly.write(art_path, opt)

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
    m.write(merged_path, opt)
    stats["files"] = {"art": "tughra_art.gds", "merged": "slot7_with_art.gds"}
    json.dump(stats, open(os.path.join(a.out, "build_stats.json"), "w"), indent=1)
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
