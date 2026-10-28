v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier} -560 -440 0 0 0.25 0.25 {}
T {SPDX-License-Identifier: Apache-2.0} -560 -410 0 0 0.25 0.25 {}
T {CACE template: bias_out_pd, dc: bias currents, supply currents, line sensitivity} -560 -370 0 0 0.4 0.4 {}
T {DUT pins carry net labels only; every source and measurement is in the code block below.} -560 -320 0 0 0.25 0.25 {}
C {bias_out_pd.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -80 -180 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -80 180 0 0 {name=p2 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -140 0 0 0 {name=p5 sig_type=std_logic lab=iref}
C {devices/lab_pin.sym} 140 -100 2 0 {name=p6 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 140 -60 2 0 {name=p7 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 140 -20 2 0 {name=p8 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 140 20 2 0 {name=p9 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 140 60 2 0 {name=p10 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 140 100 2 0 {name=p11 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} -140 100 0 0 {name=p12 sig_type=std_logic lab=en_3v3}
C {devices/vsource.sym} -400 100 0 0 {name=Ven value="0" savecurrent=false}
C {devices/lab_pin.sym} -400 70 0 0 {name=pv1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -400 130 0 0 {name=pv2 sig_type=std_logic lab=en_3v3}
C {devices/code_shown.sym} -560 260 0 0 {name=NGSPICE only_toplevel=false value=".lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_typ
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.option SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.options gmin=1e-15 abstol=1e-15 reltol=1e-6
* vdd = vddo = en_3v3 (vddo and en_3v3 follow vdd through 0 V sources)
Vvdd vdd 0 dc CACE\{vdd\}
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
* external reference: NMOS mirror sinks CACE\{iref\} out of iref; its input current comes from vext
Vext vext 0 dc CACE\{vext\}
Iext vext xg CACE\{iref\}
XEd xg xg 0 0 sg13_hv_nmos w=6u l=6u ng=1
XEm irs xg 0 0 sg13_hv_nmos w=6u l=6u ng=1
* sense: i(vsi) = current out of iref
Vsi iref irs 0
.control
let v0 = CACE\{vdd\}
let vx = v0 + 0
alter vvdd dc = $&vx
op
let t = abs(@n.x1.xbp.nsg13_hv_pmos[ids])
set mbp = $&t
let t = abs(@n.x1.xbn.nsg13_hv_nmos[ids])
set mbn = $&t
let t = abs(@n.x1.xbnc.nsg13_hv_nmos[ids])
set mbnc = $&t
let t = abs(@n.x1.xbpc.nsg13_hv_pmos[ids])
set mbpc = $&t
let t = abs(@n.xrp2.nsg13_hv_pmos[ids])
set mabp = $&t
let t = abs(@n.xrn2.nsg13_hv_nmos[ids])
set mabn = $&t
let t = i(vvdd)
set midd = $&t
let t = i(vvddo)
set middo = $&t
let t = i(vsi)
set mext = $&t
let vx = v0 + 0.1
alter vvdd dc = $&vx
op
let t = abs(@n.x1.xbp.nsg13_hv_pmos[ids])
set hbp = $&t
let t = abs(@n.x1.xbn.nsg13_hv_nmos[ids])
set hbn = $&t
let t = abs(@n.x1.xbnc.nsg13_hv_nmos[ids])
set hbnc = $&t
let t = abs(@n.x1.xbpc.nsg13_hv_pmos[ids])
set hbpc = $&t
let t = abs(@n.xrp2.nsg13_hv_pmos[ids])
set habp = $&t
let t = abs(@n.xrn2.nsg13_hv_nmos[ids])
set habn = $&t
let vx = v0 + -0.1
alter vvdd dc = $&vx
op
let t = abs(@n.x1.xbp.nsg13_hv_pmos[ids])
set lbp = $&t
let t = abs(@n.x1.xbn.nsg13_hv_nmos[ids])
set lbn = $&t
let t = abs(@n.x1.xbnc.nsg13_hv_nmos[ids])
set lbnc = $&t
let t = abs(@n.x1.xbpc.nsg13_hv_pmos[ids])
set lbpc = $&t
let t = abs(@n.xrp2.nsg13_hv_pmos[ids])
set labp = $&t
let t = abs(@n.xrn2.nsg13_hv_nmos[ids])
set labn = $&t
* results in SI units (A, fraction per V); positive = delivered by the source
let Ibp = $mbp
let Sbp = ($hbp - $lbp) / (0.2 * $mbp)
let Ibn = $mbn
let Sbn = ($hbn - $lbn) / (0.2 * $mbn)
let Ibnc = $mbnc
let Sbnc = ($hbnc - $lbnc) / (0.2 * $mbnc)
let Ibpc = $mbpc
let Sbpc = ($hbpc - $lbpc) / (0.2 * $mbpc)
let Iabp = $mabp
let Sabp = ($habp - $labp) / (0.2 * $mabp)
let Iabn = $mabn
let Sabn = ($habn - $labn) / (0.2 * $mabn)
let Iddo = $middo
let Idd = -$midd - Iddo
let Iref = $mext
echo $&Ibp $&Ibn $&Ibnc $&Ibpc $&Iabp $&Iabn $&Idd $&Iddo $&Iref $&Sbp $&Sbn $&Sbnc $&Sbpc $&Sabp $&Sabn > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
