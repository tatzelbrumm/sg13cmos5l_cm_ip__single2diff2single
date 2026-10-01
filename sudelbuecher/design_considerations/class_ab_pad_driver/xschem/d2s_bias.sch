v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {d2s_bias: bias voltages from ideal reference currents (iab = 5 uA)} 70 -780 0 0 0.6 0.6 {}
N 1180 -150 1180 -80 {lab=vss}
N 1220 -620 1240 -620 {lab=vbp}
N 1160 -620 1180 -620 {lab=vdd}
N 620 -180 640 -180 {lab=vbn}
N 580 -150 580 -80 {lab=vss}
N 560 -180 580 -180 {lab=vss}
N 380 -280 380 -210 {lab=vbnc}
N 420 -180 440 -180 {lab=vbnc}
N 380 -150 380 -80 {lab=vss}
N 360 -180 380 -180 {lab=vss}
N 1020 -620 1040 -620 {lab=vbpc}
N 960 -620 980 -620 {lab=vdd}
N 760 -150 760 -80 {lab=vss}
N 800 -620 820 -620 {lab=n1}
N 760 -560 760 -510 {lab=n1}
N 740 -620 760 -620 {lab=vdd}
N 800 -480 820 -480 {lab=vabp}
N 740 -480 760 -480 {lab=vdd}
N 220 -180 240 -180 {lab=n2}
N 180 -150 180 -80 {lab=vss}
N 160 -180 180 -180 {lab=vss}
N 220 -320 240 -320 {lab=vabn}
N 180 -240 180 -210 {lab=n2}
N 160 -320 180 -320 {lab=vss}
N 560 -180 560 -80 {lab=vss}
N 180 -80 360 -80 {lab=vss}
N 560 -80 580 -80 {lab=vss}
N 640 -240 640 -180 {lab=vbn}
N 580 -240 640 -240 {lab=vbn}
N 580 -240 580 -210 {lab=vbn}
N 360 -80 380 -80 {lab=vss}
N 360 -180 360 -80 {lab=vss}
N 380 -80 560 -80 {lab=vss}
N 380 -280 440 -280 {lab=vbnc}
N 1160 -740 1180 -740 {lab=vdd}
N 1180 -740 1180 -650 {lab=vdd}
N 1160 -740 1160 -620 {lab=vdd}
N 1180 -560 1240 -560 {lab=vbp}
N 1240 -620 1240 -560 {lab=vbp}
N 1040 -620 1040 -520 {lab=vbpc}
N 980 -520 1040 -520 {lab=vbpc}
N 980 -740 980 -650 {lab=vdd}
N 960 -740 980 -740 {lab=vdd}
N 960 -740 960 -620 {lab=vdd}
N 740 -620 740 -480 {lab=vdd}
N 740 -740 740 -620 {lab=vdd}
N 740 -740 760 -740 {lab=vdd}
N 760 -740 760 -650 {lab=vdd}
N 760 -560 820 -560 {lab=n1}
N 760 -590 760 -560 {lab=n1}
N 820 -620 820 -560 {lab=n1}
N 760 -420 820 -420 {lab=vabp}
N 820 -480 820 -420 {lab=vabp}
N 160 -80 180 -80 {lab=vss}
N 180 -380 180 -350 {lab=vabn}
N 240 -380 240 -320 {lab=vabn}
N 180 -240 240 -240 {lab=n2}
N 180 -290 180 -240 {lab=n2}
N 240 -240 240 -180 {lab=n2}
N 160 -320 160 -180 {lab=vss}
N 160 -180 160 -80 {lab=vss}
N 80 -80 160 -80 {lab=vss}
N 580 -80 760 -80 {lab=vss}
N 760 -420 760 -210 {lab=vabp}
N 980 -740 1160 -740 {lab=vdd}
N 760 -740 960 -740 {lab=vdd}
N 580 -740 740 -740 {lab=vdd}
N 1180 -560 1180 -210 {lab=vbp}
N 980 -80 1180 -80 {lab=vss}
N 760 -80 980 -80 {lab=vss}
N 980 -150 980 -80 {lab=vss}
N 980 -520 980 -210 {lab=vbpc}
N 580 -740 580 -650 {lab=vdd}
N 380 -740 580 -740 {lab=vdd}
N 380 -740 380 -650 {lab=vdd}
N 180 -740 380 -740 {lab=vdd}
N 180 -740 180 -650 {lab=vdd}
N 80 -740 180 -740 {lab=vdd}
N 640 -240 1280 -240 {lab=vbn}
N 440 -280 440 -180 {lab=vbnc}
N 440 -280 1280 -280 {lab=vbnc}
N 240 -380 1280 -380 {lab=vabn}
N 180 -380 240 -380 {lab=vabn}
N 820 -420 1280 -420 {lab=vabp}
N 580 -610 580 -240 {lab=vbn}
N 380 -610 380 -280 {lab=vbnc}
N 180 -610 180 -380 {lab=vabn}
N 1180 -590 1180 -560 {lab=vbp}
N 980 -590 980 -520 {lab=vbpc}
N 760 -450 760 -420 {lab=vabp}
N 1040 -520 1280 -520 {lab=vbpc}
N 1240 -560 1280 -560 {lab=vbp}
C {devices/iopin.sym} 80 -740 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 80 -80 0 1 {name=p2 lab=vss}
C {devices/opin.sym} 1280 -560 0 0 {name=p3 lab=vbp}
C {devices/opin.sym} 1280 -240 0 0 {name=p4 lab=vbn}
C {devices/opin.sym} 1280 -520 0 0 {name=p5 lab=vbpc}
C {devices/opin.sym} 1280 -280 0 0 {name=p6 lab=vbnc}
C {devices/opin.sym} 1280 -420 0 0 {name=p7 lab=vabp}
C {devices/opin.sym} 1280 -380 0 0 {name=p8 lab=vabn}
C {devices/isource.sym} 1180 -180 0 0 {name=IBP value=20u}
C {devices/lab_pin.sym} 1180 -230 0 1 {name=l1 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1180 -130 0 1 {name=l2 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1200 -620 0 1 {name=BP
l=2u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1240 -620 0 1 {name=l3 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1180 -670 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1180 -570 0 0 {name=l5 sig_type=std_logic lab=vbp}
C {devices/isource.sym} 580 -620 0 0 {name=IBN value=50u}
C {devices/lab_pin.sym} 580 -670 0 1 {name=l7 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 580 -570 0 1 {name=l8 sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 -180 0 1 {name=BN
l=2u
w=25u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 640 -180 0 1 {name=l9 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 580 -230 0 0 {name=l10 sig_type=std_logic lab=vbn}
C {devices/isource.sym} 380 -620 0 0 {name=IBNC value=5u}
C {devices/lab_pin.sym} 380 -670 0 1 {name=l13 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 380 -570 0 1 {name=l14 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -180 0 1 {name=BNC
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 440 -180 0 1 {name=l15 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 380 -230 0 0 {name=l16 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 380 -130 0 0 {name=l17 sig_type=std_logic lab=vss}
C {devices/isource.sym} 980 -180 0 0 {name=IBPC value=5u}
C {devices/lab_pin.sym} 980 -230 0 1 {name=l19 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 980 -130 0 1 {name=l20 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1000 -620 0 1 {name=BPC
l=4u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1040 -620 0 1 {name=l21 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 980 -670 0 0 {name=l22 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 980 -570 0 0 {name=l23 sig_type=std_logic lab=vbpc}
C {devices/isource.sym} 760 -180 0 0 {name=IABP value=5u}
C {devices/lab_pin.sym} 760 -230 0 1 {name=l25 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 760 -130 0 1 {name=l26 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 780 -620 0 1 {name=RP1
l=0.6u
w=13.32u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 820 -620 0 1 {name=l27 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 760 -670 0 0 {name=l28 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 760 -570 0 0 {name=l29 sig_type=std_logic lab=n1}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 780 -480 0 1 {name=RP2
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 820 -480 0 1 {name=l31 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 760 -530 0 0 {name=l32 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 760 -430 0 0 {name=l33 sig_type=std_logic lab=vabp}
C {devices/isource.sym} 180 -620 0 0 {name=IABN value=5u}
C {devices/lab_pin.sym} 180 -670 0 1 {name=l35 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 180 -570 0 1 {name=l36 sig_type=std_logic lab=vabn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 -180 0 1 {name=RN1
l=1u
w=8.8u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 240 -180 0 1 {name=l37 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 180 -230 0 0 {name=l38 sig_type=std_logic lab=n2}
C {devices/lab_pin.sym} 180 -130 0 0 {name=l39 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 -320 0 1 {name=RN2
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 240 -320 0 1 {name=l41 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 180 -370 0 0 {name=l42 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 180 -270 0 0 {name=l43 sig_type=std_logic lab=n2}
C {devices/title.sym} 160 0 0 0 {name=l0 author="Christoph Maier"}
