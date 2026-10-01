#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Netlist xschem/tb_d2s_*.sch with xschem and compare the top level, element by element
(name, nets in order, value), against the hand-written tb_d2s_*.spice decks. GND == 0.
Subcircuit bodies are checked separately by check_xschem.py.
    python3 check_tb_xschem.py       (needs xschem on PATH and $PDK_ROOT set)
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
XS = os.path.join(HERE, 'xschem')
NET = os.path.join(XS, 'net')
os.makedirs(NET, exist_ok=True)


def elements(text):
    """Top-level elements only: lines before the first .subckt, continuation lines joined."""
    lines, out = [], {}
    for raw in text.split('\n'):
        if raw.startswith('+') and lines:
            lines[-1] += ' ' + raw[1:]
        else:
            lines.append(raw)
    for l in lines:
        l = l.strip()
        if l.lower().startswith('.subckt'):
            break
        if not l or l[0] in '*.' or l.lower().startswith(('let', 'meas', 'plot', 'if', 'end', 'tran', 'ac ', 'print')):
            continue
        t = l.split()
        k = t[0][0].upper()
        n = {'V': 2, 'I': 2, 'R': 2, 'C': 2, 'L': 2, 'E': 4}.get(k)
        if k == 'X':
            nets, val = t[1:-1], t[-1]
        elif n:
            nets, val = t[1:1 + n], ' '.join(t[1 + n:])
        else:
            continue
        nets = ['0' if x.upper() == 'GND' else x for x in nets]
        val = re.sub(r'\s+m=1$', '', val.replace(' ', ' ').strip()).lower().replace(' ', '')
        out[t[0].upper()] = (tuple(nets), val)
    return out


bad = 0
for tb in ('tb_d2s_miller_step', 'tb_d2s_miller_loop', 'tb_d2s_loadcomp_step', 'tb_d2s_loadcomp_loop'):
    net = os.path.join(NET, tb + '.spice')
    if os.path.exists(net):
        os.remove(net)
    r = subprocess.run(['xschem', '--rcfile', os.path.join(XS, 'xschemrc'), '-n', '-s', '-q', '-x', '-o', NET,
                        os.path.join(XS, tb + '.sch')], cwd=XS, env=dict(os.environ, PWD=XS),
                       capture_output=True, text=True)
    if not os.path.exists(net):
        print(f'{tb}: NO NETLIST (xschem status {r.returncode})'); bad += 1; continue
    src, xs = elements(open(os.path.join(HERE, tb + '.spice')).read()), elements(open(net).read())
    for k in sorted(set(src) | set(xs)):
        if k not in src or k not in xs:
            print(f'{tb}: {k} only in {"deck" if k in src else "xschem"}'); bad += 1
        elif src[k] != xs[k]:
            print(f'{tb}: {k} deck {src[k]} != xschem {xs[k]}'); bad += 1
    subs = re.findall(r'^\.subckt (\S+)', open(net).read(), re.M)
    print(f'{tb}: {len(src)} top-level elements compared; subcircuits from schematics: {subs}')
print('MISMATCHES:', bad)
sys.exit(1 if bad else 0)
