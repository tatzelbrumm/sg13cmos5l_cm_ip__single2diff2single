v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 160 -1070 300 -1070 300 -115 160 -115 160 -1070 {dash=6}
P 10 5 960 -1070 1260 -1070 1260 -115 960 -115 960 -1070 {dash=6}
P 10 5 800 -1070 940 -1070 940 -115 800 -115 800 -1070 {dash=6}
P 10 5 480 -1070 780 -1070 780 -115 480 -115 480 -1070 {dash=6}
P 10 5 320 -1070 460 -1070 460 -35 320 -35 320 -1070 {dash=6}
T {[R] input} 165 -1090 0 0 0.3 0.3 {layer=10}
T {d2s_bias_out: reference current OUT of iref (into an external NMOS sink, 5 uA nominal)} 60 -1290 0 0 0.5 0.5 {}
T {PI (a copy of BP) delivers I_ref; its gate line drives the sources PBNC, PBN, PABN into the NMOS diodes; BN's gate line drives the sinks NBPC, NBP, NABP out of the PMOS diodes.} 60 -1240 0 0 0.3 0.3 {}
T {Mirror tree and diodes. The six diodes are those of d2s_bias_lp and set the bias voltages:} 60 -20 0 0 0.3 0.3 {layer=10}
T {   vbp: BP 5u/6u, 5 uA (unit tails).  vbpc: BPC 1u/4u, 2 uA (mirror cascodes).  vabp: RP2 on RP1, 5 uA (ABP, FPL).} 60 4 0 0 0.3 0.3 {layer=10}
T {   vbn: BN 6u/6u, 5 uA (fold sinks).  vbnc: BNC 1u/8u, 2 uA (fold cascodes).  vabn: RN2 on RN1, 5 uA (ABN, FNL).} 60 28 0 0 0.3 0.3 {layer=10}
T {PMOS gate lines come from PMOS diodes on vdd, NMOS gate lines from NMOS diodes on vss: bias crosses blocks as currents.} 60 52 0 0 0.3 0.3 {layer=10}
T {RP1 and RN1 are the class-AB replicas of OP and ON: they sit on the output-stage rails vddo / vsso (separate rails} 60 76 0 0 0.3 0.3 {layer=10}
T {   from the right). RP2 keeps its n-well on vdd, like ABP. RN1 needs a local substrate tap ring on vsso, like ON.} 60 100 0 0 0.3 0.3 {layer=10}
T {[8] PMOS diodes, NMOS sinks} 965 -1090 0 0 0.3 0.3 {layer=10}
T {[8] vabp} 805 -1090 0 0 0.3 0.3 {layer=10}
T {[8] PMOS sources, NMOS diodes} 485 -1090 0 0 0.3 0.3 {layer=10}
T {[8] vabn} 325 -1090 0 0 0.3 0.3 {layer=10}
N 60 -1000 200 -1000 {lab=vdd}
N 60 -560 220 -560 {lab=iref}
N 200 -1000 200 -920 {lab=vdd}
N 200 -920 220 -920 {lab=vdd}
N 220 -1000 220 -950 {lab=vdd}
N 220 -890 220 -560 {lab=iref}
N 220 -560 260 -560 {lab=iref}
N 260 -920 260 -560 {lab=iref}
N 820 -1000 820 -800 {lab=vdd}
N 820 -1000 1000 -1000 {lab=vdd}
N 820 -800 860 -800 {lab=vdd}
N 820 -380 820 -200 {lab=vbn}
N 840 -1040 840 -920 {lab=vddo}
N 840 -1040 860 -1040 {lab=vddo}
N 840 -920 860 -920 {lab=vddo}
N 860 -1040 860 -950 {lab=vddo}
N 860 -890 860 -860 {lab=n1}
N 860 -860 860 -830 {lab=n1}
N 860 -860 900 -860 {lab=n1}
N 860 -770 860 -660 {lab=vabp}
N 860 -660 860 -230 {lab=vabp}
N 860 -660 900 -660 {lab=vabp}
N 860 -200 880 -200 {lab=vss}
N 860 -170 860 -100 {lab=vss}
N 860 -100 880 -100 {lab=vss}
N 880 -200 880 -100 {lab=vss}
N 880 -100 1020 -100 {lab=vss}
N 900 -920 900 -860 {lab=n1}
N 900 -800 900 -660 {lab=vabp}
N 980 -380 980 -200 {lab=vbn}
N 980 -380 1140 -380 {lab=vbn}
N 1000 -1000 1000 -920 {lab=vdd}
N 1000 -1000 1020 -1000 {lab=vdd}
N 1000 -920 1020 -920 {lab=vdd}
N 1020 -1000 1020 -950 {lab=vdd}
N 1020 -1000 1160 -1000 {lab=vdd}
N 1020 -890 1020 -700 {lab=vbpc}
N 1020 -700 1020 -230 {lab=vbpc}
N 1020 -200 1040 -200 {lab=vss}
N 1020 -170 1020 -100 {lab=vss}
N 1020 -100 1040 -100 {lab=vss}
N 1040 -200 1040 -100 {lab=vss}
N 1060 -920 1060 -700 {lab=vbpc}
N 1140 -380 1140 -200 {lab=vbn}
N 1160 -1000 1160 -920 {lab=vdd}
N 1160 -1000 1180 -1000 {lab=vdd}
N 1160 -920 1180 -920 {lab=vdd}
N 1180 -1000 1180 -950 {lab=vdd}
N 1180 -890 1180 -740 {lab=vbp}
N 1180 -740 1180 -230 {lab=vbp}
N 1180 -740 1220 -740 {lab=vbp}
N 1180 -200 1200 -200 {lab=vss}
N 1180 -170 1180 -100 {lab=vss}
N 1180 -100 1200 -100 {lab=vss}
N 1200 -200 1200 -100 {lab=vss}
N 1220 -920 1220 -740 {lab=vbp}
N 360 -920 360 -560 {lab=iref}
N 360 -560 500 -560 {lab=iref}
N 360 -320 360 -100 {lab=vss}
N 360 -320 400 -320 {lab=vss}
N 360 -100 520 -100 {lab=vss}
N 380 -200 380 -60 {lab=vsso}
N 380 -200 400 -200 {lab=vsso}
N 380 -60 400 -60 {lab=vsso}
N 400 -1000 400 -950 {lab=vdd}
N 400 -1000 420 -1000 {lab=vdd}
N 400 -920 420 -920 {lab=vdd}
N 400 -890 400 -460 {lab=vabn}
N 400 -460 400 -350 {lab=vabn}
N 400 -460 440 -460 {lab=vabn}
N 400 -290 400 -260 {lab=n2}
N 400 -260 400 -230 {lab=n2}
N 400 -260 440 -260 {lab=n2}
N 400 -170 400 -60 {lab=vsso}
N 420 -1000 420 -920 {lab=vdd}
N 420 -1000 540 -1000 {lab=vdd}
N 440 -260 440 -200 {lab=n2}
N 500 -920 500 -560 {lab=iref}
N 500 -560 660 -560 {lab=iref}
N 520 -200 520 -100 {lab=vss}
N 520 -200 540 -200 {lab=vss}
N 520 -100 540 -100 {lab=vss}
N 540 -1000 540 -950 {lab=vdd}
N 540 -1000 560 -1000 {lab=vdd}
N 540 -920 560 -920 {lab=vdd}
N 540 -890 540 -420 {lab=vbnc}
N 540 -420 540 -230 {lab=vbnc}
N 540 -420 580 -420 {lab=vbnc}
N 540 -170 540 -100 {lab=vss}
N 540 -100 680 -100 {lab=vss}
N 560 -1000 560 -920 {lab=vdd}
N 560 -1000 700 -1000 {lab=vdd}
N 580 -420 580 -200 {lab=vbnc}
N 660 -920 660 -560 {lab=iref}
N 680 -200 680 -100 {lab=vss}
N 680 -200 700 -200 {lab=vss}
N 680 -100 700 -100 {lab=vss}
N 700 -1000 700 -950 {lab=vdd}
N 700 -1000 720 -1000 {lab=vdd}
N 700 -920 720 -920 {lab=vdd}
N 700 -890 700 -380 {lab=vbn}
N 700 -380 700 -230 {lab=vbn}
N 700 -170 700 -100 {lab=vss}
N 720 -1000 720 -920 {lab=vdd}
N 740 -380 740 -200 {lab=vbn}
N 60 -1040 840 -1040 {lab=vddo}
N 60 -60 380 -60 {lab=vsso}
N 720 -1000 820 -1000 {lab=vdd}
N 220 -1000 400 -1000 {lab=vdd}
N 200 -1000 220 -1000 {lab=vdd}
N 1040 -100 1180 -100 {lab=vss}
N 700 -100 860 -100 {lab=vss}
N 60 -100 360 -100 {lab=vss}
N 1220 -740 1300 -740 {lab=vbp}
N 1060 -700 1300 -700 {lab=vbpc}
N 1020 -700 1060 -700 {lab=vbpc}
N 900 -660 1300 -660 {lab=vabp}
N 1140 -380 1300 -380 {lab=vbn}
N 820 -380 980 -380 {lab=vbn}
N 740 -380 820 -380 {lab=vbn}
N 700 -380 740 -380 {lab=vbn}
N 580 -420 1300 -420 {lab=vbnc}
N 440 -460 1300 -460 {lab=vabn}
N 440 -460 440 -320 {lab=vabn}
N 260 -560 360 -560 {lab=iref}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 240 -920 0 1 {name=PI
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/title.sym} 170 200 0 0 {name=l0 author="Christoph Maier"}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1040 -920 0 1 {name=BPC
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1000 -200 0 0 {name=NBPC
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 1020 -700 0 0 {name=l1 sig_type=std_logic lab=vbpc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1200 -920 0 1 {name=BP
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1160 -200 0 0 {name=NBP
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 1180 -740 0 0 {name=l2 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 880 -920 0 1 {name=RP1
l=0.6u
w=13.32u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 880 -800 0 1 {name=RP2
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 860 -845 0 1 {name=l3 sig_type=std_logic lab=n1}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 840 -200 0 0 {name=NABP
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 860 -660 0 0 {name=l4 sig_type=std_logic lab=vabp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 520 -920 0 0 {name=PBNC
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 560 -200 0 1 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 540 -420 0 0 {name=l5 sig_type=std_logic lab=vbnc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 680 -920 0 0 {name=PBN
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 720 -200 0 1 {name=BN
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 700 -380 0 0 {name=l6 sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -920 0 0 {name=PABN
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 420 -320 0 1 {name=RN2
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 420 -200 0 1 {name=RN1
l=1u
w=8.8u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 400 -275 0 1 {name=l7 sig_type=std_logic lab=n2}
C {devices/lab_wire.sym} 400 -460 0 0 {name=l8 sig_type=std_logic lab=vabn}
C {devices/iopin.sym} 60 -1000 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 60 -100 0 1 {name=p2 lab=vss}
C {devices/iopin.sym} 60 -1040 0 1 {name=p3 lab=vddo}
C {devices/iopin.sym} 60 -60 0 1 {name=p4 lab=vsso}
C {devices/iopin.sym} 60 -560 0 1 {name=p5 lab=iref}
C {devices/opin.sym} 1300 -740 0 0 {name=p6 lab=vbp}
C {devices/opin.sym} 1300 -380 0 0 {name=p7 lab=vbn}
C {devices/opin.sym} 1300 -700 0 0 {name=p8 lab=vbpc}
C {devices/opin.sym} 1300 -420 0 0 {name=p9 lab=vbnc}
C {devices/opin.sym} 1300 -660 0 0 {name=p10 lab=vabp}
C {devices/opin.sym} 1300 -460 0 0 {name=p11 lab=vabn}
