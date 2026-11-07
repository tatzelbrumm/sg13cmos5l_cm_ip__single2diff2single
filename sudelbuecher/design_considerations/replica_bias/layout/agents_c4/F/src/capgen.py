# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): the bypass capacitors of pad_ref_rb as filler blocks.
    python3 capgen.py <inputs dir> <rb_place.py> <out dir>    ->  <out dir>/rb_caps.gds / .cdl
Each block of rb_place.CAPS = (cell name, net, rows, cols, W, L): rows x cols hv NMOS capacitors W x L (W along x),
gate = net, S = D = B = vss. The code is agent N's bypass() (inputs/N/build_rb_n.py, read and executed here, its
library part unchanged) with the unit's 12 um turned into W and L: the same finger (SG13_dev nmosHV turned R270), gate
column on one side, columns in facing pairs, rows 0.21 apart (Act.b) with an M1 vss bus between them, closed p+ ring,
one ThickGateOx; the gate bus on Metal2 at the top edge (vcm) or the bottom edge (vref)."""
import os
import sys

I, PLACE, OUT = sys.argv[1:4]
src = open(os.path.join(I, 'N', 'build_rb_n.py')).read()
lib = src[:src.index('# The cells')]
lib = lib[:lib.rindex('# ====')]                         # the library part: N's text up to its cell section
g = {'__name__': 'nlib'}
exec(compile(lib, 'build_rb_n.py (library part)', 'exec'), g)
pl = {}
exec(open(PLACE).read(), pl)
Cell, g5, ly, pya = g['Cell'], g['g5'], g['ly'], g['pya']


def capblock(name, net, rows, cols, W, L, lab):
    """N's bypass() for rows x cols units of W x L on one net (see N's docstring for the construction)."""
    c = Cell(name)
    H = g5(L + 0.68)
    PY = g5(H + 0.21)
    xs, x = [], 0.0
    for j in range(cols):                                # (Activ x0, mirrored, column center, fill)
        if j % 2 == 0:
            xs.append((x, False, g5(x + W + 0.33), (g5(x + W + 0.10), g5(x + W + 0.60))))
        else:
            xs.append((g5(x + W + 1.38), True, g5(x + W + 1.05), (g5(x + W + 0.78), g5(x + W + 1.28))))
            x = g5(x + 2 * W + 1.38 + 0.54)
    xr = max(xs[-1][0] + W, xs[-1][3][1]) + 0.73
    yr = (rows - 1) * PY + H + 0.51
    c.ring(-0.73, -0.51, xr, yr)
    yt, yb0 = yr + 0.03, -0.54
    seg = []
    for j, (x0, mx, xc, fill) in enumerate(xs):
        for i in range(rows):
            yb = g5((rows - 1 - i) * PY)
            dv = c.mos(lab, W, L, x0, yb, 'vss', net, 'vss', mx=mx)
            c.gate_col(xc, [dv['gate']], yb + 0.36, yb + L + 0.32, fill)
            yv = yb + L + 0.1 if net == 'vcm' else yb + 0.58
            c.via(xc, yv)
            seg.append((xc, yv))
            if i == 0:
                c.plate(dv, 'top')
            if i == rows - 1:
                c.plate(dv, 'bot')
    for r in range(rows - 1):
        c.box('M1', -0.71, r * PY + L + 0.50, xr - 0.02, r * PY + PY + 0.36 - 0.18)
    yedge = yt if net == 'vcm' else yb0
    xn = sorted({s[0] for s in seg})
    for xc in xn:
        yv = [s[1] for s in seg if s[0] == xc]
        c.box('M2', xc - 0.145, min(yv) - 0.145 if net == 'vcm' else yedge,
              xc + 0.145, yedge if net == 'vcm' else max(yv) + 0.145)
    y0 = yedge - 0.29 if net == 'vcm' else yedge
    c.box('M2', xn[0] - 0.145, y0, xn[-1] + 0.145, y0 + 0.29)
    c.pin('M2', net, xn[0] - 0.145, y0, min(xn[0] + 0.355, xn[-1] + 0.145), y0 + 0.29)
    c.pin('M1', 'vss', -0.71, -0.49, -0.21, -0.23)
    c.tgo()
    c.info = '%d x %s %gu x %gu on %s, %d rows x %d columns' % (rows * cols, lab, W, L, net, rows, cols)
    return c


cells = [capblock(*b) for b in pl['CAPS']]
os.makedirs(OUT, exist_ok=True)
os.chdir(OUT)
opt = pya.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write('rb_caps.gds', opt)
with open('rb_caps.cdl', 'w') as f:                     # as N's write(): one line per finger, bulk = vss
    f.write('* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n'
            '* rb_caps.cdl: reference netlists of rb_caps.gds (capgen.py, Claude, agent F, C4).\n')
    for k in cells:
        nets = sorted({p[0] for p in k.pins})
        f.write('\n.SUBCKT %s %s\n%s\n.ENDS %s\n' % (k.name, ' '.join(nets), '\n'.join(k.cdl), k.name))
for k in cells:
    b = k.c.dbbox()
    print('%-10s %6.2f x %6.2f um  %7.1f um2  %s' % (k.name, b.width(), b.height(), b.width() * b.height(), k.info))
