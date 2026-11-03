# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 stage B: pwr_f2, the block's supply taps and NWell bridges (pad coordinates).

    python3 make_pwr.py <out.gds>

Taps: Metal2 pad 0.60 x 0.60 with two Via2 (Vn_a 0.19, Vn_b 0.22) and a Metal3 pad into the ring rail above
(Metal3 iovdd y 84 .. 91.5 and 93.5 .. 119, iovss 126 .. 134; phase 1 report 1.4); the pad carries a Metal2 label
with the routing net, so the router ends that net there. Each supply group taps the ring at one point (the
brief: the tail and sink source buses one point each; vddo / vsso their own taps). On the stages' n+ rings the tap
sits directly on the ring (Via1 + Via2 stack).
NWell bridges (one iovdd well for the circuit's PMOS, NW_a 0.62 wide at least): loads / casc_p, casc_p / the inputs'
lower dummy tubs, the inputs' upper dummy tubs / tails, tails / bias_tree_p, and the tongue from bias_tree_p to TGP
(in d2s_tgsw_f2); the 2 kOhm stages keep their own wells (NW_b1 1.80 from the circuit's).
"""
import sys

import klayout.db as db

ly = db.Layout()
ly.dbu = 0.001
c = ly.create_cell("pwr_f2")
L = {k: ly.layer(*v) for k, v in {"M1": (8, 0), "V1": (19, 0), "M2": (10, 0), "M2pin": (10, 2), "M2txt": (10, 25),
                                  "V2": (29, 0), "M3": (30, 0), "NW": (31, 0)}.items()}


def box(k, x0, y0, x1, y1):
    c.shapes(L[k]).insert(db.DBox(round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)))


def tap(net, x, y, via1=False):
    box("M2", x - 0.40, y - 0.30, x + 0.40, y + 0.30)      # Vn_c1 0.05 beyond the via row's ends
    box("M3", x - 0.40, y - 0.30, x + 0.40, y + 0.30)
    for dx in (-0.205, 0.205):                       # Vn_a 0.19, Vn_b 0.22: centers 0.41 apart
        box("V2", x + dx - 0.095, y - 0.095, x + dx + 0.095, y + 0.095)
    if via1:                                          # straight onto a ring's Metal1 under the pad
        box("V1", x - 0.095, y - 0.095, x + 0.095, y + 0.095)
    if net:
        box("M2pin", x - 0.40, y - 0.30, x + 0.40, y + 0.30)
        c.shapes(L["M2txt"]).insert(db.DText(net, x, y))


TAPS = [("iovdd_ld", 27.50, 88.55), ("iovdd_cp", 25.00, 103.55), ("iovdd_ab", 43.70, 101.55),
        ("iovdd_o", 49.90, 101.10), ("iovdd_up", 3.30, 117.30), ("iovss_m", 60.20, 128.00),
        ("iovss_sk", 60.20, 131.60)]
for n, x, y in TAPS:
    tap(n, x, y)
# vsso (SB's source) gets its own way to the ring: a landing pad at the bottom, joined to the P frame's p+ ring
# (iovss) at the pad level (Metal1 under the joins, Metal2 over the NWell isolator)
box("M2", 64.40, 88.25, 65.00, 88.85)
box("M2pin", 64.40, 88.25, 65.00, 88.85)
c.shapes(L["M2txt"]).insert(db.DText("iovss_o", 64.70, 88.55))
tap(None, 6.40, 102.525, via1=True)                   # CMA stage's n+ ring (iovdd)
tap(None, 73.95, 102.525, via1=True)                  # CMB stage's n+ ring (mirror image)
for b in ((39.0, 101.97, 42.85, 105.15),              # loads / casc_p
          (7.19, 118.82, 7.82, 122.08), (38.10, 118.82, 42.85, 122.08),      # casc_p / inputs' lower dummy tubs
          (4.13, 146.36, 7.82, 150.20), (38.10, 146.36, 38.82, 150.20),      # inputs' upper dummy tubs / tails
          (36.00, 165.01, 38.82, 169.80),             # tails / bias_tree_p
          (1.80, 146.36, 4.13, 149.27),               # left edge stub's iovdd NWell / inputs' / tails' wells
          (42.80, 168.40, 54.20, 169.90)):            # bias_tree_p / TGP (tongue under bias_tree_n's pins)
    box("NW", *b)
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[1], opt)
print("pwr_f2", c.dbbox())
