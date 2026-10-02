#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Characterization of the two proof-of-concept class-AB pad drivers
(d2s_miller.spice, d2s_loadcomp.spice) in IHP sg13cmos5l.

Usage (IIC-OSIC-TOOLS, after `source .designinit`):
    python3 run_d2s.py > results.txt
Models: $MODELDIR, else $PDK_ROOT/$PDK/libs.tech/ngspice/models.
OSDI:   if $OSDI_DIR is set, psp103, r3_cmc and cap_cmomi are loaded from there;
        otherwise the ngspice .spiceinit in effect must load them.
Stimulus convention: vinp = vref + vd/2, vinn = vref - vd/2, vref = 1.65 V, VDD = 3.3 V.
Loop gain: vfb is fed from vout through 1 GH (DC closed) and driven by an AC source
through 1 F; T = -v(vout)/v(fb). Exact here because vfb only drives a MOS gate.
"""
import os, re, subprocess, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MODELDIR = os.environ.get('MODELDIR') or os.path.join(
    os.environ.get('PDK_ROOT', '/foss/pdks'), os.environ.get('PDK', 'ihp-sg13cmos5l'),
    'libs.tech', 'ngspice', 'models')
OSDI_DIR = os.environ.get('OSDI_DIR')
WORK = tempfile.mkdtemp(prefix='d2s_')
if OSDI_DIR:
    with open(os.path.join(WORK, '.spiceinit'), 'w') as f:
        f.write('set ngbehavior=hsa\nset ng_nomodcheck\n')
        for m in ('psp103', 'psp103_nqs', 'r3_cmc', 'cap_cmomi'):
            f.write(f"osdi {os.path.join(OSDI_DIR, m + '.osdi')}\n")

CORNERS = {  # name: (mos, res, temp)
    'tt 27C': ('mos_tt', 'res_typ', 27), 'ss 125C': ('mos_ss', 'res_wcs', 125),
    'ff -40C': ('mos_ff', 'res_bcs', -40), 'sf 27C': ('mos_sf', 'res_typ', 27),
    'fs 27C': ('mos_fs', 'res_typ', 27)}
LOADS = {
    '50R': 'RL vout vref 50\nCL vout 0 20p\n',          # 50 ohm returned to V_CM, 20 pF
    '1k||100p': 'RL vout vref 1k\nCL vout 0 100p\n',
    '1k(gnd)||100p': 'RL vout 0 1k\nCL vout 0 100p\n',  # returned to ground: sourcing only
    '20p': 'CL vout 0 20p\n', '100p': 'CL vout 0 100p\n', '1n': 'CL vout 0 1n\n'}


def header(variant, corner='tt 27C', iab='5u', dpar=''):
    mos, res, temp = CORNERS[corner]
    dut = {'miller': 'd2s_miller', 'lc': 'd2s_loadcomp'}[variant]
    h = (f".lib {MODELDIR}/cornerMOShv.lib {mos}\n.lib {MODELDIR}/cornerRES.lib {res}\n"
         f".lib {MODELDIR}/cornerCAP.lib cap_typ\n.temp {temp}\n"
         f".include {HERE}/d2s_bias.spice\n.include {HERE}/{dut}.spice\n"
         f"Vdd vdd 0 3.3\nVcm vref 0 1.65\nXb vdd 0 vbp vbn vbpc vbnc vabp vabn d2s_bias iab={iab}\n")
    return h, (lambda fb='vout': f"Xd vdd 0 vinp vinn vref vout {fb} vbp vbn vbpc vbnc vabp vabn {dut} {dpar}\n")


def sim(net, ctl):
    with open(os.path.join(WORK, 'tb.cir'), 'w') as f:
        f.write('* d2s\n' + net + '.control\n' + ctl + '.endc\n.end\n')
    r = subprocess.run(['ngspice', '-b', 'tb.cir'], cwd=WORK, capture_output=True, text=True)
    try:
        return np.loadtxt(os.path.join(WORK, 'out.txt'), ndmin=2)
    except OSError:
        raise SystemExit(r.stdout + r.stderr)
    finally:
        if os.path.exists(os.path.join(WORK, 'out.txt')):
            os.remove(os.path.join(WORK, 'out.txt'))


DIFF = "Ep vinp vref dp 0 0.5\nEn vinn vref dp 0 -0.5\n"


def dc(h, dut, load):
    sv = 'v(vout) vdd#branch @n.xd.xop.nsg13_hv_pmos[ids] @n.xd.xon.nsg13_hv_nmos[ids]'
    a = sim(h + dut() + LOADS[load] + "Vd dp 0 0\n" + DIFF + f".save {sv}\n",
            f"dc Vd -1 1 0.01\nwrdata out.txt {sv}\n")
    vd, vo, idd, ip, inn = a[:, 0], a[:, 1] - 1.65, -a[:, 3], np.abs(a[:, 5]), np.abs(a[:, 7])
    small = np.abs(vd) <= 0.2
    k = np.polyfit(vd[small], vo[small], 1)
    return dict(gain=k[0], off=k[1] * 1e3, nonlin=np.max(np.abs(vo - np.polyval(k, vd))) * 1e3,
                iqp=np.interp(0, vd, ip) * 1e6, iqn=np.interp(0, vd, inn) * 1e6, idd=np.interp(0, vd, idd) * 1e6,
                imin=min(min(np.interp(s, vd, ip), np.interp(s, vd, inn)) for s in (-1, 1)) * 1e6)


def loop(h, dut, load):
    a = sim(h + dut('fb') + LOADS[load] + "Vp vinp 0 1.65\nVn vinn 0 1.65\nLb vout fb 1G\nCb fb inj 1\nVinj inj 0 dc 0 ac 1\n",
            "ac dec 50 10 1G\nlet T=-v(vout)/v(fb)\nwrdata out.txt vdb(T) vp(T)\n")
    f, db, ph = a[:, 0], a[:, 1], np.degrees(np.unwrap(a[:, 3]))
    i = np.where(np.diff(np.sign(db)) < 0)[0]
    if not len(i):
        return dict(t0=db[0], fc=None, pm=None)
    fc = np.interp(0, [db[i[0] + 1], db[i[0]]], [f[i[0] + 1], f[i[0]]])
    pm = (np.interp(fc, f, ph) + 180) % 360
    return dict(t0=db[0], fc=fc / 1e6, pm=pm - 360 if pm > 180 else pm)


def step(h, dut, load):
    a = sim(h + dut() + LOADS[load] + "Vd dp 0 pulse(-0.5 0.5 1u 1n 1n 4u 8u)\n" + DIFF,
            "tran 2n 9u\nwrdata out.txt v(vout)\n")
    t, v = a[:, 0], a[:, 1]
    v0, v1 = np.interp(0.99e-6, t, v), np.interp(4.9e-6, t, v)
    m = (t > 1e-6) & (t < 5e-6)
    ts, seg = t[m], v[m]
    t10, t90 = ts[np.argmax(seg > v0 + 0.1 * (v1 - v0))], ts[np.argmax(seg > v0 + 0.9 * (v1 - v0))]
    out = np.where(np.abs(seg - v1) > 0.01 * abs(v1 - v0))[0]
    return dict(os=(seg.max() - v1) / (v1 - v0) * 100, sr=0.8 * (v1 - v0) / (t90 - t10) / 1e6,
                ts=(ts[out[-1]] - 1e-6) * 1e9 if len(out) else 0.0)


def thd(h, dut, load, f):
    per = 1 / f
    a = sim(h + dut() + LOADS[load] + f"Vd dp 0 sin(0 1 {f})\n" + DIFF,
            f"tran {per / 400} {6 * per} {2 * per}\nwrdata out.txt v(vout)\n")
    # exactly 4 periods, rectangular window: harmonic n falls on bin 4n, no leakage.
    # THD = root-sum-square of h2..h7 over h1. (Until 2026-10-02 this summed Hann-window bin
    # magnitudes linearly over the harmonics, which read 3-6 dB too high.)
    tt = np.linspace(2 * per, 6 * per, 4096, endpoint=False)
    F = np.abs(np.fft.rfft(np.interp(tt, a[:, 0], a[:, 1])))
    return 20 * np.log10(np.sqrt(sum(F[4 * n] ** 2 for n in range(2, 8))) / F[4])


def fmt_loop(lg):
    return f"T0={lg['t0']:5.1f}dB fc={lg['fc']:5.2f}MHz PM={lg['pm']:5.1f}" if lg['fc'] else f"T0={lg['t0']:5.1f}dB (no crossover)"


def full(variant, loads, **kw):
    h, dut = header(variant, **kw)
    for L in loads:
        d, lg, st = dc(h, dut, L), loop(h, dut, L), step(h, dut, L)
        print(f"{L:13s} gain={d['gain']:.4f} off={d['off']:6.2f}mV nonlin={d['nonlin']:5.2f}mV "
              f"IqP/IqN={d['iqp']:4.0f}/{d['iqn']:4.0f}uA Idd={d['idd']:5.0f}uA Imin={d['imin']:4.0f}uA | {fmt_loop(lg)} | "
              f"step: OS={st['os']:4.1f}% SR={st['sr']:5.2f}V/us t1%={st['ts']:5.0f}ns | "
              f"THD 10k/100k={thd(h, dut, L, 10e3):5.1f}/{thd(h, dut, L, 100e3):5.1f}dB")


if __name__ == '__main__':
    print(f"# models: {MODELDIR}\n# osdi: {OSDI_DIR or '(from .spiceinit)'}")
    print("# vd = vinp - vinn swept +-1 V; gain/offset from |vd|<=0.2 V fit; nonlin = max deviation over +-1 V;")
    print("# Imin = smaller output-device current at vd = +-1 V; step: vd -0.5 -> +0.5 V, i.e. vout vref-0.25 V -> vref+0.25 V; SR = 10-90 % rate (includes linear settling)")
    for v, name in [('miller', 'A: two-stage, Miller compensated'), ('lc', 'B: single-stage, load compensated')]:
        print(f"\n== Topology {name}, tt 27C, I_AB = 5 uA")
        full(v, ['50R', '1k||100p', '1k(gnd)||100p', '20p', '100p', '1n'])
        print(f"\n== Topology {name}: loop gain vs C_L (no resistive load), tt 27C")
        h, dut = header(v)
        row = []
        for c in ['5p', '10p', '20p', '50p', '100p', '300p', '1n']:
            LOADS['c'] = f'CL vout 0 {c}\n'
            row.append(f"{c}: {fmt_loop(loop(h, dut, 'c'))}")
        print('\n'.join(row))
        print(f"\n== Topology {name}: corners (bias reference currents ideal)")
        for c in CORNERS:
            h, dut = header(v, corner=c)
            for L in (['1k||100p', '100p'] if v == 'miller' else ['20p', '100p']):
                d, lg = dc(h, dut, L), loop(h, dut, L)
                print(f"{c:8s} {L:9s} gain={d['gain']:.4f} off={d['off']:6.2f}mV IqP/IqN={d['iqp']:4.0f}/{d['iqn']:4.0f}uA Idd={d['idd']:5.0f}uA {fmt_loop(lg)}")
    print("\n== Topology A: quiescent current vs 50 ohm performance, tt 27C")
    for iab in ['5u', '10u', '20u']:
        print(f"I_AB={iab}: ", end='')
        full('miller', ['50R'], iab=iab)
