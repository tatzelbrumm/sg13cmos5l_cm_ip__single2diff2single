v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 170 -740 620 -740 620 -120 170 -120 170 -740 {dash=6}
P 10 5 645 -1190 1035 -1190 1035 -120 645 -120 645 -1190 {dash=6}
P 10 5 1080 -1190 1240 -1190 1240 -890 1080 -890 1080 -1190 {dash=6}
P 10 5 1045 -400 1415 -400 1415 -120 1045 -120 1045 -400 {dash=6}
P 10 5 1200 -845 1595 -845 1595 -470 1200 -470 1200 -845 {dash=6}
P 10 5 1605 -640 1955 -640 1955 -515 1605 -515 1605 -640 {dash=6}
P 10 5 1680 -250 1830 -250 1830 -120 1680 -120 1680 -250 {dash=6}
P 10 5 1970 -1190 2535 -1190 2535 -120 1970 -120 1970 -1190 {dash=6}
P 10 5 2545 -250 2820 -250 2820 -120 2545 -120 2545 -250 {dash=6}
T {vcm_rb: replica bias for the pads' internal common mode (S2D vcm = D2S vref)} 100 -2024 0 0 0.6 0.6 {}
T {vcm_rb: replica bias for the internal common mode of the custom pads: S2D vcm = D2S vref (= D2S input common mode).} 100 -1954 0 0 0.25 0.25 {}
T {Task docs/launch/replica_bias_TASK.md (branch harness-test); targets and evidence docs/replica_bias/SURVEY.md, design} 100 -1932 0 0 0.25 0.25 {}
T {notes on the notes branch (sudelbuecher/design_considerations/replica_bias/).} 100 -1910 0 0 0.25 0.25 {}
T {} 100 -1888 0 0 0.25 0.25 {}
T {vcm sits at the centre of the band in which both pads stay linear (INL <= 2 mV with +-0.5 V on the unit gates):} 100 -1866 0 0 0.25 0.25 {}
T {top    edge = the gate voltage at which a unit_r2 tail (hv PMOS 5u/6u at vbp, 5 uA) leaves saturation as the input} 100 -1844 0 0 0.25 0.25 {}
T {follower (hv PMOS 20u/1u ng=2) raises its source;} 100 -1822 0 0 0.25 0.25 {}
T {bottom edge = the output voltage at which the S2D fold cascode CX / CY (hv NMOS 30u/3u at vbnc) leaves saturation} 100 -1800 0 0 0.25 0.25 {}
T {above the fold node x.} 100 -1778 0 0 0.25 0.25 {}
T {Replicas, each from the block's own lines (made from one 5 uA reference current, as bias_tree_pd does):} 100 -1756 0 0 0.25 0.25 {}
T {gh = top-edge detector: TR (5u/6u at vbp) -> MR (20u/1u ng=2, diode) -> sink SH (2 x 2.4u/6u = 4 uA, r = 0.8)} 100 -1734 0 0 0.25 0.25 {}
T {gh = top gate limit + 0.157 V (+-18 mV over corners, -40..125 C, iovdd 3.0..3.6 V, run explore_edges.py)} 100 -1712 0 0 0.25 0.25 {}
T {xp = fold-node replica: one finger of CY (15u/3u at vbnc) at 5 uA on SY (6u/6u)} 100 -1690 0 0 0.25 0.25 {}
T {bottom edge = xp + 0.559 V (+-34 mV)} 100 -1668 0 0 0.25 0.25 {}
T {m  = average of gh and xp by three identical hv PMOS diodes 1u/4u in their own wells, one above m, two in parallel} 100 -1646 0 0 0.25 0.25 {}
T {below (the asymmetry subtracts the 0.06 V offset of (gh + xp)/2 against the centre; explore_vcm_rb.py, G)} 100 -1624 0 0 0.25 0.25 {}
T {vcm = m, buffered by a 5-transistor OTA in unity gain: PMOS pair = the unit's input device (20u/1u ng=2) on a} 100 -1602 0 0 0.25 0.25 {}
T {unit tail (5u/6u at vbp, 5 uA), NMOS mirror 6u/6u; output pole at vcm with CB (12u x 12u hv NMOS capacitor} 100 -1580 0 0 0.25 0.25 {}
T {as the s2d buffer's CLP).} 100 -1558 0 0 0.25 0.25 {}
T {Lines: NI (6u/6u NMOS diode, the reference), BP (2u/6u PMOS diode at 2 uA from NBP 2.4u/6u = BP's density in the} 100 -1536 0 0 0.25 0.25 {}
T {tree), BNC (1u/8u NMOS diode at 2 uA from PBNC 2u/6u, as in the tree).} 100 -1514 0 0 0.25 0.25 {}
T {Supply current (tt 27 C): 5 uA reference + 2 (BP) + 2 (BNC) + 5 (TR) + 5 (CY) + 5 (OTA) = about 24 uA.} 100 -1492 0 0 0.25 0.25 {}
T {Ports: vdd vss iref vcm en_3v3 en_3v3_b (as oa_core_pd: en_3v3_b from en_ctrl_3v3). iref: 5 uA SOURCED into the} 100 -1470 0 0 0.25 0.25 {}
T {block (bias_gen_pd's iref, a bias_dist_pd output, or a core's iout).} 100 -1448 0 0 0.25 0.25 {}
T {Disabled (en_3v3 = 0): TGN / TGP open the reference, TDN pulls ni to vss (every NMOS off; BP pulls vbp to vdd, every} 100 -1426 0 0 0.25 0.25 {}
T {PMOS off), SPD pulls vcm to vss. The s2d pad ties its outputs to vcm while it is off; whoever disables this block} 100 -1404 0 0 0.25 0.25 {}
T {must disable every pad that uses vcm with it (vcm is the next stage's common mode while only the s2d pad is off).} 100 -1382 0 0 0.25 0.25 {}
T {drawn from netlist/source/vcm_rb.spice; make check-sheet netlists this sheet and compares it with that netlist device by device} 100 -1350 0 0 0.25 0.25 {}
T {[1] reference input} 175 -763.5 0 0 0.35 0.35 {layer=10}
T {[2] lines} 745 -1213.5 0 0 0.35 0.35 {layer=10}
T {[3] top-edge detector} 1145 -1213.5 0 0 0.35 0.35 {layer=10}
T {[3]} 1050 -423.5 0 0 0.35 0.35 {layer=10}
T {[5] average} 1205 -868.5 0 0 0.35 0.35 {layer=10}
T {[4] fold-node replica} 1610 -663.5 0 0 0.35 0.35 {layer=10}
T {[4]} 1745 -273.5 0 0 0.35 0.35 {layer=10}
T {[6] unity-gain buffer} 2165 -1213.5 0 0 0.35 0.35 {layer=10}
T {[7] disable} 2550 -273.5 0 0 0.35 0.35 {layer=10}
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
N 700 -200 700 -320 {lab=ni}
N 740 -200 740 -170 {lab=vss}
N 740 -170 740 -80 {lab=vss}
N 940 -1110 940 -230 {lab=vbnc}
N 980 -200 980 -260 {lab=vbnc}
N 980 -260 940 -260 {lab=vbnc}
N 940 -200 940 -170 {lab=vss}
N 940 -170 940 -80 {lab=vss}
N 1100 -1140 1100 -1040 {lab=vbp}
N 1140 -1140 1140 -1170 {lab=vdd}
N 1140 -1170 1140 -1240 {lab=vdd}
N 1140 -1110 1140 -970 {lab=ts}
N 1140 -940 1140 -970 {lab=ts}
N 1100 -940 1100 -880 {lab=gh}
N 1100 -880 1140 -880 {lab=gh}
N 1140 -910 1140 -880 {lab=gh}
N 1140 -880 1140 -230 {lab=gh}
N 1180 -200 1280 -200 {lab=ni}
N 1230 -320 1230 -200 {lab=ni}
N 1320 -230 1320 -380 {lab=gh}
N 1320 -380 1140 -380 {lab=gh}
N 1140 -200 1140 -170 {lab=vss}
N 1140 -170 1140 -80 {lab=vss}
N 1320 -200 1320 -170 {lab=vss}
N 1320 -170 1320 -80 {lab=vss}
N 1140 -880 1400 -880 {lab=gh}
N 1400 -880 1400 -810 {lab=gh}
N 1400 -780 1400 -810 {lab=gh}
N 1360 -780 1360 -690 {lab=m}
N 1400 -750 1400 -690 {lab=m}
N 1300 -600 1300 -630 {lab=m}
N 1300 -630 1300 -690 {lab=m}
N 1300 -570 1300 -500 {lab=xp}
N 1340 -600 1340 -500 {lab=xp}
N 1500 -600 1500 -630 {lab=m}
N 1500 -630 1500 -690 {lab=m}
N 1500 -570 1500 -500 {lab=xp}
N 1460 -600 1460 -500 {lab=xp}
N 1860 -610 1860 -1240 {lab=vdd}
N 1820 -580 1790 -580 {lab=vbnc}
N 1860 -550 1860 -500 {lab=xp}
N 1740 -230 1740 -500 {lab=xp}
N 1860 -580 1870 -580 {lab=vss}
N 1870 -580 1870 -540 {lab=vss}
N 1870 -540 1900 -540 {lab=vss}
N 1900 -540 1900 -80 {lab=vss}
N 1700 -200 1700 -320 {lab=ni}
N 1740 -200 1740 -170 {lab=vss}
N 1740 -170 1740 -80 {lab=vss}
N 1300 -500 1860 -500 {lab=xp}
N 1300 -690 2020 -690 {lab=m}
N 2060 -690 2060 -720 {lab=bt}
N 2260 -690 2260 -720 {lab=bt}
N 2060 -720 2060 -780 {lab=bt}
N 2060 -780 2260 -780 {lab=bt}
N 2260 -780 2260 -720 {lab=bt}
N 2160 -1110 2160 -780 {lab=bt}
N 2120 -1140 2120 -1040 {lab=vbp}
N 2160 -1140 2160 -1170 {lab=vdd}
N 2160 -1170 2160 -1240 {lab=vdd}
N 2060 -660 2060 -230 {lab=bd}
N 2100 -200 2220 -200 {lab=bd}
N 2100 -200 2100 -260 {lab=bd}
N 2100 -260 2060 -260 {lab=bd}
N 2060 -200 2060 -170 {lab=vss}
N 2060 -170 2060 -80 {lab=vss}
N 2260 -200 2260 -170 {lab=vss}
N 2260 -170 2260 -80 {lab=vss}
N 2260 -660 2260 -230 {lab=vcm}
N 2300 -690 2300 -440 {lab=vcm}
N 2260 -440 2840 -440 {lab=vcm}
N 2400 -200 2400 -440 {lab=vcm}
N 2440 -230 2440 -170 {lab=vss}
N 2440 -170 2440 -80 {lab=vss}
N 2720 -230 2720 -440 {lab=vcm}
N 2720 -200 2720 -170 {lab=vss}
N 2720 -170 2720 -80 {lab=vss}
N 2680 -200 2650 -200 {lab=en_3v3_b}
N 700 -320 260 -320 {lab=ni}
N 700 -320 1700 -320 {lab=ni}
N 740 -1040 2120 -1040 {lab=vbp}
N 100 -1240 2160 -1240 {lab=vdd}
N 100 -80 2720 -80 {lab=vss}
C {devices/iopin.sym} 100 -1240 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -80 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -700 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 2840 -440 0 0 {name=p3 lab=vcm}
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
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1120 -1140 0 0 {name=TR
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1120 -940 0 0 {name=MR
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1160 -200 0 1 {name=SH1
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1300 -200 0 0 {name=SH2
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1840 -580 0 0 {name=CY
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1720 -200 0 0 {name=SY
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1380 -780 0 0 {name=SU
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1320 -600 0 1 {name=SL1
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1480 -600 0 0 {name=SL2
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2140 -1140 0 0 {name=BT
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2040 -690 0 0 {name=BA
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2280 -690 0 1 {name=BB
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2080 -200 0 1 {name=BD
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2240 -200 0 0 {name=BM
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2420 -200 0 0 {name=CB
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2700 -200 0 0 {name=SPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 480 -150 0 0 {name=l1 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_wire.sym} 940 -700 0 1 {name=l2 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1140 -1000 0 1 {name=l3 sig_type=std_logic lab=ts}
C {devices/lab_wire.sym} 1340 -880 0 0 {name=l4 sig_type=std_logic lab=gh}
C {devices/lab_pin.sym} 1790 -580 0 0 {name=l5 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1560 -500 0 0 {name=l6 sig_type=std_logic lab=xp}
C {devices/lab_wire.sym} 1560 -690 0 0 {name=l7 sig_type=std_logic lab=m}
C {devices/lab_wire.sym} 2120 -780 0 0 {name=l8 sig_type=std_logic lab=bt}
C {devices/lab_wire.sym} 2060 -400 0 1 {name=l9 sig_type=std_logic lab=bd}
C {devices/lab_pin.sym} 2650 -200 0 0 {name=l10 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_wire.sym} 460 -320 0 0 {name=l11 sig_type=std_logic lab=ni}
C {devices/lab_wire.sym} 890 -1040 0 0 {name=l12 sig_type=std_logic lab=vbp}
C {devices/title.sym} 160 40 0 0 {name=l0 author="Christoph Maier"}
