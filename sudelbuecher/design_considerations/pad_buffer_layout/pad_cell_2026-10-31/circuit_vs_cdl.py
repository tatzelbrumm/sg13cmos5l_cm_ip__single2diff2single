# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Does a layout reference netlist (the CDL that LVS matched) equal the circuit? (C2, lead's check)

python3 circuit_vs_cdl.py <cdl> <cdl top> <spice files ...> -- <circuit top line ...>

Both sides are flattened. Net names: the local name of every net (hierarchy prefixes dropped), except inside instances
of `unit_r2` / `unit_r`, whose sa / sb become sa_<U> / sb_<U> (U = instance name without its X), the layout's names.
MOS (M or X with an sg13_* model) are compared as summed W per (model, L, {D, S}, G, B); dummies (D = S) are listed
apart. Resistors: summed length per (model, W, end nets after series reduction of 2-terminal chains). Diodes: count and
summed area per (model, nets). The circuit's top is given as SPICE lines after `--` (instances of the source subckts).
"""
import re, sys, collections

PARAMS = {'lcas': 3.0, 'rl': 50.6e-6}


def num(s):
    s = s.strip().lower()
    if s.startswith('{') and s.endswith('}'):
        return float(eval(s[1:-1], {}, dict(PARAMS)))
    m = re.match(r'^([-+0-9.e]+)([a-z]*)$', s)
    v, u = float(m.group(1)), m.group(2)
    return v * {'': 1, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'm': 1e-3, 'k': 1e3, 'meg': 1e6}.get(u[:3] if u.startswith('meg') else u[:1], 1)


def parse(text):
    text = re.sub(r'\n\+', ' ', text)
    subs, cur = {}, None
    for ln in text.splitlines():
        t = ln.split()
        if not t or t[0].startswith('*'):
            continue
        k = t[0].lower()
        if k == '.subckt':
            ports = [p for p in t[2:] if '=' not in p]
            cur = subs.setdefault(t[1], {'ports': ports, 'body': []})
        elif k == '.ends':
            cur = None
        elif cur is not None and t[0][0] in 'MXRDmxrd':
            cur['body'].append(t)
    return subs


def flatten(subs, lines, scope_inst=''):
    out = []
    for t in lines:
        pos = [p for p in t[1:] if '=' not in p]
        par = {p.split('=')[0].lower(): p.split('=', 1)[1] for p in t[1:] if '=' in p}
        model = pos[-1]
        if t[0][0] in 'Xx' and model in subs:
            sub = subs[model]
            m = dict(zip(sub['ports'], pos[:-1]))
            unit = model.startswith('unit_r')
            body = []
            for b in sub['body']:
                bp = [p for p in b[1:] if '=' not in p]
                bn = [p for p in b[1:] if '=' in p]
                nets = []
                for n in bp[:-1]:
                    if n in m:
                        nets.append(m[n])
                    elif unit and n in ('sa', 'sb'):
                        nets.append(f'{n}_{t[0][1:]}')
                    else:
                        nets.append(n)
                body.append([b[0]] + nets + [bp[-1]] + bn)
            out += flatten(subs, body)
        else:
            out.append((t[0], pos[:-1], model.lower(), par))
    return out


def table(devs):
    mos, dum, res, dio = (collections.defaultdict(float) for _ in range(4))
    for name, nets, model, par in devs:
        if model.startswith('sg13_') and len(nets) == 4:
            d, g, s, b = nets
            w = num(par.get('w', '0')) * float(par.get('m', '1'))
            key = (model, round(num(par['l']) * 1e6, 3), tuple(sorted((d, s))), g, b)
            (dum if d == s else mos)[key] += w * 1e6
        elif model in ('rhigh', 'rppd', 'rsil'):
            res[(model, round(num(par['w']) * 1e6, 3), tuple(nets[:2]))] += num(par['l']) * 1e6
        elif model in ('dantenna', 'dpantenna'):
            a = par.get('a') or par.get('A')
            dio[(model, tuple(nets[:2]))] += (num(a) * 1e12 if a else 1) * float(par.get('m', '1'))
    return mos, dum, res, dio


def series(res):
    """Reduce rhigh / rppd chains through nets that only two segments touch."""
    edges = [(k[0], k[1], k[2][0], k[2][1], v) for k, v in res.items()]
    changed = True
    while changed:
        changed = False
        deg = collections.Counter(n for e in edges for n in e[2:4])
        for n, c in deg.items():
            if c == 2 and not re.match(r'^(sa|sb)_|vss|iovss|pad|pa|pb', n):
                es = [e for e in edges if n in e[2:4]]
                if len(es) == 2 and es[0][:2] == es[1][:2]:
                    a = es[0][2] if es[0][3] == n else es[0][3]
                    b = es[1][2] if es[1][3] == n else es[1][3]
                    edges = [e for e in edges if e not in es] + [(es[0][0], es[0][1], a, b, es[0][4] + es[1][4])]
                    changed = True
                    break
    return collections.Counter({(m, w, tuple(sorted((a, b)))): round(l, 3) for m, w, a, b, l in edges})


if __name__ == '__main__':
    a = sys.argv[1:]
    i = a.index('--')
    cdl, top, srcs, toplines = a[0], a[1], a[2:i], a[i + 1:]
    lay = parse(open(cdl).read())
    lay_devs = flatten(lay, lay[top]['body'])
    src = {}
    for f in srcs:
        src.update(parse(open(f).read()))
    cir_devs = flatten(src, [ln.split() for ln in toplines])
    L, C = table(lay_devs), table(cir_devs)
    ok = True
    for title, i_ in (('MOS (W sums, dummies apart)', 0), ('dummies (D = S)', 1), ('diodes', 3)):
        keys = sorted(set(L[i_]) | set(C[i_]), key=str)
        diff = [(k, L[i_].get(k, 0), C[i_].get(k, 0)) for k in keys if abs(L[i_].get(k, 0) - C[i_].get(k, 0)) > 1e-3]
        print(f'## {title}: {len(keys)} keys, {len(diff)} differ')
        for k, l, c in diff:
            print(f'  {k}: layout {l:g}  circuit {c:g}')
        ok &= not diff or i_ == 1
    rl, rc = series(L[2]), series(C[2])
    keys = sorted(set(rl) | set(rc), key=str)
    diff = [(k, rl.get(k, 0), rc.get(k, 0)) for k in keys if abs(rl.get(k, 0) - rc.get(k, 0)) > 1e-3]
    print(f'## resistors (series-reduced lengths): {len(keys)} keys, {len(diff)} differ')
    for k, l, c in diff:
        print(f'  {k}: layout {l:g}  circuit {c:g}')
    print('RESULT', 'circuit == layout reference (dummies apart)' if ok and not diff else 'DIFFERENT')
