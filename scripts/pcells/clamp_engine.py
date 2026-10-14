# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Geometry engine for the parametrized sg13cmos5l ESD clamps (Clamp_N / Clamp_P).
#
# The reference cells sg13cmos5l_Clamp_{N,P}{2,8,15}N{..}D and ..._{N,P}20N0D of the
# IHP sg13cmos5l_io library (Copyright 2024 IHP PDK Authors, Apache-2.0) are flat
# layouts. Analysing them shows three kinds of content:
#
#   frame  - guard rings, wells, ring contacts: identical in every cell of a family
#            (per gate-tie variant), stored as extracted geometry in clamp_refdata.py
#   array  - the finger array, the source/drain straps and the gate bus: strictly
#            rule based; generated here from the rules below
#   tie    - the hand-drawn gate tie-off: an antenna diode + M2 'gate' strap ("D"
#            cells) or an rppd resistor to the rail ("0D" cells). Stored per reference
#            cell as extracted geometry; for "D" it is re-placed at an x position that
#            is piecewise-linearly interpolated in ng between the reference cells.
#
# Everything here is pure Python in integer nanometres (dbu = 1 nm, 5 nm grid) so the
# same code drives the KLayout PyCells (Clamp_N_code.py / Clamp_P_code.py), the batch
# generator (gen_clamp.py) and the XOR verification (verify_clamp.py).
#
# The section at the end (generate_m1) builds the M1-only variants Clamp_N_M1 /
# Clamp_P_M1 from the same array rules: no M2/M3, no tie block, variable gate
# length, guard rings that wrap the array or form the fixed 80 um frame.
#
# Shapes are tuples  (layer, purpose, kind, data)
#   kind 'box'  : data = (x1, y1, x2, y2)
#   kind 'poly' : data = ((x, y), (x, y), ...)
# Texts are tuples   (layer, purpose, string, x, y, size, halign, valign, orient)

GRID = 5          # nm, manufacturing grid
XC = 40000        # every clamp is 80 um wide and centred on x = 40 um

# ----------------------------------------------------------------------------------
# Per-family rules, measured from the reference layouts (all values in nm)
# ----------------------------------------------------------------------------------
L_GATE = 600       # hv gate length
DRAIN = 1180       # drain diffusion between two gates (ESD ballast side)
SOURCE = 640       # inner source diffusion between two gates
SOURCE_END = 470   # source diffusion at the array ends
PAIR = 2 * L_GATE + DRAIN + SOURCE          # 3020 nm: pitch of a gate pair
END_COL = 150      # contact column at the array end sits 150 nm inside the active edge

CONT = 160
VIA = 190

FAMILY = {
    'N': dict(
        height=9900,
        model='sg13_hv_nmos',
        w_finger=4400,                               # per finger per device row
        n_dev=1,                                     # MN0
        act_rows=((2750, 7150),),
        sd_m1_rows=((2750, 7150),),
        cont_rows=(tuple(2830 + 340 * k for k in range(13)),),
        drain_via1_rows=(tuple(2805 + 410 * k for k in range(11)),),
        src_via1_extra=(1875, 7835),                 # ties the source straps to the inner ring
        via2_rows=tuple(140 + 410 * k for k in range(24)),
        m2_src=(0, 9900), m3_src=(90, 9810), m2_drain=(2755, 9900),
        poly=(2380, 7520), gate_cont=(2450, 7290), gate_m1=(2370, 7370),
        bus=(7370, 7530), riser_bottom=6500,
        tgo={'D': (2410, 7490), '0D': (2460, 7490)},
        nwell=None, psd=None,
        pad_label_y=6328, gate_label_y=8282,
    ),
    'P': dict(
        height=19260,
        model='sg13_hv_pmos',
        w_finger=6660,
        n_dev=2,                                     # MP0 (lower row) + MP1 (upper row)
        act_rows=((2750, 9410), (9850, 16510)),
        sd_m1_rows=((2860, 9300), (9960, 16400)),
        cont_rows=(tuple(2940 + 340 * k for k in range(19)),
                   tuple(10040 + 340 * k for k in range(19))),
        drain_via1_rows=(tuple(3115 + 410 * k for k in range(15)),
                         tuple(10215 + 410 * k for k in range(15))),
        src_via1_extra=(1875, 17195),
        via2_rows=tuple(105 + 410 * k for k in range(47)),
        m2_src=(0, 19260), m3_src=(55, 19205), m2_drain=(3065, 19260),
        poly=(2380, 16880), gate_cont=(2450, 9550, 16650), gate_m1=(2370, 16730),
        bus=(16730, 16890), riser_bottom=15860,
        tgo={'D': (2410, 16850), '0D': (2410, 16850)},
        nwell=(620, 2130, 17130), psd=(180, 2350, 16910),
        pad_label_y=11163, gate_label_y=17643,
    ),
}

# "0D" cells: the gate bus runs right to the rppd, whose left terminal edge is here
BUS_END_0D = 66635
# Minimum clearance kept between the finger array (incl. P well) and the tie block
MIN_CLEAR = 2000
# The array must stay inside the inner guard ring (inner edge of its active at 2.14 um)
RING_INNER_X = 2140


class ClampError(ValueError):
    pass


def snap(v, grid=GRID):
    return int(round(v / grid)) * grid


def cell_name(family, ng, tie):
    """Cell name following IHP's convention: <F><fingers>N<driven fingers>D."""
    return 'sg13cmos5l_Clamp_%s%dN%dD' % (family, ng, ng if tie == 'D' else 0)


# ----------------------------------------------------------------------------------
# Array geometry
# ----------------------------------------------------------------------------------
def array_extent(ng, l=L_GATE, x0=None):
    """Active x extent of the finger array. Length is 0.30 um + (l + 0.91 um) * ng for
    both parities (odd ng ends in a 0.74 um drain instead of a 0.47 um source); for the
    IHP cells (l = 0.6 um) that is 0.30 + 1.51 * ng. Centred on XC unless the left
    edge x0 is given (the M1-only variants, clamp_m1_engine.py)."""
    n = 2 * SOURCE_END - SOURCE + ng * (l + (DRAIN + SOURCE) // 2)
    if x0 is None:
        x0 = XC - n // 2
    return x0, x0 + n


def gate_lefts(ng, l=L_GATE, x0=None):
    xa0, _ = array_extent(ng, l, x0)
    pair = 2 * l + DRAIN + SOURCE          # = PAIR for l = L_GATE
    return [xa0 + SOURCE_END + (i // 2) * pair + (i % 2) * (l + DRAIN) for i in range(ng)]


def columns(ng, l=L_GATE, x0=None):
    """(source_centres, drain_centres) of the contact columns."""
    xa0, xa1 = array_extent(ng, l, x0)
    g = gate_lefts(ng, l, x0)
    src = [xa0 + END_COL]
    drn = []
    for i in range(0, ng, 2):
        if i + 1 < ng:
            drn.append(g[i] + l + DRAIN // 2)
            if i + 2 < ng:
                src.append(g[i + 1] + l + SOURCE // 2)
    if ng % 2 == 0:
        src.append(xa1 - END_COL)
    else:
        drn.append(xa1 - END_COL)
    return src, drn


def _box(shapes, layer, purpose, x1, y1, x2, y2):
    shapes.append((layer, purpose, 'box', (x1, y1, x2, y2)))


def array_shapes(family, tie, ng):
    f = FAMILY[family]
    s = []
    xa0, xa1 = array_extent(ng)
    src, drn = columns(ng)
    g = gate_lefts(ng)

    for (y0, y1) in f['act_rows']:
        _box(s, 'Activ', 'drawing', xa0, y0, xa1, y1)
    ty0, ty1 = f['tgo'][tie]
    _box(s, 'ThickGateOx', 'drawing', xa0 - 340, ty0, xa1 + 340, ty1)
    if f['nwell']:
        d, y0, y1 = f['nwell']
        _box(s, 'NWell', 'drawing', xa0 - d, y0, xa1 + d, y1)
    if f['psd']:
        d, y0, y1 = f['psd']
        _box(s, 'pSD', 'drawing', xa0 - d, y0, xa1 + d, y1)

    def contacts(xc):
        for row in f['cont_rows']:
            for y in row:
                _box(s, 'Cont', 'drawing', xc - CONT // 2, y, xc + CONT // 2, y + CONT)

    for xc in src:
        contacts(xc)
        for (y0, y1) in f['sd_m1_rows']:
            _box(s, 'Metal1', 'drawing', xc - 105, y0, xc + 105, y1)
        ys = [f['src_via1_extra'][0]] + [y for r in f['drain_via1_rows'] for y in r] + [f['src_via1_extra'][1]]
        for y in ys:
            _box(s, 'Via1', 'drawing', xc - VIA // 2, y, xc + VIA // 2, y + VIA)
        _box(s, 'Metal2', 'drawing', xc - 100, f['m2_src'][0], xc + 100, f['m2_src'][1])
        for y in f['via2_rows']:
            _box(s, 'Via2', 'drawing', xc - VIA // 2, y, xc + VIA // 2, y + VIA)
        _box(s, 'Metal3', 'drawing', xc - 100, f['m3_src'][0], xc + 100, f['m3_src'][1])

    for xc in drn:
        contacts(xc)
        for (y0, y1) in f['sd_m1_rows']:
            _box(s, 'Metal1', 'drawing', xc - 310, y0, xc + 310, y1)
        for r in f['drain_via1_rows']:
            for y in r:
                for dx in (-205, 205):
                    _box(s, 'Via1', 'drawing', xc + dx - VIA // 2, y, xc + dx + VIA // 2, y + VIA)
        for purpose in ('drawing', 'pin'):
            _box(s, 'Metal2', purpose, xc - 305, f['m2_drain'][0], xc + 305, f['m2_drain'][1])

    for gl in g:
        gc = gl + L_GATE // 2
        _box(s, 'GatPoly', 'drawing', gl, f['poly'][0], gl + L_GATE, f['poly'][1])
        for y in f['gate_cont']:
            _box(s, 'Cont', 'drawing', gc - CONT // 2, y, gc + CONT // 2, y + CONT)
        _box(s, 'Metal1', 'drawing', gc - 80, f['gate_m1'][0], gc + 80, f['gate_m1'][1])
    return s


def bus_shapes(family, tie, ng, xs=None):
    """Horizontal M1 gate bus over the gate heads; for 'D' plus the riser down to the
    antenna diode at strap position xs."""
    f = FAMILY[family]
    g = gate_lefts(ng)
    by0, by1 = f['bus']
    s = []
    if tie == 'D':
        x_right = g[-1] + L_GATE // 2 + 80
        _box(s, 'Metal1', 'drawing', xs - 105, by0, x_right, by1)
        _box(s, 'Metal1', 'drawing', xs - 105, f['riser_bottom'], xs + 105, by0)
    else:
        x_left = g[0] + L_GATE // 2 - 80
        _box(s, 'Metal1', 'drawing', x_left, by0, BUS_END_0D, by1)
    return s


def rule_texts(family, tie, ng, xs=None):
    """One 'pad' label per drain strap. (The reference cells carry extra, arbitrarily
    placed 'pad' labels on some straps; they are cosmetic and not reproduced.)"""
    f = FAMILY[family]
    _, drn = columns(ng)
    return [('Metal2', 'text', 'pad', xc, f['pad_label_y'], 0, 'center', 'center', 'R0') for xc in drn]


# ----------------------------------------------------------------------------------
# Interpolation over the reference cells
# ----------------------------------------------------------------------------------
def interp(points, x):
    """Piecewise linear through sorted (x, y) points, linear extrapolation at the ends."""
    pts = sorted(points)
    if len(pts) == 1:
        return pts[0][1]
    if x <= pts[0][0]:
        (x0, y0), (x1, y1) = pts[0], pts[1]
    elif x >= pts[-1][0]:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
    else:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1:
                break
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def nearest_ref(refs, ng):
    """Reference ng closest to ng; ties go to the larger reference (larger diode)."""
    return min(refs, key=lambda r: (abs(r - ng), -r))


def expand(items, dx=0):
    """Expand stored geometry items (see clamp_refdata.py) into shapes."""
    out = []
    for lay, pur, kind, d in items:
        if kind == 'box':
            x1, y1, x2, y2 = d
            out.append((lay, pur, 'box', (x1 + dx, y1, x2 + dx, y2)))
        elif kind == 'poly':
            out.append((lay, pur, 'poly', tuple((x + dx, y) for x, y in d)))
        elif kind == 'array':   # x0, y0, w, h, nx, ny, px, py
            x0, y0, w, h, nx, ny, px, py = d
            for j in range(ny):
                for i in range(nx):
                    x = x0 + dx + i * px
                    y = y0 + j * py
                    out.append((lay, pur, 'box', (x, y, x + w, y + h)))
        else:
            raise ClampError('unknown item kind %r' % kind)
    return out


def shift_texts(texts, dx=0):
    return [(l, p, t, x + dx, y, sz, ha, va, o) for (l, p, t, x, y, sz, ha, va, o) in texts]


def _bbox(shapes):
    xs, ys = [], []
    for _, _, kind, d in shapes:
        if kind == 'box':
            xs += [d[0], d[2]]
            ys += [d[1], d[3]]
        else:
            xs += [p[0] for p in d]
            ys += [p[1] for p in d]
    return min(xs), min(ys), max(xs), max(ys)


def plan(family, ng, tie, refdata):
    """Resolve everything that depends on the reference data: strap position, tie
    template, decor, limits. Returns a dict that fully determines the cell."""
    if family not in FAMILY:
        raise ClampError('family must be N or P')
    if tie not in ('D', '0D'):
        raise ClampError("tie must be 'D' or '0D'")
    ng = int(ng)
    if ng < 1:
        raise ClampError('ng must be >= 1')
    fam = refdata[family][tie]
    refs = fam['refs']
    r = nearest_ref(refs, ng)
    ref = refs[r]
    if tie == 'D':
        # tie geometry is stored relative to the strap x of its reference cell
        xs = snap(interp([(k, v['xs']) for k, v in refs.items()], ng))
        dx = xs
    else:
        xs = None
        dx = 0
    tie_shapes = expand(ref['tie'], dx)
    p = dict(family=family, tie=tie, ng=ng, ref_ng=r, ref_cell=ref['cell'], xs=xs,
             interpolated=(ng not in refs),
             inside=(min(refs) <= ng <= max(refs)),
             tie_shapes=tie_shapes, tie_texts=shift_texts(ref['tie_texts'], dx),
             decor=expand(ref['decor']), decor_texts=list(ref['decor_texts']),
             frame=expand(fam['frame']), netlist=ref['netlist'])
    check_limits(p)
    return p


def check_limits(p):
    f = FAMILY[p['family']]
    xa0, xa1 = array_extent(p['ng'])
    well = f['nwell'][0] if f['nwell'] else 340     # outermost array layer (well or TGO)
    lo, hi = xa0 - well, xa1 + well
    tx0, _, tx1, _ = _bbox(p['tie_shapes'])
    if lo < RING_INNER_X + MIN_CLEAR or hi > 80000 - RING_INNER_X - MIN_CLEAR:
        raise ClampError('ng=%d does not fit inside the 80 um guard ring' % p['ng'])
    if tx0 < RING_INNER_X + MIN_CLEAR or tx1 > 80000 - RING_INNER_X - MIN_CLEAR:
        raise ClampError('ng=%d: the extrapolated tie block runs into the guard ring' % p['ng'])
    if p['tie'] == 'D' and lo - tx1 < MIN_CLEAR:
        raise ClampError('ng=%d: finger array runs into the antenna diode block '
                         '(clearance %.2f um < %.2f um)' % (p['ng'], (lo - tx1) / 1e3, MIN_CLEAR / 1e3))
    if p['tie'] == '0D' and tx0 - hi < MIN_CLEAR:
        raise ClampError('ng=%d: finger array runs into the rppd tie-off '
                         '(clearance %.2f um < %.2f um)' % (p['ng'], (tx0 - hi) / 1e3, MIN_CLEAR / 1e3))


def max_ng(family, tie, refdata):
    ng = 1
    while True:
        try:
            plan(family, ng + 1, tie, refdata)
        except ClampError:
            return ng
        ng += 1
        if ng > 200:
            return ng


def generate(family, ng, tie, refdata):
    """Complete cell: (shapes, texts, plan)."""
    p = plan(family, ng, tie, refdata)
    shapes = (p['frame'] + array_shapes(family, tie, p['ng'])
              + bus_shapes(family, tie, p['ng'], p['xs']) + p['tie_shapes'] + p['decor'])
    texts = rule_texts(family, tie, p['ng'], p['xs']) + p['tie_texts'] + p['decor_texts']
    return shapes, texts, p


# ----------------------------------------------------------------------------------
# M1-only variant: PCells Clamp_N_M1 / Clamp_P_M1
#
# Same finger array as above (1.18 um drain / 0.64 um source between the gates,
# 0.47 um end source, 0.74 um end drain for odd ng, same contact columns, gate heads,
# M1 gate bus, ThickGateOx, P: NWell + pSD and two device rows), but
#   - nothing above Metal1: no Via1/Metal2/Via2/Metal3. The source columns run down
#     in M1 into the inner ring; the drain columns are separate M1 pins 'pad', to be
#     joined from above. In P the two device rows share one M1 column.
#   - no gate tie-off (antenna diode or rppd): the M1 gate bus is the pin 'gate'.
#   - gate length l is a parameter: the diffusion widths stay, the pitch grows with l.
#   - the guard rings keep the IHP cross-section and the whole y layout. By default
#     they wrap the array in x with the spacings the IHP cells have in y (device
#     Activ -> inner ring 0.61 um, inner ring -> outer ring 1.46 um), so the array
#     starts at x = 2.75 um as it does at y = 2.75 um, and the cell is array length
#     + 5.5 um wide. With width = 80000 the rings form IHP's fixed 80 um frame and
#     the array is centred in it, as in Clamp_N / Clamp_P.
# ----------------------------------------------------------------------------------
RING_W = 340       # ring Activ / M1 width
RING_IN = 1800     # inner ring inset from the cell edge (the outer ring has inset 0)
ARRAY_X0 = 2750    # = RING_IN + RING_W + 610
CONT_PITCH = 340

# (inset, pin name or None, [(layer, grow outside, grow inside or None = solid box)])
RINGS = {
    'N': ((RING_IN, 'iovss', [('Substrate', 0, 0), ('pSD', 180, 180)]),   # p+ substrate tap
          (0, None, [('NWell', 620, 620)])),                               # n+ tap in an NWell ring
    'P': ((RING_IN, 'iovdd', [('NWell', 620, None)]),                      # n+ tap of the PMOS well
          (0, 'iovss', [('Substrate', 0, 0), ('pSD', 180, 180)])),         # p+ substrate tap
}


def _annulus(layer, X0, Y0, X1, Y1, x0, y0, x1, y1):
    """Rectangular ring, outer box X, inner box x, drawn as one polygon with a cut
    line on the left like the IHP frame polygons."""
    return (layer, 'drawing', 'poly', ((X0, Y0), (X0, y1), (x0, y1), (x0, y0), (x1, y0), (x1, y1),
                                       (X0, y1), (X0, Y1), (X1, Y1), (X1, Y0)))


def _cont_row(a0, a1):
    """Lower edges of the contacts that fit on [a0, a1] at 340 nm pitch, centred."""
    n = (a1 - a0 - CONT) // CONT_PITCH + 1
    start = a0 + (a1 - a0 - CONT - (n - 1) * CONT_PITCH) // 2 // GRID * GRID
    return [start + k * CONT_PITCH for k in range(n)]


def generate_m1(family, ng, l, width=None):
    """Complete M1-only clamp: (shapes, texts). l = gate length in nm.
    width = None: rings wrap the array; else fixed cell width in nm (80000 as IHP),
    array centred (on the 5 nm grid)."""
    f = FAMILY[family]
    if ng < 1:
        raise ClampError('ng must be >= 1')
    if l % GRID:
        raise ClampError('l = %d nm is not on the %d nm grid' % (l, GRID))
    n = array_extent(ng, l, 0)[1]                     # active length of the array
    if width is None:
        x0, W = ARRAY_X0, n + 2 * ARRAY_X0
    else:
        x0, W = (width - n) // (2 * GRID) * GRID, width
        if x0 < ARRAY_X0:
            raise ClampError('ng = %d, l = %d nm: array (%.2f um) does not fit in the %.0f um frame'
                             % (ng, l, n / 1e3, width / 1e3))
    xa0, xa1 = array_extent(ng, l, x0)
    H = f['height']
    src, drn = columns(ng, l, x0)
    s, t = [], []

    # finger array
    for (y0, y1) in f['act_rows']:
        _box(s, 'Activ', 'drawing', xa0, y0, xa1, y1)
    ty0, ty1 = f['tgo']['D']
    _box(s, 'ThickGateOx', 'drawing', xa0 - 340, ty0, xa1 + 340, ty1)
    if f['nwell']:
        d, y0, y1 = f['nwell']
        _box(s, 'NWell', 'drawing', xa0 - d, y0, xa1 + d, y1)
    if f['psd']:
        d, y0, y1 = f['psd']
        _box(s, 'pSD', 'drawing', xa0 - d, y0, xa1 + d, y1)

    sd_y0, sd_y1 = f['sd_m1_rows'][0][0], f['sd_m1_rows'][-1][1]
    for xc in src + drn:
        for row in f['cont_rows']:
            for y in row:
                _box(s, 'Cont', 'drawing', xc - CONT // 2, y, xc + CONT // 2, y + CONT)
    for xc in src:                        # down into the inner ring
        _box(s, 'Metal1', 'drawing', xc - 105, RING_IN, xc + 105, sd_y1)
    for xc in drn:
        for purpose in ('drawing', 'pin'):
            _box(s, 'Metal1', purpose, xc - 310, sd_y0, xc + 310, sd_y1)
        t.append(('Metal1', 'text', 'pad', xc, f['pad_label_y'], 0, 'center', 'center', 'R0'))

    g = gate_lefts(ng, l, x0)
    dx = (l - CONT) // 2 // GRID * GRID   # gate contact and M1 strip inside the gate (220 for l = 600)
    for gl in g:
        _box(s, 'GatPoly', 'drawing', gl, f['poly'][0], gl + l, f['poly'][1])
        for y in f['gate_cont']:
            _box(s, 'Cont', 'drawing', gl + dx, y, gl + dx + CONT, y + CONT)
        _box(s, 'Metal1', 'drawing', gl + dx, f['gate_m1'][0], gl + dx + CONT, f['gate_m1'][1])
    bx0, bx1 = g[0] + dx, g[-1] + dx + CONT
    by0, by1 = f['bus']
    for purpose in ('drawing', 'pin'):
        _box(s, 'Metal1', purpose, bx0, by0, bx1, by1)
    t.append(('Metal1', 'text', 'gate', (bx0 + bx1) // 2 // GRID * GRID, (by0 + by1) // 2, 0, 'center', 'center', 'R0'))

    # guard rings
    for inset, net, extra in RINGS[family]:
        X0, Y0, X1, Y1 = inset, inset, W - inset, H - inset
        x0, y0, x1, y1 = X0 + RING_W, Y0 + RING_W, X1 - RING_W, Y1 - RING_W
        for lay in ('Activ', 'Metal1'):
            s.append(_annulus(lay, X0, Y0, X1, Y1, x0, y0, x1, y1))
        for lay, go, gi in extra:
            if gi is None:
                _box(s, lay, 'drawing', X0 - go, Y0 - go, X1 + go, Y1 + go)
            else:
                s.append(_annulus(lay, X0 - go, Y0 - go, X1 + go, Y1 + go, x0 + gi, y0 + gi, x1 - gi, y1 - gi))
        for x in _cont_row(X0 + 90, X1 - 90):                     # bottom and top side
            for y in (Y0 + 90, Y1 - 90 - CONT):
                _box(s, 'Cont', 'drawing', x, y, x + CONT, y + CONT)
        for y in _cont_row(y0 + 180, y1 - 180):                   # left and right side
            for x in (X0 + 90, X1 - 90 - CONT):
                _box(s, 'Cont', 'drawing', x, y, x + CONT, y + CONT)
        if net:
            _box(s, 'Metal1', 'pin', X0, Y0, X1, y0)              # bottom side
            t.append(('Metal1', 'text', net, (X0 + X1) // 2 // GRID * GRID, Y0 + RING_W // 2,
                      0, 'center', 'center', 'R0'))
        if 'Substrate' in [e[0] for e in extra]:
            t.append(('TEXT', 'drawing', 'sub!', X0 + 170, Y0 + 170, 0, None, None, 'R0'))
    return s, t
