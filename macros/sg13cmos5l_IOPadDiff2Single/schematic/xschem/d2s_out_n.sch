v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {d2s_out_n: the two N clamp frames of the pad} 40 -640 0 0 0.5 0.5 {}
T {layout: 2 x Clamp_N_M1 ng 35, l 1u, 80u, wiring external; the upper one with Clamp_N_M1_wiring roles 16:rep 17:rep} 40 -590 0 0 0.25 0.25 {}
T {ON: 33 + 35 = 68 fingers, gate b, drain vout (the pad). RN1: the replica of ON, the centre pair of the upper frame (2 f), diode-connected on dabn.} 40 -560 0 0 0.25 0.25 {}
T {Netlist: ../../netlist/source/d2s_out.spice} 40 -536 0 0 0.25 0.25 {}
N 100 -200 240 -200 {lab=vsso}
N 240 -200 280 -200 {lab=vsso}
N 280 -200 480 -200 {lab=vsso}
N 480 -200 510 -200 {lab=vsso}
N 240 -250 240 -200 {lab=vsso}
N 240 -280 280 -280 {lab=vsso}
N 280 -280 280 -200 {lab=vsso}
N 100 -280 200 -280 {lab=b}
N 240 -310 240 -400 {lab=vout}
N 240 -400 700 -400 {lab=vout}
N 480 -250 480 -200 {lab=vsso}
N 480 -280 510 -280 {lab=vsso}
N 510 -280 510 -200 {lab=vsso}
N 440 -280 440 -310 {lab=dabn}
N 440 -310 480 -310 {lab=dabn}
N 480 -310 480 -340 {lab=dabn}
N 480 -340 700 -340 {lab=dabn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 220 -280 0 0 {name=ON
l=1u
w=299.2u
ng=68
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 460 -280 0 0 {name=RN1
l=1u
w=8.8u
ng=2
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/iopin.sym} 100 -200 0 1 {name=p1 lab=vsso}
C {devices/ipin.sym} 100 -280 0 0 {name=p2 lab=b}
C {devices/iopin.sym} 700 -400 0 0 {name=p3 lab=vout}
C {devices/iopin.sym} 700 -340 0 0 {name=p4 lab=dabn}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
