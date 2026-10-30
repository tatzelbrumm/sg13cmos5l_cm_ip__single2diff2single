"""2026-10-28 bias split: source netlists, tb decks, xschemrc dependency lists. usage: srcsplit.py <root>"""
import sys, os
M = os.path.join(sys.argv[1], 'macros')
def edit(rel, pairs):
    p = os.path.join(M, rel); t = open(p).read()
    for a, b in pairs:
        assert t.count(a) == 1, (rel, a, t.count(a)); t = t.replace(a, b)
    open(p, 'w').write(t)
D, S = 'sg13cmos5l_IOPadDiff2Single', 'sg13cmos5l_IOPadSingle2Diff'
edit(D + '/netlist/source/sg13cmos5l_IOPadDiff2Single.spice', [
    ('* pad = s7_an[1] (the harness IOPadAnalog pad).\n',
     '* pad = s7_an[1] (the harness IOPadAnalog pad).\n'
     '* Bias since 2026-10-28: Xg = bias_gen_pd selects the reference (iref, sourced), Xt = bias_tree_pd makes the six\n'
     '* bias lines from it; together the former Xb = bias_sel_pd, device for device (bias_sel_pd = bias_gen_pd + its tree).\n'),
    ('Xb iovdd iovss ibias vbp vbn vbpc vbnc vabp vabn en_3v3 sel0_3v3 sel1_3v3 en_3v3_b bias_sel_pd\n',
     'Xg iovdd iovss ibias iref en_3v3 sel0_3v3 sel1_3v3 bias_gen_pd\n'
     'Xt iovdd iovss iref vbp vbn vbpc vbnc vabp vabn en_3v3 en_3v3_b bias_tree_pd\n')])
edit(S + '/netlist/source/sg13cmos5l_IOPadSingle2Diff.spice', [
    ('* six bias lines (vbp vbn vbpc vbnc, same diodes at the same currents as the driver), so its bias is\n'
     '* bias_sel_noab_pd, bias_sel_pd without the class-AB branches (2026-10-27).\n',
     '* six bias lines (vbp vbn vbpc vbnc, same diodes at the same currents as the driver), so its tree is\n'
     '* bias_tree_noab_pd, bias_tree_pd without the class-AB branches (2026-10-27). Since 2026-10-28 the reference\n'
     '* selector Xg = bias_gen_pd and the tree Xt are separate instances (before: one Xb = bias_sel_noab_pd, the same devices).\n'),
    ('Xb iovdd iovss ibias vbp vbn vbpc vbnc en_3v3 sel0_3v3 sel1_3v3 en_3v3_b bias_sel_noab_pd\n',
     'Xg iovdd iovss ibias iref en_3v3 sel0_3v3 sel1_3v3 bias_gen_pd\n'
     'Xt iovdd iovss iref vbp vbn vbpc vbnc en_3v3 en_3v3_b bias_tree_noab_pd\n')])
edit(D + '/testbenches/spice/tb_pad_dc.spice', [
    ('.include ../../../bias_sel_pd/netlist/source/bias_sel_pd.spice\n', '.include ../../../bias_gen_pd/netlist/source/bias_gen_pd.spice\n')])
edit(S + '/testbenches/spice/tb_pad_dc.spice', [
    ('.include ../../../bias_sel_noab_pd/netlist/source/bias_sel_noab_pd.spice\n', '.include ../../../bias_gen_pd/netlist/source/bias_gen_pd.spice\n')])
for rel in (D + '/schematic/xschem/xschemrc', D + '/testbenches/xschem/xschemrc', S + '/schematic/xschem/xschemrc',
            S + '/testbenches/xschem/xschemrc', 'slot/schematic/xschem/xschemrc'):
    edit(rel, [(' bias_sel_pd ls_up_1v2_3v3 ', ' bias_sel_pd bias_gen_pd ls_up_1v2_3v3 ')])
print('src ok')
