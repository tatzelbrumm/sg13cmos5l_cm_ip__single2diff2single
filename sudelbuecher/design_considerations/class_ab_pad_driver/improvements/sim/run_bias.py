#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Every number in ../bias.md: real bias generators for d2s_mpdda (d2s_bias_ref.spice).

Usage (IIC-OSIC-TOOLS, after `source .designinit`, from this directory):
    python3 run_bias.py > results_bias.txt          # all sections, ~20 min
    python3 run_bias.py accuracy supply             # selected sections
Sections: accuracy supply startup mc driver corners rails area
Model / OSDI paths as run_d2s.py ($MODELDIR, $OSDI_DIR).
Bias variants: ideal (d2s_bias_lp's ideal sources on the same diodes and rails), in, out, oa, bg.
The driver is d2s_mpdda with OP / ON moved to separate rails vddo / vsso (built from d2s_mpdda.spice
here); ON's bulk is its frame's local substrate tap ring on vsso.
"""
import os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import run_d2s as r

HERE = os.path.dirname(os.path.abspath(__file__))
NOM = {'bp': 5e-6, 'bn': 5e-6, 'bnc': 2e-6, 'bpc': 2e-6, 'abp': 5e-6, 'abn': 5e-6}
DRAIN = {'bp': 'XBP', 'bn': 'XBN', 'bnc': 'XBNC', 'bpc': 'XBPC', 'abp': 'XRP2', 'abn': 'XRN2'}
SRC = open(os.path.join(HERE, 'd2s_bias_ref.spice')).read()
IDEAL = """.subckt d2s_bias_ideal vdd vss vddo vsso vbp vbn vbpc vbnc vabp vabn
IBP vbp vss 5u
IBN vdd vbn 5u
IBNC vdd vbnc 2u
IBPC vbpc vss 2u
IABP vabp vss 5u
IABN vdd vabn 5u
Xd vdd vss vddo vsso vbp vbn vbpc vbnc vabp vabn d2s_bias_diodes
.ends d2s_bias_ideal
"""
INST = {'ideal': "Xb vdd vss vddo vsso vbp vbn vbpc vbnc vabp vabn d2s_bias_ideal",
        'in': "Iref 0 iref 5u\nXb vdd vss vddo vsso iref vbp vbn vbpc vbnc vabp vabn d2s_bias_in",
        'out': "Iref iref 0 5u\nXb vdd vss vddo vsso iref vbp vbn vbpc vbnc vabp vabn d2s_bias_out",
        'oa': "Xb vdd vss vddo vsso vbp vbn vbpc vbnc vabp vabn d2s_bias_oa",
        'bg': "Xb vdd vss vddo vsso vbp vbn vbpc vbnc vabp vabn d2s_bias_bg"}
VARIANTS = ['in', 'out', 'oa', 'bg']
CORN = [('tt 27C', {}), ('ss 27C', dict(mos='mos_ss')), ('ff 27C', dict(mos='mos_ff')),
        ('sf 27C', dict(mos='mos_sf')), ('fs 27C', dict(mos='mos_fs')),
        ('res wcs', dict(res='res_wcs')), ('res bcs', dict(res='res_bcs')),
        ('pnp wcs', dict(pnp='wcs')), ('pnp bcs', dict(pnp='bcs')),
        ('tt -40C', dict(temp=-40)), ('tt 125C', dict(temp=125)),
        ('ss 3.0V -40C', dict(mos='mos_ss', vdd=3.0, temp=-40)), ('ff 3.6V 125C', dict(mos='mos_ff', vdd=3.6, temp=125))]


def sensed(src):
    """d2s_bias_diodes with a 0 V source in each diode's drain: i(Vs<name>) is that bias current"""
    m = re.search(r'\.subckt d2s_bias_diodes.*?\.ends d2s_bias_diodes', src, re.S)
    body = m.group(0)
    for k, dev in DRAIN.items():
        body = re.sub(rf'^{dev} (\S+)', lambda mm: f'Vs{k} {mm.group(1)} s{k} 0\n{dev} s{k}', body, flags=re.M)
    return src.replace(m.group(0), body)


def split_driver():
    s = open(os.path.join(HERE, 'd2s_mpdda.spice')).read()
    s = s.replace('.subckt d2s_mpdda vdd vss ', '.subckt d2s_mpdda_split vdd vss vddo vsso ').replace('.ends d2s_mpdda', '.ends d2s_mpdda_split')
    s = re.sub(r'^XOP vout a vdd vdd', 'XOP vout a vddo vddo', s, flags=re.M)
    s = re.sub(r'^XON vout b vss vss', 'XON vout b vsso vsso', s, flags=re.M)
    assert 'XOP vout a vddo vddo' in s and 'XON vout b vsso vsso' in s
    return s


def vsense(k, var):
    return f"i(v.xb.xt.xd.vs{k})" if var in ('oa', 'bg') else f"i(v.xb.xd.vs{k})"


def header(mos='mos_tt', res='res_typ', temp=27, pnp='typ', seed=None):
    mm, rr = (mos + '_mismatch', res + '_mismatch') if seed is not None else (mos, res)
    return ((f".option seed={seed}\n" if seed is not None else '') +
            f".lib {r.MODELDIR}/cornerMOShv.lib {mm}\n.lib {r.MODELDIR}/cornerRES.lib {rr}\n"
            f".lib {r.MODELDIR}/cornerCAP.lib cap_typ\n.lib {r.MODELDIR}/cornerPNP.lib {pnp}\n.temp {temp}\n")


def rails(vdd=3.3, ac=None, ramp=None):
    out = []
    for n, v in [('vdd', vdd), ('vss', 0), ('vddo', vdd), ('vsso', 0)]:
        if ramp and n in ('vdd', 'vddo'):
            out.append(f"V{n} {n} 0 pwl(0 0 {ramp} {v})")
        else:
            out.append(f"V{n} {n} 0 dc {v}" + (" ac 1" if ac == n else ''))
    return '\n'.join(out) + '\n'


def bias_net(var, vdd=3.3, ac=None, ramp=None, seed=None, src=None, **kw):
    src = src or SRC
    if seed is not None:
        src = re.sub(r'^(X\S+ .*(?:sg13_hv_[np]mos|rhigh) .*)$', r'\1 mm_ok=1', src, flags=re.M)
    return header(seed=seed, **kw) + sensed(src + IDEAL) + rails(vdd, ac, ramp) + INST[var] + '\n'


def ngspice(net, ctl):
    with open(os.path.join(r.WORK, 'b.cir'), 'w') as f:
        f.write('* x\n' + net + '.control\n' + ctl + '.endc\n.end\n')
    return subprocess.run(['ngspice', '-b', 'b.cir'], cwd=r.WORK, capture_output=True, text=True).stdout


def results(o):
    out = {}
    for l in o.splitlines():
        if l.startswith('R '):
            t = l.split()
            out[t[1]] = [float(x) for x in t[2:]] if len(t) > 3 else float(t[2])
    return out


def currents(var, **kw):
    o = results(ngspice(bias_net(var, **kw), "op\n" + ''.join(f"echo R {k} $&{vsense(k, var)}\n" for k in NOM)))
    if len(o) < 6:
        raise RuntimeError(f'{var} {kw}: no operating point')
    return {k: abs(v) for k, v in o.items()}


def accuracy():
    print("\n== Bias currents, % deviation from 5 / 5 / 2 / 2 / 5 / 5 uA (vdd = vddo = 3.3 V unless stated)")
    for var in VARIANTS:
        print(f"\n-- {var}\n  {'corner':15s} " + ''.join(f"{k:>8}" for k in NOM))
        for name, c in CORN:
            i = currents(var, **c)
            print(f"  {name:15s} " + ''.join(f"{100 * (i[k] / NOM[k] - 1):8.2f}" for k in NOM))


FREQ = [10, 1e3, 1e5, 1e6, 1e7]


def supply():
    print("\n== Bias currents vs supply: dc line sensitivity (vdd = vddo 3.0 ... 3.6 V) and AC rejection,"
          "\n   |dI / I| per volt of ripple on one rail, %/V (tt 27C)")
    for var in VARIANTS:
        lo, mid, hi = currents(var, vdd=3.0), currents(var), currents(var, vdd=3.6)
        print(f"\n-- {var}: dc line, %/V: " + '  '.join(f"{k} {100 * (hi[k] - lo[k]) / mid[k] / 0.6:+.2f}" for k in NOM))
        print(f"   AC on    current " + ''.join(f"{f:>8.0e}" for f in FREQ))
        for rail in ['vdd', 'vss', 'vddo', 'vsso']:
            ctl = "ac dec 10 1 1e8\n" + ''.join(f"let m{k} = mag({vsense(k, var)})\n" for k in NOM) + ''.join(
                f"meas ac p{k}{j} find m{k} at={f}\n" for k in NOM for j, f in enumerate(FREQ)) + ''.join(
                f"echo R {k} " + ' '.join(f"$&p{k}{j}" for j in range(len(FREQ))) + "\n" for k in NOM)
            p = results(ngspice(bias_net(var, ac=rail), ctl))
            for k in NOM:
                if rail in ('vddo', 'vsso') and k not in ('abp', 'abn'):
                    continue
                print(f"   {rail:6s}  {k:>5s}  " + ''.join(f"{100 * v / mid[k]:8.2f}" for v in p[k]))


def startup():
    print("\n== Start-up of the self-contained references: vdd = vddo ramp from 0 in t_r, all nodes at 0 (uic),"
          "\n   Gear integration; bn and abp current 1 ms after the ramp vs the dc operating point;"
          "\n   t90 = last crossing of 90 % of the final bn current")
    for var in ('oa', 'bg'):
        print(f"\n-- {var}")
        for name, c in [('tt 27C', {}), ('ss 3.0V -40C', dict(mos='mos_ss', temp=-40, vdd=3.0)),
                        ('ff 3.6V 125C', dict(mos='mos_ff', temp=125, vdd=3.6)), ('sf -40C', dict(mos='mos_sf', temp=-40)),
                        ('fs 125C', dict(mos='mos_fs', temp=125)), ('tt -40C', dict(temp=-40)), ('tt 125C', dict(temp=125))]:
            d = currents(var, **c)
            for tr in (1e-6, 100e-6):
                ts = tr + 1e-3
                ctl = (f"tran {ts / 2000} {ts} uic\nlet ib = abs({vsense('bn', var)})\nlet ia = abs({vsense('abp', var)})\n"
                       f"meas tran ibf find ib at={ts}\nmeas tran iaf find ia at={ts}\nlet ith = 0.9*ibf\n"
                       f"meas tran t90 when ib=ith cross=last\necho R res $&ibf $&iaf $&t90\n")
                o = results(ngspice(".option method=gear\n" + bias_net(var, ramp=tr, **c), ctl)).get('res')
                txt = 'NO START' if not o or len(o) < 3 else (
                    f"bn {100 * o[0] / 5e-6:6.2f} %  abp {100 * o[1] / 5e-6:6.2f} %  (dc op bn {100 * d['bn'] / 5e-6:6.2f} %)  t90 {o[2] * 1e6:6.1f} us")
                print(f"  {name:13s} t_r {tr * 1e6:4.0f} us: {txt}")


def mc(N=100):
    print(f"\n== Mismatch MC, {N} seeds (mos_tt_mismatch, res_typ_mismatch, mm_ok=1 on every MOS and rhigh;"
          "\n   pnpMPA has no mismatch model): sigma / mean of each current, % (mean deviation from nominal)")
    for var in VARIANTS:
        rs = [currents(var, seed=s) for s in range(1, N + 1)]
        print(f"  {var:4s} " + '  '.join(
            f"{k} {100 * np.std([x[k] for x in rs]) / np.mean([x[k] for x in rs]):4.2f} ({100 * (np.mean([x[k] for x in rs]) / NOM[k] - 1):+5.2f})" for k in NOM))


def driver_net(var, loop=False, ac=None, vdd=3.3, src=None, dvo=0.0, dso=0.0, **kw):
    inc = ''.join(open(os.path.join(HERE, f)).read() for f in ('units.spice', 'ccomp.spice')) + split_driver() + (src or SRC) + IDEAL
    rl = rails(vdd, ac).replace(f"Vvddo vddo 0 dc {vdd}", f"Vvddo vddo 0 dc {vdd + dvo}").replace("Vvsso vsso 0 dc 0", f"Vvsso vsso 0 dc {dso}")
    fb = 'fb' if loop else 'vout'
    return (header(**kw) + inc + rl + "Vcm vref 0 1.65\n" + INST[var] + "\nVp vinp vref 0\nVn vinn vref 0\n"
            f"Xd vdd vss vddo vsso vinp vinn vref vout {fb} vbp vbn vbpc vbnc vabp vabn d2s_mpdda_split\n" +
            ("Lb vout fb 1G\nCb fb inj 1\nVinj inj 0 dc 0 ac 1\n" if loop else '') + "RL vout vref 1k\nCL vout 0 100p\n")


def drv_dc(var, **kw):
    return results(ngspice(driver_net(var, **kw), "op\necho R iq $&@n.xd.xop.nsg13_hv_pmos[ids]\necho R idd $&i(vvdd)\n"
                                                  "echo R iddo $&i(vvddo)\nlet os = v(vout)-v(vref)\necho R os $&os\n"))


def drv_loop(var, **kw):
    return results(ngspice(driver_net(var, loop=True, **kw),
                           "ac dec 50 10 1G\nlet T=-v(vout)/v(fb)\nmeas ac T0 find vdb(T) at=10\nmeas ac fc when vdb(T)=0\n"
                           "meas ac pT find vp(T) when vdb(T)=0\nlet pm=180/pi*pT+180\necho R T0 $&T0\necho R fc $&fc\necho R pm $&pm\n"))


def driver():
    print("\n== d2s_mpdda with each bias, OP / ON on vddo / vsso, 1k || 100p to vref, tt 27C, all rails at 3.3 V / 0")
    print(f"  {'bias':6s} {'I_Q uA':>7s} {'I_vdd uA':>9s} {'I_vddo uA':>10s} {'offs mV':>8s} {'T0 dB':>6s} {'fc MHz':>7s} {'PM':>5s}")
    for var in ['ideal'] + VARIANTS:
        d, l = drv_dc(var), drv_loop(var)
        print(f"  {var:6s} {d['iq'] * 1e6:7.1f} {-d['idd'] * 1e6:9.1f} {-d['iddo'] * 1e6:10.1f} {d['os'] * 1e3:8.3f} "
              f"{l['T0']:6.1f} {l['fc'] / 1e6:7.3f} {l['pm']:5.1f}")
    print("\n== Supply-to-output gain |vout / v_rail|, dB, closed loop (signal gain 0.5 = -6 dB), tt 27C")
    print(f"  {'bias':6s} {'rail':5s} " + ''.join(f"{f:>8.0e}" for f in FREQ))
    for var in ['ideal'] + VARIANTS:
        for rail in ['vdd', 'vss', 'vddo', 'vsso']:
            ctl = "ac dec 20 1 1e8\nlet g = db(v(vout))\n" + ''.join(f"meas ac g{j} find g at={f}\n" for j, f in enumerate(FREQ)) + \
                  "echo R g " + ' '.join(f"$&g{j}" for j in range(len(FREQ))) + "\n"
            g = results(ngspice(driver_net(var, ac=rail), ctl))['g']
            print(f"  {var:6s} {rail:5s} " + ''.join(f"{x:8.1f}" for x in g))


def corners():
    print("\n== d2s_mpdda with each bias over PVT, 1k || 100p (I_DD = vdd + vddo)")
    for var in ['ideal'] + VARIANTS:
        print(f"\n-- {var}\n  {'corner':15s} {'I_Q uA':>7s} {'I_DD uA':>8s} {'offs mV':>8s} {'T0 dB':>6s} {'fc MHz':>7s} {'PM':>5s}")
        for name, c in CORN:
            if name.startswith('pnp') and var != 'bg':
                continue
            d, l = drv_dc(var, **c), drv_loop(var, **c)
            print(f"  {name:15s} {d['iq'] * 1e6:7.1f} {-(d['idd'] + d['iddo']) * 1e6:8.1f} {d['os'] * 1e3:8.3f} "
                  f"{l['T0']:6.1f} {l['fc'] / 1e6:7.3f} {l['pm']:5.1f}")


def rails_offset():
    print("\n== I_Q (uA) with the output-stage rails offset by 50 mV from the bias rails (bias 'in', tt 27C)")
    wrong = SRC.replace("XRP1 n1 n1 vddo vddo", "XRP1 n1 n1 vdd vdd").replace("XRN1 n2 n2 vsso vsso", "XRN1 n2 n2 vss vss")
    print(f"  {'replicas RP1 / RN1':24s} {'vddo-50m':>9s} {'nominal':>8s} {'vddo+50m':>9s} {'vsso-50m':>9s} {'vsso+50m':>9s}")
    for label, src in [('on vddo / vsso', SRC), ('on vdd / vss', wrong)]:
        q = [drv_dc('in', src=src, dvo=a, dso=b)['iq'] * 1e6 for a, b in [(-0.05, 0), (0, 0), (0.05, 0), (0, -0.05), (0, 0.05)]]
        print(f"  {label:24s} " + ''.join(f"{x:9.1f}" for x in q))


def area():
    print("\n== Drawn device area per block: MOS W*L, rhigh w*l, pnpMPA emitter area, um2")
    SI = {'u': 1e-6, 'p': 1e-12, 'n': 1e-9}
    num = lambda v: float(re.fullmatch(r'([\d.]+)([upn]?)', v).group(1)) * SI.get(re.fullmatch(r'([\d.]+)([upn]?)', v).group(2), 1)
    for name in ['d2s_bias_diodes', 'd2s_bias_in', 'd2s_bias_out', 'oa_core', 'bg_core']:
        body = re.search(rf'\.subckt {name} .*?\.ends {name}', SRC, re.S).group(0)
        mos = res = bjt = 0.0
        n = 0
        for l in body.splitlines():
            t = l.split()
            if not t or not t[0].startswith('X'):
                continue
            kv = dict(x.split('=') for x in t if '=' in x)
            if any(x.startswith('sg13_hv') for x in t):
                mos += num(kv['w']) * num(kv['l']) * 1e12; n += 1
            elif 'rhigh' in t:
                res += num(kv['w']) * num(kv['l']) * 1e12; n += 1
            elif 'pnpMPA' in t:
                bjt += num(kv['a']) * 1e12 * float(kv.get('m', 1)); n += 1
        print(f"  {name:16s} {n:3d} devices   MOS {mos:7.1f}   rhigh {res:6.1f}   PNP {bjt:5.1f}")


S = {'accuracy': accuracy, 'supply': supply, 'startup': startup, 'mc': mc, 'driver': driver, 'corners': corners,
     'rails': rails_offset, 'area': area}
if __name__ == '__main__':
    print(f"# models: {r.MODELDIR}\n# osdi: {r.OSDI_DIR or '(from .spiceinit)'}")
    for s in sys.argv[1:] or S:
        S[s]()
        sys.stdout.flush()
