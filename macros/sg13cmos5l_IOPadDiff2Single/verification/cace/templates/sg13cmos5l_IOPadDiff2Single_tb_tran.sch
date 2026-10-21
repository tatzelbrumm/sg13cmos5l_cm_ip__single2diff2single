v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: large-signal step response} 0 -600 0 0 0.6 0.6 {}
T {sg13cmos5l_IOPadDiff2Single.  Sources, load and analysis are in the code blocks; the DUT pins carry net labels.} 0 -540 0 0 0.3 0.3 {}
T {run directory: CACE\{simpath\}} 0 -510 0 0 0.25 0.25 {}
C {sg13cmos5l_IOPadDiff2Single.sym} 1200 0 0 0 {name=x1}
C {devices/lab_pin.sym} 1160 -180 0 1 {name=lp0 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1160 180 0 1 {name=lp1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1240 -180 0 1 {name=lp2 sig_type=std_logic lab=vcore}
C {devices/lab_pin.sym} 1240 180 0 1 {name=lp3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1420 0 0 1 {name=lp4 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 980 -120 0 1 {name=lp5 sig_type=std_logic lab=vinp}
C {devices/lab_pin.sym} 980 -100 0 1 {name=lp6 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 980 -80 0 1 {name=lp7 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 980 -40 0 1 {name=lp8 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 980 0 0 0 {name=lp9 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 980 20 0 1 {name=lp10 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 980 40 0 1 {name=lp11 sig_type=std_logic lab=s1}
C {devices/lab_pin.sym} 980 80 0 1 {name=lp12 sig_type=std_logic lab=s12}
C {devices/lab_pin.sym} 980 100 0 1 {name=lp13 sig_type=std_logic lab=s33}
C {devices/code_shown.sym} 0 -460 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerMOSlv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r=typ\}
.lib cornerCAP.lib cap_CACE\{corner_c=typ\}
.lib cornerPNP.lib CACE\{corner_pnp=typ\}
.lib cornerDIO.lib dio_tt
* IHP IO library (DCNDiode, DCPDiode); on the sourcepath of the PDK .spiceinit
.include sg13cmos5l_io.spice
"}
C {devices/code_shown.sym} 0 -260 0 0 {name=SOURCES only_toplevel=false
value="
* ---- supplies: iovdd = ring 3.3 V (front end, bias, output stage), vcore = 1.2 V core ring
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
* ---- differential input around vicm: vinp - vinn = v(dp)
Vref vref 0 CACE\{vref=1.65\}
Vic vic 0 dc CACE\{vicm=1.65\} ac 0
Vd dp 0 pulse(-CACE\{vstep=0.5\} CACE\{vstep=0.5\} 1u 1n 1n 4u 8u)
Ep vinp vic dp 0 0.5
En vinn vic dp 0 -0.5
* ---- load
RL pad vterm CACE\{rload=1000\}
Vterm vterm 0 CACE\{vterm=1.65\}
CL pad 0 CACE\{cload=1e-10\}
"}
C {devices/code_shown.sym} 1700 -460 0 0 {name=NGSPICE simulator=ngspice only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-12 gmin=1e-12 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
save v(pad)
tran 2n 9u
meas tran v0 find v(pad) at=0.99u
meas tran v1 find v(pad) at=4.9u
let dv = v1 - v0
let vn = (v(pad) - v0) / dv
meas tran t10r when vn=0.1 rise=1 from=1u to=5u
meas tran t90r when vn=0.9 rise=1 from=1u to=5u
meas tran t90f when vn=0.9 fall=1 from=5u to=9u
meas tran t10f when vn=0.1 fall=1 from=5u to=9u
let SR_rise = 0.8*dv / (t90r - t10r)
let SR_fall = 0.8*dv / (t10f - t90f)
meas tran vnmax max vn from=1u to=5u
let Overshoot = vnmax - 1
let er = abs(vn - 1)
let ef = abs(vn)
let tsr = 1u
let tsf = 5u
meas tran tsr when er=0.01 cross=last from=1u to=5u
meas tran tsf when ef=0.01 cross=last from=5u to=9u
let ts_rise = tsr - 1u
let ts_fall = tsf - 5.001u
echo $&SR_rise $&SR_fall $&Overshoot $&ts_rise $&ts_fall > CACE\{filename\}_CACE\{N\}.data
.endc
"}
