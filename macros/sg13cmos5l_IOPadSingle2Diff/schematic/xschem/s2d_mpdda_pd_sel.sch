v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_mpdda_pd_sel: CACE fixture for the loop gain of sg13cmos5l_IOPadSingle2Diff (input buffer + selectable bias, 3.3 V controls, vfbp / vfbn as pins).} 80 -880 0 0 0.35 0.35 {}
T {Not a layout cell. In the pad, vfbp = voutp = outp, vfbn = voutn = outn, and the controls come from en_ctrl_3v3; vabp / vabn are unused there too.} 80 -840 0 0 0.25 0.25 {}
C {devices/iopin.sym} 100 -700 0 1 {name=p1 lab=vdd}
C {devices/ipin.sym} 100 -540 0 0 {name=p2 lab=vin}
C {devices/ipin.sym} 100 -500 0 0 {name=p3 lab=vref}
C {devices/ipin.sym} 100 -460 0 0 {name=p4 lab=vcm}
C {devices/ipin.sym} 100 -420 0 0 {name=p5 lab=en_3v3}
C {devices/ipin.sym} 100 -400 0 0 {name=p6 lab=en_3v3_b}
C {devices/ipin.sym} 100 -320 0 0 {name=p7 lab=ibias}
C {devices/ipin.sym} 100 -240 0 0 {name=p8 lab=sel0_3v3}
C {devices/ipin.sym} 100 -220 0 0 {name=p9 lab=sel1_3v3}
C {devices/iopin.sym} 100 -100 0 1 {name=p10 lab=vss}
C {devices/opin.sym} 1240 -520 0 0 {name=p11 lab=voutp}
C {devices/opin.sym} 1240 -480 0 0 {name=p12 lab=voutn}
C {devices/ipin.sym} 1240 -560 0 1 {name=p13 lab=vfbp}
C {devices/ipin.sym} 1240 -440 0 1 {name=p14 lab=vfbn}
C {d2s_bias_sel_pd.sym} 530 -270 0 0 {name=xb}
C {s2d_mpdda_pd.sym} 960 -480 0 0 {name=xa}
N 100 -700 500 -700 {lab=vdd}
N 500 -700 540 -700 {lab=vdd}
N 540 -700 860 -700 {lab=vdd}
N 500 -700 500 -360 {lab=vdd}
N 540 -700 540 -360 {lab=vdd}
N 860 -700 860 -600 {lab=vdd}
N 100 -100 480 -100 {lab=vss}
N 480 -100 520 -100 {lab=vss}
N 520 -100 840 -100 {lab=vss}
N 480 -180 480 -100 {lab=vss}
N 520 -180 520 -100 {lab=vss}
N 840 -360 840 -100 {lab=vss}
N 100 -540 780 -540 {lab=vin}
N 100 -500 780 -500 {lab=vref}
N 100 -460 780 -460 {lab=vcm}
N 100 -420 400 -420 {lab=en_3v3}
N 400 -420 780 -420 {lab=en_3v3}
N 400 -420 400 -280 {lab=en_3v3}
N 400 -280 440 -280 {lab=en_3v3}
N 100 -400 420 -400 {lab=en_3v3_b}
N 420 -400 780 -400 {lab=en_3v3_b}
N 420 -400 420 -260 {lab=en_3v3_b}
N 420 -260 440 -260 {lab=en_3v3_b}
N 100 -320 440 -320 {lab=ibias}
N 100 -240 440 -240 {lab=sel0_3v3}
N 100 -220 440 -220 {lab=sel1_3v3}
N 620 -320 900 -320 {lab=vbp}
N 900 -320 900 -360 {lab=vbp}
C {devices/lab_pin.sym} 900 -320 0 1 {name=l_vbp sig_type=std_logic lab=vbp}
N 620 -300 920 -300 {lab=vbpc}
N 920 -300 920 -360 {lab=vbpc}
C {devices/lab_pin.sym} 920 -300 0 1 {name=l_vbpc sig_type=std_logic lab=vbpc}
N 620 -240 1000 -240 {lab=vbnc}
N 1000 -240 1000 -360 {lab=vbnc}
C {devices/lab_pin.sym} 1000 -240 0 1 {name=l_vbnc sig_type=std_logic lab=vbnc}
N 620 -220 1020 -220 {lab=vbn}
N 1020 -220 1020 -360 {lab=vbn}
C {devices/lab_pin.sym} 1020 -220 0 1 {name=l_vbn sig_type=std_logic lab=vbn}
N 620 -280 660 -280 {lab=vabp}
C {devices/lab_pin.sym} 660 -280 0 1 {name=l_vabp sig_type=std_logic lab=vabp}
N 620 -260 660 -260 {lab=vabn}
C {devices/lab_pin.sym} 660 -260 0 1 {name=l_vabn sig_type=std_logic lab=vabn}
N 1140 -520 1240 -520 {lab=voutp}
N 1140 -480 1240 -480 {lab=voutn}
N 1140 -560 1240 -560 {lab=vfbp}
N 1140 -440 1240 -440 {lab=vfbn}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 80 -140 0 0 0.2 0.2 {}
