v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 140 -220 180 -220 {lab=gate}
N 220 -190 220 -140 {lab=iovss}
N 140 -140 220 -140 {lab=iovss}
N 220 -220 240 -220 {lab=iovss}
N 240 -220 240 -140 {lab=iovss}
N 220 -140 240 -140 {lab=iovss}
N 140 -300 220 -300 {lab=iovss}
N 220 -300 220 -250 {lab=iovss}
C {sg13g2_pr/sg13_hv_nmos.sym} 200 -220 0 0 {name=MclampN15N15
l=0.6u
w=4.4u
ng=1
m=15
model=sg13_hv_nmos
spiceprefix=X
}
C {title.sym} 160 -40 0 0 {name=l1 author="Christoph Maier"}
C {ipin.sym} 140 -220 0 0 {name=p1 lab=gate
}
C {iopin.sym} 140 -140 0 1 {name=p2 lab=iovss
}
C {iopin.sym} 140 -300 0 1 {name=p3 lab=pad
}
