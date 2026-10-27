v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Clamp_N_M1: the SG13_cm_clamps PCell as placed in sg13cmos5l_IOPadDiff2Single (ng = 34, l = 1u, frame 80u), twice} 60 -540 0 0 0.4 0.4 {}
T {34 fingers 4.4 / 1 um: W = 34 x 4.4 = 149.6 um. Drains = pad, sources = iovss (inner p+ ring), gate bus = gate.
The outer n+ ring in an NWell is unlabelled and floating in the PCell: tie it to iovdd above.
Taps are not netlist devices: KLayout LVS runs with --disable_tap_extraction.} 60 -500 0 0 0.25 0.25 {}
N 60 -340 260 -340 {lab=pad}
N 260 -340 260 -270 {lab=pad}
N 60 -240 220 -240 {lab=gate}
N 60 -140 290 -140 {lab=iovss}
N 260 -210 260 -140 {lab=iovss}
N 260 -240 290 -240 {lab=iovss}
N 290 -240 290 -140 {lab=iovss}
C {devices/ipin.sym} 60 -240 0 0 {name=p1 lab=gate}
C {devices/iopin.sym} 60 -140 0 1 {name=p2 lab=iovss}
C {devices/iopin.sym} 60 -340 0 1 {name=p3 lab=pad}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 240 -240 0 0 {name=MN0
l=1u
w=149.6u
ng=34
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
