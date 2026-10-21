v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Template Testbench for start-up transient analysis - OgueyAebischerBias reference} 120 -860 0 0 0.5 0.5 {}
T {H. J. Oguey and D. Aebischer, “CMOS current reference without resistance,”
IEEE J. Solid-State Circuits, vol. 32, no. 7, pp. 1132-1135, Jul. 1997} 500 -390 0 0 0.3 0.3 {}
T {Deliberately NO .nodeset here: VDD ramps from 0 to CACE\{vdd\} and the DUT's
own start-up (kick) circuit has to escape the zero-current state unaided.
A corner/mismatch run where t_startup is never measured is a start-up
failure at that point, which is the point of this testbench.} 500 -250 0 0 0.3 0.3 {}
N 440 -260 440 -140 {lab=0}
N 500 -320 560 -320 {lab=vbp}
N 500 -300 560 -300 {lab=vbn}
N 500 -280 560 -280 {lab=vbr}
N 340 -280 380 -280 {lab=#net1}
N 340 -280 340 -240 {lab=#net1}
N 440 -360 440 -340 {lab=#net2}
N 260 -360 440 -360 {lab=#net2}
N 260 -360 260 -240 {lab=#net2}
N 260 -180 260 -140 {lab=0}
N 340 -140 440 -140 {lab=0}
N 340 -180 340 -140 {lab=0}
N 300 -140 340 -140 {lab=0}
N 300 -140 300 -120 {lab=0}
N 260 -140 300 -140 {lab=0}
C {devices/code_shown.sym} 20 -690 0 0 {name=NGSPICE
simulator=ngspice
only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
save all
tran CACE\{tstep\} CACE\{tstop\}
meas tran t_startup WHEN v(vbr)=100m RISE=1
meas tran Vbp_final find v(vbp) at=CACE\{tstop\}
meas tran Vbn_final find v(vbn) at=CACE\{tstop\}
meas tran Vbr_final find v(vbr) at=CACE\{tstop\}
echo $&t_startup $&Vbp_final $&Vbn_final $&Vbr_final > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
C {devices/code_shown.sym} 20 -810 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
"}
C {devices/vsource.sym} 260 -210 0 1 {name=VDD value="dc CACE\{vdd\} pwl(0 0 1u CACE\{vdd\})"}
C {devices/gnd.sym} 300 -120 0 0 {name=l1 lab=0}
C {devices/vsource.sym} 340 -210 0 1 {name=Voff value=0}
C {devices/title.sym} 160 -40 0 0 {name=l5 author="Christoph Maier"}
C {reference.sym} 440 -300 0 0 {name=x1}
C {devices/lab_wire.sym} 560 -320 0 0 {name=l2 lab=vbp}
C {devices/lab_wire.sym} 560 -300 0 0 {name=l3 lab=vbn}
C {devices/lab_wire.sym} 560 -280 0 0 {name=l4 lab=vbr}
