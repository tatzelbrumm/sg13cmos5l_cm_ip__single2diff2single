# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Modes of slot7_tier1 (s7_ctrl): default, swap, mon, feed, all bits high, swap+feed; with both extracted pads.

usage (repo env, from this directory): python3 -I run_modes.py [--parse]   -> modes.txt (decks and logs in runs/)

dig_in0 swap, dig_in1 mon, dig_in2 feed, dig_in5 ext, dig_in3 / dig_in4 key (1 / 0 = manual modes on). ext: bus2 / bus3\ndriven at 1.30 / 0.50 V through 10 kohm, pad_ref_rb disconnected; expected pad out vcm + (in - vref) with the external values. Buses: bus0 / bus1 through
10 kohm (harness switch and instrument) to sources at vcm +- 0.2 V in the feed modes, else open (1 Gohm); bus2 / bus3
open. Pad in swept 0 ... 1.0 V (fixed 0.5 V in the feed modes). Expected D2S pad out: direct vcm + (in - vref),
crossed vcm - (in - vref), feed vcm + (v(bus0) - v(bus1)) / 2 = vcm + 0.2 V.
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_tier1 as T  # noqa: E402

MODES = [  # name, d0..d5, kind
    ("default", "0 0 0 0 0 0", "direct"), ("swap", "1 0 0 1 0 0", "crossed"), ("mon", "0 1 0 1 0 0", "direct+mon"),
    ("feed", "0 0 1 1 0 0", "feed"), ("ext", "0 0 0 1 0 1", "ext"), ("all_high", "1 1 1 1 1 1", "direct"),
    ("swap+feed", "1 0 1 1 0 0", "feed"), ("no_key_swap", "1 0 0 0 0 0", "direct")]
POINTS = [("tt", 27, 3.3), ("ss", -40, 3.0), ("ff", 125, 3.6)]


PARSE_ONLY = "--parse" in sys.argv  # re-tabulate from the logs in runs/ without simulating


def main():
    T.RUNS.mkdir(exist_ok=True)
    incs = [T.wrapped(c) for c in T.SRC_PORTS]
    bg = T.MAC / "bg_core_pd" / "netlist" / "schematic" / "bg_core_pd_magic.spice"
    out = ["# mode       corner     | error max [mV] vs expected | v(bus0)-v(outp), v(bus1)-v(outn) [mV] (mon)"]
    for c, t, v in POINTS:
        for name, bits, kind in MODES:
            d = [float(b) * 1.2 for b in bits.split()]
            feed = kind == "feed"
            ext = kind == "ext"
            busdrv = ("Vb0 b0s 0 {vb0}\nVb1 b1s 0 {vb1}\nRb0 b0s b0 10k\nRb1 b1s b1 10k" if feed
                      else "Rb0 b0 0 1G\nRb1 b1 0 1G")
            exp = {"direct": "v(vcm_s2d) + v(padin) - v(vref_s2d)", "direct+mon": "v(vcm_s2d) + v(padin) - v(vref_s2d)",
                   "crossed": "v(vcm_s2d) - v(padin) + v(vref_s2d)", "feed": "v(vcm_s2d) + (v(b0) - v(b1))/2",
                   "ext": "1.30 + v(padin) - 0.50"}[kind]
            ana = ("op" if feed else "dc Vin 0 1.0 0.05")
            ext2 = ("Vb2 b2s 0 1.30\nVb3 b3s 0 0.50\nRb2 b2s b2 10k\nRb3 b3s b3 10k" if ext else "Rb2 b2 0 1G\nRb3 b3 0 1G")
            deck = f"""* slot7_tier1 mode {name}, {c} {t} C, {v} V
.lib cornerMOShv.lib mos_{c}
.lib cornerMOSlv.lib mos_{c}
.lib cornerRES.lib res_typ
.lib cornerPNP.lib typ
.include /foss/pdks/ihp-sg13cmos5l/libs.tech/ngspice/models/diodes.lib
.include {T.MAC}/hv_logic/netlist/source/hv_logic.spice
.include {T.MAC}/en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice
.include {bg}
""" + "".join(f".include {i}\n" for i in incs) + f""".include {T.MAC}/slot_7/netlist/source/slot_7.spice
.temp {t}
.option gmin=1e-12
Vslot vdd_3v3 0 {v}
Vio iovdd 0 {v}
Ven enable 0 1.2
Vd0 d0 0 {d[0]}
Vd1 d1 0 {d[1]}
Vd2 d2 0 {d[2]}
Vd3 d3 0 {d[3]}
Vd4 d4 0 {d[4]}
Vd5 d5 0 {d[5]}
Vin padin 0 0.5
Rout padout 0 1G
{ext2}
.param vb0=1.45 vb1=1.05
{busdrv}
XS vdd_3v3 0 enable d0 d1 d2 d3 d4 d5 b0 b1 b2 b3 vref_s2d outp outn vcm_s2d en0 enb0 iref0 vinp vinn vref_d2s iref1 enb1 en1 slot_7
X2S iovdd 0 iovdd 0 padin outp outn vcm_s2d vref_s2d iref0 en0 enb0 sg13cmos5l_IOPadSingle2Diff
X2D iovdd 0 iovdd 0 padout vinp vinn vref_d2s iref1 en1 enb1 sg13cmos5l_IOPadDiff2Single
.control
{ana}
let err = abs(v(padout) - ({exp}))
let m0 = abs(v(b0) - v(outp))
let m1 = abs(v(b1) - v(outn))
let emax = maximum(err)
let m0x = maximum(m0)
let m1x = maximum(m1)
echo "MAX $&emax $&m0x $&m1x"
.endc
.end
"""
            f = T.RUNS / f"mode_{name}_{c}_{t}.spice"
            if PARSE_ONLY:
                log = f.with_suffix(".log").read_text()
            else:
                f.write_text(deck)
                log = subprocess.run(["ngspice", "-b", f.name], cwd=T.RUNS, capture_output=True, text=True).stdout
                f.with_suffix(".log").write_text(log)
            mx = re.search(r"^MAX (\S+) (\S+) (\S+)", log, re.M)
            if not mx:
                out.append(f"{name:11s} {c} {t:4d} | FAILED")
                continue
            e, m0, m1 = (float(x) * 1e3 for x in mx.groups())
            mon = f"{m0:8.2f} {m1:8.2f}" if kind == "direct+mon" else "       -        -"
            out.append(f"{name:11s} {c} {t:4d} | {e:8.2f} | {mon}")
    (T.HERE / "modes.txt").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
