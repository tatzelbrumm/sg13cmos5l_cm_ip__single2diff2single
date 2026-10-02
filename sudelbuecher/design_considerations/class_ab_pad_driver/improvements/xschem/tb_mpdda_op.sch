v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {tb_mpdda_op: operating point of d2s_mpdda at vd = 0: device currents and saturation margin} 60 -440 0 0 0.5 0.5 {}
T {DUT and bias from the schematics in this directory; code block = the deck's .lib/.param/.save lines and its .control section} 60 -395 0 0 0.3 0.3 {}
N 100 170 100 -300 {lab=vdd}
N 100 230 100 700 {lab=GND}
N 200 170 200 130 {lab=vref}
N 200 230 200 700 {lab=GND}
N 620 300 620 -300 {lab=vdd}
N 620 620 620 700 {lab=GND}
N 920 -80 920 -300 {lab=vdd}
N 920 160 920 700 {lab=GND}
N 840 360 960 360 {lab=vbp}
N 960 360 960 160 {lab=vbp}
N 840 400 1000 400 {lab=vbn}
N 1000 400 1000 160 {lab=vbn}
N 840 440 1040 440 {lab=vbpc}
N 1040 440 1040 160 {lab=vbpc}
N 840 480 1080 480 {lab=vbnc}
N 1080 480 1080 160 {lab=vbnc}
N 840 520 1120 520 {lab=vabp}
N 1120 520 1120 160 {lab=vabp}
N 840 560 1160 560 {lab=vabn}
N 1160 560 1160 160 {lab=vabn}
N 300 230 300 700 {lab=GND}
N 300 170 300 -20 {lab=vinp}
N 300 -20 860 -20 {lab=vinp}
N 400 230 400 700 {lab=GND}
N 400 170 400 20 {lab=vinn}
N 400 20 860 20 {lab=vinn}
N 860 60 820 60 {lab=vref}
N 860 100 820 100 {lab=vout}
N 1220 -20 1320 -20 {lab=vout}
N 1420 -20 1460 -20 {lab=vout}
N 1320 40 1320 -20 {lab=vout}
N 1320 100 1320 140 {lab=vref}
N 1420 40 1420 -20 {lab=vout}
N 1420 100 1420 700 {lab=GND}
N 60 -300 100 -300 {lab=vdd}
N 100 700 200 700 {lab=GND}
N 1320 -20 1420 -20 {lab=vout}
N 620 -300 920 -300 {lab=vdd}
N 100 -300 620 -300 {lab=vdd}
N 300 700 400 700 {lab=GND}
N 200 700 300 700 {lab=GND}
N 920 700 1420 700 {lab=GND}
N 620 700 800 700 {lab=GND}
N 400 700 620 700 {lab=GND}
N 800 700 920 700 {lab=GND}
C {devices/vsource.sym} 100 200 0 0 {name=Vdd value=3.3 savecurrent=false}
C {devices/vsource.sym} 200 200 0 0 {name=Vcm value=1.65 savecurrent=false}
C {devices/lab_pin.sym} 200 130 0 1 {name=l1 sig_type=std_logic lab=vref}
C {d2s_bias_lp.sym} 700 460 0 0 {name=Xb}
C {d2s_mpdda.sym} 1040 40 0 0 {name=Xd}
C {devices/lab_wire.sym} 960 360 0 0 {name=l2 sig_type=std_logic lab=vbp}
C {devices/lab_wire.sym} 1000 400 0 0 {name=l3 sig_type=std_logic lab=vbn}
C {devices/lab_wire.sym} 1040 440 0 0 {name=l4 sig_type=std_logic lab=vbpc}
C {devices/lab_wire.sym} 1080 480 0 0 {name=l5 sig_type=std_logic lab=vbnc}
C {devices/lab_wire.sym} 1120 520 0 0 {name=l6 sig_type=std_logic lab=vabp}
C {devices/lab_wire.sym} 1160 560 0 0 {name=l7 sig_type=std_logic lab=vabn}
C {devices/vsource.sym} 300 200 0 0 {name=Vp value=1.65 savecurrent=false}
C {devices/lab_wire.sym} 300 -20 0 0 {name=l8 sig_type=std_logic lab=vinp}
C {devices/vsource.sym} 400 200 0 0 {name=Vn value=1.65 savecurrent=false}
C {devices/lab_wire.sym} 400 20 0 0 {name=l9 sig_type=std_logic lab=vinn}
C {devices/lab_pin.sym} 820 60 0 0 {name=l10 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 820 100 0 0 {name=l11 sig_type=std_logic lab=vout}
C {devices/lab_pin.sym} 1460 -20 0 1 {name=l12 sig_type=std_logic lab=vout}
C {devices/res.sym} 1320 70 0 0 {name=RL value=1k m=1}
C {devices/lab_pin.sym} 1320 140 0 1 {name=l13 sig_type=std_logic lab=vref}
C {devices/capa.sym} 1420 70 0 0 {name=CL value=100p m=1}
C {devices/code_shown.sym} 60 820 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.control
op
print v(xd.x) v(xd.y) v(xd.a) v(xd.b) v(xd.l1) v(xd.l2) v(xd.pl) v(xd.pr) i(vdd)
print @n.xd.xsx.nsg13_hv_nmos[ids] @n.xd.xsx.nsg13_hv_nmos[vds] @n.xd.xsx.nsg13_hv_nmos[vdss]
print @n.xd.xsy.nsg13_hv_nmos[ids] @n.xd.xsy.nsg13_hv_nmos[vds] @n.xd.xsy.nsg13_hv_nmos[vdss]
print @n.xd.xcx.nsg13_hv_nmos[ids] @n.xd.xcx.nsg13_hv_nmos[vds] @n.xd.xcx.nsg13_hv_nmos[vdss]
print @n.xd.xcy.nsg13_hv_nmos[ids] @n.xd.xcy.nsg13_hv_nmos[vds] @n.xd.xcy.nsg13_hv_nmos[vdss]
print @n.xd.xfnl.nsg13_hv_nmos[ids] @n.xd.xfnl.nsg13_hv_nmos[vds] @n.xd.xfnl.nsg13_hv_nmos[vdss]
print @n.xd.xabn.nsg13_hv_nmos[ids] @n.xd.xabn.nsg13_hv_nmos[vds] @n.xd.xabn.nsg13_hv_nmos[vdss]
print @n.xd.xon.nsg13_hv_nmos[ids] @n.xd.xon.nsg13_hv_nmos[vds] @n.xd.xon.nsg13_hv_nmos[vdss]
print @n.xd.xpl.nsg13_hv_pmos[ids] @n.xd.xpl.nsg13_hv_pmos[vds] @n.xd.xpl.nsg13_hv_pmos[vdss]
print @n.xd.xpr.nsg13_hv_pmos[ids] @n.xd.xpr.nsg13_hv_pmos[vds] @n.xd.xpr.nsg13_hv_pmos[vdss]
print @n.xd.xpcl.nsg13_hv_pmos[ids] @n.xd.xpcl.nsg13_hv_pmos[vds] @n.xd.xpcl.nsg13_hv_pmos[vdss]
print @n.xd.xpcr.nsg13_hv_pmos[ids] @n.xd.xpcr.nsg13_hv_pmos[vds] @n.xd.xpcr.nsg13_hv_pmos[vdss]
print @n.xd.xfpl.nsg13_hv_pmos[ids] @n.xd.xfpl.nsg13_hv_pmos[vds] @n.xd.xfpl.nsg13_hv_pmos[vdss]
print @n.xd.xabp.nsg13_hv_pmos[ids] @n.xd.xabp.nsg13_hv_pmos[vds] @n.xd.xabp.nsg13_hv_pmos[vdss]
print @n.xd.xop.nsg13_hv_pmos[ids] @n.xd.xop.nsg13_hv_pmos[vds] @n.xd.xop.nsg13_hv_pmos[vdss]
.endc"}
C {devices/lab_wire.sym} 60 -300 0 0 {name=l14 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} 800 700 0 0 {name=l0 lab=GND}
