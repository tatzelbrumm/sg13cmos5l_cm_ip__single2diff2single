#!/usr/bin/env python3
"""Render PNG previews of tughra_art.gds: composite (top layer wins), per-layer panels, and side-by-side with the source.
usage: preview.py [art_dir]    (reads tughra_art.gds, writes preview_art.png, preview_layers.png, preview_side_by_side.png)
"""
import sys, os
import numpy as np, cv2
import klayout.db as db
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import segment as S, pdk_layers as pl

D = sys.argv[1] if len(sys.argv) > 1 else HERE
PX = 12                                  # preview pixels per um
BGC = (255, 255, 255)
# display colour of each layer = the artist's colour that the layer carries (orange/gold share Metal1: shown as in source)
LCOL = {"TopMetal1": ("purple",), "Metal4": ("green",), "Metal3": ("red",), "Metal2": ("blue",), "Metal1": ("orange", "gold")}


def region_of(ly, cell, ln):
    li = ly.find_layer(*ln)
    return db.Region(cell.begin_shapes_rec(li)) if li is not None else db.Region()


def raster(reg, W, H, ox, oy, dbu):
    img = np.zeros((H, W), np.uint8)
    for p in reg.each():
        def pts(contour):
            return np.array([[(q.x * dbu - ox) * PX, H - (q.y * dbu - oy) * PX] for q in contour.each_point()], np.int32)
        hull = np.array([[(q.x * dbu - ox) * PX, H - (q.y * dbu - oy) * PX] for q in p.each_point_hull()], np.int32)
        cv2.fillPoly(img, [hull], 255)
        for h in range(p.holes()):
            hp = np.array([[(q.x * dbu - ox) * PX, H - (q.y * dbu - oy) * PX] for q in p.each_point_hole(h)], np.int32)
            cv2.fillPoly(img, [hp], 0)
    return img


def main():
    ly = db.Layout(); ly.read(os.path.join(D, "tughra_art.gds"))
    cell = ly.cell("tughra_art"); dbu = ly.dbu
    bb = cell.bbox(); ox, oy = bb.left * dbu, bb.bottom * dbu
    W = int(np.ceil(bb.width() * dbu * PX)) + 1; H = int(np.ceil(bb.height() * dbu * PX)) + 1
    ln = pl.layer_numbers()
    refs = S.sample_refs(np.array(__import__("PIL.Image", fromlist=["Image"]).open(os.path.join(HERE, "source/tughra_source.webp")).convert("RGB")))
    col = {c: tuple(int(v) for v in refs[c]) for c in S.COLORS}
    comp = np.full((H, W, 3), 255, np.uint8)
    panels = []
    order = ["Metal1", "Metal2", "Metal3", "Metal4", "TopMetal1"]
    for L in order:
        reg = region_of(ly, cell, ln[L + ".drawing"])
        m = raster(reg, W, H, ox, oy, dbu) > 0
        colname = LCOL[L][0]
        comp[m] = col[colname]
        p = np.full((H, W, 3), 255, np.uint8); p[m] = col[colname]
        cv2.putText(p, f"{L} ({'+'.join(LCOL[L])})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
        panels.append(p)
    cv2.imwrite(os.path.join(D, "preview_art.png"), comp[..., ::-1])
    # layers: 5 panels in a column
    sc = 0.5
    ps = [cv2.resize(p, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA) for p in panels]
    cv2.imwrite(os.path.join(D, "preview_layers.png"), np.vstack(ps)[..., ::-1])
    # side by side with the source (legend row cut), same height
    src = np.array(__import__("PIL.Image", fromlist=["Image"]).open(os.path.join(HERE, "source/tughra_source.webp")).convert("RGB"))[:S.LEGEND_TOP]
    lab = S.classify(src.copy() if False else np.array(__import__("PIL.Image", fromlist=["Image"]).open(os.path.join(HERE, "source/tughra_source.webp")).convert("RGB")))
    ys, xs = np.where(lab >= 0)
    src = src[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h = comp.shape[0]
    src = cv2.resize(src, (int(src.shape[1] * h / src.shape[0]), h), interpolation=cv2.INTER_AREA)
    gap = np.full((h, 30, 3), 255, np.uint8)
    side = np.hstack([src, gap, comp])
    side = cv2.resize(side, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(D, "preview_side_by_side.png"), side[..., ::-1])
    print("wrote previews", comp.shape, side.shape)


def slot_context():
    """Whole slot_7 (existing metal in grey, TopMetal1 darker) with the art in its colours, from slot7_with_art.gds."""
    m = db.Layout(); m.read(os.path.join(D, "slot7_with_art.gds"))
    top = m.cell("slot_7"); dbu = m.dbu; ln = pl.layer_numbers()
    P = 3
    bb = top.bbox(); W = int(bb.width() * dbu * P) + 1; H = int(bb.height() * dbu * P) + 1
    img = np.full((H, W, 3), 255, np.uint8)
    refs = S.sample_refs(np.array(__import__("PIL.Image", fromlist=["Image"]).open(os.path.join(HERE, "source/tughra_source.webp")).convert("RGB")))
    col = {c: tuple(int(v) for v in refs[c]) for c in S.COLORS}
    art_idx = m.cell("tughra_art").cell_index()
    for L, g in [("Metal1", 200), ("Metal2", 185), ("Metal3", 170), ("Metal4", 150), ("TopMetal1", 215)]:
        li = m.find_layer(*ln[L + ".drawing"])
        # shapes outside the art cell only: skip the art instance
        it = db.RecursiveShapeIterator(m, top, li)
        it.unselect_cells([art_idx])
        reg = db.Region(it).merged()
        mask = np.zeros((H, W), np.uint8)
        for p in reg.each():
            hull = np.array([[q.x * dbu * P, H - q.y * dbu * P] for q in p.each_point_hull()], np.int32)
            cv2.fillPoly(mask, [hull], 255)
            for h in range(p.holes()):
                hp = np.array([[q.x * dbu * P, H - q.y * dbu * P] for q in p.each_point_hole(h)], np.int32)
                cv2.fillPoly(mask, [hp], 0)
        img[mask > 0] = (g, g, g)
    for L in ["Metal1", "Metal2", "Metal3", "Metal4", "TopMetal1"]:
        inst = [i for i in top.each_inst() if i.cell_index == art_idx][0]
        reg = db.Region(m.cell(art_idx).begin_shapes_rec(m.find_layer(*ln[L + ".drawing"]))).transformed(inst.trans).merged()
        mask = np.zeros((H, W), np.uint8)
        for p in reg.each():
            hull = np.array([[q.x * dbu * P, H - q.y * dbu * P] for q in p.each_point_hull()], np.int32)
            cv2.fillPoly(mask, [hull], 255)
            for h in range(p.holes()):
                hp = np.array([[q.x * dbu * P, H - q.y * dbu * P] for q in p.each_point_hole(h)], np.int32)
                cv2.fillPoly(mask, [hp], 0)
        img[mask > 0] = col[LCOL[L][0]]
    cv2.rectangle(img, (0, 0), (W - 1, H - 1), (0, 0, 0), 2)
    cv2.imwrite(os.path.join(D, "preview_slot_context.png"), img[..., ::-1])
    print("wrote slot context", img.shape)


main()
slot_context()
