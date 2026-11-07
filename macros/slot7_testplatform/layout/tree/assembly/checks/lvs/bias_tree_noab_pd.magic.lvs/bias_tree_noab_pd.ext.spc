* NGSPICE file created from bias_tree_noab_pd.ext - technology: ihp-sg13cmos5l

.subckt bias_tree_noab_pd vdd vss iref vbp en_3v3_b vbpc vbn vbnc en_3v3
X0 tree_pmos_0.ni tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X1 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X2 vbp tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X3 vbp tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X4 tree_pmos_0.ni tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X5 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X6 vdd vbp vbp vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X7 vbnc vbnc vss vss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=8u
X8 vdd vbp vbn vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X9 vbp tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X10 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X11 vdd vbp vbp vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X12 vdd vbp vbn vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X13 tree_pmos_0.ni en_3v3_b iref vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X14 vdd vbp vdd vdd sg13_hv_pmos ad=0.17p pd=1.68u as=48.0442p ps=0.10816m w=0.5u l=6u
X15 vss tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=33.1561p ps=72.28u w=1.2u l=6u
X16 vdd vbpc vbpc vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=4u
X17 vdd vbp vbp vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X18 vdd vbp vbn vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X19 tree_pmos_0.ni en_3v3_b vss vss sg13_hv_nmos ad=0.19p pd=1.38u as=0.34p ps=2.68u w=1u l=0.45u
X20 vbp tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X21 vdd vbp vbp vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X22 vdd vbp vbnc vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X23 tree_pmos_0.ni tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X24 vdd vbp vbn vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X25 vdd vbp vdd vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=6u
X26 vbpc tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X27 iref en_3v3 tree_pmos_0.ni vss sg13_hv_nmos ad=0.34p pd=2.68u as=0.19p ps=1.38u w=1u l=0.45u
X28 vbp tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X29 vdd vbp vdd vdd sg13_hv_pmos ad=0.17p pd=1.68u as=0 ps=0 w=0.5u l=6u
X30 vdd vbp vbn vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X31 vdd vbp vbnc vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X32 vss tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0 ps=0 w=1.2u l=6u
X33 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X34 tree_pmos_0.ni tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X35 vbpc tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X36 vbn vbn vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X37 vdd vbp vbp vdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X38 tree_pmos_0.ni tree_pmos_0.ni vss vss sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
.ends

