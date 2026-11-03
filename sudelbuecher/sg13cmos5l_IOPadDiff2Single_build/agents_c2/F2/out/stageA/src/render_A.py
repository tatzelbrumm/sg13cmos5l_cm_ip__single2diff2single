# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 stage A picture: the pad top with the placed cells (named, with sizes), the rails, gaps and the CMB-stage
reserve.   python3 render_A.py <placement_A.gds> <placement_A.tsv> <out.png> [x0 y0 x1 y1]"""
import csv
import sys

import klayout.db as db
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                      # noqa: E402
from matplotlib.collections import PolyCollection    # noqa: E402
from matplotlib.patches import Rectangle              # noqa: E402

gds, tsv, png = sys.argv[1:4]
win = [float(v) for v in sys.argv[4:8]] if len(sys.argv) > 7 else [-1.0, 81.0, 81.0, 181.0]
ly = db.Layout()
ly.read(gds)
top = ly.top_cell()
u = ly.dbu
clip = db.Region(db.DBox(*win).to_itype(u))
LAYERS = [((31, 0), "#2e8b57", 0.10), ((44, 0), "#b8b860", 0.06), ((14, 0), "#d2b48c", 0.12),
          ((1, 0), "#22aa22", 0.45), ((5, 0), "#c0392b", 0.45), ((8, 0), "#3a8fd9", 0.25), ((10, 0), "#8e7cc3", 0.25)]
fig, ax = plt.subplots(figsize=(13, 16))
for (l, d), col, a in LAYERS:
    li = ly.find_layer(l, d)
    if li is None:
        continue
    r = (db.Region(top.begin_shapes_rec(li)) & clip).merged().decompose_trapezoids_to_region()
    ps = [[(p.x * u, p.y * u) for p in q.each_point_hull()] for q in r.each()]
    ax.add_collection(PolyCollection(ps, facecolor=col, alpha=a, edgecolor="none"))
rows = list(csv.DictReader(open(tsv), delimiter="\t"))
for r in rows:
    x0, y0, x1, y1 = (float(r[k]) for k in ("x0", "y0", "x1", "y1"))
    if r["cell"] == "CMB_stage_reserve":
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, hatch="///", edgecolor="#d62728", lw=1.5,
                               ls="--"))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, "CMB-stage reserve\n(not drawn)\n%.1f x %.1f" % (x1 - x0, y1 - y0),
                ha="center", va="center", fontsize=9, color="#d62728", weight="bold",
                bbox=dict(fc="white", ec="none", alpha=0.85))
        continue
    col = {"P": "#1b7a3a", "N": "#b03030", "S": "#c05800"}[r["block"]]
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor=col, lw=1.6))
    small = (x1 - x0) < 6 or (y1 - y0) < 4
    lab = r["cell"] + ("" if r["orientation"] == "R0" else " (%s)" % r["orientation"])
    if r["block"] == "S":
        lab = ("CMA" if "cma" in r["cell"] else "CMB") + " 2k stage\nd2s_sp2k_f2" + ("" if r["orientation"] == "R0" else
                                                                                    " (M90)")
    txt = lab if small else "%s\n%.2f x %.2f" % (lab, x1 - x0, y1 - y0)
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, txt, ha="center", va="center", fontsize=6.5 if small else 9,
            color=col, weight="bold", rotation=90 if (x1 - x0) < 6 else 0,
            bbox=dict(fc="white", ec="none", alpha=0.8, pad=0.5))
# device labels of the moved switches
it = top.begin_shapes_rec(ly.find_layer(63, 0))
while not it.at_end():
    s = it.shape()
    if s.is_text() and s.text_string in ("TGN", "TDN", "TGP", "BP", "BPC"):
        q = it.trans() * db.Point(s.text.x, s.text.y)
        p = db.DPoint(q.x * u, q.y * u)
        if win[1] <= p.y <= win[3]:
            ax.plot(p.x, p.y, "o", ms=4, color="#e67e00")
            ax.annotate(s.text_string, (p.x, p.y), xytext=(3, 3), textcoords="offset points", fontsize=7,
                        color="#e67e00", weight="bold")
    it.next()
# ring rails (Metal3, phase 1 report 1.4) beside the cell, and the Metal3 gaps
R = [(66, 91.5, "iovdd"), (93.5, 119, "iovdd"), (126, 134, "iovss"), (140, 158, "vss"), (160, 178, "vdd")]
for y0, y1, n in R:
    if y1 < win[1]:
        continue
    yc = max(y0, win[1])
    ax.add_patch(Rectangle((81.0, yc), 2.2, y1 - yc, color="#7f7f7f", alpha=0.5))
    ax.text(84.0, (yc + y1) / 2, "M3 %s\n%g-%g" % (n, y0, y1), fontsize=7, va="center")
for y0, y1 in ((119, 126), (134, 140)):
    ax.add_patch(Rectangle((81.0, y0), 2.2, y1 - y0, fill=False, hatch="..", edgecolor="#2a7ab0"))
    ax.text(84.0, (y0 + y1) / 2, "M3 free\n%g-%g" % (y0, y1), fontsize=7, va="center", color="#2a7ab0")
ax.add_patch(Rectangle((0, 0), 80, 180, fill=False, edgecolor="black", lw=1.0))
# gaps: column A (vertical gaps between the stacked cells) and column B
P = {r["cell"]: tuple(float(r[k]) for k in ("x0", "y0", "x1", "y1")) for r in rows}


def vgap(a, b, x):
    y0, y1 = P[a][3], P[b][1]
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", color="#0050a0", lw=0.8))
    ax.text(x + 0.3, (y0 + y1) / 2, "%.2f" % (y1 - y0), fontsize=7, color="#0050a0", va="center")


def hgap(a, b, y):
    x0, x1 = P[a][2], P[b][0]
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", color="#0050a0", lw=0.8))
    ax.text((x0 + x1) / 2, y + 0.4, "%.2f" % (x1 - x0), fontsize=7, color="#0050a0", ha="center")


for a, b, x in (("d2s_loads_c2", "d2s_casc_p_c2", 20.0), ("sp2k_cma", "d2s_casc_p_c2", 6.0),
                ("sp2k_cmb", "sinks_6x6_f2", 74.0), ("d2s_casc_p_c2", "d2s_tails_c2", 20.0),
                ("d2s_tails_c2", "d2s_inputs_c2", 20.0), ("d2s_inputs_c2", "bias_tree_p_f2", 33.0),
                ("d2s_ab_n_f2", "d2s_casc_n_f2", 58.0), ("d2s_casc_n_f2", "d2s_rhigh_f2", 50.0),
                ("d2s_rhigh_f2", "bias_tree_n_f2", 53.0), ("sinks_6x6_f2", "bias_tree_n_f2", 69.0)):
    vgap(a, b, x)
for a, b, y in (("d2s_inputs_c2", "d2s_rhigh_f2", 150.0), ("sp2k_cma", "d2s_loads_c2", 92.0), ("d2s_casc_n_f2", "sinks_6x6_f2", 120.0),
                ("bias_tree_p_f2", "bias_tree_n_f2", 172.0), ("d2s_tails_c2", "d2s_casc_n_f2", 128.0)):
    hgap(a, b, y)
ax.axhline(88.0, color="#555555", lw=0.6, ls=":")
ax.text(1.0, 86.0, "a / b joins (Metal2, y 86.4-88.0); NWell isolator 84.55-85.33; P frame below", fontsize=7)
ax.set_xlim(win[0], 95)
ax.set_ylim(win[1], win[3])
ax.set_aspect("equal")
ax.set_xlabel("x (um)")
ax.set_ylabel("y (um)")
ax.set_title("F2 stage A: placement in the pad top, before routing (green: PMOS / NWell iovdd, red: NMOS / R, "
             "substrate, orange: 2 kOhm stages)\nlayers: NWell, ThickGateOx, pSD, Activ, GatPoly, Metal1, Metal2; blue: gaps in um; orange: "
             "diodes and moved switches", fontsize=9)
fig.tight_layout()
fig.savefig(png, dpi=130)
