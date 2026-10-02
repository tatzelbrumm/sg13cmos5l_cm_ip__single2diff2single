v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 60 -300 1640 -300 {lab=vdd}
C {devices/lab_wire.sym} 60 -300 0 0 {name=l1 sig_type=std_logic lab=vdd}
N 60 700 1640 700 {lab=GND}
C {devices/gnd.sym} 800 700 0 0 {name=l0 lab=GND}
C {devices/vsource.sym} 100 200 0 0 {name=Vdd value="CACE\{vdd\}" savecurrent=false}
N 100 170 100 -300 {lab=vdd}
N 100 230 100 700 {lab=GND}
C {devices/vsource.sym} 200 200 0 0 {name=Vref value=CACE\{vref=1.65\} savecurrent=false}
N 200 170 200 130 {lab=vref}
C {devices/lab_pin.sym} 200 130 0 1 {name=l2 sig_type=std_logic lab=vref}
N 200 230 200 700 {lab=GND}
C {devices/vsource.sym} 400 200 0 0 {name=Vic value="CACE\{vicm=1.65\}" savecurrent=false}
N 400 170 400 130 {lab=vic}
C {devices/lab_pin.sym} 400 130 0 1 {name=l3 sig_type=std_logic lab=vic}
N 400 230 400 700 {lab=GND}
C {devices/vsource.sym} 1580 400 0 0 {name=Vterm value=CACE\{vterm=1.65\} savecurrent=false}
N 1580 370 1580 330 {lab=vterm}
C {devices/lab_pin.sym} 1580 330 0 1 {name=l4 sig_type=std_logic lab=vterm}
N 1580 430 1580 700 {lab=GND}
C {d2s_miller_biased.sym} 1040 40 0 0 {name=x1}
N 920 -80 920 -300 {lab=vdd}
N 920 160 920 700 {lab=GND}
N 960 160 960 200 {lab=vbp}
C {devices/lab_pin.sym} 960 200 0 1 {name=l5 sig_type=std_logic lab=vbp}
N 1000 160 1000 220 {lab=vbn}
C {devices/lab_pin.sym} 1000 220 0 1 {name=l6 sig_type=std_logic lab=vbn}
N 1040 160 1040 240 {lab=vbpc}
C {devices/lab_pin.sym} 1040 240 0 1 {name=l7 sig_type=std_logic lab=vbpc}
N 1080 160 1080 260 {lab=vbnc}
C {devices/lab_pin.sym} 1080 260 0 1 {name=l8 sig_type=std_logic lab=vbnc}
N 1120 160 1120 280 {lab=vabp}
C {devices/lab_pin.sym} 1120 280 0 1 {name=l9 sig_type=std_logic lab=vabp}
N 1160 160 1160 300 {lab=vabn}
C {devices/lab_pin.sym} 1160 300 0 1 {name=l10 sig_type=std_logic lab=vabn}
C {devices/isource.sym} 160 900 0 0 {name=IQvbp value=CACE[CACE\{ibias_err=0\}*2e-05]}
C {devices/res.sym} 240 900 0 0 {name=RQvbp value=CACE[CACE\{va_bias=1e12\}/2e-05] m=1}
N 160 870 160 840 {lab=vbp}
C {devices/lab_pin.sym} 160 840 0 1 {name=l11 sig_type=std_logic lab=vbp}
N 160 930 160 960 {lab=GND}
C {devices/lab_pin.sym} 160 960 0 1 {name=l12 sig_type=std_logic lab=GND}
N 240 870 240 840 {lab=vbp}
C {devices/lab_pin.sym} 240 840 0 1 {name=l13 sig_type=std_logic lab=vbp}
N 240 930 240 960 {lab=GND}
C {devices/lab_pin.sym} 240 960 0 1 {name=l14 sig_type=std_logic lab=GND}
C {devices/isource.sym} 380 900 0 0 {name=IQvbn value=CACE[CACE\{ibias_err=0\}*5e-05]}
C {devices/res.sym} 460 900 0 0 {name=RQvbn value=CACE[CACE\{va_bias=1e12\}/5e-05] m=1}
N 380 870 380 840 {lab=vdd}
C {devices/lab_pin.sym} 380 840 0 1 {name=l15 sig_type=std_logic lab=vdd}
N 380 930 380 960 {lab=vbn}
C {devices/lab_pin.sym} 380 960 0 1 {name=l16 sig_type=std_logic lab=vbn}
N 460 870 460 840 {lab=vdd}
C {devices/lab_pin.sym} 460 840 0 1 {name=l17 sig_type=std_logic lab=vdd}
N 460 930 460 960 {lab=vbn}
C {devices/lab_pin.sym} 460 960 0 1 {name=l18 sig_type=std_logic lab=vbn}
C {devices/isource.sym} 600 900 0 0 {name=IQvbpc value=CACE[CACE\{ibias_err=0\}*5e-06]}
C {devices/res.sym} 680 900 0 0 {name=RQvbpc value=CACE[CACE\{va_bias=1e12\}/5e-06] m=1}
N 600 870 600 840 {lab=vbpc}
C {devices/lab_pin.sym} 600 840 0 1 {name=l19 sig_type=std_logic lab=vbpc}
N 600 930 600 960 {lab=GND}
C {devices/lab_pin.sym} 600 960 0 1 {name=l20 sig_type=std_logic lab=GND}
N 680 870 680 840 {lab=vbpc}
C {devices/lab_pin.sym} 680 840 0 1 {name=l21 sig_type=std_logic lab=vbpc}
N 680 930 680 960 {lab=GND}
C {devices/lab_pin.sym} 680 960 0 1 {name=l22 sig_type=std_logic lab=GND}
C {devices/isource.sym} 820 900 0 0 {name=IQvbnc value=CACE[CACE\{ibias_err=0\}*5e-06]}
C {devices/res.sym} 900 900 0 0 {name=RQvbnc value=CACE[CACE\{va_bias=1e12\}/5e-06] m=1}
N 820 870 820 840 {lab=vdd}
C {devices/lab_pin.sym} 820 840 0 1 {name=l23 sig_type=std_logic lab=vdd}
N 820 930 820 960 {lab=vbnc}
C {devices/lab_pin.sym} 820 960 0 1 {name=l24 sig_type=std_logic lab=vbnc}
N 900 870 900 840 {lab=vdd}
C {devices/lab_pin.sym} 900 840 0 1 {name=l25 sig_type=std_logic lab=vdd}
N 900 930 900 960 {lab=vbnc}
C {devices/lab_pin.sym} 900 960 0 1 {name=l26 sig_type=std_logic lab=vbnc}
C {devices/isource.sym} 1040 900 0 0 {name=IQvabp value=CACE[CACE\{ibias_err=0\}*5e-06]}
C {devices/res.sym} 1120 900 0 0 {name=RQvabp value=CACE[CACE\{va_bias=1e12\}/5e-06] m=1}
N 1040 870 1040 840 {lab=vabp}
C {devices/lab_pin.sym} 1040 840 0 1 {name=l27 sig_type=std_logic lab=vabp}
N 1040 930 1040 960 {lab=GND}
C {devices/lab_pin.sym} 1040 960 0 1 {name=l28 sig_type=std_logic lab=GND}
N 1120 870 1120 840 {lab=vabp}
C {devices/lab_pin.sym} 1120 840 0 1 {name=l29 sig_type=std_logic lab=vabp}
N 1120 930 1120 960 {lab=GND}
C {devices/lab_pin.sym} 1120 960 0 1 {name=l30 sig_type=std_logic lab=GND}
C {devices/isource.sym} 1260 900 0 0 {name=IQvabn value=CACE[CACE\{ibias_err=0\}*5e-06]}
C {devices/res.sym} 1340 900 0 0 {name=RQvabn value=CACE[CACE\{va_bias=1e12\}/5e-06] m=1}
N 1260 870 1260 840 {lab=vdd}
C {devices/lab_pin.sym} 1260 840 0 1 {name=l31 sig_type=std_logic lab=vdd}
N 1260 930 1260 960 {lab=vabn}
C {devices/lab_pin.sym} 1260 960 0 1 {name=l32 sig_type=std_logic lab=vabn}
N 1340 870 1340 840 {lab=vdd}
C {devices/lab_pin.sym} 1340 840 0 1 {name=l33 sig_type=std_logic lab=vdd}
N 1340 930 1340 960 {lab=vabn}
C {devices/lab_pin.sym} 1340 960 0 1 {name=l34 sig_type=std_logic lab=vabn}
T {bias-source quality: extra ibias_err*I_k and R_k = va_bias/I_k across each d2s_bias reference} 160 1000 0 0 0.3 0.3 {}
N 860 -20 820 -20 {lab=vic}
C {devices/lab_pin.sym} 820 -20 0 0 {name=l35 sig_type=std_logic lab=vic}
N 860 20 820 20 {lab=vic}
C {devices/lab_pin.sym} 820 20 0 0 {name=l36 sig_type=std_logic lab=vic}
N 860 60 820 60 {lab=vref}
C {devices/lab_pin.sym} 820 60 0 0 {name=l37 sig_type=std_logic lab=vref}
N 860 100 820 100 {lab=fb}
C {devices/lab_pin.sym} 820 100 0 0 {name=l38 sig_type=std_logic lab=fb}
N 1220 -20 1440 -20 {lab=vout}
N 1440 -20 1480 -20 {lab=vout}
C {devices/lab_pin.sym} 1480 -20 0 1 {name=l39 sig_type=std_logic lab=vout}
C {devices/res.sym} 1320 70 0 0 {name=RL value=CACE\{rload=1k\} m=1}
N 1320 40 1320 -20 {lab=vout}
N 1320 100 1320 140 {lab=vterm}
C {devices/lab_pin.sym} 1320 140 0 1 {name=l40 sig_type=std_logic lab=vterm}
C {devices/capa.sym} 1440 70 0 0 {name=CL m=1 value=CACE\{cload=100p\}}
N 1440 40 1440 -20 {lab=vout}
N 1440 100 1440 700 {lab=GND}
C {devices/ind.sym} 1320 -80 2 0 {name=Lb m=1 value=1G}
N 1320 -50 1320 -20 {lab=vout}
N 1320 -110 1320 -140 {lab=fb}
C {devices/lab_pin.sym} 1320 -140 0 1 {name=l41 sig_type=std_logic lab=fb}
C {devices/capa.sym} 1580 -200 0 0 {name=Cb m=1 value=1}
N 1580 -230 1580 -260 {lab=fb}
C {devices/lab_pin.sym} 1580 -260 0 1 {name=l42 sig_type=std_logic lab=fb}
C {devices/vsource.sym} 1580 -80 0 0 {name=Vinj value="dc 0 ac 1" savecurrent=false}
N 1580 -170 1580 -110 {lab=inj}
C {devices/lab_wire.sym} 1580 -110 0 0 {name=l43 sig_type=std_logic lab=inj}
N 1580 -50 1580 -20 {lab=GND}
C {devices/lab_pin.sym} 1580 -20 0 1 {name=l44 sig_type=std_logic lab=GND}
T {CACE template: loop gain T = -v(vout)/v(fb), loop broken at the vfb gate (DC closed through Lb)} 60 -440 0 0 0.6 0.6 {}
T {run directory: CACE\{simpath\}} 60 -370 0 0 0.3 0.3 {}
C {devices/code_shown.sym} -1000 -420 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_CACE\{corner_mos\}
.lib cornerRES.lib res_CACE\{corner_r\}
.lib cornerCAP.lib cap_CACE\{corner_c=typ\}
"}
C {devices/code_shown.sym} -1000 -300 0 0 {name=NGSPICE
simulator=ngspice
only_toplevel=false
value="
.include CACE\{DUT_path\}
.temp CACE\{temp\}
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15 SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
.control
save v(vout) v(fb)
ac dec 50 1 1G
let T = -v(vout)/v(fb)
let Tdb = vdb(T)
let Tph = cph(T)*180/pi
meas ac T0 find Tdb at=10
let fc = 0
meas ac fc when Tdb=0 fall=1
let phc = -180
meas ac phc find Tph when Tdb=0 fall=1
let PM = 180 + phc
* gain margin; stays at 1000 dB if the phase never reaches -180 deg
let gmdb = -1000
meas ac gmdb find Tdb when Tph=-180 cross=1
let GM = -gmdb
echo $&T0 $&fc $&PM $&GM > CACE\{filename\}_CACE\{N\}.data
.endc
"}
