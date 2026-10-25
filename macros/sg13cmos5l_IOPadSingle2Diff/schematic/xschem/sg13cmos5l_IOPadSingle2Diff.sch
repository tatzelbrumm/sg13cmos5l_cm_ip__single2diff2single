v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sg13cmos5l_IOPadSingle2Diff (SCAFFOLD): single-ended pad in, differential out, outp - vcm = vcm - outn = pad - vref} 0 -1020 0 0 0.5 0.5 {}
T {Same ring / control / bias infrastructure as sg13cmos5l_IOPadDiff2Single. Input protection as IHP's sg13cmos5l_IOPadAnalog (clamps gate-tied, primary diodes,} 0 -970 0 0 0.3 0.3 {}
T {secondary protection with its 587 Ohm rppd between pad and padres). xa = s2d_core_ideal is a BEHAVIOURAL PLACEHOLDER: replace it by the real input buffer.} 0 -940 0 0 0.3 0.3 {}
T {[C] enable / bias select} 220 -350 0 0 0.3 0.3 {}
T {[B] bias} 620 -410 0 0 0.3 0.3 {}
T {[A] input buffer core (placeholder)} 910 -640 0 0 0.3 0.3 {}
T {[P] input protection (IHP IO cells)} 730 -780 0 0 0.3 0.3 {}
N 880 -100 1040 -100 {lab=iovss}
N 1100 -360 1100 -320 {lab=vbp}
N 1120 -360 1120 -300 {lab=vbpc}
N 1140 -360 1140 -280 {lab=vabp}
N 1180 -360 1180 -260 {lab=vabn}
N 1200 -360 1200 -240 {lab=vbnc}
N 1220 -360 1220 -220 {lab=vbn}
N 680 -100 720 -100 {lab=iovss}
N 140 -100 360 -100 {lab=iovss}
N 360 -100 680 -100 {lab=iovss}
N 140 -200 320 -200 {lab=vdd1v2_sense}
N 140 -180 320 -180 {lab=vdd3v3_sense}
N 140 -220 320 -220 {lab=sel1_1v2}
N 140 -240 320 -240 {lab=sel0_1v2}
N 140 -260 320 -260 {lab=en_1v2}
N 360 -140 360 -100 {lab=iovss}
N 140 -320 640 -320 {lab=ibias}
N 680 -180 680 -100 {lab=iovss}
N 720 -180 720 -100 {lab=iovss}
N 1040 -360 1040 -100 {lab=iovss}
N 520 -240 640 -240 {lab=sel0_3v3}
N 520 -220 640 -220 {lab=sel1_3v3}
N 580 -280 580 -260 {lab=en_3v3}
N 1340 -520 1380 -520 {lab=outp}
N 1340 -480 1380 -480 {lab=outn}
N 580 -280 640 -280 {lab=en_3v3}
N 520 -260 580 -260 {lab=en_3v3}
N 580 -420 580 -280 {lab=en_3v3}
N 580 -420 980 -420 {lab=en_3v3}
N 520 -200 600 -200 {lab=en_3v3_b}
N 600 -260 600 -200 {lab=en_3v3_b}
N 600 -260 640 -260 {lab=en_3v3_b}
N 140 -500 980 -500 {lab=vref}
N 140 -460 980 -460 {lab=vcm}
N 820 -320 1100 -320 {lab=vbp}
N 820 -300 1120 -300 {lab=vbpc}
N 820 -280 1140 -280 {lab=vabp}
N 820 -260 1180 -260 {lab=vabn}
N 820 -240 1200 -240 {lab=vbnc}
N 820 -220 1220 -220 {lab=vbn}
N 720 -100 880 -100 {lab=iovss}
N 940 -700 960 -700 {lab=padres}
N 960 -540 980 -540 {lab=padres}
N 880 -560 880 -100 {lab=iovss}
N 960 -700 960 -540 {lab=padres}
N 620 -560 880 -560 {lab=iovss}
N 880 -660 880 -560 {lab=iovss}
N 620 -720 620 -560 {lab=iovss}
N 220 -740 220 -560 {lab=iovss}
N 300 -580 300 -560 {lab=iovss}
N 220 -560 300 -560 {lab=iovss}
N 240 -640 260 -640 {lab=pad}
N 240 -700 240 -640 {lab=pad}
N 540 -700 820 -700 {lab=pad}
N 180 -780 180 -700 {lab=pad}
N 180 -700 240 -700 {lab=pad}
N 540 -760 560 -760 {lab=pad}
N 540 -760 540 -700 {lab=pad}
N 540 -700 540 -660 {lab=pad}
N 540 -660 560 -660 {lab=pad}
N 240 -700 540 -700 {lab=pad}
N 300 -560 620 -560 {lab=iovss}
N 140 -700 180 -700 {lab=pad}
N 1060 -900 1060 -600 {lab=iovdd}
N 740 -900 1060 -900 {lab=iovdd}
N 140 -880 380 -880 {lab=vdd}
N 380 -880 380 -300 {lab=vdd}
N 360 -900 360 -300 {lab=iovdd}
N 300 -900 360 -900 {lab=iovdd}
N 700 -900 700 -360 {lab=iovdd}
N 620 -900 700 -900 {lab=iovdd}
N 740 -900 740 -360 {lab=iovdd}
N 700 -900 740 -900 {lab=iovdd}
N 220 -900 220 -840 {lab=iovdd}
N 140 -900 220 -900 {lab=iovdd}
N 300 -900 300 -680 {lab=iovdd}
N 220 -900 300 -900 {lab=iovdd}
N 620 -900 620 -840 {lab=iovdd}
N 360 -900 620 -900 {lab=iovdd}
C {devices/iopin.sym} 140 -900 0 1 {name=p1 lab=iovdd}
C {devices/iopin.sym} 140 -100 0 1 {name=p2 lab=iovss}
C {devices/iopin.sym} 140 -880 0 1 {name=p3 lab=vdd}
C {devices/iopin.sym} 140 -120 0 1 {name=p4 lab=vss}
C {devices/iopin.sym} 140 -700 0 1 {name=p5 lab=pad}
C {devices/opin.sym} 1380 -520 0 0 {name=p6 lab=outp}
C {devices/opin.sym} 1380 -480 0 0 {name=p7 lab=outn}
C {devices/ipin.sym} 140 -460 0 0 {name=p8 lab=vcm}
C {devices/ipin.sym} 140 -500 0 0 {name=p9 lab=vref}
C {devices/ipin.sym} 140 -320 0 0 {name=p10 lab=ibias}
C {devices/ipin.sym} 140 -260 0 0 {name=p11 lab=en_1v2}
C {devices/ipin.sym} 140 -240 0 0 {name=p12 lab=sel0_1v2}
C {devices/ipin.sym} 140 -220 0 0 {name=p13 lab=sel1_1v2}
C {devices/ipin.sym} 140 -200 0 0 {name=p14 lab=vdd1v2_sense}
C {devices/ipin.sym} 140 -180 0 0 {name=p15 lab=vdd3v3_sense}
C {en_ctrl_3v3.sym} 420 -220 0 0 {name=xc}
C {devices/lab_pin.sym} 360 -300 0 0 {name=l0 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 380 -300 0 1 {name=l1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1040 -100 0 1 {name=l2 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 320 -260 0 0 {name=l3 sig_type=std_logic lab=en_1v2}
C {devices/lab_pin.sym} 320 -240 0 0 {name=l4 sig_type=std_logic lab=sel0_1v2}
C {devices/lab_pin.sym} 320 -220 0 0 {name=l5 sig_type=std_logic lab=sel1_1v2}
C {devices/lab_pin.sym} 320 -200 0 0 {name=l6 sig_type=std_logic lab=vdd1v2_sense}
C {devices/lab_pin.sym} 320 -180 0 0 {name=l7 sig_type=std_logic lab=vdd3v3_sense}
C {devices/lab_wire.sym} 580 -240 0 0 {name=l9 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_wire.sym} 580 -220 0 0 {name=l10 sig_type=std_logic lab=sel1_3v3}
C {d2s_bias_sel_pd.sym} 730 -270 0 0 {name=xb}
C {devices/lab_pin.sym} 700 -360 0 0 {name=l11 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 680 -180 0 0 {name=l12 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 740 -360 0 1 {name=l13 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 720 -180 0 1 {name=l14 sig_type=std_logic lab=iovss}
C {s2d_core_ideal.sym} 1160 -480 0 0 {name=xa}
C {devices/lab_pin.sym} 1060 -600 0 0 {name=l25 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1040 -360 0 0 {name=l26 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 960 -540 0 0 {name=l27 sig_type=std_logic lab=padres}
C {devices/lab_pin.sym} 1340 -520 0 1 {name=l30 sig_type=std_logic lab=outp}
C {devices/lab_pin.sym} 1340 -480 0 1 {name=l31 sig_type=std_logic lab=outn}
C {devices/lab_pin.sym} 580 -420 0 0 {name=l38 sig_type=std_logic lab=en_3v3}
C {sg13cmos5l_Clamp_P20N0D.sym} 620 -780 0 0 {name=CP}
C {devices/lab_pin.sym} 620 -840 0 0 {name=l39 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 620 -720 0 0 {name=l40 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 560 -760 0 0 {name=l41 sig_type=std_logic lab=pad}
C {sg13cmos5l_Clamp_N20N0D.sym} 620 -630 0 0 {name=CN}
C {devices/lab_pin.sym} 620 -580 0 0 {name=l42 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 560 -660 0 0 {name=l43 sig_type=std_logic lab=pad}
C {sg13cmos5l_DCNDiode.sym} 300 -640 0 0 {name=DN}
C {devices/lab_pin.sym} 300 -580 0 0 {name=l44 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 260 -640 0 0 {name=l45 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 300 -680 0 0 {name=l46 sig_type=std_logic lab=iovdd}
C {sg13cmos5l_DCPDiode.sym} 220 -780 0 0 {name=DP}
C {devices/lab_pin.sym} 180 -780 0 0 {name=l47 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 220 -840 0 0 {name=l48 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 220 -740 0 0 {name=l49 sig_type=std_logic lab=iovss}
C {sg13cmos5l_SecondaryProtection.sym} 880 -700 0 0 {name=SP}
C {devices/lab_pin.sym} 940 -700 0 1 {name=l50 sig_type=std_logic lab=padres}
C {devices/lab_pin.sym} 880 -660 0 0 {name=l51 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 820 -700 0 0 {name=l52 sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 880 -740 0 0 {name=l53 sig_type=std_logic lab=iovdd}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
C {devices/lab_wire.sym} 580 -200 0 0 {name=l60 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1100 -320 0 1 {name=l54 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1220 -220 0 1 {name=l55 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 1120 -300 0 1 {name=l56 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 1200 -240 0 1 {name=l57 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 1140 -280 0 1 {name=l58 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 1180 -260 0 1 {name=l59 sig_type=std_logic lab=vabn}
