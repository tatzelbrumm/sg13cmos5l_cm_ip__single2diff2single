# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Test Clamp_N_M1 / Clamp_P_M1 through the real PCell path (library SG13_cm_clamps).

    python3 test_m1.py [out.gds]          # default out.gds: m1_cells.gds

Needs the PDK found via $KLAYOUT_PATH or $PDKPATH (source .designinit), like
load_clamp_pcells.py. For N and P x ng 1, 2, 3, 8 x l = Lmin, Lmin + 5 nm, 0.6, 0.64, 1.0 um
(frame 'fit'), and ng 1, 3, 49 x l = Lmin + 5 nm, 0.6 um (frame '80u', 49 is the largest
ng that fits at 0.6 um): no layer above M1, Activ bbox as expected, array centred in the
80 um frame, gate contacts side by side as fit (1 below l = 0.64 um, 2 from 0.64,
3 from 0.98 um), and a klayout.db extraction (as in
lvs_clamp.py) giving one MOS with W = 4.4*ng (N) / 13.32*ng (P) um and L = l,
S on the rail, D on 'pad', G on 'gate'. Then four bad parameter sets, which must
give empty cells (the cni framework prints their tracebacks; that is expected).
Writes all cells into one GDS for xor_engine.py and the DRC run. Exit 1 on failure.
"""
import os, runpy, sys
import klayout.db as db
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # scripts/pcells
sys.path.insert(0, REPO)
runpy.run_path(os.path.join(REPO, 'load_clamp_pcells.py'))
import clamp_engine as E
from sg13cmos5l_pycell_lib.sg13_tech import SG13_Tech

L = dict(activ=(1, 0), poly=(5, 0), cont=(6, 0), m1=(8, 0), m1p=(8, 2), m1t=(8, 25), psd=(14, 0),
         nwell=(31, 0), tgo=(44, 0), sub=(40, 0), text=(63, 0))
FORBIDDEN = [(10, 0), (10, 2), (10, 25), (19, 0), (29, 0), (30, 0), (99, 31), (128, 0)]

ly = db.Layout(); ly.dbu = 0.001; ly.technology_name = SG13_Tech.TECH_NAME
top = ly.create_cell('TOP')

def check(fam, ng, l, width, cell):
    errs = []
    W = Lg = 0.0
    for ld in FORBIDDEN:
        li = ly.find_layer(*ld)
        if li is not None and not cell.bbox_per_layer(li).empty():
            errs.append('layer %s present' % (ld,))
    cw = width or E.array_extent(ng, l, 0)[1] + 2 * E.ARRAY_X0     # cell width (outer ring Activ)
    bb = cell.dbbox()
    act = cell.bbox_per_layer(ly.layer(1, 0))
    if (act.left, act.bottom, act.right, act.top) != (0, 0, cw, E.FAMILY[fam]['height']):
        errs.append('Activ bbox %s' % act)
    n_gc = (l - 2 * E.GATE_ENC - E.CONT) // E.CONT_PITCH + 1       # gate contacts side by side
    gc = db.Region(cell.begin_shapes_rec(ly.layer(6, 0))).interacting(db.Region(cell.begin_shapes_rec(ly.layer(5, 0))))
    if gc.count() != ng * len(E.FAMILY[fam]['gate_cont']) * n_gc:
        errs.append('%d gate contacts, expected %d' % (gc.count(), ng * len(E.FAMILY[fam]['gate_cont']) * n_gc))
    tgo = cell.bbox_per_layer(ly.layer(44, 0))                      # = array +- 0.34 um
    if width and abs(tgo.left + tgo.right - width) > 2 * E.GRID:
        errs.append('array not centred: ThickGateOx %d..%d nm' % (tgo.left, tgo.right))
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, cell, []))
    r = {k: (l2n.make_text_layer(ly.layer(*v), k) if k == 'm1t' else l2n.make_polygon_layer(ly.layer(*v), k))
         for k, v in L.items()}
    gate = (r['poly'] & r['activ']) - r['psd'] - r['nwell'] if fam == 'N' else r['poly'] & r['activ'] & r['psd'] & r['nwell']
    sd = r['activ'] - r['poly']
    l2n.register(gate, 'gate'); l2n.register(sd, 'sd')
    l2n.extract_devices(db.DeviceExtractorMOS3Transistor('MOS'), {'SD': sd, 'G': gate, 'P': r['poly']})
    for x in (sd, r['poly'], r['cont'], r['m1']):
        l2n.connect(x)
    l2n.connect(sd, r['cont']); l2n.connect(r['poly'], r['cont']); l2n.connect(r['cont'], r['m1'])
    l2n.connect(r['m1'], r['m1t'])
    l2n.join_net_names('pad')          # drain columns: joined above the cell
    l2n.extract_netlist()
    nl = l2n.netlist(); nl.combine_devices()
    circ = nl.circuit_by_name(cell.name)
    named = {}
    for n in circ.each_net():
        if n.name:
            named.setdefault(n.name, []).append(n)
    rail = 'iovss' if fam == 'N' else 'iovdd'
    want = {'pad', 'gate', 'iovss'} | ({'iovdd'} if fam == 'P' else set())
    if set(named) != want:
        errs.append('named nets %s, expected %s' % (sorted(named), sorted(want)))
    for k, v in named.items():
        if len(v) > 1:
            errs.append("'%s' on %d nets" % (k, len(v)))
    mos = list(circ.each_device())
    if len(mos) != 1:
        errs.append('%d MOS after combining' % len(mos))
    w_exp = E.FAMILY[fam]['w_finger'] * E.FAMILY[fam]['n_dev'] * ng * 1e-3
    for d in mos[:1]:
        W, Lg = d.parameter('W'), d.parameter('L')
        nm = lambda t: (d.net_for_terminal(t).name or '?')
        if {nm('S'), nm('D')} != {'pad', rail} or nm('G') != 'gate':
            errs.append('MOS S/D/G = %s/%s/%s' % (nm('S'), nm('D'), nm('G')))
        if abs(W - w_exp) > 1e-6 or abs(Lg - l / 1000) > 1e-6:
            errs.append('W=%.3f L=%.3f, expected %.3f %.3f' % (W, Lg, w_exp, l / 1000))
    unnamed = [n for n in circ.each_net() if not n.name]
    return errs, W, Lg, len(unnamed), bb

y = 0
bad = 0
for fam, lmin in (('N', 450), ('P', 400)):
    x = 0
    cases = [(l, ng, 'fit') for l in (lmin, lmin + 5, 600, 640, 1000) for ng in (1, 2, 3, 8)]
    cases += [(l, ng, '80u') for l in (lmin + 5, 600) for ng in (1, 3, 49)]
    for l, ng, frame in cases:
        pc = ly.create_cell('Clamp_%s_M1' % fam, 'SG13_cm_clamps', {'ng': ng, 'l': '%gu' % (l / 1000), 'frame': frame})
        c = ly.create_cell('%s_M1_ng%d_l%d%s' % (fam, ng, l, '_w80' if frame == '80u' else ''))
        c.insert(db.CellInstArray(pc.cell_index(), db.Trans()))
        c.flatten(True)
        errs, W, Lg, nun, bb = check(fam, ng, l, 80000 if frame == '80u' else None, c)
        bad += bool(errs)
        print('%-22s %5.2f x %5.2f um  W=%7.3f L=%.3f  unnamed nets %d  %s'
              % (c.name, bb.width(), bb.height(), W, Lg, nun, 'ok' if not errs else 'FAIL ' + '; '.join(errs)))
        top.insert(db.CellInstArray(c.cell_index(), db.Trans(x, y)))
        x += int(bb.width() * 1000) + 5000
    y += 30000

print('== error cases')
for fam, p in (('N', {'ng': 2, 'l': '0.4u'}), ('P', {'ng': 2, 'l': '0.603u'}), ('N', {'ng': 0, 'l': '0.6u'}),
               ('P', {'ng': 50, 'l': '0.6u', 'frame': '80u'})):
    pc = ly.create_cell('Clamp_%s_M1' % fam, 'SG13_cm_clamps', p)
    n = sum(pc.shapes(li).size() for li in ly.layer_indexes())
    bad += n != 0
    print(' ', fam, p, '-> shapes:', n, 'ok' if n == 0 else 'FAIL (expected an empty cell)')
out = sys.argv[1] if len(sys.argv) > 1 else 'm1_cells.gds'
ly.write(out)
print('wrote', out, '| failures:', bad)
sys.exit(1 if bad else 0)
