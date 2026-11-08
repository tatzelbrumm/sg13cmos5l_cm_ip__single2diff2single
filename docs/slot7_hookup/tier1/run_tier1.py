# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Simulate slot7_tier1.spice with both custom pads: round trip pad in -> S2D -> D2S -> pad out, references, currents.

usage (repo env, from this directory): python3 -I run_tier1.py   -> results.txt (decks and logs in runs/)

Blocks with a layout are simulated from their extracted layout netlists (read only, converted to simulator syntax in
runs/ and wrapped to the source port order by port name): both pads, pad_ref_rb, bias_dist_pd. bg_core_pd from its
schematic netlist, ls_up_fs (no layout yet) from its source netlist. Slot vdd_3v3 and the pad ring iovdd both 3.3 V
(3.0 / 3.6 at the corners), harness enable 1.2 V. The S2D pad input is swept 0 ... 1.0 V; the D2S pad output is
unloaded (1 Gohm). Expected: pad_out = vcm + (pad_in - vref).
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MAC = REPO / "macros"
RUNS = HERE / "runs"
sys.path.insert(0, str(MAC / "en_ctrl_3v3" / "testbenches" / "spice"))
import run_starve as RS  # noqa: E402  (its convert() reads netlist/layout/<cell>_klayout.cir)

SRC_PORTS = {
    "sg13cmos5l_IOPadSingle2Diff": "iovdd iovss vdd vss pad outp outn vcm vref iref en_3v3 en_3v3_b",
    "sg13cmos5l_IOPadDiff2Single": "iovdd iovss vdd vss pad vinp vinn vref iref en_3v3 en_3v3_b",
    "pad_ref_rb": "vddh vssh iref vcm vref en_3v3 en_3v3_b",
    "bias_dist_pd": "vddh vssh en_3v3 en_3v3_b iin0 iin1 iin2 iin3 en_in0 en_in1 en_in2 en_in3 iout0 iout1 iout2 iout3"
                    " en_out0 en_out1 en_out2 en_out3",
}
POINTS = [("tt", 27, 3.3), ("ss", -40, 3.0), ("ff", 125, 3.6), ("fs", 125, 3.6), ("sf", -40, 3.0)]


def wrapped(cell):
    RS.RUNS = RUNS
    flat = RUNS / RS.convert(cell)
    txt = flat.read_text()
    m = re.search(r"^\.SUBCKT\s+(\S+)\s+(.*)$", txt, re.M | re.I)
    lay_ports = m.group(2).split()
    txt = txt.replace(m.group(0), f".SUBCKT {cell}_lay {' '.join(lay_ports)}", 1)
    src = SRC_PORTS[cell].split()
    missing = [p for p in lay_ports if p not in src]
    assert not missing, (cell, missing)
    wrap = f"\n.subckt {cell} {' '.join(src)}\nXlay {' '.join(lay_ports)} {cell}_lay\n.ends {cell}\n"
    flat.write_text(txt + wrap)
    return flat.name


def main():
    RUNS.mkdir(exist_ok=True)
    incs = [wrapped(c) for c in SRC_PORTS]
    bg = MAC / "bg_core_pd" / "netlist" / "schematic" / "bg_core_pd_magic.spice"
    lines = ["# slot7_tier1 with both pads (extracted), pad_ref_rb and bias_dist_pd (extracted), bg_core_pd, ls_up_fs",
             "# corner  T  V  | vcm vref [V] | round-trip error max over pad_in 0..1 V [mV] | I slot vdd_3v3, I ring iovdd"
             " [uA] enabled | same [nA], 150-170 us after enable falls (transient)"]
    for c, t, v in POINTS:
        res = {}
        for en in (1.2, 0):
            # enable 0: a DC point is ill-defined (floating iref / ibg nodes); use a transient: on, off at 30 us, 200 us
            ven = "1.2" if en else "pwl(0 1.2 30u 1.2 30.1u 0)"
            opt = "" if en else " method=gear cshunt=1e-15"
            ana = """dc Vin 0 1.0 0.05
let err = v(padout) - (v(vcm_s2d) + v(padin) - v(vref_s2d))
let aerr = abs(err)
meas dc emax max aerr
meas dc vcm find v(vcm_s2d) at=0.5
meas dc vref find v(vref_s2d) at=0.5
meas dc islot find i(Vslot) at=0.5
meas dc iio find i(Vio) at=0.5""" if en else """tran 50n 200u
let emax = 0
let vcm = 0
let vref = 0
meas tran islot avg i(Vslot) from=180u to=199u
meas tran iio avg i(Vio) from=180u to=199u"""
            deck = f"""* slot7_tier1 round trip, {c} {t} C, {v} V, enable {en}
.lib cornerMOShv.lib mos_{c}
.lib cornerMOSlv.lib mos_{c}
.lib cornerRES.lib res_typ
.lib cornerPNP.lib typ
.include /foss/pdks/ihp-sg13cmos5l/libs.tech/ngspice/models/diodes.lib
.include {MAC}/hv_logic/netlist/source/hv_logic.spice
.include {MAC}/en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice
.include {bg}
""" + "".join(f".include {i}\n" for i in incs) + f""".include {HERE}/slot7_tier1.spice
.temp {t}
.option gmin=1e-12{opt}
Vslot vdd_3v3 0 {v}
Vio iovdd 0 {v}
Ven enable 0 {ven}
Vin padin 0 0.5
Rout padout 0 1G
XS vdd_3v3 0 enable 0 0 0 0 0 b0 b1 b2 b3 vref_s2d outp outn vcm_s2d en0 enb0 iref0 vinp vinn vref_d2s iref1 enb1 en1 slot7_tier1
X2S iovdd 0 iovdd 0 padin outp outn vcm_s2d vref_s2d iref0 en0 enb0 sg13cmos5l_IOPadSingle2Diff
X2D iovdd 0 iovdd 0 padout vinp vinn vref_d2s iref1 en1 enb1 sg13cmos5l_IOPadDiff2Single
.control
{ana}
echo "RES $&emax $&vcm $&vref $&islot $&iio"
.endc
.end
"""
            f = RUNS / f"tier1_{c}_{t}_{en}.spice"
            f.write_text(deck)
            log = subprocess.run(["ngspice", "-b", f.name], cwd=RUNS, capture_output=True, text=True).stdout
            f.with_suffix(".log").write_text(log)
            m = re.search(r"^RES (\S+) (\S+) (\S+) (\S+) (\S+)", log, re.M)
            res[en] = [float(x) for x in m.groups()] if m else None
        on, off = res[1.2], res[0]
        if on is None or off is None:
            lines.append(f"{c} {t:4d} {v}  FAILED (see runs/)")
            continue
        lines.append(f"{c} {t:4d} {v}  | {on[1]:.3f} {on[2]:.3f} | {on[0] * 1e3:7.2f} | {-on[3] * 1e6:6.2f} {-on[4] * 1e6:6.2f}"
                     f" | {-off[3] * 1e9:8.2f} {-off[4] * 1e9:8.2f}")
    (HERE / "results.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
