"""2026-10-28: backannotate the compact oa_core_pd layout (v2) into the subckt oa_core_pd of bias_ref_pd.spice, in place,
keeping the line order. usage: oa_ba.py <root>"""
import sys, os
p = os.path.join(sys.argv[1], 'macros/bias_tree_pd/netlist/source/bias_ref_pd.spice'); t = open(p).read()
i = t.index('.subckt oa_core_pd '); j = t.index('.ends oa_core_pd\n', i) + len('.ends oa_core_pd\n'); s = t[i:j]
chain = ''.join('XMS1_%d %s en_3v3_b %s vdd sg13_hv_pmos w=0.5u l=12.5u ng=1\n' % (k, 'ks' if k == 7 else 'ms1_%d' % (k + 1), 'vdd' if k == 0 else 'ms1_%d' % k) for k in range(8))
for a, b in (('XM11 vnc vnc vss vss sg13_hv_nmos w=90u l=1u ng=4\n', 'XM11 vnc vnc vss vss sg13_hv_nmos w=90u l=1u ng=9\n'),
             ('XM10 d10 vnc vres vss sg13_hv_nmos w=180u l=1u ng=8\n', 'XM10 d10 vnc vres vss sg13_hv_nmos w=180u l=1u ng=18\n'),
             ('XMS1 ks en_3v3_b vdd vdd sg13_hv_pmos w=0.5u l=100u ng=1\n', '* MS1 (0.5u / 100u) as drawn: 8 x 0.5u / 12.5u in series (compact layout v2, 2026-10-28)\n' + chain),
             ('.ends oa_core_pd\n', '* dummies of the compact layout v2 (2026-10-28): D = S = bulk, gates on vpg / vnc / vbr\n'
              'XMDUM0 vdd vpg vdd vdd sg13_hv_pmos w=4.4u l=8u ng=9\nXMDUM1 vss vnc vss vss sg13_hv_nmos w=36u l=1u ng=18\n'
              'XMDUM2 vss vbr vss vss sg13_hv_nmos w=4u l=1u ng=2\n.ends oa_core_pd\n')):
    assert s.count(a) == 1, a; s = s.replace(a, b)
open(p, 'w').write(t[:i] + s + t[j:]); print('oa_core_pd subckt backannotated')
