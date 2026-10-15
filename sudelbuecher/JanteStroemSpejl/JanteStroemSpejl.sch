v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {JanteStrømSpejl — 22 explicit devices; no arraying with m or ng} 40 -1010 0 0 0.5 0.5 {}
T {row 6 = diode-connected reference pair; all gates = IREF; sources = S; bodies = B} 40 -985 0 0 0.32 0.32 {}
T {row 01 -> OUT01} 790 -908 0 0 0.24 0.24 {}
T {row 02 -> OUT02} 790 -836 0 0 0.24 0.24 {}
T {row 03 -> OUT03} 790 -764 0 0 0.24 0.24 {}
T {row 04 -> OUT04} 790 -692 0 0 0.24 0.24 {}
T {row 05 -> OUT05} 790 -620 0 0 0.24 0.24 {}
T {+1 / reference pair} 790 -548 0 0 0.28 0.28 {}
T {row 07 -> OUT06} 790 -476 0 0 0.24 0.24 {}
T {row 08 -> OUT07} 790 -404 0 0 0.24 0.24 {}
T {row 09 -> OUT08} 790 -332 0 0 0.24 0.24 {}
T {row 10 -> OUT09} 790 -260 0 0 0.24 0.24 {}
T {row 11 -> OUT10} 790 -188 0 0 0.24 0.24 {}
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
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -900 0 0 {name=M_R01
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -930 1 0 {name=lDL01 sig_type=std_logic lab=OUT01}
C {devices/lab_pin.sym} 700 -930 1 0 {name=lDR01 sig_type=std_logic lab=OUT01}
C {devices/lab_pin.sym} 330 -900 0 0 {name=lGL01 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -900 0 0 {name=lGR01 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -870 3 0 {name=lSL01 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -870 3 0 {name=lSR01 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -900 2 0 {name=lBL01 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -900 2 0 {name=lBR01 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -828 0 0 {name=M_L02
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -828 0 0 {name=M_R02
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -858 1 0 {name=lDL02 sig_type=std_logic lab=OUT02}
C {devices/lab_pin.sym} 700 -858 1 0 {name=lDR02 sig_type=std_logic lab=OUT02}
C {devices/lab_pin.sym} 330 -828 0 0 {name=lGL02 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -828 0 0 {name=lGR02 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -798 3 0 {name=lSL02 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -798 3 0 {name=lSR02 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -828 2 0 {name=lBL02 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -828 2 0 {name=lBR02 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -756 0 0 {name=M_L03
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -756 0 0 {name=M_R03
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -786 1 0 {name=lDL03 sig_type=std_logic lab=OUT03}
C {devices/lab_pin.sym} 700 -786 1 0 {name=lDR03 sig_type=std_logic lab=OUT03}
C {devices/lab_pin.sym} 330 -756 0 0 {name=lGL03 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -756 0 0 {name=lGR03 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -726 3 0 {name=lSL03 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -726 3 0 {name=lSR03 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -756 2 0 {name=lBL03 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -756 2 0 {name=lBR03 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -684 0 0 {name=M_L04
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -684 0 0 {name=M_R04
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -714 1 0 {name=lDL04 sig_type=std_logic lab=OUT04}
C {devices/lab_pin.sym} 700 -714 1 0 {name=lDR04 sig_type=std_logic lab=OUT04}
C {devices/lab_pin.sym} 330 -684 0 0 {name=lGL04 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -684 0 0 {name=lGR04 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -654 3 0 {name=lSL04 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -654 3 0 {name=lSR04 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -684 2 0 {name=lBL04 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -684 2 0 {name=lBR04 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -612 0 0 {name=M_L05
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -612 0 0 {name=M_R05
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -642 1 0 {name=lDL05 sig_type=std_logic lab=OUT05}
C {devices/lab_pin.sym} 700 -642 1 0 {name=lDR05 sig_type=std_logic lab=OUT05}
C {devices/lab_pin.sym} 330 -612 0 0 {name=lGL05 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -612 0 0 {name=lGR05 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -582 3 0 {name=lSL05 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -582 3 0 {name=lSR05 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -612 2 0 {name=lBL05 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -612 2 0 {name=lBR05 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -540 0 0 {name=M_L06
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -540 0 0 {name=M_R06
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -570 1 0 {name=lDL06 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 700 -570 1 0 {name=lDR06 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 330 -540 0 0 {name=lGL06 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -540 0 0 {name=lGR06 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -510 3 0 {name=lSL06 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -510 3 0 {name=lSR06 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -540 2 0 {name=lBL06 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -540 2 0 {name=lBR06 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -468 0 0 {name=M_L07
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -468 0 0 {name=M_R07
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -498 1 0 {name=lDL07 sig_type=std_logic lab=OUT06}
C {devices/lab_pin.sym} 700 -498 1 0 {name=lDR07 sig_type=std_logic lab=OUT06}
C {devices/lab_pin.sym} 330 -468 0 0 {name=lGL07 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -468 0 0 {name=lGR07 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -438 3 0 {name=lSL07 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -438 3 0 {name=lSR07 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -468 2 0 {name=lBL07 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -468 2 0 {name=lBR07 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -396 0 0 {name=M_L08
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -396 0 0 {name=M_R08
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -426 1 0 {name=lDL08 sig_type=std_logic lab=OUT07}
C {devices/lab_pin.sym} 700 -426 1 0 {name=lDR08 sig_type=std_logic lab=OUT07}
C {devices/lab_pin.sym} 330 -396 0 0 {name=lGL08 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -396 0 0 {name=lGR08 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -366 3 0 {name=lSL08 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -366 3 0 {name=lSR08 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -396 2 0 {name=lBL08 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -396 2 0 {name=lBR08 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -324 0 0 {name=M_L09
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -324 0 0 {name=M_R09
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -354 1 0 {name=lDL09 sig_type=std_logic lab=OUT08}
C {devices/lab_pin.sym} 700 -354 1 0 {name=lDR09 sig_type=std_logic lab=OUT08}
C {devices/lab_pin.sym} 330 -324 0 0 {name=lGL09 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -324 0 0 {name=lGR09 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -294 3 0 {name=lSL09 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -294 3 0 {name=lSR09 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -324 2 0 {name=lBL09 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -324 2 0 {name=lBR09 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -252 0 0 {name=M_L10
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -252 0 0 {name=M_R10
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -282 1 0 {name=lDL10 sig_type=std_logic lab=OUT09}
C {devices/lab_pin.sym} 700 -282 1 0 {name=lDR10 sig_type=std_logic lab=OUT09}
C {devices/lab_pin.sym} 330 -252 0 0 {name=lGL10 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -252 0 0 {name=lGR10 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -222 3 0 {name=lSL10 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -222 3 0 {name=lSR10 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -252 2 0 {name=lBL10 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -252 2 0 {name=lBR10 sig_type=std_logic lab=B}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -180 0 0 {name=M_L11
l=LJ w=WJ}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -180 0 0 {name=M_R11
l=LJ w=WJ}
C {devices/lab_pin.sym} 360 -210 1 0 {name=lDL11 sig_type=std_logic lab=OUT10}
C {devices/lab_pin.sym} 700 -210 1 0 {name=lDR11 sig_type=std_logic lab=OUT10}
C {devices/lab_pin.sym} 330 -180 0 0 {name=lGL11 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 670 -180 0 0 {name=lGR11 sig_type=std_logic lab=IREF}
C {devices/lab_pin.sym} 360 -150 3 0 {name=lSL11 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 700 -150 3 0 {name=lSR11 sig_type=std_logic lab=S}
C {devices/lab_pin.sym} 390 -180 2 0 {name=lBL11 sig_type=std_logic lab=B}
C {devices/lab_pin.sym} 730 -180 2 0 {name=lBR11 sig_type=std_logic lab=B}
