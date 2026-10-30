v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {inv_hv: 3.3 V static CMOS gate (sg13_hv), y = not a. Source: netlist/source/hv_logic.spice} 0 -420 0 0 0.4 0.4 {}
N 140 -300 160 -300 {lab=a}
N 200 -300 220 -300 {lab=vdd}
N 140 -180 160 -180 {lab=a}
N 200 -150 200 -100 {lab=vss}
N 200 -180 220 -180 {lab=vss}
N 220 -180 220 -100 {lab=vss}
N 200 -100 220 -100 {lab=vss}
N 100 -100 200 -100 {lab=vss}
N 220 -380 220 -300 {lab=vdd}
N 200 -380 220 -380 {lab=vdd}
N 200 -380 200 -330 {lab=vdd}
N 100 -380 200 -380 {lab=vdd}
N 200 -240 200 -210 {lab=y}
N 140 -240 140 -180 {lab=a}
N 100 -240 140 -240 {lab=a}
N 140 -300 140 -240 {lab=a}
N 200 -240 240 -240 {lab=y}
N 200 -270 200 -240 {lab=y}
C {devices/iopin.sym} 100 -380 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -240 0 0 {name=p2 lab=a}
C {devices/opin.sym} 240 -240 0 0 {name=p3 lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 180 -300 0 0 {name=P
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 -180 0 0 {name=N
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
