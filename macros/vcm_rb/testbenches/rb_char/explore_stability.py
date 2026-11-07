# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""How much capacitance must stay inside vcm_rb and vref_s2d_rb for stability (Christoph, 2026-11-07: the bypass
capacitors go into a cell of their own, "unless an absolute minimum of capacitors is necessary for stability").

Each block alone (no pads, no other capacitor), its capacitors (XCB*) replaced by one ideal capacitor C on its output.
  stab_vcm   vcm_rb's buffer is a 5T OTA in unity gain. An AC source in series with BA's gate (the non-inverting input,
             node m) gives the closed-loop response H = v(vcm) / v(inj): its peak against the 1 kHz value (1.0 = no
             peaking, about 60 deg phase margin or more; 1.3 is about 45 deg) and the -3 dB bandwidth. C = 0 ... 0.6 pF.
             (Breaking the loop at BB's gate fails without load capacitance: BB's own gate capacitance couples the
             injection into vcm, and |T| never falls below 1.)
  stab_vref  vref_s2d_rb is a source follower, no loop. |Z(f)| of vref (1 A AC into the node): its peak against the
             1 kHz value (> 1 = resonant peaking, the follower's inductive output impedance against C). C = 0, 0.5, 2 pF.
sel 0, 3.0 / 3.6 V, ss / tt / ff, -40 / 27 / 125 C. Results in results/stab_*.tsv.
usage: python3 -I explore_stability.py stab_vcm stab_vref -j N
"""
import argparse
import itertools
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_rb as B  # noqa: E402

R = B.R
VAR = HERE / "_runs" / "stab_netlists"


def variant(block, out, c_f, brk=False):
    """copy of the block's netlist with every capacitor device (XCB*) replaced by one ideal C on the output; brk: BA's
    gate on its own node mi, driven from m through an AC injection source."""
    VAR.mkdir(parents=True, exist_ok=True)
    src = Path(B.MAC / block / "netlist/source" / f"{block}.spice").read_text()
    s = re.sub(r"^XCB\S* .*\n", "", src, flags=re.M)
    extra = f"Cstab {out} vss {c_f:g}\n"
    if brk:
        assert "XBA bd m bt bt" in s
        s = s.replace("XBA bd m bt bt", "XBA bd mi bt bt")
        extra += "Vinj mi m dc 0 ac 1\n"
    s = s.replace(f".ends {block}", extra + f".ends {block}")
    p = VAR / f"{block}_C{c_f:g}{'_brk' if brk else ''}.spice"
    p.write_text(s)
    return str(p)


def deck_stab(c):
    vcm = c["node"] == "vcm"
    block, out = ("vcm_rb", "vcm") if vcm else ("vref_s2d_rb", "vref")
    d = B.deck_rb_dc(c).replace("Xbyp 0 vcm vref bypass_rb\n", "")  # the block alone, without the bypass cell
    d = d.replace(str(B.MAC / block / "netlist/source" / f"{block}.spice"), variant(block, out, c["C"], brk=vcm))
    ctl = d[d.index(".control"):]
    if vcm:
        return d.replace(ctl, """.control
op
ac dec 50 100 2g
let H = mag(v(vcm))
meas ac h1k find H at=1e3
meas ac hpk max H
let pk = hpk/h1k
let h3 = h1k/sqrt(2)
meas ac f3 when H=h3 fall=1
echo RES $&h1k $&pk $&f3
.endc
.end
""")
    return d.replace(ctl, """Iz 0 vref dc 0 ac 1
.control
op
ac dec 50 100 2g
let Z = mag(v(vref))
meas ac z1k find Z at=1e3
meas ac zpk max Z
let pk = zpk/z1k
meas ac fpk when Z=zpk
echo RES $&z1k $&zpk $&pk
.endc
.end
""")


def conds(node, caps):
    for C, vdd, m, t in itertools.product(caps, [3.0, 3.6], ["ss", "tt", "ff"], [-40, 27, 125]):
        yield dict(node=node, C=C, vdd=vdd, corner_mos=m, temp=t, sel=0)


EXP = {
    "stab_vcm": dict(what="vcm_rb alone, CB replaced by ideal C on vcm; closed-loop response from BA's gate to vcm: "
                          "|H| at 1 kHz, peak / 1 kHz, -3 dB bandwidth", kind="dc", deck=deck_stab,
                     cols=["H_1k", "peak_ratio", "f_3dB"],
                     conds=lambda: conds("vcm", [0, 20e-15, 50e-15, 100e-15, 200e-15, 600e-15])),
    "stab_vref": dict(what="vref_s2d_rb alone, CB1 / CB2 replaced by ideal C on vref: |Z| at 1 kHz, its peak, peak / 1 kHz",
                      kind="dc", deck=deck_stab, cols=["Z_1k", "Z_peak", "peak_ratio"],
                      conds=lambda: conds("vref", [0, 500e-15, 2e-12])),
}

if __name__ == "__main__":
    R.EXPERIMENTS.update(EXP)
    ap = argparse.ArgumentParser()
    ap.add_argument("experiments", nargs="+")
    ap.add_argument("-j", type=int, default=2)
    a = ap.parse_args()
    sys.exit(1 if sum(R.experiment(e, a.j) for e in a.experiments) else 0)
