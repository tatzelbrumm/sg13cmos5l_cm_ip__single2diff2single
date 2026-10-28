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
T {[D] class-AB driver with power-down} 1120 -590 0 0 0.3 0.3 {}
T {[P] IHP primary diodes (as in sg13cmos5l_IOPadAnalog)} 2140 -740 0 0 0.3 0.3 {}
T {[O] output stage: d2s_out_p = the P clamp frame (OP, replica RP1, dummy), d2s_out_n = the two N clamp frames (ON, replica RN1),} 1600 -800 0 0 0.3 0.3 {}
T {    Miller capacitors CMA (a to pad) and CMB (pad to b), hv PMOS in accumulation, W 7.96u x L 32.16u as drawn between the diodes} 1600 -775 0 0 0.3 0.3 {}
N 1380 -360 1380 -100 {lab=iovss}
N 1160 -100 1380 -100 {lab=iovss}
N 1160 -360 1160 -100 {lab=iovss}
N 1220 -360 1220 -320 {lab=vbp}
N 1240 -360 1240 -300 {lab=vbpc}
N 1060 -300 1240 -300 {lab=vbpc}
N 1260 -360 1260 -280 {lab=vabp}
N 1060 -280 1260 -280 {lab=vabp}
N 1300 -360 1300 -260 {lab=vabn}
N 1060 -260 1300 -260 {lab=vabn}
N 1320 -360 1320 -240 {lab=vbnc}
N 1060 -240 1320 -240 {lab=vbnc}
N 1340 -360 1340 -220 {lab=vbn}
N 1060 -220 1340 -220 {lab=vbn}
N 240 -140 240 -100 {lab=iovss}
N 420 -280 420 -260 {lab=en_3v3}
N 420 -520 420 -280 {lab=en_3v3}
N 400 -200 500 -200 {lab=sel1_3v3}
N 920 -100 1160 -100 {lab=iovss}
N 160 -260 200 -260 {lab=en_1v2}
N 160 -240 200 -240 {lab=sel0_1v2}
N 160 -220 200 -220 {lab=sel1_1v2}
N 160 -200 200 -200 {lab=vdd1v2_sense}
N 160 -180 200 -180 {lab=vdd3v3_sense}
N 160 -100 240 -100 {lab=iovss}
N 160 -420 1100 -420 {lab=vref}
N 160 -460 1100 -460 {lab=vinn}
N 160 -480 1100 -480 {lab=vinp}
N 260 -580 260 -300 {lab=vdd}
N 160 -580 260 -580 {lab=vdd}
N 240 -600 240 -300 {lab=iovdd}
N 160 -600 240 -600 {lab=iovdd}
N 1400 -600 1400 -560 {lab=iovdd}
N 1180 -600 1400 -600 {lab=iovdd}
N 1180 -600 1180 -560 {lab=iovdd}
N 440 -500 440 -260 {lab=en_3v3_b}
N 420 -520 1100 -520 {lab=en_3v3}
N 400 -260 420 -260 {lab=en_3v3}
N 440 -500 1100 -500 {lab=en_3v3_b}
N 400 -240 440 -240 {lab=en_3v3_b}
N 440 -260 440 -240 {lab=en_3v3_b}
N 240 -100 920 -100 {lab=iovss}
N 940 -600 1180 -600 {lab=iovdd}
N 240 -600 940 -600 {lab=iovdd}
N 400 -220 480 -220 {lab=sel0_3v3}
N 1060 -320 1220 -320 {lab=vbp}
N 1460 -520 1540 -520 {lab=#net1}
N 1540 -660 1540 -520 {lab=#net1}
N 1540 -660 1700 -660 {lab=#net1}
N 1460 -500 1560 -500 {lab=#net2}
N 1560 -640 1560 -500 {lab=#net2}
N 1560 -640 1600 -640 {lab=#net2}
N 1600 -640 1700 -640 {lab=#net2}
N 1600 -640 1600 -560 {lab=#net2}
N 1600 -560 1940 -560 {lab=#net2}
N 1460 -420 1560 -420 {lab=#net3}
N 1560 -420 1560 -300 {lab=#net3}
N 1560 -300 1600 -300 {lab=#net3}
N 1600 -300 1700 -300 {lab=#net3}
N 1600 -380 1600 -300 {lab=#net3}
N 1600 -380 1940 -380 {lab=#net3}
N 1460 -400 1540 -400 {lab=#net4}
N 1540 -400 1540 -280 {lab=#net4}
N 1540 -280 1700 -280 {lab=#net4}
N 1980 -590 1980 -560 {lab=pad}
N 1980 -560 1980 -530 {lab=pad}
N 1980 -560 2040 -560 {lab=pad}
N 1940 -410 1940 -380 {lab=#net3}
N 1940 -380 1940 -350 {lab=#net3}
N 1980 -380 2040 -380 {lab=pad}
N 1860 -640 2040 -640 {lab=pad}
N 1860 -300 2040 -300 {lab=pad}
N 1460 -460 2040 -460 {lab=pad}
N 1780 -720 1780 -700 {lab=iovdd}
N 1780 -240 1780 -220 {lab=iovss}
N 2040 -600 2160 -600 {lab=pad}
N 2200 -680 2200 -660 {lab=iovdd}
N 2200 -560 2200 -540 {lab=iovss}
N 2040 -340 2160 -340 {lab=pad}
N 2200 -400 2200 -380 {lab=iovdd}
N 2200 -280 2200 -260 {lab=iovss}
N 2040 -480 2340 -480 {lab=pad}
N 2040 -640 2040 -600 {lab=pad}
N 2040 -600 2040 -560 {lab=pad}
N 2040 -560 2040 -480 {lab=pad}
N 2040 -480 2040 -460 {lab=pad}
N 2040 -460 2040 -380 {lab=pad}
N 2040 -380 2040 -340 {lab=pad}
N 2040 -340 2040 -300 {lab=pad}
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
C {devices/lab_wire.sym} 400 -220 0 1 {name=l23 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_wire.sym} 400 -200 0 1 {name=l24 sig_type=std_logic lab=sel1_3v3}
C {d2s_mpdda_pd.sym} 1280 -460 0 0 {name=xd}
C {devices/lab_pin.sym} 1180 -560 0 0 {name=l25 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1160 -360 0 0 {name=l26 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1400 -560 0 1 {name=l27 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1380 -360 0 1 {name=l28 sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 1100 -480 0 0 {name=l29 sig_type=std_logic lab=vinp}
C {devices/lab_pin.sym} 1100 -460 0 0 {name=l30 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 1100 -420 0 0 {name=l31 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 420 -520 0 0 {name=l40 sig_type=std_logic lab=en_3v3}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
C {devices/lab_pin.sym} 440 -500 0 0 {name=l53 sig_type=std_logic lab=en_3v3_b}
C {devices/lab_pin.sym} 1220 -320 0 1 {name=l47 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1340 -220 0 1 {name=l48 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 1240 -300 0 1 {name=l49 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 1320 -240 0 1 {name=l50 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 1260 -280 0 1 {name=l51 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 1300 -260 0 1 {name=l52 sig_type=std_logic lab=vabn}
C {devices/lab_wire.sym} 400 -260 0 1 {name=l3 sig_type=std_logic lab=en_3v3}
C {devices/lab_wire.sym} 400 -240 0 1 {name=l4 sig_type=std_logic lab=en_3v3_b}
C {d2s_out_p.sym} 1780 -640 0 0 {name=xfp}
C {d2s_out_n.sym} 1780 -300 0 0 {name=xfn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1960 -560 0 0 {name=CMA
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1960 -380 0 1 {name=CMB
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 1780 -720 0 0 {name=xlrp sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 1780 -220 0 0 {name=xlrn sig_type=std_logic lab=iovss}
C {sg13cmos5l_DCPDiode.sym} 2200 -600 0 0 {name=DP}
C {devices/lab_pin.sym} 2200 -680 0 0 {name=l43 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 2200 -540 0 0 {name=l44 sig_type=std_logic lab=iovss}
C {sg13cmos5l_DCNDiode.sym} 2200 -340 0 0 {name=DN}
C {devices/lab_pin.sym} 2200 -400 0 0 {name=l45 sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 2200 -260 0 0 {name=l46 sig_type=std_logic lab=iovss}
C {devices/iopin.sym} 2340 -480 0 0 {name=p5 lab=pad}
C {bias_gen_pd.sym} 620 -290 0 0 {name=xg}
C {bias_tree_pd.sym} 960 -270 0 0 {name=xt}
N 160 -320 530 -320 {lab=ibias}
N 420 -300 530 -300 {lab=en_3v3}
N 480 -280 480 -220 {lab=sel0_3v3}
N 480 -280 530 -280 {lab=sel0_3v3}
N 500 -260 500 -200 {lab=sel1_3v3}
N 500 -260 530 -260 {lab=sel1_3v3}
N 710 -290 730 -290 {lab=iref}
N 730 -320 730 -290 {lab=iref}
N 730 -320 860 -320 {lab=iref}
C {devices/lab_wire.sym} 730 -320 0 1 {name=l_iref sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 860 -300 0 0 {name=l_xt_en sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 860 -280 0 0 {name=l_xt_enb sig_type=std_logic lab=en_3v3_b}
N 920 -600 920 -360 {lab=iovdd}
N 900 -180 900 -100 {lab=iovss}
C {devices/lab_pin.sym} 620 -370 0 1 {name=l_xg_vdd sig_type=std_logic lab=iovdd}
C {devices/lab_pin.sym} 620 -210 0 1 {name=l_xg_vss sig_type=std_logic lab=iovss}
