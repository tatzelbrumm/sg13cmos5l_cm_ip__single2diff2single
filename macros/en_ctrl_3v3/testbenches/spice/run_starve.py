# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Starvation check: ring (iovdd) current of the two custom pads and of pad_ref_rb with the slot off, i.e. no iref,
enables anywhere (pad_ref_rb has no pad pin: its line shows pad_V 0).

usage (repo env, from this directory): python3 -I run_starve.py   -> results/starve.txt (decks and logs in runs/)

The pads are not changed: their extracted layout netlists (netlist/layout/*_klayout.cir of the two pad macros) are
read and converted to simulator syntax in runs/. iovdd 3.6 V; iref, vcm / vref / vinp / vinn and the core outputs
float (1 Gohm to iovss); en_3v3 and en_3v3_b each swept 0 ... 3.6 V in 0.3 V steps (169 combinations, as a switched-off
slot can leave them anywhere); the pad pin driven at 0, 1.8 and 3.6 V. Reported: the largest and smallest iovdd
current over the 169 combinations.
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAC = HERE.parents[2]
RUNS = HERE / "runs"
RES = HERE / "results"
PADS = {"s2d": ("sg13cmos5l_IOPadSingle2Diff", "X1 en enb iovdd 0 iref outn outp padn vcm vref",
                ["iref", "vcm", "vref", "outp", "outn"]),
        "d2s": ("sg13cmos5l_IOPadDiff2Single", "X1 en enb iovdd 0 iref padn vinn vinp vref",
                ["iref", "vinn", "vinp", "vref"]),
        "prb": ("pad_ref_rb", "X1 en enb iref vcm iovdd vref 0", ["iref", "vcm", "vref"])}
CORNERS = [("tt", 27), ("ff", 125), ("fs", 125), ("sf", 125), ("ss", -40)]


def convert(cell):
    txt = (MAC / cell / "netlist" / "layout" / f"{cell}_klayout.cir").read_text()
    txt = txt.replace("\n+", " ").replace("\\$", "n_")
    out = []
    for line in txt.splitlines():
        t = line.split()
        if not t or t[0].startswith("*"):
            continue
        k = t[0][0].upper()
        if k == "M":
            prm = " ".join(p.lower() for p in t[6:] if not p.lower().startswith("rfmode"))
            out.append(f"X{t[0][1:]} {' '.join(t[1:5])} {t[5]} {prm}")
        elif k == "R":
            out.append(f"X{t[0][1:]} {' '.join(t[1:4])} {t[4]} {' '.join(p for p in t[5:] if not p.startswith('ps='))}")
        elif k == "D":
            out.append(f"X{t[0][1:]} {t[1]} {t[2]} {t[3]} " + " ".join(p.lower() for p in t[4:]))
        else:
            out.append(line)
    f = RUNS / f"{cell}_flat.spice"
    f.write_text("\n".join(out) + "\n")
    return f.name


def main():
    RUNS.mkdir(exist_ok=True)
    RES.mkdir(exist_ok=True)
    lines = ["# starvation: pad ring current (iovdd 3.6 V) with iref open, en_3v3 / en_3v3_b each 0 ... 3.6 V (169 points)",
             "pad  corner   T  pad_V   max_nA   min_nA"]
    for pad, (cell, inst, floating) in PADS.items():
        flat = convert(cell)
        for c, t in CORNERS:
            for vp in ((0, 1.8, 3.6) if pad != "prb" else (0,)):
                fl = "\n".join(f"Rf{i} {n} 0 1G" for i, n in enumerate(floating))
                deck = f"""* starvation: {cell}, {c} {t} C, pad at {vp} V
.lib cornerMOShv.lib mos_{c}
.lib cornerRES.lib res_typ
.include /foss/pdks/ihp-sg13cmos5l/libs.tech/ngspice/models/diodes.lib
.include {flat}
.temp {t}
Vdd iovdd 0 3.6
Ven en 0 0
Venb enb 0 0
Vpad padn 0 {vp}
{fl}
{inst} {cell}
.dc Ven 0 3.6 0.3 Venb 0 3.6 0.3
.control
run
let idd = -i(Vdd)
let mx = maximum(idd)
let mn = minimum(idd)
echo "RES $&mx $&mn"
.endc
.end
"""
                f = RUNS / f"starve_{pad}_{c}_{t}_{vp}.spice"
                f.write_text(deck)
                log = subprocess.run(["ngspice", "-b", f.name], cwd=RUNS, capture_output=True, text=True).stdout
                f.with_suffix(".log").write_text(log)
                m = re.search(r"^RES (\S+) (\S+)", log, re.M)
                mx, mn = (float(m.group(1)) * 1e9, float(m.group(2)) * 1e9) if m else (float("nan"),) * 2
                lines.append(f"{pad}  {c:3s} {t:5d}  {vp:4.1f}  {mx:8.2f} {mn:8.2f}")
    (RES / "starve.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
