v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: power-down states: supply and pad leakage} 0 -600 0 0 0.6 0.6 {}
T {sg13cmos5l_IOPadDiff2Single.  Sources, load and analysis are in the code blocks; the DUT pins carry net labels.} 0 -540 0 0 0.3 0.3 {}
T {run directory: CACE\{simpath\}} 0 -510 0 0 0.25 0.25 {}
C {sg13cmos5l_IOPadDiff2Single.sym} 1200 0 0 0 {name=x1}
C {devices/lab_pin.sym} 1160 -180 0 1 {name=lp0 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1160 180 0 1 {name=lp1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1240 -180 0 1 {name=lp2 sig_type=std_logic lab=vcore}
C {devices/lab_pin.sym} 1240 180 0 1 {name=lp3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1420 0 0 1 {name=lp4 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 980 -120 0 0 {name=lp5 sig_type=std_logic lab=vinp}
C {devices/lab_pin.sym} 980 -100 0 0 {name=lp6 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 980 -80 0 0 {name=lp7 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 980 -40 0 0 {name=lp8 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 980 0 0 0 {name=lp9 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 980 20 0 0 {name=lp10 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 980 40 0 0 {name=lp11 sig_type=std_logic lab=s1}
C {devices/lab_pin.sym} 980 80 0 0 {name=lp12 sig_type=std_logic lab=s12}
C {devices/lab_pin.sym} 980 100 0 0 {name=lp13 sig_type=std_logic lab=s33}
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
Vcore vcore 0 CACE[CACE\{vddl=1.2\}*ceil((CACE\{pdstate=0\} - 3)**2/99)]
* ---- slot-side controls (1.2 V logic) and the slot supplies seen by the presence detectors
* pdstate 0: en_1v2 low | 1: slot vdd_1v2 gated off | 2: slot vdd_3v3 gated off | 3: chip core 1.2 V off
* (core ring, slot vdd_1v2 and en_1v2 all 0) | 4: enabled.  ceil((s-k)**2/99) is 0 for s = k, else 1
Ven en 0 CACE[1.2*ceil(CACE\{pdstate=0\}**2/99)*ceil((CACE\{pdstate=0\} - 3)**2/99)]
Vs0 s0 0 CACE[(CACE\{sel=0\} % 2)*CACE\{vddl=1.2\}]
Vs1 s1 0 CACE[floor(CACE\{sel=0\} / 2)*CACE\{vddl=1.2\}]
Vs12 s12 0 CACE[1.2*ceil((CACE\{pdstate=0\} - 1)**2/99)*ceil((CACE\{pdstate=0\} - 3)**2/99)]
Vs33 s33 0 CACE[3.3*ceil((CACE\{pdstate=0\} - 2)**2/99)]
* ---- harness iDAC: a sourced current from a PMOS mirror on its own 3.3 V supply
Vext vext 0 3.3
Iext xg 0 CACE\{ibias=5e-6\}
XEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
* ---- differential input around vicm: vinp - vinn = v(dp)
Vref vref 0 CACE\{vref=1.65\}
Vic vic 0 dc CACE\{vicm=1.65\} ac 0
Vd dp 0 dc 0 ac 0
Ep vinp vic dp 0 0.5
En vinn vic dp 0 -0.5
Vpad pad 0 CACE\{vpad=1.65\}
"}
C {devices/code_shown.sym} 1700 -460 0 0 {name=NGSPICE simulator=ngspice only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}] rshunt=1e14
.option warn=1
.control
save all
op
let Iio_pd = -i(vio)
let Icore_pd = -i(vcore)
let Ipad_pd = -i(vpad)
let Is12_pd = -i(vs12)
let Is33_pd = -i(vs33)
let Ven3 = v(x1.en_3v3)
echo $&Iio_pd $&Icore_pd $&Ipad_pd $&Is12_pd $&Is33_pd $&Ven3 > CACE\{filename\}_CACE\{N\}.data
.endc
"}
