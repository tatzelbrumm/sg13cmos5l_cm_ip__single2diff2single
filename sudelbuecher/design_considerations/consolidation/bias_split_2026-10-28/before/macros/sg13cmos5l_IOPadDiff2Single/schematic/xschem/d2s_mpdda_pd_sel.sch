v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {d2s_mpdda_pd_sel: CACE fixture for the loop gain of sg13cmos5l_IOPadDiff2Single (driver + selectable bias, 3.3 V controls, vfb as a pin).} 0 -800 0 0 0.35 0.35 {}
T {Not a layout cell. In the pad, vfb = vout = pad and the controls come from en_ctrl_3v3. Output stage as in the pad (d2s_out_p, d2s_out_n, CMA, CMB; since 2026-10-28).} 0 -760 0 0 0.25 0.25 {}
N 200 -140 200 -120 {lab=vss}
N 100 -120 200 -120 {lab=vss}
N 100 -100 240 -100 {lab=vsso}
N 100 -180 160 -180 {lab=sel1_3v3}
N 100 -200 160 -200 {lab=sel0_3v3}
N 700 -320 700 -100 {lab=vsso}
N 240 -100 700 -100 {lab=vsso}
N 480 -320 480 -120 {lab=vss}
N 200 -120 480 -120 {lab=vss}
N 540 -320 540 -280 {lab=vbp}
N 340 -280 540 -280 {lab=vbp}
N 560 -320 560 -260 {lab=vbpc}
N 340 -260 560 -260 {lab=vbpc}
N 580 -320 580 -240 {lab=vabp}
N 340 -240 580 -240 {lab=vabp}
N 620 -320 620 -220 {lab=vabn}
N 340 -220 620 -220 {lab=vabn}
N 640 -320 640 -200 {lab=vbnc}
N 340 -200 640 -200 {lab=vbnc}
N 660 -320 660 -180 {lab=vbn}
N 340 -180 660 -180 {lab=vbn}
N 140 -480 420 -480 {lab=en_3v3}
N 100 -280 160 -280 {lab=ibias}
N 260 -560 720 -560 {lab=vddo}
N 720 -560 720 -520 {lab=vddo}
N 220 -540 500 -540 {lab=vdd}
N 500 -540 500 -520 {lab=vdd}
N 100 -440 420 -440 {lab=vinp}
N 100 -420 420 -420 {lab=vinn}
N 100 -380 420 -380 {lab=vref}
N 220 -540 220 -320 {lab=vdd}
N 100 -540 220 -540 {lab=vdd}
N 100 -560 260 -560 {lab=vddo}
N 140 -480 140 -240 {lab=en_3v3}
N 100 -480 140 -480 {lab=en_3v3}
N 140 -240 160 -240 {lab=en_3v3}
N 100 -460 120 -460 {lab=en_3v3_b}
N 120 -460 420 -460 {lab=en_3v3_b}
N 120 -220 160 -220 {lab=en_3v3_b}
N 120 -460 120 -220 {}
C {devices/iopin.sym} 100 -540 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 100 -120 0 1 {name=p2 lab=vss}
C {devices/iopin.sym} 100 -560 0 1 {name=p3 lab=vddo}
C {devices/iopin.sym} 100 -100 0 1 {name=p4 lab=vsso}
C {devices/ipin.sym} 100 -440 0 0 {name=p5 lab=vinp}
C {devices/ipin.sym} 100 -420 0 0 {name=p6 lab=vinn}
C {devices/ipin.sym} 100 -380 0 0 {name=p7 lab=vref}
C {devices/ipin.sym} 100 -280 0 0 {name=p10 lab=ibias}
C {devices/ipin.sym} 100 -480 0 0 {name=p11 lab=en_3v3}
C {devices/ipin.sym} 100 -200 0 0 {name=p12 lab=sel0_3v3}
C {devices/ipin.sym} 100 -180 0 0 {name=p13 lab=sel1_3v3}
C {devices/ipin.sym} 100 -460 0 0 {name=p14 lab=en_3v3_b}
C {bias_sel_pd.sym} 250 -230 0 0 {name=xb}
C {devices/lab_pin.sym} 220 -320 0 0 {name=l0 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 200 -140 0 0 {name=l1 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 540 -280 0 1 {name=l5 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 660 -180 0 1 {name=l6 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 560 -260 0 1 {name=l7 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 640 -200 0 1 {name=l8 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 580 -240 0 1 {name=l9 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 620 -220 0 1 {name=l10 sig_type=std_logic lab=vabn}
C {d2s_mpdda_pd.sym} 600 -420 0 0 {name=xd}
C {devices/lab_pin.sym} 500 -520 0 0 {name=l14 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 480 -320 0 0 {name=l15 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 720 -520 0 1 {name=l16 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 700 -320 0 1 {name=l17 sig_type=std_logic lab=vsso}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
C {d2s_out_p.sym} 1100 -600 0 0 {name=xfp}
C {d2s_out_n.sym} 1100 -260 0 0 {name=xfn}
N 780 -480 860 -480 {lab=dabp}
N 860 -480 860 -620 {lab=dabp}
N 860 -620 1020 -620 {lab=dabp}
N 780 -460 880 -460 {lab=a}
N 880 -460 880 -600 {lab=a}
N 880 -600 920 -600 {lab=a}
N 920 -600 1020 -600 {lab=a}
N 920 -600 920 -520 {lab=a}
N 920 -520 1260 -520 {lab=a}
N 780 -380 880 -380 {lab=b}
N 880 -380 880 -260 {lab=b}
N 880 -260 920 -260 {lab=b}
N 920 -260 1020 -260 {lab=b}
N 920 -260 920 -340 {lab=b}
N 920 -340 1260 -340 {lab=b}
N 780 -360 860 -360 {lab=dabn}
N 860 -360 860 -240 {lab=dabn}
N 860 -240 1020 -240 {lab=dabn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1280 -520 0 0 {name=CMA
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1300 -550 1300 -520 {lab=vout}
N 1300 -520 1300 -490 {lab=vout}
N 1300 -520 1360 -520 {lab=vout}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1280 -340 0 1 {name=CMB
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1260 -370 1260 -340 {lab=b}
N 1260 -340 1260 -310 {lab=b}
N 1300 -340 1360 -340 {lab=vout}
N 1180 -600 1360 -600 {lab=vout}
N 1180 -260 1360 -260 {lab=vout}
N 1100 -660 1100 -680 {lab=vddo}
C {devices/lab_pin.sym} 1100 -680 0 0 {name=xlrp sig_type=std_logic lab=vddo}
N 1100 -200 1100 -180 {lab=vsso}
C {devices/lab_pin.sym} 1100 -180 0 0 {name=xlrn sig_type=std_logic lab=vsso}
N 1360 -440 1480 -440 {lab=vout}
C {devices/iopin.sym} 1480 -440 0 0 {name=p8 lab=vout}
N 1360 -600 1360 -520 {lab=vout}
N 1360 -520 1360 -440 {lab=vout}
N 1360 -440 1360 -340 {lab=vout}
N 1360 -340 1360 -260 {lab=vout}
N 780 -420 800 -420 {lab=vfb}
C {devices/ipin.sym} 800 -420 0 1 {name=p9 lab=vfb}
