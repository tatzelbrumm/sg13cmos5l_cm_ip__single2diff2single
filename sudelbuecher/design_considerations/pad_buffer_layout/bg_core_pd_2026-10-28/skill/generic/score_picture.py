# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""score_picture.py: the placement of a block as a 'score' picture (process-free: only cell instances and rails).
Written 2026-10-28 by Claude (Opus 5.5).

    python3 score_picture.py <gds> <cell> <out.png> '<json letter map {"cell name": "letter"}>'

Each primitive is a box with its letter and its transform in both notations (KLayout code / music alias:
R0 = P prime, M90 = R retrograde, M0 = I inversion, R180 = RI retrograde inversion). Rails = top-level shapes
spanning >= 90 % of the block width (any layer). A 10 um scale bar.
"""
import json
import sys

import klayout.db as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
from matplotlib.patches import Rectangle           # noqa: E402

gds, cell, out = sys.argv[1:4]
letters = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
ALIAS = {"r0": "P", "m90": "R", "m0": "I", "r180": "RI", "r90": "R90", "r270": "R270", "m45": "M45", "m135": "M135"}
ly = db.Layout()
ly.read(gds)
top = ly.cell(cell)
bb = top.dbbox()
fig, ax = plt.subplots(figsize=(bb.width() / 6 + 1, bb.height() / 6 + 1.2), dpi=150)
for li in ly.layer_indexes():
    for s in top.shapes(li).each():
        b = s.dbbox()
        if not s.is_text() and b.width() >= 0.9 * bb.width():
            ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fc="#9db0ff", ec="none", alpha=0.6))
cols = ["#f4d35e", "#83c5be", "#ee964b", "#a3c4f3", "#cdb4db", "#b5e48c", "#ffadad", "#bdb2ff"]
for k, inst in enumerate(top.each_inst()):
    b = inst.dbbox()
    code = inst.trans.to_s().split()[0].lower()
    name = inst.cell.name
    lt = letters.get(name, name)
    ax.add_patch(Rectangle((b.left, b.bottom), b.width(), b.height(), fc=cols[k % len(cols)], ec="black", lw=1.0))
    ax.text((b.left + b.right) / 2, (b.bottom + b.top) / 2, "%s\n%s = %s\n%s" % (lt, code.upper(), ALIAS.get(code, code),
                                                                              name),
            ha="center", va="center", fontsize=7)
ax.set_xlim(bb.left - 1, bb.right + 1)
ax.set_ylim(bb.bottom - 3, bb.top + 1)
ax.set_aspect("equal")
ax.plot([bb.left, bb.left + 10], [bb.bottom - 1.8, bb.bottom - 1.8], color="black", lw=2)
ax.text(bb.left + 5, bb.bottom - 2.2, "10 um", ha="center", va="top", fontsize=6)
ax.set_title("%s placement score: %.2f x %.2f um" % (cell, bb.width(), bb.height()), fontsize=8)
ax.axis("off")
fig.savefig(out, bbox_inches="tight")
print("wrote", out)
