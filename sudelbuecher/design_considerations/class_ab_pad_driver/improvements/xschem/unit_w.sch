v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {unit_w: well-input PMOS pair, gates at vss} 60 -500 0 0 0.4 0.4 {}
T {gp drains to y, gn drains to x; x and y go to the folding nodes} 60 -460 0 0 0.25 0.25 {}
N 60 -400 310 -400 {lab=vdd}
N 310 -370 310 -400 {lab=vdd}
N 310 -340 330 -340 {lab=vdd}
N 330 -340 330 -400 {lab=vdd}
N 60 -280 250 -280 {lab=vbp}
N 250 -280 250 -340 {lab=vbp}
N 250 -340 270 -340 {lab=vbp}
N 310 -310 310 -220 {lab=s}
N 220 -220 310 -220 {lab=s}
N 220 -220 220 -170 {lab=s}
N 400 -220 400 -170 {lab=s}
N 220 -110 220 20 {lab=y}
N 220 20 520 20 {lab=y}
N 400 -110 400 -20 {lab=x}
N 400 -20 520 -20 {lab=x}
N 220 -140 260 -140 {lab=gp}
N 260 -140 260 -80 {lab=gp}
N 260 -80 60 -80 {lab=gp}
N 400 -140 360 -140 {lab=gn}
N 360 -140 360 -40 {lab=gn}
N 360 -40 60 -40 {lab=gn}
N 180 -140 160 -140 {lab=vss}
N 160 -140 160 100 {lab=vss}
N 440 -140 460 -140 {lab=vss}
N 460 -140 460 100 {lab=vss}
N 60 100 160 100 {lab=vss}
N 310 -400 330 -400 {lab=vdd}
N 350 -220 400 -220 {lab=s}
N 310 -220 350 -220 {lab=s}
N 160 100 460 100 {lab=vss}
C {devices/opin.sym} 520 -20 0 0 {name=p1 lab=x}
C {devices/opin.sym} 520 20 0 0 {name=p2 lab=y}
C {devices/ipin.sym} 60 -80 0 0 {name=p3 lab=gp}
C {devices/ipin.sym} 60 -40 0 0 {name=p4 lab=gn}
C {devices/iopin.sym} 60 -400 0 1 {name=p5 lab=vdd}
C {devices/iopin.sym} 60 100 0 1 {name=p6 lab=vss}
C {devices/ipin.sym} 60 -280 0 0 {name=p7 lab=vbp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 290 -340 0 0 {name=T
l=2u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 200 -140 0 0 {name=Ma
l=lwi
w=wwi
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 420 -140 0 1 {name=Mb
l=lwi
w=wwi
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 350 -220 0 1 {name=l1 sig_type=std_logic lab=s}
