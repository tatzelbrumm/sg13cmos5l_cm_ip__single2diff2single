v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template, DC: d2s_bias_sel_pd. Conditions: sel, en, vdd, iref, corner_mos, corner_r, corner_pnp, temp} 0 -60 0 0 0.4 0.4 {}
C {d2s_bias_sel_pd.sym} 400 0 0 0 {name=x1}
N 330 -90 330 -130 {lab=vdd}
C {devices/lab_pin.sym} 330 -130 0 1 {name=l1 sig_type=std_logic lab=vdd}
N 330 90 330 130 {lab=GND}
C {devices/lab_pin.sym} 330 130 0 1 {name=l2 sig_type=std_logic lab=GND}
N 350 -90 350 -130 {lab=vddo}
C {devices/lab_pin.sym} 350 -130 0 1 {name=l3 sig_type=std_logic lab=vddo}
N 350 90 350 130 {lab=vsso}
C {devices/lab_pin.sym} 350 130 0 1 {name=l4 sig_type=std_logic lab=vsso}
N 290 -50 250 -50 {lab=ibias}
C {devices/lab_pin.sym} 250 -50 0 0 {name=l5 sig_type=std_logic lab=ibias}
N 510 -50 550 -50 {lab=vbp}
C {devices/lab_pin.sym} 550 -50 0 1 {name=l6 sig_type=std_logic lab=vbp}
N 510 -30 550 -30 {lab=vbn}
C {devices/lab_pin.sym} 550 -30 0 1 {name=l7 sig_type=std_logic lab=vbn}
N 510 -10 550 -10 {lab=vbpc}
C {devices/lab_pin.sym} 550 -10 0 1 {name=l8 sig_type=std_logic lab=vbpc}
N 510 10 550 10 {lab=vbnc}
C {devices/lab_pin.sym} 550 10 0 1 {name=l9 sig_type=std_logic lab=vbnc}
N 510 30 550 30 {lab=vabp}
C {devices/lab_pin.sym} 550 30 0 1 {name=l10 sig_type=std_logic lab=vabp}
N 510 50 550 50 {lab=vabn}
C {devices/lab_pin.sym} 550 50 0 1 {name=l11 sig_type=std_logic lab=vabn}
N 290 -30 250 -30 {lab=en_3v3}
C {devices/lab_pin.sym} 250 -30 0 0 {name=l12 sig_type=std_logic lab=en_3v3}
N 290 -10 250 -10 {lab=sel0_3v3}
C {devices/lab_pin.sym} 250 -10 0 0 {name=l13 sig_type=std_logic lab=sel0_3v3}
N 290 10 250 10 {lab=sel1_3v3}
C {devices/lab_pin.sym} 250 10 0 0 {name=l14 sig_type=std_logic lab=sel1_3v3}
C {devices/code_shown.sym} 0 300 0 0 {name=MODEL only_toplevel=true format="tcleval( @value )" value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_typ
.lib cornerPNP.lib CACE\{corner_pnp\}
"}
C {devices/code_shown.sym} 0 420 0 0 {name=NGSPICE only_toplevel=false value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options gmin=1e-15 abstol=1e-15 reltol=1e-4
.option warn=1
.param vd=CACE\{vdd\}
Vdd vdd 0 \{vd\}
Vddo vddo 0 \{vd\}
Vsso vsso 0 0
* harness iDAC model: a PMOS mirror on its own 3.3 V supply sources CACE\{iref\} into ibias
Vext vext 0 3.3
Iext xg 0 CACE\{iref\}
XEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
* replica loads: each copies one bias diode (same device, gate on the bias line, drain forced to the gate
* voltage by an ideal buffer), so the current through Vm.. is that diode's current
XRbp dbp vbp vdd vdd sg13_hv_pmos w=5u l=6u ng=1
Ebp ebp 0 vbp 0 1
Vmbp ebp dbp 0
XRbn dbn vbn 0 0 sg13_hv_nmos w=6u l=6u ng=1
Ebn ebn 0 vbn 0 1
Vmbn dbn ebn 0
XRbnc dbnc vbnc 0 0 sg13_hv_nmos w=1u l=8u ng=1
Ebnc ebnc 0 vbnc 0 1
Vmbnc dbnc ebnc 0
XRbpc dbpc vbpc vdd vdd sg13_hv_pmos w=1u l=4u ng=1
Ebpc ebpc 0 vbpc 0 1
Vmbpc ebpc dbpc 0
XRp1 n1r n1r vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
XRp2 dabp vabp n1r vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
Eabp eabp 0 vabp 0 1
Vmabp eabp dabp 0
XRn1 n2r n2r vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
XRn2 dabn vabn n2r 0 sg13_hv_nmos w=4.4u l=1u ng=1
Eabn eabn 0 vabn 0 1
Vmabn dabn eabn 0
* sel: 0 harness ibias, 1 Oguey-Aebischer core, 2 bandgap core, 3 both cores; en: 1 enabled, 0 disabled
.param sl=CACE\{sel\} en=CACE\{en\}
.param s0='(sl==1 || sl==3) ? vd : 0'
.param s1='(sl==2 || sl==3) ? vd : 0'
Ven en_3v3 0 \{en*vd\}
Vs0 sel0_3v3 0 \{s0\}
Vs1 sel1_3v3 0 \{s1\}
.control
op
let Ibp = abs(i(Vmbp))
let Ibn = abs(i(Vmbn))
let Ibnc = abs(i(Vmbnc))
let Ibpc = abs(i(Vmbpc))
let Iabp = abs(i(Vmabp))
let Iabn = abs(i(Vmabn))
* supply currents of the DUT alone (replica loads excluded)
let I_vdd = -i(Vdd) - Ibp - Ibpc
let I_vddo = -i(Vddo) - Iabp
let I_vsso = i(Vsso) - Iabn
let I_ibias = -i(Vext) - CACE\{iref\}
echo $&Ibp $&Ibn $&Ibnc $&Ibpc $&Iabp $&Iabn $&I_vdd $&I_vddo $&I_vsso $&I_ibias > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
