v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} -400 -600 0 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -400 -560 0 0 {name=p2 lab=vss}
C {devices/ipin.sym} -400 -520 0 0 {name=p3 lab=vbp}
C {devices/ipin.sym} -400 -480 0 0 {name=p4 lab=vbn}
C {devices/ipin.sym} -400 -440 0 0 {name=p5 lab=vbpc}
C {devices/ipin.sym} -400 -400 0 0 {name=p6 lab=vbnc}
C {devices/ipin.sym} -400 -360 0 0 {name=p7 lab=vabp}
C {devices/ipin.sym} -400 -320 0 0 {name=p8 lab=vabn}
C {devices/isource.sym} 60 -140 0 0 {name=IBP value=20u}
N 60 -170 60 -190 {lab=vbp}
C {devices/lab_pin.sym} 60 -190 0 1 {name=l1 sig_type=std_logic lab=vbp}
N 60 -110 60 -90 {lab=vss}
C {devices/lab_pin.sym} 60 -90 0 1 {name=l2 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 0 -300 0 0 {name=BP
l=2u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N -20 -300 -40 -300 {lab=vbp}
C {devices/lab_pin.sym} -40 -300 0 0 {name=l3 sig_type=std_logic lab=vbp}
N 20 -330 20 -350 {lab=vdd}
C {devices/lab_pin.sym} 20 -350 0 1 {name=l4 sig_type=std_logic lab=vdd}
N 20 -270 20 -250 {lab=vbp}
C {devices/lab_pin.sym} 20 -250 0 1 {name=l5 sig_type=std_logic lab=vbp}
N 20 -300 80 -300 {lab=vdd}
C {devices/lab_pin.sym} 80 -300 0 1 {name=l6 sig_type=std_logic lab=vdd}
C {devices/isource.sym} 360 -300 0 0 {name=IBN value=50u}
N 360 -330 360 -350 {lab=vdd}
C {devices/lab_pin.sym} 360 -350 0 1 {name=l7 sig_type=std_logic lab=vdd}
N 360 -270 360 -250 {lab=vbn}
C {devices/lab_pin.sym} 360 -250 0 1 {name=l8 sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 300 -140 0 0 {name=BN
l=2u
w=25u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 280 -140 260 -140 {lab=vbn}
C {devices/lab_pin.sym} 260 -140 0 0 {name=l9 sig_type=std_logic lab=vbn}
N 320 -170 320 -190 {lab=vbn}
C {devices/lab_pin.sym} 320 -190 0 1 {name=l10 sig_type=std_logic lab=vbn}
N 320 -110 320 -90 {lab=vss}
C {devices/lab_pin.sym} 320 -90 0 1 {name=l11 sig_type=std_logic lab=vss}
N 320 -140 380 -140 {lab=vss}
C {devices/lab_pin.sym} 380 -140 0 1 {name=l12 sig_type=std_logic lab=vss}
C {devices/isource.sym} 960 -300 0 0 {name=IBNC value=5u}
N 960 -330 960 -350 {lab=vdd}
C {devices/lab_pin.sym} 960 -350 0 1 {name=l13 sig_type=std_logic lab=vdd}
N 960 -270 960 -250 {lab=vbnc}
C {devices/lab_pin.sym} 960 -250 0 1 {name=l14 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 900 -140 0 0 {name=BNC
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 880 -140 860 -140 {lab=vbnc}
C {devices/lab_pin.sym} 860 -140 0 0 {name=l15 sig_type=std_logic lab=vbnc}
N 920 -170 920 -190 {lab=vbnc}
C {devices/lab_pin.sym} 920 -190 0 1 {name=l16 sig_type=std_logic lab=vbnc}
N 920 -110 920 -90 {lab=vss}
C {devices/lab_pin.sym} 920 -90 0 1 {name=l17 sig_type=std_logic lab=vss}
N 920 -140 980 -140 {lab=vss}
C {devices/lab_pin.sym} 980 -140 0 1 {name=l18 sig_type=std_logic lab=vss}
C {devices/isource.sym} 660 -140 0 0 {name=IBPC value=5u}
N 660 -170 660 -190 {lab=vbpc}
C {devices/lab_pin.sym} 660 -190 0 1 {name=l19 sig_type=std_logic lab=vbpc}
N 660 -110 660 -90 {lab=vss}
C {devices/lab_pin.sym} 660 -90 0 1 {name=l20 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -300 0 0 {name=BPC
l=4u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 580 -300 560 -300 {lab=vbpc}
C {devices/lab_pin.sym} 560 -300 0 0 {name=l21 sig_type=std_logic lab=vbpc}
N 620 -330 620 -350 {lab=vdd}
C {devices/lab_pin.sym} 620 -350 0 1 {name=l22 sig_type=std_logic lab=vdd}
N 620 -270 620 -250 {lab=vbpc}
C {devices/lab_pin.sym} 620 -250 0 1 {name=l23 sig_type=std_logic lab=vbpc}
N 620 -300 680 -300 {lab=vdd}
C {devices/lab_pin.sym} 680 -300 0 1 {name=l24 sig_type=std_logic lab=vdd}
C {devices/isource.sym} 1260 -120 0 0 {name=IABP value=5u}
N 1260 -150 1260 -170 {lab=vabp}
C {devices/lab_pin.sym} 1260 -170 0 1 {name=l25 sig_type=std_logic lab=vabp}
N 1260 -90 1260 -70 {lab=vss}
C {devices/lab_pin.sym} 1260 -70 0 1 {name=l26 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1200 -440 0 0 {name=RP1
l=0.6u
w=13.32u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1180 -440 1160 -440 {lab=n1}
C {devices/lab_pin.sym} 1160 -440 0 0 {name=l27 sig_type=std_logic lab=n1}
N 1220 -470 1220 -490 {lab=vdd}
C {devices/lab_pin.sym} 1220 -490 0 1 {name=l28 sig_type=std_logic lab=vdd}
N 1220 -410 1220 -390 {lab=n1}
C {devices/lab_pin.sym} 1220 -390 0 1 {name=l29 sig_type=std_logic lab=n1}
N 1220 -440 1280 -440 {lab=vdd}
C {devices/lab_pin.sym} 1280 -440 0 1 {name=l30 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1200 -280 0 0 {name=RP2
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1180 -280 1160 -280 {lab=vabp}
C {devices/lab_pin.sym} 1160 -280 0 0 {name=l31 sig_type=std_logic lab=vabp}
N 1220 -310 1220 -330 {lab=n1}
C {devices/lab_pin.sym} 1220 -330 0 1 {name=l32 sig_type=std_logic lab=n1}
N 1220 -250 1220 -230 {lab=vabp}
C {devices/lab_pin.sym} 1220 -230 0 1 {name=l33 sig_type=std_logic lab=vabp}
N 1220 -280 1280 -280 {lab=vdd}
C {devices/lab_pin.sym} 1280 -280 0 1 {name=l34 sig_type=std_logic lab=vdd}
C {devices/isource.sym} 1560 -440 0 0 {name=IABN value=5u}
N 1560 -470 1560 -490 {lab=vdd}
C {devices/lab_pin.sym} 1560 -490 0 1 {name=l35 sig_type=std_logic lab=vdd}
N 1560 -410 1560 -390 {lab=vabn}
C {devices/lab_pin.sym} 1560 -390 0 1 {name=l36 sig_type=std_logic lab=vabn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1500 -120 0 0 {name=RN1
l=1u
w=8.8u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1480 -120 1460 -120 {lab=n2}
C {devices/lab_pin.sym} 1460 -120 0 0 {name=l37 sig_type=std_logic lab=n2}
N 1520 -150 1520 -170 {lab=n2}
C {devices/lab_pin.sym} 1520 -170 0 1 {name=l38 sig_type=std_logic lab=n2}
N 1520 -90 1520 -70 {lab=vss}
C {devices/lab_pin.sym} 1520 -70 0 1 {name=l39 sig_type=std_logic lab=vss}
N 1520 -120 1580 -120 {lab=vss}
C {devices/lab_pin.sym} 1580 -120 0 1 {name=l40 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1500 -280 0 0 {name=RN2
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1480 -280 1460 -280 {lab=vabn}
C {devices/lab_pin.sym} 1460 -280 0 0 {name=l41 sig_type=std_logic lab=vabn}
N 1520 -310 1520 -330 {lab=vabn}
C {devices/lab_pin.sym} 1520 -330 0 1 {name=l42 sig_type=std_logic lab=vabn}
N 1520 -250 1520 -230 {lab=n2}
C {devices/lab_pin.sym} 1520 -230 0 1 {name=l43 sig_type=std_logic lab=n2}
N 1520 -280 1580 -280 {lab=vss}
C {devices/lab_pin.sym} 1580 -280 0 1 {name=l44 sig_type=std_logic lab=vss}
C {devices/title.sym} 160 900 0 0 {name=l0 author="Christoph Maier"}
T {d2s_bias: bias voltages from ideal reference currents (iab = 5 uA)} -400 -760 0 0 0.6 0.6 {}
