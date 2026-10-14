# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Test DCNDiode / DCPDiode through the real PCell path (library SG13_cm_clamps).

    python3 test_diode.py [out.gds]          # default out.gds: diode_cells.gds

Needs the PDK found via $KLAYOUT_PATH or $PDKPATH (source .designinit), like
load_clamp_pcells.py, and reads $PDKPATH/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds.
1. l = 27.78 um: XOR per layer (merged) and all labels against IHP's
   sg13cmos5l_DCNDiode / sg13cmos5l_DCPDiode. Must be identical.
2. l = 0.58 um (minimum), 1.585 um (odd half length, label snapping), 27.78 um and
   74.505 um (longer than the widest clamp array): connectivity by klayout.db
   extraction (stripe net, frame net and guard net distinct, each one net once the
   two stripes are joined by name, as the straps above join them), stripe Activ
   area = 2 x 1.26 um x l, Recog.diode on the stripes, and the implant/well of
   stripes, frame and guard ring (N: n+ / p+ / n+ in NWell; P: p+ in NWell /
   n+ in NWell / p+).
3. l below the minimum and l off the 5 nm grid must give empty cells (the cni
   framework prints their tracebacks; that is expected).
Writes all cells into one GDS. Exit 1 on failure.
"""
import os, runpy, sys
import klayout.db as db
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # scripts/pcells
sys.path.insert(0, REPO)
runpy.run_path(os.path.join(REPO, 'load_clamp_pcells.py'))
import clamp_engine as E
from sg13cmos5l_pycell_lib.sg13_tech import SG13_Tech

LY = dict(activ=(1, 0), cont=(6, 0), m1=(8, 0), m1t=(8, 25), psd=(14, 0), nwell=(31, 0), recog=(99, 31))
ly = db.Layout(); ly.dbu = 0.001; ly.technology_name = SG13_Tech.TECH_NAME
top = ly.create_cell('TOP')
bad = 0


def pcell(fam, l, name):
    pc = ly.create_cell('DC%sDiode' % fam, 'SG13_cm_clamps', {'l': '%gu' % (l / 1000)})
    c = ly.create_cell(name)
    c.insert(db.CellInstArray(pc.cell_index(), db.Trans()))
    c.flatten(True)
    return c


def texts(layout, c):
    out = []
    for li in layout.layer_indexes():
        i = layout.get_info(li)
        out += [((i.layer, i.datatype), s.text.string, s.text.x, s.text.y) for s in c.shapes(li).each() if s.is_text()]
    return sorted(out)


print('== l = 27.78 um against IHP')
ref = db.Layout()
ref.read(os.path.join(os.environ['PDKPATH'], 'libs.ref', 'sg13cmos5l_io', 'gds', 'sg13cmos5l_io.gds'))
for fam in 'NP':
    a = ref.cell('sg13cmos5l_DC%sDiode' % fam)
    b = pcell(fam, 27780, 'DC%sDiode_ihp' % fam)
    keys = {(ref.get_info(li).layer, ref.get_info(li).datatype) for li in ref.layer_indexes() if not a.bbox_per_layer(li).empty()}
    keys |= {(ly.get_info(li).layer, ly.get_info(li).datatype) for li in ly.layer_indexes() if not b.bbox_per_layer(li).empty()}
    diff = [k for k in sorted(keys)
            if not (db.Region(a.begin_shapes_rec(ref.layer(*k))) ^ db.Region(b.begin_shapes_rec(ly.layer(*k)))).is_empty()]
    same_t = texts(ref, a) == texts(ly, b)
    bad += bool(diff) + (not same_t)
    print('  DC%sDiode  %d layers %s, labels %s' % (fam, len(keys), 'IDENTICAL' if not diff else 'DIFFER: %s' % diff,
                                                   'identical' if same_t else 'DIFFER'))


def check(fam, l, c):
    errs = []
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, c, []))
    r = {k: (l2n.make_text_layer(ly.layer(*v), k) if k == 'm1t' else l2n.make_polygon_layer(ly.layer(*v), k))
         for k, v in LY.items()}
    for x in (r['activ'], r['cont'], r['m1']):
        l2n.connect(x)
    l2n.connect(r['activ'], r['cont']); l2n.connect(r['cont'], r['m1']); l2n.connect(r['m1'], r['m1t'])
    stripe_net, bar_net = ('cathode', 'anode') if fam == 'N' else ('anode', 'cathode')
    l2n.join_net_names(stripe_net)
    l2n.extract_netlist()
    circ = l2n.netlist().circuit_by_name(c.name)
    named = {}
    for n in circ.each_net():
        if n.name:
            named.setdefault(n.name, []).append(n)
    if sorted(named) != ['anode', 'cathode', 'guard'] or any(len(v) > 1 for v in named.values()):
        errs.append('nets %s' % {k: len(v) for k, v in named.items()})
        return errs
    act = db.Region(c.begin_shapes_rec(ly.layer(1, 0)))
    reg = lambda k: db.Region(c.begin_shapes_rec(ly.layer(*LY[k])))
    psd, nwell, recog = reg('psd'), reg('nwell'), reg('recog')
    stripes = l2n.shapes_of_net(named[stripe_net][0], r['activ'], True)
    frame = l2n.shapes_of_net(named[bar_net][0], r['activ'], True)
    guard = l2n.shapes_of_net(named['guard'][0], r['activ'], True)
    if stripes.area() != 2 * 1260 * l:
        errs.append('stripe Activ area %d, expected %d' % (stripes.area(), 2 * 1260 * l))
    if not (stripes - recog).is_empty():
        errs.append('stripes not covered by Recog.diode')
    # (region, must be inside pSD, must be inside NWell); False = must be outside
    want = {'N': ((stripes, False, False), (frame, True, False), (guard, False, True)),
            'P': ((stripes, True, True), (frame, False, True), (guard, True, False))}[fam]
    for name, (reg_, in_psd, in_nw) in zip(('stripes', 'frame', 'guard'), want):
        for layer, inside, lname in ((psd, in_psd, 'pSD'), (nwell, in_nw, 'NWell')):
            ok = (reg_ - layer).is_empty() if inside else (reg_ & layer).is_empty()
            if not ok:
                errs.append('%s %s %s' % (name, 'not inside' if inside else 'overlaps', lname))
    return errs


print('== connectivity and implants')
y = 0
for fam in 'NP':
    x = 0
    for l in (E.DIODE_L_MIN, 1585, 27780, 74505):
        c = pcell(fam, l, 'DC%sDiode_l%d' % (fam, l))
        errs = check(fam, l, c)
        bad += bool(errs)
        bb = c.dbbox()
        print('  %-18s %6.2f x %5.2f um  %s' % (c.name, bb.width(), bb.height(), 'ok' if not errs else 'FAIL ' + '; '.join(errs)))
        top.insert(db.CellInstArray(c.cell_index(), db.Trans(x, y)))
        x += c.bbox().width() + 5000
    y += 20000

print('== error cases')
for fam, l in (('N', '0.575u'), ('P', '27.783u')):
    pc = ly.create_cell('DC%sDiode' % fam, 'SG13_cm_clamps', {'l': l})
    n = sum(pc.shapes(li).size() for li in ly.layer_indexes())
    bad += n != 0
    print('  DC%sDiode l=%s -> shapes: %d %s' % (fam, l, n, 'ok' if n == 0 else 'FAIL (expected an empty cell)'))

out = sys.argv[1] if len(sys.argv) > 1 else 'diode_cells.gds'
ly.write(out)
print('wrote', out, '| failures:', bad)
sys.exit(1 if bad else 0)
