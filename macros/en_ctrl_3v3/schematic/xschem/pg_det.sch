v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {pg_det: supply-present detector, needs no 1.2 V supply. pg_b low when sense is high.} 10 -500 0 0 0.4 0.4 {}
T {ND (gate on the sensed supply) against the weak pull-up PU: pg_b = 0 when sense is present.} 40 -460 0 0 0.25 0.25 {}
T {RD pulls a floating (gated-off) sense input low. PU and RD conduct only while ena (the level-shifted} 40 -438 0 0 0.25 0.25 {}
T {en_1v2) is high, so with en_1v2 = 0 the cell draws leakage only. Source: netlist/source/en_ctrl_3v3.spice} 40 -416 0 0 0.25 0.25 {}
N 300 -240 300 -190 {lab=pg_b}
N 300 -320 320 -320 {lab=#net1}
N 240 -160 260 -160 {lab=sense}
N 300 -130 300 -100 {lab=vss}
N 300 -160 320 -160 {lab=vss}
N 180 -130 180 -100 {lab=vss}
N 180 -160 200 -160 {lab=vss}
N 200 -160 200 -100 {lab=vss}
N 180 -100 200 -100 {lab=vss}
N 80 -100 180 -100 {lab=vss}
N 80 -160 140 -160 {lab=ena}
N 240 -220 240 -160 {lab=sense}
N 180 -220 240 -220 {lab=sense}
N 180 -220 180 -190 {lab=sense}
N 80 -220 180 -220 {lab=sense}
N 320 -160 320 -100 {lab=vss}
N 300 -100 320 -100 {lab=vss}
N 200 -100 300 -100 {lab=vss}
N 80 -320 260 -320 {lab=ena_b}
N 300 -240 360 -240 {lab=pg_b}
N 300 -290 300 -240 {lab=pg_b}
N 320 -380 320 -320 {lab=#net1}
N 300 -380 320 -380 {lab=#net1}
N 300 -380 300 -350 {lab=#net1}
N 80 -380 300 -380 {lab=#net1}
C {devices/iopin.sym} 80 -380 0 1 {name=p0 lab=vddh}
C {devices/iopin.sym} 80 -100 0 1 {name=p1 lab=vss}
C {devices/ipin.sym} 80 -220 0 0 {name=p2 lab=sense}
C {devices/opin.sym} 360 -240 0 0 {name=p3 lab=pg_b}
C {devices/ipin.sym} 80 -160 0 0 {name=p4 lab=ena}
C {devices/ipin.sym} 80 -320 0 0 {name=p5 lab=ena_b}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 280 -320 0 0 {name=PU
l=50u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 280 -160 0 0 {name=ND
l=0.45u
w=2u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 160 -160 0 0 {name=RD
l=100u
w=0.3u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 180 -210 0 1 {name=l9 sig_type=std_logic lab=sense}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
