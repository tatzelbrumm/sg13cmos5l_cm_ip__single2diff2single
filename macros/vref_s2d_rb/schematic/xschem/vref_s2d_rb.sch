v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {vref_s2d_rb: generated label-style sheet from netlist/source/vref_s2d_rb.spice (gen_sheet.py)} 60 -1400 0 0 0.4 0.4 {}
T {vref_s2d_rb: replica bias for the pad reference vref of sg13cmos5l_IOPadSingle2Diff (user's choice 1a: about 0.5 V, so} 60 -1360 0 0 0.2 0.2 {}
T {that the pad range 0 ... 1 V includes iovss). Task docs/launch/replica_bias_TASK.md (branch harness-test); evidence} 60 -1338 0 0 0.2 0.2 {}
T {docs/replica_bias/SURVEY.md and the G4 runs (macros/vcm_rb/testbenches/pad_char/results/g4_s2d_vref.tsv).} 60 -1316 0 0 0.2 0.2 {}
T {The S2D input stays linear (INL <= 2 mV, u = +-0.5 V) for vref above an edge set by the input follower (hv PMOS 20u/1u)} 60 -1294 0 0 0.2 0.2 {}
T {leaving saturation against the fold node x: edge = x - V_SG(follower, 5 uA) + 0.676 V (+-4 mV over corners and iovdd at} 60 -1272 0 0 0.2 0.2 {}
T {125 C). It is below 0.4 V up to 27 C and 0.46 ... 0.54 V at 125 C (fast PMOS highest).} 60 -1250 0 0 0.2 0.2 {}
T {vref = vbnc - V_GS(F): an x-node replica at a lower current density (F = 4 fingers of the fold cascode, 15u/3u, at} 60 -1228 0 0 0.2 0.2 {}
T {1.67 uA, against the S2D's 30u/3u at 10 uA), so it rises with temperature like x (+0.3 mV/K) and sits 0.10 V above it:} 60 -1206 0 0 0.2 0.2 {}
T {about 0.49 V at 27 C (pad range from 0 V), 0.44 V at -40 C, and >= 20 mV above the INL edge at 125 C} 60 -1184 0 0 0.2 0.2 {}
T {(explore_vref.py). Output impedance about 1/gm(F) = 20 kOhm; CB1 / CB2 (2 x 12u x 12u hv NMOS to vss) hold the pin} 60 -1162 0 0 0.2 0.2 {}
T {during the pad's own transients (G6: steps and enable).} 60 -1140 0 0 0.2 0.2 {}
T {Lines as vcm_rb: NI (6u/6u NMOS diode, the 5 uA reference), BP (2u/6u at 2 uA from NBP 2.4u/6u), BNC (1u/8u at 2 uA} 60 -1118 0 0 0.2 0.2 {}
T {from PBNC 2u/6u). Supply current (tt 27 C): 5 + 2 + 2 + 1.67 = about 10.7 uA.} 60 -1096 0 0 0.2 0.2 {}
T {Ports: vdd vss iref vref en_3v3 en_3v3_b. iref: 5 uA SOURCED into the block.} 60 -1074 0 0 0.2 0.2 {}
C {devices/iopin.sym} 100 -960 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -920 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -880 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 100 -840 0 1 {name=p3 lab=vref}
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
T {[3] the reference: x-node replica at low density} 300 -500 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -440 0 0 {name=F1
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -470 0 1 {name=l33 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 420 -410 0 1 {name=l34 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 420 -440 0 1 {name=l35 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -440 0 0 {name=l36 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 620 -440 0 0 {name=F2
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 640 -470 0 1 {name=l37 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 640 -410 0 1 {name=l38 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 640 -440 0 1 {name=l39 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 600 -440 0 0 {name=l40 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 840 -440 0 0 {name=F3
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 860 -470 0 1 {name=l41 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 860 -410 0 1 {name=l42 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 860 -440 0 1 {name=l43 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 820 -440 0 0 {name=l44 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1060 -440 0 0 {name=F4
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1080 -470 0 1 {name=l45 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1080 -410 0 1 {name=l46 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 1080 -440 0 1 {name=l47 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1040 -440 0 0 {name=l48 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 -440 0 0 {name=SF
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1300 -470 0 1 {name=l49 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 1300 -410 0 1 {name=l50 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1300 -440 0 1 {name=l51 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1260 -440 0 0 {name=l52 sig_type=std_logic lab=ni}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1500 -440 0 0 {name=CB1
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1520 -470 0 1 {name=l53 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1520 -410 0 1 {name=l54 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1520 -440 0 1 {name=l55 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1480 -440 0 0 {name=l56 sig_type=std_logic lab=vref}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -300 0 0 {name=CB2
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -330 0 1 {name=l57 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 420 -270 0 1 {name=l58 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 420 -300 0 1 {name=l59 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -300 0 0 {name=l60 sig_type=std_logic lab=vref}
T {[4] disable} 300 -100 0 0 0.3 0.3 {layer=10}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -40 0 0 {name=SPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -70 0 1 {name=l61 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 420 -10 0 1 {name=l62 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 420 -40 0 1 {name=l63 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -40 0 0 {name=l64 sig_type=std_logic lab=en_3v3_b}
