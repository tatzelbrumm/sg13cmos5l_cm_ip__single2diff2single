"""Lead's check of agent D's flat CDL of bias_dist_pd against the source netlist (+ hv_logic gates flattened): device
multiset of model, {d,s}, g, b, W, L, with vdd -> vddh, vss -> vssh, gate-internal nets named <instance>_<net>.
usage: python3 -I bdp_vs_circuit.py <cdl>"""
import sys
from collections import Counter
from pathlib import Path
MAC = Path("/home/user/sg13cmos5l_cm_ip__single2diff2single/macros")
def lines(p): return Path(p).read_text().replace("\n+", " ").splitlines()
def par(ts): return dict(x.split("=", 1) for x in ts if "=" in x)
def v(s): return round(float(s.replace("u", "e-6")) * 1e9)
gates, cur = {}, None
for ln in lines(MAC / "hv_logic/netlist/source/hv_logic.spice"):
    t = ln.split()
    if not t or t[0].startswith("*"): continue
    if t[0] == ".subckt": cur = t[1]; gates[cur] = (t[2:], []); continue
    if t[0] == ".ends": cur = None; continue
    if cur: gates[cur][1].append(t)
ren = {"vdd": "vddh", "vss": "vssh"}
circ = Counter()
def add(t, m):
    d, g, s, b = [m(x) for x in t[1:5]]; p = par(t[6:])
    circ[(t[5], tuple(sorted((d, s))), g, b, v(p["w"]), v(p["l"]))] += 1
cur = None
for ln in lines(MAC / "bias_dist_pd/netlist/source/bias_dist_pd.spice"):
    t = ln.split()
    if not t or t[0].startswith("*"): continue
    if t[0] == ".subckt": cur = t[1]; continue
    if t[0] == ".ends": cur = None; continue
    if cur != "bias_dist_pd" or not t[0].startswith("X"): continue
    if "sg13_hv" in ln:
        if t[0].startswith("XMD"): continue          # layout dummies in the source (since 2026-11-07): listed from the CDL
        add(t, lambda x: ren.get(x, x))
    else:
        ports, devs = gates[t[-1]]
        conn = dict(zip(ports, [ren.get(x, x) for x in t[1:-1]]))
        for d in devs:
            add(d, lambda x, i=t[0]: conn.get(x, f"{i}_{x}"))
lay, dum = Counter(), []
for ln in lines(sys.argv[1]):
    t = ln.split()
    if t and t[0][0] in "Mm":
        p = par(t[6:]); k = (t[5], tuple(sorted((t[1], t[3]))), t[2], t[4], v(p["w"]), v(p["l"]))
        if "MD" in t[0].upper(): dum.append((t[0], *t[1:6], p["w"], p["l"]))
        else: lay[k] += int(p.get("m", 1))
print("circuit", sum(circ.values()), "cdl active", sum(lay.values()), "matched", sum((circ & lay).values()), "dummies", len(dum))
for k, n in (lay - circ).items(): print("  EXTRA  ", n, k)
for k, n in (circ - lay).items(): print("  MISSING", n, k)
for d in dum: print("  dummy", *d)
