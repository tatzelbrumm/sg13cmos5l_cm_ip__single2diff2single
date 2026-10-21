v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {d2s_bias_sel_pd: pad-driver bias with a selectable reference current into one mirror tree} 0 -60 0 0 0.4 0.4 {}
C {devices/iopin.sym} 40 40 0 0 {name=p0 lab=vdd}
C {devices/iopin.sym} 40 70 0 0 {name=p1 lab=vss}
C {devices/iopin.sym} 40 100 0 0 {name=p2 lab=vddo}
C {devices/iopin.sym} 40 130 0 0 {name=p3 lab=vsso}
C {devices/iopin.sym} 40 160 0 0 {name=p4 lab=ibias}
C {devices/opin.sym} 40 190 0 0 {name=p5 lab=vbp}
C {devices/opin.sym} 40 220 0 0 {name=p6 lab=vbn}
C {devices/opin.sym} 40 250 0 0 {name=p7 lab=vbpc}
C {devices/opin.sym} 40 280 0 0 {name=p8 lab=vbnc}
C {devices/opin.sym} 40 310 0 0 {name=p9 lab=vabp}
C {devices/opin.sym} 40 340 0 0 {name=p10 lab=vabn}
C {devices/ipin.sym} 40 370 0 0 {name=p11 lab=en_3v3}
C {devices/ipin.sym} 40 400 0 0 {name=p12 lab=sel0_3v3}
C {devices/ipin.sym} 40 430 0 0 {name=p13 lab=sel1_3v3}
C {inv_3v3_pd.sym} 300 80 0 0 {name=Xi}
N 280 40 280 20 {lab=vdd}
C {devices/lab_pin.sym} 280 20 0 1 {name=l1 sig_type=std_logic lab=vdd}
N 280 120 280 140 {lab=vss}
C {devices/lab_pin.sym} 280 140 0 1 {name=l2 sig_type=std_logic lab=vss}
N 240 80 220 80 {lab=en_3v3}
C {devices/lab_pin.sym} 220 80 0 0 {name=l3 sig_type=std_logic lab=en_3v3}
N 360 80 380 80 {lab=en_3v3_b}
C {devices/lab_pin.sym} 380 80 0 1 {name=l4 sig_type=std_logic lab=en_3v3_b}
C {d2s_bias_in_tree_pd.sym} 1100 300 0 0 {name=Xt}
N 1040 210 1040 190 {lab=vdd}
C {devices/lab_pin.sym} 1040 190 0 1 {name=l5 sig_type=std_logic lab=vdd}
N 1040 390 1040 410 {lab=vss}
C {devices/lab_pin.sym} 1040 410 0 1 {name=l6 sig_type=std_logic lab=vss}
N 1060 210 1060 190 {lab=vddo}
C {devices/lab_pin.sym} 1060 190 0 1 {name=l7 sig_type=std_logic lab=vddo}
N 1060 390 1060 410 {lab=vsso}
C {devices/lab_pin.sym} 1060 410 0 1 {name=l8 sig_type=std_logic lab=vsso}
N 1000 250 980 250 {lab=ir}
C {devices/lab_pin.sym} 980 250 0 0 {name=l9 sig_type=std_logic lab=ir}
N 1200 250 1220 250 {lab=vbp}
C {devices/lab_pin.sym} 1220 250 0 1 {name=l10 sig_type=std_logic lab=vbp}
N 1200 270 1220 270 {lab=vbn}
C {devices/lab_pin.sym} 1220 270 0 1 {name=l11 sig_type=std_logic lab=vbn}
N 1200 290 1220 290 {lab=vbpc}
C {devices/lab_pin.sym} 1220 290 0 1 {name=l12 sig_type=std_logic lab=vbpc}
N 1200 310 1220 310 {lab=vbnc}
C {devices/lab_pin.sym} 1220 310 0 1 {name=l13 sig_type=std_logic lab=vbnc}
N 1200 330 1220 330 {lab=vabp}
C {devices/lab_pin.sym} 1220 330 0 1 {name=l14 sig_type=std_logic lab=vabp}
N 1200 350 1220 350 {lab=vabn}
C {devices/lab_pin.sym} 1220 350 0 1 {name=l15 sig_type=std_logic lab=vabn}
N 1000 270 980 270 {lab=en_3v3}
C {devices/lab_pin.sym} 980 270 0 0 {name=l16 sig_type=std_logic lab=en_3v3}
N 1000 290 980 290 {lab=en_3v3_b}
C {devices/lab_pin.sym} 980 290 0 0 {name=l17 sig_type=std_logic lab=en_3v3_b}
C {nand2_hv.sym} 300 240 0 0 {name=XDA}
N 280 190 280 170 {lab=vdd}
C {devices/lab_pin.sym} 280 170 0 1 {name=l18 sig_type=std_logic lab=vdd}
N 280 290 280 310 {lab=vss}
C {devices/lab_pin.sym} 280 310 0 1 {name=l19 sig_type=std_logic lab=vss}
N 240 230 220 230 {lab=en_3v3}
C {devices/lab_pin.sym} 220 230 0 0 {name=l20 sig_type=std_logic lab=en_3v3}
N 240 250 220 250 {lab=sel0_3v3}
C {devices/lab_pin.sym} 220 250 0 0 {name=l21 sig_type=std_logic lab=sel0_3v3}
N 360 230 380 230 {lab=en_oa_b}
C {devices/lab_pin.sym} 380 230 0 1 {name=l22 sig_type=std_logic lab=en_oa_b}
C {inv_hv.sym} 520 240 0 0 {name=XDB}
N 500 200 500 180 {lab=vdd}
C {devices/lab_pin.sym} 500 180 0 1 {name=l23 sig_type=std_logic lab=vdd}
N 500 280 500 300 {lab=vss}
C {devices/lab_pin.sym} 500 300 0 1 {name=l24 sig_type=std_logic lab=vss}
N 460 240 440 240 {lab=en_oa_b}
C {devices/lab_pin.sym} 440 240 0 0 {name=l25 sig_type=std_logic lab=en_oa_b}
N 580 240 600 240 {lab=en_oa}
C {devices/lab_pin.sym} 600 240 0 1 {name=l26 sig_type=std_logic lab=en_oa}
C {nand2_hv.sym} 300 400 0 0 {name=XDC}
N 280 350 280 330 {lab=vdd}
C {devices/lab_pin.sym} 280 330 0 1 {name=l27 sig_type=std_logic lab=vdd}
N 280 450 280 470 {lab=vss}
C {devices/lab_pin.sym} 280 470 0 1 {name=l28 sig_type=std_logic lab=vss}
N 240 390 220 390 {lab=en_3v3}
C {devices/lab_pin.sym} 220 390 0 0 {name=l29 sig_type=std_logic lab=en_3v3}
N 240 410 220 410 {lab=sel1_3v3}
C {devices/lab_pin.sym} 220 410 0 0 {name=l30 sig_type=std_logic lab=sel1_3v3}
N 360 390 380 390 {lab=en_bg_b}
C {devices/lab_pin.sym} 380 390 0 1 {name=l31 sig_type=std_logic lab=en_bg_b}
C {inv_hv.sym} 520 400 0 0 {name=XDD}
N 500 360 500 340 {lab=vdd}
C {devices/lab_pin.sym} 500 340 0 1 {name=l32 sig_type=std_logic lab=vdd}
N 500 440 500 460 {lab=vss}
C {devices/lab_pin.sym} 500 460 0 1 {name=l33 sig_type=std_logic lab=vss}
N 460 400 440 400 {lab=en_bg_b}
C {devices/lab_pin.sym} 440 400 0 0 {name=l34 sig_type=std_logic lab=en_bg_b}
N 580 400 600 400 {lab=en_bg}
C {devices/lab_pin.sym} 600 400 0 1 {name=l35 sig_type=std_logic lab=en_bg}
C {nor2_hv.sym} 300 560 0 0 {name=XDE}
N 280 510 280 490 {lab=vdd}
C {devices/lab_pin.sym} 280 490 0 1 {name=l36 sig_type=std_logic lab=vdd}
N 280 610 280 630 {lab=vss}
C {devices/lab_pin.sym} 280 630 0 1 {name=l37 sig_type=std_logic lab=vss}
N 240 550 220 550 {lab=sel0_3v3}
C {devices/lab_pin.sym} 220 550 0 0 {name=l38 sig_type=std_logic lab=sel0_3v3}
N 240 570 220 570 {lab=sel1_3v3}
C {devices/lab_pin.sym} 220 570 0 0 {name=l39 sig_type=std_logic lab=sel1_3v3}
N 360 550 380 550 {lab=s00}
C {devices/lab_pin.sym} 380 550 0 1 {name=l40 sig_type=std_logic lab=s00}
C {nand2_hv.sym} 520 560 0 0 {name=XDF}
N 500 510 500 490 {lab=vdd}
C {devices/lab_pin.sym} 500 490 0 1 {name=l41 sig_type=std_logic lab=vdd}
N 500 610 500 630 {lab=vss}
C {devices/lab_pin.sym} 500 630 0 1 {name=l42 sig_type=std_logic lab=vss}
N 460 550 440 550 {lab=en_3v3}
C {devices/lab_pin.sym} 440 550 0 0 {name=l43 sig_type=std_logic lab=en_3v3}
N 460 570 440 570 {lab=s00}
C {devices/lab_pin.sym} 440 570 0 0 {name=l44 sig_type=std_logic lab=s00}
N 580 550 600 550 {lab=en_ext_b}
C {devices/lab_pin.sym} 600 550 0 1 {name=l45 sig_type=std_logic lab=en_ext_b}
C {inv_hv.sym} 740 560 0 0 {name=XDG}
N 720 520 720 500 {lab=vdd}
C {devices/lab_pin.sym} 720 500 0 1 {name=l46 sig_type=std_logic lab=vdd}
N 720 600 720 620 {lab=vss}
C {devices/lab_pin.sym} 720 620 0 1 {name=l47 sig_type=std_logic lab=vss}
N 680 560 660 560 {lab=en_ext_b}
C {devices/lab_pin.sym} 660 560 0 0 {name=l48 sig_type=std_logic lab=en_ext_b}
N 800 560 820 560 {lab=en_ext}
C {devices/lab_pin.sym} 820 560 0 1 {name=l49 sig_type=std_logic lab=en_ext}
C {oa_core_pd.sym} 800 120 0 0 {name=Xoa}
N 760 70 760 50 {lab=vdd}
C {devices/lab_pin.sym} 760 50 0 1 {name=l50 sig_type=std_logic lab=vdd}
N 760 170 760 190 {lab=vss}
C {devices/lab_pin.sym} 760 190 0 1 {name=l51 sig_type=std_logic lab=vss}
N 880 110 900 110 {lab=ir}
C {devices/lab_pin.sym} 900 110 0 1 {name=l52 sig_type=std_logic lab=ir}
N 720 110 700 110 {lab=en_oa}
C {devices/lab_pin.sym} 700 110 0 0 {name=l53 sig_type=std_logic lab=en_oa}
N 720 130 700 130 {lab=en_oa_b}
C {devices/lab_pin.sym} 700 130 0 0 {name=l54 sig_type=std_logic lab=en_oa_b}
C {bg_core_pd.sym} 800 300 0 0 {name=Xbg}
N 760 250 760 230 {lab=vdd}
C {devices/lab_pin.sym} 760 230 0 1 {name=l55 sig_type=std_logic lab=vdd}
N 760 350 760 370 {lab=vss}
C {devices/lab_pin.sym} 760 370 0 1 {name=l56 sig_type=std_logic lab=vss}
N 880 290 900 290 {lab=ir}
C {devices/lab_pin.sym} 900 290 0 1 {name=l57 sig_type=std_logic lab=ir}
N 720 290 700 290 {lab=en_bg}
C {devices/lab_pin.sym} 700 290 0 0 {name=l58 sig_type=std_logic lab=en_bg}
N 720 310 700 310 {lab=en_bg_b}
C {devices/lab_pin.sym} 700 310 0 0 {name=l59 sig_type=std_logic lab=en_bg_b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 760 760 0 0 {name=TEN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 780 730 780 710 {lab=ibias}
C {devices/lab_pin.sym} 780 710 0 1 {name=l60 sig_type=std_logic lab=ibias}
N 740 760 720 760 {lab=en_ext}
C {devices/lab_pin.sym} 720 760 0 0 {name=l61 sig_type=std_logic lab=en_ext}
N 780 790 780 810 {lab=ir}
C {devices/lab_pin.sym} 780 810 0 1 {name=l62 sig_type=std_logic lab=ir}
N 780 760 800 760 {lab=vss}
C {devices/lab_pin.sym} 800 760 0 1 {name=l63 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 960 760 0 0 {name=TEP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 980 790 980 810 {lab=ibias}
C {devices/lab_pin.sym} 980 810 0 1 {name=l64 sig_type=std_logic lab=ibias}
N 940 760 920 760 {lab=en_ext_b}
C {devices/lab_pin.sym} 920 760 0 0 {name=l65 sig_type=std_logic lab=en_ext_b}
N 980 730 980 710 {lab=ir}
C {devices/lab_pin.sym} 980 710 0 1 {name=l66 sig_type=std_logic lab=ir}
N 980 760 1000 760 {lab=vdd}
C {devices/lab_pin.sym} 1000 760 0 1 {name=l67 sig_type=std_logic lab=vdd}
T {sel1 sel0 = 0 0: harness ibias (sourced, ~5 uA = iDAC code 20 at 250 nA/step) through TEN / TEP;  0 1: Oguey-Aebischer core;} 40 900 0 0 0.25 0.25 {}
T {1 0: bandgap core;  1 1: both cores (currents add). en_3v3 = 0: everything off (tree TG and TDN, both cores, TEN / TEP open).} 40 924 0 0 0.25 0.25 {}
T {A disabled core output (POC drain) is off, so the cores share the tree input ir without a switch. Source: netlist/source/d2s_bias_sel_pd.spice} 40 948 0 0 0.25 0.25 {}
C {devices/title.sym} 160 600 0 0 {name=l0 author="Christoph Maier"}
