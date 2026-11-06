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
X0 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=1.43962n ps=2.84218m w=2u l=8u
X1 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vpc vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X2 slot7_tp_en_ctrl_0.en3_b slot7_tp_en_ctrl_0.en3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X3 a_23431_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 rhigh l=9.94u w=0.5u
X4 a_27390_31012# slot7_tp_en_ctrl_0.en1_b a_24822_30862# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X5 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X6 a_23567_31672# a_23295_29598# vss_3v3 rhigh l=9.94u w=0.5u
X7 a_21663_31672# a_21935_29598# vss_3v3 rhigh l=9.94u w=0.5u
X8 a_22751_31672# a_23159_29598# vss_3v3 rhigh l=9.94u w=0.5u
X9 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=2u
X10 a_16002_31593# slot7_tp_en_ctrl_0.en0_b vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X11 a_21527_31672# a_21255_29598# vss_3v3 rhigh l=9.94u w=0.5u
X12 dig_out[6] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X13 a_20575_31672# a_21119_29598# vss_3v3 rhigh l=9.94u w=0.5u
X14 slot7_bg_core_pd_0.slot7_bg_ms1_0.ks slot7_tp_en_ctrl_0.en1_b a_24822_30862# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X15 vdd_1v2 vdd_3v3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X16 a_21527_31672# a_22071_29598# vss_3v3 rhigh l=9.94u w=0.5u
X17 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X18 slot7_tp_en_ctrl_0.en3 a_7596_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X19 slot7_xgate_2.in slot7_xgate_3.in vdd_3v3 vdd_3v3 sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X20 vdd_3v3 slot7_tp_en_ctrl_0.en0 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X21 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X22 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X23 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=1.156p pd=7.48u as=1.156p ps=7.48u w=3.4u l=30u
X24 a_7784_9136# vdd_1v2 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X25 analog_bus0 slot7_tp_en_ctrl_0.en2_b slot7_oa_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X26 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X27 slot7_oa_core_pd_0.slot7_oa_ms1_0.ks slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X28 slot7_oa_core_pd_0.slot7_oa_ms1_0.ks slot7_tp_en_ctrl_0.en0_b vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X29 a_19759_31672# a_20031_29598# vss_3v3 rhigh l=9.94u w=0.5u
X30 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=73.8615p ps=0.3643m w=2u l=1u
X31 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X32 dig_out[9] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X33 a_16002_31893# slot7_tp_en_ctrl_0.en0_b a_13434_32043# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X34 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X35 vss_3v3 a_46558_3956# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.816p pd=5.48u as=1.06983n ps=2.49858m w=2.4u l=6u
X36 analog_bus3 slot7_tp_en_ctrl_b_0.en8_b ibias1 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X37 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X38 a_27390_31312# slot7_tp_en_ctrl_0.en1_b a_24822_31162# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X39 slot7_tp_en_ctrl_b_0.en6 a_39634_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X40 a_46558_3956# a_46558_3956# vss_3v3 vss_3v3 sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X41 a_7250_9136# dig_in[2] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X42 a_16002_31893# slot7_tp_en_ctrl_0.en0_b a_13434_31743# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X43 a_38250_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X44 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X45 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X46 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X47 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X48 analog_bus2 slot7_tp_en_ctrl_b_0.en7_b slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X49 dig_out[8] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X50 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr a_9724_27872# vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X51 slot7_xgate_7.out slot7_tp_en_ctrl_b_0.en0_b slot7_oa_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X52 analog_bus0 slot7_tp_en_ctrl_0.en2 slot7_oa_core_pd_0.iout vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X53 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X54 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X55 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=1.156p pd=7.48u as=1.156p ps=7.48u w=3.4u l=30u
X56 slot7_tp_en_ctrl_0.en1 a_6904_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X57 vss_3v3 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X58 a_19759_31672# a_19487_29598# vss_3v3 rhigh l=9.94u w=0.5u
X59 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X60 a_39980_24776# dig_in[11] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X61 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X62 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X63 a_16002_32193# slot7_tp_en_ctrl_0.en0_b a_13434_32343# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X64 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X65 dig_out[11] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X66 slot7_tp_en_ctrl_b_0.en4_b slot7_tp_en_ctrl_b_0.en4 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X67 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X68 a_22887_31672# a_23295_29598# vss_3v3 rhigh l=9.94u w=0.5u
X69 a_27390_31612# slot7_tp_en_ctrl_0.en1_b a_24822_31462# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X70 dig_out[2] a_7250_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X71 slot7_tp_en_ctrl_0.en0 a_6558_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X72 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X73 a_21663_31672# a_21119_29598# vss_3v3 rhigh l=9.94u w=0.5u
X74 a_27390_31012# slot7_tp_en_ctrl_0.en1_b a_24822_31162# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X75 a_20983_31672# a_21255_29598# vss_3v3 rhigh l=9.94u w=0.5u
X76 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X77 slot7_xgate_0.in slot7_xgate_0.in vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=8u
X78 a_6400_9136# enable a_7784_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X79 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X80 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X81 slot7_tp_en_ctrl_b_0.en7_b slot7_tp_en_ctrl_b_0.en7 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X82 slot7_tp_en_ctrl_0.en0 a_6558_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X83 slot7_xgate_7.out slot7_tp_en_ctrl_b_0.en0 slot7_oa_core_pd_0.iout vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X84 slot7_tp_en_ctrl_b_0.en4 a_38942_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X85 slot7_tp_en_ctrl_b_0.en8_b slot7_tp_en_ctrl_b_0.en8 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X86 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X87 slot7_tp_en_ctrl_b_0.en5 a_39288_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X88 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X89 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X90 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X91 dig_out[3] a_7596_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X92 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X93 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X94 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X95 vdd_3v3 slot7_tp_en_ctrl_0.en1 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X96 a_38596_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X97 a_16002_32493# slot7_tp_en_ctrl_0.en0_b slot7_oa_core_pd_0.slot7_oa_ms1_0.ks vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X98 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X99 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X100 a_16002_32193# slot7_tp_en_ctrl_0.en0_b a_13434_32043# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X101 vdd_3v3 slot7_tp_en_ctrl_0.en1_b a_24822_31762# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X102 slot7_tp_en_ctrl_b_0.en8 a_40326_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X103 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X104 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X105 a_27390_31312# slot7_tp_en_ctrl_0.en1_b a_24822_31462# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X106 slot7_tp_en_ctrl_0.en1_b slot7_tp_en_ctrl_0.en1 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X107 a_7596_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X108 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_n4_0.ea vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X109 slot7_tp_en_ctrl_0.en2_b slot7_tp_en_ctrl_0.en2 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X110 slot7_tp_en_ctrl_b_0.en3_b slot7_tp_en_ctrl_b_0.en3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X111 slot7_tp_en_ctrl_b_0.en0 a_37558_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X112 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X113 analog_bus2 slot7_tp_en_ctrl_b_0.en6 slot7_xgate_1.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X114 slot7_tp_en_ctrl_b_0.en1 a_37904_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X115 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X116 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X117 dig_out[3] a_7596_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X118 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X119 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X120 a_19895_31672# a_19351_29598# vss_3v3 rhigh l=9.94u w=0.5u
X121 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X122 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X123 a_19215_31672# a_19487_29598# vss_3v3 rhigh l=9.94u w=0.5u
X124 a_22887_31672# a_22615_29598# vss_3v3 rhigh l=9.94u w=0.5u
X125 vss_3v3 vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X126 a_22479_31672# a_21935_29598# vss_3v3 rhigh l=9.94u w=0.5u
X127 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X128 dig_out[0] a_6558_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X129 vdd_3v3 slot7_xgate_3.in vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=6u
X130 slot7_tp_en_ctrl_b_0.en3 a_38596_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X131 a_20847_31672# a_20439_29598# vss_3v3 rhigh l=9.94u w=0.5u
X132 slot7_tp_en_ctrl_b_0.en6_b slot7_tp_en_ctrl_b_0.en6 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X133 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X134 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X135 a_16002_32493# slot7_tp_en_ctrl_0.en0_b a_13434_32343# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X136 a_19895_31672# a_20439_29598# vss_3v3 rhigh l=9.94u w=0.5u
X137 a_7250_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X138 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X139 a_27390_31612# slot7_tp_en_ctrl_0.en1_b a_24822_31762# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X140 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X141 a_20847_31672# a_21391_29598# vss_3v3 rhigh l=9.94u w=0.5u
X142 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X143 vss_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_ms1_0.ks vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X144 slot7_xgate_1.in slot7_xgate_1.in vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=4u
X145 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X146 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X147 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X148 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X149 analog_bus2 slot7_tp_en_ctrl_b_0.en4_b slot7_xgate_3.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X150 slot7_tp_en_ctrl_0.en2 a_7250_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X151 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X152 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X153 vss_3v3 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X154 a_24111_31672# a_23839_29598# vss_3v3 rhigh l=9.94u w=0.5u
X155 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X156 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X157 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X158 a_46558_3956# slot7_tp_en_ctrl_b_0.en3_b vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X159 slot7_tp_en_ctrl_b_0.en4_b slot7_tp_en_ctrl_b_0.en4 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X160 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X161 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X162 dig_out[2] a_7250_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X163 a_7596_9136# dig_in[3] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X164 slot7_tp_en_ctrl_b_0.en5_b slot7_tp_en_ctrl_b_0.en5 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X165 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X166 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X167 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X168 a_39288_24776# dig_in[9] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X169 slot7_xgate_7.out slot7_tp_en_ctrl_b_0.en1_b slot7_bg_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X170 a_37558_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X171 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X172 dig_out[5] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X173 a_6558_9136# dig_in[0] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X174 slot7_xgate_1.in a_46558_3956# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.816p pd=5.48u as=0.816p ps=5.48u w=2.4u l=6u
X175 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X176 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X177 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X178 slot7_tp_en_ctrl_b_0.en5 a_39288_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X179 a_20983_31672# a_20711_29598# vss_3v3 rhigh l=9.94u w=0.5u
X180 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X181 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X182 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X183 a_20575_31672# a_20167_29598# vss_3v3 rhigh l=9.94u w=0.5u
X184 a_40326_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X185 a_39634_24776# dig_in[10] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X186 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X187 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X188 a_19623_31672# a_20167_29598# vss_3v3 rhigh l=9.94u w=0.5u
X189 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X190 a_38942_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X191 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X192 slot7_xgate_7.out slot7_tp_en_ctrl_b_0.en1 slot7_bg_core_pd_0.iout vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X193 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X194 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X195 a_37400_24776# enable a_40514_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X196 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X197 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X198 slot7_tp_en_ctrl_b_0.en3_b slot7_tp_en_ctrl_b_0.en3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X199 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X200 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X201 a_23703_31672# a_23159_29598# vss_3v3 rhigh l=9.94u w=0.5u
X202 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X203 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X204 slot7_bg_core_pd_0.iout slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X205 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X206 analog_bus3 slot7_tp_en_ctrl_b_0.en8 ibias1 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X207 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X208 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_ms1_0.ks vss_3v3 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X209 a_38250_24776# dig_in[6] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X210 analog_bus2 slot7_tp_en_ctrl_b_0.en7 slot7_xgate_0.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X211 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X212 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X213 a_38942_24776# dig_in[8] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X214 slot7_xgate_3.in slot7_xgate_3.in vdd_3v3 vdd_3v3 sg13_hv_pmos ad=1.7p pd=10.68u as=1.7p ps=10.68u w=5u l=6u
X215 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X216 a_21799_31672# a_21391_29598# vss_3v3 rhigh l=9.94u w=0.5u
X217 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X218 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X219 analog_bus2 slot7_tp_en_ctrl_b_0.en5_b slot7_xgate_2.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X220 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X221 dig_out[1] a_6904_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X222 a_46558_3956# slot7_tp_en_ctrl_b_0.en3_b slot7_xgate_7.out vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X223 slot7_tp_en_ctrl_0.en3 a_7596_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X224 slot7_tp_en_ctrl_b_0.en6 a_39634_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X225 slot7_tp_en_ctrl_b_0.en8_b slot7_tp_en_ctrl_b_0.en8 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X226 slot7_tp_en_ctrl_b_0.en2_b slot7_tp_en_ctrl_b_0.en2 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X227 slot7_tp_en_ctrl_b_0.en7 a_39980_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X228 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X229 analog_bus1 slot7_tp_en_ctrl_0.en3_b slot7_bg_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X230 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X231 slot7_bg_core_pd_0.iout slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X232 dig_out[4] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X233 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X234 vss_3v3 vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X235 dig_out[10] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X236 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X237 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X238 slot7_tp_en_ctrl_0.en1 a_6904_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X239 slot7_tp_en_ctrl_0.en2 a_7250_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X240 slot7_bg_core_pd_0.iout slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X241 slot7_bg_core_pd_0.iout slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X242 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X243 a_23431_31672# a_23023_29598# vss_3v3 rhigh l=9.94u w=0.5u
X244 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X245 a_37904_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X246 a_22479_31672# a_23023_29598# vss_3v3 rhigh l=9.94u w=0.5u
X247 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X248 slot7_tp_en_ctrl_b_0.en2 a_38250_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X249 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X250 analog_bus1 slot7_tp_en_ctrl_0.en3 slot7_bg_core_pd_0.iout vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X251 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X252 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X253 slot7_xgate_7.out slot7_tp_en_ctrl_b_0.en2_b ibias0 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X254 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X255 slot7_tp_en_ctrl_0.en3_b slot7_tp_en_ctrl_0.en3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X256 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X257 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X258 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X259 slot7_tp_en_ctrl_b_0.en1_b slot7_tp_en_ctrl_b_0.en1 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X260 slot7_tp_en_ctrl_b_0.en7_b slot7_tp_en_ctrl_b_0.en7 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X261 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X262 dig_out[0] a_6558_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X263 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X264 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X265 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X266 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X267 slot7_xgate_7.out slot7_tp_en_ctrl_b_0.en2 ibias0 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X268 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X269 a_39634_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X270 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X271 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X272 slot7_tp_en_ctrl_b_0.en8 a_40326_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X273 slot7_tp_en_ctrl_b_0.en0 a_37558_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X274 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X275 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X276 a_23703_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.ea vss_3v3 rhigh l=9.94u w=0.5u
X277 slot7_xgate_3.in a_46558_3956# vss_3v3 vss_3v3 sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X278 slot7_tp_en_ctrl_b_0.en1 a_37904_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X279 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X280 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X281 a_19623_31672# vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X282 a_22343_31672# a_22615_29598# vss_3v3 rhigh l=9.94u w=0.5u
X283 a_40326_24776# dig_in[12] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X284 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X285 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X286 a_19215_31672# slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 vss_3v3 rhigh l=9.94u w=0.5u
X287 a_40514_24776# vdd_1v2 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X288 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X289 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X290 a_21799_31672# a_22207_29598# vss_3v3 rhigh l=9.94u w=0.5u
X291 analog_bus2 slot7_tp_en_ctrl_b_0.en4 slot7_xgate_3.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X292 slot7_tp_en_ctrl_b_0.en3 a_38596_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X293 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.iout vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X294 slot7_tp_en_ctrl_0.en2_b slot7_tp_en_ctrl_0.en2 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X295 slot7_tp_en_ctrl_b_0.en4 a_38942_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X296 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X297 slot7_tp_en_ctrl_b_0.en5_b slot7_tp_en_ctrl_b_0.en5 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X298 slot7_tp_en_ctrl_b_0.en0_b slot7_tp_en_ctrl_b_0.en0 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X299 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X300 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X301 slot7_tp_en_ctrl_b_0.en6_b slot7_tp_en_ctrl_b_0.en6 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X302 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X303 slot7_tp_en_ctrl_0.en1_b slot7_tp_en_ctrl_0.en1 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X304 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X305 slot7_tp_en_ctrl_0.en0_b slot7_tp_en_ctrl_0.en0 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X306 a_6904_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X307 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_n4_0.ea pnpMPA a=4p p=8u
X308 vss_3v3 slot7_bg_core_pd_0.slot7_bg_ms1_0.ks slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X309 a_38596_24776# dig_in[7] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X310 dig_out[7] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X311 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X312 analog_bus2 slot7_tp_en_ctrl_b_0.en6_b slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X313 slot7_tp_en_ctrl_0.en0_b slot7_tp_en_ctrl_0.en0 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X314 slot7_tp_en_ctrl_b_0.en1_b slot7_tp_en_ctrl_b_0.en1 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X315 slot7_tp_en_ctrl_b_0.en2_b slot7_tp_en_ctrl_b_0.en2 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X316 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X317 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X318 a_23567_31672# a_23839_29598# vss_3v3 rhigh l=9.94u w=0.5u
X319 a_6558_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X320 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X321 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X322 a_24111_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 rhigh l=9.94u w=0.5u
X323 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X324 slot7_bg_core_pd_0.slot7_bg_n4_0.ea slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X325 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X326 a_37558_24776# dig_in[4] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X327 vss_3v3 a_19351_29598# vss_3v3 rhigh l=9.94u w=0.5u
X328 a_22751_31672# a_22207_29598# vss_3v3 rhigh l=9.94u w=0.5u
X329 slot7_xgate_0.in slot7_xgate_3.in vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=6u
X330 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X331 a_22343_31672# a_22071_29598# vss_3v3 rhigh l=9.94u w=0.5u
X332 slot7_tp_en_ctrl_b_0.en2 a_38250_24776# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X333 a_20303_31672# a_20711_29598# vss_3v3 rhigh l=9.94u w=0.5u
X334 a_39288_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X335 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X336 a_20303_31672# a_20031_29598# vss_3v3 rhigh l=9.94u w=0.5u
X337 a_46558_3956# slot7_tp_en_ctrl_b_0.en3 slot7_xgate_7.out vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X338 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X339 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X340 dig_out[1] a_6904_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X341 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X342 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X343 a_37904_24776# dig_in[5] a_37400_24776# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X344 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X345 a_16002_31593# slot7_tp_en_ctrl_0.en0_b a_13434_31743# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X346 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X347 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X348 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X349 a_6904_9136# dig_in[1] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X350 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X351 slot7_xgate_2.in slot7_xgate_2.in vss_3v3 vss_3v3 sg13_hv_nmos ad=2.04p pd=12.68u as=2.04p ps=12.68u w=6u l=6u
X352 slot7_tp_en_ctrl_b_0.en0_b slot7_tp_en_ctrl_b_0.en0 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X353 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X354 a_39980_24776# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X355 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X356 vss_3v3 slot7_tp_en_ctrl_0.en1_b slot7_bg_core_pd_0.slot7_bg_ms1_0.ks vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X357 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X358 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X359 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X360 slot7_tp_en_ctrl_b_0.en7 a_39980_24776# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X361 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X362 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X363 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X364 slot7_bg_core_pd_0.slot7_bg_n4_0.eb slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X365 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X366 analog_bus2 slot7_tp_en_ctrl_b_0.en5 slot7_xgate_2.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
.ends

