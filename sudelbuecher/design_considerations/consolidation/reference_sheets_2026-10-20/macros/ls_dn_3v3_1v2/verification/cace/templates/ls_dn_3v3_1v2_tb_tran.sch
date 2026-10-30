v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Template testbench for CACE transient analysis: ls_dn_3v3_1v2.  Conditions: vddl, vddh, corner_mos, temp, tr, cload}  0 -450 0 0 0.5 0.5 {}
N 520 -400 520 -370 {lab=vddl}
N 560 -340 600 -340 {lab=out}
N 60 -160 60 -140 {lab=GND}
N 260 -180 260 -160 {lab=GND}
N 160 -160 260 -160 {lab=GND}
N 160 -180 160 -160 {lab=GND}
N 60 -180 60 -160 {lab=GND}
N 600 -180 600 -160 {lab=GND}
N 520 -160 600 -160 {lab=GND}
N 600 -340 600 -240 {lab=out}
N 520 -310 520 -160 {lab=GND}
N 60 -160 160 -160 {lab=GND}
N 160 -400 160 -240 {lab=vddl}
N 260 -340 260 -240 {lab=in}
N 60 -260 60 -240 {lab=vddh}
N 160 -400 520 -400 {lab=vddl}
N 260 -340 480 -340 {lab=in}
N 260 -160 520 -160 {lab=GND}
C {code_shown.sym} 0 -70 0 0 {name=NGSPICE only_toplevel=false value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options gmin=1e-15 abstol=1e-15 reltol=1e-4
* Flag unsafe operating conditions (exceeds models' specified limits)
.option warn=1
.control
tran 20p 120n
* ---- time base (s): rising edge starts at t0r, falling edge at t0f; windows end tsettle after the input is done
let tr = CACE\{tr\}
let tsettle = 10e-9
let t0r = 10e-9
let t1r = t0r + tr + tsettle
let t0f = t0r + tr + 60e-9
let t1f = t0f + tr + tsettle
let b0r = t0r - 4e-9
let b1r = t0r - 0.5e-9
let b0f = t0f - 4e-9
let b1f = t0f - 0.5e-9
let vmid_in = CACE\{vddh\} / 2
let vmid_out = CACE\{vddl\} / 2
* ---- delays, 50 % input to 50 % output
meas tran m_td_r trig v(in) val=$&vmid_in rise=1 targ v(out) val=$&vmid_out fall=1
meas tran m_td_f trig v(in) val=$&vmid_in fall=1 targ v(out) val=$&vmid_out rise=1
* ---- output levels, settled (just before the next edge)
meas tran m_Voh avg v(out) from=$&b0r to=$&b1r
meas tran m_Vol avg v(out) from=$&b0f to=$&b1f
let td_r = m_td_r
let td_f = m_td_f
let Voh = m_Voh
let Vol = m_Vol
* ---- quiescent, peak and charge per source
let ab_l = abs(vl#branch)
meas tran iq_l_lo avg i(VL) from=$&b0r to=$&b1r
meas tran iq_l_hi avg i(VL) from=$&b0f to=$&b1f
meas tran q_l_r integ i(VL) from=$&t0r to=$&t1r
meas tran ib_l_r avg i(VL) from=$&b0r to=$&b1r
meas tran pk_l_r max ab_l from=$&t0r to=$&t1r
meas tran q_l_f integ i(VL) from=$&t0f to=$&t1f
meas tran ib_l_f avg i(VL) from=$&b0f to=$&b1f
meas tran pk_l_f max ab_l from=$&t0f to=$&t1f
let ab_i = abs(vin#branch)
meas tran iq_i_lo avg i(VIN) from=$&b0r to=$&b1r
meas tran iq_i_hi avg i(VIN) from=$&b0f to=$&b1f
meas tran q_i_r integ i(VIN) from=$&t0r to=$&t1r
meas tran ib_i_r avg i(VIN) from=$&b0r to=$&b1r
meas tran pk_i_r max ab_i from=$&t0r to=$&t1r
meas tran q_i_f integ i(VIN) from=$&t0f to=$&t1f
meas tran ib_i_f avg i(VIN) from=$&b0f to=$&b1f
meas tran pk_i_f max ab_i from=$&t0f to=$&t1f
* ---- results in SI units (s, V, A, C, J); the yaml units (ns, pA, fC, uA, fW*s) are display units.  Delivered by the source = positive.
let Iq_vddl_inlo = -iq_l_lo
let Iq_vddl_inhi = -iq_l_hi
let Iq_in_inlo = abs(iq_i_lo)
let Iq_in_inhi = abs(iq_i_hi)
let Q_vddl_r = -(q_l_r - ib_l_r * (t1r - t0r))
let Q_vddl_f = -(q_l_f - ib_l_f * (t1f - t0f))
let Q_in_r = abs(q_i_r - ib_i_r * (t1r - t0r))
let Q_in_f = abs(q_i_f - ib_i_f * (t1f - t0f))
let Ipk_vddl_r = pk_l_r
let Ipk_vddl_f = pk_l_f
let Ipk_in_r = pk_i_r
let Ipk_in_f = pk_i_f
let E_cycle = (Q_vddl_r + Q_vddl_f) * CACE\{vddl\}
echo $&td_r $&td_f $&Voh $&Vol $&Iq_vddl_inlo $&Iq_vddl_inhi $&Iq_in_inlo $&Iq_in_inhi $&Q_vddl_r $&Q_vddl_f $&Q_in_r $&Q_in_f $&Ipk_vddl_r $&Ipk_vddl_f $&Ipk_in_r $&Ipk_in_f $&E_cycle > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
C {code_shown.sym} 900 -400 0 0 {name=MODEL only_toplevel=true format="tcleval( @value )" value="
.lib cornerMOSlv.lib mos_CACE\{corner_mos\}
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
"}
C {lab_pin.sym} 260 -340 0 0 {name=p5 sig_type=std_logic lab=in}
C {ls_dn_3v3_1v2.sym} 520 -340 0 0 {name=x1}
C {lab_pin.sym} 520 -400 0 1 {name=p7 sig_type=std_logic lab=vddl}
C {lab_pin.sym} 600 -340 2 0 {name=p8 sig_type=std_logic lab=out}
C {vsource.sym} 160 -210 0 0 {name=VL value="dc CACE\{vddl\}" savecurrent=false}
C {lab_pin.sym} 160 -260 0 0 {name=p10 sig_type=std_logic lab=vddl}
C {gnd.sym} 60 -140 0 0 {name=g11 lab=GND}
C {vsource.sym} 60 -210 0 0 {name=VH value="dc CACE\{vddh\}" savecurrent=false}
C {lab_pin.sym} 60 -260 0 0 {name=p12 sig_type=std_logic lab=vddh}
C {vsource.sym} 260 -210 0 0 {name=VIN value="PULSE(0 CACE\{vddh\} 10n CACE\{tr\} CACE\{tr\} 60n 1)" savecurrent=false}
C {lab_pin.sym} 260 -260 0 0 {name=p14 sig_type=std_logic lab=in}
C {capa.sym} 600 -210 0 0 {name=CL m=1 value=CACE\{cload\}}
C {lab_pin.sym} 600 -260 0 0 {name=p18 sig_type=std_logic lab=out}
