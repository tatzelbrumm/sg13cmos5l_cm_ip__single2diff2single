# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Write en_ctrl_stage_b.sch (DRAFT, finished style): drop-in for tp_en_ctrl_b built from en_ctrl_3v3,
ls_up_1v2_3v3, nand2_hv and inv_hv. Source: ../../netlist/source/en_ctrl_stage_b.spice.

Layout: ports in one column at x = 60 (vdd_3v3 top, vss_3v3 bottom, every input at the height of the row it feeds),
outputs on the right edge. vdd_3v3 is a rail at the top with a trunk on the right (x 1040), vss_3v3 a rail at the bottom
with a trunk at x 1080, vdd_1v2 a trunk at x 180. One row per channel, pitch 160: [ls_up] -> nand2_hv (a = channel,
b = the en_m trunk at x 600) -> inv_hv. Rows 0 and 1 take their channel from en_ctrl_3v3's sel0 / sel1 shifters.
Every connection is a wire except vdd3v3_sense (lab_pin vdd_3v3) and the unused en_3v3_b output (lab_pin en_m_b).
"""
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'en_ctrl_stage_b.sch'
C, N = [], []


def wire(*pts, lab=''):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        assert x1 == x2 or y1 == y2, 'orthogonal only'
        N.append(f'N {x1} {y1} {x2} {y2} {{lab={lab}}}')


def inst(sym, x, y, props, rot=0, flip=0):
    C.append(f'C {{{sym}}} {x} {y} {rot} {flip} {{{props}}}')


pn = [0]


def port(kind, x, y, lab):
    pn[0] += 1
    inst(f'devices/{kind}.sym', x, y, f'name=p{pn[0]} lab={lab}')


ln = [0]


def label(x, y, lab, flip=0, sym='lab_pin'):
    ln[0] += 1
    inst(f'devices/{sym}.sym', x, y, f'name=l{ln[0]} sig_type=std_logic lab={lab}', flip=flip)


XP, XV1, XL, XM, XN, XI, XTAP, XV3, XVS, XO = 60, 180, 400, 600, 720, 900, 820, 1040, 1080, 1200
YR = [400 + 160 * k for k in range(9)]
YB = YR[-1] + 130            # vss rail
EN_TAP = 35                  # en<k>_b runs 35 below the row

# ports, in source port order (vss_3v3 placed at the bottom)
port('iopin', XP, 0, 'vdd_3v3')
port('iopin', XP, YB, 'vss_3v3')
port('iopin', XP, 40, 'vdd_1v2')
port('ipin', XP, 180, 'en0_1v2')
port('ipin', XP, 200, 'en1_1v2')
for k in range(2, 9):
    port('ipin', XP, YR[k], f'en{k}_1v2')
port('ipin', XP, 160, 'enable')
for k in range(9):
    port('opin', XO, YR[k], f'en{k}')
    port('opin', XO, YR[k] + EN_TAP, f'en{k}_b')

# rails and trunks
wire((XP, 0), (XV3, 0), lab='vdd_3v3')
wire((XV3, 0), (XV3, YR[-1] - 50), lab='vdd_3v3')
wire((XP, YB), (XVS, YB), lab='vss_3v3')
wire((XVS, 300), (XVS, YB), lab='vss_3v3')
wire((XP, 40), (380, 40), lab='vdd_1v2')
wire((XV1, 40), (XV1, YR[-1] - 40), lab='vdd_1v2')

# en_ctrl_3v3 at (420, 200): vddh (360,120) vddl (380,120) vss (360,280); inputs x 320, outputs x 520
inst('en_ctrl_3v3.sym', 420, 200, 'name=XEC')
wire((360, 120), (360, 0), lab='vdd_3v3')
wire((380, 120), (380, 40), lab='vdd_1v2')
wire((360, 280), (360, 300), (XVS, 300), lab='vss_3v3')
wire((XP, 160), (320, 160), lab='enable')
wire((XP, 180), (320, 180), lab='en0_1v2')
wire((XP, 200), (320, 200), lab='en1_1v2')
wire((XV1, 220), (320, 220), lab='vdd_1v2')            # vdd1v2_sense
wire((320, 240), (290, 240), lab='vdd_3v3')            # vdd3v3_sense
label(290, 240, 'vdd_3v3')
wire((520, 160), (XM, 160), lab='en_m')                # en_3v3 -> en_m trunk
wire((XM, 160), (XM, YR[-1] + 20), lab='en_m')
label(560, 160, 'en_m', sym='lab_wire')                # names the trunk
wire((520, 180), (550, 180), lab='en_m_b')             # unused output
label(550, 180, 'en_m_b', flip=1)
wire((520, 200), (560, 200), (560, YR[0] - 20), (XN - 60, YR[0] - 20), lab='ch0')
wire((520, 220), (580, 220), (580, YR[1] - 20), (XN - 60, YR[1] - 20), lab='ch1')

for k, y in enumerate(YR):
    x0 = XN + 20 if k < 2 else XL + 10                 # where this row's vdd_3v3 bus starts
    xs = XN if k < 2 else XL                           # where this row's vss bus starts
    if k >= 2:
        inst('ls_up_1v2_3v3.sym', XL, y, f'name=XL{k}')
        wire((XP, y), (XL - 40, y), lab=f'en{k}_1v2')
        wire((XL + 40, y), (500, y), (500, y - 20), (XN - 60, y - 20), lab=f'ch{k}')
        wire((XL - 10, y - 30), (XL - 10, y - 40), (XV1, y - 40), lab='vdd_1v2')
        wire((XL + 10, y - 30), (XL + 10, y - 50), lab='vdd_3v3')
        wire((XL, y + 30), (XL, y + 50), lab='vss_3v3')
    inst('nand2_hv.sym', XN, y, f'name=XN{k}')
    label(XN - 80, y - 20, f'ch{k}', sym='lab_wire')    # names the channel net
    inst('inv_hv.sym', XI, y, f'name=XI{k}')
    wire((XM, y + 20), (XN - 60, y + 20), lab='en_m')
    wire((XN + 60, y), (XI - 40, y), lab=f'en{k}_b')
    wire((XTAP, y), (XTAP, y + EN_TAP), (XO, y + EN_TAP), lab=f'en{k}_b')
    wire((XI + 40, y), (XO, y), lab=f'en{k}')
    wire((x0, y - 50), (XV3, y - 50), lab='vdd_3v3')
    wire((XN + 20, y - 30), (XN + 20, y - 50), lab='vdd_3v3')
    wire((XI + 20, y - 20), (XI + 20, y - 50), lab='vdd_3v3')
    wire((xs, y + 50), (XVS, y + 50), lab='vss_3v3')
    wire((XN, y + 30), (XN, y + 50), lab='vss_3v3')
    wire((XI, y + 20), (XI, y + 50), lab='vss_3v3')

T = [
    'T {en_ctrl_stage_b (DRAFT): drop-in for tp_en_ctrl_b, from existing cells, no ratioed logic} 60 -200 0 0 0.5 0.5 {}',
    'T {en_m = enable AND vdd_1v2 present AND vdd_3v3 present (en_ctrl_3v3, slot-fallback wiring); '
    'en<k>_b = NAND(ch<k>, en_m); en<k> = NOT en<k>_b} 60 -150 0 0 0.3 0.3 {}',
    'T {ch0 / ch1: en_ctrl_3v3 sel0 / sel1 shifters; ch2..ch8: ls_up_1v2_3v3. Not simulated, no layout.} '
    '60 -115 0 0 0.3 0.3 {}',
]
with open(OUT, 'w') as f:
    f.write('v {xschem version=3.4.8RC file_version=1.3}\nG {}\nK {}\nV {}\nS {}\nE {}\n')
    f.write('\n'.join(T + C + N) + '\n')
print('wrote', OUT, len(C), 'instances', len(N), 'wires')
