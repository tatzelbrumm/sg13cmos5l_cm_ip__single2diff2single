# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""cdl_compare.py: inputs/circuit_vs_cdl.py (the lead's check), adapted by agent BA (C2, 2026-11-03); C3 BA (2026-11-04)
added 6.: the drawn fingers, i.e. per MOS key (dummies included) the number of fingers of each finger width w / ng. so that both sides
may be CDLs (xschem's LVS netlist of the pad sheet against pad_candidate.cdl) or SPICE sources.

python3 cdl_compare.py <ref cdl> <ref top> <files ...> -- <circuit top line ...>

Changes against circuit_vs_cdl.py (everything else, incl. the tables and the series reduction, is unchanged):
 1. inside unit_r* instances EVERY internal net gets the suffix _<U> (sa_A as before, and now also the rhigh chain
    nodes n1_A ... n3_A, which would otherwise merge across the four units by their local names);
 2. xschem CDL resistor lines (`R<name> p m <value> $SUB=<body> $[<model>] w= l=`) are read (model from $[...]);
 3. diode area: the `a` / `A` parameter if given, else w * l (the sheet's diodes carry only w, l);
 4. IHP's sg13cmos5l_DCNDiode / sg13cmos5l_DCPDiode (black boxes in the sheet) are compared as what IHP's LVS
    extracts from the PCells (pad_candidate.cdl): dantenna (iovss, pad) 2 x 85.176p, dpantenna (pad, iovdd) 2 x 82.908p;
 5. RESULT also requires the dummies to agree (the brief: device for device, dummies included).
 6. (C3) fingers: per key, Counter{finger width: number of fingers} (ng * m fingers of w / ng each) must agree too.
"""
import re, sys, collections

PARAMS = {'lcas': 3.0, 'rl': 50.6e-6, 'wcl': 12e-6}
IOCELLS = {'sg13cmos5l_dcndiode': ('dantenna', (0, 1), '85.176p', 2), 'sg13cmos5l_dcpdiode': ('dpantenna', (0, 1), '82.908p', 2)}


def num(s):
    s = s.strip().lower()
    if s.startswith('{') and s.endswith('}'):
        return float(eval(s[1:-1], {}, dict(PARAMS)))
    m = re.match(r'^([-+0-9.e]+)([a-z]*)$', s)
    v, u = float(m.group(1)), m.group(2)
    return v * {'': 1, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'm': 1e-3, 'k': 1e3, 'meg': 1e6}.get(u[:3] if u.startswith('meg') else u[:1], 1)


def norm(t):
    """CDL resistor: R<name> p m <value> $SUB=b $[model] ... -> R<name> p m b model ..."""
    if t[0][0] in 'Rr' and any(x.startswith('$[') for x in t):
        model = [x for x in t if x.startswith('$[')][0][2:].rstrip(']').rstrip('\\')
        sub = [x.split('=', 1)[1] for x in t if x.upper().startswith('$SUB=')]
        par = [x for x in t[1:] if '=' in x and not x.startswith('$')]
        return [t[0], t[1], t[2]] + sub[:1] + [model] + par
    return t


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
            cur['body'].append(norm(t))
    return subs


def flatten(subs, lines):
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
                nets = [m[n] if n in m else (f'{n}_{t[0][1:].upper()}' if unit else n) for n in bp[:-1]]
                body.append([b[0]] + nets + [bp[-1]] + bn)
            out += flatten(subs, body)
        elif model.lower() in IOCELLS:
            dm, idx, a, mult = IOCELLS[model.lower()]
            out.append((t[0], [pos[i] for i in idx], dm, {'a': a, 'm': str(mult)}))
        else:
            out.append((t[0], pos[:-1], model.lower(), par))
    return out


def table(devs):
    mos, dum, res, dio = (collections.defaultdict(float) for _ in range(4))
    fing = collections.defaultdict(collections.Counter)
    for name, nets, model, par in devs:
        if model.startswith('sg13_') and len(nets) == 4:
            d, g, s, b = nets
            w = num(par.get('w', '0')) * float(par.get('m', '1'))
            key = (model, round(num(par['l']) * 1e6, 3), tuple(sorted((d, s))), g, b)
            (dum if d == s else mos)[key] += w * 1e6
            ng = int(float(par.get('ng', '1'))) * int(float(par.get('m', '1')))
            fing[key][round(num(par.get('w', '0')) / int(float(par.get('ng', '1'))) * 1e6, 3)] += ng
        elif model in ('rhigh', 'rppd', 'rsil'):
            res[(model, round(num(par['w']) * 1e6, 3), tuple(nets[:2]))] += num(par['l']) * 1e6
        elif model in ('dantenna', 'dpantenna'):
            a = par.get('a')
            area = num(a) * 1e12 if a else num(par['w']) * num(par['l']) * 1e12
            dio[(model, tuple(nets[:2]))] += area * float(par.get('m', '1'))
        else:
            print('  (not compared: %s %s %s)' % (name, model, ' '.join(nets)))
    return mos, dum, res, dio, fing


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
    print('devices: layout reference %d, circuit %d (one line per finger / segment on the reference side)' % (len(lay_devs), len(cir_devs)))
    L, C = table(lay_devs), table(cir_devs)
    ok = True
    for title, i_ in (('MOS (W sums, dummies apart)', 0), ('dummies (D = S)', 1), ('diodes (area, um2)', 3)):
        keys = sorted(set(L[i_]) | set(C[i_]), key=str)
        diff = [(k, L[i_].get(k, 0), C[i_].get(k, 0)) for k in keys if abs(L[i_].get(k, 0) - C[i_].get(k, 0)) > 1e-3]
        print(f'## {title}: {len(keys)} keys, {len(diff)} differ')
        for k, l, c in diff:
            print(f'  {k}: layout {l:g}  circuit {c:g}')
        ok &= not diff
    keys = sorted(set(L[4]) | set(C[4]), key=str)
    diff = [(k, dict(L[4].get(k, {})), dict(C[4].get(k, {}))) for k in keys if L[4].get(k) != C[4].get(k)]
    print(f'## fingers (finger width: count, per MOS key incl. dummies): {len(keys)} keys, {len(diff)} differ')
    for k, l, c in diff:
        print(f'  {k}: layout {l}  circuit {c}')
    ok &= not diff
    rl, rc = series(L[2]), series(C[2])
    keys = sorted(set(rl) | set(rc), key=str)
    diff = [(k, rl.get(k, 0), rc.get(k, 0)) for k in keys if abs(rl.get(k, 0) - rc.get(k, 0)) > 1e-3]
    print(f'## resistors (series-reduced lengths): {len(keys)} keys, {len(diff)} differ')
    for k, l, c in diff:
        print(f'  {k}: layout {l:g}  circuit {c:g}')
    print('RESULT', 'circuit == layout reference, dummies included' if ok and not diff else 'DIFFERENT')
    sys.exit(0 if ok and not diff else 1)
