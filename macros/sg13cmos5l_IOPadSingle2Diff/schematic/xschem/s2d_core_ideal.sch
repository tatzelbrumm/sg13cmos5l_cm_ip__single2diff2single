v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_core_ideal: BEHAVIOURAL PLACEHOLDER for the input buffer core of sg13cmos5l_IOPadSingle2Diff} 0 -640 0 0 0.4 0.4 {}
T {outp = vcm + (padres - vref), outn = vcm - (padres - vref). Replace by the transistor-level buffer; keep the port list (bias lines from d2s_bias_sel_pd, en_3v3).} 0 -600 0 0 0.25 0.25 {}
N 640 -440 640 -410 {lab=outp}
N 640 -440 700 -440 {lab=outp}
N 640 -320 700 -320 {lab=vcm}
N 640 -350 640 -320 {lab=vcm}
N 640 -320 640 -290 {lab=vcm}
N 640 -230 640 -200 {lab=outn}
N 640 -200 700 -200 {lab=outn}
N 560 -240 600 -240 {lab=vref}
N 560 -360 600 -360 {lab=vref}
N 560 -360 560 -240 {lab=vref}
N 100 -240 560 -240 {lab=vref}
N 540 -400 600 -400 {lab=padres}
N 540 -280 600 -280 {lab=padres}
N 540 -400 540 -280 {lab=padres}
N 100 -400 540 -400 {lab=padres}
C {devices/iopin.sym} 100 -540 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 100 -100 0 1 {name=p2 lab=vss}
C {devices/ipin.sym} 100 -400 0 0 {name=p3 lab=padres}
C {devices/ipin.sym} 100 -240 0 0 {name=p4 lab=vref}
C {devices/ipin.sym} 700 -320 0 1 {name=p5 lab=vcm}
C {devices/opin.sym} 700 -440 0 0 {name=p6 lab=outp}
C {devices/opin.sym} 700 -200 0 0 {name=p7 lab=outn}
C {devices/ipin.sym} 100 -500 0 0 {name=p8 lab=vbp}
C {devices/ipin.sym} 100 -140 0 0 {name=p9 lab=vbn}
C {devices/ipin.sym} 100 -480 0 0 {name=p10 lab=vbpc}
C {devices/ipin.sym} 100 -160 0 0 {name=p11 lab=vbnc}
C {devices/ipin.sym} 100 -460 0 0 {name=p12 lab=vabp}
C {devices/ipin.sym} 100 -180 0 0 {name=p13 lab=vabn}
C {devices/ipin.sym} 100 -320 0 0 {name=p14 lab=en_3v3}
C {devices/vcvs.sym} 640 -380 0 0 {name=Ep value=1}
C {devices/lab_pin.sym} 640 -410 0 1 {name=l0 sig_type=std_logic lab=outp}
C {devices/lab_pin.sym} 640 -350 0 1 {name=l1 sig_type=std_logic lab=vcm}
C {devices/vcvs.sym} 640 -260 0 0 {name=En value=1}
C {devices/lab_pin.sym} 640 -230 0 1 {name=l4 sig_type=std_logic lab=outn}
C {devices/lab_pin.sym} 640 -290 0 1 {name=l5 sig_type=std_logic lab=vcm}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
