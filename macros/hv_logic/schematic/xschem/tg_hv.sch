v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {tg_hv: 3.3 V transmission gate (sg13_hv), a <-> b while en = 1 / en_b = 0. Source: netlist/source/hv_logic.spice} 0 -500 0 0 0.4 0.4 {}
T {N and P in parallel between a and b, bulks on vss / vdd; a / b symmetric (drawn as in the source: N d = a, P d = a).} 0 -90 0 0 0.25 0.25 {}
N 100 -420 220 -420 {lab=vdd}
N 100 -140 220 -140 {lab=vss}
N 100 -320 220 -320 {lab=en_b}
N 100 -240 220 -240 {lab=en}
N 280 -380 280 -280 {lab=b}
N 280 -280 320 -280 {lab=b}
N 250 -180 280 -180 {lab=b}
N 280 -280 280 -180 {lab=b}
N 220 -240 220 -220 {lab=en}
N 160 -280 160 -180 {lab=a}
N 100 -280 160 -280 {lab=a}
N 160 -180 190 -180 {lab=a}
N 220 -180 220 -140 {lab=vss}
N 220 -420 220 -380 {lab=vdd}
N 220 -340 220 -320 {lab=en_b}
N 160 -380 190 -380 {lab=a}
N 160 -380 160 -280 {lab=a}
N 250 -380 280 -380 {lab=b}
C {devices/iopin.sym} 100 -420 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 -140 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 -240 0 0 {name=p2 lab=en}
C {devices/ipin.sym} 100 -320 0 0 {name=p3 lab=en_b}
C {devices/iopin.sym} 100 -280 0 1 {name=p4 lab=a}
C {devices/iopin.sym} 320 -280 0 0 {name=p5 lab=b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 220 -200 3 1 {name=N
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 220 -360 1 1 {name=P
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
