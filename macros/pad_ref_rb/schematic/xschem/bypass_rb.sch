v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 230 -290 370 -290 370 -140 230 -140 230 -290 {dash=6}
P 10 5 390 -290 530 -290 530 -140 390 -140 390 -290 {dash=6}
T {bypass_rb: the bypass capacitors of vcm and vref, in a cell of their own} 100 -800 0 0 0.6 0.6 {}
T {Christoph, 2026-11-07: distinct from vcm_rb and vref_s2d_rb, "6 on vref, 4 on vcm". All 12u x 12u hv NMOS to vss, the s2d} 100 -730 0 0 0.25 0.25 {}
T {pad's load-capacitor device (CLP / CLN). vcm_rb keeps its CB (the buffer's phase margin); vref_s2d_rb has none (no loop).} 100 -708 0 0 0.25 0.25 {}
T {NMOS to vss only: PMOS to iovdd couples iovdd into vref, the S2D's zero point (explore_bypass.py).} 100 -686 0 0 0.25 0.25 {}
T {drawn from netlist/source/pad_ref_rb.spice (subckt bypass_rb)} 100 -654 0 0 0.25 0.25 {}
T {[1] vcm 4 x} 305 -313.5 0 0 0.3 0.3 {layer=10}
T {[2] vref 8 x} 465 -313.5 0 0 0.3 0.3 {layer=10}
N 100 -400 300 -400 {lab=vcm}
N 300 -400 300 -240 {lab=vcm}
N 100 -460 460 -460 {lab=vref}
N 460 -460 460 -240 {lab=vref}
N 260 -200 270 -200 {lab=vss}
N 260 -200 260 -100 {lab=vss}
N 300 -200 300 -100 {lab=vss}
N 330 -200 340 -200 {lab=vss}
N 340 -200 340 -100 {lab=vss}
N 420 -200 430 -200 {lab=vss}
N 420 -200 420 -100 {lab=vss}
N 460 -200 460 -100 {lab=vss}
N 490 -200 500 -200 {lab=vss}
N 500 -200 500 -100 {lab=vss}
N 100 -100 500 -100 {lab=vss}
C {devices/iopin.sym} 100 -100 0 1 {name=p0 lab=vss}
C {devices/iopin.sym} 100 -400 0 1 {name=p1 lab=vcm}
C {devices/iopin.sym} 100 -460 0 1 {name=p2 lab=vref}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 300 -220 1 0 {name=CBM
l=12u
w=12u
ng=1
m=4
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 460 -220 1 0 {name=CBR
l=12u
w=12u
ng=1
m=8
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
