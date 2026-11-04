v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {single-ended <-> differential <-> single-ended top level
Boundary reconciled against sudelbuecher/description/s2d_d2s_pinbuffers.md
and sg13cmos5l_ocd_chipalooza/verilog/rtl/user_project_wrapper_3a.v -- see
TOP_LEVEL_MODULE.md. No scan chain (reopened, not settled -- see log).
No pin for spec's reset: user_project_wrapper_3a.v has no per-project
reset port, only a chip-global one via housekeeping SPI.} 40 -830 0 0 0.3 0.3 {}
N 640 -260 700 -260 {lab=vout}
N 140 -260 200 -260 {lab=vin}
C {devices/iopin.sym} 140 -680 2 0 {name=p1 lab=vdd_3v3}
C {devices/iopin.sym} 140 -660 2 0 {name=p2 lab=vdd_1v2}
C {devices/iopin.sym} 140 -640 2 0 {name=p3 lab=vss_3v3}
C {devices/iopin.sym} 140 -620 2 0 {name=p4 lab=vss_1v2}
C {devices/iopin.sym} 140 -600 2 0 {name=p5 lab=vssio}
C {devices/ipin.sym} 140 -560 2 1 {name=p6 lab=ena}
C {devices/ipin.sym} 140 -540 2 1 {name=p7 lab=clk}
C {devices/ipin.sym} 140 -500 2 1 {name=p8 lab=outbuf_en}
C {devices/ipin.sym} 140 -480 2 1 {name=p9 lab=inbuf_en}
C {devices/ipin.sym} 140 -460 2 1 {name=p10 lab=filter_en}
C {devices/ipin.sym} 140 -440 2 1 {name=p11 lab=vdiff_en[1]}
C {devices/ipin.sym} 140 -420 2 1 {name=p12 lab=vdiff_en[0]}
C {devices/ipin.sym} 140 -400 2 1 {name=p13 lab=vcmsel[1]}
C {devices/ipin.sym} 140 -380 2 1 {name=p14 lab=vcmsel[0]}
C {devices/ipin.sym} 140 -340 2 1 {name=p15 lab=ibias}
C {devices/ipin.sym} 140 -320 2 1 {name=p16 lab=igmc}
C {devices/ipin.sym} 140 -300 2 1 {name=p17 lab=vbias}
C {devices/ipin.sym} 140 -260 2 1 {name=p18 lab=vin}
C {devices/opin.sym} 700 -260 2 1 {name=p19 lab=vout}
C {devices/iopin.sym} 140 -180 2 0 {name=p20 lab=vcm}
C {devices/iopin.sym} 140 -140 2 0 {name=p21 lab=vdiffp}
C {devices/iopin.sym} 140 -120 2 0 {name=p22 lab=vdiffn}
C {title.sym} 160 -40 0 0 {name=l1 author="Christoph Maier"}
C {sg13cmos5l_IOPadSingle2Diff.sym} 260 -260 0 0 {name=xinbuf}
C {sg13cmos5l_IOPadDiff2Single.sym} 580 -260 0 0 {name=xoutbuf}
C {sg13cmos5l_io/sg13cmos5l_IOPadAnalog.sym} 700 -780 1 0 {name=x1}
C {sg13cmos5l_io/sg13cmos5l_IOPadInOut16mA.sym} 700 -570 1 0 {name=x2}
C {devices/lab_pin.sym} 540 -440 0 0 {name=l_outbuf_iovdd sig_type=std_logic lab=outbuf_iovdd}
C {devices/lab_pin.sym} 620 -440 0 1 {name=l_outbuf_vdd sig_type=std_logic lab=outbuf_vdd}
C {devices/lab_pin.sym} 540 -80 0 1 {name=l_outbuf_iovss sig_type=std_logic lab=outbuf_iovss}
C {devices/lab_pin.sym} 360 -300 0 0 {name=l_outbuf_iref sig_type=std_logic lab=outbuf_iref}
C {devices/lab_pin.sym} 360 -260 0 0 {name=l_outbuf_en sig_type=std_logic lab=outbuf_en_3v3}
C {devices/lab_pin.sym} 360 -240 0 0 {name=l_outbuf_enb sig_type=std_logic lab=outbuf_en_3v3_b}
C {en_ctrl_3v3.sym} 1100 140 0 0 {name=xoutbuf_c}
C {devices/lab_pin.sym} 1040 60 0 0 {name=l_xoutbuf_c_vddh sig_type=std_logic lab=outbuf_iovdd}
C {devices/lab_pin.sym} 1060 60 0 1 {name=l_xoutbuf_c_vddl sig_type=std_logic lab=outbuf_vdd}
C {devices/lab_pin.sym} 1040 220 0 1 {name=l_xoutbuf_c_vss sig_type=std_logic lab=outbuf_iovss}
C {devices/lab_pin.sym} 1200 100 0 1 {name=l_xoutbuf_c_en_3v3 sig_type=std_logic lab=outbuf_en_3v3}
C {devices/lab_pin.sym} 1200 120 0 1 {name=l_xoutbuf_c_en_3v3_b sig_type=std_logic lab=outbuf_en_3v3_b}
C {devices/lab_pin.sym} 1200 140 0 1 {name=l_xoutbuf_c_sel0_3v3 sig_type=std_logic lab=outbuf_sel0_3v3}
C {devices/lab_pin.sym} 1200 160 0 1 {name=l_xoutbuf_c_sel1_3v3 sig_type=std_logic lab=outbuf_sel1_3v3}
C {bias_gen_pd.sym} 1750 140 0 0 {name=xoutbuf_g}
C {devices/lab_pin.sym} 1750 60 0 1 {name=l_xoutbuf_g_vdd sig_type=std_logic lab=outbuf_iovdd}
C {devices/lab_pin.sym} 1750 220 0 1 {name=l_xoutbuf_g_vss sig_type=std_logic lab=outbuf_iovss}
C {devices/lab_pin.sym} 1660 130 0 0 {name=l_xoutbuf_g_en_3v3 sig_type=std_logic lab=outbuf_en_3v3}
C {devices/lab_pin.sym} 1660 150 0 0 {name=l_xoutbuf_g_sel0_3v3 sig_type=std_logic lab=outbuf_sel0_3v3}
C {devices/lab_pin.sym} 1660 170 0 0 {name=l_xoutbuf_g_sel1_3v3 sig_type=std_logic lab=outbuf_sel1_3v3}
C {devices/lab_pin.sym} 1840 140 0 1 {name=l_xoutbuf_g_iref sig_type=std_logic lab=outbuf_iref}
T {xoutbuf_c (en_ctrl_3v3) and xoutbuf_g (bias_gen_pd): outside the pad cell since 2026-11-03 (backannotation to the drawn cell),} 980 -10 0 0 0.25 0.25 {}
T {wired as in the former pad sheet; the sources that drove the old pad pins now drive them.} 980 12 0 0 0.25 0.25 {}
C {devices/lab_pin.sym} 220 -440 0 1 {name=l_inbuf_iovdd sig_type=std_logic lab=inbuf_iovdd}
C {devices/lab_pin.sym} 300 -440 0 1 {name=l_inbuf_vdd sig_type=std_logic lab=inbuf_vdd}
C {devices/lab_pin.sym} 220 -80 0 1 {name=l_inbuf_iovss sig_type=std_logic lab=inbuf_iovss}
C {devices/lab_pin.sym} 40 -300 0 0 {name=l_inbuf_iref sig_type=std_logic lab=inbuf_iref}
C {devices/lab_pin.sym} 40 -260 0 0 {name=l_inbuf_en sig_type=std_logic lab=inbuf_en_3v3}
C {devices/lab_pin.sym} 40 -240 0 0 {name=l_inbuf_enb sig_type=std_logic lab=inbuf_en_3v3_b}
C {en_ctrl_3v3.sym} 1100 440 0 0 {name=xinbuf_c}
C {devices/lab_pin.sym} 1040 360 0 0 {name=l_xinbuf_c_vddh sig_type=std_logic lab=inbuf_iovdd}
C {devices/lab_pin.sym} 1060 360 0 1 {name=l_xinbuf_c_vddl sig_type=std_logic lab=inbuf_vdd}
C {devices/lab_pin.sym} 1040 520 0 1 {name=l_xinbuf_c_vss sig_type=std_logic lab=inbuf_iovss}
C {devices/lab_pin.sym} 1200 400 0 1 {name=l_xinbuf_c_en_3v3 sig_type=std_logic lab=inbuf_en_3v3}
C {devices/lab_pin.sym} 1200 420 0 1 {name=l_xinbuf_c_en_3v3_b sig_type=std_logic lab=inbuf_en_3v3_b}
C {devices/lab_pin.sym} 1200 440 0 1 {name=l_xinbuf_c_sel0_3v3 sig_type=std_logic lab=inbuf_sel0_3v3}
C {devices/lab_pin.sym} 1200 460 0 1 {name=l_xinbuf_c_sel1_3v3 sig_type=std_logic lab=inbuf_sel1_3v3}
C {bias_gen_pd.sym} 1750 440 0 0 {name=xinbuf_g}
C {devices/lab_pin.sym} 1750 360 0 1 {name=l_xinbuf_g_vdd sig_type=std_logic lab=inbuf_iovdd}
C {devices/lab_pin.sym} 1750 520 0 1 {name=l_xinbuf_g_vss sig_type=std_logic lab=inbuf_iovss}
C {devices/lab_pin.sym} 1660 430 0 0 {name=l_xinbuf_g_en_3v3 sig_type=std_logic lab=inbuf_en_3v3}
C {devices/lab_pin.sym} 1660 450 0 0 {name=l_xinbuf_g_sel0_3v3 sig_type=std_logic lab=inbuf_sel0_3v3}
C {devices/lab_pin.sym} 1660 470 0 0 {name=l_xinbuf_g_sel1_3v3 sig_type=std_logic lab=inbuf_sel1_3v3}
C {devices/lab_pin.sym} 1840 440 0 1 {name=l_xinbuf_g_iref sig_type=std_logic lab=inbuf_iref}
T {xinbuf_c (en_ctrl_3v3) and xinbuf_g (bias_gen_pd): outside the pad cell since 2026-11-04 (backannotation to the drawn cell),} 980 280 0 0 0.25 0.25 {}
T {wired as in the former pad sheet; the sources that drove the old pad pins now drive them.} 980 302 0 0 0.25 0.25 {}
