v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 265 -595 975 -595 975 -430 265 -430 265 -595 {dash=6}
P 10 5 450 -270 570 -270 570 -140 450 -140 450 -270 {dash=6}
P 10 5 165 -270 440 -270 440 -140 165 -140 165 -270 {dash=6}
T {vref_s2d_rb: replica bias for the pad reference vref of the S2D pad} 100 -1308 0 0 0.6 0.6 {}
T {vref_s2d_rb: replica bias for the pad reference vref of sg13cmos5l_IOPadSingle2Diff (user's choice 1a: about 0.5 V, so} 100 -1238 0 0 0.25 0.25 {}
T {that the pad range 0 ... 1 V includes iovss). Task docs/launch/replica_bias_TASK.md (branch harness-test); evidence} 100 -1216 0 0 0.25 0.25 {}
T {docs/replica_bias/SURVEY.md and the G4 runs (macros/vcm_rb/testbenches/pad_char/results/g4_s2d_vref.tsv).} 100 -1194 0 0 0.25 0.25 {}
T {} 100 -1172 0 0 0.25 0.25 {}
T {The S2D input stays linear (INL <= 2 mV, u = +-0.5 V) for vref above an edge set by the input follower (hv PMOS 20u/1u)} 100 -1150 0 0 0.25 0.25 {}
T {leaving saturation against the fold node x: edge = x - V_SG(follower, 5 uA) + 0.676 V (+-4 mV over corners and iovdd at} 100 -1128 0 0 0.25 0.25 {}
T {125 C). It is below 0.4 V up to 27 C and 0.46 ... 0.54 V at 125 C (fast PMOS highest).} 100 -1106 0 0 0.25 0.25 {}
T {vref = vbnc - V_GS(F): an x-node replica at a lower current density (F = 4 fingers of the fold cascode, 15u/3u, at} 100 -1084 0 0 0.25 0.25 {}
T {1.67 uA, against the S2D's 30u/3u at 10 uA), so it rises with temperature like x and sits about 0.1 V above it:} 100 -1062 0 0 0.25 0.25 {}
T {about 0.49 V at 27 C (pad range from 0 V), 0.44 V at -40 C, and >= 30 mV above the INL edge at 125 C} 100 -1040 0 0 0.25 0.25 {}
T {(explore_vref.py). Output impedance about 1/gm(F) = 20 kOhm; CB1 / CB2 (2 x 12u x 12u hv NMOS to vss) hold the pin} 100 -1018 0 0 0.25 0.25 {}
T {during the pad's own transients (G6: steps and enable).} 100 -996 0 0 0.25 0.25 {}
T {Since 2026-11-07 the lines come from the shared cell bias_tree_rb (macros/pad_ref_rb), which also feeds vcm_rb; before,} 100 -974 0 0 0.25 0.25 {}
T {this block had its own copy (reference NI, BP, BNC). Supply current (tt 27 C): 1.67 uA (the follower).} 100 -952 0 0 0.25 0.25 {}
T {Ports: vdd vss ni vbnc vref en_3v3_b. ni / vbnc: bias_tree_rb's lines (ni = its 6u/6u NMOS reference diode, vbnc =} 100 -930 0 0 0.25 0.25 {}
T {its 1u/8u NMOS diode at 2 uA); en_3v3_b: complement of the enable.} 100 -908 0 0 0.25 0.25 {}
T {Disabled (en_3v3 = 0): the tree cuts the reference and pulls ni to vss (SF off), vbnc decays to vss (F off); SPD pulls} 100 -886 0 0 0.25 0.25 {}
T {vref to vss (the s2d pad's vref drives gates only). vref has no enable of its own: it is on whenever pad_ref_rb is} 100 -864 0 0 0.25 0.25 {}
T {(pulling vref low with the tree on would short the follower F from vbnc).} 100 -842 0 0 0.25 0.25 {}
T {drawn from netlist/source/vref_s2d_rb.spice; make check-sheet netlists this sheet and compares it with that netlist device by device} 100 -810 0 0 0.25 0.25 {}
T {[1] x-node replica} 884 -618.5 0 0 0.35 0.35 {layer=10}
T {[1]} 465 -293.5 0 0 0.35 0.35 {layer=10}
T {[2] disable} 170 -293.5 0 0 0.35 0.35 {layer=10}
N 520 -460 520 -250 {lab=vref}
N 440 -520 480 -520 {lab=vbnc}
N 800 -520 840 -520 {lab=vbnc}
N 440 -630 800 -630 {lab=vbnc}
N 880 -520 900 -520 {lab=vss}
N 520 -520 540 -520 {lab=vss}
N 400 -460 400 -250 {lab=vref}
N 420 -220 420 -100 {lab=vss}
N 680 -460 720 -460 {lab=vref}
N 400 -520 440 -520 {lab=vbnc}
N 760 -520 800 -520 {lab=vbnc}
N 400 -100 420 -100 {lab=vss}
N 540 -520 720 -520 {lab=vss}
N 800 -460 880 -460 {lab=vref}
N 520 -100 540 -100 {lab=vss}
N 100 -100 340 -100 {lab=vss}
N 720 -720 880 -720 {lab=vdd}
N 100 -630 440 -630 {lab=vbnc}
N 340 -520 360 -520 {lab=vss}
N 520 -220 540 -220 {lab=vss}
N 520 -190 520 -100 {lab=vss}
N 460 -220 480 -220 {lab=ni}
N 400 -460 520 -460 {lab=vref}
N 420 -100 520 -100 {lab=vss}
N 540 -220 540 -100 {lab=vss}
N 440 -630 440 -520 {lab=vbnc}
N 800 -630 800 -520 {lab=vbnc}
N 540 -520 540 -220 {lab=vss}
N 520 -490 520 -460 {lab=vref}
N 720 -490 720 -460 {lab=vref}
N 900 -520 900 -100 {lab=vss}
N 880 -490 880 -460 {lab=vref}
N 340 -520 340 -100 {lab=vss}
N 360 -490 360 -460 {lab=vref}
N 400 -220 420 -220 {lab=vss}
N 400 -190 400 -100 {lab=vss}
N 340 -100 400 -100 {lab=vss}
N 360 -460 400 -460 {lab=vref}
N 300 -220 360 -220 {lab=en_3v3_b}
N 460 -300 460 -220 {lab=ni}
N 100 -300 460 -300 {lab=ni}
N 720 -460 800 -460 {lab=vref}
N 520 -460 680 -460 {lab=vref}
N 880 -460 1020 -460 {lab=vref}
N 880 -720 880 -550 {lab=vdd}
N 720 -720 720 -550 {lab=vdd}
N 520 -720 720 -720 {lab=vdd}
N 520 -720 520 -550 {lab=vdd}
N 360 -720 520 -720 {lab=vdd}
N 360 -720 360 -550 {lab=vdd}
N 100 -720 360 -720 {lab=vdd}
N 300 -360 300 -220 {lab=en_3v3_b}
N 100 -360 300 -360 {lab=en_3v3_b}
C {devices/iopin.sym} 100 -720 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -300 0 0 {name=p2 lab=ni}
C {devices/ipin.sym} 100 -630 0 0 {name=p3 lab=vbnc}
C {devices/opin.sym} 1020 -460 0 0 {name=p4 lab=vref}
C {devices/ipin.sym} 100 -360 0 0 {name=p5 lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 380 -520 0 1 {name=F1
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 500 -520 0 0 {name=F2
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 740 -520 0 1 {name=F3
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 860 -520 0 0 {name=F4
l=3u
w=15u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 500 -220 0 0 {name=SF
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 380 -220 0 0 {name=SPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_wire.sym} 320 -630 0 0 {name=l3 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 420 -460 0 0 {name=l4 sig_type=std_logic lab=vref}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
C {devices/lab_wire.sym} 800 -630 0 1 {name=l2 sig_type=std_logic lab=vbnc}
N 540 -100 900 -100 {lab=vss}
