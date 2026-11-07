# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Netlist en_ctrl_stage_b.sch with xschem (as a .subckt) and compare it with the source subckt
../../netlist/source/en_ctrl_stage_b.spice: port order, and per instance the cell and the nets in pin order.
Usage: python3 check_en_ctrl_stage_b.py [sheet.sch]   (exit 1 on any difference). Needs PDK_ROOT, PDK."""
import os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
SCH = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, 'en_ctrl_stage_b.sch')
SRC = os.path.join(HERE, '../../netlist/source/en_ctrl_stage_b.spice')
CELL = 'en_ctrl_stage_b'

def lines(text):
    out = []
    for l in text.splitlines():
        if l.startswith('+') and out:
            out[-1] += ' ' + l[1:]
        else:
            out.append(l)
    return out

def parse(text, header_prefix):
    ports, inst, inside = None, {}, False
    for l in lines(text):
        t = l.split()
        if not t:
            continue
        if t[0].lower() == header_prefix and len(t) > 1 and t[1] == CELL:
            ports, inside = t[2:], True
        elif inside and t[0].lower().startswith(('.ends', '**.ends')):
            break
        elif inside and t[0][0] in 'Xx':
            inst[t[0].upper()] = (t[-1], t[1:-1])
    return ports, inst

d = tempfile.mkdtemp()
out = os.path.join(d, CELL + '.spice')
env = dict(os.environ, PWD=os.path.dirname(SCH))
r = subprocess.run(['xschem', '--rcfile', os.path.join(HERE, 'xschemrc'), '-n', '-s', '-q', '-x', '--no_x',
                    '--tcl', 'set top_is_subckt 1', '-o', d, '-N', CELL + '.spice', SCH],
                   cwd=os.path.dirname(SCH), env=env, capture_output=True, text=True)
print('xschem exit', r.returncode, (r.stderr or '').strip()[:400])
if not os.path.exists(out):
    print('FAIL: no netlist written'); sys.exit(1)
net = open(out).read()
bad = []
if 'IS MISSING' in net:
    bad.append('missing symbol(s): ' + ', '.join(sorted(set(re.findall(r'(\S+) IS MISSING', net)))))
p_src, i_src = parse(open(SRC).read(), '.subckt')
p_sch, i_sch = parse(net, '.subckt')
if p_sch is None:
    p_sch, i_sch = parse(net, '**.subckt')
if p_src != p_sch:
    bad.append(f'port order differs:\n  src {p_src}\n  sch {p_sch}')
for n in sorted(set(i_src) | set(i_sch)):
    a, b = i_src.get(n), i_sch.get(n)
    if a != b:
        bad.append(f'{n}: source {a} | sheet {b}')
print(f'source: {len(i_src)} instances, sheet: {len(i_sch)} instances')
print('\n'.join(bad) if bad else 'RESULT: MATCH')
sys.exit(1 if bad else 0)
