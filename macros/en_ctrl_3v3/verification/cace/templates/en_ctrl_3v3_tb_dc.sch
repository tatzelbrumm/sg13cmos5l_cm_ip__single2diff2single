v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template, DC truth table: en_ctrl_3v3. Conditions: case, corner_mos, temp, sup, cload} 0 -60 0 0 0.4 0.4 {}
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
.options gmin=1e-15 abstol=1e-15 reltol=1e-4
.option warn=1
* sup: 0 = (vddl, vddh) = (1.08, 3.0) V, 1 = (1.32, 3.6) V, 0.5 = nominal (1.2, 3.3) V
.param s=CACE\{sup\}
.param vl=\{1.08+0.24*s\} vh=\{3.0+0.6*s\}
Vh vddh 0 \{vh\}
Cl0 en_3v3 0 CACE\{cload\}
Cl1 sel0_3v3 0 10f
Cl2 sel1_3v3 0 10f
* case: 0 all on, en = 1 | 1 en = 0 | 2 vdd_1v2 sense off | 3 vdd_3v3 sense off | 4 vdd_1v2 gated off (vddl = sense = 0, en input still high)
*       5 vdd_1v2 sense floating (1e12 ohm to 0.6 V) | 6 vdd_3v3 sense floating (1e12 ohm to 1.65 V) | 7 all on, sel bits swapped
.param c=CACE\{case\}
.param vlv='(c==4) ? 0 : vl'
.param ven='(c==1) ? 0 : vl'
.param v12='(c==2 || c==4) ? 0 : ((c==5) ? 0.6 : vl)'
.param r12='(c==5) ? 1e12 : 1'
.param v33='(c==3) ? 0 : ((c==6) ? 1.65 : vh)'
.param r33='(c==6) ? 1e12 : 1'
.param vs0='(c==7) ? 0 : vl'
.param vs1='(c==7) ? vl : 0'
* expected outputs (in units of vddh); sel is undefined (and not checked) with vddl = 0
.param xen='(c==0 || c==7) ? 1 : 0'
.param xs0='(c==7) ? 0 : 1'
.param xs1='(c==7) ? 1 : 0'
.param chk='(c==4) ? 0 : 1'
Vl vddl 0 \{vlv\}
Ven en_1v2 0 \{ven\}
Vs0 sel0_1v2 0 \{vs0\}
Vs1 sel1_1v2 0 \{vs1\}
V12 s12 0 \{v12\}
R12 s12 vdd1v2_sense \{r12\}
V33 s33 0 \{v33\}
R33 s33 vdd3v3_sense \{r33\}
Vx1 xen 0 \{xen\}
Vx2 xs0 0 \{xs0\}
Vx3 xs1 0 \{xs1\}
Vx4 chk 0 \{chk\}
Vx5 vhn 0 \{vh\}
.control
op
let Verr_en = abs(v(en_3v3) - v(xen) * v(vhn))
let e0 = abs(v(sel0_3v3) - v(xs0) * v(vhn))
let e1 = abs(v(sel1_3v3) - v(xs1) * v(vhn))
let Verr_sel = v(chk) * (e0 + e1)
let I_vddh = -i(Vh)
let I_vddl = -i(Vl)
let I_s12 = -i(V12)
let I_s33 = -i(V33)
let I_en = -i(Ven)
echo $&Verr_en $&Verr_sel $&I_vddh $&I_vddl $&I_s12 $&I_s33 $&I_en > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
