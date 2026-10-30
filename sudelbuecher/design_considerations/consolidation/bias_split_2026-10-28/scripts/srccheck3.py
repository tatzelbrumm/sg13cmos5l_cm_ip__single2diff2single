import sys, os, re
sys.path.insert(0, os.path.dirname(__file__)); from flatten import parse, flat; from wl import compare
R, NW = sys.argv[1], sys.argv[2]
BT='bias_tree_pd/netlist/source/bias_ref_pd.spice'; HV='hv_logic/netlist/source/hv_logic.spice'; D='sg13cmos5l_IOPadDiff2Single/netlist/source/'
CASES0 = [('bias_tree_pd',[BT]), ('bias_tree_noab_pd',[BT,'bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice']),
  ('bias_sel_pd',[BT,HV,'bias_sel_pd/netlist/source/bias_sel_pd.spice']),
  ('bias_sel_noab_pd',[BT,HV,'bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice','bias_sel_noab_pd/netlist/source/bias_sel_noab_pd.spice']),
  ('d2s_mpdda_pd',[D+'units.spice',D+'d2s_mpdda_pd.spice']),
  ('bias_in_pd',[BT]), ('bias_out_pd',[BT]), ('bias_oa_pd',[BT]), ('bias_bg_pd',[BT]),
  ('d2s_out_p',[D+'d2s_out.spice']), ('d2s_out_n',[D+'d2s_out.spice']),
  ('sg13cmos5l_IOPadDiff2Single',[D+'units.spice',D+'d2s_mpdda_pd.spice',D+'d2s_out.spice',BT,HV,'ls_up_1v2_3v3/netlist/source/ls_up_1v2_3v3.spice','en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice','bias_sel_pd/netlist/source/bias_sel_pd.spice',D+'sg13cmos5l_IOPadDiff2Single.spice'])]
G='bias_gen_pd/netlist/source/bias_gen_pd.spice'; LS='ls_up_1v2_3v3/netlist/source/ls_up_1v2_3v3.spice'; EC='en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice'
S='sg13cmos5l_IOPadSingle2Diff/netlist/source/'
CASES = [('sg13cmos5l_IOPadDiff2Single',[D+'units.spice',D+'d2s_mpdda_pd.spice',D+'d2s_out.spice',BT,HV,LS,EC,G,D+'sg13cmos5l_IOPadDiff2Single.spice']),
         ('sg13cmos5l_IOPadSingle2Diff',[D+'units.spice',BT,HV,LS,EC,G,'bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice',S+'s2d_mpdda.spice',S+'s2d_pd.spice',S+'sg13cmos5l_IOPadSingle2Diff.spice'])]
for cell, srcs in CASES:
    if not all(os.path.exists(os.path.join(R, 'macros', f)) for f in srcs): continue
    mac = cell
    net = os.path.join(NW, 'macros_%s_schematic_xschem_%s.spice' % (mac, cell))
    ss, _ = parse([os.path.join(R, 'macros', f) for f in srcs]); ports = ss[cell.lower()][0]
    ds = [('top.' + d[0],) + d[1:] for d in flat(ss, ['xtop ' + ' '.join(ports) + ' ' + cell.lower()])]
    sn, tn = parse([net]); dn = flat(sn, tn)
    L = lambda dd: [d[:3] + (tuple(x.replace('w={10e-6*lcas}', 'w=30u').replace('l={1e-6*lcas}', 'l=3u') for x in d[3]),) for d in dd]
    ds, dn = L(ds), L(dn)
    npnp = sum(1 for d in ds if d[1] == 'pnpmpa')
    ds = [d for d in ds if d[1] != 'pnpmpa']; dn = [d for d in dn if d[1] != '?']
    ob, ow = compare(ds, dn)
    sym = open(os.path.join(R, 'macros', mac, 'schematic/xschem', cell + '.sym')).read()
    pins = re.findall(r'name=(\S+) dir=', sym)
    print('%s %-18s source %3d sheet %3d devices; symbol pins == source ports: %s' % ('SAME' if not ob and not ow else 'DIFF', cell, len(ds), len(dn), pins == ports))
    for d in ob[:6]: print('   - source', d[0], d[1], ' '.join(d[2]), ' '.join(d[3]))
    for d in ow[:6]: print('   + sheet ', d[0], d[1], ' '.join(d[2]), ' '.join(d[3]))
