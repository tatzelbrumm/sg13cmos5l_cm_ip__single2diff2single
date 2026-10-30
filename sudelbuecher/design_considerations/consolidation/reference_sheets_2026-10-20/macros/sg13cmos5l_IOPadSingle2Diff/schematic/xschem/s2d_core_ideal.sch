v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_core_ideal: BEHAVIOURAL PLACEHOLDER for the input buffer core of sg13cmos5l_IOPadSingle2Diff} 0 -460 0 0 0.4 0.4 {}
T {outp = vcm + (padres - vref), outn = vcm - (padres - vref). Replace by the transistor-level buffer; keep the port list (bias lines from d2s_bias_sel_pd, en_3v3).} 0 -420 0 0 0.25 0.25 {}
C {devices/iopin.sym} 0 -360 0 0 {name=p1 lab=vdd}
C {devices/iopin.sym} 0 -340 0 0 {name=p2 lab=vss}
C {devices/ipin.sym} 0 -320 0 0 {name=p3 lab=padres}
C {devices/ipin.sym} 0 -300 0 0 {name=p4 lab=vref}
C {devices/ipin.sym} 0 -280 0 0 {name=p5 lab=vcm}
C {devices/opin.sym} 0 -260 0 0 {name=p6 lab=outp}
C {devices/opin.sym} 0 -240 0 0 {name=p7 lab=outn}
C {devices/ipin.sym} 0 -220 0 0 {name=p8 lab=vbp}
C {devices/ipin.sym} 0 -200 0 0 {name=p9 lab=vbn}
C {devices/ipin.sym} 0 -180 0 0 {name=p10 lab=vbpc}
C {devices/ipin.sym} 0 -160 0 0 {name=p11 lab=vbnc}
C {devices/ipin.sym} 0 -140 0 0 {name=p12 lab=vabp}
C {devices/ipin.sym} 0 -120 0 0 {name=p13 lab=vabn}
C {devices/ipin.sym} 0 -100 0 0 {name=p14 lab=en_3v3}
C {devices/vcvs.sym} 500 0 0 0 {name=Ep value=1}
C {devices/lab_pin.sym} 500 -30 0 1 {name=l0 sig_type=std_logic lab=outp}
C {devices/lab_pin.sym} 500 30 0 1 {name=l1 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 460 -20 0 0 {name=l2 sig_type=std_logic lab=padres}
C {devices/lab_pin.sym} 460 20 0 0 {name=l3 sig_type=std_logic lab=vref}
C {devices/vcvs.sym} 800 0 0 0 {name=En value=1}
C {devices/lab_pin.sym} 800 -30 0 1 {name=l4 sig_type=std_logic lab=outn}
C {devices/lab_pin.sym} 800 30 0 1 {name=l5 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 760 -20 0 0 {name=l6 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 760 20 0 0 {name=l7 sig_type=std_logic lab=padres}
C {devices/title.sym} 160 300 0 0 {name=l_title author="Christoph Maier"}
