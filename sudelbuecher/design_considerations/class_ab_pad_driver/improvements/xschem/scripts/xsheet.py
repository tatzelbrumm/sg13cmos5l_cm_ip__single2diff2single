#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Minimal xschem sheet writer with a geometric lint, used by gen_cells.py and gen_testbenches.py.

Coordinates are xschem's (y down). Pin positions and pin order are read from the .sym files
(PDK symbols under $PDK_ROOT/$PDK/libs.tech/xschem, xschem's devices/ library, and the cell
symbols in the output directory). Every device pin gets the net it must have; the lint re-derives
connectivity from geometry (wire ends, T-junctions, pins) and reports any component that carries
two net names, any pin on a wire interior, any dangling wire end and any collinear overlap.
xschem's own netlist (check_xschem.py) is still the final check.
"""
import os, re

PDKX = os.path.join(os.environ.get('PDK_ROOT', ''), os.environ.get('PDK', 'ihp-sg13cmos5l'), 'libs.tech', 'xschem')
# xschem's library (the directory that contains devices/); first existing candidate wins
_CANDIDATES = [os.path.dirname(os.environ.get('XSCHEM_DEVICES', '').rstrip('/')),
               os.path.join(os.environ.get('XSCHEM_SHAREDIR', ''), 'xschem_library'),
               '/foss/tools/xschem/share/xschem/xschem_library',
               '/usr/local/share/xschem/xschem_library',
               '/usr/share/xschem/xschem_library']
XL = next((d for d in _CANDIDATES if d and os.path.isfile(os.path.join(d, 'devices', 'vsource.sym'))), None)
HDR = 'v {xschem version=3.4.4 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n'
_SYMS = {}


def sym_info(path):
    s = open(path).read()
    k = re.search(r'^K \{(.*?)\n\}', s, re.M | re.S) or re.search(r'^K \{(.*?)\}', s, re.M | re.S)
    kb = k.group(1) if k else ''
    typ = re.search(r'type=(\S+)', kb)
    fmt = re.search(r'\bformat="([^"]*)"', kb)
    tpl = re.search(r'\btemplate="([^"]*)"', kb, re.S)
    pins = []
    for m in re.finditer(r'^B 5 ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) \{([^}]*)\}', s, re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        a = dict(re.findall(r'(\w+)=(\S+)', m.group(5)))
        pins.append((a.get('name'), (x1 + x2) / 2, (y1 + y2) / 2, a.get('sim_pinnumber')))
    return dict(type=typ and typ.group(1), format=fmt and fmt.group(1), template=tpl and tpl.group(1), pins=pins)


def sym_pins(ref, local):
    if ref not in _SYMS:
        if ref.startswith('devices/') and XL is None:
            raise SystemExit('xschem devices library not found; set XSCHEM_DEVICES to its devices/ directory')
        if ref.startswith('devices/'):
            p = f'{XL}/{ref}'
        elif ref.startswith('sg13cmos5l_pr/'):
            p = os.path.realpath(f'{PDKX}/{ref}')
        else:
            p = os.path.join(local, ref)
        pins = sym_info(p)['pins']
        if any(q[3] for q in pins):
            pins = sorted(pins, key=lambda q: int(q[3]))
        _SYMS[ref] = [(n, x, y) for n, x, y, _ in pins]
    return _SYMS[ref]


def xf(px, py, rot, flip):
    if flip:
        px = -px
    for _ in range(rot % 4):
        px, py = -py, px
    return px, py


class Sheet:
    def __init__(self, local):
        self.local = local
        self.inst, self.wires, self.pins, self.texts, self.labels = [], [], [], [], []
        self.np = self.nl = 0

    # ---------------------------------------------------------------- instances
    def place(self, ref, x, y, rot, flip, props, nets, owner):
        pos = {}
        for n, px, py in sym_pins(ref, self.local):
            dx, dy = xf(px, py, rot, flip)
            pos[n] = (int(round(x + dx)), int(round(y + dy)))
            if n in nets:
                self.pins.append((pos[n], nets[n], f'{owner}.{n}'))
        self.inst.append(f'C {{{ref}}} {x} {y} {rot} {flip} {{{props}}}')
        return pos

    def mos(self, name, model, x, y, flip, d, g, s, b, w, l, ng=1, rot=0):
        props = f'name={name}\nl={l}\nw={w}\nng={ng}\nm=1\nmm_ok=1\nmodel={model}\nspiceprefix=X'
        return self.place(f'sg13cmos5l_pr/{model}.sym', x, y, rot, flip, props,
                          dict(D=d, G=g, S=s, B=b), name)

    def rhigh(self, name, x, y, rot, p, m, body, w, l):
        props = (f'name={name}\nw={w}\nl={l}\nmodel=rhigh\nbody={body}\nspiceprefix=X\nb=0\n'
                 f'm=1\nmm_ok=1')
        return self.place('sg13cmos5l_pr/rhigh.sym', x, y, rot, 0, props, dict(P=p, M=m), name)

    def isrc(self, name, x, y, p, m, value, rot=0):
        return self.place('devices/isource.sym', x, y, rot, 0, f'name={name} value={value}',
                          dict(p=p, m=m), name)

    def sub(self, name, ref, x, y, nets, rot=0, flip=0):
        return self.place(ref, x, y, rot, flip, f'name={name}', nets, name)

    def port(self, kind, x, y, net, flip=0):
        self.np += 1
        self.place(f'devices/{kind}.sym', x, y, 0, flip, f'name=p{self.np} lab={net}', dict(p=net), f'port {net}')

    def lab(self, x, y, net, flip=0, rot=0, kind='lab_wire'):
        self.nl += 1
        self.labels.append((x, y))
        self.place(f'devices/{kind}.sym', x, y, rot, flip, f'name=l{self.nl} sig_type=std_logic lab={net}',
                   dict(p=net), f'label {net}')

    # ---------------------------------------------------------------- wires, text
    def w(self, net, *pts):
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            assert x1 == x2 or y1 == y2, (net, pts)
            assert all(v % 10 == 0 for v in (x1, y1, x2, y2)), (net, pts)
            if (x1, y1) != (x2, y2):
                self.wires.append([x1, y1, x2, y2, net])

    def text(self, s, x, y, size=0.4):
        self.texts.append(f'T {{{s}}} {x} {y} 0 0 {size} {size} {{}}')

    # ---------------------------------------------------------------- lint
    @staticmethod
    def _inside(w, p):
        x1, y1, x2, y2 = w[:4]
        px, py = p
        if x1 == x2 == px:
            return min(y1, y2) < py < max(y1, y2)
        if y1 == y2 == py:
            return min(x1, x2) < px < max(x1, x2)
        return False

    def _split(self):
        ends = {(w[0], w[1]) for w in self.wires} | {(w[2], w[3]) for w in self.wires} | set(self.labels)
        changed = True
        while changed:
            changed = False
            for i, w in enumerate(self.wires):
                for p in ends:
                    if self._inside(w, p):
                        x1, y1, x2, y2, net = w
                        self.wires[i] = [x1, y1, p[0], p[1], net]
                        self.wires.append([p[0], p[1], x2, y2, net])
                        changed = True
                        break
                if changed:
                    break

    def lint(self):
        self._split()
        err = []
        par = {}

        def f(a):
            par.setdefault(a, a)
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a

        def u(a, b):
            par[f(a)] = f(b)
        for w in self.wires:
            u((w[0], w[1]), (w[2], w[3]))
        for p, net, who in self.pins:
            f(p)
            for w in self.wires:
                if self._inside(w, p):
                    err.append(f'pin {who} ({net}) on interior of wire {w}')
        # collinear overlaps
        for i, a in enumerate(self.wires):
            for b in self.wires[i + 1:]:
                if a[0] == a[2] == b[0] == b[2]:
                    lo, hi = max(min(a[1], a[3]), min(b[1], b[3])), min(max(a[1], a[3]), max(b[1], b[3]))
                    if hi > lo:
                        err.append(f'overlap {a} {b}')
                if a[1] == a[3] == b[1] == b[3]:
                    lo, hi = max(min(a[0], a[2]), min(b[0], b[2])), min(max(a[0], a[2]), max(b[0], b[2]))
                    if hi > lo:
                        err.append(f'overlap {a} {b}')
        names = {}
        for p, net, who in self.pins:
            names.setdefault(f(p), set()).add(net)
        for w in self.wires:
            names.setdefault(f((w[0], w[1])), set()).add(w[4])
        for r, s in names.items():
            if len(s) > 1:
                err.append(f'component at {r} joins {sorted(s)}')
        roots = {}
        for r, s in names.items():
            for n in s:
                roots.setdefault(n, set()).add(r)
        named = {(f(p), net) for p, net, who in self.pins if who.startswith(('label', 'port'))}
        for n, r in roots.items():
            if len(r) > 1 and any((q, n) not in named for q in r):
                err.append(f'net {n} is split into {len(r)} pieces, not all of them named')
        # dangling wire ends: an end must meet another wire end, a wire interior or a pin
        pinpts = {p for p, _, _ in self.pins}
        cnt = {}
        for w in self.wires:
            for p in ((w[0], w[1]), (w[2], w[3])):
                cnt[p] = cnt.get(p, 0) + 1
        for p, c in cnt.items():
            if c == 1 and p not in pinpts and not any(self._inside(w, p) for w in self.wires):
                err.append(f'dangling wire end {p}')
        # every net must be named once at least, and every device pin should be connected
        comps = {}
        for p, net, who in self.pins:
            comps.setdefault(f(p), []).append(who)
        for p, net, who in self.pins:
            if len(comps[f(p)]) == 1 and not who.startswith('port') and p not in cnt:
                err.append(f'unconnected pin {who} ({net})')
        cross = 0
        for i, a in enumerate(self.wires):
            for b in self.wires[i + 1:]:
                if a[0] == a[2] and b[1] == b[3]:
                    v, h = a, b
                elif a[1] == a[3] and b[0] == b[2]:
                    v, h = b, a
                else:
                    continue
                if self._inside(h, (v[0], h[1])) and self._inside(v, (v[0], h[1])):
                    cross += 1
                    if v[4] == h[4]:
                        err.append(f'{v[4]} crosses itself at {(v[0], h[1])} without a junction')
        return err, cross

    def write(self, path):
        err, cross = self.lint()
        body = self.texts + [f'N {x1} {y1} {x2} {y2} {{lab={n}}}' for x1, y1, x2, y2, n in self.wires] + self.inst
        open(path, 'w').write(HDR + '\n'.join(body) + '\n')
        return err, cross
