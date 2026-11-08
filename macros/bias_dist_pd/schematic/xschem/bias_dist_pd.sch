v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 1010 -1980 1530 -1980 1530 -160 1010 -160 1010 -1980 {dash=6}
P 10 5 1550 -1980 2170 -1980 2170 -1780 1550 -1780 1550 -1980 {dash=6}
P 10 5 1580 -490 1880 -490 1880 -145 1580 -145 1580 -490 {dash=6}
P 10 5 250 -1705 660 -1705 660 -450 250 -450 250 -1705 {dash=6}
P 10 5 2280 -1830 2700 -1830 2700 -640 2280 -640 2280 -1830 {dash=6}
T {bias_dist_pd: switchable distribution mirror, 4 sourced inputs -> 4 sourced outputs (1 : 1), digital enable en_3v3} 100 -2230 0 0 0.4 0.4 {}
T {Enabled inputs (en_in<k> = 1) add up in NI; NM copies the sum into the PMOS diode PD; each enabled output PO<j> sources it through its TG.} 100 -2176 0 0 0.25 0.25 {}
T {iout<j> feeds a bias_tree_pd (NMOS input diode NI behind its own TG), e.g. one per pad; a disabled output's TG is open and PO<j> carries no current.} 100 -2152 0 0 0.25 0.25 {}
T {en_3v3 = 0: all TGs open, TDN pulls ni to vssh, SVPD pulls vpd to vddh. Devices as in bias_tree_pd (NI 6u/6u, BP 5u/6u, switches 1u/0.45u). Source: netlist/source/bias_dist_pd.spice} 100 -2128 0 0 0.25 0.25 {}
T {Legs: one bdp_slice per input and output (nand2_hv | inv_hv | tg_hv, as the layout cell); en_out<j> and en_3v3 join the output slices by name. [M] [O] analog: mirror, PMOS outputs.} 100 -2104 0 0 0.25 0.25 {}
T {[M] mirror} 1015 -2003.5 0 0 0.35 0.35 {layer=10}
T {[O] PMOS outputs} 2146 -2003.5 0 0 0.35 0.35 {layer=10}
T {[DM] layout dummies} 1585 -513.5 0 0 0.35 0.35 {layer=10}
T {as drawn in the rows (pad convention):} 1590 -475 0 0 0.2 0.2 {layer=10}
T {D = S = B on the rail, gate as drawn;} 1590 -455 0 0 0.2 0.2 {layer=10}
T {MDP at both ends of PO0 PO1 PD PO2 PO3,} 1590 -435 0 0 0.2 0.2 {layer=10}
T {MDN at both ends of NI NM} 1590 -415 0 0 0.2 0.2 {layer=10}
T {[S] input slices (bdp_slice)} 255 -1898 0 0 0.35 0.35 {layer=10}
T {[S] output slices (bdp_slice)} 2285 -1853.5 0 0 0.35 0.35 {layer=10}
N 1260 -380 1350 -380 {lab=ni}
N 1060 -380 1060 -290 {lab=ni}
N 1260 -380 1260 -290 {lab=ni}
N 1350 -260 1400 -260 {lab=ni}
N 1350 -380 1350 -260 {lab=ni}
N 1060 -230 1060 -120 {lab=vssh}
N 1060 -260 1080 -260 {lab=vssh}
N 1080 -260 1080 -120 {lab=vssh}
N 1260 -230 1260 -120 {lab=vssh}
N 1240 -260 1260 -260 {lab=vssh}
N 1240 -260 1240 -120 {lab=vssh}
N 1440 -230 1440 -120 {lab=vssh}
N 1440 -260 1460 -260 {lab=vssh}
N 1460 -260 1460 -120 {lab=vssh}
N 100 -260 1020 -260 {lab=en_3v3_b}
N 1440 -2020 1440 -1950 {lab=vddh}
N 1440 -1920 1460 -1920 {lab=vddh}
N 1460 -2020 1460 -1920 {lab=vddh}
N 1280 -2020 1280 -1950 {lab=vddh}
N 1280 -1920 1300 -1920 {lab=vddh}
N 1300 -2020 1300 -1920 {lab=vddh}
N 1440 -1820 1440 -290 {lab=vpd}
N 1380 -1920 1400 -1920 {lab=vpd}
N 1380 -1920 1380 -1820 {lab=vpd}
N 1280 -1890 1280 -1820 {lab=vpd}
N 220 -1920 1240 -1920 {lab=en_3v3}
N 1380 -1820 1440 -1820 {lab=vpd}
N 1900 -1820 2060 -1820 {lab=vpd}
N 2120 -2020 2120 -1950 {lab=vddh}
N 2120 -1920 2140 -1920 {lab=vddh}
N 2140 -2020 2140 -1920 {lab=vddh}
N 2060 -1920 2080 -1920 {lab=vpd}
N 2060 -1920 2060 -1820 {lab=vpd}
N 2120 -1680 2480 -1680 {lab=po0}
N 1960 -2020 1960 -1950 {lab=vddh}
N 1960 -1920 1980 -1920 {lab=vddh}
N 1980 -2020 1980 -1920 {lab=vddh}
N 1900 -1920 1920 -1920 {lab=vpd}
N 1900 -1920 1900 -1820 {lab=vpd}
N 1960 -1360 2480 -1360 {lab=po1}
N 1800 -2020 1800 -1950 {lab=vddh}
N 1800 -1920 1820 -1920 {lab=vddh}
N 1820 -2020 1820 -1920 {lab=vddh}
N 1740 -1920 1760 -1920 {lab=vpd}
N 1740 -1920 1740 -1820 {lab=vpd}
N 1800 -1040 2480 -1040 {lab=po2}
N 1640 -2020 1640 -1950 {lab=vddh}
N 1640 -1920 1660 -1920 {lab=vddh}
N 1660 -2020 1660 -1920 {lab=vddh}
N 1580 -1920 1600 -1920 {lab=vpd}
N 1580 -1920 1580 -1820 {lab=vpd}
N 1640 -720 2480 -720 {lab=po3}
N 1720 -340 1740 -340 {lab=vddh}
N 1720 -310 1740 -310 {lab=vddh}
N 1720 -280 1740 -280 {lab=vddh}
N 1740 -310 1740 -280 {lab=vddh}
N 1640 -310 1680 -310 {lab=vpd}
N 1720 -230 1740 -230 {lab=vssh}
N 1720 -200 1740 -200 {lab=vssh}
N 1720 -170 1740 -170 {lab=vssh}
N 1740 -170 1740 -120 {lab=vssh}
N 1640 -200 1680 -200 {lab=ni}
N 2120 -2020 2140 -2020 {lab=vddh}
N 1460 -120 1740 -120 {lab=vssh}
N 220 -1620 420 -1620 {lab=en_3v3}
N 100 -1600 420 -1600 {lab=en_in0}
N 100 -1560 420 -1560 {lab=iin0}
N 580 -1560 980 -1560 {lab=ni}
N 500 -1520 500 -1500 {lab=vssh}
N 220 -1280 420 -1280 {lab=en_3v3}
N 100 -1260 420 -1260 {lab=en_in1}
N 100 -1220 420 -1220 {lab=iin1}
N 580 -1220 980 -1220 {lab=ni}
N 500 -1340 500 -1320 {lab=vddh}
N 500 -1180 500 -1160 {lab=vssh}
N 220 -940 420 -940 {lab=en_3v3}
N 100 -920 420 -920 {lab=en_in2}
N 100 -880 420 -880 {lab=iin2}
N 580 -880 980 -880 {lab=ni}
N 500 -1000 500 -980 {lab=vddh}
N 500 -840 500 -820 {lab=vssh}
N 220 -600 420 -600 {lab=en_3v3}
N 100 -580 420 -580 {lab=en_in3}
N 100 -540 420 -540 {lab=iin3}
N 580 -540 980 -540 {lab=ni}
N 500 -660 500 -640 {lab=vddh}
N 500 -500 500 -480 {lab=vssh}
N 2640 -1680 2760 -1680 {lab=iout0}
N 2560 -1800 2560 -1780 {lab=vddh}
N 2560 -1640 2560 -1620 {lab=vssh}
N 2640 -1360 2760 -1360 {lab=iout1}
N 2560 -1480 2560 -1460 {lab=vddh}
N 2560 -1320 2560 -1300 {lab=vssh}
N 2640 -1040 2760 -1040 {lab=iout2}
N 2560 -1160 2560 -1140 {lab=vddh}
N 2560 -1000 2560 -980 {lab=vssh}
N 2640 -720 2760 -720 {lab=iout3}
N 2560 -840 2560 -820 {lab=vddh}
N 2560 -680 2560 -660 {lab=vssh}
N 980 -380 1060 -380 {lab=ni}
N 1060 -380 1260 -380 {lab=ni}
N 1300 -260 1350 -260 {lab=ni}
N 100 -120 1060 -120 {lab=vssh}
N 1060 -120 1080 -120 {lab=vssh}
N 1240 -120 1260 -120 {lab=vssh}
N 1080 -120 1240 -120 {lab=vssh}
N 1260 -120 1440 -120 {lab=vssh}
N 1440 -120 1460 -120 {lab=vssh}
N 1300 -2020 1440 -2020 {lab=vddh}
N 1440 -2020 1460 -2020 {lab=vddh}
N 100 -2020 1280 -2020 {lab=vddh}
N 1280 -2020 1300 -2020 {lab=vddh}
N 1280 -1820 1380 -1820 {lab=vpd}
N 1440 -1890 1440 -1820 {lab=vpd}
N 1980 -2020 2120 -2020 {lab=vddh}
N 1820 -2020 1960 -2020 {lab=vddh}
N 1960 -2020 1980 -2020 {lab=vddh}
N 1740 -1820 1900 -1820 {lab=vpd}
N 1660 -2020 1800 -2020 {lab=vddh}
N 1800 -2020 1820 -2020 {lab=vddh}
N 1580 -1820 1740 -1820 {lab=vpd}
N 1460 -2020 1640 -2020 {lab=vddh}
N 1640 -2020 1660 -2020 {lab=vddh}
N 1440 -1820 1580 -1820 {lab=vpd}
N 1740 -370 1740 -340 {lab=vddh}
N 1740 -340 1740 -310 {lab=vddh}
N 1740 -230 1740 -200 {lab=vssh}
N 1740 -200 1740 -170 {lab=vssh}
N 100 -1920 220 -1920 {lab=en_3v3}
N 980 -1560 980 -1220 {lab=ni}
N 980 -1220 980 -880 {lab=ni}
N 980 -880 980 -540 {lab=ni}
N 500 -1880 500 -1660 {lab=vddh}
N 980 -540 980 -380 {lab=ni}
N 220 -1740 2480 -1740 {lab=en_3v3}
N 220 -1740 220 -1620 {lab=en_3v3}
N 220 -1420 2480 -1420 {lab=en_3v3}
N 220 -1420 220 -1280 {lab=en_3v3}
N 220 -1100 2480 -1100 {lab=en_3v3}
N 220 -1100 220 -940 {lab=en_3v3}
N 220 -780 2480 -780 {lab=en_3v3}
N 220 -780 220 -600 {lab=en_3v3}
N 2120 -1890 2120 -1680 {lab=po0}
N 1960 -1890 1960 -1360 {lab=po1}
N 1800 -1890 1800 -1040 {lab=po2}
N 1640 -1890 1640 -720 {lab=po3}
N 220 -1920 220 -1740 {lab=en_3v3}
N 220 -1620 220 -1420 {lab=en_3v3}
N 220 -1280 220 -1100 {lab=en_3v3}
N 220 -940 220 -780 {lab=en_3v3}
N 100 -1720 2480 -1720 {lab=en_out0}
N 100 -1400 2480 -1400 {lab=en_out1}
N 100 -1080 2480 -1080 {lab=en_out2}
N 100 -760 2480 -760 {lab=en_out3}
C {devices/iopin.sym} 100 -2020 0 1 {name=p0 lab=vddh}
C {devices/iopin.sym} 100 -120 0 1 {name=p1 lab=vssh}
C {devices/ipin.sym} 100 -1920 0 0 {name=p2 lab=en_3v3}
C {devices/ipin.sym} 100 -260 0 0 {name=p3 lab=en_3v3_b}
C {devices/iopin.sym} 100 -1560 0 1 {name=piin0 lab=iin0}
C {devices/iopin.sym} 100 -1220 0 1 {name=piin1 lab=iin1}
C {devices/iopin.sym} 100 -880 0 1 {name=piin2 lab=iin2}
C {devices/iopin.sym} 100 -540 0 1 {name=piin3 lab=iin3}
C {devices/ipin.sym} 100 -1600 0 0 {name=pen_in0 lab=en_in0}
C {devices/ipin.sym} 100 -1260 0 0 {name=pen_in1 lab=en_in1}
C {devices/ipin.sym} 100 -920 0 0 {name=pen_in2 lab=en_in2}
C {devices/ipin.sym} 100 -580 0 0 {name=pen_in3 lab=en_in3}
C {devices/opin.sym} 2760 -1680 0 0 {name=piout0 lab=iout0}
C {devices/opin.sym} 2760 -1360 0 0 {name=piout1 lab=iout1}
C {devices/opin.sym} 2760 -1040 0 0 {name=piout2 lab=iout2}
C {devices/opin.sym} 2760 -720 0 0 {name=piout3 lab=iout3}
C {devices/ipin.sym} 100 -1720 0 0 {name=p14 lab=en_out0}
C {devices/ipin.sym} 100 -1400 0 0 {name=p15 lab=en_out1}
C {devices/ipin.sym} 100 -1080 0 0 {name=p16 lab=en_out2}
C {devices/ipin.sym} 100 -760 0 0 {name=p17 lab=en_out3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1040 -260 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 -260 0 1 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1420 -260 0 0 {name=NM
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1420 -1920 0 0 {name=PD
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1260 -1920 0 0 {name=SVPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2100 -1920 0 0 {name=PO0
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1940 -1920 0 0 {name=PO1
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1780 -1920 0 0 {name=PO2
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1620 -1920 0 0 {name=PO3
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_wire.sym} 1360 -1820 0 0 {name=l8 sig_type=std_logic lab=vpd}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1700 -310 0 0 {name=MDP[1:0]
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1740 -370 0 1 {name=ldm0_r sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 1640 -310 0 0 {name=ldm0_g sig_type=std_logic lab=vpd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1700 -200 0 0 {name=MDN[1:0]
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1640 -200 0 0 {name=ldm1_g sig_type=std_logic lab=ni}
C {bdp_slice.sym} 500 -1590 0 0 {name=Xsi0}
C {devices/lab_pin.sym} 500 -1880 0 1 {name=lsi0_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 500 -1500 0 1 {name=lsi0_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -1250 0 0 {name=Xsi1}
C {devices/lab_pin.sym} 500 -1340 0 1 {name=lsi1_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 500 -1160 0 1 {name=lsi1_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -910 0 0 {name=Xsi2}
C {devices/lab_pin.sym} 500 -1000 0 1 {name=lsi2_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 500 -820 0 1 {name=lsi2_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -570 0 0 {name=Xsi3}
C {devices/lab_pin.sym} 500 -660 0 1 {name=lsi3_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 500 -480 0 1 {name=lsi3_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 980 -1560 0 1 {name=l7 sig_type=std_logic lab=ni}
C {bdp_slice.sym} 2560 -1710 0 0 {name=Xso0}
C {devices/lab_pin.sym} 2460 -1740 0 0 {name=lso0_en3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2460 -1720 0 0 {name=lso0_en sig_type=std_logic lab=en_out0}
C {devices/lab_pin.sym} 2560 -1800 0 1 {name=lso0_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2560 -1620 0 1 {name=lso0_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2440 -1680 0 0 {name=lpo0 sig_type=std_logic lab=po0}
C {bdp_slice.sym} 2560 -1390 0 0 {name=Xso1}
C {devices/lab_pin.sym} 2460 -1420 0 0 {name=lso1_en3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2460 -1400 0 0 {name=lso1_en sig_type=std_logic lab=en_out1}
C {devices/lab_pin.sym} 2560 -1480 0 1 {name=lso1_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2560 -1300 0 1 {name=lso1_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2440 -1360 0 0 {name=lpo1 sig_type=std_logic lab=po1}
C {bdp_slice.sym} 2560 -1070 0 0 {name=Xso2}
C {devices/lab_pin.sym} 2460 -1100 0 0 {name=lso2_en3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2460 -1080 0 0 {name=lso2_en sig_type=std_logic lab=en_out2}
C {devices/lab_pin.sym} 2560 -1160 0 1 {name=lso2_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2560 -980 0 1 {name=lso2_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2440 -1040 0 0 {name=lpo2 sig_type=std_logic lab=po2}
C {bdp_slice.sym} 2560 -750 0 0 {name=Xso3}
C {devices/lab_pin.sym} 2460 -780 0 0 {name=lso3_en3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2460 -760 0 0 {name=lso3_en sig_type=std_logic lab=en_out3}
C {devices/lab_pin.sym} 2560 -840 0 1 {name=lso3_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2560 -660 0 1 {name=lso3_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2440 -720 0 0 {name=lpo3 sig_type=std_logic lab=po3}
