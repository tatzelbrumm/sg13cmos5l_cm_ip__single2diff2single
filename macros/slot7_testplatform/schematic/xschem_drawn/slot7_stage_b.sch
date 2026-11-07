v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {devices/iopin.sym} 60 160 0 1 {name=p1 lab=vdd_3v3}
C {devices/iopin.sym} 60 2480 0 1 {name=p2 lab=vss_3v3}
C {devices/iopin.sym} 60 200 0 1 {name=p3 lab=vdd_1v2}
C {devices/ipin.sym} 60 640 0 0 {name=p4 lab=enable}
C {devices/ipin.sym} 60 280 0 0 {name=p5 lab=dig_in[4]}
C {devices/ipin.sym} 60 320 0 0 {name=p6 lab=dig_in[5]}
C {devices/ipin.sym} 60 360 0 0 {name=p7 lab=dig_in[6]}
C {devices/ipin.sym} 60 400 0 0 {name=p8 lab=dig_in[7]}
C {devices/ipin.sym} 60 440 0 0 {name=p9 lab=dig_in[8]}
C {devices/ipin.sym} 60 480 0 0 {name=p10 lab=dig_in[9]}
C {devices/ipin.sym} 60 520 0 0 {name=p11 lab=dig_in[10]}
C {devices/ipin.sym} 60 560 0 0 {name=p12 lab=dig_in[11]}
C {devices/ipin.sym} 60 600 0 0 {name=p13 lab=dig_in[12]}
C {devices/ipin.sym} 60 0 0 0 {name=p14 lab=i_oa}
C {devices/ipin.sym} 60 40 0 0 {name=p15 lab=i_bg}
C {devices/ipin.sym} 60 80 0 0 {name=p16 lab=ibias0}
C {devices/ipin.sym} 60 2560 0 0 {name=p17 lab=ibias1}
C {devices/iopin.sym} 1900 1740 0 0 {name=p18 lab=analog_bus2}
C {devices/iopin.sym} 1900 2340 0 0 {name=p19 lab=analog_bus3}
C {tp_en_ctrl_b.sym} 400 1300 0 0 {name=xctlb}
N 60 160 220 160 {lab=vdd_3v3}
N 60 200 220 200 {lab=vdd_1v2}
N 60 640 220 640 {lab=enable}
N 60 2480 220 2480 {lab=vss_3v3}
N 60 280 220 280 {lab=dig_in[4]}
N 60 320 220 320 {lab=dig_in[5]}
N 60 360 220 360 {lab=dig_in[6]}
N 60 400 220 400 {lab=dig_in[7]}
N 60 440 220 440 {lab=dig_in[8]}
N 60 480 220 480 {lab=dig_in[9]}
N 60 520 220 520 {lab=dig_in[10]}
N 60 560 220 560 {lab=dig_in[11]}
N 60 600 220 600 {lab=dig_in[12]}
C {xgate.sym} 800 290 0 0 {name=xr_oa}
N 580 210 790 210 {lab=en_ref_oa_b}
N 790 210 790 240 {lab=en_ref_oa_b}
N 580 410 790 410 {lab=en_ref_oa}
N 790 410 790 360 {lab=en_ref_oa}
C {devices/lab_wire.sym} 780 210 0 0 {name=lw1 sig_type=std_logic lab=en_ref_oa_b}
C {devices/lab_wire.sym} 780 410 0 0 {name=lw2 sig_type=std_logic lab=en_ref_oa}
N 860 270 900 270 {lab=vdd_3v3}
C {devices/lab_pin.sym} 900 270 0 1 {name=l3 sig_type=std_logic lab=vdd_3v3}
N 860 330 900 330 {lab=vss_3v3}
C {devices/lab_pin.sym} 900 330 0 1 {name=l4 sig_type=std_logic lab=vss_3v3}
N 860 300 1000 300 {lab=iref}
N 60 0 680 0 {lab=i_oa}
N 680 0 680 300 {lab=i_oa}
N 680 300 720 300 {lab=i_oa}
C {xgate.sym} 800 530 0 0 {name=xr_bg}
N 580 450 790 450 {lab=en_ref_bg_b}
N 790 450 790 480 {lab=en_ref_bg_b}
N 580 650 790 650 {lab=en_ref_bg}
N 790 650 790 600 {lab=en_ref_bg}
C {devices/lab_wire.sym} 780 450 0 0 {name=lw5 sig_type=std_logic lab=en_ref_bg_b}
C {devices/lab_wire.sym} 780 650 0 0 {name=lw6 sig_type=std_logic lab=en_ref_bg}
N 860 510 900 510 {lab=vdd_3v3}
C {devices/lab_pin.sym} 900 510 0 1 {name=l7 sig_type=std_logic lab=vdd_3v3}
N 860 570 900 570 {lab=vss_3v3}
C {devices/lab_pin.sym} 900 570 0 1 {name=l8 sig_type=std_logic lab=vss_3v3}
N 860 540 1000 540 {lab=iref}
N 60 40 660 40 {lab=i_bg}
N 660 40 660 540 {lab=i_bg}
N 660 540 720 540 {lab=i_bg}
C {xgate.sym} 800 770 0 0 {name=xr_ib0}
N 580 690 790 690 {lab=en_ref_ib0_b}
N 790 690 790 720 {lab=en_ref_ib0_b}
N 580 890 790 890 {lab=en_ref_ib0}
N 790 890 790 840 {lab=en_ref_ib0}
C {devices/lab_wire.sym} 780 690 0 0 {name=lw9 sig_type=std_logic lab=en_ref_ib0_b}
C {devices/lab_wire.sym} 780 890 0 0 {name=lw10 sig_type=std_logic lab=en_ref_ib0}
N 860 750 900 750 {lab=vdd_3v3}
C {devices/lab_pin.sym} 900 750 0 1 {name=l11 sig_type=std_logic lab=vdd_3v3}
N 860 810 900 810 {lab=vss_3v3}
C {devices/lab_pin.sym} 900 810 0 1 {name=l12 sig_type=std_logic lab=vss_3v3}
N 860 780 1000 780 {lab=iref}
N 60 80 640 80 {lab=ibias0}
N 640 80 640 780 {lab=ibias0}
N 640 780 720 780 {lab=ibias0}
N 1000 300 1000 1030 {lab=iref}
C {devices/lab_wire.sym} 1000 660 0 0 {name=lw13 sig_type=std_logic lab=iref}
C {bias_tree_noab_pd.sym} 1200 1080 0 0 {name=xtree}
N 1000 1030 1100 1030 {lab=iref}
N 580 1050 1100 1050 {lab=en_tree}
N 580 1070 1100 1070 {lab=en_tree_b}
C {devices/lab_wire.sym} 660 1050 0 1 {name=lw14 sig_type=std_logic lab=en_tree}
C {devices/lab_wire.sym} 860 1070 0 1 {name=lw15 sig_type=std_logic lab=en_tree_b}
N 1160 990 1160 970 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1160 970 0 1 {name=l16 sig_type=std_logic lab=vdd_3v3}
N 1140 1170 1140 1190 {lab=vss_3v3}
C {devices/lab_pin.sym} 1140 1190 0 1 {name=l17 sig_type=std_logic lab=vss_3v3}
C {xgate.sym} 1580 1370 0 0 {name=xm_vbp}
N 580 1290 1570 1290 {lab=en_m_vbp_b}
N 1570 1290 1570 1320 {lab=en_m_vbp_b}
N 580 1490 1570 1490 {lab=en_m_vbp}
N 1570 1490 1570 1440 {lab=en_m_vbp}
C {devices/lab_wire.sym} 660 1290 0 1 {name=lw18 sig_type=std_logic lab=en_m_vbp_b}
C {devices/lab_wire.sym} 660 1490 0 1 {name=lw19 sig_type=std_logic lab=en_m_vbp}
N 1640 1350 1680 1350 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1680 1350 0 1 {name=l20 sig_type=std_logic lab=vdd_3v3}
N 1640 1410 1680 1410 {lab=vss_3v3}
C {devices/lab_pin.sym} 1680 1410 0 1 {name=l21 sig_type=std_logic lab=vss_3v3}
N 1640 1380 1780 1380 {lab=analog_bus2}
N 1300 1030 1460 1030 {lab=vbp}
N 1460 1030 1460 1380 {lab=vbp}
N 1460 1380 1500 1380 {lab=vbp}
C {devices/lab_wire.sym} 1330 1030 0 1 {name=lw22 sig_type=std_logic lab=vbp}
C {xgate.sym} 1580 1610 0 0 {name=xm_vbpc}
N 580 1530 1570 1530 {lab=en_m_vbpc_b}
N 1570 1530 1570 1560 {lab=en_m_vbpc_b}
N 580 1730 1570 1730 {lab=en_m_vbpc}
N 1570 1730 1570 1680 {lab=en_m_vbpc}
C {devices/lab_wire.sym} 660 1530 0 1 {name=lw23 sig_type=std_logic lab=en_m_vbpc_b}
C {devices/lab_wire.sym} 660 1730 0 1 {name=lw24 sig_type=std_logic lab=en_m_vbpc}
N 1640 1590 1680 1590 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1680 1590 0 1 {name=l25 sig_type=std_logic lab=vdd_3v3}
N 1640 1650 1680 1650 {lab=vss_3v3}
C {devices/lab_pin.sym} 1680 1650 0 1 {name=l26 sig_type=std_logic lab=vss_3v3}
N 1640 1620 1780 1620 {lab=analog_bus2}
N 1300 1050 1440 1050 {lab=vbpc}
N 1440 1050 1440 1620 {lab=vbpc}
N 1440 1620 1500 1620 {lab=vbpc}
C {devices/lab_wire.sym} 1330 1050 0 1 {name=lw27 sig_type=std_logic lab=vbpc}
C {xgate.sym} 1580 1850 0 0 {name=xm_vbnc}
N 580 1770 1570 1770 {lab=en_m_vbnc_b}
N 1570 1770 1570 1800 {lab=en_m_vbnc_b}
N 580 1970 1570 1970 {lab=en_m_vbnc}
N 1570 1970 1570 1920 {lab=en_m_vbnc}
C {devices/lab_wire.sym} 660 1770 0 1 {name=lw28 sig_type=std_logic lab=en_m_vbnc_b}
C {devices/lab_wire.sym} 660 1970 0 1 {name=lw29 sig_type=std_logic lab=en_m_vbnc}
N 1640 1830 1680 1830 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1680 1830 0 1 {name=l30 sig_type=std_logic lab=vdd_3v3}
N 1640 1890 1680 1890 {lab=vss_3v3}
C {devices/lab_pin.sym} 1680 1890 0 1 {name=l31 sig_type=std_logic lab=vss_3v3}
N 1640 1860 1780 1860 {lab=analog_bus2}
N 1300 1110 1420 1110 {lab=vbnc}
N 1420 1110 1420 1860 {lab=vbnc}
N 1420 1860 1500 1860 {lab=vbnc}
C {devices/lab_wire.sym} 1330 1110 0 1 {name=lw32 sig_type=std_logic lab=vbnc}
C {xgate.sym} 1580 2090 0 0 {name=xm_vbn}
N 580 2010 1570 2010 {lab=en_m_vbn_b}
N 1570 2010 1570 2040 {lab=en_m_vbn_b}
N 580 2210 1570 2210 {lab=en_m_vbn}
N 1570 2210 1570 2160 {lab=en_m_vbn}
C {devices/lab_wire.sym} 660 2010 0 1 {name=lw33 sig_type=std_logic lab=en_m_vbn_b}
C {devices/lab_wire.sym} 660 2210 0 1 {name=lw34 sig_type=std_logic lab=en_m_vbn}
N 1640 2070 1680 2070 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1680 2070 0 1 {name=l35 sig_type=std_logic lab=vdd_3v3}
N 1640 2130 1680 2130 {lab=vss_3v3}
C {devices/lab_pin.sym} 1680 2130 0 1 {name=l36 sig_type=std_logic lab=vss_3v3}
N 1640 2100 1780 2100 {lab=analog_bus2}
N 1300 1130 1400 1130 {lab=vbn}
N 1400 1130 1400 2100 {lab=vbn}
N 1400 2100 1500 2100 {lab=vbn}
C {devices/lab_wire.sym} 1330 1130 0 1 {name=lw37 sig_type=std_logic lab=vbn}
N 1780 1380 1780 2100 {lab=analog_bus2}
N 1780 1740 1900 1740 {lab=analog_bus2}
C {xgate.sym} 1580 2330 0 0 {name=xi_ib1}
N 580 2250 1570 2250 {lab=en_ib1_b}
N 1570 2250 1570 2280 {lab=en_ib1_b}
N 580 2450 1570 2450 {lab=en_ib1}
N 1570 2450 1570 2400 {lab=en_ib1}
C {devices/lab_wire.sym} 660 2250 0 1 {name=lw38 sig_type=std_logic lab=en_ib1_b}
C {devices/lab_wire.sym} 660 2450 0 1 {name=lw39 sig_type=std_logic lab=en_ib1}
N 1640 2310 1680 2310 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1680 2310 0 1 {name=l40 sig_type=std_logic lab=vdd_3v3}
N 1640 2370 1680 2370 {lab=vss_3v3}
C {devices/lab_pin.sym} 1680 2370 0 1 {name=l41 sig_type=std_logic lab=vss_3v3}
N 1640 2340 1900 2340 {lab=analog_bus3}
N 60 2560 1480 2560 {lab=ibias1}
N 1480 2560 1480 2340 {lab=ibias1}
N 1480 2340 1500 2340 {lab=ibias1}
T {slot7_stage_b: bias_tree_noab_pd with a selectable reference current, its bias voltages onto analog_bus2, the harness ibias1 onto analog_bus3} 0 -200 0 0 0.5 0.5 {}
T {reference iref: i_oa (dig_in[4]), i_bg (dig_in[5]) or ibias0 (dig_in[6]); tree enable dig_in[7]; mux vbp / vbn / vbpc / vbnc -> analog_bus2 (dig_in[8..11]); ibias1 -> analog_bus3 (dig_in[12]); every enable fail-safe (tp_en_ctrl_b)} 0 -150 0 0 0.3 0.3 {}
T {source: ../../netlist/source/slot7_stage_b.spice; plan: docs/slot7_testplatform/PLAN.md section 9; switch and tree supplies are labels} 0 -120 0 0 0.3 0.3 {}
C {devices/title.sym} 160 2700 0 0 {name=l_title author="Christoph Maier"}
