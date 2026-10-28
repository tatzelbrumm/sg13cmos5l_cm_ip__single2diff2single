"""Negative LVS test: an injected M2 short (vbr - vpc) and an open (vnc drop onto nmir removed) must fail."""
import os, subprocess, sys, klayout.db as db
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(H, "..")
for case in ("short", "open"):
    ly = db.Layout(); ly.read(os.path.join(O, "oa_core_pd.gds")); top = ly.cell("oa_core_pd")
    if case == "short":
        top.shapes(ly.layer(10, 0)).insert(db.DBox(60.0, 31.8, 60.29, 32.6))
    else:
        m1 = top.shapes(ly.layer(8, 0))
        for s in list(m1.each()):
            if abs(s.dbbox().center().x - 52.35) < 0.01 and s.dbbox().height() > 2:
                m1.erase(s)
    g = os.path.join(H, "lvs_neg_%s.gds" % case); ly.write(g)
    r = subprocess.run([sys.executable, os.path.join(O, "oa_core_pd_lvs.py"), g, "oa_core_pd", os.path.join(O, "oa_core_pd.cdl")],
                       capture_output=True, text=True)
    print("%-5s exit %d | %s" % (case, r.returncode, " | ".join(r.stdout.splitlines()[:3])))
    os.remove(g)
