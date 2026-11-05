v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} 60 160 0 0 {name=p1 lab=ibias0}
C {devices/ipin.sym} 60 360 0 0 {name=p2 lab=ibias1}
C {devices/ipin.sym} 60 560 0 0 {name=p3 lab=vbias}
C {devices/ipin.sym} 60 -100 0 0 {name=p4 lab=enable}
C {devices/ipin.sym} 60 50 0 0 {name=p5 lab=ena_ib0}
C {devices/ipin.sym} 60 250 0 0 {name=p6 lab=ena_ib1}
C {devices/ipin.sym} 60 450 0 0 {name=p7 lab=ena_vbias}
C {devices/ipin.sym} 60 650 0 0 {name=p8 lab=ena_div}
C {devices/iopin.sym} 60 -220 0 0 {name=p9 lab=vdd_1v2}
C {devices/iopin.sym} 60 1040 0 0 {name=p10 lab=vss_1v2}
C {devices/iopin.sym} 60 -260 0 0 {name=p11 lab=vdd_3v3}
C {devices/iopin.sym} 60 1000 0 0 {name=p12 lab=vss_3v3}
C {devices/opin.sym} 800 360 0 0 {name=p13 lab=iref_s2d}
C {devices/opin.sym} 800 160 0 0 {name=p14 lab=iref_d2s}
C {devices/opin.sym} 800 -20 0 0 {name=p15 lab=en_3v3}
C {devices/opin.sym} 800 -100 0 0 {name=p16 lab=en_3v3_b}
C {devices/opin.sym} 800 620 0 0 {name=p17 lab=vref}
C {devices/opin.sym} 800 700 0 0 {name=p18 lab=vcm}
N 60 -100 260 -100 {}
C {ocd_ls_up_1v2_3v3.sym} 300 -100 0 0 {name=xls}
N 290 -130 290 -160 {}
C {devices/lab_pin.sym} 290 -160 0 0 {name=l19 sig_type=std_logic lab=vdd_1v2}
N 310 -130 310 -160 {}
C {devices/lab_pin.sym} 310 -160 0 1 {name=l20 sig_type=std_logic lab=vdd_3v3}
N 300 -70 300 -50 {}
C {devices/lab_pin.sym} 300 -50 0 1 {name=l21 sig_type=std_logic lab=vss_3v3}
N 340 -100 380 -100 {}
N 380 -100 420 -100 {}
C {inv_hv.sym} 460 -100 0 0 {name=xinv}
N 480 -120 480 -150 {}
C {devices/lab_pin.sym} 480 -150 0 1 {name=l22 sig_type=std_logic lab=vdd_3v3}
N 460 -80 460 -50 {}
C {devices/lab_pin.sym} 460 -50 0 1 {name=l23 sig_type=std_logic lab=vss_3v3}
N 500 -100 800 -100 {}
N 380 -100 380 -20 {}
N 380 -20 800 -20 {}
C {analog_switch_small.sym} 400 100 0 0 {name=xs_ib0}
N 60 50 250 50 {}
N 60 160 250 160 {}
N 550 50 570 50 {}
C {devices/lab_pin.sym} 570 50 0 1 {name=l24 sig_type=std_logic lab=vdd_1v2}
N 550 70 570 70 {}
C {devices/lab_pin.sym} 570 70 0 1 {name=l25 sig_type=std_logic lab=vss_1v2}
N 550 90 570 90 {}
C {devices/lab_pin.sym} 570 90 0 1 {name=l26 sig_type=std_logic lab=vdd_3v3}
N 550 110 570 110 {}
C {devices/lab_pin.sym} 570 110 0 1 {name=l27 sig_type=std_logic lab=vss_3v3}
C {analog_switch_small.sym} 400 300 0 0 {name=xs_ib1}
N 60 250 250 250 {}
N 60 360 250 360 {}
N 550 250 570 250 {}
C {devices/lab_pin.sym} 570 250 0 1 {name=l28 sig_type=std_logic lab=vdd_1v2}
N 550 270 570 270 {}
C {devices/lab_pin.sym} 570 270 0 1 {name=l29 sig_type=std_logic lab=vss_1v2}
N 550 290 570 290 {}
C {devices/lab_pin.sym} 570 290 0 1 {name=l30 sig_type=std_logic lab=vdd_3v3}
N 550 310 570 310 {}
C {devices/lab_pin.sym} 570 310 0 1 {name=l31 sig_type=std_logic lab=vss_3v3}
C {analog_switch_small.sym} 400 500 0 0 {name=xs_vb}
N 60 450 250 450 {}
N 60 560 250 560 {}
N 550 450 570 450 {}
C {devices/lab_pin.sym} 570 450 0 1 {name=l32 sig_type=std_logic lab=vdd_1v2}
N 550 470 570 470 {}
C {devices/lab_pin.sym} 570 470 0 1 {name=l33 sig_type=std_logic lab=vss_1v2}
N 550 490 570 490 {}
C {devices/lab_pin.sym} 570 490 0 1 {name=l34 sig_type=std_logic lab=vdd_3v3}
N 550 510 570 510 {}
C {devices/lab_pin.sym} 570 510 0 1 {name=l35 sig_type=std_logic lab=vss_3v3}
C {analog_switch_small.sym} 400 700 0 0 {name=xs_dv}
N 60 650 250 650 {}
N 550 650 570 650 {}
C {devices/lab_pin.sym} 570 650 0 1 {name=l36 sig_type=std_logic lab=vdd_1v2}
N 550 670 570 670 {}
C {devices/lab_pin.sym} 570 670 0 1 {name=l37 sig_type=std_logic lab=vss_1v2}
N 550 690 570 690 {}
C {devices/lab_pin.sym} 570 690 0 1 {name=l38 sig_type=std_logic lab=vdd_3v3}
N 550 710 570 710 {}
C {devices/lab_pin.sym} 570 710 0 1 {name=l39 sig_type=std_logic lab=vss_3v3}
N 550 160 800 160 {}
N 550 360 800 360 {}
N 550 560 720 560 {}
N 550 760 720 760 {}
N 720 560 720 760 {}
N 720 620 800 620 {}
N 720 700 800 700 {}
C {devices/res.sym} 140 730 0 0 {name=R1 value=200k footprint=1206 device=resistor m=1}
C {devices/res.sym} 140 790 0 0 {name=R2 value=200k footprint=1206 device=resistor m=1}
N 140 700 140 680 {}
C {devices/lab_pin.sym} 140 680 0 1 {name=l40 sig_type=std_logic lab=vdd_3v3}
N 140 820 140 850 {}
C {devices/lab_pin.sym} 140 850 0 1 {name=l41 sig_type=std_logic lab=vss_3v3}
N 140 760 250 760 {lab=vdiv}
T {ocd_pad_support (DRAFT 2026-11-05): slot-side bias and enable for the S2D / D2S pad cells} 60 -330 0 0 0.5 0.5 {}
T {enable (1.2 V) -> en_3v3, en_3v3_b. Not covered: en_3v3 low when vdd_1v2 is gated off (en_ctrl_3v3 has pg_det)} 420 -250 0 0 0.3 0.3 {}
T {ibias: sourced (iDAC).  iref: sourced into NMOS diode.} 600 185 0 0 0.3 0.3 {}
T {Same polarity: switch only, no mirror.} 600 210 0 0 0.3 0.3 {}
T {vref = vcm: vbias or divider.} 730 520 0 0 0.3 0.3 {}
T {Value open: S2D suite 1.2 V, D2S suite 1.65 V.} 730 550 0 0 0.3 0.3 {}
T {R1 = R2 placeholder (generic res), noise cap TBD} 200 935 0 0 0.3 0.3 {}
