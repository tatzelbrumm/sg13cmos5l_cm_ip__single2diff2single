v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 300 -280 300 -250 {lab=vout}
N 300 -190 300 -120 {lab=vssio}
N 300 -120 320 -120 {lab=vssio}
N 320 -220 320 -120 {lab=vssio}
N 300 -220 320 -220 {lab=vssio}
N 300 -440 320 -440 {lab=#net1}
N 300 -340 320 -340 {lab=#net1}
N 300 -280 360 -280 {lab=vout}
N 300 -310 300 -280 {lab=vout}
N 120 -120 300 -120 {lab=vssio}
N 300 -440 300 -370 {}
N 320 -440 320 -340 {}
C {title.sym} 160 -40 0 0 {name=l1 author="Christoph Maier"}
C {/foss/designs/sg13cmos5l_cm_ip__single2diff2single/macros/IOPad/schematic/xschem/sg13cmos5l_ClampN15N15.sym} 280 -220 0 0 {name=M1
l=0.6u
w=4.4u
 ng=1
 m=15
  mm_ok=1
 model=sg13_hv_nmos
spiceprefix=X
}
C {/foss/designs/sg13cmos5l_cm_ip__single2diff2single/macros/IOPad/schematic/xschem/sg13cmos5l_ClampP15N15.sym} 280 -340 0 0 {name=M2
l=0.6u
w=6.66u
 ng=2
 m=15
  mm_ok=1
 model=sg13_hv_pmos
spiceprefix=X
}
C {devices/iopin.sym} 120 -200 2 0 {name=p1 lab=vdd_3v3}
C {devices/iopin.sym} 120 -180 2 0 {name=p2 lab=vdd_1v2}
C {devices/iopin.sym} 120 -160 2 0 {name=p3 lab=vss_3v3}
C {devices/iopin.sym} 120 -140 2 0 {name=p4 lab=vss_1v2}
C {devices/iopin.sym} 120 -120 2 0 {name=p5 lab=vssio}
C {devices/opin.sym} 360 -280 2 1 {name=p19 lab=vout}
