v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template, settling after enable / sel change: bias_sel_pd. Conditions: step, corner_mos, temp, vdd, iref, cores} 0 -40 0 0 0.4 0.4 {}
N 200 0 200 40 {lab=vdd}
N 180 220 180 260 {lab=GND}
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
C {devices/code_shown.sym} 0 300 0 0 {name=MODEL only_toplevel=true format="tcleval( @value )" value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_typ
.lib cornerPNP.lib CACE\{corner_pnp\}
"}
C {devices/code_shown.sym} 0 420 0 0 {name=NGSPICE only_toplevel=false value="
* core view, condition cores (default schematic): templates/cores/<cores>.spice may define oa_core_pd and bg_core_pd
* from their layout extraction. ngspice keeps the first definition of a subckt and ignores the DUT netlist's own.
.include CACE\{templates\}/cores/CACE\{cores=schematic\}.spice
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options gmin=1e-12 abstol=1e-12 reltol=1e-4
.option warn=1
.param vd=CACE\{vdd\}
Vdd vdd 0 \{vd\}
Vddo vddo 0 \{vd\}
Vsso vsso 0 0
* class-AB diode stacks of the pad as fixtures: in the DUT's tree until 2026-10-27, in the pad since then (RP2 / RN2 in d2s_mpdda_pd, RP1 / RN1 in d2s_out_p / d2s_out_n since 2026-10-28);
* same devices on the same nets, so the circuit is the one characterized before (the replica loads below measure them)
XRP1 dabp dabp vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
XRP2 vabp vabp dabp vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
XRN1 dabn dabn vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
XRN2 vabn vabn dabn 0 sg13_hv_nmos w=4.4u l=1u ng=1
* harness iDAC model: a PMOS mirror on its own 3.3 V supply sources CACE\{iref\} into ibias
Vext vext 0 3.3
Iext xg 0 CACE\{iref\}
XEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
* replica loads: each copies one bias diode (same device, gate on the bias line, drain forced to the gate
* voltage by an ideal buffer), so the current through Vm.. is that diode's current
* (XRabp1 / XRabn1 etc. were XRp1 / XRn1 etc. until 2026-10-30: same names as the fixtures XRP1 / XRN1 in SPICE, so ngspice-47 stopped)
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
XRabp1 n1r n1r vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
XRabp2 mdabp vabp n1r vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
Eabp eabp 0 vabp 0 1
Vmabp eabp mdabp 0
XRabn1 n2r n2r vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
XRabn2 mdabn vabn n2r 0 sg13_hv_nmos w=4.4u l=1u ng=1
Eabn eabn 0 vabn 0 1
Vmabn mdabn eabn 0
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
* en_3v3_b: the inverter that was inside bias_sel_pd (XIB in en_ctrl_3v3 in the pad)
XIBP en_3v3_b en_3v3 vdd vdd sg13_hv_pmos w=1u l=0.45u ng=1
XIBN en_3v3_b en_3v3 0 0 sg13_hv_nmos w=1u l=0.45u ng=1
Vs0 sel0_3v3 0 PWL(0 \{i0*vd\} \{tsc\} \{i0*vd\} \{tsc+100p\} \{f0*vd\})
Vs1 sel1_3v3 0 PWL(0 \{i1*vd\} \{tsc\} \{i1*vd\} \{tsc+100p\} \{f1*vd\})
.control
* reltol 1e-4 for the transient: the core views magic_pex_3 / magic_pex_2_mm_ok loosen it to 1e-3 at run time for
* the op; settling to 1 % needs 1e-4 (no effect with the other views, which keep the 1e-4 of .options)
option reltol=1e-4
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
C {bias_sel_pd.sym} 230 130 0 0 {name=x1}
C {devices/lab_pin.sym} 200 0 0 0 {name=l1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 180 260 0 0 {name=l2 sig_type=std_logic lab=GND}
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
