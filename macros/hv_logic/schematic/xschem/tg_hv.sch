v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tg_hv: 3.3 V transmission gate (sg13_hv), a <-> b while en = 1 / en_b = 0. Source: netlist/source/hv_logic.spice} 0 -460 0 0 0.4 0.4 {}
T {N and P in parallel between a and b, bulks on vss / vdd; a / b symmetric (drawn as in the source: N d = a, P d = a).} 0 -420 0 0 0.25 0.25 {}
N 100 -380 220 -380 {lab=vdd}
N 100 -100 220 -100 {lab=vss}
N 100 -300 160 -300 {lab=en_b}
N 100 -180 160 -180 {lab=en}
N 200 -270 200 -240 {lab=a}
N 200 -240 200 -210 {lab=a}
N 100 -240 200 -240 {lab=a}
N 200 -330 200 -350 {lab=b}
N 200 -350 280 -350 {lab=b}
N 280 -350 280 -240 {lab=b}
N 280 -240 280 -130 {lab=b}
N 280 -130 200 -130 {lab=b}
N 200 -130 200 -150 {lab=b}
N 280 -240 320 -240 {lab=b}
N 200 -300 220 -300 {lab=vdd}
N 220 -300 220 -380 {lab=vdd}
N 200 -180 220 -180 {lab=vss}
N 220 -180 220 -100 {lab=vss}
C {devices/iopin.sym} 100 -380 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -180 0 0 {name=p2 lab=en}
C {devices/ipin.sym} 100 -300 0 0 {name=p3 lab=en_b}
C {devices/iopin.sym} 100 -240 0 1 {name=p4 lab=a}
C {devices/iopin.sym} 320 -240 0 0 {name=p5 lab=b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 -180 0 0 {name=N
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 180 -300 0 0 {name=P
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
