v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: step response, u = -vstep/2 -> +vstep/2 at 1 us} 0 -600 0 0 0.6 0.6 {}
T {sg13cmos5l_IOPadSingle2Diff: outp - outn = 2 (pad - vref), CM = vcm.  Sources and analysis are in the code blocks.} 0 -560 0 0 0.3 0.3 {}
T {Through rsrc and the pad cell (primary diodes, clamps, 587 Ohm secondary protection).} 0 -530 0 0 0.3 0.3 {}
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
Vu u 0 pulse(CACE[-CACE\{vstep=0.5\}/2] CACE[CACE\{vstep=0.5\}/2] 1u 1n 1n 4u 10u)
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
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-12 gmin=1e-12 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
save v(outp) v(outn) v(vcm)
tran 1n 5u
let vd = v(outp) - v(outn)
let vc = (v(outp) + v(outn))/2 - v(vcm)
meas tran vlo find vd at=0.99u
meas tran vhi find vd at=4.9u
let v10 = vlo + 0.1*(vhi - vlo)
let v90 = vlo + 0.9*(vhi - vlo)
meas tran t10 when vd=v10 rise=1
meas tran t90 when vd=v90 rise=1
let t_rise = t90 - t10
let band = 0.01*abs(vhi - vlo)
let dev = abs(vd - vhi)
meas tran tlast when dev=band cross=last
let t_settle = tlast - 1.0005u
meas tran vdmax max vd from=1u to=4.9u
let Overshoot = 100*(vdmax - vhi)/(vhi - vlo)
let avc = abs(vc)
meas tran Vcm_dev max avc from=1u to=4.9u
echo $&t_rise $&t_settle $&Overshoot $&Vcm_dev > CACE\{filename\}_CACE\{N\}.data
.endc
"}
