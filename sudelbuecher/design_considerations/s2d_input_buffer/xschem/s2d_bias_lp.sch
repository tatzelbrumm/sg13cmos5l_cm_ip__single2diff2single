v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 60 -500 1000 -500 {lab=vdd}
N 60 0 1000 0 {lab=vss}
C {devices/iopin.sym} 60 -500 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 60 0 0 1 {name=p2 lab=vss}
C {devices/iopin.sym} 60 -400 0 1 {name=p3 lab=vbp}
N 60 -400 120 -400 {lab=vbp}
C {devices/lab_pin.sym} 120 -400 0 1 {name=l4 sig_type=std_logic lab=vbp}
C {devices/iopin.sym} 60 -360 0 1 {name=p5 lab=vbn}
N 60 -360 120 -360 {lab=vbn}
C {devices/lab_pin.sym} 120 -360 0 1 {name=l6 sig_type=std_logic lab=vbn}
C {devices/iopin.sym} 60 -320 0 1 {name=p7 lab=vbpc}
N 60 -320 120 -320 {lab=vbpc}
C {devices/lab_pin.sym} 120 -320 0 1 {name=l8 sig_type=std_logic lab=vbpc}
C {devices/iopin.sym} 60 -280 0 1 {name=p9 lab=vbnc}
N 60 -280 120 -280 {lab=vbnc}
C {devices/lab_pin.sym} 120 -280 0 1 {name=l10 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 280 -400 0 0 {name=BP
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 300 -430 300 -500 {lab=vdd}
N 300 -400 320 -400 {lab=vdd}
N 320 -400 320 -500 {lab=vdd}
N 300 -370 300 -300 {lab=vbp}
N 300 -300 240 -300 {lab=vbp}
N 240 -300 240 -400 {lab=vbp}
N 240 -400 260 -400 {lab=vbp}
C {devices/isource.sym} 300 -230 0 0 {name=IBP value=5u}
N 300 -300 300 -260 {lab=vbp}
N 300 -200 300 0 {lab=vss}
C {devices/lab_pin.sym} 300 -300 0 1 {name=l11 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 480 -400 0 0 {name=BPC
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 500 -430 500 -500 {lab=vdd}
N 500 -400 520 -400 {lab=vdd}
N 520 -400 520 -500 {lab=vdd}
N 500 -370 500 -300 {lab=vbpc}
N 500 -300 440 -300 {lab=vbpc}
N 440 -300 440 -400 {lab=vbpc}
N 440 -400 460 -400 {lab=vbpc}
C {devices/isource.sym} 500 -230 0 0 {name=IBPC value=2u}
N 500 -300 500 -260 {lab=vbpc}
N 500 -200 500 0 {lab=vss}
C {devices/lab_pin.sym} 500 -300 0 1 {name=l12 sig_type=std_logic lab=vbpc}
C {devices/isource.sym} 700 -330 0 0 {name=IBN value=5u}
N 700 -360 700 -500 {lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 680 -100 0 0 {name=BN
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 700 -300 700 -200 {lab=vbn}
N 700 -200 700 -130 {lab=vbn}
N 700 -200 640 -200 {lab=vbn}
N 640 -200 640 -100 {lab=vbn}
N 640 -100 660 -100 {lab=vbn}
N 700 -70 700 0 {lab=vss}
N 700 -100 720 -100 {lab=vss}
N 720 -100 720 0 {lab=vss}
C {devices/lab_pin.sym} 700 -200 0 1 {name=l13 sig_type=std_logic lab=vbn}
C {devices/isource.sym} 900 -330 0 0 {name=IBNC value=2u}
N 900 -360 900 -500 {lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 880 -100 0 0 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 900 -300 900 -200 {lab=vbnc}
N 900 -200 900 -130 {lab=vbnc}
N 900 -200 840 -200 {lab=vbnc}
N 840 -200 840 -100 {lab=vbnc}
N 840 -100 860 -100 {lab=vbnc}
N 900 -70 900 0 {lab=vss}
N 900 -100 920 -100 {lab=vss}
N 920 -100 920 0 {lab=vss}
C {devices/lab_pin.sym} 900 -200 0 1 {name=l14 sig_type=std_logic lab=vbnc}
T {s2d_bias_lp: test fixture, ideal reference currents into the four bias diodes (as d2s_bias_lp, no class AB)} 60 -640 0 0 0.35 0.35 {}
T {netlist: ../sim/s2d_bias.spice; real trees there: s2d_bias_in / s2d_bias_out, fed by one 5 uA leg of bias_fanout_*} 60 -590 0 0 0.25 0.25 {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 60 60 0 0 0.2 0.2 {}

