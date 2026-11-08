# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Annotated views of bias_dist_pd (agent D's layout in the macro): the switch row, its tie strips, and the TG's split
gates with what sym_check.py's narrow-poly check measures. Device layers + M1 only."""
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch
GDS = "/home/user/sg13cmos5l_cm_ip__single2diff2single/macros/bias_dist_pd/layout/klayout/bias_dist_pd.klay.gds"
ly = db.Layout(); ly.read(GDS); u = ly.dbu
STY = [((31, 0), "#dcedc8", 0.6), ((14, 0), "#f5deb3", 0.5), ((1, 0), "#43a047", 0.55), ((5, 0), "#e53935", 0.55),
       ((6, 0), "#111111", 0.9), ((8, 0), "#1e88e5", 0.25)]
def reg(cell, ld): return db.Region(cell.begin_shapes_rec(ly.layer(*ld))).merged()
def draw(ax, cell, win=None):
    for ld, col, a in STY:
        r = reg(cell, ld)
        if win: r = r & db.Region(db.Box(*[int(v / u) for v in win]))
        for p in r.each():
            ax.add_patch(Polygon([(q.x * u, q.y * u) for q in p.each_point_hull()], fc=col, ec="none", alpha=a))
top = ly.cell("bias_dist_pd")
# --- figure 1: whole cell, the switch row framed and its slices named
fig, ax = plt.subplots(figsize=(18, 6.2))
draw(ax, top)
ax.add_patch(Rectangle((-0.6, -0.65), 61.0, 6.1, fc="none", ec="#6a1b9a", lw=2.5, ls="--"))
ax.text(-0.6, -1.25, "the switch row: one standard-cell row of 8 slices (nand2_hv | inv_hv | tg_hv) + TDN + SVPD + fillers",
        color="#6a1b9a", fontsize=11, weight="bold")
names = {0.55: "slice in0", 4.93: "slice in1", 9.31: "slice in2", 13.69: "slice in3", 18.07: "TDN", 26.03: "slice out0",
         31.28: "slice out1", 38.45: "SVPD", 41.77: "slice out2", 47.02: "slice out3"}
for inst in top.each_inst():
    b = inst.bbox(); x0 = round(b.left * u, 2)
    if inst.cell.name in ("bdp_slice", "bdp_tdn", "bdp_svpd"):
        ax.add_patch(Rectangle((b.left * u, b.bottom * u), b.width() * u, b.height() * u, fc="none", ec="#6a1b9a", lw=0.8))
        ax.text(b.left * u + b.width() * u / 2, 5.5, names.get(x0, inst.cell.name), ha="center", fontsize=8, color="#6a1b9a")
    if inst.cell.name.startswith("bdp_mirror"):
        ax.text(b.left * u + 0.5, b.top * u + 0.3, inst.cell.name + (" (NMOS: D NI NM D, closed ring)" if "_n" in inst.cell.name
                else " (PMOS: D PO0 PO1 PD PO2 PO3 D, closed ring)"), fontsize=9)
ax.set_xlim(-1.5, 61.5); ax.set_ylim(-1.8, 17); ax.set_aspect("equal"); ax.set_xlabel("µm (cell coordinates)")
ax.set_title("bias_dist_pd (60.49 × 16.24 µm): NWell light green, pSD tan, Activ green, GatPoly red, Cont black, M1 blue", fontsize=10)
fig.tight_layout(); fig.savefig("1_switch_row.png", dpi=130); plt.close(fig)
# --- figure 2: tie strips vs. ring, left part
fig, ax = plt.subplots(figsize=(15, 8))
win = (-0.6, -0.8, 21.0, 9.0)
draw(ax, top, win)
for y0, y1, lab in [(0.0, 0.3, "tie strip vssh: p+ Activ (pSD) + Cont + M1, y 0.00–0.30, x 0.27–59.52, along the whole row"),
                    (4.4, 4.7, "tie strip vddh: n+ Activ in the NWell + Cont + M1, y 4.40–4.70, x 0.27–59.52")]:
    ax.add_patch(Rectangle((0.27, y0), 20.5, y1 - y0, fc="none", ec="#ff6f00", lw=2.2))
    ax.text(0.3, y1 + 0.12 if y0 > 1 else y0 - 0.45, lab, color="#e65100", fontsize=10, weight="bold")
ax.text(0.3, 2.45, "switches and logic of the slices between the two strips; open at the left and right ends (no closed ring)",
        fontsize=9, color="#6a1b9a")
ax.annotate("closed tie ring of bdp_mirror_n (for comparison)", xy=(10, 6.95), xytext=(6, 6.2), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#2e7d32"), color="#2e7d32")
ax.set_xlim(win[0], win[2]); ax.set_ylim(win[1], win[3]); ax.set_aspect("equal"); ax.set_xlabel("µm (cell coordinates)")
ax.set_title("Tie strips of the switch row (left part: input slices in0..in3 and TDN)", fontsize=11)
fig.tight_layout(); fig.savefig("2_tie_strips.png", dpi=130); plt.close(fig)
# --- figure 3: the TG's split gates and the narrow-poly check
tg = ly.cell("bdp_tg_hv")
fig, ax = plt.subplots(figsize=(12, 11))
draw(ax, tg)
act = reg(tg, (1, 0)); gp = reg(tg, (5, 0)); ct = db.Region(tg.begin_shapes_rec(ly.layer(6, 0)))
zone = act.sized(int(round(0.25 / u)))
for p in (zone & db.Region(db.Box(int(-0.5 / u), int(0.5 / u), int(1.6 / u), int(4.3 / u)))).each():
    ax.add_patch(Polygon([(q.x * u, q.y * u) for q in p.each_point_hull()], fc="none", ec="#6a1b9a", lw=1.5, ls="--"))
beyond = (gp - zone).interacting(ct)
for p in beyond.each():
    ax.add_patch(Polygon([(q.x * u, q.y * u) for q in p.each_point_hull()], fc="#ffeb3b", ec="#f57f17", lw=2, hatch="////", alpha=0.9))
for e in beyond.width_check(int(round(0.30 / u))).each():
    for ed in (e.first, e.second):
        ax.plot([ed.p1.x * u, ed.p2.x * u], [ed.p1.y * u, ed.p2.y * u], color="red", lw=3)
ax.text(1.35, 3.45, "TGP (PMOS, gate = ei_b)", fontsize=10); ax.text(1.35, 1.2, "TGN (NMOS, gate = ei)", fontsize=10)
ax.text(1.35, 2.6, "TGP's gate poly + contact pad\n(0.45 µm wide)", fontsize=9)
ax.text(1.35, 1.95, "TGN's gate poly + contact pad\n(0.45 µm wide)", fontsize=9)
dev = sorted([p.bbox() for p in act.each() if p.bbox().height() * u > 0.5], key=lambda b: b.bottom)
ya, yb = dev[0].top * u, dev[1].bottom * u
ax.annotate("", xy=(-0.35, ya), xytext=(-0.35, yb), arrowprops=dict(arrowstyle="<->"))
ax.text(-0.95, (ya + yb) / 2, f"{yb - ya:.2f} µm\nActiv to Activ\n(round 1: 1.24)", fontsize=8, ha="center")
ax.text(1.35, 5.2, "dashed: 'endcap zone' = Activ grown by 0.25 µm\nhatched: poly beyond it that touches a contact"
        "\nred: where the check measures < 0.30 µm\n(round 2: both pads reach >= 0.32 µm beyond the zone: no flag;\n"
        "round 1 had 0.14 / 0.27 µm. The pads are 0.45 µm wide)", fontsize=9, va="top")
ax.set_xlim(-1.6, 4.6); ax.set_ylim(-0.3, 5.3); ax.set_aspect("equal"); ax.set_xlabel("µm (cell bdp_tg_hv)")
ax.set_title("Split switch gates of the transmission gate tg_hv, and the narrow-poly check", fontsize=11)
fig.tight_layout(); fig.savefig("3_split_gates_narrow_poly.png", dpi=130); plt.close(fig)
print("ok")
