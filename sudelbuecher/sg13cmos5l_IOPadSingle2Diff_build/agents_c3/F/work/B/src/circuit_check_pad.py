# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B: every device of the pad candidate against the s2d circuit plus the protection, dummies apart.

    python3 circuit_check_pad.py <pad_candidate.cdl> <circuit dir> <s2d_pad_esd_xschem.spice>

The layout's devices are taken from pad_candidate.cdl, flattened with net names (KLayout's deep LVS shows the
extracted pad equal to this file device by device: logs/pad_lvs.log). The circuit: s2d_mpdda (six unit_r2),
s2d_mpdda_pd's output ties, bias_tree_noab_pd with bias_diodes, and the protection s2d_pad_esd, flattened with the
pad's net names (vdd -> iovdd, vss -> iovss, vin -> pad, vfbp / voutp -> outp, vfbn / voutn -> outn).
Compared per signature (model, {D, S}, G, B, L) -> total W (MOS; tubs as 2 x 10/1 with B = S), rhigh chains reduced in
series to one resistor between their end nodes (total L), rppd / diodes per (model, nodes, size). A layout device
that has no circuit signature and D = S is a dummy (listed apart); everything else must match exactly."""
import collections
import re
import sys

U = lambda s: float(re.sub(r'[a-zA-Z]+$', '', s)) * {'u': 1, 'p': 1e-6, '': 1}.get(re.sub(r'^[0-9.e+-]+', '', s), 1)


def parse(path):
    subs, cur, top = {}, None, []
    for line in open(path).read().replace('\n+', ' ').splitlines():
        t = line.split()
        if not t or t[0].startswith('*'):
            continue
        if t[0].upper() == '.SUBCKT':
            cur = t[1].lower()
            subs[cur] = ([p.lower() for p in t[2:] if '=' not in p], [])
            continue
        if t[0].upper() == '.ENDS':
            cur = None
            continue
        if cur:
            subs[cur][1].append(t)
    return subs


def flat(subs, cell, nets, prefix, out):
    pins, lines = subs[cell]
    m = dict(zip(pins, nets))
    net = lambda n: m.get(n.lower(), prefix + n.lower())
    for t in lines:
        pos = [x for x in t[1:] if '=' not in x]
        par = dict(x.lower().split('=', 1) for x in t[1:] if '=' in x)
        model = pos[-1].lower()
        if t[0][0] in 'Xx' and model in subs:
            flat(subs, model, [net(n) for n in pos[:-1]], prefix + t[0].lower() + '.', out)
        else:
            out.append((t[0][0].upper(), model, [net(n) for n in pos[:-1]], par))
    return out


def signatures(devs):
    sig, dummies = collections.Counter(), collections.Counter()
    res = [d for d in devs if d[1] == 'rhigh']
    # rhigh: series chains through nodes that touch only rhigh segments (two of them) -> one resistor
    deg = collections.Counter(n for d in res for n in d[2][:2])
    other = collections.Counter(n for d in devs if d[1] != 'rhigh' for n in d[2])
    adj = collections.defaultdict(list)
    for i, d in enumerate(res):
        adj[d[2][0]].append(i)
        adj[d[2][1]].append(i)
    seen = set()
    for i, d in enumerate(res):
        if i in seen:
            continue
        chain, ends, L = {i}, [], 0.0
        stack = [i]
        while stack:
            j = stack.pop()
            for n in res[j][2][:2]:
                if deg[n] == 2 and other[n] == 0:
                    for k in adj[n]:
                        if k not in chain:
                            chain.add(k)
                            stack.append(k)
                else:
                    ends.append(n)
        seen |= chain
        L = sum(U(res[k][3]['l']) for k in chain)
        sig[('rhigh', tuple(sorted(set(ends))), round(U(d[3]['w']), 3), round(L, 3))] += 1
    for kind, model, n, p in devs:
        if model == 'rhigh':
            continue
        if kind == 'M' or model.startswith('sg13_hv'):
            d, g, s, b = n[:4]
            w = U(p['w']) * float(p.get('m', 1))
            key = (model, tuple(sorted((d, s))), g, b, round(U(p['l']), 3))
            sig[key] += round(w, 3)
        elif model in ('dantenna', 'dpantenna'):      # area (um2) from A, or from w x l
            a = U(p['a']) * 1e6 if 'a' in p else U(p['w']) * U(p['l'])
            sig[(model, tuple(n[:2]), round(a, 3))] += float(p.get('m', 1))
        else:
            vals = tuple(sorted((k, p[k]) for k in ('w', 'l') if k in p))
            sig[(model, tuple(n[:2]), n[2] if len(n) > 2 else '', vals)] += 1
    return sig


layout_subs = parse(sys.argv[1])
top = 'sg13cmos5l_iopadsingle2diff'
lay = flat(layout_subs, top, layout_subs[top][0], '', [])
# tubs: X tub instances flatten into their one MOS (d g s s), already handled by flat (tub_p20x1_c3 is a subckt)
cs = parse(sys.argv[2] + '/s2d_mpdda.spice')
cs.update(parse(sys.argv[2] + '/units.spice'))
cs.update(parse(sys.argv[2] + '/s2d_pd.spice'))
cs.update(parse(sys.argv[2] + '/bias_tree_noab_pd.spice'))
cs.update(parse(sys.argv[2] + '/bias_ref_pd.spice'))
cs.update(parse(sys.argv[3]))
# parameters: lcas = 3, rl = 50.6u, wcl = 12u
SUBST = {'{lcas}': '3', '{rl}': '50.6u', '{wcl}': '12u', '{10e-6*lcas}': '30u', '{1e-6*lcas}': '3u'}
for c in cs.values():
    for t in c[1]:
        for i, x in enumerate(t):
            for a, b in SUBST.items():
                if a in x:
                    t[i] = x.replace(a, b)
P = {'vdd': 'iovdd', 'vss': 'iovss', 'vin': 'pad', 'vref': 'vref', 'vcm': 'vcm', 'voutp': 'outp', 'voutn': 'outn',
     'vfbp': 'outp', 'vfbn': 'outn', 'en_3v3': 'en_3v3', 'en_3v3_b': 'en_3v3_b', 'iref': 'iref'}
ckt = flat(cs, 's2d_mpdda_pd', [P.get(n, n) for n in cs['s2d_mpdda_pd'][0]], 'xa.', [])
ckt = flat(cs, 'bias_tree_noab_pd', [P.get(n, n) for n in cs['bias_tree_noab_pd'][0]], 'xt.', ckt)
ckt = flat(cs, 's2d_pad_esd', ['iovdd', 'iovss', 'pad'], 'esd.', ckt)
# the circuit's internal node names differ from the layout's (xa.xs.xa1.sa vs sa_a1 ...): map them by unit
REN = {}
for u in ('a1', 'a2', 'f1', 'f2', 'm1', 'm2'):
    REN['xa.xs.x%s.sa' % u] = 'sa_%s' % u
    REN['xa.xs.x%s.sb' % u] = 'sb_%s' % u
for n in ('x', 'y', 'xc', 'yc', 'lp', 'ln', 'dd', 'vcmfb'):
    REN['xa.xs.' + n] = n
REN.update({'xt.ni': 'ni', 'esd.gp': 'gp', 'esd.gn': 'gn', 'sub!': 'iovss', 'esd.sub!': 'iovss'})
ckt = [(k, m, [REN.get(n, n) for n in nets], p) for k, m, nets, p in ckt]
lay = [(k, m, [n.lower() for n in nets], p) for k, m, nets, p in lay]
L, C = signatures(lay), signatures(ckt)
ok = True
for key in sorted(set(L) | set(C), key=str):
    a, b = L.get(key, 0), C.get(key, 0)
    if abs(a - b) > 1e-6:
        is_dummy = b == 0 and ((key[0].startswith('sg13_hv') and key[1][0] == key[1][1]) or
                               (key[0] == 'rhigh' and len(key[1]) == 1))      # D = S, or a rhigh with both ends on one net
        if is_dummy:
            print('dummy   %-70s layout %s' % (key, a))
            continue
        ok = False
        print('DIFFER  %-70s layout %s circuit %s' % (key, a, b))
print('circuit check: %d layout signatures, %d circuit signatures: %s' % (
    len(L), len(C), 'EQUAL apart from the dummies' if ok else 'DIFFERENT'))
