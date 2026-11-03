# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Lead check (C3): the non-dummy devices of an agent's CDL against the s2d circuit (s2d_mpdda / s2d_mpdda_pd /
bias_tree_noab_pd / bias_diodes), per cell. python3 circuit_check.py <cells.cdl> <P|N> [<extracted.cir> ...]
Devices are compared as (model, {D, S}, G, B, L) -> total W; dummies (D = S, not a device the circuit has, e.g. not
the MOS capacitors) are counted separately."""
import collections, re, sys
U = lambda s: float(re.sub(r'u$', '', s))
def cdl(path):
    cells, cur = {}, None
    for l in open(path).read().replace('\n+', ' ').splitlines():
        t = l.split()
        if not t: continue
        if t[0].upper() == '.SUBCKT': cur = t[1]; cells[cur] = []; continue
        if t[0].upper() == '.ENDS': cur = None; continue
        if cur and t[0][0] in 'MXRmxr': cells[cur].append(t)
    return cells
def key(t, subs):
    p = dict(x.lower().split('=', 1) for x in t if '=' in x); pos = [x for x in t[1:] if '=' not in x]
    model, nets = pos[-1], pos[:-1]
    if model in subs:                                   # a tub instance: d g s, device = 2 x 10/1, bulk = s
        d, g, s = nets; return ('sg13_hv_pmos', tuple(sorted((d, s))), g, s, 1.0), 20.0 * float(p.get('m', 1))
    if model == 'rhigh':
        return ('rhigh', tuple(sorted(nets[:2])), nets[2], '', U(p['l'])), U(p['w']) * float(p.get('m', 1))
    d, g, s, b = nets
    return (model, tuple(sorted((d, s))), g, b, U(p['l'])), U(p['w']) * float(p.get('m', 1)) * (1 if 'ng' not in p else 1)
EXP = {  # cell: list of (model, D, G, S, B, W, L) from the circuit
 'P': {
  's2d_inputs_c3': [('sg13_hv_pmos', d, g, s, s, 20, 1) for u, gp, gn, xd, yd in
      [('A1', 'vin', 'vref', 'x', 'y'), ('A2', 'vin', 'vref', 'x', 'y'), ('F1', 'vcm', 'vfbp', 'x', 'y'), ('F2', 'vfbn', 'vcm', 'x', 'y'),
       ('M1', 'vfbp', 'vcm', 'xc', 'yc'), ('M2', 'vfbn', 'vcm', 'xc', 'yc')]
      for d, g, s in ((yd, gp, f'sa_{u}'), (xd, gn, f'sb_{u}'))],
  's2d_tails_c3': [('sg13_hv_pmos', f's{h}_{u}', 'vbp', 'vdd', 'vdd', 5, 6) for u in ('A1', 'A2', 'F1', 'F2', 'M1', 'M2') for h in 'ab']
      + [('sg13_hv_pmos', 'vbp', 'vbp', 'vdd', 'vdd', 5, 6)],
  's2d_loads_c3': [('sg13_hv_pmos', n, 'vcmfb', 'vdd', 'vdd', 24, 4) for n in ('lp', 'ln', 'dd')],
  's2d_casc_p_c3': [('sg13_hv_pmos', d, 'vbpc', s, 'vdd', 30, 3) for d, s in (('voutp', 'lp'), ('voutn', 'ln'), ('vcmfb', 'dd'))]
      + [('sg13_hv_pmos', 'vbpc', 'vbpc', 'vdd', 'vdd', 1, 4)],
  's2d_pd_p_c3': [('sg13_hv_pmos', o, 'en_3v3', 'vcm', 'vdd', 1, 0.45) for o in ('voutp', 'voutn')],
  'bias_tree_noab_p_c3': [('sg13_hv_pmos', 'vbn', 'vbp', 'vdd', 'vdd', 5, 6), ('sg13_hv_pmos', 'vbnc', 'vbp', 'vdd', 'vdd', 2, 6),
      ('sg13_hv_pmos', 'iref', 'en_3v3_b', 'ni', 'vdd', 1, 0.45)]},
 'N': {
  'sinks_6x6_s2d_c3': [('sg13_hv_nmos', n, 'vbn', 'vss', 'vss', 36, 6) for n in ('x', 'y')] + [('sg13_hv_nmos', 'vbn', 'vbn', 'vss', 'vss', 6, 6)],
  's2d_sinks_cmfb_c3': [('sg13_hv_nmos', n, 'vbn', 'vss', 'vss', 24, 6) for n in ('xc', 'yc')],
  's2d_casc_n_c3': [('sg13_hv_nmos', d, 'vbnc', s, 'vss', 30, 3) for d, s in (('voutp', 'x'), ('voutn', 'y'), ('vcmfb', 'xc'), ('vdd', 'yc'))]
      + [('sg13_hv_nmos', 'vbnc', 'vbnc', 'vss', 'vss', 1, 8)],
  's2d_pd_n_c3': [('sg13_hv_nmos', o, 'en_3v3_b', 'vcm', 'vss', 1, 0.45) for o in ('voutp', 'voutn')],  # tapless: bulk an internal net named vss
  's2d_cload_c3': [('sg13_hv_nmos', 'vss', g, 'vss', 'vss', 12, 12) for g in ('voutp', 'voutn')]
      + [('sg13_hv_nmos', o, 'en_3v3_b', 'vcm', 'vss', 1, 0.45) for o in ('voutp', 'voutn')],   # N put TPN / TNN inside
  's2d_rhigh_c3': [('rhigh', f'sa_{u}', 'vss', f'sb_{u}', '', 0.5, 50.6) for u in ('A1', 'A2', 'F1', 'F2', 'M1', 'M2')],
  'bias_tree_noab_n_c3': [('sg13_hv_nmos', 'ni', 'ni', 'vss', 'vss', 6, 6), ('sg13_hv_nmos', 'vbp', 'ni', 'vss', 'vss', 6, 6),
      ('sg13_hv_nmos', 'vbpc', 'ni', 'vss', 'vss', 2.4, 6), ('sg13_hv_nmos', 'iref', 'en_3v3', 'ni', 'vss', 1, 0.45),
      ('sg13_hv_nmos', 'ni', 'en_3v3_b', 'vss', 'vss', 1, 0.45)]}}
cells = cdl(sys.argv[1]); exp = dict(EXP[sys.argv[2]])
for extra in sys.argv[3:]:                    # extracted netlists (e.g. rhigh, whose series chains LVS reduces)
    cells.update(cdl(extra))
if sys.argv[2] == 'N':
    exp['sinks_6x6_s2d_c3_core'] = exp['sinks_6x6_s2d_c3']; exp['s2d_sinks_cmfb_c3_core'] = exp['s2d_sinks_cmfb_c3']
subs = {c for c in cells if c.startswith('tub_p20x1')}
ok_all = True
for cell, devs in exp.items():
    if cell not in cells: print(f'{cell}: MISSING in the CDL'); ok_all = False; continue
    want = collections.Counter()
    for m, d, g, s, b, w, l in devs: want[(m, tuple(sorted((d, s))), g, b, float(l))] += w
    got, dummies = collections.Counter(), collections.Counter()
    for t in cells[cell]:
        k, w = key(t, subs)
        if k[1][0] == k[1][1] and k not in want: dummies[(k[0], k[4])] += 1; continue   # D = S (or R ends equal): dummy
        got[k] += w
    ok = {k: round(v, 3) for k, v in got.items()} == {k: round(v, 3) for k, v in want.items()}
    ok_all &= ok
    print(f'{cell}: {"equal to the circuit" if ok else "DIFFERENT"}; dummies {dict(dummies)}')
    if not ok:
        for k in sorted(set(got) | set(want), key=str):
            if round(got[k], 3) != round(want[k], 3): print(f'    {k}: layout W {got[k]:g}, circuit W {want[k]:g}')
sys.exit(0 if ok_all else 1)
