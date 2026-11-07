* NGSPICE file created from slot_7.ext - technology: ihp-sg13cmos5l

.subckt slot_7 s7_an_0_vref s7_an_0_vcm s7_an_0_en_3v3 s7_an_0_en_3v3_b s7_an_0_iref
+ s7_an_1_vinp s7_an_1_vinn s7_an_1_vref s7_an_1_iref s7_an_1_en_3v3_b s7_an_1_en_3v3
+ vbias dig_in[23] dig_in[22] dig_in[21] dig_in[20] dig_in[19] dig_in[18] dig_in[17]
+ dig_in[16] dig_in[15] dig_in[14] dig_in[13] dig_in[12] dig_in[11] dig_in[10] dig_in[9]
+ dig_in[8] dig_in[7] dig_in[6] dig_in[5] dig_in[4] dig_in[3] dig_in[2] dig_in[1]
+ dig_in[0] dig_out[11] dig_out[10] dig_out[9] dig_out[8] dig_out[7] dig_out[6] dig_out[5]
+ dig_out[4] dig_out[3] dig_out[2] dig_out[1] dig_out[0] ibias0 ibias1 analog_bus3
+ analog_bus2 analog_bus1 analog_bus0 enable clk reset vss_1v2 vdd_1v2 vss_3v3 vdd_3v3
+ vss_1v2_uq0
X0 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vpc vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X1 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=1.46328n ps=2.81002m w=2u l=8u
X2 slot7_tp_en_ctrl_0.en3_b slot7_tp_en_ctrl_0.en3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X3 vdd_3v3 slot7_xgate_3.in slot7_xgate_2.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X4 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X5 a_27390_31012# slot7_tp_en_ctrl_0.en1_b a_24822_30862# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X6 a_23431_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 rhigh l=9.94u w=0.5u
X7 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X8 vss_3v3 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=1.06659n ps=2.36177m w=1.2u l=6u
X9 a_23567_31672# a_23295_29598# vss_3v3 rhigh l=9.94u w=0.5u
X10 a_22751_31672# a_23159_29598# vss_3v3 rhigh l=9.94u w=0.5u
X11 a_21663_31672# a_21935_29598# vss_3v3 rhigh l=9.94u w=0.5u
X12 dig_out[6] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X13 a_16002_31593# slot7_tp_en_ctrl_0.en0_b vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X14 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=2u
X15 a_21527_31672# a_21255_29598# vss_3v3 rhigh l=9.94u w=0.5u
X16 vdd_1v2 vdd_3v3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X17 slot7_bg_core_pd_0.slot7_bg_ms1_0.ks slot7_tp_en_ctrl_0.en1_b a_24822_30862# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X18 a_20575_31672# a_21119_29598# vss_3v3 rhigh l=9.94u w=0.5u
X19 slot7_tp_en_ctrl_0.en3 a_7596_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X20 a_21527_31672# a_22071_29598# vss_3v3 rhigh l=9.94u w=0.5u
X21 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X22 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=1.156p pd=7.48u as=1.156p ps=7.48u w=3.4u l=30u
X23 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X24 a_7784_9136# vdd_1v2 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X25 analog_bus0 slot7_tp_en_ctrl_0.en2_b slot7_xgate_7.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X26 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X27 vdd_3v3 slot7_tp_en_ctrl_0.en0 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X28 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X29 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X30 a_19759_31672# a_20031_29598# vss_3v3 rhigh l=9.94u w=0.5u
X31 slot7_oa_core_pd_0.slot7_oa_ms1_0.ks slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X32 dig_out[9] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X33 vdd_3v3 slot7_xgate_3.in slot7_xgate_2.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X34 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=73.8615p ps=0.3643m w=2u l=1u
X35 slot7_oa_core_pd_0.slot7_oa_ms1_0.ks slot7_tp_en_ctrl_0.en0_b vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X36 a_16002_31893# slot7_tp_en_ctrl_0.en0_b a_13434_32043# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X37 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X38 analog_bus3 slot7_xgate_4.ena_b ibias1 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X39 vdd_3v3 slot7_xgate_3.in slot7_xgate_3.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X40 a_27390_31312# slot7_tp_en_ctrl_0.en1_b a_24822_31162# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X41 slot7_xgate_1.ena a_39634_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X42 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X43 slot7_xgate_3.in slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X44 a_7250_9136# dig_in[2] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X45 vdd_3v3 slot7_xgate_3.in slot7_xgate_2.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X46 slot7_xgate_1.in slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X47 a_16002_31893# slot7_tp_en_ctrl_0.en0_b a_13434_31743# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X48 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X49 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X50 analog_bus2 slot7_xgate_0.ena_b slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X51 a_38250_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X52 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X53 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X54 dig_out[8] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X55 slot7_xgate_7.out slot7_xgate_7.ena_b slot7_xgate_7.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X56 analog_bus0 slot7_tp_en_ctrl_0.en2 slot7_xgate_7.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X57 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr a_9724_27872# vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X58 slot7_tp_en_ctrl_0.en1 a_6904_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X59 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X60 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X61 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=1.156p pd=7.48u as=1.156p ps=7.48u w=3.4u l=30u
X62 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X63 a_19759_31672# a_19487_29598# vss_3v3 rhigh l=9.94u w=0.5u
X64 vss_3v3 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X65 a_39980_24776# dig_in[11] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X66 vdd_3v3 slot7_xgate_3.in vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0 ps=0 w=0.5u l=6u
X67 slot7_xgate_3.ena_b slot7_xgate_3.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X68 a_16002_32193# slot7_tp_en_ctrl_0.en0_b a_13434_32343# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X69 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X70 dig_out[11] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X71 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X72 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X73 dig_out[2] a_7250_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X74 vdd_3v3 slot7_xgate_3.in slot7_xgate_2.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X75 slot7_tp_en_ctrl_0.en0 a_6558_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X76 a_27390_31612# slot7_tp_en_ctrl_0.en1_b a_24822_31462# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X77 a_22887_31672# a_23295_29598# vss_3v3 rhigh l=9.94u w=0.5u
X78 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X79 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X80 a_27390_31012# slot7_tp_en_ctrl_0.en1_b a_24822_31162# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X81 a_21663_31672# a_21119_29598# vss_3v3 rhigh l=9.94u w=0.5u
X82 vdd_3v3 slot7_xgate_3.in slot7_xgate_3.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X83 a_20983_31672# a_21255_29598# vss_3v3 rhigh l=9.94u w=0.5u
X84 a_6400_9136# enable a_7784_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X85 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X86 slot7_xgate_7.out slot7_xgate_7.ena slot7_xgate_7.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X87 slot7_xgate_3.ena a_38942_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X88 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X89 slot7_tp_en_ctrl_0.en0 a_6558_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X90 slot7_xgate_0.ena_b slot7_xgate_0.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X91 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X92 slot7_xgate_2.ena a_39288_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X93 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X94 slot7_xgate_4.ena_b slot7_xgate_4.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X95 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X96 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X97 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X98 dig_out[3] a_7596_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X99 slot7_xgate_2.in slot7_xgate_2.in vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X100 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni slot7_bias_tree_noab_pd_0.en_3v3_b vss_3v3 vss_3v3 sg13_hv_nmos ad=0.19p pd=1.38u as=0.34p ps=2.68u w=1u l=0.45u
X101 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X102 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X103 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X104 a_38596_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X105 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X106 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X107 a_16002_32493# slot7_tp_en_ctrl_0.en0_b slot7_oa_core_pd_0.slot7_oa_ms1_0.ks vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X108 vdd_3v3 slot7_tp_en_ctrl_0.en1 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X109 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X110 a_16002_32193# slot7_tp_en_ctrl_0.en0_b a_13434_32043# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X111 vdd_3v3 slot7_tp_en_ctrl_0.en1_b a_24822_31762# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X112 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X113 slot7_xgate_4.ena a_40326_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X114 a_27390_31312# slot7_tp_en_ctrl_0.en1_b a_24822_31462# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X115 slot7_tp_en_ctrl_0.en1_b slot7_tp_en_ctrl_0.en1 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X116 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X117 a_7596_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X118 slot7_tp_en_ctrl_0.en2_b slot7_tp_en_ctrl_0.en2 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X119 slot7_bias_tree_noab_pd_0.en_3v3_b slot7_bias_tree_noab_pd_0.en_3v3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X120 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_n4_0.ea vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X121 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X122 slot7_xgate_7.ena a_37558_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X123 analog_bus2 slot7_xgate_1.ena slot7_xgate_1.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X124 dig_out[3] a_7596_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X125 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X126 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X127 slot7_xgate_6.ena a_37904_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X128 a_19895_31672# a_19351_29598# vss_3v3 rhigh l=9.94u w=0.5u
X129 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X130 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X131 a_22887_31672# a_22615_29598# vss_3v3 rhigh l=9.94u w=0.5u
X132 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X133 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_xgate_6.in vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X134 a_19215_31672# a_19487_29598# vss_3v3 rhigh l=9.94u w=0.5u
X135 slot7_xgate_3.in slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X136 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X137 a_22479_31672# a_21935_29598# vss_3v3 rhigh l=9.94u w=0.5u
X138 dig_out[0] a_6558_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X139 slot7_bias_tree_noab_pd_0.en_3v3 a_38596_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X140 vss_3v3 vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X141 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X142 slot7_xgate_1.ena_b slot7_xgate_1.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X143 a_20847_31672# a_20439_29598# vss_3v3 rhigh l=9.94u w=0.5u
X144 vdd_3v3 slot7_xgate_3.in slot7_xgate_3.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X145 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X146 a_7250_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X147 a_16002_32493# slot7_tp_en_ctrl_0.en0_b a_13434_32343# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X148 a_19895_31672# a_20439_29598# vss_3v3 rhigh l=9.94u w=0.5u
X149 a_20847_31672# a_21391_29598# vss_3v3 rhigh l=9.94u w=0.5u
X150 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X151 a_27390_31612# slot7_tp_en_ctrl_0.en1_b a_24822_31762# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X152 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X153 slot7_xgate_2.in slot7_xgate_2.in vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X154 vss_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_ms1_0.ks vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X155 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X156 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X157 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X158 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X159 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X160 analog_bus2 slot7_xgate_3.ena_b slot7_xgate_3.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X161 slot7_tp_en_ctrl_0.en2 a_7250_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X162 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X163 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X164 vss_3v3 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X165 a_24111_31672# a_23839_29598# vss_3v3 rhigh l=9.94u w=0.5u
X166 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X167 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X168 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X169 dig_out[2] a_7250_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X170 a_7596_9136# dig_in[3] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X171 slot7_xgate_0.in slot7_xgate_0.in vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=8u
X172 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X173 slot7_xgate_3.ena_b slot7_xgate_3.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X174 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X175 a_39288_24776# dig_in[9] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X176 slot7_xgate_2.ena_b slot7_xgate_2.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X177 slot7_xgate_7.out slot7_xgate_6.ena_b slot7_xgate_6.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X178 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X179 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X180 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X181 slot7_xgate_7.out slot7_bias_tree_noab_pd_0.en_3v3 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.19p ps=1.38u w=1u l=0.45u
X182 dig_out[5] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X183 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_xgate_6.in vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X184 a_6558_9136# dig_in[0] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X185 a_37558_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X186 slot7_xgate_2.in slot7_xgate_2.in vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X187 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X188 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X189 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_7.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X190 a_20983_31672# a_20711_29598# vss_3v3 rhigh l=9.94u w=0.5u
X191 slot7_xgate_2.ena a_39288_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X192 a_39634_24776# dig_in[10] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X193 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X194 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X195 a_40326_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X196 a_20575_31672# a_20167_29598# vss_3v3 rhigh l=9.94u w=0.5u
X197 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X198 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X199 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X200 a_19623_31672# a_20167_29598# vss_3v3 rhigh l=9.94u w=0.5u
X201 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X202 slot7_xgate_1.in slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X203 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X204 a_38942_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X205 slot7_xgate_7.out slot7_xgate_6.ena slot7_xgate_6.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X206 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X207 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X208 a_37400_24776# enable a_40514_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X209 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X210 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X211 slot7_bias_tree_noab_pd_0.en_3v3_b slot7_bias_tree_noab_pd_0.en_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X212 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X213 a_23703_31672# a_23159_29598# vss_3v3 rhigh l=9.94u w=0.5u
X214 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X215 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X216 slot7_xgate_6.in slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X217 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X218 analog_bus3 slot7_xgate_4.ena ibias1 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X219 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X220 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X221 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_ms1_0.ks vss_3v3 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X222 analog_bus2 slot7_xgate_0.ena slot7_xgate_0.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X223 a_38250_24776# dig_in[6] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X224 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X225 vss_3v3 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0 ps=0 w=1.2u l=6u
X226 a_38942_24776# dig_in[8] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X227 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X228 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X229 a_21799_31672# a_21391_29598# vss_3v3 rhigh l=9.94u w=0.5u
X230 slot7_xgate_3.in slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X231 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X232 analog_bus2 slot7_xgate_2.ena_b slot7_xgate_2.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X233 slot7_xgate_3.in slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X234 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X235 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X236 slot7_tp_en_ctrl_0.en3 a_7596_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X237 dig_out[1] a_6904_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X238 slot7_xgate_5.ena_b slot7_xgate_5.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X239 slot7_xgate_1.ena a_39634_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X240 slot7_xgate_4.ena_b slot7_xgate_4.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X241 analog_bus1 slot7_tp_en_ctrl_0.en3_b slot7_xgate_6.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X242 slot7_xgate_0.ena a_39980_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X243 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X244 slot7_xgate_6.in slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X245 dig_out[4] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X246 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X247 vss_3v3 vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X248 dig_out[10] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X249 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X250 slot7_tp_en_ctrl_0.en1 a_6904_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X251 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X252 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X253 slot7_tp_en_ctrl_0.en2 a_7250_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X254 slot7_xgate_6.in slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X255 a_23431_31672# a_23023_29598# vss_3v3 rhigh l=9.94u w=0.5u
X256 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X257 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_7.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X258 slot7_xgate_6.in slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X259 a_22479_31672# a_23023_29598# vss_3v3 rhigh l=9.94u w=0.5u
X260 a_37904_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X261 vdd_3v3 slot7_xgate_3.in slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X262 slot7_xgate_3.in slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X263 slot7_xgate_5.ena a_38250_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X264 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X265 analog_bus1 slot7_tp_en_ctrl_0.en3 slot7_xgate_6.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X266 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X267 slot7_xgate_7.out slot7_xgate_5.ena_b ibias0 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X268 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_7.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X269 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X270 slot7_tp_en_ctrl_0.en3_b slot7_tp_en_ctrl_0.en3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X271 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X272 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X273 slot7_xgate_7.out slot7_bias_tree_noab_pd_0.en_3v3_b slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X274 slot7_xgate_6.ena_b slot7_xgate_6.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X275 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X276 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_7.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X277 slot7_xgate_0.ena_b slot7_xgate_0.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X278 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_7.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X279 dig_out[0] a_6558_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X280 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X281 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X282 slot7_xgate_7.out slot7_xgate_5.ena ibias0 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X283 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X284 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X285 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X286 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X287 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X288 a_39634_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X289 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X290 slot7_xgate_4.ena a_40326_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X291 slot7_xgate_7.ena a_37558_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X292 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_xgate_6.in vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X293 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X294 slot7_xgate_6.ena a_37904_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X295 a_23703_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.ea vss_3v3 rhigh l=9.94u w=0.5u
X296 a_19623_31672# vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X297 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X298 a_40326_24776# dig_in[12] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X299 a_22343_31672# a_22615_29598# vss_3v3 rhigh l=9.94u w=0.5u
X300 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X301 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X302 a_19215_31672# slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 vss_3v3 rhigh l=9.94u w=0.5u
X303 a_40514_24776# vdd_1v2 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X304 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X305 vdd_3v3 slot7_xgate_3.in slot7_xgate_3.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X306 a_21799_31672# a_22207_29598# vss_3v3 rhigh l=9.94u w=0.5u
X307 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X308 analog_bus2 slot7_xgate_3.ena slot7_xgate_3.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X309 slot7_xgate_2.in slot7_xgate_2.in vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X310 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X311 slot7_bias_tree_noab_pd_0.en_3v3 a_38596_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X312 slot7_tp_en_ctrl_0.en2_b slot7_tp_en_ctrl_0.en2 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X313 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_xgate_6.in vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X314 vdd_3v3 slot7_xgate_1.in slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=4u
X315 slot7_xgate_3.ena a_38942_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X316 vdd_3v3 slot7_xgate_3.in vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0 ps=0 w=0.5u l=6u
X317 slot7_xgate_2.ena_b slot7_xgate_2.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X318 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X319 slot7_xgate_7.ena_b slot7_xgate_7.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X320 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X321 slot7_xgate_1.ena_b slot7_xgate_1.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X322 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X323 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X324 slot7_tp_en_ctrl_0.en1_b slot7_tp_en_ctrl_0.en1 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X325 a_6904_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X326 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X327 slot7_tp_en_ctrl_0.en0_b slot7_tp_en_ctrl_0.en0 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X328 vss_3v3 slot7_bg_core_pd_0.slot7_bg_ms1_0.ks slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X329 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_n4_0.ea pnpMPA a=4p p=8u
X330 dig_out[7] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X331 a_38596_24776# dig_in[7] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X332 analog_bus2 slot7_xgate_1.ena_b slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X333 slot7_tp_en_ctrl_0.en0_b slot7_tp_en_ctrl_0.en0 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X334 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X335 vdd_3v3 slot7_xgate_3.in vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0 ps=0 w=1u l=6u
X336 slot7_xgate_2.in slot7_xgate_2.in vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X337 vdd_3v3 slot7_xgate_3.in slot7_xgate_2.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X338 slot7_xgate_6.ena_b slot7_xgate_6.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X339 a_6558_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X340 slot7_xgate_5.ena_b slot7_xgate_5.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X341 a_23567_31672# a_23839_29598# vss_3v3 rhigh l=9.94u w=0.5u
X342 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X343 vdd_3v3 slot7_xgate_3.in slot7_xgate_3.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X344 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X345 a_37558_24776# dig_in[4] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X346 a_24111_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 rhigh l=9.94u w=0.5u
X347 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X348 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X349 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X350 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X351 slot7_bg_core_pd_0.slot7_bg_n4_0.ea slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X352 a_22751_31672# a_22207_29598# vss_3v3 rhigh l=9.94u w=0.5u
X353 vss_3v3 a_19351_29598# vss_3v3 rhigh l=9.94u w=0.5u
X354 a_22343_31672# a_22071_29598# vss_3v3 rhigh l=9.94u w=0.5u
X355 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X356 a_20303_31672# a_20711_29598# vss_3v3 rhigh l=9.94u w=0.5u
X357 slot7_xgate_5.ena a_38250_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X358 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X359 a_39288_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X360 a_20303_31672# a_20031_29598# vss_3v3 rhigh l=9.94u w=0.5u
X361 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X362 dig_out[1] a_6904_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X363 slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni slot7_bias_tree_noab_pd_0.slot7_tree_pmos_0.ni vss_3v3 vss_3v3 sg13_hv_nmos ad=0.408p pd=3.08u as=0.408p ps=3.08u w=1.2u l=6u
X364 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X365 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X366 a_37904_24776# dig_in[5] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X367 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X368 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X369 vdd_3v3 slot7_xgate_3.in slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=6u
X370 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X371 a_16002_31593# slot7_tp_en_ctrl_0.en0_b a_13434_31743# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X372 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X373 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X374 a_6904_9136# dig_in[1] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X375 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X376 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X377 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X378 slot7_xgate_7.ena_b slot7_xgate_7.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X379 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X380 a_39980_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X381 vss_3v3 slot7_tp_en_ctrl_0.en1_b slot7_bg_core_pd_0.slot7_bg_ms1_0.ks vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X382 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X383 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X384 slot7_xgate_0.ena a_39980_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X385 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X386 analog_bus2 slot7_xgate_2.ena slot7_xgate_2.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X387 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X388 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X389 slot7_bg_core_pd_0.slot7_bg_n4_0.eb slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X390 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X391 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
.ends

