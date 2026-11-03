v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 200 0 0 0 {name=DT[3:0]
l=1u
w=20u
ng=2
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_pin.sym} 180 0 0 0 {name=l1 lab=g}
C {devices/lab_pin.sym} 220 -30 0 1 {name=l2 lab=vdd}
C {devices/lab_pin.sym} 220 0 0 1 {name=l3 lab=vdd}
C {devices/lab_pin.sym} 220 30 0 1 {name=l4 lab=d[3:0]}
C {devices/iopin.sym} 0 0 0 0 {name=p1 lab=vdd}
