# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""To-scale floorplan sketches of rb_casc: A as drawn (agent N, round 5, geometry read from rb_n_cells.gds), B and C
derived from A's pitches. Activ and gate poly only; not layouts (no DRC / LVS)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

R1, R2 = (0.0, 3.68), (6.27, 9.95)          # Activ y of row 1 / row 2 (from the GDS)
G1, G2 = (0.34, 3.34), (6.61, 9.61)         # channel (gate poly) y, L = 3 um
BN = (0.635, 9.315)                         # BNC Activ y (8.68 um), spans both rows and the band
COL = {"F": "#4C78A8", "CY": "#B279A2", "BNC": "#E45756", "D": "#9D9D9D", "X": "#9D9D9D", "T": "#E45756", "d": "#9D9D9D"}

def fingers(ax, row, items):
    ya, yb = (R1 if row == 1 else R2)
    ga, gb = (G1 if row == 1 else G2)
    for x0, x1, lab, kind in items:
        if kind == "field":
            ax.add_patch(Rectangle((x0, ga), x1 - x0, gb - ga, fc="#F2B8B5", ec="#C0392B", ls="--", lw=1.0, alpha=0.6))
            ax.text((x0 + x1) / 2, (ya + yb) / 2, "poly over field", ha="center", va="center", fontsize=8, color="#7B241C")
            continue
        dummy = kind in ("D", "X", "d", "T")
        ax.add_patch(Rectangle((x0, ya), x1 - x0, yb - ya, fc=COL[kind], ec="black", lw=0.6,
                               hatch="///" if dummy else None, alpha=0.55 if dummy else 0.85))
        ax.add_patch(Rectangle((x0, ga), x1 - x0, gb - ga, fc="none", ec="#C0392B", lw=0.6))
        if x1 - x0 > 3:
            ax.text((x0 + x1) / 2, (ya + yb) / 2, lab, ha="center", va="center", fontsize=9,
                    color="black" if dummy else "white", weight="bold")

def bnc(ax, x0, lab, twin=False):
    ax.add_patch(Rectangle((x0, BN[0]), 1.0, BN[1] - BN[0], fc=COL["BNC"], ec="black", lw=0.6,
                           hatch="///" if twin else None, alpha=0.55 if twin else 0.9))
    ax.text(x0 + 0.5, 4.975, lab, ha="center", va="center", fontsize=8, rotation=90, weight="bold")

def frame(ax, x0, x1, title, notes):
    ax.add_patch(Rectangle((x0, -1.21), x1 - x0, 12.37, fc="none", ec="#2E7D32", lw=2.0))   # ring outline
    ax.axhspan(3.68, 6.27, xmin=0, xmax=1, color="#E8DAEF", alpha=0.35, lw=0)
    ax.text(x0 + 4.5, 4.975, "band: M2 tracks vbnc, vdd (+ 3 dummy tracks)", fontsize=8, va="center", color="#5B2C6F")
    ax.set_title(title, loc="left", fontsize=12, weight="bold")
    ax.text(1.0, 1.02, notes, transform=ax.transAxes, ha="right", va="bottom", fontsize=9)
    ax.set_xlim(-3, 73); ax.set_ylim(-2, 12); ax.set_aspect("equal"); ax.set_yticks([])
    ax.set_xlabel("µm")

fig, axs = plt.subplots(3, 1, figsize=(16, 11))
# A: as drawn
a1 = [(0, 2, "D", "D"), (2.25, 17.25, "F1", "F"), (17.5, 32.5, "F2", "F"),
      (35.2, 50.2, "CY", "CY"), (50.45, 65.45, "X 15/3", "X"), (65.7, 67.7, "D", "D")]
a2 = [(0, 2, "D", "D"), (2.25, 17.25, "X 15/3", "X"), (17.5, 32.5, "X 15/3", "X"),
      (35.2, 50.2, "F3", "F"), (50.45, 65.45, "F4", "F"), (65.7, 67.7, "D", "D")]
fingers(axs[0], 1, a1); fingers(axs[0], 2, a2); bnc(axs[0], 33.35, "BNC")
frame(axs[0], -2.01, 69.71, "A  as drawn (round 5): 8 slots, BNC in the middle",
      "71.7 µm long | 7 dummies: 4 × 2/3 + 3 × 15/3 | dummy gate on vbnc 159 µm² | mirror check: pass (measured)")
# B: 8 slots, the spare slots as a narrow dummy beside the active neighbour + poly over field
b1 = [(0, 2, "D", "D"), (2.25, 17.25, "F1", "F"), (17.5, 32.5, "F2", "F"),
      (35.2, 50.2, "CY", "CY"), (50.45, 52.45, "d", "d"), (52.45, 65.45, "", "field"), (65.7, 67.7, "D", "D")]
b2 = [(0, 2, "D", "D"), (2.25, 17.25, "", "field"), (17.5, 30.5, "", "field"), (30.5, 32.5, "d", "d"),
      (35.2, 50.2, "F3", "F"), (50.45, 65.45, "F4", "F"), (65.7, 67.7, "D", "D")]
fingers(axs[1], 1, b1); fingers(axs[1], 2, b2); bnc(axs[1], 33.35, "BNC")
frame(axs[1], -2.01, 69.71, "B  8 slots kept, spare slots: narrow 2/3 dummy beside the active neighbour, the rest poly over field",
      "71.7 µm | 6 dummies: 6 × 2/3 | dummy gate on vbnc 36 µm² | Activ not mirror-symmetric (F centroid unchanged)")
# C: 6 slots, BNC and its twin at the row ends; F at the outer slots of both rows (common centroid), CY / X in the middle
g, gb = 0.25, 0.85                          # finger gap; BNC to finger edge (as in A)
x = 1.0 + gb; c1, c2 = [], []
for k, (l1, k1, l2, k2) in enumerate([("F1", "F", "F3", "F"), ("CY", "CY", "X 15/3", "X"), ("F2", "F", "F4", "F")]):
    c1.append((x, x + 15, l1, k1)); c2.append((x, x + 15, l2, k2)); x += 15 + g
xe = x - g + gb
fingers(axs[2], 1, c1); fingers(axs[2], 2, c2); bnc(axs[2], 0.0, "BNC"); bnc(axs[2], xe, "BNC twin", twin=True)
frame(axs[2], -2.01, xe + 1.0 + 2.01, "C  6 slots, BNC at one end, its twin (dummy 1/8) at the other",
      f"≈ {xe + 1.0 + 4.02:.0f} µm (estimate) | 2 dummies: 1 × 15/3 + twin 1/8 | dummy gate on vbnc 53 µm² | Activ mirror-symmetric")
for ax in axs:
    ax.spines[["top", "right", "left"]].set_visible(False)
fig.suptitle("rb_casc alternatives, to scale (Activ, gate channel; hatched = dummy, D = S = B = vss, gate vbnc by abutment). "
             "Sketches from A's pitches, not drawn layouts.", fontsize=11, y=0.995)
fig.tight_layout()
fig.savefig("rb_casc_alternatives.png", dpi=130)
print("ok", xe)
