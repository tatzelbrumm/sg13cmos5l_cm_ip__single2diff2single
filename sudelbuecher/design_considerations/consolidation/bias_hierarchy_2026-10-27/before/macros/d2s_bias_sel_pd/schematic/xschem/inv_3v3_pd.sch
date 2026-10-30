v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {inv_3v3_pd: en_3v3_b for the power-down switches (1u / 0.45u hv devices on vdd / vss)} 0 220 0 0 0.4 0.4 {}
N 140 340 160 340 {lab=a}
N 200 340 220 340 {lab=vdd}
N 140 460 160 460 {lab=a}
N 200 490 200 540 {lab=vss}
N 200 460 220 460 {lab=vss}
N 220 460 220 540 {lab=vss}
N 200 540 220 540 {lab=vss}
N 100 540 200 540 {lab=vss}
N 220 260 220 340 {lab=vdd}
N 200 260 220 260 {lab=vdd}
N 200 260 200 310 {lab=vdd}
N 100 260 200 260 {lab=vdd}
N 200 400 200 430 {lab=en_3v3_b}
N 140 400 140 460 {lab=a}
N 100 400 140 400 {lab=a}
N 140 340 140 400 {lab=a}
N 200 400 240 400 {lab=en_3v3_b}
N 200 370 200 400 {lab=en_3v3_b}
C {devices/title.sym} 160 600 0 0 {name=l0 author="Christoph Maier"}
C {devices/iopin.sym} 100 260 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 100 540 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 100 400 0 0 {name=p2 lab=a}
C {devices/opin.sym} 240 400 0 0 {name=p3 lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 180 340 0 0 {name=P
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 460 0 0 {name=N
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
