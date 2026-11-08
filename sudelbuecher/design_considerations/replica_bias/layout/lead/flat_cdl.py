"""Flatten a hierarchical SPICE source (X instances of subckts, X devices sg13_hv_*) into a flat CDL (M devices) of one
top subckt, for LVS against a layout. usage: python3 -I flat_cdl.py <top> <out.cdl> <file.spice> ..."""
import sys
from pathlib import Path
top, out, files = sys.argv[1], sys.argv[2], sys.argv[3:]
subs = {}
for f in files:
    cur = None
    for ln in Path(f).read_text().replace("\n+", " ").splitlines():
        t = ln.split()
        if not t or t[0].startswith("*"): continue
        if t[0].lower() == ".subckt": cur = t[1]; subs[cur] = ([x for x in t[2:] if "=" not in x], []); continue
        if t[0].lower() == ".ends": cur = None; continue
        if cur: subs[cur][1].append(t)
lines = []
def expand(name, conn, path):
    ports, body = subs[name]
    m = dict(zip(ports, conn))
    for t in body:
        if t[0][0] not in "Xx": continue
        if "sg13_hv" in " ".join(t):
            i = next(k for k, x in enumerate(t) if x.startswith("sg13_hv"))
            nets = [m.get(x, f"{path}{x}" if path else x) for x in t[1:i]]
            params = [x for x in t[i + 1:] if "=" in x and not x.startswith("mm_ok")]
            lines.append(" ".join(["M" + path.replace(".", "_") + t[0][1:].replace("[", "_").replace("]", "")] + nets + [t[i]] + params))
        else:
            sub = t[-1]; nets = [m.get(x, f"{path}{x}" if path else x) for x in t[1:-1]]
            expand(sub, nets, f"{path}{t[0][1:]}.")
ports = subs[top][0]
expand(top, ports, "")
Path(out).write_text(f".SUBCKT {top} {' '.join(ports)}\n" + "\n".join(lines) + f"\n.ENDS {top}\n")
print(len(lines), "devices")
