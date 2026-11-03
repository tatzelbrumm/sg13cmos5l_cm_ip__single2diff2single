v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {d2s_sp2k: 2 kOhm secondary protection stage in front of CMA / CMB (pad level, 2 instances)} 0 -480 0 0 0.45 0.45 {}
T {IHP's sg13cmos5l_SecondaryProtection with a longer resistor, as drawn in d2s_sp2k_f2 (C2, F2 stage B, 2026-11-03):} 0 -430 0 0 0.25 0.25 {}
T {rppd 1u x 7.435u (1991.6 Ohm) from the pad to core; dantenna 0.64u x 3.1u core to iovss, dpantenna 0.64u x 4.98u core to iovdd.} 0 -405 0 0 0.25 0.25 {}
T {Netlist reference: ../../netlist/source/sg13cmos5l_IOPadDiff2Single.spice (.subckt d2s_sp2k)} 0 -380 0 0 0.25 0.25 {}
C {devices/iopin.sym} 560 -100 0 0 {name=p1 lab=core}
C {devices/iopin.sym} 60 -300 0 1 {name=p2 lab=iovdd}
C {devices/iopin.sym} 60 100 0 1 {name=p3 lab=iovss}
C {devices/iopin.sym} 60 -100 0 1 {name=p4 lab=pad}
N 60 -300 360 -300 {lab=iovdd}
N 60 100 360 100 {lab=iovss}
N 60 -100 190 -100 {lab=pad}
C {sg13cmos5l_pr/rppd.sym} 220 -100 3 0 {name=R0
w=1u
l=7.435u
model=rppd
body=iovss
spiceprefix=X
b=0
m=1
mm_ok=1}
N 250 -100 560 -100 {lab=core}
C {sg13cmos5l_pr/dpantenna.sym} 360 -200 0 0 {name=D0
model=dpantenna
l=4.98u
w=0.64u
spiceprefix=X}
N 360 -230 360 -300 {lab=iovdd}
N 360 -170 360 -100 {lab=core}
C {sg13cmos5l_pr/dantenna.sym} 360 0 0 0 {name=D1
model=dantenna
l=3.1u
w=0.64u
spiceprefix=X}
N 360 -30 360 -100 {lab=core}
N 360 30 360 100 {lab=iovss}
T {rppd body = iovss} 160 -60 0 0 0.2 0.2 {}
C {devices/title.sym} 160 220 0 0 {name=l1 author="Christoph Maier"}
