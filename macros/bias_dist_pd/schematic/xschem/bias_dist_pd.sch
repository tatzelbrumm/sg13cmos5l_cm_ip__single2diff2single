v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 1010 -1600 1530 -1600 1530 220 1010 220 1010 -1600 {dash=6}
P 10 5 1550 -1600 2170 -1600 2170 -1400 1550 -1400 1550 -1600 {dash=6}
T {bias_dist_pd: switchable distribution mirror, 4 sourced inputs -> 4 sourced outputs (1 : 1), digital enable en_3v3} 100 -1850 0 0 0.4 0.4 {}
T {Enabled inputs (en_in<k> = 1) add up in NI; NM copies the sum into the PMOS diode PD; each enabled output PO<j> sources it through its TG.} 100 -1796 0 0 0.25 0.25 {}
T {iout<j> feeds a bias_tree_pd (NMOS input diode NI behind its own TG), e.g. one per pad; a disabled output's TG is open and PO<j> carries no current.} 100 -1772 0 0 0.25 0.25 {}
T {en_3v3 = 0: all TGs open, TDN pulls ni to vssh, SVPD pulls vpd to vddh. Devices as in bias_tree_pd (NI 6u/6u, BP 5u/6u, switches 1u/0.45u). Source: netlist/source/bias_dist_pd.spice} 100 -1748 0 0 0.25 0.25 {}
T {Legs: one bdp_slice per input and output (nand2_hv | inv_hv | tg_hv, as the layout cell); en_out<j> and en_3v3 join the output slices by name. [M] [O] analog: mirror, PMOS outputs.} 100 -1724 0 0 0.25 0.25 {}
T {[M] mirror} 1015 -1623.5 0 0 0.35 0.35 {layer=10}
T {[O] PMOS outputs} 2146 -1623.5 0 0 0.35 0.35 {layer=10}
N 980 0 1350 0 {lab=ni}
N 1060 90 1060 0 {lab=ni}
N 1260 90 1260 0 {lab=ni}
N 1300 120 1400 120 {lab=ni}
N 1350 120 1350 0 {lab=ni}
N 1060 150 1060 260 {lab=vssh}
N 1060 120 1080 120 {lab=vssh}
N 1080 120 1080 260 {lab=vssh}
N 1260 150 1260 260 {lab=vssh}
N 1260 120 1240 120 {lab=vssh}
N 1240 120 1240 260 {lab=vssh}
N 1440 150 1440 260 {lab=vssh}
N 1440 120 1460 120 {lab=vssh}
N 1460 120 1460 260 {lab=vssh}
N 100 120 1020 120 {lab=en_3v3_b}
N 1440 -1570 1440 -1640 {lab=vddh}
N 1440 -1540 1460 -1540 {lab=vddh}
N 1460 -1540 1460 -1640 {lab=vddh}
N 1280 -1570 1280 -1640 {lab=vddh}
N 1280 -1540 1300 -1540 {lab=vddh}
N 1300 -1540 1300 -1640 {lab=vddh}
N 1440 -1510 1440 90 {lab=vpd}
N 1400 -1540 1380 -1540 {lab=vpd}
N 1380 -1540 1380 -1440 {lab=vpd}
N 1280 -1510 1280 -1440 {lab=vpd}
N 100 -1540 1240 -1540 {lab=en_3v3}
N 1280 -1440 1440 -1440 {lab=vpd}
N 1440 -1440 2060 -1440 {lab=vpd}
N 2120 -1570 2120 -1640 {lab=vddh}
N 2120 -1540 2140 -1540 {lab=vddh}
N 2140 -1540 2140 -1640 {lab=vddh}
N 2080 -1540 2060 -1540 {lab=vpd}
N 2060 -1540 2060 -1440 {lab=vpd}
N 2120 -1510 2120 -1290 {lab=po0}
N 2120 -1290 2480 -1290 {lab=po0}
N 1960 -1570 1960 -1640 {lab=vddh}
N 1960 -1540 1980 -1540 {lab=vddh}
N 1980 -1540 1980 -1640 {lab=vddh}
N 1920 -1540 1900 -1540 {lab=vpd}
N 1900 -1540 1900 -1440 {lab=vpd}
N 1960 -1510 1960 -970 {lab=po1}
N 1960 -970 2480 -970 {lab=po1}
N 1800 -1570 1800 -1640 {lab=vddh}
N 1800 -1540 1820 -1540 {lab=vddh}
N 1820 -1540 1820 -1640 {lab=vddh}
N 1760 -1540 1740 -1540 {lab=vpd}
N 1740 -1540 1740 -1440 {lab=vpd}
N 1800 -1510 1800 -650 {lab=po2}
N 1800 -650 2480 -650 {lab=po2}
N 1640 -1570 1640 -1640 {lab=vddh}
N 1640 -1540 1660 -1540 {lab=vddh}
N 1660 -1540 1660 -1640 {lab=vddh}
N 1600 -1540 1580 -1540 {lab=vpd}
N 1580 -1540 1580 -1440 {lab=vpd}
N 1640 -1510 1640 -330 {lab=po3}
N 1640 -330 2480 -330 {lab=po3}
C {devices/iopin.sym} 100 -1640 0 1 {name=p0 lab=vddh}
C {devices/iopin.sym} 100 260 0 1 {name=p1 lab=vssh}
C {devices/ipin.sym} 100 -1540 0 0 {name=p2 lab=en_3v3}
C {devices/ipin.sym} 100 120 0 0 {name=p3 lab=en_3v3_b}
C {devices/iopin.sym} 100 -1380 0 1 {name=piin0 lab=iin0}
C {devices/iopin.sym} 100 -1040 0 1 {name=piin1 lab=iin1}
C {devices/iopin.sym} 100 -700 0 1 {name=piin2 lab=iin2}
C {devices/iopin.sym} 100 -360 0 1 {name=piin3 lab=iin3}
C {devices/ipin.sym} 100 -1420 0 0 {name=pen_in0 lab=en_in0}
C {devices/ipin.sym} 100 -1080 0 0 {name=pen_in1 lab=en_in1}
C {devices/ipin.sym} 100 -740 0 0 {name=pen_in2 lab=en_in2}
C {devices/ipin.sym} 100 -400 0 0 {name=pen_in3 lab=en_in3}
C {devices/opin.sym} 2760 -1290 0 0 {name=piout0 lab=iout0}
C {devices/opin.sym} 2760 -970 0 0 {name=piout1 lab=iout1}
C {devices/opin.sym} 2760 -650 0 0 {name=piout2 lab=iout2}
C {devices/opin.sym} 2760 -330 0 0 {name=piout3 lab=iout3}
C {devices/ipin.sym} 100 -80 0 0 {name=p14 lab=en_out0}
C {devices/ipin.sym} 100 -40 0 0 {name=p15 lab=en_out1}
C {devices/ipin.sym} 100 0 0 0 {name=p16 lab=en_out2}
C {devices/ipin.sym} 100 40 0 0 {name=p17 lab=en_out3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1040 120 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 120 0 1 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1420 120 0 0 {name=NM
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1420 -1540 0 0 {name=PD
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1260 -1540 0 0 {name=SVPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2100 -1540 0 0 {name=PO0
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1940 -1540 0 0 {name=PO1
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1780 -1540 0 0 {name=PO2
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1620 -1540 0 0 {name=PO3
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_wire.sym} 1360 -1440 0 0 {name=l8 sig_type=std_logic lab=vpd}
C {devices/title.sym} 160 340 0 0 {name=l0 author="Christoph Maier"}
P 10 5 1580 -110 1880 -110 1880 235 1580 235 1580 -110 {dash=6}
T {[DM] layout dummies} 1585 -133.5 0 0 0.35 0.35 {layer=10}
T {as drawn in the rows (pad convention):} 1590 -95 0 0 0.2 0.2 {layer=10}
T {D = S = B on the rail, gate as drawn;} 1590 -75 0 0 0.2 0.2 {layer=10}
T {MDP at both ends of PO0 PO1 PD PO2 PO3,} 1590 -55 0 0 0.2 0.2 {layer=10}
T {MDN at both ends of NI NM} 1590 -35 0 0 0.2 0.2 {layer=10}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1700 70 0 0 {name=MDP[1:0]
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 1720 40 1740 40 {lab=vddh}
N 1720 70 1740 70 {lab=vddh}
N 1720 100 1740 100 {lab=vddh}
N 1740 100 1740 10 {lab=vddh}
C {devices/lab_pin.sym} 1740 10 0 1 {name=ldm0_r sig_type=std_logic lab=vddh}
N 1680 70 1640 70 {lab=vpd}
C {devices/lab_pin.sym} 1640 70 0 0 {name=ldm0_g sig_type=std_logic lab=vpd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1700 180 0 0 {name=MDN[1:0]
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 1720 150 1740 150 {lab=vssh}
N 1720 180 1740 180 {lab=vssh}
N 1720 210 1740 210 {lab=vssh}
N 1740 150 1740 260 {lab=vssh}
N 1680 180 1640 180 {lab=ni}
C {devices/lab_pin.sym} 1640 180 0 0 {name=ldm1_g sig_type=std_logic lab=ni}
N 100 -1640 2140 -1640 {lab=vddh}
N 100 260 1740 260 {lab=vssh}
N 220 -1540 220 -420 {lab=en_3v3}
C {bdp_slice.sym} 500 -1410 0 0 {name=Xsi0}
N 220 -1440 420 -1440 {lab=en_3v3}
N 100 -1420 420 -1420 {lab=en_in0}
N 100 -1380 420 -1380 {lab=iin0}
N 580 -1380 980 -1380 {lab=ni}
N 500 -1480 500 -1500 {lab=vddh}
C {devices/lab_pin.sym} 500 -1500 0 1 {name=lsi0_vdd sig_type=std_logic lab=vddh}
N 500 -1340 500 -1320 {lab=vssh}
C {devices/lab_pin.sym} 500 -1320 0 1 {name=lsi0_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -1070 0 0 {name=Xsi1}
N 220 -1100 420 -1100 {lab=en_3v3}
N 100 -1080 420 -1080 {lab=en_in1}
N 100 -1040 420 -1040 {lab=iin1}
N 580 -1040 980 -1040 {lab=ni}
N 500 -1140 500 -1160 {lab=vddh}
C {devices/lab_pin.sym} 500 -1160 0 1 {name=lsi1_vdd sig_type=std_logic lab=vddh}
N 500 -1000 500 -980 {lab=vssh}
C {devices/lab_pin.sym} 500 -980 0 1 {name=lsi1_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -730 0 0 {name=Xsi2}
N 220 -760 420 -760 {lab=en_3v3}
N 100 -740 420 -740 {lab=en_in2}
N 100 -700 420 -700 {lab=iin2}
N 580 -700 980 -700 {lab=ni}
N 500 -800 500 -820 {lab=vddh}
C {devices/lab_pin.sym} 500 -820 0 1 {name=lsi2_vdd sig_type=std_logic lab=vddh}
N 500 -660 500 -640 {lab=vssh}
C {devices/lab_pin.sym} 500 -640 0 1 {name=lsi2_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -390 0 0 {name=Xsi3}
N 220 -420 420 -420 {lab=en_3v3}
N 100 -400 420 -400 {lab=en_in3}
N 100 -360 420 -360 {lab=iin3}
N 580 -360 980 -360 {lab=ni}
N 500 -460 500 -480 {lab=vddh}
C {devices/lab_pin.sym} 500 -480 0 1 {name=lsi3_vdd sig_type=std_logic lab=vddh}
N 500 -320 500 -300 {lab=vssh}
C {devices/lab_pin.sym} 500 -300 0 1 {name=lsi3_vss sig_type=std_logic lab=vssh}
N 980 -1380 980 0 {lab=ni}
C {devices/lab_wire.sym} 980 -1380 0 1 {name=l7 sig_type=std_logic lab=ni}
C {bdp_slice.sym} 2560 -1320 0 0 {name=Xso0}
N 2480 -1350 2460 -1350 {lab=en_3v3}
C {devices/lab_pin.sym} 2460 -1350 0 0 {name=lso0_en3 sig_type=std_logic lab=en_3v3}
N 2480 -1330 2460 -1330 {lab=en_out0}
C {devices/lab_pin.sym} 2460 -1330 0 0 {name=lso0_en sig_type=std_logic lab=en_out0}
N 2640 -1290 2760 -1290 {lab=iout0}
N 2560 -1390 2560 -1410 {lab=vddh}
C {devices/lab_pin.sym} 2560 -1410 0 1 {name=lso0_vdd sig_type=std_logic lab=vddh}
N 2560 -1250 2560 -1230 {lab=vssh}
C {devices/lab_pin.sym} 2560 -1230 0 1 {name=lso0_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2440 -1290 0 0 {name=lpo0 sig_type=std_logic lab=po0}
C {bdp_slice.sym} 2560 -1000 0 0 {name=Xso1}
N 2480 -1030 2460 -1030 {lab=en_3v3}
C {devices/lab_pin.sym} 2460 -1030 0 0 {name=lso1_en3 sig_type=std_logic lab=en_3v3}
N 2480 -1010 2460 -1010 {lab=en_out1}
C {devices/lab_pin.sym} 2460 -1010 0 0 {name=lso1_en sig_type=std_logic lab=en_out1}
N 2640 -970 2760 -970 {lab=iout1}
N 2560 -1070 2560 -1090 {lab=vddh}
C {devices/lab_pin.sym} 2560 -1090 0 1 {name=lso1_vdd sig_type=std_logic lab=vddh}
N 2560 -930 2560 -910 {lab=vssh}
C {devices/lab_pin.sym} 2560 -910 0 1 {name=lso1_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2440 -970 0 0 {name=lpo1 sig_type=std_logic lab=po1}
C {bdp_slice.sym} 2560 -680 0 0 {name=Xso2}
N 2480 -710 2460 -710 {lab=en_3v3}
C {devices/lab_pin.sym} 2460 -710 0 0 {name=lso2_en3 sig_type=std_logic lab=en_3v3}
N 2480 -690 2460 -690 {lab=en_out2}
C {devices/lab_pin.sym} 2460 -690 0 0 {name=lso2_en sig_type=std_logic lab=en_out2}
N 2640 -650 2760 -650 {lab=iout2}
N 2560 -750 2560 -770 {lab=vddh}
C {devices/lab_pin.sym} 2560 -770 0 1 {name=lso2_vdd sig_type=std_logic lab=vddh}
N 2560 -610 2560 -590 {lab=vssh}
C {devices/lab_pin.sym} 2560 -590 0 1 {name=lso2_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2440 -650 0 0 {name=lpo2 sig_type=std_logic lab=po2}
C {bdp_slice.sym} 2560 -360 0 0 {name=Xso3}
N 2480 -390 2460 -390 {lab=en_3v3}
C {devices/lab_pin.sym} 2460 -390 0 0 {name=lso3_en3 sig_type=std_logic lab=en_3v3}
N 2480 -370 2460 -370 {lab=en_out3}
C {devices/lab_pin.sym} 2460 -370 0 0 {name=lso3_en sig_type=std_logic lab=en_out3}
N 2640 -330 2760 -330 {lab=iout3}
N 2560 -430 2560 -450 {lab=vddh}
C {devices/lab_pin.sym} 2560 -450 0 1 {name=lso3_vdd sig_type=std_logic lab=vddh}
N 2560 -290 2560 -270 {lab=vssh}
C {devices/lab_pin.sym} 2560 -270 0 1 {name=lso3_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2440 -330 0 0 {name=lpo3 sig_type=std_logic lab=po3}
P 10 5 250 -1525 660 -1525 660 -270 250 -270 250 -1525 {dash=6}
T {[S] input slices (bdp_slice)} 255 -1518 0 0 0.35 0.35 {layer=10}
P 10 5 2280 -1440 2700 -1440 2700 -250 2280 -250 2280 -1440 {dash=6}
T {[S] output slices (bdp_slice)} 2285 -1463.5 0 0 0.35 0.35 {layer=10}
