v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {d2s_mpdda_pd_sel: CACE fixture for the loop gain of sg13cmos5l_IOPadDiff2Single (driver + selectable bias, 3.3 V controls, vfb as a pin).} 0 -800 0 0 0.35 0.35 {}
T {Not a layout cell. In the pad, vfb = vout = pad and the controls come from en_ctrl_3v3. Output stage as in the pad (d2s_out_p, d2s_out_n, CMA, CMB; since 2026-10-28). Bias as in the pad: bias_gen_pd + bias_tree_pd (one bias_sel_pd until 2026-10-28).} 0 -760 0 0 0.25 0.25 {}
N 100 -120 600 -120 {lab=vss}
N 100 -100 640 -100 {lab=vsso}
N 1100 -320 1100 -100 {lab=vsso}
N 640 -100 1100 -100 {lab=vsso}
N 880 -320 880 -120 {lab=vss}
N 600 -120 880 -120 {lab=vss}
N 940 -320 940 -280 {lab=vbp}
N 740 -280 940 -280 {lab=vbp}
N 960 -320 960 -260 {lab=vbpc}
N 740 -260 960 -260 {lab=vbpc}
N 980 -320 980 -240 {lab=vabp}
N 740 -240 980 -240 {lab=vabp}
N 1020 -320 1020 -220 {lab=vabn}
N 740 -220 1020 -220 {lab=vabn}
N 1040 -320 1040 -200 {lab=vbnc}
N 740 -200 1040 -200 {lab=vbnc}
N 1060 -320 1060 -180 {lab=vbn}
N 740 -180 1060 -180 {lab=vbn}
N 140 -480 820 -480 {lab=en_3v3}
N 660 -560 1120 -560 {lab=vddo}
N 1120 -560 1120 -520 {lab=vddo}
N 620 -540 900 -540 {lab=vdd}
N 900 -540 900 -520 {lab=vdd}
N 100 -440 820 -440 {lab=vinp}
N 100 -420 820 -420 {lab=vinn}
N 100 -380 820 -380 {lab=vref}
N 100 -540 620 -540 {lab=vdd}
N 100 -560 660 -560 {lab=vddo}
N 100 -480 140 -480 {lab=en_3v3}
N 100 -460 120 -460 {lab=en_3v3_b}
N 120 -460 820 -460 {lab=en_3v3_b}
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
C {devices/lab_pin.sym} 940 -280 0 1 {name=l5 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1060 -180 0 1 {name=l6 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 960 -260 0 1 {name=l7 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 1040 -200 0 1 {name=l8 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 980 -240 0 1 {name=l9 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 1020 -220 0 1 {name=l10 sig_type=std_logic lab=vabn}
C {d2s_mpdda_pd.sym} 1000 -420 0 0 {name=xd}
C {devices/lab_pin.sym} 900 -520 0 0 {name=l14 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 880 -320 0 0 {name=l15 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1120 -520 0 1 {name=l16 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 1100 -320 0 1 {name=l17 sig_type=std_logic lab=vsso}
C {devices/title.sym} 560 -40 0 0 {name=l_title author="Christoph Maier"}
C {d2s_out_p.sym} 1500 -600 0 0 {name=xfp}
C {d2s_out_n.sym} 1500 -260 0 0 {name=xfn}
N 1180 -480 1260 -480 {lab=dabp}
N 1260 -480 1260 -620 {lab=dabp}
N 1260 -620 1420 -620 {lab=dabp}
N 1180 -460 1280 -460 {lab=a}
N 1280 -460 1280 -600 {lab=a}
N 1280 -600 1320 -600 {lab=a}
N 1320 -600 1420 -600 {lab=a}
N 1320 -600 1320 -520 {lab=a}
N 1320 -520 1660 -520 {lab=a}
N 1180 -380 1280 -380 {lab=b}
N 1280 -380 1280 -260 {lab=b}
N 1280 -260 1320 -260 {lab=b}
N 1320 -260 1420 -260 {lab=b}
N 1320 -260 1320 -340 {lab=b}
N 1320 -340 1660 -340 {lab=b}
N 1180 -360 1260 -360 {lab=dabn}
N 1260 -360 1260 -240 {lab=dabn}
N 1260 -240 1420 -240 {lab=dabn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1680 -520 0 0 {name=CMA
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1700 -550 1700 -520 {lab=vout}
N 1700 -520 1700 -490 {lab=vout}
N 1700 -520 1760 -520 {lab=vout}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1680 -340 0 1 {name=CMB
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1660 -370 1660 -340 {lab=b}
N 1660 -340 1660 -310 {lab=b}
N 1700 -340 1760 -340 {lab=vout}
N 1580 -600 1760 -600 {lab=vout}
N 1580 -260 1760 -260 {lab=vout}
N 1500 -660 1500 -680 {lab=vddo}
C {devices/lab_pin.sym} 1500 -680 0 0 {name=xlrp sig_type=std_logic lab=vddo}
N 1500 -200 1500 -180 {lab=vsso}
C {devices/lab_pin.sym} 1500 -180 0 0 {name=xlrn sig_type=std_logic lab=vsso}
N 1760 -440 1880 -440 {lab=vout}
C {devices/iopin.sym} 1880 -440 0 0 {name=p8 lab=vout}
N 1760 -600 1760 -520 {lab=vout}
N 1760 -520 1760 -440 {lab=vout}
N 1760 -440 1760 -340 {lab=vout}
N 1760 -340 1760 -260 {lab=vout}
N 1180 -420 1200 -420 {lab=vfb}
C {devices/ipin.sym} 1200 -420 0 1 {name=p9 lab=vfb}
C {bias_gen_pd.sym} 300 -250 0 0 {name=xg}
C {bias_tree_pd.sym} 640 -230 0 0 {name=xt}
N 100 -280 210 -280 {lab=ibias}
N 140 -480 140 -260 {lab=en_3v3}
N 140 -260 210 -260 {lab=en_3v3}
N 100 -200 160 -200 {lab=sel0_3v3}
N 160 -240 160 -200 {lab=sel0_3v3}
N 160 -240 210 -240 {lab=sel0_3v3}
N 100 -180 180 -180 {lab=sel1_3v3}
N 180 -220 180 -180 {lab=sel1_3v3}
N 180 -220 210 -220 {lab=sel1_3v3}
N 390 -250 410 -250 {lab=iref}
N 410 -280 410 -250 {lab=iref}
N 410 -280 540 -280 {lab=iref}
C {devices/lab_wire.sym} 410 -280 0 1 {name=l_iref sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 540 -260 0 0 {name=l_xt_en sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 540 -240 0 0 {name=l_xt_enb sig_type=std_logic lab=en_3v3_b}
N 600 -540 600 -320 {lab=vdd}
N 580 -140 580 -120 {lab=vss}
C {devices/lab_pin.sym} 300 -330 0 1 {name=l_xg_vdd sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 300 -170 0 1 {name=l_xg_vss sig_type=std_logic lab=vss}
