#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Every number in proposed_improvements.md (class-AB pad driver, revision proposal).
Uses the measurement functions of ../../run_d2s.py unchanged (dc, loop, step, thd, LOADS, CORNERS).

Usage (IIC-OSIC-TOOLS, after `source .designinit`, from this directory):
    python3 run_improvements.py > results_improvements.txt        # all sections, ~5 min
    python3 run_improvements.py units mc                           # selected sections
Sections: units moscv table cload lcas corners noise op mc budget slot area
Model / OSDI paths as run_d2s.py ($MODELDIR, $OSDI_DIR).
"""
import os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import run_d2s as r

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(os.path.dirname(HERE))   # class_ab_pad_driver/
r.CORNERS.update({'ss 27C': ('mos_ss', 'res_typ', 27), 'ff 27C': ('mos_ff', 'res_typ', 27),
                  'tt 27C wcs': ('mos_tt', 'res_wcs', 27), 'tt 27C bcs': ('mos_tt', 'res_bcs', 27),
                  'tt 125C': ('mos_tt', 'res_typ', 125), 'tt -40C': ('mos_tt', 'res_typ', -40)})
FILES = ['units', 'ccomp', 'd2s_mp', 'd2s_mpdda', 'd2s_bias_lp', 'd2s_lc2']
# name: (subckt, bias, extra subckt params, compensation for d2s_mp's ccomp wrapper)
V = {'baseline A': ('d2s_miller', 'd2s_bias', '', 'mom', ''),
     'MP-DDA (A sizing)': ('d2s_mp', 'd2s_bias', '', 'mom', ''),
     'MP-DDA (A sizing), MOS 18': ('d2s_mp', 'd2s_bias', '', 'mos', 'wc=18u lc=18u'),
     'd2s_mpdda': ('d2s_mpdda', 'd2s_bias_lp', '', 'mom', '')}


def header(v, corner='tt 27C', mc_seed=None, mm_dir=None, dpar=''):
    sub, bias, _, comp, cpar = V[v] if isinstance(v, str) else v
    mos, res, temp = r.CORNERS[corner]
    if mc_seed is not None:
        mos, res = 'mos_tt_mismatch', 'res_typ_mismatch'
    src = mm_dir or HERE
    inc = ''.join(f".include {src}/{f}.spice\n" for f in FILES)
    inc += f".include {mm_dir or UP}/d2s_bias.spice\n.include {mm_dir or UP}/d2s_miller.spice\n"
    h = ((f".option seed={mc_seed}\n" if mc_seed is not None else '') +
         f".lib {r.MODELDIR}/cornerMOShv.lib {mos}\n.lib {r.MODELDIR}/cornerRES.lib {res}\n"
         f".lib {r.MODELDIR}/cornerCAP.lib cap_typ\n.temp {temp}\n" + inc +
         f".subckt ccomp vout a b vss\nXc vout a b vss ccomp_{comp} {cpar}\n.ends ccomp\n"
         f"Vdd vdd 0 3.3\nVcm vref 0 1.65\nXb vdd 0 vbp vbn vbpc vbnc vabp vabn {bias}\n")
    return h, (lambda fb='vout': f"Xd vdd 0 vinp vinn vref vout {fb} vbp vbn vbpc vbnc vabp vabn {sub} {dpar}\n")


def ngspice(net, ctl, out='out.txt'):
    with open(os.path.join(r.WORK, 'u.cir'), 'w') as f:
        f.write('* x\n' + net + '.control\n' + ctl + '.endc\n.end\n')
    o = subprocess.run(['ngspice', '-b', 'u.cir'], cwd=r.WORK, capture_output=True, text=True)
    return o.stdout if out is None else np.loadtxt(os.path.join(r.WORK, out), ndmin=2)


def units():
    print("\n== DDA units: one input at vref, other swept (fA: gp = vref+x; fB: gn = vref-x);"
          "\n   MP-DDA static error from the unit curves: solve fA(u)+fB(u) = 2 fA(v)")
    for u in ['unit_r', 'unit_t', 'unit_w', 'unit_q']:
        net = (f".lib {r.MODELDIR}/cornerMOShv.lib mos_tt\n.lib {r.MODELDIR}/cornerRES.lib res_typ\n"
               f".param wwi=4u lwi=4u\n.include {HERE}/units.spice\nVdd vdd 0 3.3\nIBP vbp 0 20u\n"
               "XBP vbp vbp vdd vdd sg13_hv_pmos w=20u l=2u ng=2\nVref vref 0 1.65\nVx xd 0 0\n"
               "EpA gpa vref xd 0 1\nEnB gnb vref xd 0 -1\nEp gps vref xd 0 0.5\nEn gns vref xd 0 -0.5\n"
               + ''.join(f"Vf{k} {k} 0 0.45\n" for k in ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'])
               + f"XUA x1 y1 gpa vref vdd 0 vbp {u}\nXUB x2 y2 vref gnb vdd 0 vbp {u}\n"
               f"Vcl cl 0 1.40\nVch ch 0 1.90\nElp gl cl xd 0 0.5\nEln gnl cl xd 0 -0.5\nEhp gh ch xd 0 0.5\nEhn gnh ch xd 0 -0.5\n"
               f"XUL x3 y3 gl gnl vdd 0 vbp {u}\nXUH x4 y4 gh gnh vdd 0 vbp {u}\n")
        a = ngspice(net, "dc Vx -0.8 0.8 0.005\nwrdata out.txt i(Vfx1)-i(Vfy1) i(Vfx2)-i(Vfy2) i(Vfx3)-i(Vfy3) i(Vfx4)-i(Vfy4)\n")
        x, fA, fB, fL, fH = a[:, 0], a[:, 1], a[:, 3], a[:, 5], a[:, 7]
        g = lambda f: np.polyfit(x[abs(x) <= 0.02], f[abs(x) <= 0.02], 1)[0]
        g0 = g(fA)
        comp = max(abs(np.interp(s, x, fA) / (g0 * s) - 1) for s in (-0.5, 0.5)) * 100
        m = (x >= -0.7) & (x <= 0.7)
        err = [(np.interp((np.interp(uu, x, fA) + np.interp(uu, x, fB)) / 2, fA[m], x[m]) - uu) * 1e3 for uu in (-0.5, -0.25, 0.25, 0.5)]
        cms = (g(fH) - g(fL)) / g0 / 0.5 * 100
        print(f"{u:7s} Gm0 {g0*1e6:5.2f} uS  Gm CM sensitivity {cms:6.1f} %/V  compression at |x|=0.5 {comp:4.1f} %  "
              f"MP-DDA error at u = -0.5/-0.25/+0.25/+0.5: " + ' / '.join(f'{e:7.2f}' for e in err) + ' mV', flush=True)


def moscv():
    print("\n== C-V of hv PMOS 14 x 14 um as accumulation capacitor (gate vs S/D/well), and MOM 31 x 31 um, 1 MHz")
    net = (f".lib {r.MODELDIR}/cornerMOShv.lib mos_tt\n.lib {r.MODELDIR}/cornerCAP.lib cap_typ\n"
           "Vg g 0 dc 0 ac 1\nVw w 0 1.65\nX1 w g w w sg13_hv_pmos w=14u l=14u ng=1\n"
           "Vg2 g2 0 dc 0 ac 1\nXM g2 0 cap_cmomi w=31e-6 l=31e-6\n")
    ctl = ''.join(f"alter Vg dc = {1.65 + v}\nac lin 1 1meg 1meg\nprint -imag(i(Vg))/(2*pi*1e6)\n" for v in (-1, -0.5, 0, 0.15, 0.5, 1, 1.25, 1.5, 2)) + "print -imag(i(Vg2))/(2*pi*1e6)\n"
    o = ngspice(net, ctl, None)
    c = [float(v) for v in re.findall(r'imag.* = (\S+)', o)]
    print('V_GW [V]: ' + '  '.join(f'{v:+5.2f}' for v in (-1, -0.5, 0, 0.15, 0.5, 1, 1.25, 1.5, 2)))
    print('C [pF]:   ' + '  '.join(f'{v*1e12:5.3f}' for v in c[:-1]) + f'   (MOM 31x31: {c[-1]*1e12:.3f} pF)')


def row(name, h, dut, L):
    d, lg, st = r.dc(h, dut, L), r.loop(h, dut, L), r.step(h, dut, L)
    print(f"{name:26s} {L:13s} gain={d['gain']:.4f} off={d['off']:6.2f}mV nonlin={d['nonlin']:5.2f}mV "
          f"IqP/N={d['iqp']:4.0f}/{d['iqn']:4.0f}uA Idd={d['idd']:5.0f}uA Imin={d['imin']:4.0f}uA | {r.fmt_loop(lg)} | "
          f"OS={st['os']:4.1f}% t1%={st['ts']:5.0f}ns | THD 10k/100k={r.thd(h, dut, L, 10e3):5.1f}/{r.thd(h, dut, L, 100e3):5.1f}dB", flush=True)


def table():
    print("\n== Performance, tt 27C (Idd includes the bias fixture)")
    for v in ['baseline A', 'MP-DDA (A sizing)', 'MP-DDA (A sizing), MOS 18', 'd2s_mpdda']:
        h, d = header(v)
        for L in ['50R', '1k||100p', '1k(gnd)||100p', '20p', '100p', '1n']:
            row(v, h, d, L)


def cload_row(h, d, cs=('5p', '10p', '20p', '50p', '100p', '300p', '1n')):
    out = []
    for c in cs:
        r.LOADS['c'] = f'CL vout 0 {c}\n'
        lg = r.loop(h, d, 'c')
        out.append(f"{c}: {lg['fc']:.2f} MHz/{lg['pm']:.1f}" if lg['fc'] else f"{c}: --")
    return ' | '.join(out)


def cload():
    print("\n== fc / PM vs load capacitance (no resistive load), tt 27C")
    for v in ['baseline A', 'MP-DDA (A sizing)', 'MP-DDA (A sizing), MOS 18', 'd2s_mpdda']:
        h, d = header(v)
        print(f"{v:26s} {cload_row(h, d)}", flush=True)
    for s in (14, 16, 18):
        h, d = header('d2s_mpdda', dpar=f'wc={s}u lc={s}u')
        print(f"{'d2s_mpdda, MOS %dx%d' % (s, s):26s} {cload_row(h, d)}", flush=True)


def lcas():
    print("\n== d2s_mpdda: loop gain vs cascode length (folded and mirror cascodes, W = 10 L)")
    for lc in (1, 2, 3):
        h, d = header('d2s_mpdda', dpar=f'lcas={lc}')
        print(f"L = {lc} um: " + ' | '.join(f"{L}: {r.fmt_loop(r.loop(h, d, L))}" for L in ['1k||100p', '100p', '50R']), flush=True)


def corners():
    print("\n== Corners: gain / offset / nonlin at 1k||100p, loop at 1k||100p and 100p (bias references ideal)")
    for c in ['tt 27C', 'ss 125C', 'ff -40C', 'sf 27C', 'fs 27C', 'ss 27C', 'ff 27C', 'tt 27C wcs', 'tt 27C bcs', 'tt 125C', 'tt -40C']:
        for v in ['baseline A', 'MP-DDA (A sizing)', 'd2s_mpdda']:
            h, d = header(v, corner=c)
            x = r.dc(h, d, '1k||100p')
            print(f"{c:11s} {v:18s} gain={x['gain']:.4f} off={x['off']:6.2f}mV nonlin={x['nonlin']:5.2f}mV Iq={x['iqp']:4.0f}uA "
                  f"Idd={x['idd']:4.0f}uA | 1k||100p {r.fmt_loop(r.loop(h, d, '1k||100p'))} | 100p {r.fmt_loop(r.loop(h, d, '100p'))}", flush=True)


def noise():
    print("\n== Output noise, 1k||100p, tt 27C")
    for v in ['baseline A', 'MP-DDA (A sizing)', 'd2s_mpdda']:
        h, d = header(v)
        a = r.sim(h + d() + 'RL vout vref 1k\nCL vout 0 100p\nVd dp 0 dc 0 ac 1\n' + r.DIFF,
                  'noise v(vout) Vd dec 20 10 10meg\nsetplot noise1\nwrdata out.txt onoise_spectrum\n')
        f, n = a[:, 0], a[:, 1]
        print(f"{v:18s} 1 kHz {np.interp(1e3, f, n)*1e9:7.1f} nV/rtHz  100 kHz {np.interp(1e5, f, n)*1e9:6.1f} nV/rtHz  "
              f"10 Hz-10 MHz {np.sqrt(np.trapezoid(n**2, f))*1e6:6.1f} uV rms", flush=True)


def op():
    print("\n== d2s_mpdda operating point at vd = 0 (1k||100p): devices and saturation margin")
    h, d = header('d2s_mpdda')
    body = open(f'{HERE}/d2s_mpdda.spice').read()
    devs = [l.split()[0] for l in body.splitlines() if l.startswith('X') and 'sg13_hv' in l and not l.startswith('XCM')]
    q = lambda x: f"@n.xd.{x.lower()}.nsg13_hv_{'nmos' if x in ('XSX', 'XSY', 'XCX', 'XCY', 'XFNL', 'XABN', 'XON') else 'pmos'}"
    ctl = 'op\n' + ''.join(f"print {q(x)}[ids] {q(x)}[vds] {q(x)}[vdss]\n" for x in devs) + 'print v(xd.x) v(xd.a) v(xd.b)\n'
    o = ngspice(h + d() + "RL vout vref 1k\nCL vout 0 100p\nVp vinp 0 1.65\nVn vinn 0 1.65\n", ctl, None)
    val = dict(re.findall(r'^(\S+) = (\S+)', o, re.M))
    for x in devs:
        ids, vds, vdss = (float(val[f'{q(x)}[{k}]']) for k in ('ids', 'vds', 'vdss'))
        print(f"  {x:5s} ids={abs(ids)*1e6:7.2f} uA  |vds|={abs(vds):5.3f}  vdss={abs(vdss):5.3f}  margin={abs(vds)-abs(vdss):6.3f} V")
    print(f"  v(x) = {float(val['v(xd.x)']):.3f}  v(a) = {float(val['v(xd.a)']):.3f}  v(b) = {float(val['v(xd.b)']):.3f} V")


def mm_files(dirname, names=None):
    """Copies of the netlists with mm_ok=1 on all MOS and rhigh instances (names: only those)."""
    os.makedirs(os.path.join(r.WORK, dirname), exist_ok=True)
    for f, p in [(f, HERE) for f in FILES] + [('d2s_bias', UP), ('d2s_miller', UP)]:
        out = []
        for l in open(f'{p}/{f}.spice').read().splitlines():
            t = l.split()
            hit = t and t[0].startswith('X') and ('sg13_hv' in l or 'rhigh' in l) and (names is None or t[0] in names)
            out.append(l + ' mm_ok=1' if hit else l)
        open(os.path.join(r.WORK, dirname, f + '.spice'), 'w').write('\n'.join(out) + '\n')
    return os.path.join(r.WORK, dirname)


def mc(N=30):
    print(f"\n== Mismatch MC, {N} seeds (mos_tt_mismatch, res_typ_mismatch, mm_ok=1 on all MOS and rhigh), 1k||100p")
    dd = mm_files('mm_all')
    for v in ['baseline A', 'MP-DDA (A sizing)', 'd2s_mpdda']:
        res = [r.dc(*header(v, mc_seed=s, mm_dir=dd), '1k||100p') for s in range(1, N + 1)]
        off, gain, nl = (np.array([x[k] for x in res]) for k in ('off', 'gain', 'nonlin'))
        print(f"{v:18s} offset sd {off.std(ddof=1):5.2f} mV (range {off.min():6.2f}..{off.max():6.2f})  "
              f"gain sd {gain.std(ddof=1)/0.5*100:4.2f} % (range {gain.min():.4f}..{gain.max():.4f})  nonlin max {nl.max():.2f} mV", flush=True)


def budget(N=20):
    print(f"\n== Offset / gain mismatch budget by device group ({N} seeds, mismatch on one group at a time)")
    G = {'unit tails': ['XTa', 'XTb'], 'unit pairs': ['XMa', 'XMb'], 'unit rhigh': ['XR'], 'folding sinks': ['XSX', 'XSY'],
         'fold cascodes': ['XCX', 'XCY'], 'mirror': ['XPL', 'XPR', 'XPCL', 'XPCR'], 'class-AB': ['XFPL', 'XFNL', 'XABP', 'XABN']}
    for v in ['MP-DDA (A sizing)', 'd2s_mpdda']:
        for g, names in G.items():
            dd = mm_files('mm_g', names)
            res = [r.dc(*header(v, mc_seed=s, mm_dir=dd), '1k||100p') for s in range(1, N + 1)]
            off, gain = np.array([x['off'] for x in res]), np.array([x['gain'] for x in res])
            print(f"{v:18s} {g:14s} offset sd {off.std(ddof=1):5.2f} mV  gain sd {gain.std(ddof=1)/0.5*100:4.2f} %", flush=True)


def area():
    print("\n== Drawn device area without the output frames and without the bias fixture (W*L, rhigh w*l, cap w*l), um2")
    import re as _re
    S, D = {}, {}
    for p in [f'{UP}/d2s_miller.spice'] + [f'{HERE}/{f}.spice' for f in FILES]:
        cur = None
        for l in open(p):
            t = l.split()
            if not t:
                continue
            if t[0].lower() == '.subckt':
                cur = t[1]; S[cur] = []; D[cur] = dict(_re.findall(r'(\w+)=(\S+)', l))
            elif t[0].lower() == '.ends':
                cur = None
            elif cur and t[0][0] == 'X':
                S[cur].append(l.strip())

    def ev(v, p):
        v = v.strip('{}')
        for k in sorted(p, key=len, reverse=True):
            v = _re.sub(r'\b%s\b' % k, '(%s)' % p[k], v)
        return eval(_re.sub(r'(\d(?:\.\d+)?)u\b', r'\1e-6', v))

    def walk(sub, inst, acc):
        p = dict(D[sub]); p.update(inst)
        for l in S[sub]:
            t = l.split()
            if t[0] in ('XOP', 'XON'):
                continue
            kv = dict(_re.findall(r'(\w+)=(\{[^}]*\}|\S+)', l))
            if 'sg13_hv' in l or 'rhigh' in l or 'cap_cmomi' in l:
                k = 'res' if 'rhigh' in l else 'cap' if ('cap_cmomi' in l or t[0].startswith('XCM')) else 'gate'
                acc[k] += ev(kv['w'], p) * ev(kv['l'], p) * 1e12
            else:
                subs = [x for x in t[1:] if x in S]
                if subs:
                    walk(subs[0], {k: str(ev(v, p)) for k, v in kv.items()}, acc)
        return acc
    for name, sub, inst, comp in [('baseline A', 'd2s_miller', {}, None), ('MP-DDA (A sizing), MOM', 'd2s_mp', {}, ('ccomp_mom', {})),
                                  ('MP-DDA (A sizing), MOS 18', 'd2s_mp', {}, ('ccomp_mos', {'wc': '18e-6', 'lc': '18e-6'})),
                                  ('d2s_mpdda, lcas 1', 'd2s_mpdda', {'lcas': '1'}, None), ('d2s_mpdda, lcas 2', 'd2s_mpdda', {'lcas': '2'}, None),
                                  ('d2s_mpdda, lcas 3', 'd2s_mpdda', {'lcas': '3'}, None)]:
        a = walk(sub, inst, {'gate': 0.0, 'cap': 0.0, 'res': 0.0})
        if comp:
            walk(comp[0], comp[1], a)
        print(f"{name:26s} gate {a['gate']:6.0f}  compensation {a['cap']:6.0f}  rhigh {a['res']:4.0f}  total {sum(a.values()):6.0f}")


def slot():
    print("\n== Case (b): output devices in the slot (not clamps), load-compensated, no compensation capacitor")
    for sub in ['d2s_lc2_nc', 'd2s_lc2']:
        h, d = header((sub, 'd2s_bias_lp', '', 'mom', ''))
        x = r.dc(h, d, '100p')
        print(f"{sub:11s} gain={x['gain']:.4f} off={x['off']:6.2f}mV Idd={x['idd']:4.0f}uA | T0 (100p) {r.loop(h, d, '100p')['t0']:.1f} dB | "
              f"{cload_row(h, d, ('5p', '20p', '100p', '1n'))} | 1k||100p: {r.fmt_loop(r.loop(h, d, '1k||100p'))}", flush=True)
    h, d = header(('d2s_lc2', 'd2s_bias_lp', '', 'mom', ''))
    print("d2s_lc2 into IOPadAnalog padres -> 586.9 ohm -> pad (+2 pF) -> C_L, loop sensed at padres (near) or pad (far):")
    for c in ['20p', '100p', '1n']:
        load = f'Rs vout pad 586.9\nCL pad 0 {c}\nCpad pad 0 2p\n'
        r.LOADS['c'] = load
        near = r.fmt_loop(r.loop(h, d, 'c'))
        a = r.sim(h + d('fb') + load + 'Vp vinp 0 1.65\nVn vinn 0 1.65\nLb pad fb 1G\nCb fb inj 1\nVinj inj 0 dc 0 ac 1\n',
                  'ac dec 50 10 1G\nlet T=-v(pad)/v(fb)\nwrdata out.txt vdb(T) vp(T)\n')
        f, db, ph = a[:, 0], a[:, 1], np.degrees(np.unwrap(a[:, 3]))
        i = np.where(np.diff(np.sign(db)) < 0)[0][0]
        fc = np.interp(0, [db[i + 1], db[i]], [f[i + 1], f[i]])
        pm = (np.interp(fc, f, ph) + 180) % 360
        print(f"  C_L {c:5s} near: {near} | far: fc={fc/1e6:5.2f}MHz PM={pm if pm < 180 else pm - 360:5.1f}", flush=True)


if __name__ == '__main__':
    S = ['units', 'moscv', 'table', 'cload', 'lcas', 'corners', 'noise', 'op', 'mc', 'budget', 'slot', 'area']
    todo = sys.argv[1:] or S
    print(f"# models: {r.MODELDIR}\n# osdi: {r.OSDI_DIR or '(from .spiceinit)'}\n# sections: {' '.join(todo)}")
    for s in todo:
        globals()[s]()
