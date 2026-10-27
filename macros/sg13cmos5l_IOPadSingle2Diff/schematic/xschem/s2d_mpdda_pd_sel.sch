v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_mpdda_pd_sel: CACE fixture for the loop gain of sg13cmos5l_IOPadSingle2Diff (input buffer + selectable bias, 3.3 V controls, vfbp / vfbn as pins).} 40 -780 0 0 0.35 0.35 {}
T {Not a layout cell. In the pad, vfbp = voutp = outp, vfbn = voutn = outn, and the controls come from en_ctrl_3v3. Bias: bias_sel_noab_pd (four lines).} 40 -740 0 0 0.25 0.25 {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 80 -140 0 0 0.2 0.2 {}
N 280 -700 600 -700 {lab=vdd}
N 240 -700 280 -700 {lab=vdd}
N 240 -700 240 -360 {lab=vdd}
N 600 -700 600 -600 {lab=vdd}
N 260 -100 580 -100 {lab=vss}
N 220 -100 260 -100 {lab=vss}
N 220 -180 220 -100 {lab=vss}
N 580 -360 580 -100 {lab=vss}
N 140 -420 520 -420 {lab=en_3v3}
N 140 -420 140 -280 {lab=en_3v3}
N 140 -280 180 -280 {lab=en_3v3}
N 160 -400 520 -400 {lab=en_3v3_b}
N 160 -400 160 -260 {lab=en_3v3_b}
N 160 -260 180 -260 {lab=en_3v3_b}
N 640 -360 640 -320 {lab=vbp}
N 360 -300 660 -300 {lab=vbpc}
N 660 -360 660 -300 {lab=vbpc}
N 700 -360 700 -240 {lab=vbnc}
N 720 -360 720 -220 {lab=vbn}
N 800 -520 840 -520 {lab=vfbp}
N 800 -500 840 -500 {lab=voutp}
N 800 -460 840 -460 {lab=voutn}
N 800 -440 840 -440 {lab=vfbn}
N 100 -700 240 -700 {lab=vdd}
N 100 -100 220 -100 {lab=vss}
N 100 -420 140 -420 {lab=en_3v3}
N 100 -400 160 -400 {lab=en_3v3_b}
N 360 -320 640 -320 {lab=vbp}
N 100 -320 180 -320 {lab=ibias}
N 100 -240 180 -240 {lab=sel0_3v3}
N 100 -220 180 -220 {lab=sel1_3v3}
N 360 -240 700 -240 {lab=vbnc}
N 360 -220 720 -220 {lab=vbn}
N 100 -540 520 -540 {lab=vcm}
N 100 -500 520 -500 {lab=vin}
N 100 -460 520 -460 {lab=#net1}
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
C {devices/opin.sym} 840 -500 0 0 {name=p11 lab=voutp}
C {devices/opin.sym} 840 -460 0 0 {name=p12 lab=voutn}
C {devices/ipin.sym} 840 -520 0 1 {name=p13 lab=vfbp}
C {devices/ipin.sym} 840 -440 0 1 {name=p14 lab=vfbn}
C {bias_sel_noab_pd.sym} 270 -270 0 0 {name=xb}
C {s2d_mpdda_pd.sym} 660 -480 0 0 {name=xa}
C {devices/lab_pin.sym} 640 -320 0 1 {name=l_vbp sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 660 -300 0 1 {name=l_vbpc sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 700 -240 0 1 {name=l_vbnc sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 720 -220 0 1 {name=l_vbn sig_type=std_logic lab=vbn}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
