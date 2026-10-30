# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Pictures of oa_n10 / oa_mcs_c rendered from the GDS (IHP sg13cmos5l part), 2026-10-28, Claude (Opus 5.5).

    python3 make_pictures.py <oa_n_cells.gds> <oa_n_cells.cdl> <pad_buffer_cells.gds> <out_dir>

Writes <out_dir>/oa_n10.png, <out_dir>/oa_mcs_c.png (cell renders), ./pictures/{tile,before_after,rule_savings}.png
(IHP numbers) and ../generic/pictures/tile_roles.png (roles only, no process numbers).
IHP-only: track net names come from tools/oa_core_pd_lvs.py (cross reference against the .cdl).
"""
import os
import sys
import importlib.util
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "generic"))
import adapter                                       # noqa: E402
import render as rd                                  # noqa: E402

GDS, CDL, LIB, OUT = sys.argv[1:5]
P = adapter.Process()
spec = importlib.util.spec_from_file_location("lvs", os.path.join(HERE, "tools", "oa_core_pd_lvs.py"))
lvsm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lvsm)
ly = db.Layout()
ly.read(GDS)
NAMES = {"M10": "M10", "M11": "M11", "MC10": "MC10", "MS2": "MS2", "MS3": "MS3", "SKS": "SKS", "dummy": "d",
         "MCS": "MCS", "MCL": "MCL"}
LETTERS = {"M10": "A", "M11": "B", "MC10": "C", "MS2": "S", "MS3": "MS3", "SKS": "SKS", "dummy": "d"}


def namer_for(cell):
    """net name at a point on Metal2, from the LVS cross reference (labels for pins, reference names for the rest)"""
    lvs, fly, _ = lvsm.extract(GDS, cell, "top")
    c = lvs.netlist().circuit_by_name(cell)
    import re
    blk = re.search(r"^\.SUBCKT\s+%s\b.*?^\.ENDS\b[^\n]*" % cell, open(CDL).read(), re.S | re.M | re.I).group(0)
    tmp = os.path.join(OUT, ".ref_%s.cdl" % cell)
    open(tmp, "w").write(blk + "\n")
    ref = db.Netlist()
    ref.read(tmp, db.NetlistSpiceReader())
    os.remove(tmp)
    ref.combine_devices()
    rc = ref.circuit_by_name(cell)
    lvs.netlist().case_sensitive = False
    for p in rc.each_pin():
        pin = c.create_pin(p.name())
        n = c.net_by_name(p.name())
        if n is not None:
            c.connect_pin(pin, n)
    lvs.reference = ref
    lvs.compare(db.NetlistComparer())
    nm = {}
    for cp in lvs.xref().each_circuit_pair():
        for np_ in lvs.xref().each_net_pair(cp):
            if np_.first() is not None and np_.second() is not None:
                nm[np_.first().cluster_id] = np_.second().expanded_name().lower()
    m2 = lvs.layer_by_name("m2")
    return lambda pt: (lambda n: nm.get(n.cluster_id, "?") if n else "?")(lvs.probe_net(m2, pt))


def cell_render(cell, fn, ppu=42):
    c = ly.cell(cell)
    bb = c.dbbox()
    fig, ax = plt.subplots(figsize=((bb.width() + 3) * ppu / 100, (bb.height() + 3.5) * ppu / 100))
    rd.draw_cell(ax, ly, c, P)
    rd.finger_letters(ax, ly, c, P, NAMES, size=8)
    rd.track_names(ax, ly, c, P, namer_for(cell), window=bb, size=6.5)
    rd.pins(ax, ly, c, P, size=8)
    rd.outline(ax, bb, cell)
    rd.scale_bar(ax, bb.left, bb.bottom - 1.2, 5.0)
    ax.set_xlim(bb.left - 1.5, bb.right + 1.5)
    ax.set_ylim(bb.bottom - 1.6, bb.top + 1.9)
    ax.set_aspect("equal")
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")
    ax.grid(True, lw=0.2, alpha=0.4)
    fig.tight_layout()
    fig.savefig(fn, dpi=100)
    plt.close(fig)


def tile(fn, numbers=True):
    c = ly.cell("oa_n10")
    w = db.DBox(-1.4, -1.0, 13.2, 6.0)
    ppu = 80
    fig, ax = plt.subplots(figsize=(w.width() * ppu / 100 + 1.0, w.height() * ppu / 100 + 1.2))
    rd.draw_cell(ax, ly, c, P, window=w)
    rd.finger_letters(ax, ly, c, P, LETTERS, window=w, size=12)
    if numbers:
        rd.track_names(ax, ly, c, P, namer_for("oa_n10"), window=w, size=8)
        rd.scale_bar(ax, 8.0, -0.85, 2.0)
        ttl = "pattern tile: rows X0-X2 of oa_n10 (A = M10, B = M11, d = 2/1 dummy), IHP sg13cmos5l"
    else:
        for y, s in ((0.15, "track over B line: net of A.S"), (1.53, "track over T line: net of A.D"),
                     (2.04, "track over B line: net of B.S"), (3.42, "track over T line: net of B.D")):
            ax.text(4.0, y, s, fontsize=8, va="center", color="#300050",
                    bbox=dict(boxstyle="round,pad=0.05", fc="white", ec="none", alpha=0.75))
        ttl = "pattern tile: rows of fingers, tracks over the stripes, rows at the minimum active space"
    notes = [(-0.72, 5.6, "joiner\n(A.D net)", 90), (-0.28, 4.6, "gate bar", 90), (1.0, 5.6, "dummy strap\n(D=S)", 90),
             (6.0, -0.75, "substrate tie segment (one contact row), only below", 0)]
    for x, y, s, r in notes:
        ax.text(x, y, s, fontsize=7.5, rotation=r, ha="center", va="center", color="#7a0000",
                bbox=dict(boxstyle="round,pad=0.08", fc="#fff6e0", ec="#7a0000", lw=0.4, alpha=0.9))
    ax.set_xlim(w.left, w.right)
    ax.set_ylim(w.bottom, w.top)
    ax.set_aspect("equal")
    if numbers:
        ax.set_xlabel("x (um)")
        ax.set_ylabel("y (um)")
        ax.grid(True, lw=0.2, alpha=0.4)
    else:
        ax.set_xticks([])
        ax.set_yticks([])
    ax.set_title(ttl, fontsize=10)
    fig.tight_layout()
    fig.savefig(fn, dpi=100)
    plt.close(fig)


def before_after(fn):
    lib = db.Layout()
    lib.read(LIB)
    old = [("oa_nmir", lib.cell("oa_nmir")), ("oa_misc_n", lib.cell("oa_misc_n")), ("oa_mcs", lib.cell("oa_mcs"))]
    new_n10, new_mcs = ly.cell("oa_n10"), ly.cell("oa_mcs_c")
    ppu = 16
    fig, axs = plt.subplots(1, 2, figsize=(2 * 75 * ppu / 100, 50 * ppu / 100))
    # before: the old cells side by side / stacked as compactly as their bounding boxes allow (gaps 2 um)
    ax = axs[0]
    x, ytop = 0.0, 40.0
    tot = 0
    bbn = old[0][1].dbbox()
    pos = {"oa_nmir": (0 - bbn.left, ytop - bbn.top)}
    bbm = old[1][1].dbbox()
    pos["oa_misc_n"] = (bbn.width() + 2 - bbm.left, ytop - bbm.top)
    bbc = old[2][1].dbbox()
    pos["oa_mcs"] = (0 - bbc.left, ytop - bbn.height() - 2 - bbc.top)
    for name, c in old:
        t = db.DCplxTrans(1, 0, False, *pos[name])
        rd.draw_cell(ax, lib, c, P, trans=t.to_itrans(lib.dbu) if False else db.ICplxTrans(t, lib.dbu))
        b = c.dbbox().transformed(t)
        rd.outline(ax, b, name)
        tot += b.width() * b.height()
    ax.set_title("before (library 2026-10-27): bounding boxes sum %.0f um2" % tot, fontsize=11)
    # after: oa_n10 with oa_mcs_c below, tie shared (placement of the pair check)
    ax2 = axs[1]
    off = (4.91, -7.99)
    bb1 = new_n10.dbbox()
    t1 = db.DCplxTrans(1, 0, False, -bb1.left, ytop - bb1.top)
    t2 = db.DCplxTrans(1, 0, False, -bb1.left + off[0], ytop - bb1.top + off[1])
    rd.draw_cell(ax2, ly, new_n10, P, trans=db.ICplxTrans(t1, ly.dbu))
    rd.draw_cell(ax2, ly, new_mcs, P, trans=db.ICplxTrans(t2, ly.dbu))
    b1, b2 = bb1.transformed(t1), new_mcs.dbbox().transformed(t2)
    rd.outline(ax2, b1, "oa_n10 (incl. MC10 MS2 MS3 SKS)")
    ax2.text(b2.left, b2.bottom - 1.6, "oa_mcs_c  %.2f x %.2f um = %.0f um2  (tie shared with oa_n10)"
             % (b2.width(), b2.height(), b2.width() * b2.height()), fontsize=9, color="#aa00aa")
    ax2.add_patch(plt.Rectangle((b2.left, b2.bottom), b2.width(), b2.height(), fill=False, ec="#aa00aa", ls="--"))
    un = b1 + b2
    ax2.set_title("after: oa_n10 + oa_mcs_c, %.2f x %.2f um = %.0f um2 together (bounding boxes %.0f um2)"
                  % (un.width(), un.height(), un.width() * un.height(), b1.width() * b1.height() + b2.width() * b2.height()),
                  fontsize=11)
    for a in axs:
        a.set_xlim(-3, 72)
        a.set_ylim(-1, 46)
        a.set_aspect("equal")
        a.grid(True, lw=0.2, alpha=0.4)
        rd.scale_bar(a, 50, 1.0, 10.0)
    fig.tight_layout()
    fig.savefig(fn, dpi=100)
    plt.close(fig)


def rule_savings(fn):
    lib = db.Layout()
    lib.read(LIB)
    fig = plt.figure(figsize=(17, 15))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15])
    red = dict(fontsize=10, color="#a00000", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#a00000", lw=0.6))
    arr = dict(arrowstyle="->", color="#a00000", lw=1.2)
    # (1) old oa_nmir: shared centre tap row between two rows, M2 trunks over the channels
    ax = fig.add_subplot(gs[0, 0])
    c = lib.cell("oa_nmir")
    w = db.DBox(-2.6, -5.0, 8.0, 2.0)
    rd.draw_cell(ax, lib, c, P, window=w)
    ax.annotate("inner tap row between the rows\n(ptap1: Activ 0.78, 2 contact rows)\nnot allowed any more (user 02:36)",
                (5.0, -1.4), (8.4, -2.4), arrowprops=arr, **red)
    ax.annotate("Metal2 trunks run\nover the channels", (6.0, 0.5), (8.4, 0.6), arrowprops=arr, **red)
    ax.set_xlim(w.left, w.right + 6.5)
    ax.set_ylim(w.bottom, w.top)
    ax.set_aspect("equal")
    ax.set_title("before: oa_nmir, unrotated 10/1 fingers (crop)", fontsize=11)
    # (2) new: rows at Act.b, tracks over the stripes, one-row tie segment below
    ax = fig.add_subplot(gs[0, 1])
    c = ly.cell("oa_n10")
    w = db.DBox(-1.0, -1.0, 9.6, 6.0)
    rd.draw_cell(ax, ly, c, P, window=w)
    rd.finger_letters(ax, ly, c, P, LETTERS, window=w, size=11)
    ax.annotate("row gap = Act.b 0.21:\nno band between rows,\nthe tracks run over the stripes", (9.4, 1.78), (10.0, 0.9),
                arrowprops=arr, **red)
    ax.annotate("3 Via1 on an M1 pad,\n0.21 = V1.a + 2 V1.c", (7.7, 2.04), (10.0, 3.2), arrowprops=arr, **red)
    ax.annotate("finger gap = Gat.b1 0.25:\nthe poly endcaps merge", (2.125, 4.6), (10.0, 5.2), arrowprops=arr, **red)
    ax.annotate("tie segment: Activ 0.30 = Cnt.a + 2 Cnt.c,\none contact row, Act.b 0.21 below row X0", (8.0, -0.36),
                (10.0, -0.7), arrowprops=arr, **red)
    ax.set_xlim(w.left, w.right + 6.5)
    ax.set_ylim(w.bottom, w.top)
    ax.set_aspect("equal")
    ax.set_title("after: oa_n10, rows X0-X2 (crop, same scale)", fontsize=11)
    # (3) LU: one tie segment, farthest N+ Activ 18.9 um < LU_b 20 um -> no tie on the other three sides
    ax = fig.add_subplot(gs[1, :])
    bb = c.dbbox()
    rd.draw_cell(ax, ly, c, P, alpha=0.6)
    ax.annotate("", (12.5, -0.21), (12.5, 18.69), arrowprops=dict(arrowstyle="<->", color="#a00000", lw=1.6))
    ax.text(37.0, 13.0, "farthest N+Activ from the tie: 18.90 um\nLU_b = 20 um (json LU_b; its file 7_2_latchup.drc\n"
            "is not in this PDK copy)\n-> one tie segment, below only:\nno tie on top, left or right, no closed ring", **red)
    ax.text(37.0, 4.0, "no NWell at all. An n+ guard ring in its own NWell\nwould cost per side: NW.d1 0.62 + NW.e1 0.62\n"
            "+ Activ 0.30 + NW.e1 0.62 = 2.16 um,\nvs. Act.b 0.21 + Activ 0.30 = 0.51 um for a p+ tie;\n"
            "two wells on one rail: merge them (NW.b 0.62),\nwells on different nets: NW.b1 1.80 apart", **red)
    ax.set_xlim(bb.left - 0.5, bb.right + 19.5)
    ax.set_ylim(bb.bottom - 0.5, bb.top + 0.5)
    ax.set_aspect("equal")
    ax.set_title("latch-up distance with one tie segment (oa_n10, whole cell)", fontsize=11)
    for a in fig.axes:
        a.grid(True, lw=0.2, alpha=0.4)
        a.set_xlabel("x (um)")
    fig.tight_layout()
    fig.savefig(fn, dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    cell_render("oa_n10", os.path.join(OUT, "oa_n10.png"))
    cell_render("oa_mcs_c", os.path.join(OUT, "oa_mcs_c.png"), ppu=45)
    os.makedirs(os.path.join(HERE, "pictures"), exist_ok=True)
    tile(os.path.join(HERE, "pictures", "tile.png"), True)
    tile(os.path.join(HERE, "..", "generic", "pictures", "tile_roles.png"), False)
    before_after(os.path.join(HERE, "pictures", "before_after.png"))
    rule_savings(os.path.join(HERE, "pictures", "rule_savings.png"))
    print("pictures written")
