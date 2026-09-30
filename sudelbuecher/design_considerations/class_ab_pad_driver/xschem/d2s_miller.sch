v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} -400 -600 0 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -400 -560 0 0 {name=p2 lab=vss}
C {devices/ipin.sym} -400 -520 0 0 {name=p3 lab=vinp}
C {devices/ipin.sym} -400 -480 0 0 {name=p4 lab=vinn}
C {devices/ipin.sym} -400 -440 0 0 {name=p5 lab=vref}
C {devices/iopin.sym} -400 -400 0 0 {name=p6 lab=vout}
C {devices/ipin.sym} -400 -360 0 0 {name=p7 lab=vfb}
C {devices/ipin.sym} -400 -320 0 0 {name=p8 lab=vbp}
C {devices/ipin.sym} -400 -280 0 0 {name=p9 lab=vbn}
C {devices/ipin.sym} -400 -240 0 0 {name=p10 lab=vbpc}
C {devices/ipin.sym} -400 -200 0 0 {name=p11 lab=vbnc}
C {devices/ipin.sym} -400 -160 0 0 {name=p12 lab=vabp}
C {devices/ipin.sym} -400 -120 0 0 {name=p13 lab=vabn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 0 -560 0 0 {name=T1a
l=2u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N -20 -560 -40 -560 {lab=vbp}
C {devices/lab_pin.sym} -40 -560 0 0 {name=l1 sig_type=std_logic lab=vbp}
N 20 -590 20 -610 {lab=vdd}
C {devices/lab_pin.sym} 20 -610 0 1 {name=l2 sig_type=std_logic lab=vdd}
N 20 -530 20 -510 {lab=s1a}
C {devices/lab_pin.sym} 20 -510 0 1 {name=l3 sig_type=std_logic lab=s1a}
N 20 -560 80 -560 {lab=vdd}
C {devices/lab_pin.sym} 80 -560 0 1 {name=l4 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 320 -560 0 1 {name=T1b
l=2u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 340 -560 360 -560 {lab=vbp}
C {devices/lab_pin.sym} 360 -560 0 1 {name=l5 sig_type=std_logic lab=vbp}
N 300 -590 300 -610 {lab=vdd}
C {devices/lab_pin.sym} 300 -610 0 0 {name=l6 sig_type=std_logic lab=vdd}
N 300 -530 300 -510 {lab=s1b}
C {devices/lab_pin.sym} 300 -510 0 0 {name=l7 sig_type=std_logic lab=s1b}
N 300 -560 240 -560 {lab=vdd}
C {devices/lab_pin.sym} 240 -560 0 0 {name=l8 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/rhigh.sym} 160 -420 0 0 {name=R1
w=0.5u
l=39u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
N 160 -450 160 -470 {lab=s1a}
C {devices/lab_pin.sym} 160 -470 0 1 {name=l9 sig_type=std_logic lab=s1a}
N 160 -390 160 -370 {lab=s1b}
C {devices/lab_pin.sym} 160 -370 0 1 {name=l10 sig_type=std_logic lab=s1b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 0 -300 0 0 {name=M1a
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N -20 -300 -40 -300 {lab=vinn}
C {devices/lab_pin.sym} -40 -300 0 0 {name=l11 sig_type=std_logic lab=vinn}
N 20 -330 20 -350 {lab=s1a}
C {devices/lab_pin.sym} 20 -350 0 1 {name=l12 sig_type=std_logic lab=s1a}
N 20 -270 20 -250 {lab=x}
C {devices/lab_pin.sym} 20 -250 0 1 {name=l13 sig_type=std_logic lab=x}
N 20 -300 80 -300 {lab=s1a}
C {devices/lab_pin.sym} 80 -300 0 1 {name=l14 sig_type=std_logic lab=s1a}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 320 -300 0 1 {name=M1b
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 340 -300 360 -300 {lab=vinp}
C {devices/lab_pin.sym} 360 -300 0 1 {name=l15 sig_type=std_logic lab=vinp}
N 300 -330 300 -350 {lab=s1b}
C {devices/lab_pin.sym} 300 -350 0 0 {name=l16 sig_type=std_logic lab=s1b}
N 300 -270 300 -250 {lab=y}
C {devices/lab_pin.sym} 300 -250 0 0 {name=l17 sig_type=std_logic lab=y}
N 300 -300 240 -300 {lab=s1b}
C {devices/lab_pin.sym} 240 -300 0 0 {name=l18 sig_type=std_logic lab=s1b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 640 -560 0 0 {name=T2a
l=2u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 620 -560 600 -560 {lab=vbp}
C {devices/lab_pin.sym} 600 -560 0 0 {name=l19 sig_type=std_logic lab=vbp}
N 660 -590 660 -610 {lab=vdd}
C {devices/lab_pin.sym} 660 -610 0 1 {name=l20 sig_type=std_logic lab=vdd}
N 660 -530 660 -510 {lab=s2a}
C {devices/lab_pin.sym} 660 -510 0 1 {name=l21 sig_type=std_logic lab=s2a}
N 660 -560 720 -560 {lab=vdd}
C {devices/lab_pin.sym} 720 -560 0 1 {name=l22 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 960 -560 0 1 {name=T2b
l=2u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 980 -560 1000 -560 {lab=vbp}
C {devices/lab_pin.sym} 1000 -560 0 1 {name=l23 sig_type=std_logic lab=vbp}
N 940 -590 940 -610 {lab=vdd}
C {devices/lab_pin.sym} 940 -610 0 0 {name=l24 sig_type=std_logic lab=vdd}
N 940 -530 940 -510 {lab=s2b}
C {devices/lab_pin.sym} 940 -510 0 0 {name=l25 sig_type=std_logic lab=s2b}
N 940 -560 880 -560 {lab=vdd}
C {devices/lab_pin.sym} 880 -560 0 0 {name=l26 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/rhigh.sym} 800 -420 0 0 {name=R2
w=0.5u
l=17u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
N 800 -450 800 -470 {lab=s2a}
C {devices/lab_pin.sym} 800 -470 0 1 {name=l27 sig_type=std_logic lab=s2a}
N 800 -390 800 -370 {lab=s2b}
C {devices/lab_pin.sym} 800 -370 0 1 {name=l28 sig_type=std_logic lab=s2b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 640 -300 0 0 {name=M2a
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 620 -300 600 -300 {lab=vref}
C {devices/lab_pin.sym} 600 -300 0 0 {name=l29 sig_type=std_logic lab=vref}
N 660 -330 660 -350 {lab=s2a}
C {devices/lab_pin.sym} 660 -350 0 1 {name=l30 sig_type=std_logic lab=s2a}
N 660 -270 660 -250 {lab=y}
C {devices/lab_pin.sym} 660 -250 0 1 {name=l31 sig_type=std_logic lab=y}
N 660 -300 720 -300 {lab=s2a}
C {devices/lab_pin.sym} 720 -300 0 1 {name=l32 sig_type=std_logic lab=s2a}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 960 -300 0 1 {name=M2b
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 980 -300 1000 -300 {lab=vfb}
C {devices/lab_pin.sym} 1000 -300 0 1 {name=l33 sig_type=std_logic lab=vfb}
N 940 -330 940 -350 {lab=s2b}
C {devices/lab_pin.sym} 940 -350 0 0 {name=l34 sig_type=std_logic lab=s2b}
N 940 -270 940 -250 {lab=x}
C {devices/lab_pin.sym} 940 -250 0 0 {name=l35 sig_type=std_logic lab=x}
N 940 -300 880 -300 {lab=s2b}
C {devices/lab_pin.sym} 880 -300 0 0 {name=l36 sig_type=std_logic lab=s2b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1300 160 0 0 {name=SX
l=2u
w=25u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1280 160 1260 160 {lab=vbn}
C {devices/lab_pin.sym} 1260 160 0 0 {name=l37 sig_type=std_logic lab=vbn}
N 1320 130 1320 110 {lab=x}
C {devices/lab_pin.sym} 1320 110 0 1 {name=l38 sig_type=std_logic lab=x}
N 1320 190 1320 210 {lab=vss}
C {devices/lab_pin.sym} 1320 210 0 1 {name=l39 sig_type=std_logic lab=vss}
N 1320 160 1380 160 {lab=vss}
C {devices/lab_pin.sym} 1380 160 0 1 {name=l40 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1820 160 0 0 {name=SY
l=2u
w=25u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1800 160 1780 160 {lab=vbn}
C {devices/lab_pin.sym} 1780 160 0 0 {name=l41 sig_type=std_logic lab=vbn}
N 1840 130 1840 110 {lab=y}
C {devices/lab_pin.sym} 1840 110 0 1 {name=l42 sig_type=std_logic lab=y}
N 1840 190 1840 210 {lab=vss}
C {devices/lab_pin.sym} 1840 210 0 1 {name=l43 sig_type=std_logic lab=vss}
N 1840 160 1900 160 {lab=vss}
C {devices/lab_pin.sym} 1900 160 0 1 {name=l44 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1300 0 0 0 {name=CX
l=1u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1280 0 1260 0 {lab=vbnc}
C {devices/lab_pin.sym} 1260 0 0 0 {name=l45 sig_type=std_logic lab=vbnc}
N 1320 -30 1320 -50 {lab=l1}
C {devices/lab_pin.sym} 1320 -50 0 1 {name=l46 sig_type=std_logic lab=l1}
N 1320 30 1320 50 {lab=x}
C {devices/lab_pin.sym} 1320 50 0 1 {name=l47 sig_type=std_logic lab=x}
N 1320 0 1380 0 {lab=vss}
C {devices/lab_pin.sym} 1380 0 0 1 {name=l48 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1820 0 0 0 {name=CY
l=1u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1800 0 1780 0 {lab=vbnc}
C {devices/lab_pin.sym} 1780 0 0 0 {name=l49 sig_type=std_logic lab=vbnc}
N 1840 -30 1840 -50 {lab=b}
C {devices/lab_pin.sym} 1840 -50 0 1 {name=l50 sig_type=std_logic lab=b}
N 1840 30 1840 50 {lab=y}
C {devices/lab_pin.sym} 1840 50 0 1 {name=l51 sig_type=std_logic lab=y}
N 1840 0 1900 0 {lab=vss}
C {devices/lab_pin.sym} 1900 0 0 1 {name=l52 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1300 -560 0 0 {name=PL
l=2u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1280 -560 1260 -560 {lab=l2}
C {devices/lab_pin.sym} 1260 -560 0 0 {name=l53 sig_type=std_logic lab=l2}
N 1320 -590 1320 -610 {lab=vdd}
C {devices/lab_pin.sym} 1320 -610 0 1 {name=l54 sig_type=std_logic lab=vdd}
N 1320 -530 1320 -510 {lab=pl}
C {devices/lab_pin.sym} 1320 -510 0 1 {name=l55 sig_type=std_logic lab=pl}
N 1320 -560 1380 -560 {lab=vdd}
C {devices/lab_pin.sym} 1380 -560 0 1 {name=l56 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1820 -560 0 0 {name=PR
l=2u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1800 -560 1780 -560 {lab=l2}
C {devices/lab_pin.sym} 1780 -560 0 0 {name=l57 sig_type=std_logic lab=l2}
N 1840 -590 1840 -610 {lab=vdd}
C {devices/lab_pin.sym} 1840 -610 0 1 {name=l58 sig_type=std_logic lab=vdd}
N 1840 -530 1840 -510 {lab=pr}
C {devices/lab_pin.sym} 1840 -510 0 1 {name=l59 sig_type=std_logic lab=pr}
N 1840 -560 1900 -560 {lab=vdd}
C {devices/lab_pin.sym} 1900 -560 0 1 {name=l60 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1300 -400 0 0 {name=PCL
l=1u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1280 -400 1260 -400 {lab=vbpc}
C {devices/lab_pin.sym} 1260 -400 0 0 {name=l61 sig_type=std_logic lab=vbpc}
N 1320 -430 1320 -450 {lab=pl}
C {devices/lab_pin.sym} 1320 -450 0 1 {name=l62 sig_type=std_logic lab=pl}
N 1320 -370 1320 -350 {lab=l2}
C {devices/lab_pin.sym} 1320 -350 0 1 {name=l63 sig_type=std_logic lab=l2}
N 1320 -400 1380 -400 {lab=vdd}
C {devices/lab_pin.sym} 1380 -400 0 1 {name=l64 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1820 -400 0 0 {name=PCR
l=1u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1800 -400 1780 -400 {lab=vbpc}
C {devices/lab_pin.sym} 1780 -400 0 0 {name=l65 sig_type=std_logic lab=vbpc}
N 1840 -430 1840 -450 {lab=pr}
C {devices/lab_pin.sym} 1840 -450 0 1 {name=l66 sig_type=std_logic lab=pr}
N 1840 -370 1840 -350 {lab=a}
C {devices/lab_pin.sym} 1840 -350 0 1 {name=l67 sig_type=std_logic lab=a}
N 1840 -400 1900 -400 {lab=vdd}
C {devices/lab_pin.sym} 1900 -400 0 1 {name=l68 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1160 -200 0 0 {name=FPL
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1140 -200 1120 -200 {lab=vabp}
C {devices/lab_pin.sym} 1120 -200 0 0 {name=l69 sig_type=std_logic lab=vabp}
N 1180 -230 1180 -250 {lab=l2}
C {devices/lab_pin.sym} 1180 -250 0 1 {name=l70 sig_type=std_logic lab=l2}
N 1180 -170 1180 -150 {lab=l1}
C {devices/lab_pin.sym} 1180 -150 0 1 {name=l71 sig_type=std_logic lab=l1}
N 1180 -200 1240 -200 {lab=vdd}
C {devices/lab_pin.sym} 1240 -200 0 1 {name=l72 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1460 -200 0 1 {name=FNL
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1480 -200 1500 -200 {lab=vabn}
C {devices/lab_pin.sym} 1500 -200 0 1 {name=l73 sig_type=std_logic lab=vabn}
N 1440 -230 1440 -250 {lab=l2}
C {devices/lab_pin.sym} 1440 -250 0 0 {name=l74 sig_type=std_logic lab=l2}
N 1440 -170 1440 -150 {lab=l1}
C {devices/lab_pin.sym} 1440 -150 0 0 {name=l75 sig_type=std_logic lab=l1}
N 1440 -200 1380 -200 {lab=vss}
C {devices/lab_pin.sym} 1380 -200 0 0 {name=l76 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1780 -200 0 0 {name=ABP
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1760 -200 1740 -200 {lab=vabp}
C {devices/lab_pin.sym} 1740 -200 0 0 {name=l77 sig_type=std_logic lab=vabp}
N 1800 -230 1800 -250 {lab=a}
C {devices/lab_pin.sym} 1800 -250 0 1 {name=l78 sig_type=std_logic lab=a}
N 1800 -170 1800 -150 {lab=b}
C {devices/lab_pin.sym} 1800 -150 0 1 {name=l79 sig_type=std_logic lab=b}
N 1800 -200 1860 -200 {lab=vdd}
C {devices/lab_pin.sym} 1860 -200 0 1 {name=l80 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2060 -200 0 1 {name=ABN
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 2080 -200 2100 -200 {lab=vabn}
C {devices/lab_pin.sym} 2100 -200 0 1 {name=l81 sig_type=std_logic lab=vabn}
N 2040 -230 2040 -250 {lab=a}
C {devices/lab_pin.sym} 2040 -250 0 0 {name=l82 sig_type=std_logic lab=a}
N 2040 -170 2040 -150 {lab=b}
C {devices/lab_pin.sym} 2040 -150 0 0 {name=l83 sig_type=std_logic lab=b}
N 2040 -200 1980 -200 {lab=vss}
C {devices/lab_pin.sym} 1980 -200 0 0 {name=l84 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2280 -400 0 0 {name=OP
l=0.6u
w=546.12u
ng=82
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 2260 -400 2240 -400 {lab=a}
C {devices/lab_pin.sym} 2240 -400 0 0 {name=l85 sig_type=std_logic lab=a}
N 2300 -430 2300 -450 {lab=vdd}
C {devices/lab_pin.sym} 2300 -450 0 1 {name=l86 sig_type=std_logic lab=vdd}
N 2300 -370 2300 -350 {lab=vout}
C {devices/lab_pin.sym} 2300 -350 0 1 {name=l87 sig_type=std_logic lab=vout}
N 2300 -400 2360 -400 {lab=vdd}
C {devices/lab_pin.sym} 2360 -400 0 1 {name=l88 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2280 0 0 0 {name=ON
l=1u
w=290.4u
ng=66
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 2260 0 2240 0 {lab=b}
C {devices/lab_pin.sym} 2240 0 0 0 {name=l89 sig_type=std_logic lab=b}
N 2300 -30 2300 -50 {lab=vout}
C {devices/lab_pin.sym} 2300 -50 0 1 {name=l90 sig_type=std_logic lab=vout}
N 2300 30 2300 50 {lab=vss}
C {devices/lab_pin.sym} 2300 50 0 1 {name=l91 sig_type=std_logic lab=vss}
N 2300 0 2360 0 {lab=vss}
C {devices/lab_pin.sym} 2360 0 0 1 {name=l92 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/cap_cmomi.sym} 2200 -200 0 0 {name=CMA
model=cap_cmomi
w=31e-6
l=31e-6
mmin=1
mmax=4
feed=double
subblock=0
m=1
mm_ok=1
spiceprefix=X}
N 2200 -230 2200 -250 {lab=vout}
C {devices/lab_pin.sym} 2200 -250 0 1 {name=l93 sig_type=std_logic lab=vout}
N 2200 -170 2200 -150 {lab=a}
C {devices/lab_pin.sym} 2200 -150 0 1 {name=l94 sig_type=std_logic lab=a}
C {sg13cmos5l_pr/cap_cmomi.sym} 2480 -200 0 0 {name=CMB
model=cap_cmomi
w=31e-6
l=31e-6
mmin=1
mmax=4
feed=double
subblock=0
m=1
mm_ok=1
spiceprefix=X}
N 2480 -230 2480 -250 {lab=vout}
C {devices/lab_pin.sym} 2480 -250 0 1 {name=l95 sig_type=std_logic lab=vout}
N 2480 -170 2480 -150 {lab=b}
C {devices/lab_pin.sym} 2480 -150 0 1 {name=l96 sig_type=std_logic lab=b}
C {devices/title.sym} 160 900 0 0 {name=l0 author="Christoph Maier"}
T {d2s_miller: two-stage class-AB pad driver, Miller compensated (vfb = vout)} -400 -760 0 0 0.6 0.6 {}
