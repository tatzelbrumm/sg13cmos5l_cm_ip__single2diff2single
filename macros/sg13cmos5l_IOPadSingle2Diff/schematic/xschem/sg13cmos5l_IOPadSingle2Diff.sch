v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sg13cmos5l_IOPadSingle2Diff (SCAFFOLD): single-ended pad in, differential out, outp - vcm = vcm - outn = pad - vref} 0 -560 0 0 0.5 0.5 {}
T {Same ring / control / bias infrastructure as sg13cmos5l_IOPadDiff2Single. Input protection as IHP's sg13cmos5l_IOPadAnalog (clamps gate-tied, primary diodes,} 0 -510 0 0 0.3 0.3 {}
T {secondary protection with its 587 Ohm rppd between pad and padres). xa = s2d_core_ideal is a BEHAVIOURAL PLACEHOLDER: replace it by the real input buffer.} 0 -480 0 0 0.3 0.3 {}
T {[C] enable / bias select} 300 -330 0 0 0.3 0.3 {}
T {[B] bias} 300 30 0 0 0.3 0.3 {}
T {[A] input buffer core (placeholder)} 900 -330 0 0 0.3 0.3 {}
T {[P] input protection (IHP IO cells)} 900 330 0 0 0.3 0.3 {}
C {devices/iopin.sym} 0 -400 0 0 {name=p1 lab=iovdd}
C {devices/iopin.sym} 0 -380 0 0 {name=p2 lab=iovss}
C {devices/iopin.sym} 0 -360 0 0 {name=p3 lab=vdd}
C {devices/iopin.sym} 0 -340 0 0 {name=p4 lab=vss}
C {devices/iopin.sym} 0 -320 0 0 {name=p5 lab=pad}
C {devices/opin.sym} 0 -300 0 0 {name=p6 lab=outp}
C {devices/opin.sym} 0 -280 0 0 {name=p7 lab=outn}
C {devices/ipin.sym} 0 -260 0 0 {name=p8 lab=vcm}
C {devices/ipin.sym} 0 -240 0 0 {name=p9 lab=vref}
C {devices/ipin.sym} 0 -220 0 0 {name=p10 lab=ibias}
C {devices/ipin.sym} 0 -200 0 0 {name=p11 lab=en_1v2}
C {devices/ipin.sym} 0 -180 0 0 {name=p12 lab=sel0_1v2}
C {devices/ipin.sym} 0 -160 0 0 {name=p13 lab=sel1_1v2}
C {devices/ipin.sym} 0 -140 0 0 {name=p14 lab=vdd1v2_sense}
C {devices/ipin.sym} 0 -120 0 0 {name=p15 lab=vdd3v3_sense}
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
C {s2d_core_ideal.sym} 1200 -100 0 0 {name=xa}
C {devices/lab_pin.sym} 1080 -220 0 0 {name=l25 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1080 20 0 0 {name=l26 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1020 -160 0 0 {name=l27 sig_type=std_logic lab=padres}
C {devices/lab_pin.sym} 1020 -130 0 0 {name=l28 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 1020 -100 0 0 {name=l29 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 1380 -140 0 1 {name=l30 sig_type=std_logic lab=outp}
C {devices/lab_pin.sym} 1380 -100 0 1 {name=l31 sig_type=std_logic lab=outn}
C {devices/lab_pin.sym} 1140 20 0 1 {name=l32 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1170 20 0 1 {name=l33 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 1200 20 0 1 {name=l34 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 1230 20 0 1 {name=l35 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 1260 20 0 1 {name=l36 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 1290 20 0 1 {name=l37 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 1020 -70 0 0 {name=l38 sig_type=std_logic lab=en_3v3}
C {sg13cmos5l_Clamp_P20N0D.sym} 1000 450 0 0 {name=CP}
C {devices/lab_pin.sym} 900 460 0 0 {name=l39 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 900 480 0 0 {name=l40 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 900 500 0 0 {name=l41 sig_type=std_logic lab=pad}
C {sg13cmos5l_Clamp_N20N0D.sym} 1250 450 0 0 {name=CN}
C {devices/lab_pin.sym} 1150 460 0 0 {name=l42 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1150 480 0 0 {name=l43 sig_type=std_logic lab=pad}
C {sg13cmos5l_DCNDiode.sym} 1000 620 0 0 {name=DN}
C {devices/lab_pin.sym} 900 630 0 0 {name=l44 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 900 650 0 0 {name=l45 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 900 670 0 0 {name=l46 sig_type=std_logic lab=iovdd}
C {sg13cmos5l_DCPDiode.sym} 1250 620 0 0 {name=DP}
C {devices/lab_pin.sym} 1150 630 0 0 {name=l47 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1150 650 0 0 {name=l48 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1150 670 0 0 {name=l49 sig_type=std_logic lab=iovss}
C {sg13cmos5l_SecondaryProtection.sym} 1500 450 0 0 {name=SP}
C {devices/lab_pin.sym} 1400 460 0 0 {name=l50 sig_type=std_logic lab=padres}
C {devices/lab_pin.sym} 1400 480 0 0 {name=l51 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1400 500 0 0 {name=l52 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 1400 520 0 0 {name=l53 sig_type=std_logic lab=iovdd}
C {devices/title.sym} 160 900 0 0 {name=l_title author="Christoph Maier"}
