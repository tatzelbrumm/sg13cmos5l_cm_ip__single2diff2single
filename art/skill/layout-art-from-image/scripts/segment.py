"""Split the calligraphy image into six colour masks (soft coverage), legend row excluded.

Colour references are sampled from the legend squares at the bottom of the image (so they are the artist's own six
colours). Class = hue range of the pixel; orange vs gold share a hue band and are told apart by position (the orange
word sits left of x=795 and above y=676; gold is everything warm outside that box).
"""
import numpy as np, cv2
from PIL import Image

COLORS = ["red", "blue", "green", "orange", "purple", "gold"]
LEGEND_TOP = 897            # first image row of the legend (row 897 is the first with legend ink; art ends at row 896)
ORANGE_BOX = (0, 0, 795, 676)   # x0, y0, x1, y1 in source pixels
BG = np.array([254, 254, 251], np.float32)


def sample_refs(rgb):
    """Median colour of each legend square (found as saturated square blobs below the art)."""
    sub = rgb[LEGEND_TOP:].astype(np.float32)
    hsv = cv2.cvtColor(rgb[LEGEND_TOP:], cv2.COLOR_RGB2HSV_FULL)
    sat = (hsv[..., 1] > 150).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(sat)
    sq = []
    for i in range(1, n):
        if st[i, 4] > 800 and abs(st[i, 2] - st[i, 3]) < 6:
            cx, cy = int(cen[i][0]), int(cen[i][1])
            sq.append((cx, np.median(sub[cy - 6:cy + 7, cx - 6:cx + 7].reshape(-1, 3), 0)))
    sq.sort(key=lambda t: t[0])           # left to right: red green orange purple blue gold
    names = ["red", "green", "orange", "purple", "blue", "gold"]
    assert len(sq) == 6, len(sq)
    return {n: c for n, (x, c) in zip(names, sq)}


def classify(rgb):
    a = rgb[:LEGEND_TOP]
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    h = hsv[..., 0] * 360 / 255; s = hsv[..., 1] / 255
    ink = s > 0.28
    H, W = h.shape
    lab = np.full((H, W), -1, np.int8)
    idx = {c: i for i, c in enumerate(COLORS)}
    lab[ink & ((h >= 330) | (h < 12))] = idx["red"]
    lab[ink & (h >= 65) & (h < 170)] = idx["green"]
    lab[ink & (h >= 170) & (h < 245)] = idx["blue"]
    lab[ink & (h >= 245) & (h < 330)] = idx["purple"]
    warm = ink & (h >= 12) & (h < 65)
    X, Y = np.meshgrid(np.arange(W), np.arange(H))
    inbox = (X >= ORANGE_BOX[0]) & (X < ORANGE_BOX[2]) & (Y >= ORANGE_BOX[1]) & (Y < ORANGE_BOX[3])
    lab[warm & inbox] = idx["orange"]
    lab[warm & ~inbox] = idx["gold"]
    # 5x5 mode filter inside the ink: relabels hue-mixed fringe pixels where two colours touch
    k = np.ones((5, 5), np.float32)
    votes = np.stack([cv2.filter2D((lab == i).astype(np.float32), -1, k) for i in range(6)])
    mode = votes.argmax(0).astype(np.int8)
    lab = np.where(lab >= 0, mode, -1).astype(np.int8)
    return lab


def coverage(rgb, lab, refs):
    """Soft coverage (0..1) of the class colour over the off-white background, per pixel."""
    P = rgb[:LEGEND_TOP].astype(np.float32) - BG
    cov = np.zeros((6,) + lab.shape, np.float32)
    for i, c in enumerate(COLORS):
        d = np.array(refs[c], np.float32) - BG
        al = np.clip((P @ d) / (d @ d), 0, 1)
        cov[i] = np.where(lab == i, al, 0)
    return cov


def load(path):
    rgb = np.array(Image.open(path).convert("RGB"))
    refs = sample_refs(rgb)
    lab = classify(rgb)
    return rgb, refs, lab, coverage(rgb, lab, refs)


if __name__ == "__main__":
    import sys
    rgb, refs, lab, cov = load(sys.argv[1])
    print({k: v.tolist() for k, v in refs.items()})
    vis = np.full(rgb[:LEGEND_TOP].shape, 255, np.uint8)
    cols = np.array([refs[c] for c in COLORS], np.uint8)
    vis[lab >= 0] = cols[lab[lab >= 0]]
    Image.fromarray(vis).save(sys.argv[2])
    for i, c in enumerate(COLORS):
        print(c, int((lab == i).sum()))
