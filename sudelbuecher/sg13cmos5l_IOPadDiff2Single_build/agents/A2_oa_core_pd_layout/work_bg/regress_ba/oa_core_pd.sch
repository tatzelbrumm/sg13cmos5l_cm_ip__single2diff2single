v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 120 -1070 350 -1070 350 -115 120 -115 120 -1070 {dash=6}
P 10 5 370 -1070 860 -1070 860 -115 370 -115 370 -1070 {dash=6}
P 10 5 880 -1070 980 -1070 980 -115 880 -115 880 -1070 {dash=6}
P 10 5 125 -465 215 -465 215 -355 125 -355 125 -465 {dash=6}
P 10 5 260 -965 344 -965 344 -875 260 -875 260 -965 {dash=6}
T {oa_core_pd: reference-current core of bias_oa_pd, cut from that flat sheet (core devices and their wiring only).} 60 -1220 0 0 0.3 0.3 {}
T {iout: the core output (POC drain) into the tree input; en_3v3 / en_3v3_b: enable and its complement (from inv_3v3_pd).} 60 -1194 0 0 0.3 0.3 {}
T {Disabled: MS1 off (gate en_3v3_b), SKS pulls ks to vss, SVPG pulls vpg to vdd, so PO / POC are off and iout is high-Z.} 60 -1168 0 0 0.3 0.3 {}
T {Source: bias_ref_pd.spice} 60 -1142 0 0 0.3 0.3 {}
T {[S] start-up} 125 -1090 0 0 0.3 0.3 {layer=10}
T {[C] Oguey-Aebischer core} 375 -1090 0 0 0.3 0.3 {layer=10}
T {[R] output, I_ref} 885 -1090 0 0 0.3 0.3 {layer=10}
T {[E] enable} 125 -490 0 0 0.3 0.3 {layer=10}
T {[E] enable (en_3v3: 0 ... 3.3 V on vdd / vss, active high): IP / IN make en_3v3_b. Disabled: MS1 (gate now en_3v3_b instead of vss) is off,} 60 -1112 0 0 0.3 0.3 {layer=10}
T {[E] enable} 265 -990 0 0 0.3 0.3 {layer=10}
N 140 -920 180 -920 {lab=en_3v3_b}
N 220 -100 300 -100 {lab=vss}
N 220 -1000 220 -950 {lab=vdd}
N 220 -1000 240 -1000 {lab=vdd}
N 220 -920 240 -920 {lab=vdd}
N 220 -890 220 -560 {lab=ks}
N 220 -560 220 -450 {lab=ks}
N 220 -450 220 -230 {lab=ks}
N 220 -560 260 -560 {lab=ks}
N 200 -200 220 -200 {lab=vss}
N 220 -170 220 -100 {lab=vss}
N 200 -100 220 -100 {lab=vss}
N 240 -1000 240 -920 {lab=vdd}
N 440 -1000 460 -1000 {lab=vdd}
N 200 -200 200 -100 {lab=vss}
N 300 -560 320 -560 {lab=vss}
N 300 -530 300 -100 {lab=vss}
N 300 -100 320 -100 {lab=vss}
N 320 -560 320 -100 {lab=vss}
N 500 -200 520 -200 {lab=vbr}
N 500 -920 500 -860 {lab=vpg}
N 460 -860 500 -860 {lab=vpg}
N 500 -800 500 -740 {lab=vpc}
N 460 -740 500 -740 {lab=vpc}
N 500 -380 500 -320 {lab=vnc}
N 460 -1000 460 -950 {lab=vdd}
N 460 -1000 620 -1000 {lab=vdd}
N 440 -920 460 -920 {lab=vdd}
N 460 -890 460 -860 {lab=vpg}
N 460 -860 460 -830 {lab=vpg}
N 440 -800 460 -800 {lab=vdd}
N 460 -770 460 -740 {lab=vpc}
N 460 -720 460 -590 {lab=vpc}
N 440 -560 460 -560 {lab=vss}
N 460 -530 460 -350 {lab=d10}
N 440 -320 460 -320 {lab=vss}
N 440 -200 460 -200 {lab=vss}
N 440 -1000 440 -920 {lab=vdd}
N 440 -920 440 -800 {lab=vdd}
N 440 -560 440 -320 {lab=vss}
N 580 -920 580 -860 {lab=vpg}
N 580 -800 580 -740 {lab=vpc}
N 620 -1000 620 -950 {lab=vdd}
N 620 -1000 640 -1000 {lab=vdd}
N 620 -920 640 -920 {lab=vdd}
N 620 -890 620 -830 {lab=c8}
N 620 -800 640 -800 {lab=vdd}
N 620 -320 640 -320 {lab=vss}
N 640 -1000 640 -920 {lab=vdd}
N 640 -1000 780 -1000 {lab=vdd}
N 640 -920 640 -800 {lab=vdd}
N 740 -920 740 -860 {lab=vpg}
N 740 -860 900 -860 {lab=vpg}
N 740 -800 740 -740 {lab=vpc}
N 740 -260 780 -260 {lab=vbr}
N 780 -1000 780 -950 {lab=vdd}
N 780 -1000 800 -1000 {lab=vdd}
N 780 -920 800 -920 {lab=vdd}
N 780 -890 780 -830 {lab=c2}
N 780 -800 800 -800 {lab=vdd}
N 780 -770 780 -260 {lab=vbr}
N 780 -260 780 -230 {lab=vbr}
N 780 -200 800 -200 {lab=vss}
N 780 -170 780 -100 {lab=vss}
N 780 -100 800 -100 {lab=vss}
N 800 -1000 800 -920 {lab=vdd}
N 800 -1000 940 -1000 {lab=vdd}
N 800 -920 800 -800 {lab=vdd}
N 800 -200 800 -100 {lab=vss}
N 900 -920 900 -860 {lab=vpg}
N 900 -800 900 -740 {lab=vpc}
N 940 -1000 940 -950 {lab=vdd}
N 940 -1000 960 -1000 {lab=vdd}
N 940 -920 960 -920 {lab=vdd}
N 940 -890 940 -830 {lab=co}
N 940 -800 960 -800 {lab=vdd}
N 960 -1000 960 -920 {lab=vdd}
N 960 -920 960 -800 {lab=vdd}
N 620 -770 620 -380 {lab=vnc}
N 240 -1000 320 -1000 {lab=vdd}
N 320 -1000 340 -1000 {lab=vdd}
N 340 -1000 440 -1000 {lab=vdd}
N 500 -740 580 -740 {lab=vpc}
N 300 -720 460 -720 {lab=vpc}
N 460 -740 460 -720 {lab=vpc}
N 300 -720 300 -590 {lab=vpc}
N 640 -100 780 -100 {lab=vss}
N 740 -260 740 -200 {lab=vbr}
N 520 -260 740 -260 {lab=vbr}
N 580 -380 620 -380 {lab=vnc}
N 740 -740 900 -740 {lab=vpc}
N 580 -740 740 -740 {lab=vpc}
N 500 -560 520 -560 {lab=vbr}
N 580 -860 740 -860 {lab=vpg}
N 500 -860 580 -860 {lab=vpg}
N 620 -380 620 -350 {lab=vnc}
N 580 -380 580 -320 {lab=vnc}
N 500 -380 580 -380 {lab=vnc}
N 460 -170 460 -100 {lab=vss}
N 440 -100 460 -100 {lab=vss}
N 460 -290 460 -230 {lab=vres}
N 620 -290 620 -100 {lab=vss}
N 460 -100 620 -100 {lab=vss}
N 640 -320 640 -100 {lab=vss}
N 620 -100 640 -100 {lab=vss}
N 520 -240 520 -200 {lab=vbr}
N 260 -240 520 -240 {lab=vbr}
N 520 -560 520 -260 {lab=vbr}
N 260 -240 260 -200 {lab=vbr}
N 440 -200 440 -100 {lab=vss}
N 440 -320 440 -200 {lab=vss}
N 320 -100 440 -100 {lab=vss}
N 520 -260 520 -240 {lab=vbr}
N 180 -100 200 -100 {lab=vss}
N 140 -920 140 -580 {lab=en_3v3_b}
N 180 -450 180 -430 {lab=ks}
N 180 -450 220 -450 {lab=ks}
N 180 -370 180 -360 {lab=vss}
N 180 -360 180 -100 {lab=vss}
N 180 -400 200 -400 {lab=vss}
N 200 -400 200 -360 {lab=vss}
N 180 -360 200 -360 {lab=vss}
N 320 -1000 320 -950 {lab=vdd}
N 320 -920 340 -920 {lab=vdd}
N 340 -1000 340 -920 {lab=vdd}
N 320 -890 320 -860 {lab=vpg}
N 320 -860 460 -860 {lab=vpg}
N 140 -580 140 -400 {lab=en_3v3_b}
N 940 -770 940 -620 {lab=iout}
N 940 -620 1000 -620 {lab=iout}
N 80 -680 280 -680 {lab=en_3v3}
N 280 -920 280 -680 {lab=en_3v3}
N 80 -580 140 -580 {lab=en_3v3_b}
N 80 -1000 220 -1000 {lab=vdd}
N 80 -100 180 -100 {lab=vss}
T {MS1: replaced by the 8-device series chain MS1_0 ... MS1_7 in the [B] box} 200 -920 0 0 0.2 0.2 {}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 240 -200 0 1 {name=MS2
l=1u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 220 -700 0 0 {name=l1 sig_type=std_logic lab=ks}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 280 -560 0 0 {name=MS3
l=2u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 480 -920 0 1 {name=P0
l=8u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 480 -800 0 1 {name=P0C
l=2u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 480 -560 0 1 {name=MC10
l=1u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 480 -320 0 1 {name=M10
l=1u
w=180u
ng=18
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 480 -200 0 1 {name=MCL
l=30u
w=3.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 460 -520 0 1 {name=l2 sig_type=std_logic lab=d10}
C {devices/lab_wire.sym} 460 -260 0 1 {name=l3 sig_type=std_logic lab=vres}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -920 0 0 {name=P8
l=8u
w=16u
ng=8
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -800 0 0 {name=P8C
l=2u
w=4u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 620 -865 0 0 {name=l4 sig_type=std_logic lab=c8}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 -320 0 0 {name=M11
l=1u
w=90u
ng=9
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -920 0 0 {name=P2
l=8u
w=4u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -800 0 0 {name=P2C
l=2u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 780 -865 0 0 {name=l5 sig_type=std_logic lab=c2}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 760 -200 0 0 {name=MCS
l=30u
w=3.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 460 -875 0 1 {name=l6 sig_type=std_logic lab=vpg}
C {devices/lab_wire.sym} 460 -725 0 1 {name=l7 sig_type=std_logic lab=vpc}
C {devices/lab_wire.sym} 620 -380 0 1 {name=l8 sig_type=std_logic lab=vnc}
C {devices/lab_wire.sym} 780 -260 0 1 {name=l9 sig_type=std_logic lab=vbr}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 -920 0 0 {name=PO
l=8u
w=40u
ng=20
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 -800 0 0 {name=POC
l=2u
w=10u
ng=5
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 940 -865 0 0 {name=l10 sig_type=std_logic lab=co}
C {devices/iopin.sym} 80 -1000 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 80 -100 0 1 {name=p2 lab=vss}
C {devices/ipin.sym} 80 -680 0 0 {name=p11 lab=en_3v3}
C {devices/lab_wire.sym} 140 -580 0 1 {name=l20 sig_type=std_logic lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 160 -400 0 0 {name=SKS
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 300 -920 0 0 {name=SVPG
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/ipin.sym} 80 -580 0 0 {name=p13 lab=en_3v3_b}
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
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1240 -1050 0 0 {name=MDUM0
l=8u
w=4.4u
ng=9
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1260 -1020 0 0 {name=lba1032 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1220 -1050 2 0 {name=lba1033 sig_type=std_logic lab=vpg}
C {devices/lab_pin.sym} 1260 -1080 0 0 {name=lba1034 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1260 -1050 0 0 {name=lba1035 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1380 -1050 0 0 {name=MDUM1
l=1u
w=36u
ng=18
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 1400 -1080 0 0 {name=lba1036 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1360 -1050 2 0 {name=lba1037 sig_type=std_logic lab=vnc}
C {devices/lab_pin.sym} 1400 -1020 0 0 {name=lba1038 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1400 -1050 0 0 {name=lba1039 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1520 -1050 0 0 {name=MDUM2
l=1u
w=4u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 1540 -1080 0 0 {name=lba1040 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1500 -1050 2 0 {name=lba1041 sig_type=std_logic lab=vbr}
C {devices/lab_pin.sym} 1540 -1020 0 0 {name=lba1042 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1540 -1050 0 0 {name=lba1043 sig_type=std_logic lab=vss}
T {oa_pcas -> oa_pcas_c: own ntap ring removed, NWell to the cell edge; bulk through the merged vdd well (no device change)} 1080 -1110 0 0 0.25 0.25 {}
T {PMOS cells oa_pmir_c / oa_ms1 / oa_svpg / oa_pcas_c tap-less in ONE merged vdd NWell; n ties: thick tie under the vdd rail, two 8.2 um segments in oa_pmir_c's margins} 1080 -1088 0 0 0.25 0.25 {}
T {NMOS: oa_n10 (M10 / M11 / MC10 / MS2 / MS3 / SKS) and oa_mcs_c share one p+ tie; no ring} 1080 -1066 0 0 0.25 0.25 {}
