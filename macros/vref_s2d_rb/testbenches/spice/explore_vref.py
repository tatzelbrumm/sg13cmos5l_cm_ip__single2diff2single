# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Exploration for vref_s2d_rb: out = vbnc - V_GS(F) of NMOS followers F (fold-cascode fingers 15u/3u, x1 / x2, or 6u/6u)
at several ideal sink currents, on lines made like vcm_rb's (NI 6u/6u from 5 uA, BP 2u/6u at 2 uA, BNC 1u/8u at 2 uA),
against the S2D vref band's bottom edge of G4 (INL <= 2 mV) and the target "0.5 V, pad range down to 0 V" at <= 27 C.
usage: python3 -I explore_vref.py   (repo env)"""
import csv
import itertools
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
MACROS = HERE.parents[2]
INC = ["hv_logic/netlist/source/hv_logic.spice", "ls_up_1v2_3v3/netlist/source/ls_up_1v2_3v3.spice",
       "en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice", "bias_tree_pd/netlist/source/bias_ref_pd.spice",
       "bias_gen_pd/netlist/source/bias_gen_pd.spice"]
FOL = {"F15x1": "w=15u l=3u ng=1", "F15x2": "w=15u l=3u ng=1 m=2", "F6": "w=6u l=6u ng=1"}
CUR = [0.5e-6, 1e-6, 2e-6]


def deck(vdd, m, t, sel):
    d = [f".lib cornerMOShv.lib mos_{m}", f".lib cornerMOSlv.lib mos_{m}", ".lib cornerRES.lib res_typ",
         ".lib cornerPNP.lib typ"] + [f".include {MACROS / f}" for f in INC]
    d += [f"Vio iovdd 0 {vdd}", "Vcore vcore 0 1.2", "Ven en 0 1.2", f"Vs0 s0 0 {(sel % 2) * 1.2}",
          f"Vs1 s1 0 {(sel // 2) * 1.2}", "Vs12 s12 0 1.2", "Vs33 s33 0 3.3", "Vext vext 0 3.3",
          "Xc iovdd vcore 0 en s0 s1 s12 s33 en_3v3 sel0_3v3 sel1_3v3 en_3v3_b en_ctrl_3v3", "Iext xg 0 5u",
          "XEd xg xg vext vext sg13_hv_pmos w=5u l=6u", "XEm ib xg vext vext sg13_hv_pmos w=5u l=6u",
          "Xg iovdd 0 ib ir en_3v3 sel0_3v3 sel1_3v3 bias_gen_pd",
          "XNI ir ir 0 0 sg13_hv_nmos w=6u l=6u", "XNBP vbp ir 0 0 sg13_hv_nmos w=2.4u l=6u",
          "XBP vbp vbp iovdd iovdd sg13_hv_pmos w=2u l=6u", "XPBNC vbnc vbp iovdd iovdd sg13_hv_pmos w=2u l=6u",
          "XBNC vbnc vbnc 0 0 sg13_hv_nmos w=1u l=8u",
          # the fold-node replica of vcm_rb, for reference
          "XCY iovdd vbnc xp 0 sg13_hv_nmos w=15u l=3u", "XSY xp ir 0 0 sg13_hv_nmos w=6u l=6u"]
    names = []
    for (fn, fz), i in itertools.product(FOL.items(), CUR):
        n = f"{fn}_{i * 1e6:g}u".replace(".", "p")
        names.append(n)
        d += [f"XF{n} iovdd vbnc o{n} 0 sg13_hv_nmos {fz}", f"I{n} o{n} 0 {i}"]
    d += [f".temp {t}", ".options method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15", ".control", "op",
          "print v(xp) " + " ".join(f"v(o{n})" for n in names), ".endc", ".end"]
    return "\n".join(d), names


def run(c):
    dk, names = deck(*c)
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as f:
        f.write(dk)
    out = subprocess.run(["ngspice", "-b", f.name], capture_output=True, text=True).stdout
    os.unlink(f.name)
    g = {a.lower(): float(b) for a, b in re.findall(r"^\s*(\S+)\s*=\s*(\S+)", out, re.M) if re.match(r"-?[\d.]", b)}
    return c, names, g


if __name__ == "__main__":
    sys.path.insert(0, str(MACROS / "vcm_rb/testbenches/pad_char"))
    import analyze_bands as ab
    rows = ab.load("g4_s2d_vref")
    by = {}
    for r in rows:
        by.setdefault((r["vdd"], r["corner_mos"], r["temp"]), []).append((float(r["vref"]), float(r["INL"])))
    edge = {k: ab.band(sorted(v), 0.002) for k, v in by.items()}
    conds = list(itertools.product([3.0, 3.3, 3.6], ["ss", "sf", "tt", "fs", "ff"], [-40, 27, 125], [0]))
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(run, conds))
    names = res[0][1]
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    with open(out / "explore_vref.tsv", "w") as f:
        f.write("vdd\tcorner\ttemp\tedge_lo\txp\t" + "\t".join(names) + "\n")
        for (vdd, m, t, s), _, g in res:
            e = edge[(str(vdd), m, str(t))]
            f.write(f"{vdd}\t{m}\t{t}\t{('<' if e[2] else '')}{e[0]:.3f}\t{g['v(xp)']:.4f}\t" +
                    "\t".join(f"{g[f'v(o{n.lower()})']:.4f}" for n in names) + "\n")
    for n in names:
        at27 = [g[f"v(o{n.lower()})"] for (vdd, m, t, s), _, g in res if t == 27]
        cold = [g[f"v(o{n.lower()})"] for (vdd, m, t, s), _, g in res if t == -40]
        hot = [(g[f"v(o{n.lower()})"] - edge[(str(vdd), m, str(t))][0]) for (vdd, m, t, s), _, g in res if t == 125]
        print(f"{n:10}: 27 C {min(at27):.3f}..{max(at27):.3f}  -40 C {min(cold):.3f}..{max(cold):.3f}  "
              f"125 C margin to the INL edge {min(hot):+.3f}..{max(hot):+.3f}")
