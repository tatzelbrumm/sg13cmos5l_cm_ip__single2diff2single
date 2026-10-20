v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: closed-loop AC: gain, -3 dB bandwidth, PSRR (vdd, vss), CMRR, CM response} 60 -760 0 0 0.6 0.6 {}
T {run directory: CACE\{simpath\}} 60 -690 0 0 0.3 0.3 {}
T {DUT: s2d_mpdda_biased (s2d_mpdda + s2d_bias_lp), voutp - voutn = 2 (vin - vref), CM = vcm} 60 -650 0 0 0.3 0.3 {}
C {devices/vsource.sym} 100 -300 0 0 {name=Vdd value="dc CACE\{vdd\} ac 0" savecurrent=false}
N 100 -330 100 -360 {lab=vdd}
C {devices/lab_pin.sym} 100 -360 0 1 {name=l1 sig_type=std_logic lab=vdd}
N 100 -270 100 -240 {lab=0}
C {devices/gnd.sym} 100 -240 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 240 -300 0 0 {name=Vref value="dc CACE\{vref=1.2\} ac 0" savecurrent=false}
N 240 -330 240 -360 {lab=vref}
C {devices/lab_pin.sym} 240 -360 0 1 {name=l3 sig_type=std_logic lab=vref}
N 240 -270 240 -240 {lab=0}
C {devices/gnd.sym} 240 -240 0 0 {name=l4 lab=GND}
C {devices/vsource.sym} 380 -300 0 0 {name=Vcm value="dc CACE\{vcm=1.2\} ac 0" savecurrent=false}
N 380 -330 380 -360 {lab=vcm}
C {devices/lab_pin.sym} 380 -360 0 1 {name=l5 sig_type=std_logic lab=vcm}
N 380 -270 380 -240 {lab=0}
C {devices/gnd.sym} 380 -240 0 0 {name=l6 lab=GND}
C {devices/capa.sym} 1560 160 0 0 {name=CLp m=1 value=CACE\{cload=0.5p\}}
N 1560 130 1560 100 {lab=voutp}
C {devices/lab_pin.sym} 1560 100 0 1 {name=l7 sig_type=std_logic lab=voutp}
N 1560 190 1560 220 {lab=vsx}
C {devices/lab_pin.sym} 1560 220 0 1 {name=l8 sig_type=std_logic lab=vsx}
C {devices/capa.sym} 1680 160 0 0 {name=CLn m=1 value=CACE\{cload=0.5p\}}
N 1680 130 1680 100 {lab=voutn}
C {devices/lab_pin.sym} 1680 100 0 1 {name=l9 sig_type=std_logic lab=voutn}
N 1680 190 1680 220 {lab=vsx}
C {devices/lab_pin.sym} 1680 220 0 1 {name=l10 sig_type=std_logic lab=vsx}
C {devices/vsource.sym} 520 -300 0 0 {name=Vu value="dc 0 ac 1" savecurrent=false}
N 520 -330 520 -360 {lab=u}
C {devices/lab_pin.sym} 520 -360 0 1 {name=l11 sig_type=std_logic lab=u}
N 520 -270 520 -240 {lab=0}
C {devices/gnd.sym} 520 -240 0 0 {name=l12 lab=GND}
C {devices/vcvs.sym} 760 -300 0 0 {name=Ein value=1}
N 760 -330 760 -360 {lab=vin}
C {devices/lab_pin.sym} 760 -360 0 1 {name=l13 sig_type=std_logic lab=vin}
N 760 -270 760 -240 {lab=vref}
C {devices/lab_pin.sym} 760 -240 0 1 {name=l14 sig_type=std_logic lab=vref}
N 720 -320 680 -320 {lab=u}
C {devices/lab_pin.sym} 680 -320 0 0 {name=l15 sig_type=std_logic lab=u}
N 720 -280 680 -280 {lab=0}
C {devices/gnd.sym} 680 -280 0 0 {name=l16 lab=GND}
C {devices/vsource.sym} 900 300 0 0 {name=Vss value="dc 0 ac 0" savecurrent=false}
N 900 270 900 240 {lab=vsx}
C {devices/lab_pin.sym} 900 240 0 1 {name=l17 sig_type=std_logic lab=vsx}
N 900 330 900 360 {lab=0}
C {devices/gnd.sym} 900 360 0 0 {name=l18 lab=GND}
C {s2d_mpdda_biased.sym} 1200 0 0 0 {name=x1}
N 1020 -80 960 -80 {lab=vin}
C {devices/lab_pin.sym} 960 -80 0 0 {name=l19 sig_type=std_logic lab=vin}
N 1020 -40 960 -40 {lab=vref}
C {devices/lab_pin.sym} 960 -40 0 0 {name=l20 sig_type=std_logic lab=vref}
N 1020 0 960 0 {lab=vcm}
C {devices/lab_pin.sym} 960 0 0 0 {name=l21 sig_type=std_logic lab=vcm}
N 1020 40 960 40 {lab=voutp}
C {devices/lab_pin.sym} 960 40 0 0 {name=l22 sig_type=std_logic lab=voutp}
N 1020 80 960 80 {lab=voutn}
C {devices/lab_pin.sym} 960 80 0 0 {name=l23 sig_type=std_logic lab=voutn}
N 1380 -80 1440 -80 {lab=voutp}
C {devices/lab_pin.sym} 1440 -80 0 1 {name=l24 sig_type=std_logic lab=voutp}
N 1380 -40 1440 -40 {lab=voutn}
C {devices/lab_pin.sym} 1440 -40 0 1 {name=l25 sig_type=std_logic lab=voutn}
N 1080 -140 1080 -180 {lab=vdd}
C {devices/lab_pin.sym} 1080 -180 0 1 {name=l26 sig_type=std_logic lab=vdd}
N 1080 140 1080 200 {lab=vsx}
C {devices/lab_pin.sym} 1080 200 0 1 {name=l27 sig_type=std_logic lab=vsx}
N 1120 140 1120 200 {lab=vbp}
C {devices/lab_pin.sym} 1120 200 0 1 {name=l28 sig_type=std_logic lab=vbp}
N 1160 140 1160 200 {lab=vbn}
C {devices/lab_pin.sym} 1160 200 0 1 {name=l29 sig_type=std_logic lab=vbn}
N 1200 140 1200 200 {lab=vbpc}
C {devices/lab_pin.sym} 1200 200 0 1 {name=l30 sig_type=std_logic lab=vbpc}
N 1240 140 1240 200 {lab=vbnc}
C {devices/lab_pin.sym} 1240 200 0 1 {name=l31 sig_type=std_logic lab=vbnc}
T {One AC source at a time (alter): Vu (signal), Vdd, Vss (the cell ground; references stay on 0), Vref (vin and vref} 160 420 0 0 0.25 0.25 {}
T {together, through Ein). Rejections are input-referred: 20 log(|vd / v_u| / |vd / v_source|). Without mismatch the} 160 450 0 0 0.25 0.25 {}
T {cell is symmetric and the differential rejections are numerically infinite: run these in ac_mm_params.} 160 480 0 0 0.25 0.25 {}
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
save v(voutp) v(voutn)
alter @Vdd[acmag] = 0
alter @Vref[acmag] = 0
ac dec 20 10 100meg
let vd = v(voutp) - v(voutn)
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
alter @Vdd[acmag] = 1
ac dec 20 10 100meg
let vd = v(voutp) - v(voutn)
let vc = (v(voutp) + v(voutn))/2
let A = mag(vd)
let C = mag(vc)
meas ac p1k find A at=1k
meas ac p100k find A at=100k
meas ac c1k find C at=1k
set s_pp1k = $&p1k
set s_pp100k = $&p100k
set s_cvdd = $&c1k
alter @Vdd[acmag] = 0
alter @Vss[acmag] = 1
ac dec 20 10 100meg
let vd = v(voutp) - v(voutn)
let A = mag(vd)
meas ac n1k find A at=1k
meas ac n100k find A at=100k
set s_pn1k = $&n1k
set s_pn100k = $&n100k
alter @Vss[acmag] = 0
alter @Vref[acmag] = 1
ac dec 20 10 100meg
let vd = v(voutp) - v(voutn)
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
