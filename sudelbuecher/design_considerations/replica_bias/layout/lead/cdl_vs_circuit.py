"""Lead's own check: every non-dummy device in the layout agents' CDLs against the circuit netlists of pad_ref_rb
(multiset of model, {d,s}, g, b, w, l, ng; independent of the agents' device names). Dummies: listed with their nets.
usage: python3 -I cdl_vs_circuit.py <cdl> ...   (prints drawn vs. circuit, extras, missing)"""
import re, sys
from collections import Counter
from pathlib import Path
MAC = Path("/home/user/sg13cmos5l_cm_ip__single2diff2single/macros")
SRC = [MAC/"pad_ref_rb/netlist/source/pad_ref_rb.spice", MAC/"vcm_rb/netlist/source/vcm_rb.spice",
       MAC/"vref_s2d_rb/netlist/source/vref_s2d_rb.spice"]
SUBS = {"bias_tree_rb", "vcm_rb", "vref_s2d_rb", "bypass_rb"}   # port names = top net names (checked by hand)
def lines(p):
    return Path(p).read_text().replace("\n+", " ").splitlines()
def val(s):
    return float(s.replace("u", "e-6"))
def key(t, params):
    d, g, s, b, model = t[:5]
    return (model, tuple(sorted((d, s))), g, b, round(val(params["w"])*1e9), round(val(params["l"])*1e9), int(params.get("ng", 1)))
def parse(tokens):
    return dict(x.split("=", 1) for x in tokens if "=" in x)
circ, cdum, cur = Counter(), Counter(), None
mvals = {"{ncm}": 4, "{ncr}": 8}
for p in SRC:
    for ln in lines(p):
        t = ln.split()
        if not t or t[0].startswith("*"): continue
        if t[0].lower() == ".subckt": cur = t[1]; continue
        if t[0].lower() == ".ends": cur = None; continue
        if cur in SUBS and t[0].startswith("X") and "sg13_hv" in ln:
            pr = parse(t[6:]); k = key(t[1:6], pr); m = pr.get("m", "1"); m = mvals.get(m, None) or int(m)
            (cdum if t[0].startswith("XMD") else circ)[k] += m
drawn, ddum, where = Counter(), [], {}
for cdl in sys.argv[1:]:
    cell = None
    for ln in lines(cdl):
        t = ln.split()
        if not t or t[0].startswith("*"): continue
        if t[0].upper() == ".SUBCKT": cell = t[1]; continue
        if t[0].upper() == ".ENDS": continue
        if t[0][0] in "Mm":
            pr = parse(t[6:]); k = key(t[1:6], pr)
            d, g, s, b = t[1:5]
            if t[0].upper().startswith("MD"):
                ddum.append((cell, t[0], d, g, s, b, pr["w"], pr["l"], pr.get("ng", "1")))
            else:
                drawn[k] += int(pr.get("m", 1)); where.setdefault(k, []).append(f"{cell}:{t[0]}")
ok = sum((drawn & circ).values())
print(f"circuit: {sum(circ.values())} active devices (+ {sum(cdum.values())} netlisted dummies); drawn: {sum(drawn.values())} active; matched {ok}")
for k, n in sorted((drawn - circ).items()): print("  EXTRA   ", n, k, where[k])
for k, n in sorted((circ - drawn).items()): print("  MISSING ", n, k)
print(f"dummies drawn: {len(ddum)}")
for r in ddum: print("  ", *r, "" if (r[2] == r[4] == r[5]) else "  <-- d/s/b not on one rail")
