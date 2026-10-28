v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {d2s_out_p: the P clamp frame of the pad} 40 -640 0 0 0.5 0.5 {}
T {layout: Clamp_P_M1 ng 43, l 0.6u, 80u, wiring external, with Clamp_P_M1_wiring roles 20:dummy 21:rep} 40 -590 0 0 0.25 0.25 {}
T {OP: 41 gate columns, 82 fingers, gate a, drain vout (the pad). RP1: the replica of OP, one column (2 f), diode-connected on dabp.} 40 -560 0 0 0.25 0.25 {}
T {RPD: the dummy column next to RP1, gate on vddo (off), drain on dabp. Netlist: ../../netlist/source/d2s_out.spice} 40 -536 0 0 0.25 0.25 {}
N 100 -460 240 -460 {lab=vddo}
N 240 -460 280 -460 {lab=vddo}
N 280 -460 480 -460 {lab=vddo}
N 480 -460 510 -460 {lab=vddo}
N 510 -460 670 -460 {lab=vddo}
N 670 -460 700 -460 {lab=vddo}
N 700 -460 760 -460 {lab=vddo}
N 240 -410 240 -460 {lab=vddo}
N 240 -380 280 -380 {lab=vddo}
N 280 -380 280 -460 {lab=vddo}
N 100 -380 200 -380 {lab=a}
N 240 -350 240 -260 {lab=vout}
N 240 -260 800 -260 {lab=vout}
N 480 -410 480 -460 {lab=vddo}
N 480 -380 510 -380 {lab=vddo}
N 510 -380 510 -460 {lab=vddo}
N 440 -380 440 -350 {lab=dabp}
N 440 -350 480 -350 {lab=dabp}
N 480 -350 480 -320 {lab=dabp}
N 480 -320 700 -320 {lab=dabp}
N 700 -320 800 -320 {lab=dabp}
N 700 -350 700 -320 {lab=dabp}
N 700 -410 700 -460 {lab=vddo}
N 700 -380 670 -380 {lab=vddo}
N 670 -380 670 -460 {lab=vddo}
N 740 -380 760 -380 {lab=vddo}
N 760 -380 760 -460 {lab=vddo}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 220 -380 0 0 {name=OP
l=0.6u
w=546.12u
ng=82
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 460 -380 0 0 {name=RP1
l=0.6u
w=13.32u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 720 -380 0 1 {name=RPD
l=0.6u
w=13.32u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/iopin.sym} 100 -460 0 1 {name=p1 lab=vddo}
C {devices/ipin.sym} 100 -380 0 0 {name=p2 lab=a}
C {devices/iopin.sym} 800 -260 0 0 {name=p3 lab=vout}
C {devices/iopin.sym} 800 -320 0 0 {name=p4 lab=dabp}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
