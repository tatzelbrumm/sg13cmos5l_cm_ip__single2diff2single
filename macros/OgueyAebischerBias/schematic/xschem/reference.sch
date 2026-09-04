v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {H. J. Oguey and D. Aebischer, “CMOS current reference without resistance,”
IEEE J. Solid-State Circuits, vol. 32, no. 7, pp. 1132–1135, Jul. 1997} 240 -170 0 0 0.3 0.3 {}
N 400 -360 420 -360 { lab=vbp}
N 420 -420 420 -360 { lab=vbp}
N 420 -420 640 -420 { lab=vbp}
N 640 -420 640 -360 { lab=vbp}
N 620 -360 640 -360 { lab=vbp}
N 400 -320 420 -320 { lab=vbr}
N 420 -320 420 -240 { lab=vbr}
N 420 -240 640 -240 { lab=vbr}
N 640 -320 640 -240 { lab=vbr}
N 620 -320 640 -320 { lab=vbr}
N 400 -340 440 -340 { lab=vbn}
N 440 -340 440 -260 { lab=vbn}
N 440 -260 660 -260 { lab=vbn}
N 660 -340 660 -260 { lab=vbn}
N 620 -340 660 -340 { lab=vbn}
N 560 -300 560 -200 { lab=vss}
N 340 -200 560 -200 { lab=vss}
N 340 -300 340 -200 { lab=vss}
N 340 -500 340 -380 { lab=vdd}
N 340 -500 560 -500 { lab=vdd}
N 560 -500 560 -380 { lab=vdd}
N 220 -200 340 -200 { lab=vss}
N 220 -500 340 -500 { lab=vdd}
N 640 -420 700 -420 {
lab=vbp}
N 660 -260 700 -260 {
lab=vbn}
N 640 -240 700 -240 {
lab=vbr}
N 220 -320 280 -320 {}
C {devices/title.sym} 160 -40 0 0 {name=l1 author="Christoph Maier"}
C {OgueyAebischerBias.sym} 560 -340 0 0 {name=xbias}
C {ToBiasStartup.sym} 340 -340 0 0 {name=xstart}
C {devices/lab_wire.sym} 490 -500 0 0 {name=l3 lab=vdd}
C {devices/lab_wire.sym} 490 -420 0 0 {name=l6 lab=vbp}
C {devices/lab_wire.sym} 490 -260 0 0 {name=l7 lab=vbn}
C {devices/lab_wire.sym} 490 -240 0 0 {name=l8 lab=vbr}
C {devices/iopin.sym} 220 -200 0 1 {name=p0 lab=vss}
C {devices/iopin.sym} 220 -500 0 1 {name=p1 lab=vdd}
C {devices/iopin.sym} 700 -420 0 0 {name=p2 lab=vbp}
C {devices/iopin.sym} 700 -260 0 0 {name=p3 lab=vbn}
C {devices/iopin.sym} 700 -240 0 0 {name=p4 lab=vbr}
C {devices/ipin.sym} 220 -320 0 0 {name=p5 lab=disable}
