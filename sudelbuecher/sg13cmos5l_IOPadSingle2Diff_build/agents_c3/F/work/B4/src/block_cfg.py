# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage B: s2d_block (s2d_mpdda_pd + bias_tree_noab_pd) for generator.py (C2's two-metal grid router,
# oa_core_pd_v2_2026-10-28/v2, copied unchanged into src/). Coordinates are pad coordinates of the oriented cells'
# bounding boxes (lower left); padctx_f's prBoundary (0, 26, 80, 180) fixes the block extent; the generator moves the
# block to the origin, the pad places it back at (0, 26).
import os

import klayout.db as db

C = os.environ['FCELLS']                      # cells built for the block (run_B.sh)
I = os.environ['FINPUTS']                     # the read-only inputs
NAME = 's2d_block'
PROCESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ihp_sg13cmos5l.py')
SOURCES = {'ctx': C + '/padctx_f.gds', 'pwr': C + '/pwr_f.gds', 'P': C + '/p3_router.gds', 'N': I + '/N/s2d_n3_cells.gds',
           'T': C + '/s2d_tails_f.gds', 'CN': C + '/s2d_casc_n_f.gds', 'PF': C + '/s2d_pins_f.gds'}

IOVDD_T, IOVDD_OP, IOVDD_TP = 'iovdd_t', 'iovdd_op', 'iovdd_tp'
IOVSS_SK, IOVSS_CN, IOVSS_M = 'iovss_sk', 'iovss_cn', 'iovss_m'
OUT = {'voutp': 'outp', 'voutn': 'outn'}
# (instance, cell, orientation, x, y of the oriented bbox's lower left in pad coordinates, net map)
PLACE = [
    ('ctx', 'padctx_f', 'R0', None, None, {}),
    ('pwr', 'pwr_f', 'R0', None, None, {}),
    # left pocket: the NMOS fold (sinks pins up = the delivered R90 cell turned by 180 deg = core R270)
    ('sinks', 'sinks_6x6_s2d_c3_core', 'R270', 4.30, 32.70, {'vss': IOVSS_SK}),
    ('cascn', 's2d_casc_n_f', 'R270', 22.62, 32.70, dict(OUT, vss=IOVSS_CN, vdd=IOVDD_OP)),
    # right pocket: the PMOS output stage, one NWell
    ('cascp', 's2d_casc_p_f', 'R270', 45.50, 45.60, dict(OUT, vdd=IOVDD_OP)),
    ('loads', 's2d_loads_f', 'R270', 58.31, 45.60, {'vdd': IOVDD_OP}),
    # input group
    ('tlo', 's2d_tails_lo_f', 'M0', 4.37, 110.24, {'vdd': IOVDD_T}),
    ('inputs', 's2d_inputs_c3', 'R0', 4.30, 122.40, {'vdd': IOVDD_T, 'vin': 'pad', 'vfbp': 'outp', 'vfbn': 'outn'}),
    ('thi', 's2d_tails_hi_f', 'R0', 4.37, 151.84, {'vdd': IOVDD_T}),
    ('rhigh', 's2d_rhigh_c3', 'R90', 55.50, 126.00, {'vss': IOVSS_M}),
    ('sinkc', 's2d_sinks_cmfb_c3_core', 'R90', 59.19, 91.25, {'vss': IOVSS_M}),
    # bias tree and top band
    ('treen', 'bias_tree_noab_n_c3', 'R0', 51.49, 152.30, {'vss': IOVSS_M}),
    ('treep', 'bias_tree_noab_p_c3', 'R0', 60.00, 164.30, {'vdd': IOVDD_TP}),
    ('cload', 's2d_cload_c3', 'R0', 4.30, 162.50, dict(OUT, vss=IOVSS_M)),
    ('pdp', 's2d_pd_p_c3', 'R0', 35.00, 172.30, dict(OUT, vdd=IOVDD_TP)),
]
ORI = {'R0': db.DTrans.R0, 'R90': db.DTrans.R90, 'R180': db.DTrans.R180, 'R270': db.DTrans.R270, 'M0': db.DTrans.M0,
       'M90': db.DTrans.M90}
_lys = {}


def _cell(name):
    for k, f in SOURCES.items():
        if k not in _lys:
            _lys[k] = db.Layout()
            _lys[k].read(f)
        c = _lys[k].cell(name)
        if c is not None:
            return _lys[k], c
    raise ValueError(name)


INSTANCES, lines = {}, ['FREE']
for inst, cell, o, x, y, nets in PLACE:
    INSTANCES[inst] = dict(cell=cell, o=o, nets=nets)
    if x is None:
        lines.append('  cell %s o=%s at=0,0' % (inst, o))
        continue
    b = _cell(cell)[1].dbbox().transformed(db.DTrans(ORI[o], 0, 0))
    lines.append('  cell %s o=%s at=%.4f,%.4f' % (inst, o, x - b.left, y - b.bottom))
FLOORPLAN = '\n'.join(lines) + '\n'

UNITS = ('A1', 'A2', 'F1', 'F2', 'M1', 'M2')
SIGNAL = ['s%s_%s' % (h, u) for h in 'ab' for u in UNITS] + \
    ['x', 'y', 'xc', 'yc', 'outp', 'outn', 'vcmfb', 'lp', 'ln', 'dd', 'vbp', 'vbn', 'vbpc', 'vbnc', 'ni', 'iref',
     'en_3v3', 'en_3v3_b', 'vcm', 'vref']      # pad: drawn by F (make_pwr.py, stage B2), not routed
POWER = [IOVDD_T, IOVDD_OP, IOVDD_TP, IOVSS_SK, IOVSS_CN, IOVSS_M]
NETS = SIGNAL + POWER
# core-side pins on Metal2 at the top edge (y 180), each over the cells it serves
PORTS = {'vref': ('top', (6.0, 12.0)), 'outp': ('top', (12.0, 18.0)), 'outn': ('top', (18.0, 24.0)),
         'vcm': ('top', (24.0, 30.0)), 'en_3v3': ('top', (36.0, 42.0)), 'en_3v3_b': ('top', (42.0, 48.0)),
         'iref': ('top', (52.0, 58.0))}
# the edge reserve (Christoph, 2026-11-04): no router Metal1 in x 1.8..4.3 and 75.7..78.2 above y 31.7
RESERVE = [(1.8, 31.7, 4.3, 180.0), (75.7, 31.7, 78.2, 180.0)]
Y0 = 26.0                                     # the generator moves the block down by this (padctx_f's bottom)


def _keepouts():
    """no router metal over any channel (C2 F2): every gate (Activ & GatPoly, merged, +0.1 um) of every placed cell
    is a keep-out for all nets on Metal1 and Metal2; the reserve is a keep-out for Metal1."""
    out, seen = [], {}
    for inst, cell, o, x, y, nets in PLACE:
        if x is None:
            continue
        if cell not in seen:
            ly, c = _cell(cell)
            ra = db.Region(c.begin_shapes_rec(ly.layer(1, 0)))
            rp = db.Region(c.begin_shapes_rec(ly.layer(5, 0)))
            seen[cell] = [p.bbox().to_dtype(ly.dbu) for p in (ra & rp).merged().sized(100).merged().each()]
        for b in seen[cell]:
            out.append(dict(metal=('M1', 'M2'), inst=inst, box=(b.left, b.bottom, b.right, b.top), nets=[]))
    out += [('M1', (r[0], r[1] - Y0, r[2], r[3] - Y0)) for r in RESERVE]   # top coordinates after the move
    # stage B2: no vbp on the left (Christoph: "the u shape on the left side seems avoidable"): the tail rows' left
    # ends (their left vbp stubs and gate columns) are closed to every router net; vbp reaches them from the right
    for x0, y0, x1, y1 in ((4.30, 110.24, 7.20, 119.40), (4.30, 151.84, 7.20, 161.00)):
        out += [(m, (x0, y0 - Y0, x1, y1 - Y0)) for m in ('M1', 'M2')]
    # stage B2: no router Metal1 directly under the pad line's C3a leg and its two shields (drawn in pwr_f; a first
    # run put vbn there, 30 um under the pad); nobody has to cross that leg. (Keep-outs in the tub well gap as well
    # left 7 nets unroutable: not used.)
    for m, (x0, y0, x1, y1) in (('M1', (22.73, 106.95, 49.70, 108.75)),):
        out.append((m, (x0, y0 - Y0, x1, y1 - Y0)))
    return out


ROUTER = dict(pitch=0.27, width=0.29, margin=0.12, keepout=_keepouts())
MERGE_WELLS = True
# stage B2 (pad drawn by F): found by route_block.py's reorder rounds (round 6 of the run with vbp, vbnc first)
ROUTE_ORDER = ['en_3v3_b', 'vref', 'vbpc', 'vcm', 'vbn', 'outp', 'outn', 'sb_A1', 'sb_A2', 'sb_M1', 'sa_A1', 'sa_A2',
               'sa_M1', 'sb_M2', 'sa_F1', 'sa_F2', 'sa_M2', 'sb_F1', 'sb_F2', 'yc', 'vbp', 'vbnc', 'x', 'y', 'en_3v3',
               'dd', 'ln', 'lp', 'vcmfb', 'iovdd_tp', 'xc']    # found by route_block.py's reorder rounds
