#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
CACE testbench templates for d2s_miller (verification/cace/templates/d2s_miller_tb_*.sch).

DUT:      d2s_miller (xschem/d2s_miller.sch, hand-drawn). CACE turns d2s_miller.sym into a
          primitive and .includes its own netlist of the DUT (CACE{DUT_path}).
Fixture:  d2s_bias (xschem/d2s_bias.sch, ideal reference currents into diode replicas).
CACE DUT: d2s_miller_biased (xschem/d2s_miller_biased.sch, written by wrapper() below) =
          d2s_miller + d2s_bias, bias nets as pins. A wrapper because CACE's testbench
          netlisting only finds the DUT symbol; a second hierarchical symbol in a template
          is not on xschem's library path (the PDK xschemrc resets XSCHEM_LIBRARY_PATH).
Bias-source quality, applied to all six reference currents of d2s_bias at once:
          ibias_err  common relative error (%), an extra source ibias_err*I_k in parallel
          va_bias    "Early voltage" of the reference sources: R_k = va_bias / I_k in parallel,
                     returned to the source's far rail (vss for vbp/vbpc/vabp, vdd for vbn/vbnc/vabn)
Stimulus: vinp = vicm + v(dp)/2, vinn = vicm - v(dp)/2 (two VCVS), feedback pair on vref / vfb.
Load:     RL from vout to vterm, CL from vout to ground.

Drawing helpers come from gen_tb_xschem.py (same directory). Run:
    python3 gen_cace_templates.py
"""
import os
import re
import gen_tb_xschem as g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'verification', 'cace', 'templates')
DUT_NAME = 'd2s_miller_biased'   # wrapper: d2s_miller + d2s_bias fixture, bias nets as pins
AMP = 'd2s_miller'

VDD_Y, GND_Y, X_END = -300, 700, 1640
DUT = (1040, 40)
BIAS = (700, 460)
EP, EN = (560, -120), (560, 60)
# six reference currents of d2s_bias: (bias net, nominal current, sink to vss / source from vdd)
REFS = [('vbp', 20e-6, 'sink'), ('vbn', 50e-6, 'src'), ('vbpc', 5e-6, 'sink'),
        ('vbnc', 5e-6, 'src'), ('vabp', 5e-6, 'sink'), ('vabn', 5e-6, 'src')]

MODEL = ['.lib cornerMOShv.lib mos_CACE{corner_mos}',
         '.lib cornerRES.lib res_CACE{corner_r}',
         '.lib cornerCAP.lib cap_CACE{corner_c=typ}']


def head(solver='klu'):
    return ['.include CACE{DUT_path}',
            '.temp CACE{temp}',
            f'.options savecurrents {solver} method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 '
            'SEED=CACE[CACE{seed=12345} + CACE{iterations=0}]',
            '.option warn=1']


def ECHO(*names):
    # Relative file name: CACE runs ngspice in the run directory (= CACE{simpath}). With the
    # absolute CACE{simpath}/... the line gets long enough for xschem to wrap it with a '+'
    # continuation, which ngspice does not honour inside .control (seen with xschem 3.4.4).
    return 'echo ' + ' '.join(f'$&{n}' for n in names) + ' > CACE{filename}_CACE{N}.data'


class Sheet(g.Sheet):
    def write(self, fn):
        hdr = 'v {xschem version=3.4.4 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n'
        os.makedirs(OUT, exist_ok=True)
        open(os.path.join(OUT, fn), 'w').write(hdr + '\n'.join(self.L) + '\n')


def esc(lines):
    return '\n'.join(lines).replace('{', '\\{').replace('}', '\\}').replace('"', '\\"')


def code(s, ngspice_lines):
    s.L.append(f'C {{devices/code_shown.sym}} -1000 -420 0 0 {{name=MODEL only_toplevel=true\n'
               f'format="tcleval( @value )"\nvalue="\n{esc(MODEL)}\n"}}')
    s.L.append(f'C {{devices/code_shown.sym}} -1000 -300 0 0 {{name=NGSPICE\nsimulator=ngspice\n'
               f'only_toplevel=false\nvalue="\n{esc(ngspice_lines)}\n"}}')


def common(s, vdd_value='CACE\\{vdd\\}', vic_value='CACE\\{vicm=1.65\\}'):
    """Rails, supplies, vicm/vterm sources, bias fixture with quality perturbation, DUT."""
    s.W('vdd', (60, VDD_Y), (X_END, VDD_Y)); s.name('vdd', (60, VDD_Y))
    s.W('GND', (60, GND_Y), (X_END, GND_Y))
    s.C('devices/gnd.sym', 800, GND_Y, 'name=l0 lab=GND')
    p = s.C('devices/vsource.sym', 100, 200, f'name=Vdd value="{vdd_value}" savecurrent=false')
    s.W('vdd', p['p'], (p['p'][0], VDD_Y)); s.W('GND', p['m'], (p['m'][0], GND_Y))
    p = s.C('devices/vsource.sym', 200, 200, 'name=Vref value=CACE\\{vref=1.65\\} savecurrent=false')
    s.lab('vref', p['p'], 0, -40); s.W('GND', p['m'], (p['m'][0], GND_Y))
    p = s.C('devices/vsource.sym', 400, 200, f'name=Vic value="{vic_value}" savecurrent=false')
    s.lab('vic', p['p'], 0, -40); s.W('GND', p['m'], (p['m'][0], GND_Y))
    p = s.C('devices/vsource.sym', 1580, 400, 'name=Vterm value=CACE\\{vterm=1.65\\} savecurrent=false')
    s.lab('vterm', p['p'], 0, -40); s.W('GND', p['m'], (p['m'][0], GND_Y))
    d = s.C(f'{DUT_NAME}.sym', *DUT, 'name=x1')
    s.W('vdd', d['vdd'], (d['vdd'][0], VDD_Y)); s.W('GND', d['vss'], (d['vss'][0], GND_Y))
    for i, net in enumerate(['vbp', 'vbn', 'vbpc', 'vbnc', 'vabp', 'vabn']):
        s.lab(net, d[net], 0, 40 + 20 * i)   # staggered so neighbouring labels do not touch
    # bias-source quality fixture, below the ground bus
    for i, (net, inom, kind) in enumerate(REFS):
        x = 160 + 220 * i
        top, bot = (net, 'GND') if kind == 'sink' else ('vdd', net)
        ii = s.C('devices/isource.sym', x, 900,
                 f'name=IQ{net} value=CACE[CACE\\{{ibias_err=0\\}}*{inom:g}]')
        r = s.C('devices/res.sym', x + 80, 900,
                f'name=RQ{net} value=CACE[CACE\\{{va_bias=1e12\\}}/{inom:g}] m=1')
        for e in (ii, r):
            pp, mm = (e['p'], e['m']) if 'p' in e else (e['P'], e['M'])
            s.lab(top, pp, 0, -30); s.lab(bot, mm, 0, 30)
    s.text('bias-source quality: extra ibias_err*I_k and R_k = va_bias/I_k across each d2s_bias reference',
           160, 1000, 0.3)
    return d


def diff_inputs(s, d, vd_value):
    p = s.C('devices/vsource.sym', 300, 200, f'name=Vd value="{vd_value}" savecurrent=false')
    s.lab('dp', p['p'], 0, -40); s.W('GND', p['m'], (p['m'][0], GND_Y))
    ep = s.C('devices/vcvs.sym', *EP, 'name=Ep value=0.5')
    en = s.C('devices/vcvs.sym', *EN, 'name=En value=-0.5')
    for e in (ep, en):
        s.lab('dp', e['cp'], -40, 0); s.lab('GND', e['cm'], -40, 0)
        s.lab('vic', e['m'], 0, 30)
    s.W('vinp', ep['p'], (640, ep['p'][1]), (640, d['vinp'][1]), d['vinp']); s.name('vinp', (640, ep['p'][1]))
    s.W('vinn', en['p'], (660, en['p'][1]), (660, d['vinn'][1]), d['vinn']); s.name('vinn', (660, en['p'][1]))
    s.lab('vref', d['vref'], -40, 0)


def load(s, d, cval='CACE\\{cload=100p\\}'):
    y = d['vout'][1]
    s.W('vout', d['vout'], (1440, y)); s.lab('vout', (1440, y), 40, 0)
    r = s.C('devices/res.sym', 1320, y + 90, 'name=RL value=CACE\\{rload=1k\\} m=1')
    s.W('vout', r['P'], (r['P'][0], y)); s.lab('vterm', r['M'], 0, 40)
    c = s.C('devices/capa.sym', 1440, y + 90, f'name=CL m=1 value={cval}')
    s.W('vout', c['p'], (c['p'][0], y)); s.W('GND', c['m'], (c['m'][0], GND_Y))
    return y


def title(s, txt):
    s.text(f'CACE template: {txt}', 60, VDD_Y - 140, 0.6)
    # CACE only puts simpath into a run's condition set if the template mentions it, and its
    # plotting code expects the key; a schematic text is not netlisted, so no long line results
    s.text('run directory: CACE\\{simpath\\}', 60, VDD_Y - 70, 0.3)


# ---------------------------------------------------------------------------------------
def tb_dc():
    s = Sheet(); d = common(s)
    diff_inputs(s, d, 'dc 0'); s.lab('vout', d['vfb'], -40, 0); load(s, d)
    title(s, 'DC transfer vout(vd), closed loop (vfb = vout)')
    ids = '@n.x1.xd.xop.nsg13_hv_pmos[ids] @n.x1.xd.xon.nsg13_hv_nmos[ids]'
    code(s, head() + [
        '.control',
        f'save v(vout) v(vref) v(dp) i(vdd) {ids}',
        'dc Vd -CACE{vdmax=1} CACE{vdmax=1} CACE{vdstep=0.01}',
        'let vo = v(vout) - v(vref)',
        'meas dc vo0 find vo at=0',
        'meas dc vop find vo at=CACE{vdlin=0.2}',
        'meas dc vom find vo at=-CACE{vdlin=0.2}',
        '* small-signal gain and output offset (vout - vref at vd = 0)',
        'let Gain = (vop - vom) / (2*CACE{vdlin=0.2})',
        'let Vos_out = vo0',
        '* integral nonlinearity: max deviation from the small-signal line over +-vdmax',
        'let dev = abs(vo - vo0 - Gain*v(dp))',
        'meas dc INL max dev',
        'let idd = -i(vdd)',
        'meas dc Idd find idd at=0',
        '* output devices: quiescent currents, and the smaller of the two at full scale',
        'let ip = abs(@n.x1.xd.xop.nsg13_hv_pmos[ids])',
        'let inn = abs(@n.x1.xd.xon.nsg13_hv_nmos[ids])',
        'meas dc IqP find ip at=0',
        'meas dc IqN find inn at=0',
        'let imn = 0.5*(ip + inn - abs(ip - inn))',
        'meas dc ImA find imn at=-CACE{vdmax=1}',
        'meas dc ImB find imn at=CACE{vdmax=1}',
        'let Imin = 0.5*(ImA + ImB - abs(ImA - ImB))',
        ECHO('Gain', 'Vos_out', 'INL', 'Idd', 'IqP', 'IqN', 'Imin'),
        '.endc'])
    s.write(f'{DUT_NAME}_tb_dc.sch')


def tb_loop():
    s = Sheet(); d = common(s)
    s.lab('vic', d['vinp'], -40, 0); s.lab('vic', d['vinn'], -40, 0); s.lab('vref', d['vref'], -40, 0)
    s.lab('fb', d['vfb'], -40, 0)
    y = load(s, d)
    lb = s.C('devices/ind.sym', 1320, y - 60, 'name=Lb m=1 value=1G', rot=2)
    s.W('vout', lb['p'], (lb['p'][0], y)); s.lab('fb', lb['m'], 0, -30)
    cb = s.C('devices/capa.sym', 1580, -200, 'name=Cb m=1 value=1')
    s.lab('fb', cb['p'], 0, -30)
    vi = s.C('devices/vsource.sym', 1580, -80, 'name=Vinj value="dc 0 ac 1" savecurrent=false')
    s.W('inj', cb['m'], vi['p']); s.name('inj', vi['p'])
    s.lab('GND', vi['m'], 0, 30)
    title(s, 'loop gain T = -v(vout)/v(fb), loop broken at the vfb gate (DC closed through Lb)')
    code(s, head() + [
        '.control',
        'save v(vout) v(fb)',
        'ac dec 50 1 1G',
        'let T = -v(vout)/v(fb)',
        'let Tdb = vdb(T)',
        'let Tph = cph(T)*180/pi',
        'meas ac T0 find Tdb at=10',
        'let fc = 0',
        'meas ac fc when Tdb=0 fall=1',
        'let phc = -180',
        'meas ac phc find Tph when Tdb=0 fall=1',
        'let PM = 180 + phc',
        '* gain margin; stays at 1000 dB if the phase never reaches -180 deg',
        'let gmdb = -1000',
        'meas ac gmdb find Tdb when Tph=-180 cross=1',
        'let GM = -gmdb',
        ECHO('T0', 'fc', 'PM', 'GM'),
        '.endc'])
    s.write(f'{DUT_NAME}_tb_loop.sch')


def tb_ac():
    s = Sheet(); d = common(s, vdd_value='dc CACE\\{vdd\\} ac 0', vic_value='dc CACE\\{vicm=1.65\\} ac 0')
    diff_inputs(s, d, 'dc 0 ac 1'); s.lab('vout', d['vfb'], -40, 0)
    y = load(s, d)
    it = s.C('devices/isource.sym', 1540, y + 90, 'name=Itest value="dc 0 ac 0"')
    s.lab('GND', it['p'], 0, -30); s.lab('vout', it['m'], 0, 30)
    title(s, 'closed-loop AC: gain/bandwidth, PSRR, CMRR, output impedance')
    code(s, head() + [
        '.control',
        'save v(vout)',
        '* 1) differential signal: Vd ac 1',
        'ac dec 50 1 1G',
        'let adb = vdb(vout)',
        'meas ac Acl find adb at=1k',
        'let adn = adb - Acl',
        'let f3db = 0',
        'meas ac f3db when adn=-3 fall=1',
        'set s_acl = $&Acl',
        'set s_f3db = $&f3db',
        '* 2) supply: vdd ac 1; PSRR referred to the output, -20 log |vout/vdd|',
        'alter @vd[acmag]=0',
        'alter @vdd[acmag]=1',
        'ac dec 50 1 1G',
        'let psr = -vdb(vout)',
        'meas ac PSRR_1k find psr at=1k',
        'meas ac PSRR_100k find psr at=100k',
        'set s_p1 = $&PSRR_1k',
        'set s_p2 = $&PSRR_100k',
        '* 3) input common mode: vic ac 1; CMRR = A_dm / A_cm',
        'alter @vdd[acmag]=0',
        'alter @vic[acmag]=1',
        'ac dec 50 1 1G',
        'let cmdb = vdb(vout)',
        'meas ac Acm find cmdb at=1k',
        'set s_acm = $&Acm',
        '* 4) closed-loop output impedance: 1 A ac into vout',
        'alter @vic[acmag]=0',
        'alter @itest[acmag]=1',
        'ac dec 50 1 1G',
        'let zo = mag(v(vout))',
        'meas ac Zout_1k find zo at=1k',
        'meas ac Zout_1M find zo at=1meg',
        'let Acl_dB = $s_acl',
        'let f3dB = $s_f3db',
        'let PSRR_1k = $s_p1',
        'let PSRR_100k = $s_p2',
        'let CMRR_1k = $s_acl - $s_acm',
        ECHO('Acl_dB', 'f3dB', 'PSRR_1k', 'PSRR_100k', 'CMRR_1k', 'Zout_1k', 'Zout_1M'),
        '.endc'])
    s.write(f'{DUT_NAME}_tb_ac.sch')


def tb_tran():
    s = Sheet(); d = common(s)
    diff_inputs(s, d, 'pulse(-CACE\\{vstep=0.5\\} CACE\\{vstep=0.5\\} 1u 1n 1n 4u 8u)')
    s.lab('vout', d['vfb'], -40, 0); load(s, d)
    title(s, 'step response: vd steps -vstep -> +vstep at 1 us, back at 5 us')
    code(s, head() + [
        '.control',
        'save v(vout)',
        'tran CACE{tstep=2n} 9u',
        'meas tran v0 find v(vout) at=0.99u',
        'meas tran v1 find v(vout) at=4.9u',
        'let dv = v1 - v0',
        '* normalized output: 0 before the rising step, 1 after it',
        'let vn = (v(vout) - v0) / dv',
        'meas tran t10r when vn=0.1 rise=1 from=1u to=5u',
        'meas tran t90r when vn=0.9 rise=1 from=1u to=5u',
        'meas tran t90f when vn=0.9 fall=1 from=5u to=9u',
        'meas tran t10f when vn=0.1 fall=1 from=5u to=9u',
        'let SR_rise = 0.8*dv / (t90r - t10r)',
        'let SR_fall = 0.8*dv / (t10f - t90f)',
        'meas tran vnmax max vn from=1u to=5u',
        'let Overshoot = vnmax - 1',
        '* settling: last time the error leaves the +-1 % band',
        'let er = abs(vn - 1)',
        'let ef = abs(vn)',
        'let tsr = 1u',
        'let tsf = 5u',
        'meas tran tsr when er=0.01 cross=last from=1u to=5u',
        'meas tran tsf when ef=0.01 cross=last from=5u to=9u',
        'let ts_rise = tsr - 1u',
        'let ts_fall = tsf - 5.001u',
        ECHO('SR_rise', 'SR_fall', 'Overshoot', 'ts_rise', 'ts_fall'),
        '.endc'])
    s.write(f'{DUT_NAME}_tb_tran.sch')


def tb_thd():
    s = Sheet(); d = common(s)
    diff_inputs(s, d, 'sin(0 CACE\\{vdamp=1\\} CACE\\{fin=10k\\})')
    s.lab('vout', d['vfb'], -40, 0); load(s, d)
    title(s, 'THD: sine of amplitude vdamp on vd, harmonics 2..7 by direct Fourier sums')
    code(s, head() + [
        '.control',
        'save v(vout)',
        '* 2 periods settling, then exactly 4 periods sampled at 1024 points',
        'tran CACE[4/(1024*CACE{fin=10k})] CACE[6/CACE{fin=10k}] CACE[2/CACE{fin=10k}]',
        'linearize v(vout)',
        'let vv = v(vout)[0,1023]',
        'let ph = 2*pi*CACE{fin=10k}*(time[0,1023] - time[0])',
        'let h1 = 2*sqrt(mean(vv*cos(ph))^2 + mean(vv*sin(ph))^2)',
        'let hs = 0',
        'let k = 2',
        'while k <= 7',
        '  let hk = 2*sqrt(mean(vv*cos(k*ph))^2 + mean(vv*sin(k*ph))^2)',
        '  let hs = hs + hk^2',
        '  let k = k + 1',
        'end',
        'let THD = 20*log10(sqrt(hs)/h1)',
        'let Vout_amp = h1',
        ECHO('THD', 'Vout_amp'),
        '.endc'])
    s.write(f'{DUT_NAME}_tb_thd.sch')


def tb_noise():
    s = Sheet(); d = common(s)
    diff_inputs(s, d, 'dc 0 ac 1'); s.lab('vout', d['vfb'], -40, 0); load(s, d)
    title(s, 'output noise, closed loop; input-referred = output / gain')
    code(s, head(solver='sparse') + [
        '* .noise does not run with KLU (see the OgueyAebischerBias noise template), hence sparse',
        '.control',
        '* each sweep starts at its spot frequency, so index 0 is the spot value',
        'noise v(vout) vd dec 10 1k 10k',
        'setplot noise1',
        'let en_1k = onoise_spectrum[0]',
        'set s_n1 = $&en_1k',
        'noise v(vout) vd dec 10 100k 1meg',
        'setplot noise3',
        'let en_100k = onoise_spectrum[0]',
        'set s_n2 = $&en_100k',
        'noise v(vout) vd dec 20 CACE{fn_lo=10} CACE{fn_hi=10meg}',
        'setplot noise6',
        'let Vn_int = onoise_total',
        'let En_1k = $s_n1',
        'let En_100k = $s_n2',
        ECHO('En_1k', 'En_100k', 'Vn_int'),
        '.endc'])
    s.write(f'{DUT_NAME}_tb_noise.sch')


def tb_drive():
    s = Sheet(); d = common(s)
    diff_inputs(s, d, 'dc 0'); s.lab('vout', d['vfb'], -40, 0)
    y = load(s, d)
    rf = s.C('devices/res.sym', 1540, y + 90, 'name=Rf value=1e12 m=1')
    s.lab('vout', rf['P'], 0, -30); s.lab('vf', rf['M'], 0, 30)
    vf = s.C('devices/vsource.sym', 1540, 300, 'name=Vforce value=CACE\\{vforce=1.65\\} savecurrent=false')
    s.lab('vf', vf['p'], 0, -30); s.lab('GND', vf['m'], 0, 30)
    title(s, 'output drive: swing into the load at full overdrive, then short-circuit current into vforce')
    code(s, head() + [
        '.control',
        'save v(vout) i(vforce)',
        '* 1) swing: Rf open, vd = +-vdbig',
        'dc Vd -CACE{vdbig=3} CACE{vdbig=3} CACE[2*CACE{vdbig=3}]',
        'meas dc Vout_max find v(vout) at=CACE{vdbig=3}',
        'meas dc Vout_min find v(vout) at=-CACE{vdbig=3}',
        'set s_vmax = $&Vout_max',
        'set s_vmin = $&Vout_min',
        '* 2) short circuit: Rf = 1 mohm to vforce',
        'alter @rf[resistance]=1m',
        'dc Vd -CACE{vdbig=3} CACE{vdbig=3} CACE[2*CACE{vdbig=3}]',
        'let isc = i(vforce)',
        'meas dc Isc_src find isc at=CACE{vdbig=3}',
        'meas dc isnk find isc at=-CACE{vdbig=3}',
        'let Isc_snk = -isnk',
        'let Vout_max = $s_vmax',
        'let Vout_min = $s_vmin',
        ECHO('Vout_max', 'Vout_min', 'Isc_src', 'Isc_snk'),
        '.endc'])
    s.write(f'{DUT_NAME}_tb_drive.sch')


def wrapper():
    """xschem/d2s_miller_biased.{sch,sym}: d2s_miller (xd) + d2s_bias fixture (xb), same pins as
    d2s_miller, bias nets brought out as inout pins so testbenches can perturb them."""
    XS = g.XS
    s = Sheet()
    d = s.C(f'{AMP}.sym', 700, 0, 'name=xd')
    b = s.C('d2s_bias.sym', 300, 400, 'name=xb')
    for net in ['vbp', 'vbn', 'vbpc', 'vbnc', 'vabp', 'vabn']:
        s.W(net, b[net], (d[net][0], b[net][1]), d[net])
        s.name(net, (d[net][0], b[net][1]))
    for pin, dx in (('vinp', -60), ('vinn', -60), ('vref', -60), ('vfb', -60)):
        s.lab(pin, d[pin], dx, 0)
    s.lab('vout', d['vout'], 60, 0); s.lab('vdd', d['vdd'], 0, -40); s.lab('vss', d['vss'], -40, 0)
    s.lab('vdd', b['vdd'], 0, -40); s.lab('vss', b['vss'], 0, 40)
    pins = [('vdd', 'iopin'), ('vss', 'iopin'), ('vinp', 'ipin'), ('vinn', 'ipin'), ('vref', 'ipin'),
            ('vout', 'iopin'), ('vfb', 'ipin')] + [(n, 'iopin') for n in ['vbp', 'vbn', 'vbpc', 'vbnc', 'vabp', 'vabn']]
    for i, (n, kind) in enumerate(pins):       # port order = d2s_miller port order
        s.L.append(f'C {{devices/{kind}.sym}} 60 {-200 + 40 * i} 0 0 {{name=p{i} lab={n}}}')
    s.text('d2s_miller + d2s_bias test fixture (CACE DUT); bias nets are pins for bias-quality perturbation',
           60, -300, 0.4)
    hdr = 'v {xschem version=3.4.4 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n'
    open(os.path.join(XS, f'{DUT_NAME}.sch'), 'w').write(hdr + '\n'.join(s.L) + '\n')
    sym = open(os.path.join(XS, f'{AMP}.sym')).read()
    sym = re.sub(r'(name=(vbp|vbn|vbpc|vbnc|vabp|vabn)) dir=in', r'\1 dir=inout', sym)
    open(os.path.join(XS, f'{DUT_NAME}.sym'), 'w').write(sym)


if __name__ == '__main__':
    wrapper()
    for f in (tb_dc, tb_loop, tb_ac, tb_tran, tb_thd, tb_noise, tb_drive):
        f()
    print('written', sorted(os.listdir(OUT)))
