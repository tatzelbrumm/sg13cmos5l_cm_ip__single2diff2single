v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 485 -950 875 -950 875 -140 485 -140 485 -950 {dash=6}
P 10 5 130 -760 470 -760 470 -140 130 -140 130 -760 {dash=6}
P 10 5 372 -950 476 -950 476 -830 372 -830 372 -950 {dash=6}
T {bias_tree_rb: the lines ni / vbp / vbnc of both replica blocks, shared in pad_ref_rb} 100 -1302 0 0 0.6 0.6 {}
T {bias_tree_rb: the lines of both replica blocks, as bias_tree_pd at the pad devices' current densities.} 100 -1232 0 0 0.25 0.25 {}
T {  ni   = NI, 6u/6u NMOS diode carrying the reference (= the pads' BN density: 5 uA in 6u/6u)} 100 -1210 0 0 0.25 0.25 {}
T {  vbp  = BP, 2u/6u PMOS diode at 2 uA from NBP 2.4u/6u (= the pads' BP density: 5 uA in 5u/6u)} 100 -1188 0 0 0.25 0.25 {}
T {  vbnc = BNC, 1u/8u NMOS diode at 2 uA from PBNC 2u/6u (= the pads' BNC)} 100 -1166 0 0 0.25 0.25 {}
T {Disabled (en_3v3 = 0): TGN / TGP open the reference, TDN pulls ni to vss; BP pulls vbp to vdd, BNC vbnc to vss.} 100 -1144 0 0 0.25 0.25 {}
T {TGP: drain ni, source iref as drawn by Christoph (2026-11-07, b4cd2288); a transmission gate is symmetric.} 100 -1122 0 0 0.25 0.25 {}
T {drawn from netlist/source/pad_ref_rb.spice (subckt bias_tree_rb); cut from vref_s2d_rb.sch as Christoph drew it (d0638017)} 100 -1090 0 0 0.25 0.25 {}
T {[1] reference input} 135 -783.5 0 0 0.35 0.35 {layer=10}
T {[2] lines} 585 -973.5 0 0 0.35 0.35 {layer=10}
T {[3] layout dummy} 375 -973.5 0 0 0.35 0.35 {layer=10}
N 340 -720 340 -670 {lab=iref}
N 220 -720 220 -550 {lab=iref}
N 340 -320 340 -300 {lab=ni}
N 220 -320 340 -320 {lab=ni}
N 220 -220 240 -220 {lab=vss}
N 220 -490 220 -320 {lab=ni}
N 340 -610 340 -320 {lab=ni}
N 240 -520 240 -220 {lab=vss}
N 220 -320 220 -250 {lab=ni}
N 160 -220 180 -220 {lab=en_3v3_b}
N 220 -190 220 -100 {lab=vss}
N 240 -220 240 -100 {lab=vss}
N 220 -100 240 -100 {lab=vss}
N 340 -300 420 -300 {lab=ni}
N 240 -100 400 -100 {lab=vss}
N 420 -100 580 -100 {lab=vss}
N 220 -720 340 -720 {lab=iref}
N 680 -900 740 -900 {lab=vbp}
N 680 -900 680 -800 {lab=vbp}
N 560 -1000 560 -900 {lab=vdd}
N 800 -1000 800 -900 {lab=vdd}
N 580 -870 580 -800 {lab=vbp}
N 600 -220 600 -100 {lab=vss}
N 780 -630 840 -630 {lab=vbnc}
N 760 -220 760 -100 {lab=vss}
N 620 -900 680 -900 {lab=vbp}
N 580 -800 680 -800 {lab=vbp}
N 780 -1000 800 -1000 {lab=vdd}
N 760 -220 780 -220 {lab=vss}
N 780 -190 780 -100 {lab=vss}
N 760 -100 780 -100 {lab=vss}
N 580 -220 600 -220 {lab=vss}
N 580 -190 580 -100 {lab=vss}
N 780 -900 800 -900 {lab=vdd}
N 780 -1000 780 -930 {lab=vdd}
N 560 -900 580 -900 {lab=vdd}
N 580 -1000 580 -930 {lab=vdd}
N 560 -1000 580 -1000 {lab=vdd}
N 820 -220 840 -220 {lab=vbnc}
N 580 -100 600 -100 {lab=vss}
N 600 -100 760 -100 {lab=vss}
N 520 -220 540 -220 {lab=ni}
N 520 -300 520 -220 {lab=ni}
N 420 -1000 560 -1000 {lab=vdd}
N 580 -1000 780 -1000 {lab=vdd}
N 840 -630 940 -630 {lab=vbnc}
N 840 -630 840 -220 {lab=vbnc}
N 520 -300 940 -300 {lab=ni}
N 420 -300 520 -300 {lab=ni}
N 360 -1000 360 -640 {lab=vdd}
N 780 -630 780 -250 {lab=vbnc}
N 780 -870 780 -630 {lab=vbnc}
N 580 -800 580 -250 {lab=vbp}
N 100 -720 220 -720 {lab=iref}
N 100 -100 220 -100 {lab=vss}
N 100 -1000 360 -1000 {lab=vdd}
N 210 -520 240 -520 {lab=vss}
N 100 -520 180 -520 {lab=en_3v3}
N 160 -640 300 -640 {lab=en_3v3_b}
N 100 -640 160 -640 {lab=en_3v3_b}
N 340 -640 360 -640 {lab=vdd}
N 160 -640 160 -220 {lab=en_3v3_b}
N 680 -800 940 -800 {lab=vbp}
N 420 -300 420 -250 {lab=ni}
N 460 -220 520 -220 {lab=ni}
N 400 -220 420 -220 {lab=vss}
N 400 -220 400 -100 {lab=vss}
N 420 -190 420 -100 {lab=vss}
N 460 -900 480 -900 {lab=vbp}
N 480 -900 480 -800 {lab=vbp}
N 480 -800 580 -800 {lab=vbp}
N 420 -1000 420 -930 {lab=vdd}
N 400 -900 420 -900 {lab=vdd}
N 420 -870 420 -850 {lab=vdd}
N 400 -850 420 -850 {lab=vdd}
N 400 -900 400 -850 {lab=vdd}
N 400 -100 420 -100 {lab=vss}
N 400 -1000 420 -1000 {lab=vdd}
N 400 -1000 400 -900 {lab=vdd}
N 360 -1000 400 -1000 {lab=vdd}
C {devices/iopin.sym} 100 -1000 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -720 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 940 -300 0 0 {name=p3 lab=ni}
C {devices/opin.sym} 940 -800 0 0 {name=p4 lab=vbp}
C {devices/opin.sym} 940 -630 0 0 {name=p5 lab=vbnc}
C {devices/ipin.sym} 100 -520 0 0 {name=p6 lab=en_3v3}
C {devices/ipin.sym} 100 -640 0 0 {name=p7 lab=en_3v3_b}
P 10 5 1040 -470 1300 -470 1300 -290 1040 -290 1040 -470 {dash=6}
T {[3] layout dummies, NMOS tree row (on vss)} 1045 -493.5 0 0 0.35 0.35 {layer=10}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1100 -400 0 0 {name=MDTN6
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 1120 -430 1140 -430 {lab=vss}
N 1120 -400 1140 -400 {lab=vss}
N 1120 -370 1140 -370 {lab=vss}
N 1140 -430 1140 -340 {lab=vss}
C {devices/lab_pin.sym} 1140 -340 0 1 {name=ldn0_r sig_type=std_logic lab=vss}
N 1080 -400 1060 -400 {lab=ni}
C {devices/lab_pin.sym} 1060 -400 0 0 {name=ldn0_g sig_type=std_logic lab=ni}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1240 -400 0 0 {name=MDTN7
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 1260 -430 1280 -430 {lab=vss}
N 1260 -400 1280 -400 {lab=vss}
N 1260 -370 1280 -370 {lab=vss}
N 1280 -430 1280 -340 {lab=vss}
C {devices/lab_pin.sym} 1280 -340 0 1 {name=ldn1_r sig_type=std_logic lab=vss}
N 1220 -400 1200 -400 {lab=ni}
C {devices/lab_pin.sym} 1200 -400 0 0 {name=ldn1_g sig_type=std_logic lab=ni}
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
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 440 -220 0 1 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 160 -220 0 0 {name=l1 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_wire.sym} 400 -300 0 0 {name=l11 sig_type=std_logic lab=ni}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 560 -220 0 0 {name=NBP
l=6u
w=2.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 -900 0 1 {name=BP
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 760 -900 0 0 {name=PBNC
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 800 -220 0 1 {name=BNC
l=8u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 780 -630 0 0 {name=l6 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 680 -800 0 1 {name=l12 sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 440 -900 0 1 {name=MDPBN
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
