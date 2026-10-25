v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {nor3_hv: 3.3 V static CMOS gate (sg13_hv), y = not (a or b or c). Source: netlist/source/hv_logic.spice} 40 -620 0 0 0.4 0.4 {}
T {PMOS above, NMOS below; nets by label. vdd / vss: 3.3 V rail of the circuit using the gate.} 40 360 0 0 0.25 0.25 {}
N 580 -490 580 -430 {lab=p1}
N 120 -520 540 -520 {lab=a}
N 580 -520 600 -520 {lab=vdd}
N 580 -370 580 -310 {lab=p2}
N 320 -400 540 -400 {lab=b}
N 580 -400 600 -400 {lab=vdd}
N 580 -250 580 -220 {lab=y}
N 520 -280 540 -280 {lab=c}
N 580 -280 600 -280 {lab=vdd}
N 120 -160 140 -160 {lab=a}
N 180 -130 180 -100 {lab=vss}
N 180 -160 200 -160 {lab=vss}
N 320 -160 340 -160 {lab=b}
N 380 -130 380 -100 {lab=vss}
N 380 -160 400 -160 {lab=vss}
N 520 -160 540 -160 {lab=c}
N 580 -130 580 -100 {lab=vss}
N 580 -160 600 -160 {lab=vss}
N 600 -160 600 -100 {lab=vss}
N 580 -100 600 -100 {lab=vss}
N 80 -100 180 -100 {lab=vss}
N 200 -100 380 -100 {lab=vss}
N 400 -100 580 -100 {lab=vss}
N 400 -160 400 -100 {lab=vss}
N 380 -100 400 -100 {lab=vss}
N 200 -160 200 -100 {lab=vss}
N 180 -100 200 -100 {lab=vss}
N 520 -280 520 -160 {lab=c}
N 80 -280 520 -280 {lab=c}
N 320 -400 320 -160 {lab=b}
N 80 -400 320 -400 {lab=b}
N 120 -520 120 -160 {lab=a}
N 80 -520 120 -520 {lab=a}
N 580 -580 600 -580 {lab=vdd}
N 600 -580 600 -520 {lab=vdd}
N 580 -580 580 -550 {lab=vdd}
N 80 -580 580 -580 {lab=vdd}
N 600 -400 600 -280 {lab=vdd}
N 600 -520 600 -400 {lab=vdd}
N 180 -220 180 -190 {lab=y}
N 380 -220 580 -220 {lab=y}
N 380 -220 380 -190 {lab=y}
N 180 -220 380 -220 {lab=y}
N 580 -220 580 -190 {lab=y}
N 580 -220 680 -220 {lab=y}
C {devices/iopin.sym} 80 -580 0 1 {name=p0 lab=vdd}
C {devices/iopin.sym} 80 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 80 -520 0 0 {name=p2 lab=a}
C {devices/ipin.sym} 80 -400 0 0 {name=p3 lab=b}
C {devices/ipin.sym} 80 -280 0 0 {name=p4 lab=c}
C {devices/opin.sym} 680 -220 0 0 {name=p5 lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -520 0 0 {name=PA
l=0.45u
w=3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 580 -460 0 1 {name=l1 sig_type=std_logic lab=p1}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -400 0 0 {name=PB
l=0.45u
w=3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 580 -340 0 1 {name=l5 sig_type=std_logic lab=p2}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 560 -280 0 0 {name=PC
l=0.45u
w=3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 160 -160 0 0 {name=NA
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 120 -160 0 0 {name=l14 sig_type=std_logic lab=a}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 360 -160 0 0 {name=NB
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 320 -160 0 0 {name=l18 sig_type=std_logic lab=b}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 560 -160 0 0 {name=NC
l=0.45u
w=1u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 520 -160 0 0 {name=l22 sig_type=std_logic lab=c}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
