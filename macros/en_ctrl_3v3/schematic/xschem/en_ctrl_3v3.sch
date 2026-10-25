v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {en_ctrl_3v3: fail-safe enable and select bits for the 3.3 V pad circuits} 20 -832 0 0 0.4 0.4 {}
T {en_3v3 = en_1v2 AND vdd_1v2 present AND vdd_3v3 present; sel*_3v3 = sel*_1v2 level-shifted (gated by en_3v3 in d2s_bias_sel_pd).} 50 -792 0 0 0.25 0.25 {}
T {en_3v3_b = NOT en_3v3 (XIB): the complement for the NMOS enable switches of d2s_mpdda_pd and for the bias tree of d2s_bias_sel_pd.} 50 -770 0 0 0.25 0.25 {}
T {vddh: iovdd in the pad (vdd_3v3 in the slot fallback). vddl: input inverters of ls_up, the 1.2 V core ring vdd in the pad (vdd_1v2 in the fallback).} 50 -748 0 0 0.25 0.25 {}
T {With vddl = 0 the ls_up latches are undefined: pg_det of vdd_1v2 forces en_3v3 low. ls_up_1v2_3v3 can be replaced by IHP sg13cmos5l_LevelUp (same topology).} 50 -726 0 0 0.25 0.25 {}
T {Source: netlist/source/en_ctrl_3v3.spice} 50 -704 0 0 0.25 0.25 {}
N 240 -510 240 -100 {lab=vss}
N 420 -540 640 -540 {lab=en_ls}
N 480 -440 480 -100 {lab=vss}
N 420 -460 440 -460 {lab=en_ls}
N 520 -460 600 -460 {lab=en_ls_b}
N 780 -200 800 -200 {lab=pg1_b}
N 640 -180 660 -180 {lab=en_ls}
N 780 -360 820 -360 {lab=pg3_b}
N 640 -340 660 -340 {lab=en_ls}
N 860 -320 880 -320 {lab=en_ls_b}
N 1000 -280 1020 -280 {lab=en_3v3}
N 1020 -280 1040 -280 {lab=en_3v3}
N 1020 -280 1020 -180 {lab=en_3v3}
N 1020 -180 1080 -180 {lab=en_3v3}
N 1160 -180 1200 -180 {lab=en_3v3_b}
N 1140 -200 1140 -660 {lab=vddh}
N 960 -660 1140 -660 {lab=vddh}
N 1120 -160 1120 -100 {lab=vss}
N 940 -100 1120 -100 {lab=vss}
N 230 -620 230 -210 {lab=vddl}
N 160 -180 200 -180 {lab=sel0_1v2}
N 160 -100 240 -100 {lab=vss}
N 160 -360 200 -360 {lab=sel1_1v2}
N 160 -540 200 -540 {lab=en_1v2}
N 160 -620 230 -620 {lab=vddl}
N 280 -180 320 -180 {lab=sel0_3v3}
N 280 -360 320 -360 {lab=sel1_3v3}
N 240 -100 480 -100 {lab=vss}
N 580 -360 660 -360 {lab=vdd3v3_sense}
N 580 -200 660 -200 {lab=vdd1v2_sense}
N 640 -340 640 -180 {lab=en_ls}
N 600 -160 660 -160 {lab=en_ls_b}
N 600 -320 660 -320 {lab=en_ls_b}
N 640 -540 640 -340 {lab=en_ls}
N 420 -540 420 -460 {lab=en_ls}
N 280 -540 420 -540 {lab=en_ls}
N 600 -320 600 -160 {lab=en_ls_b}
N 600 -460 600 -320 {lab=en_ls_b}
N 500 -660 700 -660 {lab=vddh}
N 250 -660 250 -210 {lab=vddh}
N 160 -660 250 -660 {lab=vddh}
N 700 -660 960 -660 {lab=vddh}
N 700 -660 700 -240 {lab=vddh}
N 740 -280 740 -100 {lab=vss}
N 480 -100 740 -100 {lab=vss}
N 800 -280 800 -200 {lab=pg1_b}
N 800 -280 880 -280 {lab=pg1_b}
N 820 -240 880 -240 {lab=pg3_b}
N 820 -360 820 -240 {lab=pg3_b}
N 600 -460 860 -460 {lab=en_ls_b}
N 500 -660 500 -480 {lab=vddh}
N 250 -660 500 -660 {lab=vddh}
N 860 -460 860 -320 {lab=en_ls_b}
N 740 -100 940 -100 {lab=vss}
N 960 -660 960 -320 {lab=vddh}
N 940 -240 940 -100 {lab=vss}
C {devices/iopin.sym} 160 -660 0 1 {name=p0 lab=vddh}
C {devices/iopin.sym} 160 -620 0 1 {name=p1 lab=vddl}
C {devices/iopin.sym} 160 -100 0 1 {name=p2 lab=vss}
C {devices/ipin.sym} 160 -540 0 0 {name=p3 lab=en_1v2}
C {devices/ipin.sym} 160 -180 0 0 {name=p4 lab=sel0_1v2}
C {devices/ipin.sym} 160 -360 0 0 {name=p5 lab=sel1_1v2}
C {devices/ipin.sym} 580 -200 0 0 {name=p6 lab=vdd1v2_sense}
C {devices/ipin.sym} 580 -360 0 0 {name=p7 lab=vdd3v3_sense}
C {devices/opin.sym} 1040 -280 0 0 {name=p8 lab=en_3v3}
C {devices/opin.sym} 320 -180 0 0 {name=p9 lab=sel0_3v3}
C {devices/opin.sym} 320 -360 0 0 {name=p10 lab=sel1_3v3}
C {ls_up_1v2_3v3.sym} 240 -540 0 0 {name=XLE}
C {ls_up_1v2_3v3.sym} 240 -180 0 0 {name=XL0}
C {ls_up_1v2_3v3.sym} 240 -360 0 0 {name=XL1}
C {inv_hv.sym} 480 -460 0 0 {name=XIE}
C {devices/lab_pin.sym} 480 -420 0 1 {name=l17 sig_type=std_logic lab=vss}
C {pg_det.sym} 720 -180 0 0 {name=XG1}
C {devices/lab_pin.sym} 800 -200 0 1 {name=l23 sig_type=std_logic lab=pg1_b}
C {pg_det.sym} 720 -340 0 0 {name=XG3}
C {devices/lab_pin.sym} 820 -360 0 1 {name=l29 sig_type=std_logic lab=pg3_b}
C {nor3_hv.sym} 940 -280 0 0 {name=XNO}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
C {inv_hv.sym} 1120 -180 0 0 {name=XIB}
C {devices/opin.sym} 1200 -180 0 0 {name=p13 lab=en_3v3_b}
C {lab_wire.sym} 780 -460 0 0 {name=p11 lab=en_ls_b}
C {lab_wire.sym} 580 -540 0 0 {name=p12 lab=en_ls}
