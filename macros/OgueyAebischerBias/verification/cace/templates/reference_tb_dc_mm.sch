v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Template Testbench for mismatch Monte Carlo - OgueyAebischerBias reference} 120 -890 0 0 0.5 0.5 {}
T {H. J. Oguey and D. Aebischer, “CMOS current reference without resistance,”
IEEE J. Solid-State Circuits, vol. 32, no. 7, pp. 1132-1135, Jul. 1997} 400 -140 0 0 0.3 0.3 {}
T {Same operating point as reference_tb_dc.sch, but reported as two matching
figures in %, and run under corner_mos=tt_mismatch / corner_r=typ_mismatch
with collate: iterations, so CACE spreads the population itself. The per-
iteration seed comes from the SEED= expression, exactly as in the other
templates.

Run this on the SCHEMATIC netlist only. Magic's extracted netlist carries
no mm_ok=1 on its devices and splits multi-finger devices apart, so a
mismatch run against the extracted view silently produces min = typ = max,
which reads as a pass. See CLAUDE.md, "Traps that have already cost hours".} 400 -560 0 0 0.3 0.3 {}
T {The three ammeters already in OgueyAebischerBias.sch
----------------------------------------------------
  Vi1     PMOS M12 (m=1) in series with NMOS M10 (m=4)  -> core current I1
  Vi4     PMOS M13 (m=4) in series with NMOS M11 (m=1)  -> I2, nominally 4*I1
  Viaux   PMOS M14 (m=2) in series with NMOS M15        -> I3, nominally 2*I1

Ibias_accuracy grades I1 against a fixed nominal; Leg_matching grades the
4x mirror leg against its ideal ratio. Both in %, both signed.

ibias_nom defaults to 4.665e-8 A, which is the tt / 27C / 3.3V value from
the dc_params run of 2026-09-04 (RUN_2026-09-04_05-03-39). It is a measured
number, not a specification - re-read it from that run's
simulation_summary.csv and update the default whenever the device sizing
changes, otherwise Ibias_accuracy silently grades against a stale centre.} 400 -290 0 0 0.3 0.3 {}
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
op
let I1 = v.x1.xbias.vi1#branch
let I2 = v.x1.xbias.vi4#branch
let I3 = v.x1.xbias.viaux#branch
let ibias_nom = CACE\{ibias_nom=4.665e-8\}
let Ibias_accuracy = 100 * (I1 - ibias_nom) / ibias_nom
* PMOS mirror ratio M12:M13 = 1:4, so I2 should come out at 4*I1
let Leg_matching = 100 * (I2 / (4 * I1) - 1)
* to grade the 2x aux leg (M14) instead, use this line in its place:
* let Leg_matching = 100 * (I3 / (2 * I1) - 1)
echo $&Ibias_accuracy $&Leg_matching > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
C {devices/code_shown.sym} 20 -780 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
"}
C {reference.sym} 360 -300 0 0 {name=x1}
C {devices/vsource.sym} 180 -210 0 1 {name=VDD value=CACE\{vdd\}}
C {devices/gnd.sym} 180 -120 0 0 {name=l1 lab=0}
C {devices/vsource.sym} 260 -210 0 1 {name=Voff value=0}
C {devices/lab_wire.sym} 480 -320 0 0 {name=l2 lab=vbp}
C {devices/lab_wire.sym} 480 -300 0 0 {name=l3 lab=vbn}
C {devices/lab_wire.sym} 480 -280 0 0 {name=l4 lab=vbr}
C {devices/title.sym} 160 -40 0 0 {name=l5 author="Christoph Maier"}
