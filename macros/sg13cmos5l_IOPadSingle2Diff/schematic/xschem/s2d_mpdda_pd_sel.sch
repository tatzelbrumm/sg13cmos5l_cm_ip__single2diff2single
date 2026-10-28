v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_mpdda_pd_sel: CACE fixture for the loop gain of sg13cmos5l_IOPadSingle2Diff (input buffer + selectable bias, 3.3 V controls, vfbp / vfbn as pins).} 40 -780 0 0 0.35 0.35 {}
T {Not a layout cell. In the pad, vfbp = voutp = outp, vfbn = voutn = outn, and the controls come from en_ctrl_3v3. Bias: bias_gen_pd + bias_tree_noab_pd (four lines; one bias_sel_noab_pd until 2026-10-28).} 40 -740 0 0 0.25 0.25 {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 80 -140 0 0 0.2 0.2 {}
N 680 -700 1000 -700 {lab=vdd}
N 640 -700 680 -700 {lab=vdd}
N 1000 -700 1000 -600 {lab=vdd}
N 660 -100 980 -100 {lab=vss}
N 620 -100 660 -100 {lab=vss}
N 980 -360 980 -100 {lab=vss}
N 140 -420 920 -420 {lab=en_3v3}
N 160 -400 920 -400 {lab=en_3v3_b}
N 1040 -360 1040 -320 {lab=vbp}
N 760 -300 1060 -300 {lab=vbpc}
N 1060 -360 1060 -300 {lab=vbpc}
N 1100 -360 1100 -240 {lab=vbnc}
N 1120 -360 1120 -220 {lab=vbn}
N 1200 -520 1240 -520 {lab=vfbp}
N 1200 -500 1240 -500 {lab=voutp}
N 1200 -460 1240 -460 {lab=voutn}
N 1200 -440 1240 -440 {lab=vfbn}
N 100 -700 640 -700 {lab=vdd}
N 100 -100 620 -100 {lab=vss}
N 100 -420 140 -420 {lab=en_3v3}
N 100 -400 160 -400 {lab=en_3v3_b}
N 760 -320 1040 -320 {lab=vbp}
N 760 -240 1100 -240 {lab=vbnc}
N 760 -220 1120 -220 {lab=vbn}
N 100 -540 920 -540 {lab=vcm}
N 100 -500 920 -500 {lab=vin}
N 100 -460 920 -460 {lab=#net1}
C {devices/iopin.sym} 100 -700 0 1 {name=p1 lab=vdd}
C {devices/ipin.sym} 100 -500 0 0 {name=p2 lab=vin}
C {devices/ipin.sym} 100 -460 0 0 {name=p3 lab=vref}
C {devices/ipin.sym} 100 -540 0 0 {name=p4 lab=vcm}
C {devices/ipin.sym} 100 -420 0 0 {name=p5 lab=en_3v3}
C {devices/ipin.sym} 100 -400 0 0 {name=p6 lab=en_3v3_b}
C {devices/ipin.sym} 100 -320 0 0 {name=p7 lab=ibias}
C {devices/ipin.sym} 100 -240 0 0 {name=p8 lab=sel0_3v3}
C {devices/ipin.sym} 100 -220 0 0 {name=p9 lab=sel1_3v3}
C {devices/iopin.sym} 100 -100 0 1 {name=p10 lab=vss}
C {devices/opin.sym} 1240 -500 0 0 {name=p11 lab=voutp}
C {devices/opin.sym} 1240 -460 0 0 {name=p12 lab=voutn}
C {devices/ipin.sym} 1240 -520 0 1 {name=p13 lab=vfbp}
C {devices/ipin.sym} 1240 -440 0 1 {name=p14 lab=vfbn}
C {s2d_mpdda_pd.sym} 1060 -480 0 0 {name=xa}
C {devices/lab_pin.sym} 1040 -320 0 1 {name=l_vbp sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1060 -300 0 1 {name=l_vbpc sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 1100 -240 0 1 {name=l_vbnc sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 1120 -220 0 1 {name=l_vbn sig_type=std_logic lab=vbn}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
C {bias_gen_pd.sym} 320 -290 0 0 {name=xg}
C {bias_tree_noab_pd.sym} 660 -270 0 0 {name=xt}
N 100 -320 230 -320 {lab=ibias}
N 140 -420 140 -300 {lab=en_3v3}
N 140 -300 230 -300 {lab=en_3v3}
N 100 -240 180 -240 {lab=sel0_3v3}
N 180 -280 180 -240 {lab=sel0_3v3}
N 180 -280 230 -280 {lab=sel0_3v3}
N 100 -220 200 -220 {lab=sel1_3v3}
N 200 -260 200 -220 {lab=sel1_3v3}
N 200 -260 230 -260 {lab=sel1_3v3}
N 410 -290 430 -290 {lab=iref}
N 430 -320 430 -290 {lab=iref}
N 430 -320 560 -320 {lab=iref}
C {devices/lab_wire.sym} 430 -320 0 1 {name=l_iref sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 560 -300 0 0 {name=l_xt_en sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 560 -280 0 0 {name=l_xt_enb sig_type=std_logic lab=en_3v3_b}
N 620 -700 620 -360 {lab=vdd}
N 600 -180 600 -100 {lab=vss}
C {devices/lab_pin.sym} 320 -370 0 1 {name=l_xg_vdd sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 320 -210 0 1 {name=l_xg_vss sig_type=std_logic lab=vss}
