* NGSPICE file created from sg13cmos5l_IOPadSingle2Diff.ext - technology: ihp-sg13cmos5l

.subckt sg13cmos5l_IOPadSingle2Diff vref outp outn vcm en_3v3 en_3v3_b iref pad vdd
+ iovss iovdd
X0 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=0.65663n ps=2.66142m w=5u l=6u
X1 iovss iovss iovss rhigh l=12.65u w=0.5u
X2 s2d_block_0.s2d_loads_f_0.ln s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X3 s2d_block_0.s2d_loads_f_0.ln s2d_block_0.s2d_casc_p_f_0.vbpc outn iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X4 s2d_block_0.s2d_tails_hi_f_0.sa_A2 a_14374_25646# iovss rhigh l=12.65u w=0.5u
X5 s2d_block_0.s2d_casc_n_f_0.xc s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X6 iovdd s2d_block_0.s2d_casc_n_f_0.vbnc s2d_block_0.s2d_casc_n_f_0.yc iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X7 Clamp_P_M1_0.gate iovdd iovss rppd l=12.9u w=0.5u
X8 s2d_block_0.s2d_loads_f_0.ln s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X9 s2d_block_0.s2d_casc_p_f_0.vbpc s2d_block_0.bias_tree_noab_n_c3_0.ni iovss iovss sg13_hv_nmos ad=0.816p pd=5.48u as=0.816p ps=5.48u w=2.4u l=6u
X10 a_11758_27006# a_14374_25510# iovss rhigh l=12.65u w=0.5u
X11 s2d_block_0.s2d_tails_lo_f_0.sa_F1 vcm s2d_block_0.s2d_casc_n_f_0.y s2d_block_0.s2d_tails_lo_f_0.sa_F1 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X12 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0.75674n ps=2.78086m w=2u l=6u
X13 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X14 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.xc iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X15 s2d_block_0.bias_tree_noab_n_c3_0.ni en_3v3_b iovss iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X16 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X17 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=0 ps=0 w=6u l=6u
X18 s2d_block_0.s2d_casc_n_f_0.x s2d_block_0.s2d_casc_n_f_0.vbnc outp iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X19 s2d_block_0.s2d_casc_n_f_0.x vref s2d_block_0.s2d_tails_lo_f_0.sb_A2 s2d_block_0.s2d_tails_lo_f_0.sb_A2 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X20 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X21 s2d_block_0.s2d_tails_hi_f_0.sb_F1 outp s2d_block_0.s2d_casc_n_f_0.x s2d_block_0.s2d_tails_hi_f_0.sb_F1 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X22 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=1.9p pd=10.38u as=0 ps=0 w=10u l=1u
X23 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=0 ps=0 w=5u l=6u
X24 s2d_block_0.s2d_casc_n_f_0.y s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X25 s2d_block_0.s2d_tails_lo_f_0.sb_A2 a_14374_27278# iovss rhigh l=12.65u w=0.5u
X26 iovdd s2d_block_0.s2d_loads_f_0.vcmfb s2d_block_0.s2d_loads_f_0.dd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X27 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X28 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=2.068p ps=9.74u w=4.4u l=0.6u
X29 iovdd s2d_block_0.s2d_loads_f_0.vcmfb s2d_block_0.s2d_loads_f_0.lp iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X30 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X31 vcm en_3v3_b outp iovss sg13_hv_nmos ad=0.19p pd=1.38u as=0.34p ps=2.68u w=1u l=0.45u
X32 s2d_block_0.s2d_tails_lo_f_0.sa_F1 a_14374_25782# iovss rhigh l=12.65u w=0.5u
X33 a_11758_27006# a_14374_27142# iovss rhigh l=12.65u w=0.5u
X34 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=3.4p pd=20.68u as=0 ps=0 w=10u l=1u
X35 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X36 s2d_block_0.s2d_loads_f_0.lp s2d_block_0.s2d_casc_p_f_0.vbpc outp iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X37 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp s2d_block_0.s2d_tails_hi_f_0.sa_M1 iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X38 s2d_block_0.s2d_casc_n_f_0.y s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X39 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X40 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X41 iref en_3v3 s2d_block_0.bias_tree_noab_n_c3_0.ni iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X42 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X43 pad iovdd dpantenna l=1.26u w=27.78u
X44 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X45 s2d_block_0.s2d_casc_n_f_0.x vcm s2d_block_0.s2d_tails_hi_f_0.sb_F2 s2d_block_0.s2d_tails_hi_f_0.sb_F2 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X46 s2d_block_0.s2d_tails_hi_f_0.sa_A1 a_14374_25510# iovss rhigh l=12.65u w=0.5u
X47 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.y iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X48 s2d_block_0.s2d_tails_hi_f_0.sb_F1 a_14374_27414# iovss rhigh l=12.65u w=0.5u
X49 s2d_block_0.s2d_tails_lo_f_0.sa_F2 outn s2d_block_0.s2d_casc_n_f_0.y s2d_block_0.s2d_tails_lo_f_0.sa_F2 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X50 iovss s2d_block_0.bias_tree_noab_n_c3_0.ni iovss iovss sg13_hv_nmos ad=0.816p pd=5.48u as=0 ps=0 w=2.4u l=6u
X51 s2d_block_0.s2d_casc_n_f_0.y s2d_block_0.s2d_casc_n_f_0.vbnc outn iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X52 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X53 iovss s2d_block_0.s2d_casc_n_f_0.vbnc iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=3u
X54 iovss pad dantenna l=1.26u w=27.78u
X55 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X56 vcm en_3v3 outp iovdd sg13_hv_pmos ad=0.19p pd=1.38u as=0.34p ps=2.68u w=1u l=0.45u
X57 outn en_3v3 vcm iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.19p ps=1.38u w=1u l=0.45u
X58 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp s2d_block_0.s2d_tails_hi_f_0.sb_M2 iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X59 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.y iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X60 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X61 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp s2d_block_0.s2d_tails_hi_f_0.sb_F1 iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X62 iovdd s2d_block_0.s2d_loads_f_0.vcmfb s2d_block_0.s2d_loads_f_0.lp iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X63 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X64 a_11758_26734# a_14374_25782# iovss rhigh l=12.65u w=0.5u
X65 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X66 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X67 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X68 s2d_block_0.s2d_tails_hi_f_0.sb_M2 vcm s2d_block_0.s2d_casc_n_f_0.xc s2d_block_0.s2d_tails_hi_f_0.sb_M2 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X69 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X70 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X71 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X72 iovss iovss iovss rhigh l=12.65u w=0.5u
X73 s2d_block_0.s2d_casc_n_f_0.yc s2d_block_0.s2d_casc_n_f_0.vbnc iovdd iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X74 iovdd s2d_block_0.s2d_casc_p_f_0.vbpc iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X75 s2d_block_0.s2d_casc_n_f_0.yc outp s2d_block_0.s2d_tails_hi_f_0.sa_M1 s2d_block_0.s2d_tails_hi_f_0.sa_M1 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X76 s2d_block_0.s2d_casc_n_f_0.y vcm s2d_block_0.s2d_tails_lo_f_0.sa_F1 s2d_block_0.s2d_tails_lo_f_0.sa_F1 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X77 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp s2d_block_0.s2d_tails_hi_f_0.sa_A2 iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X78 s2d_block_0.s2d_tails_hi_f_0.sa_A2 pad s2d_block_0.s2d_casc_n_f_0.y s2d_block_0.s2d_tails_hi_f_0.sa_A2 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X79 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.yc iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X80 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X81 s2d_block_0.s2d_tails_hi_f_0.sb_M2 a_14374_27822# iovss rhigh l=12.65u w=0.5u
X82 s2d_block_0.s2d_casc_n_f_0.yc s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X83 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.y iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X84 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp s2d_block_0.s2d_tails_hi_f_0.sa_A1 iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X85 a_11758_26870# a_14374_25646# iovss rhigh l=12.65u w=0.5u
X86 s2d_block_0.s2d_casc_n_f_0.vbnc s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=6u
X87 s2d_block_0.s2d_tails_hi_f_0.sb_F2 a_14374_27550# iovss rhigh l=12.65u w=0.5u
X88 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=0 ps=0 w=5u l=6u
X89 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X90 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X91 a_11758_26598# a_14374_25918# iovss rhigh l=12.65u w=0.5u
X92 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.x iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X93 s2d_block_0.s2d_loads_f_0.dd s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X94 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X95 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X96 iovdd s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X97 pad iovdd dpantenna l=1.26u w=27.78u
X98 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X99 iovdd s2d_block_0.s2d_loads_f_0.vcmfb s2d_block_0.s2d_loads_f_0.ln iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X100 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=2.068p pd=9.74u as=2.596p ps=5.58u w=4.4u l=0.6u
X101 s2d_block_0.s2d_loads_f_0.lp s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X102 iovdd s2d_block_0.s2d_loads_f_0.vcmfb s2d_block_0.s2d_loads_f_0.ln iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X103 iovdd s2d_block_0.s2d_casc_p_f_0.vbpc iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X104 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X105 s2d_block_0.s2d_tails_lo_f_0.sa_M2 outn s2d_block_0.s2d_casc_n_f_0.yc s2d_block_0.s2d_tails_lo_f_0.sa_M2 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X106 iovdd s2d_block_0.s2d_casc_p_f_0.vbpc s2d_block_0.s2d_casc_p_f_0.vbpc iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=4u
X107 iovdd s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X108 s2d_block_0.s2d_casc_n_f_0.y s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X109 iovss outp iovss iovss sg13_hv_nmos ad=4.08p pd=24.68u as=0 ps=0 w=12u l=12u
X110 iovss outn iovss iovss sg13_hv_nmos ad=4.08p pd=24.68u as=0 ps=0 w=12u l=12u
X111 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp s2d_block_0.s2d_tails_hi_f_0.sb_F2 iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X112 s2d_block_0.s2d_casc_n_f_0.x outp s2d_block_0.s2d_tails_hi_f_0.sb_F1 s2d_block_0.s2d_tails_hi_f_0.sb_F1 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X113 s2d_block_0.s2d_casc_n_f_0.xc vcm s2d_block_0.s2d_tails_lo_f_0.sb_M1 s2d_block_0.s2d_tails_lo_f_0.sb_M1 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X114 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X115 iovdd s2d_block_0.s2d_casc_p_f_0.vbpc iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X116 a_11758_26326# a_14374_26190# iovss rhigh l=12.65u w=0.5u
X117 s2d_block_0.s2d_tails_lo_f_0.sb_A1 vref s2d_block_0.s2d_casc_n_f_0.x s2d_block_0.s2d_tails_lo_f_0.sb_A1 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X118 s2d_block_0.s2d_casc_n_f_0.x s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X119 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X120 s2d_block_0.s2d_tails_lo_f_0.sb_M1 a_14374_27686# iovss rhigh l=12.65u w=0.5u
X121 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X122 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X123 s2d_block_0.s2d_tails_hi_f_0.sa_A1 pad s2d_block_0.s2d_casc_n_f_0.y s2d_block_0.s2d_tails_hi_f_0.sa_A1 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X124 s2d_block_0.s2d_tails_lo_f_0.sb_M1 s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X125 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X126 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=3.4p pd=20.68u as=0 ps=0 w=10u l=1u
X127 a_11758_26326# a_14374_27822# iovss rhigh l=12.65u w=0.5u
X128 s2d_block_0.s2d_casc_n_f_0.xc s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X129 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X130 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X131 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X132 s2d_block_0.bias_tree_noab_n_c3_0.ni en_3v3_b iref iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X133 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=3.1302p ps=14.26u w=6.66u l=0.6u
X134 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X135 a_11758_26462# a_14374_26054# iovss rhigh l=12.65u w=0.5u
X136 s2d_block_0.s2d_loads_f_0.dd s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X137 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X138 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=1.9p pd=10.38u as=0 ps=0 w=10u l=1u
X139 s2d_block_0.s2d_loads_f_0.vcmfb s2d_block_0.s2d_casc_p_f_0.vbpc s2d_block_0.s2d_loads_f_0.dd iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X140 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp s2d_block_0.s2d_tails_hi_f_0.vbp iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X141 s2d_block_0.bias_tree_noab_n_c3_0.ni s2d_block_0.bias_tree_noab_n_c3_0.ni iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X142 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X143 s2d_block_0.s2d_tails_lo_f_0.sa_M2 s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X144 outn s2d_block_0.s2d_casc_n_f_0.vbnc s2d_block_0.s2d_casc_n_f_0.y iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X145 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X146 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X147 s2d_block_0.s2d_casc_n_f_0.yc s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X148 s2d_block_0.s2d_casc_n_f_0.xc vcm s2d_block_0.s2d_tails_hi_f_0.sb_M2 s2d_block_0.s2d_tails_hi_f_0.sb_M2 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X149 s2d_block_0.s2d_casc_n_f_0.y outn s2d_block_0.s2d_tails_lo_f_0.sa_F2 s2d_block_0.s2d_tails_lo_f_0.sa_F2 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X150 s2d_block_0.s2d_tails_hi_f_0.sa_M1 outp s2d_block_0.s2d_casc_n_f_0.yc s2d_block_0.s2d_tails_hi_f_0.sa_M1 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X151 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X152 s2d_block_0.s2d_tails_lo_f_0.sa_F2 a_14374_25918# iovss rhigh l=12.65u w=0.5u
X153 s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X154 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X155 iovss s2d_block_0.s2d_casc_n_f_0.vbnc iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=3u
X156 s2d_block_0.s2d_tails_lo_f_0.sa_F2 s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X157 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X158 s2d_block_0.s2d_tails_lo_f_0.sb_A2 vref s2d_block_0.s2d_casc_n_f_0.x s2d_block_0.s2d_tails_lo_f_0.sb_A2 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X159 pad Clamp_N_M1_0.gate iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=0.6u
X160 a_11758_26462# a_14374_27686# iovss rhigh l=12.65u w=0.5u
X161 s2d_block_0.s2d_casc_n_f_0.x s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X162 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X163 s2d_block_0.s2d_tails_hi_f_0.vbp s2d_block_0.bias_tree_noab_n_c3_0.ni iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X164 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=3.1302p ps=14.26u w=6.66u l=0.6u
X165 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=3.4p pd=20.68u as=0 ps=0 w=10u l=1u
X166 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.xc iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X167 Clamp_N_M1_0.gate iovss iovss rppd l=3.54u w=0.5u
X168 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X169 iovss s2d_block_0.s2d_casc_n_f_0.vbnc iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=3u
X170 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=1.9p pd=10.38u as=0 ps=0 w=10u l=1u
X171 s2d_block_0.s2d_tails_lo_f_0.sb_A1 s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X172 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X173 a_11758_26734# a_14374_27414# iovss rhigh l=12.65u w=0.5u
X174 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X175 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X176 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=3.1302p pd=14.26u as=3.9294p ps=7.84u w=6.66u l=0.6u
X177 outn s2d_block_0.s2d_casc_p_f_0.vbpc s2d_block_0.s2d_loads_f_0.ln iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X178 s2d_block_0.s2d_casc_n_f_0.y pad s2d_block_0.s2d_tails_hi_f_0.sa_A2 s2d_block_0.s2d_tails_hi_f_0.sa_A2 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X179 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X180 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X181 s2d_block_0.s2d_casc_n_f_0.yc outn s2d_block_0.s2d_tails_lo_f_0.sa_M2 s2d_block_0.s2d_tails_lo_f_0.sa_M2 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X182 s2d_block_0.s2d_tails_lo_f_0.sb_A2 s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X183 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.x iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X184 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X185 s2d_block_0.s2d_loads_f_0.lp s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X186 s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X187 s2d_block_0.s2d_tails_lo_f_0.sb_M1 vcm s2d_block_0.s2d_casc_n_f_0.xc s2d_block_0.s2d_tails_lo_f_0.sb_M1 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X188 outp s2d_block_0.s2d_casc_n_f_0.vbnc s2d_block_0.s2d_casc_n_f_0.x iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X189 s2d_block_0.s2d_tails_hi_f_0.sa_M1 a_14374_26054# iovss rhigh l=12.65u w=0.5u
X190 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X191 iovss s2d_block_0.s2d_casc_n_f_0.vbnc iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=3u
X192 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.x iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X193 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X194 iovdd s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X195 outn en_3v3_b vcm iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.19p ps=1.38u w=1u l=0.45u
X196 s2d_block_0.s2d_tails_hi_f_0.sb_F2 vcm s2d_block_0.s2d_casc_n_f_0.x s2d_block_0.s2d_tails_hi_f_0.sb_F2 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X197 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X198 s2d_block_0.s2d_casc_n_f_0.x s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X199 s2d_block_0.s2d_casc_n_f_0.y pad s2d_block_0.s2d_tails_hi_f_0.sa_A1 s2d_block_0.s2d_tails_hi_f_0.sa_A1 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X200 s2d_block_0.s2d_tails_lo_f_0.sb_A1 a_14374_27142# iovss rhigh l=12.65u w=0.5u
X201 iovdd s2d_block_0.s2d_loads_f_0.vcmfb s2d_block_0.s2d_loads_f_0.dd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X202 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=1.9p pd=10.38u as=0 ps=0 w=10u l=1u
X203 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X204 iovdd s2d_block_0.s2d_loads_f_0.vcmfb iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X205 a_11758_26598# a_14374_27550# iovss rhigh l=12.65u w=0.5u
X206 s2d_block_0.s2d_casc_n_f_0.xc s2d_block_0.s2d_casc_n_f_0.vbnc s2d_block_0.s2d_loads_f_0.vcmfb iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X207 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X208 s2d_block_0.s2d_tails_lo_f_0.sa_F1 s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X209 iovdd Clamp_P_M1_0.gate pad iovdd sg13_hv_pmos ad=3.1302p pd=14.26u as=3.9294p ps=7.84u w=6.66u l=0.6u
X210 outp s2d_block_0.s2d_casc_p_f_0.vbpc s2d_block_0.s2d_loads_f_0.lp iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X211 iovdd s2d_block_0.s2d_tails_hi_f_0.vbp iovdd iovdd sg13_hv_pmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X212 a_11758_26870# a_14374_27278# iovss rhigh l=12.65u w=0.5u
X213 s2d_block_0.s2d_casc_n_f_0.vbnc s2d_block_0.s2d_casc_n_f_0.vbnc iovss iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=8u
X214 pad Clamp_P_M1_0.gate iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X215 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn s2d_block_0.s2d_casc_n_f_0.yc iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X216 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X217 s2d_block_0.s2d_tails_lo_f_0.sa_M2 a_14374_26190# iovss rhigh l=12.65u w=0.5u
X218 s2d_block_0.s2d_loads_f_0.vcmfb s2d_block_0.s2d_casc_n_f_0.vbnc s2d_block_0.s2d_casc_n_f_0.xc iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X219 iovss pad dantenna l=1.26u w=27.78u
X220 s2d_block_0.s2d_loads_f_0.dd s2d_block_0.s2d_casc_p_f_0.vbpc s2d_block_0.s2d_loads_f_0.vcmfb iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X221 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=3.4p pd=20.68u as=0 ps=0 w=10u l=1u
X222 s2d_block_0.s2d_casc_n_f_0.x vref s2d_block_0.s2d_tails_lo_f_0.sb_A1 s2d_block_0.s2d_tails_lo_f_0.sb_A1 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X223 iovss Clamp_N_M1_0.gate pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=0.6u
X224 iovss s2d_block_0.sinks_6x6_s2d_c3_core_0.vbn iovss iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
.ends

