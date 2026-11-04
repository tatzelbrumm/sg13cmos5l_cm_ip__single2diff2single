v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s2d_mpdda: pad input -> fully differential, voutp - voutn = 2 (vin - vref), (voutp + voutn)/2 = vcm} 60 -1280 0 0 0.5 0.5 {}
T {signal units A1 = A2 (vin, vref), F1 (vcm, vfbp), F2 (vfbn, vcm); CMFB units M1 (vfbp, vcm), M2 (vfbn, vcm); all unit_r2: x += f(gp - gn)} 60 -1220 0 0 0.3 0.3 {}
T {tie vfbp to voutp and vfbn to voutn; they are pins only so that the loops can be broken in simulation. CLP / CLN: built-in minimum load.} 60 -1180 0 0 0.3 0.3 {}
T {sinks SX / SY: 6 fingers of BN (6/6), SXC / SYC: 4 fingers; loads LP / LN mirror the CMFB diode D 1:1; netlist: ../../netlist/source/s2d_mpdda.spice} 60 -40 0 0 0.25 0.25 {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 60 0 0 0 0.2 0.2 {}
N 2820 -680 2860 -680 {lab=voutn}
N 1540 -1040 1840 -1040 {lab=vbp}
N 2300 -480 2480 -480 {lab=vbnc}
N 120 -920 140 -920 {lab=vref}
N 420 -920 440 -920 {lab=vref}
N 720 -960 740 -960 {lab=vcm}
N 1020 -920 1040 -920 {lab=vcm}
N 2360 -1080 2360 -1050 {lab=vdd}
N 2360 -1020 2380 -1020 {lab=vdd}
N 2380 -1080 2380 -1020 {lab=vdd}
N 2300 -880 2320 -880 {lab=vbpc}
N 2300 -420 2320 -420 {lab=vbnc}
N 2300 -160 2320 -160 {lab=vbn}
N 2360 -160 2380 -160 {lab=vss}
N 2540 -1080 2540 -1050 {lab=vdd}
N 2540 -1020 2560 -1020 {lab=vdd}
N 2560 -1080 2560 -1020 {lab=vdd}
N 2480 -880 2500 -880 {lab=vbpc}
N 2480 -420 2500 -420 {lab=vbnc}
N 2480 -160 2500 -160 {lab=vbn}
N 2540 -160 2560 -160 {lab=vss}
N 1380 -920 1400 -920 {lab=vcm}
N 1680 -920 1700 -920 {lab=vcm}
N 2200 -1080 2200 -1050 {lab=vdd}
N 2180 -1020 2200 -1020 {lab=vdd}
N 2180 -1080 2180 -1020 {lab=vdd}
N 2240 -880 2260 -880 {lab=vbpc}
N 2200 -820 2280 -820 {lab=vcmfb}
N 2240 -1020 2280 -1020 {lab=vcmfb}
N 2140 -420 2160 -420 {lab=vbnc}
N 2140 -160 2160 -160 {lab=vbn}
N 2200 -160 2220 -160 {lab=vss}
N 1960 -420 1980 -420 {lab=vbnc}
N 1960 -160 1980 -160 {lab=vbn}
N 2020 -160 2040 -160 {lab=vss}
N 240 -320 540 -320 {lab=y}
N 540 -320 840 -320 {lab=y}
N 840 -320 1140 -320 {lab=y}
N 2360 -1080 2380 -1080 {lab=vdd}
N 2660 -100 2700 -100 {lab=vss}
N 2360 -100 2380 -100 {lab=vss}
N 2540 -1080 2560 -1080 {lab=vdd}
N 2540 -100 2560 -100 {lab=vss}
N 2200 -100 2220 -100 {lab=vss}
N 2040 -100 2200 -100 {lab=vss}
N 2020 -100 2040 -100 {lab=vss}
N 2360 -990 2360 -910 {lab=lp}
N 2540 -990 2540 -910 {lab=ln}
N 2200 -990 2200 -910 {lab=dd}
N 2380 -1020 2380 -880 {lab=vdd}
N 2560 -1020 2560 -880 {lab=vdd}
N 2180 -1020 2180 -880 {lab=vdd}
N 2180 -1080 2200 -1080 {lab=vdd}
N 2380 -1080 2540 -1080 {lab=vdd}
N 2180 -880 2200 -880 {lab=vdd}
N 2360 -880 2380 -880 {lab=vdd}
N 2540 -880 2560 -880 {lab=vdd}
N 2020 -1080 2180 -1080 {lab=vdd}
N 2360 -700 2360 -450 {lab=voutp}
N 2540 -680 2540 -450 {lab=voutn}
N 2380 -160 2380 -100 {lab=vss}
N 2360 -130 2360 -100 {lab=vss}
N 2560 -160 2560 -100 {lab=vss}
N 2540 -130 2540 -100 {lab=vss}
N 2220 -160 2220 -100 {lab=vss}
N 2200 -130 2200 -100 {lab=vss}
N 2040 -160 2040 -100 {lab=vss}
N 2020 -130 2020 -100 {lab=vss}
N 2020 -260 2020 -190 {lab=yc}
N 2360 -390 2360 -340 {lab=x}
N 2540 -390 2540 -320 {lab=y}
N 1500 -260 1800 -260 {lab=yc}
N 2850 -180 2860 -180 {lab=vss}
N 2860 -180 2860 -100 {lab=vss}
N 2820 -100 2860 -100 {lab=vss}
N 2780 -180 2780 -100 {lab=vss}
N 2780 -180 2790 -180 {lab=vss}
N 2820 -180 2820 -100 {lab=vss}
N 2780 -100 2820 -100 {lab=vss}
N 2740 -100 2780 -100 {lab=vss}
N 2700 -180 2700 -100 {lab=vss}
N 2730 -180 2740 -180 {lab=vss}
N 2740 -180 2740 -100 {lab=vss}
N 2700 -100 2740 -100 {lab=vss}
N 2660 -180 2660 -100 {lab=vss}
N 2560 -100 2660 -100 {lab=vss}
N 2660 -180 2670 -180 {lab=vss}
N 2200 -1080 2360 -1080 {lab=vdd}
N 2200 -850 2200 -820 {lab=vcmfb}
N 2280 -1020 2280 -820 {lab=vcmfb}
N 2260 -880 2260 -800 {lab=vbpc}
N 2300 -880 2300 -800 {lab=vbpc}
N 2220 -100 2360 -100 {lab=vss}
N 2260 -800 2300 -800 {lab=vbpc}
N 2480 -880 2480 -800 {lab=vbpc}
N 2460 -1020 2500 -1020 {lab=vcmfb}
N 2460 -1020 2460 -820 {lab=vcmfb}
N 2280 -820 2460 -820 {lab=vcmfb}
N 2200 -820 2200 -450 {lab=vcmfb}
N 2200 -280 2200 -190 {lab=xc}
N 2200 -390 2200 -280 {lab=xc}
N 2540 -320 2540 -190 {lab=y}
N 2360 -340 2360 -190 {lab=x}
N 2380 -420 2380 -160 {lab=vss}
N 2360 -420 2380 -420 {lab=vss}
N 2540 -420 2560 -420 {lab=vss}
N 2200 -420 2220 -420 {lab=vss}
N 2040 -420 2040 -160 {lab=vss}
N 2020 -420 2040 -420 {lab=vss}
N 2020 -1080 2020 -450 {lab=vdd}
N 2280 -1020 2320 -1020 {lab=vcmfb}
N 2480 -220 2480 -160 {lab=vbn}
N 2300 -220 2480 -220 {lab=vbn}
N 1380 -640 1680 -640 {lab=vcm}
N 1680 -920 1680 -640 {lab=vcm}
N 1380 -920 1380 -640 {lab=vcm}
N 1020 -640 1380 -640 {lab=vcm}
N 1660 -960 1700 -960 {lab=vfbn}
N 1360 -960 1400 -960 {lab=vfbp}
N 1000 -960 1040 -960 {lab=vfbn}
N 700 -920 740 -920 {lab=vfbp}
N 720 -960 720 -640 {lab=vcm}
N 60 -640 720 -640 {lab=vcm}
N 1000 -680 1660 -680 {lab=vfbn}
N 1660 -960 1660 -680 {lab=vfbn}
N 1000 -960 1000 -680 {lab=vfbn}
N 60 -680 1000 -680 {lab=vfbn}
N 700 -920 700 -700 {lab=vfbp}
N 100 -960 140 -960 {lab=vin}
N 400 -960 440 -960 {lab=vin}
N 120 -740 420 -740 {lab=vref}
N 420 -920 420 -740 {lab=vref}
N 400 -960 400 -760 {lab=vin}
N 120 -920 120 -740 {lab=vref}
N 60 -740 120 -740 {lab=vref}
N 100 -960 100 -760 {lab=vin}
N 60 -760 100 -760 {lab=vin}
N 540 -860 540 -320 {lab=y}
N 840 -860 840 -320 {lab=y}
N 1140 -860 1140 -320 {lab=y}
N 1500 -860 1500 -260 {lab=yc}
N 1800 -860 1800 -260 {lab=yc}
N 100 -760 400 -760 {lab=vin}
N 2300 -800 2480 -800 {lab=vbpc}
N 2300 -220 2300 -160 {lab=vbn}
N 2140 -220 2140 -160 {lab=vbn}
N 1960 -220 2140 -220 {lab=vbn}
N 1960 -220 1960 -160 {lab=vbn}
N 2140 -220 2300 -220 {lab=vbn}
N 2480 -480 2480 -420 {lab=vbnc}
N 2300 -480 2300 -420 {lab=vbnc}
N 2140 -480 2140 -420 {lab=vbnc}
N 1960 -480 2140 -480 {lab=vbnc}
N 1960 -480 1960 -420 {lab=vbnc}
N 2140 -480 2300 -480 {lab=vbnc}
N 2360 -700 2700 -700 {lab=voutp}
N 2380 -100 2540 -100 {lab=vss}
N 2700 -700 2700 -220 {lab=voutp}
N 2360 -850 2360 -700 {lab=voutp}
N 2820 -680 2820 -220 {lab=voutn}
N 2540 -850 2540 -680 {lab=voutn}
N 2700 -700 2860 -700 {lab=voutp}
N 2540 -680 2820 -680 {lab=voutn}
N 1840 -860 1840 -100 {lab=vss}
N 1540 -100 1840 -100 {lab=vss}
N 1540 -860 1540 -100 {lab=vss}
N 1180 -100 1540 -100 {lab=vss}
N 1180 -860 1180 -100 {lab=vss}
N 880 -860 880 -100 {lab=vss}
N 880 -100 1180 -100 {lab=vss}
N 580 -100 880 -100 {lab=vss}
N 580 -860 580 -100 {lab=vss}
N 280 -860 280 -100 {lab=vss}
N 280 -100 580 -100 {lab=vss}
N 60 -100 280 -100 {lab=vss}
N 1460 -860 1460 -280 {lab=xc}
N 1760 -860 1760 -280 {lab=xc}
N 1460 -280 1760 -280 {lab=xc}
N 1100 -860 1100 -340 {lab=x}
N 800 -340 1100 -340 {lab=x}
N 800 -860 800 -340 {lab=x}
N 500 -340 800 -340 {lab=x}
N 500 -860 500 -340 {lab=x}
N 200 -860 200 -340 {lab=x}
N 200 -340 500 -340 {lab=x}
N 1760 -1080 1760 -1020 {lab=vdd}
N 1460 -1080 1760 -1080 {lab=vdd}
N 1460 -1080 1460 -1020 {lab=vdd}
N 1100 -1080 1460 -1080 {lab=vdd}
N 1100 -1080 1100 -1020 {lab=vdd}
N 800 -1080 800 -1020 {lab=vdd}
N 800 -1080 1100 -1080 {lab=vdd}
N 500 -1080 800 -1080 {lab=vdd}
N 500 -1080 500 -1020 {lab=vdd}
N 200 -1080 200 -1020 {lab=vdd}
N 200 -1080 500 -1080 {lab=vdd}
N 60 -1080 200 -1080 {lab=vdd}
N 1840 -1040 1840 -1020 {lab=vbp}
N 1540 -1040 1540 -1020 {lab=vbp}
N 1180 -1040 1540 -1040 {lab=vbp}
N 1180 -1040 1180 -1020 {lab=vbp}
N 880 -1040 880 -1020 {lab=vbp}
N 880 -1040 1180 -1040 {lab=vbp}
N 580 -1040 880 -1040 {lab=vbp}
N 580 -1040 580 -1020 {lab=vbp}
N 280 -1040 280 -1020 {lab=vbp}
N 280 -1040 580 -1040 {lab=vbp}
N 60 -1040 280 -1040 {lab=vbp}
N 2560 -420 2560 -160 {lab=vss}
N 1840 -100 2020 -100 {lab=vss}
N 2220 -420 2220 -160 {lab=vss}
N 1760 -1080 2020 -1080 {lab=vdd}
N 1100 -340 2360 -340 {lab=x}
N 1140 -320 2540 -320 {lab=y}
N 60 -800 2260 -800 {lab=vbpc}
N 1760 -280 2200 -280 {lab=xc}
N 60 -220 1960 -220 {lab=vbn}
N 60 -480 1960 -480 {lab=vbnc}
N 1660 -680 1960 -680 {lab=vfbn}
N 1800 -260 2020 -260 {lab=yc}
N 2020 -390 2020 -260 {lab=yc}
N 60 -700 700 -700 {lab=vfbp}
N 700 -700 1360 -700 {lab=vfbp}
N 1360 -700 1960 -700 {lab=vfbp}
N 1360 -960 1360 -700 {lab=vfbp}
N 240 -860 240 -320 {lab=y}
N 1020 -920 1020 -640 {lab=vcm}
N 720 -640 1020 -640 {lab=vcm}
C {devices/iopin.sym} 60 -1080 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 60 -100 0 1 {name=p2 lab=vss}
C {devices/ipin.sym} 60 -760 0 0 {name=p3 lab=vin}
C {devices/lab_pin.sym} 400 -760 0 1 {name=l4 sig_type=std_logic lab=vin}
C {devices/ipin.sym} 60 -740 0 0 {name=p5 lab=vref}
C {devices/lab_pin.sym} 420 -740 0 1 {name=l6 sig_type=std_logic lab=vref}
C {devices/ipin.sym} 60 -640 0 0 {name=p7 lab=vcm}
C {devices/lab_pin.sym} 1680 -640 0 1 {name=l8 sig_type=std_logic lab=vcm}
C {devices/opin.sym} 2860 -700 0 0 {name=p9 lab=voutp}
C {devices/opin.sym} 2860 -680 0 0 {name=p11 lab=voutn}
C {devices/ipin.sym} 60 -700 0 0 {name=p13 lab=vfbp}
C {devices/lab_pin.sym} 1960 -700 0 1 {name=l14 sig_type=std_logic lab=vfbp}
C {devices/ipin.sym} 60 -680 0 0 {name=p15 lab=vfbn}
C {devices/lab_pin.sym} 1960 -680 0 1 {name=l16 sig_type=std_logic lab=vfbn}
C {devices/iopin.sym} 60 -1040 0 1 {name=p17 lab=vbp}
C {devices/iopin.sym} 60 -220 0 1 {name=p19 lab=vbn}
C {devices/lab_pin.sym} 2480 -220 0 1 {name=l20 sig_type=std_logic lab=vbn}
C {devices/iopin.sym} 60 -800 0 1 {name=p21 lab=vbpc}
C {devices/lab_pin.sym} 2480 -800 0 1 {name=l22 sig_type=std_logic lab=vbpc}
C {devices/iopin.sym} 60 -480 0 1 {name=p23 lab=vbnc}
C {devices/lab_pin.sym} 2480 -480 0 1 {name=l24 sig_type=std_logic lab=vbnc}
C {unit_r2.sym} 240 -940 0 0 {name=XA1}
C {devices/lab_pin.sym} 100 -960 0 0 {name=l26 sig_type=std_logic lab=vin}
C {devices/lab_pin.sym} 120 -920 0 0 {name=l27 sig_type=std_logic lab=vref}
C {unit_r2.sym} 540 -940 0 0 {name=XA2}
C {devices/lab_pin.sym} 400 -960 0 0 {name=l30 sig_type=std_logic lab=vin}
C {devices/lab_pin.sym} 420 -920 0 0 {name=l31 sig_type=std_logic lab=vref}
C {unit_r2.sym} 840 -940 0 0 {name=XF1}
C {devices/lab_pin.sym} 720 -960 0 0 {name=l34 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 700 -920 0 0 {name=l35 sig_type=std_logic lab=vfbp}
C {unit_r2.sym} 1140 -940 0 0 {name=XF2}
C {devices/lab_pin.sym} 1000 -960 0 0 {name=l38 sig_type=std_logic lab=vfbn}
C {devices/lab_pin.sym} 1020 -920 0 0 {name=l39 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 200 -340 0 0 {name=l41 sig_type=std_logic lab=x}
C {devices/lab_pin.sym} 240 -320 0 0 {name=l42 sig_type=std_logic lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2340 -1020 0 0 {name=LP
l=4u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2340 -880 0 0 {name=LPC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2340 -420 0 0 {name=CX
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2340 -160 0 0 {name=SX
l=6u
w=36u
ng=6
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 2360 -970 0 1 {name=l43 sig_type=std_logic lab=lp}
C {devices/lab_pin.sym} 2300 -1020 0 0 {name=l44 sig_type=std_logic lab=vcmfb}
C {devices/lab_pin.sym} 2300 -420 0 0 {name=l46 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 2300 -160 0 0 {name=l47 sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2520 -1020 0 0 {name=LN
l=4u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2520 -880 0 0 {name=LNC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2520 -420 0 0 {name=CY
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2520 -160 0 0 {name=SY
l=6u
w=36u
ng=6
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 2540 -970 0 1 {name=l48 sig_type=std_logic lab=ln}
C {devices/lab_pin.sym} 2460 -1020 0 0 {name=l49 sig_type=std_logic lab=vcmfb}
C {devices/lab_pin.sym} 2480 -880 0 0 {name=l50 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 2480 -420 0 0 {name=l51 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 2480 -160 0 0 {name=l52 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 2360 -700 0 0 {name=l53 sig_type=std_logic lab=voutp}
C {devices/lab_pin.sym} 2540 -680 0 0 {name=l54 sig_type=std_logic lab=voutn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2700 -200 1 0 {name=CLP
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2820 -200 1 0 {name=CLN
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {unit_r2.sym} 1500 -940 0 0 {name=XM1}
C {devices/lab_pin.sym} 1360 -960 0 0 {name=l56 sig_type=std_logic lab=vfbp}
C {devices/lab_pin.sym} 1380 -920 0 0 {name=l57 sig_type=std_logic lab=vcm}
C {unit_r2.sym} 1800 -940 0 0 {name=XM2}
C {devices/lab_pin.sym} 1840 -1040 0 1 {name=l59 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 1660 -960 0 0 {name=l60 sig_type=std_logic lab=vfbn}
C {devices/lab_pin.sym} 1680 -920 0 0 {name=l61 sig_type=std_logic lab=vcm}
C {devices/lab_pin.sym} 1460 -280 0 0 {name=l63 sig_type=std_logic lab=xc}
C {devices/lab_pin.sym} 1500 -260 0 0 {name=l64 sig_type=std_logic lab=yc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2220 -1020 0 1 {name=D
l=4u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2220 -880 0 1 {name=DC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2180 -420 0 0 {name=CXC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2180 -160 0 0 {name=SXC
l=6u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 2200 -990 0 0 {name=l65 sig_type=std_logic lab=dd}
C {devices/lab_pin.sym} 2280 -820 0 1 {name=l67 sig_type=std_logic lab=vcmfb}
C {devices/lab_pin.sym} 2140 -420 0 0 {name=l68 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 2140 -160 0 0 {name=l69 sig_type=std_logic lab=vbn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2000 -420 0 0 {name=CYC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2000 -160 0 0 {name=SYC
l=6u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_pin.sym} 1960 -420 0 0 {name=l70 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 1960 -160 0 0 {name=l71 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 2360 -340 0 1 {name=l1 sig_type=std_logic lab=x}
C {devices/lab_pin.sym} 2540 -320 0 1 {name=l2 sig_type=std_logic lab=y}
