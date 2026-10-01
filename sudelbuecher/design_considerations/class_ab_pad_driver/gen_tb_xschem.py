#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
xschem testbench schematics for the four tb_d2s_*.spice decks, drawn per the
xschem-analog-schematic skill: pin positions read from the .sym files (no hard-coded
symbol geometry), signal flow left to right, vdd bus on top, ground bus at the bottom,
wires for short routes, net labels only for long ones (vref, dp, fb, the vfb feedback).

The DUT and bias symbols resolve to xschem/d2s_*.sch (hierarchical netlisting), so the
decks' `.include d2s_*.spice` lines are not needed; the code block carries .lib/.param/.control.

    python3 gen_tb_xschem.py      # writes xschem/tb_d2s_{miller,loadcomp}_{step,loop}.sch
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
XS = os.path.join(HERE, 'xschem')
# xschem's generic device library (vsource, vcvs, res, ...); first existing candidate wins
_CANDIDATES = [os.environ.get('XSCHEM_DEVICES', ''),
               os.path.join(os.environ.get('XSCHEM_SHAREDIR', ''), 'xschem_library', 'devices'),
               '/foss/tools/xschem/share/xschem/xschem_library/devices',
               '/usr/local/share/xschem/xschem_library/devices',
               '/usr/share/xschem/xschem_library/devices']
DEV = next((d for d in _CANDIDATES if d and os.path.isfile(os.path.join(d, 'vsource.sym'))), None)
if DEV is None:
    raise SystemExit('xschem devices library not found; set XSCHEM_DEVICES')


def sym_info(path):
    s = open(path).read()
    pins = {}
    for m in re.finditer(r'^B 5 ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) \{([^}]*)\}', s, re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        a = dict(re.findall(r'(\w+)=(\S+)', m.group(5)))
        pins[a['name']] = ((x1 + x2) / 2, (y1 + y2) / 2)
    return pins


def symfile(ref):
    return os.path.join(DEV, ref.split('/', 1)[1]) if ref.startswith('devices/') else os.path.join(XS, ref)


def T(dx, dy, rot, flip):
    if flip:
        dx = -dx
    return {0: (dx, dy), 1: (-dy, dx), 2: (-dx, -dy), 3: (dy, -dx)}[rot]


class Sheet:
    def __init__(self):
        self.L, self.n = [], 0

    def C(self, ref, x, y, props, rot=0, flip=0):
        self.L.append(f'C {{{ref}}} {x} {y} {rot} {flip} {{{props}}}')
        pins = sym_info(symfile(ref))
        return {k: tuple(int(round(v)) for v in (x + T(px, py, rot, flip)[0], y + T(px, py, rot, flip)[1]))
                for k, (px, py) in pins.items()}

    def W(self, net, *pts):
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            assert x1 == x2 or y1 == y2, 'orthogonal wires only'
            self.L.append(f'N {x1} {y1} {x2} {y2} {{lab={net}}}')

    def lab(self, net, pin, dx, dy):
        x, y = pin
        self.W(net, (x, y), (x + dx, y + dy))
        self.n += 1
        right = dx > 0 or (dx == 0 and dy != 0)
        self.L.append(f'C {{devices/lab_pin.sym}} {x + dx} {y + dy} 0 {1 if right else 0} '
                      f'{{name=l{self.n} sig_type=std_logic lab={net}}}')

    def name(self, net, pt):
        """Name a wire-only net: a lab_wire on a wire end or corner. Without it xschem calls
        the net net1, net2, ... (the lab= on N lines is ignored)."""
        self.n += 1
        self.L.append(f'C {{devices/lab_wire.sym}} {pt[0]} {pt[1]} 0 0 {{name=l{self.n} sig_type=std_logic lab={net}}}')

    def text(self, s, x, y, size=0.4):
        self.L.append(f'T {{{s}}} {x} {y} 0 0 {size} {size} {{}}')

    def write(self, fn):
        hdr = 'v {xschem version=3.4.4 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n'
        open(os.path.join(XS, fn), 'w').write(hdr + '\n'.join(self.L) + '\n')


VDD_Y, GND_Y = -300, 700
X_END = 1480                      # right end of the rails
DUT = (1040, 40)                  # DUT symbol origin
BIAS = (700, 460)                 # bias block origin (outputs face right, toward the DUT bias pins)
EP, EN = (560, -120), (560, 60)   # VCVS splitting v(dp) into vinp / vinn around vref


def common(s, dut):
    """Rails, supplies, bias block, DUT, DUT supply and bias wiring. Returns DUT pins."""
    s.W('vdd', (60, VDD_Y), (X_END, VDD_Y)); s.name('vdd', (60, VDD_Y))
    s.W('GND', (60, GND_Y), (X_END, GND_Y))
    s.C('devices/gnd.sym', 800, GND_Y, 'name=l0 lab=GND')
    p = s.C('devices/vsource.sym', 100, 200, 'name=Vdd value=3.3 savecurrent=false')
    s.W('vdd', p['p'], (p['p'][0], VDD_Y)); s.W('GND', p['m'], (p['m'][0], GND_Y))
    p = s.C('devices/vsource.sym', 200, 200, 'name=Vcm value=1.65 savecurrent=false')
    s.lab('vref', p['p'], 0, -40); s.W('GND', p['m'], (p['m'][0], GND_Y))
    b = s.C('d2s_bias.sym', *BIAS, 'name=Xb')
    s.W('vdd', b['vdd'], (b['vdd'][0], VDD_Y)); s.W('GND', b['vss'], (b['vss'][0], GND_Y))
    d = s.C(f'{dut}.sym', *DUT, 'name=Xd')
    s.W('vdd', d['vdd'], (d['vdd'][0], VDD_Y)); s.W('GND', d['vss'], (d['vss'][0], GND_Y))
    # top bias output -> leftmost DUT bias pin, so the L-routes never cross each other
    for net in ['vbp', 'vbn', 'vbpc', 'vbnc', 'vabp', 'vabn']:
        s.W(net, b[net], (d[net][0], b[net][1]), d[net])
        s.name(net, (d[net][0], b[net][1]))
    return d


def code(s, lines, x=60, y=820):
    v = '\n'.join(lines).replace('{', '\\{').replace('}', '\\}').replace('"', '\\"')
    s.L.append(f'C {{devices/code_shown.sym}} {x} {y} 0 0 {{name=s1 only_toplevel=false value="{v}"}}')


LIBS = ['.lib cornerMOShv.lib mos_tt', '.lib cornerRES.lib res_typ', '.lib cornerCAP.lib cap_typ']


def load(s, d, rl):
    y = d['vout'][1]
    s.W('vout', d['vout'], (1420, y)); s.lab('vout', (1420, y), 40, 0)
    if rl:
        r = s.C('devices/res.sym', 1320, y + 90, 'name=RL value=1k m=1')
        s.W('vout', r['P'], (r['P'][0], y)); s.lab('vref', r['M'], 0, 40)
    c = s.C('devices/capa.sym', 1420, y + 90, 'name=CL m=1 value=100p')
    s.W('vout', c['p'], (c['p'][0], y)); s.W('GND', c['m'], (c['m'][0], GND_Y))


def step(dut, rl):
    s = Sheet()
    d = common(s, dut)
    p = s.C('devices/vsource.sym', 300, 200, 'name=Vd value="pulse(\\{-vstep\\} \\{vstep\\} 1u 1n 1n 4u 8u)" savecurrent=false')
    s.lab('dp', p['p'], 0, -40); s.W('GND', p['m'], (p['m'][0], GND_Y))
    ep = s.C('devices/vcvs.sym', *EP, 'name=Ep value=0.5')
    en = s.C('devices/vcvs.sym', *EN, 'name=En value=-0.5')
    for e in (ep, en):
        s.lab('dp', e['cp'], -40, 0); s.lab('GND', e['cm'], -40, 0)
        s.lab('vref', e['m'], 0, 30)
    s.W('vinp', ep['p'], (640, ep['p'][1]), (640, d['vinp'][1]), d['vinp']); s.name('vinp', (640, ep['p'][1]))
    s.W('vinn', en['p'], (660, en['p'][1]), (660, d['vinn'][1]), d['vinn']); s.name('vinn', (660, en['p'][1]))
    s.lab('vref', d['vref'], -40, 0)
    s.lab('vout', d['vfb'], -40, 0)
    load(s, d, rl)
    code(s, LIBS + ['.param vstep=0.5', '.control', 'tran 2n 9u', 'meas tran vlo find v(vout) at=0.99u',
                    'meas tran vhi find v(vout) at=4.9u', 'if $?batchmode = 0', '  plot v(vout) v(vinp) v(vinn)',
                    'end', '.endc'])
    s.text(f'tb_{dut}_step: step response, vinp - vinn = v(dp), vfb = vout', 60, VDD_Y - 120, 0.5)
    s.write(f'tb_{dut}_step.sch')


def loop(dut, rl):
    s = Sheet()
    d = common(s, dut)
    for pin in ('vinp', 'vinn', 'vref'):
        s.lab('vref', d[pin], -40, 0)
    s.lab('fb', d['vfb'], -40, 0)
    load(s, d, rl)
    lb = s.C('devices/ind.sym', 1320, d['vout'][1] - 60, 'name=Lb m=1 value=1G', rot=2)
    s.W('vout', lb['p'], (lb['p'][0], d['vout'][1])); s.lab('fb', lb['m'], 0, -30)
    cb = s.C('devices/capa.sym', 1560, -200, 'name=Cb m=1 value=1')
    s.lab('fb', cb['p'], 0, -30)
    vi = s.C('devices/vsource.sym', 1560, -80, 'name=Vinj value="dc 0 ac 1" savecurrent=false')
    s.W('inj', cb['m'], vi['p']); s.name('inj', vi['p'])
    s.W('GND', vi['m'], (vi['m'][0], GND_Y), (X_END, GND_Y))
    code(s, LIBS + ['.control', 'ac dec 50 10 1G', 'let T=-v(vout)/v(fb)', 'meas ac fc when vdb(T)=0',
                    'meas ac pT find vp(T) when vdb(T)=0', 'let pm=180/pi*pT+180', 'print pm',
                    'if $?batchmode = 0', '  plot vdb(T) 180/pi*vp(T)', 'end', '.endc'])
    s.text(f'tb_{dut}_loop: loop gain T = -v(vout)/v(fb), loop broken at the vfb gate', 60, VDD_Y - 120, 0.5)
    s.write(f'tb_{dut}_loop.sch')


if __name__ == '__main__':
    for dut, rl in (('d2s_miller', True), ('d2s_loadcomp', False)):
        step(dut, rl); loop(dut, rl)
    print('written', sorted(f for f in os.listdir(XS) if f.startswith('tb_')))
