v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sg13cmos5l_IOPadDiff2Single: differential in, single-ended out, class-AB, pad - vref = (vinp - vinn) / 2} 0 -830 0 0 0.5 0.5 {}
T {Custom padframe cell (case (a)): OP / ON of d2s_mpdda_pd are the pad's ESD clamp frames. Everything runs on the ring rails iovdd / iovss;} 0 -780 0 0 0.3 0.3 {}
T {the 1.2 V core ring vdd only feeds the level shifters' input inverters. vfb is tied to pad here (Kelvin tap at the pad).} 0 -750 0 0 0.3 0.3 {}
T {Slot fallback: iovdd = vdd_3v3, iovss = vss_3v3, vdd = vdd_1v2, vss = vss_1v2, pad = s7_an[1]. Netlist reference: ../../netlist/source/sg13cmos5l_IOPadDiff2Single.spice} 0 -720 0 0 0.3 0.3 {}
T {[C] enable / bias select: en_3v3 = en_1v2 AND vdd_1v2 present AND vdd_3v3 present} 150 -120 0 0 0.3 0.3 {}
T {[B] bias: sel 00 harness ibias (sourced, 5 uA), 01 Oguey-Aebischer, 10 bandgap, 11 both} 470 -160 0 0 0.3 0.3 {}
T {[D] class-AB driver with power-down} 760 -590 0 0 0.3 0.3 {}
T {[P] IHP primary diodes (as in sg13cmos5l_IOPadAnalog)} 1120 -570 0 0 0.3 0.3 {}
N 1020 -360 1020 -100 {lab=iovss}
N 800 -100 1020 -100 {lab=iovss}
N 800 -360 800 -100 {lab=iovss}
N 860 -360 860 -320 {lab=vbp}
N 660 -320 860 -320 {lab=vbp}
N 880 -360 880 -300 {lab=vbpc}
N 660 -300 880 -300 {lab=vbpc}
N 900 -360 900 -280 {lab=vabp}
N 660 -280 900 -280 {lab=vabp}
N 940 -360 940 -260 {lab=vabn}
N 660 -260 940 -260 {lab=vabn}
N 960 -360 960 -240 {lab=vbnc}
N 660 -240 960 -240 {lab=vbnc}
N 980 -360 980 -220 {lab=vbn}
N 660 -220 980 -220 {lab=vbn}
N 240 -140 240 -100 {lab=iovss}
N 560 -100 800 -100 {lab=iovss}
N 400 -260 440 -260 {lab=en_3v3}
N 440 -280 440 -260 {lab=en_3v3}
N 440 -520 740 -520 {lab=en_3v3}
N 440 -280 480 -280 {lab=en_3v3}
N 440 -520 440 -280 {lab=en_3v3}
N 400 -240 480 -240 {lab=sel0_3v3}
N 400 -220 480 -220 {lab=sel1_3v3}
N 520 -180 520 -100 {lab=iovss}
N 240 -100 520 -100 {lab=iovss}
N 560 -180 560 -100 {lab=iovss}
N 520 -100 560 -100 {lab=iovss}
N 1120 -280 1140 -280 {lab=pad}
N 1120 -340 1120 -280 {lab=pad}
N 1100 -480 1120 -480 {lab=pad}
N 1180 -220 1180 -100 {lab=iovss}
N 1020 -100 1180 -100 {lab=iovss}
N 1180 -100 1240 -100 {lab=iovss}
N 1120 -460 1120 -340 {lab=pad}
N 160 -260 200 -260 {lab=en_1v2}
N 160 -240 200 -240 {lab=sel0_1v2}
N 160 -220 200 -220 {lab=sel1_1v2}
N 160 -200 200 -200 {lab=vdd1v2_sense}
N 160 -180 200 -180 {lab=vdd3v3_sense}
N 160 -320 480 -320 {lab=ibias}
N 1120 -480 1200 -480 {lab=pad}
N 1240 -440 1240 -100 {lab=iovss}
N 1100 -460 1120 -460 {lab=pad}
N 1120 -480 1120 -460 {lab=pad}
N 160 -100 240 -100 {lab=iovss}
N 160 -420 740 -420 {lab=vref}
N 160 -460 740 -460 {lab=vinn}
N 160 -480 740 -480 {lab=vinp}
N 260 -580 260 -300 {lab=vdd}
N 160 -580 260 -580 {lab=vdd}
N 240 -600 240 -300 {lab=iovdd}
N 160 -600 240 -600 {lab=iovdd}
N 1180 -600 1240 -600 {lab=iovdd}
N 1240 -600 1240 -530 {lab=iovdd}
N 1120 -340 1280 -340 {lab=pad}
N 1180 -600 1180 -320 {lab=iovdd}
N 1040 -600 1180 -600 {lab=iovdd}
N 1040 -600 1040 -560 {lab=iovdd}
N 820 -600 1040 -600 {lab=iovdd}
N 820 -600 820 -560 {lab=iovdd}
N 580 -600 820 -600 {lab=iovdd}
N 580 -600 580 -360 {lab=iovdd}
N 540 -600 580 -600 {lab=iovdd}
N 540 -600 540 -360 {lab=iovdd}
N 240 -600 540 -600 {lab=iovdd}
C {devices/iopin.sym} 160 -600 0 1 {name=p1 lab=iovdd}
C {devices/iopin.sym} 160 -100 0 1 {name=p2 lab=iovss}
C {devices/iopin.sym} 160 -580 0 1 {name=p3 lab=vdd}
C {devices/iopin.sym} 160 -120 0 1 {name=p4 lab=vss}
C {devices/iopin.sym} 1280 -340 0 0 {name=p5 lab=pad}
C {devices/ipin.sym} 160 -480 0 0 {name=p6 lab=vinp}
C {devices/ipin.sym} 160 -460 0 0 {name=p7 lab=vinn}
C {devices/ipin.sym} 160 -420 0 0 {name=p8 lab=vref}
C {devices/ipin.sym} 160 -320 0 0 {name=p9 lab=ibias}
C {devices/ipin.sym} 160 -260 0 0 {name=p10 lab=en_1v2}
C {devices/ipin.sym} 160 -240 0 0 {name=p11 lab=sel0_1v2}
C {devices/ipin.sym} 160 -220 0 0 {name=p12 lab=sel1_1v2}
C {devices/ipin.sym} 160 -200 0 0 {name=p13 lab=vdd1v2_sense}
C {devices/ipin.sym} 160 -180 0 0 {name=p14 lab=vdd3v3_sense}
C {en_ctrl_3v3.sym} 300 -220 0 0 {name=xc}
C {devices/lab_pin.sym} 240 -300 0 0 {name=l0 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 260 -300 0 1 {name=l1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 240 -140 0 1 {name=l2 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 440 -260 0 1 {name=l8 sig_type=std_logic lab=en_3v3}
C {d2s_bias_sel_pd.sym} 570 -270 0 0 {name=xb}
C {devices/lab_pin.sym} 540 -360 0 0 {name=l11 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 520 -180 0 0 {name=l12 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 580 -360 0 1 {name=l13 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 560 -180 0 1 {name=l14 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 480 -320 0 0 {name=l15 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 440 -280 0 0 {name=l22 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 480 -240 0 0 {name=l23 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_pin.sym} 480 -220 0 0 {name=l24 sig_type=std_logic lab=sel1_3v3}
C {d2s_mpdda_pd.sym} 920 -460 0 0 {name=xd}
C {devices/lab_pin.sym} 820 -560 0 0 {name=l25 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 800 -360 0 0 {name=l26 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1040 -560 0 1 {name=l27 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1020 -360 0 1 {name=l28 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 740 -480 0 0 {name=l29 sig_type=std_logic lab=vinp}
C {devices/lab_pin.sym} 740 -460 0 0 {name=l30 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 740 -420 0 0 {name=l31 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 1100 -460 0 1 {name=l32 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 440 -520 0 0 {name=l40 sig_type=std_logic lab=en_3v3}
C {sg13cmos5l_DCNDiode.sym} 1180 -280 0 0 {name=DN}
C {devices/lab_pin.sym} 1180 -220 0 0 {name=l41 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1120 -280 0 0 {name=l42 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1180 -320 0 0 {name=l43 sig_type=std_logic lab=iovdd}
C {sg13cmos5l_DCPDiode.sym} 1240 -480 0 0 {name=DP}
C {devices/lab_pin.sym} 1200 -480 0 0 {name=l44 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1240 -540 0 0 {name=l45 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1240 -440 0 0 {name=l46 sig_type=std_logic lab=iovss}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
C {devices/lab_pin.sym} 860 -320 0 1 {name=l47 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 980 -220 0 1 {name=l48 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 880 -300 0 1 {name=l49 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 960 -240 0 1 {name=l50 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 900 -280 0 1 {name=l51 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 940 -260 0 1 {name=l52 sig_type=std_logic lab=vabn}
