* tb_rs_step: step response of d2s_mpdda with a series pad resistor Rs, vd -0.5 -> +0.5 V, tt 27 C
* derived from tb_mpdda_step.spice; feedback at __FB__; load __LOADNAME__; settling measured at the pad
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
.param vstep=0.5
Vd dp 0 pulse({-vstep} {vstep} 1u 1n 1n 4u 8u)
Ep vinp vref dp 0 0.5
En vinn vref dp 0 -0.5
Xd vdd 0 vddo vsso vinp vinn vref vout_a __FB__ vbp vbn vbpc vbnc vabp vabn d2s_mpdda
Rs vout_a vout __RS__
__LOAD__
.control
tran 2n 9u
meas tran vlo find v(vout) at=0.99u
meas tran vhi find v(vout) at=4.9u
meas tran vmax max v(vout) from=1u to=5u
let os = 100*(vmax - vhi)/(vhi - vlo)
let v10 = vlo + 0.1*(vhi - vlo)
let v90 = vlo + 0.9*(vhi - vlo)
meas tran t10 when v(vout)=v10 rise=1
meas tran t90 when v(vout)=v90 rise=1
let rate = 0.8*(vhi - vlo)/(t90 - t10)
let gainp = (vhi - vlo)/1.0
print vlo vhi gainp os rate
wrdata step.dat v(vout)
.endc
.end
