"""Lead's check of a flat CDL of pad_ref_rb against the circuit netlists: every device (actives and dummies) as a
multiset of model, {d,s}, g, b, W, L, ng after vddh -> vdd, vssh -> vss and the flattener's instance prefixes (c_, r_, t_, b_) removed from internal nets. usage: python3 -I flat_vs_circuit.py <cdl>"""
import sys
from collections import Counter
from pathlib import Path
MAC = Path("/home/user/sg13cmos5l_cm_ip__single2diff2single/macros")
SRC = [MAC/"pad_ref_rb/netlist/source/pad_ref_rb.spice", MAC/"vcm_rb/netlist/source/vcm_rb.spice",
       MAC/"vref_s2d_rb/netlist/source/vref_s2d_rb.spice"]
M = {"{ncm}": 4, "{ncr}": 9}
ren = {"vddh": "vdd", "vssh": "vss"}
def v(s): return round(float(s.replace("u", "e-6")) * 1e9)
def key(t, p):
    d, g, s, b, model = [ren.get(x, x[2:] if x[:2] in ("c_", "r_", "t_", "b_") else x) for x in t[:4]] + [t[4]]
    return (model, tuple(sorted((d, s))), g, b, v(p["w"]), v(p["l"]), int(p.get("ng", 1)))
def par(ts): return dict(x.split("=", 1) for x in ts if "=" in x)
circ, cur = Counter(), None
for f in SRC:
    for ln in f.read_text().replace("\n+", " ").splitlines():
        t = ln.split()
        if not t or t[0].startswith("*"): continue
        if t[0].lower() == ".subckt": cur = t[1]; continue
        if t[0].lower() == ".ends": cur = None; continue
        if cur in ("bias_tree_rb", "vcm_rb", "vref_s2d_rb", "bypass_rb") and t[0].startswith("X") and "sg13_hv" in ln:
            p = par(t[6:]); m = p.get("m", "1"); circ[key(t[1:6], p)] += M.get(m) or int(m)
lay = Counter()
for ln in Path(sys.argv[1]).read_text().replace("\n+", " ").splitlines():
    t = ln.split()
    if t and t[0][0] in "Mm":
        p = par(t[6:]); lay[key(t[1:6], p)] += int(p.get("m", 1))
print("circuit", sum(circ.values()), "cdl", sum(lay.values()), "matched", sum((circ & lay).values()))
for k, n in (lay - circ).items(): print("  EXTRA  ", n, k)
for k, n in (circ - lay).items(): print("  MISSING", n, k)
