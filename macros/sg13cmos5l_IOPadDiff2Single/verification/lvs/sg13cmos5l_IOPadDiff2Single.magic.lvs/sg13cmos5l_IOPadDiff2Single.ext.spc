* NGSPICE file created from sg13cmos5l_IOPadDiff2Single.ext - technology: ihp-sg13cmos5l

.subckt sg13cmos5l_IOPadDiff2Single pad
X0 iovdd d2s_block_0.bias_tree_n_f2_0.vbpc iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.90339n ps=3.59803m w=1u l=4u
X1 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X2 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X3 d2s_block_0.d2s_sp2k_f2_1.core d2s_cma_0.a d2s_block_0.d2s_sp2k_f2_1.core d2s_block_0.d2s_sp2k_f2_1.core sg13_hv_pmos ad=2.7064p pd=16.6u as=40.5004p ps=0.1292m w=7.96u l=32.16u
X4 d2s_block_0.bias_tree_n_f2_0.ni en_3v3_b iref iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X5 iovss pad dantenna l=1.26u w=67.6u
X6 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X7 d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn iovss sg13_hv_nmos ad=0.68p pd=4.68u as=31.08205p ps=0.23533m w=2u l=6u
X8 iovss en_3v3_b Clamp_N_M1_wiring_0.b iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X9 d2s_block_0.d2s_sp2k_f2_0.core pad iovss rppd l=7.435u w=1u
X10 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X11 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X12 iovss d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.d2s_casc_n_f2_0.y iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X13 d2s_block_0.d2s_ab_n_f2_0.l1 d2s_block_0.bias_tree_n_f2_0.vabp d2s_block_0.d2s_ab_n_f2_0.l2 iovdd sg13_hv_pmos ad=2.2644p pd=14u as=2.2644p ps=14u w=6.66u l=0.6u
X14 d2s_block_0.d2s_ab_n_f2_0.l1 d2s_block_0.d2s_ab_n_f2_0.vabn d2s_block_0.d2s_ab_n_f2_0.l2 iovss sg13_hv_nmos ad=1.496p pd=9.48u as=1.496p ps=9.48u w=4.4u l=1u
X15 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X16 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X17 d2s_block_0.d2s_casc_n_f2_0.y vref d2s_block_0.d2s_rhigh_f2_0.sa_C2 d2s_block_0.d2s_rhigh_f2_0.sa_C2 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X18 iovss d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.d2s_casc_n_f2_0.x iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X19 iovdd d2s_block_0.d2s_ab_n_f2_0.l2 d2s_block_0.d2s_casc_p_c2_0.pr iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X20 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X21 pad iovdd dpantenna l=1.26u w=65.8u
X22 iovss d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=8u
X23 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=4.9284p pd=14.8u as=2.1312p ps=7.3u w=6.66u l=0.6u
X24 d2s_block_0.d2s_casc_n_f2_0.x pad d2s_block_0.d2s_rhigh_f2_0.sb_C2 d2s_block_0.d2s_rhigh_f2_0.sb_C2 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X25 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X26 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X27 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X28 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X29 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X30 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X31 d2s_block_0.d2s_casc_p_c2_0.pr d2s_block_0.bias_tree_n_f2_0.vbpc d2s_cma_0.a iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X32 d2s_block_0.d2s_casc_p_c2_0.pl d2s_block_0.d2s_ab_n_f2_0.l2 iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X33 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X34 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X35 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X36 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X37 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X38 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X39 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X40 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X41 iovdd d2s_block_0.d2s_ab_n_f2_0.l2 d2s_block_0.d2s_casc_p_c2_0.pr iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X42 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X43 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X44 iovdd d2s_block_0.bias_tree_n_f2_0.vbp d2s_block_0.d2s_ab_n_f2_0.vabn iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X45 a_10598_32196# a_10462_29580# iovss rhigh l=12.65u w=0.5u
X46 iovdd d2s_block_0.bias_tree_n_f2_0.vbpc d2s_block_0.bias_tree_n_f2_0.vbpc iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=4u
X47 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X48 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X49 iovss d2s_block_0.bias_tree_n_f2_0.ni d2s_block_0.bias_tree_n_f2_0.vbp iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X50 iovss d2s_block_0.bias_tree_n_f2_0.ni d2s_block_0.bias_tree_n_f2_0.ni iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X51 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X52 Clamp_N_M1_wiring_0.b d2s_block_0.d2s_sp2k_f2_0.core Clamp_N_M1_wiring_0.b Clamp_N_M1_wiring_0.b sg13_hv_pmos ad=2.7064p pd=16.6u as=0.35189n ps=1.20463m w=7.96u l=32.16u
X53 d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X54 d2s_block_0.d2s_casc_p_c2_0.pl d2s_block_0.d2s_ab_n_f2_0.l2 iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X55 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X56 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X57 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X58 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X59 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X60 iovss d2s_block_0.d2s_sp2k_f2_1.core dantenna l=3.1u w=0.64u
X61 d2s_block_0.d2s_rhigh_f2_0.sb_A d2s_block_0.bias_tree_n_f2_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X62 iovss d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.d2s_casc_n_f2_0.y iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X63 d2s_block_0.d2s_rhigh_f2_0.sa_B vref d2s_block_0.d2s_casc_n_f2_0.y d2s_block_0.d2s_rhigh_f2_0.sa_B sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X64 d2s_block_0.d2s_casc_n_f2_0.y vref d2s_block_0.d2s_rhigh_f2_0.sa_C1 d2s_block_0.d2s_rhigh_f2_0.sa_C1 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X65 d2s_block_0.d2s_casc_n_f2_0.y d2s_block_0.sinks_6x6_f2_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X66 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X67 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X68 iovdd d2s_block_0.bias_tree_n_f2_0.vbp iovdd iovdd sg13_hv_pmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X69 d2s_block_0.bias_tree_n_f2_0.ni en_3v3 iref iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X70 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X71 iovdd en_3v3 d2s_cma_0.a iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X72 pad iovdd dpantenna l=1.26u w=65.8u
X73 d2s_block_0.bias_tree_n_f2_0.ni en_3v3_b iovss iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X74 d2s_block_0.d2s_sp2k_f2_1.core pad iovss rppd l=7.435u w=1u
X75 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X76 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X77 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X78 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X79 d2s_block_0.d2s_rhigh_f2_0.sb_C1 pad d2s_block_0.d2s_casc_n_f2_0.x d2s_block_0.d2s_rhigh_f2_0.sb_C1 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X80 a_9510_32196# d2s_block_0.d2s_rhigh_f2_0.sa_A iovss rhigh l=12.65u w=0.5u
X81 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=3.4p pd=20.68u as=0 ps=0 w=10u l=1u
X82 iovdd d2s_block_0.bias_tree_n_f2_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=0 ps=0 w=5u l=6u
X83 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X84 d2s_block_0.d2s_ab_n_f2_0.l2 d2s_block_0.bias_tree_n_f2_0.vbpc d2s_block_0.d2s_casc_p_c2_0.pl iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X85 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X86 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X87 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=2.2644p pd=14u as=0 ps=0 w=6.66u l=0.6u
X88 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X89 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=2.068p ps=9.74u w=4.4u l=1u
X90 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X91 iovss d2s_block_0.bias_tree_n_f2_0.ni d2s_block_0.bias_tree_n_f2_0.vbpc iovss sg13_hv_nmos ad=0.816p pd=5.48u as=0.816p ps=5.48u w=2.4u l=6u
X92 a_10734_32196# d2s_block_0.d2s_rhigh_f2_0.sb_B iovss rhigh l=12.65u w=0.5u
X93 Clamp_P_M1_wiring_0.dabp d2s_block_0.bias_tree_n_f2_0.vabp d2s_block_0.bias_tree_n_f2_0.vabp iovdd sg13_hv_pmos ad=2.2644p pd=14u as=2.2644p ps=14u w=6.66u l=0.6u
X94 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X95 d2s_block_0.d2s_rhigh_f2_0.sa_C1 d2s_block_0.bias_tree_n_f2_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X96 a_11006_32196# a_10054_29580# iovss rhigh l=12.65u w=0.5u
X97 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X98 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X99 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X100 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X101 iovdd d2s_block_0.bias_tree_n_f2_0.vbp d2s_block_0.sinks_6x6_f2_0.vbn iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X102 d2s_block_0.d2s_rhigh_f2_0.sb_A vref d2s_block_0.d2s_casc_n_f2_0.x d2s_block_0.d2s_rhigh_f2_0.sb_A sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X103 Clamp_N_M1_wiring_0.b d2s_block_0.d2s_ab_n_f2_0.vabn d2s_cma_0.a iovss sg13_hv_nmos ad=1.496p pd=9.48u as=1.496p ps=9.48u w=4.4u l=1u
X104 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=3.256p pd=10.28u as=1.408p ps=5.04u w=4.4u l=1u
X105 d2s_block_0.d2s_casc_n_f2_0.y vinp d2s_block_0.d2s_rhigh_f2_0.sa_A d2s_block_0.d2s_rhigh_f2_0.sa_A sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X106 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X107 d2s_block_0.d2s_casc_n_f2_0.y d2s_block_0.sinks_6x6_f2_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X108 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X109 d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn iovss sg13_hv_nmos ad=2.04p pd=12.68u as=0 ps=0 w=6u l=6u
X110 d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X111 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X112 d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc iovss sg13_hv_nmos ad=0.68p pd=4.68u as=19.07282p ps=0.15628m w=2u l=3u
X113 iovss iovss iovss iovss sg13_hv_nmos ad=1.496p pd=9.48u as=0.8943n ps=3.44684m w=4.4u l=1u
X114 d2s_block_0.d2s_sp2k_f2_0.core iovdd dpantenna l=0.64u w=4.98u
X115 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X116 iovdd Clamp_P_M1_wiring_0.dabp Clamp_P_M1_wiring_0.dabp iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X117 iovdd d2s_block_0.d2s_ab_n_f2_0.l2 iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X118 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X119 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X120 d2s_block_0.d2s_rhigh_f2_0.sa_C2 vref d2s_block_0.d2s_casc_n_f2_0.y d2s_block_0.d2s_rhigh_f2_0.sa_C2 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X121 d2s_block_0.d2s_rhigh_f2_0.sa_C2 d2s_block_0.bias_tree_n_f2_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X122 d2s_block_0.d2s_rhigh_f2_0.sa_A vinp d2s_block_0.d2s_casc_n_f2_0.y d2s_block_0.d2s_rhigh_f2_0.sa_A sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X123 Clamp_N_M1_wiring_0.b d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.y iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X124 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X125 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=3.4p pd=20.68u as=0 ps=0 w=10u l=1u
X126 iovss d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.d2s_casc_n_f2_0.x iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X127 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X128 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X129 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X130 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X131 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X132 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X133 a_10598_32196# d2s_block_0.d2s_rhigh_f2_0.sb_A iovss rhigh l=12.65u w=0.5u
X134 iovdd d2s_block_0.d2s_ab_n_f2_0.l2 iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X135 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X136 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=3.1302p ps=14.26u w=6.66u l=0.6u
X137 iovdd d2s_block_0.bias_tree_n_f2_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=0 ps=0 w=5u l=6u
X138 a_11006_32196# d2s_block_0.d2s_rhigh_f2_0.sb_C2 iovss rhigh l=12.65u w=0.5u
X139 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X140 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X141 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X142 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X143 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X144 d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=3u
X145 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X146 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=1.9p pd=10.38u as=0 ps=0 w=10u l=1u
X147 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X148 d2s_block_0.d2s_casc_n_f2_0.x vinn d2s_block_0.d2s_rhigh_f2_0.sb_B d2s_block_0.d2s_rhigh_f2_0.sb_B sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X149 iovdd d2s_block_0.d2s_ab_n_f2_0.l2 d2s_block_0.d2s_casc_p_c2_0.pl iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X150 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X151 iovdd Clamp_P_M1_wiring_0.dabp Clamp_P_M1_wiring_0.dabp iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X152 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X153 iovdd d2s_block_0.bias_tree_n_f2_0.vbp d2s_block_0.d2s_rhigh_f2_0.sa_B iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X154 a_9918_32196# d2s_block_0.d2s_rhigh_f2_0.sa_C2 iovss rhigh l=12.65u w=0.5u
X155 d2s_block_0.d2s_casc_n_f2_0.x d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_ab_n_f2_0.l1 iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X156 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X157 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X158 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X159 d2s_block_0.d2s_casc_n_f2_0.y vref d2s_block_0.d2s_rhigh_f2_0.sa_B d2s_block_0.d2s_rhigh_f2_0.sa_B sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X160 d2s_block_0.d2s_sp2k_f2_1.core iovdd dpantenna l=0.64u w=4.98u
X161 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X162 d2s_block_0.d2s_ab_n_f2_0.l1 d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.x iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X163 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X164 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X165 d2s_block_0.d2s_rhigh_f2_0.sb_B d2s_block_0.bias_tree_n_f2_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X166 d2s_block_0.d2s_casc_p_c2_0.pr d2s_block_0.d2s_ab_n_f2_0.l2 iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X167 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X168 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=3.1302p ps=14.26u w=6.66u l=0.6u
X169 Clamp_N_M1_wiring_0.dabn Clamp_N_M1_wiring_0.dabn iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X170 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X171 d2s_block_0.d2s_casc_n_f2_0.x d2s_block_0.sinks_6x6_f2_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X172 a_10734_32196# a_10326_29580# iovss rhigh l=12.65u w=0.5u
X173 d2s_block_0.d2s_rhigh_f2_0.sb_B vinn d2s_block_0.d2s_casc_n_f2_0.x d2s_block_0.d2s_rhigh_f2_0.sb_B sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X174 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X175 iovdd d2s_block_0.bias_tree_n_f2_0.vbp d2s_block_0.d2s_casc_n_f2_0.vbnc iovdd sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=6u
X176 a_9646_32196# a_10326_29580# iovss rhigh l=12.65u w=0.5u
X177 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X178 iovdd d2s_block_0.d2s_ab_n_f2_0.l2 d2s_block_0.d2s_casc_p_c2_0.pl iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X179 d2s_block_0.d2s_casc_p_c2_0.pl d2s_block_0.bias_tree_n_f2_0.vbpc d2s_block_0.d2s_ab_n_f2_0.l2 iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X180 iovss d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.d2s_casc_n_f2_0.x iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X181 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X182 iovdd d2s_block_0.bias_tree_n_f2_0.vbp iovdd iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=0 ps=0 w=5u l=6u
X183 iovss d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X184 d2s_block_0.d2s_ab_n_f2_0.vabn en_3v3_b iovss iovss sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X185 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X186 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X187 d2s_block_0.bias_tree_n_f2_0.ni d2s_block_0.bias_tree_n_f2_0.ni d2s_block_0.bias_tree_n_f2_0.ni iovss sg13_hv_nmos ad=0.816p pd=5.48u as=8.86665p ps=64.93u w=2.4u l=6u
X188 d2s_block_0.d2s_casc_p_c2_0.pr d2s_block_0.d2s_ab_n_f2_0.l2 iovdd iovdd sg13_hv_pmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=4u
X189 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X190 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X191 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=1.9p pd=10.38u as=0 ps=0 w=10u l=1u
X192 d2s_block_0.d2s_casc_n_f2_0.y d2s_block_0.d2s_casc_n_f2_0.vbnc Clamp_N_M1_wiring_0.b iovss sg13_hv_nmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X193 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X194 iovdd d2s_block_0.bias_tree_n_f2_0.vbp d2s_block_0.d2s_rhigh_f2_0.sb_C2 iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X195 a_9646_32196# d2s_block_0.d2s_rhigh_f2_0.sa_B iovss rhigh l=12.65u w=0.5u
X196 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X197 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X198 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X199 iovdd d2s_block_0.d2s_ab_n_f2_0.l2 iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X200 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X201 Clamp_P_M1_wiring_0.dabp iovdd iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X202 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X203 d2s_block_0.d2s_casc_n_f2_0.x vref d2s_block_0.d2s_rhigh_f2_0.sb_A d2s_block_0.d2s_rhigh_f2_0.sb_A sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X204 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X205 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X206 d2s_block_0.d2s_rhigh_f2_0.sb_C2 pad d2s_block_0.d2s_casc_n_f2_0.x d2s_block_0.d2s_rhigh_f2_0.sb_C2 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X207 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X208 iovss pad dantenna l=1.26u w=67.6u
X209 iovss d2s_block_0.d2s_sp2k_f2_0.core dantenna l=3.1u w=0.64u
X210 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X211 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X212 iovss d2s_block_0.bias_tree_n_f2_0.ni d2s_block_0.bias_tree_n_f2_0.vabp iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X213 a_10870_32196# a_10190_29580# iovss rhigh l=12.65u w=0.5u
X214 d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=3u
X215 Clamp_N_M1_wiring_0.dabn d2s_block_0.d2s_ab_n_f2_0.vabn d2s_block_0.d2s_ab_n_f2_0.vabn iovss sg13_hv_nmos ad=1.496p pd=9.48u as=1.496p ps=9.48u w=4.4u l=1u
X216 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X217 a_9510_32196# a_10462_29580# iovss rhigh l=12.65u w=0.5u
X218 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X219 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X220 a_9918_32196# a_10054_29580# iovss rhigh l=12.65u w=0.5u
X221 d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.sinks_6x6_f2_0.vbn iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X222 iovdd d2s_block_0.d2s_ab_n_f2_0.l2 iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=4u
X223 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X224 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X225 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=3.256p pd=10.28u as=1.408p ps=5.04u w=4.4u l=1u
X226 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X227 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X228 d2s_block_0.d2s_casc_n_f2_0.x d2s_block_0.sinks_6x6_f2_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X229 iovdd d2s_block_0.bias_tree_n_f2_0.vbp d2s_block_0.d2s_rhigh_f2_0.sb_C1 iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X230 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=1.9p pd=10.38u as=0 ps=0 w=10u l=1u
X231 d2s_block_0.d2s_casc_n_f2_0.y d2s_block_0.sinks_6x6_f2_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X232 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X233 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X234 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=2.2644p pd=14u as=0 ps=0 w=6.66u l=0.6u
X235 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X236 iovdd d2s_block_0.bias_tree_n_f2_0.vbp d2s_block_0.bias_tree_n_f2_0.vbp iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X237 a_9782_32196# d2s_block_0.d2s_rhigh_f2_0.sa_C1 iovss rhigh l=12.65u w=0.5u
X238 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X239 Clamp_P_M1_wiring_0.dabp iovdd iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X240 iovss iovss iovss rhigh l=12.65u w=0.5u
X241 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=3.4p pd=20.68u as=0 ps=0 w=10u l=1u
X242 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X243 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X244 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X245 d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc d2s_block_0.d2s_casc_n_f2_0.vbnc iovss sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=3u
X246 iovss d2s_block_0.sinks_6x6_f2_0.vbn d2s_block_0.d2s_casc_n_f2_0.y iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X247 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X248 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X249 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X250 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X251 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X252 iovss iovss iovss rhigh l=12.65u w=0.5u
X253 d2s_cma_0.a d2s_block_0.bias_tree_n_f2_0.vbpc d2s_block_0.d2s_casc_p_c2_0.pr iovdd sg13_hv_pmos ad=5.1p pd=30.68u as=5.1p ps=30.68u w=15u l=3u
X254 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X255 a_10870_32196# d2s_block_0.d2s_rhigh_f2_0.sb_C1 iovss rhigh l=12.65u w=0.5u
X256 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X257 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X258 d2s_block_0.d2s_casc_n_f2_0.x pad d2s_block_0.d2s_rhigh_f2_0.sb_C1 d2s_block_0.d2s_rhigh_f2_0.sb_C1 sg13_hv_pmos ad=1.9p pd=10.38u as=3.4p ps=20.68u w=10u l=1u
X259 d2s_block_0.d2s_rhigh_f2_0.sa_C1 vref d2s_block_0.d2s_casc_n_f2_0.y d2s_block_0.d2s_rhigh_f2_0.sa_C1 sg13_hv_pmos ad=3.4p pd=20.68u as=1.9p ps=10.38u w=10u l=1u
X260 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X261 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X262 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X263 a_9782_32196# a_10190_29580# iovss rhigh l=12.65u w=0.5u
X264 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X265 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X266 d2s_block_0.bias_tree_n_f2_0.vabp en_3v3 iovdd iovdd sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X267 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X268 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X269 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X270 iovdd d2s_block_0.bias_tree_n_f2_0.vbp d2s_block_0.d2s_rhigh_f2_0.sa_A iovdd sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X271 Clamp_N_M1_wiring_0.b d2s_block_0.bias_tree_n_f2_0.vabp d2s_cma_0.a iovdd sg13_hv_pmos ad=2.2644p pd=14u as=2.2644p ps=14u w=6.66u l=0.6u
X272 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X273 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X274 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X275 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X276 iovss Clamp_N_M1_wiring_0.dabn Clamp_N_M1_wiring_0.dabn iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X277 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=2.068p ps=9.74u w=4.4u l=1u
X278 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=1.9p pd=10.38u as=0 ps=0 w=10u l=1u
X279 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X280 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X281 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
X282 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=4.9284p pd=14.8u as=2.1312p ps=7.3u w=6.66u l=0.6u
X283 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X284 d2s_block_0.d2s_casc_n_f2_0.x d2s_block_0.sinks_6x6_f2_0.vbn iovss iovss sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X285 pad d2s_cma_0.a iovdd iovdd sg13_hv_pmos ad=3.9294p pd=7.84u as=2.1312p ps=7.3u w=6.66u l=0.6u
X286 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X287 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X288 iovss Clamp_N_M1_wiring_0.b pad iovss sg13_hv_nmos ad=1.408p pd=5.04u as=2.596p ps=5.58u w=4.4u l=1u
X289 iovdd iovdd iovdd iovdd sg13_hv_pmos ad=3.4p pd=20.68u as=0 ps=0 w=10u l=1u
X290 iovss iovss iovss iovss sg13_hv_nmos ad=1.496p pd=9.48u as=0 ps=0 w=4.4u l=1u
X291 iovdd d2s_cma_0.a pad iovdd sg13_hv_pmos ad=2.1312p pd=7.3u as=3.9294p ps=7.84u w=6.66u l=0.6u
X292 pad Clamp_N_M1_wiring_0.b iovss iovss sg13_hv_nmos ad=2.596p pd=5.58u as=1.408p ps=5.04u w=4.4u l=1u
.ends

