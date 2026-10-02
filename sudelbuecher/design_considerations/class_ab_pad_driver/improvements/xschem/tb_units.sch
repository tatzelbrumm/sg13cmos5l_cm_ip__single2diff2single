v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {tb_units: transfer of one DDA unit as used in the MP-DDA, tt 27 C} 60 -440 0 0 0.5 0.5 {}
T {fA = i(Vfx1) - i(Vfy1) for unit A (gp = vref + x), fB = i(Vfx2) - i(Vfy2) for unit B (gn = vref - x); replace unit_r2 by unit_r, unit_t, unit_w or unit_q to test another unit} 60 -395 0 0 0.3 0.3 {}
N 100 170 100 -300 {lab=vdd}
N 100 230 100 700 {lab=GND}
N 200 170 200 130 {lab=vref}
N 200 230 200 700 {lab=GND}
N 300 170 300 130 {lab=xd}
N 300 230 300 700 {lab=GND}
N 460 -250 460 -300 {lab=vdd}
N 460 -220 480 -220 {lab=vdd}
N 480 -220 480 -300 {lab=vdd}
N 420 -220 420 -160 {lab=vbp}
N 420 -160 460 -160 {lab=vbp}
N 460 -190 460 -160 {lab=vbp}
N 460 -160 460 -100 {lab=vbp}
N 460 130 460 700 {lab=GND}
N 460 -100 560 -100 {lab=vbp}
N 960 20 960 -300 {lab=vdd}
N 1040 20 1040 -100 {lab=vbp}
N 1040 180 1040 700 {lab=GND}
N 960 180 960 220 {lab=x1}
N 960 220 930 220 {lab=x1}
N 900 220 900 270 {lab=x1}
N 1000 180 1000 230 {lab=y1}
N 900 330 900 700 {lab=GND}
N 1000 330 1000 700 {lab=GND}
N 720 50 680 50 {lab=xd}
N 720 90 680 90 {lab=GND}
N 760 100 760 130 {lab=vref}
N 760 40 800 40 {lab=gpa}
N 800 40 800 80 {lab=gpa}
N 800 80 900 80 {lab=gpa}
N 900 120 860 120 {lab=vref}
N 1360 20 1360 -300 {lab=vdd}
N 1440 20 1440 -100 {lab=vbp}
N 1440 180 1440 700 {lab=GND}
N 1360 180 1360 220 {lab=x2}
N 1360 220 1330 220 {lab=x2}
N 1300 220 1300 270 {lab=x2}
N 1400 180 1400 230 {lab=y2}
N 1300 330 1300 700 {lab=GND}
N 1400 330 1400 700 {lab=GND}
N 1120 130 1080 130 {lab=xd}
N 1120 170 1080 170 {lab=GND}
N 1160 180 1160 210 {lab=vref}
N 1160 120 1200 120 {lab=gnb}
N 1200 120 1300 120 {lab=gnb}
N 1300 80 1260 80 {lab=vref}
N 60 -300 100 -300 {lab=vdd}
N 100 700 200 700 {lab=GND}
N 460 -100 460 70 {lab=vbp}
N 1040 -100 1440 -100 {lab=vbp}
N 560 -100 1040 -100 {lab=vbp}
N 930 220 900 220 {lab=x1}
N 1000 230 1000 270 {lab=y1}
N 1330 220 1300 220 {lab=x2}
N 1400 230 1400 270 {lab=y2}
N 480 -300 960 -300 {lab=vdd}
N 460 -300 480 -300 {lab=vdd}
N 100 -300 460 -300 {lab=vdd}
N 300 700 460 700 {lab=GND}
N 200 700 300 700 {lab=GND}
N 960 -300 1360 -300 {lab=vdd}
N 1400 700 1440 700 {lab=GND}
N 460 700 800 700 {lab=GND}
N 900 700 1000 700 {lab=GND}
N 800 700 900 700 {lab=GND}
N 1300 700 1400 700 {lab=GND}
N 1040 700 1300 700 {lab=GND}
N 1000 700 1040 700 {lab=GND}
C {devices/vsource.sym} 100 200 0 0 {name=Vdd value=3.3 savecurrent=false}
C {devices/vsource.sym} 200 200 0 0 {name=Vref value=1.65 savecurrent=false}
C {devices/lab_pin.sym} 200 130 0 1 {name=l1 sig_type=std_logic lab=vref}
C {devices/vsource.sym} 300 200 0 0 {name=Vx value=0 savecurrent=false}
C {devices/lab_pin.sym} 300 130 0 1 {name=l2 sig_type=std_logic lab=xd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 440 -220 0 0 {name=BP
l=6u
w=5u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/isource.sym} 460 100 0 0 {name=IBP value=5u}
C {devices/lab_wire.sym} 560 -100 0 0 {name=l3 sig_type=std_logic lab=vbp}
C {unit_r2.sym} 1000 100 0 0 {name=XUA}
C {devices/vsource.sym} 900 300 0 0 {name=Vfx1 value=0.45 savecurrent=false}
C {devices/vsource.sym} 1000 300 0 0 {name=Vfy1 value=0.45 savecurrent=false}
C {devices/lab_wire.sym} 930 220 0 0 {name=l4 sig_type=std_logic lab=x1}
C {devices/lab_wire.sym} 1000 230 0 1 {name=l5 sig_type=std_logic lab=y1}
C {devices/vcvs.sym} 760 70 0 0 {name=EpA value=1}
C {devices/lab_pin.sym} 680 50 0 0 {name=l6 sig_type=std_logic lab=xd}
C {devices/lab_pin.sym} 680 90 0 0 {name=l7 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 760 130 0 1 {name=l8 sig_type=std_logic lab=vref}
C {devices/lab_wire.sym} 800 40 0 0 {name=l9 sig_type=std_logic lab=gpa}
C {devices/lab_pin.sym} 860 120 0 0 {name=l10 sig_type=std_logic lab=vref}
C {unit_r2.sym} 1400 100 0 0 {name=XUB}
C {devices/vsource.sym} 1300 300 0 0 {name=Vfx2 value=0.45 savecurrent=false}
C {devices/vsource.sym} 1400 300 0 0 {name=Vfy2 value=0.45 savecurrent=false}
C {devices/lab_wire.sym} 1330 220 0 0 {name=l11 sig_type=std_logic lab=x2}
C {devices/lab_wire.sym} 1400 230 0 1 {name=l12 sig_type=std_logic lab=y2}
C {devices/vcvs.sym} 1160 150 0 0 {name=EnB value=-1}
C {devices/lab_pin.sym} 1080 130 0 0 {name=l13 sig_type=std_logic lab=xd}
C {devices/lab_pin.sym} 1080 170 0 0 {name=l14 sig_type=std_logic lab=GND}
C {devices/lab_pin.sym} 1160 210 0 1 {name=l15 sig_type=std_logic lab=vref}
C {devices/lab_wire.sym} 1200 120 0 0 {name=l16 sig_type=std_logic lab=gnb}
C {devices/lab_pin.sym} 1260 80 0 0 {name=l17 sig_type=std_logic lab=vref}
C {devices/code_shown.sym} 60 820 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.param wwi=4u lwi=4u
.control
dc Vx -0.8 0.8 0.005
let fA = i(Vfx1) - i(Vfy1)
let fB = i(Vfx2) - i(Vfy2)
meas dc fa05 find fA at=0.5
meas dc fb05 find fB at=0.5
meas dc fam05 find fA at=-0.5
meas dc fbm05 find fB at=-0.5
print fa05 fb05 fam05 fbm05
if $?batchmode = 0
  plot fA fB
  plot fA-fB
end
.endc"}
C {devices/lab_wire.sym} 60 -300 0 0 {name=l18 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} 800 700 0 0 {name=l0 lab=GND}
