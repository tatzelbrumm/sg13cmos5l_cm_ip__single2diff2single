v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tb_pd_leak: d2s_mpdda_pd + bias_in_pd disabled (en_3v3 = 0), supply currents, tt 27 C} 60 -500 0 0 0.5 0.5 {}
T {DUT and bias from the schematics in this directory; code block = the deck's .lib / .temp / .option / .param / .save lines and its .control section} 60 -455 0 0 0.3 0.3 {}
T {Reference (results_power_down.txt), vout held at 1.65 V: tt 27 C: bias 0.030 nA, driver front end} 60 -420 0 0 0.25 0.25 {}
T {0.054 nA, vddo 0.020 nA, total 0.104 nA; ff 125 C: 0.633 / 1.283 / 27.21 nA, total 29.1 nA.} 60 -398 0 0 0.25 0.25 {}
N 200 -300 200 620 {lab=vdd}
N 440 580 440 620 {lab=vss}
N 840 600 840 620 {lab=vsso}
N 900 480 1200 480 {lab=vbn}
N 900 380 1100 380 {lab=vbpc}
N 1180 120 1180 460 {lab=vbnc}
N 900 440 1160 440 {lab=vabn}
N 1240 120 1240 600 {lab=vsso}
N 920 60 960 60 {lab=vref}
N 500 100 500 140 {lab=vref}
N 600 100 600 140 {lab=vref}
N 440 260 440 290 {lab=vext}
N 420 320 440 320 {lab=vext}
N 420 260 420 320 {lab=vext}
N 420 260 440 260 {lab=vext}
N 440 260 580 260 {lab=vext}
N 580 260 580 290 {lab=vext}
N 580 320 600 320 {lab=vext}
N 600 260 600 320 {lab=vext}
N 580 260 600 260 {lab=vext}
N 510 320 540 320 {lab=xg}
N 440 350 440 380 {lab=xg}
N 440 380 510 380 {lab=xg}
N 510 320 510 380 {lab=xg}
N 440 380 440 500 {lab=xg}
N 580 350 580 380 {lab=iref}
N 580 380 700 380 {lab=iref}
N 1320 0 1380 0 {lab=vout}
N 1380 20 1380 60 {lab=vout}
N 1380 0 1480 0 {lab=vout}
N 480 320 510 320 {lab=xg}
N 1100 120 1100 380 {lab=vbpc}
N 1120 120 1120 400 {lab=vabp}
N 900 400 1120 400 {lab=vabp}
N 900 460 1180 460 {lab=vbnc}
N 1080 120 1080 360 {lab=vbp}
N 900 360 1080 360 {lab=vbp}
N 1160 120 1160 440 {lab=vabn}
N 1200 120 1200 480 {lab=vbn}
N 200 680 200 700 {lab=GND}
N 440 680 440 700 {lab=GND}
N 120 680 120 700 {lab=GND}
N 840 680 840 700 {lab=GND}
N 660 680 660 700 {lab=GND}
N 360 680 360 700 {lab=GND}
N 280 680 280 700 {lab=GND}
N 840 600 1240 600 {lab=vsso}
N 120 700 200 700 {lab=GND}
N 740 580 1020 580 {lab=vss}
N 440 580 740 580 {lab=vss}
N 440 560 440 580 {lab=vss}
N 120 -320 120 620 {lab=vddo}
N 860 -320 1260 -320 {lab=vddo}
N 1260 -320 1260 -80 {lab=vddo}
N 1320 20 1380 20 {lab=vout}
N 1380 0 1380 20 {lab=vout}
N 1040 -300 1040 -70 {lab=vdd}
N 120 -320 860 -320 {lab=vddo}
N 360 260 360 620 {lab=vext}
N 360 260 420 260 {lab=vext}
N 660 460 660 620 {lab=en}
N 660 460 710 460 {lab=en}
N 600 20 600 40 {lab=vinn}
N 920 60 920 140 {lab=vref}
N 760 -300 1040 -300 {lab=vdd}
N 500 0 500 40 {lab=vinp}
N 280 140 280 620 {lab=vref}
N 500 140 600 140 {lab=vref}
N 660 700 840 700 {lab=GND}
N 360 700 440 700 {lab=GND}
N 440 700 660 700 {lab=GND}
N 500 0 960 0 {lab=vinp}
N 600 20 960 20 {lab=vinn}
N 600 140 920 140 {lab=vref}
N 280 140 500 140 {lab=vref}
N 280 700 360 700 {lab=GND}
N 200 700 280 700 {lab=GND}
N 660 -40 960 -40 {lab=en}
N 1060 700 1060 720 {lab=GND}
N 840 700 1060 700 {lab=GND}
N 1380 120 1380 700 {lab=GND}
N 1060 700 1380 700 {lab=GND}
N 1020 120 1020 580 {lab=vss}
N 800 -20 960 -20 {lab=en_b}
N 780 80 800 80 {lab=en_b}
N 660 80 700 80 {lab=en}
N 660 80 660 460 {lab=en}
N 740 100 740 580 {lab=vss}
N 800 -20 800 80 {lab=en_b}
N 660 -40 660 80 {lab=en}
N 760 260 760 320 {lab=vddb}
N 760 -300 760 200 {lab=vdd}
N 200 -300 760 -300 {lab=vdd}
C {devices/vsource.sym} 200 650 0 0 {name=Vvdd value=3.3 savecurrent=false}
C {devices/vsource.sym} 440 650 0 0 {name=Vvss value=0 savecurrent=false}
C {devices/lab_pin.sym} 440 580 0 0 {name=l1 sig_type=std_logic lab=vss}
C {devices/vsource.sym} 120 650 0 0 {name=Vvddo value=3.3 savecurrent=false}
C {devices/lab_pin.sym} 120 -320 0 0 {name=l2 sig_type=std_logic lab=vddo}
C {devices/vsource.sym} 840 650 0 0 {name=Vvsso value=0 savecurrent=false}
C {devices/lab_pin.sym} 840 600 0 0 {name=l3 sig_type=std_logic lab=vsso}
C {devices/vsource.sym} 660 650 0 0 {name=Ven value=0 savecurrent=false}
C {devices/lab_pin.sym} 660 460 0 0 {name=l4 sig_type=std_logic lab=en}
C {devices/vsource.sym} 360 650 0 0 {name=Vext value=3.3 savecurrent=false}
C {devices/lab_pin.sym} 360 260 0 0 {name=l5 sig_type=std_logic lab=vext}
C {devices/vsource.sym} 280 650 0 0 {name=Vcm value=1.65 savecurrent=false}
C {devices/lab_pin.sym} 280 140 0 0 {name=l6 sig_type=std_logic lab=vref}
C {bias_in_pd.sym} 800 420 0 0 {name=Xb}
C {d2s_mpdda_pd.sym} 1140 20 0 0 {name=Xd}
C {devices/gnd.sym} 1060 720 0 0 {name=l0 lab=GND}
C {devices/lab_pin.sym} 740 530 0 1 {name=l8 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 860 310 0 1 {name=l9 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 840 530 0 1 {name=l10 sig_type=std_logic lab=vsso}
C {devices/lab_wire.sym} 1080 360 0 1 {name=l12 sig_type=std_logic lab=vbp}
C {devices/lab_wire.sym} 1200 480 0 1 {name=l13 sig_type=std_logic lab=vbn}
C {devices/lab_wire.sym} 1100 380 0 1 {name=l14 sig_type=std_logic lab=vbpc}
C {devices/lab_wire.sym} 1180 460 0 1 {name=l15 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1120 400 0 1 {name=l16 sig_type=std_logic lab=vabp}
C {devices/lab_wire.sym} 1160 440 0 1 {name=l17 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 1020 580 0 1 {name=l18 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1260 -320 0 1 {name=l19 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 1240 600 0 1 {name=l20 sig_type=std_logic lab=vsso}
C {devices/lab_pin.sym} 660 -40 0 0 {name=l21 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 920 60 0 0 {name=l22 sig_type=std_logic lab=vref}
C {devices/vsource.sym} 500 70 0 0 {name=Vp value=0 savecurrent=false}
C {devices/lab_wire.sym} 500 0 0 0 {name=l24 sig_type=std_logic lab=vinp}
C {devices/vsource.sym} 600 70 0 0 {name=Vn value=0 savecurrent=false}
C {devices/lab_wire.sym} 600 20 0 0 {name=l26 sig_type=std_logic lab=vinn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 460 320 0 1 {name=Ed
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 320 0 0 {name=Em
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 510 380 0 1 {name=l29 sig_type=std_logic lab=xg}
C {devices/isource.sym} 440 530 0 0 {name=Iext value=5u}
C {devices/lab_wire.sym} 580 380 0 0 {name=l30 sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 1480 0 0 1 {name=l32 sig_type=std_logic lab=vout}
C {devices/code_shown.sym} 60 820 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.temp 27
.control
op
let ibias = i(vsb)
let idrv = -i(vvdd) - i(vsb)
let iddo = -i(vvddo)
let itot = -i(vvdd) - i(vvddo)
let vsg_op = v(vddo) - v(xd.a)
let vgs_on = v(xd.b) - v(vsso)
print ibias idrv iddo itot vsg_op vgs_on
print v(vbp) v(vbpc) v(vabp) v(vabn) v(vbn) v(vbnc)
.endc"}
C {devices/lab_pin.sym} 200 -300 0 0 {name=l23 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1040 -300 0 1 {name=l7 sig_type=std_logic lab=vdd}
C {devices/vsource.sym} 760 230 0 0 {name=Vsb value=0 savecurrent=false}
C {devices/vsource.sym} 1380 90 0 0 {name=Vo value=1.65 savecurrent=false}
C {devices/lab_wire.sym} 760 290 0 0 {name=l40 sig_type=std_logic lab=vddb}
C {inv_hv.sym} 740 80 0 0 {name=XIB}
C {devices/lab_wire.sym} 800 80 0 1 {name=lxib1 sig_type=std_logic lab=en_b}
C {devices/lab_pin.sym} 800 -20 0 0 {name=l11 sig_type=std_logic lab=en_b}
