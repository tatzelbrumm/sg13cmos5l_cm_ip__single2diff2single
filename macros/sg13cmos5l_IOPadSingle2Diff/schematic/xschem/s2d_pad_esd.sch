v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {devices/iopin.sym} 60 -400 0 1 {name=p1 lab=iovdd}
C {devices/iopin.sym} 60 0 0 1 {name=p2 lab=iovss}
C {devices/iopin.sym} 60 -200 0 1 {name=p3 lab=pad}
N 60 -400 920 -400 {lab=iovdd}
N 60 0 920 0 {lab=iovss}
N 60 -200 840 -200 {lab=pad}
C {sg13cmos5l_pr/dpantenna.sym} 320 -300 0 0 {name=DP1
model=dpantenna
l=27.78u
w=1.26u
spiceprefix=X
}
N 320 -330 320 -400 {lab=iovdd}
N 320 -270 320 -200 {lab=pad}
C {sg13cmos5l_pr/dantenna.sym} 320 -100 0 0 {name=DN1
model=dantenna
l=27.78u
w=1.26u
spiceprefix=X
}
N 320 -130 320 -200 {lab=pad}
N 320 -70 320 0 {lab=iovss}
C {sg13cmos5l_pr/dpantenna.sym} 440 -300 0 0 {name=DP2
model=dpantenna
l=27.78u
w=1.26u
spiceprefix=X
}
N 440 -330 440 -400 {lab=iovdd}
N 440 -270 440 -200 {lab=pad}
C {sg13cmos5l_pr/dantenna.sym} 440 -100 0 0 {name=DN2
model=dantenna
l=27.78u
w=1.26u
spiceprefix=X
}
N 440 -130 440 -200 {lab=pad}
N 440 -70 440 0 {lab=iovss}
C {sg13cmos5l_pr/rppd.sym} 640 -330 0 0 {name=RP
w=0.5u
l=12.9u
model=rppd
body=sub!
spiceprefix=X
b=0
m=1}
N 640 -360 640 -400 {lab=iovdd}
N 640 -300 800 -300 {lab=gp}
C {devices/lab_wire.sym} 740 -300 0 1 {name=l1 lab=gp}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 820 -300 0 0 {name=MCP
l=0.6u
w=266.4u
ng=40
m=1
model=sg13_hv_pmos
spiceprefix=X
}
N 840 -330 840 -400 {lab=iovdd}
N 840 -270 840 -200 {lab=pad}
N 840 -300 920 -300 {lab=iovdd}
N 920 -300 920 -400 {lab=iovdd}
C {sg13cmos5l_pr/rppd.sym} 640 -70 0 0 {name=RN
w=0.5u
l=3.54u
model=rppd
body=sub!
spiceprefix=X
b=0
m=1}
N 640 -40 640 0 {lab=iovss}
N 640 -100 800 -100 {lab=gn}
C {devices/lab_wire.sym} 740 -100 0 1 {name=l2 lab=gn}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 820 -100 0 0 {name=MCN
l=0.6u
w=88u
ng=20
m=1
model=sg13_hv_nmos
spiceprefix=X
}
N 840 -130 840 -200 {lab=pad}
N 840 -70 840 0 {lab=iovss}
N 840 -100 920 -100 {lab=iovss}
N 920 -100 920 0 {lab=iovss}
T {s2d_pad_esd: the protection left standing in the s2d pad template (layout/klayout/template, version 4)} 0 -900 0 0 0.5 0.5 {}
T {Devices and values as drawn and as extracted with IHP's KLayout LVS (template/lvs/template_extracted.cir on the notes branch).} 0 -840 0 0 0.3 0.3 {}
T {They are IHP's IOPadAnalog protection without its SecondaryProtection: DCNDiode, DCPDiode, Clamp_N20N0D, Clamp_P20N0D.} 0 -800 0 0 0.3 0.3 {}
T {DN1/2, DP1/2: the primary diodes, 2 stripes of 1.26 x 27.78 um each (DCNDiode / DCPDiode). They carry the ESD current pad -> iovss and pad -> iovdd.} 0 -760 0 0 0.3 0.3 {}
T {MCN, MCP: the clamps, 20 hv NMOS fingers 4.4/0.6 and 20 x 2 hv PMOS fingers 6.66/0.6, drains on the pad (1.18 um drain ballast).} 0 -720 0 0 0.3 0.3 {}
T {RN (1959 Ohm), RP (6768 Ohm): the "0D" gate tie-off of IHP's Clamp_N20N0D / Clamp_P20N0D (XR0 in sg13cmos5l_io.spice). Each holds its clamp's gate} 0 -680 0 0 0.3 0.3 {}
T {at the clamp's own source rail, so the clamp is off in operation and the pad sees only drain junctions. Reasoning, not documented by IHP: the tie goes} 0 -640 0 0 0.3 0.3 {}
T {through a resistor and not a wire so that a fast ESD edge, coupled through the gate-drain capacitance, lifts the gate for about R x C_gate and turns the} 0 -600 0 0 0.3 0.3 {}
T {clamp on (gate-coupled triggering), and the gate oxide does not sit directly on a rail node during a CDM event.} 0 -560 0 0 0.3 0.3 {}
T {Difference to IHP: RP lies on the substrate here (body sub!); in IHP's cell its body is iovdd. Not drawn: the ptap1 "resistors" XR1 of IHP's spice} 0 -520 0 0 0.3 0.3 {}
T {(iovss - sub!, about 10 Ohm) are the substrate taps of the guard rings, extracted as devices, not resistors anyone drew.} 0 -480 0 0 0.3 0.3 {}
