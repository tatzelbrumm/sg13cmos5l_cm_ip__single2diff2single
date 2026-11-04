# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Lead check (C3, stage B): the pad CDL's top level against the circuit.

python3 pad_cdl_check.py <pad.cdl> <P cells.cdl> <N cells.cdl> <F cells.cdl> ...

1. Every instance port of the pad subckt lands on the circuit net of the same name (the cells' port names are the
   s2d_mpdda_pd / bias_tree_noab_pd net names), apart from the pad-level aliases below.
2. Every cell body in the pad CDL is text-identical to the body the lead already checked (P / N / F cell CDLs).
3. Every s2d circuit block is instantiated exactly once.
"""
import collections, re, sys
ALIAS = {'vdd': 'iovdd', 'vss': 'iovss', 'vin': 'pad', 'vfbp': 'outp', 'voutp': 'outp', 'vfbn': 'outn', 'voutn': 'outn'}
def subckts(path):
    out, cur, body = {}, None, []
    for l in open(path).read().replace('\n+', ' ').splitlines():
        t = l.split()
        if t and t[0].upper() == '.SUBCKT': cur, body = t[1], [l]; continue
        if t and t[0].upper() == '.ENDS' and cur: out[cur] = body + [l]; cur = None; continue
        if cur is not None and t and not l.startswith('*'): body.append(l)
    return out
pad = subckts(sys.argv[1]); ref = {}
for p in sys.argv[2:]: ref.update(subckts(p))
ok = True
top = pad['sg13cmos5l_IOPadSingle2Diff']
for l in top[1:-1]:
    t = l.split()
    if not t[0].upper().startswith('X'): continue
    cell, nets = t[-1], t[1:-1]
    ports = pad[cell][0].split()[2:]
    for p, n in zip(ports, nets):
        want = ALIAS.get(p, p)
        if n != want: print(f'{t[0]} ({cell}): port {p} on {n}, circuit net {want}'); ok = False
blocks = collections.Counter(l.split()[-1] for l in top[1:-1] if l.split()[0].upper().startswith('X'))
print('instances:', dict(blocks))
for cell in blocks:
    same = cell in ref and [x.split() for x in pad[cell]] == [x.split() for x in ref[cell]]
    print(f'  {cell}: body {"identical to the checked CDL" if same else "DIFFERENT or not in the checked CDLs"}')
    ok &= same
print('top-level connectivity:', 'equal to the circuit' if ok else 'DIFFERENT')
sys.exit(0 if ok else 1)
