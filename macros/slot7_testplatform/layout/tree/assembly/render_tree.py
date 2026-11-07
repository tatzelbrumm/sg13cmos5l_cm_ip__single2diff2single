# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Pictures of bias_tree_noab_pd from its GDS (2026-11-07, Claude).

bias_tree_noab_pd.png: the assembled cell; the top-level routing drawn in one colour per net, halves outlined.
before_after.png: the naive cell (macros/slot7_testplatform/layout/gds/bias_tree_noab_pd.gds) and the assembled
cell at one scale.
Usage: python3 render_tree.py   (run from anywhere)
"""
import os

import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from matplotlib.patches import Polygon, Rectangle     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../../../.."))
GDS = os.path.join(HERE, "bias_tree_noab_pd.gds")
NAIVE = os.path.join(REPO, "macros/slot7_testplatform/layout/gds/bias_tree_noab_pd.gds")
STYLE = [  # layer, face, alpha, edge
    ((31, 0), "#f3e7c9", 1.0, "#b89b50"),   # NWell
    ((1, 0), "#7cc46b", 0.9, "#2f7a22"),    # Activ
    ((5, 0), "#e05050", 0.6, "#a01010"),    # GatPoly
    ((8, 0), "#4a7fd0", 0.35, "#1f4f99"),   # Metal1
    ((10, 0), "#a050c8", 0.35, "#6a1f99"),  # Metal2
    ((19, 0), "#ffffff", 1.0, "#000000"),   # Via1
]
NETC = {"iref": "#d62728", "en_3v3": "#ff7f0e", "en_3v3_b": "#bcbd22", "vbp": "#1f77b4", "vbn": "#2ca02c",
        "vbpc": "#17becf", "vbnc": "#9467bd", "ni": "#8c564b"}


def polys(ly, cell, ld, rec=True):
    li = ly.find_layer(*ld)
    if li is None:
        return db.Region()
    return (db.Region(cell.begin_shapes_rec(li)) if rec else db.Region(cell.shapes(li))).merged()


def draw(ax, ly, cell, dx=0.0, dy=0.0, lw=0.3):
    for ld, fc, a, ec in STYLE:
        for p in polys(ly, cell, ld).each():
            pts = [(q.x * ly.dbu + dx, q.y * ly.dbu + dy) for q in p.to_simple_polygon().each_point()]
            ax.add_patch(Polygon(pts, closed=True, fc=fc, alpha=a, ec=ec, lw=lw))
    b = cell.dbbox()
    ax.add_patch(Rectangle((b.left + dx, b.bottom + dy), b.width(), b.height(), fill=False, ec="k", lw=0.8))


def net_of_top_shapes(ly, top):
    """Top-level Metal1 / Metal2 / Via1 shapes coloured by the net the hierarchical net extractor finds."""
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, top, []))
    m1, v1, m2 = (l2n.make_layer(ly.layer(*ld), n) for ld, n in [((8, 0), "m1"), ((19, 0), "v1"), ((10, 0), "m2")])
    l2n.make_text_layer(ly.layer(8, 25), "t1")
    l2n.make_text_layer(ly.layer(10, 25), "t2")
    l2n.connect(m1)
    l2n.connect(m2)
    l2n.connect(m1, v1)
    l2n.connect(v1, m2)
    l2n.connect(m1, l2n.layer_by_name("t1"))
    l2n.connect(m2, l2n.layer_by_name("t2"))
    l2n.extract_netlist()
    out = []
    for lay, ld in [(m1, (8, 0)), (m2, (10, 0))]:
        for s in top.shapes(ly.layer(*ld)).each():
            b = s.bbox()
            pt = b.center()
            net = l2n.probe_net(lay, db.DPoint(pt.x * ly.dbu, pt.y * ly.dbu))
            out.append((ld, b, net.expanded_name() if net else "?"))
    return out


def main():
    ly = db.Layout()
    ly.read(GDS)
    top = ly.cell("bias_tree_noab_pd")
    bb = top.dbbox()
    fig, ax = plt.subplots(figsize=(17, 11))
    draw(ax, ly, top)
    names = {}
    for ld, b, net in net_of_top_shapes(ly, top):
        net = net.split(".")[-1]
        if net in ("vdd", "vss"):
            continue
        if net not in NETC:                         # unlabelled internal net: the ni bridge
            net = "ni"
        d = b.to_dtype(ly.dbu)
        ax.add_patch(Rectangle((d.left, d.bottom), d.width(), d.height(), fc=NETC[net], alpha=0.85 if ld[0] == 10
                               else 0.5, ec=NETC[net], lw=0.6, hatch=None if ld[0] == 10 else "////"))
        names[net] = 1
    for inst in top.each_inst():
        b = inst.dbbox()
        ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False, ec="#444", lw=1.2, ls="--"))
        ax.text(b.left + 0.3, b.top - 0.6 if inst.cell.name == "tree_nmos" else b.bottom + 4.2, inst.cell.name,
                fontsize=10, color="#333", weight="bold")
    for s in top.shapes(ly.layer(10, 25)).each():
        t = s.text
        ax.annotate(t.string, (t.x * ly.dbu, t.y * ly.dbu), xytext=(bb.right + 0.6, t.y * ly.dbu), fontsize=10,
                    va="center", color=NETC.get(t.string, "k"), arrowprops=dict(arrowstyle="-", lw=0.5))
    ax.text(bb.center().x, bb.top - 0.68, "vdd rail (Metal1, tree_pmos's plate + N tie, full width)", ha="center",
            va="center", fontsize=9, color="#1f4f99")
    ax.text(bb.center().x, 0.45, "vss rail (Metal1, tree_nmos's plate + p+ tie)", ha="center", va="center",
            fontsize=9, color="#1f4f99")
    for n, c in NETC.items():
        ax.plot([], [], color=c, lw=6, label=n)
    ax.legend(loc="upper left", bbox_to_anchor=(1.06, 1.0), fontsize=9, title="top-level routing\n(solid M2, hatched M1)")
    ax.plot([1, 6], [-1.0, -1.0], "k-", lw=2)
    ax.text(3.5, -1.5, "5 um", ha="center", va="top")
    ax.set_xlim(bb.left - 0.5, bb.right + 4.5)
    ax.set_ylim(bb.bottom - 2.2, bb.top + 0.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("bias_tree_noab_pd  %.2f x %.2f = %.1f um2  (naive 57.31 x 34.41 = 1972 um2)" % (
        bb.width(), bb.height(), bb.width() * bb.height()))
    fig.savefig(os.path.join(HERE, "bias_tree_noab_pd.png"), dpi=110, bbox_inches="tight")
    plt.close(fig)

    nl = db.Layout()
    nl.read(NAIVE)
    nt = nl.top_cell()
    nb = nt.dbbox()
    fig, ax = plt.subplots(figsize=(16, 7.5))
    draw(ax, nl, nt, -nb.left, -nb.bottom, lw=0.2)
    gx = nb.width() + 4
    draw(ax, ly, top, gx, 0, lw=0.2)
    ax.text(nb.width() / 2, nb.height() + 1, "before: naive %s %.2f x %.2f = %.0f um2" % (
        nt.name, nb.width(), nb.height(), nb.width() * nb.height()), ha="center", fontsize=11)
    ax.text(gx + bb.width() / 2, bb.height() + 1, "after: assembled %.2f x %.2f = %.0f um2 (%.0f %%)" % (
        bb.width(), bb.height(), bb.width() * bb.height(),
        100 * (bb.width() * bb.height() / (nb.width() * nb.height()) - 1)), ha="center", fontsize=11)
    ax.plot([0, 10], [-2, -2], "k-", lw=2)
    ax.text(5, -2.6, "10 um", ha="center", va="top")
    ax.set_xlim(-1, gx + bb.width() + 1)
    ax.set_ylim(-4, max(nb.height(), bb.height()) + 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(os.path.join(HERE, "before_after.png"), dpi=100, bbox_inches="tight")
    plt.close(fig)
    print("wrote bias_tree_noab_pd.png, before_after.png")


if __name__ == "__main__":
    main()
