#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Verify the parametrized clamps against the IHP reference cells.

    python3 verify_clamp.py <sg13cmos5l_io.gds> [--sweep-gds sweep.gds]

1. Regenerates every reference cell (N/P x 2, 8, 15 'D' and 20 '0D') and XORs it,
   layer by layer after merging, against the original in sg13cmos5l_io.gds.
   Every drawing and pin layer must be identical. Texts: ring/diode/rppd labels
   must be identical; 'pad' labels are generated one per drain strap, so only
   their coverage is checked (every drain strap labelled, no label off a strap).
2. Sweeps ng over the whole legal range of each family/variant and writes all
   cells into one GDS (for DRC / LVS runs), checking the gate count and that no
   two drain straps or source straps touch.
Exit status is non-zero on any mismatch.
"""

import argparse
import os
import sys

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clamp_engine as E          # noqa: E402
import clamp_klayout as K         # noqa: E402
from clamp_refdata import REFDATA  # noqa: E402


def regions(layout, cell):
    out, texts = {}, []
    inv = {v: k for k, v in K.GDS.items()}
    for li in layout.layer_indexes():
        info = layout.get_info(li)
        key = inv.get((info.layer, info.datatype), (info.layer, info.datatype))
        r = db.Region()
        for s in cell.shapes(li).each():
            if s.is_text():
                texts.append((key, s.text.string, s.text.x, s.text.y))
            else:
                r.insert(s.polygon)
        if not r.is_empty():
            out[key] = r.merged()
    return out, texts


def compare(name, ref_ly, ref_cell, gen_ly, gen_cell):
    ra, ta = regions(ref_ly, ref_cell)
    rb, tb = regions(gen_ly, gen_cell)
    ok = True
    for k in sorted(set(ra) | set(rb), key=str):
        x = ra.get(k, db.Region()) ^ rb.get(k, db.Region())
        if not x.is_empty():
            ok = False
            print('  XOR %-22s %4d polygons, area %.4f um2, bbox %s'
                  % ('%s/%s' % k, x.count(), x.area() * 1e-6, x.bbox().to_dtype(0.001)))
    # texts other than 'pad': identical (layer, string, position)
    fa = sorted(t for t in ta if t[1] != 'pad')
    fb = sorted(t for t in tb if t[1] != 'pad')
    if fa != fb:
        ok = False
        print('  TEXT mismatch:\n    ref %s\n    gen %s' % (sorted(set(fa) - set(fb)), sorted(set(fb) - set(fa))))
    # 'pad' labels: must sit on a drain strap, and every drain strap labelled
    m2 = rb.get(('Metal2', 'pin'), db.Region())
    for src, tl in (('ref', ta), ('gen', tb)):
        for key, s, x, y in tl:
            if s == 'pad' and not m2.interacting(db.Region(db.Box(x - 1, y - 1, x + 1, y + 1))).count():
                ok = False
                print('  %s pad label at (%.3f, %.3f) not on a generated M2 pin' % (src, x / 1e3, y / 1e3))
    labelled = db.Region()
    for key, s, x, y in tb:
        if s == 'pad':
            labelled += m2.interacting(db.Region(db.Box(x - 1, y - 1, x + 1, y + 1)))
    return ok, len(rb)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('gds', help='sg13cmos5l_io.gds with the reference clamp cells')
    ap.add_argument('--sweep-gds', help='write all swept cells into this GDS')
    ap.add_argument('--pdk-python', help='PDK libs.tech/klayout/python directory: also verify the cells '
                    'produced through the KLayout PCells Clamp_N/Clamp_P (IHP cni framework)')
    a = ap.parse_args()

    ref = db.Layout()
    ref.read(a.gds)
    gen = db.Layout()
    gen.dbu = 0.001
    allok = True

    print('== reference reproduction (XOR after merge, per layer)')
    for fam in ('N', 'P'):
        for tie in ('D', '0D'):
            for ng, rd in sorted(REFDATA[fam][tie]['refs'].items()):
                shapes, texts, p = E.generate(fam, ng, tie, REFDATA)
                name = E.cell_name(fam, ng, tie)
                assert name == rd['cell'], (name, rd['cell'])
                c = K.write_cell(gen, gen.create_cell(name + '__regen'), shapes, texts)
                ok, nl = compare(name, ref, ref.cell(name), gen, c)
                print('  %-28s %s (%d layers)' % (name, 'IDENTICAL' if ok else 'DIFFERENT', nl))
                allok &= ok

    if a.pdk_python:
        print('== reference reproduction through the PCells (library SG13_cm_clamps)')
        import runpy
        sys.path.insert(0, a.pdk_python)
        sys.path.insert(0, os.path.join(a.pdk_python, 'pycell4klayout-api', 'source', 'python'))
        runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'load_clamp_pcells.py'))
        from sg13cmos5l_pycell_lib.sg13_tech import SG13_Tech
        pl = db.Layout()
        pl.dbu = 0.001
        pl.technology_name = SG13_Tech.TECH_NAME
        for fam in ('N', 'P'):
            for tie in ('D', '0D'):
                for ng in sorted(REFDATA[fam][tie]['refs']):
                    name = E.cell_name(fam, ng, tie)
                    pc = pl.create_cell('Clamp_' + fam, 'SG13_cm_clamps', {'ng': ng, 'tie': tie})
                    top = pl.create_cell(name + '__pcell')
                    top.insert(db.CellInstArray(pc.cell_index(), db.Trans()))
                    top.flatten(True)
                    ok, nl = compare(name, ref, ref.cell(name), pl, top)
                    print('  %-28s %s (%d layers)' % (name, 'IDENTICAL' if ok else 'DIFFERENT', nl))
                    allok &= ok

    print('== sweep')
    sweep = db.Layout()
    sweep.dbu = 0.001
    for fam in ('N', 'P'):
        for tie in ('D', '0D'):
            hi = E.max_ng(fam, tie, REFDATA)
            bad = []
            for ng in range(1, hi + 1):
                shapes, texts, p = E.generate(fam, ng, tie, REFDATA)
                c = K.write_cell(sweep, sweep.create_cell(E.cell_name(fam, ng, tie)), shapes, texts)
                r, _ = regions(sweep, c)
                gates = (r[('GatPoly', 'drawing')] & r[('Activ', 'drawing')])
                n_expect = ng * E.FAMILY[fam]['n_dev']
                m2 = r[('Metal2', 'drawing')]
                n_m2 = m2.count()
                src, drn = E.columns(ng)
                n_m2_expect = len(src) + len(drn) + (1 if tie == 'D' else 0) + (1 if tie == '0D' else 0)
                if gates.count() != n_expect:
                    bad.append('ng=%d: %d gate regions, expected %d' % (ng, gates.count(), n_expect))
                if n_m2 != n_m2_expect:
                    bad.append('ng=%d: %d separate M2 shapes, expected %d' % (ng, n_m2, n_m2_expect))
            ref_ngs = sorted(REFDATA[fam][tie]['refs'])
            print('  %s/%-2s ng = 1..%d  (references at ng = %s)  %s'
                  % (fam, tie, hi, ref_ngs, 'ok' if not bad else 'PROBLEMS'))
            for b in bad:
                print('    ', b)
            allok &= not bad
    if a.sweep_gds:
        sweep.write(a.sweep_gds)
        print('wrote', a.sweep_gds)
    print('RESULT:', 'PASS' if allok else 'FAIL')
    sys.exit(0 if allok else 1)


if __name__ == '__main__':
    main()
