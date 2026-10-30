v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sg13cmos5l_IOPadDiff2Single: differential in, single-ended out, class-AB, pad - vref = (vinp - vinn) / 2} 0 -560 0 0 0.5 0.5 {}
T {Custom padframe cell (case (a)): OP / ON of d2s_mpdda_pd are the pad's ESD clamp frames. Everything runs on the ring rails iovdd / iovss;} 0 -510 0 0 0.3 0.3 {}
T {the 1.2 V core ring vdd only feeds the level shifters' input inverters. vfb is tied to pad here (Kelvin tap at the pad).} 0 -480 0 0 0.3 0.3 {}
T {Slot fallback: iovdd = vdd_3v3, iovss = vss_3v3, vdd = vdd_1v2, vss = vss_1v2, pad = s7_an[1]. Netlist reference: ../../netlist/source/sg13cmos5l_IOPadDiff2Single.spice} 0 -450 0 0 0.3 0.3 {}
T {[C] enable / bias select: en_3v3 = en_1v2 AND vdd_1v2 present AND vdd_3v3 present} 300 -330 0 0 0.3 0.3 {}
T {[B] bias: sel 00 harness ibias (sourced, 5 uA), 01 Oguey-Aebischer, 10 bandgap, 11 both} 300 30 0 0 0.3 0.3 {}
T {[D] class-AB driver with power-down} 900 -330 0 0 0.3 0.3 {}
T {[P] IHP primary diodes (as in sg13cmos5l_IOPadAnalog)} 900 330 0 0 0.3 0.3 {}
C {devices/iopin.sym} 0 -400 0 0 {name=p1 lab=iovdd}
C {devices/iopin.sym} 0 -380 0 0 {name=p2 lab=iovss}
C {devices/iopin.sym} 0 -360 0 0 {name=p3 lab=vdd}
C {devices/iopin.sym} 0 -340 0 0 {name=p4 lab=vss}
C {devices/iopin.sym} 0 -320 0 0 {name=p5 lab=pad}
C {devices/ipin.sym} 0 -300 0 0 {name=p6 lab=vinp}
C {devices/ipin.sym} 0 -280 0 0 {name=p7 lab=vinn}
C {devices/ipin.sym} 0 -260 0 0 {name=p8 lab=vref}
C {devices/ipin.sym} 0 -240 0 0 {name=p9 lab=ibias}
C {devices/ipin.sym} 0 -220 0 0 {name=p10 lab=en_1v2}
C {devices/ipin.sym} 0 -200 0 0 {name=p11 lab=sel0_1v2}
C {devices/ipin.sym} 0 -180 0 0 {name=p12 lab=sel1_1v2}
C {devices/ipin.sym} 0 -160 0 0 {name=p13 lab=vdd1v2_sense}
C {devices/ipin.sym} 0 -140 0 0 {name=p14 lab=vdd3v3_sense}
C {en_ctrl_3v3.sym} 500 -200 0 0 {name=xc}
C {devices/lab_pin.sym} 440 -280 0 1 {name=l0 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 460 -280 0 1 {name=l1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 440 -120 0 1 {name=l2 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 400 -240 0 0 {name=l3 sig_type=std_logic lab=en_1v2}
C {devices/lab_pin.sym} 400 -220 0 0 {name=l4 sig_type=std_logic lab=sel0_1v2}
C {devices/lab_pin.sym} 400 -200 0 0 {name=l5 sig_type=std_logic lab=sel1_1v2}
C {devices/lab_pin.sym} 400 -180 0 0 {name=l6 sig_type=std_logic lab=vdd1v2_sense}
C {devices/lab_pin.sym} 400 -160 0 0 {name=l7 sig_type=std_logic lab=vdd3v3_sense}
C {devices/lab_pin.sym} 600 -240 0 1 {name=l8 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 600 -220 0 1 {name=l9 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_pin.sym} 600 -200 0 1 {name=l10 sig_type=std_logic lab=sel1_3v3}
C {d2s_bias_sel_pd.sym} 500 200 0 0 {name=xb}
C {devices/lab_pin.sym} 430 110 0 1 {name=l11 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 430 290 0 1 {name=l12 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 450 110 0 1 {name=l13 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 450 290 0 1 {name=l14 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 390 150 0 0 {name=l15 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 610 150 0 1 {name=l16 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 610 170 0 1 {name=l17 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 610 190 0 1 {name=l18 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 610 210 0 1 {name=l19 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 610 230 0 1 {name=l20 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 610 250 0 1 {name=l21 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 390 170 0 0 {name=l22 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 390 190 0 0 {name=l23 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_pin.sym} 390 210 0 0 {name=l24 sig_type=std_logic lab=sel1_3v3}
C {d2s_mpdda_pd.sym} 1200 -100 0 0 {name=xd}
C {devices/lab_pin.sym} 1080 -220 0 0 {name=l25 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1080 20 0 0 {name=l26 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1360 -220 0 1 {name=l27 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1360 20 0 1 {name=l28 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1020 -160 0 0 {name=l29 sig_type=std_logic lab=vinp}
C {devices/lab_pin.sym} 1020 -120 0 0 {name=l30 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 1020 -80 0 0 {name=l31 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 1420 -160 0 1 {name=l32 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1020 -40 0 0 {name=l33 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1120 20 0 1 {name=l34 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1160 20 0 1 {name=l35 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 1200 20 0 1 {name=l36 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 1240 20 0 1 {name=l37 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 1280 20 0 1 {name=l38 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 1320 20 0 1 {name=l39 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 1020 -180 0 0 {name=l40 sig_type=std_logic lab=en_3v3}
C {sg13cmos5l_DCNDiode.sym} 1100 450 0 0 {name=DN}
C {devices/lab_pin.sym} 1000 460 0 0 {name=l41 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1000 480 0 0 {name=l42 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1000 500 0 0 {name=l43 sig_type=std_logic lab=iovdd}
C {sg13cmos5l_DCPDiode.sym} 1400 450 0 0 {name=DP}
C {devices/lab_pin.sym} 1300 460 0 0 {name=l44 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1300 480 0 0 {name=l45 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1300 500 0 0 {name=l46 sig_type=std_logic lab=iovss}
C {devices/title.sym} 160 900 0 0 {name=l_title author="Christoph Maier"}
