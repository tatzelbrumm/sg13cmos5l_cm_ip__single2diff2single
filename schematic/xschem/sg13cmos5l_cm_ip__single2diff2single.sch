v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {single-ended <-> differential <-> single-ended top level
Boundary reconciled against sudelbuecher/description/s2d_d2s_pinbuffers.md
and sg13cmos5l_ocd_chipalooza/verilog/rtl/user_project_wrapper_3a.v -- see
TOP_LEVEL_MODULE.md. No scan chain (reopened, not settled -- see log).
No pin for spec's reset: user_project_wrapper_3a.v has no per-project
reset port, only a chip-global one via housekeeping SPI.} 40 -830 0 0 0.3 0.3 {}
C {devices/iopin.sym} 140 -680 2 0 {name=p1 lab=vdd_3v3}
C {devices/iopin.sym} 140 -660 2 0 {name=p2 lab=vdd_1v2}
C {devices/iopin.sym} 140 -640 2 0 {name=p3 lab=vss_3v3}
C {devices/iopin.sym} 140 -620 2 0 {name=p4 lab=vss_1v2}
C {devices/iopin.sym} 140 -600 2 0 {name=p5 lab=vssio}
C {devices/ipin.sym} 140 -560 2 1 {name=p6 lab=ena}
C {devices/ipin.sym} 140 -540 2 1 {name=p7 lab=clk}
C {devices/ipin.sym} 140 -500 2 1 {name=p8 lab=outbuf_en}
C {devices/ipin.sym} 140 -480 2 1 {name=p9 lab=inbuf_en}
C {devices/ipin.sym} 140 -460 2 1 {name=p10 lab=filter_en}
C {devices/ipin.sym} 140 -440 2 1 {name=p11 lab=vdiff_en[1]}
C {devices/ipin.sym} 140 -420 2 1 {name=p12 lab=vdiff_en[0]}
C {devices/ipin.sym} 140 -400 2 1 {name=p13 lab=vcmsel[1]}
C {devices/ipin.sym} 140 -380 2 1 {name=p14 lab=vcmsel[0]}
C {devices/ipin.sym} 140 -340 2 1 {name=p15 lab=ibias}
C {devices/ipin.sym} 140 -320 2 1 {name=p16 lab=igmc}
C {devices/ipin.sym} 140 -300 2 1 {name=p17 lab=vbias}
C {devices/ipin.sym} 140 -260 2 1 {name=p18 lab=vin}
C {devices/opin.sym} 140 -220 2 0 {name=p19 lab=vout}
C {devices/iopin.sym} 140 -180 2 0 {name=p20 lab=vcm}
C {devices/iopin.sym} 140 -140 2 0 {name=p21 lab=vdiffp}
C {devices/iopin.sym} 140 -120 2 0 {name=p22 lab=vdiffn}
C {title.sym} 160 -40 0 0 {name=l1 author="Stefan Schippers"}
