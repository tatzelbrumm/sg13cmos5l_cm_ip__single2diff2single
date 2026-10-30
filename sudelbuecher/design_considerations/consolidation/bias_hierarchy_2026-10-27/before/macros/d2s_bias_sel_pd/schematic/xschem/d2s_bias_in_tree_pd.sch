v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 360 -1130 500 -1130 500 -175 360 -175 360 -1130 {dash=6}
P 10 5 680 -1130 980 -1130 980 -175 680 -175 680 -1130 {dash=6}
P 10 5 520 -1130 660 -1130 660 -175 520 -175 520 -1130 {dash=6}
P 10 5 1160 -1130 1460 -1130 1460 -175 1160 -175 1160 -1130 {dash=6}
P 10 5 1000 -1130 1140 -1130 1140 -95 1000 -95 1000 -1130 {dash=6}
P 10 5 140 -1130 340 -1130 340 -175 140 -175 140 -1130 {dash=6}
T {d2s_bias_in_tree_pd: mirror tree + the six bias diodes (d2s_bias_diodes, drawn inline column by column)} 60 -1280 0 0 0.3 0.3 {}
T {Cut from macros/d2s_bias_in_pd (the flat sheet) without its inverter IP / IN; en_3v3_b is a port here.} 60 -1254 0 0 0.3 0.3 {}
T {TGN / TGP pass iref to ni while enabled; TDN pulls ni to vss while disabled. Source: d2s_bias_ref_pd.spice} 60 -1228 0 0 0.3 0.3 {}
T {[R] input} 365 -1150 0 0 0.3 0.3 {layer=10}
T {[8] PMOS diodes, NMOS sinks} 685 -1150 0 0 0.3 0.3 {layer=10}
T {[8] vabp} 525 -1150 0 0 0.3 0.3 {layer=10}
T {[8] PMOS sources, NMOS diodes} 1165 -1150 0 0 0.3 0.3 {layer=10}
T {[8] vabn} 1005 -1150 0 0 0.3 0.3 {layer=10}
T {[E] enable} 145 -1150 0 0 0.3 0.3 {layer=10}
T {[E] enable (en_3v3: 0 ... 3.3 V on vdd / vss, active high): IP / IN make en_3v3_b. Enabled, the transmission gate TGN / TGP} 80 -1196 0 0 0.3 0.3 {layer=10}
N 400 -260 400 -160 {lab=vss}
N 400 -260 420 -260 {lab=vss}
N 400 -160 420 -160 {lab=vss}
N 420 -360 460 -360 {lab=ni}
N 420 -230 420 -160 {lab=vss}
N 460 -360 540 -360 {lab=ni}
N 540 -1060 540 -860 {lab=vdd}
N 540 -860 580 -860 {lab=vdd}
N 540 -360 700 -360 {lab=ni}
N 560 -1100 560 -980 {lab=vddo}
N 560 -1100 580 -1100 {lab=vddo}
N 560 -980 580 -980 {lab=vddo}
N 580 -950 580 -920 {lab=n1}
N 580 -920 580 -890 {lab=n1}
N 580 -920 620 -920 {lab=n1}
N 580 -830 580 -720 {lab=vabp}
N 580 -720 580 -290 {lab=vabp}
N 580 -720 620 -720 {lab=vabp}
N 580 -260 600 -260 {lab=vss}
N 580 -230 580 -160 {lab=vss}
N 580 -160 600 -160 {lab=vss}
N 600 -260 600 -160 {lab=vss}
N 600 -160 740 -160 {lab=vss}
N 620 -980 620 -920 {lab=n1}
N 620 -860 620 -720 {lab=vabp}
N 620 -720 1500 -720 {lab=vabp}
N 700 -360 860 -360 {lab=ni}
N 720 -1060 720 -980 {lab=vdd}
N 720 -1060 740 -1060 {lab=vdd}
N 720 -980 740 -980 {lab=vdd}
N 740 -1060 740 -1010 {lab=vdd}
N 740 -1060 880 -1060 {lab=vdd}
N 740 -950 740 -760 {lab=vbpc}
N 740 -760 740 -290 {lab=vbpc}
N 740 -760 780 -760 {lab=vbpc}
N 740 -260 760 -260 {lab=vss}
N 740 -230 740 -160 {lab=vss}
N 740 -160 760 -160 {lab=vss}
N 760 -260 760 -160 {lab=vss}
N 760 -160 900 -160 {lab=vss}
N 780 -980 780 -760 {lab=vbpc}
N 780 -760 1500 -760 {lab=vbpc}
N 880 -1060 880 -980 {lab=vdd}
N 880 -1060 900 -1060 {lab=vdd}
N 880 -980 900 -980 {lab=vdd}
N 900 -1060 900 -1010 {lab=vdd}
N 900 -1060 1080 -1060 {lab=vdd}
N 900 -950 900 -800 {lab=vbp}
N 900 -800 900 -290 {lab=vbp}
N 900 -800 940 -800 {lab=vbp}
N 900 -260 920 -260 {lab=vss}
N 900 -230 900 -160 {lab=vss}
N 900 -160 920 -160 {lab=vss}
N 920 -260 920 -160 {lab=vss}
N 920 -160 1040 -160 {lab=vss}
N 940 -980 940 -800 {lab=vbp}
N 940 -800 1040 -800 {lab=vbp}
N 1040 -980 1040 -800 {lab=vbp}
N 1040 -800 1180 -800 {lab=vbp}
N 1040 -380 1040 -160 {lab=vss}
N 1040 -380 1080 -380 {lab=vss}
N 1040 -160 1200 -160 {lab=vss}
N 1060 -260 1060 -120 {lab=vsso}
N 1060 -260 1080 -260 {lab=vsso}
N 1060 -120 1080 -120 {lab=vsso}
N 1080 -1060 1080 -1010 {lab=vdd}
N 1080 -1060 1100 -1060 {lab=vdd}
N 1080 -980 1100 -980 {lab=vdd}
N 1080 -950 1080 -520 {lab=vabn}
N 1080 -520 1080 -410 {lab=vabn}
N 1080 -520 1120 -520 {lab=vabn}
N 1080 -350 1080 -320 {lab=n2}
N 1080 -320 1080 -290 {lab=n2}
N 1080 -320 1120 -320 {lab=n2}
N 1080 -230 1080 -120 {lab=vsso}
N 1100 -1060 1100 -980 {lab=vdd}
N 1100 -1060 1220 -1060 {lab=vdd}
N 1120 -520 1120 -380 {lab=vabn}
N 1120 -520 1500 -520 {lab=vabn}
N 1120 -320 1120 -260 {lab=n2}
N 1180 -980 1180 -800 {lab=vbp}
N 1180 -800 1340 -800 {lab=vbp}
N 1200 -260 1200 -160 {lab=vss}
N 1200 -260 1220 -260 {lab=vss}
N 1200 -160 1220 -160 {lab=vss}
N 1220 -1060 1220 -1010 {lab=vdd}
N 1220 -1060 1240 -1060 {lab=vdd}
N 1220 -980 1240 -980 {lab=vdd}
N 1220 -950 1220 -480 {lab=vbnc}
N 1220 -480 1220 -290 {lab=vbnc}
N 1220 -480 1260 -480 {lab=vbnc}
N 1220 -230 1220 -160 {lab=vss}
N 1220 -160 1360 -160 {lab=vss}
N 1240 -1060 1240 -980 {lab=vdd}
N 1240 -1060 1380 -1060 {lab=vdd}
N 1260 -480 1260 -260 {lab=vbnc}
N 1260 -480 1500 -480 {lab=vbnc}
N 1340 -980 1340 -800 {lab=vbp}
N 1340 -800 1500 -800 {lab=vbp}
N 1360 -260 1360 -160 {lab=vss}
N 1360 -260 1380 -260 {lab=vss}
N 1360 -160 1380 -160 {lab=vss}
N 1380 -1060 1380 -1010 {lab=vdd}
N 1380 -1060 1400 -1060 {lab=vdd}
N 1380 -980 1400 -980 {lab=vdd}
N 1380 -950 1380 -440 {lab=vbn}
N 1380 -440 1380 -290 {lab=vbn}
N 1380 -440 1420 -440 {lab=vbn}
N 1380 -230 1380 -160 {lab=vss}
N 1400 -1060 1400 -980 {lab=vdd}
N 1420 -440 1420 -260 {lab=vbn}
N 1420 -440 1500 -440 {lab=vbn}
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
N 860 -360 860 -260 {lab=ni}
N 540 -1060 720 -1060 {lab=vdd}
N 240 -420 240 -260 {lab=vss}
N 220 -620 220 -450 {lab=vdd}
N 300 -620 300 -570 {lab=vdd}
N 300 -510 300 -360 {lab=ni}
N 240 -160 400 -160 {lab=vss}
N 420 -160 580 -160 {lab=vss}
N 220 -390 220 -360 {lab=ni}
N 220 -360 300 -360 {lab=ni}
N 160 -260 180 -260 {lab=en_3v3_b}
N 160 -540 260 -540 {lab=en_3v3_b}
N 220 -620 300 -620 {lab=vdd}
N 300 -540 320 -540 {lab=vdd}
N 320 -1060 540 -1060 {lab=vdd}
N 300 -360 420 -360 {lab=ni}
N 580 -1100 580 -1010 {lab=vddo}
N 100 -1100 560 -1100 {lab=vddo}
N 100 -120 1060 -120 {lab=vsso}
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
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -980 0 1 {name=BPC
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 720 -260 0 0 {name=NBPC
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 740 -760 0 0 {name=l1 sig_type=std_logic lab=vbpc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 -980 0 1 {name=BP
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 880 -260 0 0 {name=NBP
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 900 -800 0 0 {name=l2 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -980 0 1 {name=RP1
l=0.6u
w=13.32u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -860 0 1 {name=RP2
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 580 -905 0 1 {name=l3 sig_type=std_logic lab=n1}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 560 -260 0 0 {name=NABP
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 580 -720 0 0 {name=l4 sig_type=std_logic lab=vabp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1200 -980 0 0 {name=PBNC
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1240 -260 0 1 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 1220 -480 0 0 {name=l5 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1360 -980 0 0 {name=PBN
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1400 -260 0 1 {name=BN
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 1380 -440 0 0 {name=l6 sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1060 -980 0 0 {name=PABN
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1100 -380 0 1 {name=RN2
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1100 -260 0 1 {name=RN1
l=1u
w=8.8u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 1080 -335 0 1 {name=l7 sig_type=std_logic lab=n2}
C {devices/lab_wire.sym} 1080 -520 0 0 {name=l8 sig_type=std_logic lab=vabn}
C {devices/iopin.sym} 100 -1060 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 100 -160 0 1 {name=p2 lab=vss}
C {devices/iopin.sym} 100 -1100 0 1 {name=p3 lab=vddo}
C {devices/iopin.sym} 100 -120 0 1 {name=p4 lab=vsso}
C {devices/iopin.sym} 100 -620 0 1 {name=p5 lab=iref}
C {devices/opin.sym} 1500 -800 0 0 {name=p6 lab=vbp}
C {devices/opin.sym} 1500 -440 0 0 {name=p7 lab=vbn}
C {devices/opin.sym} 1500 -760 0 0 {name=p8 lab=vbpc}
C {devices/opin.sym} 1500 -480 0 0 {name=p9 lab=vbnc}
C {devices/opin.sym} 1500 -720 0 0 {name=p10 lab=vabp}
C {devices/opin.sym} 1500 -520 0 0 {name=p11 lab=vabn}
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
