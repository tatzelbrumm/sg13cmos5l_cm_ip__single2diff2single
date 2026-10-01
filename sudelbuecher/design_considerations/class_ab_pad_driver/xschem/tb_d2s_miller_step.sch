v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 60 -300 1480 -300 {lab=vdd}
C {devices/lab_wire.sym} 60 -300 0 0 {name=l1 sig_type=std_logic lab=vdd}
N 60 700 1480 700 {lab=GND}
C {devices/gnd.sym} 800 700 0 0 {name=l0 lab=GND}
C {devices/vsource.sym} 100 200 0 0 {name=Vdd value=3.3 savecurrent=false}
N 100 170 100 -300 {lab=vdd}
N 100 230 100 700 {lab=GND}
C {devices/vsource.sym} 200 200 0 0 {name=Vcm value=1.65 savecurrent=false}
N 200 170 200 130 {lab=vref}
C {devices/lab_pin.sym} 200 130 0 1 {name=l2 sig_type=std_logic lab=vref}
N 200 230 200 700 {lab=GND}
C {d2s_bias.sym} 700 460 0 0 {name=Xb}
N 620 300 620 -300 {lab=vdd}
N 620 620 620 700 {lab=GND}
C {d2s_miller.sym} 1040 40 0 0 {name=Xd}
N 920 -80 920 -300 {lab=vdd}
N 920 160 920 700 {lab=GND}
N 840 360 960 360 {lab=vbp}
N 960 360 960 160 {lab=vbp}
C {devices/lab_wire.sym} 960 360 0 0 {name=l3 sig_type=std_logic lab=vbp}
N 840 400 1000 400 {lab=vbn}
N 1000 400 1000 160 {lab=vbn}
C {devices/lab_wire.sym} 1000 400 0 0 {name=l4 sig_type=std_logic lab=vbn}
N 840 440 1040 440 {lab=vbpc}
N 1040 440 1040 160 {lab=vbpc}
C {devices/lab_wire.sym} 1040 440 0 0 {name=l5 sig_type=std_logic lab=vbpc}
N 840 480 1080 480 {lab=vbnc}
N 1080 480 1080 160 {lab=vbnc}
C {devices/lab_wire.sym} 1080 480 0 0 {name=l6 sig_type=std_logic lab=vbnc}
N 840 520 1120 520 {lab=vabp}
N 1120 520 1120 160 {lab=vabp}
C {devices/lab_wire.sym} 1120 520 0 0 {name=l7 sig_type=std_logic lab=vabp}
N 840 560 1160 560 {lab=vabn}
N 1160 560 1160 160 {lab=vabn}
C {devices/lab_wire.sym} 1160 560 0 0 {name=l8 sig_type=std_logic lab=vabn}
C {devices/vsource.sym} 300 200 0 0 {name=Vd value="pulse(\{-vstep\} \{vstep\} 1u 1n 1n 4u 8u)" savecurrent=false}
N 300 170 300 130 {lab=dp}
C {devices/lab_pin.sym} 300 130 0 1 {name=l9 sig_type=std_logic lab=dp}
N 300 230 300 700 {lab=GND}
C {devices/vcvs.sym} 560 -120 0 0 {name=Ep value=0.5}
C {devices/vcvs.sym} 560 60 0 0 {name=En value=-0.5}
N 520 -140 480 -140 {lab=dp}
C {devices/lab_pin.sym} 480 -140 0 0 {name=l10 sig_type=std_logic lab=dp}
N 520 -100 480 -100 {lab=GND}
C {devices/lab_pin.sym} 480 -100 0 0 {name=l11 sig_type=std_logic lab=GND}
N 560 -90 560 -60 {lab=vref}
C {devices/lab_pin.sym} 560 -60 0 1 {name=l12 sig_type=std_logic lab=vref}
N 520 40 480 40 {lab=dp}
C {devices/lab_pin.sym} 480 40 0 0 {name=l13 sig_type=std_logic lab=dp}
N 520 80 480 80 {lab=GND}
C {devices/lab_pin.sym} 480 80 0 0 {name=l14 sig_type=std_logic lab=GND}
N 560 90 560 120 {lab=vref}
C {devices/lab_pin.sym} 560 120 0 1 {name=l15 sig_type=std_logic lab=vref}
N 560 -150 640 -150 {lab=vinp}
N 640 -150 640 -20 {lab=vinp}
N 640 -20 860 -20 {lab=vinp}
C {devices/lab_wire.sym} 640 -150 0 0 {name=l16 sig_type=std_logic lab=vinp}
N 560 30 660 30 {lab=vinn}
N 660 30 660 20 {lab=vinn}
N 660 20 860 20 {lab=vinn}
C {devices/lab_wire.sym} 660 30 0 0 {name=l17 sig_type=std_logic lab=vinn}
N 860 60 820 60 {lab=vref}
C {devices/lab_pin.sym} 820 60 0 0 {name=l18 sig_type=std_logic lab=vref}
N 860 100 820 100 {lab=vout}
C {devices/lab_pin.sym} 820 100 0 0 {name=l19 sig_type=std_logic lab=vout}
N 1220 -20 1420 -20 {lab=vout}
N 1420 -20 1460 -20 {lab=vout}
C {devices/lab_pin.sym} 1460 -20 0 1 {name=l20 sig_type=std_logic lab=vout}
C {devices/res.sym} 1320 70 0 0 {name=RL value=1k m=1}
N 1320 40 1320 -20 {lab=vout}
N 1320 100 1320 140 {lab=vref}
C {devices/lab_pin.sym} 1320 140 0 1 {name=l21 sig_type=std_logic lab=vref}
C {devices/capa.sym} 1420 70 0 0 {name=CL m=1 value=100p}
N 1420 40 1420 -20 {lab=vout}
N 1420 100 1420 700 {lab=GND}
C {devices/code_shown.sym} 60 820 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.param vstep=0.5
.control
tran 2n 9u
meas tran vlo find v(vout) at=0.99u
meas tran vhi find v(vout) at=4.9u
if $?batchmode = 0
  plot v(vout) v(vinp) v(vinn)
end
.endc"}
T {tb_d2s_miller_step: step response, vinp - vinn = v(dp), vfb = vout} 60 -420 0 0 0.5 0.5 {}
