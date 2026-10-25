#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Check that hand-edited xschem sheets still have the connectivity of a reference version.

    python3 scripts/xschem/sheet_equiv.py OLD_ROOT NEW_ROOT [SHEET ...]

OLD_ROOT and NEW_ROOT are two copies of this repository, for example a known-good commit and the
working tree. IIC-OSIC-TOOLS has no git, so export the commit on the host into ~/EDA, which the
container sees as /foss/designs (the script reads only macros/, schematic/ and testbenches/):

    host:       mkdir ~/EDA/ref_<commit>
                git -C ~/EDA/sg13cmos5l_cm_ip__single2diff2single archive <commit> macros schematic testbenches \
                  | tar -x -C ~/EDA/ref_<commit>
    container:  python3 scripts/xschem/sheet_equiv.py ../ref_<commit> .
    host:       rm -r ~/EDA/ref_<commit>

A snapshot of the sheets as delivered on 2026-10-20 is in the _sudelbuecher worktree,
sudelbuecher/design_considerations/consolidation/reference_sheets_2026-10-20 (same layout).

SHEET is a path relative to the roots; default: every .sch in macros/*/schematic/xschem,
macros/*/testbenches/xschem and macros/*/verification/cace/templates of NEW_ROOT that also exists in
OLD_ROOT.

Each sheet is netlisted by xschem in both roots (PDK xschemrc plus every macro's schematic and
testbench folder of that root on the library path), flattened to primitive devices and compared
as a graph: instance names and internal net names are ignored, ports are matched by name, MOS
drain/source and the two ends of R/C may swap, E/G sources may swap both terminal pairs at once,
models and sizes must agree. For a sheet that differs, the instances whose nets changed are
listed by name (useful when names were kept). Every symbol whose pins moved, were renamed or
were reordered is listed with the sheets that place it.

Exit status 1 if any sheet differs or netlists with a missing symbol. Needs xschem, PDK_ROOT and
PDK (source .designinit first); plain Python 3 otherwise (no extra packages).
"""
import glob, os, re, subprocess, sys, tempfile
from collections import Counter, defaultdict

SI = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e3, 'meg': 1e6, '': 1}


def num(v):
    m = re.fullmatch(r'([-+]?[\d.]+(?:e[-+]?\d+)?)(meg|[fpnumk]?)', v.lower())
    return '%.6g' % (float(m.group(1)) * SI[m.group(2)]) if m else v


def rcfile(root, tmp):
    dirs = sorted(glob.glob(os.path.join(root, 'macros', '*', 'schematic', 'xschem'))) + \
        sorted(glob.glob(os.path.join(root, 'macros', '*', 'testbenches', 'xschem'))) + \
        [os.path.join(root, 'schematic', 'xschem'), os.path.join(root, 'testbenches', 'xschem')]
    rc = os.path.join(tmp, 'xschemrc')
    with open(rc, 'w') as f:
        f.write('source $env(PDK_ROOT)/$env(PDK)/libs.tech/xschem/xschemrc\n')
        for d in dirs:
            if os.path.isdir(d):
                f.write('append XSCHEM_LIBRARY_PATH :%s\n' % os.path.abspath(d))
    return rc


def netlist(root, sheet, tmp):
    out = os.path.join(tmp, 'net'); os.makedirs(out, exist_ok=True)
    cell = os.path.splitext(os.path.basename(sheet))[0]; path = os.path.join(out, cell + '.spice')
    if os.path.exists(path): os.remove(path)
    env = dict(os.environ, PWD=tmp)
    subprocess.run(['xschem', '-n', '-s', '-q', '-x', '--no_x', '--rcfile', rcfile(root, tmp), '-o', out,
                    os.path.abspath(os.path.join(root, sheet))], cwd=tmp, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    return path if os.path.exists(path) else None


def parse(path):
    lines = []
    for ln in open(path):
        ln = ln.rstrip('\n')
        if ln.startswith('+') and lines: lines[-1] += ' ' + ln[1:]
        else: lines.append(ln)
    subs, top, cur, missing = {}, None, None, 0
    for ln in lines:
        if 'IS MISSING' in ln.upper(): missing += 1
        t = ln.split()
        if not t: continue
        k = t[0].lower()
        if k in ('.subckt', '**.subckt'):
            cur = t[1]; subs[cur] = ([x for x in t[2:] if '=' not in x], [])
            if k == '**.subckt': top = cur
            continue
        if k in ('.ends', '**.ends'): cur = None; continue
        if cur is None or t[0][0] in '*.': continue
        pos = [x for x in t[1:] if '=' not in x]
        par = {a.lower(): num(b) for a, b in (x.split('=', 1) for x in t[1:] if '=' in x) if a.lower() != 'mm_ok'}
        subs[cur][1].append((t[0], pos, par))
    return subs, top, missing


def flatten(subs, cell, nmap, out):
    loc = {}
    def net(n):
        if n in nmap: return nmap[n]
        if n.endswith('!') or n in ('0', 'GND'): return n
        return loc.setdefault(n, object())
    for name, pos, par in subs[cell][1]:
        typ = name[0].upper()
        if typ == 'X' and pos[-1] in subs:
            flatten(subs, pos[-1], {p: net(n) for p, n in zip(subs[pos[-1]][0], pos[:-1])}, out)
            continue
        if typ in 'XM': model, nets = pos[-1], pos[:-1]
        elif typ in 'EG' and len(pos) >= 5: model, nets = typ + ' ' + ' '.join(pos[4:]), pos[:4]   # linear: 4 nets + gain
        else: model, nets = typ + ' ' + ' '.join(pos[2:]), pos[:2]
        out.append((model, tuple(sorted(par.items())), [net(n) for n in nets]))


def graph(path):
    subs, top, missing = parse(path)
    devs = []; flatten(subs, top, {p: 'PORT:' + p for p in subs[top][0]}, devs)
    G = {'lab': {}, 'adj': {}}; nid = {}
    def add(n, lab): G['lab'][n] = lab; G['adj'].setdefault(n, {})
    def node(n):
        key = n if isinstance(n, str) else id(n)
        if key not in nid:
            nid[key] = ('N', len(nid)); add(nid[key], ('net', n if isinstance(n, str) else ''))
        return nid[key]
    def edge(a, b, role):
        r = tuple(sorted(G['adj'][a].get(b, ()) + (role,))); G['adj'][a][b] = r; G['adj'][b][a] = r
    for i, (model, par, nets) in enumerate(devs):
        d = ('D', i); add(d, ('dev', model, par))
        if model[:2] in ('E ', 'G ') and len(nets) == 4:   # out+ out- in+ in-: both pairs may swap together
            for k, (o, n) in enumerate(((nets[0], nets[2]), (nets[1], nets[3]))):
                a = ('A', i, k); add(a, ('pol',)); edge(d, a, 'pol')
                edge(a, node(o), 'o'); edge(a, node(n), 'i')
            continue
        mos = re.search(r'_[np]mos', model); rc = re.match(r'(rhigh|rppd|rsil|cap_c|[RC] )', model)
        for j, n in enumerate(nets):
            edge(d, node(n), 'ds' if mos and j in (0, 2) else 'ab' if rc and j in (0, 1) else str(j))
    return G, subs[top][0], len(devs), missing, subs[top][1]


class Undecided(Exception):
    pass


def refine(G1, c1, G2, c2):
    """Joint colour refinement of both graphs; None as soon as the colour histograms differ."""
    while True:
        s1 = {n: (c, tuple(sorted((r, c1[m]) for m, r in G1['adj'][n].items()))) for n, c in c1.items()}
        s2 = {n: (c, tuple(sorted((r, c2[m]) for m, r in G2['adj'][n].items()))) for n, c in c2.items()}
        keys = {k: i for i, k in enumerate(sorted(set(s1.values()) | set(s2.values())))}
        n1 = {n: keys[s] for n, s in s1.items()}; n2 = {n: keys[s] for n, s in s2.items()}
        if Counter(n1.values()) != Counter(n2.values()): return None
        if len(keys) == len(set(c1.values()) | set(c2.values())): return n1, n2
        c1, c2 = n1, n2


def search(G1, c1, G2, c2, budget):
    r = refine(G1, c1, G2, c2)
    if r is None: return False
    c1, c2 = r
    cls1, cls2 = defaultdict(list), defaultdict(list)
    for n, c in c1.items(): cls1[c].append(n)
    for n, c in c2.items(): cls2[c].append(n)
    multi = [c for c, v in cls1.items() if len(v) > 1]
    if not multi:                       # discrete: the colours define the only candidate bijection
        m = {v[0]: cls2[c][0] for c, v in cls1.items()}
        return all({(m[u], r) for u, r in G1['adj'][v].items()} == set(G2['adj'][m[v]].items()) for v in m)
    k = min(multi, key=lambda c: (len(cls1[c]), c)); v = sorted(cls1[k])[0]; fresh = len(c1) + len(c2)
    for w in sorted(cls2[k]):           # individualise v against each candidate w, refine again
        budget[0] -= 1
        if budget[0] < 0: raise Undecided
        d1 = dict(c1); d1[v] = fresh; d2 = dict(c2); d2[w] = fresh
        if search(G1, d1, G2, d2, budget): return True
    return False


def isomorphic(G1, G2):
    if len(G1['lab']) != len(G2['lab']): return False
    labs = {l: i for i, l in enumerate(sorted({repr(x) for x in list(G1['lab'].values()) + list(G2['lab'].values())}))}
    return search(G1, {n: labs[repr(l)] for n, l in G1['lab'].items()},
                  G2, {n: labs[repr(l)] for n, l in G2['lab'].items()}, [20000])


def pins(path):
    s = open(path).read(); out = []
    for m in re.finditer(r'^B 5 ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) \{([^}]*)\}', s, re.M):
        a = dict(re.findall(r'(\w+)=(\S+)', m.group(5)))
        out.append((a.get('name'), (float(m.group(1)) + float(m.group(3))) / 2, (float(m.group(2)) + float(m.group(4))) / 2))
    return out


def same_file(a, b):
    try: return open(a, 'rb').read() == open(b, 'rb').read()
    except OSError: return False


def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    sys.setrecursionlimit(20000)
    old, new = sys.argv[1], sys.argv[2]
    sheets = sys.argv[3:] or sorted(os.path.relpath(p, new) for d in ('schematic/xschem', 'testbenches/xschem',
                                                                    'verification/cace/templates')
                                    for p in glob.glob(os.path.join(new, 'macros', '*', d, '*.sch'))
                                    if os.path.exists(os.path.join(old, os.path.relpath(p, new))))
    bad = 0
    print('symbols whose pins changed (every sheet that places them must be re-wired):')
    for s in sorted(glob.glob(os.path.join(new, 'macros', '*', 'schematic', 'xschem', '*.sym'))):
        o = os.path.join(old, os.path.relpath(s, new))
        if not os.path.exists(o): continue
        pa, pb = pins(o), pins(s)
        if pa == pb: continue
        da, db = {p[0]: p[1:] for p in pa}, {p[0]: p[1:] for p in pb}
        what = []
        if set(da) != set(db): what.append('renamed/added/removed: %s' % ' '.join(sorted(set(da) ^ set(db))))
        elif [p[0] for p in pa] != [p[0] for p in pb]: what.append('ORDER changed')
        moved = [k for k in da if k in db and da[k] != db[k]]
        if moved: what.append('moved: ' + ' '.join(moved))
        name = os.path.basename(s); users = []
        for u in glob.glob(os.path.join(new, '**', '*.sch'), recursive=True):
            if re.search(r'^C \{([^}]*/)?' + re.escape(name) + r'\}', open(u, errors='replace').read(), re.M):
                r = os.path.relpath(u, new)
                users.append(r + ('' if not same_file(os.path.join(old, r), u) else ' (not re-edited)'))
        print('  %s: %s\n    used in: %s' % (name, '; '.join(what), ', '.join(sorted(users)) or '-'))
    print('\nsheets:')
    for sh in sheets:
        with tempfile.TemporaryDirectory() as ta, tempfile.TemporaryDirectory() as tb:
            fa, fb = netlist(old, sh, ta), netlist(new, sh, tb)
            if not fa or not fb:
                bad += 1; print('  NO NETLIST  %s (%s)' % (sh, 'old' if not fa else 'new')); continue
            Ga, pa, na, ma, ia = graph(fa); Gb, pb, nb, mb, ib = graph(fb)
        note = []
        try: same = sorted(pa) == sorted(pb) and isomorphic(Ga, Gb)
        except Undecided: same = False; note.append('UNDECIDED (search budget exhausted)')
        if mb: note.append('%d MISSING symbol(s)' % mb)
        if sorted(pa) != sorted(pb): note.append('ports only old: %s, only new: %s' % (sorted(set(pa) - set(pb)), sorted(set(pb) - set(pa))))
        elif pa != pb: note.append('port order of the stand-alone netlist changed (parents use the .sym)')
        ok = same and not mb
        bad += not ok
        print('  %-10s %s  (%d devices)%s' % ('equivalent' if ok else 'DIFFERENT', sh, nb, ('  ' + '; '.join(note)) if note else ''))
        if not ok:
            A = {n: p for n, p, _ in ia}; B = {n: p for n, p, _ in ib}
            for n in sorted(set(A) | set(B)):
                if A.get(n) == B.get(n): continue
                if n not in A or n not in B: print('      %-8s only in %s' % (n, 'new' if n in B else 'old')); continue
                ch = ', '.join('%s->%s' % (x, y) for x, y in zip(A[n], B[n]) if x != y)
                print('      %-8s %-16s %s' % (n, B[n][-1], ch))
    print('\n%d of %d sheets differ' % (bad, len(sheets)))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
