# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Engine-only GDS for a DRC run, no PDK needed: the same 44 Clamp_N_M1 / Clamp_P_M1
cells as test_m1.py (40 frame 'fit', 12 frame '80u'), plus Clamp_N / Clamp_P ng = 8 (identical to IHP's N8N8D /
P8N8D) as a baseline, and DCNDiode / DCPDiode at l = 0.58, 1.585, 27.78 (= IHP's
cells) and 74.505 um, all placed in top cell TOP.

    python3 drc_gds.py m1_drc.gds
    python3 $PDKPATH/libs.tech/klayout/tech/drc/run_drc.py --path=m1_drc.gds --topcell=TOP --run_mode=flat --no_density --run_dir=drc_run

Result on 2026-10-14 (KLayout 0.30.0, unmodified deck, main + maximal tables):
547 rule categories, 0 violations. Re-run 2026-10-15 with the adaptive gate
contacts (l = 0.64 um added): 0 violations.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # scripts/pcells
import klayout.db as db, clamp_engine as E, clamp_klayout as K
from clamp_refdata import REFDATA
ly = db.Layout(); ly.dbu = 0.001
top = ly.create_cell('TOP'); y = 0
for fam, lmin in (('N', 450), ('P', 400)):
    x = 0
    for l in (lmin, lmin + 5, 600, 640, 1000):
        for ng in (1, 2, 3, 8):
            c = K.write_cell(ly, ly.create_cell('%s_M1_ng%d_l%d' % (fam, ng, l)), *E.generate_m1(fam, ng, l))
            top.insert(db.CellInstArray(c.cell_index(), db.Trans(x, y))); x += c.bbox().width() + 5000
    for l in (lmin + 5, 600):
        for ng in (1, 3, 49):
            c = K.write_cell(ly, ly.create_cell('%s_M1_ng%d_l%d_w80' % (fam, ng, l)), *E.generate_m1(fam, ng, l, 80000))
            top.insert(db.CellInstArray(c.cell_index(), db.Trans(x, y))); x += c.bbox().width() + 5000
    s, t, p = E.generate(fam, 8, 'D', REFDATA)      # IHP-identical reference, as DRC baseline
    c = K.write_cell(ly, ly.create_cell(E.cell_name(fam, 8, 'D')), s, t)
    top.insert(db.CellInstArray(c.cell_index(), db.Trans(x, y)))
    y += 30000
for fam in 'NP':                                   # DC diodes; l = 27.78 um is IHP's cell
    x = 0
    for l in (E.DIODE_L_MIN, 1585, 27780, 74505):
        c = K.write_cell(ly, ly.create_cell('DC%sDiode_l%d' % (fam, l)), *E.generate_diode(fam, l))
        top.insert(db.CellInstArray(c.cell_index(), db.Trans(x, y))); x += c.bbox().width() + 5000
    y += 20000
ly.write(sys.argv[1]); print('cells', ly.cells())
