v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {devices/iopin.sym} 60 0 0 1 {name=p1 lab=vdd_3v3}
C {devices/iopin.sym} 60 1240 0 1 {name=p2 lab=vss_3v3}
C {devices/iopin.sym} 60 120 0 1 {name=p3 lab=vdd_1v2}
C {devices/iopin.sym} 60 1160 0 1 {name=p4 lab=vss_1v2}
C {devices/ipin.sym} 60 360 0 0 {name=p5 lab=enable}
C {devices/ipin.sym} 60 200 0 0 {name=p6 lab=dig_in[0]}
C {devices/ipin.sym} 60 240 0 0 {name=p7 lab=dig_in[1]}
C {devices/ipin.sym} 60 280 0 0 {name=p8 lab=dig_in[2]}
C {devices/ipin.sym} 60 320 0 0 {name=p9 lab=dig_in[3]}
C {devices/ipin.sym} 60 1480 0 0 {name=p10 lab=dig_in[4]}
C {devices/ipin.sym} 60 1520 0 0 {name=p11 lab=dig_in[5]}
C {devices/ipin.sym} 60 1560 0 0 {name=p12 lab=dig_in[6]}
C {devices/ipin.sym} 60 1600 0 0 {name=p13 lab=dig_in[7]}
C {devices/ipin.sym} 60 1640 0 0 {name=p14 lab=dig_in[8]}
C {devices/ipin.sym} 60 1680 0 0 {name=p15 lab=dig_in[9]}
C {devices/ipin.sym} 60 1720 0 0 {name=p16 lab=dig_in[10]}
C {devices/ipin.sym} 60 1760 0 0 {name=p17 lab=dig_in[11]}
C {devices/ipin.sym} 60 1800 0 0 {name=p18 lab=dig_in[12]}
C {devices/opin.sym} 1560 420 0 0 {name=p19 lab=dig_out[0]}
C {devices/opin.sym} 1560 460 0 0 {name=p20 lab=dig_out[1]}
C {devices/opin.sym} 1560 500 0 0 {name=p21 lab=dig_out[2]}
C {devices/opin.sym} 1560 540 0 0 {name=p22 lab=dig_out[3]}
C {devices/opin.sym} 1560 580 0 0 {name=p23 lab=dig_out[4]}
C {devices/opin.sym} 1560 620 0 0 {name=p24 lab=dig_out[5]}
C {devices/opin.sym} 1560 660 0 0 {name=p25 lab=dig_out[6]}
C {devices/opin.sym} 1560 700 0 0 {name=p26 lab=dig_out[7]}
C {devices/opin.sym} 1560 740 0 0 {name=p27 lab=dig_out[8]}
C {devices/opin.sym} 1560 780 0 0 {name=p28 lab=dig_out[9]}
C {devices/opin.sym} 1560 820 0 0 {name=p29 lab=dig_out[10]}
C {devices/opin.sym} 1560 860 0 0 {name=p30 lab=dig_out[11]}
C {devices/iopin.sym} 1560 220 0 0 {name=p31 lab=analog_bus0}
C {devices/iopin.sym} 1560 1040 0 0 {name=p32 lab=analog_bus1}
C {devices/iopin.sym} 1560 1520 0 0 {name=p33 lab=analog_bus2}
C {devices/iopin.sym} 1560 1560 0 0 {name=p34 lab=analog_bus3}
C {devices/ipin.sym} 60 1920 0 0 {name=p35 lab=ibias0}
C {devices/ipin.sym} 60 1960 0 0 {name=p36 lab=ibias1}
C {tp_en_ctrl.sym} 400 640 0 0 {name=xctl}
N 60 0 1280 0 {lab=vdd_3v3}
N 60 1240 1280 1240 {lab=vss_3v3}
N 400 60 400 0 {lab=vdd_3v3}
N 400 1220 400 1240 {lab=vss_3v3}
N 60 120 220 120 {lab=vdd_1v2}
N 60 1160 220 1160 {lab=vss_1v2}
N 60 200 220 200 {lab=dig_in[0]}
N 60 240 220 240 {lab=dig_in[1]}
N 60 280 220 280 {lab=dig_in[2]}
N 60 320 220 320 {lab=dig_in[3]}
N 60 360 220 360 {lab=enable}
N 580 420 1560 420 {lab=dig_out[0]}
N 580 460 1560 460 {lab=dig_out[1]}
N 580 500 1560 500 {lab=dig_out[2]}
N 580 540 1560 540 {lab=dig_out[3]}
N 580 580 1560 580 {lab=dig_out[4]}
N 580 620 1560 620 {lab=dig_out[5]}
N 580 660 1560 660 {lab=dig_out[6]}
N 580 700 1560 700 {lab=dig_out[7]}
N 580 740 1560 740 {lab=dig_out[8]}
N 580 780 1560 780 {lab=dig_out[9]}
N 580 820 1560 820 {lab=dig_out[10]}
N 580 860 1560 860 {lab=dig_out[11]}
C {oa_core_pd.sym} 900 220 0 0 {name=xoa}
C {xgate.sym} 1200 210 0 0 {name=xtg0}
N 580 200 840 200 {lab=en_oa}
N 580 240 840 240 {lab=en_oa_b}
C {devices/lab_wire.sym} 700 200 0 1 {name=lw1 sig_type=std_logic lab=en_oa}
C {devices/lab_wire.sym} 700 240 0 1 {name=lw2 sig_type=std_logic lab=en_oa_b}
N 960 220 1120 220 {lab=i_oa}
C {devices/lab_wire.sym} 1040 220 0 1 {name=lw3 sig_type=std_logic lab=i_oa}
N 1260 220 1560 220 {lab=analog_bus0}
N 580 120 1190 120 {lab=en_tg0_b}
N 1190 120 1190 160 {lab=en_tg0_b}
N 580 340 1190 340 {lab=en_tg0}
N 1190 340 1190 280 {lab=en_tg0}
C {devices/lab_wire.sym} 700 120 0 1 {name=lw4 sig_type=std_logic lab=en_tg0_b}
C {devices/lab_wire.sym} 700 340 0 1 {name=lw5 sig_type=std_logic lab=en_tg0}
N 920 160 920 0 {lab=vdd_3v3}
N 900 280 900 300 {lab=vss_3v3}
C {devices/lab_pin.sym} 900 300 0 1 {name=l6 sig_type=std_logic lab=vss_3v3}
N 1260 190 1280 190 {lab=vdd_3v3}
N 1280 190 1280 0 {lab=vdd_3v3}
N 1260 250 1300 250 {lab=vss_3v3}
C {devices/lab_pin.sym} 1300 250 0 1 {name=l7 sig_type=std_logic lab=vss_3v3}
C {bg_core_pd.sym} 900 1040 0 0 {name=xbg}
C {xgate.sym} 1200 1030 0 0 {name=xtg1}
N 580 1020 840 1020 {lab=en_bg}
N 580 1060 840 1060 {lab=en_bg_b}
C {devices/lab_wire.sym} 700 1020 0 1 {name=lw8 sig_type=std_logic lab=en_bg}
C {devices/lab_wire.sym} 700 1060 0 1 {name=lw9 sig_type=std_logic lab=en_bg_b}
N 960 1040 1120 1040 {lab=i_bg}
C {devices/lab_wire.sym} 1040 1040 0 1 {name=lw10 sig_type=std_logic lab=i_bg}
N 1260 1040 1560 1040 {lab=analog_bus1}
N 580 920 1190 920 {lab=en_tg1_b}
N 1190 920 1190 980 {lab=en_tg1_b}
N 580 1160 1190 1160 {lab=en_tg1}
N 1190 1160 1190 1100 {lab=en_tg1}
C {devices/lab_wire.sym} 700 920 0 1 {name=lw11 sig_type=std_logic lab=en_tg1_b}
C {devices/lab_wire.sym} 700 1160 0 1 {name=lw12 sig_type=std_logic lab=en_tg1}
N 900 1100 900 1240 {lab=vss_3v3}
N 920 980 920 960 {lab=vdd_3v3}
C {devices/lab_pin.sym} 920 960 0 1 {name=l13 sig_type=std_logic lab=vdd_3v3}
N 1260 1070 1280 1070 {lab=vss_3v3}
N 1280 1070 1280 1240 {lab=vss_3v3}
N 1260 1010 1300 1010 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1300 1010 0 1 {name=l14 sig_type=std_logic lab=vdd_3v3}
C {slot7_stage_b.sym} 400 1680 0 0 {name=xb}
N 60 1480 220 1480 {lab=dig_in[4]}
N 60 1520 220 1520 {lab=dig_in[5]}
N 60 1560 220 1560 {lab=dig_in[6]}
N 60 1600 220 1600 {lab=dig_in[7]}
N 60 1640 220 1640 {lab=dig_in[8]}
N 60 1680 220 1680 {lab=dig_in[9]}
N 60 1720 220 1720 {lab=dig_in[10]}
N 60 1760 220 1760 {lab=dig_in[11]}
N 60 1800 220 1800 {lab=dig_in[12]}
N 60 1920 220 1920 {lab=ibias0}
N 60 1960 220 1960 {lab=ibias1}
N 220 1360 180 1360 {lab=vdd_3v3}
C {devices/lab_pin.sym} 180 1360 0 0 {name=l15 sig_type=std_logic lab=vdd_3v3}
N 220 1400 180 1400 {lab=vdd_1v2}
C {devices/lab_pin.sym} 180 1400 0 0 {name=l16 sig_type=std_logic lab=vdd_1v2}
N 220 1440 180 1440 {lab=enable}
C {devices/lab_pin.sym} 180 1440 0 0 {name=l17 sig_type=std_logic lab=enable}
N 220 2000 180 2000 {lab=vss_3v3}
C {devices/lab_pin.sym} 180 2000 0 0 {name=l18 sig_type=std_logic lab=vss_3v3}
N 220 1840 180 1840 {lab=i_oa}
C {devices/lab_pin.sym} 180 1840 0 0 {name=l19 sig_type=std_logic lab=i_oa}
N 220 1880 180 1880 {lab=i_bg}
C {devices/lab_pin.sym} 180 1880 0 0 {name=l20 sig_type=std_logic lab=i_bg}
N 580 1520 1560 1520 {lab=analog_bus2}
N 580 1560 1560 1560 {lab=analog_bus3}
T {slot7_testplatform_ab: stage A (OA / BG cores, bus switches to analog_bus0 / analog_bus1, read-back, tie-lows) and stage B (xb: tree, reference select, bias mux)} 0 -200 0 0 0.5 0.5 {}
T {stage A as in slot7_testplatform.sch; xb takes the cores' output nets i_oa / i_bg and the shared vdd_3v3 / vss_3v3 / vdd_1v2 / enable by label} 0 -150 0 0 0.3 0.3 {}
T {source: ../../netlist/source/slot7_stage_b.spice (slot7_testplatform_ab); plan: docs/slot7_testplatform/PLAN.md section 9} 0 -120 0 0 0.3 0.3 {}
C {devices/title.sym} 160 2160 0 0 {name=l_title author="Christoph Maier"}
