v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_mpdda_pd: s2d_mpdda with a digital enable (en_3v3: 0 ... 3.3 V on vdd / vss, active high; en_3v3_b from en_ctrl_3v3)} 80 -1000 0 0 0.4 0.4 {}
T {Disabled: TPN / TPP and TNN / TNP tie voutp and voutn to vcm; the bias (d2s_bias_sel_pd) switches off every tail, sink, cascode and the CMFB diode.} 80 -950 0 0 0.25 0.25 {}
T {Enabled: the four switches are off; s2d_mpdda unchanged. vin, vref, vcm drive gates only. Source: ../../netlist/source/s2d_pd.spice} 80 -920 0 0 0.25 0.25 {}
C {devices/iopin.sym} 100 -860 0 1 {name=p1 lab=vdd}
C {devices/ipin.sym} 100 -820 0 0 {name=p2 lab=en_3v3}
C {devices/ipin.sym} 100 -800 0 0 {name=p3 lab=en_3v3_b}
C {devices/ipin.sym} 100 -620 0 0 {name=p4 lab=vin}
C {devices/ipin.sym} 100 -580 0 0 {name=p5 lab=vref}
C {devices/ipin.sym} 100 -540 0 0 {name=p6 lab=vcm}
C {devices/ipin.sym} 100 -500 0 0 {name=p7 lab=vfbp}
C {devices/ipin.sym} 100 -460 0 0 {name=p8 lab=vfbn}
C {devices/ipin.sym} 100 -300 0 0 {name=p9 lab=vbp}
C {devices/ipin.sym} 100 -280 0 0 {name=p10 lab=vbn}
C {devices/ipin.sym} 100 -260 0 0 {name=p11 lab=vbpc}
C {devices/ipin.sym} 100 -240 0 0 {name=p12 lab=vbnc}
C {devices/iopin.sym} 100 -160 0 1 {name=p13 lab=vss}
C {devices/opin.sym} 1240 -620 0 0 {name=p14 lab=voutp}
C {devices/opin.sym} 1240 -580 0 0 {name=p15 lab=voutn}
C {s2d_mpdda.sym} 500 -540 0 0 {name=xs}
N 100 -620 320 -620 {lab=vin}
N 100 -580 320 -580 {lab=vref}
N 100 -500 320 -500 {lab=vfbp}
N 100 -460 320 -460 {lab=vfbn}
N 100 -540 260 -540 {lab=vcm}
N 260 -540 320 -540 {lab=vcm}
N 100 -860 380 -860 {lab=vdd}
N 380 -860 1160 -860 {lab=vdd}
N 380 -860 380 -680 {lab=vdd}
N 100 -160 380 -160 {lab=vss}
N 380 -160 1040 -160 {lab=vss}
N 380 -400 380 -160 {lab=vss}
N 420 -400 420 -300 {lab=vbp}
N 420 -300 100 -300 {lab=vbp}
N 460 -400 460 -280 {lab=vbn}
N 460 -280 100 -280 {lab=vbn}
N 500 -400 500 -260 {lab=vbpc}
N 500 -260 100 -260 {lab=vbpc}
N 540 -400 540 -240 {lab=vbnc}
N 540 -240 100 -240 {lab=vbnc}
N 680 -620 780 -620 {lab=voutp}
N 780 -620 900 -620 {lab=voutp}
N 900 -620 1240 -620 {lab=voutp}
N 680 -580 1020 -580 {lab=voutn}
N 1020 -580 1140 -580 {lab=voutn}
N 1140 -580 1240 -580 {lab=voutn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 760 -720 0 0 {name=TPN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 880 -720 0 0 {name=TPP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1000 -720 0 0 {name=TNN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1120 -720 0 0 {name=TNP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 780 -690 780 -620 {lab=voutp}
N 780 -750 780 -780 {lab=vcm}
N 900 -690 900 -620 {lab=voutp}
N 900 -750 900 -780 {lab=vcm}
N 1020 -690 1020 -580 {lab=voutn}
N 1020 -750 1020 -780 {lab=vcm}
N 1140 -690 1140 -580 {lab=voutn}
N 1140 -750 1140 -780 {lab=vcm}
N 260 -540 260 -780 {lab=vcm}
N 260 -780 780 -780 {lab=vcm}
N 780 -780 900 -780 {lab=vcm}
N 900 -780 1020 -780 {lab=vcm}
N 1020 -780 1140 -780 {lab=vcm}
N 100 -800 720 -800 {lab=en_3v3_b}
N 720 -800 960 -800 {lab=en_3v3_b}
N 720 -800 720 -720 {lab=en_3v3_b}
N 720 -720 740 -720 {lab=en_3v3_b}
N 960 -800 960 -720 {lab=en_3v3_b}
N 960 -720 980 -720 {lab=en_3v3_b}
N 100 -820 840 -820 {lab=en_3v3}
N 840 -820 1080 -820 {lab=en_3v3}
N 840 -820 840 -720 {lab=en_3v3}
N 840 -720 860 -720 {lab=en_3v3}
N 1080 -820 1080 -720 {lab=en_3v3}
N 1080 -720 1100 -720 {lab=en_3v3}
N 780 -720 800 -720 {lab=vss}
N 800 -720 800 -160 {lab=vss}
N 1020 -720 1040 -720 {lab=vss}
N 1040 -720 1040 -160 {lab=vss}
N 900 -720 920 -720 {lab=vdd}
N 920 -720 920 -860 {lab=vdd}
N 1140 -720 1160 -720 {lab=vdd}
N 1160 -720 1160 -860 {lab=vdd}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 80 -100 0 0 0.2 0.2 {}
