v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {en_ctrl_3v3: fail-safe enable and select bits for the 3.3 V pad circuits} 0 -60 0 0 0.4 0.4 {}
C {devices/iopin.sym} 40 40 0 0 {name=p0 lab=vddh}
C {devices/iopin.sym} 40 70 0 0 {name=p1 lab=vddl}
C {devices/iopin.sym} 40 100 0 0 {name=p2 lab=vss}
C {devices/ipin.sym} 40 130 0 0 {name=p3 lab=en_1v2}
C {devices/ipin.sym} 40 160 0 0 {name=p4 lab=sel0_1v2}
C {devices/ipin.sym} 40 190 0 0 {name=p5 lab=sel1_1v2}
C {devices/ipin.sym} 40 220 0 0 {name=p6 lab=vdd1v2_sense}
C {devices/ipin.sym} 40 250 0 0 {name=p7 lab=vdd3v3_sense}
C {devices/opin.sym} 40 280 0 0 {name=p8 lab=en_3v3}
C {devices/opin.sym} 40 310 0 0 {name=p9 lab=sel0_3v3}
C {devices/opin.sym} 40 340 0 0 {name=p10 lab=sel1_3v3}
C {ls_up_1v2_3v3.sym} 300 80 0 0 {name=XLE}
N 300 110 300 130 {lab=vss}
C {devices/lab_pin.sym} 300 130 0 1 {name=l1 sig_type=std_logic lab=vss}
N 290 50 290 30 {lab=vddl}
C {devices/lab_pin.sym} 290 30 0 1 {name=l2 sig_type=std_logic lab=vddl}
N 310 50 310 30 {lab=vddh}
C {devices/lab_pin.sym} 310 30 0 1 {name=l3 sig_type=std_logic lab=vddh}
N 340 80 360 80 {lab=en_ls}
C {devices/lab_pin.sym} 360 80 0 1 {name=l4 sig_type=std_logic lab=en_ls}
N 260 80 240 80 {lab=en_1v2}
C {devices/lab_pin.sym} 240 80 0 0 {name=l5 sig_type=std_logic lab=en_1v2}
C {ls_up_1v2_3v3.sym} 300 240 0 0 {name=XL0}
N 300 270 300 290 {lab=vss}
C {devices/lab_pin.sym} 300 290 0 1 {name=l6 sig_type=std_logic lab=vss}
N 290 210 290 190 {lab=vddl}
C {devices/lab_pin.sym} 290 190 0 1 {name=l7 sig_type=std_logic lab=vddl}
N 310 210 310 190 {lab=vddh}
C {devices/lab_pin.sym} 310 190 0 1 {name=l8 sig_type=std_logic lab=vddh}
N 340 240 360 240 {lab=sel0_3v3}
C {devices/lab_pin.sym} 360 240 0 1 {name=l9 sig_type=std_logic lab=sel0_3v3}
N 260 240 240 240 {lab=sel0_1v2}
C {devices/lab_pin.sym} 240 240 0 0 {name=l10 sig_type=std_logic lab=sel0_1v2}
C {ls_up_1v2_3v3.sym} 300 400 0 0 {name=XL1}
N 300 430 300 450 {lab=vss}
C {devices/lab_pin.sym} 300 450 0 1 {name=l11 sig_type=std_logic lab=vss}
N 290 370 290 350 {lab=vddl}
C {devices/lab_pin.sym} 290 350 0 1 {name=l12 sig_type=std_logic lab=vddl}
N 310 370 310 350 {lab=vddh}
C {devices/lab_pin.sym} 310 350 0 1 {name=l13 sig_type=std_logic lab=vddh}
N 340 400 360 400 {lab=sel1_3v3}
C {devices/lab_pin.sym} 360 400 0 1 {name=l14 sig_type=std_logic lab=sel1_3v3}
N 260 400 240 400 {lab=sel1_1v2}
C {devices/lab_pin.sym} 240 400 0 0 {name=l15 sig_type=std_logic lab=sel1_1v2}
C {inv_hv.sym} 560 80 0 0 {name=XIE}
N 540 40 540 20 {lab=vddh}
C {devices/lab_pin.sym} 540 20 0 1 {name=l16 sig_type=std_logic lab=vddh}
N 540 120 540 140 {lab=vss}
C {devices/lab_pin.sym} 540 140 0 1 {name=l17 sig_type=std_logic lab=vss}
N 500 80 480 80 {lab=en_ls}
C {devices/lab_pin.sym} 480 80 0 0 {name=l18 sig_type=std_logic lab=en_ls}
N 620 80 640 80 {lab=en_ls_b}
C {devices/lab_pin.sym} 640 80 0 1 {name=l19 sig_type=std_logic lab=en_ls_b}
C {pg_det.sym} 560 260 0 0 {name=XG1}
N 540 200 540 180 {lab=vddh}
C {devices/lab_pin.sym} 540 180 0 1 {name=l20 sig_type=std_logic lab=vddh}
N 540 320 540 340 {lab=vss}
C {devices/lab_pin.sym} 540 340 0 1 {name=l21 sig_type=std_logic lab=vss}
N 500 240 480 240 {lab=vdd1v2_sense}
C {devices/lab_pin.sym} 480 240 0 0 {name=l22 sig_type=std_logic lab=vdd1v2_sense}
N 620 240 640 240 {lab=pg1_b}
C {devices/lab_pin.sym} 640 240 0 1 {name=l23 sig_type=std_logic lab=pg1_b}
N 500 260 480 260 {lab=en_ls}
C {devices/lab_pin.sym} 480 260 0 0 {name=l24 sig_type=std_logic lab=en_ls}
N 500 280 480 280 {lab=en_ls_b}
C {devices/lab_pin.sym} 480 280 0 0 {name=l25 sig_type=std_logic lab=en_ls_b}
C {pg_det.sym} 560 440 0 0 {name=XG3}
N 540 380 540 360 {lab=vddh}
C {devices/lab_pin.sym} 540 360 0 1 {name=l26 sig_type=std_logic lab=vddh}
N 540 500 540 520 {lab=vss}
C {devices/lab_pin.sym} 540 520 0 1 {name=l27 sig_type=std_logic lab=vss}
N 500 420 480 420 {lab=vdd3v3_sense}
C {devices/lab_pin.sym} 480 420 0 0 {name=l28 sig_type=std_logic lab=vdd3v3_sense}
N 620 420 640 420 {lab=pg3_b}
C {devices/lab_pin.sym} 640 420 0 1 {name=l29 sig_type=std_logic lab=pg3_b}
N 500 440 480 440 {lab=en_ls}
C {devices/lab_pin.sym} 480 440 0 0 {name=l30 sig_type=std_logic lab=en_ls}
N 500 460 480 460 {lab=en_ls_b}
C {devices/lab_pin.sym} 480 460 0 0 {name=l31 sig_type=std_logic lab=en_ls_b}
C {nor3_hv.sym} 820 260 0 0 {name=XNO}
N 800 200 800 180 {lab=vddh}
C {devices/lab_pin.sym} 800 180 0 1 {name=l32 sig_type=std_logic lab=vddh}
N 800 320 800 340 {lab=vss}
C {devices/lab_pin.sym} 800 340 0 1 {name=l33 sig_type=std_logic lab=vss}
N 760 240 740 240 {lab=en_ls_b}
C {devices/lab_pin.sym} 740 240 0 0 {name=l34 sig_type=std_logic lab=en_ls_b}
N 760 260 740 260 {lab=pg1_b}
C {devices/lab_pin.sym} 740 260 0 0 {name=l35 sig_type=std_logic lab=pg1_b}
N 760 280 740 280 {lab=pg3_b}
C {devices/lab_pin.sym} 740 280 0 0 {name=l36 sig_type=std_logic lab=pg3_b}
N 880 240 900 240 {lab=en_3v3}
C {devices/lab_pin.sym} 900 240 0 1 {name=l37 sig_type=std_logic lab=en_3v3}
T {en_3v3 = en_1v2 AND vdd_1v2 present AND vdd_3v3 present; sel*_3v3 = sel*_1v2 level-shifted (gated by en_3v3 in d2s_bias_sel_pd).} 40 560 0 0 0.25 0.25 {}
T {vddh: iovdd in the pad (vdd_3v3 in the slot fallback). vddl: input inverters of ls_up, the 1.2 V core ring vdd in the pad (vdd_1v2 in the fallback).} 40 582 0 0 0.25 0.25 {}
T {With vddl = 0 the ls_up latches are undefined: pg_det of vdd_1v2 forces en_3v3 low. ls_up_1v2_3v3 can be replaced by IHP sg13cmos5l_LevelUp (same topology).} 40 604 0 0 0.25 0.25 {}
T {Source: netlist/source/en_ctrl_3v3.spice} 40 626 0 0 0.25 0.25 {}
C {devices/title.sym} 160 600 0 0 {name=l0 author="Christoph Maier"}
