v {xschem version=3.4.8RC file_version=1.3}
G {}
V {}
E {}
S {}
C {ipin.sym} -120 0 0 0 {name=g0 lab=dig_in[23:0] }
C {ipin.sym} -120 20 0 0 {name=g1 lab=enable }
C {ipin.sym} -120 40 0 0 {name=g2 lab=clk }
C {ipin.sym} -120 60 0 0 {name=g3 lab=reset }
C {opin.sym} 120 0 0 0 {name=g4 lab=dig_out[11:0] }
C {iopin.sym} 120 20 0 0 {name=g5 lab=vss_1v2 }
C {iopin.sym} 120 40 0 0 {name=g6 lab=s7_an[0:1] }
C {iopin.sym} 120 60 0 0 {name=g7 lab=s7_an_0_esd }
C {iopin.sym} 120 80 0 0 {name=g8 lab=vbias }
C {iopin.sym} 120 100 0 0 {name=g9 lab=ibias0 }
C {iopin.sym} 120 120 0 0 {name=g10 lab=ibias1 }
C {iopin.sym} 120 140 0 0 {name=g11 lab=analog_bus3 }
C {iopin.sym} 120 160 0 0 {name=g12 lab=analog_bus2 }
C {iopin.sym} 120 180 0 0 {name=g13 lab=analog_bus1 }
C {iopin.sym} 120 200 0 0 {name=g14 lab=analog_bus0 }
C {iopin.sym} 120 220 0 0 {name=g15 lab=vdd_1v2 }
C {iopin.sym} 120 240 0 0 {name=g16 lab=vss_3v3 }
C {iopin.sym} 120 260 0 0 {name=g17 lab=vdd_3v3 }
T {slot (slot7_wrapper-compatible), SLOT FALLBACK of the pad cells: both pad macros sit inside the slot and use the harness IOPadAnalog pads.} -120 -400 0 0 0.4 0.4 {}
T {Rails: iovdd = vdd_3v3, iovss = vss_3v3, core ring vdd = vdd_1v2, vss = vss_1v2. D2S drives s7_an[1] (the bare pad node); S2D reads s7_an_0_esd (behind the harness 587 Ohm secondary protection).} -120 -350 0 0 0.25 0.25 {}
T {Chain S2D -> D2S (internal filter off). vref = vcm = vbias (harness voltage bias). ibias0 -> D2S, ibias1 -> S2D (both sourced, 5 uA = code 20). Bias select: dig_in[1:0] -> D2S, dig_in[3:2] -> S2D. enable -> both.} -120 -320 0 0 0.25 0.25 {}
T {Priority route (custom padframe cells) needs slot7_wrapper / padframe changes; see macros/slot/README.md. Unused here: clk, reset, dig_out, analog_bus[3:0], dig_in[23:4].} -120 -290 0 0 0.25 0.25 {}
C {sg13cmos5l_IOPadSingle2Diff.sym} 700 0 0 0 {name=xs2d}
C {devices/lab_pin.sym} 660 -180 0 1 {name=l0 sig_type=std_logic lab=vdd_3v3}
C {devices/lab_pin.sym} 660 180 0 1 {name=l1 sig_type=std_logic lab=vss_3v3}
C {devices/lab_pin.sym} 740 -180 0 1 {name=l2 sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 740 180 0 1 {name=l3 sig_type=std_logic lab=vss_1v2}
C {devices/lab_pin.sym} 480 -120 0 0 {name=l4 sig_type=std_logic lab=s7_an_0_esd}
C {devices/lab_pin.sym} 920 -40 0 1 {name=l5 sig_type=std_logic lab=vdiffp}
C {devices/lab_pin.sym} 920 0 0 1 {name=l6 sig_type=std_logic lab=vdiffn}
C {devices/lab_pin.sym} 920 40 0 1 {name=l7 sig_type=std_logic lab=vbias}
C {devices/lab_pin.sym} 480 -80 0 0 {name=l8 sig_type=std_logic lab=vbias}
C {devices/lab_pin.sym} 480 -40 0 0 {name=l9 sig_type=std_logic lab=ibias1}
C {devices/lab_pin.sym} 480 0 0 0 {name=l10 sig_type=std_logic lab=enable}
C {devices/lab_pin.sym} 480 20 0 0 {name=l11 sig_type=std_logic lab=dig_in[2]}
C {devices/lab_pin.sym} 480 40 0 0 {name=l12 sig_type=std_logic lab=dig_in[3]}
C {devices/lab_pin.sym} 480 80 0 0 {name=l13 sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 480 100 0 0 {name=l14 sig_type=std_logic lab=vdd_3v3}
C {sg13cmos5l_IOPadDiff2Single.sym} 1400 0 0 0 {name=xd2s}
C {devices/lab_pin.sym} 1360 -180 0 1 {name=l15 sig_type=std_logic lab=vdd_3v3}
C {devices/lab_pin.sym} 1360 180 0 1 {name=l16 sig_type=std_logic lab=vss_3v3}
C {devices/lab_pin.sym} 1440 -180 0 1 {name=l17 sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 1440 180 0 1 {name=l18 sig_type=std_logic lab=vss_1v2}
C {devices/lab_pin.sym} 1620 0 0 1 {name=l19 sig_type=std_logic lab=s7_an[1]}
C {devices/lab_pin.sym} 1180 -120 0 0 {name=l20 sig_type=std_logic lab=vdiffp}
C {devices/lab_pin.sym} 1180 -100 0 0 {name=l21 sig_type=std_logic lab=vdiffn}
C {devices/lab_pin.sym} 1180 -80 0 0 {name=l22 sig_type=std_logic lab=vbias}
C {devices/lab_pin.sym} 1180 -40 0 0 {name=l23 sig_type=std_logic lab=ibias0}
C {devices/lab_pin.sym} 1180 0 0 0 {name=l24 sig_type=std_logic lab=enable}
C {devices/lab_pin.sym} 1180 20 0 0 {name=l25 sig_type=std_logic lab=dig_in[0]}
C {devices/lab_pin.sym} 1180 40 0 0 {name=l26 sig_type=std_logic lab=dig_in[1]}
C {devices/lab_pin.sym} 1180 80 0 0 {name=l27 sig_type=std_logic lab=vdd_1v2}
C {devices/lab_pin.sym} 1180 100 0 0 {name=l28 sig_type=std_logic lab=vdd_3v3}
