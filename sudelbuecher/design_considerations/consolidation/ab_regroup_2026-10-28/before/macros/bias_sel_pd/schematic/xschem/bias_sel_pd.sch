v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {bias_sel_pd: pad-driver bias with a selectable reference current into one mirror tree} 0 -980 0 0 0.4 0.4 {}
T {sel1 sel0 = 0 0: harness ibias (sourced, ~5 uA = iDAC code 20 at 250 nA/step) through TEN / TEP;  0 1: Oguey-Aebischer core;} 60 -150 0 0 0.25 0.25 {}
T {1 0: bandgap core;  1 1: both cores (currents add). en_3v3 = 0: everything off (tree TG and TDN, both cores, TEN / TEP open); en_3v3_b = NOT en_3v3, from en_ctrl_3v3.} 60 -126 0 0 0.25 0.25 {}
T {A disabled core output (POC drain) is off, so the cores share the tree input ir without a switch. Source: netlist/source/bias_sel_pd.spice} 60 -102 0 0 0.25 0.25 {}
N 1220 -540 1220 -180 {lab=vss}
N 1260 -540 1260 -160 {lab=vsso}
N 1380 -680 1400 -680 {lab=vbp}
N 1380 -580 1400 -580 {lab=vbn}
N 1380 -660 1400 -660 {lab=vbpc}
N 1380 -600 1400 -600 {lab=vbnc}
N 1380 -640 1400 -640 {lab=vabp}
N 1380 -620 1400 -620 {lab=vabn}
N 1160 -660 1180 -660 {lab=en_3v3}
N 1140 -640 1180 -640 {lab=en_3v3_b}
N 60 -820 1140 -820 {lab=en_3v3_b}
N 520 -670 520 -180 {lab=vss}
N 620 -700 660 -700 {lab=en_oa_b}
N 740 -700 840 -700 {lab=en_oa}
N 620 -540 660 -540 {lab=en_bg_b}
N 740 -540 840 -540 {lab=en_bg}
N 280 -330 280 -180 {lab=vss}
N 200 -380 220 -380 {lab=sel0_3v3}
N 340 -360 460 -360 {lab=s00}
N 620 -380 660 -380 {lab=en_ext_b}
N 740 -380 960 -380 {lab=en_ext}
N 900 -620 900 -180 {lab=vss}
N 960 -680 1060 -680 {lab=ir}
N 960 -520 1060 -520 {lab=ir}
N 990 -320 1060 -320 {lab=ir}
N 960 -380 960 -360 {lab=en_ext}
N 920 -320 930 -320 {lab=ibias}
N 960 -320 960 -180 {lab=vss}
N 1020 -240 1020 -220 {lab=en_ext_b}
N 380 -840 1160 -840 {lab=en_3v3}
N 1160 -840 1160 -660 {lab=en_3v3}
N 380 -560 380 -400 {lab=en_3v3}
N 60 -840 380 -840 {lab=en_3v3}
N 380 -400 460 -400 {lab=en_3v3}
N 380 -560 460 -560 {lab=en_3v3}
N 380 -720 380 -560 {lab=en_3v3}
N 380 -720 460 -720 {lab=en_3v3}
N 380 -840 380 -720 {lab=en_3v3}
N 180 -520 460 -520 {lab=sel1_3v3}
N 200 -680 460 -680 {lab=sel0_3v3}
N 200 -680 200 -380 {lab=sel0_3v3}
N 60 -680 200 -680 {lab=sel0_3v3}
N 180 -340 220 -340 {lab=sel1_3v3}
N 180 -520 180 -340 {lab=sel1_3v3}
N 60 -520 180 -520 {lab=sel1_3v3}
N 580 -700 620 -700 {lab=en_oa_b}
N 620 -660 840 -660 {lab=en_oa_b}
N 520 -180 700 -180 {lab=vss}
N 620 -700 620 -660 {lab=en_oa_b}
N 540 -920 720 -920 {lab=vdd}
N 720 -920 720 -400 {lab=vdd}
N 620 -540 620 -500 {lab=en_bg_b}
N 580 -540 620 -540 {lab=en_bg_b}
N 620 -500 840 -500 {lab=en_bg_b}
N 920 -320 920 -280 {lab=ibias}
N 920 -280 990 -280 {lab=ibias}
N 1050 -280 1060 -280 {lab=ir}
N 1060 -320 1060 -280 {lab=ir}
N 700 -680 700 -180 {lab=vss}
N 620 -380 620 -220 {lab=en_ext_b}
N 620 -220 1020 -220 {lab=en_ext_b}
N 900 -180 960 -180 {lab=vss}
N 60 -280 920 -280 {lab=ibias}
N 920 -920 1020 -920 {lab=vdd}
N 1020 -920 1020 -280 {lab=vdd}
N 700 -180 900 -180 {lab=vss}
N 1060 -520 1060 -320 {lab=ir}
N 1060 -680 1180 -680 {lab=ir}
N 1060 -680 1060 -520 {lab=ir}
N 920 -920 920 -580 {lab=vdd}
N 720 -920 920 -920 {lab=vdd}
N 1020 -920 1240 -920 {lab=vdd}
N 1240 -920 1240 -720 {lab=vdd}
N 1280 -940 1280 -720 {lab=vddo}
N 60 -940 1280 -940 {lab=vddo}
N 580 -380 620 -380 {lab=en_ext_b}
N 60 -180 280 -180 {lab=vss}
N 280 -180 520 -180 {lab=vss}
N 300 -920 300 -390 {lab=vdd}
N 60 -920 300 -920 {lab=vdd}
N 540 -920 540 -410 {lab=vdd}
N 300 -920 540 -920 {lab=vdd}
N 960 -180 1220 -180 {lab=vss}
N 60 -160 1260 -160 {lab=vsso}
N 1140 -820 1140 -640 {}
C {devices/iopin.sym} 60 -920 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 60 -180 0 1 {name=p1 lab=vss}
C {devices/iopin.sym} 60 -940 0 1 {name=p2 lab=vddo}
C {devices/iopin.sym} 60 -160 0 1 {name=p3 lab=vsso}
C {devices/iopin.sym} 60 -280 0 1 {name=p4 lab=ibias}
C {devices/opin.sym} 1400 -680 0 0 {name=p5 lab=vbp}
C {devices/opin.sym} 1400 -580 0 0 {name=p6 lab=vbn}
C {devices/opin.sym} 1400 -660 0 0 {name=p7 lab=vbpc}
C {devices/opin.sym} 1400 -600 0 0 {name=p8 lab=vbnc}
C {devices/opin.sym} 1400 -640 0 0 {name=p9 lab=vabp}
C {devices/opin.sym} 1400 -620 0 0 {name=p10 lab=vabn}
C {devices/ipin.sym} 60 -840 0 0 {name=p11 lab=en_3v3}
C {devices/ipin.sym} 60 -680 0 0 {name=p12 lab=sel0_3v3}
C {devices/ipin.sym} 60 -520 0 0 {name=p13 lab=sel1_3v3}
C {devices/ipin.sym} 60 -820 0 0 {name=p14 lab=en_3v3_b}
C {bias_tree_pd.sym} 1280 -630 0 0 {name=Xt}
C {devices/lab_pin.sym} 1240 -740 0 1 {name=l5 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1220 -520 0 1 {name=l6 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1280 -740 0 1 {name=l7 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 1260 -520 0 1 {name=l8 sig_type=std_logic lab=vsso}
C {nand2_hv.sym} 520 -700 0 0 {name=XDA}
C {devices/lab_pin.sym} 540 -750 0 1 {name=l18 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 520 -650 0 1 {name=l19 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 600 -700 0 1 {name=l22 sig_type=std_logic lab=en_oa_b}
C {inv_hv.sym} 700 -700 0 0 {name=XDB}
C {nand2_hv.sym} 520 -540 0 0 {name=XDC}
C {devices/lab_pin.sym} 540 -590 0 1 {name=l27 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 520 -490 0 1 {name=l28 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 600 -540 0 1 {name=l31 sig_type=std_logic lab=en_bg_b}
C {inv_hv.sym} 700 -540 0 0 {name=XDD}
C {nor2_hv.sym} 280 -360 0 0 {name=XDE}
C {devices/lab_pin.sym} 300 -410 0 1 {name=l36 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 280 -310 0 1 {name=l37 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 200 -380 0 0 {name=l38 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_pin.sym} 180 -340 0 0 {name=l39 sig_type=std_logic lab=sel1_3v3}
C {devices/lab_pin.sym} 360 -360 0 1 {name=l40 sig_type=std_logic lab=s00}
C {nand2_hv.sym} 520 -380 0 0 {name=XDF}
C {devices/lab_pin.sym} 540 -430 0 1 {name=l41 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 520 -330 0 1 {name=l42 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 590 -380 0 1 {name=l45 sig_type=std_logic lab=en_ext_b}
C {inv_hv.sym} 700 -380 0 0 {name=XDG}
C {devices/lab_pin.sym} 720 -420 0 1 {name=l46 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 960 -380 0 1 {name=l49 sig_type=std_logic lab=en_ext}
C {oa_core_pd.sym} 900 -680 0 0 {name=Xoa}
C {devices/lab_pin.sym} 900 -610 0 0 {name=l51 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1060 -680 3 1 {name=l52 sig_type=std_logic lab=ir}
C {devices/lab_pin.sym} 820 -700 0 0 {name=l53 sig_type=std_logic lab=en_oa}
C {devices/lab_pin.sym} 820 -660 0 0 {name=l54 sig_type=std_logic lab=en_oa_b}
C {bg_core_pd.sym} 900 -520 0 0 {name=Xbg}
C {devices/lab_pin.sym} 920 -590 0 1 {name=l55 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1060 -520 0 1 {name=l57 sig_type=std_logic lab=ir}
C {devices/lab_pin.sym} 820 -540 0 0 {name=l58 sig_type=std_logic lab=en_bg}
C {devices/lab_pin.sym} 820 -500 0 0 {name=l59 sig_type=std_logic lab=en_bg_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 960 -340 1 0 {name=TEN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1060 -320 2 0 {name=l62 sig_type=std_logic lab=ir}
C {devices/lab_pin.sym} 960 -260 2 1 {name=l63 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1020 -260 3 0 {name=TEP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 1020 -220 0 1 {name=l65 sig_type=std_logic lab=en_ext_b}
C {devices/lab_pin.sym} 1020 -340 0 1 {name=l67 sig_type=std_logic lab=vdd}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
