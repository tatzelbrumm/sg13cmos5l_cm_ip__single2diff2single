v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {nor3_hv: 3.3 V static CMOS gate (sg13_hv), y = not (a or b or c). Source: netlist/source/hv_logic.spice} 0 -60 0 0 0.4 0.4 {}
C {devices/iopin.sym} 40 40 0 0 {name=p0 lab=vdd}
C {devices/iopin.sym} 40 70 0 0 {name=p1 lab=vss}
C {devices/ipin.sym} 40 100 0 0 {name=p2 lab=a}
C {devices/ipin.sym} 40 130 0 0 {name=p3 lab=b}
C {devices/ipin.sym} 40 160 0 0 {name=p4 lab=c}
C {devices/opin.sym} 40 190 0 0 {name=p5 lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 200 60 0 0 {name=PA
l=0.45u
w=3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 220 90 220 110 {lab=p1}
C {devices/lab_pin.sym} 220 110 0 1 {name=l1 sig_type=std_logic lab=p1}
N 180 60 160 60 {lab=a}
C {devices/lab_pin.sym} 160 60 0 0 {name=l2 sig_type=std_logic lab=a}
N 220 30 220 10 {lab=vdd}
C {devices/lab_pin.sym} 220 10 0 1 {name=l3 sig_type=std_logic lab=vdd}
N 220 60 240 60 {lab=vdd}
C {devices/lab_pin.sym} 240 60 0 1 {name=l4 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 60 0 0 {name=PB
l=0.45u
w=3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 420 90 420 110 {lab=p2}
C {devices/lab_pin.sym} 420 110 0 1 {name=l5 sig_type=std_logic lab=p2}
N 380 60 360 60 {lab=b}
C {devices/lab_pin.sym} 360 60 0 0 {name=l6 sig_type=std_logic lab=b}
N 420 30 420 10 {lab=p1}
C {devices/lab_pin.sym} 420 10 0 1 {name=l7 sig_type=std_logic lab=p1}
N 420 60 440 60 {lab=vdd}
C {devices/lab_pin.sym} 440 60 0 1 {name=l8 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 600 60 0 0 {name=PC
l=0.45u
w=3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 620 90 620 110 {lab=y}
C {devices/lab_pin.sym} 620 110 0 1 {name=l9 sig_type=std_logic lab=y}
N 580 60 560 60 {lab=c}
C {devices/lab_pin.sym} 560 60 0 0 {name=l10 sig_type=std_logic lab=c}
N 620 30 620 10 {lab=p2}
C {devices/lab_pin.sym} 620 10 0 1 {name=l11 sig_type=std_logic lab=p2}
N 620 60 640 60 {lab=vdd}
C {devices/lab_pin.sym} 640 60 0 1 {name=l12 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 200 260 0 0 {name=NA
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 220 230 220 210 {lab=y}
C {devices/lab_pin.sym} 220 210 0 1 {name=l13 sig_type=std_logic lab=y}
N 180 260 160 260 {lab=a}
C {devices/lab_pin.sym} 160 260 0 0 {name=l14 sig_type=std_logic lab=a}
N 220 290 220 310 {lab=vss}
C {devices/lab_pin.sym} 220 310 0 1 {name=l15 sig_type=std_logic lab=vss}
N 220 260 240 260 {lab=vss}
C {devices/lab_pin.sym} 240 260 0 1 {name=l16 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 260 0 0 {name=NB
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 420 230 420 210 {lab=y}
C {devices/lab_pin.sym} 420 210 0 1 {name=l17 sig_type=std_logic lab=y}
N 380 260 360 260 {lab=b}
C {devices/lab_pin.sym} 360 260 0 0 {name=l18 sig_type=std_logic lab=b}
N 420 290 420 310 {lab=vss}
C {devices/lab_pin.sym} 420 310 0 1 {name=l19 sig_type=std_logic lab=vss}
N 420 260 440 260 {lab=vss}
C {devices/lab_pin.sym} 440 260 0 1 {name=l20 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 260 0 0 {name=NC
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 620 230 620 210 {lab=y}
C {devices/lab_pin.sym} 620 210 0 1 {name=l21 sig_type=std_logic lab=y}
N 580 260 560 260 {lab=c}
C {devices/lab_pin.sym} 560 260 0 0 {name=l22 sig_type=std_logic lab=c}
N 620 290 620 310 {lab=vss}
C {devices/lab_pin.sym} 620 310 0 1 {name=l23 sig_type=std_logic lab=vss}
N 620 260 640 260 {lab=vss}
C {devices/lab_pin.sym} 640 260 0 1 {name=l24 sig_type=std_logic lab=vss}
T {PMOS above, NMOS below; nets by label. vdd / vss: 3.3 V rail of the circuit using the gate.} 40 360 0 0 0.25 0.25 {}
C {devices/title.sym} 160 600 0 0 {name=l0 author="Christoph Maier"}
