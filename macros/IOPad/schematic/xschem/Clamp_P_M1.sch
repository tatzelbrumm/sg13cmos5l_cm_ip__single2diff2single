v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Clamp_P_M1: the SG13_cm_clamps PCell as placed in sg13cmos5l_IOPadDiff2Single (ng = 41, l = 0.6u, frame 80u)} 60 -540 0 0 0.4 0.4 {}
T {Two rows of 41 fingers 6.66 / 0.6 um: 82 fingers, W = 41 x 13.32 = 546.12 um, as OP in d2s_mpdda_pd.
Drains = pad, sources and NWell = iovdd (inner n+ ring), gate bus = gate; the outer p+ substrate-tap ring = iovss.
Taps are not netlist devices: KLayout LVS runs with --disable_tap_extraction.} 60 -500 0 0 0.25 0.25 {}
T {iovss: no device} 90 -115 0 0 0.25 0.25 {}
N 60 -340 290 -340 {lab=iovdd}
N 260 -340 260 -270 {lab=iovdd}
N 260 -240 290 -240 {lab=iovdd}
N 290 -340 290 -240 {lab=iovdd}
N 60 -240 220 -240 {lab=gate}
N 60 -160 260 -160 {lab=pad}
N 260 -210 260 -160 {lab=pad}
C {devices/ipin.sym} 60 -240 0 0 {name=p1 lab=gate}
C {devices/iopin.sym} 60 -340 0 1 {name=p2 lab=iovdd}
C {devices/iopin.sym} 60 -100 0 1 {name=p3 lab=iovss}
C {devices/iopin.sym} 60 -160 0 1 {name=p4 lab=pad}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 240 -240 0 0 {name=MP0
l=0.6u
w=546.12u
ng=82
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
