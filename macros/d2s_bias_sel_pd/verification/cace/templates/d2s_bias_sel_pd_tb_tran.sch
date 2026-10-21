v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template, settling after enable / sel change: d2s_bias_sel_pd. Conditions: step, corner_mos, temp, vdd, iref} 0 -60 0 0 0.4 0.4 {}
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
.options gmin=1e-12 abstol=1e-12 reltol=1e-4
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
* step 0 / 1 / 2: en_3v3 rises at 1 us with sel = 0 / 1 / 2;  step 3 / 4 / 5: en high, sel changes 0 -> 1 / 1 -> 2 / 2 -> 0 at 100 us
.param st=CACE\{step\}
.param ten=1u
.param tsc=100u
* initial (i0, i1) and final (f0, f1) select bits per step
.param i0='(st==1 || st==4) ? 1 : 0'
.param i1='(st==2 || st==5) ? 1 : 0'
.param f0='(st==1 || st==3) ? 1 : 0'
.param f1='(st==2 || st==4) ? 1 : 0'
Ven en_3v3 0 PWL(0 0 \{ten\} 0 \{ten+100p\} \{vd\})
Vs0 sel0_3v3 0 PWL(0 \{i0*vd\} \{tsc\} \{i0*vd\} \{tsc+100p\} \{f0*vd\})
Vs1 sel1_3v3 0 PWL(0 \{i1*vd\} \{tsc\} \{i1*vd\} \{tsc+100p\} \{f1*vd\})
.control
tran 20n 200u
let tev = CACE\{step\} lt 3
let tev = tev * 1e-6 + (1 - tev) * 100e-6
meas tran Ibp_end find i(Vmbp) at=199u
let err = abs(i(Vmbp) / Ibp_end - 1)
let Ibp_end = abs(Ibp_end)
meas tran tx when err=0.01 fall=last
let t_settle = tx - tev
echo $&t_settle $&Ibp_end > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
