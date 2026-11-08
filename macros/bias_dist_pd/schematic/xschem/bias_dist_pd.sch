v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 950 -1980 1270 -1980 1270 -160 950 -160 950 -1980 {dash=6}
P 10 5 1290 -1980 1910 -1980 1910 -1780 1290 -1780 1290 -1980 {dash=6}
P 10 5 1320 -490 1620 -490 1620 -145 1320 -145 1320 -490 {dash=6}
P 10 5 250 -1705 660 -1705 660 -450 250 -450 250 -1705 {dash=6}
P 10 5 2260 -1830 2680 -1830 2680 -640 2260 -640 2260 -1830 {dash=6}
P 10 5 1940 -2120 2240 -2120 2240 -1775 1940 -1775 1940 -2120 {dash=6}
T {bias_dist_pd: switchable distribution mirror, 4 sourced inputs -> 4 sourced outputs (1 : 1), digital enable en_3v3} 100 -2230 0 0 0.4 0.4 {}
T {Enabled inputs (en_in<k> = 1) add up in NI; NM copies the sum into the PMOS diode PD; each enabled output PO<j> sources it through its TG.} 100 -2176 0 0 0.25 0.25 {}
T {iout<j> feeds a bias_tree_pd (NMOS input diode NI behind its own TG), e.g. one per pad; a disabled output's TG is open and PO<j> carries no current.} 100 -2152 0 0 0.25 0.25 {}
T {en_3v3 = 0: all TGs open, TDN pulls ni to vssh, SVPD pulls vpd to vddh. Devices as in bias_tree_pd (NI 6u/6u, BP 5u/6u, switches 1u/0.45u). Source: netlist/source/bias_dist_pd.spice} 100 -2128 0 0 0.25 0.25 {}
T {Legs: one bdp_slice per input and output (nand2_hv | inv_hv | tg_hv, as the layout cell); en_out<j> and en_3v3 join the output slices by name. [M] [O] analog: mirror, PMOS outputs.} 100 -2104 0 0 0.25 0.25 {}
T {[M] mirror} 955 -2003.5 0 0 0.35 0.35 {layer=10}
T {[O] PMOS outputs} 1886 -2003.5 0 0 0.35 0.35 {layer=10}
T {[DM] layout dummies} 1325 -513.5 0 0 0.35 0.35 {layer=10}
T {as drawn in the rows (pad convention):} 1330 -475 0 0 0.2 0.2 {layer=10}
T {D = S = B on the rail, gate as drawn;} 1330 -455 0 0 0.2 0.2 {layer=10}
T {MDP at both ends of PO0 PO1 PD PO2 PO3,} 1330 -435 0 0 0.2 0.2 {layer=10}
T {MDN at both ends of NI NM} 1330 -415 0 0 0.2 0.2 {layer=10}
T {[S] input slices (bdp_slice)} 255 -1898 0 0 0.35 0.35 {layer=10}
T {[S] output slices (bdp_slice)} 2265 -1853.5 0 0 0.35 0.35 {layer=10}
T {[DM] layout dummies} 1945 -2143.5 0 0 0.35 0.35 {layer=10}
T {as drawn in the rows (pad convention):} 1950 -2105 0 0 0.2 0.2 {layer=10}
T {D = S = B on the rail, gate as drawn;} 1950 -2085 0 0 0.2 0.2 {layer=10}
T {MDP at both ends of PO0 PO1 PD PO2 PO3,} 1950 -2065 0 0 0.2 0.2 {layer=10}
T {MDN at both ends of NI NM} 1950 -2045 0 0 0.2 0.2 {layer=10}
N 1000 -380 1090 -380 {lab=ni}
N 1000 -380 1000 -290 {lab=ni}
N 1090 -260 1140 -260 {lab=ni}
N 1090 -380 1090 -260 {lab=ni}
N 720 -230 720 -120 {lab=vssh}
N 740 -260 740 -120 {lab=vssh}
N 1000 -230 1000 -120 {lab=vssh}
N 980 -260 1000 -260 {lab=vssh}
N 980 -260 980 -120 {lab=vssh}
N 1180 -230 1180 -120 {lab=vssh}
N 1180 -260 1200 -260 {lab=vssh}
N 1200 -260 1200 -120 {lab=vssh}
N 1180 -2020 1180 -1950 {lab=vddh}
N 1180 -1920 1200 -1920 {lab=vddh}
N 1200 -2020 1200 -1920 {lab=vddh}
N 720 -2020 720 -1950 {lab=vddh}
N 740 -2020 740 -1920 {lab=vddh}
N 1180 -1820 1180 -290 {lab=vpd}
N 1120 -1920 1140 -1920 {lab=vpd}
N 1120 -1920 1120 -1820 {lab=vpd}
N 720 -1890 720 -1820 {lab=vpd}
N 1120 -1820 1180 -1820 {lab=vpd}
N 1640 -1820 1800 -1820 {lab=vpd}
N 1860 -2020 1860 -1950 {lab=vddh}
N 1860 -1920 1880 -1920 {lab=vddh}
N 1880 -2020 1880 -1920 {lab=vddh}
N 1800 -1920 1820 -1920 {lab=vpd}
N 1800 -1920 1800 -1820 {lab=vpd}
N 1700 -2020 1700 -1950 {lab=vddh}
N 1700 -1920 1720 -1920 {lab=vddh}
N 1720 -2020 1720 -1920 {lab=vddh}
N 1640 -1920 1660 -1920 {lab=vpd}
N 1640 -1920 1640 -1820 {lab=vpd}
N 1540 -2020 1540 -1950 {lab=vddh}
N 1540 -1920 1560 -1920 {lab=vddh}
N 1560 -2020 1560 -1920 {lab=vddh}
N 1480 -1920 1500 -1920 {lab=vpd}
N 1480 -1920 1480 -1820 {lab=vpd}
N 1380 -2020 1380 -1950 {lab=vddh}
N 1380 -1920 1400 -1920 {lab=vddh}
N 1400 -2020 1400 -1920 {lab=vddh}
N 1320 -1920 1340 -1920 {lab=vpd}
N 1320 -1920 1320 -1820 {lab=vpd}
N 2080 -1950 2100 -1950 {lab=vddh}
N 2080 -1920 2100 -1920 {lab=vddh}
N 2080 -1890 2100 -1890 {lab=vddh}
N 2100 -1920 2100 -1890 {lab=vddh}
N 2000 -1920 2040 -1920 {lab=vpd}
N 1460 -290 1480 -290 {lab=vssh}
N 1460 -260 1480 -260 {lab=vssh}
N 1460 -230 1480 -230 {lab=vssh}
N 1380 -260 1420 -260 {lab=ni}
N 1860 -2020 1880 -2020 {lab=vddh}
N 220 -1620 420 -1620 {lab=en_3v3}
N 100 -1600 420 -1600 {lab=en_in0}
N 100 -1560 420 -1560 {lab=iin0}
N 520 -1520 520 -1500 {lab=vssh}
N 220 -1280 420 -1280 {lab=en_3v3}
N 100 -1260 420 -1260 {lab=en_in1}
N 100 -1220 420 -1220 {lab=iin1}
N 480 -1340 480 -1320 {lab=vddh}
N 520 -1180 520 -1160 {lab=vssh}
N 220 -940 420 -940 {lab=en_3v3}
N 100 -920 420 -920 {lab=en_in2}
N 100 -880 420 -880 {lab=iin2}
N 480 -1000 480 -980 {lab=vddh}
N 520 -840 520 -820 {lab=vssh}
N 220 -600 420 -600 {lab=en_3v3}
N 100 -580 420 -580 {lab=en_in3}
N 100 -540 420 -540 {lab=iin3}
N 480 -660 480 -640 {lab=vddh}
N 520 -500 520 -480 {lab=vssh}
N 2620 -1680 2740 -1680 {lab=iout0}
N 2520 -1800 2520 -1780 {lab=vddh}
N 2560 -1640 2560 -1620 {lab=vssh}
N 2620 -1360 2740 -1360 {lab=iout1}
N 2520 -1480 2520 -1460 {lab=vddh}
N 2560 -1320 2560 -1300 {lab=vssh}
N 2620 -1040 2740 -1040 {lab=iout2}
N 2520 -1160 2520 -1140 {lab=vddh}
N 2560 -1000 2560 -980 {lab=vssh}
N 2620 -720 2740 -720 {lab=iout3}
N 2520 -840 2520 -820 {lab=vddh}
N 2560 -680 2560 -660 {lab=vssh}
N 720 -380 1000 -380 {lab=ni}
N 1040 -260 1090 -260 {lab=ni}
N 720 -120 740 -120 {lab=vssh}
N 980 -120 1000 -120 {lab=vssh}
N 1000 -120 1180 -120 {lab=vssh}
N 1180 -120 1200 -120 {lab=vssh}
N 1180 -2020 1200 -2020 {lab=vddh}
N 1400 -2020 1540 -2020 {lab=vddh}
N 1180 -1890 1180 -1820 {lab=vpd}
N 1720 -2020 1860 -2020 {lab=vddh}
N 1560 -2020 1700 -2020 {lab=vddh}
N 1700 -2020 1720 -2020 {lab=vddh}
N 1480 -1820 1640 -1820 {lab=vpd}
N 1540 -2020 1560 -2020 {lab=vddh}
N 1320 -1820 1480 -1820 {lab=vpd}
N 1200 -2020 1380 -2020 {lab=vddh}
N 1380 -2020 1400 -2020 {lab=vddh}
N 1180 -1820 1320 -1820 {lab=vpd}
N 2100 -1950 2100 -1920 {lab=vddh}
N 1480 -290 1480 -260 {lab=vssh}
N 1480 -260 1480 -230 {lab=vssh}
N 100 -1920 220 -1920 {lab=en_3v3}
N 720 -1560 720 -1220 {lab=ni}
N 720 -1220 720 -880 {lab=ni}
N 720 -880 720 -540 {lab=ni}
N 400 -1000 400 -660 {lab=vddh}
N 720 -380 720 -290 {lab=ni}
N 220 -1740 220 -1620 {lab=en_3v3}
N 220 -1420 220 -1280 {lab=en_3v3}
N 220 -1100 220 -940 {lab=en_3v3}
N 220 -780 220 -600 {lab=en_3v3}
N 1860 -1890 1860 -1680 {lab=po0}
N 1700 -1890 1700 -1360 {lab=po1}
N 1540 -1890 1540 -1040 {lab=po2}
N 1380 -1890 1380 -720 {lab=po3}
N 220 -1920 220 -1740 {lab=en_3v3}
N 220 -1620 220 -1420 {lab=en_3v3}
N 220 -1280 220 -1100 {lab=en_3v3}
N 220 -940 220 -780 {lab=en_3v3}
N 100 -2020 400 -2020 {lab=vddh}
N 480 -1680 480 -1660 {lab=vddh}
N 400 -660 480 -660 {lab=vddh}
N 400 -1000 480 -1000 {lab=vddh}
N 400 -1340 400 -1000 {lab=vddh}
N 400 -1340 480 -1340 {lab=vddh}
N 400 -1680 400 -1340 {lab=vddh}
N 400 -1680 480 -1680 {lab=vddh}
N 400 -2020 400 -1680 {lab=vddh}
N 2560 -1620 2640 -1620 {lab=vssh}
N 2640 -660 2640 -120 {lab=vssh}
N 2560 -660 2640 -660 {lab=vssh}
N 2640 -980 2640 -660 {lab=vssh}
N 2560 -980 2640 -980 {lab=vssh}
N 2640 -1300 2640 -980 {lab=vssh}
N 2560 -1300 2640 -1300 {lab=vssh}
N 2640 -1620 2640 -1300 {lab=vssh}
N 520 -1500 600 -1500 {lab=vssh}
N 600 -480 600 -120 {lab=vssh}
N 100 -120 600 -120 {lab=vssh}
N 520 -480 600 -480 {lab=vssh}
N 600 -820 600 -480 {lab=vssh}
N 520 -820 600 -820 {lab=vssh}
N 600 -1160 600 -820 {lab=vssh}
N 520 -1160 600 -1160 {lab=vssh}
N 600 -1500 600 -1160 {lab=vssh}
N 600 -120 720 -120 {lab=vssh}
N 720 -260 740 -260 {lab=vssh}
N 100 -260 680 -260 {lab=en_3v3_b}
N 1200 -120 1480 -120 {lab=vssh}
N 580 -1560 720 -1560 {lab=ni}
N 580 -1220 720 -1220 {lab=ni}
N 580 -880 720 -880 {lab=ni}
N 580 -540 720 -540 {lab=ni}
N 400 -2020 720 -2020 {lab=vddh}
N 720 -2020 740 -2020 {lab=vddh}
N 720 -1920 740 -1920 {lab=vddh}
N 220 -1920 680 -1920 {lab=en_3v3}
N 740 -120 980 -120 {lab=vssh}
N 740 -2020 1180 -2020 {lab=vddh}
N 720 -540 720 -380 {lab=ni}
N 1480 -230 1480 -120 {lab=vssh}
N 1090 -380 1380 -380 {lab=ni}
N 1380 -380 1380 -260 {lab=ni}
N 1860 -1680 2460 -1680 {lab=po0}
N 1700 -1360 2460 -1360 {lab=po1}
N 1540 -1040 2460 -1040 {lab=po2}
N 1380 -720 2460 -720 {lab=po3}
N 1480 -120 2640 -120 {lab=vssh}
N 100 -760 2460 -760 {lab=en_out3}
N 220 -780 2460 -780 {lab=en_3v3}
N 100 -1080 2460 -1080 {lab=en_out2}
N 220 -1100 2460 -1100 {lab=en_3v3}
N 220 -1420 2460 -1420 {lab=en_3v3}
N 100 -1400 2460 -1400 {lab=en_out1}
N 220 -1740 2460 -1740 {lab=en_3v3}
N 100 -1720 2460 -1720 {lab=en_out0}
N 2000 -1920 2000 -1820 {lab=vpd}
N 1800 -1820 2000 -1820 {lab=vpd}
N 1880 -2020 2100 -2020 {lab=vddh}
N 2100 -2020 2100 -1950 {lab=vddh}
N 2440 -840 2520 -840 {lab=vddh}
N 2440 -1160 2440 -840 {lab=vddh}
N 2100 -2020 2440 -2020 {lab=vddh}
N 2440 -1160 2520 -1160 {lab=vddh}
N 2440 -1480 2440 -1160 {lab=vddh}
N 2440 -1480 2520 -1480 {lab=vddh}
N 2440 -1800 2440 -1480 {lab=vddh}
N 2440 -1800 2520 -1800 {lab=vddh}
N 2440 -2020 2440 -1800 {lab=vddh}
N 720 -1820 1120 -1820 {lab=vpd}
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
C {devices/opin.sym} 2740 -1680 0 0 {name=piout0 lab=iout0}
C {devices/opin.sym} 2740 -1360 0 0 {name=piout1 lab=iout1}
C {devices/opin.sym} 2740 -1040 0 0 {name=piout2 lab=iout2}
C {devices/opin.sym} 2740 -720 0 0 {name=piout3 lab=iout3}
C {devices/ipin.sym} 100 -1720 0 0 {name=p14 lab=en_out0}
C {devices/ipin.sym} 100 -1400 0 0 {name=p15 lab=en_out1}
C {devices/ipin.sym} 100 -1080 0 0 {name=p16 lab=en_out2}
C {devices/ipin.sym} 100 -760 0 0 {name=p17 lab=en_out3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 700 -260 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1020 -260 0 1 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1160 -260 0 0 {name=NM
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1160 -1920 0 0 {name=PD
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 700 -1920 0 0 {name=SVPD
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1840 -1920 0 0 {name=PO0
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1680 -1920 0 0 {name=PO1
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1520 -1920 0 0 {name=PO2
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1360 -1920 0 0 {name=PO3
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_wire.sym} 720 -1820 0 0 {name=l8 sig_type=std_logic lab=vpd}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2060 -1920 0 0 {name=MDP[1:0]
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 2100 -1980 0 1 {name=ldm0_r sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2000 -1920 0 0 {name=ldm0_g sig_type=std_logic lab=vpd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1440 -260 0 0 {name=MDN[1:0]
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1380 -260 0 0 {name=ldm1_g sig_type=std_logic lab=ni}
C {bdp_slice.sym} 500 -1590 0 0 {name=Xsi0}
C {devices/lab_pin.sym} 400 -660 0 0 {name=lsi0_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 520 -1500 0 0 {name=lsi0_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -1250 0 0 {name=Xsi1}
C {devices/lab_pin.sym} 480 -1340 0 1 {name=lsi1_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 520 -1160 0 0 {name=lsi1_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -910 0 0 {name=Xsi2}
C {devices/lab_pin.sym} 480 -1000 0 1 {name=lsi2_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 520 -820 0 0 {name=lsi2_vss sig_type=std_logic lab=vssh}
C {bdp_slice.sym} 500 -570 0 0 {name=Xsi3}
C {devices/lab_pin.sym} 480 -660 0 1 {name=lsi3_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 520 -480 0 0 {name=lsi3_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 720 -1560 0 1 {name=l7 sig_type=std_logic lab=ni}
C {bdp_slice.sym} 2540 -1710 0 0 {name=Xso0}
C {devices/lab_pin.sym} 2400 -1740 0 0 {name=lso0_en3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2400 -1720 0 0 {name=lso0_en sig_type=std_logic lab=en_out0}
C {devices/lab_pin.sym} 2520 -1800 0 1 {name=lso0_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2560 -1620 0 0 {name=lso0_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2420 -1680 0 0 {name=lpo0 sig_type=std_logic lab=po0}
C {bdp_slice.sym} 2540 -1390 0 0 {name=Xso1}
C {devices/lab_pin.sym} 2400 -1420 0 0 {name=lso1_en3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2400 -1400 0 0 {name=lso1_en sig_type=std_logic lab=en_out1}
C {devices/lab_pin.sym} 2520 -1480 0 1 {name=lso1_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2560 -1300 0 0 {name=lso1_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2420 -1360 0 0 {name=lpo1 sig_type=std_logic lab=po1}
C {bdp_slice.sym} 2540 -1070 0 0 {name=Xso2}
C {devices/lab_pin.sym} 2400 -1100 0 0 {name=lso2_en3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2400 -1080 0 0 {name=lso2_en sig_type=std_logic lab=en_out2}
C {devices/lab_pin.sym} 2520 -1160 0 1 {name=lso2_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2560 -980 0 0 {name=lso2_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2420 -1040 0 0 {name=lpo2 sig_type=std_logic lab=po2}
C {bdp_slice.sym} 2540 -750 0 0 {name=Xso3}
C {devices/lab_pin.sym} 2400 -780 0 0 {name=lso3_en3 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 2400 -760 0 0 {name=lso3_en sig_type=std_logic lab=en_out3}
C {devices/lab_pin.sym} 2520 -840 0 1 {name=lso3_vdd sig_type=std_logic lab=vddh}
C {devices/lab_pin.sym} 2560 -660 0 0 {name=lso3_vss sig_type=std_logic lab=vssh}
C {devices/lab_wire.sym} 2420 -720 0 0 {name=lpo3 sig_type=std_logic lab=po3}
C {devices/lab_pin.sym} 480 -1680 0 1 {name=lsi1 sig_type=std_logic lab=vddh}
