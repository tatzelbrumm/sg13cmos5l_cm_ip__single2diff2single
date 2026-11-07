# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""All input cells of F at one scale: the rows of P, P3 and N as delivered (read only)."""
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
B = "/tmp/claude-0/-home-user-sg13cmos5l-cm-ip--single2diff2single/f7165478-7787-531e-a1d8-6ec7206ebfcb/scratchpad/layout_rb/"
SRC = [("P/out/rb_p_cells.gds", ["rb_tree_p", "rb_tails", "rb_tubs"]), ("P3/out/rb_avg_v3.gds", ["rb_avg"]),
       ("N/out/rb_n_cells.gds", ["rb_tree_n", "rb_casc", "rb_mirror", "rb_cload", "bypass_rb"])]
NOTE = {"rb_tree_p": "TGP PBNC BP + MDPBN (vbp)", "rb_tails": "D TR BT D (vbp)", "rb_tubs": "D MR BA BB D (own wells)",
        "rb_avg": "D SU D / D SL1 SL2 D (wells gh, m)", "rb_tree_n": "TGN SH2 SF NBP SY NI SH1 D D TDN (ni)",
        "rb_casc": "8 slots: F1-F4, CY, BNC, 7 dummies (vbnc)", "rb_mirror": "D BD BM D (bd)",
        "rb_cload": "CB (vcm), CBR #9 (vref), SPDC, SPDR", "bypass_rb": "4 CBM (vcm) + 8 CBR (vref), 3 x 4"}
STY = [((31, 0), "#c8e6c9", 0.5), ((1, 0), "#2f8f2f", 0.75), ((5, 0), "#e8443a", 0.55), ((8, 0), "#4a90e2", 0.30),
       ((10, 0), "#b05ad6", 0.30)]
cells = []
for f, names in SRC:
    ly = db.Layout(); ly.read(B + f)
    for n in names:
        c = ly.cell(n); bb = c.bbox()
        polys = {}
        for ld, col, a in STY:
            li = ly.find_layer(*ld)
            if li is None: continue
            r = db.Region(c.begin_shapes_rec(li)).merged()
            polys[ld] = [[(p.x * ly.dbu, p.y * ly.dbu) for p in poly.each_point_hull()] for poly in r.each()]
        cells.append((n, (bb.left * ly.dbu, bb.bottom * ly.dbu, bb.right * ly.dbu, bb.top * ly.dbu), polys))
rows = [["rb_tree_p", "rb_tails", "rb_tubs", "rb_avg"], ["rb_tree_n", "rb_casc", "rb_mirror", "rb_cload"], ["bypass_rb"]]
byname = {c[0]: c for c in cells}
fig, ax = plt.subplots(figsize=(18, 9.5))
y = 0.0; tot = 0.0
for row in rows:
    h = max(byname[n][1][3] - byname[n][1][1] for n in row); x = 0.0
    for n in row:
        _, (x0, y0, x1, y1), polys = byname[n]
        dx, dy = x - x0, y - y1
        for ld, col, a in STY:
            for pts in polys.get(ld, []):
                ax.add_patch(Polygon([(px + dx, py + dy) for px, py in pts], closed=True, fc=col, ec="none", alpha=a))
        ax.add_patch(Rectangle((x, y - (y1 - y0)), x1 - x0, y1 - y0, fc="none", ec="black", lw=0.8, ls="--"))
        area = (x1 - x0) * (y1 - y0); tot += area
        ax.text(x, y + 0.8, f"{n}  {x1-x0:.1f} x {y1-y0:.1f} um ({area:.0f} um2)\n{NOTE[n]}", fontsize=8.5,
                va="bottom")
        x += (x1 - x0) + 8
    y -= h + 9
ax.set_aspect("equal"); ax.autoscale_view(); ax.set_xlabel("um")
ax.set_title(f"Inputs of F: the 9 cells of pad_ref_rb as delivered (P, P3, N), one scale; sum of cell areas {tot:.0f} um2. "
             "NWell light green, Activ green, GatPoly red, M1 blue, M2 violet", fontsize=11)
fig.tight_layout(); fig.savefig("inputs_overview.png", dpi=120)
print("sum", round(tot), [ (c[0], round((c[1][2]-c[1][0])*(c[1][3]-c[1][1]))) for c in cells])
