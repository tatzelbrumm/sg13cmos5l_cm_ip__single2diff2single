v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {devices/iopin.sym} -400 -600 0 0 {name=p1 lab=vdd_3v3}
C {devices/iopin.sym} -400 -560 0 0 {name=p2 lab=vss_3v3}
C {devices/iopin.sym} -400 -520 0 0 {name=p3 lab=vdd_1v2}
C {devices/iopin.sym} -400 -480 0 0 {name=p4 lab=vss_1v2}
C {devices/ipin.sym} -400 -440 0 0 {name=p5 lab=en0_1v2}
C {devices/ipin.sym} -400 -400 0 0 {name=p6 lab=en1_1v2}
C {devices/ipin.sym} -400 -360 0 0 {name=p7 lab=en2_1v2}
C {devices/ipin.sym} -400 -320 0 0 {name=p8 lab=en3_1v2}
C {devices/ipin.sym} -400 -280 0 0 {name=p9 lab=enable}
C {devices/opin.sym} -400 -240 0 0 {name=p10 lab=en0}
C {devices/opin.sym} -400 -200 0 0 {name=p11 lab=en0_b}
C {devices/opin.sym} -400 -160 0 0 {name=p12 lab=en1}
C {devices/opin.sym} -400 -120 0 0 {name=p13 lab=en1_b}
C {devices/opin.sym} -400 -80 0 0 {name=p14 lab=en2}
C {devices/opin.sym} -400 -40 0 0 {name=p15 lab=en2_b}
C {devices/opin.sym} -400 0 0 0 {name=p16 lab=en3}
C {devices/opin.sym} -400 40 0 0 {name=p17 lab=en3_b}
C {devices/opin.sym} -400 80 0 0 {name=p18 lab=rb0}
C {devices/opin.sym} -400 120 0 0 {name=p19 lab=rb1}
C {devices/opin.sym} -400 160 0 0 {name=p20 lab=rb2}
C {devices/opin.sym} -400 200 0 0 {name=p21 lab=rb3}
C {devices/opin.sym} -400 240 0 0 {name=p22 lab=lo4}
C {devices/opin.sym} -400 280 0 0 {name=p23 lab=lo5}
C {devices/opin.sym} -400 320 0 0 {name=p24 lab=lo6}
C {devices/opin.sym} -400 360 0 0 {name=p25 lab=lo7}
C {devices/opin.sym} -400 400 0 0 {name=p26 lab=lo8}
C {devices/opin.sym} -400 440 0 0 {name=p27 lab=lo9}
C {devices/opin.sym} -400 480 0 0 {name=p28 lab=lo10}
C {devices/opin.sym} -400 520 0 0 {name=p29 lab=lo11}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 0 -400 0 0 {name=PU0
l=20u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N -20 -400 -40 -400 {lab=vss_3v3}
C {devices/lab_pin.sym} -40 -400 0 0 {name=l1 sig_type=std_logic lab=vss_3v3}
N 20 -430 20 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 20 -450 0 1 {name=l2 sig_type=std_logic lab=vdd_3v3}
N 20 -370 20 -350 {lab=xb0}
C {devices/lab_pin.sym} 20 -350 0 1 {name=l3 sig_type=std_logic lab=xb0}
N 20 -400 60 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 60 -400 0 1 {name=l4 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 200 -400 0 0 {name=PU1
l=20u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 180 -400 160 -400 {lab=vss_3v3}
C {devices/lab_pin.sym} 160 -400 0 0 {name=l5 sig_type=std_logic lab=vss_3v3}
N 220 -430 220 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 220 -450 0 1 {name=l6 sig_type=std_logic lab=vdd_3v3}
N 220 -370 220 -350 {lab=xb1}
C {devices/lab_pin.sym} 220 -350 0 1 {name=l7 sig_type=std_logic lab=xb1}
N 220 -400 260 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 260 -400 0 1 {name=l8 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 -400 0 0 {name=PU2
l=20u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 380 -400 360 -400 {lab=vss_3v3}
C {devices/lab_pin.sym} 360 -400 0 0 {name=l9 sig_type=std_logic lab=vss_3v3}
N 420 -430 420 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 420 -450 0 1 {name=l10 sig_type=std_logic lab=vdd_3v3}
N 420 -370 420 -350 {lab=xb2}
C {devices/lab_pin.sym} 420 -350 0 1 {name=l11 sig_type=std_logic lab=xb2}
N 420 -400 460 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 460 -400 0 1 {name=l12 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -400 0 0 {name=PU3
l=20u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 580 -400 560 -400 {lab=vss_3v3}
C {devices/lab_pin.sym} 560 -400 0 0 {name=l13 sig_type=std_logic lab=vss_3v3}
N 620 -430 620 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 620 -450 0 1 {name=l14 sig_type=std_logic lab=vdd_3v3}
N 620 -370 620 -350 {lab=xb3}
C {devices/lab_pin.sym} 620 -350 0 1 {name=l15 sig_type=std_logic lab=xb3}
N 620 -400 660 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 660 -400 0 1 {name=l16 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 800 -400 0 0 {name=PA0
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 780 -400 760 -400 {lab=xb0}
C {devices/lab_pin.sym} 760 -400 0 0 {name=l17 sig_type=std_logic lab=xb0}
N 820 -430 820 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 820 -450 0 1 {name=l18 sig_type=std_logic lab=vdd_3v3}
N 820 -370 820 -350 {lab=en0}
C {devices/lab_pin.sym} 820 -350 0 1 {name=l19 sig_type=std_logic lab=en0}
N 820 -400 860 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 860 -400 0 1 {name=l20 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1000 -400 0 0 {name=PB0
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 980 -400 960 -400 {lab=en0}
C {devices/lab_pin.sym} 960 -400 0 0 {name=l21 sig_type=std_logic lab=en0}
N 1020 -430 1020 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1020 -450 0 1 {name=l22 sig_type=std_logic lab=vdd_3v3}
N 1020 -370 1020 -350 {lab=en0_b}
C {devices/lab_pin.sym} 1020 -350 0 1 {name=l23 sig_type=std_logic lab=en0_b}
N 1020 -400 1060 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1060 -400 0 1 {name=l24 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1200 -400 0 0 {name=PA1
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 1180 -400 1160 -400 {lab=xb1}
C {devices/lab_pin.sym} 1160 -400 0 0 {name=l25 sig_type=std_logic lab=xb1}
N 1220 -430 1220 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1220 -450 0 1 {name=l26 sig_type=std_logic lab=vdd_3v3}
N 1220 -370 1220 -350 {lab=en1}
C {devices/lab_pin.sym} 1220 -350 0 1 {name=l27 sig_type=std_logic lab=en1}
N 1220 -400 1260 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1260 -400 0 1 {name=l28 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1400 -400 0 0 {name=PB1
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 1380 -400 1360 -400 {lab=en1}
C {devices/lab_pin.sym} 1360 -400 0 0 {name=l29 sig_type=std_logic lab=en1}
N 1420 -430 1420 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1420 -450 0 1 {name=l30 sig_type=std_logic lab=vdd_3v3}
N 1420 -370 1420 -350 {lab=en1_b}
C {devices/lab_pin.sym} 1420 -350 0 1 {name=l31 sig_type=std_logic lab=en1_b}
N 1420 -400 1460 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1460 -400 0 1 {name=l32 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1600 -400 0 0 {name=PA2
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 1580 -400 1560 -400 {lab=xb2}
C {devices/lab_pin.sym} 1560 -400 0 0 {name=l33 sig_type=std_logic lab=xb2}
N 1620 -430 1620 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1620 -450 0 1 {name=l34 sig_type=std_logic lab=vdd_3v3}
N 1620 -370 1620 -350 {lab=en2}
C {devices/lab_pin.sym} 1620 -350 0 1 {name=l35 sig_type=std_logic lab=en2}
N 1620 -400 1660 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1660 -400 0 1 {name=l36 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1800 -400 0 0 {name=PB2
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 1780 -400 1760 -400 {lab=en2}
C {devices/lab_pin.sym} 1760 -400 0 0 {name=l37 sig_type=std_logic lab=en2}
N 1820 -430 1820 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1820 -450 0 1 {name=l38 sig_type=std_logic lab=vdd_3v3}
N 1820 -370 1820 -350 {lab=en2_b}
C {devices/lab_pin.sym} 1820 -350 0 1 {name=l39 sig_type=std_logic lab=en2_b}
N 1820 -400 1860 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1860 -400 0 1 {name=l40 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2000 -400 0 0 {name=PA3
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 1980 -400 1960 -400 {lab=xb3}
C {devices/lab_pin.sym} 1960 -400 0 0 {name=l41 sig_type=std_logic lab=xb3}
N 2020 -430 2020 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 2020 -450 0 1 {name=l42 sig_type=std_logic lab=vdd_3v3}
N 2020 -370 2020 -350 {lab=en3}
C {devices/lab_pin.sym} 2020 -350 0 1 {name=l43 sig_type=std_logic lab=en3}
N 2020 -400 2060 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 2060 -400 0 1 {name=l44 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2200 -400 0 0 {name=PB3
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 2180 -400 2160 -400 {lab=en3}
C {devices/lab_pin.sym} 2160 -400 0 0 {name=l45 sig_type=std_logic lab=en3}
N 2220 -430 2220 -450 {lab=vdd_3v3}
C {devices/lab_pin.sym} 2220 -450 0 1 {name=l46 sig_type=std_logic lab=vdd_3v3}
N 2220 -370 2220 -350 {lab=en3_b}
C {devices/lab_pin.sym} 2220 -350 0 1 {name=l47 sig_type=std_logic lab=en3_b}
N 2220 -400 2260 -400 {lab=vdd_3v3}
C {devices/lab_pin.sym} 2260 -400 0 1 {name=l48 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2400 -400 0 0 {name=PR0
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 2380 -400 2360 -400 {lab=xb0}
C {devices/lab_pin.sym} 2360 -400 0 0 {name=l49 sig_type=std_logic lab=xb0}
N 2420 -430 2420 -450 {lab=vdd_1v2}
C {devices/lab_pin.sym} 2420 -450 0 1 {name=l50 sig_type=std_logic lab=vdd_1v2}
N 2420 -370 2420 -350 {lab=rb0}
C {devices/lab_pin.sym} 2420 -350 0 1 {name=l51 sig_type=std_logic lab=rb0}
N 2420 -400 2460 -400 {lab=vdd_1v2}
C {devices/lab_pin.sym} 2460 -400 0 1 {name=l52 sig_type=std_logic lab=vdd_1v2}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2600 -400 0 0 {name=PR1
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 2580 -400 2560 -400 {lab=xb1}
C {devices/lab_pin.sym} 2560 -400 0 0 {name=l53 sig_type=std_logic lab=xb1}
N 2620 -430 2620 -450 {lab=vdd_1v2}
C {devices/lab_pin.sym} 2620 -450 0 1 {name=l54 sig_type=std_logic lab=vdd_1v2}
N 2620 -370 2620 -350 {lab=rb1}
C {devices/lab_pin.sym} 2620 -350 0 1 {name=l55 sig_type=std_logic lab=rb1}
N 2620 -400 2660 -400 {lab=vdd_1v2}
C {devices/lab_pin.sym} 2660 -400 0 1 {name=l56 sig_type=std_logic lab=vdd_1v2}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2800 -400 0 0 {name=PR2
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 2780 -400 2760 -400 {lab=xb2}
C {devices/lab_pin.sym} 2760 -400 0 0 {name=l57 sig_type=std_logic lab=xb2}
N 2820 -430 2820 -450 {lab=vdd_1v2}
C {devices/lab_pin.sym} 2820 -450 0 1 {name=l58 sig_type=std_logic lab=vdd_1v2}
N 2820 -370 2820 -350 {lab=rb2}
C {devices/lab_pin.sym} 2820 -350 0 1 {name=l59 sig_type=std_logic lab=rb2}
N 2820 -400 2860 -400 {lab=vdd_1v2}
C {devices/lab_pin.sym} 2860 -400 0 1 {name=l60 sig_type=std_logic lab=vdd_1v2}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 3000 -400 0 0 {name=PR3
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X}
N 2980 -400 2960 -400 {lab=xb3}
C {devices/lab_pin.sym} 2960 -400 0 0 {name=l61 sig_type=std_logic lab=xb3}
N 3020 -430 3020 -450 {lab=vdd_1v2}
C {devices/lab_pin.sym} 3020 -450 0 1 {name=l62 sig_type=std_logic lab=vdd_1v2}
N 3020 -370 3020 -350 {lab=rb3}
C {devices/lab_pin.sym} 3020 -350 0 1 {name=l63 sig_type=std_logic lab=rb3}
N 3020 -400 3060 -400 {lab=vdd_1v2}
C {devices/lab_pin.sym} 3060 -400 0 1 {name=l64 sig_type=std_logic lab=vdd_1v2}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 0 0 0 0 {name=NI0
l=0.45u
w=2u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N -20 0 -40 0 {lab=en0_1v2}
C {devices/lab_pin.sym} -40 0 0 0 {name=l65 sig_type=std_logic lab=en0_1v2}
N 20 -30 20 -50 {lab=xb0}
C {devices/lab_pin.sym} 20 -50 0 1 {name=l66 sig_type=std_logic lab=xb0}
N 20 30 20 50 {lab=ns1}
C {devices/lab_pin.sym} 20 50 0 1 {name=l67 sig_type=std_logic lab=ns1}
N 20 0 60 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 60 0 0 1 {name=l68 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 0 0 0 {name=NI1
l=0.45u
w=2u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 180 0 160 0 {lab=en1_1v2}
C {devices/lab_pin.sym} 160 0 0 0 {name=l69 sig_type=std_logic lab=en1_1v2}
N 220 -30 220 -50 {lab=xb1}
C {devices/lab_pin.sym} 220 -50 0 1 {name=l70 sig_type=std_logic lab=xb1}
N 220 30 220 50 {lab=ns1}
C {devices/lab_pin.sym} 220 50 0 1 {name=l71 sig_type=std_logic lab=ns1}
N 220 0 260 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 260 0 0 1 {name=l72 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 0 0 0 {name=NI2
l=0.45u
w=2u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 380 0 360 0 {lab=en2_1v2}
C {devices/lab_pin.sym} 360 0 0 0 {name=l73 sig_type=std_logic lab=en2_1v2}
N 420 -30 420 -50 {lab=xb2}
C {devices/lab_pin.sym} 420 -50 0 1 {name=l74 sig_type=std_logic lab=xb2}
N 420 30 420 50 {lab=ns1}
C {devices/lab_pin.sym} 420 50 0 1 {name=l75 sig_type=std_logic lab=ns1}
N 420 0 460 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 460 0 0 1 {name=l76 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 0 0 0 {name=NI3
l=0.45u
w=2u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 580 0 560 0 {lab=en3_1v2}
C {devices/lab_pin.sym} 560 0 0 0 {name=l77 sig_type=std_logic lab=en3_1v2}
N 620 -30 620 -50 {lab=xb3}
C {devices/lab_pin.sym} 620 -50 0 1 {name=l78 sig_type=std_logic lab=xb3}
N 620 30 620 50 {lab=ns1}
C {devices/lab_pin.sym} 620 50 0 1 {name=l79 sig_type=std_logic lab=ns1}
N 620 0 660 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 660 0 0 1 {name=l80 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 800 0 0 0 {name=NE
l=0.45u
w=2u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 780 0 760 0 {lab=enable}
C {devices/lab_pin.sym} 760 0 0 0 {name=l81 sig_type=std_logic lab=enable}
N 820 -30 820 -50 {lab=ns1}
C {devices/lab_pin.sym} 820 -50 0 1 {name=l82 sig_type=std_logic lab=ns1}
N 820 30 820 50 {lab=ns2}
C {devices/lab_pin.sym} 820 50 0 1 {name=l83 sig_type=std_logic lab=ns2}
N 820 0 860 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 860 0 0 1 {name=l84 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1000 0 0 0 {name=NV
l=0.45u
w=2u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 980 0 960 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 960 0 0 0 {name=l85 sig_type=std_logic lab=vdd_1v2}
N 1020 -30 1020 -50 {lab=ns2}
C {devices/lab_pin.sym} 1020 -50 0 1 {name=l86 sig_type=std_logic lab=ns2}
N 1020 30 1020 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 1020 50 0 1 {name=l87 sig_type=std_logic lab=vss_3v3}
N 1020 0 1060 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 1060 0 0 1 {name=l88 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1200 0 0 0 {name=NA0
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 1180 0 1160 0 {lab=xb0}
C {devices/lab_pin.sym} 1160 0 0 0 {name=l89 sig_type=std_logic lab=xb0}
N 1220 -30 1220 -50 {lab=en0}
C {devices/lab_pin.sym} 1220 -50 0 1 {name=l90 sig_type=std_logic lab=en0}
N 1220 30 1220 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 1220 50 0 1 {name=l91 sig_type=std_logic lab=vss_3v3}
N 1220 0 1260 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 1260 0 0 1 {name=l92 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1400 0 0 0 {name=NB0
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 1380 0 1360 0 {lab=en0}
C {devices/lab_pin.sym} 1360 0 0 0 {name=l93 sig_type=std_logic lab=en0}
N 1420 -30 1420 -50 {lab=en0_b}
C {devices/lab_pin.sym} 1420 -50 0 1 {name=l94 sig_type=std_logic lab=en0_b}
N 1420 30 1420 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 1420 50 0 1 {name=l95 sig_type=std_logic lab=vss_3v3}
N 1420 0 1460 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 1460 0 0 1 {name=l96 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1600 0 0 0 {name=NA1
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 1580 0 1560 0 {lab=xb1}
C {devices/lab_pin.sym} 1560 0 0 0 {name=l97 sig_type=std_logic lab=xb1}
N 1620 -30 1620 -50 {lab=en1}
C {devices/lab_pin.sym} 1620 -50 0 1 {name=l98 sig_type=std_logic lab=en1}
N 1620 30 1620 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 1620 50 0 1 {name=l99 sig_type=std_logic lab=vss_3v3}
N 1620 0 1660 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 1660 0 0 1 {name=l100 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1800 0 0 0 {name=NB1
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 1780 0 1760 0 {lab=en1}
C {devices/lab_pin.sym} 1760 0 0 0 {name=l101 sig_type=std_logic lab=en1}
N 1820 -30 1820 -50 {lab=en1_b}
C {devices/lab_pin.sym} 1820 -50 0 1 {name=l102 sig_type=std_logic lab=en1_b}
N 1820 30 1820 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 1820 50 0 1 {name=l103 sig_type=std_logic lab=vss_3v3}
N 1820 0 1860 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 1860 0 0 1 {name=l104 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2000 0 0 0 {name=NA2
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 1980 0 1960 0 {lab=xb2}
C {devices/lab_pin.sym} 1960 0 0 0 {name=l105 sig_type=std_logic lab=xb2}
N 2020 -30 2020 -50 {lab=en2}
C {devices/lab_pin.sym} 2020 -50 0 1 {name=l106 sig_type=std_logic lab=en2}
N 2020 30 2020 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 2020 50 0 1 {name=l107 sig_type=std_logic lab=vss_3v3}
N 2020 0 2060 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 2060 0 0 1 {name=l108 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2200 0 0 0 {name=NB2
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 2180 0 2160 0 {lab=en2}
C {devices/lab_pin.sym} 2160 0 0 0 {name=l109 sig_type=std_logic lab=en2}
N 2220 -30 2220 -50 {lab=en2_b}
C {devices/lab_pin.sym} 2220 -50 0 1 {name=l110 sig_type=std_logic lab=en2_b}
N 2220 30 2220 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 2220 50 0 1 {name=l111 sig_type=std_logic lab=vss_3v3}
N 2220 0 2260 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 2260 0 0 1 {name=l112 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2400 0 0 0 {name=NA3
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 2380 0 2360 0 {lab=xb3}
C {devices/lab_pin.sym} 2360 0 0 0 {name=l113 sig_type=std_logic lab=xb3}
N 2420 -30 2420 -50 {lab=en3}
C {devices/lab_pin.sym} 2420 -50 0 1 {name=l114 sig_type=std_logic lab=en3}
N 2420 30 2420 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 2420 50 0 1 {name=l115 sig_type=std_logic lab=vss_3v3}
N 2420 0 2460 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 2460 0 0 1 {name=l116 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2600 0 0 0 {name=NB3
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 2580 0 2560 0 {lab=en3}
C {devices/lab_pin.sym} 2560 0 0 0 {name=l117 sig_type=std_logic lab=en3}
N 2620 -30 2620 -50 {lab=en3_b}
C {devices/lab_pin.sym} 2620 -50 0 1 {name=l118 sig_type=std_logic lab=en3_b}
N 2620 30 2620 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 2620 50 0 1 {name=l119 sig_type=std_logic lab=vss_3v3}
N 2620 0 2660 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 2660 0 0 1 {name=l120 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2800 0 0 0 {name=NR0
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 2780 0 2760 0 {lab=xb0}
C {devices/lab_pin.sym} 2760 0 0 0 {name=l121 sig_type=std_logic lab=xb0}
N 2820 -30 2820 -50 {lab=rb0}
C {devices/lab_pin.sym} 2820 -50 0 1 {name=l122 sig_type=std_logic lab=rb0}
N 2820 30 2820 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 2820 50 0 1 {name=l123 sig_type=std_logic lab=vss_1v2}
N 2820 0 2860 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 2860 0 0 1 {name=l124 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3000 0 0 0 {name=NR1
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 2980 0 2960 0 {lab=xb1}
C {devices/lab_pin.sym} 2960 0 0 0 {name=l125 sig_type=std_logic lab=xb1}
N 3020 -30 3020 -50 {lab=rb1}
C {devices/lab_pin.sym} 3020 -50 0 1 {name=l126 sig_type=std_logic lab=rb1}
N 3020 30 3020 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 3020 50 0 1 {name=l127 sig_type=std_logic lab=vss_1v2}
N 3020 0 3060 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 3060 0 0 1 {name=l128 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3200 0 0 0 {name=NR2
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 3180 0 3160 0 {lab=xb2}
C {devices/lab_pin.sym} 3160 0 0 0 {name=l129 sig_type=std_logic lab=xb2}
N 3220 -30 3220 -50 {lab=rb2}
C {devices/lab_pin.sym} 3220 -50 0 1 {name=l130 sig_type=std_logic lab=rb2}
N 3220 30 3220 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 3220 50 0 1 {name=l131 sig_type=std_logic lab=vss_1v2}
N 3220 0 3260 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 3260 0 0 1 {name=l132 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3400 0 0 0 {name=NR3
l=0.45u
w=1u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 3380 0 3360 0 {lab=xb3}
C {devices/lab_pin.sym} 3360 0 0 0 {name=l133 sig_type=std_logic lab=xb3}
N 3420 -30 3420 -50 {lab=rb3}
C {devices/lab_pin.sym} 3420 -50 0 1 {name=l134 sig_type=std_logic lab=rb3}
N 3420 30 3420 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 3420 50 0 1 {name=l135 sig_type=std_logic lab=vss_1v2}
N 3420 0 3460 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 3460 0 0 1 {name=l136 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3600 0 0 0 {name=NRD
l=20u
w=0.3u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 3580 0 3560 0 {lab=vdd_3v3}
C {devices/lab_pin.sym} 3560 0 0 0 {name=l137 sig_type=std_logic lab=vdd_3v3}
N 3620 -30 3620 -50 {lab=vdd_1v2}
C {devices/lab_pin.sym} 3620 -50 0 1 {name=l138 sig_type=std_logic lab=vdd_1v2}
N 3620 30 3620 50 {lab=vss_3v3}
C {devices/lab_pin.sym} 3620 50 0 1 {name=l139 sig_type=std_logic lab=vss_3v3}
N 3620 0 3660 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 3660 0 0 1 {name=l140 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3800 0 0 0 {name=NL4
l=0.45u
w=0.5u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 3780 0 3760 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 3760 0 0 0 {name=l141 sig_type=std_logic lab=vdd_1v2}
N 3820 -30 3820 -50 {lab=lo4}
C {devices/lab_pin.sym} 3820 -50 0 1 {name=l142 sig_type=std_logic lab=lo4}
N 3820 30 3820 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 3820 50 0 1 {name=l143 sig_type=std_logic lab=vss_1v2}
N 3820 0 3860 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 3860 0 0 1 {name=l144 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 4000 0 0 0 {name=NL5
l=0.45u
w=0.5u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 3980 0 3960 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 3960 0 0 0 {name=l145 sig_type=std_logic lab=vdd_1v2}
N 4020 -30 4020 -50 {lab=lo5}
C {devices/lab_pin.sym} 4020 -50 0 1 {name=l146 sig_type=std_logic lab=lo5}
N 4020 30 4020 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 4020 50 0 1 {name=l147 sig_type=std_logic lab=vss_1v2}
N 4020 0 4060 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 4060 0 0 1 {name=l148 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 4200 0 0 0 {name=NL6
l=0.45u
w=0.5u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 4180 0 4160 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 4160 0 0 0 {name=l149 sig_type=std_logic lab=vdd_1v2}
N 4220 -30 4220 -50 {lab=lo6}
C {devices/lab_pin.sym} 4220 -50 0 1 {name=l150 sig_type=std_logic lab=lo6}
N 4220 30 4220 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 4220 50 0 1 {name=l151 sig_type=std_logic lab=vss_1v2}
N 4220 0 4260 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 4260 0 0 1 {name=l152 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 4400 0 0 0 {name=NL7
l=0.45u
w=0.5u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 4380 0 4360 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 4360 0 0 0 {name=l153 sig_type=std_logic lab=vdd_1v2}
N 4420 -30 4420 -50 {lab=lo7}
C {devices/lab_pin.sym} 4420 -50 0 1 {name=l154 sig_type=std_logic lab=lo7}
N 4420 30 4420 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 4420 50 0 1 {name=l155 sig_type=std_logic lab=vss_1v2}
N 4420 0 4460 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 4460 0 0 1 {name=l156 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 4600 0 0 0 {name=NL8
l=0.45u
w=0.5u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 4580 0 4560 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 4560 0 0 0 {name=l157 sig_type=std_logic lab=vdd_1v2}
N 4620 -30 4620 -50 {lab=lo8}
C {devices/lab_pin.sym} 4620 -50 0 1 {name=l158 sig_type=std_logic lab=lo8}
N 4620 30 4620 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 4620 50 0 1 {name=l159 sig_type=std_logic lab=vss_1v2}
N 4620 0 4660 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 4660 0 0 1 {name=l160 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 4800 0 0 0 {name=NL9
l=0.45u
w=0.5u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 4780 0 4760 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 4760 0 0 0 {name=l161 sig_type=std_logic lab=vdd_1v2}
N 4820 -30 4820 -50 {lab=lo9}
C {devices/lab_pin.sym} 4820 -50 0 1 {name=l162 sig_type=std_logic lab=lo9}
N 4820 30 4820 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 4820 50 0 1 {name=l163 sig_type=std_logic lab=vss_1v2}
N 4820 0 4860 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 4860 0 0 1 {name=l164 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 5000 0 0 0 {name=NL10
l=0.45u
w=0.5u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 4980 0 4960 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 4960 0 0 0 {name=l165 sig_type=std_logic lab=vdd_1v2}
N 5020 -30 5020 -50 {lab=lo10}
C {devices/lab_pin.sym} 5020 -50 0 1 {name=l166 sig_type=std_logic lab=lo10}
N 5020 30 5020 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 5020 50 0 1 {name=l167 sig_type=std_logic lab=vss_1v2}
N 5020 0 5060 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 5060 0 0 1 {name=l168 sig_type=std_logic lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 5200 0 0 0 {name=NL11
l=0.45u
w=0.5u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X}
N 5180 0 5160 0 {lab=vdd_1v2}
C {devices/lab_pin.sym} 5160 0 0 0 {name=l169 sig_type=std_logic lab=vdd_1v2}
N 5220 -30 5220 -50 {lab=lo11}
C {devices/lab_pin.sym} 5220 -50 0 1 {name=l170 sig_type=std_logic lab=lo11}
N 5220 30 5220 50 {lab=vss_1v2}
C {devices/lab_pin.sym} 5220 50 0 1 {name=l171 sig_type=std_logic lab=vss_1v2}
N 5220 0 5260 0 {lab=vss_3v3}
C {devices/lab_pin.sym} 5260 0 0 1 {name=l172 sig_type=std_logic lab=vss_3v3}
T {tp_en_ctrl: xb<c> = NOT(en<c>_1v2 AND enable AND vdd_1v2) (ratioed, weak PU 0.3/20); en<c> = NOT xb<c>; en<c>_b = NOT en<c>; rb<c> = en<c> on 1.2 V; lo<k> tie-low; NRD pulls a floating vdd_1v2 low; c = 0..3} -400 -720 0 0 0.3 0.3 {}
T {tp_en_ctrl (draft sheet, generated by gen_sheets.py)} -400 -780 0 0 0.5 0.5 {}
