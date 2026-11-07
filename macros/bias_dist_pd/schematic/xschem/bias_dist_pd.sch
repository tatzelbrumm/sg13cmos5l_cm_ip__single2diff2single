v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 160 -1550 610 -1550 610 -480 160 -480 160 -1550 {dash=6}
P 10 5 620 -1550 1000 -1550 1000 -480 620 -480 620 -1550 {dash=6}
P 10 5 1010 -1600 1530 -1600 1530 -120 1010 -120 1010 -1600 {dash=6}
P 10 5 1550 -1600 2170 -1600 2170 -1400 1550 -1400 1550 -1600 {dash=6}
P 10 5 2190 -1490 2630 -1490 2630 -140 2190 -140 2190 -1490 {dash=6}
P 10 5 2640 -1490 3080 -1490 3080 -140 2640 -140 2640 -1490 {dash=6}
T {bias_dist_pd: switchable distribution mirror, 3 sourced inputs -> 4 sourced outputs (1 : 1), digital enable en_3v3} 100 -1850 0 0 0.4 0.4 {}
T {Enabled inputs (en_in<k> = 1) add up in NI; NM copies the sum into the PMOS diode PD; each enabled output PO<j> sources it through its TG.} 100 -1796 0 0 0.25 0.25 {}
T {iout<j> feeds a bias_tree_pd (NMOS input diode NI behind its own TG), e.g. one per pad; a disabled output's TG is open and PO<j> carries no current.} 100 -1772 0 0 0.25 0.25 {}
T {en_3v3 = 0: all TGs open, TDN pulls ni to vss, SVPD pulls vpd to vdd. Devices as in bias_tree_pd (NI 6u/6u, BP 5u/6u, switches 1u/0.45u). Source: netlist/source/bias_dist_pd.spice} 100 -1748 0 0 0.25 0.25 {}
T {[D] digital: one nand2_hv / inv_hv per input and output (en_out<j> and en_3v3 join the output decode by name). [S] [M] [O] analog: transmission gates, mirror, PMOS outputs.} 100 -1724 0 0 0.25 0.25 {}
T {[D] enable decode} 165 -1573.5 0 0 0.35 0.35 {layer=10}
T {[S] input switches} 745 -1573.5 0 0 0.35 0.35 {layer=10}
T {[M] mirror} 1015 -1623.5 0 0 0.35 0.35 {layer=10}
T {[O] PMOS outputs} 2146 -1623.5 0 0 0.35 0.35 {layer=10}
T {[D] enable decode} 2210 -1513.5 0 0 0.35 0.35 {layer=10}
T {[S] output switches} 2765 -1513.5 0 0 0.35 0.35 {layer=10}
N 100 -1440.0 280.0 -1440.0 {lab=en_in0}
N 220 -1480.0 280.0 -1480.0 {lab=en_3v3}
N 400.0 -1460.0 660 -1460.0 {lab=ei0_b}
N 660 -1460.0 660 -1400 {lab=ei0_b}
N 660 -1400 680 -1400 {lab=ei0_b}
N 440 -1460.0 440 -1220.0 {lab=ei0_b}
N 440 -1220.0 500.0 -1220.0 {lab=ei0_b}
N 580.0 -1220.0 800 -1220.0 {lab=ei0}
N 800 -1220.0 800 -1300 {lab=ei0}
N 800 -1300 820 -1300 {lab=ei0}
N 100 -1350 860 -1350 {lab=iin0}
N 860 -1330 860 -1350 {lab=iin0}
N 720 -1370 720 -1350 {lab=iin0}
N 720 -1430 720 -1450 {lab=ni}
N 720 -1450 980 -1450 {lab=ni}
N 860 -1270 860 -1250 {lab=ni}
N 860 -1250 980 -1250 {lab=ni}
N 860 -1300 880 -1300 {lab=vss}
N 720 -1400 740 -1400 {lab=vdd}
N 100 -1100.0 280.0 -1100.0 {lab=en_in1}
N 220 -1140.0 280.0 -1140.0 {lab=en_3v3}
N 400.0 -1120.0 660 -1120.0 {lab=ei1_b}
N 660 -1120.0 660 -1060 {lab=ei1_b}
N 660 -1060 680 -1060 {lab=ei1_b}
N 440 -1120.0 440 -880.0 {lab=ei1_b}
N 440 -880.0 500.0 -880.0 {lab=ei1_b}
N 580.0 -880.0 800 -880.0 {lab=ei1}
N 800 -880.0 800 -960 {lab=ei1}
N 800 -960 820 -960 {lab=ei1}
N 100 -1010 860 -1010 {lab=iin1}
N 860 -990 860 -1010 {lab=iin1}
N 720 -1030 720 -1010 {lab=iin1}
N 720 -1090 720 -1110 {lab=ni}
N 720 -1110 980 -1110 {lab=ni}
N 860 -930 860 -910 {lab=ni}
N 860 -910 980 -910 {lab=ni}
N 860 -960 880 -960 {lab=vss}
N 720 -1060 740 -1060 {lab=vdd}
N 100 -760.0 280.0 -760.0 {lab=en_in2}
N 220 -800.0 280.0 -800.0 {lab=en_3v3}
N 400.0 -780.0 660 -780.0 {lab=ei2_b}
N 660 -780.0 660 -720 {lab=ei2_b}
N 660 -720 680 -720 {lab=ei2_b}
N 440 -780.0 440 -540.0 {lab=ei2_b}
N 440 -540.0 500.0 -540.0 {lab=ei2_b}
N 580.0 -540.0 800 -540.0 {lab=ei2}
N 800 -540.0 800 -620 {lab=ei2}
N 800 -620 820 -620 {lab=ei2}
N 100 -670 860 -670 {lab=iin2}
N 860 -650 860 -670 {lab=iin2}
N 720 -690 720 -670 {lab=iin2}
N 720 -750 720 -770 {lab=ni}
N 720 -770 980 -770 {lab=ni}
N 860 -590 860 -570 {lab=ni}
N 860 -570 980 -570 {lab=ni}
N 860 -620 880 -620 {lab=vss}
N 720 -720 740 -720 {lab=vdd}
N 220 -1480.0 220 -800.0 {lab=en_3v3}
N 740 -720 740 -1640 {lab=vdd}
N 880 -1300 880 -80 {lab=vss}
N 980 -1450 980 -340 {lab=ni}
N 980 -340 1350 -340 {lab=ni}
N 1060 -250 1060 -340 {lab=ni}
N 1260 -250 1260 -340 {lab=ni}
N 1300 -220 1400 -220 {lab=ni}
N 1350 -220 1350 -340 {lab=ni}
N 1060 -190 1060 -80 {lab=vss}
N 1060 -220 1080 -220 {lab=vss}
N 1080 -220 1080 -80 {lab=vss}
N 1260 -190 1260 -80 {lab=vss}
N 1260 -220 1240 -220 {lab=vss}
N 1240 -220 1240 -80 {lab=vss}
N 1440 -190 1440 -80 {lab=vss}
N 1440 -220 1460 -220 {lab=vss}
N 1460 -220 1460 -80 {lab=vss}
N 100 -220 1020 -220 {lab=en_3v3_b}
N 1440 -1570 1440 -1640 {lab=vdd}
N 1440 -1540 1460 -1540 {lab=vdd}
N 1460 -1540 1460 -1640 {lab=vdd}
N 1280 -1570 1280 -1640 {lab=vdd}
N 1280 -1540 1300 -1540 {lab=vdd}
N 1300 -1540 1300 -1640 {lab=vdd}
N 1440 -1510 1440 -250 {lab=vpd}
N 1400 -1540 1380 -1540 {lab=vpd}
N 1380 -1540 1380 -1440 {lab=vpd}
N 1280 -1510 1280 -1440 {lab=vpd}
N 100 -1540 1240 -1540 {lab=en_3v3}
N 220 -1540 220 -1480.0 {lab=en_3v3}
N 1280 -1440 1440 -1440 {lab=vpd}
N 1440 -1440 2060 -1440 {lab=vpd}
N 2120 -1570 2120 -1640 {lab=vdd}
N 2120 -1540 2140 -1540 {lab=vdd}
N 2140 -1540 2140 -1640 {lab=vdd}
N 2080 -1540 2060 -1540 {lab=vpd}
N 2060 -1540 2060 -1440 {lab=vpd}
N 2420.0 -1400.0 2680 -1400.0 {lab=eo0_b}
N 2680 -1400.0 2680 -1340 {lab=eo0_b}
N 2680 -1340 2700 -1340 {lab=eo0_b}
N 2460 -1400.0 2460 -1160.0 {lab=eo0_b}
N 2460 -1160.0 2520.0 -1160.0 {lab=eo0_b}
N 2600.0 -1160.0 2820 -1160.0 {lab=eo0}
N 2820 -1160.0 2820 -1240 {lab=eo0}
N 2820 -1240 2840 -1240 {lab=eo0}
N 2120 -1510 2120 -1290 {lab=po0}
N 2120 -1290 2880 -1290 {lab=po0}
N 2880 -1270 2880 -1290 {lab=po0}
N 2740 -1310 2740 -1290 {lab=po0}
N 2740 -1370 2740 -1390 {lab=iout0}
N 2740 -1390 3060 -1390 {lab=iout0}
N 2880 -1210 2880 -1190 {lab=iout0}
N 2880 -1190 3060 -1190 {lab=iout0}
N 3060 -1390 3060 -1290 {lab=iout0}
N 3060 -1290 3100 -1290 {lab=iout0}
N 3060 -1290 3060 -1190 {lab=iout0}
N 2300.0 -1380.0 2270.0 -1380.0 {lab=en_out0}
N 2300.0 -1420.0 2270.0 -1420.0 {lab=en_3v3}
N 2880 -1240 2900 -1240 {lab=vss}
N 2740 -1340 2760 -1340 {lab=vdd}
N 1960 -1570 1960 -1640 {lab=vdd}
N 1960 -1540 1980 -1540 {lab=vdd}
N 1980 -1540 1980 -1640 {lab=vdd}
N 1920 -1540 1900 -1540 {lab=vpd}
N 1900 -1540 1900 -1440 {lab=vpd}
N 2420.0 -1080.0 2680 -1080.0 {lab=eo1_b}
N 2680 -1080.0 2680 -1020 {lab=eo1_b}
N 2680 -1020 2700 -1020 {lab=eo1_b}
N 2460 -1080.0 2460 -840.0 {lab=eo1_b}
N 2460 -840.0 2520.0 -840.0 {lab=eo1_b}
N 2600.0 -840.0 2820 -840.0 {lab=eo1}
N 2820 -840.0 2820 -920 {lab=eo1}
N 2820 -920 2840 -920 {lab=eo1}
N 1960 -1510 1960 -970 {lab=po1}
N 1960 -970 2880 -970 {lab=po1}
N 2880 -950 2880 -970 {lab=po1}
N 2740 -990 2740 -970 {lab=po1}
N 2740 -1050 2740 -1070 {lab=iout1}
N 2740 -1070 3060 -1070 {lab=iout1}
N 2880 -890 2880 -870 {lab=iout1}
N 2880 -870 3060 -870 {lab=iout1}
N 3060 -1070 3060 -970 {lab=iout1}
N 3060 -970 3100 -970 {lab=iout1}
N 3060 -970 3060 -870 {lab=iout1}
N 2300.0 -1060.0 2270.0 -1060.0 {lab=en_out1}
N 2300.0 -1100.0 2270.0 -1100.0 {lab=en_3v3}
N 2880 -920 2900 -920 {lab=vss}
N 2740 -1020 2760 -1020 {lab=vdd}
N 1800 -1570 1800 -1640 {lab=vdd}
N 1800 -1540 1820 -1540 {lab=vdd}
N 1820 -1540 1820 -1640 {lab=vdd}
N 1760 -1540 1740 -1540 {lab=vpd}
N 1740 -1540 1740 -1440 {lab=vpd}
N 2420.0 -760.0 2680 -760.0 {lab=eo2_b}
N 2680 -760.0 2680 -700 {lab=eo2_b}
N 2680 -700 2700 -700 {lab=eo2_b}
N 2460 -760.0 2460 -520.0 {lab=eo2_b}
N 2460 -520.0 2520.0 -520.0 {lab=eo2_b}
N 2600.0 -520.0 2820 -520.0 {lab=eo2}
N 2820 -520.0 2820 -600 {lab=eo2}
N 2820 -600 2840 -600 {lab=eo2}
N 1800 -1510 1800 -650 {lab=po2}
N 1800 -650 2880 -650 {lab=po2}
N 2880 -630 2880 -650 {lab=po2}
N 2740 -670 2740 -650 {lab=po2}
N 2740 -730 2740 -750 {lab=iout2}
N 2740 -750 3060 -750 {lab=iout2}
N 2880 -570 2880 -550 {lab=iout2}
N 2880 -550 3060 -550 {lab=iout2}
N 3060 -750 3060 -650 {lab=iout2}
N 3060 -650 3100 -650 {lab=iout2}
N 3060 -650 3060 -550 {lab=iout2}
N 2300.0 -740.0 2270.0 -740.0 {lab=en_out2}
N 2300.0 -780.0 2270.0 -780.0 {lab=en_3v3}
N 2880 -600 2900 -600 {lab=vss}
N 2740 -700 2760 -700 {lab=vdd}
N 1640 -1570 1640 -1640 {lab=vdd}
N 1640 -1540 1660 -1540 {lab=vdd}
N 1660 -1540 1660 -1640 {lab=vdd}
N 1600 -1540 1580 -1540 {lab=vpd}
N 1580 -1540 1580 -1440 {lab=vpd}
N 2420.0 -440.0 2680 -440.0 {lab=eo3_b}
N 2680 -440.0 2680 -380 {lab=eo3_b}
N 2680 -380 2700 -380 {lab=eo3_b}
N 2460 -440.0 2460 -200.0 {lab=eo3_b}
N 2460 -200.0 2520.0 -200.0 {lab=eo3_b}
N 2600.0 -200.0 2820 -200.0 {lab=eo3}
N 2820 -200.0 2820 -280 {lab=eo3}
N 2820 -280 2840 -280 {lab=eo3}
N 1640 -1510 1640 -330 {lab=po3}
N 1640 -330 2880 -330 {lab=po3}
N 2880 -310 2880 -330 {lab=po3}
N 2740 -350 2740 -330 {lab=po3}
N 2740 -410 2740 -430 {lab=iout3}
N 2740 -430 3060 -430 {lab=iout3}
N 2880 -250 2880 -230 {lab=iout3}
N 2880 -230 3060 -230 {lab=iout3}
N 3060 -430 3060 -330 {lab=iout3}
N 3060 -330 3100 -330 {lab=iout3}
N 3060 -330 3060 -230 {lab=iout3}
N 2300.0 -420.0 2270.0 -420.0 {lab=en_out3}
N 2300.0 -460.0 2270.0 -460.0 {lab=en_3v3}
N 2880 -280 2900 -280 {lab=vss}
N 2740 -380 2760 -380 {lab=vdd}
N 2760 -380 2760 -1640 {lab=vdd}
N 2900 -1240 2900 -80 {lab=vss}
N 360.0 -1490.0 360.0 -1510.0 {lab=vdd}
N 560.0 -1240.0 560.0 -1260.0 {lab=vdd}
N 360.0 -1150.0 360.0 -1170.0 {lab=vdd}
N 560.0 -900.0 560.0 -920.0 {lab=vdd}
N 360.0 -810.0 360.0 -830.0 {lab=vdd}
N 560.0 -560.0 560.0 -580.0 {lab=vdd}
N 2380.0 -1430.0 2380.0 -1450.0 {lab=vdd}
N 2580.0 -1180.0 2580.0 -1200.0 {lab=vdd}
N 2380.0 -1110.0 2380.0 -1130.0 {lab=vdd}
N 2580.0 -860.0 2580.0 -880.0 {lab=vdd}
N 2380.0 -790.0 2380.0 -810.0 {lab=vdd}
N 2580.0 -540.0 2580.0 -560.0 {lab=vdd}
N 2380.0 -470.0 2380.0 -490.0 {lab=vdd}
N 2580.0 -220.0 2580.0 -240.0 {lab=vdd}
N 340.0 -1430.0 340.0 -1410.0 {lab=vss}
N 540.0 -1200.0 540.0 -1180.0 {lab=vss}
N 340.0 -1090.0 340.0 -1070.0 {lab=vss}
N 540.0 -860.0 540.0 -840.0 {lab=vss}
N 340.0 -750.0 340.0 -730.0 {lab=vss}
N 540.0 -520.0 540.0 -500.0 {lab=vss}
N 2360.0 -1370.0 2360.0 -1350.0 {lab=vss}
N 2560.0 -1140.0 2560.0 -1120.0 {lab=vss}
N 2360.0 -1050.0 2360.0 -1030.0 {lab=vss}
N 2560.0 -820.0 2560.0 -800.0 {lab=vss}
N 2360.0 -730.0 2360.0 -710.0 {lab=vss}
N 2560.0 -500.0 2560.0 -480.0 {lab=vss}
N 2360.0 -410.0 2360.0 -390.0 {lab=vss}
N 2560.0 -180.0 2560.0 -160.0 {lab=vss}
N 100 -1640 2760 -1640 {lab=vdd}
N 100 -80 2900 -80 {lab=vss}
C {devices/iopin.sym} 100 -1640 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -80 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -1540 0 0 {name=p2 lab=en_3v3}
C {devices/ipin.sym} 100 -220 0 0 {name=p3 lab=en_3v3_b}
C {devices/iopin.sym} 100 -1350 0 1 {name=p4 lab=iin0}
C {devices/iopin.sym} 100 -1010 0 1 {name=p5 lab=iin1}
C {devices/iopin.sym} 100 -670 0 1 {name=p6 lab=iin2}
C {devices/ipin.sym} 100 -1440.0 0 0 {name=p7 lab=en_in0}
C {devices/ipin.sym} 100 -1100.0 0 0 {name=p8 lab=en_in1}
C {devices/ipin.sym} 100 -760.0 0 0 {name=p9 lab=en_in2}
C {devices/opin.sym} 3100 -1290 0 0 {name=p10 lab=iout0}
C {devices/opin.sym} 3100 -970 0 0 {name=p11 lab=iout1}
C {devices/opin.sym} 3100 -650 0 0 {name=p12 lab=iout2}
C {devices/opin.sym} 3100 -330 0 0 {name=p13 lab=iout3}
C {devices/ipin.sym} 100 -560 0 0 {name=p14 lab=en_out0}
C {devices/ipin.sym} 100 -520 0 0 {name=p15 lab=en_out1}
C {devices/ipin.sym} 100 -480 0 0 {name=p16 lab=en_out2}
C {devices/ipin.sym} 100 -440 0 0 {name=p17 lab=en_out3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 840 -1300 0 0 {name=TIN0
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 700 -1400 0 0 {name=TIP0
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 840 -960 0 0 {name=TIN1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 700 -1060 0 0 {name=TIP1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 840 -620 0 0 {name=TIN2
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 700 -720 0 0 {name=TIP2
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1040 -220 0 0 {name=TDN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 -220 0 1 {name=NI
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1420 -220 0 0 {name=NM
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
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2860 -1240 0 0 {name=TON0
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2720 -1340 0 0 {name=TOP0
l=0.45u
w=1u
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
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2860 -920 0 0 {name=TON1
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2720 -1020 0 0 {name=TOP1
l=0.45u
w=1u
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
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2860 -600 0 0 {name=TON2
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2720 -700 0 0 {name=TOP2
l=0.45u
w=1u
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
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2860 -280 0 0 {name=TON3
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2720 -380 0 0 {name=TOP3
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_wire.sym} 590 -1460 0 0 {name=l1 sig_type=std_logic lab=ei0_b}
C {devices/lab_wire.sym} 780 -1220 0 0 {name=l2 sig_type=std_logic lab=ei0}
C {devices/lab_wire.sym} 590 -1120 0 0 {name=l3 sig_type=std_logic lab=ei1_b}
C {devices/lab_wire.sym} 780 -880 0 0 {name=l4 sig_type=std_logic lab=ei1}
C {devices/lab_wire.sym} 590 -780 0 0 {name=l5 sig_type=std_logic lab=ei2_b}
C {devices/lab_wire.sym} 780 -540 0 0 {name=l6 sig_type=std_logic lab=ei2}
C {devices/lab_wire.sym} 980 -1450 0 1 {name=l7 sig_type=std_logic lab=ni}
C {devices/lab_wire.sym} 1360 -1440 0 0 {name=l8 sig_type=std_logic lab=vpd}
C {devices/lab_wire.sym} 2610 -1400 0 0 {name=l9 sig_type=std_logic lab=eo0_b}
C {devices/lab_wire.sym} 2800 -1160 0 0 {name=l10 sig_type=std_logic lab=eo0}
C {devices/lab_wire.sym} 2700 -1290 0 0 {name=l11 sig_type=std_logic lab=po0}
C {devices/lab_pin.sym} 2270.0 -1380.0 0 0 {name=l12 sig_type=std_logic lab=en_out0}
C {devices/lab_pin.sym} 2270.0 -1420.0 0 0 {name=l13 sig_type=std_logic lab=en_3v3}
C {devices/lab_wire.sym} 2610 -1080 0 0 {name=l14 sig_type=std_logic lab=eo1_b}
C {devices/lab_wire.sym} 2800 -840 0 0 {name=l15 sig_type=std_logic lab=eo1}
C {devices/lab_wire.sym} 2700 -970 0 0 {name=l16 sig_type=std_logic lab=po1}
C {devices/lab_pin.sym} 2270.0 -1060.0 0 0 {name=l17 sig_type=std_logic lab=en_out1}
C {devices/lab_pin.sym} 2270.0 -1100.0 0 0 {name=l18 sig_type=std_logic lab=en_3v3}
C {devices/lab_wire.sym} 2610 -760 0 0 {name=l19 sig_type=std_logic lab=eo2_b}
C {devices/lab_wire.sym} 2800 -520 0 0 {name=l20 sig_type=std_logic lab=eo2}
C {devices/lab_wire.sym} 2700 -650 0 0 {name=l21 sig_type=std_logic lab=po2}
C {devices/lab_pin.sym} 2270.0 -740.0 0 0 {name=l22 sig_type=std_logic lab=en_out2}
C {devices/lab_pin.sym} 2270.0 -780.0 0 0 {name=l23 sig_type=std_logic lab=en_3v3}
C {devices/lab_wire.sym} 2610 -440 0 0 {name=l24 sig_type=std_logic lab=eo3_b}
C {devices/lab_wire.sym} 2800 -200 0 0 {name=l25 sig_type=std_logic lab=eo3}
C {devices/lab_wire.sym} 2700 -330 0 0 {name=l26 sig_type=std_logic lab=po3}
C {devices/lab_pin.sym} 2270.0 -420.0 0 0 {name=l27 sig_type=std_logic lab=en_out3}
C {devices/lab_pin.sym} 2270.0 -460.0 0 0 {name=l28 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 360.0 -1510.0 0 1 {name=l29 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 560.0 -1260.0 0 1 {name=l30 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 360.0 -1170.0 0 1 {name=l31 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 560.0 -920.0 0 1 {name=l32 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 360.0 -830.0 0 1 {name=l33 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 560.0 -580.0 0 1 {name=l34 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2380.0 -1450.0 0 1 {name=l35 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2580.0 -1200.0 0 1 {name=l36 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2380.0 -1130.0 0 1 {name=l37 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2580.0 -880.0 0 1 {name=l38 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2380.0 -810.0 0 1 {name=l39 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2580.0 -560.0 0 1 {name=l40 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2380.0 -490.0 0 1 {name=l41 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 2580.0 -240.0 0 1 {name=l42 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 340.0 -1410.0 0 1 {name=l43 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 540.0 -1180.0 0 1 {name=l44 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 340.0 -1070.0 0 1 {name=l45 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 540.0 -840.0 0 1 {name=l46 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 340.0 -730.0 0 1 {name=l47 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 540.0 -500.0 0 1 {name=l48 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2360.0 -1350.0 0 1 {name=l49 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2560.0 -1120.0 0 1 {name=l50 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2360.0 -1030.0 0 1 {name=l51 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2560.0 -800.0 0 1 {name=l52 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2360.0 -710.0 0 1 {name=l53 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2560.0 -480.0 0 1 {name=l54 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2360.0 -390.0 0 1 {name=l55 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 2560.0 -160.0 0 1 {name=l56 sig_type=std_logic lab=vss}
C {nand2_hv.sym} 340 -1460 0 0 {name=XIA0}
C {inv_hv.sym} 540 -1220 0 0 {name=XIB0}
C {nand2_hv.sym} 340 -1120 0 0 {name=XIA1}
C {inv_hv.sym} 540 -880 0 0 {name=XIB1}
C {nand2_hv.sym} 340 -780 0 0 {name=XIA2}
C {inv_hv.sym} 540 -540 0 0 {name=XIB2}
C {nand2_hv.sym} 2360 -1400 0 0 {name=XOA0}
C {inv_hv.sym} 2560 -1160 0 0 {name=XOB0}
C {nand2_hv.sym} 2360 -1080 0 0 {name=XOA1}
C {inv_hv.sym} 2560 -840 0 0 {name=XOB1}
C {nand2_hv.sym} 2360 -760 0 0 {name=XOA2}
C {inv_hv.sym} 2560 -520 0 0 {name=XOB2}
C {nand2_hv.sym} 2360 -440 0 0 {name=XOA3}
C {inv_hv.sym} 2560 -200 0 0 {name=XOB3}
C {devices/title.sym} 160 0 0 0 {name=l0 author="Christoph Maier"}
