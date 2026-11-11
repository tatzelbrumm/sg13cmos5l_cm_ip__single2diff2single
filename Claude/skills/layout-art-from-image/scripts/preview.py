#!/usr/bin/env python3
"""Render PNG previews from the GDS files: composite (upper layer wins), per-layer panels, side by side with the source,
and the art in place inside slot_7.
usage: preview.py [art_dir]   reads tughra_art.gds, slot7_with_art.gds, layer_colour_map.npz
writes preview_art.png, preview_layers.png, preview_side_by_side.png, preview_slot_context.png
Layers shared by several colours (Metal1: red, orange) are drawn in the colour of the nearest source stroke
(layer_colour_map.npz, written by build_art.py); the GDS itself carries no colour.
"""
import sys, os
import numpy as np, cv2
from PIL import Image
import klayout.db as db
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import segment as S, pdk_layers as pl

D = sys.argv[1] if len(sys.argv) > 1 else HERE
PX = 12                                  # preview pixels per um
LAYERS = ["GatPoly", "Metal1", "Metal2", "Metal3", "Metal4"]           # bottom to top
LCOL = {"GatPoly": ("purple",), "Metal1": ("red", "orange"), "Metal2": ("gold",), "Metal3": ("blue",), "Metal4": ("green",)}
SRC = os.path.join(HERE, "source/tughra_source.webp")


def load_cols():
    rgb = np.array(Image.open(SRC).convert("RGB"))
    refs = S.sample_refs(rgb)
    return rgb, {c: tuple(int(v) for v in refs[c]) for c in S.COLORS}


def raster(reg, W, H, ox, oy, dbu, px):
    """Region (dbu) -> uint8 mask, pixel (0,0) = top-left of the box whose lower-left is (ox, oy) um."""
    img = np.zeros((H, W), np.uint8)
    for p in reg.each():
        hull = np.array([[(q.x * dbu - ox) * px, H - (q.y * dbu - oy) * px] for q in p.each_point_hull()], np.int32)
        cv2.fillPoly(img, [hull], 255)
        for h in range(p.holes()):
            hp = np.array([[(q.x * dbu - ox) * px, H - (q.y * dbu - oy) * px] for q in p.each_point_hole(h)], np.int32)
            cv2.fillPoly(img, [hp], 0)
    return img


def layer_rgb(L, mask, W, H, ox_art, oy_art, px, cmaps, col):
    """Colour image for one layer's mask; (ox_art, oy_art) = art-cell coordinates (um) of the lower-left pixel corner."""
    out = np.full((H, W, 3), 255, np.uint8)
    cols = LCOL[L]
    if len(cols) == 1 or L not in cmaps:
        out[mask > 0] = col[cols[0]]
        return out
    cm = cmaps[L]; Hc, Wc = cm.shape; G = float(cmaps["grid_um"])
    yy, xx = np.nonzero(mask)
    xa = ox_art + (xx + 0.5) / px; ya = oy_art + (H - yy - 0.5) / px
    cc = np.clip((xa / G).astype(int), 0, Wc - 1); rr = np.clip(Hc - 1 - (ya / G).astype(int), 0, Hc - 1)
    lab = cm[rr, cc]
    colarr = np.array([col[c] for c in S.COLORS], np.uint8)
    out[yy, xx] = colarr[lab]
    return out


def main():
    rgb, col = load_cols()
    cmaps = np.load(os.path.join(D, "layer_colour_map.npz"))
    cmaps = {k: cmaps[k] for k in cmaps.files}
    ly = db.Layout(); ly.read(os.path.join(D, "tughra_art.gds"))
    cell = ly.cell("tughra_art"); dbu = ly.dbu; ln = pl.layer_numbers()
    allreg = db.Region()                    # box of the art layers only (the no-fill markers are larger)
    for L in LAYERS:
        li = ly.find_layer(*ln[L + ".drawing"])
        if li is not None:
            allreg += db.Region(cell.begin_shapes_rec(li))
    bb = allreg.bbox(); ox, oy = bb.left * dbu, bb.bottom * dbu
    W = int(np.ceil(bb.width() * dbu * PX)) + 1; H = int(np.ceil(bb.height() * dbu * PX)) + 1
    comp = np.full((H, W, 3), 255, np.uint8); panels = []
    for L in LAYERS:
        li = ly.find_layer(*ln[L + ".drawing"])
        reg = db.Region(cell.begin_shapes_rec(li)) if li is not None else db.Region()
        m = raster(reg, W, H, ox, oy, dbu, PX)
        img = layer_rgb(L, m, W, H, ox, oy, PX, cmaps, col)
        comp[m > 0] = img[m > 0]
        p = img.copy()
        cv2.putText(p, f"{L} ({'+'.join(LCOL[L])})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
        panels.append(p)
    cv2.imwrite(os.path.join(D, "preview_art.png"), comp[..., ::-1])
    ps = [cv2.resize(p, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA) for p in panels]
    cv2.imwrite(os.path.join(D, "preview_layers.png"), np.vstack(ps)[..., ::-1])
    # side by side with the source (legend row cut), same height
    src = rgb[:S.LEGEND_TOP]
    lab = S.classify(rgb)
    ys, xs = np.where(lab >= 0)
    src = src[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h = comp.shape[0]
    src = cv2.resize(src, (int(src.shape[1] * h / src.shape[0]), h), interpolation=cv2.INTER_AREA)
    side = np.hstack([src, np.full((h, 30, 3), 255, np.uint8), comp])
    side = cv2.resize(side, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(D, "preview_side_by_side.png"), side[..., ::-1])
    print("wrote previews", comp.shape, side.shape)

    # ---- the art in place in slot_7
    m = db.Layout(); m.read(os.path.join(D, "slot7_with_art.gds"))
    top = m.cell("slot_7"); dbu = m.dbu
    P = 3
    bb = top.bbox(); Ws = int(bb.width() * dbu * P) + 1; Hs = int(bb.height() * dbu * P) + 1
    img = np.full((Hs, Ws, 3), 255, np.uint8)
    art_idx = m.cell("tughra_art").cell_index()
    inst = [i for i in top.each_inst() if i.cell_index == art_idx][0]
    ax, ay = inst.trans.disp.x * dbu, inst.trans.disp.y * dbu
    greys = {"GatPoly": 228, "Metal1": 200, "Metal2": 185, "Metal3": 170, "Metal4": 150, "TopMetal1": 215}
    for L in ["GatPoly", "Metal1", "Metal2", "Metal3", "Metal4", "TopMetal1"]:
        li = m.find_layer(*ln[L + ".drawing"])
        it = db.RecursiveShapeIterator(m, top, li)
        it.unselect_cells([art_idx])                       # everything except the art
        mask = raster(db.Region(it).merged(), Ws, Hs, 0, 0, dbu, P)
        img[mask > 0] = (greys[L],) * 3
    for L in LAYERS:
        reg = db.Region(m.cell(art_idx).begin_shapes_rec(m.find_layer(*ln[L + ".drawing"]))).transformed(inst.trans).merged()
        mask = raster(reg, Ws, Hs, 0, 0, dbu, P)
        rgbL = layer_rgb(L, mask, Ws, Hs, -ax, 0 - ay, P, cmaps, col)
        img[mask > 0] = rgbL[mask > 0]
    cv2.rectangle(img, (0, 0), (Ws - 1, Hs - 1), (0, 0, 0), 2)
    cv2.imwrite(os.path.join(D, "preview_slot_context.png"), img[..., ::-1])
    print("wrote slot context", img.shape)


main()
