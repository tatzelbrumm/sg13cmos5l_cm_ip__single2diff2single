v {xschem version=3.4.8RC file_version=1.3}
G {}
V {}
E {}
S {}
C {ipin.sym} 60 180 0 0 {name=g0 lab=dig_in[23:0] }
C {ipin.sym} 60 100 0 0 {name=g1 lab=enable }
C {ipin.sym} 60 1120 0 0 {name=g2 lab=clk }
C {ipin.sym} 60 1140 0 0 {name=g3 lab=reset }
C {opin.sym} 1960 1120 0 0 {name=g4 lab=dig_out[11:0] }
C {iopin.sym} 60 1040 0 1 {name=g5 lab=vss_1v2 }
C {iopin.sym} 1960 680 0 0 {name=g6 lab=s7_an[0:1] }
C {iopin.sym} 1960 -260 0 0 {name=g7 lab=s7_an_0_esd }
C {iopin.sym} 60 -180 0 1 {name=g8 lab=vbias }
C {iopin.sym} 60 610 0 1 {name=g9 lab=ibias0 }
C {iopin.sym} 60 -70 0 1 {name=g10 lab=ibias1 }
C {iopin.sym} 60 1180 0 1 {name=g11 lab=analog_bus3 }
C {iopin.sym} 60 1200 0 1 {name=g12 lab=analog_bus2 }
C {iopin.sym} 60 1220 0 1 {name=g13 lab=analog_bus1 }
C {iopin.sym} 60 1240 0 1 {name=g14 lab=analog_bus0 }
C {iopin.sym} 60 -260 0 1 {name=g15 lab=vdd_1v2 }
C {iopin.sym} 60 1000 0 1 {name=g16 lab=vss_3v3 }
C {iopin.sym} 60 -300 0 1 {name=g17 lab=vdd_3v3 }
T {slot (slot7_wrapper-compatible), SLOT FALLBACK of the pad cells: both pad macros sit inside the slot and use the harness IOPadAnalog pads.} 60 -640 0 0 0.4 0.4 {}
T {Rails: iovdd = vdd_3v3, iovss = vss_3v3, core ring vdd = vdd_1v2, vss = vss_1v2. D2S drives s7_an[1] (the bare pad node); S2D reads s7_an_0_esd (behind the harness 587 Ohm secondary protection).} 60 -580 0 0 0.25 0.25 {}
T {Chain S2D -> D2S (internal filter off). vref = vcm = vbias (harness voltage bias). ibias0 -> D2S, ibias1 -> S2D (both sourced, 5 uA = code 20). Bias select: dig_in[1:0] -> D2S, dig_in[3:2] -> S2D. enable -> both.} 60 -555 0 0 0.25 0.25 {}
T {Priority route (custom padframe cells) needs slot7_wrapper / padframe changes; see macros/slot/README.md. Unused here: clk, reset, dig_out, analog_bus[3:0], dig_in[23:4].} 60 -530 0 0 0.25 0.25 {}
T {One generator per pad: each pad has its own en_ctrl_3v3 (level shift of enable and the two select bits) and its own bias_gen_pd (Oguey-Aebischer core,} 60 -495 0 0 0.25 0.25 {}
T {bandgap core or the harness ibias through a switch, chosen by the select bits); the generator's iref is the pad's 5 uA reference current.} 60 -473 0 0 0.25 0.25 {}
P 10 5 210 -340 1770 -340 1770 280 210 280 210 -340 {dash=6}
T {[S2D] single-to-differential pad xs2d with its own enable control xs2d_c and bias generator xs2d_g} 215 -375 0 0 0.35 0.35 {layer=10}
T {xs2d_c (en_ctrl_3v3) and xs2d_g (bias_gen_pd): outside the pad cell since 2026-11-04 (backannotation to the drawn cell),} 225 -325 0 0 0.25 0.25 {}
T {wired as in the former pad sheet; the sources that drove the old pad pins now drive them.} 225 -303 0 0 0.25 0.25 {}
P 10 5 210 420 1770 420 1770 960 210 960 210 420 {dash=6}
T {[D2S] differential-to-single pad xd2s with its own enable control xd2s_c and bias generator xd2s_g} 215 385 0 0 0.35 0.35 {layer=10}
T {xd2s_c (en_ctrl_3v3) and xd2s_g (bias_gen_pd): outside the pad cell since 2026-11-03 (backannotation to the drawn cell),} 225 435 0 0 0.25 0.25 {}
T {wired as in the former pad sheet; the sources that drove the old pad pins now drive them.} 225 457 0 0 0.25 0.25 {}
T {not connected here} -120 1095 0 0 0.25 0.25 {}
T {not connected here} 1950 1095 0 0 0.25 0.25 {}
C {sg13cmos5l_IOPadSingle2Diff.sym} 1460 0 0 0 {name=xs2d}
C {sg13cmos5l_IOPadDiff2Single.sym} 1460 680 0 0 {name=xd2s}
C {en_ctrl_3v3.sym} 420 820 0 0 {name=xd2s_c}
C {bias_gen_pd.sym} 940 640 0 0 {name=xd2s_g}
C {en_ctrl_3v3.sym} 420 140 0 0 {name=xs2d_c}
C {bias_gen_pd.sym} 940 -40 0 0 {name=xs2d_g}
N 60 100 180 100 {lab=enable}
N 180 100 320 100 {lab=enable}
N 180 100 180 780 {lab=enable}
N 180 780 320 780 {lab=enable}
N 360 60 360 40 {lab=vdd_3v3}
N 380 60 380 40 {lab=vdd_1v2}
N 360 220 360 240 {lab=vss_3v3}
N 320 120 300 120 {lab=dig_in[2]}
N 320 140 300 140 {lab=dig_in[3]}
N 320 160 300 160 {lab=vdd_1v2}
N 320 180 300 180 {lab=vdd_3v3}
N 520 100 560 100 {lab=s2d_en_3v3}
N 560 100 1060 100 {lab=s2d_en_3v3}
N 1060 100 1060 0 {lab=s2d_en_3v3}
N 1060 0 1240 0 {lab=s2d_en_3v3}
N 560 100 560 -50 {lab=s2d_en_3v3}
N 560 -50 850 -50 {lab=s2d_en_3v3}
N 520 120 1190 120 {lab=s2d_en_3v3_b}
N 1190 120 1190 20 {lab=s2d_en_3v3_b}
N 1190 20 1240 20 {lab=s2d_en_3v3_b}
N 520 140 680 140 {lab=s2d_sel0_3v3}
N 680 140 680 -30 {lab=s2d_sel0_3v3}
N 680 -30 850 -30 {lab=s2d_sel0_3v3}
N 520 160 800 160 {lab=s2d_sel1_3v3}
N 800 160 800 -10 {lab=s2d_sel1_3v3}
N 800 -10 850 -10 {lab=s2d_sel1_3v3}
N 940 -120 940 -140 {lab=vdd_3v3}
N 940 40 940 60 {lab=vss_3v3}
N 60 -70 850 -70 {lab=ibias1}
N 1030 -40 1240 -40 {lab=s2d_iref}
N 1420 -180 1420 -220 {lab=vdd_3v3}
N 1500 -180 1500 -220 {lab=vdd_1v2}
N 1420 180 1420 200 {lab=vss_3v3}
N 1500 180 1500 200 {lab=vss_1v2}
N 1240 -80 1220 -80 {lab=vbias}
N 360 740 360 720 {lab=vdd_3v3}
N 380 740 380 720 {lab=vdd_1v2}
N 360 900 360 920 {lab=vss_3v3}
N 320 800 300 800 {lab=dig_in[0]}
N 320 820 300 820 {lab=dig_in[1]}
N 320 840 300 840 {lab=vdd_1v2}
N 320 860 300 860 {lab=vdd_3v3}
N 520 780 560 780 {lab=d2s_en_3v3}
N 560 780 1060 780 {lab=d2s_en_3v3}
N 1060 780 1060 680 {lab=d2s_en_3v3}
N 1060 680 1240 680 {lab=d2s_en_3v3}
N 560 780 560 630 {lab=d2s_en_3v3}
N 560 630 850 630 {lab=d2s_en_3v3}
N 520 800 1190 800 {lab=d2s_en_3v3_b}
N 1190 800 1190 700 {lab=d2s_en_3v3_b}
N 1190 700 1240 700 {lab=d2s_en_3v3_b}
N 520 820 680 820 {lab=d2s_sel0_3v3}
N 680 820 680 650 {lab=d2s_sel0_3v3}
N 680 650 850 650 {lab=d2s_sel0_3v3}
N 520 840 800 840 {lab=d2s_sel1_3v3}
N 800 840 800 670 {lab=d2s_sel1_3v3}
N 800 670 850 670 {lab=d2s_sel1_3v3}
N 940 560 940 540 {lab=vdd_3v3}
N 940 720 940 740 {lab=vss_3v3}
N 60 610 850 610 {lab=ibias0}
N 1030 640 1240 640 {lab=d2s_iref}
N 1420 500 1420 460 {lab=vdd_3v3}
N 1500 500 1500 460 {lab=vdd_1v2}
N 1420 860 1420 880 {lab=vss_3v3}
N 1500 860 1500 880 {lab=vss_1v2}
N 1240 600 1220 600 {lab=vbias}
N 1960 -260 1200 -260 {lab=s7_an_0_esd}
N 1200 -260 1200 -120 {lab=s7_an_0_esd}
N 1200 -120 1240 -120 {lab=s7_an_0_esd}
N 1680 40 1700 40 {lab=vbias}
N 1680 0 1800 0 {lab=vdiffn}
N 1800 0 1800 320 {lab=vdiffn}
N 1800 320 1110 320 {lab=vdiffn}
N 1110 320 1110 580 {lab=vdiffn}
N 1110 580 1240 580 {lab=vdiffn}
N 1680 -40 1840 -40 {lab=vdiffp}
N 1840 -40 1840 360 {lab=vdiffp}
N 1840 360 1150 360 {lab=vdiffp}
N 1150 360 1150 560 {lab=vdiffp}
N 1150 560 1240 560 {lab=vdiffp}
N 1680 680 1700 680 {lab=s7_an[1]}
C {devices/lab_pin.sym} 360 40 0 0 {name=l_xs2d_c_vddh sig_type=std_logic lab=vdd_3v3}
C {devices/lab_pin.sym} 380 40 0 1 {name=l_xs2d_c_vddl sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 360 240 0 1 {name=l_xs2d_c_vss sig_type=std_logic lab=vss_3v3}
C {devices/lab_pin.sym} 300 120 0 0 {name=l_xs2d_c_sel0_1v2 sig_type=std_logic lab=dig_in[2]}
C {devices/lab_pin.sym} 300 140 0 0 {name=l_xs2d_c_sel1_1v2 sig_type=std_logic lab=dig_in[3]}
C {devices/lab_pin.sym} 300 160 0 0 {name=l_xs2d_c_vdd1v2_sense sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 300 180 0 0 {name=l_xs2d_c_vdd3v3_sense sig_type=std_logic lab=vdd_3v3}
C {devices/lab_wire.sym} 560 80 0 1 {name=lw_s2d_en_3v3 sig_type=std_logic lab=s2d_en_3v3}
C {devices/lab_wire.sym} 680 80 0 1 {name=lw_s2d_sel0_3v3 sig_type=std_logic lab=s2d_sel0_3v3}
C {devices/lab_wire.sym} 800 80 0 1 {name=lw_s2d_sel1_3v3 sig_type=std_logic lab=s2d_sel1_3v3}
C {devices/lab_wire.sym} 1185 120 0 0 {name=lw_s2d_en_3v3_b sig_type=std_logic lab=s2d_en_3v3_b}
C {devices/lab_pin.sym} 940 -140 0 1 {name=l_xs2d_g_vdd sig_type=std_logic lab=vdd_3v3}
C {devices/lab_pin.sym} 940 60 0 1 {name=l_xs2d_g_vss sig_type=std_logic lab=vss_3v3}
C {devices/lab_wire.sym} 1230 -40 0 0 {name=lw_s2d_iref sig_type=std_logic lab=s2d_iref}
C {devices/lab_pin.sym} 1420 -220 0 0 {name=l_xs2d_iovdd sig_type=std_logic lab=vdd_3v3}
C {devices/lab_pin.sym} 1500 -220 0 1 {name=l_xs2d_vdd sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 1420 200 0 0 {name=l_xs2d_iovss sig_type=std_logic lab=vss_3v3}
C {devices/lab_pin.sym} 1500 200 0 1 {name=l_xs2d_vss sig_type=std_logic lab=vss_1v2}
C {devices/lab_pin.sym} 1220 -80 0 0 {name=l_xs2d_vref sig_type=std_logic lab=vbias}
C {devices/lab_pin.sym} 360 720 0 0 {name=l_xd2s_c_vddh sig_type=std_logic lab=vdd_3v3}
C {devices/lab_pin.sym} 380 720 0 1 {name=l_xd2s_c_vddl sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 360 920 0 1 {name=l_xd2s_c_vss sig_type=std_logic lab=vss_3v3}
C {devices/lab_pin.sym} 300 800 0 0 {name=l_xd2s_c_sel0_1v2 sig_type=std_logic lab=dig_in[0]}
C {devices/lab_pin.sym} 300 820 0 0 {name=l_xd2s_c_sel1_1v2 sig_type=std_logic lab=dig_in[1]}
C {devices/lab_pin.sym} 300 840 0 0 {name=l_xd2s_c_vdd1v2_sense sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 300 860 0 0 {name=l_xd2s_c_vdd3v3_sense sig_type=std_logic lab=vdd_3v3}
C {devices/lab_wire.sym} 560 760 0 1 {name=lw_d2s_en_3v3 sig_type=std_logic lab=d2s_en_3v3}
C {devices/lab_wire.sym} 680 760 0 1 {name=lw_d2s_sel0_3v3 sig_type=std_logic lab=d2s_sel0_3v3}
C {devices/lab_wire.sym} 800 760 0 1 {name=lw_d2s_sel1_3v3 sig_type=std_logic lab=d2s_sel1_3v3}
C {devices/lab_wire.sym} 1185 800 0 0 {name=lw_d2s_en_3v3_b sig_type=std_logic lab=d2s_en_3v3_b}
C {devices/lab_pin.sym} 940 540 0 1 {name=l_xd2s_g_vdd sig_type=std_logic lab=vdd_3v3}
C {devices/lab_pin.sym} 940 740 0 1 {name=l_xd2s_g_vss sig_type=std_logic lab=vss_3v3}
C {devices/lab_wire.sym} 1230 640 0 0 {name=lw_d2s_iref sig_type=std_logic lab=d2s_iref}
C {devices/lab_pin.sym} 1420 460 0 0 {name=l_xd2s_iovdd sig_type=std_logic lab=vdd_3v3}
C {devices/lab_pin.sym} 1500 460 0 1 {name=l_xd2s_vdd sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 1420 880 0 0 {name=l_xd2s_iovss sig_type=std_logic lab=vss_3v3}
C {devices/lab_pin.sym} 1500 880 0 1 {name=l_xd2s_vss sig_type=std_logic lab=vss_1v2}
C {devices/lab_pin.sym} 1220 600 0 0 {name=l_xd2s_vref sig_type=std_logic lab=vbias}
C {devices/lab_pin.sym} 1700 40 0 1 {name=l_xs2d_vcm sig_type=std_logic lab=vbias}
C {devices/lab_wire.sym} 1500 360 0 1 {name=l5 sig_type=std_logic lab=vdiffp}
C {devices/lab_wire.sym} 1500 320 0 1 {name=l6 sig_type=std_logic lab=vdiffn}
C {devices/lab_pin.sym} 1700 680 0 1 {name=l19 sig_type=std_logic lab=s7_an[1]}
