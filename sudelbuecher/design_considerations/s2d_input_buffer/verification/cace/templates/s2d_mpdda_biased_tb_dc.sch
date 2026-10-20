v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template: DC transfer vd(u), u = vin - vref, closed loop (vfbp = voutp, vfbn = voutn)} 60 -760 0 0 0.6 0.6 {}
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
C {devices/vsource.sym} 520 -300 0 0 {name=Vu value="dc 0" savecurrent=false}
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
C {s2d_mpdda_biased.sym} 1200 0 0 0 {name=x1}
N 1020 -80 960 -80 {lab=vin}
C {devices/lab_pin.sym} 960 -80 0 0 {name=l17 sig_type=std_logic lab=vin}
N 1020 -40 960 -40 {lab=vref}
C {devices/lab_pin.sym} 960 -40 0 0 {name=l18 sig_type=std_logic lab=vref}
N 1020 0 960 0 {lab=vcm}
C {devices/lab_pin.sym} 960 0 0 0 {name=l19 sig_type=std_logic lab=vcm}
N 1020 40 960 40 {lab=voutp}
C {devices/lab_pin.sym} 960 40 0 0 {name=l20 sig_type=std_logic lab=voutp}
N 1020 80 960 80 {lab=voutn}
C {devices/lab_pin.sym} 960 80 0 0 {name=l21 sig_type=std_logic lab=voutn}
N 1380 -80 1440 -80 {lab=voutp}
C {devices/lab_pin.sym} 1440 -80 0 1 {name=l22 sig_type=std_logic lab=voutp}
N 1380 -40 1440 -40 {lab=voutn}
C {devices/lab_pin.sym} 1440 -40 0 1 {name=l23 sig_type=std_logic lab=voutn}
N 1080 -140 1080 -180 {lab=vdd}
C {devices/lab_pin.sym} 1080 -180 0 1 {name=l24 sig_type=std_logic lab=vdd}
N 1080 140 1080 200 {lab=0}
C {devices/gnd.sym} 1080 200 0 0 {name=l25 lab=GND}
N 1120 140 1120 200 {lab=vbp}
C {devices/lab_pin.sym} 1120 200 0 1 {name=l26 sig_type=std_logic lab=vbp}
N 1160 140 1160 200 {lab=vbn}
C {devices/lab_pin.sym} 1160 200 0 1 {name=l27 sig_type=std_logic lab=vbn}
N 1200 140 1200 200 {lab=vbpc}
C {devices/lab_pin.sym} 1200 200 0 1 {name=l28 sig_type=std_logic lab=vbpc}
N 1240 140 1240 200 {lab=vbnc}
C {devices/lab_pin.sym} 1240 200 0 1 {name=l29 sig_type=std_logic lab=vbnc}
C {devices/isource.sym} 160 560 0 0 {name=IQvbp value=CACE[CACE\{ibias_err=0\}*5e-06]}
N 160 530 160 500 {lab=vbp}
C {devices/lab_pin.sym} 160 500 0 1 {name=l30 sig_type=std_logic lab=vbp}
N 160 590 160 620 {lab=0}
C {devices/gnd.sym} 160 620 0 0 {name=l31 lab=GND}
C {devices/res.sym} 260 560 0 0 {name=RQvbp value=CACE[CACE\{va_bias=1e12\}/5e-06] m=1}
N 260 530 260 500 {lab=vbp}
C {devices/lab_pin.sym} 260 500 0 1 {name=l32 sig_type=std_logic lab=vbp}
N 260 590 260 620 {lab=0}
C {devices/gnd.sym} 260 620 0 0 {name=l33 lab=GND}
C {devices/isource.sym} 420 560 0 0 {name=IQvbn value=CACE[CACE\{ibias_err=0\}*5e-06]}
N 420 530 420 500 {lab=vdd}
C {devices/lab_pin.sym} 420 500 0 1 {name=l34 sig_type=std_logic lab=vdd}
N 420 590 420 620 {lab=vbn}
C {devices/lab_pin.sym} 420 620 0 1 {name=l35 sig_type=std_logic lab=vbn}
C {devices/res.sym} 520 560 0 0 {name=RQvbn value=CACE[CACE\{va_bias=1e12\}/5e-06] m=1}
N 520 530 520 500 {lab=vdd}
C {devices/lab_pin.sym} 520 500 0 1 {name=l36 sig_type=std_logic lab=vdd}
N 520 590 520 620 {lab=vbn}
C {devices/lab_pin.sym} 520 620 0 1 {name=l37 sig_type=std_logic lab=vbn}
C {devices/isource.sym} 680 560 0 0 {name=IQvbpc value=CACE[CACE\{ibias_err=0\}*2e-06]}
N 680 530 680 500 {lab=vbpc}
C {devices/lab_pin.sym} 680 500 0 1 {name=l38 sig_type=std_logic lab=vbpc}
N 680 590 680 620 {lab=0}
C {devices/gnd.sym} 680 620 0 0 {name=l39 lab=GND}
C {devices/res.sym} 780 560 0 0 {name=RQvbpc value=CACE[CACE\{va_bias=1e12\}/2e-06] m=1}
N 780 530 780 500 {lab=vbpc}
C {devices/lab_pin.sym} 780 500 0 1 {name=l40 sig_type=std_logic lab=vbpc}
N 780 590 780 620 {lab=0}
C {devices/gnd.sym} 780 620 0 0 {name=l41 lab=GND}
C {devices/isource.sym} 940 560 0 0 {name=IQvbnc value=CACE[CACE\{ibias_err=0\}*2e-06]}
N 940 530 940 500 {lab=vdd}
C {devices/lab_pin.sym} 940 500 0 1 {name=l42 sig_type=std_logic lab=vdd}
N 940 590 940 620 {lab=vbnc}
C {devices/lab_pin.sym} 940 620 0 1 {name=l43 sig_type=std_logic lab=vbnc}
C {devices/res.sym} 1040 560 0 0 {name=RQvbnc value=CACE[CACE\{va_bias=1e12\}/2e-06] m=1}
N 1040 530 1040 500 {lab=vdd}
C {devices/lab_pin.sym} 1040 500 0 1 {name=l44 sig_type=std_logic lab=vdd}
N 1040 590 1040 620 {lab=vbnc}
C {devices/lab_pin.sym} 1040 620 0 1 {name=l45 sig_type=std_logic lab=vbnc}
T {bias-source quality: extra ibias_err*I_k and R_k = va_bias/I_k across each of the four s2d_bias_lp references} 160 680 0 0 0.3 0.3 {}
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
save v(voutp) v(voutn) v(vcm) v(u) i(vdd)
dc Vu -CACE\{umax=0.5\} CACE\{umax=0.5\} 0.005
let vd = v(voutp) - v(voutn)
let vc = (v(voutp) + v(voutn))/2 - v(vcm)
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
* vdd current at u = 0, including the fixture's diode currents from vdd (14 uA)
let idd = -i(vdd)
meas dc Idd find idd at=0
echo $&Gain $&Vos_in $&INL $&Vcm_err $&Idd > CACE\{filename\}_CACE\{N\}.data
.endc
"}
