# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Exploration for vcm_rb: candidate blocks (complete, with their own lines from a 5 uA reference) against the measured
bands of both pads (S2D vcm band of G3 / G10 intersected with the D2S band of G1 / G10, INL <= 2 mV).

Each candidate gets its reference from its own bias_gen_pd (the same selection as the pads' in G3 / G1 / G10).
usage: python3 -I explore_vcm_rb.py  -> prints per candidate: vcm - centre and the worst margin to the band edges
"""
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

P, N = "sg13_hv_pmos", "sg13_hv_nmos"


def block(name, tr, sh, cy_sink, up, lo):
    """tr: TR size; sh: list of sink sizes at ni for gh; cy_sink: list of sink sizes under CY; up / lo: stack sizes."""
    s = [f".subckt {name} vdd vss iref vcm en_3v3 en_3v3_b",
         f"XTGN iref en_3v3 ni vss {N} w=1u l=0.45u", f"XTGP iref en_3v3_b ni vdd {P} w=1u l=0.45u",
         f"XTDN ni en_3v3_b vss vss {N} w=1u l=0.45u", f"XNI ni ni vss vss {N} w=6u l=6u",
         f"XNBP vbp ni vss vss {N} w=2.4u l=6u", f"XBP vbp vbp vdd vdd {P} w=2u l=6u",
         f"XPBNC vbnc vbp vdd vdd {P} w=2u l=6u", f"XBNC vbnc vbnc vss vss {N} w=1u l=8u",
         f"XTR ts vbp vdd vdd {P} {tr}", f"XMR gh gh ts ts {P} w=20u l=1u ng=2"]
    s += [f"XSH{i} gh ni vss vss {N} {z}" for i, z in enumerate(sh)]
    s += [f"XCY vdd vbnc xp vss {N} w=15u l=3u"] + [f"XSY{i} xp ni vss vss {N} {z}" for i, z in enumerate(cy_sink)]
    s += [f"XSU vcm vcm gh gh {P} {up}", f"XSL xp xp vcm vcm {P} {lo}",
          f"XPD vcm en_3v3_b vss vss {N} w=1u l=0.45u", ".ends"]
    return "\n".join(s)


CANDS = {
    "D_5uA_asym": dict(tr="w=5u l=6u", sh=["w=2.4u l=6u", "w=2.4u l=6u"], cy_sink=["w=6u l=6u"], up="w=1u l=4u",
                       lo="w=5u l=6u"),
    "E_lo2u6u": dict(tr="w=5u l=6u", sh=["w=2.4u l=6u", "w=2.4u l=6u"], cy_sink=["w=6u l=6u"], up="w=1u l=4u",
                     lo="w=2u l=6u"),
    "F_lo6u4u": dict(tr="w=5u l=6u", sh=["w=2.4u l=6u", "w=2.4u l=6u"], cy_sink=["w=6u l=6u"], up="w=1u l=4u",
                     lo="w=6u l=4u"),
    "G_lo2x1u4u": dict(tr="w=5u l=6u", sh=["w=2.4u l=6u", "w=2.4u l=6u"], cy_sink=["w=6u l=6u"], up="w=1u l=4u",
                       lo="w=1u l=4u m=2"),
}


def deck(vdd, m, t, sel):
    d = [f"* vcm_rb candidates {vdd} {m} {t} {sel}", f".lib cornerMOShv.lib mos_{m}", f".lib cornerMOSlv.lib mos_{m}",
         ".lib cornerRES.lib res_typ", ".lib cornerPNP.lib typ"] + [f".include {MACROS / f}" for f in INC]
    d += [block(n, **c) for n, c in CANDS.items()]
    d += [f"Vio iovdd 0 {vdd}", "Vcore vcore 0 1.2", "Ven en 0 1.2", f"Vs0 s0 0 {(sel % 2) * 1.2}",
          f"Vs1 s1 0 {(sel // 2) * 1.2}", "Vs12 s12 0 1.2", "Vs33 s33 0 3.3", "Vext vext 0 3.3",
          "Xc iovdd vcore 0 en s0 s1 s12 s33 en_3v3 sel0_3v3 sel1_3v3 en_3v3_b en_ctrl_3v3"]
    for k, n in enumerate(CANDS):
        d += [f"Iext{k} xg{k} 0 5u", f"XEd{k} xg{k} xg{k} vext vext {P} w=5u l=6u",
              f"XEm{k} ib{k} xg{k} vext vext {P} w=5u l=6u",
              f"Xg{k} iovdd 0 ib{k} ir{k} en_3v3 sel0_3v3 sel1_3v3 bias_gen_pd",
              f"Xb{k} iovdd 0 ir{k} vcm{k} en_3v3 en_3v3_b {n}"]
    pr = " ".join(f"v(vcm{k}) v(xb{k}.gh) v(xb{k}.xp)" for k in range(len(CANDS))) + " i(vio)"
    d += [f".temp {t}", ".options method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15", ".control", "op",
          f"print {pr}", ".endc", ".end"]
    return "\n".join(d)


def run(c):
    vdd, m, t, sel = c
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as f:
        f.write(deck(vdd, m, t, sel))
    out = subprocess.run(["ngspice", "-b", f.name], capture_output=True, text=True).stdout
    os.unlink(f.name)
    got = {a.lower(): float(b) for a, b in re.findall(r"^\s*(\S+)\s*=\s*(\S+)", out, re.M) if re.match(r"-?[\d.]", b)}
    return c, got


def bands():
    sys.path.insert(0, str(HERE.parent / "pad_char"))
    import analyze_bands as ab  # noqa: E402

    def get(exp, x, grp):
        rows = ab.load(exp)
        by = {}
        for r in rows:
            by.setdefault(tuple(r[g] for g in grp), []).append((float(r[x]), float(r["INL"])))
        return {k: ab.band(sorted(v), 0.002) for k, v in by.items()}
    return (get("g3_s2d_vcm", "vcm", ["vdd", "corner_mos", "temp"]),
            get("g1_d2s_vref", "vref", ["vdd", "corner_mos", "temp"]),
            get("g10_s2d_sel", "vcm", ["corner_mos", "temp", "sel"]),
            get("g10_d2s_sel", "vref", ["corner_mos", "temp", "sel"]))


if __name__ == "__main__":
    conds = list(itertools.product([3.0, 3.3, 3.6], ["ss", "sf", "tt", "fs", "ff"], [-40, 27, 125], [0]))
    conds += list(itertools.product([3.0], ["ss", "tt", "ff"], [-40, 27, 125], [1, 2]))
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(run, conds))
    S, D, S10, D10 = bands()
    out = HERE / "results" / "explore_vcm_rb.tsv"
    with open(out, "w") as f:
        f.write("vdd\tcorner\ttemp\tsel\tlo\thi\t" + "\t".join(f"vcm_{n}" for n in CANDS) + "\tiio\n")
        stats = {n: [] for n in CANDS}
        for (vdd, m, t, sel), g in res:
            if sel == 0:
                s, d = S.get((str(vdd), m, str(t))), D.get((str(vdd), m, str(t)))
            else:
                s, d = S10.get((m, str(t), str(sel))), D10.get((m, str(t), str(sel)))
            if not s or not d:
                lo = hi = float("nan")
            else:
                lo, hi = s[0], min(s[1], d[1])
            vals = [g.get(f"v(vcm{k})", float("nan")) for k in range(len(CANDS))]
            f.write(f"{vdd}\t{m}\t{t}\t{sel}\t{lo:.3f}\t{hi:.3f}\t" + "\t".join(f"{v:.4f}" for v in vals) +
                    f"\t{-g.get('i(vio)', float('nan')):.4g}\n")
            for n, v in zip(CANDS, vals):
                stats[n].append((v - (lo + hi) / 2, min(v - lo, hi - v), (vdd, m, t, sel)))
    for n, st_ in stats.items():
        dc = [x[0] for x in st_ if x[0] == x[0]]
        mg = sorted(st_, key=lambda x: x[1])
        print(f"{n:11}: vcm - centre {min(dc):+.3f} .. {max(dc):+.3f} (mean {sum(dc) / len(dc):+.3f});"
              f" worst margin {mg[0][1]:+.3f} at {mg[0][2]}, next {mg[1][1]:+.3f} at {mg[1][2]}")
    print(f"-> {out}")
