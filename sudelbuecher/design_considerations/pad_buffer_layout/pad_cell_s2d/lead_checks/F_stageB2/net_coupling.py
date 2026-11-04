# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Net-priority evaluation (C3, lead): capacitance per net and coupling between nets from a magic C-coupled PEX
(sak-pex.sh -m 2). python3 net_coupling.py <label>=<pex.spice> [<label>=<pex.spice> ...]

Magic names internal nets hierarchically (s2d_block_0.<cell>.<net>); the last component is the circuit net name.
Unnamed nodes (a_*#, e.g. rhigh heads) and device-internal names are kept as they are. Values in fF."""
import collections, re, sys
SENS = ['pad', 'vref', 'vcm', 'outp', 'outn', 'x', 'y', 'xc', 'yc', 'vbp', 'vbn', 'vbpc', 'vbnc', 'vcmfb', 'iref', 'ni']
AGG = ['en_3v3', 'en_3v3_b']
SUP = ['iovdd', 'iovss', 'vdd', 'vss']
PAIRS = [('outp', 'outn'), ('x', 'y'), ('xc', 'yc')]
def val(s):
    m = re.match(r'([0-9.eE+-]+)([a-zA-Z]*)', s); v = float(m.group(1)); u = m.group(2).lower()
    return v * {'': 1e15, 'f': 1, 'a': 1e-3, 'p': 1e3, 'n': 1e6, 'ff': 1, 'pf': 1e3, 'af': 1e-3}.get(u, 1e15)
def load(path):
    tot, cpl = collections.Counter(), collections.Counter()
    name = lambda n: n.split('.')[-1] if '.' in n and not n.startswith('a_') else n
    for l in open(path).read().replace('\n+', ' ').splitlines():
        t = l.split()
        if not t or t[0][0] not in 'Cc' or len(t) < 4: continue
        a, b, c = name(t[1]), name(t[2]), val(t[3])
        tot[a] += c; tot[b] += c
        if a != b: cpl[tuple(sorted((a, b)))] += c
    return tot, cpl
runs = [(a.split('=', 1)[0], load(a.split('=', 1)[1])) for a in sys.argv[1:]]
hdr = ' | '.join(r for r, _ in runs)
print(f'## Total capacitance per net (fF): {hdr}\n\n| net | ' + ' | '.join(r for r, _ in runs) + ' |\n|---|' + '---:|' * len(runs))
for n in SENS + AGG:
    print(f'| {n} | ' + ' | '.join(f'{t[n]:.2f}' for _, (t, c) in runs) + ' |')
print(f'\n## Pair balance (fF, total C of each side)\n\n| pair | ' + ' | '.join(r for r, _ in runs) + ' |\n|---|' + '---|' * len(runs))
for p, q in PAIRS:
    print(f'| {p} / {q} | ' + ' | '.join(f'{t[p]:.2f} / {t[q]:.2f} (Δ {t[p] - t[q]:+.2f})' for _, (t, c) in runs) + ' |')
print(f'\n## Coupling of the sensitive nets to the enables and to each other (fF, > 0.01)\n\n| net pair | ' + ' | '.join(r for r, _ in runs) + ' |\n|---|' + '---:|' * len(runs))
keys = set()
for _, (t, c) in runs:
    keys |= {k for k, v in c.items() if v > 0.01 and ((k[0] in SENS and k[1] in SENS + AGG) or (k[1] in SENS and k[0] in SENS + AGG))}
for k in sorted(keys, key=lambda k: -max(c.get(k, 0) for _, (t, c) in runs)):
    print(f'| {k[0]} – {k[1]} | ' + ' | '.join(f'{c.get(k, 0):.3f}' for _, (t, c) in runs) + ' |')
