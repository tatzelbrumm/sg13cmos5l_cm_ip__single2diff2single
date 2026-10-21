v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {inv_hv: 3.3 V static CMOS gate (sg13_hv), y = not a. Source: netlist/source/hv_logic.spice} 0 -60 0 0 0.4 0.4 {}
C {devices/iopin.sym} 40 40 0 0 {name=p0 lab=vdd}
C {devices/iopin.sym} 40 70 0 0 {name=p1 lab=vss}
C {devices/ipin.sym} 40 100 0 0 {name=p2 lab=a}
C {devices/opin.sym} 40 130 0 0 {name=p3 lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 200 60 0 0 {name=P
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 220 90 220 110 {lab=y}
C {devices/lab_pin.sym} 220 110 0 1 {name=l1 sig_type=std_logic lab=y}
N 180 60 160 60 {lab=a}
C {devices/lab_pin.sym} 160 60 0 0 {name=l2 sig_type=std_logic lab=a}
N 220 30 220 10 {lab=vdd}
C {devices/lab_pin.sym} 220 10 0 1 {name=l3 sig_type=std_logic lab=vdd}
N 220 60 240 60 {lab=vdd}
C {devices/lab_pin.sym} 240 60 0 1 {name=l4 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 260 0 0 {name=N
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 220 230 220 210 {lab=y}
C {devices/lab_pin.sym} 220 210 0 1 {name=l5 sig_type=std_logic lab=y}
N 180 260 160 260 {lab=a}
C {devices/lab_pin.sym} 160 260 0 0 {name=l6 sig_type=std_logic lab=a}
N 220 290 220 310 {lab=vss}
C {devices/lab_pin.sym} 220 310 0 1 {name=l7 sig_type=std_logic lab=vss}
N 220 260 240 260 {lab=vss}
C {devices/lab_pin.sym} 240 260 0 1 {name=l8 sig_type=std_logic lab=vss}
T {PMOS above, NMOS below; nets by label. vdd / vss: 3.3 V rail of the circuit using the gate.} 40 360 0 0 0.25 0.25 {}
C {devices/title.sym} 160 600 0 0 {name=l0 author="Christoph Maier"}
