v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 10 5 240 -300 600 -300 600 -130 240 -130 240 -300 {dash=6}
P 10 5 640 -300 880 -300 880 -130 640 -130 640 -300 {dash=6}
T {bypass_rb: the bypass capacitors of vcm and vref, in a cell of their own} 100 -800 0 0 0.6 0.6 {}
T {Christoph, 2026-11-07: distinct from vcm_rb and vref_s2d_rb, "6 on vref, 4 on vcm". hv NMOS to vss, the s2d pad's load-capacitor} 100 -730 0 0 0.25 0.25 {}
T {device type. vcm_rb keeps its CB (the buffer's phase margin); vref_s2d_rb has none (no loop). NMOS to vss only: PMOS to iovdd} 100 -708 0 0 0.25 0.25 {}
T {couples iovdd into vref, the S2D's zero point (explore_bypass.py).} 100 -686 0 0 0.25 0.25 {}
T {Shapes as drawn in the layout (pad_ref_rb v2, agent F): the gate area of the 12u x 12u array they replace, vref 9 x 144 um2, vcm 4 x 144 um2;} 100 -654 0 0 0.25 0.25 {}
T {"capacitor placement is pretty much ad lib (maintaining overall capacitance to the nodes and avoiding long interconnects)". Drawn from netlist/source/pad_ref_rb.spice} 100 -632 0 0 0.25 0.25 {}
T {[1] vcm 576 um2} 245 -323.5 0 0 0.3 0.3 {layer=10}
T {[2] vref 1297 um2} 645 -323.5 0 0 0.3 0.3 {layer=10}
N 100 -400 540 -400 {lab=vcm}
N 100 -460 820 -460 {lab=vref}
N 100 -100 860 -100 {lab=vss}
C {devices/iopin.sym} 100 -100 0 1 {name=p0 lab=vss}
C {devices/iopin.sym} 100 -400 0 1 {name=p1 lab=vcm}
C {devices/iopin.sym} 100 -460 0 1 {name=p2 lab=vref}
N 300 -400 300 -240 {lab=vcm}
N 260 -200 270 -200 {lab=vss}
N 260 -200 260 -100 {lab=vss}
N 300 -200 300 -100 {lab=vss}
N 330 -200 340 -200 {lab=vss}
N 340 -200 340 -100 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 300 -220 1 0 {name=CBM1
l=12.66u
w=19.24u
ng=1
m=2
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 420 -400 420 -240 {lab=vcm}
N 380 -200 390 -200 {lab=vss}
N 380 -200 380 -100 {lab=vss}
N 420 -200 420 -100 {lab=vss}
N 450 -200 460 -200 {lab=vss}
N 460 -200 460 -100 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 420 -220 1 0 {name=CBM2
l=3.25u
w=8.18u
ng=1
m=2
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 540 -400 540 -240 {lab=vcm}
N 500 -200 510 -200 {lab=vss}
N 500 -200 500 -100 {lab=vss}
N 540 -200 540 -100 {lab=vss}
N 570 -200 580 -200 {lab=vss}
N 580 -200 580 -100 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 540 -220 1 0 {name=CBM3
l=12.4u
w=2.9u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 700 -460 700 -240 {lab=vref}
N 660 -200 670 -200 {lab=vss}
N 660 -200 660 -100 {lab=vss}
N 700 -200 700 -100 {lab=vss}
N 730 -200 740 -200 {lab=vss}
N 740 -200 740 -100 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 700 -220 1 0 {name=CBR1
l=12u
w=12u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
N 820 -460 820 -240 {lab=vref}
N 780 -200 790 -200 {lab=vss}
N 780 -200 780 -100 {lab=vss}
N 820 -200 820 -100 {lab=vss}
N 850 -200 860 -200 {lab=vss}
N 860 -200 860 -100 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 820 -220 1 0 {name=CBR2
l=16.9u
w=34.1u
ng=1
m=2
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
