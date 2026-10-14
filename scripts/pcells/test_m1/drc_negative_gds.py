# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Negative control for the DRC run: proof that the deck sees these cells. Writes
three deliberately broken cells into top cell TOP:
  N_m1_spacing      Clamp_N_M1 ng=2 with an extra M1 box 0.1 um from a drain column
  N/P_ring_too_close  the array 0.21 um from the inner ring instead of 0.61 um

    python3 drc_negative_gds.py m1_neg.gds
    python3 $PDKPATH/libs.tech/klayout/tech/drc/run_drc.py --path=m1_neg.gds --topcell=TOP --run_mode=flat --no_density --run_dir=drc_neg

Result on 2026-10-14: M1.b x 2 and pSD.d x 2. A clean run here means the deck is broken.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # scripts/pcells
import klayout.db as db, clamp_engine as E, clamp_klayout as K
ly = db.Layout(); ly.dbu = 0.001; top = ly.create_cell('TOP')
c = K.write_cell(ly, ly.create_cell('N_m1_spacing'), *E.generate_m1('N', 2, 600))
_, drn = E.columns(2, 600, E.ARRAY_X0)
c.shapes(ly.layer(8, 0)).insert(db.Box(drn[0] + 310 + 100, 4000, drn[0] + 310 + 400, 5000))   # M1 100 nm from drain
top.insert(db.CellInstArray(c.cell_index(), db.Trans()))
E.ARRAY_X0 = 2750 - 400            # array 0.21 um from the inner ring instead of 0.61
for fam in 'NP':
    c = K.write_cell(ly, ly.create_cell('%s_ring_too_close' % fam), *E.generate_m1(fam, 2, 600))
    top.insert(db.CellInstArray(c.cell_index(), db.Trans(20000 * (1 + 'NP'.index(fam)), 0)))
ly.write(sys.argv[1])
