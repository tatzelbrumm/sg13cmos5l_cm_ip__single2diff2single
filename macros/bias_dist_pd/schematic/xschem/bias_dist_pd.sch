v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_dist_pd: switchable distribution mirror, 3 sourced inputs -> 4 sourced outputs (1 : 1), digital enable en_3v3} 60 -1180 0 0 0.4 0.4 {}
T {Enabled inputs (en_in<k> = 1) add up in NI; NM copies the sum into the PMOS diode PD; each enabled output PO<j> sources it through its TG.} 60 -1140 0 0 0.25 0.25 {}
T {iout<j> feeds a bias_tree_pd (NMOS input diode NI behind its own TG), e.g. one per pad; a disabled output's TG is open and PO<j> carries no current.} 60 -1116 0 0 0.25 0.25 {}
T {en_3v3 = 0: all TGs open, TDN pulls ni to vss, SVPD pulls vpd to vdd. Devices as in bias_tree_pd (NI 6u/6u, BP 5u/6u, switches 1u/0.45u). Source: netlist/source/bias_dist_pd.spice} 60 -1092 0 0 0.25 0.25 {}
T {[I] input switches} 300 -1020 0 0 0.3 0.3 {layer=10}
T {[M] mirror} 1340 -1020 0 0 0.3 0.3 {layer=10}
T {[O] outputs} 1880 -1020 0 0 0.3 0.3 {layer=10}
T {[E] enable decode} 820 -1020 0 0 0.3 0.3 {layer=10}
C {devices/iopin.sym} 100 -960 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -920 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -880 0 0 {name=p2 lab=en_3v3}
C {devices/ipin.sym} 100 -840 0 0 {name=p3 lab=en_3v3_b}
C {devices/iopin.sym} 100 -800 0 1 {name=p4 lab=iin0}
C {devices/iopin.sym} 100 -760 0 1 {name=p5 lab=iin1}
C {devices/iopin.sym} 100 -720 0 1 {name=p6 lab=iin2}
C {devices/ipin.sym} 100 -680 0 0 {name=p7 lab=en_in0}
C {devices/ipin.sym} 100 -640 0 0 {name=p8 lab=en_in1}
C {devices/ipin.sym} 100 -600 0 0 {name=p9 lab=en_in2}
C {devices/opin.sym} 2900 -900 0 0 {name=p10 lab=iout0}
C {devices/opin.sym} 2900 -740 0 0 {name=p11 lab=iout1}
C {devices/opin.sym} 2900 -580 0 0 {name=p12 lab=iout2}
C {devices/opin.sym} 2900 -420 0 0 {name=p13 lab=iout3}
C {devices/ipin.sym} 100 -560 0 0 {name=p14 lab=en_out0}
C {devices/ipin.sym} 100 -520 0 0 {name=p15 lab=en_out1}
C {devices/ipin.sym} 100 -480 0 0 {name=p16 lab=en_out2}
C {devices/ipin.sym} 100 -440 0 0 {name=p17 lab=en_out3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -900 0 0 {name=TIN0
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -930 0 1 {name=l1 sig_type=std_logic lab=iin0}
C {devices/lab_pin.sym} 420 -870 0 1 {name=l2 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 420 -900 0 1 {name=l3 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -900 0 0 {name=l4 sig_type=std_logic lab=ei0}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -900 0 0 {name=TIP0
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 580 -870 0 1 {name=l5 sig_type=std_logic lab=iin0}
C {devices/lab_pin.sym} 580 -930 0 1 {name=l6 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 580 -900 0 1 {name=l7 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 540 -900 0 0 {name=l8 sig_type=std_logic lab=ei0_b}
C {nand2_hv.sym} 900 -900 0 0 {name=XIA0}
C {devices/lab_pin.sym} 920 -930 0 1 {name=l9 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 900 -870 0 1 {name=l10 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 840 -920 0 0 {name=l11 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 840 -880 0 0 {name=l12 sig_type=std_logic lab=en_in0}
C {devices/lab_pin.sym} 960 -900 0 1 {name=l13 sig_type=std_logic lab=ei0_b}
C {inv_hv.sym} 1100 -900 0 0 {name=XIB0}
C {devices/lab_pin.sym} 1120 -920 0 1 {name=l14 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1100 -880 0 1 {name=l15 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1060 -900 0 0 {name=l16 sig_type=std_logic lab=ei0_b}
C {devices/lab_pin.sym} 1140 -900 0 1 {name=l17 sig_type=std_logic lab=ei0}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -700 0 0 {name=TIN1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -730 0 1 {name=l18 sig_type=std_logic lab=iin1}
C {devices/lab_pin.sym} 420 -670 0 1 {name=l19 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 420 -700 0 1 {name=l20 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -700 0 0 {name=l21 sig_type=std_logic lab=ei1}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -700 0 0 {name=TIP1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 580 -670 0 1 {name=l22 sig_type=std_logic lab=iin1}
C {devices/lab_pin.sym} 580 -730 0 1 {name=l23 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 580 -700 0 1 {name=l24 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 540 -700 0 0 {name=l25 sig_type=std_logic lab=ei1_b}
C {nand2_hv.sym} 900 -700 0 0 {name=XIA1}
C {devices/lab_pin.sym} 920 -730 0 1 {name=l26 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 900 -670 0 1 {name=l27 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 840 -720 0 0 {name=l28 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 840 -680 0 0 {name=l29 sig_type=std_logic lab=en_in1}
C {devices/lab_pin.sym} 960 -700 0 1 {name=l30 sig_type=std_logic lab=ei1_b}
C {inv_hv.sym} 1100 -700 0 0 {name=XIB1}
C {devices/lab_pin.sym} 1120 -720 0 1 {name=l31 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1100 -680 0 1 {name=l32 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1060 -700 0 0 {name=l33 sig_type=std_logic lab=ei1_b}
C {devices/lab_pin.sym} 1140 -700 0 1 {name=l34 sig_type=std_logic lab=ei1}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -500 0 0 {name=TIN2
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -530 0 1 {name=l35 sig_type=std_logic lab=iin2}
C {devices/lab_pin.sym} 420 -470 0 1 {name=l36 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 420 -500 0 1 {name=l37 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 380 -500 0 0 {name=l38 sig_type=std_logic lab=ei2}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -500 0 0 {name=TIP2
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 580 -470 0 1 {name=l39 sig_type=std_logic lab=iin2}
C {devices/lab_pin.sym} 580 -530 0 1 {name=l40 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 580 -500 0 1 {name=l41 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 540 -500 0 0 {name=l42 sig_type=std_logic lab=ei2_b}
C {nand2_hv.sym} 900 -500 0 0 {name=XIA2}
C {devices/lab_pin.sym} 920 -530 0 1 {name=l43 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 900 -470 0 1 {name=l44 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 840 -520 0 0 {name=l45 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 840 -480 0 0 {name=l46 sig_type=std_logic lab=en_in2}
C {devices/lab_pin.sym} 960 -500 0 1 {name=l47 sig_type=std_logic lab=ei2_b}
C {inv_hv.sym} 1100 -500 0 0 {name=XIB2}
C {devices/lab_pin.sym} 1120 -520 0 1 {name=l48 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1100 -480 0 1 {name=l49 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1060 -500 0 0 {name=l50 sig_type=std_logic lab=ei2_b}
C {devices/lab_pin.sym} 1140 -500 0 1 {name=l51 sig_type=std_logic lab=ei2}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1400 -900 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1420 -930 0 1 {name=l52 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 1420 -870 0 1 {name=l53 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1420 -900 0 1 {name=l54 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1380 -900 0 0 {name=l55 sig_type=std_logic lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1400 -700 0 0 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1420 -730 0 1 {name=l56 sig_type=std_logic lab=ni}
C {devices/lab_pin.sym} 1420 -670 0 1 {name=l57 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1420 -700 0 1 {name=l58 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1380 -700 0 0 {name=l59 sig_type=std_logic lab=ni}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1400 -500 0 0 {name=NM
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1420 -530 0 1 {name=l60 sig_type=std_logic lab=vpd}
C {devices/lab_pin.sym} 1420 -470 0 1 {name=l61 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1420 -500 0 1 {name=l62 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1380 -500 0 0 {name=l63 sig_type=std_logic lab=ni}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1600 -700 0 0 {name=PD
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1620 -670 0 1 {name=l64 sig_type=std_logic lab=vpd}
C {devices/lab_pin.sym} 1620 -730 0 1 {name=l65 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1620 -700 0 1 {name=l66 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1580 -700 0 0 {name=l67 sig_type=std_logic lab=vpd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1600 -900 0 0 {name=SVPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1620 -870 0 1 {name=l68 sig_type=std_logic lab=vpd}
C {devices/lab_pin.sym} 1620 -930 0 1 {name=l69 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1620 -900 0 1 {name=l70 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1580 -900 0 0 {name=l71 sig_type=std_logic lab=en_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1900 -900 0 0 {name=PO0
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1920 -870 0 1 {name=l72 sig_type=std_logic lab=po0}
C {devices/lab_pin.sym} 1920 -930 0 1 {name=l73 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1920 -900 0 1 {name=l74 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1880 -900 0 0 {name=l75 sig_type=std_logic lab=vpd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2060 -900 0 0 {name=TON0
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2080 -930 0 1 {name=l76 sig_type=std_logic lab=po0}
C {devices/lab_pin.sym} 2080 -870 0 1 {name=l77 sig_type=std_logic lab=iout0}
C {devices/lab_pin.sym} 2080 -900 0 1 {name=l78 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2040 -900 0 0 {name=l79 sig_type=std_logic lab=eo0}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2220 -900 0 0 {name=TOP0
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2240 -870 0 1 {name=l80 sig_type=std_logic lab=po0}
C {devices/lab_pin.sym} 2240 -930 0 1 {name=l81 sig_type=std_logic lab=iout0}
C {devices/lab_pin.sym} 2240 -900 0 1 {name=l82 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2200 -900 0 0 {name=l83 sig_type=std_logic lab=eo0_b}
C {nand2_hv.sym} 2500 -900 0 0 {name=XOA0}
C {devices/lab_pin.sym} 2520 -930 0 1 {name=l84 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2500 -870 0 1 {name=l85 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2440 -920 0 0 {name=l86 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2440 -880 0 0 {name=l87 sig_type=std_logic lab=en_out0}
C {devices/lab_pin.sym} 2560 -900 0 1 {name=l88 sig_type=std_logic lab=eo0_b}
C {inv_hv.sym} 2700 -900 0 0 {name=XOB0}
C {devices/lab_pin.sym} 2720 -920 0 1 {name=l89 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2700 -880 0 1 {name=l90 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2660 -900 0 0 {name=l91 sig_type=std_logic lab=eo0_b}
C {devices/lab_pin.sym} 2740 -900 0 1 {name=l92 sig_type=std_logic lab=eo0}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1900 -740 0 0 {name=PO1
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1920 -710 0 1 {name=l93 sig_type=std_logic lab=po1}
C {devices/lab_pin.sym} 1920 -770 0 1 {name=l94 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1920 -740 0 1 {name=l95 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1880 -740 0 0 {name=l96 sig_type=std_logic lab=vpd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2060 -740 0 0 {name=TON1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2080 -770 0 1 {name=l97 sig_type=std_logic lab=po1}
C {devices/lab_pin.sym} 2080 -710 0 1 {name=l98 sig_type=std_logic lab=iout1}
C {devices/lab_pin.sym} 2080 -740 0 1 {name=l99 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2040 -740 0 0 {name=l100 sig_type=std_logic lab=eo1}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2220 -740 0 0 {name=TOP1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2240 -710 0 1 {name=l101 sig_type=std_logic lab=po1}
C {devices/lab_pin.sym} 2240 -770 0 1 {name=l102 sig_type=std_logic lab=iout1}
C {devices/lab_pin.sym} 2240 -740 0 1 {name=l103 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2200 -740 0 0 {name=l104 sig_type=std_logic lab=eo1_b}
C {nand2_hv.sym} 2500 -740 0 0 {name=XOA1}
C {devices/lab_pin.sym} 2520 -770 0 1 {name=l105 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2500 -710 0 1 {name=l106 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2440 -760 0 0 {name=l107 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2440 -720 0 0 {name=l108 sig_type=std_logic lab=en_out1}
C {devices/lab_pin.sym} 2560 -740 0 1 {name=l109 sig_type=std_logic lab=eo1_b}
C {inv_hv.sym} 2700 -740 0 0 {name=XOB1}
C {devices/lab_pin.sym} 2720 -760 0 1 {name=l110 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2700 -720 0 1 {name=l111 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2660 -740 0 0 {name=l112 sig_type=std_logic lab=eo1_b}
C {devices/lab_pin.sym} 2740 -740 0 1 {name=l113 sig_type=std_logic lab=eo1}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1900 -580 0 0 {name=PO2
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1920 -550 0 1 {name=l114 sig_type=std_logic lab=po2}
C {devices/lab_pin.sym} 1920 -610 0 1 {name=l115 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1920 -580 0 1 {name=l116 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1880 -580 0 0 {name=l117 sig_type=std_logic lab=vpd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2060 -580 0 0 {name=TON2
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2080 -610 0 1 {name=l118 sig_type=std_logic lab=po2}
C {devices/lab_pin.sym} 2080 -550 0 1 {name=l119 sig_type=std_logic lab=iout2}
C {devices/lab_pin.sym} 2080 -580 0 1 {name=l120 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2040 -580 0 0 {name=l121 sig_type=std_logic lab=eo2}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2220 -580 0 0 {name=TOP2
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2240 -550 0 1 {name=l122 sig_type=std_logic lab=po2}
C {devices/lab_pin.sym} 2240 -610 0 1 {name=l123 sig_type=std_logic lab=iout2}
C {devices/lab_pin.sym} 2240 -580 0 1 {name=l124 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2200 -580 0 0 {name=l125 sig_type=std_logic lab=eo2_b}
C {nand2_hv.sym} 2500 -580 0 0 {name=XOA2}
C {devices/lab_pin.sym} 2520 -610 0 1 {name=l126 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2500 -550 0 1 {name=l127 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2440 -600 0 0 {name=l128 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2440 -560 0 0 {name=l129 sig_type=std_logic lab=en_out2}
C {devices/lab_pin.sym} 2560 -580 0 1 {name=l130 sig_type=std_logic lab=eo2_b}
C {inv_hv.sym} 2700 -580 0 0 {name=XOB2}
C {devices/lab_pin.sym} 2720 -600 0 1 {name=l131 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2700 -560 0 1 {name=l132 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2660 -580 0 0 {name=l133 sig_type=std_logic lab=eo2_b}
C {devices/lab_pin.sym} 2740 -580 0 1 {name=l134 sig_type=std_logic lab=eo2}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1900 -420 0 0 {name=PO3
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1920 -390 0 1 {name=l135 sig_type=std_logic lab=po3}
C {devices/lab_pin.sym} 1920 -450 0 1 {name=l136 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1920 -420 0 1 {name=l137 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1880 -420 0 0 {name=l138 sig_type=std_logic lab=vpd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2060 -420 0 0 {name=TON3
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2080 -450 0 1 {name=l139 sig_type=std_logic lab=po3}
C {devices/lab_pin.sym} 2080 -390 0 1 {name=l140 sig_type=std_logic lab=iout3}
C {devices/lab_pin.sym} 2080 -420 0 1 {name=l141 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2040 -420 0 0 {name=l142 sig_type=std_logic lab=eo3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2220 -420 0 0 {name=TOP3
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2240 -390 0 1 {name=l143 sig_type=std_logic lab=po3}
C {devices/lab_pin.sym} 2240 -450 0 1 {name=l144 sig_type=std_logic lab=iout3}
C {devices/lab_pin.sym} 2240 -420 0 1 {name=l145 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2200 -420 0 0 {name=l146 sig_type=std_logic lab=eo3_b}
C {nand2_hv.sym} 2500 -420 0 0 {name=XOA3}
C {devices/lab_pin.sym} 2520 -450 0 1 {name=l147 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2500 -390 0 1 {name=l148 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2440 -440 0 0 {name=l149 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2440 -400 0 0 {name=l150 sig_type=std_logic lab=en_out3}
C {devices/lab_pin.sym} 2560 -420 0 1 {name=l151 sig_type=std_logic lab=eo3_b}
C {inv_hv.sym} 2700 -420 0 0 {name=XOB3}
C {devices/lab_pin.sym} 2720 -440 0 1 {name=l152 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2700 -400 0 1 {name=l153 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2660 -420 0 0 {name=l154 sig_type=std_logic lab=eo3_b}
C {devices/lab_pin.sym} 2740 -420 0 1 {name=l155 sig_type=std_logic lab=eo3}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
