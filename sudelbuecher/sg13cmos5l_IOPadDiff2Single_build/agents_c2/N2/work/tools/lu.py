"""lu.py <gds> cells...: farthest N+ Activ (Activ not under pSD) from the nearest p+ tie (Activ under pSD)"""
import sys
import klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1]); u = ly.dbu
for name in sys.argv[2:]:
    c = ly.cell(name)
    act = db.Region(c.begin_shapes_rec(ly.find_layer(1, 0))).merged()
    psd = db.Region(c.begin_shapes_rec(ly.find_layer(14, 0))).merged()
    tie, nact = act & psd, act - psd
    lo, hi = 0, 40000
    while hi - lo > 10:
        m = (lo + hi) // 2
        if (nact - tie.sized(m, m, 2)).is_empty():
            hi = m
        else:
            lo = m
    print("%-18s farthest N+ Activ from a tie: %.2f um (LU_b 20)" % (name, hi * u))
