v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: closed-loop AC: gain, -3 dB bandwidth, PSRR (iovdd, iovss), CMRR, CM response} 0 -600 0 0 0.6 0.6 {}
T {sg13cmos5l_IOPadSingle2Diff: outp - outn = 2 (pad - vref), CM = vcm.  Sources and analysis are in the code blocks.} 0 -560 0 0 0.3 0.3 {}
T {One AC source at a time (alter): Vu (signal), Vio (iovdd), Vgio (iovss; references and sources stay on 0), Vref (pad and vref together).} 0 -530 0 0 0.3 0.3 {}
T {Rejections are input-referred, 20 log(|vd / u| / |vd / v_source|); without mismatch they are numerically infinite (ac_mm_params).} 0 -500 0 0 0.3 0.3 {}
T {run directory: CACE\{simpath\}} 0 -480 0 0 0.25 0.25 {}
C {sg13cmos5l_IOPadSingle2Diff.sym} 1200 0 0 0 {name=x1}
C {devices/lab_pin.sym} 1160 -180 0 1 {name=lp0 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1160 180 0 1 {name=lp1 sig_type=std_logic lab=gio}
C {devices/lab_pin.sym} 1240 -180 0 1 {name=lp2 sig_type=std_logic lab=vcore}
C {devices/lab_pin.sym} 1240 180 0 1 {name=lp3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 980 -120 0 0 {name=lp4 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1420 -40 0 1 {name=lp5 sig_type=std_logic lab=outp}
C {devices/lab_pin.sym} 1420 0 0 1 {name=lp6 sig_type=std_logic lab=outn}
C {devices/lab_pin.sym} 1420 40 0 1 {name=lp7 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 980 -80 0 0 {name=lp8 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 980 -40 0 0 {name=lp9 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 980 0 0 0 {name=lp10 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 980 20 0 0 {name=lp11 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 980 40 0 0 {name=lp12 sig_type=std_logic lab=s1}
C {devices/lab_pin.sym} 980 80 0 0 {name=lp13 sig_type=std_logic lab=s12}
C {devices/lab_pin.sym} 980 100 0 0 {name=lp14 sig_type=std_logic lab=s33}
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
Vu u 0 dc 0 ac 1
Ein vsrc vref u 0 1
Rsrc vsrc pad CACE\{rsrc=50\}
* ---- load per output (gates of the next stage, routing), on top of the buffer's built-in CLP / CLN
Cp outp 0 CACE\{cload=0.5e-12\}
Cn outn 0 CACE\{cload=0.5e-12\}
* ---- the IO ring ground, for the iovss rejection
Vgio gio 0 dc 0 ac 0
"}
C {devices/code_shown.sym} 1700 -460 0 0 {name=NGSPICE simulator=ngspice only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
save v(outp) v(outn)
ac dec 20 10 100meg
let vd = v(outp) - v(outn)
let A = mag(vd)
meas ac a1k find A at=1k
meas ac a100k find A at=100k
let a3 = a1k/sqrt(2)
let f3dB = 1e12
meas ac f3dB when A=a3 fall=1
let Acl_dB = 20*log10(a1k)
set s_a1k = $&a1k
set s_a100k = $&a100k
set s_f3 = $&f3dB
set s_acl = $&Acl_dB
alter @Vu[acmag] = 0
alter @Vio[acmag] = 1
ac dec 20 10 100meg
let vd = v(outp) - v(outn)
let vc = (v(outp) + v(outn))/2
let A = mag(vd)
let C = mag(vc)
meas ac p1k find A at=1k
meas ac p100k find A at=100k
meas ac c1k find C at=1k
set s_pp1k = $&p1k
set s_pp100k = $&p100k
set s_cvdd = $&c1k
alter @Vio[acmag] = 0
alter @Vgio[acmag] = 1
ac dec 20 10 100meg
let vd = v(outp) - v(outn)
let A = mag(vd)
meas ac n1k find A at=1k
meas ac n100k find A at=100k
set s_pn1k = $&n1k
set s_pn100k = $&n100k
alter @Vgio[acmag] = 0
alter @Vref[acmag] = 1
ac dec 20 10 100meg
let vd = v(outp) - v(outn)
let A = mag(vd)
meas ac m1k find A at=1k
let Acl_dB = $s_acl
let f3dB = $s_f3
let PSRRp_1k = 20*log10($s_a1k/$s_pp1k)
let PSRRp_100k = 20*log10($s_a100k/$s_pp100k)
let PSRRn_1k = 20*log10($s_a1k/$s_pn1k)
let PSRRn_100k = 20*log10($s_a100k/$s_pn100k)
let CMRR_1k = 20*log10($s_a1k/m1k)
let CMvdd_1k = 20*log10($s_cvdd)
echo $&Acl_dB $&f3dB $&PSRRp_1k $&PSRRp_100k $&PSRRn_1k $&PSRRn_100k $&CMRR_1k $&CMvdd_1k > CACE\{filename\}_CACE\{N\}.data
.endc
"}
