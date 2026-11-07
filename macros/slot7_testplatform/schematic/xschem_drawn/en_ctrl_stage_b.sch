v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
E {}
T {en_ctrl_stage_b (DRAFT): drop-in for tp_en_ctrl_b, from existing cells, no ratioed logic} 60 -200 0 0 0.5 0.5 {}
T {en_m = enable AND vdd_1v2 present AND vdd_3v3 present (en_ctrl_3v3, slot-fallback wiring); en<k>_b = NAND(ch<k>, en_m); en<k> = NOT en<k>_b} 60 -150 0 0 0.3 0.3 {}
T {ch0 / ch1: en_ctrl_3v3 sel0 / sel1 shifters; ch2..ch8: ls_up_1v2_3v3. Not simulated, no layout.} 60 -115 0 0 0.3 0.3 {}
C {devices/iopin.sym} 60 0 0 0 {name=p1 lab=vdd_3v3}
C {devices/iopin.sym} 60 1810 0 0 {name=p2 lab=vss_3v3}
C {devices/iopin.sym} 60 40 0 0 {name=p3 lab=vdd_1v2}
C {devices/ipin.sym} 60 180 0 0 {name=p4 lab=en0_1v2}
C {devices/ipin.sym} 60 200 0 0 {name=p5 lab=en1_1v2}
C {devices/ipin.sym} 60 720 0 0 {name=p6 lab=en2_1v2}
C {devices/ipin.sym} 60 880 0 0 {name=p7 lab=en3_1v2}
C {devices/ipin.sym} 60 1040 0 0 {name=p8 lab=en4_1v2}
C {devices/ipin.sym} 60 1200 0 0 {name=p9 lab=en5_1v2}
C {devices/ipin.sym} 60 1360 0 0 {name=p10 lab=en6_1v2}
C {devices/ipin.sym} 60 1520 0 0 {name=p11 lab=en7_1v2}
C {devices/ipin.sym} 60 1680 0 0 {name=p12 lab=en8_1v2}
C {devices/ipin.sym} 60 160 0 0 {name=p13 lab=enable}
C {devices/opin.sym} 1200 400 0 0 {name=p14 lab=en0}
C {devices/opin.sym} 1200 435 0 0 {name=p15 lab=en0_b}
C {devices/opin.sym} 1200 560 0 0 {name=p16 lab=en1}
C {devices/opin.sym} 1200 595 0 0 {name=p17 lab=en1_b}
C {devices/opin.sym} 1200 720 0 0 {name=p18 lab=en2}
C {devices/opin.sym} 1200 755 0 0 {name=p19 lab=en2_b}
C {devices/opin.sym} 1200 880 0 0 {name=p20 lab=en3}
C {devices/opin.sym} 1200 915 0 0 {name=p21 lab=en3_b}
C {devices/opin.sym} 1200 1040 0 0 {name=p22 lab=en4}
C {devices/opin.sym} 1200 1075 0 0 {name=p23 lab=en4_b}
C {devices/opin.sym} 1200 1200 0 0 {name=p24 lab=en5}
C {devices/opin.sym} 1200 1235 0 0 {name=p25 lab=en5_b}
C {devices/opin.sym} 1200 1360 0 0 {name=p26 lab=en6}
C {devices/opin.sym} 1200 1395 0 0 {name=p27 lab=en6_b}
C {devices/opin.sym} 1200 1520 0 0 {name=p28 lab=en7}
C {devices/opin.sym} 1200 1555 0 0 {name=p29 lab=en7_b}
C {devices/opin.sym} 1200 1680 0 0 {name=p30 lab=en8}
C {devices/opin.sym} 1200 1715 0 0 {name=p31 lab=en8_b}
C {en_ctrl_3v3.sym} 420 200 0 0 {name=XEC}
C {devices/lab_pin.sym} 290 240 0 0 {name=l1 sig_type=std_logic lab=vdd_3v3}
C {devices/lab_wire.sym} 560 160 0 0 {name=l2 sig_type=std_logic lab=en_m}
C {devices/lab_pin.sym} 550 180 0 1 {name=l3 sig_type=std_logic lab=en_m_b}
C {nand2_hv.sym} 720 400 0 0 {name=XN0}
C {devices/lab_wire.sym} 640 380 0 0 {name=l4 sig_type=std_logic lab=ch0}
C {inv_hv.sym} 900 400 0 0 {name=XI0}
C {nand2_hv.sym} 720 560 0 0 {name=XN1}
C {devices/lab_wire.sym} 640 540 0 0 {name=l5 sig_type=std_logic lab=ch1}
C {inv_hv.sym} 900 560 0 0 {name=XI1}
C {ls_up_1v2_3v3.sym} 400 720 0 0 {name=XL2}
C {nand2_hv.sym} 720 720 0 0 {name=XN2}
C {devices/lab_wire.sym} 640 700 0 0 {name=l6 sig_type=std_logic lab=ch2}
C {inv_hv.sym} 900 720 0 0 {name=XI2}
C {ls_up_1v2_3v3.sym} 400 880 0 0 {name=XL3}
C {nand2_hv.sym} 720 880 0 0 {name=XN3}
C {devices/lab_wire.sym} 640 860 0 0 {name=l7 sig_type=std_logic lab=ch3}
C {inv_hv.sym} 900 880 0 0 {name=XI3}
C {ls_up_1v2_3v3.sym} 400 1040 0 0 {name=XL4}
C {nand2_hv.sym} 720 1040 0 0 {name=XN4}
C {devices/lab_wire.sym} 640 1020 0 0 {name=l8 sig_type=std_logic lab=ch4}
C {inv_hv.sym} 900 1040 0 0 {name=XI4}
C {ls_up_1v2_3v3.sym} 400 1200 0 0 {name=XL5}
C {nand2_hv.sym} 720 1200 0 0 {name=XN5}
C {devices/lab_wire.sym} 640 1180 0 0 {name=l9 sig_type=std_logic lab=ch5}
C {inv_hv.sym} 900 1200 0 0 {name=XI5}
C {ls_up_1v2_3v3.sym} 400 1360 0 0 {name=XL6}
C {nand2_hv.sym} 720 1360 0 0 {name=XN6}
C {devices/lab_wire.sym} 640 1340 0 0 {name=l10 sig_type=std_logic lab=ch6}
C {inv_hv.sym} 900 1360 0 0 {name=XI6}
C {ls_up_1v2_3v3.sym} 400 1520 0 0 {name=XL7}
C {nand2_hv.sym} 720 1520 0 0 {name=XN7}
C {devices/lab_wire.sym} 640 1500 0 0 {name=l11 sig_type=std_logic lab=ch7}
C {inv_hv.sym} 900 1520 0 0 {name=XI7}
C {ls_up_1v2_3v3.sym} 400 1680 0 0 {name=XL8}
C {nand2_hv.sym} 720 1680 0 0 {name=XN8}
C {devices/lab_wire.sym} 640 1660 0 0 {name=l12 sig_type=std_logic lab=ch8}
C {inv_hv.sym} 900 1680 0 0 {name=XI8}
N 60 0 1040 0 {lab=vdd_3v3}
N 1040 0 1040 1630 {lab=vdd_3v3}
N 60 1810 1080 1810 {lab=vss_3v3}
N 1080 300 1080 1810 {lab=vss_3v3}
N 60 40 380 40 {lab=vdd_1v2}
N 180 40 180 1640 {lab=vdd_1v2}
N 360 120 360 0 {lab=vdd_3v3}
N 380 120 380 40 {lab=vdd_1v2}
N 360 280 360 300 {lab=vss_3v3}
N 360 300 1080 300 {lab=vss_3v3}
N 60 160 320 160 {lab=enable}
N 60 180 320 180 {lab=en0_1v2}
N 60 200 320 200 {lab=en1_1v2}
N 180 220 320 220 {lab=vdd_1v2}
N 320 240 290 240 {lab=vdd_3v3}
N 520 160 600 160 {lab=en_m}
N 600 160 600 1700 {lab=en_m}
N 520 180 550 180 {lab=en_m_b}
N 520 200 560 200 {lab=ch0}
N 560 200 560 380 {lab=ch0}
N 560 380 660 380 {lab=ch0}
N 520 220 580 220 {lab=ch1}
N 580 220 580 540 {lab=ch1}
N 580 540 660 540 {lab=ch1}
N 600 420 660 420 {lab=en_m}
N 780 400 860 400 {lab=en0_b}
N 820 400 820 435 {lab=en0_b}
N 820 435 1200 435 {lab=en0_b}
N 940 400 1200 400 {lab=en0}
N 740 350 1040 350 {lab=vdd_3v3}
N 740 370 740 350 {lab=vdd_3v3}
N 920 380 920 350 {lab=vdd_3v3}
N 720 450 1080 450 {lab=vss_3v3}
N 720 430 720 450 {lab=vss_3v3}
N 900 420 900 450 {lab=vss_3v3}
N 600 580 660 580 {lab=en_m}
N 780 560 860 560 {lab=en1_b}
N 820 560 820 595 {lab=en1_b}
N 820 595 1200 595 {lab=en1_b}
N 940 560 1200 560 {lab=en1}
N 740 510 1040 510 {lab=vdd_3v3}
N 740 530 740 510 {lab=vdd_3v3}
N 920 540 920 510 {lab=vdd_3v3}
N 720 610 1080 610 {lab=vss_3v3}
N 720 590 720 610 {lab=vss_3v3}
N 900 580 900 610 {lab=vss_3v3}
N 60 720 360 720 {lab=en2_1v2}
N 440 720 500 720 {lab=ch2}
N 500 720 500 700 {lab=ch2}
N 500 700 660 700 {lab=ch2}
N 390 690 390 680 {lab=vdd_1v2}
N 390 680 180 680 {lab=vdd_1v2}
N 410 690 410 670 {lab=vdd_3v3}
N 400 750 400 770 {lab=vss_3v3}
N 600 740 660 740 {lab=en_m}
N 780 720 860 720 {lab=en2_b}
N 820 720 820 755 {lab=en2_b}
N 820 755 1200 755 {lab=en2_b}
N 940 720 1200 720 {lab=en2}
N 410 670 1040 670 {lab=vdd_3v3}
N 740 690 740 670 {lab=vdd_3v3}
N 920 700 920 670 {lab=vdd_3v3}
N 400 770 1080 770 {lab=vss_3v3}
N 720 750 720 770 {lab=vss_3v3}
N 900 740 900 770 {lab=vss_3v3}
N 60 880 360 880 {lab=en3_1v2}
N 440 880 500 880 {lab=ch3}
N 500 880 500 860 {lab=ch3}
N 500 860 660 860 {lab=ch3}
N 390 850 390 840 {lab=vdd_1v2}
N 390 840 180 840 {lab=vdd_1v2}
N 410 850 410 830 {lab=vdd_3v3}
N 400 910 400 930 {lab=vss_3v3}
N 600 900 660 900 {lab=en_m}
N 780 880 860 880 {lab=en3_b}
N 820 880 820 915 {lab=en3_b}
N 820 915 1200 915 {lab=en3_b}
N 940 880 1200 880 {lab=en3}
N 410 830 1040 830 {lab=vdd_3v3}
N 740 850 740 830 {lab=vdd_3v3}
N 920 860 920 830 {lab=vdd_3v3}
N 400 930 1080 930 {lab=vss_3v3}
N 720 910 720 930 {lab=vss_3v3}
N 900 900 900 930 {lab=vss_3v3}
N 60 1040 360 1040 {lab=en4_1v2}
N 440 1040 500 1040 {lab=ch4}
N 500 1040 500 1020 {lab=ch4}
N 500 1020 660 1020 {lab=ch4}
N 390 1010 390 1000 {lab=vdd_1v2}
N 390 1000 180 1000 {lab=vdd_1v2}
N 410 1010 410 990 {lab=vdd_3v3}
N 400 1070 400 1090 {lab=vss_3v3}
N 600 1060 660 1060 {lab=en_m}
N 780 1040 860 1040 {lab=en4_b}
N 820 1040 820 1075 {lab=en4_b}
N 820 1075 1200 1075 {lab=en4_b}
N 940 1040 1200 1040 {lab=en4}
N 410 990 1040 990 {lab=vdd_3v3}
N 740 1010 740 990 {lab=vdd_3v3}
N 920 1020 920 990 {lab=vdd_3v3}
N 400 1090 1080 1090 {lab=vss_3v3}
N 720 1070 720 1090 {lab=vss_3v3}
N 900 1060 900 1090 {lab=vss_3v3}
N 60 1200 360 1200 {lab=en5_1v2}
N 440 1200 500 1200 {lab=ch5}
N 500 1200 500 1180 {lab=ch5}
N 500 1180 660 1180 {lab=ch5}
N 390 1170 390 1160 {lab=vdd_1v2}
N 390 1160 180 1160 {lab=vdd_1v2}
N 410 1170 410 1150 {lab=vdd_3v3}
N 400 1230 400 1250 {lab=vss_3v3}
N 600 1220 660 1220 {lab=en_m}
N 780 1200 860 1200 {lab=en5_b}
N 820 1200 820 1235 {lab=en5_b}
N 820 1235 1200 1235 {lab=en5_b}
N 940 1200 1200 1200 {lab=en5}
N 410 1150 1040 1150 {lab=vdd_3v3}
N 740 1170 740 1150 {lab=vdd_3v3}
N 920 1180 920 1150 {lab=vdd_3v3}
N 400 1250 1080 1250 {lab=vss_3v3}
N 720 1230 720 1250 {lab=vss_3v3}
N 900 1220 900 1250 {lab=vss_3v3}
N 60 1360 360 1360 {lab=en6_1v2}
N 440 1360 500 1360 {lab=ch6}
N 500 1360 500 1340 {lab=ch6}
N 500 1340 660 1340 {lab=ch6}
N 390 1330 390 1320 {lab=vdd_1v2}
N 390 1320 180 1320 {lab=vdd_1v2}
N 410 1330 410 1310 {lab=vdd_3v3}
N 400 1390 400 1410 {lab=vss_3v3}
N 600 1380 660 1380 {lab=en_m}
N 780 1360 860 1360 {lab=en6_b}
N 820 1360 820 1395 {lab=en6_b}
N 820 1395 1200 1395 {lab=en6_b}
N 940 1360 1200 1360 {lab=en6}
N 410 1310 1040 1310 {lab=vdd_3v3}
N 740 1330 740 1310 {lab=vdd_3v3}
N 920 1340 920 1310 {lab=vdd_3v3}
N 400 1410 1080 1410 {lab=vss_3v3}
N 720 1390 720 1410 {lab=vss_3v3}
N 900 1380 900 1410 {lab=vss_3v3}
N 60 1520 360 1520 {lab=en7_1v2}
N 440 1520 500 1520 {lab=ch7}
N 500 1520 500 1500 {lab=ch7}
N 500 1500 660 1500 {lab=ch7}
N 390 1490 390 1480 {lab=vdd_1v2}
N 390 1480 180 1480 {lab=vdd_1v2}
N 410 1490 410 1470 {lab=vdd_3v3}
N 400 1550 400 1570 {lab=vss_3v3}
N 600 1540 660 1540 {lab=en_m}
N 780 1520 860 1520 {lab=en7_b}
N 820 1520 820 1555 {lab=en7_b}
N 820 1555 1200 1555 {lab=en7_b}
N 940 1520 1200 1520 {lab=en7}
N 410 1470 1040 1470 {lab=vdd_3v3}
N 740 1490 740 1470 {lab=vdd_3v3}
N 920 1500 920 1470 {lab=vdd_3v3}
N 400 1570 1080 1570 {lab=vss_3v3}
N 720 1550 720 1570 {lab=vss_3v3}
N 900 1540 900 1570 {lab=vss_3v3}
N 60 1680 360 1680 {lab=en8_1v2}
N 440 1680 500 1680 {lab=ch8}
N 500 1680 500 1660 {lab=ch8}
N 500 1660 660 1660 {lab=ch8}
N 390 1650 390 1640 {lab=vdd_1v2}
N 390 1640 180 1640 {lab=vdd_1v2}
N 410 1650 410 1630 {lab=vdd_3v3}
N 400 1710 400 1730 {lab=vss_3v3}
N 600 1700 660 1700 {lab=en_m}
N 780 1680 860 1680 {lab=en8_b}
N 820 1680 820 1715 {lab=en8_b}
N 820 1715 1200 1715 {lab=en8_b}
N 940 1680 1200 1680 {lab=en8}
N 410 1630 1040 1630 {lab=vdd_3v3}
N 740 1650 740 1630 {lab=vdd_3v3}
N 920 1660 920 1630 {lab=vdd_3v3}
N 400 1730 1080 1730 {lab=vss_3v3}
N 720 1710 720 1730 {lab=vss_3v3}
N 900 1700 900 1730 {lab=vss_3v3}
