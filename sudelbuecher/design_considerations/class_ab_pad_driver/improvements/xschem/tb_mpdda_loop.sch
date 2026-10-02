v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tb_mpdda_loop: loop gain of d2s_mpdda, tt 27 C} 60 -440 0 0 0.5 0.5 {}
T {loop broken at the vfb gate: Lb closes it at DC, Cb and Vinj inject the AC test signal; T = -v(vout)/v(fb)} 60 -395 0 0 0.3 0.3 {}
N 100 -300 100 170 {lab=vdd}
N 100 230 100 700 {lab=GND}
N 200 130 200 170 {lab=vref}
N 200 230 200 700 {lab=GND}
N 620 -300 620 300 {lab=vdd}
N 620 620 620 700 {lab=GND}
N 920 -300 920 -80 {lab=vdd}
N 920 160 920 700 {lab=GND}
N 840 360 960 360 {lab=vbp}
N 960 160 960 360 {lab=vbp}
N 840 400 1000 400 {lab=vbn}
N 1000 160 1000 400 {lab=vbn}
N 840 440 1040 440 {lab=vbpc}
N 1040 160 1040 440 {lab=vbpc}
N 840 480 1080 480 {lab=vbnc}
N 1080 160 1080 480 {lab=vbnc}
N 840 520 1120 520 {lab=vabp}
N 1120 160 1120 520 {lab=vabp}
N 840 560 1160 560 {lab=vabn}
N 1160 160 1160 560 {lab=vabn}
N 300 230 300 700 {lab=GND}
N 300 -20 300 170 {lab=vinp}
N 300 -20 860 -20 {lab=vinp}
N 400 230 400 700 {lab=GND}
N 400 20 400 170 {lab=vinn}
N 400 20 860 20 {lab=vinn}
N 820 60 860 60 {lab=vref}
N 820 100 860 100 {lab=fb}
N 1220 -20 1320 -20 {lab=vout}
N 1420 -20 1460 -20 {lab=vout}
N 1320 -20 1320 40 {lab=vout}
N 1320 100 1320 140 {lab=vref}
N 1420 -20 1420 40 {lab=vout}
N 1420 100 1420 700 {lab=GND}
N 1320 -50 1320 -20 {lab=vout}
N 1320 -140 1320 -110 {lab=fb}
N 1560 -260 1560 -230 {lab=fb}
N 1560 -170 1560 -110 {lab=inj}
N 1560 -50 1560 700 {lab=GND}
N 60 -300 100 -300 {lab=vdd}
N 100 700 200 700 {lab=GND}
N 1320 -20 1420 -20 {lab=vout}
N 620 -300 920 -300 {lab=vdd}
N 100 -300 620 -300 {lab=vdd}
N 300 700 400 700 {lab=GND}
N 200 700 300 700 {lab=GND}
N 620 700 920 700 {lab=GND}
N 400 700 620 700 {lab=GND}
N 1420 700 1560 700 {lab=GND}
N 920 700 1420 700 {lab=GND}
C {devices/vsource.sym} 100 200 0 0 {name=Vdd value=3.3 savecurrent=false}
C {devices/vsource.sym} 200 200 0 0 {name=Vcm value=1.65 savecurrent=false}
C {devices/lab_pin.sym} 200 130 0 1 {name=l1 sig_type=std_logic lab=vref}
C {d2s_bias_lp.sym} 700 460 0 0 {name=Xb}
C {d2s_mpdda.sym} 1040 40 0 0 {name=Xd}
C {devices/lab_wire.sym} 960 360 0 0 {name=l2 sig_type=std_logic lab=vbp}
C {devices/lab_wire.sym} 1000 400 0 0 {name=l3 sig_type=std_logic lab=vbn}
C {devices/lab_wire.sym} 1040 440 0 0 {name=l4 sig_type=std_logic lab=vbpc}
C {devices/lab_wire.sym} 1080 480 0 0 {name=l5 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1120 520 0 0 {name=l6 sig_type=std_logic lab=vabp}
C {devices/lab_wire.sym} 1160 560 0 0 {name=l7 sig_type=std_logic lab=vabn}
C {devices/vsource.sym} 300 200 0 0 {name=Vp value=1.65 savecurrent=false}
C {devices/lab_wire.sym} 300 -20 0 0 {name=l8 sig_type=std_logic lab=vinp}
C {devices/vsource.sym} 400 200 0 0 {name=Vn value=1.65 savecurrent=false}
C {devices/lab_wire.sym} 400 20 0 0 {name=l9 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 820 60 0 0 {name=l10 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 820 100 0 0 {name=l11 sig_type=std_logic lab=fb}
C {devices/lab_pin.sym} 1460 -20 0 1 {name=l12 sig_type=std_logic lab=vout}
C {devices/res.sym} 1320 70 0 0 {name=RL value=1k m=1}
C {devices/lab_pin.sym} 1320 140 0 1 {name=l13 sig_type=std_logic lab=vref}
C {devices/capa.sym} 1420 70 0 0 {name=CL value=100p m=1}
C {devices/ind.sym} 1320 -80 2 0 {name=Lb value=1G m=1}
C {devices/lab_pin.sym} 1320 -140 0 1 {name=l14 sig_type=std_logic lab=fb}
C {devices/capa.sym} 1560 -200 0 0 {name=Cb value=1 m=1}
C {devices/lab_pin.sym} 1560 -260 0 1 {name=l15 sig_type=std_logic lab=fb}
C {devices/vsource.sym} 1560 -80 0 0 {name=Vinj value="dc 0 ac 1" savecurrent=false}
C {devices/lab_wire.sym} 1560 -140 0 0 {name=l16 sig_type=std_logic lab=inj}
C {devices/code_shown.sym} 60 820 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.control
ac dec 50 10 1G
let T=-v(vout)/v(fb)
meas ac T0 find vdb(T) at=10
meas ac fc when vdb(T)=0
meas ac pT find vp(T) when vdb(T)=0
let pm=180/pi*pT+180
print T0 fc pm
if $?batchmode = 0
  plot vdb(T) 180/pi*vp(T)
end
.endc"}
C {devices/lab_wire.sym} 60 -300 0 0 {name=l17 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} 800 700 0 0 {name=l0 lab=GND}
