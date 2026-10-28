"""Negative test of oa_core_pd_drc.py: inject one violation per rule family far right of the block."""
import sys, klayout.db as db
H = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location("drc", H + "/../oa_core_pd_drc.py"); drc = importlib.util.module_from_spec(spec)
sys.argv = ["x", "x", "x"]; spec.loader.exec_module(drc)
ly = db.Layout(); ly.read(H + "/../oa_core_pd.gds"); top = ly.cell("oa_core_pd")
def B(l, d, x0, y0, x1, y1): top.shapes(ly.layer(l, d)).insert(db.DBox(x0, y0, x1, y1))
X = 120.0
expect = {}
# metal / via
B(8,0, X,0, X+0.12,2); expect["M1.a"]=1
B(8,0, X+1,0, X+1.29,2); B(8,0, X+1.44,0, X+1.73,2); expect["M1.b"]=1
B(10,0, X+3,0, X+3.15,2); expect["M2.a"]=1
B(10,0, X+4,0, X+4.29,2); B(10,0, X+4.47,0, X+4.76,2); expect["M2.b"]=1
B(8,0, X+6,0, X+7,3); B(8,0, X+7.2,0, X+7.49,3); expect["M1.e"]=1
B(10,0, X+9,0, X+10,3); B(10,0, X+10.22,0, X+10.51,3); expect["M2.e"]=1
B(19,0, X+12,0, X+12.2,0.2); B(8,0, X+11.9,-0.1, X+12.3,0.3); B(10,0, X+11.9,-0.1, X+12.3,1.0); expect["V1.a"]=1
B(19,0, X+13,0, X+13.19,0.19); B(8,0, X+12.9,-0.1, X+13.3,0.3); expect["M2.c/x"]=1
B(19,0, X+14,0, X+14.19,0.19); B(8,0, X+13.98,-0.02, X+14.21,0.21); B(10,0, X+13.9,-0.1,X+14.3,1); expect["V1.c1"]=1
B(10,0, X+15,0, X+15.29,0.29); expect["M2.d"]=1
B(8,0, X+16,0, X+16.29,0.29); expect["M1.d"]=1
B(8,2, X+17,0, X+17.3,0.3); expect["Pin.e"]=1
B(8,0, X+18.0025,0, X+18.3,1); expect["OffGrid"]=1
B(30,0, X+19,0, X+20,1); expect["M3+"]=1
B(32,0, X+21,0, X+22,1); expect["CMOS5L.FORB"]=1
# FEOL: two NWells 1.0 apart (unconnected = different nets), TGO 0.5 apart, Activ 0.15 apart
B(31,0, X,10, X+2,12); B(31,0, X+3,10, X+5,12); expect["NW.b1"]=1
B(44,0, X+7,10, X+9,12); B(44,0, X+9.5,10, X+11.5,12); expect["TGO.e"]=1
B(1,0, X+13,10, X+14,11); B(1,0, X+14.15,10, X+15,11); expect["Act.b"]=1
B(6,0, X+16,10, X+16.16,10.16); expect["Cnt.g"]=1; expect["Cnt.h"]=1
# PMOS in NWell + TGO with L = 0.3, no NWell tie (LU.a), and an NMOS with no substrate tie (LU.b)
B(31,0, X,20, X+6,26); B(44,0, X+0.7,20.7, X+5.3,25.3); B(14,0, X+1,21, X+5,25); B(1,0, X+1.5,22, X+4.5,24); B(5,0, X+2.85,21.5, X+3.15,24.5)
expect["Gat.a4"]=1; expect["LU.a"]=1
B(44,0, X+10,20, X+15,25); B(1,0, X+11,21, X+14,24); B(5,0, X+12.25,20.5, X+12.75,24.5); expect["LU.b"]=1
# antenna: 1 x 0.45 HV NMOS gate (inside the LU.b test device) tied to a 60 um2 M2 plate through poly contact
B(5,0, X+12.25,24.5, X+12.75,26.5); B(6,0, X+12.42,25.92, X+12.58,26.08); B(8,0, X+12.2,25.8, X+12.8,26.2)
B(19,0, X+12.405,25.905, X+12.595,26.095); B(10,0, X+12.2,25.8, X+40,37)
G = H + "/drc_selftest.gds"; ly.write(G)
res = drc.run(G, "oa_core_pd")
got = {r[0]: r[3] for r in res}
ant = drc.antenna(G, "oa_core_pd"); __import__("os").remove(G)
ok = True
for k in expect:
    print("%-12s expected >=1, got %d %s" % (k, got.get(k, -1), "ok" if got.get(k, 0) >= 1 else "MISSED"))
    ok &= got.get(k, 0) >= 1
print("other rules firing:", {k: v for k, v in got.items() if v and k not in expect})
print("antenna:", [a for a in ant if a[2] >= 200])
print("ALL INJECTED VIOLATIONS FOUND" if ok else "SOME MISSED")
