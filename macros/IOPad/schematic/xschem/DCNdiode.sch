v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 200 -160 200 -140 {lab=anode}
N 140 -140 200 -140 {lab=anode}
N 140 -240 200 -240 {lab=cathode}
N 200 -240 200 -220 {lab=cathode}
C {title.sym} 160 -40 0 0 {name=l1 author="Christoph Maier"}
C {iopin.sym} 140 -240 0 1 {name=p2 lab=cathode
}
C {iopin.sym} 140 -140 0 1 {name=p1 lab=anode
}
C {sg13g2_pr/dantenna.sym} 200 -190 0 0 {name=D1
model=dantenna
l=1.26u
w=27.78u
m=2
spiceprefix=X
}
