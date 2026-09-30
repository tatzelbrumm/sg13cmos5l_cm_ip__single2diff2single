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
# Shapes are tuples  (layer, purpose, kind, data)
#   kind 'box'  : data = (x1, y1, x2, y2)
#   kind 'poly' : data = ((x, y), (x, y), ...)
# Texts are tuples   (layer, purpose, string, x, y, size, halign, valign, orient)

#
# ANNOTATED COPY (2026-09-30) of scripts/pcells/clamp_engine.py. The code is unchanged: its
# syntax tree is identical to the original's. Only comments were added.
#
# WHERE THIS FILE SITS
#   No imports. Called from these files of scripts/pcells/, with these names:
#     clamp_base_code.py         generate, cell_name, FAMILY, ClampError   the PCells
#     gen_clamp.py               generate, cell_name, max_ng               batch GDS/CDL/SPICE
#     verify_clamp.py            generate, cell_name, max_ng, columns, FAMILY   XOR vs IHP, sweep
#     clamp_netlist.py           plan, cell_name, FAMILY                   CDL / ngspice
#     lvs_clamp.py               FAMILY                                    expected device W
#     extract_clamp_refdata.py   array_shapes, bus_shapes, FAMILY          writes clamp_refdata.py
#
#   The last line is the tight coupling. clamp_refdata.py (REFDATA) holds what is left of
#   IHP's eight reference cells after subtracting what array_shapes() + bus_shapes() draw
#   (extract_clamp_refdata.py:230-249). A generated cell is REFDATA + those two functions
#   again, so the two are complementary halves: change the array or bus rules and
#   clamp_refdata.py has to be regenerated, or shapes come out doubled or missing.
#
#   The shape and text tuple formats above are the interface in both directions:
#     out: clamp_base_code.genLayout (PCell path) and clamp_klayout.write_cell (batch path)
#          consume them;
#     in:  REFDATA items use the same format plus kind 'array', which expand() unpacks.
#
# ---------------------------------------------------------------------------------------
# GRID: read only by snap() (xs interpolation). XC: read only by array_extent(); the
# REFDATA frame is centred on the same x, so only the array needs to be told.
GRID = 5          # nm, manufacturing grid
XC = 40000        # every clamp is 80 um wide and centred on x = 40 um

# ----------------------------------------------------------------------------------
# Per-family rules, measured from the reference layouts (all values in nm)
# ----------------------------------------------------------------------------------
# Every x in the finger array follows from these and ng (y comes from FAMILY below).
# Readers: L_GATE gate_lefts, columns, array_shapes, bus_shapes; DRAIN gate_lefts, columns;
# SOURCE columns; SOURCE_END, PAIR gate_lefts; END_COL columns.
L_GATE = 600       # hv gate length
DRAIN = 1180       # drain diffusion between two gates (ESD ballast side)
SOURCE = 640       # inner source diffusion between two gates
SOURCE_END = 470   # source diffusion at the array ends
PAIR = 2 * L_GATE + DRAIN + SOURCE          # 3020 nm: pitch of a gate pair
END_COL = 150      # contact column at the array end sits 150 nm inside the active edge

# Cut sizes for array_shapes() only. Cuts that come from REFDATA (ring contacts, diode,
# rppd heads) carry their own sizes.
CONT = 160
VIA = 190

# The per-family rule set; the key is the class attribute FAMILY of Clamp_N / Clamp_P.
# Which key is read where:
#   array_shapes   act_rows sd_m1_rows cont_rows drain_via1_rows src_via1_extra via2_rows
#                  m2_src m3_src m2_drain poly gate_cont gate_m1 tgo nwell psd
#   bus_shapes     bus riser_bottom
#   rule_texts     pad_label_y
#   check_limits   nwell (outermost array layer)
#   model          clamp_base_code.py (default of the inert PCell parameter), clamp_netlist.py
#   w_finger, n_dev   clamp_netlist.py, lvs_clamp.py, verify_clamp.py (not the layout)
#   height         extract_clamp_refdata.py only (finding the M2 gate strap)
#   gate_label_y   nothing (the 'gate' label comes from REFDATA tie_texts)
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
# bus_shapes(), 0D only. The rppd the bus runs to is not drawn here: it is the REFDATA
# 0D tie block, which is not moved, so this x and that block stay aligned.
BUS_END_0D = 66635
# Minimum clearance kept between the finger array (incl. P well) and the tie block
# MIN_CLEAR and RING_INNER_X are read only by check_limits(); through it they decide
# max_ng() and every ClampError about fit.
MIN_CLEAR = 2000
# The array must stay inside the inner guard ring (inner edge of its active at 2.14 um)
RING_INNER_X = 2140


# Raised by plan, check_limits, expand. clamp_base_code.genLayout re-raises it as a plain
# Exception, which cni PCellWrapper.produce prints (cell stays empty); max_ng() uses it as
# its stop signal.
class ClampError(ValueError):
    pass


# Caller: plan() (the interpolated strap position xs).
# IN:    v      number, nm
#        grid   int, nm (default GRID)
# OUT:   int, nm: v rounded to the nearest multiple of grid
# CALLS: round, int (Python built-ins)
def snap(v, grid=GRID):
    return int(round(v / grid)) * grid


# Not used for geometry. Callers: clamp_base_code.py (the inert 'cellName' property),
# clamp_netlist.py (subcircuit names), gen_clamp.py (file names), verify_clamp.py (to find
# the matching IHP cell in sg13cmos5l_io.gds).
# IN:    family 'N' | 'P'
#        ng     int
#        tie    'D' | '0D'
# OUT:   str, IHP-style cell name, e.g. 'sg13cmos5l_Clamp_N15N15D'
# CALLS: none
def cell_name(family, ng, tie):
    """Cell name following IHP's convention: <F><fingers>N<driven fingers>D."""
    return 'sg13cmos5l_Clamp_%s%dN%dD' % (family, ng, ng if tie == 'D' else 0)


# ----------------------------------------------------------------------------------
# Array geometry
# ----------------------------------------------------------------------------------
# The only place ng sets the array's x size. Callers: gate_lefts, columns, array_shapes,
# check_limits.
# IN:    ng     int
# OUT:   (xa0, xa1) ints, nm: left and right x of the array active
# CALLS: none
def array_extent(ng):
    """Active x extent of the finger array. Length is 0.30 um + 1.51 um * ng for both
    parities (odd ng ends in a 0.74 um drain instead of a 0.47 um source)."""
    half = 150 + 755 * ng
    return XC - half, XC + half


# Callers: columns, array_shapes, bus_shapes.
# IN:    ng     int
# OUT:   list of ng ints, nm: left x of each gate, left to right
# CALLS: array_extent
#        range (built-in)
def gate_lefts(ng):
    xa0, _ = array_extent(ng)
    return [xa0 + SOURCE_END + (i // 2) * PAIR + (i % 2) * (L_GATE + DRAIN) for i in range(ng)]


# Callers: array_shapes (contacts, straps), rule_texts (one 'pad' label per drain column),
# verify_clamp.py (expected number of separate M2 straps).
# IN:    ng     int
# OUT:   (src, drn): two lists of ints, nm: x centres of the source and of the drain contact columns
# CALLS: array_extent, gate_lefts
#        range, list.append (built-ins)
def columns(ng):
    """(source_centres, drain_centres) of the contact columns."""
    xa0, xa1 = array_extent(ng)
    g = gate_lefts(ng)
    src = [xa0 + END_COL]
    drn = []
    for i in range(0, ng, 2):
        if i + 1 < ng:
            drn.append(g[i] + L_GATE + DRAIN // 2)
            if i + 2 < ng:
                src.append(g[i + 1] + L_GATE + SOURCE // 2)
    if ng % 2 == 0:
        src.append(xa1 - END_COL)
    else:
        drn.append(xa1 - END_COL)
    return src, drn


# Appends one shape tuple in the format of the header; used by array_shapes, bus_shapes.
# IN:    shapes list, extended in place
#        layer, purpose  str, names as in the PDK .lyp
#        x1, y1, x2, y2  ints, nm
# OUT:   None; appends one (layer, purpose, 'box', (x1, y1, x2, y2)) tuple to shapes
# CALLS: list.append (built-in)
def _box(shapes, layer, purpose, x1, y1, x2, y2):
    shapes.append((layer, purpose, 'box', (x1, y1, x2, y2)))


# Two callers with opposite purposes:
#   generate()                          draws it into every cell;
#   extract_clamp_refdata.py:230        subtracts it from IHP's cells, so nothing drawn here
#                                       is stored in REFDATA.
# The P-family NWell drawn here lies inside the NWell box of the REFDATA frame; extract kept
# it there (extract_clamp_refdata.py:237-248) instead of punching a hole into the frame.
# IN:    family 'N' | 'P'
#        tie    'D' | '0D' (selects the ThickGateOx extent)
#        ng     int
# OUT:   list of shape tuples: active, implants, wells, contacts, Metal1-3, vias, gates of the finger array
# CALLS: array_extent, columns, gate_lefts, _box
#        contacts(xc): local helper defined inside this function, appends one column of contact boxes
#        range (built-in)
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


# Same two callers as array_shapes. For D, xs comes from plan(). The riser drawn here ends
# on the diode stored in REFDATA tie; the Metal1 stored there is the diode's Metal1 minus
# this riser (in P2 and P8 only two thin slivers are left).
# IN:    family 'N' | 'P'
#        tie    'D' | '0D'
#        ng     int
#        xs     int, nm: strap x from plan(); used only for 'D'
# OUT:   list of shape tuples: the Metal1 gate bus, plus the riser for D
# CALLS: gate_lefts, _box
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


# extract_clamp_refdata.py dropped IHP's own 'pad' labels (extract :295-296), so these are
# the only 'pad' labels in a generated cell. All other labels come from REFDATA.
# IN:    family 'N' | 'P'
#        tie    'D' | '0D' (unused)
#        ng     int
#        xs     (unused)
# OUT:   list of text tuples: one 'pad' label per drain column
# CALLS: columns
def rule_texts(family, tie, ng, xs=None):
    """One 'pad' label per drain strap. (The reference cells carry extra, arbitrarily
    placed 'pad' labels on some straps; they are cosmetic and not reproduced.)"""
    f = FAMILY[family]
    _, drn = columns(ng)
    return [('Metal2', 'text', 'pad', xc, f['pad_label_y'], 0, 'center', 'center', 'R0') for xc in drn]


# ----------------------------------------------------------------------------------
# Interpolation over the reference cells
# ----------------------------------------------------------------------------------
# Caller: plan(), with the (ng, xs) pairs of the D reference cells in REFDATA.
# IN:    points iterable of (x, y) pairs; here (reference ng, reference xs)
#        x      number; here ng
# OUT:   float: y at x, piecewise linear, linear extrapolation outside the points
# CALLS: sorted, len, zip (built-ins)
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


# Caller: plan(). Picks which reference cell's tie block, decor and netlist values are
# copied. For D this is where the diode size switches (P: 0.48 um diode from P2 and P8,
# 0.78 um from P15; N: 0.78 um throughout).
# IN:    refs   dict keyed by reference ng (REFDATA[...][...]['refs']); only the keys are used
#        ng     int
# OUT:   int: the reference ng closest to ng (ties: the larger one)
# CALLS: min, abs (built-ins)
def nearest_ref(refs, ng):
    """Reference ng closest to ng; ties go to the larger reference (larger diode)."""
    return min(refs, key=lambda r: (abs(r - ng), -r))


# Converts REFDATA items into shape tuples. Kind 'array' is the packing that
# extract_clamp_refdata.encode() (extract :104-155) applied to small square cuts.
# dx: xs for D tie blocks (stored relative to xs), 0 otherwise. Caller: plan().
# IN:    items  list of REFDATA items (kinds box, poly, array)
#        dx     int, nm: x shift applied to every item
# OUT:   list of shape tuples (kinds box, poly only)
# CALLS: ClampError (raised for an unknown kind)
#        tuple, range, list.append (built-ins)
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


# The text counterpart of expand(dx); caller: plan().
# IN:    texts  list of text tuples
#        dx     int, nm
# OUT:   list of text tuples, x shifted by dx
# CALLS: none
def shift_texts(texts, dx=0):
    return [(l, p, t, x + dx, y, sz, ha, va, o) for (l, p, t, x, y, sz, ha, va, o) in texts]


# Caller: check_limits (extent of the tie block).
# IN:    shapes list of shape tuples (kinds box, poly)
# OUT:   (xmin, ymin, xmax, ymax) ints, nm
# CALLS: min, max (built-ins)
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


# The only function that reads REFDATA (passed in as refdata). Keys read:
#   refdata[family][tie]['frame'], ['refs'], and per reference 'cell', 'xs', 'tie',
#   'tie_texts', 'decor', 'decor_texts', 'netlist'.
# Callers: generate (and through it the PCells, gen_clamp, verify_clamp), max_ng,
# clamp_netlist.py (reads 'netlist' and 'ng' of the returned dict).
# IN:    family 'N' | 'P'
#        ng     int (or anything int() accepts)
#        tie    'D' | '0D'
#        refdata  REFDATA from clamp_refdata.py
# OUT:   dict p: family, tie, ng, ref_ng, ref_cell, xs, interpolated, inside, tie_shapes, tie_texts,
#                decor, decor_texts, frame, netlist
#        raises ClampError for bad arguments or when the cell does not fit (via check_limits)
# CALLS: nearest_ref, interp, snap, expand, shift_texts, check_limits, ClampError
#        int, min, max, dict, list, dict.items (built-ins)
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


# Caller: plan(). Its failures are what max_ng() counts up to.
# IN:    p      the dict built by plan()
# OUT:   None; raises ClampError if the array or the tie block does not fit
# CALLS: array_extent, _bbox, ClampError
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


# Not used by the PCells. Callers: gen_clamp.py (--limits), verify_clamp.py (sweep range).
# IN:    family 'N' | 'P'
#        tie    'D' | '0D'
#        refdata  REFDATA
# OUT:   int: the largest ng for which plan() raises no ClampError (capped at 201)
# CALLS: plan
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


# Callers: clamp_base_code.genLayout (PCells), gen_clamp.py, verify_clamp.py.
# The cell = REFDATA parts (frame, tie, decor, their texts) + rule parts (array, bus,
# 'pad' labels). List order = insertion order; it does not affect the geometry.
# IN:    family 'N' | 'P'
#        ng     int
#        tie    'D' | '0D'
#        refdata  REFDATA
# OUT:   (shapes, texts, p): list of shape tuples, list of text tuples, the plan() dict
# CALLS: plan, array_shapes, bus_shapes, rule_texts
def generate(family, ng, tie, refdata):
    """Complete cell: (shapes, texts, plan)."""
    p = plan(family, ng, tie, refdata)
    shapes = (p['frame'] + array_shapes(family, tie, p['ng'])
              + bus_shapes(family, tie, p['ng'], p['xs']) + p['tie_shapes'] + p['decor'])
    texts = rule_texts(family, tie, p['ng'], p['xs']) + p['tie_texts'] + p['decor_texts']
    return shapes, texts, p
