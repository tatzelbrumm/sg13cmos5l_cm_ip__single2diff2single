# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""CACE suite of analog_pswitch_small (harness cell of sg13cmos5l_ocd_chipalooza, Tim Edwards / Open Circuit Design):
four templates (xschem sheets with MODEL / SOURCES / NGSPICE code blocks; the DUT's lab_pins sit on the pins read from
analog_pswitch_small.sym) and the yaml.  Pattern of macros/pad_ref_rb/verification/gen_cace.py.

The DUT sheets are byte-identical harness copies and are NOT touched.  Two simulation details the templates handle:
 1. xschem netlists the three standard cells of the sheet (sg13cmos5l_inv_4, _antennanp, _decap_4) as EMPTY subcircuits
    (their .sch views are not in the PDK install).  ngspice keeps the FIRST definition of a subcircuit and ignores later
    ones ("redefinition of .subckt ..., ignored"), so every template includes the PDK's sg13cmos5l_stdcell.spice BEFORE
    the DUT netlist (both in the NGSPICE block, in that order).
 2. ngspice-47 stalls (time step collapses, no abort) in a transient through the PDK antenna diode `dantenna` at
    85 C and above (model darea, tt = 701 ns; found by bisection: tt = 0 removes the stall, the other parameters do
    not).  The transient templates therefore define sg13cmos5l_antennanp first, identical to the PDK cell except that
    darea's transit time is 0.  tt only adds diffusion charge in FORWARD bias, which the enable input never sees in
    these tests; at tt / 27 C (where the PDK cell runs) the results with and without the change agree to 5 digits.
    The DC templates use the unmodified PDK cell.

usage: python3 -I gen_cace.py   (writes macros/ocd_analog_switches/verification/cace/{analog_pswitch_small.yaml, templates/})
"""
import re
from pathlib import Path

MAC = Path(__file__).resolve().parents[1]
TOP = "analog_pswitch_small"
SYM = MAC / "schematic/xschem" / f"{TOP}.sym"
RC = MAC.parent / "en_ctrl_3v3/verification/cace/templates/xschemrc"   # same template xschemrc as the other macros

MODEL = r""".lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerMOSlv.lib mos_CACE\{corner_mos\}
.lib cornerDIO.lib dio_tt"""

# antenna cell with darea's transit time set to 0 (see the docstring); model card = PDK diodes.lib darea, tt changed
ANT = r"""* ---- sg13cmos5l_antennanp as in the PDK, but darea with tt = 0 (ngspice stalls on tt = 701 ns above 85 C in transients)
.subckt sg13cmos5l_antennanp A VDD VSS
XD1 VSS A dantenna_tt0 l=780n w=780n m=1
XD0 A VDD dpantenna l=1.34u w=1.05u m=1
.ends
.subckt dantenna_tt0 1 2
.params l=780n w=780n DEV_A=(l*w)/1p DEV_P=(l+w)/0.5u DEV_C=4
D1 1 2 darea_tt0 area=DEV_A
D2 1 2 dperim area=DEV_P
D3 1 2 dcorner area=DEV_C
.ends
.model darea_tt0 D (tnom=27 is=2.315E-019 n=1.009 ik=1.434E-007 rs=2.193E+005 cj0=9.371E-016 m=0.3036 vj=0.696 fc=0.5
+ bv=11.64 ibv=3.458E-007 tcv=0.001 nbv=48.9 isr=7.413E-019 xti=5.039 trs=0 trs2=0 tt=0)"""

INC = r"""* ---- the PDK standard cells FIRST: the DUT netlist below defines them again as empty subcircuits (ignored by ngspice)
.include sg13cmos5l_stdcell.spice
.include CACE\{DUT_path\}
.temp CACE\{temp\}"""

ECHO = r"> CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data"

# ------------------------------------------------------------------ DC: switch between two voltage sources
DC_VARS = ["R_sw", "I_out", "I_in", "I_dvdd", "I_avdd", "I_en", "Vg"]
DC_SRC = r"""* case: 0 on (enable = dvdd) | 1 off (enable = 0) | 2 dvdd = 0, enable = 0, latch preset ON | 3 same, preset OFF
.param c=CACE\{case=0\}
.param vdd_d='(c >= 2) ? 0 : CACE\{dvdd=1.2\}'
.param ven='(c == 0) ? CACE\{dvdd=1.2\} : 0'
* vin < 0: in follows out - 10 mV (on-resistance); else in = vin.  out is swept vout - 10 mV .. vout in the analysis.
.param vo=CACE\{vout=1.0\}
.param vi='(CACE\{vin=-1\} < 0) ? vo - 0.01 : CACE\{vin=-1\}'
Vdd dvdd 0 \{vdd_d\}
Vav avdd 0 CACE\{avdd=3.3\}
Ven enable 0 \{ven\}
Vout out 0 \{vo\}
Vin in 0 \{vi\}
* level-shifter latch preset (x1.x5 = sw_lvl_shift; ON: net1 low, S1_N high).  Driven cases: the input decides
* (the transient groups show that it can flip the latch); cases 2 / 3: the DC state that the preset falls into.
.nodeset v(x1.x5.net1)=CACE[CACE\{avdd=3.3\} * (CACE\{case=0\} % 2)] v(x1.x5.s1_n)=CACE[CACE\{avdd=3.3\} * (1 - CACE\{case=0\} % 2)]"""
DC_NG = INC + r"""
.options gmin=1e-15 abstol=1e-15 reltol=1e-4
.option warn=1
.control
dc Vout CACE[CACE\{vout=1.0\} - 0.01] CACE[CACE\{vout=1.0\} + 0.0001] 0.01
let iout = -i(Vout)
let iin = -i(Vin)
let idd = -i(Vdd)
let iav = -i(Vav)
let ien = -i(Ven)
let vg = v(x1.net3)
* R_sw = 10 mV / change of the out current (cancels the junction leakage of out to the n-well)
let R_sw = 0.01 / (abs(iout[1] - iout[0]) + 1e-24)
let I_out = iout[1]
let I_in = iin[1]
let I_dvdd = idd[1]
let I_avdd = iav[1]
let I_en = ien[1]
let Vg = vg[1]
echo $&R_sw $&I_out $&I_in $&I_dvdd $&I_avdd $&I_en $&Vg """ + ECHO + r"""
.endc"""

# ------------------------------------------------------------------ DC: bias-current leg
BIAS_VARS = ["V_in", "V_out", "V_drop", "V_head", "I_in", "I_err", "I_nb", "I_err18", "Vg"]
BIAS_SRC = r"""Vdd dvdd 0 CACE\{dvdd=1.2\}
Vav avdd 0 CACE\{avdd=3.3\}
Ven enable 0 CACE\{dvdd=1.2\}
Ven2 en2 0 0
* ---- harness iDAC stand-in: sourced current from a 1:1 hv PMOS mirror on avdd (the harness iDAC is a cascoded hv PMOS
*      source on vdd3v3); out = the shared iDAC node (idac1_source / idac2_source of chipalooza_frame)
Iref g 0 CACE\{ibias=5e-6\}
XPd g g avdd avdd sg13_hv_pmos w=10u l=2u ng=1 m=4
XPm src g avdd avdd sg13_hv_pmos w=10u l=2u ng=1 m=4
Vmo src out 0
* x1 = the switch under test (on), x2 = one off neighbour on the same node (the harness has 18 per iDAC)
Vm1 out o1 0
Vm2 out o2 0
* load: the NMOS input diode of a bias tree (hv 6u/6u); the neighbour's in sits on an unbiased diode of the same size
Vmi in d 0
XN d d 0 0 sg13_hv_nmos w=6u l=6u ng=1 m=1
Vmn in2 d2 0
XN2 d2 d2 0 0 sg13_hv_nmos w=6u l=6u ng=1 m=1
.nodeset v(x1.x5.net1)=0 v(x1.x5.s1_n)=CACE\{avdd=3.3\} v(x2.x5.net1)=CACE\{avdd=3.3\} v(x2.x5.s1_n)=0"""
BIAS_NG = INC + r"""
.options gmin=1e-15 abstol=1e-15 reltol=1e-4
.option warn=1
.control
op
let i1 = i(Vm1)
let inb = i(Vm2)
let iin = i(Vmi)
let V_in = v(in)
let V_out = v(out)
let V_drop = v(out) - v(in)
let V_head = CACE\{avdd=3.3\} - v(out)
let I_in = iin
* errors in percent: (delivered - taken) / taken; I_err18 with 18 off neighbours that also draw from the iDAC node
let I_err = 100 * (iin - i1) / i1
let I_nb = inb
let I_err18 = 100 * (iin - i1 - 18 * inb) / (i1 + 18 * inb)
let Vg = v(x1.net3)
echo $&V_in $&V_out $&V_drop $&V_head $&I_in $&I_err $&I_nb $&I_err18 $&Vg """ + ECHO + r"""
.endc"""

# ------------------------------------------------------------------ transient: toggling, delays, load, charge injection
TRAN_VARS = ["Verr_on", "Verr_off", "td_on", "td_off", "t_on", "t_off", "V_load", "Q_inj"]
TRAN_SRC = r"""Vdd dvdd 0 CACE\{dvdd=1.2\}
Vav avdd 0 CACE\{avdd=3.3\}
* enable (0.1 ns edges): 0 | on at 0.2 us | off at 0.7 us | on at 1.2 us | end 1.7 us
Ven enable 0 PWL(0 0 0.2u 0 0.2001u CACE\{dvdd=1.2\} 0.7u CACE\{dvdd=1.2\} 0.7001u 0 1.2u 0 1.2001u CACE\{dvdd=1.2\})
Vs out 0 CACE\{vsig=2.5\}
* x1: 10 kOhm || 1 pF load at in.  x2: held node in2 (1 pF only), starts at vsig
Rl in 0 10k
Cl in 0 1p
Ch in2 0 1p
.ic v(in2)=CACE\{vsig=2.5\}"""
TRAN_NG = ANT + "\n" + INC + r"""
.options gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
* max step 0.1 ns: delays within ~3 % of a 0.02 ns run (checked at tt, 125 C)
tran 0.1n 1.7u 0 0.1n
let va = CACE\{avdd=3.3\}
let vs = CACE\{vsig=2.5\}
* gate of the pass PMOS (x1.net3) before each enable edge: off, on, off, on
meas tran g0 find v(x1.net3) at=0.19u
meas tran g1 find v(x1.net3) at=0.69u
meas tran g2 find v(x1.net3) at=1.19u
meas tran g3 find v(x1.net3) at=1.69u
let Verr_on = 0.5 * (g1 + g3 + abs(g1 - g3))
let Verr_off = va - 0.5 * (g0 + g2 - abs(g0 - g2))
* defaults (1 s) stay when a measurement finds no crossing
let td_on = 1
let td_off = 1
let t_on = 1
let t_off = 1
meas tran td_on trig v(enable) val=CACE[CACE\{dvdd=1.2\} / 2] td=1.1u rise=1 targ v(x1.net3) val=CACE[CACE\{avdd=3.3\} / 2] td=1.1u fall=1
meas tran td_off trig v(enable) val=CACE[CACE\{dvdd=1.2\} / 2] td=0.6u fall=1 targ v(x1.net3) val=CACE[CACE\{avdd=3.3\} / 2] td=0.6u rise=1
meas tran vl3 find v(in) at=1.69u
meas tran vl1 find v(in) at=0.69u
let V_load = vl3 / vs
let h3 = 0.5 * vl3
let h1 = 0.5 * vl1
meas tran t_on trig v(enable) val=CACE[CACE\{dvdd=1.2\} / 2] td=1.1u rise=1 targ v(in) val=$&h3 td=1.1u rise=1
meas tran t_off trig v(enable) val=CACE[CACE\{dvdd=1.2\} / 2] td=0.6u fall=1 targ v(in) val=$&h1 td=0.6u fall=1
meas tran hb find v(in2) at=0.69u
meas tran ha find v(in2) at=1.15u
let Q_inj = 1e-12 * (ha - hb)
echo $&Verr_on $&Verr_off $&td_on $&td_off $&t_on $&t_off $&V_load $&Q_inj """ + ECHO + r"""
.endc"""

# ------------------------------------------------------------------ transient: dvdd loss / power-up without dvdd
PWR_VARS = ["S_50u", "S_1m", "S_10m", "S_100m", "I_avdd", "Verr_end"]
PWR_SRC = r"""* scen 1: dvdd lost at 10 us (1 us ramp) with the switch on, enable follows dvdd; dvdd and enable back at 100 ms
* scen 2: same with the switch off | scen 3: avdd ramps up 10 .. 20 us with dvdd = 0, enable = 0; dvdd up at 100 ms
.param sc=CACE\{scen=1\} vl=CACE\{dvdd=1.2\} va=CACE\{avdd=3.3\}
.param vd0='(sc == 3) ? 0 : vl'
.param en0='(sc == 1) ? vl : 0'
.param va0='(sc == 3) ? 0 : va'
.param gx='(sc == 1) ? 0 : va'
Vdd dvdd 0 PWL(0 \{vd0\} 10u \{vd0\} 11u 0 100m 0 100.001m \{vl\})
Ven enable 0 PWL(0 \{en0\} 10u \{en0\} 11u 0 100m 0 100.001m \{en0\})
Vav avdd 0 PWL(0 \{va0\} 10u \{va0\} 20u \{va\})
* expected gate voltage after dvdd is back (0 on, avdd off)
Vx gx 0 \{gx\}
Vs out 0 2.0
Rl in 0 10k"""
PWR_NG = ANT + "\n" + INC + r"""
.options gmin=1e-15 abstol=1e-14 reltol=1e-4 method=gear SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
tran 10u 100.05m 0 0.5m
let va = CACE\{avdd=3.3\}
* S = gate / avdd: 1 = off, 0 = on
meas tran g50u find v(x1.net3) at=50u
meas tran g1m find v(x1.net3) at=1m
meas tran g10m find v(x1.net3) at=10m
meas tran g100m find v(x1.net3) at=99.9m
meas tran gend find v(x1.net3) at=100.04m
meas tran gexp find v(gx) at=100.04m
meas tran iav find i(Vav) at=99.9m
let S_50u = g50u / va
let S_1m = g1m / va
let S_10m = g10m / va
let S_100m = g100m / va
let I_avdd = -iav
let Verr_end = abs(gend - gexp)
echo $&S_50u $&S_1m $&S_10m $&S_100m $&I_avdd $&Verr_end """ + ECHO + r"""
.endc"""


def code(name, x, y, value, top=False):
    head = f"C {{devices/code_shown.sym}} {x} {y} 0 0 {{name={name} " + \
           ("only_toplevel=true\nformat=\"tcleval( @value )\"" if top else
            ("simulator=ngspice only_toplevel=false" if name == "NGSPICE" else "only_toplevel=false"))
    return [head, 'value="', value, '"}']


def sym_pins(sym):
    """{pin: (x, y)} from the B 5 pin boxes of an xschem symbol (box centre)."""
    out = {}
    for m in re.finditer(r"^B 5 (\S+) (\S+) (\S+) (\S+) \{[^}]*name=(\S+)", sym.read_text(), re.M):
        x1, y1, x2, y2 = (float(m.group(k)) for k in range(1, 5))
        out[m.group(5)] = ((x1 + x2) / 2, (y1 + y2) / 2)
    return out


SUP = {"dvdd": "dvdd", "dvss": "0", "avdd": "avdd", "avss": "0"}


def template(title, duts, src, ng):
    """duts = [(instance, {pin: net}), ...] placed side by side."""
    o = ["v {xschem version=3.4.8RC file_version=1.3}", "G {}", "K {}", "V {}", "S {}", "F {}", "E {}",
         f"T {{CACE template: {title}}} 0 -600 0 0 0.6 0.6 {{}}",
         f"T {{{TOP}: harness PMOS switch; sources and analysis are in the code blocks (generated by ../gen_cace.py)}}"
         " 0 -560 0 0 0.3 0.3 {}"]
    k = 0
    for j, (inst, nets) in enumerate(duts):
        x0, y0 = 1400 + 500 * j, 0
        o.append(f"C {{{TOP}.sym}} {x0} {y0} 0 0 {{name={inst}}}")
        for p, (x, y) in sym_pins(SYM).items():
            flip = 0 if x < 0 else 1
            o.append(f"C {{devices/lab_pin.sym}} {x0 + x:g} {y0 + y:g} 0 {flip} {{name=lp{k} sig_type=std_logic "
                     f"lab={nets.get(p, SUP.get(p, p))}}}")
            k += 1
    o += code("MODEL", 0, -460, MODEL, top=True) + code("SOURCES", 0, -340, src) + code("NGSPICE", 2600, -460, ng)
    return "\n".join(o) + "\n"


TEMPLATES = {
    f"{TOP}_tb_dc.sch": ("DC, switch between two voltage sources (on-resistance, leakage, supply currents)",
                         [("x1", {})], DC_SRC, DC_NG, DC_VARS),
    f"{TOP}_tb_bias.sch": ("DC, bias-current leg: PMOS-mirror source -> switch -> 6u/6u hv NMOS diode, one off neighbour",
                           [("x1", {"out": "o1"}), ("x2", {"in": "in2", "out": "o2", "enable": "en2"})], BIAS_SRC, BIAS_NG,
                           BIAS_VARS),
    f"{TOP}_tb_tran.sch": ("transient, enable toggling: polarity, delays, 10k||1p load, charge injection on a held 1 pF",
                           [("x1", {}), ("x2", {"in": "in2"})], TRAN_SRC, TRAN_NG, TRAN_VARS),
    f"{TOP}_tb_pwr.sch": ("transient, dvdd lost / avdd up without dvdd: state of the switch over 100 ms",
                          [("x1", {})], PWR_SRC, PWR_NG, PWR_VARS),
}

# ------------------------------------------------------------------ yaml
CORN = ["ss", "sf", "tt", "fs", "ff"]
TEMPS = [-40, 27, 125]
def iters(n):
    return {"description": "Monte-Carlo iteration (seed = 12345 + iteration)", "display": "Iterations", "minimum": 1,
            "maximum": n, "step": "linear", "stepsize": 1}
A = "any"
# spec entries: var -> (display, unit, minimum, maximum).  Limits marked P in the comments of each group are PROPOSALS
# (worst simulated case + margin); "functional" limits follow from the function (gate at the rail it should be at).


def dc_spec(rsw=(A, A), iout=(A, A), iin=(A, A), idd=(A, A), iav=(A, A), ien=(A, A), vg=(A, A), what=""):
    return {"R_sw": (f"Switch resistance 10 mV / dI{what}", "Ω") + rsw,
            "I_out": ("Current into out", "pA") + iout,
            "I_in": ("Current into in", "pA") + iin,
            "I_dvdd": ("Current from dvdd", "nA") + idd,
            "I_avdd": ("Current from avdd", "nA") + iav,
            "I_en": ("Current into enable", "pA") + ien,
            "Vg": ("Gate of the pass PMOS", "V") + vg}


def grp(name, tpl, spec, cond, collate=False, plots=None, comment=""):
    return dict(name=name, tpl=f"{TOP}_tb_{tpl}.sch", vars=TEMPLATES[f"{TOP}_tb_{tpl}.sch"][4], spec=spec, cond=cond,
                collate=collate, plots=plots or {}, comment=comment)


GROUPS = [
    grp("ron_params", "dc",
        dc_spec(vg=(A, 0.1), idd=(A, 120), iav=(A, 2), ien=(A, 2000)),
        dict(case=0, vout=[0.3, 0.6, 0.9, 1.1, 1.2, 1.3, 1.5, 2.0, 2.5, 3.0], vin=-1, avdd=[3.0, 3.3, 3.6],
             corner_mos=CORN, temp=TEMPS),
        plots={"R_sw_vs_vout": dict(type="semilogy", xaxis="vout", yaxis="R_sw")},
        comment="On (enable = dvdd = 1.2 V): R_sw vs the switched node (out = vout, in = vout - 10 mV), 10 x 3 avdd x 5 x 3 "
                "= 450 runs.  Vg functional; I_dvdd / I_avdd / I_en limits P."),
    grp("leak_params", "dc",
        dc_spec(iout=(-5000, 5000), iin=(-5000, 5000), idd=(A, 130), iav=(A, 3), ien=(-800, A), vg=(3.5, A)),
        dict(case=1, vout=[0, 1.7, 3.6], vin=[0, 1.7, 3.6], avdd=3.6, dvdd=1.32, corner_mos=CORN, temp=[27, 125]),
        comment="Off (enable = 0), avdd 3.6 V, dvdd 1.32 V: leakage with in / out at 0, 1.7 (top of the bias-node range) "
                "and 3.6 V, both directions, 9 x 5 x 2 = 90 runs.  Vg functional; current limits P."),
    grp("dvdd_off_params", "dc",
        dc_spec(),
        dict(case=[2, 3], vout=2.0, vin=-1, avdd=[3.0, 3.6], corner_mos=CORN, temp=TEMPS),
        plots={"Vg_vs_temp": dict(type="xyplot", xaxis="temp", yaxis="Vg")},
        comment="dvdd = 0, enable = 0, avdd up: DC state from a latch preset ON (case 2) / OFF (case 3), R_sw at 2.0 V, "
                "2 x 2 x 5 x 3 = 60 runs.  Characterization only (no requirement known): see the README."),
    grp("bias_params", "bias",
        {"V_in": ("Diode (bias-tree input) voltage", "V", A, A),
         "V_out": ("Switch input = iDAC node voltage", "V", A, A),
         "V_drop": ("Drop across the switch", "V", A, 0.8),
         "V_head": ("avdd - iDAC node (headroom left for the iDAC)", "V", 1.0, A),
         "I_in": ("Current delivered into the diode", "uA", A, A),
         "I_err": ("Current error of the switch (in - out) / out, %", "", -0.05, 0.05),
         "I_nb": ("Current drawn from the iDAC node by one off neighbour", "pA", -250, 250),
         "I_err18": ("Current error with 18 off neighbours, %", "", -0.5, 0.5),
         "Vg": ("Gate of the pass PMOS", "V", A, 0.1)},
        dict(ibias=[1e-6, 5e-6, 50e-6], avdd=[3.0, 3.3, 3.6], corner_mos=CORN, temp=TEMPS),
        plots={"V_drop_vs_temp": dict(type="xyplot", xaxis="temp", yaxis="V_drop"),
               "V_out_vs_temp": dict(type="xyplot", xaxis="temp", yaxis="V_out")},
        comment="Bias leg: 1 / 5 / 50 uA, 3 x 3 avdd x 5 x 3 = 135 runs.  Vg functional; V_drop, V_head, I_err, I_nb, "
                "I_err18 limits P."),
    grp("func_params", "tran",
        {"Verr_on": ("Gate in the on state (2 on phases, max)", "V", A, 0.1),
         "Verr_off": ("avdd - gate in the off state (2 off phases, max)", "V", A, 0.1),
         "td_on": ("Enable 50 % rise -> gate 50 % fall", "ns", A, 50),
         "td_off": ("Enable 50 % fall -> gate 50 % rise", "ns", A, 40),
         "t_on": ("Enable 50 % -> load 50 % rise (10k || 1p)", "ns", A, 50),
         "t_off": ("Enable 50 % -> load 50 % fall", "ns", A, 50),
         "V_load": ("Load voltage / vsig in the on state", "", 0.9, A),
         "Q_inj": ("Charge onto a held 1 pF at turn-off", "fC", A, A)},
        dict(dvdd=[1.08, 1.2, 1.32], avdd=[3.0, 3.3, 3.6], vsig=2.5, corner_mos=CORN, temp=TEMPS),
        plots={"td_on_vs_temp": dict(type="xyplot", xaxis="temp", yaxis="td_on"),
               "td_off_vs_temp": dict(type="xyplot", xaxis="temp", yaxis="td_off")},
        comment="Toggling 0 -> 1 -> 0 -> 1 with vsig = 2.5 V, dvdd x avdd crossed (1.08 / 1.2 / 1.32 x 3.0 / 3.3 / 3.6), "
                "x 5 x 3 = 135 runs.  Verr functional; delays, V_load limits P."),
    grp("func1v_params", "tran",
        {"Verr_on": ("Gate in the on state (2 on phases, max)", "V", A, 0.1),
         "Verr_off": ("avdd - gate in the off state (2 off phases, max)", "V", A, 0.1),
         "td_on": ("Enable 50 % rise -> gate 50 % fall", "ns", A, A),
         "td_off": ("Enable 50 % fall -> gate 50 % rise", "ns", A, A),
         "t_on": ("Enable 50 % -> load 50 % rise (meaningless when V_load ~ 0)", "ns", A, A),
         "t_off": ("Enable 50 % -> load 50 % fall (meaningless when V_load ~ 0)", "ns", A, A),
         "V_load": ("Load voltage / vsig in the on state", "", A, A),
         "Q_inj": ("Charge onto a held 1 pF at turn-off", "fC", A, A)},
        dict(vsig=1.0, corner_mos=CORN, temp=TEMPS),
        comment="The same with vsig = 1.0 V into 10k || 1p (the load suggested in the task), nominal supplies, 15 runs: "
                "shows that a PMOS-only switch does not pass 1 V.  Verr functional, the rest characterization."),
    grp("func_mm_params", "tran",
        {"Verr_on": ("Gate in the on state: mismatch", "V", A, 0.1),
         "Verr_off": ("avdd - gate in the off state: mismatch", "V", A, 0.1),
         "td_on": ("Enable 50 % rise -> gate 50 % fall: mismatch", "ns", A, 500),
         "td_off": ("Enable 50 % fall -> gate 50 % rise: mismatch", "ns", A, 500),
         "t_on": ("Enable 50 % -> load 50 % rise: mismatch", "ns", A, 500),
         "t_off": ("Enable 50 % -> load 50 % fall: mismatch", "ns", A, 500),
         "V_load": ("Load voltage / vsig: mismatch", "", 0.9, A),
         "Q_inj": ("Charge onto a held 1 pF: mismatch", "fC", A, A)},
        dict(iterations=iters(200), corner_mos="sf_mismatch", temp=-40, dvdd=1.08, avdd=3.6, vsig=2.5),
        comment="Mismatch MC (200 runs, one run per iteration so that the CSV holds them) at the slowest-toggling PVT point "
                "of func_params (sf, -40 C, dvdd 1.08 V, avdd 3.6 V: the level shifter's 1.2 V-driven NMOS fights the PMOS "
                "latch there).  Verr functional; delays P = flips within the 0.5 us phase."),
    grp("pwr_params", "pwr",
        {"S_50u": ("gate/avdd 50 us (1 off, 0 on)", "", A, A),
         "S_1m": ("gate/avdd 1 ms", "", A, A),
         "S_10m": ("gate/avdd 10 ms", "", A, A),
         "S_100m": ("gate/avdd 100 ms", "", A, A),
         "I_avdd": ("Current from avdd at 100 ms", "uA", A, A),
         "Verr_end": ("Gate error after dvdd is back (enable = prior state)", "V", A, 0.1)},
        dict(scen=[1, 2, 3], avdd=[3.0, 3.6], corner_mos=CORN, temp=TEMPS),
        plots={"S_10m_vs_temp": dict(type="xyplot", xaxis="temp", yaxis="S_10m")},
        comment="dvdd lost while on (1) / off (2), avdd up with dvdd = 0 (3): state over 100 ms, then dvdd back; "
                "3 x 2 x 5 x 3 = 90 runs.  Verr_end functional (recovery); S_* characterization."),
    grp("pwr_mm_params", "pwr",
        {"S_50u": ("gate/avdd 50 us (1 off, 0 on): mismatch", "", A, A),
         "S_1m": ("gate/avdd 1 ms: mismatch", "", A, A),
         "S_10m": ("gate/avdd 10 ms: mismatch", "", A, A),
         "S_100m": ("gate/avdd 100 ms: mismatch", "", A, A),
         "I_avdd": ("Current from avdd at 100 ms: mismatch", "uA", A, A),
         "Verr_end": ("Gate error after dvdd is back: mismatch", "V", A, 0.1)},
        dict(iterations=iters(50), scen=3, corner_mos="tt_mismatch", temp=27, avdd=3.3),
        comment="Mismatch MC (50 runs) of scenario 3 (avdd up with dvdd = 0) at tt, 27 C: is the power-up state of the "
                "latch systematic or set by mismatch?"),
]

HEADER = f"""# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#--------------------------------------------------------------
# CACE circuit characterization file: {TOP} (generated by ../gen_cace.py; edit the generator, not this file)
#--------------------------------------------------------------
# Harness cell of sg13cmos5l_ocd_chipalooza (Tim Edwards, Open Circuit Design; sheets byte-identical, not edited):
# hv PMOS pass switch 5u/0.4u m=4 (bulk avdd), gate from sw_lvl_shift (1.2 -> 3.3 V) behind two sg13cmos5l_inv_4 on dvdd.
# enable is active high on the dvdd domain.  In the harness one of these sits between each slot's ibias pin (in) and the
# shared sourced iDAC node idac1_source / idac2_source (out), 19 per iDAC.
# LIMITS: functional ones (gate at the right rail) are fixed; all others are PROPOSALS = worst simulated case + margin,
# set after the first full run (2026-11-07), not requirements.  "any" = characterized only.
# Sign convention: currents positive when delivered by the source into the DUT terminal.  Testbenches echo SI values,
# except the error ratios (percent) and the unitless ratios.
# Run on the schematic only (-s schematic): no layout key, and mismatch is vacuous on extracted netlists.
"""


def yaml_text():
    y = [HEADER, f"""name:           {TOP}
description:    "Harness PMOS-only analog switch (sg13cmos5l_ocd_ip__analog_switches), 1.2 V enable, 3.3 V switched domain"
PDK:            ihp-sg13cmos5l

cace_format:    5.2

authorship:
  designer:         Tim Edwards (cell); characterization suite for Christoph Maier
  creation_date:    November 7, 2026
  license:          Apache-2.0

paths:
  root:             ..
  schematic:        ../schematic/xschem
  netlist:          cace/netlist
  documentation:    cace/_docs
  runs:             cace/_runs

pins:
  dvdd:
    description: 1.2 V supply of the enable inverters
    type: power
    direction: inout
    Vmin: 1.08
    Vmax: 1.32
  dvss:
    description: 1.2 V ground
    type: ground
    direction: inout
  avdd:
    description: 3.3 V supply of the level shifter, bulk of the pass PMOS
    type: power
    direction: inout
    Vmin: 3.0
    Vmax: 3.6
  avss:
    description: 3.3 V ground
    type: ground
    direction: inout
  enable:
    description: Switch on, active high, 0 .. dvdd
    type: digital
    direction: input
  in:
    description: Switched node (harness - the slot's ibias pin)
    type: signal
    direction: inout
  out:
    description: Switched node (harness - the shared iDAC node)
    type: signal
    direction: inout

default_conditions:
  corner_mos:
    description: Process corner MOSFET
    display: Corner MOSFET
    typical: tt
  temp:
    description: Ambient temperature
    display: Temperature
    unit: °C
    typical: 27
  dvdd:
    description: dvdd
    display: dvdd
    unit: V
    typical: 1.2
  avdd:
    description: avdd
    display: avdd
    unit: V
    typical: 3.3
  case:
    description: 0 on, 1 off, 2 dvdd = 0 preset on, 3 dvdd = 0 preset off (DC template)
    display: Case
    typical: 0
  vout:
    description: Voltage at out (DC template)
    display: Vout
    unit: V
    typical: 1.0
  vin:
    description: Voltage at in, -1 = vout - 10 mV (DC template)
    display: Vin
    unit: V
    typical: -1
  ibias:
    description: Sourced bias current (bias template)
    display: Ibias
    unit: A
    typical: 5e-06
  vsig:
    description: Voltage at out, transient template
    display: Vsig
    unit: V
    typical: 2.5
  scen:
    description: 1 dvdd lost while on, 2 while off, 3 avdd up with dvdd = 0 (power template)
    display: Scenario
    typical: 1

parameters:
"""]
    for g in GROUPS:
        y.append(f"  # {g['comment']}")
        y.append(f"  {g['name']}:\n    spec:")
        for var, (disp, unit, lo, hi) in g["spec"].items():
            y.append(f"      {var}:\n        display: \"{disp}\"")
            if unit:
                y.append(f"        unit: {unit}")
            y.append(f"        minimum:\n          value: {lo}\n        typical:\n          value: any\n"
                     f"        maximum:\n          value: {hi}")
        y.append(f"    tool:\n      ngspice:\n        template: {g['tpl']}")
        if g["collate"]:
            y.append("        collate: iterations")
        y.append("        format: ascii\n        suffix: .data\n        variables: [" + ", ".join(g["vars"]) + "]")
        if g["plots"]:
            y.append("    plot:")
            for pn, pd in g["plots"].items():
                y.append(f"      {pn}:\n" + "\n".join(f"        {a}: {b}" for a, b in pd.items()) + "\n        limits: auto")
        y.append("    conditions:")
        for k, v in g["cond"].items():
            if isinstance(v, list):
                y.append(f"      {k}:\n        enumerate: [{', '.join(str(x) for x in v)}]")
            elif isinstance(v, dict):
                y.append(f"      {k}:\n" + "\n".join(f"        {a}: {b}" for a, b in v.items()))
            else:
                y.append(f"      {k}:\n        typical: {v}")
    return "\n".join(y) + "\n"


if __name__ == "__main__":
    cdir = MAC / "verification" / "cace"
    (cdir / "templates").mkdir(parents=True, exist_ok=True)
    for fn, (title, duts, src, ng, _) in TEMPLATES.items():
        (cdir / "templates" / fn).write_text(template(title, duts, src, ng))
    (cdir / "templates" / "xschemrc").write_text(RC.read_text())
    (cdir / f"{TOP}.yaml").write_text(yaml_text())
    print(TOP, "->", cdir, "pins", sym_pins(SYM))
