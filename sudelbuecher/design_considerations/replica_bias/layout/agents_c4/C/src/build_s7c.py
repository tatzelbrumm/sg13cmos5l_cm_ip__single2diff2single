# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent C (C4): s7_ctrl layout. python3 build_s7c.py <outdir>
# Rows (bottom to top): 7 ls_up_fs (efs_ls_core, mirrored in y, inputs on the bottom edge) | channel C1 (M1 tracks)
# | one row of D's bdp_nand2_hv / bdp_inv_hv / bdp_tg_hv | channel C2 (switch tracks) | top edge: switch pins, en, en_b.
import klayout.db as db, sys, os
REPO = '/home/user/sg13cmos5l_cm_ip__single2diff2single'
OUT = sys.argv[1]
ly = db.Layout(); ly.dbu = 0.001
ly.read(REPO + '/macros/bias_dist_pd/layout/klayout/bias_dist_pd.klay.gds')
ly.read(REPO + '/macros/en_ctrl_3v3/layout/klayout/ls_up_fs.klay.gds')
C = {n: ly.cell(n) for n in ['bdp_nand2_hv', 'bdp_inv_hv', 'bdp_tg_hv', 'efs_ls_core']}
top = ly.create_cell('s7_ctrl')
L = {k: ly.layer(*v) for k, v in dict(act=(1, 0), poly=(5, 0), cnt=(6, 0), m1=(8, 0), m1p=(8, 2), m1t=(8, 25),
                                        v1=(19, 0), m2=(10, 0), m2p=(10, 2), m2t=(10, 25), nw=(31, 0), tgo=(44, 0)).items()}
def box(l, x1, y1, x2, y2):
    top.shapes(L[l]).insert(db.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
def via(cx, cy):
    box('v1', cx - 0.095, cy - 0.095, cx + 0.095, cy + 0.095)
def place(name, x, y, mirror=False):
    t = db.DTrans(db.DTrans.M0 if mirror else db.DTrans.R0, db.DVector(x, y))
    top.insert(db.DCellInstArray(C[name].cell_index(), t))
R = lambda v: round(v * 200) / 200.0   # 5 nm grid
W2 = 0.20                              # M2 stub width (via 0.19, Mn.c 0.005)
TP, TW = 0.39, 0.21                    # M1 track pitch / width

# ---------------- level shifters (bottom row, mirrored: in / out near the top) ----------------
LSH, G, XLS0 = 27.02, 0.40, 0.80
ls_order = [('XL0', 'd0', 'sw', None), ('XL1', 'd1', 'mon', None), ('XL2', 'd2', 'fd', None), ('XL3', 'd3', 'k1', None),
            ('XL4', 'd4', None, 'k0_b'), ('XL5', 'd5', 'ex', None), ('XLE', 'enable', 'en', 'en_b')]
lsx = [R(XLS0 + i * (9.68 + G)) for i in range(7)]
for x in lsx:
    place('efs_ls_core', x, LSH, True)
fy = lambda y: LSH - y   # LS frame -> top frame

# ---------------- logic row ----------------
X0 = 1.00
OFF = {('nand', 'inv'): 1.66, ('inv', 'tg'): 1.38, ('tg', 'tg'): 1.36, ('tg', 'nand'): 1.34, ('inv', 'nand'): 1.36}
pairs = [('V', 'k1', 'k0_b', 'valid_b', 'valid'), ('S', 'sw', 'valid', 's_b', 's'), ('F', 'fd', 'valid', 'f_b', 'f'),
         ('M', 'mon', 'valid', 'm_b', 'm'), ('1', 'f_b', 's_b', 'x1_b', 'x1'), ('2', 'f_b', 's', 'x2_b', 'x2'),
         ('3', 'm', 'f_b', 'x3_b', 'x3')]
groups = [('LD', 'x1', 'ld', [('outp', 'vinp'), ('outn', 'vinn')]), ('LX', 'x2', 'lx', [('outp', 'vinn'), ('outn', 'vinp')]),
          ('SB', 'x3', 'sb', [('outp', 'bus0'), ('outn', 'bus1')]), ('BD', 'f', 'bd', [('bus0', 'vinp'), ('bus1', 'vinn')]),
          ('RC', 'e_b', 'rc', [('vcm_rb', 'vcm_pad'), ('vref_rb', 'vref_pad')])]
need_out = {'valid', 's_b', 's', 'f_b', 'f', 'm', 'x1', 'x2', 'x3', 'e_b'}
seq = []
for n, a, b, yb, y in pairs:
    seq += [('nand', (a, b, yb)), ('inv', (yb, y))]
for n, b, e, tgs in groups:
    seq += [('nand', ('en', b, e + '_b')), ('inv', (e + '_b', e))] + [('tg', (e, e + '_b') + t) for t in tgs]
seq += [('nand', ('ex', 'valid', 'e_b'))]
pos, x, prev = [], X0, None
for k, nets in seq:
    if prev: x = R(x + OFF[(prev, k)])
    pos.append((k, x, nets)); prev = k
row_end = pos[-1][1] + 1.96

above, below = [], []   # C1 stubs: (net, cx, y_from)  [y_from: via centre]
tg_risers = []          # C2: (net, cx)
for i, (k, x, nets) in enumerate(pos):
    if k == 'nand':
        a, b, y = nets
        above += [(a, x + 0.565, 2.115), (b, x + 1.395, 2.115)]
        if y in need_out:
            above.append((y, x + 0.15, 1.945)); YPAD = (x + 0.045, 1.80, x + 0.255, 2.09)
            pos[i] = (k, x, nets, YPAD)
    elif k == 'inv':
        if nets[1] in need_out:
            above.append((nets[1], x + 0.98, 2.045)); pos[i] = (k, x, nets, (x + 0.875, 1.90, x + 1.085, 2.19))
    else:
        tg_risers += [(nets[2], x + 0.15), (nets[3], x + 0.98)]
# en / en_b risers to the top edge, right of the logic row
RX_EN = R(row_end + 1.0); RX_ENB = R(RX_EN + 0.6)

# LS stubs: choose x in the allowed range away from every above stub
def pick(lo, hi, avoid):
    best, bx = -1, None
    c = lo
    while c <= hi + 1e-9:
        d = min([abs(c - a) for a in avoid] + [9])
        if d > best + 1e-9 or (abs(d - best) < 1e-9 and abs(c - (lo + hi) / 2) < abs(bx - (lo + hi) / 2)):
            best, bx = d, c
        c = R(c + 0.05)
    return bx, best
avoid = [a[1] for a in above] + [RX_EN, RX_ENB]
ls_stub = []
for (nm, inp, o, ob), x in zip(ls_order, lsx):
    if o:
        cx, d = pick(x + 6.15, x + 7.9, avoid); below.append((o, cx, fy(2.10))); ls_stub.append((o, cx, 'out', x))
    if ob:
        cx, d = pick(x + 8.86, x + 9.53, avoid); below.append((ob, cx, fy(2.74))); ls_stub.append((ob, cx, 'out_b', x))
above += [('en', RX_EN, None), ('en_b', RX_ENB, None)]

# ---------------- C1 track assignment (left edge with vertical constraints) ----------------
nets1 = sorted(set([a[0] for a in above] + [b[0] for b in below]))
span = {n: [min(s[1] for s in above + below if s[0] == n) - 0.15, max(s[1] for s in above + below if s[0] == n) + 0.15] for n in nets1}
must_below = {n: set() for n in nets1}   # must_below[B] = nets whose tracks must lie below B's
for bn, bx, _ in below:
    for an, ax, _ in above:
        if an != bn and abs(ax - bx) < 0.45: must_below[an].add(bn)
for s1 in above:
    for s2 in above:
        if s1[0] != s2[0] and abs(s1[1] - s2[1]) < 0.41: raise SystemExit('stub clash %s %s' % (s1, s2))
track1, k = {}, 0
while len(track1) < len(nets1):
    ready = sorted([n for n in nets1 if n not in track1 and all(m in track1 and track1[m] < k for m in must_below[n])],
                   key=lambda n: span[n][0])
    if not ready: raise SystemExit('cycle')
    last = -1e9
    for n in ready:
        if span[n][0] >= last + 0.18:
            track1[n] = k; last = span[n][1]
    k += 1
N1 = k
TY0 = R(LSH + 0.18)               # first track bottom (LS vss strip top 27.02)
ty1 = lambda n: TY0 + TP * track1[n]
YL = R(TY0 + TP * N1 + 0.0)       # logic row origin: top track top + 0.18
for n in nets1:
    box('m1', span[n][0], ty1(n), span[n][1], ty1(n) + TW)

# ---------------- logic row instances and glue ----------------
for p in pos:
    k, x, nets = p[:3]
    place({'nand': 'bdp_nand2_hv', 'inv': 'bdp_inv_hv', 'tg': 'bdp_tg_hv'}[k], x, YL)
    if len(p) > 3:
        x1, y1, x2, y2 = p[3]; box('m1', x1, YL + y1, x2, YL + y2)
for i, p in enumerate(pos):
    k, x = p[0], p[1]
    if k == 'nand' and i + 1 < len(pos) and pos[i + 1][0] == 'inv':
        box('m1', x + 1.06, YL + 2.61, x + 2.095, YL + 2.87)          # nand y -> inv a (D's slice)
        if i + 2 < len(pos) and pos[i + 2][0] == 'tg':                # group: D's slice glue, poly bars over both TGs
            xe = pos[i + 3][1] + 0.79
            box('poly', x + 2.0, YL + 2.55, xe, YL + 3.1)              # e_b bridge: inv gate -> TGP gates
            box('poly', x + 2.63, YL + 1.8, xe, YL + 2.3)              # e bar -> TGN gates
            box('cnt', x + 2.7, YL + 2.04, x + 2.86, YL + 2.2)
            box('m1', x + 2.56, YL + 1.99, x + 2.91, YL + 2.25)
# C1 stubs
for n, cx, yv in above:
    yt = ty1(n) + TW / 2
    if yv is None:
        continue
    via(cx, YL + yv); via(cx, yt)
    box('m2', cx - W2 / 2, yt - 0.145, cx + W2 / 2, YL + yv + 0.145)
for n, cx, yv in below:
    yt = ty1(n) + TW / 2
    via(cx, yv); via(cx, yt)
    box('m2', cx - W2 / 2, yv - 0.145, cx + W2 / 2, yt + 0.145)

# ---------------- C2 (switch tracks) ----------------
cnt = {}
for n, cx in tg_risers: cnt[n] = cnt.get(n, 0) + 1
nets2 = sorted([n for n in cnt if cnt[n] > 1])
span2 = {n: [min(c for m, c in tg_risers if m == n) - 0.15, max(c for m, c in tg_risers if m == n) + 0.15] for n in nets2}
track2, k = {}, 0
while len(track2) < len(nets2):
    last = -1e9
    for n in sorted([n for n in nets2 if n not in track2], key=lambda n: span2[n][0]):
        if span2[n][0] >= last + 0.18: track2[n] = k; last = span2[n][1]
    k += 1
N2 = k
TY2 = R(YL + 4.90 + 0.18)
ty2 = lambda n: TY2 + TP * track2[n]
H = R(TY2 + TP * N2 + 0.30)
for n in nets2:
    box('m1', span2[n][0], ty2(n), span2[n][1], ty2(n) + TW)
pins = []
pinx = {n: max(c for m, c in tg_risers if m == n) for n in cnt}
for n, cx in tg_risers:
    box('m1', cx - 0.105, YL + 4.13, cx + 0.105, YL + 4.42); via(cx, YL + 4.275)
    if pinx[n] == cx:
        yt = H
        pins.append((n, 'Metal2', (cx - 0.145, H - 0.40, cx + 0.145, H)))
    else:
        yt = ty2(n) + TW / 2 + 0.145
    if n in nets2: via(cx, ty2(n) + TW / 2)
    box('m2', cx - 0.145, YL + 4.13, cx + 0.145, yt)
for n, cx in [('en', RX_EN), ('en_b', RX_ENB)]:
    yt = ty1(n) + TW / 2; via(cx, yt)
    box('m2', cx - W2 / 2, yt - 0.145, cx + W2 / 2, H)
    pins.append((n, 'Metal2', (cx - W2 / 2, H - 0.40, cx + W2 / 2, H)))

# ---------------- LS inputs (bottom edge), LS stubs, supplies ----------------
for (nm, inp, o, ob), x in zip(ls_order, lsx):
    cx = x + 0.395; yv = fy(2.145); via(cx, yv)
    box('m2', cx - W2 / 2, 0, cx + W2 / 2, yv + 0.145)
    pins.append((inp, 'Metal2', (cx - W2 / 2, 0, cx + W2 / 2, 0.40)))
for a, b in zip(lsx[:-1], lsx[1:]):
    box('m1', a + 9.38, fy(0.30), b + 0.30, fy(0.0))        # vss strips
    box('m1', a + 9.06, fy(26.40), b + 0.62, fy(26.10))      # vddh rails
    box('nw', a + 9.68, fy(27.02), b, fy(2.55))              # one NWell
W = R(lsx[-1] + 9.68 + 0.64)
# vss: left M1 strap from the LS vss strip to the logic row's vss strip
box('m1', 0, fy(0.30), lsx[0] + 0.30, fy(0.0))
box('m1', 0, YL, X0 - 0.105, YL + 0.30)
box('m1', 0, fy(0.30), 0.30, YL + 0.30)
pins.append(('vss', 'Metal1', (0, fy(0.30), 0.30, YL + 0.30)))
# vddh: right M1 strap from the LS vddh rail to the logic row's vdd strip
box('m1', lsx[-1] + 9.06, fy(26.40), W, fy(26.10))
box('m1', row_end - 0.10, YL + 4.60, W, YL + 4.90)
box('m1', W - 0.30, fy(26.40), W, YL + 4.90)
pins.append(('vddh', 'Metal1', (W - 0.30, fy(26.40), W, YL + 4.90)))
box('tgo', 0, 0, W, H)   # one thick-gate-oxide region over the whole cell (all devices hv)
for n, lay, (x1, y1, x2, y2) in pins:
    l = 'm1' if lay == 'Metal1' else 'm2'
    box(l + 'p', x1, y1, x2, y2)
    top.shapes(L[l + 't']).insert(db.DText(n, db.DTrans(db.DVector((x1 + x2) / 2, (y1 + y2) / 2))))
# drop everything not under s7_ctrl
for ci in [c.cell_index() for c in ly.top_cells() if c.name != 's7_ctrl']:
    ly.prune_cell(ci, -1)
os.makedirs(OUT, exist_ok=True)
ly.write(OUT + '/s7_ctrl.gds')
with open(OUT + '/s7_ctrl_pins.txt', 'w') as f:
    f.write('# s7_ctrl pins: name layer x1 y1 x2 y2 (um, cell origin at lower left; bbox 0 0 %.3f %.3f)\n' % (W, H))
    for n, lay, b in sorted(pins, key=lambda p: p[0]):
        f.write('%-9s %-7s %8.3f %8.3f %8.3f %8.3f\n' % ((n, lay) + tuple(b)))
print('W x H = %.3f x %.3f um; C1 tracks %d, C2 tracks %d, YL %.3f, row_end %.3f' % (W, H, N1, N2, YL, row_end))
print('LS stubs', ls_stub)
