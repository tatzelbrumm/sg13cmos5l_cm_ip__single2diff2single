v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 500 -1190 660 -1190 660 -900 500 -900 500 -1190 {dash=6}
P 10 5 525 -380 795 -380 795 -120 525 -120 525 -380 {dash=6}
P 10 5 640 -845 1035 -845 1035 -470 640 -470 640 -845 {dash=6}
P 10 5 125 -640 445 -640 445 -515 125 -515 125 -640 {dash=6}
P 10 5 300 -250 450 -250 450 -120 300 -120 300 -250 {dash=6}
P 10 5 1060 -1190 1405 -1190 1405 -120 1060 -120 1060 -1190 {dash=6}
P 10 5 865 -395 1035 -395 1035 -120 865 -120 865 -395 {dash=6}
T {vcm_rb: replica bias for the pads' internal common mode (S2D vcm = D2S vref)} 100 -2046 0 0 0.6 0.6 {}
T {vcm_rb: replica bias for the internal common mode of the custom pads: S2D vcm = D2S vref (= D2S input common mode).} 100 -1976 0 0 0.25 0.25 {}
T {Task docs/launch/replica_bias_TASK.md (branch harness-test); targets and evidence docs/replica_bias/SURVEY.md, design} 100 -1954 0 0 0.25 0.25 {}
T {notes on the notes branch (sudelbuecher/design_considerations/replica_bias/).} 100 -1932 0 0 0.25 0.25 {}
T {} 100 -1910 0 0 0.25 0.25 {}
T {vcm sits at the centre of the band in which both pads stay linear (INL <= 2 mV with +-0.5 V on the unit gates):} 100 -1888 0 0 0.25 0.25 {}
T {  top    edge = the gate voltage at which a unit_r2 tail (hv PMOS 5u/6u at vbp, 5 uA) leaves saturation as the input} 100 -1866 0 0 0.25 0.25 {}
T {                follower (hv PMOS 20u/1u ng=2) raises its source;} 100 -1844 0 0 0.25 0.25 {}
T {  bottom edge = the output voltage at which the S2D fold cascode CX / CY (hv NMOS 30u/3u at vbnc) leaves saturation} 100 -1822 0 0 0.25 0.25 {}
T {                above the fold node x.} 100 -1800 0 0 0.25 0.25 {}
T {Replicas, on the lines of the shared tree bias_tree_rb (macros/pad_ref_rb):} 100 -1778 0 0 0.25 0.25 {}
T {  gh = top-edge detector: TR (5u/6u at vbp) -> MR (20u/1u ng=2, diode) -> sink SH (2 x 2.4u/6u = 4 uA, r = 0.8)} 100 -1756 0 0 0.25 0.25 {}
T {       gh = top gate limit + 0.157 V (+-18 mV over corners, -40..125 C, iovdd 3.0..3.6 V, run explore_edges.py)} 100 -1734 0 0 0.25 0.25 {}
T {  xp = fold-node replica: one finger of CY (15u/3u at vbnc) on SY (6u/6u, 5 uA); CY carries 5 uA minus the averaging} 100 -1712 0 0 0.25 0.25 {}
T {       stack's current (nA ... 0.9 uA). bottom edge = xp + 0.559 V (+-34 mV)} 100 -1690 0 0 0.25 0.25 {}
T {  m  = average of gh and xp by three identical hv PMOS diodes 1u/4u in their own wells, one above m, two in parallel} 100 -1668 0 0 0.25 0.25 {}
T {       below (the asymmetry subtracts the 0.06 V offset of (gh + xp)/2 against the centre; explore_vcm_rb.py, G)} 100 -1646 0 0 0.25 0.25 {}
T {  vcm = m, buffered by a 5-transistor OTA in unity gain: PMOS pair = the unit's input device (20u/1u ng=2) on a} 100 -1624 0 0 0.25 0.25 {}
T {       unit tail (5u/6u at vbp, 5 uA), NMOS mirror 6u/6u; output pole at vcm with CB (12u x 12u hv NMOS capacitor} 100 -1602 0 0 0.25 0.25 {}
T {       as the s2d buffer's CLP).} 100 -1580 0 0 0.25 0.25 {}
T {Since 2026-11-07 the lines (reference NI, BP, BNC) are the shared cell bias_tree_rb, which also feeds vref_s2d_rb;} 100 -1558 0 0 0.25 0.25 {}
T {before, each block had its own copy (option A of the user's question on sharing). The lines are gate voltages from} 100 -1536 0 0 0.25 0.25 {}
T {the neighbouring cell on the same rails, inside pad_ref_rb.} 100 -1514 0 0 0.25 0.25 {}
T {Supply current (tt 27 C): 4 (SH) + 5 (SY) + 5 (OTA) = about 14 uA; the tree adds 5 uA reference + 2 (BP) + 2 (BNC).} 100 -1492 0 0 0.25 0.25 {}
T {Ports: vdd vss ni vbp vbnc vcm en_3v3_b. ni / vbp / vbnc: bias_tree_rb's lines (ni = its 6u/6u NMOS reference diode,} 100 -1470 0 0 0.25 0.25 {}
T {vbp = its 2u/6u PMOS diode at 2 uA, vbnc = its 1u/8u NMOS diode at 2 uA); en_3v3_b: complement of the enable.} 100 -1448 0 0 0.25 0.25 {}
T {Disabled (en_3v3 = 0): the tree cuts the reference and pulls ni to vss (every NMOS off; BP pulls vbp to vdd, every} 100 -1426 0 0 0.25 0.25 {}
T {PMOS off), SPD pulls vcm to vss. The s2d pad ties its outputs to vcm while it is off; whoever disables pad_ref_rb} 100 -1404 0 0 0.25 0.25 {}
T {must disable every pad that uses vcm with it (vcm is the next stage's common mode while only the s2d pad is off).} 100 -1382 0 0 0.25 0.25 {}
T {drawn from netlist/source/vcm_rb.spice; make check-sheet netlists this sheet and compares it with that netlist device by device} 100 -1350 0 0 0.25 0.25 {}
T {[1] top-edge detector} 605 -1213.5 0 0 0.35 0.35 {layer=10}
T {[1]} 530 -374 0 0 0.35 0.35 {layer=10}
T {[3] average} 745 -868.5 0 0 0.35 0.35 {layer=10}
T {[2] fold-node replica} 130 -663.5 0 0 0.35 0.35 {layer=10}
T {[2]} 335 -273.5 0 0 0.35 0.35 {layer=10}
T {[4] unity-gain buffer} 1255 -1213.5 0 0 0.35 0.35 {layer=10}
T {[5] disable} 885 -389 0 0 0.35 0.35 {layer=10}
N 520 -1140 520 -1040 {lab=vbp}
N 600 -1240 600 -1140 {lab=vdd}
N 640 -940 640 -880 {lab=gh}
N 580 -910 580 -880 {lab=gh}
N 580 -360 580 -230 {lab=gh}
N 660 -320 660 -200 {lab=ni}
N 740 -360 740 -230 {lab=gh}
N 560 -200 560 -80 {lab=vss}
N 760 -200 760 -80 {lab=vss}
N 720 -880 740 -880 {lab=gh}
N 720 -880 720 -780 {lab=gh}
N 800 -780 800 -690 {lab=m}
N 740 -750 740 -690 {lab=m}
N 720 -690 720 -600 {lab=m}
N 740 -570 740 -500 {lab=xp}
N 800 -600 800 -500 {lab=xp}
N 960 -690 960 -600 {lab=m}
N 940 -570 940 -500 {lab=xp}
N 880 -600 880 -500 {lab=xp}
N 380 -1240 380 -610 {lab=vdd}
N 380 -550 380 -500 {lab=xp}
N 380 -500 380 -230 {lab=xp}
N 380 -580 400 -580 {lab=vss}
N 400 -200 400 -80 {lab=vss}
N 320 -320 320 -200 {lab=ni}
N 1150 -780 1150 -690 {lab=bt}
N 1310 -780 1330 -780 {lab=bt}
N 1310 -780 1310 -690 {lab=bt}
N 1230 -1110 1230 -780 {lab=bt}
N 1170 -1140 1170 -1040 {lab=vbp}
N 1250 -1240 1250 -1140 {lab=vdd}
N 1130 -260 1130 -230 {lab=bd}
N 1230 -200 1290 -200 {lab=bd}
N 1230 -260 1230 -200 {lab=bd}
N 1130 -260 1230 -260 {lab=bd}
N 1130 -200 1130 -80 {lab=vss}
N 1350 -200 1350 -80 {lab=vss}
N 1330 -440 1330 -230 {lab=vcm}
N 1390 -690 1390 -440 {lab=vcm}
N 1470 -340 1470 -200 {lab=vcm}
N 960 -200 960 -80 {lab=vss}
N 880 -200 900 -200 {lab=en_3v3_b}
N 1230 -1240 1250 -1240 {lab=vdd}
N 580 -1240 600 -1240 {lab=vdd}
N 660 -200 720 -200 {lab=ni}
N 580 -880 580 -360 {lab=gh}
N 740 -690 800 -690 {lab=m}
N 380 -80 400 -80 {lab=vss}
N 1150 -780 1230 -780 {lab=bt}
N 1130 -660 1130 -260 {lab=bd}
N 1330 -80 1350 -80 {lab=vss}
N 1330 -440 1390 -440 {lab=vcm}
N 1390 -440 1470 -440 {lab=vcm}
N 1330 -660 1330 -440 {lab=vcm}
N 740 -200 760 -200 {lab=vss}
N 380 -200 400 -200 {lab=vss}
N 1330 -200 1350 -200 {lab=vss}
N 1500 -160 1500 -80 {lab=vss}
N 940 -200 960 -200 {lab=vss}
N 940 -170 940 -80 {lab=vss}
N 1330 -170 1330 -80 {lab=vss}
N 380 -170 380 -80 {lab=vss}
N 740 -170 740 -80 {lab=vss}
N 1310 -690 1330 -690 {lab=bt}
N 1230 -780 1310 -780 {lab=bt}
N 1130 -780 1150 -780 {lab=bt}
N 1130 -780 1130 -720 {lab=bt}
N 1330 -780 1330 -720 {lab=bt}
N 580 -1140 600 -1140 {lab=vdd}
N 1230 -1140 1250 -1140 {lab=vdd}
N 1230 -1240 1230 -1170 {lab=vdd}
N 580 -1240 580 -1170 {lab=vdd}
N 1470 -160 1470 -80 {lab=vss}
N 1470 -80 1500 -80 {lab=vss}
N 1440 -80 1470 -80 {lab=vss}
N 1440 -160 1440 -80 {lab=vss}
N 1350 -80 1440 -80 {lab=vss}
N 880 -500 940 -500 {lab=xp}
N 740 -500 800 -500 {lab=xp}
N 560 -200 580 -200 {lab=vss}
N 580 -170 580 -80 {lab=vss}
N 560 -80 580 -80 {lab=vss}
N 1170 -200 1230 -200 {lab=bd}
N 320 -200 340 -200 {lab=ni}
N 520 -1140 540 -1140 {lab=vbp}
N 1170 -1140 1190 -1140 {lab=vbp}
N 100 -1040 520 -1040 {lab=vbp}
N 620 -940 640 -940 {lab=gh}
N 580 -880 640 -880 {lab=gh}
N 780 -780 800 -780 {lab=m}
N 880 -600 900 -600 {lab=xp}
N 800 -500 880 -500 {lab=xp}
N 780 -600 800 -600 {lab=xp}
N 720 -780 740 -780 {lab=gh}
N 740 -880 740 -810 {lab=gh}
N 560 -940 580 -940 {lab=ts}
N 560 -1000 560 -940 {lab=ts}
N 560 -1000 580 -1000 {lab=ts}
N 580 -1110 580 -1000 {lab=ts}
N 580 -1000 580 -970 {lab=ts}
N 380 -500 740 -500 {lab=xp}
N 100 -80 380 -80 {lab=vss}
N 400 -80 560 -80 {lab=vss}
N 320 -320 660 -320 {lab=ni}
N 620 -200 660 -200 {lab=ni}
N 580 -360 740 -360 {lab=gh}
N 580 -80 740 -80 {lab=vss}
N 740 -80 760 -80 {lab=vss}
N 380 -1240 580 -1240 {lab=vdd}
N 100 -1240 380 -1240 {lab=vdd}
N 400 -580 400 -200 {lab=vss}
N 100 -580 340 -580 {lab=vbnc}
N 720 -600 740 -600 {lab=m}
N 940 -600 960 -600 {lab=m}
N 740 -690 740 -630 {lab=m}
N 720 -690 740 -690 {lab=m}
N 940 -690 940 -630 {lab=m}
N 100 -320 320 -320 {lab=ni}
N 940 -690 960 -690 {lab=m}
N 800 -690 940 -690 {lab=m}
N 640 -880 720 -880 {lab=gh}
N 1130 -80 1330 -80 {lab=vss}
N 940 -340 940 -230 {lab=vcm}
N 1470 -440 1470 -340 {lab=vcm}
N 880 -400 880 -200 {lab=en_3v3_b}
N 940 -80 960 -80 {lab=vss}
N 760 -80 940 -80 {lab=vss}
N 100 -400 880 -400 {lab=en_3v3_b}
N 1470 -440 1550 -440 {lab=vcm}
N 1370 -690 1390 -690 {lab=vcm}
N 520 -1040 1170 -1040 {lab=vbp}
N 960 -80 1130 -80 {lab=vss}
N 940 -340 1470 -340 {lab=vcm}
N 600 -1240 1230 -1240 {lab=vdd}
N 960 -690 1090 -690 {lab=m}
N 1130 -690 1150 -690 {lab=bt}
C {devices/iopin.sym} 100 -1240 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -80 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -320 0 0 {name=p2 lab=ni}
C {devices/ipin.sym} 100 -1040 0 0 {name=p3 lab=vbp}
C {devices/ipin.sym} 100 -580 0 0 {name=p4 lab=vbnc}
C {devices/opin.sym} 1550 -440 0 0 {name=p5 lab=vcm}
C {devices/ipin.sym} 100 -400 0 0 {name=p6 lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -1140 0 0 {name=TR
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -940 0 1 {name=MR
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 -200 0 1 {name=SH1
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 720 -200 0 0 {name=SH2
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 360 -580 0 0 {name=CY
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 360 -200 0 0 {name=SY
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -780 0 1 {name=SU
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -600 0 1 {name=SL1
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 -600 0 0 {name=SL2
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1210 -1140 0 0 {name=BT
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1110 -690 0 0 {name=BA
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1350 -690 0 1 {name=BB
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1150 -200 0 1 {name=BD
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1310 -200 0 0 {name=BM
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1470 -180 1 0 {name=CB
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 920 -200 0 0 {name=SPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_wire.sym} 560 -1000 0 0 {name=l3 sig_type=std_logic lab=ts}
C {devices/lab_wire.sym} 640 -880 0 1 {name=l4 sig_type=std_logic lab=gh}
C {devices/lab_wire.sym} 920 -500 0 0 {name=l6 sig_type=std_logic lab=xp}
C {devices/lab_wire.sym} 920 -690 0 0 {name=l7 sig_type=std_logic lab=m}
C {devices/lab_wire.sym} 1190 -780 0 0 {name=l8 sig_type=std_logic lab=bt}
C {devices/lab_wire.sym} 1130 -400 0 1 {name=l9 sig_type=std_logic lab=bd}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
P 10 5 1680 -1190 2000 -1190 2000 -380 1680 -380 1680 -1190 {dash=6}
T {[DM] layout dummies} 1685 -1213.5 0 0 0.35 0.35 {layer=10}
T {as drawn in the rows (pad convention):} 1690 -1170 0 0 0.2 0.2 {layer=10}
T {D = S = B on the rail, gate as drawn} 1690 -1150 0 0 0.2 0.2 {layer=10}
T {MDAU, MDAL: rail = well net} 1690 -1130 0 0 0.2 0.2 {layer=10}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1800 -1060 0 0 {name=MDT[1:0]
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 1820 -1090 1840 -1090 {lab=vdd}
N 1820 -1060 1840 -1060 {lab=vdd}
N 1820 -1030 1840 -1030 {lab=vdd}
N 1840 -1030 1840 -1120 {lab=vdd}
C {devices/lab_pin.sym} 1840 -1120 0 1 {name=ldm0_r sig_type=std_logic lab=vdd}
N 1780 -1060 1740 -1060 {lab=vbp}
C {devices/lab_pin.sym} 1740 -1060 0 0 {name=ldm0_g sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1800 -920 0 0 {name=MDU[1:0]
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 1820 -950 1840 -950 {lab=vdd}
N 1820 -920 1840 -920 {lab=vdd}
N 1820 -890 1840 -890 {lab=vdd}
N 1840 -890 1840 -980 {lab=vdd}
C {devices/lab_pin.sym} 1840 -980 0 1 {name=ldm1_r sig_type=std_logic lab=vdd}
N 1780 -920 1740 -920 {lab=vdd}
C {devices/lab_pin.sym} 1740 -920 0 0 {name=ldm1_g sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1800 -780 0 0 {name=MDAU[1:0]
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 1820 -810 1840 -810 {lab=gh}
N 1820 -780 1840 -780 {lab=gh}
N 1820 -750 1840 -750 {lab=gh}
N 1840 -750 1840 -840 {lab=gh}
C {devices/lab_pin.sym} 1840 -840 0 1 {name=ldm2_r sig_type=std_logic lab=gh}
N 1780 -780 1740 -780 {lab=m}
C {devices/lab_pin.sym} 1740 -780 0 0 {name=ldm2_g sig_type=std_logic lab=m}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1800 -640 0 0 {name=MDAL[1:0]
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 1820 -670 1840 -670 {lab=m}
N 1820 -640 1840 -640 {lab=m}
N 1820 -610 1840 -610 {lab=m}
N 1840 -610 1840 -700 {lab=m}
C {devices/lab_pin.sym} 1840 -700 0 1 {name=ldm3_r sig_type=std_logic lab=m}
N 1780 -640 1740 -640 {lab=xp}
C {devices/lab_pin.sym} 1740 -640 0 0 {name=ldm3_g sig_type=std_logic lab=xp}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1800 -480 0 0 {name=MDM[1:0]
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 1820 -510 1840 -510 {lab=vss}
N 1820 -480 1840 -480 {lab=vss}
N 1820 -450 1840 -450 {lab=vss}
N 1840 -510 1840 -420 {lab=vss}
C {devices/lab_pin.sym} 1840 -420 0 1 {name=ldm4_r sig_type=std_logic lab=vss}
N 1780 -480 1740 -480 {lab=bd}
C {devices/lab_pin.sym} 1740 -480 0 0 {name=ldm4_g sig_type=std_logic lab=bd}
