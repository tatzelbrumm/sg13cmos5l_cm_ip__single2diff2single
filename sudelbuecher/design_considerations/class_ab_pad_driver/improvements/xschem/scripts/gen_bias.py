#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Draw the bias sheets of improvements/xschem/ from ../../sim/d2s_bias_ref.spice: d2s_bias_in,
d2s_bias_out, d2s_bias_oa, d2s_bias_bg (with their symbols). Every sheet is flat: reference, mirror
tree and the six bias diodes at transistor level; check_xschem.py compares it with the flattened
netlist. Columns are current branches between the rails. The output-stage rails vddo / vsso come in
from the right, next to the outputs, and reach only RP1 / RN1.
Like gen_cells.py, the output goes to a directory of its own unless --overwrite is given.

    python3 gen_bias.py OUTDIR [--overwrite]      (needs $PDK_ROOT; PDK defaults to ihp-sg13cmos5l)
"""
import os, sys
from xsheet import Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
XSDIR = os.path.dirname(HERE)                                        # improvements/xschem


def out_dir():
    """output directory from the command line; the hand-edited sheets are not overwritten by default"""
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        raise SystemExit(__doc__)
    out = os.path.abspath(args[0])
    os.makedirs(out, exist_ok=True)
    if os.path.isdir(XSDIR) and os.path.samefile(out, XSDIR) and '--overwrite' not in sys.argv:
        raise SystemExit(f'{out} holds the hand-edited sheets: write to another directory, or add --overwrite')
    return out


OUT = out_dir()
report = []
MAG = 10   # xschem layer for block outlines, tags and legend


def save(sh, name):
    err, cross = sh.write(os.path.join(OUT, name + '.sch'))
    report.append((name, err, cross))


def block(s, x1, y1, x2, y2, tag, tx, ty, size=0.35):
    """dashed outline around a functional block, short tag at (tx, ty)"""
    s.texts.append(f'P {MAG} 5 {x1} {y1} {x2} {y1} {x2} {y2} {x1} {y2} {x1} {y1} {{dash=6}}')
    s.texts.append(f'T {{{tag}}} {tx} {ty} 0 0 {size} {size} {{layer={MAG}}}')


def legend(s, lines, x=1250, y=-110, size=0.3, step=24):
    for i, t in enumerate(lines):
        assert '{' not in t and '}' not in t
        s.texts.append(f'T {{{t}}} {x} {y + step * i} 0 0 {size} {size} {{layer={MAG}}}')


P, N = 'sg13_hv_pmos', 'sg13_hv_nmos'
YV, YVO, YG, YGO = -1000, -1040, -100, -60          # vdd, vddo above it; vss, vsso below it
PT, PC, NB, N2 = -920, -800, -200, -320             # rows: PMOS top, PMOS cascode, NMOS bottom, NMOS 2nd


def pdiode(s, name, x, y, node, src, w, l, ng=1, bulk='vdd'):
    """diode-connected PMOS, gate tied to the drain 60 below the device"""
    s.mos(name, P, x, y, 0, d=node, g=node, s=src, b=bulk, w=w, l=l, ng=ng)
    s.w(node, (x - 20, y), (x - 20, y + 60), (x + 20, y + 60)); s.w(node, (x + 20, y + 30), (x + 20, y + 60))


def ndiode(s, name, x, y, node, src, w, l, ng=1, bulk='vss'):
    """diode-connected NMOS, gate tied to the drain 60 above the device"""
    s.mos(name, N, x, y, 0, d=node, g=node, s=src, b=bulk, w=w, l=l, ng=ng)
    s.w(node, (x - 20, y), (x - 20, y - 60), (x + 20, y - 60)); s.w(node, (x + 20, y - 30), (x + 20, y - 60))


# ------------------------------------------------------------------------- symbols
def bias_sym(name, desc, iref):
    """box with vdd / vddo on top, vss / vsso at the bottom, iref on the left, outputs on the right;
    the B 5 order is the .subckt port order"""
    pins = [('vdd', -80, -180, 'inout', 't'), ('vss', -80, 180, 'inout', 'b'),
            ('vddo', 80, -180, 'inout', 't'), ('vsso', 80, 180, 'inout', 'b')]
    if iref:
        pins.append(('iref', -140, 0, 'inout', 'l'))
    pins += [(n, 140, y, 'out', 'r') for n, y in
             [('vbp', -100), ('vbn', -60), ('vbpc', -20), ('vbnc', 20), ('vabp', 60), ('vabn', 100)]]
    L = ['v {xschem version=3.4.4 file_version=1.2}\nG {}\nK {type=subcircuit\nformat="@name @pinlist @symname"\n'
         'template="name=x1"\n}\nV {}\nS {}\nE {}',
         'P 4 5 -120 -160 120 -160 120 160 -120 160 -120 -160 {}',
         'T {@symname} -110 -200 0 0 0.3 0.3 {}', 'T {@name} -110 170 0 0 0.3 0.3 {}',
         f'T {{{desc}}} -110 -40 0 0 0.18 0.18 {{}}']
    for n, x, y, d, side in pins:
        if side == 't':
            L += [f'L 4 {x} -180 {x} -160 {{}}', f'T {{{n}}} {x - 12} -155 0 0 0.2 0.2 {{}}']
        elif side == 'b':
            L += [f'L 4 {x} 160 {x} 180 {{}}', f'T {{{n}}} {x - 12} 135 0 0 0.2 0.2 {{}}']
        elif side == 'l':
            L += [f'L 4 -140 {y} -120 {y} {{}}', f'T {{{n}}} -115 {y - 7} 0 0 0.2 0.2 {{}}']
        else:
            L += [f'L 4 120 {y} 140 {y} {{}}', f'T {{{n}}} 115 {y - 7} 0 1 0.2 0.2 {{}}']
        L.append(f'B 5 {x - 2.5} {y - 2.5} {x + 2.5} {y + 2.5} {{name={n} dir={d}}}')
    open(os.path.join(OUT, name + '.sym'), 'w').write('\n'.join(L) + '\n')


# ------------------------------------------------------------------------- device helpers
def pmos_top(s, name, x, d, g, w, l, ng=1, src='vdd', rail=YV):
    """PMOS in the top row, source and n-well on the rail"""
    s.mos(name, P, x, PT, 0, d=d, g=g, s=src, b=src, w=w, l=l, ng=ng)
    s.w(src, (x + 20, PT - 30), (x + 20, rail))
    s.w(src, (x + 20, PT), (x + 40, PT), (x + 40, rail))


def pmos_casc(s, name, x, d, g, src, w, l, ng=1):
    """PMOS cascode under a top-row device (source = its drain), n-well on vdd through x+40"""
    s.mos(name, P, x, PC, 0, d=d, g=g, s=src, b='vdd', w=w, l=l, ng=ng)
    s.w(src, (x + 20, PT + 30), (x + 20, PC - 30))
    s.w('vdd', (x + 20, PC), (x + 40, PC), (x + 40, PT))


def pdiode_top(s, name, x, node, w, l, ng=1):
    """diode-connected PMOS in the top row: node at (x+20, PT+60)"""
    pdiode(s, name, x, PT, node, 'vdd', w, l, ng)
    s.w('vdd', (x + 20, PT - 30), (x + 20, YV))
    s.w('vdd', (x + 20, PT), (x + 40, PT), (x + 40, YV))


def pdiode_casc(s, name, x, node, src, w, l, ng=1, well_x=40):
    """diode-connected PMOS in the cascode row, source on the device above: node at (x+20, PC+60)"""
    pdiode(s, name, x, PC, node, src, w, l, ng)
    s.w(src, (x + 20, PT + 60), (x + 20, PC - 30))
    s.w('vdd', (x + 20, PC), (x + well_x, PC), (x + well_x, YV if well_x != 40 else PT))


def nmos_bot(s, name, x, d, g, w, l, ng=1, y=NB):
    """NMOS with source and bulk on vss"""
    s.mos(name, N, x, y, 0, d=d, g=g, s='vss', b='vss', w=w, l=l, ng=ng)
    s.w('vss', (x + 20, y + 30), (x + 20, YG))
    s.w('vss', (x + 20, y), (x + 40, y), (x + 40, YG))


def ndiode_bot(s, name, x, node, w, l, ng=1):
    """diode-connected NMOS in the bottom row: node at (x+20, NB-60)"""
    ndiode(s, name, x, NB, node, 'vss', w, l, ng)
    s.w('vss', (x + 20, NB + 30), (x + 20, YG))
    s.w('vss', (x + 20, NB), (x + 40, NB), (x + 40, YG))


# ------------------------------------------------------------------------- mirror tree + diodes
def tree(s, c0, kind):
    """columns c0 (input) ... c0+960 (RN); kind 'in' (NI, NMOS input diode) or 'out' (PI, PMOS input).
    Returns the x of the right port column."""
    c = [c0 + 160 * k for k in range(7)]
    # c0: input diode; for 'in' the input current arrives on node iref at (c0+20, NB-60)
    if kind in ('in', 'core'):
        ndiode_bot(s, 'NI', c[0], 'iref', '6u', '6u')
        sink_gate = 'iref'
    else:
        pdiode_top(s, 'PI', c[0], 'iref', '5u', '6u')
        sink_gate = 'vbn'
    src_gate = 'iref' if kind == 'out' else 'vbp'
    # c1, c2: PMOS diodes BPC, BP with their NMOS sinks
    for k, (dn, sn, node, dw, dl, sw) in enumerate([('BPC', 'NBPC', 'vbpc', '1u', '4u', '2.4u'),
                                                     ('BP', 'NBP', 'vbp', '5u', '6u', '6u')], start=1):
        pdiode_top(s, dn, c[k], node, dw, dl)
        nmos_bot(s, sn, c[k], node, sink_gate, sw, '6u')
        s.w(node, (c[k] + 20, PT + 60), (c[k] + 20, NB - 30))
        s.lab(c[k] + 20, -600, node)
    # c3: RP1 (on vddo) / RP2 (n-well on vdd) / sink NABP
    x = c[3]
    pdiode(s, 'RP1', x, PT, 'n1', 'vddo', '13.32u', '0.6u', 2, bulk='vddo')
    s.w('vddo', (x + 20, PT - 30), (x + 20, YVO))
    s.w('vddo', (x + 20, PT), (x + 40, PT), (x + 40, PT - 40), (x + 20, PT - 40))
    pdiode(s, 'RP2', x, PC, 'vabp', 'n1', '6.66u', '0.6u')
    s.w('n1', (x + 20, PT + 60), (x + 20, PC - 30))
    s.w('vdd', (x + 20, PC), (x + 60, PC), (x + 60, YV))
    s.lab(x + 20, PC - 45, 'n1')
    nmos_bot(s, 'NABP', x, 'vabp', sink_gate, '6u', '6u')
    s.w('vabp', (x + 20, PC + 60), (x + 20, NB - 30))
    s.lab(x + 20, -600, 'vabp')
    # c4, c5: PMOS sources PBNC, PBN into the NMOS diodes BNC, BN
    for k, (pn, dn, node, pw, dw, dl) in enumerate([('PBNC', 'BNC', 'vbnc', '2u', '1u', '8u'),
                                                     ('PBN', 'BN', 'vbn', '5u', '6u', '6u')], start=4):
        pmos_top(s, pn, c[k], node, src_gate, pw, '6u')
        ndiode_bot(s, dn, c[k], node, dw, dl)
        s.w(node, (c[k] + 20, PT + 30), (c[k] + 20, NB - 60))
        s.lab(c[k] + 20, -600, node)
    # c6: PABN / RN2 (bulk vss) / RN1 (source and local tap ring on vsso)
    x = c[6]
    pmos_top(s, 'PABN', x, 'vabn', src_gate, '5u', '6u')
    ndiode(s, 'RN2', x, N2, 'vabn', 'n2', '4.4u', '1u')
    s.w('vabn', (x + 20, PT + 30), (x + 20, N2 - 60))
    s.w('vss', (x + 20, N2), (x + 60, N2), (x + 60, YG))
    ndiode(s, 'RN1', x, NB, 'n2', 'vsso', '8.8u', '1u', 2, bulk='vsso')
    s.w('n2', (x + 20, N2 + 30), (x + 20, NB - 60))
    s.w('vsso', (x + 20, NB + 30), (x + 20, YGO))
    s.w('vsso', (x + 20, NB), (x + 40, NB), (x + 40, NB + 40), (x + 20, NB + 40))
    s.lab(x + 20, N2 + 45, 'n2')
    s.lab(x + 20, -600, 'vabn')
    # gate buses
    if kind in ('in', 'core'):
        # NI's line to the three sinks, along y = NB-60
        s.w('iref', (c[0] + 20, NB - 60), (c[3] - 20, NB - 60))
        for k in (1, 2, 3):
            s.w('iref', (c[k] - 20, NB - 60), (c[k] - 20, NB))
        # BP's line to the three sources, along y = -680
        s.w('vbp', (c[2] + 20, -680), (c[6] - 20, -680))
        for k in (4, 5, 6):
            s.w('vbp', (c[k] - 20, -680), (c[k] - 20, PT))
    else:
        # PI's line to the three sources, along y = -680
        s.w('iref', (c[0] + 20, PT + 60), (c[0] + 20, -680), (c[6] - 20, -680))
        for k in (4, 5, 6):
            s.w('iref', (c[k] - 20, -680), (c[k] - 20, PT))
        # BN's line to the three sinks, along y = -560
        s.w('vbn', (c[5] + 20, -560), (c[1] - 20, -560))
        for k in (1, 2, 3):
            s.w('vbn', (c[k] - 20, -560), (c[k] - 20, NB))
    # output-stage rails from the right, outputs as named ports on the right
    xr = c[6] + 220
    s.w('vddo', (c[3] + 20, YVO), (xr, YVO))
    s.w('vsso', (c[6] + 20, YGO), (xr, YGO))
    return xr, c


def rails(s, c6):
    s.w('vdd', (60, YV), (c6 + 40, YV))
    s.w('vss', (60, YG), (c6 + 60, YG))


def ports(s, xr, iref_y=None):
    """pins in .subckt order (a stand-alone netlist takes its port order from the .sch):
    vdd, vss on the left, vddo, vsso on the right, iref on the left, outputs on the right"""
    s.port('iopin', 60, YV, 'vdd', 1)
    s.port('iopin', 60, YG, 'vss', 1)
    s.port('iopin', xr, YVO, 'vddo')
    s.port('iopin', xr, YGO, 'vsso')
    if iref_y is not None:
        s.port('iopin', 60, iref_y, 'iref', 1)
    for i, n in enumerate(['vbp', 'vbn', 'vbpc', 'vbnc', 'vabp', 'vabn']):
        s.port('opin', xr, -760 + 50 * i, n)


LEG_TREE = [
    'Mirror tree and diodes. The six diodes are those of d2s_bias_lp and set the bias voltages:',
    '   vbp: BP 5u/6u, 5 uA (unit tails).  vbpc: BPC 1u/4u, 2 uA (mirror cascodes).  vabp: RP2 on RP1, 5 uA (ABP, FPL).',
    '   vbn: BN 6u/6u, 5 uA (fold sinks).  vbnc: BNC 1u/8u, 2 uA (fold cascodes).  vabn: RN2 on RN1, 5 uA (ABN, FNL).',
    'PMOS gate lines come from PMOS diodes on vdd, NMOS gate lines from NMOS diodes on vss: bias crosses blocks as currents.',
    'RP1 and RN1 are the class-AB replicas of OP and ON: they sit on the output-stage rails vddo / vsso (separate rails',
    '   from the right). RP2 keeps its n-well on vdd, like ABP. RN1 needs a local substrate tap ring on vsso, like ON.',
]


def frame_tree(s, c, kind):
    top, bot, ty = YVO - 30, YG - 15, YVO - 50
    block(s, c[1] - 40, top, c[2] + 100, bot, '[8] PMOS diodes, NMOS sinks', c[1] - 35, ty, 0.3)
    block(s, c[3] - 40, top, c[3] + 100, bot, '[8] vabp', c[3] - 35, ty, 0.3)
    block(s, c[4] - 40, top, c[5] + 100, bot, '[8] PMOS sources, NMOS diodes', c[4] - 35, ty, 0.3)
    block(s, c[6] - 40, top, c[6] + 100, YGO + 25, '[8] vabn', c[6] - 35, ty, 0.3)
    if kind != 'core':
        block(s, c[0] - 40, top, c[0] + 100, bot, '[R] input', c[0] - 35, ty, 0.3)


# ------------------------------------------------------------------------- variants 1, 2
def d2s_bias_in():
    s = Sheet(OUT)
    xr, c = tree(s, 200, 'in')
    rails(s, c[6])
    ports(s, xr, NB - 60)
    s.w('iref', (60, NB - 60), (c[0] - 20, NB - 60))
    frame_tree(s, c, 'in')
    s.text('d2s_bias_in: reference current INTO iref (from an external PMOS source, 5 uA nominal)', 60, -1290, 0.5)
    s.text('NI (a copy of BN) takes I_ref; its gate line drives the sinks NBPC, NBP, NABP out of the PMOS diodes; '
           'BP\'s gate line drives the sources PBNC, PBN, PABN into the NMOS diodes.', 60, -1240, 0.3)
    legend(s, LEG_TREE, x=60, y=-20)
    s.place('devices/title.sym', 170, 200, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, 'd2s_bias_in')


def d2s_bias_out():
    s = Sheet(OUT)
    xr, c = tree(s, 200, 'out')
    rails(s, c[6])
    ports(s, xr, PT + 60)
    s.w('iref', (60, PT + 60), (c[0] - 20, PT + 60))
    frame_tree(s, c, 'out')
    s.text('d2s_bias_out: reference current OUT of iref (into an external NMOS sink, 5 uA nominal)', 60, -1290, 0.5)
    s.text('PI (a copy of BP) delivers I_ref; its gate line drives the sources PBNC, PBN, PABN into the NMOS diodes; '
           'BN\'s gate line drives the sinks NBPC, NBP, NABP out of the PMOS diodes.', 60, -1240, 0.3)
    legend(s, LEG_TREE, x=60, y=-20)
    s.place('devices/title.sym', 170, 200, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, 'd2s_bias_out')


# ------------------------------------------------------------------------- self-contained cores
def startup(s, sense, xs=200, x3=280, xref=440):
    """MS1 (always on, weak) pulls ks up while `sense` is low; MS3 then pulls the cascode line vpc
    (the reference column's diode corner at (xref-20, PC+60)) down; MS2 releases it once `sense` is up"""
    pmos_top(s, 'MS1', xs, 'ks', 'vss', '0.5u', '100u')
    s.w('vss', (xs - 20, PT), (xs - 60, PT), (xs - 60, YG))
    nmos_bot(s, 'MS2', xs, 'ks', sense, '10u', '1u')
    s.w('ks', (xs + 20, PT + 30), (xs + 20, NB - 30))
    s.lab(xs + 20, -700, 'ks')
    y3 = -560
    s.mos('MS3', N, x3, y3, 0, d='vpc', g='ks', s='vss', b='vss', w='0.5u', l='2u', ng=1)
    s.w('ks', (xs + 20, y3), (x3 - 20, y3))
    s.w('vpc', (x3 + 20, y3 - 30), (x3 + 20, PC + 60), (xref - 20, PC + 60))
    s.w('vss', (x3 + 20, y3 + 30), (x3 + 20, YG))
    s.w('vss', (x3 + 20, y3), (x3 + 40, y3), (x3 + 40, YG))
    block(s, xs - 80, YVO - 30, x3 + 70, YG - 15, '[S] start-up', xs - 75, YVO - 50, 0.3)


def pmos_pair(s, xcol, name, cname, d, w, l, ng, cw, cl, cng, mid):
    """mirror output with cascode: gate vpg / vpc, drain `d` at (xcol+20, PC+30)"""
    pmos_top(s, name, xcol, mid, 'vpg', w, l, ng)
    pmos_casc(s, cname, xcol, d, 'vpc', mid, cw, cl, cng)
    s.lab(xcol + 20, PT + 55, mid)


def gate_buses(s, xref, cols):
    """vpg along y = PT+60 and vpc along y = PC+60, from the reference column to the gates of `cols`"""
    s.w('vpg', (xref + 20, PT + 60), (cols[-1] - 20, PT + 60))
    s.w('vpc', (xref + 20, PC + 60), (cols[-1] - 20, PC + 60))
    for x in cols:
        s.w('vpg', (x - 20, PT + 60), (x - 20, PT))
        s.w('vpc', (x - 20, PC + 60), (x - 20, PC))
    s.lab(xref + 20, PT + 45, 'vpg')
    s.lab(xref + 20, PC + 75, 'vpc')


def output_column(s, c0, w, l, ng, cw, cl, cng):
    pmos_pair(s, c0, 'PO', 'POC', 'iref', w, l, ng, cw, cl, cng, 'co')
    s.w('iref', (c0 + 20, PC + 30), (c0 + 20, NB - 60))
    s.lab(c0 + 20, -600, 'iref')
    block(s, c0 - 40, YVO - 30, c0 + 100, YG - 15, '[R] output, I_ref', c0 - 35, YVO - 50, 0.3)


LEG_OA = [
    'oa_core (Oguey-Aebischer, JSSC 32(7) 1997): no resistor, no BJT.',
    '   M11 (8 I0) and M10 (2 x M11 size, I0) share their gate vnc and run in weak inversion, so vres = U_T ln 16 = 72 mV.',
    '   MCS (diode, 2 I0) and MCL (triode, I0) share gate vbr and size; MCL drops vres only at one inversion level, so',
    '   I0 = const * 2 n mu Cox U_T^2 (W/L)_C, independent of V_T. I0 = 0.25 uA; PO / POC deliver 20 I0 = 5 uA into NI.',
    '   MC10 cascodes M10; P0 / P0C are stacked diodes, so every mirror output copies P0\'s V_DS (line sensitivity).',
    '   Temperature: I0 ~ mu T^2, about -35 % at -40 C and +33 % at 125 C.',
]
LEG_BG = [
    'bg_core: current-mode (Banba type) bandgap, no op-amp.',
    '   The PMOS mirror makes both branch currents equal and the NMOS pair NA / NB (gates on g) forces ea = eb, so each',
    '   branch carries V_BE1 / R1 + U_T ln 8 / R0 (Q2 = 8 x Q1). rhigh (-0.22 %/K) nearly cancels V_BE\'s -1.77 mV/K already,',
    '   so the PTAT share through R0 is small. PO / POC deliver twice the branch current, 5 uA, into NI.',
    '   R1A is 10 % longer than R1B: with both PNPs off the loop gain is then > 1, so the core cannot rest there.',
    '   PB / PBC are stacked diodes; the PMOS run in moderate inversion for headroom at 3.0 V, ss, -40 C.',
]


def d2s_bias_oa():
    s = Sheet(OUT)
    xs, xr0, xn, xc, c0 = 200, 440, 600, 760, 920
    startup(s, 'vbr', xs=xs, xref=xr0)
    # reference column: P0 / P0C diodes, MC10, M10, MCL
    pdiode_top(s, 'P0', xr0, 'vpg', '2u', '8u')
    pdiode_casc(s, 'P0C', xr0, 'vpc', 'vpg', '0.5u', '2u')
    for name, y, d, g, src, w, l, ng in [('MC10', -560, 'vpc', 'vbr', 'd10', '10u', '1u', 1),
                                          ('M10', -440, 'd10', 'vnc', 'vres', '180u', '1u', 8),
                                          ('MCL', -320, 'vres', 'vbr', 'vss', '3.4u', '30u', 1)]:
        s.mos(name, N, xr0, y, 0, d=d, g=g, s=src, b='vss', w=w, l=l, ng=ng)
        s.w('vss', (xr0 + 20, y), (xr0 + 40, y))
    s.w('vss', (xr0 + 40, -560), (xr0 + 40, YG))
    s.w('vpc', (xr0 + 20, PC + 60), (xr0 + 20, -590))
    s.w('d10', (xr0 + 20, -530), (xr0 + 20, -470))
    s.w('vres', (xr0 + 20, -410), (xr0 + 20, -350))
    s.w('vss', (xr0 + 20, -290), (xr0 + 20, YG))
    s.lab(xr0 + 20, -520, 'd10')
    s.lab(xr0 + 20, -380, 'vres')
    # M11 column and composite-diode column, with their mirror outputs
    pmos_pair(s, xn, 'P8', 'P8C', 'vnc', '16u', '8u', 8, '4u', '2u', 2, 'c8')
    ndiode_bot(s, 'M11', xn, 'vnc', '90u', '1u', 4)
    s.w('vnc', (xn + 20, PC + 30), (xn + 20, NB - 60))
    pmos_pair(s, xc, 'P2', 'P2C', 'vbr', '4u', '8u', 2, '1u', '2u', 1, 'c2')
    ndiode_bot(s, 'MCS', xc, 'vbr', '3.4u', '30u')
    s.w('vbr', (xc + 20, PC + 30), (xc + 20, NB - 60))
    output_column(s, c0, '40u', '8u', 20, '10u', '2u', 5)
    gate_buses(s, xr0, [xn, xc, c0])
    # vnc to M10's gate; vbr to MC10, MCL and the start-up sense MS2
    s.w('vnc', (xn + 20, -500), (xr0 - 20, -500), (xr0 - 20, -440))
    s.w('vbr', (xc + 20, -620), (xr0 - 40, -620), (xr0 - 40, -280), (xs - 20, -280), (xs - 20, NB))
    s.w('vbr', (xr0 - 40, -560), (xr0 - 20, -560))
    s.w('vbr', (xr0 - 40, -320), (xr0 - 20, -320))
    s.lab(xn + 20, -600, 'vnc')
    s.lab(xc + 20, -560, 'vbr')
    block(s, xr0 - 70, YVO - 30, xc + 100, YG - 15, '[C] Oguey-Aebischer core', xr0 - 65, YVO - 50, 0.3)
    xr, c = tree(s, c0, 'core')
    rails(s, c[6])
    ports(s, xr)
    frame_tree(s, c, 'core')
    s.text('d2s_bias_oa: self-contained bias without resistor or BJT (Oguey-Aebischer core + mirror tree of d2s_bias_in)',
           60, -1290, 0.5)
    s.text('core current I0 = 0.25 uA (P0 branch); M11 8 I0, MCS 2 I0; I_ref = 20 I0 = 5 uA into NI', 60, -1240, 0.3)
    legend(s, LEG_OA + LEG_TREE, x=60, y=-20)
    s.place('devices/title.sym', 170, 340, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, 'd2s_bias_oa')


def d2s_bias_bg():
    s = Sheet(OUT)
    xs, xb, xa, c0 = 200, 440, 760, 1000
    startup(s, 'g', xs=xs, xref=xb)
    # branch B (reference side): PB / PBC diodes, NB, then R1B || (R0 + Q2) from eb
    pdiode_top(s, 'PB', xb, 'vpg', '40u', '1u', 4)
    pdiode_casc(s, 'PBC', xb, 'vpc', 'vpg', '40u', '1u', 4)
    s.mos('NB', N, xb, -560, 0, d='vpc', g='g', s='eb', b='vss', w='20u', l='4u', ng=1)
    s.w('vpc', (xb + 20, PC + 60), (xb + 20, -590))
    s.w('vss', (xb + 20, -560), (xb + 40, -560), (xb + 40, -260))
    s.place('sg13cmos5l_pr/rhigh.sym', xb + 20, -440, 0, 0,
            'name=R1B\nw=0.5u\nl=99.36u\nmodel=rhigh\nbody=vss\nspiceprefix=X\nb=0\nm=1\nmm_ok=1',
            dict(P='eb', M='vss'), 'R1B')
    s.w('eb', (xb + 20, -530), (xb + 20, -470))
    s.w('vss', (xb + 20, -410), (xb + 20, YG))
    s.w('vss', (xb + 40, -260), (xb + 20, -260))
    s.place('sg13cmos5l_pr/rhigh.sym', xb + 140, -440, 0, 0,
            'name=R0\nw=0.5u\nl=179.5u\nmodel=rhigh\nbody=vss\nspiceprefix=X\nb=0\nm=1\nmm_ok=1',
            dict(P='eb', M='e2'), 'R0')
    s.w('eb', (xb + 20, -500), (xb + 140, -500), (xb + 140, -470))
    s.place('sg13cmos5l_pr/pnpMPA.sym', xb + 120, -320, 0, 0,
            'name=Q2\nmodel=pnpMPA\nspiceprefix=X\nw=2e-6\nl=2e-6\nm=8', dict(emitter='e2', base='vss', collector='vss'), 'Q2')
    s.w('e2', (xb + 140, -410), (xb + 140, -350))
    s.w('vss', (xb + 140, -290), (xb + 140, YG))
    s.w('vss', (xb + 100, -320), (xb + 100, -260), (xb + 140, -260))
    s.lab(xb + 20, -515, 'eb')
    s.lab(xb + 140, -380, 'e2')
    s.text('m = 8: Q2 = 8 x Q1', xb + 165, -280, 0.25)
    # branch A: PA / PAC, NA (diode on g), then Q1 || R1A from ea
    pmos_pair(s, xa, 'PA', 'PAC', 'g', '40u', '1u', 4, '40u', '1u', 4, 'ca')
    s.mos('NA', N, xa, -560, 0, d='g', g='g', s='ea', b='vss', w='20u', l='4u', ng=1)
    s.w('g', (xa + 20, PC + 30), (xa + 20, -590))
    s.w('g', (xa - 20, -560), (xa - 20, -620), (xa + 20, -620))
    s.w('vss', (xa + 20, -560), (xa + 40, -560), (xa + 40, -260))
    s.place('sg13cmos5l_pr/rhigh.sym', xa + 20, -440, 0, 0,
            'name=R1A\nw=0.5u\nl=109.3u\nmodel=rhigh\nbody=vss\nspiceprefix=X\nb=0\nm=1\nmm_ok=1',
            dict(P='ea', M='vss'), 'R1A')
    s.w('ea', (xa + 20, -530), (xa + 20, -470))
    s.w('vss', (xa + 20, -410), (xa + 20, YG))
    s.w('vss', (xa + 40, -260), (xa + 20, -260))
    s.place('sg13cmos5l_pr/pnpMPA.sym', xa + 80, -320, 0, 0,
            'name=Q1\nmodel=pnpMPA\nspiceprefix=X\nw=2e-6\nl=2e-6\nm=1', dict(emitter='ea', base='vss', collector='vss'), 'Q1')
    s.w('ea', (xa + 20, -500), (xa + 100, -500), (xa + 100, -350))
    s.w('vss', (xa + 100, -290), (xa + 100, YG))
    s.w('vss', (xa + 60, -320), (xa + 60, -260), (xa + 100, -260))
    s.lab(xa + 20, -515, 'ea')
    # g to NB and to the start-up sense MS2
    s.w('g', (xa - 20, -620), (xb - 40, -620), (xb - 40, -560), (xb - 20, -560))
    s.w('g', (xb - 40, -560), (xb - 40, -280), (xs - 20, -280), (xs - 20, NB))
    s.lab(xa + 20, -700, 'g')
    output_column(s, c0, '80u', '1u', 8, '80u', '1u', 8)
    gate_buses(s, xb, [xa, c0])
    block(s, xb - 70, YVO - 30, xa + 150, YG - 15, '[C] bandgap core', xb - 65, YVO - 50, 0.3)
    xr, c = tree(s, c0, 'core')
    rails(s, c[6])
    ports(s, xr)
    frame_tree(s, c, 'core')
    s.text('d2s_bias_bg: self-contained bias, current-mode bandgap with pnpMPA and rhigh + mirror tree of d2s_bias_in',
           60, -1290, 0.5)
    s.text('branch current V_BE1/R1 + U_T ln 8 / R0 = 2.5 uA; I_ref = 2 x branch = 5 uA into NI; Q1 / Q2: emitter 2u x 2u',
           60, -1240, 0.3)
    legend(s, LEG_BG + LEG_TREE, x=60, y=-20)
    s.place('devices/title.sym', 170, 340, 0, 0, 'name=l0 author="Christoph Maier"', {}, 'title')
    save(s, 'd2s_bias_bg')


if __name__ == '__main__':
    bias_sym('d2s_bias_in', 'I_ref into iref (PMOS source)', True)
    bias_sym('d2s_bias_out', 'I_ref out of iref (NMOS sink)', True)
    bias_sym('d2s_bias_oa', 'self-contained, no R, no BJT', False)
    bias_sym('d2s_bias_bg', 'self-contained bandgap (pnpMPA)', False)
    d2s_bias_in()
    d2s_bias_out()
    d2s_bias_oa()
    d2s_bias_bg()
    bad = 0
    for name, err, cross in report:
        print(f'{name}: {len(err)} lint errors, {cross} wire crossings')
        for e in err:
            print('   ', e)
        bad += len(err)
    sys.exit(1 if bad else 0)
