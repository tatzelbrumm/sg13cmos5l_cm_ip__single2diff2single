v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 60 -70 60 -30 {lab=in}
N 150 -70 240 -70 {lab=in}
N 240 -70 240 -30 {lab=in}
N 60 30 60 70 {lab=out}
N 150 70 240 70 {lab=out}
N 240 30 240 70 {lab=out}
N 60 0 110 0 {lab=avss}
N 190 0 240 0 {lab=avdd}
N 110 -50 110 0 {lab=avss}
N 190 -20 190 0 {lab=avdd}
N 150 -100 150 -70 {lab=in}
N 60 -70 150 -70 {lab=in}
N 150 70 150 100 {lab=out}
N 60 70 150 70 {lab=out}
N 280 0 330 0 {lab=#net1}
N -10 20 -10 140 {lab=#net1}
N -10 140 330 140 {lab=#net1}
N 330 0 330 140 {lab=#net1}
N -520 0 -500 0 {lab=#net2}
N -650 -180 -590 -180 {lab=dvdd}
N -650 -150 -590 -150 {lab=dvss}
N -650 -120 -590 -120 {lab=avdd}
N -650 -90 -590 -90 {lab=avss}
N -370 40 -340 40 {lab=avdd}
N -370 60 -340 60 {lab=avss}
N -520 0 -520 40 {lab=#net2}
N -540 0 -520 0 {lab=#net2}
N -520 40 -430 40 {lab=#net2}
N -430 20 -430 40 {lab=#net2}
N -40 0 20 0 {lab=#net3}
N -40 20 -10 20 {lab=#net1}
N -680 -0 -620 -0 {lab=enable}
N -420 0 -340 0 {lab=#net4}
N -430 20 -340 20 {lab=#net2}
N -620 110 -580 110 {lab=enable}
N -620 0 -620 110 {lab=enable}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 40 0 0 0 {name=M1
l=0.45u
w=10u
ng=1
m=40
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 260 0 0 1 {name=M2
l=0.4u
w=10u
ng=1
m=40
model=sg13_hv_pmos
spiceprefix=X
}
C {lab_pin.sym} 190 -20 0 0 {name=p1 sig_type=std_logic lab=avdd}
C {lab_pin.sym} 110 -50 0 1 {name=p2 sig_type=std_logic lab=avss}
C {iopin.sym} 150 -100 0 0 {name=p3 lab=in}
C {iopin.sym} 150 100 0 0 {name=p4 lab=out}
C {sg13cmos5l_stdcells/sg13cmos5l_inv_4.sym} -580 0 0 0 {name=x2 VDD=dvdd VSS=dvss prefix=sg13cmos5l_ }
C {sg13cmos5l_stdcells/sg13cmos5l_inv_4.sym} -460 0 0 0 {name=x3 VDD=dvdd VSS=dvss prefix=sg13cmos5l_ }
C {sg13cmos5l_stdcells/sg13cmos5l_antennanp.sym} -490 110 0 0 {name=x4 VDD=dvdd VSS=dvss prefix=sg13cmos5l_ }
C {sg13cmos5l_stdcells/sg13cmos5l_decap_4.sym} -490 160 0 0 {name=x5[1:0] VDD=dvdd VSS=dvss prefix=sg13cmos5l_ }
C {ipin.sym} -680 0 0 0 {name=p5 lab=enable}
C {iopin.sym} -650 -180 0 1 {name=p6 lab=dvdd}
C {iopin.sym} -650 -150 0 1 {name=p7 lab=dvss}
C {iopin.sym} -650 -120 0 1 {name=p8 lab=avdd}
C {iopin.sym} -650 -90 0 1 {name=p9 lab=avss}
C {lab_pin.sym} -590 -180 0 1 {name=p10 sig_type=std_logic lab=dvdd}
C {lab_pin.sym} -590 -150 0 1 {name=p11 sig_type=std_logic lab=dvss}
C {lab_pin.sym} -590 -120 0 1 {name=p12 sig_type=std_logic lab=avdd}
C {lab_pin.sym} -590 -90 0 1 {name=p13 sig_type=std_logic lab=avss}
C {gate_drive_med.sym} -190 40 0 0 {name=x1}
C {lab_pin.sym} -370 60 0 0 {name=p14 sig_type=std_logic lab=avss}
C {lab_pin.sym} -370 40 0 0 {name=p15 sig_type=std_logic lab=avdd}
