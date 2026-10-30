v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier} -560 -440 0 0 0.25 0.25 {}
T {SPDX-License-Identifier: Apache-2.0} -560 -410 0 0 0.25 0.25 {}
T {CACE template: bias_in_pd, ac: supply rejection of the bias currents per rail} -560 -370 0 0 0.4 0.4 {}
T {DUT pins carry net labels only; every source and measurement is in the code block below.} -560 -320 0 0 0.25 0.25 {}
C {bias_in_pd.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -40 -100 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -60 100 0 0 {name=p2 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -100 -40 0 0 {name=p5 sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 100 -60 2 0 {name=p6 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 100 60 2 0 {name=p7 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 100 -40 2 0 {name=p8 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 100 40 2 0 {name=p9 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 100 -20 2 0 {name=p10 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 100 20 2 0 {name=p11 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} -100 40 0 0 {name=p12 sig_type=std_logic lab=en_3v3}
C {devices/vsource.sym} -400 100 0 0 {name=Ven value="dc CACE\{vdd\}" savecurrent=false}
C {devices/lab_pin.sym} -400 70 0 0 {name=pv1 sig_type=std_logic lab=en_3v3}
C {devices/gnd.sym} -400 130 0 0 {name=l0 lab=GND}
C {devices/code_shown.sym} -560 260 0 0 {name=NGSPICE only_toplevel=false value=".lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_typ
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options gmin=1e-15 abstol=1e-15 reltol=1e-6
Vvdd vdd 0 dc CACE\{vdd\} ac 0
Vvss vss 0 dc 0 ac 0
Vvddo vddo 0 dc CACE\{vdd\} ac 0
Vvsso vsso 0 dc 0 ac 0
* class-AB diode stacks of the pad as fixtures: drawn in the DUT until 2026-10-27, in d2s_mpdda_pd since then;
* same devices on the same nets, so the circuit is the one characterized before
XRP1 dabp dabp vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
XRP2 vabp vabp dabp vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
XRN1 dabn dabn vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
XRN2 vabn vabn dabn vss sg13_hv_nmos w=4.4u l=1u ng=1
* Ven (drawn): en_3v3 is a dc source of its own (no ripple)
* ideal 5 uA reference into iref, as in run_bias.py: the PSRR of the cell alone
Iref 0 iref CACE\{iref\}
* replicas of the six diodes, gate on the bias line, drain held at the line voltage (E) through a 0 V sense
* source: their small-signal current equals the diode's (same VGS, VDS, rails), as run_bias.py measures it
Ebp dbp 0 vbp 0 1
Vsbp dbp sbp 0
XRbp sbp vbp vdd vdd sg13_hv_pmos w=5u l=6u ng=1
Ebn dbn 0 vbn 0 1
Vsbn dbn sbn 0
XRbn sbn vbn vss vss sg13_hv_nmos w=6u l=6u ng=1
Ebnc dbnc 0 vbnc 0 1
Vsbnc dbnc sbnc 0
XRbnc sbnc vbnc vss vss sg13_hv_nmos w=1u l=8u ng=1
Ebpc dbpc 0 vbpc 0 1
Vsbpc dbpc sbpc 0
XRbpc sbpc vbpc vdd vdd sg13_hv_pmos w=1u l=4u ng=1
XRp1 r1 r1 vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
Eabp mdabp 0 vabp 0 1
Vsabp mdabp sabp 0
XRabp sabp vabp r1 vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
XRn1 r2 r2 vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
Eabn mdabn 0 vabn 0 1
Vsabn mdabn sabn 0
XRabn sabn vabn r2 vss sg13_hv_nmos w=4.4u l=1u ng=1
.control
op
let t = abs(i(vsbp))
set dcbp = $&t
let t = abs(i(vsbn))
set dcbn = $&t
let t = abs(i(vsbnc))
set dcbnc = $&t
let t = abs(i(vsbpc))
set dcbpc = $&t
let t = abs(i(vsabp))
set dcabp = $&t
let t = abs(i(vsabn))
set dcabn = $&t
alter @vvdd[acmag] = 1
ac dec 10 100 1e7
let mbp = mag(i(vsbp)) / $dcbp
let mbn = mag(i(vsbn)) / $dcbn
let mbnc = mag(i(vsbnc)) / $dcbnc
let mbpc = mag(i(vsbpc)) / $dcbpc
let mabp = mag(i(vsabp)) / $dcabp
let mabn = mag(i(vsabn)) / $dcabn
* elementwise maximum over the six currents
let mx = mbp
let mx = (mx + mbn + abs(mx - mbn)) / 2
let mx = (mx + mbnc + abs(mx - mbnc)) / 2
let mx = (mx + mbpc + abs(mx - mbpc)) / 2
let mx = (mx + mabp + abs(mx - mabp)) / 2
let mx = (mx + mabn + abs(mx - mabn)) / 2
meas ac p1k find mx at=1000.0
set Pvdd1k = $&p1k
meas ac p100k find mx at=100000.0
set Pvdd100k = $&p100k
meas ac p1M find mx at=1000000.0
set Pvdd1M = $&p1M
alter @vvdd[acmag] = 0
alter @vvss[acmag] = 1
ac dec 10 100 1e7
let mbp = mag(i(vsbp)) / $dcbp
let mbn = mag(i(vsbn)) / $dcbn
let mbnc = mag(i(vsbnc)) / $dcbnc
let mbpc = mag(i(vsbpc)) / $dcbpc
let mabp = mag(i(vsabp)) / $dcabp
let mabn = mag(i(vsabn)) / $dcabn
* elementwise maximum over the six currents
let mx = mbp
let mx = (mx + mbn + abs(mx - mbn)) / 2
let mx = (mx + mbnc + abs(mx - mbnc)) / 2
let mx = (mx + mbpc + abs(mx - mbpc)) / 2
let mx = (mx + mabp + abs(mx - mabp)) / 2
let mx = (mx + mabn + abs(mx - mabn)) / 2
meas ac p1k find mx at=1000.0
set Pvss1k = $&p1k
meas ac p100k find mx at=100000.0
set Pvss100k = $&p100k
meas ac p1M find mx at=1000000.0
set Pvss1M = $&p1M
alter @vvss[acmag] = 0
alter @vvddo[acmag] = 1
ac dec 10 100 1e7
let mbp = mag(i(vsbp)) / $dcbp
let mbn = mag(i(vsbn)) / $dcbn
let mbnc = mag(i(vsbnc)) / $dcbnc
let mbpc = mag(i(vsbpc)) / $dcbpc
let mabp = mag(i(vsabp)) / $dcabp
let mabn = mag(i(vsabn)) / $dcabn
* elementwise maximum over the six currents
let mx = mbp
let mx = (mx + mbn + abs(mx - mbn)) / 2
let mx = (mx + mbnc + abs(mx - mbnc)) / 2
let mx = (mx + mbpc + abs(mx - mbpc)) / 2
let mx = (mx + mabp + abs(mx - mabp)) / 2
let mx = (mx + mabn + abs(mx - mabn)) / 2
meas ac p1k find mx at=1000.0
set Pvddo1k = $&p1k
meas ac p100k find mx at=100000.0
set Pvddo100k = $&p100k
meas ac p1M find mx at=1000000.0
set Pvddo1M = $&p1M
alter @vvddo[acmag] = 0
alter @vvsso[acmag] = 1
ac dec 10 100 1e7
let mbp = mag(i(vsbp)) / $dcbp
let mbn = mag(i(vsbn)) / $dcbn
let mbnc = mag(i(vsbnc)) / $dcbnc
let mbpc = mag(i(vsbpc)) / $dcbpc
let mabp = mag(i(vsabp)) / $dcabp
let mabn = mag(i(vsabn)) / $dcabn
* elementwise maximum over the six currents
let mx = mbp
let mx = (mx + mbn + abs(mx - mbn)) / 2
let mx = (mx + mbnc + abs(mx - mbnc)) / 2
let mx = (mx + mbpc + abs(mx - mbpc)) / 2
let mx = (mx + mabp + abs(mx - mabp)) / 2
let mx = (mx + mabn + abs(mx - mabn)) / 2
meas ac p1k find mx at=1000.0
set Pvsso1k = $&p1k
meas ac p100k find mx at=100000.0
set Pvsso100k = $&p100k
meas ac p1M find mx at=1000000.0
set Pvsso1M = $&p1M
alter @vvsso[acmag] = 0
* results: max over the six currents of |dI / I| per volt of ripple on the rail (fraction / V)
let P_vdd_1k = $Pvdd1k
let P_vdd_100k = $Pvdd100k
let P_vdd_1M = $Pvdd1M
let P_vss_1k = $Pvss1k
let P_vss_100k = $Pvss100k
let P_vss_1M = $Pvss1M
let P_vddo_1k = $Pvddo1k
let P_vddo_100k = $Pvddo100k
let P_vddo_1M = $Pvddo1M
let P_vsso_1k = $Pvsso1k
let P_vsso_100k = $Pvsso100k
let P_vsso_1M = $Pvsso1M
echo $&P_vdd_1k $&P_vdd_100k $&P_vdd_1M $&P_vss_1k $&P_vss_100k $&P_vss_1M $&P_vddo_1k $&P_vddo_100k $&P_vddo_1M $&P_vsso_1k $&P_vsso_100k $&P_vsso_1M > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
