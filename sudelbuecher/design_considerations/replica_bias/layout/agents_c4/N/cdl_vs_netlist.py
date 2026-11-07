# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""cdl_vs_netlist.py <cdl> <spice>...: every non-dummy device line of the CDL (M<label>_<n> d g s b ... w= l=) against
the device X<label> of the circuit netlists (d g s b, w, l; SPDC / SPDR = XSPD of vcm_rb / vref_s2d_rb, CBM / CBR =
bypass_rb's m-devices). Prints one line per device and a summary."""
import re
import sys

dev = {}
for f in sys.argv[2:]:
    sub = None
    for ln in open(f):
        t = ln.split()
        if not t or t[0].startswith("*"):
            continue
        if t[0].lower() == ".subckt":
            sub = t[1]
        elif t[0].upper().startswith("X") and len(t) > 5 and t[5].startswith("sg13_"):
            kv = dict(re.findall(r"(\w+)=(\S+)", ln))
            dev[(sub, t[0][1:])] = (t[1:5], kv["w"], kv["l"])
alias = {"SPDC": ("vcm_rb", "SPD"), "SPDR": ("vref_s2d_rb", "SPD"), "CBM": ("bypass_rb", "CBM"),
         "CBR": ("bypass_rb", "CBR")}
bad = n = 0
for ln in open(sys.argv[1]):
    t = ln.split()
    if not t or not t[0].startswith("M") or t[0].startswith("MD"):
        continue
    lab = t[0][1:].rsplit("_", 1)[0]
    kv = dict(re.findall(r"(\w+)=(\S+)", ln))
    keys = [alias[lab]] if lab in alias else [k for k in dev if k[1] == lab]
    ok = len(keys) == 1 and dev[keys[0]] == (t[1:5], kv["w"], kv["l"])
    n, bad = n + 1, bad + (not ok)
    print("%-4s %-10s %-34s %s" % ("ok" if ok else "BAD", t[0], " ".join(t[1:5]) + " " + kv["w"] + "/" + kv["l"],
                                   keys[0] if keys else "not in netlists"))
print("%d devices, %d mismatches" % (n, bad))
