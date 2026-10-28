"""2026-10-28: backannotate the compact oa_core_pd layout (v2) into oa_core_pd.sch, drawn in the sheet's own style:
M10 ng 8 -> 18, M11 ng 4 -> 9; MS1 as the drawn chain of 8 x 0.5u/12.5u (new box [S1] right of [R]);
the three dummies (box [D]). usage: oa_sheet_ba.py <root>"""
import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/tools')
from schedit import Sheet, name_of, kind
R = sys.argv[1]; p = os.path.join(R, 'macros/oa_core_pd/schematic/xschem/oa_core_pd.sch')
s = Sheet(p)
def set_ng(name, old, new):
    i = s.find_inst(name); t = ''.join(s.items[i]); assert t.count('ng=%d\n' % old) == 1, name
    from schedit import parse
    s.items[i:i + 1] = parse(t.replace('ng=%d\n' % old, 'ng=%d\n' % new))
set_ng('M10', 8, 18); set_ng('M11', 4, 9)
# MS1 out of [S]: the device, its rail / bulk / gate wires, the unused top of the en_3v3_b bus; ks keeps a labelled stub
s.del_inst('MS1', 'l1')
s.del_wire((220, -1000, 220, -950), (220, -920, 240, -920), (240, -1000, 240, -920), (140, -920, 180, -920),
           (220, -890, 220, -560), (140, -920, 140, -580))
W = lambda x1, y1, x2, y2, lab: 'N %g %g %g %g {lab=%s}' % (x1, y1, x2, y2, lab)
LP = lambda x, y, n, lab, f=0: 'C {devices/lab_pin.sym} %g %g 0 %d {name=%s sig_type=std_logic lab=%s}' % (x, y, f, n, lab)
def dev(kind_, name, x, y, w, l, ng):
    return ('C {sg13cmos5l_pr/sg13_hv_%s.sym} %g %g 0 0 {name=%s\nl=%s\nw=%s\nng=%d\nm=1\nmm_ok=1\nmodel=sg13_hv_%s\nspiceprefix=X}'
            % (kind_, x, y, name, l, w, ng, kind_))
add = [W(220, -620, 220, -560, 'ks'), 'C {devices/lab_wire.sym} 220 -620 0 0 {name=l1 sig_type=std_logic lab=ks}',
       'T {MS1 (0.5u / 100u) is drawn as} 126 -870 0 0 0.2 0.2 {}', 'T {8 x 0.5u / 12.5u in series: [S1]} 126 -852 0 0 0.2 0.2 {}']
# [S1]: the chain, vdd -> ms1_1 ... ms1_7 -> ks, gates en_3v3_b, bulks vdd
X, Y0, P = 1140, -960, 80
ys = [Y0 + P * k for k in range(8)]
for k, y in enumerate(ys):
    add.append(dev('pmos', 'MS1_%d' % k, X, y, '0.5u', '12.5u', 1))
    add += [W(X - 40, y, X - 20, y, 'en_3v3_b'), W(X + 20, y, X + 40, y, 'vdd')]
    if k < 7: add.append(W(X + 20, y + 30, X + 20, ys[k + 1] - 30, 'ms1_%d' % (k + 1)))
add += [W(X - 40, ys[0], X - 40, ys[-1], 'en_3v3_b'), LP(X - 40, ys[0], 'l_s1_g', 'en_3v3_b'),
        W(X + 20, ys[0] - 30, X + 20, ys[0] - 50, 'vdd'), W(X + 20, ys[0] - 50, X + 40, ys[0] - 50, 'vdd'),
        W(X + 40, ys[0] - 50, X + 40, ys[-1], 'vdd'), LP(X + 40, ys[0] - 50, 'l_s1_vdd', 'vdd', 1),
        W(X + 20, ys[-1] + 30, X + 20, ys[-1] + 60, 'ks'), LP(X + 20, ys[-1] + 60, 'l_s1_ks', 'ks', 1),
        'P 10 5 1040 -1070 1250 -1070 1250 -280 1040 -280 1040 -1070 {dash=6}',
        'T {[S1] MS1 as drawn} 1045 -1110 0 0 0.3 0.3 {layer=10}',
        'T {8 x 0.5u / 12.5u, vdd to ks, gates en_3v3_b} 1045 -1088 0 0 0.2 0.2 {layer=10}']
# [D]: the dummies of the compact layout (D = S = bulk, gate on a signal net)
for name, kd, y, w, l, ng, g, rail in (('MDUM0', 'pmos', -960, '4.4u', '8u', 9, 'vpg', 'vdd'),
                                       ('MDUM1', 'nmos', -780, '36u', '1u', 18, 'vnc', 'vss'),
                                       ('MDUM2', 'nmos', -600, '4u', '1u', 2, 'vbr', 'vss')):
    x = 1360
    add += [dev(kd, name, x, y, w, l, ng), LP(x - 20, y, 'l_%s_g' % name.lower(), g),
            W(x + 20, y - 30, x + 40, y - 30, rail), W(x + 20, y, x + 40, y, rail), W(x + 20, y + 30, x + 40, y + 30, rail),
            W(x + 40, y - 30, x + 40, y + 30, rail), LP(x + 40, y - 30, 'l_%s_r' % name.lower(), rail, 1)]
add += ['P 10 5 1290 -1070 1500 -1070 1500 -500 1290 -500 1290 -1070 {dash=6}',
        'T {[D] dummies of the layout} 1295 -1110 0 0 0.3 0.3 {layer=10}',
        'T {D = S = bulk; gates vpg / vnc / vbr} 1295 -1088 0 0 0.2 0.2 {layer=10}',
        'T {Since 2026-10-28 backannotated from the compact layout v2 (layout/gds/oa_core_pd.gds): M10 ng 18, M11 ng 9 (W, L as before), MS1 as drawn [S1], dummies [D].} 60 -1246 0 0 0.3 0.3 {}']
for a in add: s.append(a)
s.save(); print('sheet backannotated')
