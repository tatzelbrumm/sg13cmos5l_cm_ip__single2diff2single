v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {en_ctrl_3v3 (v2): fail-safe enable and select bits for the 3.3 V circuits of slot 7 and its pads} 0 -1090 0 0 0.4 0.4 {}
T {en_3v3 = en_1v2 at 3.3 V, en_3v3_b = NOT en_3v3 (XE). sel0_3v3 / sel1_3v3 = sel0_1v2 / sel1_1v2 at 3.3 V} 40 -1040 0 0 0.25 0.25 {}
T {(XS0, XS1), gated by en_3v3 downstream; sel0_b, sel1_b are not used.} 40 -1018 0 0 0.25 0.25 {}
T {Each bit is one ls_up_fs, shifted without a 1.2 V supply: the inputs are valid 1.2 V levels from the harness} 40 -996 0 0 0.25 0.25 {}
T {always-on rail (enable, dig_in), also while the slot vdd_1v2 is off.} 40 -974 0 0 0.25 0.25 {}
T {vddh / vss: the slot switched vdd_3v3 / vss_3v3; the cell is unpowered with it. No supply sensing.} 40 -952 0 0 0.25 0.25 {}
T {Static current: the leaker of each ls_up_fs whose input is 1. Source: netlist/source/en_ctrl_3v3.spice} 40 -930 0 0 0.25 0.25 {}
T {not connected (kept for the symbol)} 90 -808 0 0 0.25 0.25 {}
T {not connected (kept for the symbol)} 90 -228 0 0 0.25 0.25 {}
T {not connected (kept for the symbol)} 90 -188 0 0 0.25 0.25 {}
N 60 -840 420 -840 {lab=vddh}
N 420 -840 420 -400 {lab=vddh}
N 60 -120 720 -120 {lab=vss}
N 720 -120 720 -640 {lab=vss}
N 500 -780 500 -800 {lab=vddh}
N 420 -800 500 -800 {lab=vddh}
N 540 -660 540 -640 {lab=vss}
N 540 -640 720 -640 {lab=vss}
N 60 -740 440 -740 {lab=en_1v2}
N 600 -740 860 -740 {lab=en_3v3}
N 600 -720 860 -720 {lab=en_3v3_b}
N 500 -580 500 -600 {lab=vddh}
N 420 -600 500 -600 {lab=vddh}
N 540 -460 540 -440 {lab=vss}
N 540 -440 720 -440 {lab=vss}
N 60 -540 440 -540 {lab=sel0_1v2}
N 600 -540 860 -540 {lab=sel0_3v3}
N 600 -520 620 -520 {lab=sel0_b}
N 500 -380 500 -400 {lab=vddh}
N 420 -400 500 -400 {lab=vddh}
N 540 -260 540 -240 {lab=vss}
N 540 -240 720 -240 {lab=vss}
N 60 -340 440 -340 {lab=sel1_1v2}
N 600 -340 860 -340 {lab=sel1_3v3}
N 600 -320 620 -320 {lab=sel1_b}
C {devices/iopin.sym} 60 -840 0 1 {name=p0 lab=vddh}
C {devices/iopin.sym} 60 -800 0 1 {name=p1 lab=vddl}
C {devices/iopin.sym} 60 -120 0 1 {name=p2 lab=vss}
C {devices/ipin.sym} 60 -740 0 0 {name=p3 lab=en_1v2}
C {devices/ipin.sym} 60 -540 0 0 {name=p4 lab=sel0_1v2}
C {devices/ipin.sym} 60 -340 0 0 {name=p5 lab=sel1_1v2}
C {devices/ipin.sym} 60 -220 0 0 {name=p6 lab=vdd1v2_sense}
C {devices/ipin.sym} 60 -180 0 0 {name=p7 lab=vdd3v3_sense}
C {devices/opin.sym} 860 -740 0 0 {name=p8 lab=en_3v3}
C {devices/opin.sym} 860 -540 0 0 {name=p9 lab=sel0_3v3}
C {devices/opin.sym} 860 -340 0 0 {name=p10 lab=sel1_3v3}
C {devices/opin.sym} 860 -720 0 0 {name=p11 lab=en_3v3_b}
C {ls_up_fs.sym} 520 -720 0 0 {name=XE}
C {ls_up_fs.sym} 520 -520 0 0 {name=XS0}
C {ls_up_fs.sym} 520 -320 0 0 {name=XS1}
C {devices/lab_pin.sym} 620 -520 0 1 {name=lXS0 sig_type=std_logic lab=sel0_b}
C {devices/lab_pin.sym} 620 -320 0 1 {name=lXS1 sig_type=std_logic lab=sel1_b}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
