#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Check the finished-style sheets in this directory against the source netlist.

For tp_en_ctrl.sch and slot7_testplatform.sch:
  1. netlist with xschem (this directory's xschemrc, absolute paths, PWD set, old netlist deleted first,
     'set top_is_subckt 1'); report 'IS MISSING' symbols;
  2. compare with ../../netlist/source/slot7_testplatform.spice device by device: model, terminal nets in order,
     w / l / ng, and the port order of the .subckt header;
  3. the .sym next to each sheet: pin order = .subckt port order, pin names = the sheet's ipin/opin/iopin names;
  4. drawing lint: wire ends that touch nothing (dangling) and wire ends of different nets that touch.
Exit 1 on any difference.

    python3 check_drawn.py              # check both sheets, print MATCH or the differences
    python3 check_drawn.py --selftest   # must report the expected failures (see selftest())
Needs PDK_ROOT (default /foss/pdks) and PDK (default ihp-sg13cmos5l).  Pure standard-library Python.
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', '..', 'netlist', 'source', 'slot7_testplatform.spice'))
OUTD = os.path.join(HERE, 'check_out')
SHEETS = ['tp_en_ctrl', 'slot7_testplatform']


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
        devs[tok[0].upper()[1:]] = (pos[-1], pos[:-1], {k: kv.get(k) for k in ('w', 'l', 'ng')})
    return ports, devs


def netlist(sch, outdir, rc):
    os.makedirs(outdir, exist_ok=True)
    net = os.path.join(outdir, os.path.basename(sch).replace('.sch', '.spice'))
    if os.path.exists(net):
        os.remove(net)
    env = dict(os.environ, PWD=os.path.dirname(sch))
    env.setdefault('PDK_ROOT', '/foss/pdks')
    env.setdefault('PDK', 'ihp-sg13cmos5l')
    p = subprocess.run(['xschem', '--rcfile', rc, '-n', '-s', '-q', '-x', '--no_x', '--tcl', 'set top_is_subckt 1',
                        '-o', outdir, sch], capture_output=True, text=True, env=env, cwd=os.path.dirname(sch),
                       timeout=180)
    msg = (p.stdout + p.stderr).strip()
    print(f'xschem {os.path.basename(sch)}: exit {p.returncode}', msg[-300:])
    if not os.path.exists(net):
        return '', ['no netlist written']
    text = open(net).read()
    missing = re.findall(r'.*IS MISSING.*', text)
    return text, [f'MISSING symbol: {m.strip()}' for m in missing]


def compare(cell, sch_text, src_text):
    sp, sd = subckt(src_text, cell)
    xp, xd = subckt(sch_text, cell)
    if xp is None:
        return [f'{cell}: no .subckt in the xschem netlist']
    errs = []
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
                if a[2][k] and a[2][k].lower() != (b[2][k] or '').lower():
                    errs.append(f'{cell}: {n} {k}={a[2][k]} vs sheet {b[2][k]}')
    print(f'{cell}: {len(sd)} source devices, {len(xd)} sheet devices, {len(errs)} differences')
    return errs


def sym_pins(path):
    s = open(path).read()
    pins = []
    for m in re.finditer(r'^B 5 ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) \{([^}]*)\}', s, re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        a = dict(re.findall(r'(\w+)=(\S+)', m.group(5)))
        pins.append((a.get('sim_pinnumber'), a['name'], (x1 + x2) / 2, (y1 + y2) / 2))
    if pins and all(p[0] for p in pins):
        pins.sort(key=lambda p: int(p[0]))
    return [(n, x, y) for _, n, x, y in pins]


def check_symbol(cell, d, src_text):
    sp, _ = subckt(src_text, cell)
    names = [p[0] for p in sym_pins(os.path.join(d, cell + '.sym'))]
    sch = open(os.path.join(d, cell + '.sch')).read()
    sheet = re.findall(r'^C \{devices/(?:ipin|opin|iopin)\.sym\}[^\n]*?lab=([^\s}]+)', sch, re.M)
    errs = []
    if names != sp:
        errs.append(f'{cell}.sym: pin order {names}\n  .subckt order {sp}')
    if sorted(sheet) != sorted(names):
        errs.append(f'{cell}: sheet ports {sorted(set(sheet) - set(names))} / symbol pins '
                    f'{sorted(set(names) - set(sheet))} differ')
    if sheet != sp:
        errs.append(f'{cell}.sch: pin instances not in .subckt order (stand-alone netlists would reorder)')
    return errs


# ------------------------------------------------------------------------------------------------ drawing lint
def find_sym(ref, d):
    paths = [d, os.path.join(os.environ.get('PDK_ROOT', '/foss/pdks'), os.environ.get('PDK', 'ihp-sg13cmos5l'),
                             'libs.tech', 'xschem')]
    paths += [os.path.join(HERE, '..', '..', '..', m, 'schematic', 'xschem')
              for m in ('oa_core_pd', 'bg_core_pd', 'ocd_analog_switches')]
    xl = shutil.which('xschem')
    if xl:
        paths.append(os.path.join(os.path.dirname(os.path.realpath(xl)), '..', 'share', 'xschem', 'xschem_library'))
    for p in paths:
        f = os.path.join(p, ref)
        if os.path.exists(f):
            return f
    return None


def xform(px, py, rot, flip):
    if flip:
        px = -px
    for _ in range(rot % 4):
        px, py = -py, px
    return px, py


def lint(sch_path):
    """dangling wire ends, and wire ends / pins of different wire 'lab' hints that touch (a silent merge)"""
    d = os.path.dirname(sch_path)
    text = open(sch_path).read()
    wires = [(float(a), float(b), float(c), float(e), lab) for a, b, c, e, lab in
             re.findall(r'^N ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) \{lab=([^}]*)\}', text, re.M)]
    pins = []
    for ref, x, y, rot, flip in re.findall(r'^C \{([^}]*)\} ([-\d.]+) ([-\d.]+) (\d) (\d)', text, re.M):
        f = find_sym(ref, d)
        if not f:
            continue
        for _, px, py in sym_pins(f):
            dx, dy = xform(px, py, int(rot), int(flip))
            pins.append((round(float(x) + dx), round(float(y) + dy), ref))

    def on(x, y, w):
        x1, y1, x2, y2, _ = w
        return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2) and (x1 == x2 or y1 == y2)

    pinset = {(x, y) for x, y, _ in pins}
    msgs = []
    for i, w in enumerate(wires):
        for (x, y) in ((w[0], w[1]), (w[2], w[3])):
            touch = [v for j, v in enumerate(wires) if j != i and on(x, y, v)]
            if (round(x), round(y)) not in pinset and not touch:
                msgs.append(f'dangling wire end ({x:g}, {y:g}) lab={w[4]}')
            for v in touch:
                if v[4] and w[4] and v[4] != w[4]:
                    msgs.append(f'wire end ({x:g}, {y:g}) lab={w[4]} touches a wire lab={v[4]}')
    return msgs


def check(d, rc, outdir):
    src = open(SRC).read()
    errs = []
    for s in SHEETS:
        text, miss = netlist(os.path.join(d, s + '.sch'), outdir, rc)
        errs += miss
        errs += compare(s, text, src)
        errs += check_symbol(s, d, src)
        lm = lint(os.path.join(d, s + '.sch'))
        print(f'{s}: drawing lint {len(lm)} findings')
        errs += [f'{s}: {m}' for m in lm]
    return errs


def selftest():
    """1. one lab_pin vdd_1v2 -> vss_1v2 in a copy of tp_en_ctrl.sch: the compare must fail;
       2. the copy's top sheet netlisted with an rc that lacks the reused macros: IS MISSING must be reported."""
    d = os.path.join(OUTD, 'selftest')
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in os.listdir(HERE):
        if f.endswith(('.sch', '.sym')):
            shutil.copy(os.path.join(HERE, f), d)
    t = open(os.path.join(d, 'tp_en_ctrl.sch')).read()
    t2 = re.sub(r'(lab_pin\.sym\}[^\n]*lab=)vdd_1v2\}', r'\1vss_1v2}', t, count=1)
    assert t2 != t
    open(os.path.join(d, 'tp_en_ctrl.sch'), 'w').write(t2)
    # rc of the copy: only the PDK and the copy's own directory, so the reused macros are missing
    open(os.path.join(d, 'xschemrc'), 'w').write(
        'source $env(PDK_ROOT)/$env(PDK)/libs.tech/xschem/xschemrc\nappend XSCHEM_LIBRARY_PATH :[file dirname [info script]]\n')
    src = open(SRC).read()
    text, miss = netlist(os.path.join(d, 'tp_en_ctrl.sch'), d, os.path.join(d, 'xschemrc'))
    e1 = compare('tp_en_ctrl', text, src)
    for e in e1:
        print('  ', e)
    text, miss = netlist(os.path.join(d, 'slot7_testplatform.sch'), d, os.path.join(d, 'xschemrc'))
    for m in miss:
        print('  ', m)
    ok = bool(e1) and bool(miss)
    print('selftest:', 'PASS (changed label and missing symbols both detected)' if ok else
          f'FAIL (label change detected: {bool(e1)}, missing symbols detected: {bool(miss)})')
    return ok


def main():
    if '--selftest' in sys.argv:
        sys.exit(0 if selftest() else 1)
    errs = check(HERE, os.path.join(HERE, 'xschemrc'), OUTD)
    for e in errs:
        print(e)
    print('RESULT:', 'MATCH' if not errs else f'{len(errs)} differences')
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
