# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Phase 1 of the replica-bias task: regenerate every table of docs/replica_bias/SURVEY.md from committed results.

Read-only. No simulation. Inputs:
  - the CACE CSVs of the two pads in the design checkout (schematic and extracted),
  - results_s2d.txt section 3 (design decks, ideal bias fixture) on the notes branch.
Usage (from anywhere):
  python3 -I survey_tables.py <design checkout> <notes checkout>
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

LIMIT_INL_MV = 2.0  # S2D dc_params limit; the survey's "band" criterion (INL over u = +-0.5 V)

design = Path(sys.argv[1])
notes = Path(sys.argv[2])
s2d_res = design / "macros/sg13cmos5l_IOPadSingle2Diff/verification/cace/results"
d2s_res = design / "macros/sg13cmos5l_IOPadDiff2Single/verification/cace/results"
res_s2d_txt = notes / "sudelbuecher/design_considerations/s2d_input_buffer/sim/results_s2d.txt"


def rows(path):
    with open(path) as f:
        rd = csv.reader(f)
        hdr = next(rd)
        return hdr, list(rd)


def tkey(c):
    return (c[0], int(c[1]))


print("# survey_tables.py output")
print(f"# design checkout: {design}")
print(f"# notes checkout:  {notes}")

# ---------------------------------------------------------------- S2D range_params (vref x vcm, iovdd 3.0 V)
for src in ("sg13cmos5l_IOPadSingle2Diff", "sg13cmos5l_IOPadSingle2Diff_pex"):
    hdr, rr = rows(s2d_res / src / "range_params.csv")
    # columns: vdd,vref,vcm,corner_mos,temp,Gain[],None[],INL[mV],Vcm_err[mV],None[]  (values in SI units: V)
    d = defaultdict(dict)
    for r in rr:
        d[(float(r[1]), float(r[2]))][(r[3], r[4])] = (float(r[7]) * 1e3, float(r[5]), float(r[8]) * 1e3)
    conds = sorted({c for v in d.values() for c in v}, key=tkey)
    print(f"\n== S2D range_params, {src}: {len(rr)} runs, iovdd {rr[0][0]} V; INL in mV over u = +-0.5 V")
    print("vref  vcm  | " + " ".join(f"{c[0]}/{c[1]:>4}" for c in conds) + " | worst | gain min..max | Vcm_err mV")
    for k in sorted(d):
        inl = [d[k][c][0] for c in conds]
        g = [d[k][c][1] for c in conds]
        e = [d[k][c][2] for c in conds]
        flag = "ok" if max(inl) <= LIMIT_INL_MV else "OUT"
        print(f"{k[0]:4} {k[1]:4} | " + " ".join(f"{x:8.2f}" for x in inl)
              + f" | {max(inl):6.2f} {flag:3} | {min(g):.4f}..{max(g):.4f} | {min(e):.1f}..{max(e):.1f}")

# ---------------------------------------------------------------- S2D window_params (vref 0.5 V)
for src in ("sg13cmos5l_IOPadSingle2Diff", "sg13cmos5l_IOPadSingle2Diff_pex"):
    hdr, rr = rows(s2d_res / src / "window_params.csv")
    print(f"\n== S2D window_params, {src}: {len(rr)} runs (vref 0.5 V, vcm 1.2 V); pad range linear to 1 mV, V")
    print("iovdd corner temp  Vin_min  Vin_max  Vin_max-(iovdd)")
    for r in rr:
        print(f"{r[1]:5} {r[2]:6} {r[3]:>4}  {float(r[4]):7.4f}  {float(r[5]):7.4f}  {float(r[5]) - float(r[1]):+7.3f}")

# ---------------------------------------------------------------- S2D dc_params INL by iovdd (vref = vcm = 1.2 V)
for src in ("sg13cmos5l_IOPadSingle2Diff", "sg13cmos5l_IOPadSingle2Diff_pex"):
    hdr, rr = rows(s2d_res / src / "dc_params.csv")
    iI = hdr.index("INL[mV]")
    m = defaultdict(list)
    for r in rr:
        m[r[0]].append(float(r[iI]) * 1e3)
    print(f"\n== S2D dc_params, {src}: {len(rr)} runs, vref = vcm = 1.2 V; worst INL per iovdd, mV")
    for k in sorted(m):
        print(f"iovdd {k}: {max(m[k]):.2f}")

# ---------------------------------------------------------------- D2S dc_params / dc_3v0_params (vref = vicm = 1.65 V)
for g in ("dc_params", "dc_3v0_params"):
    hdr, rr = rows(d2s_res / "sg13cmos5l_IOPadDiff2Single" / f"{g}.csv")
    iI = hdr.index("INL[mV]")
    print(f"\n== D2S {g}: {len(rr)} runs, vref = vicm = 1.65 V, INL over vd = +-1 V (pad = vref +- 0.5 V), mV")
    m = defaultdict(dict)
    for r in rr:
        m[r[2]][(r[0], r[1])] = float(r[iI]) * 1e3
    for v in sorted(m):
        conds = sorted(m[v], key=tkey)
        print(f"iovdd {v}: " + "  ".join(f"{c[0]}/{c[1]} {m[v][c]:.2f}" for c in conds))
        print(f"iovdd {v}: worst {max(m[v].values()):.2f}")

# ---------------------------------------------------------------- results_s2d.txt section 3: band edges
txt = res_s2d_txt.read_text()
sec = txt.split("== 3.")[1].split("== 4.")[0]
print("\n== results_s2d.txt section 3 (s2d_mpdda + ideal fixture, vref = vcm): INL mV; band where INL <= 2 mV")
print("     (edges by linear interpolation between the swept vcm values; '<1.0' / '>1.65' = not reached)")
for line in sec.strip().splitlines()[0:]:
    mm = re.match(r"\s*(\d\.\d) V (\w\w) (-?\d+)C\s+(.*)", line)
    if not mm:
        continue
    vdd, corner, temp, rest = mm.groups()
    pts = [(float(a), float(b)) for a, b in re.findall(r"(\d\.\d+):\s+([\d.]+)", rest)]
    ok = [p for p in pts if p[1] <= LIMIT_INL_MV]
    lo = hi = None
    # low edge: between the first point and the first point that is ok
    if pts[0][1] <= LIMIT_INL_MV:
        lo = "<1.0"
    else:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if y0 > LIMIT_INL_MV >= y1:
                lo = f"{x0 + (x1 - x0) * (y0 - LIMIT_INL_MV) / (y0 - y1):.3f}"
                break
    if pts[-1][1] <= LIMIT_INL_MV:
        hi = ">1.65"
    else:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if y0 <= LIMIT_INL_MV < y1:
                hi = f"{x0 + (x1 - x0) * (LIMIT_INL_MV - y0) / (y1 - y0):.3f}"
                break
    top_gate = ""
    if hi and not hi.startswith(">"):
        top_gate = f"  top unit gate (vcm + 0.5) = {float(hi) + 0.5:.3f} V = iovdd - {float(vdd) - float(hi) - 0.5:.3f} V"
    print(f"{vdd} V {corner} {temp:>4} C: vcm band {lo} ... {hi}{top_gate}")
