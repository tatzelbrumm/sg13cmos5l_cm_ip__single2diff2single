v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Template Testbench for disable / quiescent-current analysis - OgueyAebischerBias reference} 0 -960 0 0 0.5 0.5 {}
T {H. J. Oguey and D. Aebischer, “CMOS current reference without resistance,”
IEEE J. Solid-State Circuits, vol. 32, no. 7, pp. 1132-1135, Jul. 1997} 0 -430 0 0 0.3 0.3 {}
T {VDD is held at CACE\{vdd\} for the whole run - unlike reference_tb_tran.sch
this is not a start-up test. Vdis steps disable from 0 to CACE\{vdd\} at
t = 200us, and the run continues to 400us so the disabled state has time
to settle.

Timeline (fixed, NOT parameterised - the three numbers below must agree,
so if you change one, change all three):

  0 ... 200us     enabled     Iq_enabled  averaged over 150us..195us
  200us           disable rises, 100ns edge
  200 ... 400us   disabled    Iq_disabled averaged over 350us..395us

t_disable is the delay from that 200us edge until vbr falls back through
100mV, i.e. the same 100mV threshold reference_tb_tran.sch uses on the way
up. If vbr never gets there the meas fails, no value is echoed, and CACE
reports the parameter as failed - which is the correct outcome, because it
means the disable path does not actually shut the core down.} 600 -560 0 0 0.3 0.3 {}
T {Supply current sign: i(vdd) is the current flowing INTO the source's
positive terminal, so the current drawn from the supply is -i(vdd).
Both Iq values are negated below and are therefore positive for a
normally-operating circuit. A negative Iq in the results means the
DUT is sourcing current back into the rail - look at the netlist, not
at the sign convention.} 600 -240 0 0 0.3 0.3 {}
N 180 -140 180 -120 {lab=0}
N 420 -320 480 -320 {lab=vbp}
N 420 -300 480 -300 {lab=vbn}
N 420 -280 480 -280 {lab=vbr}
N 260 -280 300 -280 {lab=disable}
N 360 -260 360 -140 {lab=0}
N 260 -140 360 -140 {lab=0}
N 180 -180 180 -140 {lab=0}
N 260 -180 260 -140 {lab=0}
N 180 -140 260 -140 {lab=0}
N 260 -280 260 -240 {lab=disable}
N 360 -360 360 -340 {lab=#net1}
N 180 -360 360 -360 {lab=#net1}
N 180 -360 180 -240 {lab=#net1}
C {devices/code_shown.sym} 20 -890 0 0 {name=NGSPICE
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
tran CACE\{tstep=100n\} 400u
* supply current drawn = -i(vdd); vector is VDD#branch
meas tran iq_en_raw avg i(vdd) from=1.5e-4 to=1.95e-4
meas tran iq_dis_raw avg i(vdd) from=3.5e-4 to=3.95e-4
let Iq_enabled = -iq_en_raw
let Iq_disabled = -iq_dis_raw
* turn-off delay, referred to the 200us disable edge
meas tran t_dis_abs when v(vbr)=100m fall=1 td=2e-4
let t_disable = t_dis_abs - 2e-4
echo $&t_disable $&Iq_enabled $&Iq_disabled > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
C {devices/code_shown.sym} 20 -510 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
"}
C {reference.sym} 360 -300 0 0 {name=x1}
C {devices/vsource.sym} 180 -210 0 1 {name=VDD value=CACE\{vdd\}}
C {devices/gnd.sym} 180 -120 0 0 {name=l1 lab=0}
C {devices/vsource.sym} 260 -210 0 0 {name=Vdis value="dc 0 pulse(0 CACE\{vdd\} 200u 100n 100n 1 2)"}
C {devices/lab_wire.sym} 260 -280 0 0 {name=l6 lab=disable}
C {devices/lab_wire.sym} 480 -320 0 0 {name=l2 lab=vbp}
C {devices/lab_wire.sym} 480 -300 0 0 {name=l3 lab=vbn}
C {devices/lab_wire.sym} 480 -280 0 0 {name=l4 lab=vbr}
C {devices/title.sym} 160 -40 0 0 {name=l5 author="Christoph Maier"}
