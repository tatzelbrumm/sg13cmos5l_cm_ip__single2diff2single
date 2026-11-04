v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sg13cmos5l_IOPadDiff2Single: differential in, single-ended out, class-AB, pad - vref = (vinp - vinn) / 2} 0 -890 0 0 0.5 0.5 {}
T {Custom padframe cell (case (a)): OP / ON are the pad's ESD clamp frames (d2s_out_p, d2s_out_n). Everything runs on the ring rails iovdd / iovss;} 0 -840 0 0 0.3 0.3 {}
T {the 1.2 V core ring vdd is not connected inside the cell; vss joins iovss through the p-substrate (Rsub). vfb is tied to the pad (Kelvin line from the pad junction).} 0 -810 0 0 0.3 0.3 {}
T {Slot fallback: iovdd = vdd_3v3, iovss = vss_3v3, vdd = vdd_1v2, vss = vss_1v2, pad = s7_an[1]. Netlist reference: ../../netlist/source/sg13cmos5l_IOPadDiff2Single.spice} 0 -780 0 0 0.3 0.3 {}
T {Backannotated 2026-11-03 to the drawn cell (C2, layout/klayout, reference netlist pad_candidate.cdl): the cell holds Xd + Xt as drawn; en_ctrl_3v3 (en_3v3, en_3v3_b)} 0 -750 0 0 0.3 0.3 {}
T {and bias_gen_pd (iref) sit next to it (slot, top level, CACE templates). CMA / CMB in v8 polarity, each behind its own 2 kOhm stage [S].} 0 -720 0 0 0.3 0.3 {}
T {[D] class-AB driver with power-down} 1120 -620 0 0 0.3 0.3 {}
C {devices/iopin.sym} 160 -600 0 1 {name=p1 lab=iovdd}
C {devices/iopin.sym} 160 -100 0 1 {name=p2 lab=iovss}
C {devices/iopin.sym} 160 -580 0 1 {name=p3 lab=vdd}
C {devices/iopin.sym} 160 -120 0 1 {name=p4 lab=vss}
C {devices/iopin.sym} 2740 -460 0 0 {name=p5 lab=pad}
C {devices/ipin.sym} 160 -480 0 0 {name=p6 lab=vinp}
C {devices/ipin.sym} 160 -460 0 0 {name=p7 lab=vinn}
C {devices/ipin.sym} 160 -420 0 0 {name=p8 lab=vref}
C {devices/iopin.sym} 160 -320 0 1 {name=p9 lab=iref}
C {devices/ipin.sym} 160 -520 0 0 {name=p10 lab=en_3v3}
C {devices/ipin.sym} 160 -500 0 0 {name=p11 lab=en_3v3_b}
T {vdd: n.c.; vss: tied to iovss by Rsub (the p-substrate)} 200 -575 0 0 0.2 0.2 {}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
N 160 -600 920 -600 {lab=iovdd}
N 920 -600 1180 -600 {lab=iovdd}
N 1180 -600 1400 -600 {lab=iovdd}
N 1180 -600 1180 -560 {lab=iovdd}
N 1400 -600 1400 -560 {lab=iovdd}
N 920 -600 920 -360 {lab=iovdd}
N 160 -100 900 -100 {lab=iovss}
N 900 -100 1160 -100 {lab=iovss}
N 1160 -100 1380 -100 {lab=iovss}
N 1160 -360 1160 -100 {lab=iovss}
N 1380 -360 1380 -100 {lab=iovss}
N 900 -180 900 -100 {lab=iovss}
N 160 -480 1100 -480 {lab=vinp}
N 160 -460 1100 -460 {lab=vinn}
N 160 -420 1100 -420 {lab=vref}
N 160 -520 1100 -520 {lab=en_3v3}
N 160 -500 1100 -500 {lab=en_3v3_b}
N 160 -320 860 -320 {lab=iref}
C {devices/lab_pin.sym} 860 -300 0 0 {name=l_xt_en sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 860 -280 0 0 {name=l_xt_enb sig_type=std_logic lab=en_3v3_b}
C {bias_tree_pd.sym} 960 -270 0 0 {name=xt}
C {d2s_mpdda_pd.sym} 1280 -460 0 0 {name=xd}
N 1220 -360 1220 -320 {lab=vbp}
N 1060 -320 1220 -320 {lab=vbp}
C {devices/lab_pin.sym} 1220 -320 0 1 {name=l47 sig_type=std_logic lab=vbp}
N 1240 -360 1240 -300 {lab=vbpc}
N 1060 -300 1240 -300 {lab=vbpc}
C {devices/lab_pin.sym} 1240 -300 0 1 {name=l49 sig_type=std_logic lab=vbpc}
N 1260 -360 1260 -280 {lab=vabp}
N 1060 -280 1260 -280 {lab=vabp}
C {devices/lab_pin.sym} 1260 -280 0 1 {name=l51 sig_type=std_logic lab=vabp}
N 1300 -360 1300 -260 {lab=vabn}
N 1060 -260 1300 -260 {lab=vabn}
C {devices/lab_pin.sym} 1300 -260 0 1 {name=l52 sig_type=std_logic lab=vabn}
N 1320 -360 1320 -240 {lab=vbnc}
N 1060 -240 1320 -240 {lab=vbnc}
C {devices/lab_pin.sym} 1320 -240 0 1 {name=l50 sig_type=std_logic lab=vbnc}
N 1340 -360 1340 -220 {lab=vbn}
N 1060 -220 1340 -220 {lab=vbn}
C {devices/lab_pin.sym} 1340 -220 0 1 {name=l48 sig_type=std_logic lab=vbn}
N 1460 -520 1540 -520 {lab=dabp}
N 1540 -520 1540 -720 {lab=dabp}
N 1540 -720 1700 -720 {lab=dabp}
N 1460 -500 1560 -500 {lab=a}
N 1560 -500 1560 -700 {lab=a}
N 1560 -700 1700 -700 {lab=a}
N 1560 -580 1940 -580 {lab=a}
N 1460 -420 1560 -420 {lab=b}
N 1560 -420 1560 -200 {lab=b}
N 1560 -200 1700 -200 {lab=b}
N 1560 -300 1940 -300 {lab=b}
N 1940 -310 1940 -300 {lab=b}
N 1460 -400 1540 -400 {lab=dabn}
N 1540 -400 1540 -180 {lab=dabn}
N 1540 -180 1700 -180 {lab=dabn}
C {devices/lab_wire.sym} 1600 -580 0 0 {name=l_a sig_type=std_logic lab=a}
C {devices/lab_wire.sym} 1600 -300 0 0 {name=l_b sig_type=std_logic lab=b}
C {devices/lab_wire.sym} 1600 -720 0 0 {name=l_dabp sig_type=std_logic lab=dabp}
C {devices/lab_wire.sym} 1600 -180 0 0 {name=l_dabn sig_type=std_logic lab=dabn}
N 1460 -460 1500 -460 {lab=pad}
C {devices/lab_pin.sym} 1500 -460 0 1 {name=l_vfb sig_type=std_logic lab=pad}
C {d2s_out_p.sym} 1780 -700 0 0 {name=xfp}
N 1780 -760 1780 -780 {lab=iovdd}
C {devices/lab_pin.sym} 1780 -780 0 1 {name=xlrp sig_type=std_logic lab=iovdd}
C {d2s_out_n.sym} 1780 -200 0 0 {name=xfn}
N 1780 -140 1780 -120 {lab=iovss}
C {devices/lab_pin.sym} 1780 -120 0 1 {name=xlrn sig_type=std_logic lab=iovss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1960 -580 0 0 {name=CMA
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1980 -610 1980 -580 {lab=pa}
N 1980 -580 1980 -550 {lab=pa}
N 1980 -580 2080 -580 {lab=pa}
C {devices/lab_wire.sym} 2070 -580 0 0 {name=l_pa sig_type=std_logic lab=pa}
C {d2s_sp2k.sym} 2160 -580 0 1 {name=XSPA}
N 2160 -660 2160 -680 {lab=iovdd}
C {devices/lab_pin.sym} 2160 -680 0 1 {name=l_spa_vdd sig_type=std_logic lab=iovdd}
N 2160 -500 2160 -480 {lab=iovss}
C {devices/lab_pin.sym} 2160 -480 0 1 {name=l_spa_vss sig_type=std_logic lab=iovss}
N 2240 -580 2440 -580 {lab=pad}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1960 -340 0 1 {name=CMB
l=32.16u
w=7.96u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
N 1940 -370 1940 -340 {lab=b}
N 1940 -340 1940 -310 {lab=b}
N 1980 -340 2080 -340 {lab=pb}
C {devices/lab_wire.sym} 2040 -340 0 0 {name=l_pb sig_type=std_logic lab=pb}
C {d2s_sp2k.sym} 2160 -340 0 1 {name=XSPB}
N 2160 -420 2160 -440 {lab=iovdd}
C {devices/lab_pin.sym} 2160 -440 0 1 {name=l_spb_vdd sig_type=std_logic lab=iovdd}
N 2160 -260 2160 -240 {lab=iovss}
C {devices/lab_pin.sym} 2160 -240 0 1 {name=l_spb_vss sig_type=std_logic lab=iovss}
N 2240 -340 2440 -340 {lab=pad}
N 1860 -700 2440 -700 {lab=pad}
N 1860 -200 2440 -200 {lab=pad}
N 2440 -700 2440 -200 {lab=pad}
N 2440 -460 2740 -460 {lab=pad}
N 2440 -620 2600 -620 {lab=pad}
C {sg13cmos5l_pr/dpantenna.sym} 2600 -650 0 0 {name=DP0
model=dpantenna
l=65.8u
w=1.26u
spiceprefix=X}
C {sg13cmos5l_pr/dpantenna.sym} 2680 -650 0 0 {name=DP1
model=dpantenna
l=65.8u
w=1.26u
spiceprefix=X}
C {devices/lab_pin.sym} 2680 -620 0 1 {name=lDP1a sig_type=std_logic lab=pad}
C {devices/lab_pin.sym} 2680 -680 0 1 {name=lDP1c sig_type=std_logic lab=iovdd}
N 2600 -680 2600 -700 {lab=iovdd}
C {devices/lab_pin.sym} 2600 -700 0 1 {name=l43 sig_type=std_logic lab=iovdd}
N 2440 -300 2600 -300 {lab=pad}
C {sg13cmos5l_pr/dantenna.sym} 2600 -270 0 0 {name=DN0
model=dantenna
l=67.6u
w=1.26u
spiceprefix=X}
C {sg13cmos5l_pr/dantenna.sym} 2680 -270 0 0 {name=DN1
model=dantenna
l=67.6u
w=1.26u
spiceprefix=X}
C {devices/lab_pin.sym} 2680 -240 0 1 {name=lDN1a sig_type=std_logic lab=iovss}
C {devices/lab_pin.sym} 2680 -300 0 1 {name=lDN1c sig_type=std_logic lab=pad}
N 2600 -240 2600 -220 {lab=iovss}
C {devices/lab_pin.sym} 2600 -220 0 1 {name=l46 sig_type=std_logic lab=iovss}
T {[O] output stage: d2s_out_p = the P clamp frame (OP, replica RP1, dummy RPD), d2s_out_n = the two N clamp frames (ON, replica RN1);} 1600 -870 0 0 0.3 0.3 {}
T {    Miller capacitors CMA (gate a; S, D, well on pa) and CMB (gate on pb; S, D, well on b), hv PMOS 7.96u x 32.16u as drawn (v8 polarity)} 1600 -845 0 0 0.3 0.3 {}
T {[S] 2 kOhm secondary stages d2s_sp2k (rppd 1u x 7.435u, dantenna, dpantenna), pad -> pa and pad -> pb} 1600 -820 0 0 0.3 0.3 {}
T {[P] IHP primary diodes DCPDiode / DCNDiode as drawn: 2 stripes 1.26u x 65.8u / 67.6u each (IHP's cell: 27.78u)} 2520 -770 0 0 0.3 0.3 {}
N 160 -120 300 -120 {lab=vss}
C {devices/res.sym} 330 -120 1 0 {name=Rsub
value=1
footprint=1206
device=resistor
lvs_ignore=open
m=1}
C {devices/lab_pin.sym} 360 -120 0 1 {name=l_rsub sig_type=std_logic lab=iovss}
T {Rsub: vss and iovss share the p-substrate. The vss band p+ tie (edge contract, as in IOPadAnalog) and the iovss ties sit in one
substrate, so LVS with --disable_tap_extraction (sak-lvs.sh) and magic see one net (Christoph, 2026-11-03: 2(a)).
Simulation: 1 Ohm, a stand-in for the substrate path. LVS netlists (lvs_ignore=1): left out (open). A SPICE subckt cannot
join two ports, and xschem refuses to short two port nets (Error 10). The layout has no top vss text, so both LVS see iovss.} 390 -190 0 0 0.2 0.2 {}
