#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Netlist the schematics in this directory with xschem (-> net/*.spice) and compare every
subcircuit in those netlists, device by device, against its source in ../sim/*.spice:
model, terminal nets in order, w / l / ng / value, and port order (.sch and .sym). Source parameters are
evaluated at their .subckt defaults ({10e-6*lcas} -> 30u). Subcircuit instances must not
override their child's defaults. The testbench schematics tb_*.sch are compared with the decks in
../sim/tb/: every top-level element (name, nets with GND = 0, value or model and w / l / ng) and the
code lines (.lib, .param, .save and the .control block, comments ignored).
Prints every mismatch; exit status 1 on any.
    cd improvements/xschem && python3 check_xschem.py      (needs xschem, $PDK_ROOT)
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, '..', 'sim')
CELLS = ['unit_r', 'unit_r2', 'unit_t', 'unit_w', 'unit_q', 'd2s_bias_lp', 'd2s_mpdda', 'd2s_lc2',
         'd2s_lc2_nc', 'd2s_mpdda_biased', 'd2s_mpdda_flat', 'd2s_mpdda_bias_flat']
# the assemblies have no .spice source; this is what they must netlist to
FIXTURE = """.subckt d2s_mpdda_biased vdd vss vinp vinn vref vout vfb vbp vbn vbpc vbnc vabp vabn
xd vdd vss vinp vinn vref vout vfb vbp vbn vbpc vbnc vabp vabn d2s_mpdda
xb vdd vss vbp vbn vbpc vbnc vabp vabn d2s_bias_lp
.ends
.subckt d2s_mpdda_bias_flat vdd vss vinp vinn vref vout vfb
xd vdd vss vinp vinn vref vout vfb vbp vbn vbpc vbnc vabp vabn d2s_mpdda
xb vdd vss vbp vbn vbpc vbnc vabp vabn d2s_bias_lp
.ends"""
# flat schematics: compared against their source with every subcircuit expanded. Devices and
# internal nets of a DDA unit get the unit's name as suffix (Ta_A, sa_A); the two assemblies
# above are transparent (their parts keep their own names).
FLAT = {'d2s_mpdda_flat': 'd2s_mpdda', 'd2s_mpdda_bias_flat': 'd2s_mpdda_bias_flat'}
TRANSPARENT = ('d2s_mpdda_biased', 'd2s_mpdda_bias_flat')
TBS = ['tb_mpdda_dc', 'tb_mpdda_step', 'tb_mpdda_thd', 'tb_mpdda_noise', 'tb_mpdda_op', 'tb_mpdda_loop',
       'tb_lc2_loop', 'tb_units', 'tb_moscv']
SI = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e3, 'meg': 1e6, '': 1}


def num(v):
    m = re.fullmatch(r'([-+]?[\d.]+(?:e[-+]?\d+)?)(meg|[fpnumk]?)', str(v).lower())
    return round(float(m.group(1)) * SI[m.group(2)], 18) if m else v


def blocks(text):
    """{name: (ports, defaults, lines)} for '.subckt' and xschem's top-level '**.subckt'."""
    out, cur = {}, None
    for line in text.splitlines():
        t = line.split()
        if t and t[0].lower() in ('.subckt', '**.subckt'):
            cur = t[1]
            out[cur] = ([p for p in t[2:] if '=' not in p], dict(p.split('=') for p in t[2:] if '=' in p), [])
        elif t and t[0].lower() in ('.ends', '**.ends'):
            cur = None
        elif cur and t and t[0][0] in 'XxIi':
            out[cur][2].append(line)
    return out


def devices(lines, defaults):
    env = {k: num(v) for k, v in defaults.items()}
    devs = {}
    for line in lines:
        line = re.sub(r'\{([^}]*)\}', lambda m: repr(eval(m.group(1), {}, env)), line)
        t = line.split()
        kv = {k: num(v) for k, v in (x.split('=', 1) for x in t if '=' in x)}
        pos = [x for x in t[1:] if '=' not in x]
        if t[0][0] in 'Xx':
            devs[t[0][1:]] = (pos[-1], tuple(pos[:-1]), kv)
        else:
            devs[t[0]] = ('isource', tuple(pos[:2]), {'value': num(pos[2])})
    return devs


src = {}
for f in sorted(os.listdir(SIM)):
    if f.endswith('.spice'):
        src.update(blocks(open(os.path.join(SIM, f)).read()))
src.update(blocks(FIXTURE))


def flat(name, sfx=''):
    """devices of subcircuit `name` with all subcircuits expanded; internal nets and device
    names get suffix sfx, port nets keep the port name (the caller maps them)"""
    ports, defs, lines = src[name]
    out = {}
    for n, (m, nets, p) in devices(lines, defs).items():
        nets = tuple(x if x in ports else x + sfx for x in nets)
        if m in src:
            mp = dict(zip(src[m][0], nets))
            for dn, (dm, dnets, dp) in flat(m, sfx if name in TRANSPARENT else '_' + n + sfx).items():
                out[dn] = (dm, tuple(mp.get(x, x) for x in dnets), dp)
        else:
            out[n + sfx] = (m, nets, p)
    return out


def top_level(text):
    """elements and code lines outside every .subckt, of a deck or of xschem's netlist"""
    lines = []
    for raw in text.splitlines():
        if raw.startswith('+') and lines:
            lines[-1] += ' ' + raw[1:]
        else:
            lines.append(raw)
    gnd = lambda x: '0' if x.upper() == 'GND' else x
    elems, code, ctl, sub = {}, [], False, False
    for l in lines:
        s = ' '.join(l.split())
        low = s.lower()
        if low.startswith('.subckt'):
            sub = True
            continue
        if low.startswith('.ends'):
            sub = False
            continue
        if sub or not s or s.startswith('*'):
            continue
        if low.startswith('.control'):
            ctl = True
        if ctl or s.startswith('.'):
            if not (low == '.end' or low.startswith(('.include', '.global', '.title'))):
                code.append(s)
            if low.startswith('.endc'):
                ctl = False
            continue
        t = s.split()
        k = t[0][0].upper()
        if k == 'X':
            pos = [x for x in t[1:] if '=' not in x]
            kv = {a: num(b) for a, b in (x.split('=', 1) for x in t if '=' in x)}
            elems[t[0].upper()] = (tuple(gnd(x) for x in pos[:-1]), pos[-1].lower(), kv)
        elif k in 'VIRCLE':
            n = 4 if k == 'E' else 2
            val = re.sub(r'\s*\bm=1$', '', ' '.join(t[1 + n:])).lower().replace(' ', '')
            elems[t[0].upper()] = (tuple(gnd(x) for x in t[1:1 + n]), val, {})
    return elems, code


os.makedirs(os.path.join(HERE, 'net'), exist_ok=True)
bad, seen = 0, {}
for c in CELLS + TBS:
    net = os.path.join(HERE, 'net', f'{c}.spice')
    if os.path.exists(net):
        os.remove(net)  # never compare against a stale netlist
    r = subprocess.run(['xschem', '--rcfile', os.path.join(HERE, 'xschemrc'), '-n', '-s', '-q', '-x',
                        '-o', os.path.join(HERE, 'net'), os.path.join(HERE, f'{c}.sch')],
                       cwd=HERE, env=dict(os.environ, PWD=HERE), capture_output=True, text=True)
    if r.returncode or not os.path.exists(net):
        # a nonzero status is not an error by itself; report it, then compare what was written
        print(f'{c}: xschem exit status {r.returncode}' + ('' if os.path.exists(net) else ', NO NETLIST'))
        for l in [l for l in (r.stdout + r.stderr).splitlines() if not l.startswith('MODELS_')][-15:]:
            print('   ', l)
        if not os.path.exists(net):
            bad += 1
            continue
    for name, (ports, _, lines) in blocks(open(net).read()).items():
        if name in TBS:
            continue    # a testbench's own top level: compared with its deck below
        if FLAT.get(name, name) not in src:
            print(f'{c}: subcircuit {name} has no source'); bad += 1; continue
        sports, sdef, slines = src[FLAT.get(name, name)]
        if ports != sports:
            print(f'{c}/{name}: port order {ports} != {sports}'); bad += 1
        s = flat(FLAT[name]) if name in FLAT else devices(slines, sdef)
        x = devices(lines, {})
        for n in sorted(set(s) | set(x)):
            if n not in s or n not in x:
                print(f'{c}/{name}: {n} only in {"source" if n in s else "xschem"}'); bad += 1; continue
            (ms, ns, ps), (mx, nx, px) = s[n], x[n]
            if ms != mx or ns != nx:
                print(f'{c}/{name}: {n} {ms}{ns} != {mx}{nx}'); bad += 1
            if ms in src:   # subcircuit instance: source parameters must equal the child's defaults
                for k, v in ps.items():
                    if num(src[ms][1].get(k)) != v:
                        print(f'{c}/{name}: {n} {k}={v} differs from {ms} default {src[ms][1].get(k)}'); bad += 1
                continue
            for k in ('w', 'l', 'ng', 'value'):
                if k in ps and ps[k] != px.get(k, 1 if k == 'ng' else None):
                    print(f'{c}/{name}: {n} {k} {ps[k]} != {px.get(k)}'); bad += 1
        seen[name] = seen.get(name, 0) + 1
        print(f'{c}/{name}: {len(s)} devices, {len(ports)} ports compared')
    if c in TBS:   # testbench: top level against the deck
        (ds, dc), (xs, xc) = top_level(open(os.path.join(SIM, 'tb', c + '.spice')).read()), top_level(open(net).read())
        for k in sorted(set(ds) | set(xs)):
            if k not in ds or k not in xs:
                print(f'{c}: {k} only in {"deck" if k in ds else "xschem"}'); bad += 1; continue
            (nd, vd, pd), (nx, vx, px) = ds[k], xs[k]
            if nd != nx or vd != vx:
                print(f'{c}: {k} deck {nd} {vd} != xschem {nx} {vx}'); bad += 1
            for p, v in pd.items():
                if p in ('w', 'l', 'ng') and px.get(p, 1 if p == 'ng' else None) != v:
                    print(f'{c}: {k} {p} deck {v} != xschem {px.get(p)}'); bad += 1
        if dc != xc:
            print(f'{c}: code lines differ'); bad += 1
            for a, b in zip(dc + [''] * len(xc), xc + [''] * len(dc)):
                if a != b:
                    print(f'    deck: {a}\n    sch:  {b}'); break
        seen[c] = 1
        print(f'{c}: {len(ds)} top-level elements and {len(dc)} code lines compared')
for c in CELLS:  # parents take the port order from the .sym: it must equal the source's
    sym = os.path.join(HERE, f'{c}.sym')
    if os.path.exists(sym):
        pins = re.findall(r'^B 5 [^{]*\{name=(\S+)', open(sym).read(), re.M)
        if pins != src[FLAT.get(c, c)][0]:
            print(f'{c}.sym: pin order {pins} != {src[FLAT.get(c, c)][0]}'); bad += 1
missing = [n for n in CELLS + TBS if n not in seen]
if missing:
    print('never compared:', missing); bad += len(missing)
print('MISMATCHES:', bad)
sys.exit(1 if bad else 0)
