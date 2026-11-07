v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 170 -740 620 -740 620 -120 170 -120 170 -740 {dash=6}
P 10 5 645 -1190 1035 -1190 1035 -120 645 -120 645 -1190 {dash=6}
P 10 5 1045 -785 1755 -785 1755 -620 1045 -620 1045 -785 {dash=6}
P 10 5 1180 -250 1330 -250 1330 -120 1180 -120 1180 -250 {dash=6}
P 10 5 1705 -250 2035 -250 2035 -120 1705 -120 1705 -250 {dash=6}
P 10 5 2070 -250 2360 -250 2360 -120 2070 -120 2070 -250 {dash=6}
T {vref_s2d_rb: replica bias for the pad reference vref of the S2D pad} 100 -1804 0 0 0.6 0.6 {}
T {vref_s2d_rb: replica bias for the pad reference vref of sg13cmos5l_IOPadSingle2Diff (user's choice 1a: about 0.5 V, so} 100 -1734 0 0 0.25 0.25 {}
T {that the pad range 0 ... 1 V includes iovss). Task docs/launch/replica_bias_TASK.md (branch harness-test); evidence} 100 -1712 0 0 0.25 0.25 {}
T {docs/replica_bias/SURVEY.md and the G4 runs (macros/vcm_rb/testbenches/pad_char/results/g4_s2d_vref.tsv).} 100 -1690 0 0 0.25 0.25 {}
T {} 100 -1668 0 0 0.25 0.25 {}
T {The S2D input stays linear (INL <= 2 mV, u = +-0.5 V) for vref above an edge set by the input follower (hv PMOS 20u/1u)} 100 -1646 0 0 0.25 0.25 {}
T {leaving saturation against the fold node x: edge = x - V_SG(follower, 5 uA) + 0.676 V (+-4 mV over corners and iovdd at} 100 -1624 0 0 0.25 0.25 {}
T {125 C). It is below 0.4 V up to 27 C and 0.46 ... 0.54 V at 125 C (fast PMOS highest).} 100 -1602 0 0 0.25 0.25 {}
T {vref = vbnc - V_GS(F): an x-node replica at a lower current density (F = 4 fingers of the fold cascode, 15u/3u, at} 100 -1580 0 0 0.25 0.25 {}
T {1.67 uA, against the S2D's 30u/3u at 10 uA), so it rises with temperature like x (+0.3 mV/K) and sits 0.10 V above it:} 100 -1558 0 0 0.25 0.25 {}
T {about 0.49 V at 27 C (pad range from 0 V), 0.44 V at -40 C, and >= 20 mV above the INL edge at 125 C} 100 -1536 0 0 0.25 0.25 {}
T {(explore_vref.py). Output impedance about 1/gm(F) = 20 kOhm; CB1 / CB2 (2 x 12u x 12u hv NMOS to vss) hold the pin} 100 -1514 0 0 0.25 0.25 {}
T {during the pad's own transients (G6: steps and enable).} 100 -1492 0 0 0.25 0.25 {}
T {Lines as vcm_rb: NI (6u/6u NMOS diode, the 5 uA reference), BP (2u/6u at 2 uA from NBP 2.4u/6u), BNC (1u/8u at 2 uA} 100 -1470 0 0 0.25 0.25 {}
T {from PBNC 2u/6u). Supply current (tt 27 C): 5 + 2 + 2 + 1.67 = about 10.7 uA.} 100 -1448 0 0 0.25 0.25 {}
T {Ports: vdd vss iref vref en_3v3 en_3v3_b. iref: 5 uA SOURCED into the block.} 100 -1426 0 0 0.25 0.25 {}
T {Disabled (en_3v3 = 0): TGN / TGP open the reference, TDN pulls ni to vss, BP pulls vbp to vdd: no current; SPD pulls} 100 -1404 0 0 0.25 0.25 {}
T {vref to vss (the s2d pad's vref drives gates only).} 100 -1382 0 0 0.25 0.25 {}
T {drawn from netlist/source/vref_s2d_rb.spice; make check-sheet netlists this sheet and compares it with that netlist device by device} 100 -1350 0 0 0.25 0.25 {}
T {[1] reference input} 175 -763.5 0 0 0.35 0.35 {layer=10}
T {[2] lines} 745 -1213.5 0 0 0.35 0.35 {layer=10}
T {[3] x-node replica} 1664 -808.5 0 0 0.35 0.35 {layer=10}
T {[3]} 1245 -273.5 0 0 0.35 0.35 {layer=10}
T {[3]} 1745 -273.5 0 0 0.35 0.35 {layer=10}
T {[4] disable} 2075 -273.5 0 0 0.35 0.35 {layer=10}
N 100 -700 380 -700 {lab=iref}
N 380 -700 380 -650 {lab=iref}
N 260 -530 260 -700 {lab=iref}
N 100 -620 340 -620 {lab=en_3v3_b}
N 100 -500 220 -500 {lab=en_3v3}
N 380 -620 390 -620 {lab=vdd}
N 390 -620 390 -660 {lab=vdd}
N 390 -660 410 -660 {lab=vdd}
N 410 -660 410 -1240 {lab=vdd}
N 260 -500 270 -500 {lab=vss}
N 270 -500 270 -460 {lab=vss}
N 270 -460 290 -460 {lab=vss}
N 290 -460 290 -80 {lab=vss}
N 260 -470 260 -320 {lab=ni}
N 380 -590 380 -320 {lab=ni}
N 380 -320 380 -230 {lab=ni}
N 340 -200 340 -320 {lab=ni}
N 380 -200 380 -170 {lab=vss}
N 380 -170 380 -80 {lab=vss}
N 520 -230 520 -320 {lab=ni}
N 520 -200 520 -170 {lab=vss}
N 520 -170 520 -80 {lab=vss}
N 480 -200 480 -150 {lab=en_3v3_b}
N 780 -1140 900 -1140 {lab=vbp}
N 840 -1140 840 -1040 {lab=vbp}
N 740 -1140 740 -1170 {lab=vdd}
N 740 -1170 740 -1240 {lab=vdd}
N 940 -1140 940 -1170 {lab=vdd}
N 940 -1170 940 -1240 {lab=vdd}
N 740 -1110 740 -1040 {lab=vbp}
N 740 -1040 740 -230 {lab=vbp}
N 740 -1040 840 -1040 {lab=vbp}
N 700 -200 700 -320 {lab=ni}
N 740 -200 740 -170 {lab=vss}
N 740 -170 740 -80 {lab=vss}
N 940 -1110 940 -230 {lab=vbnc}
N 980 -200 980 -260 {lab=vbnc}
N 980 -260 940 -260 {lab=vbnc}
N 940 -200 940 -170 {lab=vss}
N 940 -170 940 -80 {lab=vss}
N 1140 -750 1140 -1240 {lab=vdd}
N 1140 -690 1140 -650 {lab=vref}
N 1300 -750 1300 -1240 {lab=vdd}
N 1300 -690 1300 -650 {lab=vref}
N 1500 -750 1500 -1240 {lab=vdd}
N 1500 -690 1500 -650 {lab=vref}
N 1660 -750 1660 -1240 {lab=vdd}
N 1660 -690 1660 -650 {lab=vref}
N 1180 -720 1260 -720 {lab=vbnc}
N 1540 -720 1620 -720 {lab=vbnc}
N 1220 -720 1220 -820 {lab=vbnc}
N 1580 -720 1580 -820 {lab=vbnc}
N 940 -820 1580 -820 {lab=vbnc}
N 1140 -650 1660 -650 {lab=vref}
N 1140 -720 1130 -720 {lab=vss}
N 1130 -720 1130 -680 {lab=vss}
N 1130 -680 1110 -680 {lab=vss}
N 1110 -680 1110 -80 {lab=vss}
N 1660 -720 1670 -720 {lab=vss}
N 1670 -720 1670 -680 {lab=vss}
N 1670 -680 1690 -680 {lab=vss}
N 1690 -680 1690 -80 {lab=vss}
N 1300 -720 1310 -720 {lab=vss}
N 1310 -720 1310 -680 {lab=vss}
N 1310 -680 1490 -680 {lab=vss}
N 1490 -680 1490 -720 {lab=vss}
N 1490 -720 1500 -720 {lab=vss}
N 1400 -680 1400 -80 {lab=vss}
N 1240 -230 1240 -650 {lab=vref}
N 1200 -200 1200 -320 {lab=ni}
N 1240 -200 1240 -170 {lab=vss}
N 1240 -170 1240 -80 {lab=vss}
N 1580 -650 1580 -440 {lab=vref}
N 1580 -440 2340 -440 {lab=vref}
N 1740 -200 1740 -440 {lab=vref}
N 1780 -230 1780 -170 {lab=vss}
N 1780 -170 1780 -80 {lab=vss}
N 1900 -200 1900 -440 {lab=vref}
N 1940 -230 1940 -170 {lab=vss}
N 1940 -170 1940 -80 {lab=vss}
N 2240 -230 2240 -440 {lab=vref}
N 2240 -200 2240 -170 {lab=vss}
N 2240 -170 2240 -80 {lab=vss}
N 2200 -200 2170 -200 {lab=en_3v3_b}
N 700 -320 260 -320 {lab=ni}
N 700 -320 1200 -320 {lab=ni}
N 100 -1240 1660 -1240 {lab=vdd}
N 100 -80 2240 -80 {lab=vss}
C {devices/iopin.sym} 100 -1240 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -80 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -700 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 2340 -440 0 0 {name=p3 lab=vref}
C {devices/ipin.sym} 100 -500 0 0 {name=p4 lab=en_3v3}
C {devices/ipin.sym} 100 -620 0 0 {name=p5 lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 240 -500 0 0 {name=TGN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 360 -620 2 1 {name=TGP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 500 -200 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 360 -200 0 0 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 720 -200 0 0 {name=NBP
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -1140 0 1 {name=BP
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 -1140 0 0 {name=PBNC
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 960 -200 0 1 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1160 -720 0 1 {name=F1
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 -720 0 0 {name=F2
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1520 -720 0 1 {name=F3
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1640 -720 0 0 {name=F4
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1220 -200 0 0 {name=SF
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1760 -200 0 0 {name=CB1
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1920 -200 0 0 {name=CB2
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2220 -200 0 0 {name=SPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 480 -150 0 0 {name=l1 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_wire.sym} 820 -1040 0 0 {name=l2 sig_type=std_logic lab=vbp}
C {devices/lab_wire.sym} 1100 -820 0 0 {name=l3 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1200 -650 0 0 {name=l4 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 2170 -200 0 0 {name=l5 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_wire.sym} 460 -320 0 0 {name=l6 sig_type=std_logic lab=ni}
C {devices/lab_wire.sym} 940 -700 0 1 {name=l7 sig_type=std_logic lab=vbnc}
C {devices/title.sym} 160 40 0 0 {name=l0 author="Christoph Maier"}
