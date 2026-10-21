v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Template testbench for CACE transient analysis: ls_up_1v2_3v3.  Conditions: vddl, vddh, corner_mos, temp, tr, cload}  0 -470 0 0 0.5 0.5 {}
N 530 -390 530 -360 {lab=vddl}
N 580 -330 620 -330 {lab=out}
N 80 -150 80 -130 {lab=GND}
N 280 -170 280 -150 {lab=GND}
N 180 -150 280 -150 {lab=GND}
N 180 -170 180 -150 {lab=GND}
N 80 -170 80 -150 {lab=GND}
N 620 -170 620 -150 {lab=GND}
N 620 -330 620 -230 {lab=out}
N 540 -300 540 -150 {lab=GND}
N 280 -150 540 -150 {lab=GND}
N 80 -150 180 -150 {lab=GND}
N 550 -410 550 -360 {lab=vddh}
N 180 -390 530 -390 {lab=vddl}
N 180 -390 180 -230 {lab=vddl}
N 80 -410 550 -410 {lab=vddh}
N 80 -410 80 -230 {lab=vddh}
N 280 -330 500 -330 {lab=in}
N 280 -330 280 -230 {lab=in}
N 540 -150 620 -150 {lab=GND}
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
let vmid_in = CACE\{vddl\} / 2
let vmid_out = CACE\{vddh\} / 2
* ---- delays, 50 % input to 50 % output
meas tran m_td_r trig v(in) val=$&vmid_in rise=1 targ v(out) val=$&vmid_out rise=1
meas tran m_td_f trig v(in) val=$&vmid_in fall=1 targ v(out) val=$&vmid_out fall=1
* ---- output levels, settled (just before the next edge)
meas tran m_Voh avg v(out) from=$&b0f to=$&b1f
meas tran m_Vol avg v(out) from=$&b0r to=$&b1r
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
let ab_h = abs(vh#branch)
meas tran iq_h_lo avg i(VH) from=$&b0r to=$&b1r
meas tran iq_h_hi avg i(VH) from=$&b0f to=$&b1f
meas tran q_h_r integ i(VH) from=$&t0r to=$&t1r
meas tran ib_h_r avg i(VH) from=$&b0r to=$&b1r
meas tran pk_h_r max ab_h from=$&t0r to=$&t1r
meas tran q_h_f integ i(VH) from=$&t0f to=$&t1f
meas tran ib_h_f avg i(VH) from=$&b0f to=$&b1f
meas tran pk_h_f max ab_h from=$&t0f to=$&t1f
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
let Iq_vddh_inlo = -iq_h_lo
let Iq_vddh_inhi = -iq_h_hi
let Iq_in_inlo = abs(iq_i_lo)
let Iq_in_inhi = abs(iq_i_hi)
let Q_vddl_r = -(q_l_r - ib_l_r * (t1r - t0r))
let Q_vddl_f = -(q_l_f - ib_l_f * (t1f - t0f))
let Q_vddh_r = -(q_h_r - ib_h_r * (t1r - t0r))
let Q_vddh_f = -(q_h_f - ib_h_f * (t1f - t0f))
let Q_in_r = abs(q_i_r - ib_i_r * (t1r - t0r))
let Q_in_f = abs(q_i_f - ib_i_f * (t1f - t0f))
let Ipk_vddl_r = pk_l_r
let Ipk_vddl_f = pk_l_f
let Ipk_vddh_r = pk_h_r
let Ipk_vddh_f = pk_h_f
let Ipk_in_r = pk_i_r
let Ipk_in_f = pk_i_f
let E_cycle = (Q_vddl_r + Q_vddl_f) * CACE\{vddl\} + (Q_vddh_r + Q_vddh_f) * CACE\{vddh\}
echo $&td_r $&td_f $&Voh $&Vol $&Iq_vddl_inlo $&Iq_vddl_inhi $&Iq_vddh_inlo $&Iq_vddh_inhi $&Iq_in_inlo $&Iq_in_inhi $&Q_vddl_r $&Q_vddl_f $&Q_vddh_r $&Q_vddh_f $&Q_in_r $&Q_in_f $&Ipk_vddl_r $&Ipk_vddl_f $&Ipk_vddh_r $&Ipk_vddh_f $&Ipk_in_r $&Ipk_in_f $&E_cycle > CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data
.endc
"}
C {code_shown.sym} 900 -400 0 0 {name=MODEL only_toplevel=true format="tcleval( @value )" value="
.lib cornerMOSlv.lib mos_CACE\{corner_mos\}
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
"}
C {ls_up_1v2_3v3.sym} 540 -330 0 0 {name=x1}
C {lab_pin.sym} 550 -410 2 0 {name=p3 sig_type=std_logic lab=vddh}
C {lab_pin.sym} 280 -330 0 0 {name=p5 sig_type=std_logic lab=in}
C {lab_pin.sym} 530 -390 0 1 {name=p7 sig_type=std_logic lab=vddl}
C {lab_pin.sym} 620 -330 2 0 {name=p8 sig_type=std_logic lab=out}
C {vsource.sym} 180 -200 0 0 {name=VL value="dc CACE\{vddl\}" savecurrent=false}
C {lab_pin.sym} 180 -250 0 0 {name=p10 sig_type=std_logic lab=vddl}
C {gnd.sym} 80 -130 0 0 {name=g11 lab=GND}
C {vsource.sym} 80 -200 0 0 {name=VH value="dc CACE\{vddh\}" savecurrent=false}
C {lab_pin.sym} 80 -250 0 0 {name=p12 sig_type=std_logic lab=vddh}
C {vsource.sym} 280 -200 0 0 {name=VIN value="PULSE(0 CACE\{vddl\} 10n CACE\{tr\} CACE\{tr\} 60n 1)" savecurrent=false}
C {lab_pin.sym} 280 -250 0 0 {name=p14 sig_type=std_logic lab=in}
C {capa.sym} 620 -200 0 0 {name=CL m=1 value=CACE\{cload\}}
C {lab_pin.sym} 620 -250 0 0 {name=p18 sig_type=std_logic lab=out}
