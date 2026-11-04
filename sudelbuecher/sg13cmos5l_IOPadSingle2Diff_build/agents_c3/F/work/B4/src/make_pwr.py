# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B: pwr_f, the block's supply taps and NWell bridges, in pad coordinates (after C2 F2's make_pwr.py).
    python3 make_pwr.py <out.gds>
Tap: Metal2 pad 0.80 x 0.60 with two Via2 (Vn_a 0.19, Vn_b 0.22, Vn_c1 0.05) and a Metal3 pad inside the ring rail
above (template Metal3: iovss 7..32.5, 34.5..60, 126..134; iovdd 66..91.5, 93.5..119). The pad carries a Metal2 text
with its supply group; the router joins the group's cell pins (rings, ties) to it. One tap per group, so the tail
source bus and the sink source bus each tap the ring at one point (layout_primitives.md section 6).
NWell bridges (NW_a 0.62 wide at least; NW_b1 1.80 to the active tubs' wells kept): the tail rows' wells to the
inputs' all-vdd dummy tubs at both row ends (one iovdd well for the front end).
Tail-to-tub links (drawn here, not by the router: the 12 sa / sb links of equal shape, rule 2): each tail drain pin
(Metal2, 1.11 wide, on the tail row's edge facing the tubs) to its tub's source pin (Metal1 0.67 x 0.30 on the
inputs' edge): the tub pin runs on in Metal1 1.05 um into the junction channel (the inputs' own x / y tracks lie on
Metal2 over the pin), one Via1, a Metal2 jog (0.39 high) to the tail pin's centre and a 0.40 wide Metal2 run onto the
tail pin. Offsets tub - tail: -2.125 + 0.85 k um (tub pitch 6.10, tail pitch 5.25); all twelve links of a junction have
the same shape, mirrored about the tubs' centre line (y 135.62) between the two junctions."""
import sys

import klayout.db as db

ly = db.Layout()
ly.dbu = 0.001
c = ly.create_cell('pwr_f')
L = {k: ly.layer(*v) for k, v in {'M1': (8, 0), 'M1txt': (8, 25), 'M3txt': (30, 25), 'V1': (19, 0), 'M2': (10, 0), 'M2pin': (10, 2), 'M2txt': (10, 25), 'V2': (29, 0), 'M3': (30, 0),
                                  'NW': (31, 0)}.items()}


def box(k, x0, y0, x1, y1):
    c.shapes(L[k]).insert(db.DBox(round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)))


TAPS = [('iovss_sk', 12.50, 32.15),    # sinks' ring (sink source bus), under iovss 7..32.5
        ('iovss_cn', 39.60, 50.00),    # casc_n's ring, channel C9, under iovss 34.5..60
        ('iovdd_op', 72.95, 70.00),    # casc_p, loads, CYC drains; right pocket strip, under iovdd 66..91.5
        ('iovdd_t', 54.30, 112.00),    # both tail rows (tail source bus) + the inputs' dummy tubs, under iovdd 93.5..119
                                       # (stage B2: moved from x 51.50, out of the pad corridor)
        ('iovss_m', 65.50, 126.50),    # sinks_cmfb, rhigh, tree_n, cload; on rhigh's ring, under iovss 126..134
        ('iovdd_tp', 76.95, 117.50)]   # tree_p, pd_p; in the right edge reserve (Metal2 / Via2 / Metal3 only)
for n, x, y in TAPS:
    for k in ('M2', 'M3', 'M2pin'):
        box(k, x - 0.40, y - 0.30, x + 0.40, y + 0.30)
    for dx in (-0.205, 0.205):
        box('V2', x + dx - 0.095, y - 0.095, x + dx + 0.095, y + 0.095)
    c.shapes(L['M2txt']).insert(db.DText(n, x, y))
# rail tie: the two Metal3 iovdd rails (66..91.5, 93.5..119) meet in the pad only through the IO ring; inside this cell
# they are two nets, and the front end taps the upper one, the protection and the output stage the lower one. One
# Metal2 strap in the right edge reserve (Metal2 / Via2 only there) with two Via2 pairs joins them.
box('M2', 76.55, 90.20, 77.35, 95.20)
for y in (90.80, 94.60):
    box('M3', 76.55, y - 0.30, 77.35, y + 0.30)
    for dx in (-0.205, 0.205):
        box('V2', 76.95 + dx - 0.095, y - 0.095, 76.95 + dx + 0.095, y + 0.095)
for b in ((5.00, 119.00, 8.50, 123.10), (47.70, 119.00, 49.20, 123.10),     # tails_lo / lower dummy tubs
          (5.00, 148.10, 8.50, 152.20), (47.70, 148.10, 49.20, 152.20)):    # upper dummy tubs / tails_hi
    box('NW', *b)
# tail-to-tub links: inputs at (4.30, 122.40), tails_lo (M0) at (4.37, 110.24), tails_hi at (4.37, 151.84)
LO = ['sb_A2', 'sa_F1', 'sa_F2', 'sb_A1', 'sb_M1', 'sa_M2']      # tails_lo's pins = the lower tubs' source pins
HI = ['sa_A1', 'sb_F2', 'sb_F1', 'sa_A2', 'sa_M1', 'sb_M2']      # tails_hi's pins = the upper tubs' source pins
for k in range(6):
    xt = 4.37 + 8.915 + 5.25 * k + 0.555          # tail drain pin centre
    xi0 = 4.30 + 7.08 + 6.10 * k                  # tub source pin, left edge (0.67 wide)
    xi = xi0 + 0.335
    for pin_edge, y_far, yv, ytail, net in ((122.40, 121.40, 121.57, 119.20, LO[k]), (148.84, 149.84, 149.48, 152.04, HI[k])):
        up = y_far > pin_edge
        box('M1', xi0, min(pin_edge - 0.05, y_far) if not up else pin_edge - 0.05, xi0 + 0.67,
            pin_edge + 0.05 if not up else y_far)
        box('V1', xi - 0.095, yv, xi + 0.095, yv + 0.19)
        ym0, ym1 = yv - 0.10, yv + 0.29
        box('M2', min(xi, xt) - 0.20, ym0, max(xi, xt) + 0.20, ym1)
        box('M2', xt - 0.20, min(ym0, ytail), xt + 0.20, max(ym1, ytail))
        # pin box on the straight vertical part (a text alone would take the bounding box of the whole L-shaped
        # link as its pin, including the empty corner): the router then sees one terminal group per net
        yp0, yp1 = (ym1, ytail) if ytail > ym1 else (ytail, ym0)
        box('M2pin', xt - 0.20, yp0, xt + 0.20, yp1)
        c.shapes(L['M2txt']).insert(db.DText(net, xt, round((yp0 + yp1) / 2, 3)))
        c.shapes(L['M1txt']).insert(db.DText(net, xi, (pin_edge + y_far) / 2))
# ---- stage B2 (Christoph, 2026-11-04): the pad net up the middle of the cell, with a shield on each side --------------
# Path (centre line): the template's pad pin (M2 x 20.40..21.02, top 31.18) -> M2 up channel C1 between sinks and casc_n
# (x 21.715) -> M2 right in the gap C3a under tails_lo (y 107.85) -> M2 up beside tails_lo's right end (x 50.85) ->
# Via2 -> M3 left in the rail gap 119..126 (y 121.00; every M3 shape >= 0.5 from the rails at 119 and 126, Christoph's
# "well clear") -> Via2 + Via1 -> M1 up the 1.80 um well gap between tub columns 6 and 7 (x 46.39) -> Via1 onto the
# inputs' vin track (M2, y 136.80). The tails rows block every straighter path (their gates fill them; the M3 above
# them is the iovdd rail).
# Shields: 0.30 wide, 0.40 from the pad line on both sides, on iovss (the substrate and the protection's ground, the
# pad signal's own reference). Both shields meet at the pad end (an M1 bridge under the pad's M2) and are tied there
# to the M3 iovss rail 7..32.5 by one Via2: one end only, so no supply current flows in them (no loop, no drop
# along the pad line).
W, D = 0.30, 0.70                              # line width, centre spacing pad - shield
h = W / 2


def hseg(k, y, x0, x1):
    box(k, min(x0, x1) - h, y - h, max(x0, x1) + h, y + h)


def vseg(k, x, y0, y1):
    box(k, x - h, min(y0, y1) - h, x + h, max(y0, y1) + h)


def via(k, x, y):
    box(k, x - 0.095, y - 0.095, x + 0.095, y + 0.095)


def path(segs):
    for k, a, b in segs:
        (hseg if a[1] == b[1] else vseg)(k, *((a[1], a[0], b[0]) if a[1] == b[1] else (a[0], a[1], b[1])))


XC, YH, XV, YM, XG, YV = 21.715, 107.85, 50.85, 121.00, 46.39, 136.80
box('M2', 20.40, 30.88, XC + h, 31.48)                                    # onto the pad pin's top
for off in (0.0, -D, D):                                                  # pad, left shield, right shield
    xc, yh, xv, ym, xg = XC + off, YH - off, XV + off, YM + off, XG + off   # left of travel: -x, +y, -x, -y, -x
    ys = 31.18 if off == 0 else (32.05 if off < 0 else 31.70)
    path([('M2', (xc, ys), (xc, yh)), ('M2', (xc, yh), (xv, yh)), ('M2', (xv, yh), (xv, ym)),
          ('M3', (xv, ym), (xg, ym)), ('M1', (xg, ym), (xg, YV + (0.0 if off == 0 else -0.2)))])
    via('V2', xv, ym)                                                     # M2 -> M3
    via('V2', xg, ym)                                                     # M3 -> M2 landing -> M1
    ext = 0.20 if off >= 0 else -0.20                                     # M2 landing 0.30 x 0.50 (Mn_d 0.144),
    box('M2', xg - h, min(ym - h, ym - h + ext), xg + h, max(ym + h, ym + h + ext))   # away from its neighbours
    via('V1', xg, ym)
via('V1', XG, YV)                                                         # onto the vin track
for xs in (XC - D, XC + D):                                               # shield bridge under the pad, M1
    via('V1', xs, 32.05)
box('M1', XC - D - h, 32.05 - h, XC + D + h, 32.05 + h)
box('M3', XC + D - 0.20, 31.50, XC + D + 0.20, 31.90)                     # shield tie: Via2 into iovss 7..32.5
via('V2', XC + D, 31.70)
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[1], opt)
print('pwr_f', c.dbbox())
