v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 140 -1070 380 -1070 380 -115 140 -115 140 -1070 {dash=6}
P 10 5 860 -1070 980 -1070 980 -115 860 -115 860 -1070 {dash=6}
P 10 5 400 -1070 840 -1070 840 -115 400 -115 400 -1070 {dash=6}
P 10 5 165 -255 255 -255 255 -135 165 -135 165 -255 {dash=6}
P 10 5 570 -965 644 -965 644 -875 570 -875 570 -965 {dash=6}
T {bg_core_pd: reference-current core of bias_bg_pd, cut from that flat sheet (core devices and their wiring only).} 60 -1190 0 0 0.3 0.3 {}
T {iout: the core output (POC drain) into the tree input; en_3v3 / en_3v3_b: enable and its complement (from inv_3v3_pd).} 60 -1164 0 0 0.3 0.3 {}
T {Disabled: MS1 off (gate en_3v3_b), SKS pulls ks to vss, SVPG pulls vpg to vdd, so PO / POC are off and iout is high-Z.} 60 -1138 0 0 0.3 0.3 {}
T {Source: bias_ref_pd.spice} 60 -1112 0 0 0.3 0.3 {}
T {[S] start-up} 145 -1090 0 0 0.3 0.3 {layer=10}
T {[R] output, I_ref} 865 -1090 0 0 0.3 0.3 {layer=10}
T {[C] bandgap core} 405 -1090 0 0 0.3 0.3 {layer=10}
T {[E] enable} 165 -280 0 0 0.3 0.3 {layer=10}
T {[E] enable} 575 -990 0 0 0.3 0.3 {layer=10}
N 260 -1000 260 -950 {lab=vdd}
N 260 -920 280 -920 {lab=vdd}
N 280 -1000 280 -920 {lab=vdd}
N 180 -920 220 -920 {lab=en_3v3_b}
N 240 -440 260 -440 {lab=vss}
N 260 -560 300 -560 {lab=ks}
N 340 -720 340 -590 {lab=vpc}
N 340 -560 360 -560 {lab=vss}
N 360 -560 360 -100 {lab=vss}
N 500 -920 500 -860 {lab=vpg}
N 460 -890 460 -860 {lab=vpg}
N 460 -1000 460 -950 {lab=vdd}
N 440 -920 460 -920 {lab=vdd}
N 440 -1000 440 -920 {lab=vdd}
N 500 -800 500 -740 {lab=vpc}
N 460 -740 500 -740 {lab=vpc}
N 460 -770 460 -740 {lab=vpc}
N 460 -860 460 -830 {lab=vpg}
N 440 -800 460 -800 {lab=vdd}
N 440 -920 440 -800 {lab=vdd}
N 440 -440 460 -440 {lab=vss}
N 460 -410 460 -380 {lab=eb}
N 460 -380 580 -380 {lab=eb}
N 580 -380 580 -350 {lab=eb}
N 540 -200 540 -100 {lab=vss}
N 780 -1000 780 -950 {lab=vdd}
N 780 -920 800 -920 {lab=vdd}
N 800 -1000 800 -920 {lab=vdd}
N 780 -800 800 -800 {lab=vdd}
N 800 -920 800 -800 {lab=vdd}
N 740 -500 740 -440 {lab=g}
N 740 -500 780 -500 {lab=g}
N 780 -440 800 -440 {lab=vss}
N 780 -380 780 -350 {lab=ea}
N 700 -380 780 -380 {lab=ea}
N 740 -200 740 -100 {lab=vss}
N 500 -500 500 -440 {lab=g}
N 500 -500 740 -500 {lab=g}
N 940 -1000 940 -950 {lab=vdd}
N 940 -920 960 -920 {lab=vdd}
N 960 -1000 960 -920 {lab=vdd}
N 940 -890 940 -830 {lab=co}
N 940 -800 960 -800 {lab=vdd}
N 960 -920 960 -800 {lab=vdd}
N 740 -920 740 -860 {lab=vpg}
N 740 -800 740 -740 {lab=vpc}
N 900 -920 900 -860 {lab=vpg}
N 900 -800 900 -740 {lab=vpc}
N 460 -380 460 -350 {lab=eb}
N 780 -500 780 -470 {lab=g}
N 700 -170 700 -100 {lab=vss}
N 580 -170 580 -100 {lab=vss}
N 780 -410 780 -380 {lab=ea}
N 780 -290 780 -100 {lab=vss}
N 700 -380 700 -230 {lab=ea}
N 580 -290 580 -230 {lab=e2}
N 460 -290 460 -100 {lab=vss}
N 800 -440 800 -100 {lab=vss}
N 440 -440 440 -100 {lab=vss}
N 340 -530 340 -100 {lab=vss}
N 460 -860 500 -860 {lab=vpg}
N 460 -720 460 -470 {lab=vpc}
N 260 -410 260 -100 {lab=vss}
N 260 -520 260 -470 {lab=ks}
N 300 -500 300 -440 {lab=g}
N 260 -1000 280 -1000 {lab=vdd}
N 640 -1000 780 -1000 {lab=vdd}
N 440 -1000 460 -1000 {lab=vdd}
N 780 -1000 800 -1000 {lab=vdd}
N 240 -100 260 -100 {lab=vss}
N 260 -100 340 -100 {lab=vss}
N 340 -100 360 -100 {lab=vss}
N 460 -100 540 -100 {lab=vss}
N 440 -100 460 -100 {lab=vss}
N 540 -100 580 -100 {lab=vss}
N 580 -100 700 -100 {lab=vss}
N 700 -100 740 -100 {lab=vss}
N 780 -100 800 -100 {lab=vss}
N 280 -1000 440 -1000 {lab=vdd}
N 780 -890 780 -830 {lab=ca}
N 360 -100 440 -100 {lab=vss}
N 780 -770 780 -500 {lab=g}
N 340 -720 460 -720 {lab=vpc}
N 460 -740 460 -720 {lab=vpc}
N 300 -500 500 -500 {lab=g}
N 220 -520 220 -230 {lab=ks}
N 220 -520 260 -520 {lab=ks}
N 220 -170 220 -100 {lab=vss}
N 220 -200 240 -200 {lab=vss}
N 240 -200 240 -100 {lab=vss}
N 220 -100 240 -100 {lab=vss}
N 620 -1000 620 -950 {lab=vdd}
N 620 -920 640 -920 {lab=vdd}
N 640 -1000 640 -920 {lab=vdd}
N 620 -890 620 -860 {lab=vpg}
N 260 -890 260 -560 {lab=ks}
N 620 -1000 640 -1000 {lab=vdd}
N 500 -860 620 -860 {lab=vpg}
N 460 -1000 620 -1000 {lab=vdd}
N 240 -440 240 -200 {lab=vss}
N 260 -560 260 -520 {lab=ks}
N 580 -920 580 -680 {lab=en_3v3}
N 180 -580 180 -200 {lab=en_3v3_b}
N 740 -100 780 -100 {lab=vss}
N 940 -1000 960 -1000 {lab=vdd}
N 740 -740 900 -740 {lab=vpc}
N 500 -740 740 -740 {lab=vpc}
N 740 -860 900 -860 {lab=vpg}
N 620 -860 740 -860 {lab=vpg}
N 800 -1000 940 -1000 {lab=vdd}
N 180 -920 180 -580 {lab=en_3v3_b}
N 940 -770 940 -620 {lab=iout}
N 940 -620 1000 -620 {}
N 100 -1000 260 -1000 {lab=vdd}
N 100 -100 220 -100 {lab=vss}
N 100 -680 580 -680 {lab=en_3v3}
N 100 -580 180 -580 {lab=en_3v3_b}
T {MS1: replaced by the 8-device series chain MS1_0 ... MS1_7 in the [B] box} 240 -920 0 0 0.2 0.2 {}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 280 -440 0 1 {name=MS2
l=1u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 260 -700 0 0 {name=l1 sig_type=std_logic lab=ks}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 -560 0 0 {name=MS3
l=2u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 480 -920 0 1 {name=PB
l=1u
w=40u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 480 -800 0 1 {name=PBC
l=1u
w=40u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 480 -440 0 1 {name=NB
l=4u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
T {R1B: replaced by the 10-segment series chain R1B_0 ... R1B_9 in the [B] box} 460 -320 0 0 0.2 0.2 {}
T {R0: replaced by the 18-segment series chain R0_0 ... R0_17 in the [B] box} 580 -320 0 0 0.2 0.2 {}
C {sg13cmos5l_pr/pnpMPA.sym} 560 -200 0 0 {name=Q2
model=pnpMPA
spiceprefix=X
w=2e-6
l=2e-6
m=8}
C {devices/lab_wire.sym} 460 -395 0 0 {name=l2 sig_type=std_logic lab=eb}
C {devices/lab_wire.sym} 580 -260 0 0 {name=l3 sig_type=std_logic lab=e2}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -920 0 0 {name=PA
l=1u
w=40u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -800 0 0 {name=PAC
l=1u
w=40u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 780 -865 0 0 {name=l4 sig_type=std_logic lab=ca}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 760 -440 0 0 {name=NA
l=4u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
T {R1A: replaced by the 11-segment series chain R1A_0 ... R1A_10 in the [B] box} 780 -320 0 0 0.2 0.2 {}
C {sg13cmos5l_pr/pnpMPA.sym} 720 -200 0 1 {name=Q1
model=pnpMPA
spiceprefix=X
w=2e-6
l=2e-6
m=1}
C {devices/lab_wire.sym} 780 -395 0 0 {name=l5 sig_type=std_logic lab=ea}
C {devices/lab_wire.sym} 780 -700 0 0 {name=l6 sig_type=std_logic lab=g}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 -920 0 0 {name=PO
l=1u
w=80u
ng=8
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 -800 0 0 {name=POC
l=1u
w=80u
ng=8
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 940 -865 0 0 {name=l7 sig_type=std_logic lab=co}
C {devices/lab_wire.sym} 460 -875 0 1 {name=l9 sig_type=std_logic lab=vpg}
C {devices/lab_wire.sym} 460 -725 0 1 {name=l10 sig_type=std_logic lab=vpc}
C {devices/iopin.sym} 100 -1000 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 100 -100 0 1 {name=p2 lab=vss}
C {devices/ipin.sym} 100 -680 0 0 {name=p11 lab=en_3v3}
C {devices/lab_wire.sym} 180 -580 0 1 {name=l19 sig_type=std_logic lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 -200 0 0 {name=SKS
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -920 0 0 {name=SVPG
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/ipin.sym} 100 -580 0 0 {name=p13 lab=en_3v3_b}
C {devices/opin.sym} 1000 -620 0 0 {name=p14 lab=iout}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
T {[B] layout-driven backannotation (series splits, dummies): see device_changes.txt} 1080 -1140 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -1050 0 0 {name=MS1_0
l=12.5u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -1020 0 0 {name=lba1000 sig_type=std_logic lab=ms1_1}
C {devices/lab_pin.sym} 1080 -1050 2 0 {name=lba1001 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1120 -1080 0 0 {name=lba1002 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1120 -1050 0 0 {name=lba1003 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -950 0 0 {name=MS1_1
l=12.5u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -920 0 0 {name=lba1004 sig_type=std_logic lab=ms1_2}
C {devices/lab_pin.sym} 1080 -950 2 0 {name=lba1005 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1120 -980 0 0 {name=lba1006 sig_type=std_logic lab=ms1_1}
C {devices/lab_pin.sym} 1120 -950 0 0 {name=lba1007 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -850 0 0 {name=MS1_2
l=12.5u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -820 0 0 {name=lba1008 sig_type=std_logic lab=ms1_3}
C {devices/lab_pin.sym} 1080 -850 2 0 {name=lba1009 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1120 -880 0 0 {name=lba1010 sig_type=std_logic lab=ms1_2}
C {devices/lab_pin.sym} 1120 -850 0 0 {name=lba1011 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -750 0 0 {name=MS1_3
l=12.5u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -720 0 0 {name=lba1012 sig_type=std_logic lab=ms1_4}
C {devices/lab_pin.sym} 1080 -750 2 0 {name=lba1013 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1120 -780 0 0 {name=lba1014 sig_type=std_logic lab=ms1_3}
C {devices/lab_pin.sym} 1120 -750 0 0 {name=lba1015 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -650 0 0 {name=MS1_4
l=12.5u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -620 0 0 {name=lba1016 sig_type=std_logic lab=ms1_5}
C {devices/lab_pin.sym} 1080 -650 2 0 {name=lba1017 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1120 -680 0 0 {name=lba1018 sig_type=std_logic lab=ms1_4}
C {devices/lab_pin.sym} 1120 -650 0 0 {name=lba1019 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -550 0 0 {name=MS1_5
l=12.5u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -520 0 0 {name=lba1020 sig_type=std_logic lab=ms1_6}
C {devices/lab_pin.sym} 1080 -550 2 0 {name=lba1021 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1120 -580 0 0 {name=lba1022 sig_type=std_logic lab=ms1_5}
C {devices/lab_pin.sym} 1120 -550 0 0 {name=lba1023 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -450 0 0 {name=MS1_6
l=12.5u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -420 0 0 {name=lba1024 sig_type=std_logic lab=ms1_7}
C {devices/lab_pin.sym} 1080 -450 2 0 {name=lba1025 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1120 -480 0 0 {name=lba1026 sig_type=std_logic lab=ms1_6}
C {devices/lab_pin.sym} 1120 -450 0 0 {name=lba1027 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -350 0 0 {name=MS1_7
l=12.5u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1120 -320 0 0 {name=lba1028 sig_type=std_logic lab=ks}
C {devices/lab_pin.sym} 1080 -350 2 0 {name=lba1029 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1120 -380 0 0 {name=lba1030 sig_type=std_logic lab=ms1_7}
C {devices/lab_pin.sym} 1120 -350 0 0 {name=lba1031 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/rhigh.sym} 1240 -1050 0 0 {name=R1B_0
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -1080 0 0 {name=lba1032 sig_type=std_logic lab=eb}
C {devices/lab_pin.sym} 1240 -1020 0 0 {name=lba1033 sig_type=std_logic lab=r1b_1}
C {sg13cmos5l_pr/rhigh.sym} 1240 -950 0 0 {name=R1B_1
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -980 0 0 {name=lba1034 sig_type=std_logic lab=r1b_1}
C {devices/lab_pin.sym} 1240 -920 0 0 {name=lba1035 sig_type=std_logic lab=r1b_2}
C {sg13cmos5l_pr/rhigh.sym} 1240 -850 0 0 {name=R1B_2
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -880 0 0 {name=lba1036 sig_type=std_logic lab=r1b_2}
C {devices/lab_pin.sym} 1240 -820 0 0 {name=lba1037 sig_type=std_logic lab=r1b_3}
C {sg13cmos5l_pr/rhigh.sym} 1240 -750 0 0 {name=R1B_3
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -780 0 0 {name=lba1038 sig_type=std_logic lab=r1b_3}
C {devices/lab_pin.sym} 1240 -720 0 0 {name=lba1039 sig_type=std_logic lab=r1b_4}
C {sg13cmos5l_pr/rhigh.sym} 1240 -650 0 0 {name=R1B_4
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -680 0 0 {name=lba1040 sig_type=std_logic lab=r1b_4}
C {devices/lab_pin.sym} 1240 -620 0 0 {name=lba1041 sig_type=std_logic lab=r1b_5}
C {sg13cmos5l_pr/rhigh.sym} 1240 -550 0 0 {name=R1B_5
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -580 0 0 {name=lba1042 sig_type=std_logic lab=r1b_5}
C {devices/lab_pin.sym} 1240 -520 0 0 {name=lba1043 sig_type=std_logic lab=r1b_6}
C {sg13cmos5l_pr/rhigh.sym} 1240 -450 0 0 {name=R1B_6
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -480 0 0 {name=lba1044 sig_type=std_logic lab=r1b_6}
C {devices/lab_pin.sym} 1240 -420 0 0 {name=lba1045 sig_type=std_logic lab=r1b_7}
C {sg13cmos5l_pr/rhigh.sym} 1240 -350 0 0 {name=R1B_7
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -380 0 0 {name=lba1046 sig_type=std_logic lab=r1b_7}
C {devices/lab_pin.sym} 1240 -320 0 0 {name=lba1047 sig_type=std_logic lab=r1b_8}
C {sg13cmos5l_pr/rhigh.sym} 1240 -250 0 0 {name=R1B_8
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -280 0 0 {name=lba1048 sig_type=std_logic lab=r1b_8}
C {devices/lab_pin.sym} 1240 -220 0 0 {name=lba1049 sig_type=std_logic lab=r1b_9}
C {sg13cmos5l_pr/rhigh.sym} 1240 -150 0 0 {name=R1B_9
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1240 -180 0 0 {name=lba1050 sig_type=std_logic lab=r1b_9}
C {devices/lab_pin.sym} 1240 -120 0 0 {name=lba1051 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/rhigh.sym} 1380 -1050 0 0 {name=R0_0
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -1080 0 0 {name=lba1052 sig_type=std_logic lab=eb}
C {devices/lab_pin.sym} 1380 -1020 0 0 {name=lba1053 sig_type=std_logic lab=r0_1}
C {sg13cmos5l_pr/rhigh.sym} 1380 -950 0 0 {name=R0_1
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -980 0 0 {name=lba1054 sig_type=std_logic lab=r0_1}
C {devices/lab_pin.sym} 1380 -920 0 0 {name=lba1055 sig_type=std_logic lab=r0_2}
C {sg13cmos5l_pr/rhigh.sym} 1380 -850 0 0 {name=R0_2
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -880 0 0 {name=lba1056 sig_type=std_logic lab=r0_2}
C {devices/lab_pin.sym} 1380 -820 0 0 {name=lba1057 sig_type=std_logic lab=r0_3}
C {sg13cmos5l_pr/rhigh.sym} 1380 -750 0 0 {name=R0_3
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -780 0 0 {name=lba1058 sig_type=std_logic lab=r0_3}
C {devices/lab_pin.sym} 1380 -720 0 0 {name=lba1059 sig_type=std_logic lab=r0_4}
C {sg13cmos5l_pr/rhigh.sym} 1380 -650 0 0 {name=R0_4
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -680 0 0 {name=lba1060 sig_type=std_logic lab=r0_4}
C {devices/lab_pin.sym} 1380 -620 0 0 {name=lba1061 sig_type=std_logic lab=r0_5}
C {sg13cmos5l_pr/rhigh.sym} 1380 -550 0 0 {name=R0_5
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -580 0 0 {name=lba1062 sig_type=std_logic lab=r0_5}
C {devices/lab_pin.sym} 1380 -520 0 0 {name=lba1063 sig_type=std_logic lab=r0_6}
C {sg13cmos5l_pr/rhigh.sym} 1380 -450 0 0 {name=R0_6
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -480 0 0 {name=lba1064 sig_type=std_logic lab=r0_6}
C {devices/lab_pin.sym} 1380 -420 0 0 {name=lba1065 sig_type=std_logic lab=r0_7}
C {sg13cmos5l_pr/rhigh.sym} 1380 -350 0 0 {name=R0_7
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -380 0 0 {name=lba1066 sig_type=std_logic lab=r0_7}
C {devices/lab_pin.sym} 1380 -320 0 0 {name=lba1067 sig_type=std_logic lab=r0_8}
C {sg13cmos5l_pr/rhigh.sym} 1380 -250 0 0 {name=R0_8
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -280 0 0 {name=lba1068 sig_type=std_logic lab=r0_8}
C {devices/lab_pin.sym} 1380 -220 0 0 {name=lba1069 sig_type=std_logic lab=r0_9}
C {sg13cmos5l_pr/rhigh.sym} 1380 -150 0 0 {name=R0_9
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1380 -180 0 0 {name=lba1070 sig_type=std_logic lab=r0_9}
C {devices/lab_pin.sym} 1380 -120 0 0 {name=lba1071 sig_type=std_logic lab=r0_10}
C {sg13cmos5l_pr/rhigh.sym} 1520 -1050 0 0 {name=R0_10
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1520 -1080 0 0 {name=lba1072 sig_type=std_logic lab=r0_10}
C {devices/lab_pin.sym} 1520 -1020 0 0 {name=lba1073 sig_type=std_logic lab=r0_11}
C {sg13cmos5l_pr/rhigh.sym} 1520 -950 0 0 {name=R0_11
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1520 -980 0 0 {name=lba1074 sig_type=std_logic lab=r0_11}
C {devices/lab_pin.sym} 1520 -920 0 0 {name=lba1075 sig_type=std_logic lab=r0_12}
C {sg13cmos5l_pr/rhigh.sym} 1520 -850 0 0 {name=R0_12
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1520 -880 0 0 {name=lba1076 sig_type=std_logic lab=r0_12}
C {devices/lab_pin.sym} 1520 -820 0 0 {name=lba1077 sig_type=std_logic lab=r0_13}
C {sg13cmos5l_pr/rhigh.sym} 1520 -750 0 0 {name=R0_13
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1520 -780 0 0 {name=lba1078 sig_type=std_logic lab=r0_13}
C {devices/lab_pin.sym} 1520 -720 0 0 {name=lba1079 sig_type=std_logic lab=r0_14}
C {sg13cmos5l_pr/rhigh.sym} 1520 -650 0 0 {name=R0_14
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1520 -680 0 0 {name=lba1080 sig_type=std_logic lab=r0_14}
C {devices/lab_pin.sym} 1520 -620 0 0 {name=lba1081 sig_type=std_logic lab=r0_15}
C {sg13cmos5l_pr/rhigh.sym} 1520 -550 0 0 {name=R0_15
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1520 -580 0 0 {name=lba1082 sig_type=std_logic lab=r0_15}
C {devices/lab_pin.sym} 1520 -520 0 0 {name=lba1083 sig_type=std_logic lab=r0_16}
C {sg13cmos5l_pr/rhigh.sym} 1520 -450 0 0 {name=R0_16
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1520 -480 0 0 {name=lba1084 sig_type=std_logic lab=r0_16}
C {devices/lab_pin.sym} 1520 -420 0 0 {name=lba1085 sig_type=std_logic lab=r0_17}
C {sg13cmos5l_pr/rhigh.sym} 1520 -350 0 0 {name=R0_17
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1520 -380 0 0 {name=lba1086 sig_type=std_logic lab=r0_17}
C {devices/lab_pin.sym} 1520 -320 0 0 {name=lba1087 sig_type=std_logic lab=e2}
C {sg13cmos5l_pr/rhigh.sym} 1660 -1050 0 0 {name=R1A_0
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -1080 0 0 {name=lba1088 sig_type=std_logic lab=ea}
C {devices/lab_pin.sym} 1660 -1020 0 0 {name=lba1089 sig_type=std_logic lab=r1a_1}
C {sg13cmos5l_pr/rhigh.sym} 1660 -950 0 0 {name=R1A_1
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -980 0 0 {name=lba1090 sig_type=std_logic lab=r1a_1}
C {devices/lab_pin.sym} 1660 -920 0 0 {name=lba1091 sig_type=std_logic lab=r1a_2}
C {sg13cmos5l_pr/rhigh.sym} 1660 -850 0 0 {name=R1A_2
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -880 0 0 {name=lba1092 sig_type=std_logic lab=r1a_2}
C {devices/lab_pin.sym} 1660 -820 0 0 {name=lba1093 sig_type=std_logic lab=r1a_3}
C {sg13cmos5l_pr/rhigh.sym} 1660 -750 0 0 {name=R1A_3
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -780 0 0 {name=lba1094 sig_type=std_logic lab=r1a_3}
C {devices/lab_pin.sym} 1660 -720 0 0 {name=lba1095 sig_type=std_logic lab=r1a_4}
C {sg13cmos5l_pr/rhigh.sym} 1660 -650 0 0 {name=R1A_4
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -680 0 0 {name=lba1096 sig_type=std_logic lab=r1a_4}
C {devices/lab_pin.sym} 1660 -620 0 0 {name=lba1097 sig_type=std_logic lab=r1a_5}
C {sg13cmos5l_pr/rhigh.sym} 1660 -550 0 0 {name=R1A_5
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -580 0 0 {name=lba1098 sig_type=std_logic lab=r1a_5}
C {devices/lab_pin.sym} 1660 -520 0 0 {name=lba1099 sig_type=std_logic lab=r1a_6}
C {sg13cmos5l_pr/rhigh.sym} 1660 -450 0 0 {name=R1A_6
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -480 0 0 {name=lba1100 sig_type=std_logic lab=r1a_6}
C {devices/lab_pin.sym} 1660 -420 0 0 {name=lba1101 sig_type=std_logic lab=r1a_7}
C {sg13cmos5l_pr/rhigh.sym} 1660 -350 0 0 {name=R1A_7
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -380 0 0 {name=lba1102 sig_type=std_logic lab=r1a_7}
C {devices/lab_pin.sym} 1660 -320 0 0 {name=lba1103 sig_type=std_logic lab=r1a_8}
C {sg13cmos5l_pr/rhigh.sym} 1660 -250 0 0 {name=R1A_8
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -280 0 0 {name=lba1104 sig_type=std_logic lab=r1a_8}
C {devices/lab_pin.sym} 1660 -220 0 0 {name=lba1105 sig_type=std_logic lab=r1a_9}
C {sg13cmos5l_pr/rhigh.sym} 1660 -150 0 0 {name=R1A_9
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1660 -180 0 0 {name=lba1106 sig_type=std_logic lab=r1a_9}
C {devices/lab_pin.sym} 1660 -120 0 0 {name=lba1107 sig_type=std_logic lab=r1a_10}
C {sg13cmos5l_pr/rhigh.sym} 1800 -1050 0 0 {name=R1A_10
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_pin.sym} 1800 -1080 0 0 {name=lba1108 sig_type=std_logic lab=r1a_10}
C {devices/lab_pin.sym} 1800 -1020 0 0 {name=lba1109 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1940 -1050 0 0 {name=MDUM0
l=1u
w=2.4u
ng=8
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1960 -1020 0 0 {name=lba1110 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1920 -1050 2 0 {name=lba1111 sig_type=std_logic lab=vpg}
C {devices/lab_pin.sym} 1960 -1080 0 0 {name=lba1112 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1960 -1050 0 0 {name=lba1113 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2080 -1050 0 0 {name=MDUM1
l=1u
w=2.4u
ng=8
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 2100 -1020 0 0 {name=lba1114 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2060 -1050 2 0 {name=lba1115 sig_type=std_logic lab=vpc}
C {devices/lab_pin.sym} 2100 -1080 0 0 {name=lba1116 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2100 -1050 0 0 {name=lba1117 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2220 -1050 0 0 {name=MDUM2
l=1u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 2240 -1080 0 0 {name=lba1118 sig_type=std_logic lab=g}
C {devices/lab_pin.sym} 2200 -1050 2 0 {name=lba1119 sig_type=std_logic lab=g}
C {devices/lab_pin.sym} 2240 -1020 0 0 {name=lba1120 sig_type=std_logic lab=g}
C {devices/lab_pin.sym} 2240 -1050 0 0 {name=lba1121 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2360 -1050 0 0 {name=MDUM3
l=4u
w=16u
ng=8
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 2380 -1080 0 0 {name=lba1122 sig_type=std_logic lab=g}
C {devices/lab_pin.sym} 2340 -1050 2 0 {name=lba1123 sig_type=std_logic lab=g}
C {devices/lab_pin.sym} 2380 -1020 0 0 {name=lba1124 sig_type=std_logic lab=g}
C {devices/lab_pin.sym} 2380 -1050 0 0 {name=lba1125 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/rhigh.sym} 2500 -1050 0 0 {name=RDUM0
w=0.5u
l=9.94u
model=rhigh
body=vss
spiceprefix=X
b=0
m=2
mm_ok=1}
C {devices/lab_pin.sym} 2500 -1080 0 0 {name=lba1126 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2500 -1020 0 0 {name=lba1127 sig_type=std_logic lab=vss}
T {PMOS cells bg_pmir_pcas_c / bg_ms1 / bg_svpg tap-less in ONE merged vdd NWell; n ties: thick tie under the vdd rail, one 13.1 um segment in bg_pmir_pcas_c's bottom margin over bg_ms1} 1080 -1110 0 0 0.25 0.25 {}
T {bg_n4 (NA, NB, MS2, MS3, SKS): own p+ ties at bottom and top; its dummies D = S = G = g (user's choice 2026-10-28 05:43)} 1080 -1088 0 0 0.25 0.25 {}
T {bg_res_c: the library's rhigh segments (0.5 x 9.94 um, 0.68 um pitch, the library's interleave) without the p-tap ring; bg_pnp_c: the library's 3 x 3 pnpMPA array (Q1 centre) with its emitter / base wiring} 1080 -1066 0 0 0.25 0.25 {}
