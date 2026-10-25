v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: loop gain of the input buffer (fixture s2d_mpdda_pd_sel), differential (Tdm) and common mode (Tcm), broken at vfbp / vfbn} 0 -600 0 0 0.5 0.5 {}
T {en_3v3 tied to vdd, en_3v3_b to 0; vin = vref (u = 0). vfbp / vfbn drive only gates: DC closed through 1 GH, AC injected through 1 F; first +1 / -1, then +1 / +1.} 0 -550 0 0 0.25 0.25 {}
T {run directory: CACE\{simpath\}} 0 -510 0 0 0.25 0.25 {}
C {s2d_mpdda_pd_sel.sym} 960 0 0 0 {name=x1}
C {devices/lab_pin.sym} 860 -160 0 1 {name=lp0 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 840 160 0 1 {name=lp1 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 780 -60 0 0 {name=lp2 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 780 -20 0 0 {name=lp3 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 780 20 0 0 {name=lp4 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 1140 -40 0 1 {name=lp5 sig_type=std_logic lab=voutp}
C {devices/lab_pin.sym} 1140 0 0 1 {name=lp6 sig_type=std_logic lab=voutn}
C {devices/lab_pin.sym} 1140 -80 0 1 {name=lp7 sig_type=std_logic lab=fbp}
C {devices/lab_pin.sym} 1140 40 0 1 {name=lp8 sig_type=std_logic lab=fbn}
C {devices/lab_pin.sym} 780 -100 0 0 {name=lp9 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 780 60 0 0 {name=lp10 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 780 80 0 0 {name=lp11 sig_type=std_logic lab=0}
C {devices/lab_pin.sym} 780 100 0 0 {name=lp12 sig_type=std_logic lab=s0}
C {devices/lab_pin.sym} 780 120 0 0 {name=lp13 sig_type=std_logic lab=s1}
C {devices/code_shown.sym} 0 -460 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r=typ\}
.lib cornerCAP.lib cap_CACE\{corner_c=typ\}
.lib cornerPNP.lib CACE\{corner_pnp=typ\}
"}
C {devices/code_shown.sym} 0 -260 0 0 {name=SOURCES only_toplevel=false
value="
* all rails on one supply (the pad's iovdd / iovss)
Vdd vdd 0 CACE\{vdd\}
Vs0 s0 0 CACE[(CACE\{sel=0\} % 2)*CACE\{vdd\}]
Vs1 s1 0 CACE[floor(CACE\{sel=0\} / 2)*CACE\{vdd\}]
Vext vext 0 3.3
Iext xg 0 CACE\{ibias=5e-6\}
XEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
Vref vref 0 CACE\{vref=1.2\}
Vcm vcm 0 CACE\{vcm=1.2\}
* load per output
CLp voutp 0 CACE\{cload=0.5e-12\}
CLn voutn 0 CACE\{cload=0.5e-12\}
* loop broken at vfbp / vfbn
Lbp voutp fbp 1G
Lbn voutn fbn 1G
Cbp fbp injp 1
Cbn fbn injn 1
Vinjp injp 0 dc 0 ac 1
Vinjn injn 0 dc 0 ac 1 180
"}
C {devices/code_shown.sym} 1700 -460 0 0 {name=NGSPICE simulator=ngspice only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
save v(voutp) v(voutn) v(fbp) v(fbn)
ac dec 50 10 1G
let T = -(v(voutp) - v(voutn))/(v(fbp) - v(fbn))
let Tdb = vdb(T)
let Tph = cph(T)*180/pi
meas ac t0 find Tdb at=10
let fc = 0
meas ac fc when Tdb=0 fall=1
let phc = -180
meas ac phc find Tph when Tdb=0 fall=1
let gmdb = -1000
meas ac gmdb find Tdb when Tph=-180 cross=1
set s_T0dm = $&t0
set s_fcdm = $&fc
set s_PMdm = $&phc
set s_GMdm = $&gmdb
alter @Vinjn[acphase] = 0
ac dec 50 10 1G
let T = -(v(voutp) + v(voutn))/(v(fbp) + v(fbn))
let Tdb = vdb(T)
let Tph = cph(T)*180/pi
meas ac t0 find Tdb at=10
let fc = 0
meas ac fc when Tdb=0 fall=1
let phc = -180
meas ac phc find Tph when Tdb=0 fall=1
let gmdb = -1000
meas ac gmdb find Tdb when Tph=-180 cross=1
let T0dm = $s_T0dm
let fcdm = $s_fcdm
let PMdm = 180 + $s_PMdm
let GMdm = 0 - $s_GMdm
let T0cm = t0
let fccm = fc
let PMcm = 180 + phc
let GMcm = 0 - gmdb
echo $&T0dm $&fcdm $&PMdm $&GMdm $&T0cm $&fccm $&PMcm $&GMcm > CACE\{filename\}_CACE\{N\}.data
.endc
"}
