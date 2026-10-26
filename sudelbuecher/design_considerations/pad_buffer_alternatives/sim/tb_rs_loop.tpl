* tb_rs_loop: loop gain of d2s_mpdda with a series pad resistor Rs, tt 27 C
* derived from tb_mpdda_loop.spice; Rs between the output-stage node vout_a and the pad vout;
* feedback taken at __FB__ (vout_a: before Rs; vout: at the pad); load __LOADNAME__
.lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.include ../units.spice
.include ../ccomp.spice
.include ../d2s_mpdda.spice
.include ../d2s_bias_lp.spice
Vdd vdd 0 3.3
Vddo vddo 0 3.3
Vsso vsso 0 0
Vcm vref 0 1.65
Xb vdd 0 vddo vsso vbp vbn vbpc vbnc vabp vabn d2s_bias_lp
Vp vinp 0 1.65
Vn vinn 0 1.65
Xd vdd 0 vddo vsso vinp vinn vref vout_a fb vbp vbn vbpc vbnc vabp vabn d2s_mpdda
Rs vout_a vout __RS__
Lb __FB__ fb 1G
Cb fb inj 1
Vinj inj 0 dc 0 ac 1
__LOAD__
.control
ac dec 50 10 1G
let T=-v(__FB__)/v(fb)
meas ac T0 find vdb(T) at=10
meas ac fc when vdb(T)=0
meas ac pT find vp(T) when vdb(T)=0
let pm=180/pi*pT+180
print T0 fc pm
.endc
.end
