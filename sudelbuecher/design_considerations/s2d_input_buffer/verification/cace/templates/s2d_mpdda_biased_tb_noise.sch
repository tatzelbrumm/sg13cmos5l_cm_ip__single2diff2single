v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: noise referred to u = vin - vref, with the 587 ohm pad resistor} 60 -760 0 0 0.6 0.6 {}
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
C {devices/vsource.sym} 520 -300 0 0 {name=Vu value="dc 0 ac 1" savecurrent=false}
N 520 -330 520 -360 {lab=u}
C {devices/lab_pin.sym} 520 -360 0 1 {name=l11 sig_type=std_logic lab=u}
N 520 -270 520 -240 {lab=0}
C {devices/gnd.sym} 520 -240 0 0 {name=l12 lab=GND}
C {devices/vcvs.sym} 760 -300 0 0 {name=Ein value=1}
N 760 -330 760 -360 {lab=pad}
C {devices/lab_pin.sym} 760 -360 0 1 {name=l13 sig_type=std_logic lab=pad}
N 760 -270 760 -240 {lab=vref}
C {devices/lab_pin.sym} 760 -240 0 1 {name=l14 sig_type=std_logic lab=vref}
N 720 -320 680 -320 {lab=u}
C {devices/lab_pin.sym} 680 -320 0 0 {name=l15 sig_type=std_logic lab=u}
N 720 -280 680 -280 {lab=0}
C {devices/gnd.sym} 680 -280 0 0 {name=l16 lab=GND}
C {devices/res.sym} 900 -300 0 0 {name=Rpad value=586.9 m=1}
N 900 -330 900 -360 {lab=pad}
C {devices/lab_pin.sym} 900 -360 0 1 {name=l17 sig_type=std_logic lab=pad}
N 900 -270 900 -240 {lab=vin}
C {devices/lab_pin.sym} 900 -240 0 1 {name=l18 sig_type=std_logic lab=vin}
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
N 1080 140 1080 200 {lab=0}
C {devices/gnd.sym} 1080 200 0 0 {name=l27 lab=GND}
N 1120 140 1120 200 {lab=vbp}
C {devices/lab_pin.sym} 1120 200 0 1 {name=l28 sig_type=std_logic lab=vbp}
N 1160 140 1160 200 {lab=vbn}
C {devices/lab_pin.sym} 1160 200 0 1 {name=l29 sig_type=std_logic lab=vbn}
N 1200 140 1200 200 {lab=vbpc}
C {devices/lab_pin.sym} 1200 200 0 1 {name=l30 sig_type=std_logic lab=vbpc}
N 1240 140 1240 200 {lab=vbnc}
C {devices/lab_pin.sym} 1240 200 0 1 {name=l31 sig_type=std_logic lab=vbnc}
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
.options savecurrents sparse method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
noise v(voutp,voutn) Vu dec 20 10 10meg
setplot noise2
let Vn_out = onoise_total
set s_vn = $&Vn_out
noise v(voutp,voutn) Vu lin 1 1k 1k
let En_1k = inoise_spectrum[0]
set s_e1 = $&En_1k
noise v(voutp,voutn) Vu lin 1 100k 100k
let En_100k = inoise_spectrum[0]
let En_1k = $s_e1
let Vn_out = $s_vn
echo $&En_1k $&En_100k $&Vn_out > CACE\{filename\}_CACE\{N\}.data
.endc
"}
