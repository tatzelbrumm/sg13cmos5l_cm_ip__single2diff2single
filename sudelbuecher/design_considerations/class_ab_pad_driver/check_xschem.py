#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Netlist the xschem schematics (xschem/*.sch -> xschem/net/*.spice) and compare them against
the source subcircuits, device by device: model, terminal nets in order, w / l / ng / value,
and port order. Prints mismatches and a count; exit status 1 on any mismatch.
    python3 check_xschem.py          (needs xschem on PATH and $PDK_ROOT set)
"""
import os, re, subprocess, sys
from gen_xschem import parse, HERE

XS = os.path.join(HERE, 'xschem')
os.makedirs(os.path.join(XS, 'net'), exist_ok=True)
for s in ('d2s_miller', 'd2s_loadcomp', 'd2s_bias'):
    net = os.path.join(XS, 'net', f'{s}.spice')
    if os.path.exists(net):
        os.remove(net)  # never compare against a stale netlist
    r = subprocess.run(['xschem', '--rcfile', os.path.join(XS, 'xschemrc'), '-n', '-s', '-q', '-x',
                        '-o', os.path.join(XS, 'net'), os.path.join(XS, f'{s}.sch')],
                       cwd=XS, env=dict(os.environ, PWD=XS), capture_output=True, text=True)
    if r.returncode or not os.path.exists(net):
        # xschem's exit status is not an error by itself (it can be nonzero with a complete
        # netlist); report it and xschem's messages, then compare whatever netlist was written
        msg = [l for l in (r.stdout + r.stderr).splitlines() if not l.startswith('MODELS_')]
        print(f'{s}: xschem exit status {r.returncode}' + ('' if os.path.exists(net) else ', NO NETLIST WRITTEN'))
        for l in msg[-15:]:
            print('   ', l)

def num(v):
    m = re.match(r'^([-\d.e+]+)([a-zA-Z]*)$', v)
    if not m:
        return v
    sc = {'': 1, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'm': 1e-3, 'k': 1e3}
    return round(float(m.group(1)) * sc.get(m.group(2).lower(), 1), 15)

def xnet(fn):
    devs = {}
    for line in open(fn):
        tok = line.split()
        if not tok or tok[0].startswith('*') or tok[0].startswith('.'):
            continue
        kv = {k: num(v) for k, v in (t.split('=') for t in tok if '=' in t)}
        pos = [t for t in tok[1:] if '=' not in t]
        if tok[0][0] in 'Xx':
            devs[tok[0][1:]] = (pos[-1], tuple(pos[:-1]), kv)
        elif tok[0][0] in 'Ii':
            devs[tok[0]] = ('isource', tuple(pos[:2]), {'value': num(pos[2])})
    return devs

bad = 0
for spice, sub, dfl in [('d2s_miller.spice', 'd2s_miller', None), ('d2s_loadcomp.spice', 'd2s_loadcomp', None),
                        ('d2s_bias.spice', 'd2s_bias', {'iab': '5u'})]:
    ports, devs = parse(spice, sub, dfl)
    netfile = os.path.join(HERE, 'xschem', 'net', f'{sub}.spice')
    if not os.path.exists(netfile):
        print(f'{sub}: no netlist, skipped'); bad += 1; continue
    x = xnet(netfile)
    hdr = open(netfile).read()
    m = re.search(rf'\.subckt {sub} (.*)', hdr)
    xports = m.group(1).split() if m else []
    if xports != ports:
        print(f'{sub}: port order {xports} != {ports}'); bad += 1
    src = {d['name']: (d['model'], tuple(d['nets']), {k: num(v) for k, v in d['p'].items()}) for d in devs}
    for n in sorted(set(src) | set(x)):
        if n not in x or n not in src:
            print(f'{sub}: {n} only in {"source" if n in src else "xschem"}'); bad += 1; continue
        (ms, ns, ps), (mx, nx, px) = src[n], x[n]
        if ms != mx or ns != nx:
            print(f'{sub}: {n} {ms}{ns} != {mx}{nx}'); bad += 1
        for k in ('w', 'l', 'ng', 'value'):
            if k in ps and num(str(ps[k])) != px.get(k, 1 if k == 'ng' else None):
                print(f'{sub}: {n} {k} {ps[k]} != {px.get(k)}'); bad += 1
    print(f'{sub}: {len(src)} devices, {len(ports)} ports compared')
print('MISMATCHES:', bad)
sys.exit(1 if bad else 0)
