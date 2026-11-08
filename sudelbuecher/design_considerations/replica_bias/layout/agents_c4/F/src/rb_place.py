# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent F (C4), v2 (after Christoph's review): the placement of pad_ref_rb (read by rb_cfg.py, capgen.py,
# make_frame.py, render.py, compose_cdl_rb.py). Rigid rows packed by signal flow, the bypass capacitors as filler.
# Rows bottom to top:
#   capr (vref capacitors, full width) | rb_casc (R180: vref top right, xp top left, vbnc / vdd right edge)
#   rb_tree_n (R0, pins up, en_3v3 on the left edge) | rb_tails (M0) | rb_tree_p (M0, abutting: vbp stubs meet)
#   rb_mirror (M90) + capm (vcm) on it | rb_avg (R0) | rb_tubs (R0, D MR BA BB D, over the tails) | capt (vcm)
#   capv (vcm) | rb_cload (M0, pins down onto BB's vcm)
# Coordinates: lower left of each oriented bounding box (P cells: their NWell; N cells and capacitors: ThickGateOx).
X0 = 0.9                                  # left channel: input pins (en_3v3, en_3v3_b, iref), vssh, vddh
# capacitor blocks (name, net, rows, cols, W, L, label): capgen.py. Gate area per node (um2):
#   vcm : CB 144 (rb_cload) + capv 2 x 19.24 x 12.66 + capm 2 x 8.18 x 3.25 + capt 1 x 2.9 x 12.4 = 144 + 576.3
#   vref: CBR 144 (rb_cload) + capr 2 x 34.1 x 16.9 = 144 + 1152.6
CAPS = [('capr', 'vref', 1, 2, 34.1, 16.9, 'CBR'), ('capm', 'vcm', 1, 2, 8.18, 3.25, 'CBM'),
        ('capt', 'vcm', 1, 1, 2.9, 12.4, 'CBM'), ('capv', 'vcm', 1, 2, 19.24, 12.66, 'CBM')]
H_CAPR = 16.9 + 2.24
Y_CAPR = 0.15                             # bottom margin (router edge track)
Y_CASC = Y_CAPR + H_CAPR                  # abutting: one ThickGateOx, rings 0.54 apart
Y2 = Y_CASC + 12.37 + 1.5                 # channel: vref, xp, vbnc, vdd
Y3 = Y2 + 9.16 + 3.23                     # tails-tubs channel; tree_p's top 1.80 below the tubs (NW.b1)
T = X0 + 34.01 + 0.86 + 2.345             # rb_tubs x0: tails start 2.345 left of it (TR under MR, BT under BA / BB)
Y_AVG_TOP = Y3 + 14.66
W = X0 + 34.01 + 0.86 + 24.19 + 12.94 + 0.9
PLACE = [
    ('frame', 'frame_f', 'R0', 0.0, 0.0),
    ('capr', 'capr', 'R0', X0, Y_CAPR),                          # vref bus on its bottom edge
    ('casc', 'rb_casc', 'R180', X0, Y_CASC),
    ('treen', 'rb_tree_n', 'R0', X0, Y2),                        # pins up (gh, xp, vbp, vref, iref); en_3v3 left
    ('tails', 'rb_tails', 'M0', T - 2.345, Y2),                  # ts / bt up; vbp stub right
    ('treep', 'rb_tree_p', 'M0', T - 2.345 + 24.19, Y2 + 0.22),  # vbp stub left (abuts), vbnc down, TGP up
    ('tubs', 'rb_tubs', 'R0', T, Y3),                            # ts / bt / bd down, gh / m / vcm up
    ('avg', 'rb_avg', 'R0', T - 2.5 - 8.19, Y3),                 # gh top, m sides, xp bottom
    ('mirror', 'rb_mirror', 'M90', X0, Y3),                      # bd / vcm on its right edge, high
    ('capm', 'capm', 'R0', X0, Y3 + 9.17),                       # on the mirror (abutting)
    ('capt', 'capt', 'R0', T + 28.70 + 0.9, Y3),                 # right of the tubs
    ('capv', 'capv', 'R0', X0, Y_AVG_TOP + 1.0),                 # vcm bus on its top edge
    ('cload', 'rb_cload', 'M0', W - 0.6 - 29.56, Y3 + 14.64),    # on capt (abutting); vcm / en_3v3_b / vref down
]
H = Y_AVG_TOP + 1.0 + 12.66 + 2.24 + 0.15
VCM_Y = Y3 + 8.7                          # vcm pin on the right edge: the D2S vref (slot y 223.3) straight out
SLOT_Y0 = 223.315 - VCM_Y                 # so the cell's lower left sits at (535.0 - W, SLOT_Y0) in slot7
# pins: (net, side, lo, hi) along the edge
PINS = [('vref', 'right', 9.8, 10.2), ('vcm', 'right', VCM_Y - 0.2, VCM_Y + 0.2),
        ('en_3v3', 'left', Y2 + 3.9, Y2 + 4.3), ('en_3v3_b', 'left', Y2 + 5.0, Y2 + 5.4),
        ('iref', 'left', Y2 + 6.1, Y2 + 6.5), ('vssh', 'left', 9.8, 10.2), ('vddh', 'left', Y3 - 2.0, Y3 - 1.6)]
# rb_casc's vdd (its band's vdd track and the three dummy tracks tied to it, pin on its right edge in R180, frame
# y 5.83..6.12 -> Y_CASC + 12.37 - 1.21 - y): not routed; a router landing there fills the gaps between those tracks
# (same net) into a plate wider than Mn.e_w next to vbnc (M2.e, measured in v1 and v2a). Instead F draws a strap of
# the track's width (after routing, finalize.py) from the pin stub to a vddh terminal box in the right channel.
_vy0, _vy1 = Y_CASC + 12.37 - 1.21 - 6.12, Y_CASC + 12.37 - 1.21 - 5.83
NETMAP = {'casc': {'vdd': 'vddh_casc'}}
FPINS = [('vddh', (X0 + 71.72 + 0.4, _vy0, X0 + 71.72 + 0.8, _vy1))]
STRAPS = [(X0 + 71.72 - 0.25, _vy0, X0 + 71.72 + 0.5, _vy1)]
EXTRA_KEEPOUT = [('M2', (X0 + 71.72 - 0.25, _vy0 - 0.3, X0 + 71.72 + 0.4, _vy1 + 0.3))]
ROUTE_ORDER_PLACE = []
