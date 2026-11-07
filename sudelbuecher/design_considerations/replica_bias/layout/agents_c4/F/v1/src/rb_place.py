# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent F (C4): the placement of pad_ref_rb (read by rb_cfg.py, make_frame.py, render.py).
# Rows bottom to top: bypass_rb_f (2 x 6) | rb_casc | rb_tree_p + rb_tails | rb_mirror, rb_tubs, rb_avg | rb_cload, rb_tree_n.
# Coordinates: lower left of each oriented bounding box (P cells: their NWell; N cells: ThickGateOx).
CL = 4.0            # left channel: vssh / vddh rails + vbnc, casc's vdd tie
T = CL + 19.75 + 3.0  # rb_tubs x0: mirror, 3.0 um gap (vcm, ni, en_3v3_b, iref down to TGP), tubs
Y_BYP = 1.0
H_BYP = 27.13                       # bypass_rb_f: 2 rows x 6 columns (build_f_cells.py)
Y_CASC = Y_BYP + H_BYP + 2.0     # bypass-casc channel 2.0: vcm / vref buses out, vssh
Y_TAILS = Y_CASC + 12.37 + 2.5
Y_TUBS = Y_TAILS + 9.16 + 3.4         # tails-tubs channel 3.4 (ts, bt, bd; tree_p's top 1.97 below the tubs: NW.b1)
PLACE = [
    ('frame', 'frame_f', 'R0', 0.0, 0.0),
    ('byp', 'bypass_rb_f', 'R0', CL, Y_BYP),
    ('casc', 'rb_casc', 'M0', CL, Y_CASC),                       # vref top left, xp top right, vbnc / vdd left
    ('tails', 'rb_tails', 'R180', T + 6.855, Y_TAILS),           # ts / bt up under MR / BA-BB; vbp stub left
    ('treep', 'rb_tree_p', 'R180', T + 6.855 - 12.94, Y_TAILS + 0.22),   # abuts tails: vbp stubs meet, one NWell
    ('tubs', 'rb_tubs', 'M90', T, Y_TUBS),                       # D BB BA MR D; ts / bt / bd down, gh / m / vcm up
    ('mirror', 'rb_mirror', 'R180', CL, Y_TUBS - 1.0),           # bd / vcm on its right edge, low
    ('avg', 'rb_avg', 'R0', T + 28.70 + 2.5, Y_TUBS),            # gh top, m sides, xp bottom
    ('cload', 'rb_cload', 'M0', CL, Y_TUBS + 11.97 + 2.0),       # vcm / en_3v3_b / vref down
    ('treen', 'rb_tree_n', 'R180', T + 10.38, Y_TUBS + 14.66 + 2.0),   # pins down: gh over tubs' gh; en_3v3 right
]
W = CL + 79.22 + 2.0
H = Y_TUBS + 11.97 + 2.0 + 14.24 + 0.5
PORT_P = 1.08                                   # port pitch: 4 router tracks (0.27)
PORT_Y = Y_TUBS + 14.66 + 2.0 + 5.595 - 2 * PORT_P   # en_3v3 level of tree_n's right edge, minus two port pitches,
PORT_Y = 0.265 + 0.27 * round((PORT_Y - 0.265) / 0.27)  # on a router track (first track 0.12 + 0.145 above y 0)
# rb_casc (M0) vdd pin: frame y 5.83..6.12 -> Y_CASC + 11.16 - y; strap from the vddh rail (x 1.8..2.8) to the pin stub
STRAPS = [(2.6, Y_CASC + 11.16 - 6.12, CL + 0.25, Y_CASC + 11.16 - 5.83)]
NETMAP = {'casc': {'vdd': 'vddh_casc'}}     # drawn, not routed
EXTRA_KEEPOUT = [('M2', (s[0] - 0.4, s[1] - 0.5, s[2] + 0.4, s[3] + 0.5)) for s in STRAPS]
ROUTE_ORDER_PLACE = []
