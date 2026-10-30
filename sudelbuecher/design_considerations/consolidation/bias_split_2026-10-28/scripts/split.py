"""2026-10-28: every bias_sel_pd instance -> bias_gen_pd (xg) + bias_tree_pd (xt); bias_sel_noab_pd -> bias_gen_pd + bias_tree_noab_pd.
The sheet is stretched by D right of x = cut to make room; xt takes xb's place (its outputs on xb's), xg goes into the gap.
usage: split.py <root>"""
import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/tools')
from schedit import Sheet
R = sys.argv[1]; M = os.path.join(R, 'macros')
def W(x1, y1, x2, y2, lab): return 'N %g %g %g %g {lab=%s}' % (x1, y1, x2, y2, lab)
def LP(x, y, name, lab, flip=0): return 'C {devices/lab_pin.sym} %g %g 0 %d {name=%s sig_type=std_logic lab=%s}' % (x, y, flip, name, lab)

def split(path, xb, cut, D, g, tree, top, bot, vdd, vss, labs, dele, add, repl=()):
    Xb, Yb = xb; Xg, Yg = g
    s = Sheet(path)
    # before the stretch: xb, the wires into its left pins, its rail wires and rail labels
    s.del_inst('xb', *labs)
    s.del_wire(*dele, (Xb - 30, top, Xb - 30, Yb - 90), (Xb - 50, Yb + 90, Xb - 50, bot))
    s.map_x(lambda x: x + D if x > cut else x)
    Xt, Yt = Xb + D - 10, Yb                       # xt's outputs land on xb's (stretched) output wires
    s.append('C {bias_gen_pd.sym} %g %g 0 0 {name=xg}' % (Xg, Yg))
    s.append('C {%s.sym} %g %g 0 0 {name=xt}' % (tree, Xt, Yt))
    for w in add: s.append(W(*w))               # left side into xg (all left of the cut)
    xo, yo = Xg + 90, Yg; xi, yi = Xt - 100, Yt - 50; xm = xo + 20
    for w in ((xo, yo, xm, yo), (xm, yi, xm, yo), (xm, yi, xi, yi)): s.append(W(*w, 'iref'))
    s.append('C {devices/lab_wire.sym} %g %g 0 1 {name=l_iref sig_type=std_logic lab=iref}' % (xm, yi))
    s.append(LP(xi, Yt - 30, 'l_xt_en', 'en_3v3')); s.append(LP(xi, Yt - 10, 'l_xt_enb', 'en_3v3_b'))
    s.append(W(Xt - 40, top, Xt - 40, Yt - 90, vdd)); s.append(W(Xt - 60, Yt + 90, Xt - 60, bot, vss))
    # xb's rail labels (labs) go: xt's rails are wired; xg gets labels, text to the right (clear of the symbol's texts)
    s.append(LP(Xg, Yg - 80, 'l_xg_vdd', vdd, 1)); s.append(LP(Xg, Yg + 80, 'l_xg_vss', vss, 1))
    for a, b in repl: s.replace(a, b)
    s.save()

D2S = os.path.join(M, 'sg13cmos5l_IOPadDiff2Single/schematic/xschem')
S2D = os.path.join(M, 'sg13cmos5l_IOPadSingle2Diff/schematic/xschem')
# A: the d2s pad (xb at 610 -270, left pins at x 520)
split(os.path.join(D2S, 'sg13cmos5l_IOPadDiff2Single.sch'), (610, -270), 510, 360, (620, -290), 'bias_tree_pd', -600, -100,
      'iovdd', 'iovss', ['l11', 'l12'],
      [(160, -320, 520, -320), (420, -280, 520, -280), (440, -260, 520, -260), (480, -240, 520, -240), (480, -240, 480, -220),
       (500, -220, 520, -220), (500, -220, 500, -200)],
      [(160, -320, 530, -320, 'ibias'), (420, -300, 530, -300, 'en_3v3'), (480, -280, 480, -220, 'sel0_3v3'), (480, -280, 530, -280, 'sel0_3v3'),
       (500, -260, 500, -200, 'sel1_3v3'), (500, -260, 530, -260, 'sel1_3v3')])
# B: the s2d pad (xb at 730 -270, left pins at x 640)
split(os.path.join(S2D, 'sg13cmos5l_IOPadSingle2Diff.sch'), (730, -270), 630, 360, (740, -290), 'bias_tree_noab_pd', -900, -100,
      'iovdd', 'iovss', ['l11', 'l12'],
      [(140, -320, 640, -320), (540, -280, 640, -280), (560, -260, 640, -260), (600, -240, 640, -240), (600, -240, 600, -220),
       (620, -220, 640, -220), (620, -220, 620, -200)],
      [(140, -320, 650, -320, 'ibias'), (540, -300, 650, -300, 'en_3v3'), (600, -280, 600, -220, 'sel0_3v3'), (600, -280, 650, -280, 'sel0_3v3'),
       (620, -260, 620, -200, 'sel1_3v3'), (620, -260, 650, -260, 'sel1_3v3')])
# C: d2s_mpdda_pd_sel (xb at 250 -230, left pins at x 160)
split(os.path.join(D2S, 'd2s_mpdda_pd_sel.sch'), (250, -230), 150, 400, (300, -250), 'bias_tree_pd', -540, -120,
      'vdd', 'vss', ['l0', 'l1'],
      [(100, -280, 160, -280), (140, -240, 160, -240), (140, -480, 140, -240), (120, -220, 160, -220), (120, -460, 120, -220),
       (100, -200, 160, -200), (100, -180, 160, -180)],
      [(100, -280, 210, -280, 'ibias'), (140, -480, 140, -260, 'en_3v3'), (140, -260, 210, -260, 'en_3v3'),
       (100, -200, 160, -200, 'sel0_3v3'), (160, -240, 160, -200, 'sel0_3v3'), (160, -240, 210, -240, 'sel0_3v3'),
       (100, -180, 180, -180, 'sel1_3v3'), (180, -220, 180, -180, 'sel1_3v3'), (180, -220, 210, -220, 'sel1_3v3')],
      [('Output stage as in the pad (d2s_out_p, d2s_out_n, CMA, CMB; since 2026-10-28).}',
        'Output stage as in the pad (d2s_out_p, d2s_out_n, CMA, CMB; since 2026-10-28). Bias as in the pad: bias_gen_pd + bias_tree_pd (one bias_sel_pd until 2026-10-28).}')])
# D: s2d_mpdda_pd_sel (xb at 270 -270, left pins at x 180)
split(os.path.join(S2D, 's2d_mpdda_pd_sel.sch'), (270, -270), 170, 400, (320, -290), 'bias_tree_noab_pd', -700, -100,
      'vdd', 'vss', [],
      [(100, -320, 180, -320), (140, -280, 180, -280), (140, -420, 140, -280), (160, -260, 180, -260), (160, -400, 160, -260),
       (100, -240, 180, -240), (100, -220, 180, -220)],
      [(100, -320, 230, -320, 'ibias'), (140, -420, 140, -300, 'en_3v3'), (140, -300, 230, -300, 'en_3v3'),
       (100, -240, 180, -240, 'sel0_3v3'), (180, -280, 180, -240, 'sel0_3v3'), (180, -280, 230, -280, 'sel0_3v3'),
       (100, -220, 200, -220, 'sel1_3v3'), (200, -260, 200, -220, 'sel1_3v3'), (200, -260, 230, -260, 'sel1_3v3')],
      [('Bias: bias_sel_noab_pd (four lines).}', 'Bias: bias_gen_pd + bias_tree_noab_pd (four lines; one bias_sel_noab_pd until 2026-10-28).}')])
print('split ok')
