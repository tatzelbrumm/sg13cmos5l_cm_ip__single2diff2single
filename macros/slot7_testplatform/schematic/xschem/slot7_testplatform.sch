v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {devices/iopin.sym} -400 -600 0 0 {name=p1 lab=vdd_3v3}
C {devices/iopin.sym} -400 -560 0 0 {name=p2 lab=vss_3v3}
C {devices/iopin.sym} -400 -520 0 0 {name=p3 lab=vdd_1v2}
C {devices/iopin.sym} -400 -480 0 0 {name=p4 lab=vss_1v2}
C {devices/ipin.sym} -400 -440 0 0 {name=p5 lab=enable}
C {devices/ipin.sym} -400 -400 0 0 {name=p6 lab=dig_in[0]}
C {devices/ipin.sym} -400 -360 0 0 {name=p7 lab=dig_in[1]}
C {devices/ipin.sym} -400 -320 0 0 {name=p8 lab=dig_in[2]}
C {devices/ipin.sym} -400 -280 0 0 {name=p9 lab=dig_in[3]}
C {devices/opin.sym} -400 -240 0 0 {name=p10 lab=dig_out[0]}
C {devices/opin.sym} -400 -200 0 0 {name=p11 lab=dig_out[1]}
C {devices/opin.sym} -400 -160 0 0 {name=p12 lab=dig_out[2]}
C {devices/opin.sym} -400 -120 0 0 {name=p13 lab=dig_out[3]}
C {devices/opin.sym} -400 -80 0 0 {name=p14 lab=dig_out[4]}
C {devices/opin.sym} -400 -40 0 0 {name=p15 lab=dig_out[5]}
C {devices/opin.sym} -400 0 0 0 {name=p16 lab=dig_out[6]}
C {devices/opin.sym} -400 40 0 0 {name=p17 lab=dig_out[7]}
C {devices/opin.sym} -400 80 0 0 {name=p18 lab=dig_out[8]}
C {devices/opin.sym} -400 120 0 0 {name=p19 lab=dig_out[9]}
C {devices/opin.sym} -400 160 0 0 {name=p20 lab=dig_out[10]}
C {devices/opin.sym} -400 200 0 0 {name=p21 lab=dig_out[11]}
C {devices/iopin.sym} -400 240 0 0 {name=p22 lab=analog_bus0}
C {devices/iopin.sym} -400 280 0 0 {name=p23 lab=analog_bus1}
C {tp_en_ctrl.sym} 0 0 0 0 {name=ctl}
N -180.0 -380.0 -220.0 -380.0 {lab=vdd_3v3}
C {devices/lab_pin.sym} -220.0 -380.0 0 0 {name=l1 sig_type=std_logic lab=vdd_3v3}
N -180.0 -340.0 -220.0 -340.0 {lab=vss_3v3}
C {devices/lab_pin.sym} -220.0 -340.0 0 0 {name=l2 sig_type=std_logic lab=vss_3v3}
N -180.0 -300.0 -220.0 -300.0 {lab=vdd_1v2}
C {devices/lab_pin.sym} -220.0 -300.0 0 0 {name=l3 sig_type=std_logic lab=vdd_1v2}
N -180.0 -260.0 -220.0 -260.0 {lab=vss_1v2}
C {devices/lab_pin.sym} -220.0 -260.0 0 0 {name=l4 sig_type=std_logic lab=vss_1v2}
N -180.0 -220.0 -220.0 -220.0 {lab=dig_in[0]}
C {devices/lab_pin.sym} -220.0 -220.0 0 0 {name=l5 sig_type=std_logic lab=dig_in[0]}
N -180.0 -180.0 -220.0 -180.0 {lab=dig_in[1]}
C {devices/lab_pin.sym} -220.0 -180.0 0 0 {name=l6 sig_type=std_logic lab=dig_in[1]}
N -180.0 -140.0 -220.0 -140.0 {lab=dig_in[2]}
C {devices/lab_pin.sym} -220.0 -140.0 0 0 {name=l7 sig_type=std_logic lab=dig_in[2]}
N -180.0 -100.0 -220.0 -100.0 {lab=dig_in[3]}
C {devices/lab_pin.sym} -220.0 -100.0 0 0 {name=l8 sig_type=std_logic lab=dig_in[3]}
N -180.0 -60.0 -220.0 -60.0 {lab=enable}
C {devices/lab_pin.sym} -220.0 -60.0 0 0 {name=l9 sig_type=std_logic lab=enable}
N 180.0 -380.0 220.0 -380.0 {lab=en_oa}
C {devices/lab_pin.sym} 220.0 -380.0 0 1 {name=l10 sig_type=std_logic lab=en_oa}
N 180.0 -340.0 220.0 -340.0 {lab=en_oa_b}
C {devices/lab_pin.sym} 220.0 -340.0 0 1 {name=l11 sig_type=std_logic lab=en_oa_b}
N 180.0 -300.0 220.0 -300.0 {lab=en_bg}
C {devices/lab_pin.sym} 220.0 -300.0 0 1 {name=l12 sig_type=std_logic lab=en_bg}
N 180.0 -260.0 220.0 -260.0 {lab=en_bg_b}
C {devices/lab_pin.sym} 220.0 -260.0 0 1 {name=l13 sig_type=std_logic lab=en_bg_b}
N 180.0 -220.0 220.0 -220.0 {lab=en_tg0}
C {devices/lab_pin.sym} 220.0 -220.0 0 1 {name=l14 sig_type=std_logic lab=en_tg0}
N 180.0 -180.0 220.0 -180.0 {lab=en_tg0_b}
C {devices/lab_pin.sym} 220.0 -180.0 0 1 {name=l15 sig_type=std_logic lab=en_tg0_b}
N 180.0 -140.0 220.0 -140.0 {lab=en_tg1}
C {devices/lab_pin.sym} 220.0 -140.0 0 1 {name=l16 sig_type=std_logic lab=en_tg1}
N 180.0 -100.0 220.0 -100.0 {lab=en_tg1_b}
C {devices/lab_pin.sym} 220.0 -100.0 0 1 {name=l17 sig_type=std_logic lab=en_tg1_b}
N 180.0 -60.0 220.0 -60.0 {lab=dig_out[0]}
C {devices/lab_pin.sym} 220.0 -60.0 0 1 {name=l18 sig_type=std_logic lab=dig_out[0]}
N 180.0 -20.0 220.0 -20.0 {lab=dig_out[1]}
C {devices/lab_pin.sym} 220.0 -20.0 0 1 {name=l19 sig_type=std_logic lab=dig_out[1]}
N 180.0 20.0 220.0 20.0 {lab=dig_out[2]}
C {devices/lab_pin.sym} 220.0 20.0 0 1 {name=l20 sig_type=std_logic lab=dig_out[2]}
N 180.0 60.0 220.0 60.0 {lab=dig_out[3]}
C {devices/lab_pin.sym} 220.0 60.0 0 1 {name=l21 sig_type=std_logic lab=dig_out[3]}
N 180.0 100.0 220.0 100.0 {lab=dig_out[4]}
C {devices/lab_pin.sym} 220.0 100.0 0 1 {name=l22 sig_type=std_logic lab=dig_out[4]}
N 180.0 140.0 220.0 140.0 {lab=dig_out[5]}
C {devices/lab_pin.sym} 220.0 140.0 0 1 {name=l23 sig_type=std_logic lab=dig_out[5]}
N 180.0 180.0 220.0 180.0 {lab=dig_out[6]}
C {devices/lab_pin.sym} 220.0 180.0 0 1 {name=l24 sig_type=std_logic lab=dig_out[6]}
N 180.0 220.0 220.0 220.0 {lab=dig_out[7]}
C {devices/lab_pin.sym} 220.0 220.0 0 1 {name=l25 sig_type=std_logic lab=dig_out[7]}
N 180.0 260.0 220.0 260.0 {lab=dig_out[8]}
C {devices/lab_pin.sym} 220.0 260.0 0 1 {name=l26 sig_type=std_logic lab=dig_out[8]}
N 180.0 300.0 220.0 300.0 {lab=dig_out[9]}
C {devices/lab_pin.sym} 220.0 300.0 0 1 {name=l27 sig_type=std_logic lab=dig_out[9]}
N 180.0 340.0 220.0 340.0 {lab=dig_out[10]}
C {devices/lab_pin.sym} 220.0 340.0 0 1 {name=l28 sig_type=std_logic lab=dig_out[10]}
N 180.0 380.0 220.0 380.0 {lab=dig_out[11]}
C {devices/lab_pin.sym} 220.0 380.0 0 1 {name=l29 sig_type=std_logic lab=dig_out[11]}
C {oa_core_pd.sym} 700 -400 0 0 {name=oa}
N 720.0 -460.0 720.0 -500.0 {lab=vdd_3v3}
C {devices/lab_pin.sym} 720.0 -500.0 0 1 {name=l30 sig_type=std_logic lab=vdd_3v3}
N 700.0 -340.0 700.0 -300.0 {lab=vss_3v3}
C {devices/lab_pin.sym} 700.0 -300.0 0 1 {name=l31 sig_type=std_logic lab=vss_3v3}
N 760.0 -400.0 800.0 -400.0 {lab=i_oa}
C {devices/lab_pin.sym} 800.0 -400.0 0 1 {name=l32 sig_type=std_logic lab=i_oa}
N 640.0 -420.0 600.0 -420.0 {lab=en_oa}
C {devices/lab_pin.sym} 600.0 -420.0 0 0 {name=l33 sig_type=std_logic lab=en_oa}
N 640.0 -380.0 600.0 -380.0 {lab=en_oa_b}
C {devices/lab_pin.sym} 600.0 -380.0 0 0 {name=l34 sig_type=std_logic lab=en_oa_b}
C {bg_core_pd.sym} 700 0 0 0 {name=bg}
N 720.0 -60.0 720.0 -100.0 {lab=vdd_3v3}
C {devices/lab_pin.sym} 720.0 -100.0 0 1 {name=l35 sig_type=std_logic lab=vdd_3v3}
N 700.0 60.0 700.0 100.0 {lab=vss_3v3}
C {devices/lab_pin.sym} 700.0 100.0 0 1 {name=l36 sig_type=std_logic lab=vss_3v3}
N 760.0 0.0 800.0 0.0 {lab=i_bg}
C {devices/lab_pin.sym} 800.0 0.0 0 1 {name=l37 sig_type=std_logic lab=i_bg}
N 640.0 -20.0 600.0 -20.0 {lab=en_bg}
C {devices/lab_pin.sym} 600.0 -20.0 0 0 {name=l38 sig_type=std_logic lab=en_bg}
N 640.0 20.0 600.0 20.0 {lab=en_bg_b}
C {devices/lab_pin.sym} 600.0 20.0 0 0 {name=l39 sig_type=std_logic lab=en_bg_b}
C {xgate.sym} 1300 -400 0 0 {name=tg0}
N 1290.0 -450.0 1290.0 -490.0 {lab=en_tg0_b}
C {devices/lab_pin.sym} 1290.0 -490.0 0 1 {name=l40 sig_type=std_logic lab=en_tg0_b}
N 1360.0 -420.0 1400.0 -420.0 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1400.0 -420.0 0 1 {name=l41 sig_type=std_logic lab=vdd_3v3}
N 1220.0 -390.0 1180.0 -390.0 {lab=i_oa}
C {devices/lab_pin.sym} 1180.0 -390.0 0 0 {name=l42 sig_type=std_logic lab=i_oa}
N 1360.0 -390.0 1400.0 -390.0 {lab=analog_bus0}
C {devices/lab_pin.sym} 1400.0 -390.0 0 1 {name=l43 sig_type=std_logic lab=analog_bus0}
N 1360.0 -360.0 1400.0 -360.0 {lab=vss_3v3}
C {devices/lab_pin.sym} 1400.0 -360.0 0 1 {name=l44 sig_type=std_logic lab=vss_3v3}
N 1290.0 -330.0 1290.0 -290.0 {lab=en_tg0}
C {devices/lab_pin.sym} 1290.0 -290.0 0 1 {name=l45 sig_type=std_logic lab=en_tg0}
C {xgate.sym} 1300 0 0 0 {name=tg1}
N 1290.0 -50.0 1290.0 -90.0 {lab=en_tg1_b}
C {devices/lab_pin.sym} 1290.0 -90.0 0 1 {name=l46 sig_type=std_logic lab=en_tg1_b}
N 1360.0 -20.0 1400.0 -20.0 {lab=vdd_3v3}
C {devices/lab_pin.sym} 1400.0 -20.0 0 1 {name=l47 sig_type=std_logic lab=vdd_3v3}
N 1220.0 10.0 1180.0 10.0 {lab=i_bg}
C {devices/lab_pin.sym} 1180.0 10.0 0 0 {name=l48 sig_type=std_logic lab=i_bg}
N 1360.0 10.0 1400.0 10.0 {lab=analog_bus1}
C {devices/lab_pin.sym} 1400.0 10.0 0 1 {name=l49 sig_type=std_logic lab=analog_bus1}
N 1360.0 40.0 1400.0 40.0 {lab=vss_3v3}
C {devices/lab_pin.sym} 1400.0 40.0 0 1 {name=l50 sig_type=std_logic lab=vss_3v3}
N 1290.0 70.0 1290.0 110.0 {lab=en_tg1}
C {devices/lab_pin.sym} 1290.0 110.0 0 1 {name=l51 sig_type=std_logic lab=en_tg1}
T {slot7_testplatform (stage A): OA / BG cores, fail-safe enables, iout -> analog_bus0 / analog_bus1 through xgate (dig_in[2] / dig_in[3] via tp_en_ctrl); docs/slot7_testplatform/PLAN.md} -400 -720 0 0 0.3 0.3 {}
T {slot7_testplatform (draft sheet, generated by gen_sheets.py)} -400 -780 0 0 0.5 0.5 {}
