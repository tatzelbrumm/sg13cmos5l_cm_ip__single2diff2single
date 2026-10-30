v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {inv_3v3_pd: en_3v3_b for the power-down switches (1u / 0.45u hv devices on vdd / vss)} 0 -60 0 0 0.4 0.4 {}
C {devices/iopin.sym} 40 40 0 0 {name=p0 lab=vdd}
C {devices/iopin.sym} 40 70 0 0 {name=p1 lab=vss}
C {devices/ipin.sym} 40 100 0 0 {name=p2 lab=en_3v3}
C {devices/opin.sym} 40 130 0 0 {name=p3 lab=en_3v3_b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 240 60 0 0 {name=IP
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 260 90 260 110 {lab=en_3v3_b}
C {devices/lab_pin.sym} 260 110 0 1 {name=l1 sig_type=std_logic lab=en_3v3_b}
N 220 60 200 60 {lab=en_3v3}
C {devices/lab_pin.sym} 200 60 0 0 {name=l2 sig_type=std_logic lab=en_3v3}
N 260 30 260 10 {lab=vdd}
C {devices/lab_pin.sym} 260 10 0 1 {name=l3 sig_type=std_logic lab=vdd}
N 260 60 280 60 {lab=vdd}
C {devices/lab_pin.sym} 280 60 0 1 {name=l4 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 240 220 0 0 {name=IN
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 260 190 260 170 {lab=en_3v3_b}
C {devices/lab_pin.sym} 260 170 0 1 {name=l5 sig_type=std_logic lab=en_3v3_b}
N 220 220 200 220 {lab=en_3v3}
C {devices/lab_pin.sym} 200 220 0 0 {name=l6 sig_type=std_logic lab=en_3v3}
N 260 250 260 270 {lab=vss}
C {devices/lab_pin.sym} 260 270 0 1 {name=l7 sig_type=std_logic lab=vss}
N 260 220 280 220 {lab=vss}
C {devices/lab_pin.sym} 280 220 0 1 {name=l8 sig_type=std_logic lab=vss}
C {devices/title.sym} 160 600 0 0 {name=l0 author="Christoph Maier"}
