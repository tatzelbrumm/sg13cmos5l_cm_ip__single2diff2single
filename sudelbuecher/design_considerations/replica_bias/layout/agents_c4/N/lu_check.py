# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""lu_check.py <gds> <cell>...: farthest N+ Activ (Activ not under pSD) from the p+ tie Activ (Activ under pSD):
the smallest isotropic growth of the tie that covers every N+ Activ, bisection to 0.01 um (C3's measure; LU.b 20 um,
SG13CMOS5L_os_layout_rules.txt section 7.2.2)."""
import sys
import klayout.db as db

ly = db.Layout()
ly.read(sys.argv[1])
u = ly.dbu
for name in sys.argv[2:]:
    c = ly.cell(name)
    act = db.Region(c.begin_shapes_rec(ly.find_layer(1, 0))).merged()
    psd = db.Region(c.begin_shapes_rec(ly.find_layer(14, 0))).merged()
    tie, nact = act & psd, act - psd
    lo, hi = 0.0, 40.0
    while hi - lo > 0.01:
        mid = (lo + hi) / 2
        grown = tie.sized(int(round(mid / u)), int(round(mid / u)), 2)
        lo, hi = (lo, mid) if (nact - grown).is_empty() else (mid, hi)
    print("%-12s farthest N+ to tie %6.2f um (LU.b 20)" % (name, hi))
