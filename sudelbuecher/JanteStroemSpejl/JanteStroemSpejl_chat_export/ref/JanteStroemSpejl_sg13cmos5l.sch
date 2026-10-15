v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}

N 220 -350 280 -350 {
lab=IREF}
N 280 -350 340 -350 {
lab=IREF}
N 280 -390 280 -350 {
lab=IREF}
N 280 -390 500 -390 {
lab=VBIAS}
N 500 -390 500 -320 {
lab=VBIAS}
N 280 -320 300 -320 {
lab=VBIAS}
N 280 -350 280 -320 {
lab=VBIAS}

N 540 -350 600 -350 {
lab=IOUT}

N 340 -290 340 -250 {
lab=VSS}
N 340 -320 370 -320 {
lab=VSS}
N 370 -320 370 -250 {
lab=VSS}
N 340 -250 540 -250 {
lab=VSS}
N 540 -290 540 -250 {
lab=VSS}
N 540 -320 570 -320 {
lab=VSS}
N 570 -320 570 -250 {
lab=VSS}
N 420 -250 420 -220 {
lab=VSS}

C {devices/ipin.sym} 220 -350 0 0 {name=p1 lab=IREF}
C {devices/opin.sym} 600 -350 0 0 {name=p2 lab=IOUT}
C {devices/iopin.sym} 420 -220 1 0 {name=p3 lab=VSS}

C {sg13g2_pr/sg13_lv_nmos.sym} 320 -320 0 0 {name=MREF
l={64*lambda}
w={4*lambda}
ng=1
m=11
model=sg13_lv_nmos
spiceprefix=X
}

C {sg13g2_pr/sg13_lv_nmos.sym} 520 -320 0 0 {name=MOUT
l={64*lambda}
w={4*lambda}
ng=1
m=11
model=sg13_lv_nmos
spiceprefix=X
}

C {devices/code_shown.sym} 120 -120 0 0 {name=PARAMS only_toplevel=false
value="
* JanteStroemSpejl geometry, interpreted as an NMOS current mirror.
* Square contact in artwork = 2 lambda.
* SG13CMOS5L contact side assumed 0.16 um -> lambda = 0.08 um.
.param lambda=80n
"
}

C {devices/title.sym} 160 -40 0 0 {name=l1 author="JanteStroemSpejl -> IHP SG13CMOS5L, geometry-derived"}
T {JanteStrømSpejl: compact electrical interpretation of the artwork} 150 -470 0 0 0.4 0.4 {}
T {Artwork geometry: contact=2λ; diffusion width W=4λ; poly overlap L=64λ; 11 rows => m=11 per side} 150 -445 0 0 0.3 0.3 {}
T {With contact=0.16 µm: λ=0.08 µm, W=0.32 µm, L=5.12 µm, effective W per side=3.52 µm} 150 -425 0 0 0.3 0.3 {}
T {MREF is diode-connected; MOUT mirrors IREF. Bulk and source -> VSS.} 150 -405 0 0 0.3 0.3 {}
