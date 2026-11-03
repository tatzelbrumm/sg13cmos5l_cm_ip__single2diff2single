#!/usr/bin/env python3
"""users_ba.py ROOT: re-wire every user of sg13cmos5l_IOPadDiff2Single.sym to the backannotated ports (agent BA, C2 2026-11-03).
The old pins ibias en_1v2 sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense leave the symbol; iref en_3v3 en_3v3_b take the
places of ibias en_1v2 sel0_1v2. Next to the pad an en_ctrl_3v3 and a bias_gen_pd instance get the nets the old pins had,
wired as in the former pad sheet (xc: vddh = iovdd, vddl = vdd, vss = iovss; xg: vdd = iovdd, vss = iovss)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sch import LP, T
R = sys.argv[1]
OLD = {'iovdd': (-40, -180), 'iovss': (-40, 180), 'vdd': (40, -180), 'ibias': (-220, -40), 'en_1v2': (-220, 0),
       'sel0_1v2': (-220, 20), 'sel1_1v2': (-220, 40), 'vdd1v2_sense': (-220, 80), 'vdd3v3_sense': (-220, 100)}
XC = {'vddh': (-60, -80, 0), 'vddl': (-40, -80, 1), 'vss': (-60, 80, 1), 'en_1v2': (-100, -40, 0), 'sel0_1v2': (-100, -20, 0),
      'sel1_1v2': (-100, 0, 0), 'vdd1v2_sense': (-100, 20, 0), 'vdd3v3_sense': (-100, 40, 0), 'en_3v3': (100, -40, 1),
      'en_3v3_b': (100, -20, 1), 'sel0_3v3': (100, 0, 1), 'sel1_3v3': (100, 20, 1)}
XG = {'vdd': (0, -80, 1), 'vss': (0, 80, 1), 'ibias': (-90, -30, 0), 'en_3v3': (-90, -10, 0), 'sel0_3v3': (-90, 10, 0),
      'sel1_3v3': (-90, 30, 0), 'iref': (90, 0, 1)}
LPRE = re.compile(r'^C \{devices/lab_pin\.sym\} (-?[\d.]+) (-?[\d.]+) 0 (\d) \{name=(\S+) sig_type=std_logic lab=([^ }]+)\}\n', re.M)


def edit(path, dut, cpos, gpos, pre, iname_c, iname_g, label_rails=False, note=None, extra=()):
    s = open(path).read()
    m = re.search(r'^C \{sg13cmos5l_IOPadDiff2Single\.sym\} (-?[\d.]+) (-?[\d.]+) 0 0 \{name=%s\}' % dut, s, re.M)
    X, Y = float(m.group(1)), float(m.group(2))
    labs = {(float(a.group(1)), float(a.group(2))): a for a in LPRE.finditer(s)}
    net = {}
    for p, (dx, dy) in OLD.items():
        a = labs.get((X + dx, Y + dy))
        net[p] = a.group(5) if a else None
    # remove the labels of the six old pins
    for p in ('ibias', 'en_1v2', 'sel0_1v2', 'sel1_1v2', 'vdd1v2_sense', 'vdd3v3_sense'):
        a = labs.get((X + OLD[p][0], Y + OLD[p][1]))
        if a: s = s.replace(a.group(0), '', 1)
    n = {k: pre + k for k in ('iref', 'en_3v3', 'en_3v3_b', 'sel0_3v3', 'sel1_3v3')}
    add = []
    if label_rails:                          # the top sheet: the pad's rail pins carried no net; name them for xc / xg
        for p in ('iovdd', 'vdd', 'iovss'):
            if net[p] is None:
                net[p] = pre + p; add.append(LP(X + OLD[p][0], Y + OLD[p][1], 'l_%s%s' % (pre, p), net[p], 1))
    add += [LP(X - 220, Y - 40, 'l_%siref' % pre, n['iref']), LP(X - 220, Y, 'l_%sen' % pre, n['en_3v3']),
            LP(X - 220, Y + 20, 'l_%senb' % pre, n['en_3v3_b'])]
    cnet = {'vddh': net['iovdd'], 'vddl': net['vdd'], 'vss': net['iovss'], 'en_1v2': net['en_1v2'], 'sel0_1v2': net['sel0_1v2'],
            'sel1_1v2': net['sel1_1v2'], 'vdd1v2_sense': net['vdd1v2_sense'], 'vdd3v3_sense': net['vdd3v3_sense'],
            'en_3v3': n['en_3v3'], 'en_3v3_b': n['en_3v3_b'], 'sel0_3v3': n['sel0_3v3'], 'sel1_3v3': n['sel1_3v3']}
    gnet = {'vdd': net['iovdd'], 'vss': net['iovss'], 'ibias': net['ibias'], 'en_3v3': n['en_3v3'], 'sel0_3v3': n['sel0_3v3'],
            'sel1_3v3': n['sel1_3v3'], 'iref': n['iref']}
    add.append('C {en_ctrl_3v3.sym} %g %g 0 0 {name=%s}' % (cpos[0], cpos[1], iname_c))
    for p, (dx, dy, f) in XC.items():
        if cnet[p]: add.append(LP(cpos[0] + dx, cpos[1] + dy, 'l_%s_%s' % (iname_c, p), cnet[p], f))
    add.append('C {bias_gen_pd.sym} %g %g 0 0 {name=%s}' % (gpos[0], gpos[1], iname_g))
    for p, (dx, dy, f) in XG.items():
        if gnet[p]: add.append(LP(gpos[0] + dx, gpos[1] + dy, 'l_%s_%s' % (iname_g, p), gnet[p], f))
    if note:
        add += [T(t, note[0], note[1] + 22 * i, 0.25) for i, t in enumerate(note[2])]
    for a, b in extra:
        assert s.count(a) == 1, (path, a); s = s.replace(a, b)
    open(path, 'w').write(s.rstrip('\n') + '\n' + '\n'.join(add) + '\n')
    print('%s: old pin nets %s' % (os.path.relpath(path, R), net))


NOTE = ['%s (en_ctrl_3v3) and %s (bias_gen_pd): outside the pad cell since 2026-11-03 (backannotation to the drawn cell),',
        'wired as in the former pad sheet; the sources that drove the old pad pins now drive them.']
tdir = os.path.join(R, 'macros/sg13cmos5l_IOPadDiff2Single/verification/cace/templates')
for t in ('ac', 'dc', 'drive', 'enable', 'noise', 'pd', 'thd', 'tran'):
    extra = [('let Ven3 = v(x1.en_3v3)', 'let Ven3 = v(en_3v3)')] if t == 'pd' else []
    edit(os.path.join(tdir, 'sg13cmos5l_IOPadDiff2Single_tb_%s.sch' % t), 'x1', (900, 420), (1300, 420), '', 'xc', 'xg',
         note=(780, 300, [NOTE[0] % ('xc', 'xg'), NOTE[1]]), extra=extra)
edit(os.path.join(R, 'macros/slot/schematic/xschem/slot.sch'), 'xd2s', (1300, 420), (1700, 420), 'd2s_', 'xd2s_c', 'xd2s_g',
     note=(1180, 300, [NOTE[0] % ('xd2s_c', 'xd2s_g'), NOTE[1]]))
edit(os.path.join(R, 'schematic/xschem/sg13cmos5l_cm_ip__single2diff2single.sch'), 'xoutbuf', (1100, 140), (1500, 140), 'outbuf_',
     'xoutbuf_c', 'xoutbuf_g', label_rails=True, note=(980, 20, [NOTE[0] % ('xoutbuf_c', 'xoutbuf_g'), NOTE[1]]))
