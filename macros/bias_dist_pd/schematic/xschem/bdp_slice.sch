v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bdp_slice: one switched leg of bias_dist_pd, as the layout cell bdp_slice: nand2_hv | inv_hv | tg_hv} 0 -260 0 0 0.4 0.4 {}
T {e_b = NAND(en_3v3, en), e = NOT e_b; the transmission gate passes a <-> b while en_3v3 = 1 and en = 1.} 0 -210 0 0 0.25 0.25 {}
T {Source: netlist/source/bias_dist_pd.spice. vdd / vss: 3.3 V rail of bias_dist_pd (vddh / vssh), for the gates and the TG bulks.} 0 -188 0 0 0.25 0.25 {}
N 60 -20 200 -20 {lab=en_3v3}
N 60 20 200 20 {lab=en}
N 320 0 360 0 {lab=e_b}
N 360 0 400 0 {lab=e_b}
N 360 0 360 160 {lab=e_b}
N 360 160 620 160 {lab=e_b}
N 620 140 620 160 {lab=e_b}
N 480 0 620 0 {lab=e}
N 620 0 620 60 {lab=e}
N 60 100 580 100 {lab=a}
N 660 100 800 100 {lab=b}
N 260 30 260 220 {lab=vss}
N 440 20 440 220 {lab=vss}
N 650 140 650 220 {lab=vss}
N 440 220 650 220 {lab=vss}
N 60 220 260 220 {lab=vss}
N 260 220 440 220 {lab=vss}
N 650 -100 650 60 {lab=vdd}
N 460 -100 650 -100 {lab=vdd}
N 280 -100 280 -30 {lab=vdd}
N 60 -100 280 -100 {lab=vdd}
N 460 -100 460 -20 {lab=vdd}
N 280 -100 460 -100 {lab=vdd}
C {devices/lab_pin.sym} 280 -50 0 1 {name=l1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 260 50 0 1 {name=l2 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 460 -40 0 1 {name=l3 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 440 40 0 1 {name=l4 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 650 40 0 1 {name=l5 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 650 160 0 1 {name=l6 sig_type=std_logic lab=vss}
C {devices/lab_wire.sym} 560 0 0 0 {name=l7 sig_type=std_logic lab=e}
C {devices/lab_wire.sym} 560 160 0 0 {name=l8 sig_type=std_logic lab=e_b}
C {devices/iopin.sym} 60 -100 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 60 220 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 60 -20 0 0 {name=p2 lab=en_3v3}
C {devices/ipin.sym} 60 20 0 0 {name=p3 lab=en}
C {devices/iopin.sym} 60 100 0 1 {name=p4 lab=a}
C {devices/iopin.sym} 800 100 0 0 {name=p5 lab=b}
C {nand2_hv.sym} 260 0 0 0 {name=XA}
C {inv_hv.sym} 440 0 0 0 {name=XB}
C {tg_hv.sym} 620 100 0 0 {name=XT}
C {devices/title.sym} 160 320 0 0 {name=l0 author="Christoph Maier"}
