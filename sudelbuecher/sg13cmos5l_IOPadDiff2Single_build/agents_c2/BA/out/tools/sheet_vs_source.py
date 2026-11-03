#!/usr/bin/env python3
"""sheet_vs_source.py ROOT CELL SHEET SOURCE.spice ... (agent BA, C2 2026-11-03)
Netlists SHEET (xschem, as scripts/xschem/sheet_equiv.py does), flattens it and the subckt CELL of the source netlists
(with .subckt parameter defaults and instance overrides evaluated), and tests the two for graph isomorphism with the
ports anchored by name (sheet_equiv's matcher: MOS D/S and R ends may swap). Sizes compared: w, l, ng (m = 1)."""
import os, re, sys, tempfile
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts', 'xschem'))
import sheet_equiv as se
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from intended_equiv import graph_of, Net

SI = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e3, 'meg': 1e6, '': 1}
def val(v, scope):
    v = v.strip()
    if v.startswith('{') and v.endswith('}'): return float(eval(v[1:-1], {}, dict(scope)))
    m = re.fullmatch(r'([-+]?[\d.]+(?:e[-+]?\d+)?)(meg|[fpnumk]?)', v.lower())
    return float(m.group(1)) * SI[m.group(2)] if m else v
def norm(par):
    out = {k: '%.6g' % par[k] for k in ('w', 'l') if k in par}
    out['ng'] = '%d' % int(float(par.get('ng', 1)))
    return out

def parse_src(files):
    subs = {}
    for f in files:
        txt = re.sub(r'\n\+', ' ', open(f).read()); cur = None
        for ln in txt.splitlines():
            t = ln.split()
            if not t or t[0][0] in '*': continue
            if t[0].lower() == '.subckt':
                cur = t[1]; subs[cur] = ([p for p in t[2:] if '=' not in p], {p.split('=')[0]: p.split('=', 1)[1] for p in t[2:] if '=' in p}, [])
            elif t[0].lower() == '.ends': cur = None
            elif cur: subs[cur][2].append(t)
    return subs

def flat_src(subs, cell, nmap, scope, out):
    loc = {}
    def net(n):
        if n in nmap: return nmap[n]
        if n in ('0', 'GND') or n.endswith('!'): return n
        return loc.setdefault(n, Net())
    for t in subs[cell][2]:
        pos = [p for p in t[1:] if '=' not in p]; par = {p.split('=')[0].lower(): p.split('=', 1)[1] for p in t[1:] if '=' in p}
        model = pos[-1]
        if t[0][0] in 'Xx' and model in subs:
            ports, defs, _ = subs[model]
            sc = {k: val(v, {}) for k, v in defs.items()}
            sc.update({k: val(v, scope) for k, v in par.items()})
            flat_src(subs, model, {p: net(n) for p, n in zip(ports, pos[:-1])}, sc, out); continue
        out.append(dict(model=model, par=norm({k: val(v, scope) for k, v in par.items()}), nets=[net(n) for n in pos[:-1]]))

def flat_sheet(subs, cell, nmap, out):
    loc = {}
    def net(n):
        if n in nmap: return nmap[n]
        if n in ('0', 'GND') or n.endswith('!'): return n
        return loc.setdefault(n, Net())
    for name, pos, par in subs[cell][1]:
        if name[0].upper() == 'X' and pos[-1] in subs:
            flat_sheet(subs, pos[-1], {p: net(n) for p, n in zip(subs[pos[-1]][0], pos[:-1])}, out); continue
        out.append(dict(model=pos[-1], par=norm({k: float(v) for k, v in par.items() if k in ('w', 'l', 'ng')}), nets=[net(n) for n in pos[:-1]]))

root, cell, sheet, srcs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
sys.setrecursionlimit(20000)
with tempfile.TemporaryDirectory() as td:
    f = se.netlist(root, sheet, td); subs, top, miss = se.parse(f)
a = []; flat_sheet(subs, top, {p: 'PORT:' + p for p in subs[top][0]}, a)
src = parse_src(srcs); b = []
flat_src(src, cell, {p: 'PORT:' + p for p in src[cell][0]}, {k: val(v, {}) for k, v in src[cell][1].items()}, b)
po = subs[top][0] == src[cell][0]
same = sorted(subs[top][0]) == sorted(src[cell][0]) and se.isomorphic(graph_of(a), graph_of(b))
print('%-10s %s vs .subckt %s: sheet %d devices, source %d; port order %s; missing symbols %d' % (
    'equivalent' if same else 'DIFFERENT', sheet, cell, len(a), len(b), 'same' if po else 'DIFFERS %s / %s' % (subs[top][0], src[cell][0]), miss))
sys.exit(0 if same and po and not miss else 1)
