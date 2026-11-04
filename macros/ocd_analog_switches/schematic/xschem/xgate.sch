v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 100 -80 140 -80 {lab=out}
N 140 -0 140 90 {lab=out}
N 100 90 140 90 {lab=out}
N 10 -80 40 -80 {lab=in}
N 10 0 10 90 {lab=in}
N 10 90 40 90 {lab=in}
N -20 0 10 0 {lab=in}
N 10 -80 10 0 {lab=in}
N 140 -0 170 0 {lab=out}
N 140 -80 140 -0 {lab=out}
N -20 -50 70 -50 {lab=vdd}
N 70 -80 70 -50 {lab=vdd}
N -20 50 70 50 {lab=vss}
N 70 50 70 90 {lab=vss}
N 70 -150 70 -120 {lab=ena_b}
N 70 130 70 170 {lab=ena}
N 0 170 70 170 {lab=ena}
N 0 -150 70 -150 {lab=ena_b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 70 -100 1 0 {name=M1
l=0.5u
w=2u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 70 110 3 0 {name=M2
l=0.5u
w=2u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {iopin.sym} 170 0 0 0 {name=p1 lab=out}
C {iopin.sym} -20 0 0 1 {name=p2 lab=in}
C {iopin.sym} -20 -50 0 1 {name=p3 lab=vdd}
C {iopin.sym} -20 50 0 1 {name=p4 lab=vss}
C {ipin.sym} 0 -150 0 0 {name=p5 lab=ena_b}
C {ipin.sym} 0 170 0 0 {name=p6 lab=ena}
