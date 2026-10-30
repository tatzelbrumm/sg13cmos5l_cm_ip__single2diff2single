"""2026-10-28: backannotate the compact bg_core_pd layout into the subckt bg_core_pd of bias_ref_pd.spice, in place,
keeping the line order; resistor names and chain nets as the sheet netlists them (vector instances). usage: bg_ba.py <root>"""
import sys, os
p = os.path.join(sys.argv[1], 'macros/bias_tree_pd/netlist/source/bias_ref_pd.spice'); t = open(p).read()
i = t.index('.subckt bg_core_pd '); j = t.index('.ends bg_core_pd\n', i) + len('.ends bg_core_pd\n'); s = t[i:j]
def chain(name, n, a, b, net, note):
    nodes = [a] + ['%s[%d]' % (net, k) for k in range(n - 2, -1, -1)] + [b]
    return ('* %s\n' % note + ''.join('X%s[%d] %s %s vss rhigh w=0.5u l=9.94u\n' % (name, n - 1 - k, nodes[k], nodes[k + 1])
                                      for k in range(n)))
ms1 = ''.join('XMS1_%d %s en_3v3_b %s vdd sg13_hv_pmos w=0.5u l=12.5u ng=1\n' % (k, 'ks' if k == 7 else 'ms1_%d' % (k + 1), 'vdd' if k == 0 else 'ms1_%d' % k) for k in range(8))
for a, b in (('XNA g g ea vss sg13_hv_nmos w=20u l=4u ng=1\n', 'XNA g g ea vss sg13_hv_nmos w=20u l=4u ng=2\n'),
             ('XNB vpc g eb vss sg13_hv_nmos w=20u l=4u ng=1\n', 'XNB vpc g eb vss sg13_hv_nmos w=20u l=4u ng=2\n'),
             ('XR1A ea vss vss rhigh w=0.5u l=109.3u\n', chain('R1A', 11, 'ea', 'vss', 'n1a', 'R1A (0.5u / 109.3u) as drawn: 11 x 0.5u / 9.94u in series (compact layout, 2026-10-28)')),
             ('XR0 eb e2 vss rhigh w=0.5u l=179.5u\n', chain('R0', 18, 'eb', 'e2', 'n0', 'R0 (0.5u / 179.5u) as drawn: 18 x 0.5u / 9.94u in series')),
             ('XR1B eb vss vss rhigh w=0.5u l=99.36u\n', chain('R1B', 10, 'eb', 'vss', 'n1b', 'R1B (0.5u / 99.36u) as drawn: 10 x 0.5u / 9.94u in series')),
             ('XMS1 ks en_3v3_b vdd vdd sg13_hv_pmos w=0.5u l=100u ng=1\n', '* MS1 (0.5u / 100u) as drawn: 8 x 0.5u / 12.5u in series\n' + ms1),
             ('.ends bg_core_pd\n', '* dummies of the compact layout (2026-10-28): PMOS D = S = bulk = vdd on vpg / vpc; NMOS D = S = G = g; rhigh on vss\n'
              'XMDUM0 vdd vpg vdd vdd sg13_hv_pmos w=2.4u l=1u ng=8\nXMDUM1 vdd vpc vdd vdd sg13_hv_pmos w=2.4u l=1u ng=8\n'
              'XMDUM2 g g g vss sg13_hv_nmos w=2u l=1u ng=1\nXMDUM3 g g g vss sg13_hv_nmos w=16u l=4u ng=8\n'
              'XRDUM[1] vss vss vss rhigh w=0.5u l=9.94u\nXRDUM[0] vss vss vss rhigh w=0.5u l=9.94u\n.ends bg_core_pd\n')):
    assert s.count(a) == 1, a; s = s.replace(a, b)
open(p, 'w').write(t[:i] + s + t[j:]); print('bg_core_pd subckt backannotated')
