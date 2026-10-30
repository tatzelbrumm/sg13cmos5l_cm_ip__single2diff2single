v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {d2s_mpdda_pd_sel: CACE fixture for the loop gain of sg13cmos5l_IOPadDiff2Single (driver + selectable bias, 3.3 V controls, vfb as a pin).} 0 -420 0 0 0.35 0.35 {}
T {Not a layout cell. In the pad, vfb = vout = pad and the controls come from en_ctrl_3v3.} 0 -380 0 0 0.25 0.25 {}
C {devices/iopin.sym} 0 -300 0 0 {name=p1 lab=vdd}
C {devices/iopin.sym} 0 -280 0 0 {name=p2 lab=vss}
C {devices/iopin.sym} 0 -260 0 0 {name=p3 lab=vddo}
C {devices/iopin.sym} 0 -240 0 0 {name=p4 lab=vsso}
C {devices/ipin.sym} 0 -220 0 0 {name=p5 lab=vinp}
C {devices/ipin.sym} 0 -200 0 0 {name=p6 lab=vinn}
C {devices/ipin.sym} 0 -180 0 0 {name=p7 lab=vref}
C {devices/iopin.sym} 0 -160 0 0 {name=p8 lab=vout}
C {devices/ipin.sym} 0 -140 0 0 {name=p9 lab=vfb}
C {devices/ipin.sym} 0 -120 0 0 {name=p10 lab=ibias}
C {devices/ipin.sym} 0 -100 0 0 {name=p11 lab=en_3v3}
C {devices/ipin.sym} 0 -80 0 0 {name=p12 lab=sel0_3v3}
C {devices/ipin.sym} 0 -60 0 0 {name=p13 lab=sel1_3v3}
C {d2s_bias_sel_pd.sym} 500 200 0 0 {name=xb}
C {devices/lab_pin.sym} 430 110 0 1 {name=l0 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 430 290 0 1 {name=l1 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 450 110 0 1 {name=l2 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 450 290 0 1 {name=l3 sig_type=std_logic lab=vsso}
C {devices/lab_pin.sym} 390 150 0 0 {name=l4 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 610 150 0 1 {name=l5 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 610 170 0 1 {name=l6 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 610 190 0 1 {name=l7 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 610 210 0 1 {name=l8 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 610 230 0 1 {name=l9 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 610 250 0 1 {name=l10 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 390 170 0 0 {name=l11 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 390 190 0 0 {name=l12 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_pin.sym} 390 210 0 0 {name=l13 sig_type=std_logic lab=sel1_3v3}
C {d2s_mpdda_pd.sym} 1100 -100 0 0 {name=xd}
C {devices/lab_pin.sym} 980 -220 0 0 {name=l14 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 980 20 0 0 {name=l15 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1260 -220 0 1 {name=l16 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 1260 20 0 1 {name=l17 sig_type=std_logic lab=vsso}
C {devices/lab_pin.sym} 920 -160 0 0 {name=l18 sig_type=std_logic lab=vinp}
C {devices/lab_pin.sym} 920 -120 0 0 {name=l19 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 920 -80 0 0 {name=l20 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 1320 -160 0 1 {name=l21 sig_type=std_logic lab=vout}
C {devices/lab_pin.sym} 920 -40 0 0 {name=l22 sig_type=std_logic lab=vfb}
C {devices/lab_pin.sym} 1020 20 0 1 {name=l23 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1060 20 0 1 {name=l24 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 1100 20 0 1 {name=l25 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 1140 20 0 1 {name=l26 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 1180 20 0 1 {name=l27 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 1220 20 0 1 {name=l28 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 920 -180 0 0 {name=l29 sig_type=std_logic lab=en_3v3}
C {devices/title.sym} 160 700 0 0 {name=l_title author="Christoph Maier"}
