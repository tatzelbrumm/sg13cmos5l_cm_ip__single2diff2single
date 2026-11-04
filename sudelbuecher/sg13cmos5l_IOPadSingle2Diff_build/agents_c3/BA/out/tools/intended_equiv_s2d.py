#!/usr/bin/env python3
"""intended_equiv_s2d.py OLD_ROOT NEW_ROOT SHEET ... (agent BA, C3 2026-11-04; C2's intended_equiv.py with the s2d revert)

Shows that a sheet differs from its old version ONLY by the intended backannotation: each sheet is netlisted in both
roots (scripts/xschem/sheet_equiv.py's netlist / parse / graph / isomorphic, unchanged), the NEW flat netlist is
reverted by exactly the intended changes, and the result must be isomorphic to the OLD one (ports anchored by name).
Reverted (and counted), by hierarchical instance name and the subckt it sits in:
  s2d_mpdda_pd:      dummies XMD* / XRD[*] removed          s2d_mpdda: dummies XMDL[*] removed
  bias_tree_noab_pd: XMDBP / XMDBN removed                  sg13cmos5l_IOPadSingle2Diff: Rsub removed
  s2d_pad_esd (xp):  its 8 devices removed; in their place the old IHP cells XCP / XCN / XDN / XDP / XSP are put back
                     with the old pin order, on the pad / iovdd / iovss nets of that pad instance, and a new net padres
                     (XSP's core side) replaces the pad net at every device inside that pad's xa (the buffer's vin).
Hierarchy is flattened, so en_ctrl_3v3 / bias_gen_pd moving from inside the pad to beside it is no difference.
The unit_r2 chains are not reverted: the old tree already has C2's 4-segment unit_r2."""
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
    cnt = Counter(); keep = []; esd = {}
    for d in devs:
        nm, pa = d['name'], d['parent']
        if pa == 's2d_mpdda_pd' and (nm.startswith('XMD') or nm.startswith('XRD[')): cnt['s2d_mpdda_pd dummy removed'] += 1; continue
        if pa == 's2d_mpdda' and nm.startswith('XMDL['): cnt['s2d_mpdda load dummy removed'] += 1; continue
        if pa == 'bias_tree_noab_pd' and nm in ('XMDBP', 'XMDBN'): cnt['tree dummy removed'] += 1; continue
        if pa == 'sg13cmos5l_IOPadSingle2Diff' and nm == 'Rsub': cnt['Rsub removed'] += 1; continue
        if pa == 's2d_pad_esd':
            esd.setdefault(d['path'], {})[nm] = d; cnt['s2d_pad_esd device removed'] += 1; continue
        keep.append(d)
    for path, e in esd.items():
        assert sorted(e) == ['XDN1', 'XDN2', 'XDP1', 'XDP2', 'XMCN', 'XMCP', 'XRN', 'XRP'], (path, sorted(e))
        pad, iovdd, iovss = e['XMCP']['nets'][0], e['XMCP']['nets'][2], e['XMCN']['nets'][2]
        assert e['XMCN']['nets'][0] is pad and e['XRP']['nets'][0] is iovdd and e['XRN']['nets'][1] is iovss
        top = path[:-len('xp.')]
        padres = Net()
        for d in keep:
            if d['path'].startswith(top + 'xa.'):
                d['nets'] = [padres if n is pad else n for n in d['nets']]
        for nm, model, nets in (('XCP', 'sg13cmos5l_Clamp_P20N0D', (iovdd, iovss, pad)), ('XCN', 'sg13cmos5l_Clamp_N20N0D', (iovss, pad)),
                                ('XDN', 'sg13cmos5l_DCNDiode', (iovss, pad, iovdd)), ('XDP', 'sg13cmos5l_DCPDiode', (pad, iovdd, iovss)),
                                ('XSP', 'sg13cmos5l_SecondaryProtection', (padres, iovss, pad, iovdd))):
            keep.append(dict(name=nm, path=top, parent='sg13cmos5l_IOPadSingle2Diff', model=model, par={}, nets=list(nets)))
            cnt['IHP cell put back'] += 1
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
