v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {CACE template, start-up from a supply ramp: bias_sel_pd. Conditions: sel, vdd, tramp, iref, corner_mos, corner_r, corner_pnp, temp, cores} 0 -40 0 0 0.4 0.4 {}
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
C {devices/code_shown.sym} 0 300 0 0 {name=MODEL only_toplevel=true format="tcleval( @value )" value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_typ
.lib cornerPNP.lib CACE\{corner_pnp\}
"}
C {devices/code_shown.sym} 0 420 0 0 {name=NGSPICE only_toplevel=false value="
* start-up from 0 V (added 2026-10-30, cloud session C1; measurement of bias_oa_pd_tb_startup.sch): every supply,
* the harness supply and its current, en_3v3 and the select bits ramp from 0 in tramp; all nodes start at 0 V (uic).
* The dc value of each source is what op sees (the reference operating point), the pwl is what tran sees.
* Core view as in bias_sel_pd_tb_dc.sch.
.include CACE\{templates\}/cores/CACE\{cores=schematic\}.spice
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options gmin=1e-12 abstol=1e-12 reltol=1e-4 method=gear
.option warn=1
* itl4: sel 2, ff, -40 C, 3.6 V, 1 us ramp stopped with 'timestep too small' in pnpMPA at the default 10
.option itl4=1000
.param vd=CACE\{vdd\}
.param tr=CACE\{tramp\}
Vdd vdd 0 dc \{vd\} pwl(0 0 \{tr\} \{vd\})
Vddo vddo 0 dc \{vd\} pwl(0 0 \{tr\} \{vd\})
Vsso vsso 0 0
* class-AB diode stacks of the pad as fixtures (as in bias_sel_pd_tb_dc.sch)
XRP1 dabp dabp vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2
XRP2 vabp vabp dabp vdd sg13_hv_pmos w=6.66u l=0.6u ng=1
XRN1 dabn dabn vsso vsso sg13_hv_nmos w=8.8u l=1u ng=2
XRN2 vabn vabn dabn 0 sg13_hv_nmos w=4.4u l=1u ng=1
* harness iDAC model (as in bias_sel_pd_tb_dc.sch), ramped with the rest
Vext vext 0 dc 3.3 pwl(0 0 \{tr\} 3.3)
Iext xg 0 dc CACE\{iref\} pwl(0 0 \{tr\} CACE\{iref\})
XEd xg xg vext vext sg13_hv_pmos w=5u l=6u
XEm ibias xg vext vext sg13_hv_pmos w=5u l=6u
* replica loads (as in bias_sel_pd_tb_dc.sch): each copies one bias diode, drain forced to the gate voltage
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
* sel: 0 harness ibias, 1 Oguey-Aebischer core, 2 bandgap core, 3 both cores; en_3v3 and the select bits follow vdd
.param sl=CACE\{sel\}
.param f0='(sl==1 || sl==3) ? 1 : 0'
.param f1='(sl==2 || sl==3) ? 1 : 0'
Een en_3v3 0 vdd 0 1
XIBP en_3v3_b en_3v3 vdd vdd sg13_hv_pmos w=1u l=0.45u ng=1
XIBN en_3v3_b en_3v3 0 0 sg13_hv_nmos w=1u l=0.45u ng=1
Es0 sel0_3v3 0 vdd 0 \{f0\}
Es1 sel1_3v3 0 vdd 0 \{f1\}
.control
op
let t = abs(i(Vmbp))
set dcbp = $&t
let t = abs(i(Vmabn))
set dcabn = $&t
let ts = CACE\{tramp\} + 1m
let tstep = ts / 4000
set tss = $&ts
tran $&tstep $&ts uic
let ib = abs(i(Vmbp))
let ia = abs(i(Vmabn))
meas tran ibf find ib at=$tss
meas tran iaf find ia at=$tss
let ith = 0.9 * ibf
meas tran t90 when ib=$&ith cross=last
* results: t90 = last crossing of 90 % of the final vbp current, counted from t = 0 (s);
* final vbp / vabn currents 1 ms after the ramp relative to the dc operating point (fraction)
let t_su90 = t90
let Rbp_end = ibf / $dcbp
let Rabn_end = iaf / $dcabn
echo $&t_su90 $&Rbp_end $&Rabn_end > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
