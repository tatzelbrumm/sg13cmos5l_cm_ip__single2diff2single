#!/usr/bin/env python3
"""Lint an xschem sheet for the geometric joins that merge nets silently.

    python3 -I sch_lint.py [-v] [--lib DIR ...] SHEET.sch [SHEET.sch ...]

xschem joins every pin and every wire end that lies anywhere on a wire, at its ends or in its
interior, and joins all labels of the same name. A wire drawn along a row of pins therefore
connects all of them, and the netlist shows it only as renamed nets. This script rebuilds the
connectivity from the geometry, the way xschem does, and reports:

  SHORT    a connected group that carries two or more different label / port names; under it,
           every join (wire end or device pin touching a wire, or two points on one spot) whose
           removal separates the names, and every device pin of the group that lies inside a
           wire (the wire runs on through the pin instead of ending on it): the spots to look at.
  THROUGH  (with -v) the same "pin inside a wire" for groups without a short: legal, often
           harmless (a bulk tied to its source along the column), but the usual way a long wire
           picks up a pin it should only pass.
  CROSSING (with -v) wires that cross without a junction (no connection; listed for review).

Exit status 1 if any sheet has a SHORT, else 0. Pure Python 3 standard library.
Tested on the vcm_rb sheet of sg13cmos5l_cm_ip__single2diff2single: b4cd2288 (the m wire ran on
through BA's gate and bulk pins into BA's bulk jog) gives "SHORT ... bt, m", join at (1750,-690),
BA.G and BA.B inside the m wire; d0638017 (the fix) is clean.

Symbols are looked up in the sheet's folder, in each --lib DIR, in XSCHEM_LIBRARY_PATH, in
$PDK_ROOT/$PDK/libs.tech/xschem and in xschem's own xschem_library next to the xschem binary.
A symbol that is not found is reported and its pins are ignored.
"""
import os
import re
import shutil
import sys
from collections import defaultdict


def tf(px, py, rot, flip):
    if flip:
        px = -px
    return {0: (px, py), 1: (-py, px), 2: (-px, -py), 3: (py, -px)}[rot % 4]


def sym_pins(path, cache={}):
    if path in cache:
        return cache[path]
    s = open(path).read()
    k = re.search(r'^K \{(.*?)\n?\}\s*$', s, re.M | re.S)
    typ = re.search(r'\btype=(\S+)', k.group(1) if k else s)
    pins = []
    for m in re.finditer(r'^B 5 ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) ([-\d.e]+) \{([^}]*)\}', s, re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        name = re.search(r'name=(\S+)', m.group(5))
        pins.append((name.group(1) if name else '?', (x1 + x2) / 2, (y1 + y2) / 2))
    cache[path] = (typ.group(1) if typ else None, pins)
    return cache[path]


def lib_dirs(sheet, extra):
    d = [os.path.dirname(os.path.abspath(sheet))] + list(extra)
    d += [p for p in os.environ.get('XSCHEM_LIBRARY_PATH', '').split(':') if p]
    if os.environ.get('PDK_ROOT') and os.environ.get('PDK'):
        d.append(os.path.join(os.environ['PDK_ROOT'], os.environ['PDK'], 'libs.tech', 'xschem'))
    x = shutil.which('xschem')
    if x:
        d.append(os.path.join(os.path.dirname(os.path.realpath(x)), '..', 'share', 'xschem', 'xschem_library'))
    return d


def find_sym(ref, dirs):
    for d in dirs:
        p = os.path.join(d, ref)
        if os.path.isfile(p):
            return p
    return None


def parse(sheet, dirs):
    txt = open(sheet).read()
    wires, points, missing = [], [], []
    for m in re.finditer(r'^N ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) \{([^}]*)\}', txt, re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        lab = re.search(r'lab=(\S+)', m.group(5))
        wires.append((x1, y1, x2, y2, lab.group(1) if lab else ''))
    for m in re.finditer(r'^C \{([^}]*)\} ([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) \{(.*?)\}\s*$', txt, re.M | re.S):
        ref, x, y, rot, flip, props = m.group(1), float(m.group(2)), float(m.group(3)), int(float(m.group(4))), \
            int(float(m.group(5))), m.group(6)
        name = re.search(r'(?:^|\s)name=(\S+)', props)
        name = name.group(1) if name else '?'
        p = find_sym(ref, dirs)
        if not p:
            missing.append(ref)
            continue
        typ, pins = sym_pins(p)
        lab = re.search(r'(?:^|\s)lab=(\S+)', props)
        for (pn, px, py) in pins:
            dx, dy = tf(px, py, rot, flip)
            if typ in ('label', 'ipin', 'opin', 'iopin') and lab:
                points.append((x + dx, y + dy, 'label', name, lab.group(1)))
            else:
                points.append((x + dx, y + dy, 'pin', f'{name}.{pn}', None))
    return wires, points, sorted(set(missing))


def on(w, x, y, interior=False):
    x1, y1, x2, y2 = w[:4]
    if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
        return not interior or (y not in (y1, y2))
    if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
        return not interior or (x not in (x1, x2))
    return False


def contacts(wires, points):
    """every geometric join, as (a, b, kind, (x, y), what): element ids a, b (wires 0..W-1, points W..)"""
    W = len(wires)
    out = []
    for i, w in enumerate(wires):
        for j, v in enumerate(wires):
            if i == j:
                continue
            for (x, y) in ((w[0], w[1]), (w[2], w[3])):
                if on(v, x, y):
                    kind = 'interior' if on(v, x, y, True) else 'end'
                    out.append((i, j, kind, (x, y), f'wire end ({x:g},{y:g}) on wire {fmt(v)}'))
    for k, p in enumerate(points):
        for j, v in enumerate(wires):
            if on(v, p[0], p[1]):
                kind = 'interior' if on(v, p[0], p[1], True) else 'end'
                out.append((W + k, j, kind, (p[0], p[1]), f'{p[2]} {p[3]} at ({p[0]:g},{p[1]:g}) on wire {fmt(v)}'))
        for k2 in range(k + 1, len(points)):
            q = points[k2]
            if (p[0], p[1]) == (q[0], q[1]):
                out.append((W + k, W + k2, 'end', (p[0], p[1]), f'{p[3]} on {q[3]} at ({p[0]:g},{p[1]:g})'))
    return out


def fmt(w):
    return f'({w[0]:g},{w[1]:g})-({w[2]:g},{w[3]:g})'


def groups(n, cons, skip=None):
    par = list(range(n))

    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for c in cons:
        if c is not skip:
            par[f(c[0])] = f(c[1])
    return f


def lint(sheet, extra=(), verbose=False):
    dirs = lib_dirs(sheet, extra)
    wires, points, missing = parse(sheet, dirs)
    W, n = len(wires), len(wires) + len(points)
    cons = contacts(wires, points)
    f = groups(n, cons)
    names = defaultdict(set)
    for k, p in enumerate(points):
        if p[2] == 'label':
            names[f(W + k)].add(p[4])
    shorts = []
    label_ids = {W + k for k, p in enumerate(points) if p[2] == 'label'}
    for root, ns in names.items():
        if len(ns) < 2:
            continue
        culprits, seen = [], set()
        for c in cons:
            pair = frozenset((c[0], c[1]))
            if f(c[0]) != root or pair in seen or pair & label_ids:
                continue
            seen.add(pair)
            same = [d for d in cons if frozenset((d[0], d[1])) == pair]
            g = groups(n, [d for d in cons if frozenset((d[0], d[1])) != pair])
            side = defaultdict(set)
            for k, p in enumerate(points):
                if p[2] == 'label' and f(W + k) == root:
                    side[g(W + k)].add(p[4])
            if len(side) > 1:
                culprits.append((same[0][2], same[0][4], sorted(sorted(s) for s in side.values())))
        inside = [f'{p[3]} at ({p[0]:g},{p[1]:g}) lies inside wire {fmt(w)}'
                  for k, p in enumerate(points) if p[2] == 'pin' and f(W + k) == root
                  for w in wires if on(w, p[0], p[1], True)]
        shorts.append((sorted(ns), culprits, inside))
    through = []
    for k, p in enumerate(points):
        if p[2] != 'pin' or any(f(W + k) == names_root for names_root in
                                (r for r, ns in names.items() if len(ns) > 1)):
            continue
        for w in wires:
            if on(w, p[0], p[1], True):
                through.append(f'{p[3]} at ({p[0]:g},{p[1]:g}): wire {fmt(w)} runs through it')
    cross = []
    if verbose:
        for i, a in enumerate(wires):
            for b in wires[i + 1:]:
                if (a[0] == a[2]) != (b[0] == b[2]):
                    v, h = (a, b) if a[0] == a[2] else (b, a)
                    if min(v[1], v[3]) < h[1] < max(v[1], v[3]) and min(h[0], h[2]) < v[0] < max(h[0], h[2]):
                        cross.append(f'({v[0]:g},{h[1]:g})')
    print(f'{sheet}: {len(wires)} wires, {sum(1 for p in points if p[2] == "pin")} pins, '
          f'{sum(1 for p in points if p[2] == "label")} labels / ports')
    for m in missing:
        print(f'  MISSING symbol {m} (its pins are not checked)')
    for ns, culprits, inside in shorts:
        print(f'  SHORT  one connected group carries the names {", ".join(ns)}')
        for kind, what, sides in culprits:
            print(f'         join: {what} ({kind}); without it: {" | ".join(",".join(s) for s in sides)}')
        if not culprits:
            print('         (no single join separates them: several joins, or one label on two nets)')
        for t in inside:
            print(f'         pin {t}')
    if verbose:
        for t in through:
            print(f'  THROUGH {t}')
        print(f'  CROSSING {len(cross)} unconnected crossings: {" ".join(cross)}')
    if not shorts:
        print('  clean: no group carries two names' + ('' if verbose or not through else
                                                       f' ({len(through)} pin(s) inside a wire, see -v)'))
    return 1 if shorts else 0


if __name__ == '__main__':
    args, extra, verbose = sys.argv[1:], [], False
    if not args or args[0] in ('-h', '--help'):
        sys.exit(__doc__)
    sheets = []
    while args:
        a = args.pop(0)
        if a == '--lib':
            extra.append(args.pop(0))
        elif a == '-v':
            verbose = True
        else:
            sheets.append(a)
    sys.exit(max(lint(s, extra, verbose) for s in sheets))
