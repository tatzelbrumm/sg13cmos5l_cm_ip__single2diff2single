v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 170 -740 470 -740 470 -120 170 -120 170 -740 {dash=6}
P 10 5 485 -1190 875 -1190 875 -120 485 -120 485 -1190 {dash=6}
P 10 5 1100 -1190 1260 -1190 1260 -890 1100 -890 1100 -1190 {dash=6}
P 10 5 1125 -380 1395 -380 1395 -120 1125 -120 1125 -380 {dash=6}
P 10 5 1240 -845 1635 -845 1635 -470 1240 -470 1240 -845 {dash=6}
P 10 5 925 -640 1045 -640 1045 -515 925 -515 925 -640 {dash=6}
P 10 5 900 -250 1050 -250 1050 -120 900 -120 900 -250 {dash=6}
P 10 5 1660 -1190 2005 -1190 2005 -120 1660 -120 1660 -1190 {dash=6}
P 10 5 1465 -250 1580 -250 1580 -120 1465 -120 1465 -250 {dash=6}
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
T {[2] lines} 585 -1213.5 0 0 0.35 0.35 {layer=10}
T {[3] top-edge detector} 1105 -1213.5 0 0 0.35 0.35 {layer=10}
T {[3]} 1130 -403.5 0 0 0.35 0.35 {layer=10}
T {[5] average} 1245 -868.5 0 0 0.35 0.35 {layer=10}
T {[4] fold-node replica} 930 -663.5 0 0 0.35 0.35 {layer=10}
T {[4]} 935 -273.5 0 0 0.35 0.35 {layer=10}
T {[6] unity-gain buffer} 1835 -1213.5 0 0 0.35 0.35 {layer=10}
T {[7] disable} 1470 -273.5 0 0 0.35 0.35 {layer=10}
N 260 -700 380 -700 {lab=iref}
N 380 -700 380 -650 {lab=iref}
N 260 -700 260 -530 {lab=iref}
N 200 -620 340 -620 {lab=en_3v3_b}
N 100 -500 220 -500 {lab=en_3v3}
N 380 -620 400 -620 {lab=vdd}
N 400 -1240 400 -620 {lab=vdd}
N 260 -500 280 -500 {lab=vss}
N 280 -200 280 -80 {lab=vss}
N 380 -360 380 -320 {lab=ni}
N 380 -320 380 -230 {lab=ni}
N 440 -320 440 -200 {lab=ni}
N 360 -200 360 -80 {lab=vss}
N 680 -1140 740 -1140 {lab=vbp}
N 680 -1140 680 -1040 {lab=vbp}
N 560 -1240 560 -1140 {lab=vdd}
N 800 -1240 800 -1140 {lab=vdd}
N 580 -1110 580 -1040 {lab=vbp}
N 580 -1040 580 -230 {lab=vbp}
N 520 -320 520 -200 {lab=ni}
N 600 -200 600 -80 {lab=vss}
N 780 -580 840 -580 {lab=vbnc}
N 760 -200 760 -80 {lab=vss}
N 1120 -1140 1120 -1040 {lab=vbp}
N 1200 -1240 1200 -1140 {lab=vdd}
N 1240 -940 1240 -880 {lab=gh}
N 1180 -910 1180 -880 {lab=gh}
N 1180 -360 1180 -230 {lab=gh}
N 1260 -320 1260 -200 {lab=ni}
N 1340 -360 1340 -230 {lab=gh}
N 1160 -200 1160 -80 {lab=vss}
N 1360 -200 1360 -80 {lab=vss}
N 1320 -880 1340 -880 {lab=gh}
N 1320 -880 1320 -780 {lab=gh}
N 1400 -780 1400 -690 {lab=m}
N 1340 -750 1340 -690 {lab=m}
N 1320 -690 1320 -600 {lab=m}
N 1340 -570 1340 -500 {lab=xp}
N 1400 -600 1400 -500 {lab=xp}
N 1560 -690 1560 -600 {lab=m}
N 1540 -570 1540 -500 {lab=xp}
N 1480 -600 1480 -500 {lab=xp}
N 980 -1240 980 -610 {lab=vdd}
N 980 -550 980 -500 {lab=xp}
N 980 -500 980 -230 {lab=xp}
N 980 -580 1000 -580 {lab=vss}
N 1000 -200 1000 -80 {lab=vss}
N 920 -320 920 -200 {lab=ni}
N 1750 -780 1750 -690 {lab=bt}
N 1910 -780 1930 -780 {lab=bt}
N 1910 -780 1910 -690 {lab=bt}
N 1830 -1110 1830 -780 {lab=bt}
N 1770 -1140 1770 -1040 {lab=vbp}
N 1850 -1240 1850 -1140 {lab=vdd}
N 1730 -260 1730 -230 {lab=bd}
N 1830 -200 1890 -200 {lab=bd}
N 1830 -260 1830 -200 {lab=bd}
N 1730 -260 1830 -260 {lab=bd}
N 1730 -200 1730 -80 {lab=vss}
N 1950 -200 1950 -80 {lab=vss}
N 1930 -440 1930 -230 {lab=vcm}
N 1990 -690 1990 -440 {lab=vcm}
N 2070 -340 2070 -200 {lab=vcm}
N 1560 -200 1560 -80 {lab=vss}
N 1480 -200 1500 -200 {lab=en_3v3_b}
N 1830 -1240 1850 -1240 {lab=vdd}
N 100 -700 260 -700 {lab=iref}
N 580 -1240 780 -1240 {lab=vdd}
N 360 -80 380 -80 {lab=vss}
N 260 -360 380 -360 {lab=ni}
N 260 -80 280 -80 {lab=vss}
N 620 -1140 680 -1140 {lab=vbp}
N 580 -1040 680 -1040 {lab=vbp}
N 780 -1240 800 -1240 {lab=vdd}
N 780 -580 780 -230 {lab=vbnc}
N 1180 -1240 1200 -1240 {lab=vdd}
N 1260 -200 1320 -200 {lab=ni}
N 1180 -880 1180 -360 {lab=gh}
N 1340 -690 1400 -690 {lab=m}
N 980 -80 1000 -80 {lab=vss}
N 1750 -780 1830 -780 {lab=bt}
N 1730 -660 1730 -260 {lab=bd}
N 1930 -80 1950 -80 {lab=vss}
N 1930 -440 1990 -440 {lab=vcm}
N 1990 -440 2070 -440 {lab=vcm}
N 1930 -660 1930 -440 {lab=vcm}
N 760 -200 780 -200 {lab=vss}
N 780 -170 780 -80 {lab=vss}
N 760 -80 780 -80 {lab=vss}
N 580 -200 600 -200 {lab=vss}
N 580 -170 580 -80 {lab=vss}
N 360 -200 380 -200 {lab=vss}
N 260 -200 280 -200 {lab=vss}
N 260 -170 260 -80 {lab=vss}
N 280 -80 360 -80 {lab=vss}
N 380 -170 380 -80 {lab=vss}
N 380 -320 440 -320 {lab=ni}
N 260 -470 260 -360 {lab=ni}
N 380 -590 380 -360 {lab=ni}
N 1340 -200 1360 -200 {lab=vss}
N 980 -200 1000 -200 {lab=vss}
N 1930 -200 1950 -200 {lab=vss}
N 2100 -160 2100 -80 {lab=vss}
N 1540 -200 1560 -200 {lab=vss}
N 1540 -170 1540 -80 {lab=vss}
N 1930 -170 1930 -80 {lab=vss}
N 980 -170 980 -80 {lab=vss}
N 1340 -170 1340 -80 {lab=vss}
N 1910 -690 1930 -690 {lab=bt}
N 1830 -780 1910 -780 {lab=bt}
N 1730 -780 1750 -780 {lab=bt}
N 1730 -780 1730 -720 {lab=bt}
N 1930 -780 1930 -720 {lab=bt}
N 780 -1140 800 -1140 {lab=vdd}
N 1180 -1140 1200 -1140 {lab=vdd}
N 1830 -1140 1850 -1140 {lab=vdd}
N 1830 -1240 1830 -1170 {lab=vdd}
N 1180 -1240 1180 -1170 {lab=vdd}
N 780 -1240 780 -1170 {lab=vdd}
N 2070 -160 2070 -80 {lab=vss}
N 2070 -80 2100 -80 {lab=vss}
N 2040 -80 2070 -80 {lab=vss}
N 2040 -160 2040 -80 {lab=vss}
N 1950 -80 2040 -80 {lab=vss}
N 560 -1140 580 -1140 {lab=vdd}
N 580 -1240 580 -1170 {lab=vdd}
N 560 -1240 580 -1240 {lab=vdd}
N 1480 -500 1540 -500 {lab=xp}
N 1340 -500 1400 -500 {lab=xp}
N 780 -1110 780 -580 {lab=vbnc}
N 840 -580 840 -200 {lab=vbnc}
N 1160 -200 1180 -200 {lab=vss}
N 1180 -170 1180 -80 {lab=vss}
N 1160 -80 1180 -80 {lab=vss}
N 1770 -200 1830 -200 {lab=bd}
N 920 -200 940 -200 {lab=ni}
N 1120 -1140 1140 -1140 {lab=vbp}
N 1770 -1140 1790 -1140 {lab=vbp}
N 680 -1040 1120 -1040 {lab=vbp}
N 1220 -940 1240 -940 {lab=gh}
N 1180 -880 1240 -880 {lab=gh}
N 1380 -780 1400 -780 {lab=m}
N 1480 -600 1500 -600 {lab=xp}
N 1400 -500 1480 -500 {lab=xp}
N 1380 -600 1400 -600 {lab=xp}
N 1320 -780 1340 -780 {lab=gh}
N 1340 -880 1340 -810 {lab=gh}
N 1160 -940 1180 -940 {lab=ts}
N 1160 -1000 1160 -940 {lab=ts}
N 1160 -1000 1180 -1000 {lab=ts}
N 1180 -1110 1180 -1000 {lab=ts}
N 1180 -1000 1180 -970 {lab=ts}
N 980 -500 1340 -500 {lab=xp}
N 780 -80 980 -80 {lab=vss}
N 1000 -80 1160 -80 {lab=vss}
N 920 -320 1260 -320 {lab=ni}
N 1220 -200 1260 -200 {lab=ni}
N 1180 -360 1340 -360 {lab=gh}
N 1180 -80 1340 -80 {lab=vss}
N 1340 -80 1360 -80 {lab=vss}
N 980 -1240 1180 -1240 {lab=vdd}
N 800 -1240 980 -1240 {lab=vdd}
N 1000 -580 1000 -200 {lab=vss}
N 840 -580 940 -580 {lab=vbnc}
N 1320 -600 1340 -600 {lab=m}
N 1540 -600 1560 -600 {lab=m}
N 1340 -690 1340 -630 {lab=m}
N 1320 -690 1340 -690 {lab=m}
N 1540 -690 1540 -630 {lab=m}
N 100 -1240 400 -1240 {lab=vdd}
N 280 -500 280 -200 {lab=vss}
N 100 -80 260 -80 {lab=vss}
N 260 -360 260 -230 {lab=ni}
N 420 -200 440 -200 {lab=ni}
N 820 -200 840 -200 {lab=vbnc}
N 520 -320 920 -320 {lab=ni}
N 520 -200 540 -200 {lab=ni}
N 580 -80 600 -80 {lab=vss}
N 600 -80 760 -80 {lab=vss}
N 200 -200 220 -200 {lab=en_3v3_b}
N 200 -400 200 -200 {lab=en_3v3_b}
N 100 -620 200 -620 {lab=en_3v3_b}
N 1540 -690 1560 -690 {lab=m}
N 1400 -690 1540 -690 {lab=m}
N 1240 -880 1320 -880 {lab=gh}
N 1730 -80 1930 -80 {lab=vss}
N 1540 -340 1540 -230 {lab=vcm}
N 2070 -440 2070 -340 {lab=vcm}
N 200 -620 200 -400 {lab=en_3v3_b}
N 1480 -400 1480 -200 {lab=en_3v3_b}
N 400 -1240 560 -1240 {lab=vdd}
N 440 -320 520 -320 {lab=ni}
N 380 -80 580 -80 {lab=vss}
N 1540 -80 1560 -80 {lab=vss}
N 1360 -80 1540 -80 {lab=vss}
N 200 -400 1480 -400 {lab=en_3v3_b}
N 2070 -440 2150 -440 {lab=vcm}
N 1970 -690 1990 -690 {lab=vcm}
N 1120 -1040 1770 -1040 {lab=vbp}
N 1560 -80 1730 -80 {lab=vss}
N 1540 -340 2070 -340 {lab=vcm}
N 1200 -1240 1830 -1240 {lab=vdd}
N 1560 -690 1690 -690 {lab=m}
N 1730 -690 1750 -690 {lab=bt}
C {devices/iopin.sym} 100 -1240 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -80 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -700 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 2150 -440 0 0 {name=p3 lab=vcm}
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
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 360 -620 0 0 {name=TGP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 240 -200 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -200 0 1 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 560 -200 0 0 {name=NBP
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -1140 0 1 {name=BP
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -1140 0 0 {name=PBNC
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 800 -200 0 1 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1160 -1140 0 0 {name=TR
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1200 -940 0 1 {name=MR
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1200 -200 0 1 {name=SH1
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1320 -200 0 0 {name=SH2
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 960 -580 0 0 {name=CY
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 960 -200 0 0 {name=SY
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1360 -780 0 1 {name=SU
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1360 -600 0 1 {name=SL1
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1520 -600 0 0 {name=SL2
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1810 -1140 0 0 {name=BT
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1710 -690 0 0 {name=BA
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1950 -690 0 1 {name=BB
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1750 -200 0 1 {name=BD
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1910 -200 0 0 {name=BM
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2070 -180 1 0 {name=CB
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1520 -200 0 0 {name=SPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 200 -200 0 0 {name=l1 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_wire.sym} 780 -700 0 1 {name=l2 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1160 -1000 0 0 {name=l3 sig_type=std_logic lab=ts}
C {devices/lab_wire.sym} 1240 -880 0 1 {name=l4 sig_type=std_logic lab=gh}
C {devices/lab_pin.sym} 780 -580 0 0 {name=l5 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1520 -500 0 0 {name=l6 sig_type=std_logic lab=xp}
C {devices/lab_wire.sym} 1520 -690 0 0 {name=l7 sig_type=std_logic lab=m}
C {devices/lab_wire.sym} 1790 -780 0 0 {name=l8 sig_type=std_logic lab=bt}
C {devices/lab_wire.sym} 1730 -400 0 1 {name=l9 sig_type=std_logic lab=bd}
C {devices/lab_pin.sym} 1580 -200 0 0 {name=l10 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_wire.sym} 460 -320 0 0 {name=l11 sig_type=std_logic lab=ni}
C {devices/lab_wire.sym} 730 -1040 0 0 {name=l12 sig_type=std_logic lab=vbp}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
