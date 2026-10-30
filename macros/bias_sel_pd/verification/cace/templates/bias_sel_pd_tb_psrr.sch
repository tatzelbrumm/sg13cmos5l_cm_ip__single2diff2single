v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template, supply rejection: bias_sel_pd. Conditions: sel, vdd, iref, corner_mos, corner_r, corner_pnp, temp, cores} 0 -40 0 0 0.4 0.4 {}
N 200 0 200 40 {lab=vdd}
N 180 220 180 260 {lab=VSS}
N 100 80 140 80 {lab=ibias}
N 320 80 360 80 {lab=vbp}
N 320 180 360 180 {lab=vbn}
N 320 100 360 100 {lab=vbpc}
N 320 160 360 160 {lab=vbnc}
N 320 120 360 120 {lab=vabp}
N 320 140 360 140 {lab=vabn}
N 100 120 140 120 {lab=en_3v3}
N 100 160 140 160 {lab=sel0_3v3}
N 100 180 140 180 {lab=sel1_3v3}
N 100 140 140 140 {lab=en_3v3_b}
C {bias_sel_pd.sym} 230 130 0 0 {name=x1}
C {devices/lab_pin.sym} 200 0 0 0 {name=l1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 180 260 0 0 {name=l2 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 100 80 0 0 {name=l5 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 360 80 0 1 {name=l6 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 360 180 0 1 {name=l7 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 360 100 0 1 {name=l8 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 360 160 0 1 {name=l9 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 360 120 0 1 {name=l10 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 360 140 0 1 {name=l11 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} 100 120 0 0 {name=l12 sig_type=std_logic lab=en_3v3}
C {devices/lab_pin.sym} 100 160 0 0 {name=l13 sig_type=std_logic lab=sel0_3v3}
C {devices/lab_pin.sym} 100 180 0 0 {name=l14 sig_type=std_logic lab=sel1_3v3}
C {devices/lab_pin.sym} 100 140 0 0 {name=l15 sig_type=std_logic lab=en_3v3_b}
C {devices/code_shown.sym} 0 300 0 0 {name=MODEL only_toplevel=true format="tcleval( @value )" value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_typ
.lib cornerPNP.lib CACE\{corner_pnp\}
"}
C {devices/code_shown.sym} 0 420 0 0 {name=NGSPICE only_toplevel=false value="
* supply rejection of the six bias currents (added 2026-10-30, cloud session C1; measurement of bias_oa_pd_tb_psrr.sch):
* largest |dI / I| of the six per volt of ripple on vdd, vss, vddo, vsso in turn, at 1 k / 100 k / 1 MHz.
* The DUT's vss is the node VSS here (GND in the DC template) so that it can carry ripple; en_3v3, the select bits
* and the harness supply vext have none. Core view as in bias_sel_pd_tb_dc.sch.
.include CACE\{templates\}/cores/CACE\{cores=schematic\}.spice
.include CACE\{DUT_path\}
.temp CACE\{temp\}
* reltol 1e-4 as in the DC template: with bias_oa_pd's 1e-6 the op of sel 0, ss, -40 C fell back to a transient op
.options gmin=1e-15 abstol=1e-15 reltol=1e-4
.option warn=1
.param vd=CACE\{vdd\}
Vdd vdd 0 dc \{vd\} ac 0
Vss VSS 0 dc 0 ac 0
Vddo vddo 0 dc \{vd\} ac 0
Vsso vsso 0 dc 0 ac 0
* class-AB diode stacks of the pad as fixtures (as in bias_sel_pd_tb_dc.sch)
XRP1 dabp dabp vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
XRP2 vabp vabp dabp vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
XRN1 dabn dabn vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
XRN2 vabn vabn dabn VSS sg13_hv_nmos w=4.4u l=1u ng=1
* harness iDAC model (as in bias_sel_pd_tb_dc.sch), on its own supply without ripple
Vext vext 0 3.3
Iext xg 0 CACE\{iref\}
XEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
* replica loads (as in bias_sel_pd_tb_dc.sch): each copies one bias diode, drain forced to the gate voltage
XRbp dbp vbp vdd vdd sg13_hv_pmos w=5u l=6u ng=1
Ebp ebp 0 vbp 0 1
Vmbp ebp dbp 0
XRbn dbn vbn VSS VSS sg13_hv_nmos w=6u l=6u ng=1
Ebn ebn 0 vbn 0 1
Vmbn dbn ebn 0
XRbnc dbnc vbnc VSS VSS sg13_hv_nmos w=1u l=8u ng=1
Ebnc ebnc 0 vbnc 0 1
Vmbnc dbnc ebnc 0
XRbpc dbpc vbpc vdd vdd sg13_hv_pmos w=1u l=4u ng=1
Ebpc ebpc 0 vbpc 0 1
Vmbpc ebpc dbpc 0
XRabp1 n1r n1r vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
XRabp2 mdabp vabp n1r vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
Eabp eabp 0 vabp 0 1
Vmabp eabp mdabp 0
XRabn1 n2r n2r vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
XRabn2 mdabn vabn n2r VSS sg13_hv_nmos w=4.4u l=1u ng=1
Eabn eabn 0 vabn 0 1
Vmabn mdabn eabn 0
* sel: 0 harness ibias, 1 Oguey-Aebischer core, 2 bandgap core, 3 both cores
.param sl=CACE\{sel\}
.param s0='(sl==1 || sl==3) ? vd : 0'
.param s1='(sl==2 || sl==3) ? vd : 0'
Ven en_3v3 0 \{vd\}
XIBP en_3v3_b en_3v3 vdd vdd sg13_hv_pmos w=1u l=0.45u ng=1
XIBN en_3v3_b en_3v3 VSS VSS sg13_hv_nmos w=1u l=0.45u ng=1
Vs0 sel0_3v3 0 \{s0\}
Vs1 sel1_3v3 0 \{s1\}
.control
op
let t = abs(i(Vmbp))
set dcbp = $&t
let t = abs(i(Vmbn))
set dcbn = $&t
let t = abs(i(Vmbnc))
set dcbnc = $&t
let t = abs(i(Vmbpc))
set dcbpc = $&t
let t = abs(i(Vmabp))
set dcabp = $&t
let t = abs(i(Vmabn))
set dcabn = $&t
alter @Vdd[acmag] = 1
ac dec 10 100 1e7
let mbp = mag(i(Vmbp)) / $dcbp
let mbn = mag(i(Vmbn)) / $dcbn
let mbnc = mag(i(Vmbnc)) / $dcbnc
let mbpc = mag(i(Vmbpc)) / $dcbpc
let mabp = mag(i(Vmabp)) / $dcabp
let mabn = mag(i(Vmabn)) / $dcabn
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
alter @Vdd[acmag] = 0
alter @Vss[acmag] = 1
ac dec 10 100 1e7
let mbp = mag(i(Vmbp)) / $dcbp
let mbn = mag(i(Vmbn)) / $dcbn
let mbnc = mag(i(Vmbnc)) / $dcbnc
let mbpc = mag(i(Vmbpc)) / $dcbpc
let mabp = mag(i(Vmabp)) / $dcabp
let mabn = mag(i(Vmabn)) / $dcabn
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
alter @Vss[acmag] = 0
alter @Vddo[acmag] = 1
ac dec 10 100 1e7
let mbp = mag(i(Vmbp)) / $dcbp
let mbn = mag(i(Vmbn)) / $dcbn
let mbnc = mag(i(Vmbnc)) / $dcbnc
let mbpc = mag(i(Vmbpc)) / $dcbpc
let mabp = mag(i(Vmabp)) / $dcabp
let mabn = mag(i(Vmabn)) / $dcabn
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
alter @Vddo[acmag] = 0
alter @Vsso[acmag] = 1
ac dec 10 100 1e7
let mbp = mag(i(Vmbp)) / $dcbp
let mbn = mag(i(Vmbn)) / $dcbn
let mbnc = mag(i(Vmbnc)) / $dcbnc
let mbpc = mag(i(Vmbpc)) / $dcbpc
let mabp = mag(i(Vmabp)) / $dcabp
let mabn = mag(i(Vmabn)) / $dcabn
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
* echo with many $var in a row drops every other one: through vectors, as bias_oa_pd_tb_psrr.sch does
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
