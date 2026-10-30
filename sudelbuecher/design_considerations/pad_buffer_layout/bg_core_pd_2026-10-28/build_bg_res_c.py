# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""bg_res_c: the bandgap's rhigh array (R0, R1A, R1B) without the added p-tap ring and without the 0.6 um R0
stretch reserves, wired anew. Written 2026-10-28 by Claude (Opus 5.5).

    python3 build_bg_res_c.py <pad_buffer_cells.gds> <out.gds> <out.cdl>

What stays: the library's rhigh cell (rhigh$1, 0.5 x 9.94 um, unmodified), the 41 positions at 0.68 um pitch and
their interleave (read from the library bg_res's own labels: dummy, R0 x 18, R1A x 11, R1B x 10, dummy).
What is new: the wiring. Each resistor is a chain of consecutive segments, left to right, linked alternately at
the bottom and top heads: Via1 on the head's Metal1, a Metal2 stub to a link level, a Metal1 link along the level.
Links share levels where they do not overlap (interval colouring), so there are as few levels as the pattern
needs. Terminals (revised for the bg_core_pd floorplan): e2 (R0 start, left end), ea (R1A end, right end) and eb
(R0 end + R1B end, right end) as Metal2 pins on the TOP edge. R1A runs from vss (left, entered at its bottom head:
11 segments put its two ends on opposite sides) to ea (right, top head). vss on the BOTTOM edge through two Metal2
drop columns at the array ends (the vss starts of R1A and R1B on the left, the dummies), joined by a Metal2 bus.
No tie: rhigh's bulk is the substrate, tied by the block (the deck's latch-up rules concern MOS diffusion only).
Rule values: out/v2/process/ihp_sg13cmos5l.py (json keys there): M1_b 0.18, M2 Mn_b 0.21, V1_a 0.19, V1_c1 0.05,
grid 0.005; wire = via pad 0.29 (V1_a + 2 V1_c1).
"""
import importlib.util
import os
import sys

import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("adapter", os.path.join(HERE, "..", "out", "v2", "process",
                                                                      "ihp_sg13cmos5l.py"))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
R = P.rules()
LIB, OUT, CDL = sys.argv[1], sys.argv[2], sys.argv[3]

g5 = lambda v: round(round(v / R["grid"]) * R["grid"], 4)
W = g5(R["via1.size"] + 2 * R["via1.enc_end"])      # 0.29: wire = via pad
H = W / 2
S1, S2 = R["m1.space"], R["m2.space"]
PITCH = 0.68                                          # library bg_res pitch (rhigh 0.5 + Gat.b 0.18)
HEAD_BOT, HEAD_TOP = -0.28, 10.22                     # head Metal1 centres in rhigh$1 (measured: M1 -0.41..-0.15,
HEAD_M1 = (-0.41, -0.15, 10.09, 10.35)                #  10.09..10.35); head x centre 0.25
XC = 0.25

src = db.Layout()
src.read(LIB)
lib_res = src.cell("bg_res")
labels = sorted((s.dtext.x, s.text_string) for s in lib_res.shapes(src.find_layer(63, 0)).each() if s.is_text())
pattern = [n.split(".")[0] for _, n in labels]       # 'dummy', 'R0', 'R1A', 'R1B'
assert len(pattern) == 41 and pattern.count("R0") == 18 and pattern.count("R1A") == 11 and pattern.count("R1B") == 10

ly = db.Layout()
ly.dbu = src.dbu
rcell = ly.create_cell("rhigh$1")
for li in src.layer_indexes():                         # copy the device cell unchanged
    info = src.get_info(li)
    for s in src.cell("rhigh$1").shapes(li).each():
        rcell.shapes(ly.layer(info.layer, info.datatype)).insert(s)
top = ly.create_cell("bg_res_c")
L = {k: ly.layer(*P.LAYERS[k]) for k in ("m1", "via1", "m2", "m2.pin", "m2.text", "m1.pin", "m1.text")}
note = ly.layer(63, 0)
for i in range(41):
    top.insert(db.DCellInstArray(rcell.cell_index(), db.DTrans(g5(i * PITCH), 0)))
    top.shapes(note).insert(db.DText("%s" % pattern[i], g5(i * PITCH + XC), 5.0))
xh = lambda i: g5(i * PITCH + XC)


def box(lay, x0, y0, x1, y1):
    top.shapes(L[lay]).insert(db.DBox(g5(min(x0, x1)), g5(min(y0, y1)), g5(max(x0, x1)), g5(max(y0, y1))))


def via(x, y):
    a = R["via1.size"] / 2
    box("via1", x - a, y - a, x + a, y + a)


# ---- chains, links, terminals ----------------------------------------------------------------------------------
pos = {r: [i for i, p in enumerate(pattern) if p == r] for r in ("R0", "R1A", "R1B")}
# start terminal (at the TOP head of the first segment, left) and end terminal of each chain
ENDS = {"R0": ("e2", "eb"), "R1A": ("vss", "ea"), "R1B": ("vss", "eb")}
START = {"R0": "top", "R1A": "bot", "R1B": "top"}   # head side the first segment is entered at
links = {"top": [], "bot": []}                         # (net, x_a, x_b, [via xs], tag)
heads_term = []                                        # (net, side, i)
devices = []                                           # (name, a, b) for the reference
for r, ps in pos.items():
    n = len(ps)
    nodes = [ENDS[r][0]] + ["%s_%d" % (r, k + 1) for k in range(n - 1)] + [ENDS[r][1]]
    for k, i in enumerate(ps):
        other = "bot" if START[r] == "top" else "top"
        enter = START[r] if k % 2 == 0 else other
        leave = "bot" if enter == "top" else "top"
        devices.append(("%s_%d" % (r, k), nodes[k], nodes[k + 1]))
        if k == 0:
            heads_term.append((nodes[0], enter, i))
        if k == n - 1:
            heads_term.append((nodes[-1], leave, i))
        else:
            links[leave].append((nodes[k + 1], xh(i), xh(ps[k + 1]), [xh(i), xh(ps[k + 1])], r))
# drop columns for vss (left and right of the array), dummies tied there
XL = g5(xh(0) - W - S2)                                # M2 column left of the dummy's own stub column
XR = g5(xh(40) + W + S2)
devices += [("dummy_L", "vss", "vss"), ("dummy_R", "vss", "vss")]
term = {}
for net, side, i in heads_term:
    term.setdefault(net, []).append((side, i))
# vss: R1B's start (top, left) -> left column; R1A's end (bottom, right) -> right column
for side, i in term.pop("vss"):
    col = XL if i < 20 else XR
    links[side].append(("vss", min(col, xh(i)), max(col, xh(i)), [xh(i), col], "vss"))
# eb: R0's end and R1B's end, both on top at the right: one link
eb = term.pop("eb")
assert all(s == "top" for s, _ in eb), eb
links["top"].append(("eb", min(xh(i) for _, i in eb), max(xh(i) for _, i in eb), [xh(i) for _, i in eb], "eb"))
pins_top = [(net, xh(i)) for net, lst in term.items() for side, i in lst if side == "top"]
pins_top.append(("eb", xh(max(i for _, i in eb))))
assert all(side == "top" for lst in term.values() for side, _ in lst), term


def levels(lst):
    """greedy interval colouring: links on one level keep the Metal1 space"""
    out = []
    for l in sorted(lst, key=lambda t: (t[1], t[2])):
        for k, lev in enumerate(out):
            if all(l[1] - H >= o[2] + H + S1 or o[1] - H >= l[2] + H + S1 for o in lev):
                lev.append(l)
                break
        else:
            out.append([l])
    return out


LV = {s: levels(links[s]) for s in ("top", "bot")}
y_lev = {"bot": [g5(HEAD_M1[0] - S1 - H - k * (W + S1)) for k in range(len(LV["bot"]))],
         "top": [g5(HEAD_M1[3] + S1 + H + k * (W + S1)) for k in range(len(LV["top"]))]}
y_head = {"bot": HEAD_BOT, "top": HEAD_TOP}
for side in ("top", "bot"):
    for k, lev in enumerate(LV[side]):
        y = y_lev[side][k]
        for net, x0, x1, vx, tag in lev:
            box("m1", x0 - H, y - H, x1 + H, y + H)          # the link
            for x in vx:
                via(x, y)
                if x in (XL, XR):                            # drop column: Metal2 down to the bottom edge later
                    continue
                via(x, y_head[side])                         # head via
                box("m2", x - H, min(y, y_head[side]) - H, x + H, max(y, y_head[side]) + H)
# edges
y_top = g5((y_lev["top"][-1] if y_lev["top"] else HEAD_M1[3]) + H)
y_bot = g5((y_lev["bot"][-1] if y_lev["bot"] else HEAD_M1[0]) - H)
# terminal pins on the top edge: head via + Metal2 straight up
for net, x in pins_top:
    via(x, HEAD_TOP)
    box("m2", x - H, HEAD_TOP - H, x + H, y_top)
    box("m2.pin", x - H, y_top - W, x + H, y_top)
    top.shapes(L["m2.text"]).insert(db.DText(net, x, g5(y_top - H)))
# vss bus: Metal2 below the lowest link level (no head stub reaches below its level), joins both drop columns
y_bus = g5(y_bot - S2 - H)
box("m2", XL - H, y_bus - H, XR + H, y_bus + H)
y_bot = g5(y_bus - H)
# dummies: both heads by Metal1 to the drop column of their side; drop columns from the top level to the bus
for i, col in ((0, XL), (40, XR)):
    for yh, side in ((HEAD_BOT, "bot"), (HEAD_TOP, "top")):
        box("m1", min(col, xh(i)) - H, yh - 0.13, max(col, xh(i)) + H, yh + 0.13)
        via(col, yh)
    yc_top = max([HEAD_TOP] + [y_lev["top"][k] for k, lev in enumerate(LV["top"]) for l in lev if col in l[3]])
    box("m2", col - H, y_bot, col + H, yc_top + H)
    box("m2.pin", col - H, y_bot, col + H, y_bot + W)
    top.shapes(L["m2.text"]).insert(db.DText("vss", col, g5(y_bot + H)))
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(OUT, opt)
bb = top.dbbox()
sq = 9.94 / 0.5
with open(CDL, "w") as f:
    f.write("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
            "* bg_res_c (build_bg_res_c.py, 2026-10-28, Claude): rhigh segments as two-terminal resistors, R in\n"
            "* squares (l / w = 9.94 / 0.5); bulk = substrate (vss), not a port of the comparison.\n"
            "* R0 e2-eb 18 x 9.94 = 178.92 um, R1A vss-ea 11 x = 109.34 um, R1B vss-eb 10 x = 99.40 um, 2 dummies on vss\n"
            ".SUBCKT bg_res_c e2 ea eb vss\n")
    for name, a, b in devices:
        f.write("R%s %s %s %g\n" % (name, a, b, sq))
    f.write(".ENDS bg_res_c\n")
print("bg_res_c: %.3f x %.3f um = %.1f um2 (library bg_res 30.40 x 16.94 = 515.0); levels top %d bottom %d; pins %s"
      % (bb.width(), bb.height(), bb.width() * bb.height(), len(LV["top"]), len(LV["bot"]),
         sorted(pins_top) + [("vss", XL), ("vss", XR)]))
