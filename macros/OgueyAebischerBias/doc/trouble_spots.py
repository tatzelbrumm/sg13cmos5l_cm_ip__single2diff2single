"""OgueyAebischerBias core, netlist-first, with the three measured trouble spots marked.

Netlist transcribed from
macros/OgueyAebischerBias/verification/cace/netlist/schematic/reference.spice
(.subckt OgueyAebischerBias).  The 0 V ammeters Vi1 / Vi4 / Viaux are shorts, so
they are merged into the nets they sit in and shown as branch-current
annotations instead of symbols.  ToBiasStartup is not drawn: Iq_disabled = 66 pA
measured, so it contributes nothing at DC.

Local VDD / GND port symbols are used rather than one global rail net, so the
only long wires left are the three that actually matter: vbp, vbn, vbr.

Numbers on the figure are from RUN_2026-09-04_08-27-47 (tt, 27 C, 3.3 V).
"""
import sys
sys.path.insert(0, 'scripts')
from sch_netlist import Circuit, Mosfet, Port, save_png

W, H = 1260, 940
c = Circuit(W, H)

# --------------------------------------------------------------- devices
# col 1 (x=170): branch 1, I1   M12 -> M10 -> vres -> M16/M18/M20/M22 -> vss
# col 2 (x=420): branch 2, I2   M13 -> M11 -> vss
# col 3 (x=670): branch 3, I3   M14 -> M15/M17/M19/M21 -> vss
P = {}
def dev(n, kind, at, gate, label=None):
    d = c.add(Mosfet(n, kind, at, gate=gate, source_up=(kind == 'p'), label=label or n))
    P[n] = d
    return d

dev('M12', 'p', (170, 140), 'L', 'M12 ×1')
dev('M13', 'p', (420, 200), 'L', 'M13 ×4')
dev('M14', 'p', (670, 260), 'L', 'M14 ×2')
dev('M11', 'n', (420, 360), 'R', 'M11 ×1')
dev('M10', 'n', (170, 430), 'R', 'M10 ×4')
for n, y in [('M16', 530), ('M18', 615), ('M20', 700), ('M22', 785)]:
    dev(n, 'n', (170, y), 'R')
for n, y in [('M15', 530), ('M17', 615), ('M19', 700), ('M21', 785)]:
    dev(n, 'n', (670, y), 'L')

rails, gnds = {}, {}
for n, at in [('M12', (170, 100)), ('M13', (420, 160)), ('M14', (670, 220))]:
    rails[n] = c.add(Port('VDD_' + n, at, 'VDD'))
for n, at in [('M11', (420, 424)), ('M22', (170, 849)), ('M21', (670, 849)),
              ('M10', (60, 430)), ('M16', (60, 530)), ('M18', (60, 615)),
              ('M20', (60, 700)), ('M15', (730, 530)), ('M17', (730, 615)),
              ('M19', (730, 700))]:
    gnds[n] = c.add(Port('GND_' + n, at, '', kind='gnd'))

# --------------------------------------------------------------- nets
for n in ('M12', 'M13', 'M14'):
    c.net('vdd_' + n, [P[n].P('S'), P[n].P('B'), rails[n].P('p')], trunk=('v', P[n].cx))
c.net('vbp', [P['M12'].P('D'), P['M12'].P('G'), P['M13'].P('G'),
              P['M14'].P('G'), P['M10'].P('D')],                  trunk=('v',  90))
c.net('vbn', [P['M13'].P('D'), P['M11'].P('D'), P['M11'].P('G'),
              P['M10'].P('G')],                                   trunk=('v', 300))
c.net('vres', [P['M10'].P('S'), P['M16'].P('D')],                 trunk=('v', 170))
c.net('vbr', [P['M14'].P('D'), P['M15'].P('D'),
              P['M15'].P('G'), P['M17'].P('G'), P['M19'].P('G'), P['M21'].P('G'),
              P['M16'].P('G'), P['M18'].P('G'), P['M20'].P('G'), P['M22'].P('G')],
      trunk=('v', 545))
for a_, b_, x in [('M15', 'M17', 670), ('M17', 'M19', 670), ('M19', 'M21', 670),
                  ('M16', 'M18', 170), ('M18', 'M20', 170), ('M20', 'M22', 170)]:
    c.net(f'n_{a_}_{b_}', [P[a_].P('S'), P[b_].P('D')], trunk=('v', x))
c.net('vss_M11', [P['M11'].P('S'), P['M11'].P('B'), gnds['M11'].P('p')], trunk=('v', 420))
c.net('vss_M22', [P['M22'].P('S'), P['M22'].P('B'), gnds['M22'].P('p')], trunk=('v', 170))
c.net('vss_M21', [P['M21'].P('S'), P['M21'].P('B'), gnds['M21'].P('p')], trunk=('v', 670))
for n in ('M10', 'M16', 'M18', 'M20', 'M15', 'M17', 'M19'):
    c.net('bulk_' + n, [P[n].P('B'), gnds[n].P('p')], trunk=('v', P[n].pins['B'].x))

v = c.drc()
print('DRC violations:', v if v else 'none')
c.render('oab.svg')

# --------------------------------------------------------------- annotation overlay
RED, AMB, VIO, INK, MID = '#c0392b', '#b9770e', '#6c3483', '#111', '#555'
F = 'Georgia,serif'
a = []
def txt(x, y, s, size=14, fill=INK, anchor='start', weight='normal', style='normal'):
    a.append(f'<text x="{x}" y="{y}" font-size="{size}" font-family="{F}" fill="{fill}" '
             f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}">{s}</text>')
def badge(x, y, n, col):
    a.append(f'<circle cx="{x}" cy="{y}" r="12" fill="{col}"/>')
    a.append(f'<text x="{x}" y="{y+5}" font-size="14" font-family="{F}" fill="#fff" '
             f'text-anchor="middle" font-weight="bold">{n}</text>')
def band(x1, y1, x2, y2, col, op=0.15):
    a.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="6" '
             f'fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-opacity="0.55" '
             f'stroke-width="1.5" stroke-dasharray="5 3"/>')

# -- (2) vbr trunk, its eight gate rungs, and the two stacks it controls
a.append(f'<rect x="536" y="286" width="18" height="505" rx="9" fill="{AMB}" fill-opacity="0.22"/>')
for y in (530, 615, 700, 785):
    a.append(f'<rect x="200" y="{y-7}" width="440" height="14" rx="7" fill="{AMB}" fill-opacity="0.16"/>')
a.append(f'<rect x="118" y="486" width="104" height="340" rx="10" fill="{AMB}" fill-opacity="0.09"/>')
a.append(f'<rect x="618" y="486" width="104" height="340" rx="10" fill="{AMB}" fill-opacity="0.09"/>')

# -- (1) the three devices whose Vds rides on the supply
for cx, cy in ((420, 200), (670, 260), (170, 430)):
    band(cx - 48, cy - 42, cx + 50, cy + 42, RED)

# -- badges
badge(520, 200, '1', RED); badge(520, 228, '3', VIO)
badge(770, 260, '1', RED); badge(770, 288, '3', VIO)
badge(252, 398, '1', RED); badge(252, 370, '3', VIO)
badge(258, 140, '3', VIO)
badge(466, 398, '3', VIO)
badge(545, 266, '2', AMB)

# -- node / branch annotations
txt(14, 128, 'vbp = 2.674 V', 13, MID, weight='bold')
txt(250, 222, 'vbn = 0.614 V', 13, MID, weight='bold')
txt(424, 282, 'vbr = 1.012 V', 13, MID, weight='bold')
txt(188, 478, 'vres = 93 mV', 13, MID, weight='bold')
txt(188, 495, '= n·U', 11, MID); txt(221, 498, 'T', 9, MID); txt(228, 495, '·ln 16', 11, MID)
txt(196, 306, 'I₁ = 47 nA', 13, MID, style='italic')
txt(440, 306, 'I₂ = 187 nA', 13, MID, style='italic')
txt(592, 344, 'I₃ = 93 nA', 13, MID, style='italic')
txt(255, 566, 'stack devices: L = 20 µm, ×4 in series', 12, MID, style='italic')

# -- title + footnotes
txt(30, 36, 'OgueyAebischerBias core — where the PSRR and the matching go', 20, INK, weight='bold')
txt(30, 58, 'measured tt, 27 °C, 3.3 V — RUN_2026-09-04_08-27-47', 13, MID, style='italic')
txt(30, 900, 'ToBiasStartup (start-up kick + disable) is not drawn: Iq_disabled = 66 pA measured, so it contributes nothing at DC.', 12, MID, style='italic')
txt(30, 918, 'Vi1 / Vi4 / Viaux are 0 V ammeters — electrically shorts — so they appear as branch currents, not symbols.', 12, MID, style='italic')

# -- legend panel
LX, LY = 870, 92
a.append(f'<rect x="{LX-14}" y="{LY-32}" width="390" height="812" rx="10" fill="#fafafa" stroke="#ddd"/>')
def block(y, col, n, head, lines):
    badge(LX + 4, y, n, col)
    txt(LX + 26, y + 5, head, 15, col, weight='bold')
    yy = y + 30
    for ln in lines:
        txt(LX + 26, yy, ln, 13, INK)
        yy += 18
    return yy + 18

y = block(LY, RED, '1', 'The disturbance gets in here', [
    'M13, M14 and M10 each have a drain that',
    'moves 1 : 1 with VDD. M12 and M11 are',
    'diode-connected, so their Vds is pinned.',
    '',
    'Leg_matching typ = +5.568 % is exactly this:',
    'M12 and M13 share Vsg, but their drains sit',
    '2.06 V apart, so',
    '     (1/I)·dI/dVsd = 2.70 %/V,   V_A ≈ 37 V.',
    'The device is fine — this is only the door.',
    '',
    'Fix: cascode M13, M14, M10. vbr and vbn are',
    'already sitting there to use as cascode gates.',
])
y = block(y, AMB, '2', 'Then the loop multiplies it ×10', [
    'vbr gates all eight stack devices at once, and',
    'vbr moves 61.7 mV/V. They sit at Vgs−Vth ≈ 0.3 V,',
    'so the stack conductance — which IS the',
    'reference resistor — swings with the supply.',
    '',
    'Positive feedback:',
    '     VDD↑ → I₃↑ → vbr↑ → G↑ → I↑ → I₃↑',
    'Loop gain ≈ 0.9, hence 1/(1−T) ≈ 10.',
    '',
    '     per device        2.70 %/V',
    '     at the output   27.5 %/V   ⇒   PSRR 24.3 dB',
    '',
    'The ×10 is structural. Shrink what gets',
    'injected instead — that is (1).',
])
y = block(y, VIO, '3', 'Everything here is 1 µm²', [
    'M10 M11 M12 M13 M14 are all W = L = 1 µm.',
    'From Leg_matching σ ≈ 12 %: A_VT ≈ 5–7 mV·µm.',
    '',
    'Ibias_accuracy spans −76 % … +148 %, σ ≈ 50 %',
    '— the same ×10 loop, amplifying mismatch now.',
    '',
    'For σ ≈ 3 % you need W·L ≈ 75–100 µm² each,',
    'i.e. ×100 area. It is a √area law, no escape.',
    'The same area buys ×10 on the 1/f noise.',
])

svg = open('oab.svg').read().replace('</svg>', ''.join(a) + '</svg>')
open('oab_annotated.svg', 'w').write(svg)
save_png('oab_annotated.svg', 'oab_annotated.png', width=1500)
print('annotated')
