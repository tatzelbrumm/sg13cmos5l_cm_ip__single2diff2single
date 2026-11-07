v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 445 -950 835 -950 835 -140 445 -140 445 -950 {dash=6}
P 10 5 845 -595 1555 -595 1555 -430 845 -430 845 -595 {dash=6}
P 10 5 1030 -270 1150 -270 1150 -140 1030 -140 1030 -270 {dash=6}
P 10 5 1205 -270 1435 -270 1435 -140 1205 -140 1205 -270 {dash=6}
P 10 5 900 -270 1020 -270 1020 -140 900 -140 900 -270 {dash=6}
P 10 5 130 -760 430 -760 430 -140 130 -140 130 -760 {dash=6}
T {vref_s2d_rb: replica bias for the pad reference vref of the S2D pad} 100 -1544 0 0 0.6 0.6 {}
T {vref_s2d_rb: replica bias for the pad reference vref of sg13cmos5l_IOPadSingle2Diff (user's choice 1a: about 0.5 V, so} 100 -1474 0 0 0.25 0.25 {}
T {that the pad range 0 ... 1 V includes iovss). Task docs/launch/replica_bias_TASK.md (branch harness-test); evidence} 100 -1452 0 0 0.25 0.25 {}
T {docs/replica_bias/SURVEY.md and the G4 runs (macros/vcm_rb/testbenches/pad_char/results/g4_s2d_vref.tsv).} 100 -1430 0 0 0.25 0.25 {}
T {} 100 -1408 0 0 0.25 0.25 {}
T {The S2D input stays linear (INL <= 2 mV, u = +-0.5 V) for vref above an edge set by the input follower (hv PMOS 20u/1u)} 100 -1386 0 0 0.25 0.25 {}
T {leaving saturation against the fold node x: edge = x - V_SG(follower, 5 uA) + 0.676 V (+-4 mV over corners and iovdd at} 100 -1364 0 0 0.25 0.25 {}
T {125 C). It is below 0.4 V up to 27 C and 0.46 ... 0.54 V at 125 C (fast PMOS highest).} 100 -1342 0 0 0.25 0.25 {}
T {vref = vbnc - V_GS(F): an x-node replica at a lower current density (F = 4 fingers of the fold cascode, 15u/3u, at} 100 -1320 0 0 0.25 0.25 {}
T {1.67 uA, against the S2D's 30u/3u at 10 uA), so it rises with temperature like x (+0.3 mV/K) and sits 0.10 V above it:} 100 -1298 0 0 0.25 0.25 {}
T {about 0.49 V at 27 C (pad range from 0 V), 0.44 V at -40 C, and >= 20 mV above the INL edge at 125 C} 100 -1276 0 0 0.25 0.25 {}
T {(explore_vref.py). Output impedance about 1/gm(F) = 20 kOhm; CB1 / CB2 (2 x 12u x 12u hv NMOS to vss) hold the pin} 100 -1254 0 0 0.25 0.25 {}
T {during the pad's own transients (G6: steps and enable).} 100 -1232 0 0 0.25 0.25 {}
T {Lines as vcm_rb: NI (6u/6u NMOS diode, the 5 uA reference), BP (2u/6u at 2 uA from NBP 2.4u/6u), BNC (1u/8u at 2 uA} 100 -1210 0 0 0.25 0.25 {}
T {from PBNC 2u/6u). Supply current (tt 27 C): 5 + 2 + 2 + 1.67 = about 10.7 uA.} 100 -1188 0 0 0.25 0.25 {}
T {Ports: vdd vss iref vref en_3v3 en_3v3_b. iref: 5 uA SOURCED into the block.} 100 -1166 0 0 0.25 0.25 {}
T {Disabled (en_3v3 = 0): TGN / TGP open the reference, TDN pulls ni to vss, BP pulls vbp to vdd: no current; SPD pulls} 100 -1144 0 0 0.25 0.25 {}
T {vref to vss (the s2d pad's vref drives gates only).} 100 -1122 0 0 0.25 0.25 {}
T {drawn from netlist/source/vref_s2d_rb.spice; make check-sheet netlists this sheet and compares it with that netlist device by device} 100 -1090 0 0 0.25 0.25 {}
T {[3] x-node replica} 1464 -618.5 0 0 0.35 0.35 {layer=10}
T {[3]} 1045 -293.5 0 0 0.35 0.35 {layer=10}
T {[3]} 1205 -293.5 0 0 0.35 0.35 {layer=10}
T {[4] disable} 815 -293.5 0 0 0.35 0.35 {layer=10}
T {[1] reference input} 135 -783.5 0 0 0.35 0.35 {layer=10}
T {[2] lines} 545 -973.5 0 0 0.35 0.35 {layer=10}
N 1100 -460 1100 -250 {lab=vref}
N 1020 -520 1060 -520 {lab=vbnc}
N 1380 -520 1420 -520 {lab=vbnc}
N 1020 -630 1380 -630 {lab=vbnc}
N 1460 -520 1480 -520 {lab=vss}
N 1100 -520 1120 -520 {lab=vss}
N 980 -460 980 -250 {lab=vref}
N 1000 -220 1000 -100 {lab=vss}
N 1260 -460 1300 -460 {lab=vref}
N 980 -520 1020 -520 {lab=vbnc}
N 1340 -520 1380 -520 {lab=vbnc}
N 980 -100 1000 -100 {lab=vss}
N 1120 -520 1300 -520 {lab=vss}
N 1380 -460 1460 -460 {lab=vref}
N 340 -720 340 -670 {lab=iref}
N 220 -720 220 -550 {lab=iref}
N 340 -320 340 -300 {lab=ni}
N 340 -300 340 -250 {lab=ni}
N 400 -300 400 -220 {lab=ni}
N 220 -320 340 -320 {lab=ni}
N 320 -220 340 -220 {lab=vss}
N 220 -220 240 -220 {lab=vss}
N 220 -490 220 -320 {lab=ni}
N 340 -610 340 -320 {lab=ni}
N 240 -520 240 -220 {lab=vss}
N 220 -320 220 -250 {lab=ni}
N 380 -220 400 -220 {lab=ni}
N 160 -220 180 -220 {lab=en_3v3_b}
N 160 -360 160 -220 {lab=en_3v3_b}
N 220 -190 220 -100 {lab=vss}
N 340 -190 340 -100 {lab=vss}
N 320 -220 320 -100 {lab=vss}
N 240 -220 240 -100 {lab=vss}
N 220 -100 240 -100 {lab=vss}
N 340 -300 400 -300 {lab=ni}
N 320 -100 340 -100 {lab=vss}
N 240 -100 320 -100 {lab=vss}
N 340 -100 540 -100 {lab=vss}
N 220 -720 340 -720 {lab=iref}
N 640 -900 700 -900 {lab=vbp}
N 640 -900 640 -800 {lab=vbp}
N 520 -1000 520 -900 {lab=vdd}
N 760 -1000 760 -900 {lab=vdd}
N 540 -870 540 -800 {lab=vbp}
N 560 -220 560 -100 {lab=vss}
N 740 -630 800 -630 {lab=vbnc}
N 720 -220 720 -100 {lab=vss}
N 580 -900 640 -900 {lab=vbp}
N 540 -800 640 -800 {lab=vbp}
N 740 -1000 760 -1000 {lab=vdd}
N 720 -220 740 -220 {lab=vss}
N 740 -190 740 -100 {lab=vss}
N 720 -100 740 -100 {lab=vss}
N 540 -220 560 -220 {lab=vss}
N 540 -190 540 -100 {lab=vss}
N 740 -900 760 -900 {lab=vdd}
N 740 -1000 740 -930 {lab=vdd}
N 520 -900 540 -900 {lab=vdd}
N 540 -1000 540 -930 {lab=vdd}
N 520 -1000 540 -1000 {lab=vdd}
N 780 -220 800 -220 {lab=vbnc}
N 540 -100 560 -100 {lab=vss}
N 560 -100 720 -100 {lab=vss}
N 1100 -100 1120 -100 {lab=vss}
N 740 -100 920 -100 {lab=vss}
N 480 -220 500 -220 {lab=ni}
N 480 -300 480 -220 {lab=ni}
N 1300 -1000 1460 -1000 {lab=vdd}
N 360 -1000 520 -1000 {lab=vdd}
N 540 -1000 740 -1000 {lab=vdd}
N 800 -630 1020 -630 {lab=vbnc}
N 800 -630 800 -220 {lab=vbnc}
N 920 -520 940 -520 {lab=vss}
N 1100 -220 1120 -220 {lab=vss}
N 1100 -190 1100 -100 {lab=vss}
N 1040 -220 1060 -220 {lab=ni}
N 980 -460 1100 -460 {lab=vref}
N 1000 -100 1100 -100 {lab=vss}
N 1120 -220 1120 -100 {lab=vss}
N 1020 -630 1020 -520 {lab=vbnc}
N 1380 -630 1380 -520 {lab=vbnc}
N 1120 -520 1120 -220 {lab=vss}
N 1100 -490 1100 -460 {lab=vref}
N 1300 -490 1300 -460 {lab=vref}
N 1480 -520 1480 -100 {lab=vss}
N 1460 -490 1460 -460 {lab=vref}
N 920 -520 920 -100 {lab=vss}
N 940 -490 940 -460 {lab=vref}
N 980 -220 1000 -220 {lab=vss}
N 980 -190 980 -100 {lab=vss}
N 920 -100 980 -100 {lab=vss}
N 1420 -100 1480 -100 {lab=vss}
N 940 -460 980 -460 {lab=vref}
N 880 -220 940 -220 {lab=en_3v3_b}
N 1040 -300 1040 -220 {lab=ni}
N 480 -300 1040 -300 {lab=ni}
N 400 -300 480 -300 {lab=ni}
N 1380 -460 1380 -240 {lab=vref}
N 1300 -460 1380 -460 {lab=vref}
N 1260 -460 1260 -240 {lab=vref}
N 1100 -460 1260 -460 {lab=vref}
N 1260 -200 1260 -100 {lab=vss}
N 1220 -100 1260 -100 {lab=vss}
N 1380 -200 1380 -100 {lab=vss}
N 1340 -100 1380 -100 {lab=vss}
N 1220 -200 1230 -200 {lab=vss}
N 1220 -200 1220 -100 {lab=vss}
N 1120 -100 1220 -100 {lab=vss}
N 1290 -200 1300 -200 {lab=vss}
N 1300 -200 1300 -100 {lab=vss}
N 1260 -100 1300 -100 {lab=vss}
N 1340 -200 1350 -200 {lab=vss}
N 1340 -200 1340 -100 {lab=vss}
N 1300 -100 1340 -100 {lab=vss}
N 1410 -200 1420 -200 {lab=vss}
N 1420 -200 1420 -100 {lab=vss}
N 1380 -100 1420 -100 {lab=vss}
N 1460 -460 1600 -460 {lab=vref}
N 360 -1000 360 -640 {lab=vdd}
N 1460 -1000 1460 -550 {lab=vdd}
N 1300 -1000 1300 -550 {lab=vdd}
N 1100 -1000 1300 -1000 {lab=vdd}
N 1100 -1000 1100 -550 {lab=vdd}
N 940 -1000 1100 -1000 {lab=vdd}
N 940 -1000 940 -550 {lab=vdd}
N 760 -1000 940 -1000 {lab=vdd}
N 740 -630 740 -250 {lab=vbnc}
N 740 -870 740 -630 {lab=vbnc}
N 540 -800 540 -250 {lab=vbp}
N 100 -720 220 -720 {lab=iref}
N 100 -100 220 -100 {lab=vss}
N 100 -1000 360 -1000 {lab=vdd}
N 210 -520 240 -520 {lab=vss}
N 100 -520 180 -520 {lab=en_3v3}
N 160 -640 300 -640 {lab=en_3v3_b}
N 100 -640 160 -640 {lab=en_3v3_b}
N 340 -640 360 -640 {lab=vdd}
N 880 -360 880 -220 {lab=en_3v3_b}
N 160 -360 880 -360 {lab=en_3v3_b}
N 160 -640 160 -360 {lab=en_3v3_b}
C {devices/iopin.sym} 100 -1000 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -720 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 1600 -460 0 0 {name=p3 lab=vref}
C {devices/ipin.sym} 100 -520 0 0 {name=p4 lab=en_3v3}
C {devices/ipin.sym} 100 -640 0 0 {name=p5 lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 960 -520 0 1 {name=F1
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1080 -520 0 0 {name=F2
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1320 -520 0 1 {name=F3
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1440 -520 0 0 {name=F4
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1080 -220 0 0 {name=SF
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1260 -220 1 0 {name=CB1
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1380 -220 1 0 {name=CB2
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 960 -220 0 0 {name=SPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_wire.sym} 900 -630 0 0 {name=l3 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1000 -460 0 0 {name=l4 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 880 -360 0 1 {name=l5 sig_type=std_logic lab=en_3v3_b}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 -520 0 0 {name=TGN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 320 -640 0 0 {name=TGP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 -220 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 360 -220 0 1 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 160 -220 0 0 {name=l1 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_wire.sym} 420 -300 0 0 {name=l11 sig_type=std_logic lab=ni}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 520 -220 0 0 {name=NBP
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -900 0 1 {name=BP
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 720 -900 0 0 {name=PBNC
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 760 -220 0 1 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_wire.sym} 1380 -630 0 1 {name=l2 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 740 -630 0 0 {name=l6 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 640 -800 0 1 {name=l12 sig_type=std_logic lab=vbp}
