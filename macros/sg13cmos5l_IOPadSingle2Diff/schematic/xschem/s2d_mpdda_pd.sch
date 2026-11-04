v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_mpdda_pd: s2d_mpdda with a digital enable (en_3v3: 0 ... 3.3 V on vdd / vss, active high; en_3v3_b from en_ctrl_3v3)} 0 -760 0 0 0.4 0.4 {}
T {Disabled: TPN / TPP and TNN / TNP tie voutp and voutn to vcm; the bias (bias_sel_pd) switches off every tail, sink, cascode and the CMFB diode.} 0 -710 0 0 0.25 0.25 {}
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
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1360 -620 0 0 {name=MDT[3:0]
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1380 -650 1400 -650 {lab=vdd}
N 1380 -620 1400 -620 {lab=vdd}
N 1380 -590 1400 -590 {lab=vdd}
N 1400 -590 1400 -680 {lab=vdd}
C {devices/lab_pin.sym} 1400 -680 0 1 {name=ldm0_r sig_type=std_logic lab=vdd}
N 1340 -620 1300 -620 {lab=vdd}
C {devices/lab_pin.sym} 1300 -620 0 0 {name=ldm0_g sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1360 -480 0 0 {name=MDTL[2:0]
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1380 -510 1400 -510 {lab=vdd}
N 1380 -480 1400 -480 {lab=vdd}
N 1380 -450 1400 -450 {lab=vdd}
N 1400 -450 1400 -540 {lab=vdd}
C {devices/lab_pin.sym} 1400 -540 0 1 {name=ldm1_r sig_type=std_logic lab=vdd}
N 1340 -480 1300 -480 {lab=vbp}
C {devices/lab_pin.sym} 1300 -480 0 0 {name=ldm1_g sig_type=std_logic lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1360 -340 0 0 {name=MDPC[2:0]
l=4u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1380 -370 1400 -370 {lab=vdd}
N 1380 -340 1400 -340 {lab=vdd}
N 1380 -310 1400 -310 {lab=vdd}
N 1400 -310 1400 -400 {lab=vdd}
C {devices/lab_pin.sym} 1400 -400 0 1 {name=ldm2_r sig_type=std_logic lab=vdd}
N 1340 -340 1300 -340 {lab=vbpc}
C {devices/lab_pin.sym} 1300 -340 0 0 {name=ldm2_g sig_type=std_logic lab=vbpc}
C {sg13cmos5l_pr/rhigh.sym} 1360 -200 0 0 {name=RD[1:0]
w=0.5u
l=12.65u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
N 1360 -230 1360 -250 {lab=vss}
C {devices/lab_pin.sym} 1360 -250 0 1 {name=ldm_r0 sig_type=std_logic lab=vss}
N 1360 -170 1360 -150 {lab=vss}
C {devices/lab_pin.sym} 1360 -150 0 1 {name=ldm_r1 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1680 -620 0 0 {name=MDSK[3:0]
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1700 -650 1720 -650 {lab=vss}
N 1700 -620 1720 -620 {lab=vss}
N 1700 -590 1720 -590 {lab=vss}
N 1720 -650 1720 -560 {lab=vss}
C {devices/lab_pin.sym} 1720 -560 0 1 {name=ldm3_r sig_type=std_logic lab=vss}
N 1660 -620 1620 -620 {lab=vbn}
C {devices/lab_pin.sym} 1620 -620 0 0 {name=ldm3_g sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1680 -480 0 0 {name=MDBNT
l=6u
w=6u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1700 -510 1720 -510 {lab=vss}
N 1700 -480 1720 -480 {lab=vss}
N 1700 -450 1720 -450 {lab=vss}
N 1720 -510 1720 -420 {lab=vss}
C {devices/lab_pin.sym} 1720 -420 0 1 {name=ldm4_r sig_type=std_logic lab=vss}
N 1660 -480 1620 -480 {lab=vbn}
C {devices/lab_pin.sym} 1620 -480 0 0 {name=ldm4_g sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1680 -340 0 0 {name=MDSC[3:0]
l=6u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1700 -370 1720 -370 {lab=vss}
N 1700 -340 1720 -340 {lab=vss}
N 1700 -310 1720 -310 {lab=vss}
N 1720 -370 1720 -280 {lab=vss}
C {devices/lab_pin.sym} 1720 -280 0 1 {name=ldm5_r sig_type=std_logic lab=vss}
N 1660 -340 1620 -340 {lab=vbn}
C {devices/lab_pin.sym} 1620 -340 0 0 {name=ldm5_g sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1680 -200 0 0 {name=MDCN[3:0]
l=3u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1700 -230 1720 -230 {lab=vss}
N 1700 -200 1720 -200 {lab=vss}
N 1700 -170 1720 -170 {lab=vss}
N 1720 -230 1720 -140 {lab=vss}
C {devices/lab_pin.sym} 1720 -140 0 1 {name=ldm6_r sig_type=std_logic lab=vss}
N 1660 -200 1620 -200 {lab=vbnc}
C {devices/lab_pin.sym} 1620 -200 0 0 {name=ldm6_g sig_type=std_logic lab=vbnc}
P 10 5 1260 -720 1840 -720 1840 -110 1260 -110 1260 -720 {dash=6}
T {[DM]} 1265 -745 0 0 0.35 0.35 {layer=10}
T {[DM] dummies of the s2d layout cells, as drawn (pad_candidate.cdl, C3 2026-11-04); every one a device, D = S on the rail} 1260 -880 0 0 0.25 0.25 {layer=10}
T {PMOS (D = S = B = vdd): MDT inputs (4 tubs 20u / 1u ng 2, gate vdd), MDTL tails (gate vbp), MDPC casc_p (gate vbpc); loads MDL: in s2d_mpdda (gate vcmfb)} 1260 -856 0 0 0.25 0.25 {layer=10}
T {NMOS (D = S = B = vss): MDSK sinks + MDBNT the twin of BN, MDSC sinks_cmfb (gate vbn), MDCN casc_n (gate vbnc); RD: the 2 dummy rhigh strips (vss)} 1260 -832 0 0 0.25 0.25 {layer=10}
T {BP / BN / BPC / BNC are drawn in the s2d cells but stay in bias_tree_noab_pd (same flat netlist).} 1260 -808 0 0 0.25 0.25 {layer=10}
