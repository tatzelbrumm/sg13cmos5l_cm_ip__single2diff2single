"""2026-10-28: backannotate the compact bg_core_pd layout into bg_core_pd.sch, in the sheet's own style:
R0 / R1A / R1B as xschem vector instances (chains of 18 / 11 / 10 rhigh segments 0.5u / 9.94u, connected by bus labels),
NA / NB ng 2, MS1 as the drawn 8-device chain [S1], the dummies [D]. [C] is widened (+180 from x 520, +360 from x 820)
so the bus labels fit (B +210, C/D +230, from x 820 +470). usage: bg_sheet_ba.py <root>"""
import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/tools')
from schedit import Sheet, parse
R = sys.argv[1]; p = os.path.join(R, 'macros/bg_core_pd/schematic/xschem/bg_core_pd.sch')
s = Sheet(p)
def set_ng(name, old, new):
    i = s.find_inst(name); t = ''.join(s.items[i]); assert t.count('ng=%d\n' % old) == 1, name
    s.items[i:i + 1] = parse(t.replace('ng=%d\n' % old, 'ng=%d\n' % new))
set_ng('NA', 1, 2); set_ng('NB', 1, 2)
# --- removals, in the old coordinates
s.del_inst('R0', 'R1A', 'R1B', 'l3', 'l2', 'MS1', 'l1')
s.del_wire((460, -380, 460, -350), (460, -380, 580, -380), (580, -380, 580, -350), (580, -290, 580, -230),
           (460, -290, 460, -100), (780, -380, 780, -350), (780, -290, 780, -100),
           (260, -1000, 260, -950), (260, -920, 280, -920), (280, -1000, 280, -920), (180, -920, 220, -920),
           (180, -920, 180, -580), (260, -890, 260, -560))
# --- widen [C]: column B (Q2, SVPG, en_3v3) and C/D (Q1, NA, PA, PAC) +180, [C]'s right edge and [R] +360
s.map_x(lambda x: x if x < 520 else (x + 210 if x < 670 else (x + 230 if x < 820 else x + 470)))
# --- additions, in the new coordinates
W = lambda x1, y1, x2, y2, lab: 'N %g %g %g %g {lab=%s}' % (x1, y1, x2, y2, lab)
LP = lambda x, y, n, lab, f=0: 'C {devices/lab_pin.sym} %g %g 0 %d {name=%s sig_type=std_logic lab=%s}' % (x, y, f, n, lab)
LW = lambda x, y, n, lab: 'C {devices/lab_wire.sym} %g %g 0 0 {name=%s sig_type=std_logic lab=%s}' % (x, y, n, lab)
T = lambda t, x, y, sz=0.2, lay='': 'T {%s} %g %g 0 0 %g %g {%s}' % (t, x, y, sz, sz, 'layer=%d' % lay if lay else '')
def mos(kind_, name, x, y, w, l, ng):
    return ('C {sg13cmos5l_pr/sg13_hv_%s.sym} %g %g 0 0 {name=%s\nl=%s\nw=%s\nng=%d\nm=1\nmm_ok=1\nmodel=sg13_hv_%s\nspiceprefix=X}'
            % (kind_, x, y, name, l, w, ng, kind_))
def res(name, x, y):
    return ('C {sg13cmos5l_pr/rhigh.sym} %g %g 0 0 {name=%s\nw=0.5u\nl=9.94u\nmodel=rhigh\nbody=vss\nspiceprefix=X\nb=0\nm=1\nmm_ok=1}'
            % (x, y, name))
add = [LW(460, -380, 'l2', 'eb'),                                    # NB source stub keeps its label, now at its end
       W(260, -620, 260, -560, 'ks'), LW(260, -620, 'l1', 'ks'),       # ks stub (MS1 moved to [S1])
       T('MS1 (0.5u / 100u) is drawn as', 150, -960), T('8 x 0.5u / 12.5u in series: [S1]', 150, -942)]
# [C]: the three resistor chains, eb / ea at the top label, vss / e2 at the bottom label
for name, x, top, bot in (('R1B[9:0]', 580, 'eb,n1b[8:0]', 'n1b[8:0],vss'), ('R0[17:0]', 790, 'eb,n0[16:0]', 'n0[16:0],e2'),
                          ('R1A[10:0]', 1170, 'ea,n1a[9:0]', 'n1a[9:0],vss')):
    k = name.split('[')[0].lower()
    add += [res(name, x, -320), LP(x, -350, 'l_%s_p' % k, top), LP(x, -290, 'l_%s_m' % k, bot)]
add += [W(790, -230, 790, -250, 'e2'), LP(790, -250, 'l_e2', 'e2', 1),
        T('R0, R1A, R1B as drawn (compact layout): chains of 18 / 11 / 10 rhigh', 480, -656),
        T('segments 0.5u / 9.94u, as vector instances R0[17:0], R1A[10:0], R1B[9:0];', 480, -638),
        T('the bus labels name the chain nodes (eb, n0[16] ... n0[0], e2).', 480, -620),
        T('Each segment has its own heads: R +0.70 % (R0), +1.03 % (R1A), +1.02 % (R1B)', 480, -602),
        T('against the single devices 0.5u / 179.5u, 109.3u, 99.36u.', 480, -584)]
# [S1]: MS1 chain, vdd -> ms1_1 ... ms1_7 -> ks, gates en_3v3_b, bulks vdd
X, Y0, P = 1660, -960, 80
ys = [Y0 + P * k for k in range(8)]
for k, y in enumerate(ys):
    add.append(mos('pmos', 'MS1_%d' % k, X, y, '0.5u', '12.5u', 1))
    add += [W(X - 40, y, X - 20, y, 'en_3v3_b'), W(X + 20, y, X + 40, y, 'vdd')]
    if k < 7: add.append(W(X + 20, y + 30, X + 20, ys[k + 1] - 30, 'ms1_%d' % (k + 1)))
add += [W(X - 40, ys[0], X - 40, ys[-1], 'en_3v3_b'), LP(X - 40, ys[0], 'l_s1_g', 'en_3v3_b'),
        W(X + 20, ys[0] - 30, X + 20, ys[0] - 50, 'vdd'), W(X + 20, ys[0] - 50, X + 40, ys[0] - 50, 'vdd'),
        W(X + 40, ys[0] - 50, X + 40, ys[-1], 'vdd'), LP(X + 40, ys[0] - 50, 'l_s1_vdd', 'vdd', 1),
        W(X + 20, ys[-1] + 30, X + 20, ys[-1] + 60, 'ks'), LP(X + 20, ys[-1] + 60, 'l_s1_ks', 'ks', 1),
        'P 10 5 1560 -1070 1770 -1070 1770 -280 1560 -280 1560 -1070 {dash=6}',
        T('[S1] MS1 as drawn', 1565, -1110, 0.3, 10), T('8 x 0.5u / 12.5u, vdd to ks, gates en_3v3_b', 1565, -1088, 0.2, 10)]
# [D]: dummies of the compact layout
x = 1900
for name, y, g in (('MDUM0', -960, 'vpg'), ('MDUM1', -820, 'vpc')):   # PMOS 8 x 0.3u / 1u, D = S = bulk = vdd
    add += [mos('pmos', name, x, y, '2.4u', '1u', 8), LP(x - 20, y, 'l_%s_g' % name.lower(), g),
            W(x + 20, y - 30, x + 40, y - 30, 'vdd'), W(x + 20, y, x + 40, y, 'vdd'), W(x + 20, y + 30, x + 40, y + 30, 'vdd'),
            W(x + 40, y - 30, x + 40, y + 30, 'vdd'), LP(x + 40, y - 30, 'l_%s_r' % name.lower(), 'vdd', 1)]
for name, y, w, l, ng in (('MDUM2', -660, '2u', '1u', 1), ('MDUM3', -500, '16u', '4u', 8)):   # NMOS, D = S = G = g, bulk vss
    add += [mos('nmos', name, x, y, w, l, ng),
            W(x - 20, y, x - 40, y, 'g'), W(x + 20, y - 30, x + 20, y - 50, 'g'), W(x + 20, y - 50, x - 40, y - 50, 'g'),
            W(x - 40, y - 50, x - 40, y + 50, 'g'), W(x + 20, y + 30, x + 20, y + 50, 'g'), W(x + 20, y + 50, x - 40, y + 50, 'g'),
            LP(x - 40, y - 50, 'l_%s_g' % name.lower(), 'g'),
            W(x + 20, y, x + 40, y, 'vss'), W(x + 40, y, x + 40, y + 70, 'vss'), LP(x + 40, y + 70, 'l_%s_b' % name.lower(), 'vss', 1)]
add += [res('RDUM[1:0]', x, -320), LP(x, -350, 'l_rdum_p', 'vss'), LP(x, -290, 'l_rdum_m', 'vss'),
        'P 10 5 1810 -1070 2110 -1070 2110 -200 1810 -200 1810 -1070 {dash=6}',
        T('[D] dummies of the layout', 1815, -1132, 0.3, 10),
        T('PMOS: D = S = bulk = vdd, gates vpg / vpc', 1815, -1110, 0.2, 10),
        T('NMOS: D = S = G = g (Vgs = 0), bulk vss; rhigh: both ends vss', 1815, -1092, 0.2, 10),
        T('Since 2026-10-28 backannotated from the compact layout (layout/gds/bg_core_pd.gds): resistors as chains [C], '
          'NA / NB ng 2 (W, L as before), MS1 as drawn [S1], dummies [D].', 60, -1216, 0.3)]
for a in add: s.append(a)
s.save(); print('sheet backannotated')
