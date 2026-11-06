# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Pad-level characterization for the replica bias (gap runs G1-G6, G9, G10 of docs/replica_bias/SURVEY.md).

ngspice decks on the pads' SOURCE netlists (as testbenches/spice/tb_pad_dc.spice of each pad), with the measurement code
of the pads' CACE templates copied verbatim (S2D: sg13cmos5l_IOPadSingle2Diff_tb_dc.sch, D2S: _tb_dc.sch). vref / vcm /
vicm are ideal sources here unless an experiment says otherwise. Nothing in the pad macros is changed or written.

usage (repo root env: export PDK_ROOT=/foss/pdks; source .designinit):
  python3 -I run_pad_char.py <experiment> [-j 4]
experiments: see EXPERIMENTS at the end. Output: results/<experiment>.tsv (one line per run), decks and logs in _runs/.
"""
import argparse
import itertools
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
MACROS = HERE.parents[2]
RUNS = HERE / "_runs"
RES = HERE / "results"

CORNERS = ["ss", "sf", "tt", "fs", "ff"]
TEMPS = [-40, 27, 125]
VDDS = [3.0, 3.3, 3.6]


def models(c):
    m = c.get("corner_mos", "tt")
    r = c.get("corner_r", "typ")
    return (f".lib cornerMOShv.lib mos_{m}\n.lib cornerMOSlv.lib mos_{m}\n.lib cornerRES.lib res_{r}\n"
            ".lib cornerCAP.lib cap_typ\n.lib cornerPNP.lib typ\n.lib cornerDIO.lib dio_tt\n")


S2D_INC = ["hv_logic/netlist/source/hv_logic.spice", "ls_up_1v2_3v3/netlist/source/ls_up_1v2_3v3.spice",
           "en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice", "sg13cmos5l_IOPadDiff2Single/netlist/source/units.spice",
           "bias_tree_pd/netlist/source/bias_ref_pd.spice", "bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice",
           "bias_gen_pd/netlist/source/bias_gen_pd.spice", "sg13cmos5l_IOPadSingle2Diff/netlist/source/s2d_mpdda.spice",
           "sg13cmos5l_IOPadSingle2Diff/netlist/source/s2d_pd.spice",
           "sg13cmos5l_IOPadSingle2Diff/netlist/source/sg13cmos5l_IOPadSingle2Diff.spice"]
D2S_INC = ["hv_logic/netlist/source/hv_logic.spice", "ls_up_1v2_3v3/netlist/source/ls_up_1v2_3v3.spice",
           "en_ctrl_3v3/netlist/source/en_ctrl_3v3.spice", "sg13cmos5l_IOPadDiff2Single/netlist/source/units.spice",
           "sg13cmos5l_IOPadDiff2Single/netlist/source/ccomp.spice",
           "sg13cmos5l_IOPadDiff2Single/netlist/source/d2s_mpdda_pd.spice",
           "sg13cmos5l_IOPadDiff2Single/netlist/source/d2s_out.spice", "bias_tree_pd/netlist/source/bias_ref_pd.spice",
           "bias_gen_pd/netlist/source/bias_gen_pd.spice",
           "sg13cmos5l_IOPadDiff2Single/netlist/source/sg13cmos5l_IOPadDiff2Single.spice"]


def includes(files, extra=()):
    seen, out = set(), []
    for f in list(files) + list(extra):
        p = f if f.startswith("/") else str(MACROS / f)
        if p not in seen:
            seen.add(p)
            out.append(f".include {p}")
    return "\n".join(out) + "\n.include sg13cmos5l_io.spice\n"


def harness(c, pre=""):
    """slot-side controls, the harness iDAC, en_ctrl_3v3 and bias_gen_pd next to a pad (as the CACE templates)."""
    sel = int(c.get("sel", 0))
    return f"""Vcore{pre} vcore{pre} 0 1.2
Ven{pre} en{pre} 0 {c.get('en', 1.2)}
Vs0{pre} s0{pre} 0 {(sel % 2) * 1.2}
Vs1{pre} s1{pre} 0 {(sel // 2) * 1.2}
Vs12{pre} s12{pre} 0 1.2
Vs33{pre} s33{pre} 0 3.3
Vext{pre} vext{pre} 0 3.3
Iext{pre} xg{pre} 0 {c.get('ibias', 5e-6)}
XEd{pre} xg{pre} xg{pre} vext{pre} vext{pre} sg13_hv_pmos w=5u l=6u
XEm{pre} ibias{pre} xg{pre} vext{pre} vext{pre} sg13_hv_pmos w=5u l=6u
Xc{pre} iovdd vcore{pre} 0 en{pre} s0{pre} s1{pre} s12{pre} s33{pre} en_3v3{pre} sel0_3v3{pre} sel1_3v3{pre} en_3v3_b{pre} en_ctrl_3v3
Xg{pre} iovdd 0 ibias{pre} iref{pre} en_3v3{pre} sel0_3v3{pre} sel1_3v3{pre} bias_gen_pd
"""


OPTS_S2D = ".options savecurrents method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15\n.option warn=1\n"
OPTS_D2S = ".options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15\n.option warn=1\n"


# ------------------------------------------------------------------ S2D DC (template code of _tb_dc.sch)
def deck_s2d_dc(c):
    umax = c.get("umax", 0.5)
    return f"""* S2D pad DC, {c}
{models(c)}{includes(S2D_INC)}
Vio iovdd 0 dc {c['vdd']}
{harness(c)}Vref vref 0 dc {c['vref']}
Vcm vcm 0 {c['vcm']}
Vu u 0 dc 0
Ein vsrc vref u 0 1
Rsrc vsrc pad 50
Cp outp 0 0.5p
Cn outn 0 0.5p
X1 iovdd 0 vcore 0 pad outp outn vcm vref iref en_3v3 en_3v3_b sg13cmos5l_IOPadSingle2Diff
.temp {c['temp']}
{OPTS_S2D}.control
save v(outp) v(outn) v(vcm) v(u) i(vio) i(vcore)
dc Vu -{umax} {umax} 0.005
let vd = v(outp) - v(outn)
let vc = (v(outp) + v(outn))/2 - v(vcm)
meas dc vdp find vd at=0.1
meas dc vdm find vd at=-0.1
meas dc vd0 find vd at=0
meas dc vc0 find vc at=0
let Gain = (vdp - vdm)/0.2
let Vos_in = vd0/Gain
let Vcm_err = vc0
let dev = abs(vd - vd0 - Gain*v(u))/Gain
meas dc INL max dev
let iio = -i(vio)
meas dc Iio find iio at=0
echo RES $&Gain $&Vos_in $&INL $&Vcm_err $&Iio
.endc
.end
"""


S2D_DC_COLS = ["Gain", "Vos_in", "INL", "Vcm_err", "Iio"]

# ------------------------------------------------------------------ S2D OP with saturation margins (G5)
S2D_DEV = {  # name: (instance path below x1, polarity)
    "A1_Ta": ("xa.xs.xa1.xta", "p"), "A1_Ma": ("xa.xs.xa1.xma", "p"), "A1_Mb": ("xa.xs.xa1.xmb", "p"),
    "F1_Ta": ("xa.xs.xf1.xta", "p"), "F1_Tb": ("xa.xs.xf1.xtb", "p"), "F1_Mb": ("xa.xs.xf1.xmb", "p"),
    "M1_Ta": ("xa.xs.xm1.xta", "p"), "SX": ("xa.xs.xsx", "n"), "CX": ("xa.xs.xcx", "n"), "CY": ("xa.xs.xcy", "n"),
    "LP": ("xa.xs.xlp", "p"), "LPC": ("xa.xs.xlpc", "p"), "LNC": ("xa.xs.xlnc", "p"), "D": ("xa.xs.xd", "p"),
}
S2D_NODES = ["x1.vbp", "x1.vbn", "x1.vbpc", "x1.vbnc", "x1.xa.xs.x", "x1.xa.xs.y", "x1.xa.xs.vcmfb", "outp", "outn",
             "x1.xa.xs.xa1.sa", "x1.xa.xs.xf1.sb"]


def devq(path, kind, q):
    return f"@n.x1.{path}.nsg13_hv_{'pmos' if kind == 'p' else 'nmos'}[{q}]"


def deck_s2d_op(c):
    saves = " ".join(f"v({n})" for n in S2D_NODES)
    saves += " " + " ".join(devq(p, k, q) for p, k in S2D_DEV.values() for q in ("ids", "vds", "vdss"))
    prints = []
    for u in c["u_list"]:
        prints.append(f"alter Vu dc={u}\nop")
        items = [f"v({n})" for n in S2D_NODES] + [f"{devq(p, k, 'ids')} {devq(p, k, 'vds')} {devq(p, k, 'vdss')}"
                                                  for p, k in S2D_DEV.values()]
        prints.append("echo OPU " + str(u))
        prints.append("print " + " ".join(items))
    return f"""* S2D pad OP, {c}
{models(c)}{includes(S2D_INC)}
Vio iovdd 0 dc {c['vdd']}
{harness(c)}Vref vref 0 dc {c['vref']}
Vcm vcm 0 {c['vcm']}
Vu u 0 dc 0
Ein vsrc vref u 0 1
Rsrc vsrc pad 50
Cp outp 0 0.5p
Cn outn 0 0.5p
X1 iovdd 0 vcore 0 pad outp outn vcm vref iref en_3v3 en_3v3_b sg13cmos5l_IOPadSingle2Diff
.temp {c['temp']}
{OPTS_S2D}.control
save {saves}
{chr(10).join(prints)}
.endc
.end
"""


# ------------------------------------------------------------------ D2S DC (template code of _tb_dc.sch)
def deck_d2s_dc(c):
    vterm = c.get("vterm", c["vref"])
    return f"""* D2S pad DC, {c}
{models(c)}{includes(D2S_INC)}
Vio iovdd 0 dc {c['vdd']}
{harness(c)}Vref vref 0 {c['vref']}
Vic vic 0 dc {c['vicm']}
Vd dp 0 dc 0
Ep vinp vic dp 0 0.5
En vinn vic dp 0 -0.5
RL pad vterm {c.get('rload', 1000)}
Vterm vterm 0 {vterm}
CL pad 0 100p
X1 iovdd 0 vcore 0 pad vinp vinn vref iref en_3v3 en_3v3_b sg13cmos5l_IOPadDiff2Single
.temp {c['temp']}
{OPTS_D2S}.control
save v(pad) v(vref) v(dp) i(vio) i(vcore) @n.x1.xfp.xop.nsg13_hv_pmos[ids] @n.x1.xfn.xon.nsg13_hv_nmos[ids]
dc Vd -1 1 0.01
let vo = v(pad) - v(vref)
meas dc vo0 find vo at=0
meas dc vop find vo at=0.2
meas dc vom find vo at=-0.2
let Gain = (vop - vom) / (2*0.2)
let Vos_out = vo0
let dev = abs(vo - vo0 - Gain*v(dp))
meas dc INL max dev
let iio = -i(vio)
meas dc Iio find iio at=0
let ip = abs(@n.x1.xfp.xop.nsg13_hv_pmos[ids])
let inn = abs(@n.x1.xfn.xon.nsg13_hv_nmos[ids])
meas dc IqP find ip at=0
meas dc IqN find inn at=0
let imn = 0.5*(ip + inn - abs(ip - inn))
meas dc ImA find imn at=-1
meas dc ImB find imn at=1
let Imin = 0.5*(ImA + ImB - abs(ImA - ImB))
echo RES $&Gain $&Vos_out $&INL $&Iio $&IqP $&Imin
.endc
.end
"""


D2S_DC_COLS = ["Gain", "Vos_out", "INL", "Iio", "IqP", "Imin"]

D2S_DEV = {"A_Ta": ("xd.xa.xta", "p"), "A_Ma": ("xd.xa.xma", "p"), "C1_Ta": ("xd.xc1.xta", "p"),
           "C1_Mb": ("xd.xc1.xmb", "p"), "SX": ("xd.xsx", "n"), "CX": ("xd.xcx", "n"), "CY": ("xd.xcy", "n"),
           "PL": ("xd.xpl", "p"), "PCR": ("xd.xpcr", "p")}
D2S_NODES = ["x1.vbp", "x1.vbn", "x1.vbpc", "x1.vbnc", "x1.xd.x", "x1.xd.y", "x1.a", "x1.b", "pad"]


def deck_d2s_op(c):
    vterm = c.get("vterm", c["vref"])
    saves = " ".join(f"v({n})" for n in D2S_NODES)
    saves += " " + " ".join(devq(p, k, q) for p, k in D2S_DEV.values() for q in ("ids", "vds", "vdss"))
    prints = []
    for vd in c["vd_list"]:
        prints.append(f"alter Vd dc={vd}\nop")
        items = [f"v({n})" for n in D2S_NODES] + [f"{devq(p, k, 'ids')} {devq(p, k, 'vds')} {devq(p, k, 'vdss')}"
                                                  for p, k in D2S_DEV.values()]
        prints.append("echo OPU " + str(vd))
        prints.append("print " + " ".join(items))
    return f"""* D2S pad OP, {c}
{models(c)}{includes(D2S_INC)}
Vio iovdd 0 dc {c['vdd']}
{harness(c)}Vref vref 0 {c['vref']}
Vic vic 0 dc {c['vicm']}
Vd dp 0 dc 0
Ep vinp vic dp 0 0.5
En vinn vic dp 0 -0.5
RL pad vterm 1000
Vterm vterm 0 {vterm}
CL pad 0 100p
X1 iovdd 0 vcore 0 pad vinp vinn vref iref en_3v3 en_3v3_b sg13cmos5l_IOPadDiff2Single
.temp {c['temp']}
{OPTS_D2S}.control
save {saves}
{chr(10).join(prints)}
.endc
.end
"""


# ------------------------------------------------------------------ round trip S2D pad -> D2S pad (G9)
def deck_loop(c):
    return f"""* round trip S2D pad -> D2S pad, {c}
{models(c)}{includes(S2D_INC, D2S_INC)}
Vio iovdd 0 dc {c['vdd']}
{harness(c, 's')}{harness(c, 'd')}Vrefs vrefs 0 {c['vref_s2d']}
Vcm vcm 0 {c['vcm']}
Vu u 0 dc 0
Ein vsrc vrefs u 0 1
Rsrc vsrc pin 50
Xs iovdd 0 vcores 0 pin dp dn vcm vrefs irefs en_3v3s en_3v3_bs sg13cmos5l_IOPadSingle2Diff
Cwp dp 0 0.5p
Cwn dn 0 0.5p
Xd iovdd 0 vcored 0 pout dp dn vcm irefd en_3v3d en_3v3_bd sg13cmos5l_IOPadDiff2Single
RL pout vcm 1000
CL pout 0 100p
.temp {c['temp']}
{OPTS_S2D}.control
save v(pout) v(vcm) v(u) v(dp) v(dn) i(vio)
dc Vu -0.5 0.5 0.005
let vo = v(pout) - v(vcm)
meas dc vop find vo at=0.1
meas dc vom find vo at=-0.1
meas dc vo0 find vo at=0
let Gain = (vop - vom)/0.2
let Vos = vo0
let dev = abs(vo - vo0 - Gain*v(u))
meas dc INL max dev
let vdi = v(dp) - v(dn)
meas dc vdi0 find vdi at=0
let iio = -i(vio)
meas dc Iio find iio at=0
echo RES $&Gain $&Vos $&INL $&vdi0 $&Iio
.endc
.end
"""


LOOP_COLS = ["Gain", "Vos", "INL", "Vd_s2d0", "Iio"]


# ------------------------------------------------------------------ G6: source impedance of vref / vcm
# The ideal sources Vref / Vcm feed the pad pins vrefi / vcmi through Rs, with Cb from the pin to ground. The pad's input
# source is referenced to the EXTERNAL vref (it must not follow the disturbed pin).
def zsrc(c, names=("vref", "vcm")):
    s = ""
    for n in names:
        s += f"R{n} {n} {n}i {c['rs']}\n"
        if c["cb"]:
            s += f"C{n} {n}i 0 {c['cb']}\n"
    return s


def s2d_bench_z(c, vu, en="1.2"):
    cc = dict(c, en=en)
    return f"""{models(c)}{includes(S2D_INC)}
Vio iovdd 0 dc {c['vdd']} ac 0
{harness(cc)}Vref vref 0 dc {c['vref']}
Vcm vcm 0 {c['vcm']}
{zsrc(c)}Vu u 0 {vu}
Ein vsrc vref u 0 1
Rsrc vsrc pad 50
Cp outp 0 0.5p
Cn outn 0 0.5p
X1 iovdd 0 vcore 0 pad outp outn vcmi vrefi iref en_3v3 en_3v3_b sg13cmos5l_IOPadSingle2Diff
.temp {c['temp']}
"""


def deck_s2d_ac_z(c):
    return f"""* S2D AC with source impedance, {c}
{s2d_bench_z(c, 'dc 0 ac 1')}{OPTS_S2D}.control
save v(outp) v(outn) v(vrefi) v(vcmi)
ac dec 20 10 100meg
let vd = v(outp) - v(outn)
let A = mag(vd)
meas ac a1k find A at=1k
let a3 = a1k/sqrt(2)
let f3dB = 1e12
meas ac f3dB when A=a3 fall=1
let Acl_dB = 20*log10(a1k)
let kr = mag(v(vrefi))
let kc = mag(v(vcmi))
meas ac kr1k find kr at=1k
meas ac kr100k find kr at=100k
meas ac kc100k find kc at=100k
echo RES $&Acl_dB $&f3dB $&kr1k $&kr100k $&kc100k
.endc
.end
"""


def deck_s2d_tran_z(c):
    return f"""* S2D step with source impedance, {c}
{s2d_bench_z(c, 'pulse(-0.25 0.25 1u 1n 1n 4u 10u)')}.options savecurrents method=gear reltol=1e-4 abstol=1e-12 gmin=1e-12
.option warn=1
.control
save v(outp) v(outn) v(vcm) v(vrefi) v(vcmi) v(vref)
tran 1n 5u
let vd = v(outp) - v(outn)
let vc = (v(outp) + v(outn))/2 - v(vcm)
meas tran vlo find vd at=0.99u
meas tran vhi find vd at=4.9u
let band = 0.01*abs(vhi - vlo)
let dev = abs(vd - vhi)
meas tran tlast when dev=band cross=last
let t_settle = tlast - 1.0005u
let avc = abs(vc)
meas tran Vcm_dev max avc from=1u to=4.9u
let er = abs(v(vrefi) - v(vref))
let ec = abs(v(vcmi) - v(vcm))
meas tran dvref max er from=1u to=4.9u
meas tran dvcm max ec from=1u to=4.9u
echo RES $&t_settle $&Vcm_dev $&dvref $&dvcm $&vhi
.endc
.end
"""


def deck_s2d_en_z(c):
    return f"""* S2D enable with source impedance, {c}
{s2d_bench_z(c, 'dc 0.25', en='pwl(0 0 1u 0 1.001u 1.2)')}.options savecurrents method=gear reltol=1e-4 abstol=1e-12 gmin=1e-12
.option warn=1
.control
save v(outp) v(outn) v(vcm) v(vcmi) v(vrefi) v(vref) i(vio)
tran 5n 10u
let vd = v(outp) - v(outn)
let vc = (v(outp) + v(outn))/2 - v(vcm)
meas tran vd_end find vd at=10u
let ee = abs(vd - vd_end)
meas tran t1 when ee=1m cross=last from=1u to=10u
let t_on = t1 - 1u
meas tran Vc_max max vc from=1u to=10u
meas tran Vc_min min vc from=1u to=10u
let ec = v(vcmi) - v(vcm)
meas tran dvcm_max max ec from=1u to=10u
meas tran dvcm_min min ec from=1u to=10u
let er = abs(v(vrefi) - v(vref))
meas tran dvref max er from=1u to=10u
echo RES $&t_on $&Vc_max $&Vc_min $&dvcm_max $&dvcm_min $&dvref $&vd_end
.endc
.end
"""


def d2s_bench_z(c, vd):
    return f"""{models(c)}{includes(D2S_INC)}
Vio iovdd 0 dc {c['vdd']} ac 0
{harness(c)}Vref vref 0 {c['vref']}
{zsrc(c, ('vref',))}Vic vic 0 dc {c['vicm']} ac 0
Vd dp 0 {vd}
Ep vinp vic dp 0 0.5
En vinn vic dp 0 -0.5
RL pad vterm 1000
Vterm vterm 0 {c['vref']}
CL pad 0 100p
X1 iovdd 0 vcore 0 pad vinp vinn vrefi iref en_3v3 en_3v3_b sg13cmos5l_IOPadDiff2Single
.temp {c['temp']}
"""


def deck_d2s_ac_z(c):
    return f"""* D2S AC with source impedance, {c}
{d2s_bench_z(c, 'dc 0 ac 1')}{OPTS_D2S}.control
save v(pad) v(vrefi)
ac dec 50 1 1G
let adb = vdb(pad)
meas ac Acl find adb at=1k
let adn = adb - Acl
let f3db = 0
meas ac f3db when adn=-3 fall=1
meas ac Apk max adn
let kr = mag(v(vrefi))
meas ac kr1k find kr at=1k
meas ac kr100k find kr at=100k
echo RES $&Acl $&f3db $&Apk $&kr1k $&kr100k
.endc
.end
"""


def deck_d2s_tran_z(c):
    return f"""* D2S step with source impedance, {c}
{d2s_bench_z(c, 'pulse(-0.5 0.5 1u 1n 1n 4u 8u)')}.options savecurrents klu method=gear reltol=1e-4 abstol=1e-12 gmin=1e-12
.option warn=1
.control
save v(pad) v(vrefi) v(vref)
tran 2n 9u
meas tran v0 find v(pad) at=0.99u
meas tran v1 find v(pad) at=4.9u
let dv = v1 - v0
let vn = (v(pad) - v0) / dv
meas tran vnmax max vn from=1u to=5u
let Overshoot = vnmax - 1
let er = abs(vn - 1)
let tsr = 1u
meas tran tsr when er=0.01 cross=last from=1u to=5u
let ts_rise = tsr - 1u
let e2 = abs(v(vrefi) - v(vref))
meas tran dvref max e2 from=1u to=9u
echo RES $&ts_rise $&Overshoot $&dvref $&dv
.endc
.end
"""


def zgrid(pad):
    base = dict(vref=0.5, vcm=1.2) if pad == "s2d" else dict(vref=1.2, vicm=1.2)
    for rs, cb, m in itertools.product([1e-3, 1e3, 1e4, 1e5, 1e6], [0, 1e-12], ["ss", "tt", "ff"]):
        yield dict(vdd=3.3, corner_mos=m, temp=27, rs=rs, cb=cb, **base)


# ------------------------------------------------------------------ runner
def complete(out, kind, ncol):
    if kind == "op":
        return bool(parse_op(out))
    r = parse_res(out)
    return r is not None and len(r) == ncol and all(not x.startswith("$") for x in r)


def run_one(args):
    """Runs a deck; if it gives no complete result (the operating point failed: seen at tt / -40 C in the disabled
    bandgap core's floating rhigh chain), runs it once more with .options rshunt=1e12 (1 TOhm from every node to
    ground). Returns (name, returncode, seconds, stdout, convergence note)."""
    name, deck, kind, ncol = args
    p = RUNS / f"{name}.spice"
    p.write_text(deck)
    t0 = time.time()
    r = subprocess.run(["ngspice", "-b", str(p)], capture_output=True, text=True, cwd=RUNS, timeout=1800)
    (RUNS / f"{name}.log").write_text(r.stdout + "\n" + r.stderr)
    note = "ok"
    if not complete(r.stdout, kind, ncol):
        p2 = RUNS / f"{name}_rshunt.spice"
        p2.write_text(deck.replace(".control\n", ".options rshunt=1e12\n.control\n", 1))
        r = subprocess.run(["ngspice", "-b", str(p2)], capture_output=True, text=True, cwd=RUNS, timeout=1800)
        (RUNS / f"{name}_rshunt.log").write_text(r.stdout + "\n" + r.stderr)
        note = "rshunt" if complete(r.stdout, kind, ncol) else "failed"
    return name, r.returncode, time.time() - t0, r.stdout, note


def parse_res(out):
    for l in out.splitlines():
        if l.startswith("RES "):
            return l.split()[1:]
    return None


def parse_op(out):
    """returns {u: {name: value}} from 'echo OPU u' + 'print' blocks (ngspice prints 'name = value')."""
    res, cur = {}, None
    for l in out.splitlines():
        m = re.match(r"OPU (\S+)", l)
        if m:
            cur = m.group(1)
            res[cur] = {}
            continue
        m = re.match(r"\s*(\S+)\s*=\s*(\S+)", l)
        if cur is not None and m:
            try:
                res[cur][m.group(1)] = float(m.group(2))
            except ValueError:
                pass
    return res


def grid(**axes):
    keys = list(axes)
    for vals in itertools.product(*(axes[k] for k in keys)):
        yield dict(zip(keys, vals))


def tag(c):
    return "_".join(f"{k}{v}" for k, v in c.items() if not isinstance(v, (list, tuple))).replace("-", "m")


def experiment(name, jobs):
    E = EXPERIMENTS[name]
    conds = list(E["conds"]())
    RUNS.mkdir(exist_ok=True)
    RES.mkdir(exist_ok=True)
    work = [(f"{name}__{i:04d}", E["deck"](c), E["kind"], len(E.get("cols", []))) for i, c in enumerate(conds)]
    t0 = time.time()
    with ThreadPoolExecutor(jobs) as ex:
        outs = list(ex.map(run_one, work))
    keys = [k for k in conds[0] if not isinstance(conds[0][k], (list, tuple))]
    fail = 0
    with open(RES / f"{name}.tsv", "w") as f:
        f.write(f"# {name}: {E['what']}\n# {len(conds)} runs, {time.time() - t0:.0f} s wall with -j {jobs}, "
                f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; SI units\n")
        if E["kind"] == "op":
            first = None
            for c, (n, rc, dt, out, note) in zip(conds, outs):
                ops = parse_op(out)
                for u, vals in ops.items():
                    if first is None:
                        first = list(vals)
                        f.write("\t".join(keys + ["u"] + first + ["conv"]) + "\n")
                    f.write("\t".join([str(c[k]) for k in keys] + [u] + [f"{vals.get(q, float('nan')):.6g}"
                                                                         for q in first] + [note]) + "\n")
                if not ops:
                    fail += 1
        else:
            f.write("\t".join(keys + E["cols"] + ["conv"]) + "\n")
            for c, (n, rc, dt, out, note) in zip(conds, outs):
                r = parse_res(out)
                if note == "failed" or r is None or len(r) != len(E["cols"]):
                    fail += 1
                    r = ["nan"] * len(E["cols"])
                f.write("\t".join([str(c[k]) for k in keys] + r + [note]) + "\n")
    print(f"{name}: {len(conds)} runs, {fail} without result, {time.time() - t0:.0f} s -> {RES / (name + '.tsv')}")
    return fail


EXPERIMENTS = {
    # validation against committed CACE points (S2D range_params 2026-11-05; D2S CACE-2.11 smoke run 2026-11-06)
    "val_s2d": dict(what="S2D DC deck against CACE range_params / dc_params points", kind="dc", deck=deck_s2d_dc,
                    cols=S2D_DC_COLS, conds=lambda: [
                        dict(vdd=3.0, vref=1.2, vcm=1.4, corner_mos="ss", temp=-40),
                        dict(vdd=3.0, vref=0.5, vcm=1.0, corner_mos="ff", temp=125),
                        dict(vdd=3.0, vref=1.65, vcm=1.2, corner_mos="tt", temp=125),
                        dict(vdd=3.3, vref=1.2, vcm=1.2, corner_mos="tt", temp=27)]),
    "val_d2s": dict(what="D2S DC deck against the CACE-2.11 dc_ibias point (tt 27 C 3.3 V, vref = vicm = vterm = 1.65)",
                    kind="dc", deck=deck_d2s_dc, cols=D2S_DC_COLS, conds=lambda: [
                        dict(vdd=3.3, vref=1.65, vicm=1.65, vterm=1.65, corner_mos="tt", temp=27)]),
    # G3: S2D vcm band at pad level
    "g3_s2d_vcm": dict(what="S2D INL (u = +-0.5 V) vs vcm at vref 0.8 V", kind="dc", deck=deck_s2d_dc,
                       cols=S2D_DC_COLS, conds=lambda: grid(
                           vdd=VDDS, corner_mos=CORNERS, temp=TEMPS, vref=[0.8],
                           vcm=[0.8, 0.9, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6, 1.7])),
    # G4: S2D vref band at pad level
    "g4_s2d_vref": dict(what="S2D INL (u = +-0.5 V) vs vref at vcm 1.2 V", kind="dc", deck=deck_s2d_dc,
                        cols=S2D_DC_COLS, conds=lambda: grid(
                            vdd=VDDS, corner_mos=CORNERS, temp=TEMPS, vcm=[1.2],
                            vref=[0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 1.0, 1.2, 1.3, 1.4])),
    # G1: D2S band, vref = vicm, load to vterm = vref
    "g1_d2s_vref": dict(what="D2S INL (vd = +-1 V) vs vref = vicm, 1 kOhm || 100 pF to vterm = vref", kind="dc",
                        deck=deck_d2s_dc, cols=D2S_DC_COLS, conds=lambda: (
                            dict(vdd=v, corner_mos=m, temp=t, vref=x, vicm=x) for v, m, t, x in itertools.product(
                                VDDS, CORNERS, TEMPS, [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.65]))),
    # G2: D2S tolerance to vicm != vref
    "g2_d2s_vicm": dict(what="D2S INL / gain / offset vs vicm - vref at vref 1.2 V", kind="dc", deck=deck_d2s_dc,
                        cols=D2S_DC_COLS, conds=lambda: (
                            dict(vdd=v, corner_mos=m, temp=t, vref=1.2, vicm=round(1.2 + d, 3))
                            for v, (m, t), d in itertools.product(
                                [3.0, 3.3], [("ss", -40), ("tt", 27), ("ff", 125), ("ss", 125), ("ff", -40)],
                                [-0.3, -0.2, -0.1, -0.05, 0, 0.05, 0.1, 0.2, 0.3]))),
    # G10: bias source at the edge corners
    "g10_s2d_sel": dict(what="S2D INL vs vcm per bias selection (0 harness, 1 OA, 2 bandgap), edge corners, 3.0 V",
                        kind="dc", deck=deck_s2d_dc, cols=S2D_DC_COLS, conds=lambda: (
                            dict(vdd=3.0, corner_mos=m, temp=t, sel=s, vref=0.8, vcm=x)
                            for (m, t), s, x in itertools.product(
                                [("ss", -40), ("ss", 125), ("ff", 125), ("tt", 27)], [0, 1, 2],
                                [0.9, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4]))),
    "g10_d2s_sel": dict(what="D2S INL vs vref = vicm per bias selection, edge corners, 3.0 V", kind="dc",
                        deck=deck_d2s_dc, cols=D2S_DC_COLS, conds=lambda: (
                            dict(vdd=3.0, corner_mos=m, temp=t, sel=s, vref=x, vicm=x)
                            for (m, t), s, x in itertools.product(
                                [("ss", -40), ("ss", 125), ("ff", 125), ("tt", 27)], [0, 1, 2],
                                [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]))),
    # G5: operating points and saturation margins at u = -0.5 / 0 / +0.5 V
    "g5_s2d_op": dict(what="S2D OP (nodes, ids / vds / vdss of key devices) at vref 0.8, vcm 1.2, u = -0.5/0/+0.5",
                      kind="op", deck=deck_s2d_op, conds=lambda: (
                          dict(vdd=v, corner_mos=m, temp=t, sel=s, vref=0.8, vcm=1.2, u_list=[-0.5, 0, 0.5])
                          for v, m, t, s in itertools.product(VDDS, CORNERS, TEMPS, [0, 1, 2]))),
    "g5_d2s_op": dict(what="D2S OP at vref = vicm = 1.2, vd = -1/0/+1", kind="op", deck=deck_d2s_op, conds=lambda: (
        dict(vdd=v, corner_mos=m, temp=t, sel=s, vref=1.2, vicm=1.2, vd_list=[-1, 0, 1])
        for v, m, t, s in itertools.product(VDDS, CORNERS, TEMPS, [0, 1, 2]))),
    # G9: round trip at pad level
    "g9_loop": dict(what="round trip S2D pad (vref_s2d) -> D2S pad (vref = vcm), out - vcm vs pad - vref_s2d",
                    kind="dc", deck=deck_loop, cols=LOOP_COLS, conds=lambda: (
                        dict(vdd=v, corner_mos=m, temp=t, vref_s2d=r, vcm=1.2)
                        for v, m, t, r in itertools.product(VDDS, CORNERS, TEMPS, [0.5, 1.2]))),
    # G6: source impedance Rs (and bypass Cb) in series with vref / vcm
    "g6_s2d_ac": dict(what="S2D closed-loop AC with Rs / Cb on vref and vcm (vref 0.5, vcm 1.2); kr / kc = |v(pin)| / |u|",
                      kind="dc", deck=deck_s2d_ac_z, cols=["Acl_dB", "f3dB", "kr1k", "kr100k", "kc100k"],
                      conds=lambda: zgrid("s2d")),
    "g6_s2d_tran": dict(what="S2D step u -0.25 -> +0.25 V with Rs / Cb on vref and vcm; pin deviations from the sources",
                        kind="dc", deck=deck_s2d_tran_z, cols=["t_settle", "Vcm_dev", "dvref", "dvcm", "vd_hi"],
                        conds=lambda: zgrid("s2d")),
    "g6_s2d_en": dict(what="S2D enable (en_1v2 at 1 us, u = +0.25 V) with Rs / Cb on vref and vcm", kind="dc",
                      deck=deck_s2d_en_z, cols=["t_on", "Vc_max", "Vc_min", "dvcm_max", "dvcm_min", "dvref", "vd_end"],
                      conds=lambda: zgrid("s2d")),
    "g6_d2s_ac": dict(what="D2S closed-loop AC with Rs / Cb on vref (vref = vicm = vterm = 1.2); kr = |v(vrefi)| / |vd|",
                      kind="dc", deck=deck_d2s_ac_z, cols=["Acl_dB", "f3dB", "Peak_dB", "kr1k", "kr100k"],
                      conds=lambda: zgrid("d2s")),
    "g6_d2s_tran": dict(what="D2S step vd -0.5 -> +0.5 V with Rs / Cb on vref", kind="dc", deck=deck_d2s_tran_z,
                        cols=["ts_rise", "Overshoot", "dvref", "dv"], conds=lambda: zgrid("d2s")),
}

def keys_of(conds):
    return [k for k in conds[0] if not isinstance(conds[0][k], (list, tuple))]


def rerun_failed(name, jobs):
    """Reruns (with the rshunt retry of run_one) only the runs of results/<name>.tsv without a result, in place."""
    E = EXPERIMENTS[name]
    conds = list(E["conds"]())
    lines = open(RES / f"{name}.tsv").read().splitlines()
    head = [l for l in lines if l.startswith("#")]
    hdr = [l for l in lines if not l.startswith("#")][0]
    body = [l for l in lines if not l.startswith("#")][1:]
    assert len(body) == len(conds), "rerun_failed: the TSV does not match the experiment's conditions"
    nf = len(keys_of(conds)) + len(E["cols"])
    idx = [i for i, l in enumerate(body) if "nan" in l.split("\t") or len(l.split("\t")) < nf]
    work = [(f"{name}__{i:04d}", E["deck"](conds[i]), E["kind"], len(E.get("cols", []))) for i in idx]
    with ThreadPoolExecutor(jobs) as ex:
        outs = list(ex.map(run_one, work))
    keys = [k for k in conds[0] if not isinstance(conds[0][k], (list, tuple))]
    fail = 0
    for i, (n, rc, dt, out, note) in zip(idx, outs):
        r = parse_res(out)
        if note == "failed" or r is None or len(r) != len(E["cols"]):
            fail += 1
            r = ["nan"] * len(E["cols"])
        body[i] = "\t".join([str(conds[i][k]) for k in keys] + r + [note])
    if "conv" not in hdr.split("\t"):
        hdr += "\tconv"
        body = [l if len(l.split("\t")) == len(hdr.split("\t")) else l + "\tok" for l in body]
    head.append(f"# {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}: rerun of {len(idx)} runs without a result "
                f"(rshunt retry), {fail} still without")
    open(RES / f"{name}.tsv", "w").write("\n".join(head + [hdr] + body) + "\n")
    print(f"{name}: reran {len(idx)}, {fail} still without a result")
    return fail


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("experiments", nargs="+")
    ap.add_argument("-j", type=int, default=4)
    ap.add_argument("--rerun-failed", action="store_true")
    a = ap.parse_args()
    f = rerun_failed if a.rerun_failed else experiment
    bad = sum(f(e, a.j) for e in a.experiments)
    sys.exit(1 if bad else 0)
