v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tb_pd_enable: vout of d2s_mpdda_pd + d2s_bias_in_pd while en_3v3 rises at 10 us and falls at 60 us, tt 27 C} 60 -500 0 0 0.5 0.5 {}
T {DUT and bias from the schematics in this directory; code block = the deck's .lib / .temp / .option / .param / .save lines and its .control section} 60 -455 0 0 0.3 0.3 {}
T {vinp = vinn = vref, so vout should sit at vref = 1.65 V when enabled; disabled, RL holds it there.} 60 -420 0 0 0.25 0.25 {}
T {Reference (results_power_down.txt), 1k||100p: after the enable edge vout spans 1.542 ... 1.761 V and is} 60 -398 0 0 0.25 0.25 {}
T {within 1 mV of its final value 0.87 us after the edge; after the disable edge 1.646 ... 1.650 V.} 60 -376 0 0 0.25 0.25 {}
C {devices/vsource.sym} 100 200 0 0 {name=Vvdd value=3.3 savecurrent=false}
N 100 -300 100 170 {lab=vdd}
N 100 230 100 700 {lab=GND}
C {devices/vsource.sym} 200 200 0 0 {name=Vvss value=0 savecurrent=false}
N 200 130 200 170 {lab=vss}
C {devices/lab_pin.sym} 200 130 0 1 {name=l1 sig_type=std_logic lab=vss}
N 200 230 200 700 {lab=GND}
C {devices/vsource.sym} 300 200 0 0 {name=Vvddo value=3.3 savecurrent=false}
N 300 130 300 170 {lab=vddo}
C {devices/lab_pin.sym} 300 130 0 1 {name=l2 sig_type=std_logic lab=vddo}
N 300 230 300 700 {lab=GND}
C {devices/vsource.sym} 400 200 0 0 {name=Vvsso value=0 savecurrent=false}
N 400 130 400 170 {lab=vsso}
C {devices/lab_pin.sym} 400 130 0 1 {name=l3 sig_type=std_logic lab=vsso}
N 400 230 400 700 {lab=GND}
C {devices/vsource.sym} 500 200 0 0 {name=Ven value="pwl(0 0 10u 0 10.01u 3.3 60u 3.3 60.01u 0)" savecurrent=false}
N 500 130 500 170 {lab=en}
C {devices/lab_pin.sym} 500 130 0 1 {name=l4 sig_type=std_logic lab=en}
N 500 230 500 700 {lab=GND}
C {devices/vsource.sym} 600 200 0 0 {name=Vext value=3.3 savecurrent=false}
N 600 130 600 170 {lab=vext}
C {devices/lab_pin.sym} 600 130 0 1 {name=l5 sig_type=std_logic lab=vext}
N 600 230 600 700 {lab=GND}
C {devices/vsource.sym} 700 200 0 0 {name=Vcm value=1.65 savecurrent=false}
N 700 130 700 170 {lab=vref}
C {devices/lab_pin.sym} 700 130 0 1 {name=l6 sig_type=std_logic lab=vref}
N 700 230 700 700 {lab=GND}
N 60 -300 100 -300 {lab=vdd}
C {devices/lab_wire.sym} 60 -300 0 0 {name=l7 sig_type=std_logic lab=vdd}
C {d2s_bias_in_pd.sym} 1300 460 0 0 {name=Xb}
C {d2s_mpdda_pd.sym} 1640 40 0 0 {name=Xd}
N 100 -300 1220 -300 {lab=vdd}
N 1220 -300 1520 -300 {lab=vdd}
N 1220 -300 1220 280 {lab=vdd}
N 1520 -300 1520 -80 {lab=vdd}
N 100 700 2020 700 {lab=GND}
C {devices/gnd.sym} 1500 700 0 0 {name=l0 lab=GND}
N 1220 640 1220 680 {lab=vss}
C {devices/lab_pin.sym} 1220 680 0 1 {name=l8 sig_type=std_logic lab=vss}
N 1380 280 1380 240 {lab=vddo}
C {devices/lab_pin.sym} 1380 240 0 1 {name=l9 sig_type=std_logic lab=vddo}
N 1380 640 1380 680 {lab=vsso}
C {devices/lab_pin.sym} 1380 680 0 1 {name=l10 sig_type=std_logic lab=vsso}
N 1120 560 1160 560 {lab=en}
C {devices/lab_pin.sym} 1120 560 0 0 {name=l11 sig_type=std_logic lab=en}
N 1440 360 1560 360 {lab=vbp}
N 1560 360 1560 160 {lab=vbp}
C {devices/lab_wire.sym} 1560 360 0 0 {name=l12 sig_type=std_logic lab=vbp}
N 1440 400 1600 400 {lab=vbn}
N 1600 400 1600 160 {lab=vbn}
C {devices/lab_wire.sym} 1600 400 0 0 {name=l13 sig_type=std_logic lab=vbn}
N 1440 440 1640 440 {lab=vbpc}
N 1640 440 1640 160 {lab=vbpc}
C {devices/lab_wire.sym} 1640 440 0 0 {name=l14 sig_type=std_logic lab=vbpc}
N 1440 480 1680 480 {lab=vbnc}
N 1680 480 1680 160 {lab=vbnc}
C {devices/lab_wire.sym} 1680 480 0 0 {name=l15 sig_type=std_logic lab=vbnc}
N 1440 520 1720 520 {lab=vabp}
N 1720 520 1720 160 {lab=vabp}
C {devices/lab_wire.sym} 1720 520 0 0 {name=l16 sig_type=std_logic lab=vabp}
N 1440 560 1760 560 {lab=vabn}
N 1760 560 1760 160 {lab=vabn}
C {devices/lab_wire.sym} 1760 560 0 0 {name=l17 sig_type=std_logic lab=vabn}
N 1520 160 1520 200 {lab=vss}
C {devices/lab_pin.sym} 1520 200 0 1 {name=l18 sig_type=std_logic lab=vss}
N 1800 -80 1800 -120 {lab=vddo}
C {devices/lab_pin.sym} 1800 -120 0 1 {name=l19 sig_type=std_logic lab=vddo}
N 1800 160 1800 200 {lab=vsso}
C {devices/lab_pin.sym} 1800 200 0 1 {name=l20 sig_type=std_logic lab=vsso}
N 1420 -40 1460 -40 {lab=en}
C {devices/lab_pin.sym} 1420 -40 0 0 {name=l21 sig_type=std_logic lab=en}
N 1420 60 1460 60 {lab=vref}
C {devices/lab_pin.sym} 1420 60 0 0 {name=l22 sig_type=std_logic lab=vref}
N 1420 100 1460 100 {lab=vout}
C {devices/lab_pin.sym} 1420 100 0 0 {name=l23 sig_type=std_logic lab=vout}
C {devices/vsource.sym} 1160 -120 0 0 {name=Vp value=\{vd/2\} savecurrent=false}
N 1160 -150 1240 -150 {lab=vinp}
N 1240 -150 1240 -20 {lab=vinp}
N 1240 -20 1460 -20 {lab=vinp}
C {devices/lab_wire.sym} 1240 -150 0 0 {name=l24 sig_type=std_logic lab=vinp}
N 1160 -90 1160 -60 {lab=vref}
C {devices/lab_pin.sym} 1160 -60 0 1 {name=l25 sig_type=std_logic lab=vref}
C {devices/vsource.sym} 1160 60 0 0 {name=Vn value=\{-vd/2\} savecurrent=false}
N 1160 30 1260 30 {lab=vinn}
N 1260 30 1260 20 {lab=vinn}
N 1260 20 1460 20 {lab=vinn}
C {devices/lab_wire.sym} 1260 30 0 0 {name=l26 sig_type=std_logic lab=vinn}
N 1160 90 1160 120 {lab=vref}
C {devices/lab_pin.sym} 1160 120 0 1 {name=l27 sig_type=std_logic lab=vref}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 400 0 1 {name=Ed
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1020 400 0 0 {name=Em
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 900 370 900 340 {lab=vext}
N 900 400 880 400 {lab=vext}
N 880 400 880 340 {lab=vext}
N 880 340 900 340 {lab=vext}
N 900 340 970 340 {lab=vext}
N 970 340 1040 340 {lab=vext}
N 1040 370 1040 340 {lab=vext}
N 1040 400 1060 400 {lab=vext}
N 1060 400 1060 340 {lab=vext}
N 1060 340 1040 340 {lab=vext}
N 970 340 970 310 {lab=vext}
C {devices/lab_pin.sym} 970 310 0 1 {name=l28 sig_type=std_logic lab=vext}
N 940 400 1000 400 {lab=xg}
N 900 430 900 460 {lab=xg}
N 900 460 970 460 {lab=xg}
N 970 460 970 400 {lab=xg}
C {devices/lab_wire.sym} 970 460 0 1 {name=l29 sig_type=std_logic lab=xg}
C {devices/isource.sym} 900 520 0 0 {name=Iext value=5u}
N 900 490 900 460 {lab=xg}
N 900 550 900 700 {lab=GND}
N 1040 430 1040 460 {lab=iref}
N 1040 460 1160 460 {lab=iref}
C {devices/lab_wire.sym} 1120 460 0 0 {name=l30 sig_type=std_logic lab=iref}
N 1860 -20 1920 -20 {lab=vout}
N 1920 -20 1920 40 {lab=vout}
C {devices/res.sym} 1920 70 0 0 {name=RL value=1k m=1}
N 1920 100 1920 140 {lab=vref}
C {devices/lab_pin.sym} 1920 140 0 1 {name=l31 sig_type=std_logic lab=vref}
N 1920 -20 2020 -20 {lab=vout}
N 2020 -20 2020 40 {lab=vout}
C {devices/capa.sym} 2020 70 0 0 {name=CL value=100p m=1}
N 2020 100 2020 700 {lab=GND}
N 2020 -20 2060 -20 {lab=vout}
C {devices/lab_pin.sym} 2060 -20 0 1 {name=l32 sig_type=std_logic lab=vout}
C {devices/code_shown.sym} 60 820 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.temp 27
.option method=gear
.param vd=0
.save v(vout) v(en) v(xd.a) v(xd.b) v(vbn) v(vbp)
.control
tran 2n 110u
meas tran vf find v(vout) at=59u
meas tran emin min v(vout) from=10u to=59u
meas tran emax max v(vout) from=10u to=59u
meas tran dmin min v(vout) from=60u to=62u
meas tran dmax max v(vout) from=60u to=62u
let dv = abs(v(vout) - vf)
meas tran tset when dv=1m cross=last from=10u to=59u
let t_1mV = tset - 10u
print vf emin emax t_1mV dmin dmax
if $?batchmode = 0
  plot v(vout) v(xd.a) v(xd.b) v(en)
end
.endc"}
