#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Generate xschem schematics (.sch) and symbols (.sym) from the d2s_*.spice subcircuits.

Every device terminal gets a short wire stub and a net label (lab_pin), so connectivity is
exact and independent of wire routing; placement follows signal flow but is meant to be
tidied by hand in xschem. Subcircuit parameters (wdp, wdn, iab) are frozen at their defaults.

    python3 gen_xschem.py            # writes xschem/*.sch, xschem/*.sym
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'xschem')
LIB = 'sg13cmos5l_pr'
HDR = 'v {xschem version=3.4.4 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n'


def parse(fn, sub, defaults=None):
    """Return (ports, devices) of .subckt `sub`; params in {braces} replaced by defaults."""
    txt = open(os.path.join(HERE, fn)).read()
    m = re.search(rf'^\.subckt {sub} (.*?)$(.*?)^\.ends', txt, re.M | re.S)
    head = m.group(1).split()
    ports = [t for t in head if '=' not in t]
    defs = dict(t.split('=') for t in head if '=' in t)
    defs.update(defaults or {})
    devs = []
    for line in m.group(2).splitlines():
        line = line.strip()
        if not line or line.startswith('*'):
            continue
        for k, v in defs.items():
            line = line.replace('{' + k + '}', v)
        tok = line.split()
        name = tok[0]
        if name[0] in 'Xx':
            kv = dict(t.split('=') for t in tok if '=' in t)
            pos = [t for t in tok[1:] if '=' not in t]
            model = pos[-1]
            devs.append(dict(name=name[1:], model=model, nets=pos[:-1], p=kv))
        elif name[0] in 'Ii':
            devs.append(dict(name=name, model='isource', nets=tok[1:3], p={'value': tok[3]}))
    return ports, devs


class Sch:
    def __init__(self):
        self.items, self.n = [], 0

    def wire(self, x1, y1, x2, y2, net):
        self.items.append(f'N {x1} {y1} {x2} {y2} {{lab={net}}}')

    def label(self, x, y, net, right):
        self.n += 1
        self.items.append(f'C {{devices/lab_pin.sym}} {x} {y} 0 {1 if right else 0} {{name=l{self.n} sig_type=std_logic lab={net}}}')

    def stub(self, px, py, dx, dy, net):
        self.wire(px, py, px + dx, py + dy, net)
        self.label(px + dx, py + dy, net, right=dx > 0 or (dx == 0 and self.right_default))

    def text(self, s, x, y, size=0.4):
        self.items.append(f'T {{{s}}} {x} {y} 0 0 {size} {size} {{}}')

    def place(self, d, x, y, flip=0):
        s = -1 if flip else 1
        m = d['model']
        if m in ('sg13_hv_nmos', 'sg13_hv_pmos'):
            dn, gn, sn, bn = d['nets']
            p = d['p']
            prop = (f"name={d['name']}\nl={p['l']}\nw={p['w']}\nng={p.get('ng', '1')}\nm={p.get('m', '1')}\n"
                    f"mm_ok=1\nmodel={m}\nspiceprefix=X")
            self.items.append(f'C {{{LIB}/{m}.sym}} {x} {y} 0 {flip} {{{prop}}}')
            top, bot = (dn, sn) if m == 'sg13_hv_nmos' else (sn, dn)
            self.right_default = not flip
            self.stub(x - 20 * s, y, -20 * s, 0, gn)
            self.stub(x + 20 * s, y - 30, 0, -20, top)
            self.stub(x + 20 * s, y + 30, 0, 20, bot)
            self.stub(x + 20 * s, y, 60 * s, 0, bn)
        elif m == 'rhigh':
            a, b, body = d['nets']
            p = d['p']
            prop = f"name={d['name']}\nw={p['w']}\nl={p['l']}\nmodel=rhigh\nbody={body}\nspiceprefix=X\nb=0\nm=1\nmm_ok=1"
            self.items.append(f'C {{{LIB}/rhigh.sym}} {x} {y} 0 0 {{{prop}}}')
            self.right_default = True
            self.stub(x, y - 30, 0, -20, a)
            self.stub(x, y + 30, 0, 20, b)
        elif m == 'cap_cmomi':
            a, b = d['nets']
            p = d['p']
            prop = f"name={d['name']}\nmodel=cap_cmomi\nw={p['w']}\nl={p['l']}\nmmin=1\nmmax=4\nfeed=double\nsubblock=0\nm=1\nmm_ok=1\nspiceprefix=X"
            self.items.append(f'C {{{LIB}/cap_cmomi.sym}} {x} {y} 0 0 {{{prop}}}')
            self.right_default = True
            self.stub(x, y - 30, 0, -20, a)
            self.stub(x, y + 30, 0, 20, b)
        elif m == 'isource':
            a, b = d['nets']
            self.items.append(f"C {{devices/isource.sym}} {x} {y} 0 0 {{name={d['name']} value={d['p']['value']}}}")
            self.right_default = True
            self.stub(x, y - 30, 0, -20, a)
            self.stub(x, y + 30, 0, 20, b)
        else:
            raise ValueError(m)

    def pins(self, ports, dirs, x, y):
        for i, pname in enumerate(ports):
            sym = {'i': 'ipin', 'o': 'opin', 'io': 'iopin'}[dirs.get(pname, 'i')]
            self.items.append(f'C {{devices/{sym}.sym}} {x} {y + 40 * i} 0 0 {{name=p{i + 1} lab={pname}}}')

    def write(self, fn, title, ytop=-760):
        self.items.append(f'C {{devices/title.sym}} 160 900 0 0 {{name=l0 author="Christoph Maier"}}')
        self.text(title, -400, ytop, 0.6)
        open(os.path.join(OUT, fn), 'w').write(HDR + '\n'.join(self.items) + '\n')


def symbol(fn, name, left, right, top, bottom, desc):
    """Box symbol; pin order in the file = .subckt port order (left, right, top, bottom lists are
    (port, dir) tuples in the order they appear in the .subckt)."""
    order = []
    h = 40 * max(len(left), len(right), 2) + 40
    w = max(40 * max(len(top), len(bottom), 3) + 40, 240)
    L = [f'v {{xschem version=3.4.4 file_version=1.2}}\nG {{}}\nK {{type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}}\nV {{}}\nS {{}}\nE {{}}',
         f'P 4 5 {-w // 2} {-h // 2} {w // 2} {-h // 2} {w // 2} {h // 2} {-w // 2} {h // 2} {-w // 2} {-h // 2} {{}}',
         f'T {{@symname}} {-w // 2 + 10} {-h // 2 - 30} 0 0 0.3 0.3 {{}}', f'T {{@name}} {-w // 2 + 10} {h // 2 + 10} 0 0 0.3 0.3 {{}}',
         f'T {{{desc}}} {-w // 2 + 10} {-h // 2 - 50} 0 0 0.2 0.2 {{}}']
    pins = {}
    for i, (pn, dr) in enumerate(left):
        y = -h // 2 + 40 + 40 * i
        pins[pn] = (f'L 4 {-w // 2 - 20} {y} {-w // 2} {y} {{}}\nB 5 {-w // 2 - 22.5} {y - 2.5} {-w // 2 - 17.5} {y + 2.5} {{name={pn} dir={dr}}}\n'
                    f'T {{{pn}}} {-w // 2 + 5} {y - 6} 0 0 0.2 0.2 {{}}')
    for i, (pn, dr) in enumerate(right):
        y = -h // 2 + 40 + 40 * i
        pins[pn] = (f'L 4 {w // 2} {y} {w // 2 + 20} {y} {{}}\nB 5 {w // 2 + 17.5} {y - 2.5} {w // 2 + 22.5} {y + 2.5} {{name={pn} dir={dr}}}\n'
                    f'T {{{pn}}} {w // 2 - 5} {y - 6} 0 1 0.2 0.2 {{}}')
    for i, (pn, dr) in enumerate(top):
        x = -w // 2 + 40 + 40 * i
        pins[pn] = (f'L 4 {x} {-h // 2 - 20} {x} {-h // 2} {{}}\nB 5 {x - 2.5} {-h // 2 - 22.5} {x + 2.5} {-h // 2 - 17.5} {{name={pn} dir={dr}}}\n'
                    f'T {{{pn}}} {x - 5} {-h // 2 + 5} 0 0 0.2 0.2 {{}}')
    for i, (pn, dr) in enumerate(bottom):
        x = -w // 2 + 40 + 40 * i
        pins[pn] = (f'L 4 {x} {h // 2} {x} {h // 2 + 20} {{}}\nB 5 {x - 2.5} {h // 2 + 17.5} {x + 2.5} {h // 2 + 22.5} {{name={pn} dir={dr}}}\n'
                    f'T {{{pn}}} {x + 5} {h // 2 - 20} 1 0 0.2 0.2 {{}}')
    return L, pins


def write_symbol(fn, ports, L, pins):
    open(os.path.join(OUT, fn), 'w').write('\n'.join(L + [pins[p] for p in ports]) + '\n')


# ---------------------------------------------------------------- placement
FRONT = {  # name: (x, y, flip)  -- DDA front end, folded cascode, mirror, class-AB control
    'T1a': (0, -560, 0), 'T1b': (320, -560, 1), 'R1': (160, -420, 0), 'M1a': (0, -300, 0), 'M1b': (320, -300, 1),
    'T2a': (640, -560, 0), 'T2b': (960, -560, 1), 'R2': (800, -420, 0), 'M2a': (640, -300, 0), 'M2b': (960, -300, 1),
    'PL': (1300, -560, 0), 'PCL': (1300, -400, 0), 'FPL': (1160, -200, 0), 'FNL': (1460, -200, 1),
    'CX': (1300, 0, 0), 'SX': (1300, 160, 0),
    'PR': (1820, -560, 0), 'PCR': (1820, -400, 0), 'ABP': (1780, -200, 0), 'ABN': (2060, -200, 1),
    'CY': (1820, 0, 0), 'SY': (1820, 160, 0),
    'OP': (2280, -400, 0), 'ON': (2280, 0, 0), 'CMA': (2200, -200, 0), 'CMB': (2480, -200, 0),
    'DP': (2200, -560, 0), 'DN': (2200, 160, 0)}
BIAS = {'BP': (0, -300, 0), 'IBP': (60, -140, 0), 'BN': (300, -140, 0), 'IBN': (360, -300, 0),
        'BPC': (600, -300, 0), 'IBPC': (660, -140, 0), 'BNC': (900, -140, 0), 'IBNC': (960, -300, 0),
        'RP1': (1200, -440, 0), 'RP2': (1200, -280, 0), 'IABP': (1260, -120, 0),
        'RN1': (1500, -120, 0), 'RN2': (1500, -280, 0), 'IABN': (1560, -440, 0)}
DUT_DIRS = {'vdd': 'io', 'vss': 'io', 'vout': 'io'}


def build(spice, sub, placement, title, defaults=None, desc=''):
    ports, devs = parse(spice, sub, defaults)
    s = Sch()
    s.pins(ports, DUT_DIRS, -400, -600)
    missing = [d['name'] for d in devs if d['name'] not in placement]
    if missing:
        raise SystemExit(f'{sub}: no placement for {missing}')
    for d in devs:
        s.place(d, *placement[d['name']])
    s.write(f'{sub}.sch', title, ytop=min(-760, min(p[1] for p in placement.values()) - 200))
    sig = [p for p in ports if p not in ('vdd', 'vss')]
    left = [(p, 'in') for p in sig if p in ('vinp', 'vinn', 'vref', 'vfb')]
    right = [(p, 'inout') for p in sig if p == 'vout']
    top = [('vdd', 'inout')]
    bottom = [('vss', 'inout')] + [(p, 'in') for p in sig if p.startswith('vb') or p.startswith('vab')]
    if sub == 'd2s_bias':
        left, right, bottom = [], [(p, 'out') for p in sig], [('vss', 'inout')]
    L, pins = symbol(f'{sub}.sym', sub, left, right, top, bottom, desc)
    write_symbol(f'{sub}.sym', ports, L, pins)
    return ports, devs


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    build('d2s_miller.spice', 'd2s_miller', FRONT, 'd2s_miller: two-stage class-AB pad driver, Miller compensated (vfb = vout)',
          desc='vout-vref = (vinp-vinn)/2, tie vfb to vout')
    build('d2s_loadcomp.spice', 'd2s_loadcomp', FRONT, 'd2s_loadcomp: single-stage class-AB pad driver, load compensated (vfb = vout)',
          desc='vout-vref = (vinp-vinn)/2, tie vfb to vout, C_L >= 5 pF')
    build('d2s_bias.spice', 'd2s_bias', BIAS, 'd2s_bias: bias voltages from ideal reference currents (iab = 5 uA)',
          defaults={'iab': '5u'}, desc='ideal reference currents')
    print('written:', sorted(os.listdir(OUT)))
