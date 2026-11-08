# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): bypass_rb as drawn in pad_ref_rb v2, for the LVS reference and the lead's backannotation.
    python3 bypass_spice.py <rb_place.py> <out.spice>
bypass_rb keeps its ports and parameters; its devices are the capacitor blocks of rb_place.CAPS plus the 9th vref
capacitor that sits in rb_cload (12u x 12u, the pad's CLN slot), all hv NMOS with S = D = B = vss."""
import sys

g = {}
exec(open(sys.argv[1]).read(), g)
area = {'vcm': 0.0, 'vref': 144.0}
lines = ['XCBR_cload vss vref vss vss sg13_hv_nmos w=12u l=12u ng=1 m=1']
for name, net, rows, cols, w, l, lab in g['CAPS']:
    n = rows * cols
    lines.append('X%s_%s vss %s vss vss sg13_hv_nmos w=%gu l=%gu ng=1 m=%d' % (lab, name, net, w, l, n))
    area[net] += n * w * l
with open(sys.argv[2], 'w') as f:
    f.write('* bypass_rb as drawn in pad_ref_rb v2 (bypass_spice.py, Claude, agent F, C4); gate area: vcm %.1f um2 '
            '(+ CB 144 in vcm_rb), vref %.1f um2\n' % (area['vcm'], area['vref']))
    f.write('.subckt bypass_rb vss vcm vref ncm=4 ncr=9\n%s\n.ends bypass_rb\n' % '\n'.join(lines))
print('bypass_rb gate area: vcm %.2f um2 (+ CB 144), vref %.2f um2' % (area['vcm'], area['vref']))
