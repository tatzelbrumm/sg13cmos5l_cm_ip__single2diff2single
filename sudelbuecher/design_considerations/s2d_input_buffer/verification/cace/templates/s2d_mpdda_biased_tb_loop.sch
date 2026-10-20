v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: loop gain, differential (Tdm) and common mode (Tcm), broken at vfbp / vfbn} 60 -760 0 0 0.6 0.6 {}
T {run directory: CACE\{simpath\}} 60 -690 0 0 0.3 0.3 {}
T {DUT: s2d_mpdda_biased (s2d_mpdda + s2d_bias_lp), voutp - voutn = 2 (vin - vref), CM = vcm} 60 -650 0 0 0.3 0.3 {}
C {devices/vsource.sym} 100 -300 0 0 {name=Vdd value="dc CACE\{vdd\}" savecurrent=false}
N 100 -330 100 -360 {lab=vdd}
C {devices/lab_pin.sym} 100 -360 0 1 {name=l1 sig_type=std_logic lab=vdd}
N 100 -270 100 -240 {lab=0}
C {devices/gnd.sym} 100 -240 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 240 -300 0 0 {name=Vref value="dc CACE\{vref=1.2\}" savecurrent=false}
N 240 -330 240 -360 {lab=vref}
C {devices/lab_pin.sym} 240 -360 0 1 {name=l3 sig_type=std_logic lab=vref}
N 240 -270 240 -240 {lab=0}
C {devices/gnd.sym} 240 -240 0 0 {name=l4 lab=GND}
C {devices/vsource.sym} 380 -300 0 0 {name=Vcm value="dc CACE\{vcm=1.2\}" savecurrent=false}
N 380 -330 380 -360 {lab=vcm}
C {devices/lab_pin.sym} 380 -360 0 1 {name=l5 sig_type=std_logic lab=vcm}
N 380 -270 380 -240 {lab=0}
C {devices/gnd.sym} 380 -240 0 0 {name=l6 lab=GND}
C {devices/capa.sym} 1560 160 0 0 {name=CLp m=1 value=CACE\{cload=0.5p\}}
N 1560 130 1560 100 {lab=voutp}
C {devices/lab_pin.sym} 1560 100 0 1 {name=l7 sig_type=std_logic lab=voutp}
N 1560 190 1560 220 {lab=0}
C {devices/gnd.sym} 1560 220 0 0 {name=l8 lab=GND}
C {devices/capa.sym} 1680 160 0 0 {name=CLn m=1 value=CACE\{cload=0.5p\}}
N 1680 130 1680 100 {lab=voutn}
C {devices/lab_pin.sym} 1680 100 0 1 {name=l9 sig_type=std_logic lab=voutn}
N 1680 190 1680 220 {lab=0}
C {devices/gnd.sym} 1680 220 0 0 {name=l10 lab=GND}
C {s2d_mpdda_biased.sym} 1200 0 0 0 {name=x1}
N 1020 -80 960 -80 {lab=vref}
C {devices/lab_pin.sym} 960 -80 0 0 {name=l11 sig_type=std_logic lab=vref}
N 1020 -40 960 -40 {lab=vref}
C {devices/lab_pin.sym} 960 -40 0 0 {name=l12 sig_type=std_logic lab=vref}
N 1020 0 960 0 {lab=vcm}
C {devices/lab_pin.sym} 960 0 0 0 {name=l13 sig_type=std_logic lab=vcm}
N 1020 40 960 40 {lab=fbp}
C {devices/lab_pin.sym} 960 40 0 0 {name=l14 sig_type=std_logic lab=fbp}
N 1020 80 960 80 {lab=fbn}
C {devices/lab_pin.sym} 960 80 0 0 {name=l15 sig_type=std_logic lab=fbn}
N 1380 -80 1440 -80 {lab=voutp}
C {devices/lab_pin.sym} 1440 -80 0 1 {name=l16 sig_type=std_logic lab=voutp}
N 1380 -40 1440 -40 {lab=voutn}
C {devices/lab_pin.sym} 1440 -40 0 1 {name=l17 sig_type=std_logic lab=voutn}
N 1080 -140 1080 -180 {lab=vdd}
C {devices/lab_pin.sym} 1080 -180 0 1 {name=l18 sig_type=std_logic lab=vdd}
N 1080 140 1080 200 {lab=0}
C {devices/gnd.sym} 1080 200 0 0 {name=l19 lab=GND}
N 1120 140 1120 200 {lab=vbp}
C {devices/lab_pin.sym} 1120 200 0 1 {name=l20 sig_type=std_logic lab=vbp}
N 1160 140 1160 200 {lab=vbn}
C {devices/lab_pin.sym} 1160 200 0 1 {name=l21 sig_type=std_logic lab=vbn}
N 1200 140 1200 200 {lab=vbpc}
C {devices/lab_pin.sym} 1200 200 0 1 {name=l22 sig_type=std_logic lab=vbpc}
N 1240 140 1240 200 {lab=vbnc}
C {devices/lab_pin.sym} 1240 200 0 1 {name=l23 sig_type=std_logic lab=vbnc}
C {devices/ind.sym} 1900 -300 0 0 {name=Lbp value=1G m=1}
N 1900 -330 1900 -360 {lab=voutp}
C {devices/lab_pin.sym} 1900 -360 0 1 {name=l24 sig_type=std_logic lab=voutp}
N 1900 -270 1900 -240 {lab=fbp}
C {devices/lab_pin.sym} 1900 -240 0 1 {name=l25 sig_type=std_logic lab=fbp}
C {devices/ind.sym} 2040 -300 0 0 {name=Lbn value=1G m=1}
N 2040 -330 2040 -360 {lab=voutn}
C {devices/lab_pin.sym} 2040 -360 0 1 {name=l26 sig_type=std_logic lab=voutn}
N 2040 -270 2040 -240 {lab=fbn}
C {devices/lab_pin.sym} 2040 -240 0 1 {name=l27 sig_type=std_logic lab=fbn}
C {devices/capa.sym} 1900 -60 0 0 {name=Cbp value=1 m=1}
N 1900 -90 1900 -120 {lab=fbp}
C {devices/lab_pin.sym} 1900 -120 0 1 {name=l28 sig_type=std_logic lab=fbp}
N 1900 -30 1900 0 {lab=injp}
C {devices/lab_pin.sym} 1900 0 0 1 {name=l29 sig_type=std_logic lab=injp}
C {devices/capa.sym} 2040 -60 0 0 {name=Cbn value=1 m=1}
N 2040 -90 2040 -120 {lab=fbn}
C {devices/lab_pin.sym} 2040 -120 0 1 {name=l30 sig_type=std_logic lab=fbn}
N 2040 -30 2040 0 {lab=injn}
C {devices/lab_pin.sym} 2040 0 0 1 {name=l31 sig_type=std_logic lab=injn}
C {devices/vsource.sym} 1900 180 0 0 {name=Vinjp value="dc 0 ac 1" savecurrent=false}
N 1900 150 1900 120 {lab=injp}
C {devices/lab_pin.sym} 1900 120 0 1 {name=l32 sig_type=std_logic lab=injp}
N 1900 210 1900 240 {lab=0}
C {devices/gnd.sym} 1900 240 0 0 {name=l33 lab=GND}
C {devices/vsource.sym} 2040 180 0 0 {name=Vinjn value="dc 0 ac 1 180" savecurrent=false}
N 2040 150 2040 120 {lab=injn}
C {devices/lab_pin.sym} 2040 120 0 1 {name=l34 sig_type=std_logic lab=injn}
N 2040 210 2040 240 {lab=0}
C {devices/gnd.sym} 2040 240 0 0 {name=l35 lab=GND}
T {vfbp / vfbn drive only gates: DC closed through 1 GH, AC injected through 1 F.} 1820 300 0 0 0.25 0.25 {}
T {First run: injection +1 / -1 (differential); then Vinjn alters to +1 (common mode).} 1820 330 0 0 0.25 0.25 {}
C {devices/code_shown.sym} -900 -760 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
"}
C {devices/code_shown.sym} -900 -640 0 0 {name=NGSPICE
simulator=ngspice
only_toplevel=false
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
