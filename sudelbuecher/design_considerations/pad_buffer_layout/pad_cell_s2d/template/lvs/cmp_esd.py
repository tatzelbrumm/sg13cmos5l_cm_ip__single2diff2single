# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# usage: python3 cmp_esd.py <xschem netlist of s2d_pad_esd.sch> <template_extracted.cir>
# compare the xschem netlist of s2d_pad_esd with the layout extraction of the template (device classes, nets, sizes)
import re, sys
from collections import Counter
def val(s):
    m = re.match(r'([\d.]+)([unp]?)', s); return float(m.group(1)) * {'u': 1, 'n': 1e-3, 'p': 1, '': 1e6}[m.group(2)]
def parse(path, netmap):
    lines = open(path).read().replace('\n+', ' ').splitlines()
    out = Counter()
    for l in lines:
        f = l.split()
        if not f or f[0][0] not in 'XMRD' or f[0].startswith('X') and len(f) < 4: continue
        n = lambda x: netmap.get(x, x)
        kv = dict(p.split('=') for p in f if '=' in p)
        mod = next(p for p in f[1:] if p in ('sg13_hv_nmos', 'sg13_hv_pmos', 'rppd', 'dantenna', 'dpantenna'))
        nets = [n(x) for x in f[1:f.index(mod)]]
        if mod.startswith('sg13_hv'):
            d, g, s, b = nets
            out[(mod, tuple(sorted((d, s))), g, b, round(val(kv.get('W', kv.get('w'))), 2))] += 1
        elif mod == 'rppd':
            out[(mod, tuple(sorted(nets[:2])), nets[2], round(val(kv['l']), 2))] += 1
        else:
            a = val(kv['A']) if 'A' in kv else val(kv['l']) * val(kv['w'])
            out[(mod, tuple(nets), 'area')] += round(a * int(kv.get('m', 1)), 1)
    return out
sch = parse(sys.argv[1], {'sub!': 'iovss'})
lm = {'iovss|vss': 'iovss'}                     # the layout's unnamed gate nets, named by the clamp they drive
for l in open(sys.argv[2]).read().replace('\n+', ' ').splitlines():
    f = l.split()
    if f and f[0].startswith('M') and 'sg13_hv_pmos' in f:
        lm[f[2]] = 'gp'
    if f and f[0].startswith('M') and 'sg13_hv_nmos' in f:
        lm[f[2]] = 'gn'
lay = parse(sys.argv[2], lm)
for k in sorted(set(sch) | set(lay), key=str):
    print('ok ' if sch[k] == lay[k] else 'DIFF', k, 'sch', sch[k], 'lay', lay[k])
sys.exit(0 if sch == lay else 1)
