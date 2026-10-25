v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: loop gain of the pad driver (fixture d2s_mpdda_pd_sel, loop opened at vfb)} 0 -600 0 0 0.6 0.6 {}
T {run directory: CACE\{simpath\}} 0 -510 0 0 0.25 0.25 {}
C {d2s_mpdda_pd_sel.sym} 1200 0 0 0 {name=x1}
C {devices/lab_pin.sym} 1140 -140 0 1 {name=lp0 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1140 140 0 1 {name=lp1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1260 -140 0 1 {name=lp2 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1260 140 0 1 {name=lp3 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1020 -80 0 0 {name=lp4 sig_type=std_logic lab=vinp}
C {devices/lab_pin.sym} 1020 -60 0 0 {name=lp5 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 1020 -40 0 0 {name=lp6 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 1020 -20 0 0 {name=lp7 sig_type=std_logic lab=fb}
C {devices/lab_pin.sym} 1020 0 0 0 {name=lp8 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 1020 20 0 0 {name=lp9 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1020 60 0 0 {name=lp10 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 1020 80 0 0 {name=lp11 sig_type=std_logic lab=s1}
C {devices/lab_pin.sym} 1020 40 0 0 {name=lp13 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 1380 0 0 1 {name=lp12 sig_type=std_logic lab=vout}
C {devices/code_shown.sym} 0 -460 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r=typ\}
.lib cornerCAP.lib cap_CACE\{corner_c=typ\}
.lib cornerPNP.lib CACE\{corner_pnp=typ\}
"}
C {devices/code_shown.sym} 0 -300 0 0 {name=SOURCES only_toplevel=false
value="
* all rails on one supply (the pad's iovdd / iovss); en_3v3 tied to vdd, en_3v3_b to 0
Vdd vdd 0 CACE\{vdd\}
Vs0 s0 0 CACE[(CACE\{sel=0\} % 2)*CACE\{vdd\}]
Vs1 s1 0 CACE[floor(CACE\{sel=0\} / 2)*CACE\{vdd\}]
Vext vext 0 3.3
Iext xg 0 CACE\{ibias=5e-6\}
XEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
Vref vref 0 CACE\{vref=1.65\}
Vic vic 0 CACE\{vicm=1.65\}
Ep vinp vic 0 0 0.5
En vinn vic 0 0 -0.5
* loop broken at vfb: DC through Lb, AC injected through Cb
Lb vout fb 1G
Cb fb inj 1
Vinj inj 0 dc 0 ac 1
RL vout vterm CACE\{rload=1000\}
Vterm vterm 0 CACE\{vterm=1.65\}
CL vout 0 CACE\{cload=1e-10\}
"}
C {devices/code_shown.sym} 1700 -460 0 0 {name=NGSPICE simulator=ngspice only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15
.option warn=1
.control
save v(vout) v(fb)
ac dec 50 1 1G
let T = -v(vout)/v(fb)
let Tdb = vdb(T)
let Tph = cph(T)*180/pi
meas ac T0 find Tdb at=10
let fc = 0
meas ac fc when Tdb=0 fall=1
let phc = -180
meas ac phc find Tph when Tdb=0 fall=1
let PM = 180 + phc
let gmdb = -1000
meas ac gmdb find Tdb when Tph=-180 cross=1
let GM = -gmdb
echo $&T0 $&fc $&PM $&GM > CACE\{filename\}_CACE\{N\}.data
.endc
"}
