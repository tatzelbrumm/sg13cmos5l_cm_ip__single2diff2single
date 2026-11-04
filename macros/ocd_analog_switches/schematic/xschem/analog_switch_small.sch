v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -90 -70 -90 -30 {lab=in}
N 0 -70 90 -70 {lab=in}
N 90 -70 90 -30 {lab=in}
N -90 30 -90 70 {lab=out}
N 0 70 90 70 {lab=out}
N 90 30 90 70 {lab=out}
N -90 0 -40 0 {lab=avss}
N 40 0 90 0 {lab=avdd}
N -40 -50 -40 0 {lab=avss}
N 40 -20 40 0 {lab=avdd}
N 0 -100 0 -70 {lab=in}
N -90 -70 0 -70 {lab=in}
N 0 70 0 100 {lab=out}
N -90 70 0 70 {lab=out}
N 130 0 180 0 {lab=#net1}
N -160 20 -160 140 {lab=#net1}
N -160 140 180 140 {lab=#net1}
N 180 0 180 140 {lab=#net1}
N -650 -180 -590 -180 {lab=dvdd}
N -650 -150 -590 -150 {lab=dvss}
N -650 -120 -590 -120 {lab=avdd}
N -650 -90 -590 -90 {lab=avss}
N -540 20 -500 20 {lab=#net2}
N -190 0 -130 0 {lab=#net3}
N -190 20 -160 20 {lab=#net1}
N -680 20 -620 20 {lab=enable}
N -620 130 -580 130 {lab=enable}
N -620 20 -620 130 {lab=enable}
N -420 20 -340 20 {lab=#net4}
N -500 -20 -500 20 {lab=#net2}
N -500 -20 -340 -20 {lab=#net2}
N -340 -20 -340 -0 {lab=#net2}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} -110 0 0 0 {name=M1
l=0.45u
w=5u
ng=1
m=4
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 110 0 0 1 {name=M2
l=0.4u
w=5u
ng=1
m=4
model=sg13_hv_pmos
spiceprefix=X
}
C {lab_pin.sym} 40 -20 0 0 {name=p1 sig_type=std_logic lab=avdd}
C {lab_pin.sym} -40 -50 0 1 {name=p2 sig_type=std_logic lab=avss}
C {iopin.sym} 0 -100 0 0 {name=p3 lab=in}
C {iopin.sym} 0 100 0 0 {name=p4 lab=out}
C {sg13cmos5l_stdcells/sg13cmos5l_inv_4.sym} -580 20 0 0 {name=x2 VDD=dvdd VSS=dvss prefix=sg13cmos5l_ }
C {sg13cmos5l_stdcells/sg13cmos5l_inv_4.sym} -460 20 0 0 {name=x3 VDD=dvdd VSS=dvss prefix=sg13cmos5l_ }
C {sg13cmos5l_stdcells/sg13cmos5l_antennanp.sym} -490 130 0 0 {name=x4 VDD=dvdd VSS=dvss prefix=sg13cmos5l_ }
C {sg13cmos5l_stdcells/sg13cmos5l_decap_4.sym} -490 180 0 0 {name=x5[1:0] VDD=dvdd VSS=dvss prefix=sg13cmos5l_ }
C {ipin.sym} -680 20 0 0 {name=p5 lab=enable}
C {iopin.sym} -650 -180 0 1 {name=p6 lab=dvdd}
C {iopin.sym} -650 -150 0 1 {name=p7 lab=dvss}
C {iopin.sym} -650 -120 0 1 {name=p8 lab=avdd}
C {iopin.sym} -650 -90 0 1 {name=p9 lab=avss}
C {lab_pin.sym} -590 -180 0 1 {name=p10 sig_type=std_logic lab=dvdd}
C {lab_pin.sym} -590 -150 0 1 {name=p11 sig_type=std_logic lab=dvss}
C {lab_pin.sym} -590 -120 0 1 {name=p12 sig_type=std_logic lab=avdd}
C {lab_pin.sym} -590 -90 0 1 {name=p13 sig_type=std_logic lab=avss}
C {sw_lvl_shift.sym} -190 40 0 0 {name=x5 avdd=avdd avss=avss}
