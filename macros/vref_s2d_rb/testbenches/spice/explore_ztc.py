# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Exploration for vref_s2d_rb: V_GS of diode-connected hv devices of the pads' sizes vs current, temperature, corner.
usage: python3 -I explore_ztc.py  (prints a table; repo env: PDK_ROOT, .designinit)"""
import subprocess, tempfile, os, re
DEV = [("BN_6/6", "nmos", "6u", "6u"), ("BNC_1/8", "nmos", "1u", "8u"), ("NBPC_2.4/6", "nmos", "2.4u", "6u"),
       ("BP_5/6", "pmos", "5u", "6u")]
I = ["0.5u", "1u", "2u", "5u", "10u", "20u"]
rows = {}
for c in ["ss", "tt", "ff"]:
    for t in [-40, 27, 125]:
        d = [f"* ztc {c} {t}", f".lib cornerMOShv.lib mos_{c}", "Vdd vdd 0 3.3", "I0 0 r 1u", "V0 r 0 0", f".temp {t}"]
        for k, (n, typ, w, l) in enumerate(DEV):
            if typ == "nmos":
                d += [f"F{k} 0 g{k} V0 1", f"X{k} g{k} g{k} 0 0 sg13_hv_nmos w={w} l={l} ng=1"]
            else:
                d += [f"F{k} g{k} 0 V0 1", f"X{k} g{k} g{k} vdd vdd sg13_hv_pmos w={w} l={l} ng=1"]
        d += [".control", "dc I0 0.25u 25u 0.25u"]
        for k, (n, typ, w, l) in enumerate(DEV):
            for ii in I:
                expr = f"v(g{k})" if typ == "nmos" else f"3.3-v(g{k})"
                d += [f"let q{k} = {expr}", f"meas dc m{k}_{ii.replace('.', 'p')} find q{k} at={ii}"]
        d += [".endc", ".end"]
        with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as f:
            f.write("\n".join(d))
        out = subprocess.run(["ngspice", "-b", f.name], capture_output=True, text=True).stdout
        os.unlink(f.name)
        for m in re.finditer(r"m(\d)_(\S+)\s*=\s*(\S+)", out):
            rows[(int(m.group(1)), m.group(2), c, t)] = float(m.group(3))
for k, (n, *_r) in enumerate(DEV):
    print(f"== {n}: |V_GS| in V (columns ss/-40 ss/27 ss/125 tt/-40 tt/27 tt/125 ff/-40 ff/27 ff/125)")
    for ii in I:
        key = ii.replace('.', 'p')
        vals = [rows.get((k, key, c, t), float('nan')) for c in ["ss", "tt", "ff"] for t in [-40, 27, 125]]
        tt = vals[3:6]
        print(f"  {ii:>5}: " + " ".join(f"{v:.3f}" for v in vals) + f"   tt span over T {max(tt) - min(tt):.3f}, all {max(vals) - min(vals):.3f}")
