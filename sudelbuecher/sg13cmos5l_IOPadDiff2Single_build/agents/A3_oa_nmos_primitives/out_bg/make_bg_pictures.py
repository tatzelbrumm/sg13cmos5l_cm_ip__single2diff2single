# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Pictures of bg_n4 rendered from the GDS, 2026-10-28, Claude (Opus 5.5).

    python3 make_bg_pictures.py <bg_n_cells.gds> <bg_n_cells.cdl> <pad_buffer_cells.gds> <out_dir>

Writes bg_n4.png (cell, finger names, track nets, pins, scale bar) and bg_n4_before_after.png (library bg_nab +
bg_misc_n against bg_n4, one scale). Net names from ../out/skill/ihp_sg13cmos5l/tools/oa_core_pd_lvs.py (IHP-only).
"""
import os
import re
import sys
import importlib.util
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..", "out", "skill")
sys.path.insert(0, os.path.join(SK, "generic"))
sys.path.insert(0, os.path.join(SK, "ihp_sg13cmos5l"))
import adapter                                       # noqa: E402
import render as rd                                  # noqa: E402

GDS, CDL, LIB, OUT = sys.argv[1:5]
P = adapter.Process()
spec = importlib.util.spec_from_file_location("lvs", os.path.join(SK, "ihp_sg13cmos5l", "tools", "oa_core_pd_lvs.py"))
lvsm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lvsm)
ly = db.Layout()
ly.read(GDS)
NAMES = {"NA": "NA", "NB": "NB", "MS2": "MS2", "MS3": "MS3", "SKS": "SKS", "dummy": "d"}


def namer(cell):
    lvs, fly, _ = lvsm.extract(GDS, cell, "top")
    c = lvs.netlist().circuit_by_name(cell)
    blk = re.search(r"^\.SUBCKT\s+%s\b.*?^\.ENDS\b[^\n]*" % cell, open(CDL).read(), re.S | re.M | re.I).group(0)
    tmp = os.path.join(OUT, ".ref_%s.cdl" % cell)
    open(tmp, "w").write(blk + "\n")
    ref = db.Netlist()
    ref.read(tmp, db.NetlistSpiceReader())
    os.remove(tmp)
    ref.combine_devices()
    lvs.netlist().case_sensitive = False
    for p in ref.circuit_by_name(cell).each_pin():
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


def cell_render(fn, ppu=48):
    c = ly.cell("bg_n4")
    bb = c.dbbox()
    fig, ax = plt.subplots(figsize=((bb.width() + 4) * ppu / 100, (bb.height() + 4) * ppu / 100))
    rd.draw_cell(ax, ly, c, P)
    rd.finger_letters(ax, ly, c, P, NAMES, size=9)
    rd.track_names(ax, ly, c, P, namer("bg_n4"), window=bb, size=7, min_len=1.0)
    rd.pins(ax, ly, c, P, size=8)
    rd.outline(ax, bb, "bg_n4")
    rd.scale_bar(ax, bb.left, bb.bottom - 1.3, 5.0)
    for y, s in ((0.15, "R0  A (S bottom)"), (5.04, "R1  B"), (9.93, "R2  B  flip (S top)"), (14.82, "R3  A  flip"),
                 (19.71, "Y   MS2 flip + coda")):
        ax.text(bb.right + 0.3, y + 1.0, s, fontsize=8, color="#7a0000", va="center")
    ax.set_xlim(bb.left - 1.5, bb.right + 6.5)
    ax.set_ylim(bb.bottom - 1.8, bb.top + 1.6)
    ax.set_aspect("equal")
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")
    ax.grid(True, lw=0.2, alpha=0.4)
    fig.tight_layout()
    fig.savefig(fn, dpi=100)
    plt.close(fig)


def before_after(fn):
    lib = db.Layout()
    lib.read(LIB)
    nab, misc = lib.cell("bg_nab"), lib.cell("bg_misc_n")
    new = ly.cell("bg_n4")
    fig, axs = plt.subplots(1, 2, figsize=(21, 7.5), gridspec_kw=dict(width_ratios=[2.1, 1]))
    ax = axs[0]
    b1 = nab.dbbox()
    t1 = db.DCplxTrans(1, 0, False, -b1.left, 14.0 - b1.bottom)
    b2 = misc.dbbox()
    t2 = db.DCplxTrans(1, 0, False, -b2.left, -b2.bottom)
    tot = 0
    for c, t, nm in ((nab, t1, "bg_nab (NA, NB)"), (misc, t2, "bg_misc_n (MS2, MS3, SKS)")):
        rd.draw_cell(ax, lib, c, P, trans=db.ICplxTrans(t, lib.dbu))
        b = c.dbbox().transformed(t)
        rd.outline(ax, b, nm)
        tot += b.width() * b.height()
    ax.set_title("before (library): bounding boxes %.0f um2" % tot, fontsize=11)
    ax.set_xlim(-1, 52)
    ax.set_ylim(-1.5, 26)
    ax2 = axs[1]
    bn = new.dbbox()
    tn = db.DCplxTrans(1, 0, False, -bn.left, -bn.bottom)
    rd.draw_cell(ax2, ly, new, P, trans=db.ICplxTrans(tn, ly.dbu))
    rd.outline(ax2, bn.transformed(tn), "bg_n4")
    ax2.set_title("after: bg_n4, %.0f um2\n(ties and MS2 / MS3 / SKS included)" % (bn.width() * bn.height()),
                  fontsize=11)
    ax2.set_xlim(-1, 23)
    ax2.set_ylim(-1.5, 26)
    for a in axs:
        a.set_aspect("equal")
        a.grid(True, lw=0.2, alpha=0.4)
        rd.scale_bar(a, 0.5, -1.0, 5.0)
    fig.tight_layout()
    fig.savefig(fn, dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    cell_render(os.path.join(OUT, "bg_n4.png"))
    before_after(os.path.join(OUT, "bg_n4_before_after.png"))
    print("pictures written")
