# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Exploration for vcm_rb: edge-detector replicas on a copy of the pad's bias, over PVT and bias selection.

Bias as in the S2D pad: en_ctrl_3v3 + bias_gen_pd (sel 0 harness 5 uA, 1 OA core, 2 bandgap) + bias_tree_noab_pd.
Hung on its lines (exploration only: a real block makes its own lines from a current leg):
  top    : TR (hv PMOS 5u/6u, gate vbp, the unit tail) -> ts -> MR (hv PMOS 20u/1u ng=2, source = bulk = ts, gate = drain = gH,
           the unit's input follower) -> sink r * I(TRc), TRc = saturated copy of TR. gH = the gate voltage at which the tail
           has lost (1 - r) of its current.
  bottom : iovdd -> source r * I(CRc chain) -> gL -> CR (hv NMOS 15u/3u, gate vbnc, one finger of the fold cascode CX)
           -> xr -> SR (hv NMOS 6u/6u, gate vbn, one finger of the fold sink SX). gL = the output voltage at which the
           cascode chain has lost (1 - r) of its current.
usage: python3 -I explore_edges.py [r ...]   prints a TSV to stdout
"""
import itertools
import re
import subprocess
import sys
import tempfile
import os
from pathlib import Path

MACROS = Path(__file__).resolve().parents[3]
INC = ["hv_logic/netlist/source/hv_logic.spice", "ls_up_1v2_3v3/netlist/source/ls_up_1v2_3v3.spice",
       "en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice", "bias_tree_pd/netlist/source/bias_ref_pd.spice",
       "bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice", "bias_gen_pd/netlist/source/bias_gen_pd.spice"]
rs = [float(x) for x in sys.argv[1:]] or [0.9, 0.75]


def deck(vdd, m, t, sel):
    d = [f"* edges {vdd} {m} {t} {sel}", f".lib cornerMOShv.lib mos_{m}", f".lib cornerMOSlv.lib mos_{m}",
         ".lib cornerRES.lib res_typ", ".lib cornerPNP.lib typ"] + [f".include {MACROS / f}" for f in INC]
    d += [f"Vio iovdd 0 {vdd}", "Vcore vcore 0 1.2", "Ven en 0 1.2", f"Vs0 s0 0 {(sel % 2) * 1.2}",
          f"Vs1 s1 0 {(sel // 2) * 1.2}", "Vs12 s12 0 1.2", "Vs33 s33 0 3.3", "Vext vext 0 3.3", "Iext xg 0 5u",
          "XEd xg xg vext vext sg13_hv_pmos w=5u l=6u", "XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u",
          "Xc iovdd vcore 0 en s0 s1 s12 s33 en_3v3 sel0_3v3 sel1_3v3 en_3v3_b en_ctrl_3v3",
          "Xg iovdd 0 ibias iref en_3v3 sel0_3v3 sel1_3v3 bias_gen_pd",
          "Xt iovdd 0 iref vbp vbn vbpc vbnc en_3v3 en_3v3_b bias_tree_noab_pd",
          # saturated reference copies
          "XTRc trc vbp iovdd iovdd sg13_hv_pmos w=5u l=6u", "VTRc trc 0 1.0",
          "VCRc iovdd crc 0", "XCRc crc vbnc xrc 0 sg13_hv_nmos w=15u l=3u", "XSRc xrc vbn 0 0 sg13_hv_nmos w=6u l=6u",
          # x-node replica with the fold's density: 2 fingers of SY (12u/6u, 10 uA) under one CY finger at 5 uA ... as in
          # the pad, where SY sinks 30 uA (6 fingers) and CY carries 10 uA: the units' 20 uA go into an ideal 5 uA source
          "XCYp iovdd vbnc xp 0 sg13_hv_nmos w=15u l=3u", "XSYp xp vbn 0 0 sg13_hv_nmos w=6u l=6u ng=1",
          "XSYq xp vbn 0 0 sg13_hv_nmos w=6u l=6u ng=1", "Iun 0 xp 5u",
          # the input follower as a diode at its 5 uA (V_SG of the unit's XMa), source and bulk at iovdd
          "XMD gd gd iovdd iovdd sg13_hv_pmos w=20u l=1u ng=2", "IMD gd 0 5u"]
    for k, r in enumerate(rs):
        d += [f"XTR{k} ts{k} vbp iovdd iovdd sg13_hv_pmos w=5u l=6u",
              f"XMR{k} gh{k} gh{k} ts{k} ts{k} sg13_hv_pmos w=20u l=1u ng=2",
              f"FH{k} gh{k} 0 VTRc {r}",
              f"FL{k} iovdd gl{k} VCRc {r}",
              f"XCR{k} gl{k} vbnc xr{k} 0 sg13_hv_nmos w=15u l=3u", f"XSR{k} xr{k} vbn 0 0 sg13_hv_nmos w=6u l=6u"]
    pr = " ".join(["v(vbp)", "v(vbn)", "v(vbpc)", "v(vbnc)", "i(VTRc)", "i(VCRc)", "v(xp)", "v(xrc)", "v(gd)"] +
                  [f"v(gh{k}) v(gl{k})" for k in range(len(rs))])
    d += [f".temp {t}", ".options method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15", ".control", "op",
          f"print {pr}", ".endc", ".end"]
    return "\n".join(d)


names = ["vbp", "vbn", "vbpc", "vbnc", "i(vtrc)", "i(vcrc)", "xp", "xrc", "gd"] + [f"{a}{k}" for k in range(len(rs)) for a in ("gh", "gl")]
print("# explore_edges.py, r = " + " ".join(str(r) for r in rs))
print("\t".join(["vdd", "corner", "temp", "sel"] + names))
for vdd, m, t, sel in itertools.product([3.0, 3.3, 3.6], ["ss", "sf", "tt", "fs", "ff"], [-40, 27, 125], [0, 1, 2]):
    with tempfile.NamedTemporaryFile("w", suffix=".spice", delete=False) as f:
        f.write(deck(vdd, m, t, sel))
    out = subprocess.run(["ngspice", "-b", f.name], capture_output=True, text=True).stdout
    os.unlink(f.name)
    got = {a.lower(): b for a, b in re.findall(r"^\s*(\S+)\s*=\s*(\S+)", out, re.M)}
    keys = ["v(vbp)", "v(vbn)", "v(vbpc)", "v(vbnc)", "i(vtrc)", "i(vcrc)", "v(xp)", "v(xrc)", "v(gd)"] + \
        [f"v({a}{k})" for k in range(len(rs)) for a in ("gh", "gl")]
    if os.environ.get("EDGE_DEBUG"):
        print(out)
        sys.exit(0)
    print("\t".join([str(vdd), m, str(t), str(sel)] + [got.get(q, "nan") for q in keys]), flush=True)
