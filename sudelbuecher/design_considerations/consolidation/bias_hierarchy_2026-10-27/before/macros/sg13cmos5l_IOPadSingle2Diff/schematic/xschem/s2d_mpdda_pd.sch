v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_mpdda_pd: s2d_mpdda with a digital enable (en_3v3: 0 ... 3.3 V on vdd / vss, active high; en_3v3_b from en_ctrl_3v3)} 0 -760 0 0 0.4 0.4 {}
T {Disabled: TPN / TPP and TNN / TNP tie voutp and voutn to vcm; the bias (d2s_bias_sel_pd) switches off every tail, sink, cascode and the CMFB diode.} 0 -710 0 0 0.25 0.25 {}
T {Enabled: the four switches are off; s2d_mpdda unchanged. vin, vref, vcm drive gates only. Source: ../../netlist/source/s2d_pd.spice} 0 -680 0 0 0.25 0.25 {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 80 -100 0 0 0.2 0.2 {}
N 620 -470 620 -360 {lab=voutp}
N 780 -430 780 -320 {lab=voutn}
N 100 -580 480 -580 {lab=en_3v3_b}
N 480 -580 720 -580 {lab=en_3v3_b}
N 480 -460 500 -460 {lab=en_3v3_b}
N 720 -460 740 -460 {lab=en_3v3_b}
N 660 -500 680 -500 {lab=en_3v3}
N 900 -500 920 -500 {lab=en_3v3}
N 540 -460 560 -460 {lab=vss}
N 780 -460 800 -460 {lab=vss}
N 600 -500 620 -500 {lab=vdd}
N 840 -500 860 -500 {lab=vdd}
N 240 -240 240 -120 {lab=vss}
N 360 -240 360 -180 {lab=vbnc}
N 300 -240 300 -220 {lab=vbp}
N 100 -120 240 -120 {lab=vss}
N 100 -160 380 -160 {lab=vbn}
N 380 -240 380 -160 {lab=vbn}
N 100 -180 360 -180 {lab=vbnc}
N 100 -200 320 -200 {lab=vbpc}
N 320 -240 320 -200 {lab=vbpc}
N 100 -220 300 -220 {lab=vbp}
N 100 -340 180 -340 {lab=vin}
N 100 -300 180 -300 {lab=vref}
N 140 -380 180 -380 {lab=vcm}
N 620 -560 780 -560 {lab=vcm}
N 780 -560 860 -560 {lab=vcm}
N 140 -560 540 -560 {lab=vcm}
N 800 -460 800 -120 {lab=vss}
N 560 -460 560 -120 {lab=vss}
N 540 -360 620 -360 {lab=voutp}
N 460 -320 780 -320 {lab=voutn}
N 860 -320 960 -320 {lab=voutn}
N 100 -380 140 -380 {lab=vcm}
N 600 -640 840 -640 {lab=vdd}
N 240 -120 560 -120 {lab=vss}
N 560 -120 800 -120 {lab=vss}
N 460 -380 960 -380 {lab=vfbp}
N 460 -300 960 -300 {lab=vfbn}
N 260 -640 600 -640 {lab=vdd}
N 480 -580 480 -460 {lab=en_3v3_b}
N 720 -580 720 -460 {lab=en_3v3_b}
N 680 -600 680 -500 {lab=en_3v3}
N 920 -600 920 -500 {lab=en_3v3}
N 680 -600 920 -600 {lab=en_3v3}
N 100 -600 680 -600 {lab=en_3v3}
N 780 -560 780 -490 {lab=vcm}
N 540 -560 540 -490 {lab=vcm}
N 140 -560 140 -380 {lab=vcm}
N 620 -360 960 -360 {lab=voutp}
N 860 -470 860 -320 {lab=voutn}
N 780 -320 860 -320 {lab=voutn}
N 860 -560 860 -530 {lab=vcm}
N 840 -640 840 -500 {lab=vdd}
N 600 -640 600 -500 {lab=vdd}
N 620 -560 620 -530 {lab=vcm}
N 540 -560 620 -560 {lab=vcm}
N 540 -430 540 -360 {lab=voutp}
N 460 -360 540 -360 {lab=voutp}
N 260 -640 260 -440 {lab=vdd}
N 100 -640 260 -640 {lab=vdd}
C {devices/iopin.sym} 100 -640 0 1 {name=p1 lab=vdd}
C {devices/ipin.sym} 100 -600 0 0 {name=p2 lab=en_3v3}
C {devices/ipin.sym} 100 -580 0 0 {name=p3 lab=en_3v3_b}
C {devices/ipin.sym} 100 -340 0 0 {name=p4 lab=vin}
C {devices/ipin.sym} 100 -300 0 0 {name=p5 lab=vref}
C {devices/ipin.sym} 100 -380 0 0 {name=p6 lab=vcm}
C {devices/ipin.sym} 960 -380 0 1 {name=p7 lab=vfbp}
C {devices/ipin.sym} 960 -300 0 1 {name=p8 lab=vfbn}
C {devices/ipin.sym} 100 -220 0 0 {name=p9 lab=vbp}
C {devices/ipin.sym} 100 -160 0 0 {name=p10 lab=vbn}
C {devices/ipin.sym} 100 -200 0 0 {name=p11 lab=vbpc}
C {devices/ipin.sym} 100 -180 0 0 {name=p12 lab=vbnc}
C {devices/iopin.sym} 100 -120 0 1 {name=p13 lab=vss}
C {devices/opin.sym} 960 -360 0 0 {name=p14 lab=voutp}
C {devices/opin.sym} 960 -320 0 0 {name=p15 lab=voutn}
C {s2d_mpdda.sym} 320 -340 0 0 {name=xs}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 520 -460 0 0 {name=TPN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 640 -500 0 1 {name=TPP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 760 -460 0 0 {name=TNN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 880 -500 0 1 {name=TNP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
