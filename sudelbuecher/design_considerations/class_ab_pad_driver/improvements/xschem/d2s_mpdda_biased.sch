v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 860 -160 860 -120 {lab=vddo}
N 860 120 860 160 {lab=vsso}
N 260 200 260 240 {lab=vddo}
N 260 560 260 600 {lab=vsso}
C {d2s_mpdda.sym} 700 0 0 0 {name=xd}
C {d2s_bias_lp.sym} 300 400 0 0 {name=xb}
N 440 300 620 300 {lab=vbp}
N 620 300 620 120 {lab=vbp}
C {devices/lab_wire.sym} 620 300 0 0 {name=l1 sig_type=std_logic lab=vbp}
N 440 340 660 340 {lab=vbn}
N 660 340 660 120 {lab=vbn}
C {devices/lab_wire.sym} 660 340 0 0 {name=l2 sig_type=std_logic lab=vbn}
N 440 380 700 380 {lab=vbpc}
N 700 380 700 120 {lab=vbpc}
C {devices/lab_wire.sym} 700 380 0 0 {name=l3 sig_type=std_logic lab=vbpc}
N 440 420 740 420 {lab=vbnc}
N 740 420 740 120 {lab=vbnc}
C {devices/lab_wire.sym} 740 420 0 0 {name=l4 sig_type=std_logic lab=vbnc}
N 440 460 780 460 {lab=vabp}
N 780 460 780 120 {lab=vabp}
C {devices/lab_wire.sym} 780 460 0 0 {name=l5 sig_type=std_logic lab=vabp}
N 440 500 820 500 {lab=vabn}
N 820 500 820 120 {lab=vabn}
C {devices/lab_wire.sym} 820 500 0 0 {name=l6 sig_type=std_logic lab=vabn}
N 520 -60 460 -60 {lab=vinp}
C {devices/lab_pin.sym} 460 -60 0 0 {name=l7 sig_type=std_logic lab=vinp}
N 520 -20 460 -20 {lab=vinn}
C {devices/lab_pin.sym} 460 -20 0 0 {name=l8 sig_type=std_logic lab=vinn}
N 520 20 460 20 {lab=vref}
C {devices/lab_pin.sym} 460 20 0 0 {name=l9 sig_type=std_logic lab=vref}
N 520 60 460 60 {lab=vfb}
C {devices/lab_pin.sym} 460 60 0 0 {name=l10 sig_type=std_logic lab=vfb}
N 920 -60 940 -60 {lab=vout}
C {devices/lab_pin.sym} 940 -60 0 1 {name=l11 sig_type=std_logic lab=vout}
N 580 -120 580 -160 {lab=vdd}
C {devices/lab_pin.sym} 580 -160 0 1 {name=l12 sig_type=std_logic lab=vdd}
N 580 120 540 120 {lab=vss}
C {devices/lab_pin.sym} 540 120 0 0 {name=l13 sig_type=std_logic lab=vss}
N 220 240 220 200 {lab=vdd}
C {devices/lab_pin.sym} 220 200 0 1 {name=l14 sig_type=std_logic lab=vdd}
N 220 560 220 600 {lab=vss}
C {devices/lab_pin.sym} 220 600 0 1 {name=l15 sig_type=std_logic lab=vss}
C {devices/iopin.sym} 60 -200 0 0 {name=p0 lab=vdd}
C {devices/iopin.sym} 60 -160 0 0 {name=p1 lab=vss}
C {devices/iopin.sym} 60 -120 0 0 {name=p2 lab=vddo}
C {devices/iopin.sym} 60 -80 0 0 {name=p3 lab=vsso}
C {devices/ipin.sym} 60 -40 0 0 {name=p4 lab=vinp}
C {devices/ipin.sym} 60 0 0 0 {name=p5 lab=vinn}
C {devices/ipin.sym} 60 40 0 0 {name=p6 lab=vref}
C {devices/iopin.sym} 60 80 0 0 {name=p7 lab=vout}
C {devices/ipin.sym} 60 120 0 0 {name=p8 lab=vfb}
C {devices/iopin.sym} 60 160 0 0 {name=p9 lab=vbp}
C {devices/iopin.sym} 60 200 0 0 {name=p10 lab=vbn}
C {devices/iopin.sym} 60 240 0 0 {name=p11 lab=vbpc}
C {devices/iopin.sym} 60 280 0 0 {name=p12 lab=vbnc}
C {devices/iopin.sym} 60 320 0 0 {name=p13 lab=vabp}
C {devices/iopin.sym} 60 360 0 0 {name=p14 lab=vabn}
T {d2s_mpdda + d2s_bias_lp test fixture (CACE DUT); bias nets are pins for bias-quality perturbation} 60 -300 0 0 0.4 0.4 {}
C {devices/lab_pin.sym} 860 -160 0 1 {name=l31 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 860 160 0 1 {name=l32 sig_type=std_logic lab=vsso}
C {devices/lab_pin.sym} 260 200 0 1 {name=l33 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 260 600 0 1 {name=l34 sig_type=std_logic lab=vsso}
