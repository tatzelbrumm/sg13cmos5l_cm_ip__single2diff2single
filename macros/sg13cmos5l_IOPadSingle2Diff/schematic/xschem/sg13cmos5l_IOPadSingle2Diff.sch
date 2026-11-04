v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {sg13cmos5l_IOPadSingle2Diff: single-ended pad in, differential out, outp - vcm = vcm - outn = pad - vref} 0 -1080 0 0 0.5 0.5 {}
T {Custom padframe cell. Everything runs on the ring rails iovdd / iovss; the 1.2 V core ring vdd is not connected inside the cell; vss joins iovss through the p-substrate (Rsub).} 0 -1030 0 0 0.3 0.3 {}
T {xa = s2d_mpdda_pd, the matched-pair DDA input buffer (gain 2, vfbp / vfbn tied to outp / outn); xt = bias_tree_noab_pd. Netlist reference: ../../netlist/source/sg13cmos5l_IOPadSingle2Diff.spice} 0 -1000 0 0 0.3 0.3 {}
T {Backannotated 2026-11-04 to the drawn cell (C3, layout/klayout, reference netlist pad_candidate.cdl): the cell holds xa + xt + xp as drawn; en_ctrl_3v3 (en_3v3, en_3v3_b)} 0 -970 0 0 0.3 0.3 {}
T {and bias_gen_pd (iref) sit next to it (slot, top level, CACE templates). No secondary protection: the buffer's vin is the pad. Primary protection xp = s2d_pad_esd, as drawn.} 0 -940 0 0 0.3 0.3 {}
T {[P] primary protection as drawn} 580 -880 0 0 0.3 0.3 {layer=10}
T {xp = s2d_pad_esd: clamps MCP / MCN with their rppd gate ties RP / RN (bodies on iovss),} 200 -660 0 0 0.2 0.2 {}
T {diodes DP1 / DP2 (pad -> iovdd), DN1 / DN2 (iovss -> pad), 1.26u x 27.78u each} 200 -640 0 0 0.2 0.2 {}
T {[B] bias} 960 -400 0 0 0.3 0.3 {layer=10}
T {[A] input buffer s2d_mpdda_pd} 1270 -640 0 0 0.3 0.3 {layer=10}
C {devices/iopin.sym} 140 -900 0 1 {name=p1 lab=iovdd}
C {devices/iopin.sym} 140 -100 0 1 {name=p2 lab=iovss}
C {devices/iopin.sym} 140 -880 0 1 {name=p3 lab=vdd}
C {devices/iopin.sym} 140 -120 0 1 {name=p4 lab=vss}
C {devices/iopin.sym} 140 -700 0 1 {name=p5 lab=pad}
C {devices/opin.sym} 1660 -500 0 0 {name=p6 lab=outp}
C {devices/opin.sym} 1660 -460 0 0 {name=p7 lab=outn}
C {devices/ipin.sym} 140 -540 0 0 {name=p8 lab=vcm}
C {devices/ipin.sym} 140 -460 0 0 {name=p9 lab=vref}
C {devices/iopin.sym} 140 -320 0 1 {name=p10 lab=iref}
C {devices/ipin.sym} 140 -420 0 0 {name=p11 lab=en_3v3}
C {devices/ipin.sym} 140 -400 0 0 {name=p12 lab=en_3v3_b}
T {vdd: n.c.} 180 -875 0 0 0.2 0.2 {}
C {devices/title.sym} 160 -40 0 0 {name=l_title author="Christoph Maier"}
N 140 -900 1040 -900 {lab=iovdd}
N 1040 -900 1420 -900 {lab=iovdd}
N 1420 -900 1420 -600 {lab=iovdd}
N 1040 -900 1040 -360 {lab=iovdd}
N 140 -100 1020 -100 {lab=iovss}
N 1020 -100 1400 -100 {lab=iovss}
N 1400 -360 1400 -100 {lab=iovss}
N 1020 -180 1020 -100 {lab=iovss}
N 140 -700 1320 -700 {lab=pad}
N 1320 -700 1320 -500 {lab=pad}
N 1320 -500 1340 -500 {lab=pad}
C {devices/lab_wire.sym} 1240 -700 0 0 {name=l_pad sig_type=std_logic lab=pad}
N 140 -540 1340 -540 {lab=vcm}
N 140 -460 1340 -460 {lab=vref}
N 140 -420 1340 -420 {lab=en_3v3}
N 140 -400 1340 -400 {lab=en_3v3_b}
N 140 -320 980 -320 {lab=iref}
C {devices/lab_pin.sym} 980 -300 0 0 {name=l_xt_en sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 980 -280 0 0 {name=l_xt_enb sig_type=std_logic lab=en_3v3_b}
C {bias_tree_noab_pd.sym} 1080 -270 0 0 {name=xt}
C {s2d_mpdda_pd.sym} 1480 -480 0 0 {name=xa}
N 1460 -360 1460 -320 {lab=vbp}
N 1180 -320 1460 -320 {lab=vbp}
C {devices/lab_pin.sym} 1460 -320 0 1 {name=l54 sig_type=std_logic lab=vbp}
N 1480 -360 1480 -300 {lab=vbpc}
N 1180 -300 1480 -300 {lab=vbpc}
C {devices/lab_pin.sym} 1480 -300 0 1 {name=l56 sig_type=std_logic lab=vbpc}
N 1520 -360 1520 -240 {lab=vbnc}
N 1180 -240 1520 -240 {lab=vbnc}
C {devices/lab_pin.sym} 1520 -240 0 1 {name=l57 sig_type=std_logic lab=vbnc}
N 1540 -360 1540 -220 {lab=vbn}
N 1180 -220 1540 -220 {lab=vbn}
C {devices/lab_pin.sym} 1540 -220 0 1 {name=l55 sig_type=std_logic lab=vbn}
N 1620 -500 1640 -500 {lab=outp}
N 1640 -500 1660 -500 {lab=outp}
N 1640 -520 1640 -500 {lab=outp}
N 1620 -520 1640 -520 {lab=outp}
N 1620 -460 1640 -460 {lab=outn}
N 1640 -460 1660 -460 {lab=outn}
N 1620 -440 1640 -440 {lab=outn}
N 1640 -460 1640 -440 {lab=outn}
C {s2d_pad_esd.sym} 640 -780 0 0 {name=xp}
N 560 -820 560 -900 {lab=iovdd}
N 560 -740 520 -740 {lab=iovss}
C {devices/lab_pin.sym} 520 -740 0 0 {name=l_xp_vss sig_type=std_logic lab=iovss}
N 720 -780 760 -780 {lab=pad}
N 760 -780 760 -700 {lab=pad}
N 140 -120 300 -120 {lab=vss}
C {devices/res.sym} 330 -120 1 0 {name=Rsub
value=1
footprint=1206
device=resistor
lvs_ignore=open
m=1}
C {devices/lab_pin.sym} 360 -120 0 1 {name=l_rsub sig_type=std_logic lab=iovss}
T {Rsub: vss and iovss share the p-substrate (as sg13cmos5l_IOPadDiff2Single,
Christoph 2026-11-03: 2(a)). The layout has no top vss text, so LVS
(--disable_tap_extraction) and magic see one net. Simulation: 1 Ohm, a stand-in
for the substrate path. LVS netlists (lvs_ignore=1): left out (open). A SPICE subckt
cannot join two ports, and xschem refuses to short two port nets (Error 10).} 420 -230 0 0 0.2 0.2 {}
