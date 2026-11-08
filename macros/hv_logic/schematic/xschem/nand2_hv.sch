v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {nand2_hv: 3.3 V static CMOS gate (sg13_hv), y = not (a and b). Source: netlist/source/hv_logic.spice} 0 -600 0 0 0.4 0.4 {}
T {PMOS above, NMOS below; nets by label. vdd / vss: 3.3 V rail of the circuit using the gate.} 40 -100 0 0 0.25 0.25 {}
N 420 -400 420 -350 {lab=y}
N 360 -480 380 -480 {lab=a}
N 420 -480 440 -480 {lab=vdd}
N 240 -450 240 -420 {lab=y}
N 240 -480 260 -480 {lab=vdd}
N 360 -320 380 -320 {lab=a}
N 420 -320 440 -320 {lab=vss}
N 420 -170 420 -120 {lab=vss}
N 420 -200 440 -200 {lab=vss}
N 360 -480 360 -320 {lab=a}
N 60 -320 360 -320 {lab=a}
N 180 -480 200 -480 {lab=b}
N 180 -480 180 -200 {lab=b}
N 60 -480 180 -480 {lab=b}
N 180 -200 380 -200 {lab=b}
N 420 -560 440 -560 {lab=vdd}
N 440 -560 440 -480 {lab=vdd}
N 420 -560 420 -510 {lab=vdd}
N 260 -560 420 -560 {lab=vdd}
N 260 -560 260 -480 {lab=vdd}
N 240 -560 260 -560 {lab=vdd}
N 240 -560 240 -510 {lab=vdd}
N 60 -560 240 -560 {lab=vdd}
N 420 -400 500 -400 {lab=y}
N 420 -420 420 -400 {lab=y}
N 420 -290 420 -230 {lab=n1}
N 440 -200 440 -120 {lab=vss}
N 420 -120 440 -120 {lab=vss}
N 60 -120 420 -120 {lab=vss}
N 240 -420 420 -420 {lab=y}
N 420 -450 420 -420 {lab=y}
C {devices/iopin.sym} 60 -560 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 60 -120 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 60 -320 0 0 {name=p2 lab=a}
C {devices/ipin.sym} 60 -480 0 0 {name=p3 lab=b}
C {devices/opin.sym} 500 -400 0 0 {name=p4 lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 -480 0 0 {name=PA
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -430 0 1 {name=l1 sig_type=std_logic lab=y}
C {devices/lab_pin.sym} 360 -480 0 0 {name=l2 sig_type=std_logic lab=a}
C {devices/lab_pin.sym} 420 -530 0 1 {name=l3 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 440 -480 0 1 {name=l4 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 220 -480 0 0 {name=PB
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 240 -430 0 1 {name=l5 sig_type=std_logic lab=y}
C {devices/lab_pin.sym} 180 -480 0 0 {name=l6 sig_type=std_logic lab=b}
C {devices/lab_pin.sym} 240 -530 0 1 {name=l7 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 260 -480 0 1 {name=l8 sig_type=std_logic lab=vdd}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -320 0 0 {name=NA
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -370 0 1 {name=l9 sig_type=std_logic lab=y}
C {devices/lab_pin.sym} 360 -320 0 0 {name=l10 sig_type=std_logic lab=a}
C {devices/lab_pin.sym} 420 -270 0 1 {name=l11 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 440 -320 0 1 {name=l12 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 400 -200 0 0 {name=NB
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 420 -250 0 1 {name=l13 sig_type=std_logic lab=n1}
C {devices/lab_pin.sym} 360 -200 0 0 {name=l14 sig_type=std_logic lab=b}
C {devices/lab_pin.sym} 420 -150 0 1 {name=l15 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 440 -200 0 1 {name=l16 sig_type=std_logic lab=vss}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
