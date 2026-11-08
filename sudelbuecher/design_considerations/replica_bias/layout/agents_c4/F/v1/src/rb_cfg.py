# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent F (C4, 2026-11-07): pad_ref_rb for generator.py (C2's two-metal grid router, copied unchanged from
# C3 F). Placement = the table PLACE (lower left of each oriented bounding box, cell coordinates of pad_ref_rb);
# frame_f (make_frame.py) holds the prBoundary and the two supply rails vssh / vddh on the left edge.
import os

import klayout.db as db

C = os.environ['FCELLS']                      # cells built by F (frame, _f copies)
I = os.environ['FINPUTS']                     # the read-only inputs
NAME = 'pad_ref_rb'
PROCESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ihp_sg13cmos5l.py')
# P3 before P: P's superseded rb_avg is then the renamed copy (rb_avg$1) and is dropped as unused
SOURCES = {'frame': C + '/frame_f.gds', 'P3': I + '/P3/rb_avg_v3.gds', 'P': I + '/P/rb_p_cells.gds',
           'N': I + '/N/rb_n_cells.gds'}
for k, f in (('F', C + '/rb_f_cells.gds'),):
    if os.path.exists(f):
        SOURCES = dict(list(SOURCES.items())[:1] + [(k, f)] + list(SOURCES.items())[1:])

SUP = {'vdd': 'vddh', 'vss': 'vssh'}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rb_place.py')).read())   # PLACE, W, H, PORT_Y

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
for inst, cell, o, x, y in PLACE:
    INSTANCES[inst] = dict(cell=cell, o=o, nets=dict(SUP, **NETMAP.get(inst, {})))
    b = _cell(cell)[1].dbbox().transformed(db.DTrans(ORI[o], 0, 0))
    lines.append('  cell %s o=%s at=%.4f,%.4f' % (inst, o, x - b.left, y - b.bottom))
FLOORPLAN = '\n'.join(lines) + '\n'

SIGNAL = ['ts', 'bt', 'vbp', 'ni', 'iref', 'en_3v3', 'en_3v3_b', 'vbnc', 'gh', 'm', 'xp', 'bd', 'vcm', 'vref']
POWER = ['vddh', 'vssh']
NETS = SIGNAL + POWER
# signal pins on Metal2 at the right edge, bottom to top in the slot boundary's order, PORT_P apart
PORTS = {n: ('right', (PORT_Y + PORT_P * i - 0.1, PORT_Y + PORT_P * i + 0.1))
         for i, n in enumerate(['vref', 'vcm', 'en_3v3', 'en_3v3_b', 'iref'])}


def _keepouts():
    """no router metal over any gate (C2 F2 / C3 F): every gate (Activ & GatPoly, merged, + 0.1 um) of every placed
    cell is a keep-out for all nets on Metal1 and Metal2."""
    out, seen = [], {}
    for inst, cell, o, x, y in PLACE:
        if cell == 'frame_f':
            continue
        if cell not in seen:
            ly, c = _cell(cell)
            ra = db.Region(c.begin_shapes_rec(ly.layer(1, 0)))
            rp = db.Region(c.begin_shapes_rec(ly.layer(5, 0)))
            seen[cell] = [p.bbox().to_dtype(ly.dbu) for p in (ra & rp).merged().sized(100).merged().each()]
        for b in seen[cell]:
            out.append(dict(metal=('M1', 'M2'), inst=inst, box=(b.left, b.bottom, b.right, b.top), nets=[]))
    # the port group on the right edge: each port's strip of the edge (0.7 um deep) is open to its own net only, so
    # no net runs along the edge past another's port
    names = ['vref', 'vcm', 'en_3v3', 'en_3v3_b', 'iref']
    for i, n in enumerate(names):
        y = PORT_Y + PORT_P * i
        out.append(dict(metal=('M1', 'M2'), inst='frame', box=(W - 0.7, y - 0.54, W, y + 0.54), nets=[n]))
    out.append(dict(metal=('M1', 'M2'), inst='frame', box=(W - 0.7, PORT_Y - 3.0, W, PORT_Y - 0.54), nets=[]))
    out.append(dict(metal=('M1', 'M2'), inst='frame', box=(W - 0.7, PORT_Y + 4 * PORT_P + 0.54, W, PORT_Y + 8.0), nets=[]))
    out += EXTRA_KEEPOUT
    return out


ROUTER = dict(pitch=0.27, width=0.29, margin=0.12, keepout=_keepouts())
MERGE_WELLS = True
ROUTE_ORDER = ROUTE_ORDER_PLACE
