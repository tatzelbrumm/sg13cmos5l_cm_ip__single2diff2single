"""planted faults on a copy of the candidate (checker self-test, not a deliverable)"""
import sys, klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1]); t = ly.top_cell()
c = ly.create_cell('planted'); t.insert(db.CellInstArray(c.cell_index(), db.Trans()))
L = lambda l, d: ly.find_layer(l, d) if ly.find_layer(l, d) is not None else ly.layer(l, d)
B = lambda l, d, *b: c.shapes(L(l, d)).insert(db.DBox(*b))
B(10, 0, 75.15, 0.5, 75.6, 2.5)                      # 1 M2 0.15 from the pad bar (M2.b, M2.e)
B(29, 0, 6.48, 33.0, 6.67, 33.19)                    # 2 Via2 on an N strap in the rail gap (M3.c)
B(29, 0, 8.95, 45.0, 9.14, 45.19)                    # 3 Via2 from the P pad line k=0 into the iovss rail (short)
B(31, 0, 38.3, 45.0, 39.0, 46.0)                     # 4 floating NWell 0.33 from CMA's well (NW.b1)
B(6, 0, 3.98, 46.06, 4.14, 46.22)                    # 5 contact 0.05 from CMA's gate (Cnt.f, Cnt.b)
B(31, 0, 10, 120, 40, 130); B(1, 0, 11, 121, 39, 129); B(14, 0, 10.8, 120.8, 39.2, 129.2)   # 6 p+ in an untied NWell (LU.a)
B(8, 0, 10, 50.92, 12, 51.1)                         # 7 M1 0.10 above CMB/CMA head (M1.b)
B(8, 0, 60, 89, 62, 91); B(10, 0, 60, 89, 62, 91)    # 8 4 x 4 Via1 at 0.22 both ways (V1.b1)
for i in range(4):
    for j in range(4):
        B(19, 0, 60.2 + 0.41 * i, 89.2 + 0.41 * j, 60.39 + 0.41 * i, 89.39 + 0.41 * j)
o = db.SaveLayoutOptions(); o.write_context_info = True; ly.write(sys.argv[2], o)
