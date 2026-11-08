v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s7_doutpd: pull-downs that hold the unused harness dig_out[11:0] of slot 7 low} 0 -760 0 0 0.4 0.4 {}
T {M0..M11: sg13_hv_nmos 0.5u / 0.45u, drain on d<k> (harness dig_out<k>), gate on vdd_1v2, source on vss_1v2,} 40 -700 0 0 0.25 0.25 {}
T {bulk on vss_3v3. While the slot vdd_1v2 is up each line is pulled to vss_1v2; with vdd_1v2 off the lines float.} 40 -676 0 0 0.25 0.25 {}
T {Back-annotated from the slot layout. Source: netlist/source/slot_7.spice (subckt s7_doutpd).} 40 -652 0 0 0.25 0.25 {}
N 320 -30 320 -540 {lab=d0}
N 320 -540 2200 -540 {lab=d0}
N 280 0 260 0 {lab=vdd_1v2}
N 260 0 260 80 {lab=vdd_1v2}
N 320 30 320 140 {lab=vss_1v2}
N 320 0 340 0 {lab=vss_3v3}
N 340 0 340 200 {lab=vss_3v3}
N 480 -30 480 -500 {lab=d1}
N 480 -500 2200 -500 {lab=d1}
N 440 0 420 0 {lab=vdd_1v2}
N 420 0 420 80 {lab=vdd_1v2}
N 480 30 480 140 {lab=vss_1v2}
N 480 0 500 0 {lab=vss_3v3}
N 500 0 500 200 {lab=vss_3v3}
N 640 -30 640 -460 {lab=d2}
N 640 -460 2200 -460 {lab=d2}
N 600 0 580 0 {lab=vdd_1v2}
N 580 0 580 80 {lab=vdd_1v2}
N 640 30 640 140 {lab=vss_1v2}
N 640 0 660 0 {lab=vss_3v3}
N 660 0 660 200 {lab=vss_3v3}
N 800 -30 800 -420 {lab=d3}
N 800 -420 2200 -420 {lab=d3}
N 760 0 740 0 {lab=vdd_1v2}
N 740 0 740 80 {lab=vdd_1v2}
N 800 30 800 140 {lab=vss_1v2}
N 800 0 820 0 {lab=vss_3v3}
N 820 0 820 200 {lab=vss_3v3}
N 960 -30 960 -380 {lab=d4}
N 960 -380 2200 -380 {lab=d4}
N 920 0 900 0 {lab=vdd_1v2}
N 900 0 900 80 {lab=vdd_1v2}
N 960 30 960 140 {lab=vss_1v2}
N 960 0 980 0 {lab=vss_3v3}
N 980 0 980 200 {lab=vss_3v3}
N 1120 -30 1120 -340 {lab=d5}
N 1120 -340 2200 -340 {lab=d5}
N 1080 0 1060 0 {lab=vdd_1v2}
N 1060 0 1060 80 {lab=vdd_1v2}
N 1120 30 1120 140 {lab=vss_1v2}
N 1120 0 1140 0 {lab=vss_3v3}
N 1140 0 1140 200 {lab=vss_3v3}
N 1280 -30 1280 -300 {lab=d6}
N 1280 -300 2200 -300 {lab=d6}
N 1240 0 1220 0 {lab=vdd_1v2}
N 1220 0 1220 80 {lab=vdd_1v2}
N 1280 30 1280 140 {lab=vss_1v2}
N 1280 0 1300 0 {lab=vss_3v3}
N 1300 0 1300 200 {lab=vss_3v3}
N 1440 -30 1440 -260 {lab=d7}
N 1440 -260 2200 -260 {lab=d7}
N 1400 0 1380 0 {lab=vdd_1v2}
N 1380 0 1380 80 {lab=vdd_1v2}
N 1440 30 1440 140 {lab=vss_1v2}
N 1440 0 1460 0 {lab=vss_3v3}
N 1460 0 1460 200 {lab=vss_3v3}
N 1600 -30 1600 -220 {lab=d8}
N 1600 -220 2200 -220 {lab=d8}
N 1560 0 1540 0 {lab=vdd_1v2}
N 1540 0 1540 80 {lab=vdd_1v2}
N 1600 30 1600 140 {lab=vss_1v2}
N 1600 0 1620 0 {lab=vss_3v3}
N 1620 0 1620 200 {lab=vss_3v3}
N 1760 -30 1760 -180 {lab=d9}
N 1760 -180 2200 -180 {lab=d9}
N 1720 0 1700 0 {lab=vdd_1v2}
N 1700 0 1700 80 {lab=vdd_1v2}
N 1760 30 1760 140 {lab=vss_1v2}
N 1760 0 1780 0 {lab=vss_3v3}
N 1780 0 1780 200 {lab=vss_3v3}
N 1920 -30 1920 -140 {lab=d10}
N 1920 -140 2200 -140 {lab=d10}
N 1880 0 1860 0 {lab=vdd_1v2}
N 1860 0 1860 80 {lab=vdd_1v2}
N 1920 30 1920 140 {lab=vss_1v2}
N 1920 0 1940 0 {lab=vss_3v3}
N 1940 0 1940 200 {lab=vss_3v3}
N 2080 -30 2080 -100 {lab=d11}
N 2080 -100 2200 -100 {lab=d11}
N 2040 0 2020 0 {lab=vdd_1v2}
N 2020 0 2020 80 {lab=vdd_1v2}
N 2080 30 2080 140 {lab=vss_1v2}
N 2080 0 2100 0 {lab=vss_3v3}
N 2100 0 2100 200 {lab=vss_3v3}
N 60 80 2020 80 {lab=vdd_1v2}
N 60 140 2080 140 {lab=vss_1v2}
N 60 200 2100 200 {lab=vss_3v3}
C {devices/opin.sym} 2200 -540 0 0 {name=p_d0 lab=d0}
C {devices/opin.sym} 2200 -500 0 0 {name=p_d1 lab=d1}
C {devices/opin.sym} 2200 -460 0 0 {name=p_d2 lab=d2}
C {devices/opin.sym} 2200 -420 0 0 {name=p_d3 lab=d3}
C {devices/opin.sym} 2200 -380 0 0 {name=p_d4 lab=d4}
C {devices/opin.sym} 2200 -340 0 0 {name=p_d5 lab=d5}
C {devices/opin.sym} 2200 -300 0 0 {name=p_d6 lab=d6}
C {devices/opin.sym} 2200 -260 0 0 {name=p_d7 lab=d7}
C {devices/opin.sym} 2200 -220 0 0 {name=p_d8 lab=d8}
C {devices/opin.sym} 2200 -180 0 0 {name=p_d9 lab=d9}
C {devices/opin.sym} 2200 -140 0 0 {name=p_d10 lab=d10}
C {devices/opin.sym} 2200 -100 0 0 {name=p_d11 lab=d11}
C {devices/iopin.sym} 60 80 0 1 {name=p_vdd_1v2 lab=vdd_1v2}
C {devices/iopin.sym} 60 140 0 1 {name=p_vss_1v2 lab=vss_1v2}
C {devices/iopin.sym} 60 200 0 1 {name=p_vss_3v3 lab=vss_3v3}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 300 0 0 0 {name=M0
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 460 0 0 0 {name=M1
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 620 0 0 0 {name=M2
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 780 0 0 0 {name=M3
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 940 0 0 0 {name=M4
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1100 0 0 0 {name=M5
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1260 0 0 0 {name=M6
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1420 0 0 0 {name=M7
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1580 0 0 0 {name=M8
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1740 0 0 0 {name=M9
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1900 0 0 0 {name=M10
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 2060 0 0 0 {name=M11
l=0.45u
w=0.5u
ng=1
m=1
mm_ok=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/title.sym} 160 300 0 0 {name=l0 author="Christoph Maier"}
