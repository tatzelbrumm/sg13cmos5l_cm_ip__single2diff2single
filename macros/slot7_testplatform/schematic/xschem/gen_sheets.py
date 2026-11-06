#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Generate the xschem sheets and symbols of slot7_testplatform from ../../netlist/source/slot7_testplatform.spice.

Written 2026-11-06 (cloud session) after the xschem-analog-schematic skill and
sudelbuecher/design_considerations/class_ab_pad_driver/gen_xschem.py.  DRAFT STYLE: every terminal gets a short wire
stub and a net label (lab_pin), so connectivity is exact; placement is in rows (PMOS on top, NMOS below, signal flow
left to right) and is meant to be tidied by hand.  Pin positions of the PDK and macro symbols are read from their
.sym files, not assumed.  Verified by check_sheets.py (xschem netlist vs. source, device by device).

    python3 gen_sheets.py        # writes tp_en_ctrl.sch/.sym, slot7_testplatform.sch/.sym here
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MAC = os.path.normpath(os.path.join(HERE, '..', '..'))
MACROS = os.path.normpath(os.path.join(MAC, '..'))
SRC = os.path.join(MAC, 'netlist', 'source', 'slot7_testplatform.spice')
PDK = os.path.join(os.environ.get('PDK_ROOT', '/foss/pdks'), os.environ.get('PDK', 'ihp-sg13cmos5l'))
PDKSYM = os.path.join(PDK, 'libs.tech', 'xschem', 'sg13cmos5l_pr')
HDR = 'v {xschem version=3.4.8RC file_version=1.3}\nG {}\nK {}\nV {}\nS {}\nF {}\nE {}\n'
SUBSYM = {'oa_core_pd': os.path.join(MACROS, 'oa_core_pd', 'schematic', 'xschem', 'oa_core_pd.sym'),
          'bg_core_pd': os.path.join(MACROS, 'bg_core_pd', 'schematic', 'xschem', 'bg_core_pd.sym'),
          'xgate': os.path.join(MACROS, 'ocd_analog_switches', 'schematic', 'xschem', 'xgate.sym'),
          'tp_en_ctrl': os.path.join(HERE, 'tp_en_ctrl.sym')}


def sym_pins(path):
    """[(name, x, y)] in @pinlist order (B 5 boxes, sim_pinnumber wins)."""
    s = open(path).read()
    pins = []
    for m in re.finditer(r'^B 5 ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) \{([^}]*)\}', s, re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        a = dict(re.findall(r'(\w+)=(\S+)', m.group(5)))
        pins.append((a.get('sim_pinnumber'), a['name'], (x1 + x2) / 2, (y1 + y2) / 2))
    if all(p[0] for p in pins):
        pins.sort(key=lambda p: int(p[0]))
    return [(n, x, y) for _, n, x, y in pins]


def parse(sub):
    txt = open(SRC).read().replace('\n+', ' ')
    m = re.search(rf'^\.subckt {sub} (.*?)$(.*?)^\.ends', txt, re.M | re.S)
    ports = m.group(1).split()
    devs = []
    for line in m.group(2).splitlines():
        tok = line.split()
        if not tok or tok[0].startswith('*'):
            continue
        kv = dict(t.split('=') for t in tok if '=' in t)
        pos = [t for t in tok[1:] if '=' not in t]
        devs.append(dict(name=tok[0][1:], model=pos[-1], nets=pos[:-1], p=kv))
    return ports, devs


class Sch:
    def __init__(self):
        self.items, self.n = [], 0

    def wire(self, x1, y1, x2, y2, net):
        self.items.append(f'N {x1} {y1} {x2} {y2} {{lab={net}}}')

    def label(self, x, y, net, right):
        self.n += 1
        self.items.append(f'C {{devices/lab_pin.sym}} {x} {y} 0 {1 if right else 0} {{name=l{self.n} sig_type=std_logic lab={net}}}')

    def stub(self, px, py, dx, dy, net, right):
        self.wire(px, py, px + dx, py + dy, net)
        self.label(px + dx, py + dy, net, right)

    def text(self, s, x, y, size=0.4):
        self.items.append(f'T {{{s}}} {x} {y} 0 0 {size} {size} {{}}')

    def mos(self, d, x, y):
        m = d['model']
        dn, gn, sn, bn = d['nets']
        p = d['p']
        prop = (f"name={d['name']}\nl={p['l']}\nw={p['w']}\nng={p.get('ng', '1')}\nm={p.get('m', '1')}\n"
                f"model={m}\nspiceprefix=X")
        self.items.append(f'C {{sg13cmos5l_pr/{m}.sym}} {x} {y} 0 0 {{{prop}}}')
        top, bot = (dn, sn) if m == 'sg13_hv_nmos' else (sn, dn)
        self.stub(x - 20, y, -20, 0, gn, False)
        self.stub(x + 20, y - 30, 0, -20, top, True)
        self.stub(x + 20, y + 30, 0, 20, bot, True)
        self.stub(x + 20, y, 40, 0, bn, True)

    def inst(self, d, x, y):
        sym = d['model']
        pins = sym_pins(SUBSYM[sym])
        assert len(pins) == len(d['nets']), (d, pins)
        self.items.append(f'C {{{sym}.sym}} {x} {y} 0 0 {{name={d["name"]}}}')
        xmin, xmax = min(p[1] for p in pins), max(p[1] for p in pins)
        for (pn, px, py), net in zip(pins, d['nets']):
            ax, ay = x + px, y + py
            # stub away from the symbol body: horizontal on the left / right edge, else vertical
            if px in (xmin, xmax):
                dx, dy = (40 if px == xmax else -40), 0
            else:
                dx, dy = 0, (40 if py > 0 else -40)
            self.stub(ax, ay, dx, dy, net, dx > 0 or dx == 0)

    def pins(self, ports, dirs, x, y):
        for i, pname in enumerate(ports):
            sym = {'i': 'ipin', 'o': 'opin', 'io': 'iopin'}[dirs.get(pname, 'io')]
            self.items.append(f'C {{devices/{sym}.sym}} {x} {y + 40 * i} 0 0 {{name=p{i + 1} lab={pname}}}')

    def write(self, fn, title, y_title):
        self.text(title, -400, y_title, 0.5)
        open(os.path.join(HERE, fn), 'w').write(HDR + '\n'.join(self.items) + '\n')


def box_symbol(fn, ports, side, desc):
    """Box symbol; pins in .subckt port order; side[port] = ('l'|'r', dir)."""
    left = [p for p in ports if side[p][0] == 'l']
    right = [p for p in ports if side[p][0] == 'r']
    h = 40 * max(len(left), len(right)) + 40
    w = 320
    out = ['v {xschem version=3.4.8RC file_version=1.3}\nG {}\nK {type=subcircuit\nformat="@name @pinlist @symname"\n'
           f'template="name=x1"\ndescription="{desc}"\n}}\nV {{}}\nS {{}}\nF {{}}\nE {{}}',
           f'P 4 5 {-w // 2} {-h // 2} {w // 2} {-h // 2} {w // 2} {h // 2} {-w // 2} {h // 2} {-w // 2} {-h // 2} {{}}',
           f'T {{@symname}} {-w // 2} {-h // 2 - 30} 0 0 0.3 0.3 {{}}', f'T {{@name}} {-w // 2} {h // 2 + 10} 0 0 0.3 0.3 {{}}']
    for p in ports:
        s, d = side[p]
        lst = left if s == 'l' else right
        y = -h // 2 + 40 + 40 * lst.index(p)
        if s == 'l':
            out.append(f'L 4 {-w // 2 - 20} {y} {-w // 2} {y} {{}}\nB 5 {-w // 2 - 22.5} {y - 2.5} {-w // 2 - 17.5} {y + 2.5} {{name={p} dir={d}}}\n'
                       f'T {{{p}}} {-w // 2 + 5} {y - 6} 0 0 0.2 0.2 {{}}')
        else:
            out.append(f'L 4 {w // 2} {y} {w // 2 + 20} {y} {{}}\nB 5 {w // 2 + 17.5} {y - 2.5} {w // 2 + 22.5} {y + 2.5} {{name={p} dir={d}}}\n'
                       f'T {{{p}}} {w // 2 - 5} {y - 6} 0 1 0.2 0.2 {{}}')
    open(os.path.join(HERE, fn), 'w').write('\n'.join(out) + '\n')


def build_tp_en_ctrl():
    ports, devs = parse('tp_en_ctrl')
    s = Sch()
    dirs = {p: 'i' for p in ('en0_1v2', 'en1_1v2', 'en2_1v2', 'en3_1v2', 'enable')}
    dirs.update({p: 'o' for p in ports if p.startswith(('en0', 'en1', 'en2', 'en3', 'rb', 'lo')) and not p.endswith('1v2')})
    s.pins(ports, dirs, -400, -600)
    pm = [d for d in devs if d['model'] == 'sg13_hv_pmos']
    nm = [d for d in devs if d['model'] == 'sg13_hv_nmos']
    for i, d in enumerate(pm):
        s.mos(d, 200 * i, -400)
    for i, d in enumerate(nm):
        s.mos(d, 200 * i, 0)
    s.text('tp_en_ctrl: xb<c> = NOT(en<c>_1v2 AND enable AND vdd_1v2) (ratioed, weak PU 0.3/20); en<c> = NOT xb<c>; '
           'en<c>_b = NOT en<c>; rb<c> = en<c> on 1.2 V; lo<k> tie-low; NRD pulls a floating vdd_1v2 low; c = 0..3', -400, -720, 0.3)
    s.write('tp_en_ctrl.sch', 'tp_en_ctrl (draft sheet, generated by gen_sheets.py)', -780)
    side = {p: ('l', 'inout') for p in ('vdd_3v3', 'vss_3v3', 'vdd_1v2', 'vss_1v2')}
    side.update({p: ('l', 'in') for p in ('en0_1v2', 'en1_1v2', 'en2_1v2', 'en3_1v2', 'enable')})
    side.update({p: ('r', 'out') for p in ports if p not in side})
    box_symbol('tp_en_ctrl.sym', ports, side, 'fail-safe enables (cores, bus switches), read-back, tie-lows')


def build_top():
    ports, devs = parse('slot7_testplatform')
    s = Sch()
    dirs = {p: 'i' for p in ports if p.startswith('dig_in') or p == 'enable'}
    dirs.update({p: 'o' for p in ports if p.startswith('dig_out')})
    s.pins(ports, dirs, -400, -600)
    place = {'ctl': (0, 0), 'oa': (700, -400), 'bg': (700, 0), 'tg0': (1300, -400), 'tg1': (1300, 0)}
    for d in devs:
        s.inst(d, *place[d['name']])
    s.text('slot7_testplatform (stage A): OA / BG cores, fail-safe enables, iout -> analog_bus0 / analog_bus1 '
           'through xgate (dig_in[2] / dig_in[3] via tp_en_ctrl); docs/slot7_testplatform/PLAN.md', -400, -720, 0.3)
    s.write('slot7_testplatform.sch', 'slot7_testplatform (draft sheet, generated by gen_sheets.py)', -780)
    side = {p: ('l', 'inout') for p in ('vdd_3v3', 'vss_3v3', 'vdd_1v2', 'vss_1v2')}
    side.update({p: ('l', 'in') for p in ports if p.startswith('dig_in') or p == 'enable'})
    side.update({p: ('r', 'out') for p in ports if p.startswith('dig_out')})
    side.update({p: ('r', 'inout') for p in ('analog_bus0', 'analog_bus1')})
    box_symbol('slot7_testplatform.sym', ports, side, 'slot 7 test platform, stage A')


if __name__ == '__main__':
    build_tp_en_ctrl()
    build_top()
    print('written: tp_en_ctrl.sch/.sym, slot7_testplatform.sch/.sym in', HERE)
