v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 60 -760 3420 -760 {lab=vdd}
N 60 -100 3420 -100 {lab=vss}
C {devices/iopin.sym} 60 -760 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 60 -100 0 1 {name=p2 lab=vss}
C {devices/ipin.sym} 60 -680 0 0 {name=p3 lab=vin}
N 60 -680 120 -680 {lab=vin}
C {devices/lab_pin.sym} 120 -680 0 1 {name=l4 sig_type=std_logic lab=vin}
C {devices/ipin.sym} 60 -640 0 0 {name=p5 lab=vref}
N 60 -640 120 -640 {lab=vref}
C {devices/lab_pin.sym} 120 -640 0 1 {name=l6 sig_type=std_logic lab=vref}
C {devices/ipin.sym} 60 -600 0 0 {name=p7 lab=vcm}
N 60 -600 120 -600 {lab=vcm}
C {devices/lab_pin.sym} 120 -600 0 1 {name=l8 sig_type=std_logic lab=vcm}
C {devices/opin.sym} 3500 -520 0 0 {name=p9 lab=voutp}
N 3500 -520 3440 -520 {lab=voutp}
C {devices/lab_pin.sym} 3440 -520 0 0 {name=l10 sig_type=std_logic lab=voutp}
C {devices/opin.sym} 3500 -480 0 0 {name=p11 lab=voutn}
N 3500 -480 3440 -480 {lab=voutn}
C {devices/lab_pin.sym} 3440 -480 0 0 {name=l12 sig_type=std_logic lab=voutn}
C {devices/ipin.sym} 60 -480 0 0 {name=p13 lab=vfbp}
N 60 -480 120 -480 {lab=vfbp}
C {devices/lab_pin.sym} 120 -480 0 1 {name=l14 sig_type=std_logic lab=vfbp}
C {devices/ipin.sym} 60 -440 0 0 {name=p15 lab=vfbn}
N 60 -440 120 -440 {lab=vfbn}
C {devices/lab_pin.sym} 120 -440 0 1 {name=l16 sig_type=std_logic lab=vfbn}
C {devices/iopin.sym} 60 -400 0 1 {name=p17 lab=vbp}
N 60 -400 120 -400 {lab=vbp}
C {devices/lab_pin.sym} 120 -400 0 1 {name=l18 sig_type=std_logic lab=vbp}
C {devices/iopin.sym} 60 -360 0 1 {name=p19 lab=vbn}
N 60 -360 120 -360 {lab=vbn}
C {devices/lab_pin.sym} 120 -360 0 1 {name=l20 sig_type=std_logic lab=vbn}
C {devices/iopin.sym} 60 -320 0 1 {name=p21 lab=vbpc}
N 60 -320 120 -320 {lab=vbpc}
C {devices/lab_pin.sym} 120 -320 0 1 {name=l22 sig_type=std_logic lab=vbpc}
C {devices/iopin.sym} 60 -280 0 1 {name=p23 lab=vbnc}
N 60 -280 120 -280 {lab=vbnc}
C {devices/lab_pin.sym} 120 -280 0 1 {name=l24 sig_type=std_logic lab=vbnc}
C {unit_r2.sym} 420 -480 0 0 {name=XA1}
N 380 -560 380 -760 {lab=vdd}
N 460 -560 460 -580 {lab=vbp}
C {devices/lab_pin.sym} 460 -580 0 1 {name=l25 sig_type=std_logic lab=vbp}
N 320 -500 300 -500 {lab=vin}
C {devices/lab_pin.sym} 300 -500 0 0 {name=l26 sig_type=std_logic lab=vin}
N 320 -460 300 -460 {lab=vref}
C {devices/lab_pin.sym} 300 -460 0 0 {name=l27 sig_type=std_logic lab=vref}
N 380 -400 380 -300 {lab=x}
N 420 -400 420 -260 {lab=y}
N 460 -400 460 -380 {lab=vss}
C {devices/lab_pin.sym} 460 -380 0 1 {name=l28 sig_type=std_logic lab=vss}
C {unit_r2.sym} 720 -480 0 0 {name=XA2}
N 680 -560 680 -760 {lab=vdd}
N 760 -560 760 -580 {lab=vbp}
C {devices/lab_pin.sym} 760 -580 0 1 {name=l29 sig_type=std_logic lab=vbp}
N 620 -500 600 -500 {lab=vin}
C {devices/lab_pin.sym} 600 -500 0 0 {name=l30 sig_type=std_logic lab=vin}
N 620 -460 600 -460 {lab=vref}
C {devices/lab_pin.sym} 600 -460 0 0 {name=l31 sig_type=std_logic lab=vref}
N 680 -400 680 -300 {lab=x}
N 720 -400 720 -260 {lab=y}
N 760 -400 760 -380 {lab=vss}
C {devices/lab_pin.sym} 760 -380 0 1 {name=l32 sig_type=std_logic lab=vss}
C {unit_r2.sym} 1020 -480 0 0 {name=XF1}
N 980 -560 980 -760 {lab=vdd}
N 1060 -560 1060 -580 {lab=vbp}
C {devices/lab_pin.sym} 1060 -580 0 1 {name=l33 sig_type=std_logic lab=vbp}
N 920 -500 900 -500 {lab=vcm}
C {devices/lab_pin.sym} 900 -500 0 0 {name=l34 sig_type=std_logic lab=vcm}
N 920 -460 900 -460 {lab=vfbp}
C {devices/lab_pin.sym} 900 -460 0 0 {name=l35 sig_type=std_logic lab=vfbp}
N 980 -400 980 -300 {lab=x}
N 1020 -400 1020 -260 {lab=y}
N 1060 -400 1060 -380 {lab=vss}
C {devices/lab_pin.sym} 1060 -380 0 1 {name=l36 sig_type=std_logic lab=vss}
C {unit_r2.sym} 1320 -480 0 0 {name=XF2}
N 1280 -560 1280 -760 {lab=vdd}
N 1360 -560 1360 -580 {lab=vbp}
C {devices/lab_pin.sym} 1360 -580 0 1 {name=l37 sig_type=std_logic lab=vbp}
N 1220 -500 1200 -500 {lab=vfbn}
C {devices/lab_pin.sym} 1200 -500 0 0 {name=l38 sig_type=std_logic lab=vfbn}
N 1220 -460 1200 -460 {lab=vcm}
C {devices/lab_pin.sym} 1200 -460 0 0 {name=l39 sig_type=std_logic lab=vcm}
N 1280 -400 1280 -300 {lab=x}
N 1320 -400 1320 -260 {lab=y}
N 1360 -400 1360 -380 {lab=vss}
C {devices/lab_pin.sym} 1360 -380 0 1 {name=l40 sig_type=std_logic lab=vss}
N 380 -300 1720 -300 {lab=x}
C {devices/lab_pin.sym} 380 -300 0 0 {name=l41 sig_type=std_logic lab=x}
N 420 -260 2200 -260 {lab=y}
C {devices/lab_pin.sym} 420 -260 0 0 {name=l42 sig_type=std_logic lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1700 -680 0 0 {name=LP
l=4u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1700 -600 0 0 {name=LPC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1700 -340 0 0 {name=CX
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1700 -200 0 0 {name=SX
l=6u
w=36u
ng=6
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1720 -710 1720 -760 {lab=vdd}
N 1720 -680 1740 -680 {lab=vdd}
N 1740 -680 1740 -760 {lab=vdd}
N 1720 -650 1720 -630 {lab=lp}
C {devices/lab_pin.sym} 1720 -650 0 1 {name=l43 sig_type=std_logic lab=lp}
N 1720 -600 1760 -600 {lab=vdd}
N 1760 -600 1760 -760 {lab=vdd}
N 1680 -680 1660 -680 {lab=vcmfb}
C {devices/lab_pin.sym} 1660 -680 0 0 {name=l44 sig_type=std_logic lab=vcmfb}
N 1680 -600 1660 -600 {lab=vbpc}
C {devices/lab_pin.sym} 1660 -600 0 0 {name=l45 sig_type=std_logic lab=vbpc}
N 1720 -570 1720 -470 {lab=voutp}
N 1720 -470 1720 -370 {lab=voutp}
N 1720 -310 1720 -300 {lab=x}
N 1720 -300 1720 -230 {lab=x}
N 1680 -340 1660 -340 {lab=vbnc}
C {devices/lab_pin.sym} 1660 -340 0 0 {name=l46 sig_type=std_logic lab=vbnc}
N 1680 -200 1660 -200 {lab=vbn}
C {devices/lab_pin.sym} 1660 -200 0 0 {name=l47 sig_type=std_logic lab=vbn}
N 1720 -340 1760 -340 {lab=vss}
N 1760 -340 1760 -100 {lab=vss}
N 1720 -200 1740 -200 {lab=vss}
N 1740 -200 1740 -100 {lab=vss}
N 1720 -170 1720 -100 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2220 -680 0 1 {name=LN
l=4u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2220 -600 0 1 {name=LNC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2220 -340 0 1 {name=CY
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2220 -200 0 1 {name=SY
l=6u
w=36u
ng=6
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 2200 -710 2200 -760 {lab=vdd}
N 2200 -680 2180 -680 {lab=vdd}
N 2180 -680 2180 -760 {lab=vdd}
N 2200 -650 2200 -630 {lab=ln}
C {devices/lab_pin.sym} 2200 -650 0 0 {name=l48 sig_type=std_logic lab=ln}
N 2200 -600 2160 -600 {lab=vdd}
N 2160 -600 2160 -760 {lab=vdd}
N 2240 -680 2260 -680 {lab=vcmfb}
C {devices/lab_pin.sym} 2260 -680 0 1 {name=l49 sig_type=std_logic lab=vcmfb}
N 2240 -600 2260 -600 {lab=vbpc}
C {devices/lab_pin.sym} 2260 -600 0 1 {name=l50 sig_type=std_logic lab=vbpc}
N 2200 -570 2200 -470 {lab=voutn}
N 2200 -470 2200 -370 {lab=voutn}
N 2200 -310 2200 -260 {lab=y}
N 2200 -260 2200 -230 {lab=y}
N 2240 -340 2260 -340 {lab=vbnc}
C {devices/lab_pin.sym} 2260 -340 0 1 {name=l51 sig_type=std_logic lab=vbnc}
N 2240 -200 2260 -200 {lab=vbn}
C {devices/lab_pin.sym} 2260 -200 0 1 {name=l52 sig_type=std_logic lab=vbn}
N 2200 -340 2160 -340 {lab=vss}
N 2160 -340 2160 -100 {lab=vss}
N 2200 -200 2180 -200 {lab=vss}
N 2180 -200 2180 -100 {lab=vss}
N 2200 -170 2200 -100 {lab=vss}
C {devices/lab_pin.sym} 1720 -470 0 0 {name=l53 sig_type=std_logic lab=voutp}
C {devices/lab_pin.sym} 2200 -470 0 1 {name=l54 sig_type=std_logic lab=voutn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1820 -470 0 0 {name=CLP
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 1720 -470 1800 -470 {lab=voutp}
N 1840 -500 1840 -470 {lab=vss}
N 1840 -470 1840 -440 {lab=vss}
N 1840 -440 1840 -100 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2100 -470 0 1 {name=CLN
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 2200 -470 2120 -470 {lab=voutn}
N 2080 -500 2080 -470 {lab=vss}
N 2080 -470 2080 -440 {lab=vss}
N 2080 -440 2080 -100 {lab=vss}
C {unit_r2.sym} 2560 -480 0 0 {name=XM1}
N 2520 -560 2520 -760 {lab=vdd}
N 2600 -560 2600 -580 {lab=vbp}
C {devices/lab_pin.sym} 2600 -580 0 1 {name=l55 sig_type=std_logic lab=vbp}
N 2460 -500 2440 -500 {lab=vfbp}
C {devices/lab_pin.sym} 2440 -500 0 0 {name=l56 sig_type=std_logic lab=vfbp}
N 2460 -460 2440 -460 {lab=vcm}
C {devices/lab_pin.sym} 2440 -460 0 0 {name=l57 sig_type=std_logic lab=vcm}
N 2520 -400 2520 -300 {lab=xc}
N 2560 -400 2560 -260 {lab=yc}
N 2600 -400 2600 -380 {lab=vss}
C {devices/lab_pin.sym} 2600 -380 0 1 {name=l58 sig_type=std_logic lab=vss}
C {unit_r2.sym} 2860 -480 0 0 {name=XM2}
N 2820 -560 2820 -760 {lab=vdd}
N 2900 -560 2900 -580 {lab=vbp}
C {devices/lab_pin.sym} 2900 -580 0 1 {name=l59 sig_type=std_logic lab=vbp}
N 2760 -500 2740 -500 {lab=vfbn}
C {devices/lab_pin.sym} 2740 -500 0 0 {name=l60 sig_type=std_logic lab=vfbn}
N 2760 -460 2740 -460 {lab=vcm}
C {devices/lab_pin.sym} 2740 -460 0 0 {name=l61 sig_type=std_logic lab=vcm}
N 2820 -400 2820 -300 {lab=xc}
N 2860 -400 2860 -260 {lab=yc}
N 2900 -400 2900 -380 {lab=vss}
C {devices/lab_pin.sym} 2900 -380 0 1 {name=l62 sig_type=std_logic lab=vss}
N 2520 -300 3120 -300 {lab=xc}
C {devices/lab_pin.sym} 2520 -300 0 0 {name=l63 sig_type=std_logic lab=xc}
N 2560 -260 3360 -260 {lab=yc}
C {devices/lab_pin.sym} 2560 -260 0 0 {name=l64 sig_type=std_logic lab=yc}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 3100 -680 0 0 {name=D
l=4u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 3100 -600 0 0 {name=DC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3100 -340 0 0 {name=CXC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3100 -200 0 0 {name=SXC
l=6u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 3120 -710 3120 -760 {lab=vdd}
N 3120 -680 3140 -680 {lab=vdd}
N 3140 -680 3140 -760 {lab=vdd}
N 3120 -650 3120 -630 {lab=dd}
C {devices/lab_pin.sym} 3120 -650 0 1 {name=l65 sig_type=std_logic lab=dd}
N 3120 -600 3160 -600 {lab=vdd}
N 3160 -600 3160 -760 {lab=vdd}
N 3080 -600 3060 -600 {lab=vbpc}
C {devices/lab_pin.sym} 3060 -600 0 0 {name=l66 sig_type=std_logic lab=vbpc}
N 3120 -570 3120 -520 {lab=vcmfb}
N 3120 -520 3120 -370 {lab=vcmfb}
N 3120 -520 3040 -520 {lab=vcmfb}
N 3040 -520 3040 -680 {lab=vcmfb}
N 3040 -680 3080 -680 {lab=vcmfb}
C {devices/lab_pin.sym} 3040 -520 0 0 {name=l67 sig_type=std_logic lab=vcmfb}
N 3120 -310 3120 -300 {lab=xc}
N 3120 -300 3120 -230 {lab=xc}
N 3080 -340 3060 -340 {lab=vbnc}
C {devices/lab_pin.sym} 3060 -340 0 0 {name=l68 sig_type=std_logic lab=vbnc}
N 3080 -200 3060 -200 {lab=vbn}
C {devices/lab_pin.sym} 3060 -200 0 0 {name=l69 sig_type=std_logic lab=vbn}
N 3120 -340 3160 -340 {lab=vss}
N 3160 -340 3160 -100 {lab=vss}
N 3120 -200 3140 -200 {lab=vss}
N 3140 -200 3140 -100 {lab=vss}
N 3120 -170 3120 -100 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3380 -340 0 1 {name=CYC
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 3380 -200 0 1 {name=SYC
l=6u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 3360 -370 3360 -760 {lab=vdd}
N 3360 -310 3360 -260 {lab=yc}
N 3360 -260 3360 -230 {lab=yc}
N 3400 -340 3420 -340 {lab=vbnc}
C {devices/lab_pin.sym} 3420 -340 0 1 {name=l70 sig_type=std_logic lab=vbnc}
N 3400 -200 3420 -200 {lab=vbn}
C {devices/lab_pin.sym} 3420 -200 0 1 {name=l71 sig_type=std_logic lab=vbn}
N 3360 -340 3320 -340 {lab=vss}
N 3320 -340 3320 -100 {lab=vss}
N 3360 -200 3340 -200 {lab=vss}
N 3340 -200 3340 -100 {lab=vss}
N 3360 -170 3360 -100 {lab=vss}
T {s2d_mpdda: pad input -> fully differential, voutp - voutn = 2 (vin - vref), (voutp + voutn)/2 = vcm} 60 -960 0 0 0.5 0.5 {}
T {signal units A1 = A2 (vin, vref), F1 (vcm, vfbp), F2 (vfbn, vcm); CMFB units M1 (vfbp, vcm), M2 (vfbn, vcm); all unit_r2: x += f(gp - gn)} 60 -900 0 0 0.3 0.3 {}
T {tie vfbp to voutp and vfbn to voutn; they are pins only so that the loops can be broken in simulation. CLP / CLN: built-in minimum load.} 60 -860 0 0 0.3 0.3 {}
T {sinks SX / SY: 6 fingers of BN (6/6), SXC / SYC: 4 fingers; loads LP / LN mirror the CMFB diode D 1:1; netlist: ../sim/s2d_mpdda.spice} 60 -40 0 0 0.25 0.25 {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 60 0 0 0 0.2 0.2 {}

