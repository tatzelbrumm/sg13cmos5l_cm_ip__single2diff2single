# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F (C3) stage B: reference netlist of the pad candidate, from the primitives' own CDLs (after C2 F2's compose_cdl.py).

    python3 compose_cdl.py <block_cfg.py> <out.cdl> <cells.cdl>...

s2d_block = s2d_mpdda_pd + bias_tree_noab_pd as placed (block_cfg.PLACE), every instance an X line whose ports
are mapped by name through the instance's net map, then vdd -> iovdd, vss -> iovss (the pad's buffer supplies). The
*_core cells (sinks placed without N's R90 wrapper) get N's wrapper netlists under their own names. Pad level: the
block and the protection as drawn in the template (s2d_pad_esd.sch, equal to the template's extraction device by
device): rppd RP / RN, the clamps MCP / MCN, two dpantenna / dantenna stripes each; vss is a port without devices
(the 1.2 V ring rail), as in IHP's IOPadAnalog."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[1])))
import block_cfg as B  # noqa: E402

OUT = sys.argv[2]
subs, order = {}, []
for f in sys.argv[3:]:
    cur = None
    for raw in open(f):
        line = raw.rstrip('\n')
        t = line.split()
        if not t or line.startswith('*'):
            continue
        if t[0].upper() == '.SUBCKT':
            cur = t[1]
            subs[cur] = (t[2:], [])
            order.append(cur)
        elif t[0].upper() == '.ENDS':
            cur = None
        elif cur is not None:
            if line.startswith('+'):
                subs[cur][1][-1] += ' ' + line[1:].strip()
            else:
                subs[cur][1].append(line)
ALIAS = {'sinks_6x6_s2d_c3_core': 'sinks_6x6_s2d_c3', 's2d_sinks_cmfb_c3_core': 's2d_sinks_cmfb_c3'}
SUP = {'vdd': 'iovdd', 'vss': 'iovss'}
PORTS = ['iovdd', 'iovss', 'pad', 'outp', 'outn', 'vcm', 'vref', 'iref', 'en_3v3', 'en_3v3_b']
need, blk = [], []
for inst, cell, o, x, y, nets in B.PLACE:
    if x is None:
        continue
    src = ALIAS.get(cell, cell)
    if cell in ALIAS and cell not in subs:
        subs[cell] = subs[src]
    pins = subs[cell][0]

    def net(p):
        n = nets.get(p, p)
        if n.startswith('iovdd_'):
            return 'iovdd'
        if n.startswith('iovss_'):
            return 'iovss'
        return SUP.get(n, n)
    blk.append('X%s %s %s' % (inst, ' '.join(net(p) for p in pins), cell))
    need.append(cell)
# the block's cells sit directly in the pad subckt: inside the layout's s2d_block the supply groups meet only on the
# template's Metal3 rails (pad level), so s2d_block is flattened by the comparison (no schematic counterpart)
PAD = """.SUBCKT sg13cmos5l_IOPadSingle2Diff iovdd iovss vdd vss pad outp outn vcm vref iref en_3v3 en_3v3_b
* s2d_block (s2d_mpdda_pd + bias_tree_noab_pd as placed)
%s
""" % '\n'.join(blk) + """* protection as drawn in the template (s2d_pad_esd.sch; template_extracted.cir)
RRP iovdd gp iovss rppd w=0.5u l=12.9u m=1 b=0
MMCP pad gp iovdd iovdd sg13_hv_pmos w=266.4u l=0.6u ng=40 m=1
RRN gn iovss iovss rppd w=0.5u l=3.54u m=1 b=0
MMCN pad gn iovss iovss sg13_hv_nmos w=88u l=0.6u ng=20 m=1
DDP1 pad iovdd dpantenna A=35.0028p P=58.08u m=1
DDP2 pad iovdd dpantenna A=35.0028p P=58.08u m=1
DDN1 iovss pad dantenna A=35.0028p P=58.08u m=1
DDN2 iovss pad dantenna A=35.0028p P=58.08u m=1
.ENDS sg13cmos5l_IOPadSingle2Diff"""


def deps(c, acc):
    for line in subs[c][1]:
        t = line.split()
        if t[0][0] in 'Xx':
            m = [w for w in t[1:] if '=' not in w][-1]
            if m in subs and m not in acc:
                deps(m, acc)
    if c not in acc:
        acc.append(c)
    return acc


acc = []
for c in need:
    deps(c, acc)
txt = ['* SPDX-FileCopyrightText: 2026 Christoph Maier', '* SPDX-License-Identifier: Apache-2.0',
       '* pad_candidate.cdl: reference netlist of pad_candidate.gds (F, C3 stage B, compose_cdl.py)', '']
for c in acc:
    pins, lines = subs[c]
    txt += ['.SUBCKT %s %s' % (c, ' '.join(pins))] + lines + ['.ENDS %s' % c, '']
txt += [PAD, '']
open(OUT, 'w').write('\n'.join(txt))
print('wrote', OUT, len(acc), 'cells')
