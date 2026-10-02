v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {tb_moscv: C-V of a thick-oxide PMOS used as accumulation capacitor (gate vs S/D/well),} 60 -200 0 0 0.5 0.5 {}
T {X1: hv PMOS 14u x 14u, gate g against S/D/well w (accumulation); XM: cap_cmomi 31u x 31u} 60 -155 0 0 0.3 0.3 {}
N 200 230 200 400 {lab=GND}
N 200 170 200 0 {lab=g}
N 200 0 300 0 {lab=g}
N 440 -30 440 0 {lab=w}
N 440 0 440 30 {lab=w}
N 440 0 520 0 {lab=w}
N 560 0 560 170 {lab=w}
N 560 230 560 400 {lab=GND}
N 700 230 700 400 {lab=GND}
N 700 170 700 100 {lab=g2}
N 700 100 760 100 {lab=g2}
N 820 100 820 170 {lab=g2}
N 820 230 820 400 {lab=GND}
N 200 400 480 400 {lab=GND}
N 300 0 400 0 {lab=g}
N 520 0 560 0 {lab=w}
N 760 100 820 100 {lab=g2}
N 700 400 820 400 {lab=GND}
N 480 400 560 400 {lab=GND}
N 560 400 700 400 {lab=GND}
C {devices/vsource.sym} 200 200 0 0 {name=Vg value="dc \{1.65+vgw\} ac 1" savecurrent=false}
C {devices/lab_wire.sym} 300 0 0 0 {name=l1 sig_type=std_logic lab=g}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 420 0 0 0 {name=1
l=14u
w=14u
ng=1
m=1
mm_ok=1
model=sg13_hv_pmos
spiceprefix=X}
C {devices/lab_wire.sym} 520 0 0 1 {name=l2 sig_type=std_logic lab=w}
C {devices/vsource.sym} 560 200 0 0 {name=Vw value=1.65 savecurrent=false}
C {devices/vsource.sym} 700 200 0 0 {name=Vg2 value="dc 0 ac 1" savecurrent=false}
C {devices/lab_wire.sym} 760 100 0 0 {name=l3 sig_type=std_logic lab=g2}
C {sg13cmos5l_pr/cap_cmomi.sym} 820 200 0 0 {name=M
model=cap_cmomi
w=31e-6
l=31e-6
mmin=1
mmax=4
feed=double
subblock=0
m=1
mm_ok=1
spiceprefix=X}
C {devices/code_shown.sym} 60 520 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerCAP.lib cap_typ
.param vgw=0.5
.control
foreach v -1.0 -0.5 0 0.15 0.5 1.0 1.25 1.5 2.0
  alter Vg dc = $v + 1.65
  ac lin 1 1meg 1meg
  let c = -imag(i(Vg))/(2*pi*1e6)
  echo vgw = $v  C = $&c
end
let cm = -imag(i(Vg2))/(2*pi*1e6)
echo MOM 31x31: C = $&cm
.endc"}
C {devices/gnd.sym} 480 400 0 0 {name=l0 lab=GND}
