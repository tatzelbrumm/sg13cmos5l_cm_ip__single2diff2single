v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {vcm_rb: generated label-style sheet from netlist/source/vcm_rb.spice (gen_sheet.py)} 60 -1400 0 0 0.4 0.4 {}
T {vcm_rb: replica bias for the internal common mode of the custom pads: S2D vcm = D2S vref (= D2S input common mode).} 60 -1360 0 0 0.2 0.2 {}
T {Task docs/launch/replica_bias_TASK.md (branch harness-test); targets and evidence docs/replica_bias/SURVEY.md, design} 60 -1338 0 0 0.2 0.2 {}
T {notes on the notes branch (sudelbuecher/design_considerations/replica_bias/).} 60 -1316 0 0 0.2 0.2 {}
T {vcm sits at the centre of the band in which both pads stay linear (INL <= 2 mV with +-0.5 V on the unit gates):} 60 -1294 0 0 0.2 0.2 {}
T {top    edge = the gate voltage at which a unit_r2 tail (hv PMOS 5u/6u at vbp, 5 uA) leaves saturation as the input} 60 -1272 0 0 0.2 0.2 {}
T {follower (hv PMOS 20u/1u ng=2) raises its source;} 60 -1250 0 0 0.2 0.2 {}
T {bottom edge = the output voltage at which the S2D fold cascode CX / CY (hv NMOS 30u/3u at vbnc) leaves saturation} 60 -1228 0 0 0.2 0.2 {}
T {above the fold node x.} 60 -1206 0 0 0.2 0.2 {}
T {Replicas, each from the block's own lines (made from one 5 uA reference current, as bias_tree_pd does):} 60 -1184 0 0 0.2 0.2 {}
T {gh = top-edge detector: TR (5u/6u at vbp) -> MR (20u/1u ng=2, diode) -> sink SH (2 x 2.4u/6u = 4 uA, r = 0.8)} 60 -1162 0 0 0.2 0.2 {}
T {gh = top gate limit + 0.157 V (+-18 mV over corners, -40..125 C, iovdd 3.0..3.6 V, run explore_edges.py)} 60 -1140 0 0 0.2 0.2 {}
T {xp = fold-node replica: one finger of CY (15u/3u at vbnc) at 5 uA on SY (6u/6u)} 60 -1118 0 0 0.2 0.2 {}
T {bottom edge = xp + 0.559 V (+-34 mV)} 60 -1096 0 0 0.2 0.2 {}
T {m  = average of gh and xp by three identical hv PMOS diodes 1u/4u in their own wells, one above m, two in parallel} 60 -1074 0 0 0.2 0.2 {}
C {devices/iopin.sym} 100 -960 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -920 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -880 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 100 -840 0 1 {name=p3 lab=vcm}
C {devices/ipin.sym} 100 -800 0 0 {name=p4 lab=en_3v3}
C {devices/ipin.sym} 100 -760 0 0 {name=p5 lab=en_3v3_b}
T {[1] reference input (as bias_tree_pd)} 300 -1020 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -960 0 0 {name=TGN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -990 0 1 {name=l1 sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 420 -930 0 1 {name=l2 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 420 -960 0 1 {name=l3 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -960 0 0 {name=l4 sig_type=std_logic lab=en_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 620 -960 0 0 {name=TGP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 640 -990 0 1 {name=l5 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 640 -930 0 1 {name=l6 sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 640 -960 0 1 {name=l7 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 600 -960 0 0 {name=l8 sig_type=std_logic lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 840 -960 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 860 -990 0 1 {name=l9 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 860 -930 0 1 {name=l10 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 860 -960 0 1 {name=l11 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 820 -960 0 0 {name=l12 sig_type=std_logic lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1060 -960 0 0 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1080 -990 0 1 {name=l13 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 1080 -930 0 1 {name=l14 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1080 -960 0 1 {name=l15 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1040 -960 0 0 {name=l16 sig_type=std_logic lab=ni}
T {[2] lines} 300 -760 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -700 0 0 {name=NBP
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -730 0 1 {name=l17 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 420 -670 0 1 {name=l18 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 420 -700 0 1 {name=l19 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -700 0 0 {name=l20 sig_type=std_logic lab=ni}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 620 -700 0 0 {name=BP
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 640 -730 0 1 {name=l21 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 640 -670 0 1 {name=l22 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 640 -700 0 1 {name=l23 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 600 -700 0 0 {name=l24 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 840 -700 0 0 {name=PBNC
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 860 -730 0 1 {name=l25 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 860 -670 0 1 {name=l26 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 860 -700 0 1 {name=l27 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 820 -700 0 0 {name=l28 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1060 -700 0 0 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1080 -730 0 1 {name=l29 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 1080 -670 0 1 {name=l30 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1080 -700 0 1 {name=l31 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1040 -700 0 0 {name=l32 sig_type=std_logic lab=vbnc}
T {[3] top-edge detector} 300 -500 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 -440 0 0 {name=TR
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -470 0 1 {name=l33 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 420 -410 0 1 {name=l34 sig_type=std_logic lab=ts}
C {devices/lab_pin.sym} 420 -440 0 1 {name=l35 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 380 -440 0 0 {name=l36 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 620 -440 0 0 {name=MR
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 640 -470 0 1 {name=l37 sig_type=std_logic lab=ts}
C {devices/lab_pin.sym} 640 -410 0 1 {name=l38 sig_type=std_logic lab=gh}
C {devices/lab_pin.sym} 640 -440 0 1 {name=l39 sig_type=std_logic lab=ts}
C {devices/lab_pin.sym} 600 -440 0 0 {name=l40 sig_type=std_logic lab=gh}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 840 -440 0 0 {name=SH1
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 860 -470 0 1 {name=l41 sig_type=std_logic lab=gh}
C {devices/lab_pin.sym} 860 -410 0 1 {name=l42 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 860 -440 0 1 {name=l43 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 820 -440 0 0 {name=l44 sig_type=std_logic lab=ni}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1060 -440 0 0 {name=SH2
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1080 -470 0 1 {name=l45 sig_type=std_logic lab=gh}
C {devices/lab_pin.sym} 1080 -410 0 1 {name=l46 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1080 -440 0 1 {name=l47 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1040 -440 0 0 {name=l48 sig_type=std_logic lab=ni}
T {[4] fold-node replica} 300 -240 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -180 0 0 {name=CY
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -210 0 1 {name=l49 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 420 -150 0 1 {name=l50 sig_type=std_logic lab=xp}
C {devices/lab_pin.sym} 420 -180 0 1 {name=l51 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -180 0 0 {name=l52 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 620 -180 0 0 {name=SY
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 640 -210 0 1 {name=l53 sig_type=std_logic lab=xp}
C {devices/lab_pin.sym} 640 -150 0 1 {name=l54 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 640 -180 0 1 {name=l55 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 600 -180 0 0 {name=l56 sig_type=std_logic lab=ni}
T {[5] average: gh -> m -> xp, three identical PMOS diodes in their own wells} 300 20 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 80 0 0 {name=SU
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 50 0 1 {name=l57 sig_type=std_logic lab=gh}
C {devices/lab_pin.sym} 420 110 0 1 {name=l58 sig_type=std_logic lab=m}
C {devices/lab_pin.sym} 420 80 0 1 {name=l59 sig_type=std_logic lab=gh}
C {devices/lab_pin.sym} 380 80 0 0 {name=l60 sig_type=std_logic lab=m}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 620 80 0 0 {name=SL1
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 640 50 0 1 {name=l61 sig_type=std_logic lab=m}
C {devices/lab_pin.sym} 640 110 0 1 {name=l62 sig_type=std_logic lab=xp}
C {devices/lab_pin.sym} 640 80 0 1 {name=l63 sig_type=std_logic lab=m}
C {devices/lab_pin.sym} 600 80 0 0 {name=l64 sig_type=std_logic lab=xp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 840 80 0 0 {name=SL2
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 860 50 0 1 {name=l65 sig_type=std_logic lab=m}
C {devices/lab_pin.sym} 860 110 0 1 {name=l66 sig_type=std_logic lab=xp}
C {devices/lab_pin.sym} 860 80 0 1 {name=l67 sig_type=std_logic lab=m}
C {devices/lab_pin.sym} 820 80 0 0 {name=l68 sig_type=std_logic lab=xp}
T {[6] unity-gain buffer: m -> vcm} 300 280 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 340 0 0 {name=BT
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 310 0 1 {name=l69 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 420 370 0 1 {name=l70 sig_type=std_logic lab=bt}
C {devices/lab_pin.sym} 420 340 0 1 {name=l71 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 380 340 0 0 {name=l72 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 620 340 0 0 {name=BA
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 640 310 0 1 {name=l73 sig_type=std_logic lab=bt}
C {devices/lab_pin.sym} 640 370 0 1 {name=l74 sig_type=std_logic lab=bd}
C {devices/lab_pin.sym} 640 340 0 1 {name=l75 sig_type=std_logic lab=bt}
C {devices/lab_pin.sym} 600 340 0 0 {name=l76 sig_type=std_logic lab=m}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 840 340 0 0 {name=BB
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 860 310 0 1 {name=l77 sig_type=std_logic lab=bt}
C {devices/lab_pin.sym} 860 370 0 1 {name=l78 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 860 340 0 1 {name=l79 sig_type=std_logic lab=bt}
C {devices/lab_pin.sym} 820 340 0 0 {name=l80 sig_type=std_logic lab=vcm}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1060 340 0 0 {name=BD
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1080 310 0 1 {name=l81 sig_type=std_logic lab=bd}
C {devices/lab_pin.sym} 1080 370 0 1 {name=l82 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1080 340 0 1 {name=l83 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1040 340 0 0 {name=l84 sig_type=std_logic lab=bd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 340 0 0 {name=BM
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1300 310 0 1 {name=l85 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 1300 370 0 1 {name=l86 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1300 340 0 1 {name=l87 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1260 340 0 0 {name=l88 sig_type=std_logic lab=bd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1500 340 0 0 {name=CB
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1520 310 0 1 {name=l89 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1520 370 0 1 {name=l90 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1520 340 0 1 {name=l91 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1480 340 0 0 {name=l92 sig_type=std_logic lab=vcm}
T {[7] disable} 300 540 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 600 0 0 {name=SPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 570 0 1 {name=l93 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 420 630 0 1 {name=l94 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 420 600 0 1 {name=l95 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 600 0 0 {name=l96 sig_type=std_logic lab=en_3v3_b}
