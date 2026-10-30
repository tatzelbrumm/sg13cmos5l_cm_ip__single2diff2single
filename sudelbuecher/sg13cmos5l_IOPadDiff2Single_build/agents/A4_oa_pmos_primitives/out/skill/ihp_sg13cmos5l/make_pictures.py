# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""make_pictures.py: the skill's pictures, rendered from the IHP sg13cmos5l example GDS (examples/), 2026-10-28.

    python3 make_pictures.py            (run in this folder; writes ../generic/pictures/ and pictures/)

  ../generic/pictures/tile_stack.png   pattern tile: oa_pmir_c with the parent's tap segments, letters, tracks, pins
  ../generic/pictures/tile_chain.png   oa_ms1 and oa_svpg
  pictures/before_after.png            old library cells vs new, same scale, outline dimensions
  pictures/rule_savings.png            top-left corner old vs new, same scale, each saving with its rule and value
  ../generic/pictures/tile_cstack.png  pattern tile: bg_pmir_pcas_c (mirror + cascode stack), left half
  pictures/before_after_bg.png         bandgap PMOS cells old vs new, same scale
"""
import os
import sys
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "generic"))
import generator as G                      # noqa: E402
import render as Rn                        # noqa: E402
import matplotlib.pyplot as plt            # noqa: E402
from matplotlib.patches import Rectangle   # noqa: E402

P = G.load_adapter(os.path.join(HERE, "adapter.py"))
EX = os.path.join(HERE, "examples")
SHORT = {"PO": "o", "P8": "8", "P2": "2", "P0": "1", "dummy": "x", "dummyn": "d"}


def lay(name):
    ly = db.Layout()
    ly.read(os.path.join(EX, name))
    return ly


def finish(ax, x0, x1, y0, y1, title):
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")
    ax.grid(True, lw=0.2, alpha=0.4)


def note(ax, x, y, s, xt, yt, col="#222222", fs=8):
    ax.annotate(s, (x, y), (xt, yt), fontsize=fs, color=col, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=col, lw=0.8),
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=col, lw=0.5, alpha=0.9))


def tile_stack():
    ly = lay("lu_context.gds")
    c = ly.cell("ctx_tb")
    fig, ax = plt.subplots(figsize=(11.5, 14))
    Rn.draw(ax, ly, c, P, fs=11, short=SHORT, skip=("pmosHV",))
    pm = ly.cell("oa_pmir_c").dbbox()
    Rn.dims(ax, pm, "  (cell oa_pmir_c, tap-less)")
    for t in ("ctx_tb_tap0", "ctx_tb_tap1"):
        b = db.Region(ly.cell(t).begin_shapes_rec(ly.find_layer(*P.layer("diff")))).bbox().to_dtype(ly.dbu)
        ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fill=False, ec="#d35400", lw=1.5))
    note(ax, 9.4, 38.6, "parent's tap segment (assumed): one contact column,\nin the top margin under the vdd plate",
         21.0, 41.0, "#d35400")
    note(ax, 9.4, -0.36, "parent's tap segment (assumed), bottom", 21.0, -2.0, "#d35400")
    note(ax, 19.4, 28.95, "band A (Metal2), bottom to top:\nco  c8  c2  vpg", 21.0, 30.5)
    note(ax, 19.4, 9.5, "band B = point image:\nvpg  c2  c8  co  (pins on the right edge)", 21.0, 7.0)
    note(ax, -0.5, 19.1, "staircase (Metal2): c2, c8, co lines join\nband A and band B; outermost net outermost",
         -14.0, 19.1)
    note(ax, -0.3, 33.0, "gate column (Metal1, vpg) along every row end,\nVia1 onto the vpg track of each band",
         -14.0, 33.0)
    note(ax, 0.15, 28.95, "rest 'd' (one contact wide): D = S strapped,\ncontinues through the band = vdd spine",
         -14.0, 26.0)
    note(ax, 9.4, 19.12, "shared source plate, rows 2 and 3", -14.0, 14.0)
    note(ax, 5.0, -0.5, "vdd plate to the cell edge (pin)", -14.0, 2.0)
    note(ax, 10.55, 14.7, "x = P0's point partner", 21.0, 15.5)
    Rn.scalebar(ax, -12.0, -3.2, 5.0)
    ax.text(-14.0, 44.0, "score (o = PO, 8 = P8, 2 = P2, 1 = P0, x = P0's partner, d = rest):\n"
            "| d o o o 8 o o 8 o d |\n| d o 8 o 1 2 8 o o d |\n"
            "| d o o 8 2 x o 8 o d |\n| d o 8 o o 8 o o o d |   = R180 image of itself with 1 <-> x", fontsize=9, family="monospace",
            va="top")
    finish(ax, -14.5, 33.5, -4.0, 45.0, "pattern tile: mirror stack (instance: IHP sg13cmos5l, see ../ihp_sg13cmos5l/)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "..", "generic", "pictures", "tile_stack.png"), dpi=100)
    plt.close(fig)


def tile_chain():
    ly = lay("oa_p_cells.gds")
    fig, ax = plt.subplots(figsize=(10, 7.5))
    b1 = Rn.draw(ax, ly, ly.cell("oa_ms1"), P, fs=9, short={"MS1_%d" % k: str(k) for k in range(8)}, skip=("pmosHV",))
    Rn.dims(ax, b1, "")
    b2 = Rn.draw(ax, ly, ly.cell("oa_svpg"), P, dx=9.5, dy=0.0, fs=8, skip=("pmosHV",))
    Rn.dims(ax, b2, "")
    note(ax, 0.6, 0.15, "links alternate bottom / top (hocket):\n_ ^ _ ^ _ ^ _", 1.0, -2.5)
    note(ax, -0.2, 9.0, "one merged gate strip, contact column\nat the left end", -9.0, 9.0)
    note(ax, 2.9, 7.0, "8 x repetition (one AREF), fingers 0 ... 7", 13.0, 9.5)
    note(ax, 10.5, 0.6, "single: gate contact beside the channel", 13.0, 4.0)
    ax.text(-9.0, 15.8, "chain | S S S S S S S S |   links _ ^ _ ^ _ ^ _\nsingle | W |", fontsize=9,
            family="monospace", va="top")
    Rn.scalebar(ax, -8.0, -3.6, 2.0)
    finish(ax, -9.5, 22.0, -4.5, 16.5, "pattern tile: chain (oa_ms1) and single (oa_svpg); instance: IHP sg13cmos5l")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "..", "generic", "pictures", "tile_chain.png"), dpi=100)
    plt.close(fig)


def before_after():
    old, new = lay("before_cells.gds"), lay("oa_p_cells.gds")
    fig, ax = plt.subplots(figsize=(15, 9.5))
    xs = 0.0
    items = [(old, "oa_pmir", "before: oa_pmir (library)"), (new, "oa_pmir_c", "after: oa_pmir_c"),
             (old, "oa_misc_p", "before: oa_misc_p"), (new, "oa_ms1", "after: oa_ms1"), (new, "oa_svpg", "+ oa_svpg")]
    for ly, n, lab in items:
        c = ly.cell(n)
        b = c.dbbox()
        dx, dy = xs - b.left, -b.bottom
        bb = Rn.draw(ax, ly, c, P, dx=dx, dy=dy, letters=False, pins=False)
        Rn.dims(ax, bb, "", fs=8)
        ax.text((bb.left + bb.right) / 2, bb.top + 2.2, lab, ha="center", fontsize=9)
        xs = bb.right + 4.0
    ax.text(0, -3.0, "same scale; dashed = cell outline. oa_pmir: 1198.6 -> 793.4 um2 (-34 %).  oa_misc_p: 206.4 -> "
            "100.8 + 5.3 um2 (-49 %; library before rotation 58.2 x 5.5 = 320 um2). The new cells carry no tap: "
            "the parent's merged vdd well gets it.", fontsize=9)
    Rn.scalebar(ax, 0, -5.0, 10.0)
    finish(ax, -2, xs, -7, 48, "before / after (IHP sg13cmos5l)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pictures", "before_after.png"), dpi=100)
    plt.close(fig)


def rule_savings():
    old, new = lay("before_cells.gds"), lay("oa_p_cells.gds")
    fig, axs = plt.subplots(1, 2, figsize=(15, 11.5))
    r = P.rule
    win = (-4.3, 9.0, 25.6, 41.3)
    # before: top-left corner of oa_pmir (row 1 Activ top 38.81, left end dummy Activ at x = 0)
    ax = axs[0]
    Rn.draw(ax, old, old.cell("oa_pmir"), P, letters=True, pins=True, fs=8, skip=("pmosHV",))
    for n, (x, y) in enumerate([(1.0, 34.0), (-1.4, 35.0), (-2.9, 27.0), (4.0, 40.2), (5.0, 29.15), (-0.8, 36.5)], 1):
        Rn.mark(ax, x, y, n)
    finish(ax, *win, "before: oa_pmir (library), top-left corner")
    ax.text(0.0, -0.08, "1  end dummy 2/8: W 2.00\n"
            "2  ntap ring: two contact columns, Activ 0.78, NWell 0.24 beyond, TGO 0.38 inside\n"
            "3  Metal1 jumpers band A <-> band B outside the ring: 1.8 um, pins to x = -3.755\n"
            "4  top: plate + ring = 1.98 above the Activ\n"
            "5  band A 1.94: Metal2 tracks 0.29 at 0.50 pitch\n"
            "6  gate column 0.70 from the dummy (dummy lane + gate column)",
            transform=ax.transAxes, fontsize=9, va="top", family="monospace")
    # after
    ax = axs[1]
    Rn.draw(ax, new, new.cell("oa_pmir_c"), P, letters=True, pins=True, fs=9, short=SHORT, skip=("pmosHV",))
    wd = G.min_contact_width(P)
    gb = 2 * (r("m1_space") - r("diff_encl_contact") + r("via1_size") / 2 + r("m1_encl_via1")) + \
        3 * (r("m2_width") + r("m2_space"))
    for n, (x, y) in enumerate([(0.15, 33.0), (-0.62, 35.0), (-0.1, 26.6), (4.0, 38.6), (5.0, 28.75), (-0.28, 36.5)], 1):
        Rn.mark(ax, x, y, n)
    finish(ax, *win, "after: oa_pmir_c, same scale")
    ax.text(0.0, -0.08,
            "1  rest W = 2 Cnt_c + Cnt_a = %.2f (one S/D contact): -1.70 per row end\n"
            "2  no ring: cell edge at NW_c1 = %.2f beyond Activ; the parent taps the merged\n"
            "   well (LU_a = %.0f um; numbers in the report)\n"
            "3  staircase in Metal2 over the row end: no area (pitch Mn_a + Mn_b = %.2f)\n"
            "4  top: NW_c1 = %.2f (was 1.98)\n"
            "5  band %.2f = 2 (M1_b - Cnt_c + V1_a/2 + V1_c) + 3 (Mn_a + Mn_b); tracks Mn_a = %.2f\n"
            "6  gate column M1_b = %.2f from the S/D Metal1, contact Cnt_e >= %.2f from Activ"
            % (wd, r("well_encl_pdiff"), r("lu_tap_dist"), r("m2_width") + r("m2_space"), r("well_encl_pdiff"), gb,
               r("m2_width"), r("m1_space"), r("poly_contact_to_diff")),
            transform=ax.transAxes, fontsize=9, va="top", family="monospace")
    fig.text(0.01, 0.01, "width 28.03 -> 20.09 um: rests -3.40, left side 3.755 -> 0.62, right side 2.02 -> 0.62.   "
             "height 42.77 -> 39.49 um: top / bottom 1.98 -> 0.62 each, bands 1.94 -> 1.66 each.   "
             "Keys: sg13cmos5l_tech_default.json.", fontsize=9)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(HERE, "pictures", "rule_savings.png"), dpi=100)
    plt.close(fig)


SHORT_BG = {"PO": "o", "PB": "b", "PA": "a", "POC": "O", "PBC": "B", "PAC": "A", "dummyn": "d"}


def tile_cstack():
    ly = lay("bg_p_cells.gds")
    c = ly.cell("bg_pmir_pcas_c")
    fig, ax = plt.subplots(figsize=(13, 11))
    Rn.draw(ax, ly, c, P, fs=11, short=SHORT_BG, skip=("pmosHV",))
    rows = ["Ma  mirror, drain down", "Ca  cascodes of Ma", "Cb  cascodes of Mb", "Mb  mirror, drain up",
            "Ma", "Ca", "Cb", "Mb"]
    for i, t in enumerate(rows):
        ax.text(-12.2, 14.07 - i * 1.89, t, fontsize=9, va="center")
    for n, (x, y) in enumerate([(7.0, 13.9), (8.5, 13.12), (3.0, 14.31), (-0.28, 9.4), (-1.15, 4.0), (0.15, 6.5),
                                (20.0, 7.45)], 1):
        Rn.mark(ax, x, y, n)
    Rn.scalebar(ax, 12.0, -1.6, 5.0)
    finish(ax, -12.5, 22.0, -2.6, 16.2, "pattern tile: cascode stack, left half (instance IHP sg13cmos5l, "
           "cell 45.17 x 16.15 um)")
    ax.text(0.0, -0.10,
            "score (o b a = PO PB PA, O B A = their cascodes): | d o b a o d | d a o o b d | d b o o a d | d o a b o d |\n"
            "= its own R180 image; every row and every column holds b, a, o, o (Latin square)\n"
            "1  the same 3-Via1 tab on every finger: only the via picks the lane\n"
            "2  mirror drain = cascode source: one Metal1 joint across the 0.21 Activ gap (no band)\n"
            "3  three Metal2 lanes over each row's own channel: co vpg ca (mirror), iout vpc g (cascode)\n"
            "4  gate pad at both ends of every row, Via1 onto the middle lane (vpg / vpc)\n"
            "5  Metal1 side lines vpg co ca (right side: vpc g iout), full height; pins at their ends\n"
            "6  rests d, one contact wide: their straps form the vdd spine through all rows\n"
            "7  shared vdd plate between Mb and the next Ma",
            transform=ax.transAxes, fontsize=9, va="top", family="monospace")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "..", "generic", "pictures", "tile_cstack.png"), dpi=100)
    plt.close(fig)


def before_after_bg():
    old, new = lay("before_bg_cells.gds"), lay("bg_p_cells.gds")
    fig, ax = plt.subplots(figsize=(17, 7.5))
    xs = 0.0
    items = [(old, "bg_pmir_pcas", "before: bg_pmir_pcas (library)"), (new, "bg_pmir_pcas_c", "after: bg_pmir_pcas_c"),
             (old, "bg_misc_p", "before: bg_misc_p"), (new, "bg_ms1", "after: bg_ms1"), (new, "bg_svpg", "+ bg_svpg")]
    for ly, n, lab in items:
        c = ly.cell(n)
        b = c.dbbox()
        bb = Rn.draw(ax, ly, c, P, dx=xs - b.left, dy=-b.bottom, letters=False, pins=False)
        Rn.dims(ax, bb, "", fs=8)
        ax.text((bb.left + bb.right) / 2, bb.top + 2.0, lab, ha="center", fontsize=9)
        xs = bb.right + 4.0
    ax.text(0, -3.0, "same scale; dashed = cell outline. bg_pmir_pcas: 38.59 x 27.60 = 1065.0 -> 45.17 x 16.15 = 729.5 um2"
            " (-31.5 %).  bg_misc_p: 206.4 -> 100.8 + 5.3 um2 (-49 %). New cells: tap-less, NWell to every edge.",
            fontsize=9)
    Rn.scalebar(ax, 0, -5.0, 10.0)
    finish(ax, -2, xs, -6.5, 33, "before / after: bandgap PMOS cells (IHP sg13cmos5l)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "pictures", "before_after_bg.png"), dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    tile_stack()
    tile_chain()
    before_after()
    rule_savings()
    tile_cstack()
    before_after_bg()
    print("pictures written")
