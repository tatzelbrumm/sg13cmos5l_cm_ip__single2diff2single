# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""The whole slot7 frame (537.15 x 273 um) with the drawn layouts placed, for a size estimate: pad_ref_rb v2 (agent F)
at F's proposed position; oa_core_pd and bg_core_pd stacked vertically to its left and bias_dist_pd (agent D) above them
(positions proposed). vcm / vref drawn straight out to the edge; the run to the S2D
pins is global routing. Device layers of the placed cells; frame pins from final/gds/slot_7.gds."""
import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
REPO = "/home/user/sg13cmos5l_cm_ip__single2diff2single/"
F = "/tmp/claude-0/-home-user-sg13cmos5l-cm-ip--single2diff2single/f7165478-7787-531e-a1d8-6ec7206ebfcb/scratchpad/layout_rb/F/out/"
W, H = 537.15, 273.0
PLACE = [  # (gds, cell, x0, y0 of the cell's bbox corner, label)
    (F + "pad_ref_rb.gds", "pad_ref_rb", 461.20, 169.07, "pad_ref_rb v2\n73.8 × 76.3"),
    (REPO + "macros/bg_core_pd/layout/gds/bg_core_pd.gds", "bg_core_pd", 457.2 - 47.55, 169.07, "bg_core_pd\n47.6 × 50.1"),
    (REPO + "macros/oa_core_pd/layout/gds/oa_core_pd.gds", "oa_core_pd", 457.2 - 40.51, 169.07 - 2 - 58.13, "oa_core_pd\n40.5 × 58.1"),
    ("/tmp/claude-0/-home-user-sg13cmos5l-cm-ip--single2diff2single/f7165478-7787-531e-a1d8-6ec7206ebfcb/scratchpad/layout_rb/D/out/bias_dist_pd.gds",
     "bias_dist_pd", 457.2 - 60.49, 221.12, "bias_dist_pd (agent D)\n60.5 × 16.2"),
]
STY = [((31, 0), "#c8e6c9", 0.55), ((1, 0), "#2f8f2f", 0.7), ((5, 0), "#e8443a", 0.5), ((8, 0), "#4a90e2", 0.3),
       ((10, 0), "#b05ad6", 0.3)]
fig, ax = plt.subplots(figsize=(18, 9.6))
ax.add_patch(Rectangle((0, 0), W, H, fc="#fafafa", ec="black", lw=1.5))
used = 0.0
for gds, name, x0, y0, lab in PLACE:
    ly = db.Layout(); ly.read(gds); c = ly.cell(name); u = ly.dbu; bb = c.bbox()
    dx, dy = x0 - bb.left * u, y0 - bb.bottom * u
    for ld, col, a in STY:
        li = ly.find_layer(*ld)
        if li is None: continue
        for p in db.Region(c.begin_shapes_rec(li)).merged().each():
            ax.add_patch(Polygon([(q.x * u + dx, q.y * u + dy) for q in p.each_point_hull()], fc=col, ec="none", alpha=a))
    w, h = bb.width() * u, bb.height() * u; used += w * h
    ax.add_patch(Rectangle((x0, y0), w, h, fc="none", ec="#c0392b", lw=1.2))
    ax.text(x0 + w / 2, y0 + h + 1.5, lab, ha="center", va="bottom", fontsize=7.5, color="#c0392b")
# frame pins
ly = db.Layout(); ly.read(REPO + "final/gds/slot_7.gds"); t = ly.top_cell(); u = ly.dbu
for li in ly.layer_indexes():
    for sh in t.shapes(li).each():
        if sh.is_text():
            x, y, s = sh.text.x * u, sh.text.y * u, sh.text.string
            if x > 530 and ly.get_info(li).layer == 30:
                ax.plot([535.05, 536.45], [y, y], color="#e67e22", lw=2.5)
            elif x < 5 and s in ("ibias0", "ibias1", "vbias", "vdd_3v3", "vss_3v3", "vdd_1v2", "vss_1v2"):
                ax.plot([0, 2], [y, y], color="#2c3e50", lw=2.5); ax.text(3, y, s, fontsize=7, va="center")
for y, s in [(112.26, "S2D vref"), (136.02, "S2D vcm"), (159.51, "S2D iref"), (223.34, "D2S vref (= vcm)"), (260.6, "D2S iref")]:
    ax.text(538, y, s, fontsize=7, va="center", color="#e67e22")
ax.add_patch(Rectangle((533.15, 11.63), 2.0, 59.43, fc="#b39ddb", ec="none")); ax.text(531, 40, "M2 vss_1v2", rotation=90, fontsize=7, ha="right")
# pad_ref_rb outputs straight out (pins from F's pin map: vcm y 223.34, vref y 179.06 at the cell's right edge x 535.0)
ax.plot([535.0, 536.45], [223.34, 223.34], color="#8e44ad", lw=2); ax.plot([535.0, 536.45], [179.06, 179.06], color="#e91e63", lw=2)
ax.text(533, 181.5, "vref straight out", fontsize=6.5, ha="right", color="#e91e63")
ax.set_xlim(-5, 575); ax.set_ylim(-5, 280); ax.set_aspect("equal"); ax.set_xlabel("x (µm, slot coordinates)")
ax.set_title(f"slot7 (537.15 × 273 µm = 146,600 µm²) with the drawn layouts placed: {used:,.0f} µm² ({100 * used / (W * H):.1f} %) "
             "; core / bias_dist positions are proposals, the routes to the pad pins are global routing", fontsize=10)
fig.tight_layout(); fig.savefig("slot_frame_view.png", dpi=130)
print("placed", round(used), "um2", round(100 * used / (W * H), 1), "%")
