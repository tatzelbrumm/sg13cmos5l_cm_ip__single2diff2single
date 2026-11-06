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
X0 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=1.2524n ps=1.97673m w=2u l=8u
X1 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vpc vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X2 slot7_xgate_0.ena_b slot7_xgate_0.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X3 a_23431_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 rhigh l=9.94u w=0.5u
X4 a_27390_31012# slot7_bg_core_pd_0.en_3v3_b a_24822_30862# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X5 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X6 a_23567_31672# a_23295_29598# vss_3v3 rhigh l=9.94u w=0.5u
X7 a_21663_31672# a_21935_29598# vss_3v3 rhigh l=9.94u w=0.5u
X8 a_22751_31672# a_23159_29598# vss_3v3 rhigh l=9.94u w=0.5u
X9 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=2u
X10 a_16002_31593# slot7_oa_core_pd_0.en_3v3_b vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X11 a_21527_31672# a_21255_29598# vss_3v3 rhigh l=9.94u w=0.5u
X12 dig_out[6] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X13 a_20575_31672# a_21119_29598# vss_3v3 rhigh l=9.94u w=0.5u
X14 vdd_1v2 vdd_3v3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X15 slot7_bg_core_pd_0.slot7_bg_ms1_0.ks slot7_bg_core_pd_0.en_3v3_b a_24822_30862# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X16 a_21527_31672# a_22071_29598# vss_3v3 rhigh l=9.94u w=0.5u
X17 slot7_xgate_0.ena a_7596_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X18 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X19 vdd_3v3 slot7_oa_core_pd_0.en_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X20 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X21 a_7784_9136# vdd_1v2 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X22 analog_bus0 slot7_xgate_1.ena_b slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X23 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=1.156p pd=7.48u as=1.156p ps=7.48u w=3.4u l=30u
X24 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X25 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X26 slot7_oa_core_pd_0.slot7_oa_ms1_0.ks slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X27 slot7_oa_core_pd_0.slot7_oa_ms1_0.ks slot7_oa_core_pd_0.en_3v3_b vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X28 a_19759_31672# a_20031_29598# vss_3v3 rhigh l=9.94u w=0.5u
X29 dig_out[9] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X30 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X31 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=73.8615p ps=0.3643m w=2u l=1u
X32 a_16002_31893# slot7_oa_core_pd_0.en_3v3_b a_13434_32043# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X33 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X34 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X35 a_27390_31312# slot7_bg_core_pd_0.en_3v3_b a_24822_31162# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X36 a_7250_9136# dig_in[2] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X37 a_16002_31893# slot7_oa_core_pd_0.en_3v3_b a_13434_31743# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X38 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X39 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X40 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X41 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.94054n ps=1.63919m w=2u l=1u
X42 dig_out[8] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X43 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr a_9724_27872# vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X44 analog_bus0 slot7_xgate_1.ena slot7_xgate_1.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X45 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X46 slot7_bg_core_pd_0.en_3v3 a_6904_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X47 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=1.156p pd=7.48u as=1.156p ps=7.48u w=3.4u l=30u
X48 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X49 vss_3v3 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X50 a_19759_31672# a_19487_29598# vss_3v3 rhigh l=9.94u w=0.5u
X51 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X52 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X53 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X54 a_16002_32193# slot7_oa_core_pd_0.en_3v3_b a_13434_32343# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X55 dig_out[11] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X56 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X57 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X58 a_22887_31672# a_23295_29598# vss_3v3 rhigh l=9.94u w=0.5u
X59 dig_out[2] a_7250_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X60 slot7_oa_core_pd_0.en_3v3 a_6558_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X61 a_27390_31612# slot7_bg_core_pd_0.en_3v3_b a_24822_31462# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X62 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X63 a_21663_31672# a_21119_29598# vss_3v3 rhigh l=9.94u w=0.5u
X64 a_27390_31012# slot7_bg_core_pd_0.en_3v3_b a_24822_31162# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X65 a_20983_31672# a_21255_29598# vss_3v3 rhigh l=9.94u w=0.5u
X66 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X67 a_6400_9136# enable a_7784_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X68 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X69 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X70 slot7_oa_core_pd_0.en_3v3 a_6558_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X71 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X72 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X73 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X74 dig_out[3] a_7596_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X75 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X76 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X77 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X78 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X79 vdd_3v3 slot7_bg_core_pd_0.en_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X80 a_16002_32493# slot7_oa_core_pd_0.en_3v3_b slot7_oa_core_pd_0.slot7_oa_ms1_0.ks vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X81 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X82 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X83 a_16002_32193# slot7_oa_core_pd_0.en_3v3_b a_13434_32043# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X84 vdd_3v3 slot7_bg_core_pd_0.en_3v3_b a_24822_31762# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X85 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X86 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X87 slot7_bg_core_pd_0.en_3v3_b slot7_bg_core_pd_0.en_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X88 a_7596_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X89 a_27390_31312# slot7_bg_core_pd_0.en_3v3_b a_24822_31462# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X90 slot7_xgate_1.ena_b slot7_xgate_1.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X91 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_n4_0.ea vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X92 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X93 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X94 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X95 dig_out[3] a_7596_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X96 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X97 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X98 a_19895_31672# a_19351_29598# vss_3v3 rhigh l=9.94u w=0.5u
X99 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X100 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X101 a_19215_31672# a_19487_29598# vss_3v3 rhigh l=9.94u w=0.5u
X102 a_22887_31672# a_22615_29598# vss_3v3 rhigh l=9.94u w=0.5u
X103 vss_3v3 vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X104 a_22479_31672# a_21935_29598# vss_3v3 rhigh l=9.94u w=0.5u
X105 dig_out[0] a_6558_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X106 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X107 a_20847_31672# a_20439_29598# vss_3v3 rhigh l=9.94u w=0.5u
X108 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X109 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X110 a_16002_32493# slot7_oa_core_pd_0.en_3v3_b a_13434_32343# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X111 a_19895_31672# a_20439_29598# vss_3v3 rhigh l=9.94u w=0.5u
X112 a_7250_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X113 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X114 a_27390_31612# slot7_bg_core_pd_0.en_3v3_b a_24822_31762# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X115 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X116 a_20847_31672# a_21391_29598# vss_3v3 rhigh l=9.94u w=0.5u
X117 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X118 vss_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_ms1_0.ks vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X119 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X120 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X121 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X122 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X123 slot7_xgate_1.ena a_7250_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X124 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X125 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X126 vss_3v3 slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vbr vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X127 a_24111_31672# a_23839_29598# vss_3v3 rhigh l=9.94u w=0.5u
X128 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X129 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X130 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X131 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X132 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X133 dig_out[2] a_7250_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X134 a_7596_9136# dig_in[3] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X135 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X136 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X137 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X138 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X139 dig_out[5] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X140 a_6558_9136# dig_in[0] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X141 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X142 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X143 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X144 a_20983_31672# a_20711_29598# vss_3v3 rhigh l=9.94u w=0.5u
X145 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X146 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X147 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X148 a_20575_31672# a_20167_29598# vss_3v3 rhigh l=9.94u w=0.5u
X149 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X150 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X151 a_19623_31672# a_20167_29598# vss_3v3 rhigh l=9.94u w=0.5u
X152 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X153 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X154 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X155 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X156 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X157 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X158 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X159 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X160 a_23703_31672# a_23159_29598# vss_3v3 rhigh l=9.94u w=0.5u
X161 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X162 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X163 slot7_xgate_0.in slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X164 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X165 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X166 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_ms1_0.ks vss_3v3 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X167 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X168 a_19918_34040# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X169 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X170 a_21799_31672# a_21391_29598# vss_3v3 rhigh l=9.94u w=0.5u
X171 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X172 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X173 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X174 dig_out[1] a_6904_9136# vdd_1v2 vdd_1v2 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X175 slot7_xgate_0.ena a_7596_9136# vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X176 analog_bus1 slot7_xgate_0.ena_b slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X177 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X178 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X179 slot7_xgate_0.in slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X180 dig_out[4] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X181 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X182 vss_3v3 vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X183 dig_out[10] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X184 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X185 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X186 slot7_bg_core_pd_0.en_3v3 a_6904_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X187 slot7_xgate_1.ena a_7250_9136# vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X188 slot7_xgate_0.in slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X189 slot7_xgate_0.in slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X190 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X191 a_23431_31672# a_23023_29598# vss_3v3 rhigh l=9.94u w=0.5u
X192 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X193 a_22479_31672# a_23023_29598# vss_3v3 rhigh l=9.94u w=0.5u
X194 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X195 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X196 analog_bus1 slot7_xgate_0.ena slot7_xgate_0.in vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.5u
X197 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X198 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X199 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X200 slot7_xgate_0.ena_b slot7_xgate_0.ena vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X201 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X202 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X203 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X204 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_xgate_1.in vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X205 dig_out[0] a_6558_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X206 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X207 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X208 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X209 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X210 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X211 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X212 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X213 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X214 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X215 a_23703_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.ea vss_3v3 rhigh l=9.94u w=0.5u
X216 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X217 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X218 a_19623_31672# vss_3v3 vss_3v3 rhigh l=9.94u w=0.5u
X219 a_22343_31672# a_22615_29598# vss_3v3 rhigh l=9.94u w=0.5u
X220 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X221 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X222 a_19215_31672# slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 vss_3v3 rhigh l=9.94u w=0.5u
X223 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X224 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=8u
X225 a_21799_31672# a_22207_29598# vss_3v3 rhigh l=9.94u w=0.5u
X226 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc slot7_xgate_0.in vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X227 slot7_xgate_1.ena_b slot7_xgate_1.ena vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X228 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc a_19918_34040# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X229 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X230 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X231 slot7_bg_core_pd_0.en_3v3_b slot7_bg_core_pd_0.en_3v3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X232 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X233 slot7_oa_core_pd_0.en_3v3_b slot7_oa_core_pd_0.en_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X234 a_6904_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X235 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X236 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_n4_0.ea pnpMPA a=4p p=8u
X237 dig_out[7] vdd_1v2 vss_1v2 vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=0.45u
X238 vss_3v3 slot7_bg_core_pd_0.slot7_bg_ms1_0.ks slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vss_3v3 sg13_hv_nmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=2u
X239 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X240 slot7_oa_core_pd_0.en_3v3_b slot7_oa_core_pd_0.en_3v3 vss_3v3 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X241 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X242 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X243 a_23567_31672# a_23839_29598# vss_3v3 rhigh l=9.94u w=0.5u
X244 a_6558_9136# vss_3v3 vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0.102p ps=1.28u w=0.3u l=20u
X245 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X246 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X247 a_24111_31672# slot7_bg_core_pd_0.slot7_bg_n4_0.eb vss_3v3 rhigh l=9.94u w=0.5u
X248 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X249 slot7_bg_core_pd_0.slot7_bg_n4_0.ea slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X250 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X251 vss_3v3 a_19351_29598# vss_3v3 rhigh l=9.94u w=0.5u
X252 a_22751_31672# a_22207_29598# vss_3v3 rhigh l=9.94u w=0.5u
X253 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X254 a_22343_31672# a_22071_29598# vss_3v3 rhigh l=9.94u w=0.5u
X255 a_20303_31672# a_20711_29598# vss_3v3 rhigh l=9.94u w=0.5u
X256 a_19918_32528# slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X257 a_20303_31672# a_20031_29598# vss_3v3 rhigh l=9.94u w=0.5u
X258 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X259 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_n10_0.vpc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=2u
X260 dig_out[1] a_6904_9136# vss_1v2 vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X261 vss_3v3 vss_3v3 slot7_bg_core_pd_0.slot7_bg_res_c_0.e2 pnpMPA a=4p p=8u
X262 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X263 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X264 a_16002_31593# slot7_oa_core_pd_0.en_3v3_b a_13434_31743# vdd_3v3 sg13_hv_pmos ad=0.17p pd=1.68u as=0.17p ps=1.68u w=0.5u l=12.5u
X265 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.co slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X266 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X267 a_6904_9136# dig_in[1] a_6400_9136# vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X268 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X269 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X270 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.102p pd=1.28u as=0 ps=0 w=0.3u l=1u
X271 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X272 vss_3v3 slot7_bg_core_pd_0.en_3v3_b slot7_bg_core_pd_0.slot7_bg_ms1_0.ks vss_3v3 sg13_hv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
X273 vdd_3v3 slot7_bg_core_pd_0.slot7_bg_svpg_0.vpg a_19918_32528# vdd_3v3 sg13_hv_pmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X274 vss_3v3 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=1u
X275 slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_n10_0.vnc vss_3v3 vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
X276 vdd_3v3 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c2 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X277 slot7_oa_core_pd_0.slot7_oa_pmir_c_0.c8 slot7_oa_core_pd_0.slot7_oa_svpg_0.vpg vdd_3v3 vdd_3v3 sg13_hv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=8u
X278 slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g vss_3v3 sg13_hv_nmos ad=0.68p pd=4.68u as=0 ps=0 w=2u l=4u
X279 slot7_bg_core_pd_0.slot7_bg_n4_0.eb slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.g slot7_bg_core_pd_0.slot7_bg_pmir_pcas_c_0.vpc vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=4u
X280 a_9724_27872# slot7_oa_core_pd_0.slot7_oa_n10_0.vnc slot7_oa_core_pd_0.slot7_oa_mcs_c_0.vres vss_3v3 sg13_hv_nmos ad=3.4p pd=20.68u as=3.4p ps=20.68u w=10u l=1u
.ends

