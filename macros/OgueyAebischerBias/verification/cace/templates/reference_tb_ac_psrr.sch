v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Template Testbench for supply-rejection (AC) analysis - OgueyAebischerBias reference} 120 -830 0 0 0.5 0.5 {}
T {H. J. Oguey and D. Aebischer, “CMOS current reference without resistance,”
IEEE J. Solid-State Circuits, vol. 32, no. 7, pp. 1132-1135, Jul. 1997} 400 -140 0 0 0.3 0.3 {}
T {VDD carries a 1 V AC excitation on top of its DC value, so v(vbr) IS the
supply-to-vbr transfer function. PSRR is its inverse, in dB, so a large
positive number is good rejection. disable held low (enabled).

The .nodeset is the same hint used in reference_tb_dc.sch: without it the
op point ngspice finds before the AC sweep may be the degenerate
zero-current solution, and the AC result would be meaningless.} 510 -290 0 0 0.3 0.3 {}
N 180 -140 180 -120 {lab=0}
N 420 -320 480 -320 {lab=vbp}
N 420 -300 480 -300 {lab=vbn}
N 420 -280 480 -280 {lab=vbr}
N 260 -280 300 -280 {lab=#net1}
N 360 -260 360 -140 {lab=0}
N 260 -140 360 -140 {lab=0}
N 180 -180 180 -140 {lab=0}
N 260 -180 260 -140 {lab=0}
N 180 -140 260 -140 {lab=0}
N 260 -280 260 -240 {lab=#net1}
N 360 -360 360 -340 {lab=#net2}
N 180 -360 360 -360 {lab=#net2}
N 180 -360 180 -240 {lab=#net2}
C {devices/code_shown.sym} 20 -670 0 0 {name=NGSPICE
simulator=ngspice
only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.nodeset v(vbp)=200m
.control
save all
ac dec CACE\{ac_pts=21\} CACE\{fstart=1\} CACE\{fstop=1G\}
* v(vbr) is the vdd->vbr transfer (AC amplitude on VDD is exactly 1).
* PSRR_vbr = -20*log10(|v(vbr)|): positive dB = rejection.
let psrr_vbr_db = -db(v(vbr))
meas ac PSRR_vbr find psrr_vbr_db when frequency = CACE\{f_psrr=1000\}
echo $&PSRR_vbr > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
C {devices/code_shown.sym} 20 -780 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
"}
C {reference.sym} 360 -300 0 0 {name=x1}
C {devices/vsource.sym} 180 -210 0 1 {name=VDD value="dc CACE\{vdd\} ac 1"}
C {devices/gnd.sym} 180 -120 0 0 {name=l1 lab=0}
C {devices/vsource.sym} 260 -210 0 1 {name=Voff value=0}
C {devices/lab_wire.sym} 480 -320 0 0 {name=l2 lab=vbp}
C {devices/lab_wire.sym} 480 -300 0 0 {name=l3 lab=vbn}
C {devices/lab_wire.sym} 480 -280 0 0 {name=l4 lab=vbr}
C {devices/title.sym} 160 -40 0 0 {name=l5 author="Christoph Maier"}
