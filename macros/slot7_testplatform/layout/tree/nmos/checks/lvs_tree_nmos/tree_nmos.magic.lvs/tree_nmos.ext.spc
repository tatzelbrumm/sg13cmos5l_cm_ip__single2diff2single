* NGSPICE file created from tree_nmos.ext - technology: ihp-sg13cmos5l

.subckt tree_nmos vss ni vbn vbpc vbp vbnc en_3v3 en_3v3_b iref
X0 ni ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X1 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X2 vbp ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X3 vbnc vbnc vss vss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=8u
X4 ni ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X5 vss ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=33.1561p ps=72.28u w=1.2u l=6u
X6 vbpc ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X7 ni ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X8 ni ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X9 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X10 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X11 vbp ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X12 vbp ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X13 vbp ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X14 vbpc ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X15 ni ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X16 vss ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0 ps=0 w=1.2u l=6u
X17 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X18 vbp ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X19 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X20 iref en_3v3 ni vss sg13_hv_nmos ad=0.34p pd=2.68u as=0.19p ps=1.38u w=1u l=0.45u
X21 ni en_3v3_b vss vss sg13_hv_nmos ad=0.19p pd=1.38u as=0.34p ps=2.68u w=1u l=0.45u
.ends

