# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Stage A placement table (F, C3). Coordinates in um: x / y of the placed bounding box's lower-left corner.
Bounding boxes: P cells = their NWell; N cells = ThickGateOx (Activ + TGO.a 0.27) or their edge pins.
Orientations are KLayout's (R90 = 90 deg counterclockwise; M0 = mirror at the x axis, M90 = at the y axis).
"""
# free region and keep-outs of template version 4 (fit_s2d.py REGION / OBST, refined):
#  - 1.5 um from the protection's outer rings (brief rule 5): CN NWell top 30.10 -> 31.6
#  - 1.5 um around the pad pin strap (M2 x 20.40-21.02, top 31.18)
#  - RN / RP EXTBlock (x 38.6-41.3, to 36.68) and DP / CP / iovdd bar (to 41.6): as fit_s2d.py
#  - the iovdd risers' x ranges (42.6-45.2, 75.5-78.4) up to y 73.05, 0.25 um M2 margin (M2.b 0.21)
REGION = (1.8, 31.6, 78.2, 180.0)
KEEP_OUT = [(0.0, 0.0, 39.45, 31.6), (18.9, 0.0, 22.52, 32.68), (37.0, 0.0, 42.8, 38.2), (40.3, 0.0, 80.0, 43.1),
            (42.35, 0.0, 45.45, 73.05), (75.25, 0.0, 80.0, 73.05)]

# (cell, orientation, x0, y0, block P/N/R, label)
PLACE = [
    # left pocket: the NMOS fold, next to each other; the vin channel x 18.31-22.6 between them, straight above
    # the pad pin strap
    ('sinks_6x6_s2d_c3', 'R180', 1.80, 31.70, 'N', 'sinks'),          # pins (y / vbn / x) at the top center
    ('s2d_casc_n_c3', 'R270', 22.60, 32.70, 'N', 'casc_n'),           # band + x / y pins at the top
    # right pocket: the PMOS output stage, one NWell (abutted), pins at the top
    ('s2d_casc_p_c3', 'R270', 45.50, 45.60, 'P', 'casc_p'),           # band voutp / vcmfb / voutn + lp / ln / dd on top
    ('s2d_loads_c3', 'R270', 58.31, 45.60, 'P', 'loads'),             # abuts casc_p: NWells merge
    # input group: each tail row faces its tub row (column map aligned), R beside the tubs' middle
    ('s2d_tails_lo_f', 'M0', 4.37, 110.24, 'P', 'tails_lo'),          # drains up, onto the lower tubs' sources
    ('s2d_inputs_c3', 'R0', 4.30, 122.40, 'P', 'inputs'),
    ('s2d_tails_hi_f', 'R0', 4.37, 151.84, 'P', 'tails_hi'),          # drains down, onto the upper tubs' sources
    ('s2d_rhigh_c3', 'R90', 55.50, 126.00, 'R', 'rhigh'),              # pins on the left edge; pin bank centered on the tubs
    ('s2d_sinks_cmfb_c3', 'R0', 61.69, 91.25, 'N', 'sinks_cmfb'),      # pins (yc / vbn / xc) at the bottom center
    # bias tree: beside tails_hi (vbp) and next to the core-side pins (iref, en_3v3, en_3v3_b)
    ('bias_tree_noab_n_c3', 'R0', 53.90, 152.30, 'N', 'tree_n'),
    ('bias_tree_noab_p_c3', 'R0', 60.00, 164.30, 'P', 'tree_p'),
    # top band: the load capacitors and the PMOS output ties, next to outp / outn
    ('s2d_cload_c3', 'R0', 2.30, 162.50, 'N', 'cload'),
    ('s2d_pd_p_c3', 'R0', 33.00, 172.30, 'P', 'pd_p'),
]
# reserved M1 / M2 wiring channels (x0, y0, x1, y1, name); widths: nets x M2 pitch 0.48 (0.26 track + M2.b 0.21,
# P's TP) unless stated
CHANNELS = [
    (18.31, 32.70, 22.60, 110.24, 'C1 vin (+ y)'),
    (1.80, 82.70, 4.30, 176.74, 'C2 output trunk, x / y, vref / vcm'),
    (4.30, 105.44, 61.69, 110.24, 'C3a'),
    (36.97, 97.83, 61.69, 105.44, 'C3b band, x y xc yc, vbnc'),
    (58.31, 88.79, 61.69, 122.40, 'C4 lp ln dd, xc yc'),
    (4.30, 119.40, 55.50, 122.40, 'C5 tails_lo-tubs + R'),
    (4.30, 148.84, 53.90, 151.84, 'C5 tubs-tails_hi + R'),
    (51.88, 119.40, 55.50, 151.84, 'C6 R feeders'),
    (75.59, 91.25, 78.20, 164.30, 'C7 vbn vbnc vbpc'),
    (1.80, 176.74, 78.20, 180.00, 'C8 core-side pins'),
    (36.97, 38.20, 42.35, 97.83, 'C9 casc_n long side'),
]
