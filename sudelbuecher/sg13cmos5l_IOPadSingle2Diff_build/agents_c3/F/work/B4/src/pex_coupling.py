# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B4: coupling capacitance of one net to every other net in a magic PEX netlist (C elements summed per
net pair; hierarchical names reduced to their last component).   python3 pex_coupling.py <pex.spice> <net> [n]"""
import sys
from collections import defaultdict
f, net = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
unit = {'f': 1.0, 'a': 1e-3, 'p': 1e3}
s = defaultdict(float)
for line in open(f):
    t = line.split()
    if len(t) < 4 or not t[0].upper().startswith('C'):
        continue
    a, b, v = t[1].split('.')[-1], t[2].split('.')[-1], t[3]
    val = float(v[:-1]) * unit[v[-1]] if v[-1] in unit else float(v) * 1e15
    if a == net and b != net:
        s[b] += val
    elif b == net and a != net:
        s[a] += val
print(f'| {net} to | C (fF) |\n|---|---:|')
for k, v in sorted(s.items(), key=lambda kv: -kv[1])[:n]:
    print(f'| {k} | {v:.3f} |')
