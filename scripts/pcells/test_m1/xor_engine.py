# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
XOR the PCell output of test_m1.py against the pure engine (clamp_engine.generate_m1),
per layer, for every <F>_M1_ng<ng>_l<l>[_w80] cell.

    python3 xor_engine.py [m1_cells.gds]

Then the 80 um frame "as before": Clamp_N_M1 / Clamp_P_M1 with frame 80u and l = 0.6 um
must equal Clamp_N / Clamp_P (tie D, same ng) on Activ, pSD, GatPoly, ThickGateOx,
NWell, Substrate and the array contacts, apart from the antenna diode they omit.

No PDK needed. Exit 1 on any mismatch.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # scripts/pcells
import klayout.db as db
import clamp_engine as E, clamp_klayout as K
a = db.Layout(); a.read(sys.argv[1] if len(sys.argv) > 1 else 'm1_cells.gds')
b = db.Layout(); b.dbu = 0.001
bad = 0
for c in a.each_cell():
    m = re.fullmatch(r'([NP])_M1_ng(\d+)_l(\d+)(_w80)?', c.name)
    if not m: continue
    s, t = E.generate_m1(m.group(1), int(m.group(2)), int(m.group(3)), 80000 if m.group(4) else None)
    cb = K.write_cell(b, b.create_cell(c.name), s, t)
    for li in a.layer_indexes():
        info = a.get_info(li)
        ra = db.Region(c.begin_shapes_rec(li)); rb = db.Region(cb.begin_shapes_rec(b.layer(info.layer, info.datatype)))
        if not (ra ^ rb).is_empty(): bad += 1; print('XOR', c.name, info)
print('XOR mismatches:', bad)

from clamp_refdata import REFDATA
for fam in 'NP':
    for ng in (1, 2, 8, 15, E.max_ng(fam, 'D', REFDATA)):
        ca = K.write_cell(b, b.create_cell('ihp'), *E.generate(fam, ng, 'D', REFDATA)[:2])
        cb = K.write_cell(b, b.create_cell('m1'), *E.generate_m1(fam, ng, 600, 80000))
        diode = db.Region(ca.begin_shapes_rec(b.layer(99, 31))).sized(500)
        h = E.FAMILY[fam]['height']
        for ld, keep in (((1, 0), None), ((14, 0), None), ((5, 0), None), ((44, 0), None), ((31, 0), None),
                         ((40, 0), None), ((6, 0), db.Box(2140, 2140, 77860, h - 2140))):   # Cont: inside the inner ring
            li = b.layer(*ld)
            x = (db.Region(ca.begin_shapes_rec(li)) ^ db.Region(cb.begin_shapes_rec(li))) - diode
            if keep:
                x &= db.Region(keep)
            if not x.is_empty():
                bad += 1; print('80u vs Clamp_%s ng=%d differs on %d/%d' % ((fam, ng) + ld))
print('after the 80 um frame comparison, mismatches:', bad)
sys.exit(1 if bad else 0)
