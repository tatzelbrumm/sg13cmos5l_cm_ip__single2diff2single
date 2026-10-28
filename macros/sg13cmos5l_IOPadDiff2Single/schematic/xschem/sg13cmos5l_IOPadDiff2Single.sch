v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sg13cmos5l_IOPadDiff2Single: differential in, single-ended out, class-AB, pad - vref = (vinp - vinn) / 2} 0 -830 0 0 0.5 0.5 {}
T {Custom padframe cell (case (a)): OP / ON are the pad's ESD clamp frames (d2s_out_p, d2s_out_n). Everything runs on the ring rails iovdd / iovss;} 0 -780 0 0 0.3 0.3 {}
T {the 1.2 V core ring vdd only feeds the level shifters' input inverters. vfb is tied to pad here (Kelvin tap at the pad).} 0 -750 0 0 0.3 0.3 {}
T {Slot fallback: iovdd = vdd_3v3, iovss = vss_3v3, vdd = vdd_1v2, vss = vss_1v2, pad = s7_an[1]. Netlist reference: ../../netlist/source/sg13cmos5l_IOPadDiff2Single.spice} 0 -720 0 0 0.3 0.3 {}
T {[C] enable / bias select: en_3v3 = en_1v2 AND vdd_1v2 present AND vdd_3v3 present} 150 -120 0 0 0.3 0.3 {}
T {[B] bias: sel 00 harness ibias (sourced, 5 uA), 01 Oguey-Aebischer, 10 bandgap, 11 both} 510 -160 0 0 0.3 0.3 {}
T {[D] class-AB driver with power-down} 760 -590 0 0 0.3 0.3 {}
T {[P] IHP primary diodes (as in sg13cmos5l_IOPadAnalog)} 1780 -740 0 0 0.3 0.3 {}
N 1020 -360 1020 -100 {lab=iovss}
N 800 -100 1020 -100 {lab=iovss}
N 800 -360 800 -100 {lab=iovss}
N 860 -360 860 -320 {lab=vbp}
N 880 -360 880 -300 {lab=vbpc}
N 700 -300 880 -300 {lab=vbpc}
N 900 -360 900 -280 {lab=vabp}
N 700 -280 900 -280 {lab=vabp}
N 940 -360 940 -260 {lab=vabn}
N 700 -260 940 -260 {lab=vabn}
N 960 -360 960 -240 {lab=vbnc}
N 700 -240 960 -240 {lab=vbnc}
N 980 -360 980 -220 {lab=vbn}
N 700 -220 980 -220 {lab=vbn}
N 240 -140 240 -100 {lab=iovss}
N 600 -100 800 -100 {lab=iovss}
N 420 -280 420 -260 {lab=en_3v3}
N 420 -520 420 -280 {lab=en_3v3}
N 400 -200 500 -200 {lab=sel1_3v3}
N 560 -180 560 -100 {lab=iovss}
N 560 -100 600 -100 {lab=iovss}
N 160 -260 200 -260 {lab=en_1v2}
N 160 -240 200 -240 {lab=sel0_1v2}
N 160 -220 200 -220 {lab=sel1_1v2}
N 160 -200 200 -200 {lab=vdd1v2_sense}
N 160 -180 200 -180 {lab=vdd3v3_sense}
N 160 -100 240 -100 {lab=iovss}
N 160 -420 740 -420 {lab=vref}
N 160 -460 740 -460 {lab=vinn}
N 160 -480 740 -480 {lab=vinp}
N 260 -580 260 -300 {lab=vdd}
N 160 -580 260 -580 {lab=vdd}
N 240 -600 240 -300 {lab=iovdd}
N 160 -600 240 -600 {lab=iovdd}
N 1040 -600 1040 -560 {lab=iovdd}
N 820 -600 1040 -600 {lab=iovdd}
N 820 -600 820 -560 {lab=iovdd}
N 620 -600 820 -600 {lab=iovdd}
N 580 -600 580 -360 {lab=iovdd}
N 440 -500 440 -260 {lab=en_3v3_b}
N 420 -520 740 -520 {lab=en_3v3}
N 400 -260 420 -260 {lab=en_3v3}
N 440 -500 740 -500 {lab=en_3v3_b}
N 400 -240 440 -240 {lab=en_3v3_b}
N 440 -260 440 -240 {lab=en_3v3_b}
N 240 -100 560 -100 {lab=iovss}
N 580 -600 620 -600 {lab=iovdd}
N 240 -600 580 -600 {lab=iovdd}
N 160 -320 520 -320 {lab=ibias}
N 420 -280 520 -280 {lab=en_3v3}
N 440 -260 520 -260 {lab=en_3v3_b}
N 500 -220 500 -200 {lab=sel1_3v3}
N 500 -220 520 -220 {lab=sel1_3v3}
N 480 -240 520 -240 {lab=sel0_3v3}
N 480 -240 480 -220 {lab=sel0_3v3}
N 400 -220 480 -220 {lab=sel0_3v3}
N 700 -320 860 -320 {lab=vbp}
C {devices/iopin.sym} 160 -600 0 1 {name=p1 lab=iovdd}
C {devices/iopin.sym} 160 -100 0 1 {name=p2 lab=iovss}
C {devices/iopin.sym} 160 -580 0 1 {name=p3 lab=vdd}
C {devices/iopin.sym} 160 -120 0 1 {name=p4 lab=vss}
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
C {bias_sel_pd.sym} 610 -270 0 0 {name=xb}
C {devices/lab_pin.sym} 580 -360 0 0 {name=l11 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 560 -180 0 0 {name=l12 sig_type=std_logic lab=iovss}
C {devices/lab_wire.sym} 400 -220 0 1 {name=l23 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_wire.sym} 400 -200 0 1 {name=l24 sig_type=std_logic lab=sel1_3v3}
C {d2s_mpdda_pd.sym} 920 -460 0 0 {name=xd}
C {devices/lab_pin.sym} 820 -560 0 0 {name=l25 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 800 -360 0 0 {name=l26 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1040 -560 0 1 {name=l27 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1020 -360 0 1 {name=l28 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 740 -480 0 0 {name=l29 sig_type=std_logic lab=vinp}
C {devices/lab_pin.sym} 740 -460 0 0 {name=l30 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 740 -420 0 0 {name=l31 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 420 -520 0 0 {name=l40 sig_type=std_logic lab=en_3v3}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
C {devices/lab_pin.sym} 440 -500 0 0 {name=l53 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 860 -320 0 1 {name=l47 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 980 -220 0 1 {name=l48 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 880 -300 0 1 {name=l49 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 960 -240 0 1 {name=l50 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 900 -280 0 1 {name=l51 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 940 -260 0 1 {name=l52 sig_type=std_logic lab=vabn}
C {devices/lab_wire.sym} 400 -260 0 1 {name=l3 sig_type=std_logic lab=en_3v3}
C {devices/lab_wire.sym} 400 -240 0 1 {name=l4 sig_type=std_logic lab=en_3v3_b}
C {d2s_out_p.sym} 1420 -640 0 0 {name=xfp}
C {d2s_out_n.sym} 1420 -300 0 0 {name=xfn}
N 1100 -520 1180 -520 {lab=dabp}
N 1180 -520 1180 -660 {lab=dabp}
N 1180 -660 1340 -660 {lab=dabp}
N 1100 -500 1200 -500 {lab=a}
N 1200 -500 1200 -640 {lab=a}
N 1200 -640 1240 -640 {lab=a}
N 1240 -640 1340 -640 {lab=a}
N 1240 -640 1240 -560 {lab=a}
N 1240 -560 1580 -560 {lab=a}
N 1100 -420 1200 -420 {lab=b}
N 1200 -420 1200 -300 {lab=b}
N 1200 -300 1240 -300 {lab=b}
N 1240 -300 1340 -300 {lab=b}
N 1240 -300 1240 -380 {lab=b}
N 1240 -380 1580 -380 {lab=b}
N 1100 -400 1180 -400 {lab=dabn}
N 1180 -400 1180 -280 {lab=dabn}
N 1180 -280 1340 -280 {lab=dabn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1600 -560 0 0 {name=CMA
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1620 -590 1620 -560 {lab=pad}
N 1620 -560 1620 -530 {lab=pad}
N 1620 -560 1680 -560 {lab=pad}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1600 -380 0 1 {name=CMB
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1580 -410 1580 -380 {lab=b}
N 1580 -380 1580 -350 {lab=b}
N 1620 -380 1680 -380 {lab=pad}
N 1500 -640 1680 -640 {lab=pad}
N 1500 -300 1680 -300 {lab=pad}
N 1100 -460 1680 -460 {lab=pad}
N 1420 -700 1420 -720 {lab=iovdd}
C {devices/lab_pin.sym} 1420 -720 0 0 {name=xlrp sig_type=std_logic lab=iovdd}
N 1420 -240 1420 -220 {lab=iovss}
C {devices/lab_pin.sym} 1420 -220 0 0 {name=xlrn sig_type=std_logic lab=iovss}
C {sg13cmos5l_DCPDiode.sym} 1840 -600 0 0 {name=DP}
N 1680 -600 1800 -600 {lab=pad}
N 1840 -660 1840 -680 {lab=iovdd}
C {devices/lab_pin.sym} 1840 -680 0 0 {name=l43 sig_type=std_logic lab=iovdd}
N 1840 -560 1840 -540 {lab=iovss}
C {devices/lab_pin.sym} 1840 -540 0 0 {name=l44 sig_type=std_logic lab=iovss}
C {sg13cmos5l_DCNDiode.sym} 1840 -340 0 0 {name=DN}
N 1680 -340 1800 -340 {lab=pad}
N 1840 -380 1840 -400 {lab=iovdd}
C {devices/lab_pin.sym} 1840 -400 0 0 {name=l45 sig_type=std_logic lab=iovdd}
N 1840 -280 1840 -260 {lab=iovss}
C {devices/lab_pin.sym} 1840 -260 0 0 {name=l46 sig_type=std_logic lab=iovss}
N 1680 -480 1980 -480 {lab=pad}
C {devices/iopin.sym} 1980 -480 0 0 {name=p5 lab=pad}
N 1680 -640 1680 -600 {lab=pad}
N 1680 -600 1680 -560 {lab=pad}
N 1680 -560 1680 -480 {lab=pad}
N 1680 -480 1680 -460 {lab=pad}
N 1680 -460 1680 -380 {lab=pad}
N 1680 -380 1680 -340 {lab=pad}
N 1680 -340 1680 -300 {lab=pad}
T {[O] output stage: d2s_out_p = the P clamp frame (OP, replica RP1, dummy), d2s_out_n = the two N clamp frames (ON, replica RN1),} 1240 -800 0 0 0.3 0.3 {}
T {    Miller capacitors CMA (a to pad) and CMB (pad to b), hv PMOS in accumulation, W 7.96u x L 32.16u as drawn between the diodes} 1240 -775 0 0 0.3 0.3 {}
