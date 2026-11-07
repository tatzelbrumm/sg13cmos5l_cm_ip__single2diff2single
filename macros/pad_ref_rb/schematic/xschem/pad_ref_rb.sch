v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {pad_ref_rb: replica bias of the pads' reference voltages vcm and vref, one shared bias tree} 100 -1128 0 0 0.6 0.6 {}
T {pad_ref_rb: the replica bias of the custom pads' reference voltages in one cell (2026-11-07, option A of the user's} 100 -1058 0 0 0.25 0.25 {}
T {question on sharing): the shared bias tree bias_tree_rb feeds vcm_rb (S2D vcm = D2S vref) and vref_s2d_rb (S2D vref).} 100 -1036 0 0 0.25 0.25 {}
T {One 5 uA reference current, one enable. Needs ../../../vcm_rb/netlist/source/vcm_rb.spice and} 100 -1014 0 0 0.25 0.25 {}
T {../../../vref_s2d_rb/netlist/source/vref_s2d_rb.spice. Task docs/launch/replica_bias_TASK.md (branch harness-test),} 100 -992 0 0 0.25 0.25 {}
T {records in docs/replica_bias/.} 100 -970 0 0 0.25 0.25 {}
T {Ports: vdd vss iref vcm vref en_3v3 en_3v3_b (iref: 5 uA SOURCED into the cell, from bias_gen_pd's iref, a bias_dist_pd} 100 -948 0 0 0.25 0.25 {}
T {output or a core's iout; en_3v3 / en_3v3_b from en_ctrl_3v3). vdd / vss: the rails of the pads it serves (the top edge} 100 -926 0 0 0.25 0.25 {}
T {that vcm_rb tracks is referenced to the pads' unit rail).} 100 -904 0 0 0.25 0.25 {}
T {Supply current (tt 27 C, 3.3 V): tree 9 uA (5 uA reference + 2 BP + 2 BNC) + vcm_rb 14 uA + vref_s2d_rb 1.7 uA.} 100 -882 0 0 0.25 0.25 {}
T {drawn from netlist/source/pad_ref_rb.spice; Xt bias_tree_rb (this folder), Xc vcm_rb, Xr vref_s2d_rb} 100 -850 0 0 0.25 0.25 {}
N 500 -800 500 -630 {lab=vdd}
N 500 -490 500 -380 {lab=vss}
N 1000 -800 1000 -620 {lab=vdd}
N 1000 -460 1000 -380 {lab=vss}
N 1500 -800 1500 -610 {lab=vdd}
N 1500 -470 1500 -380 {lab=vss}
N 1000 -800 1500 -800 {lab=vdd}
N 1000 -380 1500 -380 {lab=vss}
N 100 -590 400 -590 {lab=iref}
N 100 -570 400 -570 {lab=en_3v3}
N 200 -550 400 -550 {lab=en_3v3_b}
N 680 -580 900 -580 {lab=ni}
N 600 -560 900 -560 {lab=vbp}
N 720 -540 900 -540 {lab=vbnc}
N 680 -720 680 -580 {lab=ni}
N 680 -720 1360 -720 {lab=ni}
N 1360 -720 1360 -570 {lab=ni}
N 1360 -570 1400 -570 {lab=ni}
N 720 -680 720 -540 {lab=vbnc}
N 720 -680 1340 -680 {lab=vbnc}
N 1340 -680 1340 -550 {lab=vbnc}
N 1340 -550 1400 -550 {lab=vbnc}
N 200 -550 200 -420 {lab=en_3v3_b}
N 860 -420 1380 -420 {lab=en_3v3_b}
N 1380 -530 1380 -420 {lab=en_3v3_b}
N 1380 -530 1400 -530 {lab=en_3v3_b}
N 860 -520 860 -420 {lab=en_3v3_b}
N 860 -520 900 -520 {lab=en_3v3_b}
N 1600 -540 1760 -540 {lab=vref}
N 1100 -540 1140 -540 {lab=vcm}
N 1140 -540 1140 -440 {lab=vcm}
N 1140 -440 1760 -440 {lab=vcm}
N 100 -800 500 -800 {lab=vdd}
N 100 -380 500 -380 {lab=vss}
N 500 -800 1000 -800 {lab=vdd}
N 500 -380 1000 -380 {lab=vss}
N 600 -580 680 -580 {lab=ni}
N 600 -540 720 -540 {lab=vbnc}
N 100 -550 200 -550 {lab=en_3v3_b}
N 200 -420 860 -420 {lab=en_3v3_b}
C {devices/iopin.sym} 100 -800 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -380 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -590 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 1760 -440 0 0 {name=p3 lab=vcm}
C {devices/opin.sym} 1760 -540 0 0 {name=p4 lab=vref}
C {devices/ipin.sym} 100 -570 0 0 {name=p5 lab=en_3v3}
C {devices/ipin.sym} 100 -550 0 0 {name=p6 lab=en_3v3_b}
C {bias_tree_rb.sym} 500 -560 0 0 {name=Xt}
C {vcm_rb.sym} 1000 -540 0 0 {name=Xc}
C {vref_s2d_rb.sym} 1500 -540 0 0 {name=Xr}
C {devices/lab_wire.sym} 800 -720 0 0 {name=l1 sig_type=std_logic lab=ni}
C {devices/lab_wire.sym} 800 -680 0 0 {name=l2 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 800 -560 0 0 {name=l3 sig_type=std_logic lab=vbp}
C {devices/title.sym} 160 -300 0 0 {name=l0 author="Christoph Maier"}
