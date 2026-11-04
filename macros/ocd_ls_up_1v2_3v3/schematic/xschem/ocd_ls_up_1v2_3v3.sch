v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {ocd_ls_up_1v2_3v3: 1.2 V -> 3.3 V level shifter, non-inverting} -680 -300 0 0 0.5 0.5 {}
T {Input stage of analog_switch_small (2 x sg13cmos5l_inv_4 on vddl) feeding sw_lvl_shift of sg13cmos5l_ocd_ip__analog_switches.} -680 -270 0 0 0.3 0.3 {}
T {out follows in; the complementary output outn of sw_lvl_shift is not used (pin left open).} -680 -245 0 0 0.3 0.3 {}
N -650 -180 -590 -180 {lab=vss}
N -650 -150 -590 -150 {lab=vddl}
N -650 -120 -590 -120 {lab=vddh}
N -680 20 -620 20 {lab=in}
N -540 20 -500 20 {lab=inb}
N -500 -20 -500 20 {lab=inb}
N -500 -20 -340 -20 {lab=inb}
N -340 -20 -340 0 {lab=inb}
N -420 20 -340 20 {lab=inbb}
N -190 0 -130 0 {lab=out}
C {iopin.sym} -650 -180 0 1 {name=p1 lab=vss}
C {iopin.sym} -650 -150 0 1 {name=p2 lab=vddl}
C {iopin.sym} -650 -120 0 1 {name=p3 lab=vddh}
C {opin.sym} -130 0 0 0 {name=p4 lab=out}
C {ipin.sym} -680 20 0 0 {name=p5 lab=in}
C {lab_pin.sym} -590 -180 0 1 {name=p6 sig_type=std_logic lab=vss}
C {lab_pin.sym} -590 -150 0 1 {name=p7 sig_type=std_logic lab=vddl}
C {lab_pin.sym} -590 -120 0 1 {name=p8 sig_type=std_logic lab=vddh}
C {sg13cmos5l_stdcells/sg13cmos5l_inv_4.sym} -580 20 0 0 {name=x2 VDD=vddl VSS=vss prefix=sg13cmos5l_ }
C {sg13cmos5l_stdcells/sg13cmos5l_inv_4.sym} -460 20 0 0 {name=x3 VDD=vddl VSS=vss prefix=sg13cmos5l_ }
C {sw_lvl_shift.sym} -190 40 0 0 {name=x1 avdd=vddh avss=vss}
C {title.sym} -520 120 0 0 {name=l1 author="Christoph Maier"}
