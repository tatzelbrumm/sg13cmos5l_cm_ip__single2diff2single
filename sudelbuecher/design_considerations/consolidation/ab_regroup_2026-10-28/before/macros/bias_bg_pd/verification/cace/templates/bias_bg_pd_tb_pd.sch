v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier} -560 -440 0 0 0.25 0.25 {}
T {SPDX-License-Identifier: Apache-2.0} -560 -410 0 0 0.25 0.25 {}
T {CACE template: bias_bg_pd, op + tran: disabled supply currents, enable time} -560 -370 0 0 0.4 0.4 {}
T {DUT pins carry net labels only; every source and measurement is in the code block below.} -560 -320 0 0 0.25 0.25 {}
C {bias_bg_pd.sym} 0 0 0 0 {name=x1}
C {devices/lab_pin.sym} -80 -180 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -80 180 0 0 {name=p2 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 80 -180 2 0 {name=p3 sig_type=std_logic lab=vddo}
C {devices/lab_pin.sym} 80 180 2 0 {name=p4 sig_type=std_logic lab=vsso}
C {devices/lab_pin.sym} 140 -100 2 0 {name=p5 sig_type=std_logic lab=vbp}
C {devices/lab_pin.sym} 140 -60 2 0 {name=p6 sig_type=std_logic lab=vbn}
C {devices/lab_pin.sym} 140 -20 2 0 {name=p7 sig_type=std_logic lab=vbpc}
C {devices/lab_pin.sym} 140 20 2 0 {name=p8 sig_type=std_logic lab=vbnc}
C {devices/lab_pin.sym} 140 60 2 0 {name=p9 sig_type=std_logic lab=vabp}
C {devices/lab_pin.sym} 140 100 2 0 {name=p10 sig_type=std_logic lab=vabn}
C {devices/lab_pin.sym} -140 100 0 0 {name=p11 sig_type=std_logic lab=en_3v3}
C {devices/vsource.sym} -400 100 0 0 {name=Ven value="pulse(0 CACE\{vdd\} 10u 10n 10n 1 2)" savecurrent=false}
C {devices/lab_pin.sym} -400 70 0 0 {name=pv1 sig_type=std_logic lab=en_3v3}
C {devices/gnd.sym} -400 130 0 0 {name=l0 lab=GND}
C {devices/code_shown.sym} -560 260 0 0 {name=NGSPICE only_toplevel=false value=".lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_typ
.lib cornerPNP.lib CACE\{corner_pnp\}
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options gmin=1e-15 abstol=1e-15 reltol=1e-4 method=gear
Vvdd vdd 0 dc CACE\{vdd\}
Vvss vss 0 0
Vvddo vddo 0 dc CACE\{vdd\}
Vvsso vsso 0 0
* en_3v3 low (operating point = disabled state), rises at 10 us in 10 ns
* Ven (drawn)
.control
save all @n.x1.xbn.nsg13_hv_nmos[ids] @n.x1.xrp2.nsg13_hv_pmos[ids]
op
let Idd_off = -i(vvdd)
let Iddo_off = -i(vvddo)
let Ib_off = abs(@n.x1.xbp.nsg13_hv_pmos[ids])
let t = abs(@n.x1.xbn.nsg13_hv_nmos[ids])
let Ib_off = (Ib_off + t + abs(Ib_off - t)) / 2
let t = abs(@n.x1.xbnc.nsg13_hv_nmos[ids])
let Ib_off = (Ib_off + t + abs(Ib_off - t)) / 2
let t = abs(@n.x1.xbpc.nsg13_hv_pmos[ids])
let Ib_off = (Ib_off + t + abs(Ib_off - t)) / 2
let t = abs(@n.x1.xrp2.nsg13_hv_pmos[ids])
let Ib_off = (Ib_off + t + abs(Ib_off - t)) / 2
let t = abs(@n.x1.xrn2.nsg13_hv_nmos[ids])
let Ib_off = (Ib_off + t + abs(Ib_off - t)) / 2
set Idd_off = $&Idd_off
set Iddo_off = $&Iddo_off
set Ib_off = $&Ib_off
* the transient with relaxed tolerances (1e-15 slows the floating disabled nodes ~27x)
option abstol=1e-12 gmin=1e-12
let ts = 10u + CACE\{ten\}
let tstep = ts / 4000
set tss = $&ts
tran $&tstep $&ts
let ib = abs(@n.x1.xbn.nsg13_hv_nmos[ids])
let ia = abs(@n.x1.xrp2.nsg13_hv_pmos[ids])
meas tran ibf find ib at=$tss
meas tran iaf find ia at=$tss
let ith = 0.9 * ibf
let ith2 = 0.9 * iaf
* two-sided settling: last time the current is outside +-10 % of its settled value
let eb = abs(ib - ibf) - 0.1 * ibf
let ea = abs(ia - iaf) - 0.1 * iaf
meas tran tb when eb=0 cross=last
meas tran ta when ea=0 cross=last
* results: disabled supply currents per rail, largest bias current while disabled (A);
* time from the en_3v3 edge until the bn / abp current stays within +-10 % of its settled value (s)
let t_en90_bn = tb - 10u
let t_en90_abp = ta - 10u
let Idd_off = $Idd_off
let Iddo_off = $Iddo_off
let Ib_off = $Ib_off
echo $&Idd_off $&Iddo_off $&Ib_off $&t_en90_bn $&t_en90_abp > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
