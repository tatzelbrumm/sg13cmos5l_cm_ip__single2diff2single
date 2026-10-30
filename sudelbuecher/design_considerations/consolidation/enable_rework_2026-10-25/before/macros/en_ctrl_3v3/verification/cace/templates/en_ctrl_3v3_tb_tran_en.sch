v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template, enable / disable delay: en_ctrl_3v3. Conditions: corner_mos, temp, sup, cload} 0 -60 0 0 0.4 0.4 {}
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
* enable (rise at 20 ns) and disable (fall at 520 ns) of en_1v2, 100 ps edges; both senses on
Vl vddl 0 \{vl\}
Ven en_1v2 0 PULSE(0 \{vl\} 20n 100p 100p 500n 2u)
Vs0 sel0_1v2 0 0
Vs1 sel1_1v2 0 0
V12 vdd1v2_sense 0 \{vl\}
V33 vdd3v3_sense 0 \{vh\}
.control
tran 50p 1u
let vmh = CACE\{sup\} * 0.6 + 3.0
let vmh2 = vmh / 2
let vml2 = (CACE\{sup\} * 0.24 + 1.08) / 2
meas tran td_on trig v(en_1v2) val=$&vml2 rise=1 targ v(en_3v3) val=$&vmh2 rise=1
meas tran td_off trig v(en_1v2) val=$&vml2 fall=1 targ v(en_3v3) val=$&vmh2 fall=1
echo $&td_on $&td_off > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
