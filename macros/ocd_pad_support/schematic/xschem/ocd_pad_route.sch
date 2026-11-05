v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} 40 160 0 0 {name=p42 lab=ibias0}
C {devices/ipin.sym} 40 200 0 0 {name=p43 lab=ibias1}
C {devices/ipin.sym} 40 240 0 0 {name=p44 lab=vbias}
C {devices/ipin.sym} 40 280 0 0 {name=p45 lab=enable}
C {devices/ipin.sym} 40 320 0 0 {name=p46 lab=dig_in[0]}
C {devices/ipin.sym} 40 360 0 0 {name=p47 lab=dig_in[1]}
C {devices/ipin.sym} 40 400 0 0 {name=p48 lab=dig_in[2]}
C {devices/ipin.sym} 40 440 0 0 {name=p49 lab=dig_in[3]}
C {devices/iopin.sym} 40 0 0 0 {name=p50 lab=vdd_3v3}
C {devices/iopin.sym} 40 30 0 0 {name=p51 lab=vdd_1v2}
C {devices/iopin.sym} 40 560 0 0 {name=p52 lab=vss_3v3}
C {devices/iopin.sym} 40 590 0 0 {name=p53 lab=vss_1v2}
C {devices/iopin.sym} 600 180 0 1 {name=p54 lab=s7_an[0]}
C {devices/iopin.sym} 2000 300 0 0 {name=p55 lab=s7_an[1]}
N 40 160 130 160 {}
N 40 200 130 200 {}
N 40 240 130 240 {}
N 40 280 130 280 {}
N 40 320 130 320 {}
N 40 360 130 360 {}
N 40 400 130 400 {}
N 40 440 130 440 {}
C {ocd_pad_support.sym} 300 300 0 0 {name=xsup}
N 260 110 260 80 {}
C {devices/lab_pin.sym} 260 80 0 0 {name=l56 sig_type=std_logic lab=vdd_3v3}
N 340 110 340 80 {}
C {devices/lab_pin.sym} 340 80 0 1 {name=l57 sig_type=std_logic lab=vdd_1v2}
N 260 490 260 520 {}
C {devices/lab_pin.sym} 260 520 0 0 {name=l58 sig_type=std_logic lab=vss_3v3}
N 340 490 340 520 {}
C {devices/lab_pin.sym} 340 520 0 1 {name=l59 sig_type=std_logic lab=vss_1v2}
N 470 200 500 200 {}
C {devices/lab_pin.sym} 500 200 0 1 {name=l60 sig_type=std_logic lab=iref_s2d}
N 470 240 500 240 {}
C {devices/lab_pin.sym} 500 240 0 1 {name=l61 sig_type=std_logic lab=iref_d2s}
N 470 280 500 280 {}
C {devices/lab_pin.sym} 500 280 0 1 {name=l62 sig_type=std_logic lab=vref}
N 470 320 500 320 {}
C {devices/lab_pin.sym} 500 320 0 1 {name=l63 sig_type=std_logic lab=vcm}
N 470 360 500 360 {}
C {devices/lab_pin.sym} 500 360 0 1 {name=l64 sig_type=std_logic lab=en_3v3}
N 470 400 500 400 {}
C {devices/lab_pin.sym} 500 400 0 1 {name=l65 sig_type=std_logic lab=en_3v3_b}
C {sg13cmos5l_IOPadSingle2Diff.sym} 950 300 0 0 {name=xs2d}
N 600 180 730 180 {lab=s7_an[0]}
N 730 220 700 220 {}
C {devices/lab_pin.sym} 700 220 0 0 {name=l66 sig_type=std_logic lab=vref}
N 730 260 700 260 {}
C {devices/lab_pin.sym} 700 260 0 0 {name=l67 sig_type=std_logic lab=iref_s2d}
N 730 300 700 300 {}
C {devices/lab_pin.sym} 700 300 0 0 {name=l68 sig_type=std_logic lab=en_3v3}
N 730 320 700 320 {}
C {devices/lab_pin.sym} 700 320 0 0 {name=l69 sig_type=std_logic lab=en_3v3_b}
N 910 120 910 90 {}
C {devices/lab_pin.sym} 910 90 0 0 {name=l70 sig_type=std_logic lab=vdd_3v3}
N 990 120 990 90 {}
C {devices/lab_pin.sym} 990 90 0 1 {name=l71 sig_type=std_logic lab=vdd_1v2}
N 910 480 910 510 {}
C {devices/lab_pin.sym} 910 510 0 0 {name=l72 sig_type=std_logic lab=vss_3v3}
N 990 480 990 510 {}
C {devices/lab_pin.sym} 990 510 0 1 {name=l73 sig_type=std_logic lab=vss_1v2}
N 1170 340 1200 340 {}
C {devices/lab_pin.sym} 1200 340 0 1 {name=l74 sig_type=std_logic lab=vcm}
C {sg13cmos5l_IOPadDiff2Single.sym} 1650 300 0 0 {name=xd2s}
N 1170 260 1250 260 {}
N 1250 260 1250 180 {}
N 1250 180 1430 180 {lab=vdiffp}
N 1170 300 1280 300 {}
N 1280 300 1280 200 {}
N 1280 200 1430 200 {lab=vdiffn}
N 1430 220 1400 220 {}
C {devices/lab_pin.sym} 1400 220 0 0 {name=l75 sig_type=std_logic lab=vref}
N 1430 260 1400 260 {}
C {devices/lab_pin.sym} 1400 260 0 0 {name=l76 sig_type=std_logic lab=iref_d2s}
N 1430 300 1400 300 {}
C {devices/lab_pin.sym} 1400 300 0 0 {name=l77 sig_type=std_logic lab=en_3v3}
N 1430 320 1400 320 {}
C {devices/lab_pin.sym} 1400 320 0 0 {name=l78 sig_type=std_logic lab=en_3v3_b}
N 1610 120 1610 90 {}
C {devices/lab_pin.sym} 1610 90 0 0 {name=l79 sig_type=std_logic lab=vdd_3v3}
N 1690 120 1690 90 {}
C {devices/lab_pin.sym} 1690 90 0 1 {name=l80 sig_type=std_logic lab=vdd_1v2}
N 1610 480 1610 510 {}
C {devices/lab_pin.sym} 1610 510 0 0 {name=l81 sig_type=std_logic lab=vss_3v3}
N 1690 480 1690 510 {}
C {devices/lab_pin.sym} 1690 510 0 1 {name=l82 sig_type=std_logic lab=vss_1v2}
N 1870 300 2000 300 {lab=s7_an[1]}
T {Padframe route (DRAFT 2026-11-05): pad cells in the ring, bias and enable support in the slot} 40 -90 0 0 0.5 0.5 {}
T {dig_in[0..3]: switch enables.  dig_out[11:0]: tie low (not drawn).} 140 610 0 0 0.3 0.3 {}
T {iref: sourced from harness iDAC, no mirror} 480 450 0 0 0.3 0.3 {}
T {S2D: pad - vref = (outp - outn) / 2} 900 610 0 0 0.3 0.3 {}
T {D2S: pad - vref = (vinp - vinn) / 2} 1560 610 0 0 0.3 0.3 {}
