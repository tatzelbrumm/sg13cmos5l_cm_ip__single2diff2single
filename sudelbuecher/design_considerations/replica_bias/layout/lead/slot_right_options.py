# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""slot7 to scale: the pins that matter for pad_ref_rb and the bias blocks (from final/gds/slot_7.gds and
slot7_pins.md), and two candidate positions for pad_ref_rb near the custom pads. Blocks without layout are dashed
placeholders of guessed size. A sketch for Christoph's decision, not a floorplan."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
W, H = 537.15, 273.0
R = [("vref", 112.26, "S2D"), ("outp", 123.87, "S2D"), ("outn", 129.97, "S2D"), ("vcm", 136.02, "S2D"),
     ("en_3v3", 142.65, "S2D"), ("en_3v3_b", 153.84, "S2D"), ("iref", 159.51, "S2D"),
     ("vinp", 222.26, "D2S"), ("vinn", 222.8, "D2S"), ("vref (= vcm)", 223.34, "D2S"), ("iref", 260.6, "D2S"),
     ("en_3v3_b", 261.14, "D2S"), ("en_3v3", 261.68, "D2S")]
L = [("vbias", 95.22), ("ibias0", 98.16), ("ibias1", 101.09), ("analog_bus3..0", 104.03), ("vss_3v3", 128.55),
     ("vdd_3v3", 203.6), ("dig_in / dig_out", 72.3), ("vdd_1v2", 29.4)]
fig, axs = plt.subplots(2, 1, figsize=(15, 15.5))
for ax, (title, prb, note) in zip(axs, [
        ("Option 1: pad_ref_rb beside the S2D pins; vref (112.3) and vcm (136.0) straight out",
         (441, 104, 90, 37, (452, 70, 79, 27)), "core top below the S2D's en_3v3 line (142.7), so the pads' en / iref lines pass above it; bypass_rb below the core, on vref / vcm"),
        ("Option 2: pad_ref_rb between the pad pin groups (top right)",
         (465, 166, 66, 50, (380, 175, 79, 27)), "vcm 30 / 57 µm vertical to 136.0 and 223.3, vref 54 µm down to 112.3; bypass_rb left of the core")]):
    ax.add_patch(Rectangle((0, 0), W, H, fc="none", ec="black", lw=1.5))
    ax.add_patch(Rectangle((533.15, 11.63), 2.0, 59.4, fc="#b39ddb", ec="none"))
    ax.text(530, 40, "M2 vss_1v2", rotation=90, fontsize=7, ha="right")
    for n, y, p in R:
        c = "#e67e22" if p == "S2D" else "#8e44ad"
        ax.plot([535.05, 536.45], [y, y], color=c, lw=3)
        dy = {"vinp": -4, "vinn": 0, "vref (= vcm)": 4, "iref": 0 if p == "S2D" else -4, "en_3v3_b": 0 if p == "S2D" else 0,
              "en_3v3": 0 if p == "S2D" else 4}.get(n, 0)
        ax.text(538, y + dy, f"{p} {n} {y:.1f}", fontsize=6.5, va="center", color=c)
    for n, y in L:
        ax.plot([0, 2], [y, y], color="#2c3e50", lw=3); ax.text(4, y, f"{n} {y:.1f}", fontsize=6.5, va="center")
    x, y, w, h, (bx, by, bw, bh) = prb
    ax.add_patch(Rectangle((x, y), w, h, fc="#f5b7b1", ec="#c0392b", lw=1.5))
    ax.text(x + w / 2, y + h / 2, f"pad_ref_rb core\n(rows 2640 µm²;\n≈ {w} × {h} µm at ~80 %)", ha="center", va="center", fontsize=7)
    ax.add_patch(Rectangle((bx, by), bw, bh, fc="#fadbd8", ec="#c0392b", lw=1.2, ls="--"))
    ax.text(bx + bw / 2, by + bh / 2, f"bypass_rb 2 × 6\n{bw} × {bh} µm (2133 µm²)", ha="center", va="center", fontsize=7)
    x = min(x, bx) if bx < x else x
    # bias blocks: cores to scale (oa 40.5 x 58.1, bg 47.6 x 50.1), the rest placeholders
    ax.add_patch(Rectangle((x - 50, y - 6), 40, 40, fc="none", ec="#1f77b4", ls="--", lw=1.2))
    ax.text(x - 30, y + 14, "bias_dist_pd\n(no layout)", ha="center", fontsize=7, color="#1f77b4")
    ax.add_patch(Rectangle((x - 150, y - 25), 40.5, 58.1, fc="#d6eaf8", ec="#1f77b4"))
    ax.text(x - 130, y + 4, "oa_core_pd\n40.5 × 58.1", ha="center", fontsize=7)
    ax.add_patch(Rectangle((x - 105, y - 25), 47.6, 50.1, fc="#d6eaf8", ec="#1f77b4"))
    ax.text(x - 81, y, "bg_core_pd\n47.6 × 50.1", ha="center", fontsize=7)
    ax.text(x - 150, y - 34, "bias_gen_pd (sel. logic + TGs: no layout)", fontsize=7, color="#1f77b4")
    ax.annotate("", xy=(x - 150, 99.5), xytext=(3, 99.5), arrowprops=dict(arrowstyle="->", color="gray", ls=":"))
    ax.text(150, 95, "harness ibias0 / ibias1 from the left edge", fontsize=7, color="gray")
    ax.set_title(title, fontsize=10, loc="left"); ax.text(300, -16, note, ha="center", fontsize=9)
    ax.set_xlim(-5, 610); ax.set_ylim(-22, 280); ax.set_aspect("equal"); ax.set_xlabel("x (µm, slot coordinates)")
fig.suptitle("slot7 (537 × 273 µm) to scale: pad pins (right edge, Metal3), harness bias pins (left edge); "
             "bias blocks' positions are placeholders to be decided", fontsize=10)
fig.tight_layout(); fig.savefig("slot_right_options.png", dpi=130)
