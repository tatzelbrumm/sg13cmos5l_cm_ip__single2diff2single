#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Netlist tp_en_ctrl.sch and slot7_testplatform.sch with xschem and compare them with the source netlist,
device by device (model, terminal nets in order, w / l / ng) and port by port.  Exit 1 on any difference.

    python3 check_sheets.py [--selftest]
--selftest changes one label in a copy of tp_en_ctrl.sch and expects the check to fail.
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', '..', 'netlist', 'source', 'slot7_testplatform.spice'))
OUTD = os.path.join(HERE, 'check_out')


def subckt(text, name):
    text = text.replace('\n+', ' ')
    m = re.search(rf'^\.subckt {re.escape(name)} (.*?)$(.*?)^\.ends', text, re.M | re.S | re.I)
    if not m:
        return None, None
    ports = [t for t in m.group(1).split() if '=' not in t]
    devs = {}
    for line in m.group(2).splitlines():
        tok = line.split()
        if not tok or tok[0][0] in '*.':
            continue
        kv = dict(t.split('=', 1) for t in tok if '=' in t)
        pos = [t for t in tok[1:] if '=' not in t]
        devs[tok[0].upper().lstrip('X')] = (pos[-1], pos[:-1], {k: kv.get(k) for k in ('w', 'l', 'ng')})
    return ports, devs


def netlist(sch, outdir):
    os.makedirs(outdir, exist_ok=True)
    net = os.path.join(outdir, os.path.basename(sch).replace('.sch', '.spice'))
    if os.path.exists(net):
        os.remove(net)
    env = dict(os.environ, PWD=os.path.dirname(sch))
    p = subprocess.run(['xschem', '--rcfile', os.path.join(HERE, 'xschemrc'), '-n', '-s', '-q', '-x', '--no_x',
                        '--tcl', 'set top_is_subckt 1', '-o', outdir, sch], capture_output=True, text=True,
                       env=env, cwd=os.path.dirname(sch), timeout=120)
    print(f'xschem {os.path.basename(sch)}: exit {p.returncode}', (p.stdout + p.stderr).strip()[-300:])
    text = open(net).read()
    if 'IS MISSING' in text:
        print('  MISSING symbols:', re.findall(r'.*IS MISSING.*', text))
    return text


def compare(cell, sch_text, src_text):
    sp, sd = subckt(src_text, cell)
    xp, xd = subckt(sch_text, cell)
    errs = []
    if xp is None:
        return [f'{cell}: no .subckt in the xschem netlist']
    if sp != xp:
        errs.append(f'{cell}: ports differ\n  source {sp}\n  xschem {xp}')
    for n in sorted(set(sd) | set(xd)):
        if n not in xd:
            errs.append(f'{cell}: {n} missing in the sheet')
        elif n not in sd:
            errs.append(f'{cell}: {n} only in the sheet')
        else:
            a, b = sd[n], xd[n]
            if a[0] != b[0] or a[1] != b[1]:
                errs.append(f'{cell}: {n} {a[0]} {a[1]} vs sheet {b[0]} {b[1]}')
            for k in ('w', 'l', 'ng'):
                if a[2][k] and (a[2][k] or '').lower() != (b[2][k] or '').lower():
                    errs.append(f'{cell}: {n} {k}={a[2][k]} vs sheet {b[2][k]}')
    print(f'{cell}: {len(sd)} source devices, {len(xd)} sheet devices, {len(errs)} differences')
    return errs


def main():
    src = open(SRC).read()
    sheets = ['tp_en_ctrl', 'slot7_testplatform']
    if '--selftest' in sys.argv:
        d = os.path.join(OUTD, 'selftest')
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(HERE):
            if f.endswith(('.sch', '.sym')):
                shutil.copy(os.path.join(HERE, f), d)
        t = open(os.path.join(d, 'tp_en_ctrl.sch')).read()
        t = re.sub(r'(lab_pin\.sym\}[^\n]*lab=)ns2\}', r'\1ns1}', t, count=1)   # a label, not a wire hint
        open(os.path.join(d, 'tp_en_ctrl.sch'), 'w').write(t)
        errs = compare('tp_en_ctrl', netlist(os.path.join(d, 'tp_en_ctrl.sch'), d), src)
        print('selftest:', 'PASS (difference found)' if errs else 'FAIL (no difference found)')
        sys.exit(0 if errs else 1)
    errs = []
    for s in sheets:
        errs += compare(s, netlist(os.path.join(HERE, s + '.sch'), OUTD), src)
    for e in errs:
        print(e)
    print('RESULT:', 'MATCH' if not errs else f'{len(errs)} differences')
    sys.exit(1 if errs else 0)


main()
