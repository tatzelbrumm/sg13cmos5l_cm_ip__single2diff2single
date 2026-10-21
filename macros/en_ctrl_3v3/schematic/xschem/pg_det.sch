v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {pg_det: supply-present detector, needs no 1.2 V supply. pg_b low when sense is high.} 0 -60 0 0 0.4 0.4 {}
C {devices/iopin.sym} 40 40 0 0 {name=p0 lab=vddh}
C {devices/iopin.sym} 40 70 0 0 {name=p1 lab=vss}
C {devices/ipin.sym} 40 100 0 0 {name=p2 lab=sense}
C {devices/opin.sym} 40 130 0 0 {name=p3 lab=pg_b}
C {devices/ipin.sym} 40 160 0 0 {name=p4 lab=ena}
C {devices/ipin.sym} 40 190 0 0 {name=p5 lab=ena_b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 260 60 0 0 {name=PU
l=50u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
N 280 90 280 110 {lab=pg_b}
C {devices/lab_pin.sym} 280 110 0 1 {name=l1 sig_type=std_logic lab=pg_b}
N 240 60 220 60 {lab=ena_b}
C {devices/lab_pin.sym} 220 60 0 0 {name=l2 sig_type=std_logic lab=ena_b}
N 280 30 280 10 {lab=vddh}
C {devices/lab_pin.sym} 280 10 0 1 {name=l3 sig_type=std_logic lab=vddh}
N 280 60 300 60 {lab=vddh}
C {devices/lab_pin.sym} 300 60 0 1 {name=l4 sig_type=std_logic lab=vddh}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 260 260 0 0 {name=ND
l=0.45u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 280 230 280 210 {lab=pg_b}
C {devices/lab_pin.sym} 280 210 0 1 {name=l5 sig_type=std_logic lab=pg_b}
N 240 260 220 260 {lab=sense}
C {devices/lab_pin.sym} 220 260 0 0 {name=l6 sig_type=std_logic lab=sense}
N 280 290 280 310 {lab=vss}
C {devices/lab_pin.sym} 280 310 0 1 {name=l7 sig_type=std_logic lab=vss}
N 280 260 300 260 {lab=vss}
C {devices/lab_pin.sym} 300 260 0 1 {name=l8 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 500 260 0 0 {name=RD
l=100u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 520 230 520 210 {lab=sense}
C {devices/lab_pin.sym} 520 210 0 1 {name=l9 sig_type=std_logic lab=sense}
N 480 260 460 260 {lab=ena}
C {devices/lab_pin.sym} 460 260 0 0 {name=l10 sig_type=std_logic lab=ena}
N 520 290 520 310 {lab=vss}
C {devices/lab_pin.sym} 520 310 0 1 {name=l11 sig_type=std_logic lab=vss}
N 520 260 540 260 {lab=vss}
C {devices/lab_pin.sym} 540 260 0 1 {name=l12 sig_type=std_logic lab=vss}
T {ND (gate on the sensed supply) against the weak pull-up PU: pg_b = 0 when sense is present.} 40 380 0 0 0.25 0.25 {}
T {RD pulls a floating (gated-off) sense input low. PU and RD conduct only while ena (the level-shifted} 40 402 0 0 0.25 0.25 {}
T {en_1v2) is high, so with en_1v2 = 0 the cell draws leakage only. Source: netlist/source/en_ctrl_3v3.spice} 40 424 0 0 0.25 0.25 {}
C {devices/title.sym} 160 600 0 0 {name=l0 author="Christoph Maier"}
