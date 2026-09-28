# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Netlists for the parametrized clamps.

cdl(...)    - LVS netlist, same conventions as sg13cmos5l_io.cdl (M/D/R devices,
              ptap1 substrate tap, bare 'sub!' bulk node).
ngspice(...) - simulation subcircuit in the formats of the PDK xschem symbols
              (sg13_hv_[np]mos, dantenna/dpantenna, ptap1, rppd are X-called
              subcircuits). 'sub!' must be global in the deck; the file written by
              gen_clamp.py starts with '.global sub!' for that reason.

Device data (antenna diode size, rppd geometry, ptap1 area/perimeter) come from
the reference cell whose tie block the layout uses, so layout and netlist agree.
"""

import math
import re

try:
    from .clamp_engine import FAMILY, cell_name, plan
except ImportError:
    from clamp_engine import FAMILY, cell_name, plan

_SI = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e3, 'K': 1e3, '': 1.0}


def si(s):
    m = re.fullmatch(r'([-+0-9.eE]+)([fpnumkK]?)', s)
    return float(m.group(1)) * _SI[m.group(2)]


def _u(v):
    """metres -> '<x>u' with no float noise"""
    return ('%.6f' % (v * 1e6)).rstrip('0').rstrip('.') + 'u'


def pins(family, tie):
    return {('N', 'D'): ['gate', 'iovss', 'pad'], ('N', '0D'): ['iovss', 'pad'],
            ('P', 'D'): ['gate', 'iovdd', 'iovss', 'pad'], ('P', '0D'): ['iovdd', 'iovss', 'pad']}[(family, tie)]


def _devices(family, ng, tie, refdata):
    p = plan(family, ng, tie, refdata)
    f = FAMILY[family]
    net = p['netlist']
    w = f['w_finger'] * 1e-9 * ng
    gate = 'gate' if tie == 'D' else 'net2'
    if family == 'N':
        mos = [('MN0', 'pad', gate, 'iovss', 'sub!')]
    else:
        mos = [('MP0', 'pad', gate, 'iovdd', 'iovdd'), ('MP1', 'pad', gate, 'iovdd', 'iovdd')]
    return p, f, net, w, mos


def cdl(family, ng, tie, refdata):
    p, f, net, w, mos = _devices(family, ng, tie, refdata)
    name = cell_name(family, p['ng'], tie)
    pl = pins(family, tie)
    out = ['.SUBCKT %s %s' % (name, ' '.join(pl)),
           '*.PININFO ' + ' '.join('%s:%s' % (x, 'I' if x == 'gate' else 'B') for x in pl)]
    for inst, d, g, s, b in mos:
        out.append('%s %s %s %s %s %s m=1 w=%s l=600.0n ng=%d' % (inst, d, g, s, b, f['model'], _u(w), p['ng']))
    t = net['ptap']
    out.append('XR0 iovss sub! ptap1 A=%s P=%s' % (t['A'], t['P']))
    if tie == 'D':
        dd = net['diode']
        a, c = ('sub!', 'gate') if family == 'N' else ('gate', 'iovdd')
        out.append('DD0 %s %s %s m=1 w=%s l=%s a=%s p=%s' % (a, c, dd['model'], dd['w'], dd['l'], dd['a'], dd['p']))
    else:
        r = net['rppd']
        n1, n2 = ('iovss', 'net2') if family == 'N' else ('net2', 'iovdd')
        out.append('RR0 %s %s %s $SUB=%s $[rppd] l=%s w=%s b=%s m=1' % (n1, n2, r['value'], r['sub'], r['l'], r['w'], r['b']))
    out.append('.ENDS')
    return '\n'.join(out) + '\n'


def ngspice(family, ng, tie, refdata):
    p, f, net, w, mos = _devices(family, ng, tie, refdata)
    name = cell_name(family, p['ng'], tie)
    out = ['.subckt %s %s' % (name, ' '.join(pins(family, tie)))]
    for inst, d, g, s, b in mos:
        out.append('X%s %s %s %s %s %s w=%s l=0.6u ng=%d m=1' % (inst, d, g, s, b, f['model'], _u(w), p['ng']))
    # ptap1: the symbol takes w/l of an equivalent rectangle; recover it from A and P
    A, P = si(net['ptap']['A']), si(net['ptap']['P'])
    s = P / 4.0
    disc = max(s * s - A, 0.0)
    tw, tl = s + math.sqrt(disc), s - math.sqrt(disc)
    R = 1.0 / (1.0 / (9.8e-10 / A) + 1.0 / (9.8e-4 / P))     # formula of ptap1.sym
    out.append('XR0 iovss sub! ptap1 R=%.4g w=%s l=%s' % (R, _u(tw), _u(tl)))
    if tie == 'D':
        dd = net['diode']
        a, c = ('sub!', 'gate') if family == 'N' else ('gate', 'iovdd')
        out.append('XDD0 %s %s %s l=%s w=%s' % (a, c, dd['model'], _u(si(dd['l'])), _u(si(dd['w']))))
    else:
        r = net['rppd']
        n1, n2 = ('iovss', 'net2') if family == 'N' else ('net2', 'iovdd')
        out.append('XRR0 %s %s %s rppd w=%s l=%s m=1 b=%s' % (n1, n2, r['sub'], _u(si(r['w'])), _u(si(r['l'])), r['b']))
    out.append('.ends')
    return '\n'.join(out) + '\n'
