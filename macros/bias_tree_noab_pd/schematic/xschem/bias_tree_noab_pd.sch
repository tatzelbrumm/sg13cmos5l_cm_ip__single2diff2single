v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 360 -1130 500 -1130 500 -175 360 -175 360 -1130 {dash=6}
P 10 5 520 -1130 820 -1130 820 -175 520 -175 520 -1130 {dash=6}
P 10 5 900 -1130 1200 -1130 1200 -175 900 -175 900 -1130 {dash=6}
P 10 5 140 -1130 340 -1130 340 -175 140 -175 140 -1130 {dash=6}
T {bias_tree_noab_pd: bias_tree_pd without the class-AB branches NABP / PABN, for s2d (2026-10-27)} 60 -1280 0 0 0.3 0.3 {}
T {Cut from macros/bias_in_pd (the flat sheet) without its inverter IP / IN; en_3v3_b is a port here.} 60 -1254 0 0 0.3 0.3 {}
T {TGN / TGP pass iref to ni while enabled; TDN pulls ni to vss while disabled. Source: bias_ref_pd.spice} 60 -1228 0 0 0.3 0.3 {}
T {[R] input} 365 -1150 0 0 0.3 0.3 {layer=10}
T {[8] PMOS diodes, NMOS sinks} 525 -1150 0 0 0.3 0.3 {layer=10}
T {[8] PMOS sources, NMOS diodes} 905 -1150 0 0 0.3 0.3 {layer=10}
T {[E] enable} 145 -1150 0 0 0.3 0.3 {layer=10}
T {[E] enable (en_3v3: 0 ... 3.3 V on vdd / vss, active high): IP / IN make en_3v3_b. Enabled, the transmission gate TGN / TGP} 80 -1196 0 0 0.3 0.3 {layer=10}
T {Outputs vbp, vbpc, vbn, vbnc only; the four bias diodes BP, BPC, BN, BNC as in bias_tree_pd.} 60 -1202 0 0 0.3 0.3 {}
N 400 -260 400 -160 {lab=vss}
N 400 -260 420 -260 {lab=vss}
N 400 -160 420 -160 {lab=vss}
N 420 -360 460 -360 {lab=ni}
N 420 -230 420 -160 {lab=vss}
N 460 -360 520 -360 {lab=ni}
N 520 -360 540 -360 {lab=ni}
N 520 -160 580 -160 {lab=vss}
N 540 -360 700 -360 {lab=ni}
N 560 -1060 560 -980 {lab=vdd}
N 560 -1060 580 -1060 {lab=vdd}
N 560 -980 580 -980 {lab=vdd}
N 580 -1060 580 -1010 {lab=vdd}
N 580 -1060 720 -1060 {lab=vdd}
N 580 -950 580 -760 {lab=vbpc}
N 580 -760 580 -290 {lab=vbpc}
N 580 -760 620 -760 {lab=vbpc}
N 580 -260 600 -260 {lab=vss}
N 580 -230 580 -160 {lab=vss}
N 580 -160 600 -160 {lab=vss}
N 600 -260 600 -160 {lab=vss}
N 600 -160 740 -160 {lab=vss}
N 620 -980 620 -760 {lab=vbpc}
N 620 -760 1240 -760 {lab=vbpc}
N 720 -1060 720 -980 {lab=vdd}
N 720 -1060 740 -1060 {lab=vdd}
N 720 -980 740 -980 {lab=vdd}
N 740 -1060 740 -1010 {lab=vdd}
N 740 -1060 900 -1060 {lab=vdd}
N 740 -950 740 -800 {lab=vbp}
N 740 -800 740 -290 {lab=vbp}
N 740 -800 780 -800 {lab=vbp}
N 740 -260 760 -260 {lab=vss}
N 740 -230 740 -160 {lab=vss}
N 740 -160 760 -160 {lab=vss}
N 760 -260 760 -160 {lab=vss}
N 760 -160 900 -160 {lab=vss}
N 780 -980 780 -800 {lab=vbp}
N 780 -800 900 -800 {lab=vbp}
N 900 -800 920 -800 {lab=vbp}
N 900 -160 940 -160 {lab=vss}
N 900 -1060 960 -1060 {lab=vdd}
N 920 -980 920 -800 {lab=vbp}
N 920 -800 1080 -800 {lab=vbp}
N 940 -260 940 -160 {lab=vss}
N 940 -260 960 -260 {lab=vss}
N 940 -160 960 -160 {lab=vss}
N 960 -1060 960 -1010 {lab=vdd}
N 960 -1060 980 -1060 {lab=vdd}
N 960 -980 980 -980 {lab=vdd}
N 960 -950 960 -480 {lab=vbnc}
N 960 -480 960 -290 {lab=vbnc}
N 960 -480 1000 -480 {lab=vbnc}
N 960 -230 960 -160 {lab=vss}
N 960 -160 1100 -160 {lab=vss}
N 980 -1060 980 -980 {lab=vdd}
N 980 -1060 1120 -1060 {lab=vdd}
N 1000 -480 1000 -260 {lab=vbnc}
N 1000 -480 1240 -480 {lab=vbnc}
N 1080 -980 1080 -800 {lab=vbp}
N 1080 -800 1240 -800 {lab=vbp}
N 1100 -260 1100 -160 {lab=vss}
N 1100 -260 1120 -260 {lab=vss}
N 1100 -160 1120 -160 {lab=vss}
N 1120 -1060 1120 -1010 {lab=vdd}
N 1120 -1060 1140 -1060 {lab=vdd}
N 1120 -980 1140 -980 {lab=vdd}
N 1120 -950 1120 -440 {lab=vbn}
N 1120 -440 1120 -290 {lab=vbn}
N 1120 -440 1160 -440 {lab=vbn}
N 1120 -230 1120 -160 {lab=vss}
N 1140 -1060 1140 -980 {lab=vdd}
N 1160 -440 1160 -260 {lab=vbn}
N 1160 -440 1240 -440 {lab=vbn}
N 160 -540 160 -260 {lab=en_3v3_b}
N 220 -260 240 -260 {lab=vss}
N 220 -160 240 -160 {lab=vss}
N 240 -260 240 -160 {lab=vss}
N 220 -230 220 -160 {lab=vss}
N 220 -360 220 -290 {lab=ni}
N 420 -360 420 -290 {lab=ni}
N 460 -360 460 -260 {lab=ni}
N 540 -360 540 -260 {lab=ni}
N 700 -360 700 -260 {lab=ni}
N 520 -1060 560 -1060 {lab=vdd}
N 240 -420 240 -260 {lab=vss}
N 220 -620 220 -450 {lab=vdd}
N 300 -620 300 -570 {lab=vdd}
N 300 -510 300 -360 {lab=ni}
N 240 -160 400 -160 {lab=vss}
N 420 -160 520 -160 {lab=vss}
N 220 -390 220 -360 {lab=ni}
N 220 -360 300 -360 {lab=ni}
N 160 -260 180 -260 {lab=en_3v3_b}
N 160 -540 260 -540 {lab=en_3v3_b}
N 220 -620 300 -620 {lab=vdd}
N 300 -540 320 -540 {lab=vdd}
N 320 -1060 520 -1060 {lab=vdd}
N 300 -360 420 -360 {lab=ni}
N 100 -540 160 -540 {lab=en_3v3_b}
N 100 -160 220 -160 {lab=vss}
N 100 -620 220 -620 {lab=vdd}
N 320 -1060 320 -540 {lab=vdd}
N 100 -1060 320 -1060 {lab=vdd}
N 100 -420 180 -420 {lab=en_3v3}
N 220 -420 240 -420 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 440 -260 0 1 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -980 0 1 {name=BPC
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 560 -260 0 0 {name=NBPC
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 580 -760 0 0 {name=l1 sig_type=std_logic lab=vbpc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -980 0 1 {name=BP
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 720 -260 0 0 {name=NBP
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 740 -800 0 0 {name=l2 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 940 -980 0 0 {name=PBNC
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 980 -260 0 1 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 960 -480 0 0 {name=l5 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1100 -980 0 0 {name=PBN
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1140 -260 0 1 {name=BN
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 1120 -440 0 0 {name=l6 sig_type=std_logic lab=vbn}
C {devices/iopin.sym} 100 -1060 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 100 -160 0 1 {name=p2 lab=vss}
C {devices/iopin.sym} 100 -620 0 1 {name=p5 lab=iref}
C {devices/opin.sym} 1240 -800 0 0 {name=p6 lab=vbp}
C {devices/opin.sym} 1240 -440 0 0 {name=p7 lab=vbn}
C {devices/opin.sym} 1240 -760 0 0 {name=p8 lab=vbpc}
C {devices/opin.sym} 1240 -480 0 0 {name=p9 lab=vbnc}
C {devices/ipin.sym} 100 -420 0 0 {name=p12 lab=en_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 280 -540 0 0 {name=TGP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 -420 0 0 {name=TGN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 -260 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 220 -360 0 0 {name=l9 sig_type=std_logic lab=ni}
C {devices/ipin.sym} 100 -540 0 0 {name=p13 lab=en_3v3_b}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
