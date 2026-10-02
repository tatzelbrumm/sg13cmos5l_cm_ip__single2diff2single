#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Draw the cell schematics of improvements/xschem/ from ../../sim/*.spice: unit_r, unit_r2,
unit_t, unit_w, unit_q (with their symbols), d2s_mpdda, d2s_mpdda_flat, d2s_mpdda_bias_flat,
d2s_lc2, d2s_lc2_nc, d2s_bias_lp and the fixture d2s_mpdda_biased. This is how the first drafts
were made; the sheets in improvements/xschem/ have been edited by hand since, so the output goes
to a directory of its own unless --overwrite is given.
Parameters are frozen at the .subckt defaults: lcas=3, wc=lc=16u, rl=50.6u (unit_r2),
iab=5u, ibnc=2u, wdp=6.66u, wdn=3.8u. The top-level symbols copy the hand-checked
../../../xschem/d2s_miller.sym, d2s_bias.sym and d2s_miller_biased.sym.

    python3 gen_cells.py OUTDIR [--overwrite]      (needs $PDK_ROOT; PDK defaults to ihp-sg13cmos5l)
then  python3 gen_testbenches.py OUTDIR  for the tb_*.sch, and check with xschem / check_xschem.py.
"""
import os, re, shutil, sys
from xsheet import Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
XSDIR = os.path.dirname(HERE)                                        # improvements/xschem
REF = os.path.join(XSDIR, '..', '..', 'xschem')                      # class_ab_pad_driver/xschem


def out_dir():
    """output directory from the command line; the hand-edited sheets are not overwritten by default"""
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        raise SystemExit(__doc__)
    out = os.path.abspath(args[0])
    os.makedirs(out, exist_ok=True)
    if os.path.samefile(out, XSDIR) and '--overwrite' not in sys.argv:
        raise SystemExit(f'{out} holds the hand-edited sheets: write to another directory, or add --overwrite')
    return out


OUT = out_dir()
P, N = 'sg13_hv_pmos', 'sg13_hv_nmos'
report = []


def save(sh, name):
    err, cross = sh.write(os.path.join(OUT, name + '.sch'))
    report.append((name, err, cross))


# ======================================================================== symbols
def unit_sym(name, desc):
    pins = [('x', -40, 80, 'out', 'b'), ('y', 0, 80, 'out', 'b'), ('gp', -100, -20, 'in', 'l'),
            ('gn', -100, 20, 'in', 'l'), ('vdd', -40, -80, 'inout', 't'), ('vss', 40, 80, 'inout', 'b'),
            ('vbp', 40, -80, 'in', 't')]
    L = ['v {xschem version=3.4.4 file_version=1.2}\nG {}\nK {type=subcircuit\nformat="@name @pinlist @symname"\n'
         'template="name=x1"\n}\nV {}\nS {}\nE {}',
         'P 4 5 -80 -60 80 -60 80 60 -80 60 -80 -60 {}',
         'T {@symname} -45 -38 0 0 0.25 0.25 {}', 'T {@name} -45 -14 0 0 0.3 0.3 {}',
         f'T {{{desc}}} -45 12 0 0 0.15 0.15 {{}}']
    for n, x, y, d, side in pins:
        if side == 'l':
            L += [f'L 4 -100 {y} -80 {y} {{}}', f'T {{{n}}} -75 {y - 7} 0 0 0.2 0.2 {{}}']
        elif side == 't':
            L += [f'L 4 {x} -80 {x} -60 {{}}', f'T {{{n}}} {x - 10} -56 0 0 0.2 0.2 {{}}']
        else:
            L += [f'L 4 {x} 60 {x} 80 {{}}', f'T {{{n}}} {x - 4 * len(n)} 40 0 0 0.2 0.2 {{}}']
        L.append(f'B 5 {x - 2.5} {y - 2.5} {x + 2.5} {y + 2.5} {{name={n} dir={d}}}')
    open(os.path.join(OUT, name + '.sym'), 'w').write('\n'.join(L) + '\n')


def copy_sym(src, name):
    """same pins and geometry as the hand-checked d2s_miller.sym / d2s_bias.sym"""
    shutil.copy(os.path.join(REF, src), os.path.join(OUT, name + '.sym'))


# ======================================================================== unit cells
def unit_ports(s, vss_y=100, gp_y=-140, gn_y=-60):
    s.port('opin', 520, -20, 'x')
    s.port('opin', 520, 20, 'y')
    s.port('ipin', 60, gp_y, 'gp')
    s.port('ipin', 60, gn_y, 'gn')
    s.port('iopin', 60, -400, 'vdd', 1)
    s.port('iopin', 60, vss_y, 'vss', 1)
    s.port('ipin', 60, -280, 'vbp')


def unit_split(name, tw, tl, degen, title):
    """unit_r / unit_r2 / unit_t: split tails Ta/Tb, degeneration between sa and sb, pair Ma/Mb."""
    s = Sheet(OUT)
    unit_ports(s)
    s.mos('Ta', P, 240, -340, 1, d='sa', g='vbp', s='vdd', b='vdd', w=tw, l=tl)
    s.mos('Tb', P, 380, -340, 0, d='sb', g='vbp', s='vdd', b='vdd', w=tw, l=tl)
    s.mos('Ma', P, 200, -140, 0, d='y', g='gp', s='sa', b='sa', w='20u', l='1u', ng=2)
    s.mos('Mb', P, 420, -140, 1, d='x', g='gn', s='sb', b='sb', w='20u', l='1u', ng=2)
    rail = 420
    if degen[0] == 'r':
        s.rhigh('R', 310, -220, 3, 'sa', 'sb', 'vss', '0.5u', degen[1])
        s.text('rhigh body = vss', 270, -190, 0.2)
    else:
        s.mos('D', P, 310, -200, 1, rot=1, d='sa', g='vss', s='sb', b='vdd', w=degen[1], l=degen[2])
        s.w('vdd', (310, -220), (310, -260), (440, -260), (440, -400))
        s.w('vss', (310, -180), (310, 100), (60, 100))
        rail = 440
    s.w('vdd', (60, -400), (rail, -400))
    s.w('vdd', (220, -370), (220, -400)); s.w('vdd', (220, -340), (200, -340), (200, -400))
    s.w('vdd', (400, -370), (400, -400)); s.w('vdd', (400, -340), (420, -340), (420, -400))
    s.w('vbp', (60, -280), (260, -280), (260, -340), (360, -340))
    s.w('sa', (220, -310), (220, -170)); s.w('sa', (220, -220), (280, -220))
    s.w('sa', (220, -140), (240, -140), (240, -220))
    s.w('sb', (400, -310), (400, -170)); s.w('sb', (400, -220), (340, -220))
    s.w('sb', (400, -140), (380, -140), (380, -220))
    s.w('gp', (60, -140), (180, -140))
    s.w('gn', (60, -60), (460, -60), (460, -140), (440, -140))
    s.w('y', (220, -110), (220, 20), (520, 20))
    s.w('x', (400, -110), (400, -20), (520, -20))
    s.lab(260, -220, 'sa'); s.lab(360, -220, 'sb', flip=1)
    s.text(title, 60, -500, 0.4)
    s.text('gp drains to y, gn drains to x; x and y go to the folding nodes', 60, -460, 0.25)
    save(s, name)


def unit_single(name, tw, tl, tng, pair, title):
    """unit_q (gate input) / unit_w (well input, gates at vss): single tail T, pair Ma/Mb."""
    s = Sheet(OUT)
    well = pair[0] == 'well'
    unit_ports(s, gp_y=-80 if well else -140, gn_y=-40 if well else -60)
    s.mos('T', P, 290, -340, 0, d='s', g='vbp', s='vdd', b='vdd', w=tw, l=tl, ng=tng)
    s.w('vdd', (60, -400), (330, -400)); s.w('vdd', (310, -370), (310, -400))
    s.w('vdd', (310, -340), (330, -340), (330, -400))
    s.w('vbp', (60, -280), (250, -280), (250, -340), (270, -340))
    s.w('s', (310, -310), (310, -220)); s.w('s', (220, -220), (400, -220))
    s.w('s', (220, -220), (220, -170)); s.w('s', (400, -220), (400, -170))
    s.w('y', (220, -110), (220, 20), (520, 20))
    s.w('x', (400, -110), (400, -20), (520, -20))
    w, l = pair[1], pair[2]
    if well:   # inputs on the bulks, gates at vss
        s.mos('Ma', P, 200, -140, 0, d='y', g='vss', s='s', b='gp', w=w, l=l)
        s.mos('Mb', P, 420, -140, 1, d='x', g='vss', s='s', b='gn', w=w, l=l)
        s.w('gp', (220, -140), (260, -140), (260, -80), (60, -80))
        s.w('gn', (400, -140), (360, -140), (360, -40), (60, -40))
        s.w('vss', (180, -140), (160, -140), (160, 100))
        s.w('vss', (440, -140), (460, -140), (460, 100))
        s.w('vss', (60, 100), (460, 100))
    else:
        s.mos('Ma', P, 200, -140, 0, d='y', g='gp', s='s', b='s', w=w, l=l)
        s.mos('Mb', P, 420, -140, 1, d='x', g='gn', s='s', b='s', w=w, l=l)
        s.w('s', (220, -140), (240, -140), (240, -220))
        s.w('s', (400, -140), (380, -140), (380, -220))
        s.w('gp', (60, -140), (180, -140))
        s.w('gn', (60, -60), (460, -60), (460, -140), (440, -140))
    s.lab(350, -220, 's', flip=1)
    s.text(title, 60, -500, 0.4)
    s.text('gp drains to y, gn drains to x; x and y go to the folding nodes', 60, -460, 0.25)
    save(s, name)


# ======================================================================== annotation
MAG = 10   # xschem layer for block outlines, tags and legend (magenta in the dark scheme)


def block(s, x1, y1, x2, y2, tag, tx, ty, size=0.35):
    """dashed outline around a functional block, short tag at (tx, ty)"""
    s.texts.append(f'P {MAG} 5 {x1} {y1} {x2} {y1} {x2} {y2} {x1} {y2} {x1} {y1} {{dash=6}}')
    s.texts.append(f'T {{{tag}}} {tx} {ty} 0 0 {size} {size} {{layer={MAG}}}')


def legend(s, lines, x=1250, y=-110, size=0.3, step=24):
    for i, t in enumerate(lines):
        assert '{' not in t and '}' not in t
        s.texts.append(f'T {{{t}}} {x} {y + step * i} 0 0 {size} {size} {{layer={MAG}}}')


LEG_CORE = [
    '[1] DDA units A, B, C1, C2: split-tail PMOS pair, rhigh between the sources. Each adds f(gp - gn) to the fold nodes:'
    ' the gp device drains to y, the gn device to x.',
    '      A: vinp - vref,  B: vref - vinn,  C1 = C2: vref - vfb.  The loop forces f(vinp - vref) + f(vref - vinn) = 2 f(vfb - vref),'
    ' so vfb - vref = (vinp - vinn)/2.',
    '[2] fold: sinks SX, SY (gate vbn) and NMOS cascodes CX, CY (gate vbnc). x and y are the fold nodes.',
    '[3] PMOS cascoded mirror: PL, PCL is the input side (gates tied to l2), PR, PCR the output side into node a. Cascode gates vbpc.',
    '[4] class-AB control: ABP (gate vabp) and ABN (gate vabn) between a and b. With RP1/RP2 and RN1/RN2 in the bias it sets'
    ' the quiescent current of OP and ON.',
    '[5] FPL, FNL: copy of [4] in the mirror input branch (between l2 and l1), so both fold branches carry the same element.',
]


class Shift:
    """the same sheet with every x moved by dx (the part right of the DDA units)"""
    def __init__(self, s, dx):
        self.s, self.dx = s, dx

    def mos(self, name, model, x, y, flip, **k):
        return self.s.mos(name, model, x + self.dx, y, flip, **k)

    def w(self, net, *pts):
        self.s.w(net, *[(x + self.dx, y) for x, y in pts])

    def lab(self, x, y, net, **k):
        self.s.lab(x + self.dx, y, net, **k)

    def block(self, x1, y1, x2, y2, tag, tx, ty):
        block(self.s, x1 + self.dx, y1, x2 + self.dx, y2, tag, tx + self.dx, ty)

    def place(self, ref, x, y, *a):
        return self.s.place(ref, x + self.dx, y, *a)


# ======================================================================== d2s_mpdda / d2s_lc2
UNITS = [('A', 'vinp', 'vref'), ('B', 'vref', 'vinn'), ('C1', 'vref', 'vfb'), ('C2', 'vref', 'vfb')]
BUS = {'vinp': -560, 'vinn': -540, 'vref': -520, 'vfb': -500, 'vabp': -480, 'vabn': -460, 'vbnc': -440}
BIASN = ('vbp', 'vbn', 'vbpc', 'vbnc', 'vabp', 'vabn')


def unit_flat(s, name, cx, gp, gn):
    """unit_r2 at transistor level, centred on cx: tails at -980, rhigh at -840, pair at -760.
    Devices and internal nets carry the suffix _<unit name>."""
    sa, sb = 'sa_' + name, 'sb_' + name
    s.mos('Ta_' + name, P, cx - 70, -980, 1, d=sa, g='vbp', s='vdd', b='vdd', w='5u', l='6u')
    s.mos('Tb_' + name, P, cx + 70, -980, 0, d=sb, g='vbp', s='vdd', b='vdd', w='5u', l='6u')
    s.rhigh('R_' + name, cx, -840, 3, sa, sb, 'vss', '0.5u', '50.6u')
    s.mos('Ma_' + name, P, cx - 110, -760, 0, d='y', g=gp, s=sa, b=sa, w='20u', l='1u', ng=2)
    s.mos('Mb_' + name, P, cx + 110, -760, 1, d='x', g=gn, s=sb, b=sb, w='20u', l='1u', ng=2)
    for sg in (-1, 1):
        s.w('vdd', (cx + 90 * sg, -1010), (cx + 90 * sg, -1040))
        s.w('vdd', (cx + 90 * sg, -980), (cx + 110 * sg, -980), (cx + 110 * sg, -1040))
    s.w('vbp', (cx - 50, -980), (cx + 50, -980)); s.w('vbp', (cx, -980), (cx, -920))
    for sg, n in ((-1, sa), (1, sb)):
        s.w(n, (cx + 90 * sg, -950), (cx + 90 * sg, -790)); s.w(n, (cx + 90 * sg, -840), (cx + 30 * sg, -840))
        s.w(n, (cx + 90 * sg, -760), (cx + 70 * sg, -760), (cx + 70 * sg, -840))
    s.w(gp, (cx - 150, BUS[gp]), (cx - 150, -760), (cx - 130, -760))
    s.w(gn, (cx + 150, BUS[gn]), (cx + 150, -760), (cx + 130, -760))
    s.w('y', (cx - 90, -730), (cx - 90, -300)); s.w('x', (cx + 90, -730), (cx + 90, -340))
    s.lab(cx - 50, -840, sa); s.lab(cx + 50, -840, sb, flip=1)
    fn = {'A': 'vinp - vref', 'B': 'vref - vinn', 'C1': 'vref - vfb', 'C2': 'vref - vfb'}[name]
    block(s, cx - 170, -1030, cx + 170, -700, f'[1] {name}: f({fn})', cx - 165, -1068)


def core(s, flat=False, ux0=300, dx=0, bias=None):
    """Ports, the four DDA units (unit_r2 boxes, or transistors if flat), fold, mirror and class-AB
    control. Everything right of the units is drawn at the d2s_mpdda.sch coordinates moved by dx.
    bias=None: the bias nets are ports at x=60; else {net: x} where each bias bus starts."""
    r = Shift(s, dx)
    vbpc_y = -880 if flat else -780
    BY = dict(BUS, vbp=-920, vbpc=vbpc_y, vbn=-260)
    s.port('iopin', 60, -1040, 'vdd', 1)
    s.port('iopin', 60, -140, 'vss', 1)
    for n in ('vinp', 'vinn', 'vref'):
        s.port('ipin', 60, BUS[n], n)
    s.port('iopin', 2440 + dx, -600, 'vout')
    s.port('ipin', 60, BUS['vfb'], 'vfb')
    if bias is None:
        for n in BIASN:
            s.port('ipin', 60, BY[n], n)
        bias = {n: 60 for n in BIASN}
    # ---- DDA units
    ends, xs, ys = {}, [], []
    for k, (name, gp, gn) in enumerate(UNITS):
        if flat:
            cx = ux0 + 360 * k
            unit_flat(s, name, cx, gp, gn)
            gpx, gnx, xd, yd, vbx = cx - 150, cx + 150, cx + 90, cx - 90, cx
        else:
            cx = ux0 + 240 * k
            s.sub('X' + name, 'unit_r2.sym', cx, -660, dict(x='x', y='y', gp=gp, gn=gn, vdd='vdd', vss='vss', vbp='vbp'))
            s.w('vdd', (cx - 40, -740), (cx - 40, -1040))
            s.w('vbp', (cx + 40, -740), (cx + 40, -920))
            s.w('x', (cx - 40, -580), (cx - 40, -340))
            s.w('y', (cx, -580), (cx, -300))
            s.w('vss', (cx + 40, -580), (cx + 40, -140))
            s.w(gp, (cx - 140, BUS[gp]), (cx - 140, -680), (cx - 100, -680))
            s.w(gn, (cx - 120, BUS[gn]), (cx - 120, -640), (cx - 100, -640))
            gpx, gnx, xd, yd, vbx = cx - 140, cx - 120, cx - 40, cx, cx + 40
        ends[gp] = max(ends.get(gp, 0), gpx)
        ends[gn] = max(ends.get(gn, 0), gnx)
        xs.append(xd); ys.append(yd)
    if not flat:
        block(s, ux0 - 150, -775, ux0 + 720 + 110, -565, '[1]', ux0 - 145, -771)
    for n, xe in ends.items():
        s.w(n, (60, BUS[n]), (xe, BUS[n]))
    s.w('vbp', (bias['vbp'], -920), (vbx, -920))
    s.w('x', (min(xs), -340), (1260 + dx, -340))
    s.w('y', (min(ys), -300), (2120 + dx, -300))
    # ---- left NMOS column (fold node x): FNL, CX, SX; bulk line x=1280
    r.mos('FNL', N, 1240, -660, 0, d='l2', g='vabn', s='l1', b='vss', w='4.4u', l='1u')
    r.mos('CX', N, 1240, -420, 0, d='l1', g='vbnc', s='x', b='vss', w='30u', l='3u', ng=2)
    r.mos('SX', N, 1240, -220, 0, d='x', g='vbn', s='vss', b='vss', w='36u', l='6u', ng=4)
    for y in (-660, -420, -220):
        r.w('vss', (1260, y), (1280, y))
    r.w('vss', (1280, -660), (1280, -140)); r.w('vss', (1260, -190), (1260, -140))
    r.w('x', (1260, -390), (1260, -250))
    r.w('l1', (1260, -630), (1260, -450)); r.w('l1', (1260, -600), (1520, -600), (1520, -630))
    # ---- left PMOS column (mirror input, l2): PL, PCL, FPL; bulk line x=1500
    r.mos('PL', P, 1540, -980, 1, d='pl', g='l2', s='vdd', b='vdd', w='24u', l='4u', ng=4)
    r.mos('PCL', P, 1540, -820, 1, d='l2', g='vbpc', s='pl', b='vdd', w='30u', l='3u', ng=2)
    r.mos('FPL', P, 1540, -660, 1, d='l1', g='vabp', s='l2', b='vdd', w='6.66u', l='0.6u')
    for y in (-980, -820, -660):
        r.w('vdd', (1520, y), (1500, y))
    r.w('vdd', (1500, -1040), (1500, -660)); r.w('vdd', (1520, -1010), (1520, -1040))
    r.w('pl', (1520, -950), (1520, -850))
    r.w('l2', (1520, -790), (1520, -720), (1520, -690)); r.w('l2', (1260, -690), (1260, -720), (1700, -720), (1700, -980))
    r.w('l2', (1560, -980), (1840, -980))
    # ---- right PMOS column (mirror output, a): PR, PCR, ABP; bulk line x=1900
    r.mos('PR', P, 1860, -980, 0, d='pr', g='l2', s='vdd', b='vdd', w='24u', l='4u', ng=4)
    r.mos('PCR', P, 1860, -820, 0, d='a', g='vbpc', s='pr', b='vdd', w='30u', l='3u', ng=2)
    r.mos('ABP', P, 1860, -660, 0, d='b', g='vabp', s='a', b='vdd', w='6.66u', l='0.6u')
    for y in (-980, -820, -660):
        r.w('vdd', (1880, y), (1900, y))
    r.w('vdd', (1900, -1040), (1900, -660)); r.w('vdd', (1880, -1010), (1880, -1040))
    r.w('pr', (1880, -950), (1880, -850))
    # ---- right NMOS column (fold node y): ABN, CY, SY; bulk line x=2140
    r.mos('ABN', N, 2100, -660, 0, d='a', g='vabn', s='b', b='vss', w='4.4u', l='1u')
    r.mos('CY', N, 2100, -420, 0, d='b', g='vbnc', s='y', b='vss', w='30u', l='3u', ng=2)
    r.mos('SY', N, 2100, -220, 0, d='y', g='vbn', s='vss', b='vss', w='36u', l='6u', ng=4)
    for y in (-660, -420, -220):
        r.w('vss', (2120, y), (2140, y))
    r.w('vss', (2140, -660), (2140, -140)); r.w('vss', (2120, -190), (2120, -140))
    r.w('y', (2120, -390), (2120, -250))
    # ---- class-AB nodes a (top) and b (bottom), trunks at x=2220 to the output gates
    r.w('a', (1880, -790), (1880, -690)); r.w('a', (1880, -740), (2220, -740)); r.w('a', (2120, -740), (2120, -690))
    r.w('a', (2220, -740), (2220, -980), (2320, -980))
    r.w('b', (1880, -630), (1880, -600), (2220, -600)); r.w('b', (2120, -630), (2120, -600), (2120, -450))
    r.w('b', (2220, -600), (2220, -220), (2320, -220))
    # ---- bias buses: from the port column (or the bias columns) to the gates
    s.w('vbpc', (bias['vbpc'], vbpc_y), (1820 + dx, vbpc_y))
    r.w('vbpc', (1820, vbpc_y), (1820, -820), (1840, -820)); r.w('vbpc', (1580, vbpc_y), (1580, -820), (1560, -820))
    s.w('vabp', (bias['vabp'], BUS['vabp']), (1700 + dx, BUS['vabp']))
    r.w('vabp', (1700, BUS['vabp']), (1700, -660)); r.w('vabp', (1560, -660), (1840, -660))
    for n, yg in (('vabn', -660), ('vbnc', -420), ('vbn', -220)):
        s.w(n, (bias[n], BY[n]), (2060 + dx, BY[n]))
        r.w(n, (2060, BY[n]), (2060, yg), (2080, yg))
        r.w(n, (1200, BY[n]), (1200, yg), (1220, yg))
    s.w('vdd', (60, -1040), (2380 + dx, -1040))
    s.w('vss', (60, -140), (2380 + dx, -140))
    if any(x != 60 for x in bias.values()):   # bias nets drawn on the sheet: name them where they enter
        for n in BIASN:
            s.lab(ux0 - 190, BY[n], n)
    for n, x, y, f in [('x', 1160, -340, 0), ('y', 1160, -300, 0), ('l1', 1400, -600, 0), ('l2', 1400, -720, 0),
                       ('pl', 1520, -900, 0), ('pr', 1880, -900, 1), ('a', 2000, -740, 0), ('b', 2000, -600, 0)]:
        r.lab(x, y, n, flip=f)
    # ---- functional blocks
    r.block(1185, -475, 1345, -165, '[2]', 1355, -420)
    r.block(2040, -475, 2215, -165, '[2]', 2000, -420)
    r.block(1370, -1030, 1970, -795, '[3]', 1590, -965)
    r.block(1815, -735, 2215, -610, '[4]', 1820, -758)
    r.block(1180, -735, 1595, -610, '[5]', 1185, -758)
    return r


def out_mpdda(r):
    """output devices OP, ON and the MOS Miller capacitors CMA, CMB (d2s_mpdda.sch coordinates)"""
    r.mos('OP', P, 2340, -980, 0, d='vout', g='a', s='vdd', b='vdd', w='546.12u', l='0.6u', ng=82)
    r.mos('ON', N, 2340, -220, 0, d='vout', g='b', s='vss', b='vss', w='290.4u', l='1u', ng=66)
    r.w('vdd', (2360, -1010), (2360, -1040)); r.w('vdd', (2360, -980), (2380, -980), (2380, -1040))
    r.w('vss', (2360, -190), (2360, -140)); r.w('vss', (2360, -220), (2380, -220), (2380, -140))
    r.w('vout', (2360, -950), (2360, -250)); r.w('vout', (2360, -600), (2440, -600))
    # Miller capacitors: thick-oxide PMOS in accumulation (gate over n-well), 16u x 16u
    r.mos('CMA', P, 2280, -740, 0, d='vout', g='a', s='vout', b='vout', w='16u', l='16u')
    r.w('vout', (2300, -770), (2300, -710)); r.w('vout', (2300, -740), (2360, -740))
    r.w('a', (2220, -740), (2260, -740))
    r.mos('CMB', P, 2320, -520, 1, d='b', g='vout', s='b', b='b', w='16u', l='16u')
    r.w('b', (2300, -550), (2300, -490)); r.w('b', (2300, -520), (2220, -520))
    r.w('vout', (2340, -520), (2360, -520))
    r.block(2290, -1030, 2470, -925, '[6]', 2295, -1062)
    r.block(2290, -275, 2470, -165, '[6]', 2295, -298)
    r.block(2235, -795, 2390, -690, '[7]', 2170, -795)
    r.block(2230, -570, 2390, -470, '[7]', 2170, -545)


LEG_MPDDA = ['[6] output devices OP (gate a), ON (gate b), drains on vout.',
             '[7] Miller capacitors CMA (between a and vout) and CMB (between vout and b): hv PMOS in accumulation,'
             ' gate over n-well, 16u x 16u.']


def d2s_mpdda():
    s = Sheet(OUT)
    out_mpdda(core(s))
    s.text('d2s_mpdda: matched-pair DDA (4 x unit_r2), folded cascode, class-AB output, '
           'MOS Miller compensation (vfb = vout)', 90, -1140, 0.6)
    s.text('frozen .subckt defaults: lcas = 3 (CX, CY, PCL, PCR 30u / 3u ng=2), wc = lc = 16u (CMA, CMB), '
           'rl = 50.6u (in unit_r2.sch)', 90, -1090, 0.3)
    s.text('the DDA units at transistor level: d2s_mpdda_flat.sch; with the bias network: d2s_mpdda_bias_flat.sch; '
           'block descriptions: README.md', 90, -1065, 0.3)
    legend(s, LEG_CORE + LEG_MPDDA)
    s.place('devices/title.sym', 170, -40, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, 'd2s_mpdda')


def d2s_mpdda_flat():
    s = Sheet(OUT)
    out_mpdda(core(s, flat=True, ux0=300, dx=400))
    s.text('d2s_mpdda_flat: d2s_mpdda with the four DDA units (unit_r2) drawn at transistor level', 90, -1220, 0.6)
    s.text('same ports and devices as d2s_mpdda; unit devices and nets carry the unit name: Ta_A, Tb_A, R_A, Ma_A, Mb_A,'
           ' sa_A, sb_A, ...  rhigh body = vss', 90, -1170, 0.3)
    s.text('frozen .subckt defaults: lcas = 3, wc = lc = 16u, rl = 50.6u; block descriptions: README.md', 90, -1145, 0.3)
    legend(s, LEG_CORE + LEG_MPDDA)
    s.place('devices/title.sym', 170, -40, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, 'd2s_mpdda_flat')


def d2s_lc2(cascode):
    name = 'd2s_lc2' if cascode else 'd2s_lc2_nc'
    s = Sheet(OUT)
    core(s)
    w_p, w_n, ng_p, ng_n = '273.06u', '145.2u', 41, 33
    s.w('vdd', (2360, -1010), (2360, -1040)); s.w('vdd', (2360, -980), (2380, -980), (2380, -1040))
    s.w('vss', (2360, -190), (2360, -140))
    s.w('vout', (2360, -600), (2440, -600))
    if cascode:
        s.mos('OP', P, 2340, -980, 0, d='op', g='a', s='vdd', b='vdd', w=w_p, l='0.6u', ng=ng_p)
        s.mos('OPC', P, 2340, -820, 0, d='vout', g='vref', s='op', b='op', w=w_p, l='0.6u', ng=ng_p)
        s.mos('ONC', N, 2340, -380, 0, d='vout', g='vref', s='on', b='vss', w=w_n, l='0.6u', ng=ng_n)
        s.mos('ON', N, 2340, -220, 0, d='on', g='b', s='vss', b='vss', w=w_n, l='1u', ng=ng_n)
        s.w('op', (2360, -950), (2360, -850)); s.w('op', (2360, -820), (2380, -820), (2380, -900), (2360, -900))
        s.w('vout', (2360, -790), (2360, -410))
        s.w('on', (2360, -350), (2360, -250))
        s.w('vss', (2360, -380), (2380, -380), (2380, -140)); s.w('vss', (2360, -220), (2380, -220))
        s.w('vref', (2320, -820), (2300, -820), (2300, -380), (2320, -380))
        s.lab(2300, -680, 'vref', kind='lab_pin')
        s.lab(2360, -900, 'op', flip=1); s.lab(2360, -300, 'on', flip=1)
        block(s, 2290, -1030, 2470, -925, '[6]', 2295, -1062)
        block(s, 2290, -275, 2470, -165, '[6]', 2410, -298)
        block(s, 2290, -870, 2470, -770, '[7]', 2410, -893)
        block(s, 2290, -430, 2470, -330, '[7]', 2410, -453)
        title = ('d2s_lc2: case (b), cascoded output devices in the slot (half frames), cascode gates at vref, '
                 'load-compensated (no Miller capacitor)')
        leg = ['[6] output devices OP (gate a), ON (gate b): half frames, in the slot, not the pad clamps.',
               '[7] output cascodes OPC, ONC, gates at vref (output range about 1.0 ... 2.4 V).',
               '[9] diode replicas DP (on a), DN (on b), 1/41 and 1/38 of OP, ON: low-impedance gate nodes.'
               ' No compensation capacitor: the load capacitance is the dominant pole.']
    else:
        s.mos('OP', P, 2340, -980, 0, d='vout', g='a', s='vdd', b='vdd', w=w_p, l='0.6u', ng=ng_p)
        s.mos('ON', N, 2340, -220, 0, d='vout', g='b', s='vss', b='vss', w=w_n, l='1u', ng=ng_n)
        s.w('vout', (2360, -950), (2360, -250))
        s.w('vss', (2360, -220), (2380, -220), (2380, -140))
        block(s, 2290, -1030, 2470, -925, '[6]', 2295, -1062)
        block(s, 2290, -275, 2470, -165, '[6]', 2410, -298)
        title = 'd2s_lc2_nc: d2s_lc2 without the output cascodes, load-compensated (no Miller capacitor)'
        leg = ['[6] output devices OP (gate a), ON (gate b): half frames, in the slot, not the pad clamps.',
               '[9] diode replicas DP (on a), DN (on b), 1/41 and 1/38 of OP, ON: low-impedance gate nodes.'
               ' No compensation capacitor: the load capacitance is the dominant pole.']
    # diode replicas on a and b (low-impedance gate nodes)
    s.mos('DP', P, 2180, -900, 1, d='a', g='a', s='vdd', b='vdd', w='6.66u', l='0.6u')
    s.w('a', (2200, -900), (2220, -900)); s.w('a', (2160, -870), (2160, -840), (2220, -840))
    s.w('vdd', (2160, -930), (2160, -1040)); s.w('vdd', (2160, -900), (2140, -900), (2140, -1040))
    s.mos('DN', N, 2180, -480, 1, d='b', g='b', s='vss', b='vss', w='3.8u', l='1u')
    s.w('b', (2200, -480), (2220, -480)); s.w('b', (2160, -510), (2160, -540), (2220, -540))
    s.w('vss', (2160, -450), (2160, -440), (2140, -440)); s.w('vss', (2160, -480), (2140, -480))
    block(s, 2110, -950, 2230, -820, '[9]', 2060, -950)
    block(s, 2110, -560, 2230, -430, '[9]', 2235, -585)
    s.text(title, 90, -1140, 0.6)
    s.text('frozen .subckt defaults: lcas = 3 (CX, CY, PCL, PCR 30u / 3u ng=2), wdp = 6.66u, wdn = 3.8u; '
           'units are unit_r2 (rl = 50.6u)', 90, -1090, 0.3)
    s.text('block descriptions: README.md', 90, -1065, 0.3)
    legend(s, LEG_CORE + leg)
    s.place('devices/title.sym', 170, -40, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, name)


# ======================================================================== d2s_bias_lp
LEG_BIAS = [
    '[8] bias: ideal reference currents into diode-connected devices.',
    '      vbp: BP 5u/6u at 5 uA, for the unit tails Ta, Tb (5u/6u, 5 uA each).   vbn: BN 6u/6u at 5 uA, for the sinks SX, SY'
    ' (36u/6u, 30 uA each).',
    '      vbpc: BPC 1u/4u at 2 uA, for the mirror cascodes PCL, PCR.   vbnc: BNC 1u/8u at 2 uA, for the fold cascodes CX, CY.',
    '      vabp: RP2 (= ABP) on RP1 (2 x ABP) at 5 uA, for ABP, FPL.   vabn: RN2 (= ABN) on RN1 (2 x ABN) at 5 uA, for ABN, FNL.',
]


def pdiode(s, name, x, y, node, src, w, l, ng=1):
    """diode-connected PMOS, gate tied to the drain 60 below the device"""
    s.mos(name, P, x, y, 0, d=node, g=node, s=src, b='vdd', w=w, l=l, ng=ng)
    s.w(node, (x - 20, y), (x - 20, y + 60), (x + 20, y + 60)); s.w(node, (x + 20, y + 30), (x + 20, y + 60))


def ndiode(s, name, x, y, node, src, w, l, ng=1):
    """diode-connected NMOS, gate tied to the drain 60 above the device"""
    s.mos(name, N, x, y, 0, d=node, g=node, s=src, b='vss', w=w, l=l, ng=ng)
    s.w(node, (x - 20, y), (x - 20, y - 60), (x + 20, y - 60)); s.w(node, (x + 20, y - 30), (x + 20, y - 60))


def bias_tag(s, x, ytop, ybot, node, tag_y):
    block(s, x - 45, ytop, x + 105, ybot, f'[8] {node}', x - 40, tag_y)


def d2s_bias_lp():
    s = Sheet(OUT)
    yv, yg = -840, -60
    s.port('iopin', 60, yv, 'vdd', 1)
    s.port('iopin', 60, yg, 'vss', 1)
    out = {'vbp': -540, 'vbn': -420, 'vbpc': -500, 'vbnc': -380, 'vabp': -460, 'vabn': -340}
    for n in ('vbp', 'vbn', 'vbpc', 'vbnc', 'vabp', 'vabn'):
        s.port('opin', 1200, out[n], n)
    # PMOS-diode columns: diode at the top, current sink to vss at the bottom
    for name, iname, x, node, w, l, i in [('BP', 'IBP', 200, 'vbp', '5u', '6u', '5u'),
                                          ('BPC', 'IBPC', 360, 'vbpc', '1u', '4u', '2u')]:
        pdiode(s, name, x, -760, node, 'vdd', w, l)
        s.w('vdd', (x + 20, -790), (x + 20, yv)); s.w('vdd', (x + 20, -760), (x + 40, -760), (x + 40, yv))
        s.isrc(iname, x + 20, -140, node, 'vss', i)
        s.w(node, (x + 20, -700), (x + 20, -170)); s.w('vss', (x + 20, -110), (x + 20, yg))
        s.w(node, (x + 20, out[node]), (1200, out[node]))
        bias_tag(s, x, -830, -70, node, -870)
    # vabp: two stacked PMOS diodes (RP1 2x, RP2 1x), sink IABP
    pdiode(s, 'RP1', 520, -760, 'n1', 'vdd', '13.32u', '0.6u', 2)
    s.w('vdd', (540, -790), (540, yv)); s.w('vdd', (540, -760), (560, -760), (560, yv))
    pdiode(s, 'RP2', 520, -640, 'vabp', 'n1', '6.66u', '0.6u')
    s.w('n1', (540, -700), (540, -670)); s.w('vdd', (540, -640), (560, -640), (560, -760))
    s.isrc('IABP', 540, -140, 'vabp', 'vss', '5u')
    s.w('vabp', (540, -580), (540, -170)); s.w('vss', (540, -110), (540, yg))
    s.w('vabp', (540, out['vabp']), (1200, out['vabp']))
    s.lab(540, -690, 'n1')
    bias_tag(s, 520, -830, -70, 'vabp', -870)
    # NMOS-diode columns: current source from vdd at the top, diode at the bottom
    for name, iname, x, node, w, l, i in [('BN', 'IBN', 680, 'vbn', '6u', '6u', '5u'),
                                          ('BNC', 'IBNC', 840, 'vbnc', '1u', '8u', '2u')]:
        s.isrc(iname, x + 20, -760, 'vdd', node, i)
        s.w('vdd', (x + 20, -790), (x + 20, yv)); s.w(node, (x + 20, -730), (x + 20, -200))
        ndiode(s, name, x, -140, node, 'vss', w, l)
        s.w('vss', (x + 20, -110), (x + 20, yg)); s.w('vss', (x + 20, -140), (x + 40, -140), (x + 40, yg))
        s.w(node, (x + 20, out[node]), (1200, out[node]))
        bias_tag(s, x, -830, -70, node, -870)
    # vabn: IABN from vdd, two stacked NMOS diodes (RN2 1x on top, RN1 2x at the bottom)
    s.isrc('IABN', 1020, -760, 'vdd', 'vabn', '5u')
    s.w('vdd', (1020, -790), (1020, yv)); s.w('vabn', (1020, -730), (1020, -320))
    ndiode(s, 'RN2', 1000, -260, 'vabn', 'n2', '4.4u', '1u')
    ndiode(s, 'RN1', 1000, -140, 'n2', 'vss', '8.8u', '1u', 2)
    s.w('n2', (1020, -230), (1020, -200))
    s.w('vss', (1020, -110), (1020, yg)); s.w('vss', (1020, -140), (1040, -140), (1040, yg))
    s.w('vss', (1020, -260), (1040, -260), (1040, -140))
    s.w('vabn', (1020, out['vabn']), (1200, out['vabn']))
    s.lab(1020, -220, 'n2')
    bias_tag(s, 1000, -830, -70, 'vabn', -870)
    s.w('vdd', (60, yv), (1020, yv))
    s.w('vss', (60, yg), (1040, yg))
    s.text('d2s_bias_lp: bias for d2s_mpdda / d2s_lc2 (ideal reference currents, iab = 5u, ibnc = 2u)',
           60, -980, 0.5)
    s.text('vabp, vabn: replicas of the class-AB pairs (FPL/ABP 6.66u/0.6u, FNL/ABN 4.4u/1u), '
           'stacked on a 2x diode', 60, -930, 0.3)
    legend(s, LEG_BIAS, x=60, y=-30)
    s.place('devices/title.sym', 160, 160, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, 'd2s_bias_lp')


def bias_cols(s):
    """d2s_bias_lp drawn between the port column and the DDA units (rails at -1040 / -140).
    The column order keeps every bus clear of the diode junctions to its right.
    Returns {net: x where its bus starts}."""
    tap = {}
    # vabp: RP1 (2x) under RP2 (1x), sink IABP
    pdiode(s, 'RP1', 200, -980, 'n1', 'vdd', '13.32u', '0.6u', 2)
    s.w('vdd', (220, -1010), (220, -1040)); s.w('vdd', (220, -980), (240, -980), (240, -1040))
    pdiode(s, 'RP2', 200, -860, 'vabp', 'n1', '6.66u', '0.6u')
    s.w('n1', (220, -920), (220, -890)); s.w('vdd', (220, -860), (240, -860), (240, -980))
    s.isrc('IABP', 220, -200, 'vabp', 'vss', '5u')
    s.w('vabp', (220, -800), (220, -230)); s.w('vss', (220, -170), (220, -140))
    s.lab(220, -905, 'n1')
    tap['vabp'] = 220
    for name, iname, x, node, w, l, i in [('BPC', 'IBPC', 360, 'vbpc', '1u', '4u', '2u'),
                                          ('BP', 'IBP', 520, 'vbp', '5u', '6u', '5u')]:
        pdiode(s, name, x, -980, node, 'vdd', w, l)
        s.w('vdd', (x + 20, -1010), (x + 20, -1040)); s.w('vdd', (x + 20, -980), (x + 40, -980), (x + 40, -1040))
        s.isrc(iname, x + 20, -200, node, 'vss', i)
        s.w(node, (x + 20, -920), (x + 20, -230)); s.w('vss', (x + 20, -170), (x + 20, -140))
        tap[node] = x + 20
    # vabn: IABN from vdd, RN2 (1x) on RN1 (2x)
    s.isrc('IABN', 700, -980, 'vdd', 'vabn', '5u')
    s.w('vdd', (700, -1010), (700, -1040)); s.w('vabn', (700, -950), (700, -380))
    ndiode(s, 'RN2', 680, -320, 'vabn', 'n2', '4.4u', '1u')
    ndiode(s, 'RN1', 680, -200, 'n2', 'vss', '8.8u', '1u', 2)
    s.w('n2', (700, -290), (700, -260))
    s.w('vss', (700, -170), (700, -140)); s.w('vss', (700, -200), (720, -200), (720, -140))
    s.w('vss', (700, -320), (720, -320), (720, -200))
    s.lab(700, -280, 'n2')
    tap['vabn'] = 700
    for name, iname, x, node, w, l, i in [('BNC', 'IBNC', 840, 'vbnc', '1u', '8u', '2u'),
                                          ('BN', 'IBN', 1000, 'vbn', '6u', '6u', '5u')]:
        s.isrc(iname, x + 20, -980, 'vdd', node, i)
        s.w('vdd', (x + 20, -1010), (x + 20, -1040)); s.w(node, (x + 20, -950), (x + 20, -260))
        ndiode(s, name, x, -200, node, 'vss', w, l)
        s.w('vss', (x + 20, -170), (x + 20, -140)); s.w('vss', (x + 20, -200), (x + 40, -200), (x + 40, -140))
        tap[node] = x + 20
    for x, node in ((200, 'vabp'), (360, 'vbpc'), (520, 'vbp'), (680, 'vabn'), (840, 'vbnc'), (1000, 'vbn')):
        bias_tag(s, x, -1030, -150, node, -1068)
    return tap


def d2s_mpdda_bias_flat():
    s = Sheet(OUT)
    tap = bias_cols(s)
    out_mpdda(core(s, flat=True, ux0=1300, dx=1400, bias=tap))
    s.text('d2s_mpdda_bias_flat: d2s_mpdda and d2s_bias_lp in one sheet, all at transistor level', 90, -1220, 0.6)
    s.text('same devices as d2s_mpdda_biased (d2s_mpdda + d2s_bias_lp); unit devices and nets carry the unit name: '
           'Ta_A, Tb_A, R_A, Ma_A, Mb_A, sa_A, sb_A, ...  rhigh body = vss', 90, -1170, 0.3)
    s.text('the bias nets are internal here (d2s_mpdda_biased keeps them as pins for CACE); '
           'frozen defaults lcas = 3, wc = lc = 16u, rl = 50.6u, iab = 5u, ibnc = 2u; block descriptions: README.md',
           90, -1145, 0.3)
    legend(s, LEG_CORE + LEG_MPDDA + LEG_BIAS)
    s.place('devices/title.sym', 170, -40, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, 'd2s_mpdda_bias_flat')


def strip_sym(src, name, drop):
    """copy a hand-checked symbol without the pins in `drop` (each pin is an L, B, T line triple)"""
    L = open(os.path.join(REF, src)).read().splitlines()
    out, i = [], 0
    while i < len(L):
        if L[i].startswith('L ') and i + 1 < len(L) and any(f'{{name={p} ' in L[i + 1] for p in drop):
            i += 3
            continue
        out.append(L[i]); i += 1
    open(os.path.join(OUT, name + '.sym'), 'w').write('\n'.join(out) + '\n')


def fixture():
    """d2s_mpdda + d2s_bias_lp, same wiring as the hand-made d2s_miller_biased.sch."""
    t = open(os.path.join(REF, 'd2s_miller_biased.sch')).read()
    t = t.replace('{d2s_miller.sym}', '{d2s_mpdda.sym}').replace('{d2s_bias.sym}', '{d2s_bias_lp.sym}')
    t = t.replace('d2s_miller + d2s_bias test fixture', 'd2s_mpdda + d2s_bias_lp test fixture')
    open(os.path.join(OUT, 'd2s_mpdda_biased.sch'), 'w').write(t)


if __name__ == '__main__':
    if not os.path.samefile(OUT, XSDIR):
        shutil.copy(os.path.join(XSDIR, 'xschemrc'), OUT)
    unit_sym('unit_r', 'x,y += f(gp-gn)')
    unit_sym('unit_r2', 'x,y += f(gp-gn)')
    unit_sym('unit_t', 'x,y += f(gp-gn)')
    unit_sym('unit_w', 'x,y += f(gp-gn)')
    unit_sym('unit_q', 'x,y += f(gp-gn)')
    unit_split('unit_r2', '5u', '6u', ('r', '50.6u'), 'unit_r2: split-tail PMOS pair, rhigh degeneration (unit of d2s_mpdda)')
    unit_split('unit_r', '10u', '2u', ('r', '36.4u'), 'unit_r: split-tail PMOS pair, rhigh degeneration')
    unit_split('unit_t', '10u', '2u', ('t', '0.5u', '3u'), 'unit_t: split-tail PMOS pair, triode hv PMOS degeneration')
    unit_single('unit_q', '10u', '2u', 1, ('gate', '2u', '6u'), 'unit_q: undegenerated square-law PMOS pair')
    unit_single('unit_w', '20u', '2u', 2, ('well', 'wwi', 'lwi'), 'unit_w: well-input PMOS pair, gates at vss')
    copy_sym('d2s_miller.sym', 'd2s_mpdda')
    copy_sym('d2s_miller.sym', 'd2s_lc2')
    copy_sym('d2s_miller.sym', 'd2s_lc2_nc')
    copy_sym('d2s_bias.sym', 'd2s_bias_lp')
    copy_sym('d2s_miller_biased.sym', 'd2s_mpdda_biased')
    copy_sym('d2s_miller.sym', 'd2s_mpdda_flat')
    strip_sym('d2s_miller.sym', 'd2s_mpdda_bias_flat', BIASN)
    d2s_mpdda()
    d2s_mpdda_flat()
    d2s_mpdda_bias_flat()
    d2s_lc2(True)
    d2s_lc2(False)
    d2s_bias_lp()
    fixture()
    bad = 0
    for name, err, cross in report:
        print(f'{name}: {len(err)} lint errors, {cross} wire crossings')
        for e in err:
            print('   ', e)
        bad += len(err)
    sys.exit(1 if bad else 0)
