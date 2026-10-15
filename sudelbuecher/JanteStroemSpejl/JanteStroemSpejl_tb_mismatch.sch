v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Mismatch characterization: 10 mirror outputs at VDS = VGS(ref)} 40 -900 0 0 0.5 0.5 {}
T {Each output is clamped by an independent unity-gain VCVS, so it does not load IREF.} 40 -875 0 0 0.3 0.3 {}
N 200 -390 200 -300 {lab=0}
N 200 -450 300 -450 {lab=#net1}
N 300 -390 300 -360 {lab=IREF}
C {JanteStroemSpejl.sym} 430 -500 0 0 {name=XJANTE}
C {devices/gnd.sym} 200 -300 0 0 {name=GND1 lab=0}
C {devices/vsource.sym} 200 -420 0 0 {name=VDD value=1.2}
C {devices/isource.sym} 300 -420 0 0 {name=IREFSRC value=100u}
C {devices/lab_pin.sym} 300 -360 3 0 {name=lref lab=IREF}
C {devices/lab_pin.sym} 270 -640 0 0 {name=li lab=IREF}
C {devices/lab_pin.sym} 270 -580 0 0 {name=ls lab=0}
C {devices/lab_pin.sym} 270 -520 0 0 {name=lb lab=0}
C {devices/lab_pin.sym} 590 -680 2 0 {name=lout01 lab=OUT01}
C {devices/lab_pin.sym} 590 -640 2 0 {name=lout02 lab=OUT02}
C {devices/lab_pin.sym} 590 -600 2 0 {name=lout03 lab=OUT03}
C {devices/lab_pin.sym} 590 -560 2 0 {name=lout04 lab=OUT04}
C {devices/lab_pin.sym} 590 -520 2 0 {name=lout05 lab=OUT05}
C {devices/lab_pin.sym} 590 -480 2 0 {name=lout06 lab=OUT06}
C {devices/lab_pin.sym} 590 -440 2 0 {name=lout07 lab=OUT07}
C {devices/lab_pin.sym} 590 -400 2 0 {name=lout08 lab=OUT08}
C {devices/lab_pin.sym} 590 -360 2 0 {name=lout09 lab=OUT09}
C {devices/lab_pin.sym} 590 -320 2 0 {name=lout10 lab=OUT10}
C {devices/code_shown.sym} 700 -840 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt_mismatch
"}
C {devices/code_shown.sym} 700 -600 0 0 {name=CLAMPS only_toplevel=true
value="
ECL01 CL01 0 IREF 0 1
VMON01 CL01 OUT01 0
ECL02 CL02 0 IREF 0 1
VMON02 CL02 OUT02 0
ECL03 CL03 0 IREF 0 1
VMON03 CL03 OUT03 0
ECL04 CL04 0 IREF 0 1
VMON04 CL04 OUT04 0
ECL05 CL05 0 IREF 0 1
VMON05 CL05 OUT05 0
ECL06 CL06 0 IREF 0 1
VMON06 CL06 OUT06 0
ECL07 CL07 0 IREF 0 1
VMON07 CL07 OUT07 0
ECL08 CL08 0 IREF 0 1
VMON08 CL08 OUT08 0
ECL09 CL09 0 IREF 0 1
VMON09 CL09 OUT09 0
ECL10 CL10 0 IREF 0 1
VMON10 CL10 OUT10 0
"}
C {devices/code_shown.sym} 700 -260 0 0 {name=NGSPICE only_toplevel=true
value="
.temp 27
.control
  set wr_singlescale
  set wr_vecnames
  set appendwrite
  let run = 0
  dowhile run < 5
    reset
    op
  let e01 = (-i(VMON01)/100u)-1
  let e02 = (-i(VMON02)/100u)-1
  let e03 = (-i(VMON03)/100u)-1
  let e04 = (-i(VMON04)/100u)-1
  let e05 = (-i(VMON05)/100u)-1
  let e06 = (-i(VMON06)/100u)-1
  let e07 = (-i(VMON07)/100u)-1
  let e08 = (-i(VMON08)/100u)-1
  let e09 = (-i(VMON09)/100u)-1
  let e10 = (-i(VMON10)/100u)-1
    wrdata JanteStroemSpejl_mismatch.dat run e01 e02 e03 e04 e05 e06 e07 e08 e09 e10
    let run = run + 1
  end
  quit
.endc
"}
C {devices/launcher.sym} 1000 -820 0 0 {name=h1 descr="simulate mismatch"
tclcommand="xschem save; xschem netlist; xschem simulate"}
