# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Pictures of tree_pmos from its GDS (2026-11-07, Claude).

tree_pmos.png: the cell with device letters, lanes, pins, tie and a scale bar.
before_after.png: the naive tree's PMOS row (tree_row_p), the S2D pad's bias_tree_noab_p_c3 and tree_pmos, one scale.
Usage: python3 render_tree_pmos.py   (run from anywhere; paths relative to the repo)
"""
import os
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from matplotlib.patches import Rectangle, Polygon     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../../../.."))
STYLE = [  # layer, face, alpha, edge
    ((31, 0), "#f3e7c9", 1.0, "#b89b50"),   # NWell
    ((14, 0), "none", 1.0, "#d07a00"),      # pSD outline
    ((1, 0), "#7cc46b", 0.9, "#2f7a22"),    # Activ
    ((5, 0), "#e05050", 0.75, "#a01010"),   # GatPoly
    ((8, 0), "#4a7fd0", 0.45, "#1f4f99"),   # Metal1
    ((10, 0), "#a050c8", 0.45, "#6a1f99"),  # Metal2
    ((6, 0), "#202020", 1.0, "#202020"),    # Cont
    ((19, 0), "#ffffff", 1.0, "#000000"),   # Via1
]


def draw(ax, ly, cell, dx=0.0, dy=0.0):
    for (l, d), fc, a, ec in STYLE:
        li = ly.find_layer(l, d)
        if li is None:
            continue
        r = db.Region(cell.begin_shapes_rec(li)).merged()
        for p in r.each():
            pts = [((q.x * ly.dbu) + dx, (q.y * ly.dbu) + dy) for q in p.to_simple_polygon().each_point()]
            ax.add_patch(Polygon(pts, closed=True, fc=fc, alpha=a, ec=ec, lw=0.4))


def load(path, name):
    ly = db.Layout()
    ly.read(path)
    return ly, ly.cell(name)


def main():
    ly, c = load(os.path.join(HERE, "tree_pmos.gds"), "tree_pmos")
    bb = c.dbbox()
    fig, ax = plt.subplots(figsize=(16, 7.6), dpi=110)
    draw(ax, ly, c)
    # finger letters (TEXT 63/0 in the top cell)
    names = {"a": "BP", "b": "PBN", "c": "PBNC", "x": "x", "r": "r"}
    for s in c.each_shape(ly.find_layer(63, 0)):
        if s.is_text():
            t = s.dtext
            ax.text(t.x, t.y, t.string, ha="center", va="center", fontsize=15, weight="bold",
                    color="#7a0000" if t.string in "abc" else "#555555")
            ax.text(t.x, t.y - 0.7, names[t.string], ha="center", va="center", fontsize=6.5, rotation=90)
    ax.text(1.12, 5.0, "k\nBPC\n1/4", ha="center", va="center", fontsize=10, weight="bold", color="#7a0000")
    ax.text(1.18, 1.82, "t TGP", ha="center", va="center", fontsize=8, weight="bold", color="#7a0000")
    # lanes, pins
    labs = sorted((s.dtext for s in c.each_shape(ly.find_layer(8, 25)) if s.is_text()), key=lambda t: t.x)
    k = 0
    for t in labs:
        if t.string == "vdd":
            ax.text(bb.width() / 2, t.y + 0.05, "vdd plate + N tie (Metal1 pin along the top edge)", ha="center",
                    fontsize=9, color="#1f4f99")
            continue
        ax.annotate(t.string, (t.x, 0.0), (t.x, -0.55 - 0.4 * (k % 3)), ha="center", fontsize=9,
                    color="#1f4f99", arrowprops=dict(arrowstyle="-", color="#1f4f99", lw=0.6))
        k += 1
    for n, y in (("vbp", 1.02), ("vbn", 1.43), ("vbnc", 1.84)):
        ax.text(bb.width() + 0.15, y, "Metal2 lane " + n if n != "vbp" else "Metal2 lane vbp (also gate columns)",
                va="center", fontsize=7.5, color="#6a1f99")
    ax.plot([0.3, 5.3], [-1.9, -1.9], color="k", lw=2)
    ax.text(2.8, -2.25, "5 um", ha="center", fontsize=9)
    ax.set_title("tree_pmos  %.3f x %.3f um = %.1f um2   score  | k/t | n g | r a b c a b b x a b a c a b r | g n |"
                 % (bb.width(), bb.height(), bb.width() * bb.height()), fontsize=11)
    ax.set_xlim(-0.6, bb.width() + 4.2)
    ax.set_ylim(-2.6, bb.height() + 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "tree_pmos.png"))
    plt.close(fig)

    # before / after, one scale
    items = [(os.path.join(REPO, "macros/slot7_testplatform/layout/gds/bias_tree_noab_pd.gds"), "tree_row_p",
              "naive tree_row_p (PMOS row of bias_tree_noab_pd)"),
             (os.path.join(REPO, "macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds"),
              "bias_tree_noab_p_c3", "S2D pad bias_tree_noab_p_c3 (no BP, BPC)"),
             (os.path.join(HERE, "tree_pmos.gds"), "tree_pmos", "tree_pmos (all six PMOS devices)")]
    fig, ax = plt.subplots(figsize=(15, 9), dpi=100)
    y = 0.0
    for path, name, label in items:
        l2, c2 = load(path, name)
        b = c2.dbbox()
        draw(ax, l2, c2, -b.left, y - b.bottom)
        ax.add_patch(Rectangle((0, y), b.width(), b.height(), fill=False, ec="k", lw=0.8, ls="--"))
        ax.text(0, y + b.height() + 0.3, "%s: %.2f x %.2f um = %.0f um2" % (label, b.width(), b.height(),
                                                                       b.width() * b.height()), fontsize=10)
        y += b.height() + 2.5
    ax.plot([0, 10], [-1.2, -1.2], color="k", lw=2)
    ax.text(5, -2.0, "10 um", ha="center")
    ax.set_xlim(-1, 38)
    ax.set_ylim(-2.5, y)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "before_after.png"))
    plt.close(fig)


if __name__ == "__main__":
    main()
