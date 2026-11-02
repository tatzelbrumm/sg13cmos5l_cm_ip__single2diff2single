"""Stage-1 floorplan of the amplifier block of sg13cmos5l_IOPadDiff2Single (y 84-178), two variants.
Rectangles are planned outlines (um, absolute pad-cell coordinates). Prints overlaps and areas, draws a PNG.
Usage: python3 floorplan_stage1.py <out.png>"""
import sys, itertools
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# kind -> colour: P = PMOS on iovdd well, T = input tubs (own wells), N = NMOS, R = rhigh, B = bias tree (mine),
# F = fixed (existing pad top), G = guard / stubs (mine), S = spare / reserve
COL = dict(P="#f4a6a6", T="#e8c070", N="#9fc5e8", R="#b6d7a8", B="#c9a0dc", F="#cccccc", G="#ffe599", S="#ffffff")

COMMON = [  # existing pad top and my rings / stubs
    ("P frame (Clamp_P_M1, as drawn)", 0, 65, 80, 84.44, "F"),
    ("NWell isolator (iovdd)", 2.6, 84.50, 77.4, 85.28, "G"),
    ("a join M2", 3.2, 86.4, 77.5, 87.0, "F"),
    ("b join M2", 0.5, 87.4, 79.5, 88.0, "F"),
    ("p+ stub iovss L", 0, 84.51, 0.9, 139.92, "G"),
    ("p+ stub iovss R", 79.1, 84.51, 80, 139.92, "G"),
    ("n+/NW iovdd L", 0, 147.73, 1.6, 149.27, "G"), ("n+/NW iovdd R", 78.4, 147.73, 80, 149.27, "G"),
    ("p+ vss L", 0.25, 156.85, 1.6, 157.15, "G"), ("p+ vss R", 78.4, 156.85, 79.75, 157.15, "G"),
    ("n+/NW vdd L", 0, 166.23, 1.6, 167.77, "G"), ("n+/NW vdd R", 78.4, 166.23, 80, 167.77, "G"),
]

V1 = [  # recommended: three columns, P left, N right, input stage centre
    ("casc_p\n(PCL PCR BPC)", 2.5, 88.6, 15.0, 122.6, "P"),
    ("loads\n(PL PR)", 2.5, 123.2, 17.7, 156.2, "P"),
    ("d2s_rhigh", 15.8, 90.0, 30.6, 104.5, "R"),
    ("ab_n", 31.6, 88.6, 39.1, 98.1, "N"),
    ("ab_p", 39.6, 88.6, 47.4, 98.1, "P"),
    ("pd_p", 47.9, 88.6, 51.9, 91.6, "P"),
    ("pd_n", 52.6, 88.6, 56.1, 91.1, "N"),
    ("bias_tree_pd\n(L-shape)", 47.9, 92.2, 66.0, 107.6, "B"),
    ("tree", 54.1, 107.6, 66.0, 123.0, "B"),
    ("tails (BP)", 19.5, 108.2, 53.5, 123.2, "P"),
    ("d2s_inputs\n(8 tubs + dummies)", 19.5, 125.0, 53.5, 152.0, "T"),
    ("casc_n\n(CX CY BNC)", 66.5, 88.6, 77.5, 122.6, "N"),
    ("sinks_6x6\n(SX SY BN)\nupright", 59.5, 123.5, 77.5, 177.0, "N"),
    ("spare / CMB reserve", 2.5, 157.0, 59.0, 177.5, "S"),
]

V2 = [  # alternative: sinks native across the top, tree in the right column
    ("casc_p", 2.5, 88.6, 15.0, 122.6, "P"),
    ("loads", 2.5, 123.2, 17.7, 156.2, "P"),
    ("d2s_rhigh", 15.8, 90.0, 30.6, 104.5, "R"),
    ("ab_n", 31.6, 88.6, 39.1, 98.1, "N"),
    ("ab_p", 39.6, 88.6, 47.4, 98.1, "P"),
    ("pd_p", 47.9, 88.6, 51.9, 91.6, "P"),
    ("pd_n", 52.6, 88.6, 56.1, 91.1, "N"),
    ("spare / CMB reserve", 47.9, 92.2, 66.0, 107.6, "S"),
    ("tails (BP)", 19.5, 108.2, 53.5, 123.2, "P"),
    ("d2s_inputs", 19.5, 125.0, 53.5, 152.0, "T"),
    ("casc_n", 66.5, 88.6, 77.5, 122.6, "N"),
    ("bias_tree_pd", 59.5, 123.5, 77.5, 150.0, "B"),
    ("sinks_6x6 (native rows)", 2.5, 159.0, 56.0, 177.0, "N"),
    ("spare", 59.5, 151.0, 77.5, 177.5, "S"),
]

PINS = {  # core-side pins, M2, x centre, y 179-180
 "V1": [("vinp", 25.0), ("vref", 31.0), ("vinn", 37.0), ("iref", 54.5), ("en_3v3", 56.5), ("en_3v3_b", 58.5)],
 "V2": [("vinp", 25.0), ("vref", 31.0), ("vinn", 37.0), ("iref", 62.0), ("en_3v3", 64.0), ("en_3v3_b", 66.0)],
}

def check(name, rects):
    blocks = [r for r in rects if r[5] not in "FG"]
    bad = []
    for a, b in itertools.combinations(blocks, 2):
        if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
            if not (a[0] == "tree" or b[0] == "tree"):  # the two parts of the L-shaped tree may touch
                bad.append((a[0], b[0]))
    area = {}
    for r in blocks:
        area[r[5]] = area.get(r[5], 0) + (r[3]-r[1])*(r[4]-r[2])
    used = sum(v for k, v in area.items() if k != "S")
    print(f"{name}: overlaps {bad or 'none'}; planned outlines {used:.0f} um2 "
          f"(P {area.get('P',0):.0f}, T {area.get('T',0):.0f}, N {area.get('N',0):.0f}, R {area.get('R',0):.0f}, "
          f"B {area.get('B',0):.0f}); spare {area.get('S',0):.0f} um2 of {75*88.9:.0f} (x 2.5-77.5, y 88.6-177.5)")

def draw(ax, title, rects, pins, notes):
    ax.set_title(title, fontsize=10)
    # ring rails (M3), as bands at the right margin
    for (y1, y2, n, c) in [(66, 91.5, "iovdd", "#f4cccc"), (93.5, 119, "iovdd", "#f4cccc"), (126, 134, "iovss", "#cfe2f3"),
                           (140, 158, "vss", "#d9ead3"), (160, 178, "vdd", "#fce5cd")]:
        ax.add_patch(Rectangle((81, y1), 4, y2-y1, fc=c, ec="k", lw=0.3))
        ax.text(83, (y1+y2)/2, n, rotation=90, ha="center", va="center", fontsize=6)
    for (y1, y2) in [(119, 126), (134, 140)]:
        ax.add_patch(Rectangle((0, y1), 80, y2-y1, fc="none", ec="#6aa84f", lw=0.6, ls=":"))
        ax.text(81.2, (y1+y2)/2, "M3 gap", fontsize=5, va="center", color="#38761d")
    for r in COMMON + rects:
        n, x1, y1, x2, y2, k = r
        ax.add_patch(Rectangle((x1, y1), x2-x1, y2-y1, fc=COL[k], ec="k", lw=0.5, ls="--" if k == "S" else "-"))
        if k not in "G" and (x2-x1) > 3 and (y2-y1) > 2 and n != "tree":
            ax.text((x1+x2)/2, (y1+y2)/2, n, ha="center", va="center", fontsize=5.5 if (x2-x1) > 9 else 4.5)
    ax.add_patch(Rectangle((0, 0), 80, 180, fc="none", ec="k", lw=1.0))
    for (p, x) in pins:
        ax.add_patch(Rectangle((x-0.2, 178.0), 0.4, 2.0, fc="#1155cc", ec="none"))
        ax.text(x, 181, p, rotation=90, ha="center", va="bottom", fontsize=5)
    # dabp / dabn pins (existing)
    ax.add_patch(Rectangle((38.15, 85), 0.3, 1, fc="#990000")); ax.add_patch(Rectangle((38.94, 85), 0.61, 1, fc="#990000"))
    for (xs, ys, c, lab) in notes:
        ax.plot(xs, ys, color=c, lw=1.0)
        ax.text(xs[-1], ys[-1], lab, fontsize=5, color=c)
    ax.set_xlim(-2, 88); ax.set_ylim(80, 190); ax.set_aspect("equal")
    ax.set_xlabel("x (um)", fontsize=7); ax.tick_params(labelsize=6)

NOTES_V1 = [
    ([2.15, 2.15, 18.6, 18.6], [88.3, 120.2, 120.2, 126.5], "#cc0000", "vfb (Kelvin, M2/M3)"),
    ([8.0, 8.0], [88.6, 86.7], "#000000", "a"),
    ([72.0, 72.0], [88.6, 87.7], "#000000", "b"),
    ([53.5, 59.5], [138.0, 138.0], "#0b5394", "x,y"),
    ([15.0, 31.1, 31.1, 47.4], [89.3, 89.3, 99.3, 99.3], "#674ea7", "l2, vbpc"),
]
NOTES_V2 = [
    ([2.15, 2.15, 18.6, 18.6], [88.3, 120.2, 120.2, 126.5], "#cc0000", "vfb"),
    ([36.0, 36.0], [152.0, 159.0], "#0b5394", "x,y up"),
    ([56.5, 56.5, 66.5], [159.0, 121.0, 121.0], "#0b5394", "x,y to casc_n"),
]

if __name__ == "__main__":
    check("V1", V1); check("V2", V2)
    fig, axs = plt.subplots(1, 2, figsize=(13, 9.2))
    draw(axs[0], "Variant 1 (recommended): columns, P left / N right, inputs centre", V1, PINS["V1"], NOTES_V1)
    draw(axs[1], "Variant 2: sinks native across the top, tree right", V2, PINS["V2"], NOTES_V2)
    leg = [Rectangle((0, 0), 1, 1, fc=COL[k], ec="k") for k in "PTNRBFGS"]
    fig.legend(leg, ["PMOS, one iovdd NWell (P)", "input tubs, own wells (P)", "NMOS (N)", "rhigh (F)",
                     "bias_tree_pd (F)", "existing pad top", "rings / edge stubs (F)", "spare"],
               loc="lower center", ncol=8, fontsize=7)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(sys.argv[1], dpi=160)
