v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {DCPDiode: the SG13_cm_clamps PCell as placed in sg13cmos5l_IOPadDiff2Single (l = 63.78u)} 60 -540 0 0 0.4 0.4 {}
T {Two p+ stripes 1.26 x 63.78 um = anode, in an NWell with an n+ frame = cathode;
the p+ substrate-tap guard ring = guard. IHP's sg13cmos5l_DCPDiode is the same cell at l = 27.78u.
Taps and the NWell-to-substrate diode are not netlist devices: KLayout LVS runs with --disable_tap_extraction.} 60 -500 0 0 0.25 0.25 {}
T {guard: no device} 90 -255 0 0 0.25 0.25 {}
N 60 -340 460 -340 {lab=cathode}
N 340 -340 340 -290 {lab=cathode}
N 460 -340 460 -290 {lab=cathode}
N 60 -140 460 -140 {lab=anode}
N 340 -230 340 -140 {lab=anode}
N 460 -230 460 -140 {lab=anode}
C {devices/iopin.sym} 60 -140 0 1 {name=p1 lab=anode}
C {devices/iopin.sym} 60 -340 0 1 {name=p2 lab=cathode}
C {devices/iopin.sym} 60 -240 0 1 {name=p3 lab=guard}
C {sg13cmos5l_pr/dpantenna.sym} 340 -260 0 0 {name=D0
model=dpantenna
l=63.78u
w=1.26u
spiceprefix=X
}
C {sg13cmos5l_pr/dpantenna.sym} 460 -260 0 0 {name=D1
model=dpantenna
l=63.78u
w=1.26u
spiceprefix=X
}
C {devices/title.sym} 160 -40 0 0 {name=l0 author="Christoph Maier"}
