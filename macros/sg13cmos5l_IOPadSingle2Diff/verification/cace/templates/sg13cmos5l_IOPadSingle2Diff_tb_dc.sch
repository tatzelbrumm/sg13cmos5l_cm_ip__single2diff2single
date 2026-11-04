v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: DC transfer vd(u), u = pad - vref} 0 -600 0 0 0.6 0.6 {}
T {sg13cmos5l_IOPadSingle2Diff: outp - outn = 2 (pad - vref), CM = vcm.  Sources and analysis are in the code blocks.} 0 -560 0 0 0.3 0.3 {}
T {run directory: CACE\{simpath\}} 0 -480 0 0 0.25 0.25 {}
C {sg13cmos5l_IOPadSingle2Diff.sym} 1200 0 0 0 {name=x1}
C {devices/lab_pin.sym} 1160 -180 0 1 {name=lp0 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1160 180 0 1 {name=lp1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1240 -180 0 1 {name=lp2 sig_type=std_logic lab=vcore}
C {devices/lab_pin.sym} 1240 180 0 1 {name=lp3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 980 -120 0 0 {name=lp4 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1420 -40 0 1 {name=lp5 sig_type=std_logic lab=outp}
C {devices/lab_pin.sym} 1420 0 0 1 {name=lp6 sig_type=std_logic lab=outn}
C {devices/lab_pin.sym} 1420 40 0 1 {name=lp7 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 980 -80 0 0 {name=lp8 sig_type=std_logic lab=vref}
C {devices/code_shown.sym} 0 -460 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerMOSlv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r=typ\}
.lib cornerCAP.lib cap_CACE\{corner_c=typ\}
.lib cornerPNP.lib CACE\{corner_pnp=typ\}
.lib cornerDIO.lib dio_tt
.include sg13cmos5l_io.spice
"}
C {devices/code_shown.sym} 0 -260 0 0 {name=SOURCES only_toplevel=false
value="
* ---- supplies: iovdd = IO ring 3.3 V (buffer, bias, control), vcore = 1.2 V core ring
Vio iovdd 0 dc CACE\{vdd\} ac 0
Vcore vcore 0 CACE\{vddl=1.2\}
* ---- slot-side controls (1.2 V logic) and the slot supplies seen by the presence detectors
Ven en 0 CACE\{en=1.2\}
Vs0 s0 0 CACE[(CACE\{sel=0\} % 2)*CACE\{vddl=1.2\}]
Vs1 s1 0 CACE[floor(CACE\{sel=0\} / 2)*CACE\{vddl=1.2\}]
Vs12 s12 0 CACE\{vs12=1.2\}
Vs33 s33 0 CACE\{vs33=3.3\}
* ---- harness iDAC: a sourced current from a PMOS mirror on its own 3.3 V supply
Vext vext 0 3.3
Iext xg 0 CACE\{ibias=5e-6\}
XEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
* ---- references (gates only) and the input: pad source = vref + u, through rsrc
Vref vref 0 dc CACE\{vref=1.2\} ac 0
Vcm vcm 0 CACE\{vcm=1.2\}
Vu u 0 dc 0
Ein vsrc vref u 0 1
Rsrc vsrc pad CACE\{rsrc=50\}
* ---- load per output (gates of the next stage, routing), on top of the buffer's built-in CLP / CLN
Cp outp 0 CACE\{cload=0.5e-12\}
Cn outn 0 CACE\{cload=0.5e-12\}
"}
C {devices/code_shown.sym} 1700 -460 0 0 {name=NGSPICE simulator=ngspice only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
save v(outp) v(outn) v(vcm) v(u) i(vio) i(vcore)
dc Vu -CACE\{umax=0.5\} CACE\{umax=0.5\} 0.005
let vd = v(outp) - v(outn)
let vc = (v(outp) + v(outn))/2 - v(vcm)
meas dc vdp find vd at=0.1
meas dc vdm find vd at=-0.1
meas dc vd0 find vd at=0
meas dc vc0 find vc at=0
* small-signal gain (ideally 2), offset referred to the input, output common-mode error
let Gain = (vdp - vdm)/0.2
let Vos_in = vd0/Gain
let Vcm_err = vc0
* integral nonlinearity referred to the input: max deviation from the small-signal line over +-umax
let dev = abs(vd - vd0 - Gain*v(u))/Gain
meas dc INL max dev
* IO ring current at u = 0: buffer + bias tree + reference + enable control
let iio = -i(vio)
meas dc Iio find iio at=0
echo $&Gain $&Vos_in $&INL $&Vcm_err $&Iio > CACE\{filename\}_CACE\{N\}.data
.endc
"}
C {devices/lab_pin.sym} 980 -40 0 0 {name=l_iref sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 980 0 0 0 {name=l_en sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 980 20 0 0 {name=l_enb sig_type=std_logic lab=en_3v3_b}
C {en_ctrl_3v3.sym} 900 420 0 0 {name=xc}
C {devices/lab_pin.sym} 840 340 0 0 {name=l_xc_vddh sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 860 340 0 1 {name=l_xc_vddl sig_type=std_logic lab=vcore}
C {devices/lab_pin.sym} 840 500 0 1 {name=l_xc_vss sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 800 380 0 0 {name=l_xc_en_1v2 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 800 400 0 0 {name=l_xc_sel0_1v2 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 800 420 0 0 {name=l_xc_sel1_1v2 sig_type=std_logic lab=s1}
C {devices/lab_pin.sym} 800 440 0 0 {name=l_xc_vdd1v2_sense sig_type=std_logic lab=s12}
C {devices/lab_pin.sym} 800 460 0 0 {name=l_xc_vdd3v3_sense sig_type=std_logic lab=s33}
C {devices/lab_pin.sym} 1000 380 0 1 {name=l_xc_en_3v3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 1000 400 0 1 {name=l_xc_en_3v3_b sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1000 420 0 1 {name=l_xc_sel0_3v3 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_pin.sym} 1000 440 0 1 {name=l_xc_sel1_3v3 sig_type=std_logic lab=sel1_3v3}
C {bias_gen_pd.sym} 1300 420 0 0 {name=xg}
C {devices/lab_pin.sym} 1300 340 0 1 {name=l_xg_vdd sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1300 500 0 1 {name=l_xg_vss sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1210 390 0 0 {name=l_xg_ibias sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 1210 410 0 0 {name=l_xg_en_3v3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 1210 430 0 0 {name=l_xg_sel0_3v3 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_pin.sym} 1210 450 0 0 {name=l_xg_sel1_3v3 sig_type=std_logic lab=sel1_3v3}
C {devices/lab_pin.sym} 1390 420 0 1 {name=l_xg_iref sig_type=std_logic lab=iref}
T {xc (en_ctrl_3v3) and xg (bias_gen_pd): outside the pad cell since 2026-11-04 (backannotation to the drawn cell),} 780 260 0 0 0.25 0.25 {}
T {wired as in the former pad sheet; the sources that drove the old pad pins now drive them.} 780 282 0 0 0.25 0.25 {}
