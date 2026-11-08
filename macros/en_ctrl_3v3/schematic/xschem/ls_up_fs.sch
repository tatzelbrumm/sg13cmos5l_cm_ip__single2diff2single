v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {ls_up_fs: fail-safe 1.2 V -> 3.3 V level shifter that needs no 1.2 V supply (sg13_hv)} 0 -1620 0 0 0.4 0.4 {}
T {x = NOT in: N1 (1u/0.45u, gate in) pulls x low. The leaker PL10 ... PL1 (10 x 0.3u/20u in series, gates on in)} 40 -1570 0 0 0.25 0.25 {}
T {pulls x high while in = 0 (full gate drive) and is 2 ... 5 x weaker than N1 while in = 1.2 V.} 40 -1548 0 0 0.25 0.25 {}
T {PF (0.3u/5u, gate y) latches x high once y is low: hysteresis, and it holds x against the leakage of N1.} 40 -1526 0 0 0.25 0.25 {}
T {y = NOT x = in at 3.3 V (XI1), out_b = NOT y (XI2), out = NOT out_b (XI3).} 40 -1504 0 0 0.25 0.25 {}
T {in: a valid 1.2 V level from an always-on rail (the harness enable, dig_in), also while the slot vdd_1v2 is off.} 40 -1482 0 0 0.25 0.25 {}
T {Static current only while in = 1: the leaker, 28 ... 92 nA. vddh / vss: 3.3 V rail of the circuit using the shifter.} 40 -1460 0 0 0.25 0.25 {}
T {Source: netlist/source/en_ctrl_3v3.spice} 40 -1438 0 0 0.25 0.25 {}
N 60 -1340 1060 -1340 {lab=vddh}
N 60 -100 1040 -100 {lab=vss}
N 400 -1270 400 -1340 {lab=vddh}
N 400 -370 400 -410 {lab=l1}
N 400 -470 400 -510 {lab=l2}
N 400 -570 400 -610 {lab=l3}
N 400 -670 400 -710 {lab=l4}
N 400 -770 400 -810 {lab=l5}
N 400 -870 400 -910 {lab=l6}
N 400 -970 400 -1010 {lab=l7}
N 400 -1070 400 -1110 {lab=l8}
N 400 -1170 400 -1210 {lab=l9}
N 400 -310 400 -280 {lab=x}
N 400 -230 400 -280 {lab=x}
N 400 -170 400 -100 {lab=vss}
N 400 -340 420 -340 {lab=vddh}
N 400 -440 420 -440 {lab=vddh}
N 400 -540 420 -540 {lab=vddh}
N 400 -640 420 -640 {lab=vddh}
N 400 -740 420 -740 {lab=vddh}
N 400 -840 420 -840 {lab=vddh}
N 400 -940 420 -940 {lab=vddh}
N 400 -1040 420 -1040 {lab=vddh}
N 400 -1140 420 -1140 {lab=vddh}
N 400 -1240 420 -1240 {lab=vddh}
N 420 -1340 420 -340 {lab=vddh}
N 400 -200 420 -200 {lab=vss}
N 420 -200 420 -100 {lab=vss}
N 360 -340 340 -340 {lab=in}
N 360 -440 340 -440 {lab=in}
N 360 -540 340 -540 {lab=in}
N 360 -640 340 -640 {lab=in}
N 360 -740 340 -740 {lab=in}
N 360 -840 340 -840 {lab=in}
N 360 -940 340 -940 {lab=in}
N 360 -1040 340 -1040 {lab=in}
N 360 -1140 340 -1140 {lab=in}
N 360 -1240 340 -1240 {lab=in}
N 340 -1240 340 -200 {lab=in}
N 60 -200 360 -200 {lab=in}
N 400 -280 680 -280 {lab=x}
N 580 -330 580 -280 {lab=x}
N 580 -390 580 -1340 {lab=vddh}
N 580 -360 560 -360 {lab=vddh}
N 560 -360 560 -1340 {lab=vddh}
N 620 -360 800 -360 {lab=y}
N 800 -360 800 -280 {lab=y}
N 760 -280 840 -280 {lab=y}
N 920 -280 1000 -280 {lab=out_b}
N 1080 -280 1160 -280 {lab=out}
N 960 -280 960 -200 {lab=out_b}
N 960 -200 1160 -200 {lab=out_b}
N 740 -300 740 -1340 {lab=vddh}
N 720 -260 720 -100 {lab=vss}
N 900 -300 900 -1340 {lab=vddh}
N 880 -260 880 -100 {lab=vss}
N 1060 -300 1060 -1340 {lab=vddh}
N 1040 -260 1040 -100 {lab=vss}
C {devices/iopin.sym} 60 -1340 0 1 {name=p0 lab=vddh}
C {devices/iopin.sym} 60 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 60 -200 0 0 {name=p2 lab=in}
C {devices/opin.sym} 1160 -280 0 0 {name=p3 lab=out}
C {devices/opin.sym} 1160 -200 0 0 {name=p4 lab=out_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 380 -200 0 0 {name=N1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -1240 0 0 {name=PL10
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -1140 0 0 {name=PL9
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -1040 0 0 {name=PL8
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -940 0 0 {name=PL7
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -840 0 0 {name=PL6
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -740 0 0 {name=PL5
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -640 0 0 {name=PL4
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -540 0 0 {name=PL3
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -440 0 0 {name=PL2
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -340 0 0 {name=PL1
l=20u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -360 0 1 {name=PF
l=5u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {inv_hv.sym} 720 -280 0 0 {name=XI1}
C {inv_hv.sym} 880 -280 0 0 {name=XI2}
C {inv_hv.sym} 1040 -280 0 0 {name=XI3}
C {devices/lab_wire.sym} 400 -380 0 0 {name=ll1 sig_type=std_logic lab=l1}
C {devices/lab_wire.sym} 400 -480 0 0 {name=ll2 sig_type=std_logic lab=l2}
C {devices/lab_wire.sym} 400 -580 0 0 {name=ll3 sig_type=std_logic lab=l3}
C {devices/lab_wire.sym} 400 -680 0 0 {name=ll4 sig_type=std_logic lab=l4}
C {devices/lab_wire.sym} 400 -780 0 0 {name=ll5 sig_type=std_logic lab=l5}
C {devices/lab_wire.sym} 400 -880 0 0 {name=ll6 sig_type=std_logic lab=l6}
C {devices/lab_wire.sym} 400 -980 0 0 {name=ll7 sig_type=std_logic lab=l7}
C {devices/lab_wire.sym} 400 -1080 0 0 {name=ll8 sig_type=std_logic lab=l8}
C {devices/lab_wire.sym} 400 -1180 0 0 {name=ll9 sig_type=std_logic lab=l9}
C {devices/lab_wire.sym} 500 -280 0 0 {name=lx sig_type=std_logic lab=x}
C {devices/lab_wire.sym} 700 -360 0 0 {name=ly sig_type=std_logic lab=y}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
