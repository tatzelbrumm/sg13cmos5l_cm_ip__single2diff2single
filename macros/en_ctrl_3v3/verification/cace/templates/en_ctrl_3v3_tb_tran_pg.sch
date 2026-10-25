v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template, supply-loss response: en_ctrl_3v3. Conditions: scenario, corner_mos, temp, sup, cload} 0 -60 0 0 0.4 0.4 {}
C {en_ctrl_3v3.sym} 400 0 0 0 {name=x1}
N 340 -80 340 -120 {lab=vddh}
C {devices/lab_pin.sym} 340 -120 0 1 {name=l1 sig_type=std_logic lab=vddh}
N 360 -80 360 -120 {lab=vddl}
C {devices/lab_pin.sym} 360 -120 0 1 {name=l2 sig_type=std_logic lab=vddl}
N 340 80 340 120 {lab=GND}
C {devices/lab_pin.sym} 340 120 0 1 {name=l3 sig_type=std_logic lab=GND}
N 300 -40 260 -40 {lab=en_1v2}
C {devices/lab_pin.sym} 260 -40 0 0 {name=l4 sig_type=std_logic lab=en_1v2}
N 300 -20 260 -20 {lab=sel0_1v2}
C {devices/lab_pin.sym} 260 -20 0 0 {name=l5 sig_type=std_logic lab=sel0_1v2}
N 300 0 260 0 {lab=sel1_1v2}
C {devices/lab_pin.sym} 260 0 0 0 {name=l6 sig_type=std_logic lab=sel1_1v2}
N 300 20 260 20 {lab=vdd1v2_sense}
C {devices/lab_pin.sym} 260 20 0 0 {name=l7 sig_type=std_logic lab=vdd1v2_sense}
N 300 40 260 40 {lab=vdd3v3_sense}
C {devices/lab_pin.sym} 260 40 0 0 {name=l8 sig_type=std_logic lab=vdd3v3_sense}
N 500 -40 540 -40 {lab=en_3v3}
C {devices/lab_pin.sym} 540 -40 0 1 {name=l9 sig_type=std_logic lab=en_3v3}
N 500 -20 540 -20 {lab=sel0_3v3}
C {devices/lab_pin.sym} 540 -20 0 1 {name=l10 sig_type=std_logic lab=sel0_3v3}
N 500 0 540 0 {lab=sel1_3v3}
C {devices/lab_pin.sym} 540 0 0 1 {name=l11 sig_type=std_logic lab=sel1_3v3}
N 500 20 540 20 {lab=en_3v3_b}
C {devices/lab_pin.sym} 540 20 0 1 {name=l12 sig_type=std_logic lab=en_3v3_b}
C {devices/code_shown.sym} 0 300 0 0 {name=MODEL only_toplevel=true format="tcleval( @value )" value="
.lib cornerMOSlv.lib mos_CACE\{corner_mos\}
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
"}
C {devices/code_shown.sym} 0 420 0 0 {name=NGSPICE only_toplevel=false value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options gmin=1e-12 abstol=1e-12 reltol=1e-4
.option warn=1
* sup: 0 = (vddl, vddh) = (1.08, 3.0) V, 1 = (1.32, 3.6) V, 0.5 = nominal (1.2, 3.3) V
.param s=CACE\{sup\}
.param vl=\{1.08+0.24*s\} vh=\{3.0+0.6*s\}
Vh vddh 0 \{vh\}
Cl0 en_3v3 0 CACE\{cload\}
Cl1 sel0_3v3 0 10f
Cl2 sel1_3v3 0 10f
* supply loss with en_1v2 held high: scenario 1 vdd_1v2 sense, 2 vdd_3v3 sense, 3 vdd_1v2 = vddl and sense together (slot fallback)
*   ramps to 0 V between 1 us and 2 us
.param c=CACE\{scenario\}
.param a12='(c==1 || c==3) ? 0 : 1'
.param a33='(c==2) ? 0 : 1'
.param al='(c==3) ? 0 : 1'
Vl vddl 0 PWL(0 \{vl\} 1u \{vl\} 2u \{al*vl\})
Ven en_1v2 0 \{vl\}
Vs0 sel0_1v2 0 0
Vs1 sel1_1v2 0 0
V12 vdd1v2_sense 0 PWL(0 \{vl\} 1u \{vl\} 2u \{a12*vl\})
V33 vdd3v3_sense 0 PWL(0 \{vh\} 1u \{vh\} 2u \{a33*vh\})
.control
tran 1n 10u
let vmh2 = (CACE\{sup\} * 0.6 + 3.0) / 2
meas tran t50 when v(en_3v3)=$&vmh2 fall=1
let t_pg = t50 - 1e-6
meas tran Ven_end find v(en_3v3) at=9.9u
echo $&t_pg $&Ven_end > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
