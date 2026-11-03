#!/usr/bin/env python3
"""intended_equiv.py OLD_ROOT NEW_ROOT SHEET ... (agent BA, C2 2026-11-03)

Shows that a sheet differs from its old version ONLY by the intended backannotation: each sheet is netlisted in both
roots (scripts/xschem/sheet_equiv.py's netlist / parse / graph / isomorphic, unchanged), the NEW flat netlist is
reverted by exactly the intended changes, and the result must be isomorphic to the OLD one (ports anchored by name).
Reverted (and counted), by hierarchical instance name and the subckt it sits in:
  unit_r2:        R[3..0] (4 x 0.5u / 12.65u, sa n1 n2 n3 sb) -> one R 0.5u / 50.6u sa sb
  d2s_mpdda_pd:   dummies MD* / RD[*] removed; SX / SY ng 6 -> 4; SA bulk vdd -> its source (vddo), SB bulk vss -> vsso
  sg13cmos5l_IOPadDiff2Single: MDBP / MDBN removed; each d2s_sp2k: R0 shorted (pa / pb merge into pad), D0 / D1 removed
Hierarchy is flattened, so en_ctrl_3v3 / bias_gen_pd moving from inside the pad to beside it is no difference."""
import os, re, sys, tempfile
from collections import Counter
sys.path.insert(0, os.path.join(sys.argv[2], 'scripts', 'xschem'))
import sheet_equiv as se


class Net:
    pass


def flat(subs, cell, nmap, path, parent, out):
    loc = {}
    def net(n):
        if n in nmap: return nmap[n]
        if n.endswith('!') or n in ('0', 'GND'): return n
        return loc.setdefault(n, Net())
    for name, pos, par in subs[cell][1]:
        typ = name[0].upper()
        if typ == 'X' and pos[-1] in subs:
            flat(subs, pos[-1], {p: net(n) for p, n in zip(subs[pos[-1]][0], pos[:-1])}, path + name + '.', pos[-1], out)
            continue
        if typ in 'XM': model, nets = pos[-1], pos[:-1]
        elif typ in 'EG' and len(pos) >= 5: model, nets = typ + ' ' + ' '.join(pos[4:]), pos[:4]
        else: model, nets = typ + ' ' + ' '.join(pos[2:]), pos[:2]
        out.append(dict(name=name, path=path, parent=parent, model=model, par=dict(par), nets=[net(n) for n in nets]))


def revert(devs):
    cnt = Counter(); parent = {}
    def find(n):
        while n in parent: n = parent[n]
        return n
    keep, chains = [], {}
    for d in devs:
        nm, pa = d['name'], d['parent']
        if pa == 'unit_r2' and re.fullmatch(r'XR\[[0-3]\]', nm):
            chains.setdefault(d['path'], {})[int(nm[3])] = d; continue
        if pa == 'd2s_mpdda_pd':
            if nm.startswith('XMD') or nm.startswith('XRD['): cnt['d2s dummy removed'] += 1; continue
            if nm in ('XSX', 'XSY'): assert d['par']['ng'] == '6'; d['par']['ng'] = '4'; cnt['SX/SY ng 6 -> 4'] += 1
            if nm in ('XSA', 'XSB'): d['nets'][3] = d['nets'][2]; cnt['SA/SB bulk -> source'] += 1
        if pa == 'sg13cmos5l_IOPadDiff2Single' and nm in ('XMDBP', 'XMDBN'): cnt['bias-tree dummy removed'] += 1; continue
        if pa == 'd2s_sp2k':
            if nm == 'XR0':
                a, b = find(d['nets'][0]), find(d['nets'][1])
                if a is not b: parent[b if not isinstance(b, str) else a] = a if not isinstance(b, str) else b
                cnt['sp2k R0 shorted'] += 1; continue
            cnt['sp2k diode removed'] += 1; continue
        keep.append(d)
    for path, ch in chains.items():
        assert sorted(ch) == [0, 1, 2, 3] and all(c['par']['l'] == '1.265e-05' for c in ch.values()), path
        assert ch[3]['nets'][1] is ch[2]['nets'][0] and ch[2]['nets'][1] is ch[1]['nets'][0] and ch[1]['nets'][1] is ch[0]['nets'][0]
        d = dict(ch[3]); d['name'] = 'XR'; d['par'] = dict(ch[3]['par'], l='5.06e-05'); d['nets'] = [ch[3]['nets'][0], ch[0]['nets'][1], ch[3]['nets'][2]]
        keep.append(d); cnt['unit_r2 chain -> one R'] += 1
    for d in keep:
        d['nets'] = [find(n) for n in d['nets']]
    return keep, cnt


def graph_of(devs):
    G = {'lab': {}, 'adj': {}}; nid = {}
    def add(n, lab): G['lab'][n] = lab; G['adj'].setdefault(n, {})
    def node(n):
        key = n if isinstance(n, str) else id(n)
        if key not in nid: nid[key] = ('N', len(nid)); add(nid[key], ('net', n if isinstance(n, str) else ''))
        return nid[key]
    def edge(a, b, role):
        r = tuple(sorted(G['adj'][a].get(b, ()) + (role,))); G['adj'][a][b] = r; G['adj'][b][a] = r
    for i, d in enumerate(devs):
        model, par, nets = d['model'], tuple(sorted(d['par'].items())), d['nets']
        v = ('D', i); add(v, ('dev', model, par))
        if model[:2] in ('E ', 'G ') and len(nets) == 4:
            for k, (o, n) in enumerate(((nets[0], nets[2]), (nets[1], nets[3]))):
                a = ('A', i, k); add(a, ('pol',)); edge(v, a, 'pol'); edge(a, node(o), 'o'); edge(a, node(n), 'i')
            continue
        mos = re.search(r'_[np]mos', model); rc = re.match(r'(rhigh|rppd|rsil|cap_c|[RC] )', model)
        for j, n in enumerate(nets):
            edge(v, node(n), 'ds' if mos and j in (0, 2) else 'ab' if rc and j in (0, 1) else str(j))
    return G


def main():
    sys.setrecursionlimit(20000)
    old, new, sheets = sys.argv[1], sys.argv[2], sys.argv[3:]
    bad = 0
    for sh in sheets:
        with tempfile.TemporaryDirectory() as ta, tempfile.TemporaryDirectory() as tb:
            fa, fb = se.netlist(old, sh, ta), se.netlist(new, sh, tb)
            if not fa or not fb: print('  NO NETLIST %s' % sh); bad += 1; continue
            (sa, ta_, ma), (sb, tb_, mb) = se.parse(fa), se.parse(fb)
        da, db = [], []
        flat(sa, ta_, {p: 'PORT:' + p for p in sa[ta_][0]}, '', ta_, da)
        flat(sb, tb_, {p: 'PORT:' + p for p in sb[tb_][0]}, '', tb_, db)
        rb, cnt = revert(db)
        ports_ok = sorted(sa[ta_][0]) == sorted(sb[tb_][0])
        try: same = ports_ok and se.isomorphic(graph_of(da), graph_of(rb))
        except se.Undecided: same = False
        bad += not same
        print('  %-10s %s  (old %d devices, new %d, reverted %d; missing symbols old %d new %d)%s\n      reverted: %s' % (
            'equivalent' if same else 'DIFFERENT', sh, len(da), len(db), len(rb), ma, mb,
            '' if ports_ok else '  ports old %s new %s' % (sa[ta_][0], sb[tb_][0]),
            ', '.join('%s %d' % kv for kv in sorted(cnt.items())) or '-'))
    print('%d of %d sheets differ after reverting the intended changes' % (bad, len(sheets)))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
