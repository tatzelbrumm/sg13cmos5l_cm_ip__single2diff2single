v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {JanteStrømSpejl — 22 explicit devices; no arraying with m or ng} 40 -1010 0 0 0.5 0.5 {}
T {row 6 = diode-connected reference pair; all gates = IREF; sources = S; bodies = B} 40 -985 0 0 0.32 0.32 {}
T {row 01 -> OUT01} 770 -908 0 0 0.24 0.24 {}
T {row 02 -> OUT02} 770 -836 0 0 0.24 0.24 {}
T {row 03 -> OUT03} 770 -764 0 0 0.24 0.24 {}
T {row 04 -> OUT04} 770 -692 0 0 0.24 0.24 {}
T {row 05 -> OUT05} 770 -620 0 0 0.24 0.24 {}
T {+1 / reference pair} 770 -548 0 0 0.28 0.28 {}
T {row 07 -> OUT06} 770 -476 0 0 0.24 0.24 {}
T {row 08 -> OUT07} 770 -404 0 0 0.24 0.24 {}
T {row 09 -> OUT08} 770 -332 0 0 0.24 0.24 {}
T {row 10 -> OUT09} 770 -260 0 0 0.24 0.24 {}
T {row 11 -> OUT10} 770 -188 0 0 0.24 0.24 {}
N 380 -950 380 -930 {lab=OUT01}
N 310 -900 340 -900 {lab=IREF}
N 380 -900 410 -900 {lab=B}
N 720 -950 720 -930 {lab=OUT01}
N 650 -900 680 -900 {lab=IREF}
N 720 -900 750 -900 {lab=B}
N 310 -828 340 -828 {lab=IREF}
N 380 -828 410 -828 {lab=B}
N 650 -828 680 -828 {lab=IREF}
N 720 -828 750 -828 {lab=B}
N 310 -756 340 -756 {lab=IREF}
N 380 -756 410 -756 {lab=B}
N 650 -756 680 -756 {lab=IREF}
N 720 -756 750 -756 {lab=B}
N 310 -684 340 -684 {lab=IREF}
N 380 -684 410 -684 {lab=B}
N 650 -684 680 -684 {lab=IREF}
N 720 -684 750 -684 {lab=B}
N 310 -612 340 -612 {lab=IREF}
N 380 -612 410 -612 {lab=B}
N 650 -612 680 -612 {lab=IREF}
N 720 -612 750 -612 {lab=B}
N 310 -540 340 -540 {lab=IREF}
N 380 -540 410 -540 {lab=B}
N 650 -540 680 -540 {lab=IREF}
N 720 -540 750 -540 {lab=B}
N 310 -468 340 -468 {lab=IREF}
N 380 -468 410 -468 {lab=B}
N 650 -468 680 -468 {lab=IREF}
N 720 -468 750 -468 {lab=B}
N 310 -396 340 -396 {lab=IREF}
N 380 -396 410 -396 {lab=B}
N 650 -396 680 -396 {lab=IREF}
N 720 -396 750 -396 {lab=B}
N 310 -324 340 -324 {lab=IREF}
N 380 -324 410 -324 {lab=B}
N 650 -324 680 -324 {lab=IREF}
N 720 -324 750 -324 {lab=B}
N 310 -252 340 -252 {lab=IREF}
N 380 -252 410 -252 {lab=B}
N 650 -252 680 -252 {lab=IREF}
N 720 -252 750 -252 {lab=B}
N 310 -180 340 -180 {lab=IREF}
N 380 -150 380 -130 {lab=S}
N 380 -180 410 -180 {lab=B}
N 650 -180 680 -180 {lab=IREF}
N 720 -150 720 -130 {lab=S}
N 720 -180 750 -180 {lab=B}
N 380 -878 380 -850 {lab=S}
N 720 -878 720 -850 {lab=S}
N 380 -806 380 -778 {lab=S}
N 720 -806 720 -778 {lab=S}
N 380 -734 380 -706 {lab=S}
N 720 -734 720 -706 {lab=S}
N 380 -662 380 -634 {lab=S}
N 720 -662 720 -634 {lab=S}
N 380 -590 380 -562 {lab=S}
N 720 -590 720 -562 {lab=S}
N 380 -518 380 -490 {lab=S}
N 720 -518 720 -490 {lab=S}
N 380 -446 380 -418 {lab=S}
N 720 -446 720 -418 {lab=S}
N 380 -374 380 -346 {lab=S}
N 720 -374 720 -346 {lab=S}
N 380 -302 380 -274 {lab=S}
N 720 -302 720 -274 {lab=S}
N 380 -230 380 -202 {lab=S}
N 720 -230 720 -202 {lab=S}
C {devices/code_shown.sym} 40 -70 0 0 {name=PARAMS only_toplevel=false
value="
.param lambda=0.08u
.param WJ='4*lambda'
.param LJ='64*lambda'
"}
C {devices/iopin.sym} 70 -930 2 0 {name=pIREF lab=IREF}
C {devices/iopin.sym} 70 -900 2 0 {name=pS lab=S}
C {devices/iopin.sym} 70 -870 2 0 {name=pB lab=B}
C {devices/iopin.sym} 1010 -930 0 0 {name=pOUT01 lab=OUT01}
C {devices/iopin.sym} 1010 -870 0 0 {name=pOUT02 lab=OUT02}
C {devices/iopin.sym} 1010 -810 0 0 {name=pOUT03 lab=OUT03}
C {devices/iopin.sym} 1010 -750 0 0 {name=pOUT04 lab=OUT04}
C {devices/iopin.sym} 1010 -690 0 0 {name=pOUT05 lab=OUT05}
C {devices/iopin.sym} 1010 -630 0 0 {name=pOUT06 lab=OUT06}
C {devices/iopin.sym} 1010 -570 0 0 {name=pOUT07 lab=OUT07}
C {devices/iopin.sym} 1010 -510 0 0 {name=pOUT08 lab=OUT08}
C {devices/iopin.sym} 1010 -450 0 0 {name=pOUT09 lab=OUT09}
C {devices/iopin.sym} 1010 -390 0 0 {name=pOUT10 lab=OUT10}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -900 0 0 {name=M_L01
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -900 0 0 {name=M_R01
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -828 0 0 {name=M_L02
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -828 0 0 {name=M_R02
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -756 0 0 {name=M_L03
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -756 0 0 {name=M_R03
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -684 0 0 {name=M_L04
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -684 0 0 {name=M_R04
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -612 0 0 {name=M_L05
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -612 0 0 {name=M_R05
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -540 0 0 {name=M_L06
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -540 0 0 {name=M_R06
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -468 0 0 {name=M_L07
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -468 0 0 {name=M_R07
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -396 0 0 {name=M_L08
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -396 0 0 {name=M_R08
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -324 0 0 {name=M_L09
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -324 0 0 {name=M_R09
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -252 0 0 {name=M_L10
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -252 0 0 {name=M_R10
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -180 0 0 {name=M_L11
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -180 0 0 {name=M_R11
l=LJ
w=WJ
ng=1
m=1
mm_ok=1
model=sg13_lv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} 380 -950 1 0 {name=lDL01 sig_type=std_logic lab=OUT01}
C {devices/lab_pin.sym} 310 -900 0 0 {name=lGL01 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -850 3 0 {name=lSL01 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -900 2 0 {name=lBL01 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -950 1 0 {name=lDR01 sig_type=std_logic lab=OUT01}
C {devices/lab_pin.sym} 650 -900 0 0 {name=lGR01 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -850 3 0 {name=lSR01 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -900 2 0 {name=lBR01 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -878 1 0 {name=lDL02 sig_type=std_logic lab=OUT02}
C {devices/lab_pin.sym} 310 -828 0 0 {name=lGL02 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -778 3 0 {name=lSL02 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -828 2 0 {name=lBL02 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -878 1 0 {name=lDR02 sig_type=std_logic lab=OUT02}
C {devices/lab_pin.sym} 650 -828 0 0 {name=lGR02 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -778 3 0 {name=lSR02 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -828 2 0 {name=lBR02 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -806 1 0 {name=lDL03 sig_type=std_logic lab=OUT03}
C {devices/lab_pin.sym} 310 -756 0 0 {name=lGL03 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -706 3 0 {name=lSL03 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -756 2 0 {name=lBL03 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -806 1 0 {name=lDR03 sig_type=std_logic lab=OUT03}
C {devices/lab_pin.sym} 650 -756 0 0 {name=lGR03 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -706 3 0 {name=lSR03 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -756 2 0 {name=lBR03 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -734 1 0 {name=lDL04 sig_type=std_logic lab=OUT04}
C {devices/lab_pin.sym} 310 -684 0 0 {name=lGL04 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -634 3 0 {name=lSL04 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -684 2 0 {name=lBL04 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -734 1 0 {name=lDR04 sig_type=std_logic lab=OUT04}
C {devices/lab_pin.sym} 650 -684 0 0 {name=lGR04 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -634 3 0 {name=lSR04 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -684 2 0 {name=lBR04 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -662 1 0 {name=lDL05 sig_type=std_logic lab=OUT05}
C {devices/lab_pin.sym} 310 -612 0 0 {name=lGL05 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -562 3 0 {name=lSL05 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -612 2 0 {name=lBL05 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -662 1 0 {name=lDR05 sig_type=std_logic lab=OUT05}
C {devices/lab_pin.sym} 650 -612 0 0 {name=lGR05 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -562 3 0 {name=lSR05 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -612 2 0 {name=lBR05 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -590 1 0 {name=lDL06 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 310 -540 0 0 {name=lGL06 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -490 3 0 {name=lSL06 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -540 2 0 {name=lBL06 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -590 1 0 {name=lDR06 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 650 -540 0 0 {name=lGR06 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -490 3 0 {name=lSR06 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -540 2 0 {name=lBR06 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -518 1 0 {name=lDL07 sig_type=std_logic lab=OUT06}
C {devices/lab_pin.sym} 310 -468 0 0 {name=lGL07 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -418 3 0 {name=lSL07 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -468 2 0 {name=lBL07 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -518 1 0 {name=lDR07 sig_type=std_logic lab=OUT06}
C {devices/lab_pin.sym} 650 -468 0 0 {name=lGR07 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -418 3 0 {name=lSR07 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -468 2 0 {name=lBR07 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -446 1 0 {name=lDL08 sig_type=std_logic lab=OUT07}
C {devices/lab_pin.sym} 310 -396 0 0 {name=lGL08 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -346 3 0 {name=lSL08 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -396 2 0 {name=lBL08 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -446 1 0 {name=lDR08 sig_type=std_logic lab=OUT07}
C {devices/lab_pin.sym} 650 -396 0 0 {name=lGR08 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -346 3 0 {name=lSR08 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -396 2 0 {name=lBR08 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -374 1 0 {name=lDL09 sig_type=std_logic lab=OUT08}
C {devices/lab_pin.sym} 310 -324 0 0 {name=lGL09 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -274 3 0 {name=lSL09 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -324 2 0 {name=lBL09 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -374 1 0 {name=lDR09 sig_type=std_logic lab=OUT08}
C {devices/lab_pin.sym} 650 -324 0 0 {name=lGR09 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -274 3 0 {name=lSR09 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -324 2 0 {name=lBR09 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -302 1 0 {name=lDL10 sig_type=std_logic lab=OUT09}
C {devices/lab_pin.sym} 310 -252 0 0 {name=lGL10 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -202 3 0 {name=lSL10 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -252 2 0 {name=lBL10 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -302 1 0 {name=lDR10 sig_type=std_logic lab=OUT09}
C {devices/lab_pin.sym} 650 -252 0 0 {name=lGR10 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -202 3 0 {name=lSR10 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -252 2 0 {name=lBR10 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 380 -230 1 0 {name=lDL11 sig_type=std_logic lab=OUT10}
C {devices/lab_pin.sym} 310 -180 0 0 {name=lGL11 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 380 -130 3 0 {name=lSL11 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 410 -180 2 0 {name=lBL11 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 720 -230 1 0 {name=lDR11 sig_type=std_logic lab=OUT10}
C {devices/lab_pin.sym} 650 -180 0 0 {name=lGR11 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 720 -130 3 0 {name=lSR11 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 750 -180 2 0 {name=lBR11 sig_type=std_logic lab=B}
