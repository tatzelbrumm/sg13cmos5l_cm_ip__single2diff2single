v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_bias_lp: test fixture, ideal reference currents into the four bias diodes (as d2s_bias_lp, no class AB)} 60 -640 0 0 0.35 0.35 {}
T {netlist: ../sim/s2d_bias.spice; real trees there: s2d_bias_in / s2d_bias_out, fed by one 5 uA leg of bias_fanout_*} 60 -590 0 0 0.25 0.25 {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 60 60 0 0 0.2 0.2 {}
N 800 -200 840 -200 {lab=vbnc}
N 140 -500 140 -430 {lab=vdd}
N 120 -400 140 -400 {lab=vdd}
N 120 -500 120 -400 {lab=vdd}
N 140 -340 140 -130 {lab=vbp}
N 140 -340 200 -340 {lab=vbp}
N 180 -400 200 -400 {lab=vbp}
N 340 -500 340 -430 {lab=vdd}
N 320 -400 340 -400 {lab=vdd}
N 320 -500 320 -400 {lab=vdd}
N 340 -370 340 -300 {lab=vbpc}
N 340 -300 400 -300 {lab=vbpc}
N 400 -400 400 -300 {lab=vbpc}
N 380 -400 400 -400 {lab=vbpc}
N 340 -300 340 -130 {lab=vbpc}
N 540 -160 540 -130 {lab=vbn}
N 540 -160 600 -160 {lab=vbn}
N 600 -160 600 -100 {lab=vbn}
N 580 -100 600 -100 {lab=vbn}
N 540 -70 540 0 {lab=vss}
N 520 -100 540 -100 {lab=vss}
N 520 -100 520 0 {lab=vss}
N 740 -200 740 -130 {lab=vbnc}
N 800 -200 800 -100 {lab=vbnc}
N 780 -100 800 -100 {lab=vbnc}
N 740 -70 740 0 {lab=vss}
N 720 -100 740 -100 {lab=vss}
N 720 -100 720 0 {lab=vss}
N 120 -500 140 -500 {lab=vdd}
N 320 -500 340 -500 {lab=vdd}
N 540 -500 740 -500 {lab=vdd}
N 720 0 740 0 {lab=vss}
N 540 -370 540 -160 {lab=vbn}
N 740 -370 740 -200 {lab=vbnc}
N 540 -500 540 -430 {lab=vdd}
N 740 -500 740 -430 {lab=vdd}
N 340 -70 340 0 {lab=vss}
N 140 -70 140 0 {lab=vss}
N 140 0 340 0 {lab=vss}
N 340 0 520 0 {lab=vss}
N 540 0 720 0 {lab=vss}
N 520 0 540 0 {lab=vss}
N 340 -500 540 -500 {lab=vdd}
N 140 -500 320 -500 {lab=vdd}
N 140 -370 140 -340 {lab=vbp}
N 200 -400 200 -340 {lab=vbp}
N 740 -200 800 -200 {lab=vbnc}
N 600 -160 840 -160 {lab=vbn}
N 400 -300 840 -300 {lab=vbpc}
N 200 -340 840 -340 {lab=vbp}
N 60 -500 120 -500 {lab=vdd}
N 60 0 140 0 {lab=vss}
C {devices/iopin.sym} 60 -500 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 60 0 0 1 {name=p2 lab=vss}
C {devices/iopin.sym} 840 -340 0 0 {name=p3 lab=vbp}
C {devices/iopin.sym} 840 -160 0 0 {name=p5 lab=vbn}
C {devices/iopin.sym} 840 -300 0 0 {name=p7 lab=vbpc}
C {devices/iopin.sym} 840 -200 0 0 {name=p9 lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 160 -400 0 1 {name=BP
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/isource.sym} 140 -100 0 0 {name=IBP value=5u}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 360 -400 0 1 {name=BPC
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/isource.sym} 340 -100 0 0 {name=IBPC value=2u}
C {devices/isource.sym} 540 -400 0 0 {name=IBN value=5u}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 560 -100 0 1 {name=BN
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/isource.sym} 740 -400 0 0 {name=IBNC value=2u}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 760 -100 0 1 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
