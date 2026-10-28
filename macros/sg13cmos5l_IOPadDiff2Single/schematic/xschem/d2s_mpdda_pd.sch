v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 190 -895 1170 -895 1170 -685 190 -685 190 -895 {dash=6}
P 10 5 1225 -565 1385 -565 1385 -285 1225 -285 1225 -565 {dash=6}
P 10 5 2080 -565 2255 -565 2255 -285 2080 -285 2080 -565 {dash=6}
P 10 5 1510 -1140 1970 -1140 1970 -895 1510 -895 1510 -1140 {dash=6}
P 10 5 1855 -855 2255 -855 2255 -730 1855 -730 1855 -855 {dash=6}
P 10 5 1220 -855 1635 -855 1635 -730 1220 -730 1220 -855 {dash=6}
P 10 5 1140 -1260 1290 -1260 1290 -1170 1140 -1170 1140 -1260 {dash=6}
P 10 5 2200 -1260 2350 -1260 2350 -1170 2200 -1170 2200 -1260 {dash=6}
P 10 5 115 -250 270 -250 270 -160 115 -160 115 -250 {dash=6}
P 10 5 2200 -250 2350 -250 2350 -160 2200 -160 2200 -250 {dash=6}
T {[1]} 195 -891 0 0 0.35 0.35 {layer=10}
T {[2]} 1395 -540 0 0 0.35 0.35 {layer=10}
T {[2]} 2040 -540 0 0 0.35 0.35 {layer=10}
T {[3]} 1510 -1165 0 0 0.35 0.35 {layer=10}
T {[4]} 1860 -878 0 0 0.35 0.35 {layer=10}
T {[5]} 1225 -878 0 0 0.35 0.35 {layer=10}
T {d2s_mpdda_pd: matched-pair DDA (4 x unit_r2), folded cascode, class-AB drive of the output gates a / b, digital enable en_3v3 / en_3v3_b} 0 -1440 0 0 0.6 0.6 {}
T {frozen .subckt defaults: lcas = 3 (CX, CY, PCL, PCR 30u / 3u ng=2), rl = 50.6u (in unit_r2.sch)} 0 -1390 0 0 0.3 0.3 {}
T {d2s_mpdda (../../improvements/xschem) plus the [E] switches; unit_r2.sym from ../../improvements/xschem; block descriptions: README.md there and here} 0 -1365 0 0 0.3 0.3 {}
T {[1] DDA units A, B, C1, C2: split-tail PMOS pair, rhigh between the sources. Each adds f(gp - gn) to the fold nodes: the gp device drains to y, the gn device to x.} 1250 -110 0 0 0.3 0.3 {layer=10}
T {      A: vinp - vref,  B: vref - vinn,  C1 = C2: vref - vfb.  The loop forces f(vinp - vref) + f(vref - vinn) = 2 f(vfb - vref), so vfb - vref = (vinp - vinn)/2.} 1250 -86 0 0 0.3 0.3 {layer=10}
T {[2] fold: sinks SX, SY (gate vbn) and NMOS cascodes CX, CY (gate vbnc). x and y are the fold nodes.} 1250 -62 0 0 0.3 0.3 {layer=10}
T {[3] PMOS cascoded mirror: PL, PCL is the input side (gates tied to l2), PR, PCR the output side into node a. Cascode gates vbpc.} 1250 -38 0 0 0.3 0.3 {layer=10}
T {[4] class-AB control: ABP (gate vabp) and ABN (gate vabn) between a and b. With RP2 / RN2 [8] and the replicas RP1 / RN1 at pad level it sets the quiescent current of OP and ON.} 1250 -14 0 0 0.3 0.3 {layer=10}
T {[5] FPL, FNL: copy of [4] in the mirror input branch (between l2 and l1), so both fold branches carry the same element.} 1250 10 0 0 0.3 0.3 {layer=10}
T {[6] the output devices OP / ON, their replicas RP1 / RN1 (dabp / dabn) and the dummy RPD are at pad level since 2026-10-28: d2s_out_p, d2s_out_n (the clamp frames).} 1250 34 0 0 0.3 0.3 {layer=10}
T {[7] the Miller capacitors CMA (a to the pad) and CMB (pad to b) are at pad level since 2026-10-28, in the gap between the diodes. vfb is the feedback input (the pad).} 1250 58 0 0 0.3 0.3 {layer=10}
T {[E]} 1145 -1258 0 0 0.25 0.25 {layer=10}
T {[E]} 2205 -1258 0 0 0.25 0.25 {layer=10}
T {[E]} 120 -177 0 0 0.25 0.25 {layer=10}
T {[E]} 2205 -177 0 0 0.25 0.25 {layer=10}
T {[E] enable, en_3v3 (0 ... 3.3 V on vdd / vss, active high); en_3v3_b from en_ctrl_3v3. Disabled: SA pulls a to vddo and SB pulls b to vsso, so OP and ON (pad level) are off} 1250 82 0 0 0.3 0.3 {layer=10}
T {      with their gates on their sources, as in a clamp; SABP pulls vabp to vdd and SABN pulls vabn to vss, so ABP / ABN cannot conduct from one pull} 1250 106 0 0 0.3 0.3 {layer=10}
T {      into the other. Enabled: the four switches are off and the cell is d2s_mpdda.} 1250 130 0 0 0.3 0.3 {layer=10}
P 10 5 2320 -1060 2520 -1060 2520 -900 2320 -900 2320 -1060 {dash=6}
P 10 5 2320 -680 2520 -680 2520 -520 2320 -520 2320 -680 {dash=6}
T {[8]} 2325 -1083 0 0 0.35 0.35 {layer=10}
T {[8]} 2325 -703 0 0 0.35 0.35 {layer=10}
N 300 -1280 300 -860 {lab=vdd}
N 380 -1040 380 -860 {lab=vbp}
N 300 -700 300 -460 {lab=x}
N 340 -700 340 -420 {lab=y}
N 380 -700 380 -140 {lab=vss}
N 200 -800 200 -680 {lab=vinp}
N 200 -800 240 -800 {lab=vinp}
N 220 -760 220 -640 {lab=vref}
N 220 -760 240 -760 {lab=vref}
N 540 -1280 540 -860 {lab=vdd}
N 620 -1040 620 -860 {lab=vbp}
N 540 -700 540 -460 {lab=x}
N 580 -700 580 -420 {lab=y}
N 620 -700 620 -140 {lab=vss}
N 440 -800 440 -640 {lab=vref}
N 440 -800 480 -800 {lab=vref}
N 460 -760 460 -660 {lab=vinn}
N 460 -760 480 -760 {lab=vinn}
N 780 -1280 780 -860 {lab=vdd}
N 860 -1040 860 -860 {lab=vbp}
N 780 -700 780 -460 {lab=x}
N 820 -700 820 -420 {lab=y}
N 860 -700 860 -140 {lab=vss}
N 680 -800 680 -640 {lab=vref}
N 680 -800 720 -800 {lab=vref}
N 700 -760 700 -620 {lab=vfb}
N 700 -760 720 -760 {lab=vfb}
N 1020 -1280 1020 -860 {lab=vdd}
N 1100 -1040 1100 -860 {lab=vbp}
N 1020 -700 1020 -460 {lab=x}
N 1060 -700 1060 -420 {lab=y}
N 1100 -700 1100 -140 {lab=vss}
N 920 -800 920 -640 {lab=vref}
N 920 -800 960 -800 {lab=vref}
N 940 -760 940 -620 {lab=vfb}
N 940 -760 960 -760 {lab=vfb}
N 100 -680 200 -680 {lab=vinp}
N 100 -640 220 -640 {lab=vref}
N 100 -660 460 -660 {lab=vinn}
N 100 -620 700 -620 {lab=vfb}
N 100 -1040 380 -1040 {lab=vbp}
N 300 -460 540 -460 {lab=x}
N 340 -420 580 -420 {lab=y}
N 1300 -780 1320 -780 {lab=vss}
N 1300 -520 1320 -520 {lab=vss}
N 1300 -340 1320 -340 {lab=vss}
N 1300 -310 1300 -140 {lab=vss}
N 1300 -750 1300 -720 {lab=l1}
N 1300 -720 1560 -720 {lab=l1}
N 1560 -750 1560 -720 {lab=l1}
N 1540 -1100 1560 -1100 {lab=vdd}
N 1540 -940 1560 -940 {lab=vdd}
N 1540 -780 1560 -780 {lab=vdd}
N 1540 -1280 1540 -1100 {lab=vdd}
N 1560 -1280 1560 -1130 {lab=vdd}
N 1560 -1070 1560 -970 {lab=pl}
N 1560 -910 1560 -840 {lab=l2}
N 1560 -840 1560 -810 {lab=l2}
N 1300 -840 1300 -810 {lab=l2}
N 1300 -840 1560 -840 {lab=l2}
N 1740 -1100 1740 -840 {lab=l2}
N 1600 -1100 1740 -1100 {lab=l2}
N 1920 -1100 1940 -1100 {lab=vdd}
N 1920 -940 1940 -940 {lab=vdd}
N 1920 -780 1940 -780 {lab=vdd}
N 1940 -1280 1940 -1100 {lab=vdd}
N 1920 -1280 1920 -1130 {lab=vdd}
N 1920 -1070 1920 -970 {lab=pr}
N 2160 -780 2180 -780 {lab=vss}
N 2160 -520 2180 -520 {lab=vss}
N 2160 -340 2180 -340 {lab=vss}
N 2160 -310 2160 -140 {lab=vss}
N 1920 -910 1920 -860 {lab=a}
N 1920 -860 2160 -860 {lab=a}
N 2160 -860 2160 -810 {lab=a}
N 1920 -750 1920 -720 {lab=b}
N 1920 -720 2160 -720 {lab=b}
N 2160 -750 2160 -720 {lab=b}
N 2160 -720 2160 -550 {lab=b}
N 2260 -720 2260 -640 {lab=b}
N 100 -900 1620 -900 {lab=vbpc}
N 1860 -940 1860 -900 {lab=vbpc}
N 1860 -940 1880 -940 {lab=vbpc}
N 1620 -940 1620 -900 {lab=vbpc}
N 1600 -940 1620 -940 {lab=vbpc}
N 1740 -780 1740 -600 {lab=vabp}
N 1600 -780 1740 -780 {lab=vabp}
N 2100 -780 2100 -580 {lab=vabn}
N 2100 -780 2120 -780 {lab=vabn}
N 1240 -780 1240 -580 {lab=vabn}
N 1240 -780 1260 -780 {lab=vabn}
N 100 -560 1240 -560 {lab=vbnc}
N 2100 -520 2120 -520 {lab=vbnc}
N 1240 -560 1240 -520 {lab=vbnc}
N 1240 -520 1260 -520 {lab=vbnc}
N 100 -380 1240 -380 {lab=vbn}
N 2100 -380 2100 -340 {lab=vbn}
N 2100 -340 2120 -340 {lab=vbn}
N 1240 -380 1240 -340 {lab=vbn}
N 1240 -340 1260 -340 {lab=vbn}
N 680 -640 920 -640 {lab=vref}
N 220 -640 440 -640 {lab=vref}
N 700 -620 940 -620 {lab=vfb}
N 860 -1040 1100 -1040 {lab=vbp}
N 380 -1040 620 -1040 {lab=vbp}
N 540 -460 780 -460 {lab=x}
N 820 -420 1060 -420 {lab=y}
N 580 -420 820 -420 {lab=y}
N 1300 -460 1300 -370 {lab=x}
N 1300 -720 1300 -550 {lab=l1}
N 1540 -1100 1540 -940 {lab=vdd}
N 1740 -1100 1880 -1100 {lab=l2}
N 1940 -1100 1940 -940 {lab=vdd}
N 2180 -340 2180 -140 {lab=vss}
N 2160 -420 2160 -370 {lab=y}
N 1920 -860 1920 -810 {lab=a}
N 2160 -720 2260 -720 {lab=b}
N 2260 -640 2260 -340 {lab=b}
N 1620 -900 1860 -900 {lab=vbpc}
N 1240 -560 2100 -560 {lab=vbnc}
N 1240 -380 2100 -380 {lab=vbn}
N 440 -640 680 -640 {lab=vref}
N 620 -1040 860 -1040 {lab=vbp}
N 1020 -460 1300 -460 {lab=x}
N 780 -460 1020 -460 {lab=x}
N 1060 -420 2160 -420 {lab=y}
N 1540 -940 1540 -780 {lab=vdd}
N 1560 -840 1740 -840 {lab=l2}
N 1940 -940 1940 -780 {lab=vdd}
N 2160 -860 2260 -860 {lab=a}
N 100 -1280 300 -1280 {lab=vdd}
N 300 -1280 540 -1280 {lab=vdd}
N 540 -1280 780 -1280 {lab=vdd}
N 780 -1280 1020 -1280 {lab=vdd}
N 1020 -1280 1200 -1280 {lab=vdd}
N 1200 -1280 1220 -1280 {lab=vdd}
N 1220 -1280 1540 -1280 {lab=vdd}
N 1540 -1280 1560 -1280 {lab=vdd}
N 1560 -1280 1920 -1280 {lab=vdd}
N 1920 -1280 1940 -1280 {lab=vdd}
N 100 -1300 2260 -1300 {lab=vddo}
N 2260 -1300 2280 -1300 {lab=vddo}
N 100 -140 180 -140 {lab=vss}
N 180 -140 200 -140 {lab=vss}
N 200 -140 380 -140 {lab=vss}
N 380 -140 620 -140 {lab=vss}
N 620 -140 860 -140 {lab=vss}
N 860 -140 1100 -140 {lab=vss}
N 1100 -140 1300 -140 {lab=vss}
N 1300 -140 1320 -140 {lab=vss}
N 1320 -140 2160 -140 {lab=vss}
N 2160 -140 2180 -140 {lab=vss}
N 100 -120 2260 -120 {lab=vsso}
N 2260 -120 2280 -120 {lab=vsso}
N 2260 -1100 2260 -860 {lab=a}
N 1320 -340 1320 -140 {lab=vss}
N 1240 -580 2100 -580 {lab=vabn}
N 1740 -780 1880 -780 {lab=vabp}
N 100 -580 180 -580 {lab=vabn}
N 180 -580 1240 -580 {lab=vabn}
N 100 -600 1200 -600 {lab=vabp}
N 1200 -600 1740 -600 {lab=vabp}
N 100 -1160 1160 -1160 {lab=en_3v3}
N 1160 -1160 2220 -1160 {lab=en_3v3}
N 100 -260 140 -260 {lab=en_3v3_b}
N 140 -260 2220 -260 {lab=en_3v3_b}
N 1200 -1280 1200 -1240 {lab=vdd}
N 1200 -1210 1220 -1210 {lab=vdd}
N 1220 -1280 1220 -1210 {lab=vdd}
N 1160 -1210 1160 -1160 {lab=en_3v3}
N 1200 -1180 1200 -600 {lab=vabp}
N 2260 -1300 2260 -1240 {lab=vddo}
N 2260 -1210 2280 -1210 {lab=vddo}
N 2280 -1300 2280 -1210 {lab=vddo}
N 2220 -1210 2220 -1160 {lab=en_3v3}
N 2260 -1180 2260 -1100 {lab=a}
N 180 -180 180 -140 {lab=vss}
N 180 -210 200 -210 {lab=vss}
N 200 -210 200 -140 {lab=vss}
N 140 -260 140 -210 {lab=en_3v3_b}
N 180 -580 180 -240 {lab=vabn}
N 2260 -180 2260 -120 {lab=vsso}
N 2260 -210 2280 -210 {lab=vsso}
N 2280 -210 2280 -120 {lab=vsso}
N 2220 -260 2220 -210 {lab=en_3v3_b}
N 2260 -340 2260 -240 {lab=b}
N 2180 -780 2180 -520 {lab=vss}
N 2100 -560 2100 -520 {lab=vbnc}
N 2180 -520 2180 -340 {lab=vss}
N 1320 -780 1320 -520 {lab=vss}
N 1320 -520 1320 -340 {lab=vss}
N 2160 -490 2160 -420 {lab=y}
N 1300 -490 1300 -460 {lab=x}
C {devices/iopin.sym} 100 -1280 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 100 -140 0 1 {name=p2 lab=vss}
C {devices/iopin.sym} 100 -1300 0 1 {name=p14 lab=vddo}
C {devices/iopin.sym} 100 -120 0 1 {name=p15 lab=vsso}
C {devices/ipin.sym} 100 -680 0 0 {name=p3 lab=vinp}
C {devices/ipin.sym} 100 -660 0 0 {name=p4 lab=vinn}
C {devices/ipin.sym} 100 -640 0 0 {name=p5 lab=vref}
C {devices/ipin.sym} 100 -620 0 0 {name=p7 lab=vfb}
C {devices/ipin.sym} 100 -1040 0 0 {name=p8 lab=vbp}
C {devices/ipin.sym} 100 -380 0 0 {name=p9 lab=vbn}
C {devices/ipin.sym} 100 -900 0 0 {name=p10 lab=vbpc}
C {devices/ipin.sym} 100 -560 0 0 {name=p11 lab=vbnc}
C {devices/ipin.sym} 100 -600 0 0 {name=p12 lab=vabp}
C {devices/ipin.sym} 100 -580 0 0 {name=p13 lab=vabn}
C {unit_r2.sym} 340 -780 0 0 {name=XA}
C {unit_r2.sym} 580 -780 0 0 {name=XB}
C {unit_r2.sym} 820 -780 0 0 {name=XC1}
C {unit_r2.sym} 1060 -780 0 0 {name=XC2}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 -780 0 0 {name=FNL
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 -520 0 0 {name=CX
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1280 -340 0 0 {name=SX
l=6u
w=36u
ng=4
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1580 -1100 0 1 {name=PL
l=4u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1580 -940 0 1 {name=PCL
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1580 -780 0 1 {name=FPL
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1900 -1100 0 0 {name=PR
l=4u
w=24u
ng=4
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1900 -940 0 0 {name=PCR
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1900 -780 0 0 {name=ABP
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2140 -780 0 0 {name=ABN
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2140 -520 0 0 {name=CY
l=3u
w=30u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2140 -340 0 0 {name=SY
l=6u
w=36u
ng=4
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/lab_wire.sym} 1200 -460 0 0 {name=l1 sig_type=std_logic lab=x}
C {devices/lab_wire.sym} 1200 -420 0 0 {name=l2 sig_type=std_logic lab=y}
C {devices/lab_wire.sym} 1440 -720 0 0 {name=l3 sig_type=std_logic lab=l1}
C {devices/lab_wire.sym} 1440 -840 0 0 {name=l4 sig_type=std_logic lab=l2}
C {devices/lab_wire.sym} 1560 -1020 0 0 {name=l5 sig_type=std_logic lab=pl}
C {devices/lab_wire.sym} 1920 -1020 0 1 {name=l6 sig_type=std_logic lab=pr}
C {devices/lab_wire.sym} 2040 -860 0 0 {name=l7 sig_type=std_logic lab=a}
C {devices/lab_wire.sym} 2040 -720 0 0 {name=l8 sig_type=std_logic lab=b}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
C {devices/ipin.sym} 100 -1160 0 0 {name=p16 lab=en_3v3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1180 -1210 0 0 {name=SABP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2240 -1210 0 0 {name=SA
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 160 -210 0 0 {name=SABN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2240 -210 0 0 {name=SB
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/ipin.sym} 100 -260 0 0 {name=p17 lab=en_3v3_b}
N 2260 -860 2600 -860 {lab=a}
N 2260 -720 2600 -720 {lab=b}
C {devices/opin.sym} 2600 -860 0 0 {name=p6 lab=a}
C {devices/opin.sym} 2600 -720 0 0 {name=p18 lab=b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 2400 -980 0 0 {name=RP2
l=0.6u
w=6.66u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 2380 -980 2380 -950 {lab=vabp}
N 2380 -950 2420 -950 {lab=vabp}
N 2420 -950 2420 -920 {lab=vabp}
C {devices/lab_pin.sym} 2420 -920 1 1 {name=l80 sig_type=std_logic lab=vabp}
N 2420 -980 2460 -980 {lab=vdd}
C {devices/lab_pin.sym} 2460 -980 2 0 {name=l81 sig_type=std_logic lab=vdd}
N 2420 -1010 2600 -1010 {lab=dabp}
C {devices/iopin.sym} 2600 -1010 0 0 {name=p19 lab=dabp}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2400 -600 0 0 {name=RN2
l=1u
w=4.4u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
N 2380 -600 2380 -630 {lab=vabn}
N 2380 -630 2420 -630 {lab=vabn}
N 2420 -630 2420 -660 {lab=vabn}
C {devices/lab_pin.sym} 2420 -660 3 1 {name=l82 sig_type=std_logic lab=vabn}
N 2420 -600 2460 -600 {lab=vss}
C {devices/lab_pin.sym} 2460 -600 2 0 {name=l83 sig_type=std_logic lab=vss}
N 2420 -570 2600 -570 {lab=dabn}
C {devices/iopin.sym} 2600 -570 0 0 {name=p20 lab=dabn}
T {[8] RP2 / RN2: the upper halves of the class-AB diode stacks (with FPL / ABP and FNL / ABN the AB groups of layout_primitives P7); their sources dabp / dabn go to RP1 / RN1 in the clamp frames.} 1250 154 0 0 0.3 0.3 {layer=10}
