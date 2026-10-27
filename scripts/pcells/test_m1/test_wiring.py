# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Test Clamp_N_M1 / Clamp_P_M1 with wiring = external plus Clamp_N_M1_wiring /
Clamp_P_M1_wiring through the real PCell path (library SG13_cm_clamps), 2026-10-27.

    python3 test_wiring.py [out.gds]       # default out.gds: wiring_cells.gds

Needs the PDK found via $KLAYOUT_PATH or $PDKPATH, like test_m1.py. For each case the
clamp and its wiring cell are placed at one origin; checks:
  1. clamp + wiring equal the pure engine (generate_m1(..., 'external') + generate_m1_wiring)
     on every layer, texts included;
  2. without roles, clamp + wiring equal the clamp with wiring = internal (merged per layer);
  3. klayout.db extraction: output device W / L with G on the gate net and D on 'pad',
     replica gate = drain = the replica net, dummy gate = source = rail (off);
  4. Metal1 width 0.16 / space 0.18 um, and no layer above Metal1.
Exit 1 on failure.
"""
import os, runpy, sys, collections
import klayout.db as db
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # scripts/pcells
sys.path.insert(0, REPO)
runpy.run_path(os.path.join(REPO, 'load_clamp_pcells.py'))
import clamp_engine as E, clamp_klayout as K
from sg13cmos5l_pycell_lib.sg13_tech import SG13_Tech

ly = db.Layout(); ly.dbu = 0.001; ly.technology_name = SG13_Tech.TECH_NAME
top = ly.create_cell('TOP')
lib = db.Library.library_by_name('SG13_cm_clamps')
FORBIDDEN = [(10, 0), (10, 2), (10, 25), (19, 0), (29, 0), (30, 0)]
fails = 0

def pcell(name, params):
    decl = lib.layout().pcell_declaration(name)
    pid = ly.add_pcell_variant(lib, decl.id(), {k: v for k, v in params.items()})
    return ly.cell(pid)

def flat(cells):
    c = ly.create_cell('chk')
    for x in cells:
        c.insert(db.CellInstArray(x.cell_index(), db.Trans()))
    c.flatten(-1, True)
    return c

def layers_of(cell):
    out = {}
    for li in ly.layer_indexes():
        r = db.Region(cell.begin_shapes_rec(li))
        if not r.is_empty():
            out[(ly.get_info(li).layer, ly.get_info(li).datatype)] = r.merged()
    return out

def texts_of(cell):
    return collections.Counter((s.text.string, s.text.x, s.text.y) for li in ly.layer_indexes()
                               for s in cell.shapes(li).each() if s.is_text())

def extract(cell, fam):
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, cell, []))
    g = lambda a, b: l2n.make_polygon_layer(ly.layer(a, b), 'L%d_%d' % (a, b))
    A, P, PS, NW, C, M1 = g(1, 0), g(5, 0), g(14, 0), g(31, 0), g(6, 0), g(8, 0)
    gate = (P & A) - PS - NW if fam == 'N' else P & A & PS & NW
    sd = A - P
    l2n.register(gate, 'gate'); l2n.register(sd, 'sd')
    l2n.extract_devices(db.DeviceExtractorMOS3Transistor('MOS'), {'SD': sd, 'G': gate, 'P': P})
    for x in (sd, P, C, M1): l2n.connect(x)
    l2n.connect(sd, C); l2n.connect(P, C); l2n.connect(C, M1)
    t = l2n.make_text_layer(ly.layer(8, 25), 'T'); l2n.connect(M1, t)
    l2n.extract_netlist(); nl = l2n.netlist(); nl.combine_devices()
    c = nl.circuit_by_name(cell.name)
    devs = collections.Counter()
    for d in c.each_device():
        nets = sorted(((d.net_for_terminal('S').name or '?'), (d.net_for_terminal('D').name or '?')))
        devs[(round(d.parameter('W'), 2), round(d.parameter('L'), 2), d.net_for_terminal('G').name or '?', tuple(nets))] += 1
    return devs

CASES = [  # family, ng, l (um), frame, roles mode, gate net, replica net, rail
    ('P', 43, 0.6, '80u', 'single', 'a', 'dabp', 'iovdd'),
    ('N', 35, 1.0, '80u', 'pair', 'b', 'dabn', 'iovss'),
    ('N', 35, 1.0, '80u', None, 'gate', 'rep', 'iovss'),       # no roles: must equal wiring = internal
    ('P', 8, 0.6, 'fit', {0: 'rep', 1: 'dummy'}, 'gate', 'rep', 'iovdd'),
    ('N', 8, 0.64, 'fit', {2: 'dummy', 3: 'rep'}, 'gate', 'rep', 'iovss'),
]
for fam, ng, l, frame, mode, gnet, rnet, rail in CASES:
    lnm, width = int(round(l * 1000)), (80000 if frame == '80u' else None)
    roles = mode if isinstance(mode, dict) else (E.centre_roles(fam, ng, lnm, width, mode) if mode else {})
    rstr = ' '.join('%d:%s' % kv for kv in sorted(roles.items()))
    clamp = pcell('Clamp_%s_M1' % fam, dict(ng=ng, l='%gu' % l, frame=frame, wiring='external'))
    wire = pcell('Clamp_%s_M1_wiring' % fam, dict(ng=ng, l='%gu' % l, frame=frame, roles=rstr, gate_net=gnet, rep_net=rnet))
    both = flat([clamp, wire])
    errs = []
    # 1. against the engine
    eng = ly.create_cell('eng')
    s, t = E.generate_m1(fam, ng, lnm, width, 'external'); s2, t2 = E.generate_m1_wiring(fam, ng, lnm, width, roles, gnet, rnet)
    K.write_cell(ly, eng, s + s2, t + t2)
    La, Lb = layers_of(both), layers_of(eng)
    for k in set(La) | set(Lb):
        if not (La.get(k, db.Region()) ^ Lb.get(k, db.Region())).is_empty():
            errs.append('engine XOR on %s' % (k,))
    if texts_of(both) != texts_of(eng):
        errs.append('texts differ from the engine')
    # 2. no roles: equal to wiring = internal
    if not roles:
        intl = flat([pcell('Clamp_%s_M1' % fam, dict(ng=ng, l='%gu' % l, frame=frame))])
        Li = layers_of(intl)
        for k in set(La) | set(Li):
            if not (La.get(k, db.Region()) ^ Li.get(k, db.Region())).is_empty():
                errs.append('differs from internal on %s' % (k,))
        if texts_of(both) != texts_of(intl):
            errs.append('texts differ from internal')
    # 3. devices
    devs = extract(both, fam)
    wf = E.FAMILY[fam]['w_finger'] * E.FAMILY[fam]['n_dev'] / 1000.0
    n_rep = sum(1 for r in roles.values() if r == 'rep'); n_dum = sum(1 for r in roles.values() if r == 'dummy')
    w_out = sum(k[0] * v for k, v in devs.items() if k[2] == gnet and k[3] == tuple(sorted((rail, 'pad'))))
    w_rep = sum(k[0] * v for k, v in devs.items() if k[2] == rnet and set(k[3]) == {rail, rnet})
    w_dum = sum(k[0] * v for k, v in devs.items() if k[2] == rail and set(k[3]) == {rail, rnet})
    w_all = sum(k[0] * v for k, v in devs.items())
    exp = ((ng - n_rep - n_dum) * wf, n_rep * wf, n_dum * wf)
    if (round(w_out, 2), round(w_rep, 2), round(w_dum, 2)) != tuple(round(x, 2) for x in exp) or round(w_all, 2) != round(ng * wf, 2):
        errs.append('W out / rep / dummy %.2f / %.2f / %.2f, expected %.2f / %.2f / %.2f' % (w_out, w_rep, w_dum, *exp))
    if any(abs(k[1] - l) > 1e-6 for k in devs):
        errs.append('L not %g' % l)
    # 4. rules
    m1 = La.get((8, 0), db.Region())
    if m1.width_check(160).count() or m1.space_check(180).count():
        errs.append('M1 width / space')
    for ld in FORBIDDEN:
        if ld in La: errs.append('layer %s present' % (ld,))
    print('%s ng %d l %g %s roles {%s}: W out %.2f rep %.2f dummy %.2f -> %s' % (fam, ng, l, frame, rstr, w_out, w_rep, w_dum, 'ok' if not errs else '; '.join(errs)))
    fails += bool(errs)
    top.insert(db.CellInstArray(both.cell_index(), db.Trans()))
ly.write(sys.argv[1] if len(sys.argv) > 1 else 'wiring_cells.gds')
print('failures:', fails)
sys.exit(1 if fails else 0)
