v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {pad_ref_rb: replica bias of the pads' reference voltages vcm and vref, one shared bias tree} 100 -908 0 0 0.6 0.6 {}
T {pad_ref_rb: the replica bias of the custom pads' reference voltages in one cell (2026-11-07, option A of the user's} 100 -838 0 0 0.25 0.25 {}
T {question on sharing): the shared bias tree bias_tree_rb feeds vcm_rb (S2D vcm = D2S vref) and vref_s2d_rb (S2D vref).} 100 -816 0 0 0.25 0.25 {}
T {One 5 uA reference current, one enable. Needs ../../../vcm_rb/netlist/source/vcm_rb.spice and} 100 -794 0 0 0.25 0.25 {}
T {../../../vref_s2d_rb/netlist/source/vref_s2d_rb.spice. Task docs/launch/replica_bias_TASK.md (branch harness-test),} 100 -772 0 0 0.25 0.25 {}
T {records in docs/replica_bias/.} 100 -750 0 0 0.25 0.25 {}
T {Ports: vdd vss iref vcm vref en_3v3 en_3v3_b (iref: 5 uA SOURCED into the cell, from bias_gen_pd's iref, a bias_dist_pd} 100 -728 0 0 0.25 0.25 {}
T {output or a core's iout; en_3v3 / en_3v3_b from en_ctrl_3v3). vdd / vss: the rails of the pads it serves (the top edge} 100 -706 0 0 0.25 0.25 {}
T {that vcm_rb tracks is referenced to the pads' unit rail).} 100 -684 0 0 0.25 0.25 {}
T {Supply current (tt 27 C, 3.3 V): tree 9 uA (5 uA reference + 2 BP + 2 BNC) + vcm_rb 14 uA + vref_s2d_rb 1.7 uA.} 100 -662 0 0 0.25 0.25 {}
T {drawn from netlist/source/pad_ref_rb.spice; Xt bias_tree_rb (this folder), Xc vcm_rb, Xr vref_s2d_rb} 100 -630 0 0 0.25 0.25 {}
N 500 -580 500 -490 {lab=vdd}
N 500 -350 500 -100 {lab=vss}
N 1000 -580 1000 -480 {lab=vdd}
N 1000 -320 1000 -100 {lab=vss}
N 1500 -580 1500 -470 {lab=vdd}
N 1500 -330 1500 -100 {lab=vss}
N 1000 -580 1500 -580 {lab=vdd}
N 1000 -100 1500 -100 {lab=vss}
N 100 -450 400 -450 {lab=iref}
N 100 -430 400 -430 {lab=en_3v3}
N 200 -410 400 -410 {lab=en_3v3_b}
N 680 -440 900 -440 {lab=ni}
N 600 -420 900 -420 {lab=vbp}
N 720 -400 900 -400 {lab=vbnc}
N 680 -540 680 -440 {lab=ni}
N 680 -540 1360 -540 {lab=ni}
N 1360 -540 1360 -430 {lab=ni}
N 1360 -430 1400 -430 {lab=ni}
N 720 -520 720 -400 {lab=vbnc}
N 720 -520 1340 -520 {lab=vbnc}
N 1340 -520 1340 -410 {lab=vbnc}
N 1340 -410 1400 -410 {lab=vbnc}
N 200 -410 200 -280 {lab=en_3v3_b}
N 860 -280 1380 -280 {lab=en_3v3_b}
N 1380 -390 1380 -280 {lab=en_3v3_b}
N 1380 -390 1400 -390 {lab=en_3v3_b}
N 860 -380 860 -280 {lab=en_3v3_b}
N 860 -380 900 -380 {lab=en_3v3_b}
N 1100 -400 1140 -400 {lab=vcm}
N 1140 -400 1140 -300 {lab=vcm}
N 100 -580 500 -580 {lab=vdd}
N 100 -100 500 -100 {lab=vss}
N 500 -580 1000 -580 {lab=vdd}
N 500 -100 1000 -100 {lab=vss}
N 600 -440 680 -440 {lab=ni}
N 600 -400 720 -400 {lab=vbnc}
N 100 -410 200 -410 {lab=en_3v3_b}
N 200 -280 860 -280 {lab=en_3v3_b}
N 1500 -100 1700 -100 {lab=vss}
N 1680 -300 1760 -300 {lab=vcm}
N 1720 -400 1760 -400 {lab=vref}
N 1700 -140 1700 -100 {lab=vss}
N 1720 -400 1720 -240 {lab=vref}
N 1600 -400 1720 -400 {lab=vref}
N 1680 -300 1680 -240 {lab=vcm}
N 1140 -300 1680 -300 {lab=vcm}
C {devices/iopin.sym} 100 -580 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -450 0 0 {name=p2 lab=iref}
C {devices/opin.sym} 1760 -300 0 0 {name=p3 lab=vcm}
C {devices/opin.sym} 1760 -400 0 0 {name=p4 lab=vref}
C {devices/ipin.sym} 100 -430 0 0 {name=p5 lab=en_3v3}
C {devices/ipin.sym} 100 -410 0 0 {name=p6 lab=en_3v3_b}
C {bias_tree_rb.sym} 500 -420 0 0 {name=Xt}
C {vcm_rb.sym} 1000 -400 0 0 {name=Xc}
C {vref_s2d_rb.sym} 1500 -400 0 0 {name=Xr}
C {bypass_rb.sym} 1700 -190 0 0 {name=Xb ncm=4 ncr=9}
C {devices/lab_wire.sym} 800 -540 0 0 {name=l1 sig_type=std_logic lab=ni}
C {devices/lab_wire.sym} 800 -520 0 0 {name=l2 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 800 -420 0 0 {name=l3 sig_type=std_logic lab=vbp}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
