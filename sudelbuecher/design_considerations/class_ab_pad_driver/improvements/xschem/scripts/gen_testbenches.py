#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""xschem testbench schematics tb_*.sch for the decks in ../../sim/tb/*.spice.
Layout follows the hand-checked tb_d2s_*.sch: vdd rail at -300, ground rail at 700, supplies on
the left, bias block at (700, 460), DUT at (1040, 40), load on the right, code block below.
The code block carries the deck's .lib/.param/.save lines and its .control section verbatim;
the subcircuits come from the schematics (no .include). The output directory must hold the
cell symbols (d2s_mpdda.sym, d2s_lc2.sym, d2s_bias_lp.sym, unit_r2.sym), as improvements/xschem/
or a gen_cells.py output does; the output goes to a directory of its own unless --overwrite is given.

    python3 gen_testbenches.py OUTDIR [--overwrite]      (needs $PDK_ROOT)
"""
import os, re, sys
from xsheet import Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
XSDIR = os.path.dirname(HERE)                                        # improvements/xschem
TB = os.path.join(XSDIR, '..', 'sim', 'tb')


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
VDD_Y, GND_Y = -300, 700
report = []


def pv(v):
    """xschem property value: braces escaped, quoted if it has blanks"""
    v = v.replace('{', '\\{').replace('}', '\\}')
    return f'"{v}"' if ' ' in v else v


def code_lines(deck):
    """the deck's non-element lines in order: .lib/.param/.save and the .control block"""
    out, ctl = [], False
    for l in open(os.path.join(TB, deck + '.spice')).read().splitlines():
        s = l.strip()
        if s.lower().startswith('.control'):
            ctl = True
        if ctl:
            out.append(l)
            if s.lower().startswith('.endc'):
                ctl = False
            continue
        if s.startswith('.') and not s.lower().startswith(('.include', '.end', '.title')):
            out.append(l)
    return out


def first_comment(deck):
    return open(os.path.join(TB, deck + '.spice')).readline().lstrip('* ').strip()


class TbSheet(Sheet):
    def __init__(self, local, gnd_y=GND_Y):
        super().__init__(local)
        self.gnd_y, self.vx, self.gx = gnd_y, [], []

    def gnd(self, x, y):
        self.labels.append((x, y))
        self.place('devices/gnd.sym', x, y, 0, 0, 'name=l0 lab=GND', {'p': 'GND'}, 'label GND')

    def to_vdd(self, pt, *via):
        self.w('vdd', pt, *via, ((via[-1] if via else pt)[0], VDD_Y)); self.vx.append((via[-1] if via else pt)[0])

    def to_gnd(self, pt):
        self.w('GND', pt, (pt[0], self.gnd_y)); self.gx.append(pt[0])

    def rails(self, gnd_at=800):
        """vdd rail from its label at x=60 to the last drop, ground rail across its drops"""
        if self.vx:
            self.w('vdd', (60, VDD_Y), (max(self.vx), VDD_Y)); self.lab(60, VDD_Y, 'vdd')
        lo, hi = min(self.gx + [gnd_at]), max(self.gx + [gnd_at])
        self.w('GND', (lo, self.gnd_y), (hi, self.gnd_y)); self.gnd(gnd_at, self.gnd_y)

    def pin_lab(self, net, pt, dx, dy):
        """stub from a pin plus a lab_pin at its end"""
        x, y = pt
        self.w(net, (x, y), (x + dx, y + dy))
        self.lab(x + dx, y + dy, net, flip=1 if (dx > 0 or (dx == 0 and dy != 0)) else 0, kind='lab_pin')

    def vsrc(self, name, x, y, p, m, value):
        return self.place('devices/vsource.sym', x, y, 0, 0, f'name={name} value={pv(value)} savecurrent=false',
                          dict(p=p, m=m), name)

    def dev(self, sym, name, x, y, nets, value, rot=0, extra=''):
        return self.place(f'devices/{sym}.sym', x, y, rot, 0, f'name={name} value={pv(value)}{extra}', nets, name)

    def code(self, lines, x=60, y=820):
        v = '\n'.join(lines).replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}').replace('"', '\\"')
        self.inst.append(f'C {{devices/code_shown.sym}} {x} {y} 0 0 {{name=s1 only_toplevel=false value="{v}"}}')


def save(s, name):
    s.rails(s.gnd_at if hasattr(s, 'gnd_at') else 800)
    err, cross = s.write(os.path.join(OUT, name + '.sch'))
    report.append((name, err, cross))


def common(s):
    """rails, Vdd, Vcm, bias block, DUT with supplies and bias wiring; returns DUT pin positions"""
    p = s.vsrc('Vdd', 100, 200, 'vdd', 'GND', '3.3')
    s.to_vdd(p['p']); s.to_gnd(p['m'])
    p = s.vsrc('Vcm', 200, 200, 'vref', 'GND', '1.65')
    s.pin_lab('vref', p['p'], 0, -40); s.to_gnd(p['m'])
    bias = ('vbp', 'vbn', 'vbpc', 'vbnc', 'vabp', 'vabn')
    b = s.sub('Xb', 'd2s_bias_lp.sym', 700, 460, dict(vdd='vdd', vss='GND', **{n: n for n in bias}))
    s.to_vdd(b['vdd']); s.to_gnd(b['vss'])
    return b, bias


def dut(s, b, bias, name, nets):
    d = s.sub('Xd', f'{name}.sym', 1040, 40, nets)
    s.to_vdd(d['vdd']); s.to_gnd(d['vss'])
    for n in bias:   # top bias output to the leftmost DUT bias pin: the L-routes never cross
        s.w(n, b[n], (d[n][0], b[n][1]), d[n])
        s.lab(d[n][0], b[n][1], n)
    return d


def stim_diff(s, d, vd_value):
    """Vd drives dp; Ep, En put vinp, vinn symmetrically around vref (vinp - vinn = v(dp))"""
    p = s.vsrc('Vd', 300, 200, 'dp', 'GND', vd_value)
    s.pin_lab('dp', p['p'], 0, -40); s.to_gnd(p['m'])
    for name, (x, y), out, g in (('Ep', (560, -120), 'vinp', '0.5'), ('En', (560, 60), 'vinn', '-0.5')):
        e = s.dev('vcvs', name, x, y, dict(p=out, m='vref', cp='dp', cm='GND'), g)
        s.pin_lab('dp', e['cp'], -40, 0); s.pin_lab('GND', e['cm'], -40, 0); s.pin_lab('vref', e['m'], 0, 30)
    s.w('vinp', (560, -150), (640, -150), (640, d['vinp'][1]), d['vinp']); s.lab(640, -150, 'vinp')
    s.w('vinn', (560, 30), (660, 30), (660, d['vinn'][1]), d['vinn']); s.lab(660, 30, 'vinn')


def stim_dc(s, d):
    """Vp, Vn hold vinp and vinn at 1.65 V"""
    for name, x, net in (('Vp', 300, 'vinp'), ('Vn', 400, 'vinn')):
        p = s.vsrc(name, x, 200, net, 'GND', '1.65')
        s.to_gnd(p['m'])
        s.w(net, p['p'], (x, d[net][1]), d[net])
        s.lab(x, d[net][1], net)


def load_rc(s, d, rl=True):
    y = d['vout'][1]
    s.w('vout', d['vout'], (1420, y)); s.pin_lab('vout', (1420, y), 40, 0)
    if rl:
        r = s.dev('res', 'RL', 1320, y + 90, dict(P='vout', M='vref'), '1k', extra=' m=1')
        s.w('vout', r['P'], (1320, y)); s.pin_lab('vref', r['M'], 0, 40)
    c = s.dev('capa', 'CL', 1420, y + 90, dict(p='vout', m='GND'), '100p', extra=' m=1')
    s.w('vout', c['p'], (1420, y)); s.to_gnd(c['m'])


def loop_break(s, d, x_inj=1560):
    """Lb closes the loop at DC, Cb/Vinj inject the AC test signal at fb"""
    y = d['vout'][1]
    lb = s.dev('ind', 'Lb', 1320, y - 60, dict(p='vout', m='fb'), '1G', rot=2, extra=' m=1')
    s.w('vout', lb['p'], (1320, y)); s.pin_lab('fb', lb['m'], 0, -30)
    cb = s.dev('capa', 'Cb', x_inj, -200, dict(p='fb', m='inj'), '1', extra=' m=1')
    s.pin_lab('fb', cb['p'], 0, -30)
    vi = s.vsrc('Vinj', x_inj, -80, 'inj', 'GND', 'dc 0 ac 1')
    s.w('inj', cb['m'], vi['p']); s.lab(x_inj, -140, 'inj')
    s.to_gnd(vi['m'])


def header(s, deck, extra=None):
    s.text(f'{deck}: {first_comment(deck).split(": ", 1)[-1]}', 60, VDD_Y - 140, 0.5)
    s.text(extra or 'DUT and bias from the schematics in this directory; code block = the deck\'s .lib/.param/.save'
           ' lines and its .control section', 60, VDD_Y - 95, 0.3)
    s.code(code_lines(deck))


DUT_NETS = dict(vdd='vdd', vss='GND', vinp='vinp', vinn='vinn', vref='vref', vout='vout', vfb='vout',
                vbp='vbp', vbn='vbn', vbpc='vbpc', vbnc='vbnc', vabp='vabp', vabn='vabn')


def tb_diff(deck, vd_value):
    """dc, step, thd, noise: differential stimulus, vfb = vout, 1 kOhm || 100 pF"""
    s = TbSheet(OUT)
    b, bias = common(s)
    d = dut(s, b, bias, 'd2s_mpdda', DUT_NETS)
    stim_diff(s, d, vd_value)
    s.pin_lab('vref', d['vref'], -40, 0); s.pin_lab('vout', d['vfb'], -40, 0)
    load_rc(s, d)
    header(s, deck)
    save(s, deck)


def tb_op():
    s = TbSheet(OUT)
    b, bias = common(s)
    d = dut(s, b, bias, 'd2s_mpdda', DUT_NETS)
    stim_dc(s, d)
    s.pin_lab('vref', d['vref'], -40, 0); s.pin_lab('vout', d['vfb'], -40, 0)
    load_rc(s, d)
    header(s, 'tb_mpdda_op')
    save(s, 'tb_mpdda_op')


def tb_loop():
    s = TbSheet(OUT)
    b, bias = common(s)
    d = dut(s, b, bias, 'd2s_mpdda', dict(DUT_NETS, vfb='fb'))
    stim_dc(s, d)
    s.pin_lab('vref', d['vref'], -40, 0); s.pin_lab('fb', d['vfb'], -40, 0)
    load_rc(s, d)
    loop_break(s, d)
    header(s, 'tb_mpdda_loop', 'loop broken at the vfb gate: Lb closes it at DC, Cb and Vinj inject the AC'
           ' test signal; T = -v(vout)/v(fb)')
    save(s, 'tb_mpdda_loop')


def tb_lc2_loop():
    s = TbSheet(OUT)
    b, bias = common(s)
    d = dut(s, b, bias, 'd2s_lc2', dict(DUT_NETS, vfb='fb'))
    stim_dc(s, d)
    s.pin_lab('vref', d['vref'], -40, 0); s.pin_lab('fb', d['vfb'], -40, 0)
    y = d['vout'][1]
    s.w('vout', d['vout'], (1370, y)); s.lab(1250, y, 'vout')
    rs = s.dev('res', 'Rs', 1400, y, dict(P='vout', M='pad'), '586.9', rot=3, extra=' m=1')
    s.w('pad', rs['M'], (1560, y)); s.lab(1520, y, 'pad')
    cp = s.dev('capa', 'Cpad', 1480, y + 90, dict(p='pad', m='GND'), '2p', extra=' m=1')
    s.w('pad', cp['p'], (1480, y)); s.to_gnd(cp['m'])
    cl = s.dev('capa', 'CL', 1560, y + 90, dict(p='pad', m='GND'), '100p', extra=' m=1')
    s.w('pad', cl['p'], (1560, y)); s.to_gnd(cl['m'])
    loop_break(s, d, x_inj=1680)
    header(s, 'tb_lc2_loop', 'd2s_lc2 drives the pad through IOPadAnalog\'s 586.9 ohm (Rs); the loop is sensed at'
           ' vout (padres, near side); T = -v(vout)/v(fb)')
    save(s, 'tb_lc2_loop')


def tb_units():
    s = TbSheet(OUT)
    p = s.vsrc('Vdd', 100, 200, 'vdd', 'GND', '3.3')
    s.to_vdd(p['p']); s.to_gnd(p['m'])
    for name, x, net, val in (('Vref', 200, 'vref', '1.65'), ('Vx', 300, 'xd', '0')):
        p = s.vsrc(name, x, 200, net, 'GND', val)
        s.pin_lab(net, p['p'], 0, -40); s.to_gnd(p['m'])
    # tail bias: 5 uA into a 5u/6u diode (as d2s_bias_lp)
    s.mos('BP', P, 440, -220, 0, d='vbp', g='vbp', s='vdd', b='vdd', w='5u', l='6u')
    s.to_vdd((460, -250)); s.to_vdd((460, -220), (480, -220))
    s.w('vbp', (420, -220), (420, -160), (460, -160)); s.w('vbp', (460, -190), (460, -160), (460, 70))
    i = s.isrc('IBP', 460, 100, 'vbp', 'GND', '5u')
    s.to_gnd(i['m'])
    s.w('vbp', (460, -100), (1440, -100)); s.lab(560, -100, 'vbp')
    for k, (u, ex, ux) in enumerate((('XUA', 'EpA', 1000), ('XUB', 'EnB', 1400))):
        x1, y1 = f'x{k + 1}', f'y{k + 1}'
        gp, gn = ('gpa', 'vref') if k == 0 else ('vref', 'gnb')
        q = s.sub(u, 'unit_r2.sym', ux, 100, dict(x=x1, y=y1, gp=gp, gn=gn, vdd='vdd', vss='GND', vbp='vbp'))
        s.to_vdd(q['vdd']); s.w('vbp', q['vbp'], (q['vbp'][0], -100))
        s.to_gnd(q['vss'])
        fx = s.vsrc(f'Vfx{k + 1}', ux - 100, 300, x1, 'GND', '0.45')
        fy = s.vsrc(f'Vfy{k + 1}', ux, 300, y1, 'GND', '0.45')
        s.w(x1, q['x'], (q['x'][0], 220), (ux - 100, 220), fx['p']); s.lab(ux - 70, 220, x1)
        s.w(y1, q['y'], fy['p']); s.lab(ux, 230, y1, flip=1)
        s.to_gnd(fx['m']); s.to_gnd(fy['m'])
        # controlled source: EpA gpa = vref + v(xd), EnB gnb = vref - v(xd)
        ex_x = ux - 240
        out = gp if k == 0 else gn
        e = s.dev('vcvs', ex, ex_x, 110 + 40 * k - 40 * (1 - k), dict(p=out, m='vref', cp='xd', cm='GND'),
                  '1' if k == 0 else '-1')
        s.pin_lab('xd', e['cp'], -40, 0); s.pin_lab('GND', e['cm'], -40, 0); s.pin_lab('vref', e['m'], 0, 30)
        tgt = q['gp'] if k == 0 else q['gn']
        s.w(out, e['p'], (e['p'][0] + 40, e['p'][1]), (e['p'][0] + 40, tgt[1]), tgt)
        s.lab(e['p'][0] + 40, e['p'][1], out)
        other = q['gn'] if k == 0 else q['gp']
        s.pin_lab('vref', other, -40, 0)
    header(s, 'tb_units', 'fA = i(Vfx1) - i(Vfy1) for unit A (gp = vref + x), fB = i(Vfx2) - i(Vfy2) for unit B'
           ' (gn = vref - x); replace unit_r2 by unit_r, unit_t, unit_w or unit_q to test another unit')
    save(s, 'tb_units')


def tb_moscv():
    s = TbSheet(OUT, gnd_y=400)
    s.gnd_at = 480
    p = s.vsrc('Vg', 200, 200, 'g', 'GND', 'dc {1.65+vgw} ac 1')
    s.to_gnd(p['m']); s.w('g', p['p'], (200, 0), (400, 0)); s.lab(300, 0, 'g')
    s.mos('1', P, 420, 0, 0, d='w', g='g', s='w', b='w', w='14u', l='14u')
    s.w('w', (440, -30), (440, 0), (440, 30)); s.w('w', (440, 0), (560, 0), (560, 170))
    s.lab(520, 0, 'w', flip=1)
    p = s.vsrc('Vw', 560, 200, 'w', 'GND', '1.65')
    s.to_gnd(p['m'])
    p = s.vsrc('Vg2', 700, 200, 'g2', 'GND', 'dc 0 ac 1')
    s.to_gnd(p['m']); s.w('g2', p['p'], (700, 100), (820, 100), (820, 170)); s.lab(760, 100, 'g2')
    props = ('name=M\nmodel=cap_cmomi\nw=31e-6\nl=31e-6\nmmin=1\nmmax=4\nfeed=double\nsubblock=0\nm=1\n'
             'mm_ok=1\nspiceprefix=X')
    c = s.place('sg13cmos5l_pr/cap_cmomi.sym', 820, 200, 0, 0, props, dict(c0='g2', c1='GND'), 'XM')
    s.to_gnd(c['c1'])
    s.text('tb_moscv: ' + first_comment('tb_moscv').split(': ', 1)[-1], 60, -200, 0.5)
    s.text('X1: hv PMOS 14u x 14u, gate g against S/D/well w (accumulation); XM: cap_cmomi 31u x 31u', 60, -155, 0.3)
    s.code(code_lines('tb_moscv'), 60, 520)
    save(s, 'tb_moscv')


if __name__ == '__main__':
    tb_diff('tb_mpdda_dc', '0')
    tb_diff('tb_mpdda_step', 'pulse({-vstep} {vstep} 1u 1n 1n 4u 8u)')
    tb_diff('tb_mpdda_thd', 'sin(0 1 {fin})')
    tb_diff('tb_mpdda_noise', 'dc 0 ac 1')
    tb_op()
    tb_loop()
    tb_lc2_loop()
    tb_units()
    tb_moscv()
    bad = 0
    for name, err, cross in report:
        print(f'{name}: {len(err)} lint errors, {cross} wire crossings')
        for e in err:
            print('   ', e)
        bad += len(err)
    sys.exit(1 if bad else 0)
