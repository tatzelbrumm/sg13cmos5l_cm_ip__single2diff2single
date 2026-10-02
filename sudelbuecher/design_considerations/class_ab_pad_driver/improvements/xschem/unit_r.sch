v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {rhigh body = vss} 270 -190 0 0 0.2 0.2 {}
T {unit_r: split-tail PMOS pair, rhigh degeneration} 60 -500 0 0 0.4 0.4 {}
T {gp drains to y, gn drains to x; x and y go to the folding nodes} 60 -460 0 0 0.25 0.25 {}
N 60 -400 200 -400 {lab=vdd}
N 220 -400 220 -370 {lab=vdd}
N 200 -340 220 -340 {lab=vdd}
N 200 -400 200 -340 {lab=vdd}
N 400 -400 400 -370 {lab=vdd}
N 400 -340 420 -340 {lab=vdd}
N 420 -400 420 -340 {lab=vdd}
N 60 -280 260 -280 {lab=vbp}
N 260 -340 260 -280 {lab=vbp}
N 260 -340 360 -340 {lab=vbp}
N 220 -310 220 -220 {lab=sa}
N 220 -220 240 -220 {lab=sa}
N 220 -140 240 -140 {lab=sa}
N 240 -220 240 -140 {lab=sa}
N 400 -310 400 -220 {lab=sb}
N 380 -220 400 -220 {lab=sb}
N 380 -140 400 -140 {lab=sb}
N 380 -220 380 -140 {lab=sb}
N 60 -140 180 -140 {lab=gp}
N 60 -60 460 -60 {lab=gn}
N 460 -140 460 -60 {lab=gn}
N 440 -140 460 -140 {lab=gn}
N 220 -110 220 20 {lab=y}
N 220 20 520 20 {lab=y}
N 400 -110 400 -20 {lab=x}
N 400 -20 520 -20 {lab=x}
N 400 -400 420 -400 {lab=vdd}
N 200 -400 220 -400 {lab=vdd}
N 220 -220 220 -170 {lab=sa}
N 240 -220 280 -220 {lab=sa}
N 400 -220 400 -170 {lab=sb}
N 220 -400 400 -400 {lab=vdd}
N 340 -220 380 -220 {lab=sb}
C {devices/opin.sym} 520 -20 0 0 {name=p1 lab=x}
C {devices/opin.sym} 520 20 0 0 {name=p2 lab=y}
C {devices/ipin.sym} 60 -140 0 0 {name=p3 lab=gp}
C {devices/ipin.sym} 60 -60 0 0 {name=p4 lab=gn}
C {devices/iopin.sym} 60 -400 0 1 {name=p5 lab=vdd}
C {devices/iopin.sym} 60 100 0 1 {name=p6 lab=vss}
C {devices/ipin.sym} 60 -280 0 0 {name=p7 lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 240 -340 0 1 {name=Ta
l=2u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -340 0 0 {name=Tb
l=2u
w=10u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 200 -140 0 0 {name=Ma
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 420 -140 0 1 {name=Mb
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/rhigh.sym} 310 -220 3 0 {name=R
w=0.5u
l=36.4u
model=rhigh
body=vss
spiceprefix=X
b=0
m=1
mm_ok=1}
C {devices/lab_wire.sym} 260 -220 0 0 {name=l1 sig_type=std_logic lab=sa}
C {devices/lab_wire.sym} 360 -220 0 1 {name=l2 sig_type=std_logic lab=sb}
