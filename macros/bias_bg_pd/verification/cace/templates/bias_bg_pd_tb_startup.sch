v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier} -560 -440 0 0 0.25 0.25 {}
T {SPDX-License-Identifier: Apache-2.0} -560 -410 0 0 0.25 0.25 {}
T {CACE template: bias_bg_pd, tran: start-up from 0 V} -560 -370 0 0 0.4 0.4 {}
T {DUT pins carry net labels only; every source and measurement is in the code block below.} -560 -320 0 0 0.25 0.25 {}
C {bias_bg_pd.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -80 -180 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -80 180 0 0 {name=p2 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 140 -100 2 0 {name=p5 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 140 -60 2 0 {name=p6 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 140 -20 2 0 {name=p7 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 140 20 2 0 {name=p8 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 140 60 2 0 {name=p9 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 140 100 2 0 {name=p10 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} -140 100 0 0 {name=p11 sig_type=std_logic lab=en_3v3}
C {devices/vsource.sym} -400 100 0 0 {name=Ven value="0" savecurrent=false}
C {devices/lab_pin.sym} -400 70 0 0 {name=pv1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -400 130 0 0 {name=pv2 sig_type=std_logic lab=en_3v3}
C {devices/code_shown.sym} -560 260 0 0 {name=NGSPICE only_toplevel=false value=".lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_typ
.lib cornerPNP.lib CACE\{corner_pnp\}
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options gmin=1e-12 abstol=1e-12 reltol=1e-4 method=gear
* every supply ramps from 0 V in tramp, all nodes start at 0 V (uic); en_3v3 follows vdd.
* The dc value is what op sees (the reference operating point), the pwl is what tran sees.
Vvdd vdd 0 dc CACE\{vdd\} pwl(0 0 CACE\{tramp\} CACE\{vdd\})
Vvss vss 0 0
Vvddo vdd vddo 0
Vvsso vsso 0 0
* class-AB diode stacks of the pad as fixtures: drawn in the DUT until 2026-10-27, in the pad since then (RP2 / RN2 in d2s_mpdda_pd, RP1 / RN1 in d2s_out_p / d2s_out_n since 2026-10-28);
* same devices on the same nets, so the circuit is the one characterized before
XRP1 dabp dabp vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
XRP2 vabp vabp dabp vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
XRN1 dabn dabn vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
XRN2 vabn vabn dabn vss sg13_hv_nmos w=4.4u l=1u ng=1
* Ven (drawn): en_3v3 = vdd
.control
save all @n.x1.xbn.nsg13_hv_nmos[ids] @n.xrp2.nsg13_hv_pmos[ids]
op
let t = abs(@n.x1.xbn.nsg13_hv_nmos[ids])
set dcbn = $&t
let t = abs(@n.xrp2.nsg13_hv_pmos[ids])
set dcabp = $&t
let ts = CACE\{tramp\} + 1m
let tstep = ts / 4000
set tss = $&ts
tran $&tstep $&ts uic
let ib = abs(@n.x1.xbn.nsg13_hv_nmos[ids])
let ia = abs(@n.xrp2.nsg13_hv_pmos[ids])
meas tran ibf find ib at=$tss
meas tran iaf find ia at=$tss
let ith = 0.9 * ibf
meas tran t90 when ib=$&ith cross=last
* results: t90 = last crossing of 90 % of the final bn current, counted from t = 0 (s);
* final currents 1 ms after the ramp relative to the dc operating point (fraction)
let t_su90 = t90
let Rbn_end = ibf / $dcbn
let Rabp_end = iaf / $dcabp
echo $&t_su90 $&Rbn_end $&Rabp_end > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
