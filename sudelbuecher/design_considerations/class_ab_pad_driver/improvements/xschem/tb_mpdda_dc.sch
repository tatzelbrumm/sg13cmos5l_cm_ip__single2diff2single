v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tb_mpdda_dc: DC transfer of d2s_mpdda, tt 27 C, load 1 kOhm to vref || 100 pF} 60 -440 0 0 0.5 0.5 {}
T {DUT and bias from the schematics in this directory; code block = the deck's .lib/.param/.save lines and its .control section} 60 -395 0 0 0.3 0.3 {}
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
N 300 130 300 170 {lab=dp}
N 300 230 300 700 {lab=GND}
N 480 -140 520 -140 {lab=dp}
N 480 -100 520 -100 {lab=GND}
N 560 -90 560 -60 {lab=vref}
N 480 40 520 40 {lab=dp}
N 480 80 520 80 {lab=GND}
N 560 90 560 120 {lab=vref}
N 560 -150 640 -150 {lab=vinp}
N 640 -150 640 -20 {lab=vinp}
N 640 -20 860 -20 {lab=vinp}
N 560 30 660 30 {lab=vinn}
N 660 20 660 30 {lab=vinn}
N 660 20 860 20 {lab=vinn}
N 820 60 860 60 {lab=vref}
N 820 100 860 100 {lab=vout}
N 1260 -20 1320 -20 {lab=vout}
N 1420 -20 1460 -20 {lab=vout}
N 1320 -20 1320 40 {lab=vout}
N 1320 100 1320 140 {lab=vref}
N 1420 -20 1420 40 {lab=vout}
N 1420 100 1420 700 {lab=GND}
N 60 -300 100 -300 {lab=vdd}
N 100 700 200 700 {lab=GND}
N 1320 -20 1420 -20 {lab=vout}
N 620 -300 920 -300 {lab=vdd}
N 100 -300 620 -300 {lab=vdd}
N 300 700 620 700 {lab=GND}
N 200 700 300 700 {lab=GND}
N 620 700 920 700 {lab=GND}
N 920 700 1420 700 {lab=GND}
N 400 130 400 170 {lab=vddo}
N 400 230 400 700 {lab=GND}
N 500 130 500 170 {lab=vsso}
N 500 230 500 700 {lab=GND}
N 1200 -120 1200 -80 {lab=vddo}
N 1200 160 1200 200 {lab=vsso}
N 660 260 660 300 {lab=vddo}
N 660 620 660 660 {lab=vsso}
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
C {devices/vsource.sym} 300 200 0 0 {name=Vd value=0 savecurrent=false}
C {devices/lab_pin.sym} 300 130 0 1 {name=l8 sig_type=std_logic lab=dp}
C {devices/vcvs.sym} 560 -120 0 0 {name=Ep value=0.5}
C {devices/lab_pin.sym} 480 -140 0 0 {name=l9 sig_type=std_logic lab=dp}
C {devices/lab_pin.sym} 480 -100 0 0 {name=l10 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 560 -60 0 1 {name=l11 sig_type=std_logic lab=vref}
C {devices/vcvs.sym} 560 60 0 0 {name=En value=-0.5}
C {devices/lab_pin.sym} 480 40 0 0 {name=l12 sig_type=std_logic lab=dp}
C {devices/lab_pin.sym} 480 80 0 0 {name=l13 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 560 120 0 1 {name=l14 sig_type=std_logic lab=vref}
C {devices/lab_wire.sym} 640 -150 0 0 {name=l15 sig_type=std_logic lab=vinp}
C {devices/lab_wire.sym} 660 30 0 0 {name=l16 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 820 60 0 0 {name=l17 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 820 100 0 0 {name=l18 sig_type=std_logic lab=vout}
C {devices/lab_pin.sym} 1460 -20 0 1 {name=l19 sig_type=std_logic lab=vout}
C {devices/res.sym} 1320 70 0 0 {name=RL value=1k m=1}
C {devices/lab_pin.sym} 1320 140 0 1 {name=l20 sig_type=std_logic lab=vref}
C {devices/capa.sym} 1420 70 0 0 {name=CL value=100p m=1}
C {devices/code_shown.sym} 60 820 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.param vstep=0.5
.save v(vout) v(dp) vdd#branch vddo#branch @n.xd.xop.nsg13_hv_pmos[ids] @n.xd.xon.nsg13_hv_nmos[ids]
.control
dc Vd -1 1 0.01
let vo = v(vout) - 1.65
let ip = abs(@n.xd.xop.nsg13_hv_pmos[ids])
let in = abs(@n.xd.xon.nsg13_hv_nmos[ids])
let idd = -i(vdd) - i(vddo)
meas dc vop find vo at=0.2
meas dc von find vo at=-0.2
meas dc off find vo at=0
meas dc iqp find ip at=0
meas dc iqn find in at=0
meas dc iddq find idd at=0
let gain = (vop - von)/0.4
let err = vo - gain*v(dp) - off
let nonlin = vecmax(abs(err))
print gain off nonlin iqp iqn iddq
if $?batchmode = 0
  plot vo
  plot err
end
.endc"}
C {devices/lab_wire.sym} 60 -300 0 0 {name=l21 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} 800 700 0 0 {name=l0 lab=GND}
C {devices/vsource.sym} 400 200 0 0 {name=Vddo value=3.3 savecurrent=false}
C {devices/vsource.sym} 500 200 0 0 {name=Vsso value=0 savecurrent=false}
C {devices/lab_pin.sym} 400 130 0 1 {name=l31 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 500 130 0 1 {name=l32 sig_type=std_logic lab=vsso}
C {devices/lab_pin.sym} 1200 -120 0 1 {name=l33 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 1200 200 0 1 {name=l34 sig_type=std_logic lab=vsso}
C {devices/lab_pin.sym} 660 260 0 1 {name=l35 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 660 660 0 1 {name=l36 sig_type=std_logic lab=vsso}
