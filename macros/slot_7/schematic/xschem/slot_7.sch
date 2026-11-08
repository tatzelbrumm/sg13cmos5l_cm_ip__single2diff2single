v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {slot_7: slot 7 with the custom pads (tier 1, 2026-11-08)} 0 -1460 0 0 0.4 0.4 {}
T {XC s7_ctrl: master enable (enable -> en / en_b), mode decode (dig_in0..5) and the switch matrix S2D -> D2S / analog_bus0 / 1.} 40 -1400 0 0 0.25 0.25 {}
T {XBG bg_core_pd: 5 uA reference into bias_dist_pd input 0. XD bias_dist_pd: input 0 on, inputs 1..3 off (tied to vss_3v3);} 40 -1376 0 0 0.25 0.25 {}
T {outputs 0..2 on (iout0 -> pad_ref_rb, iout1 / iout2 -> the pads iref), iout3 off (isp, open). XR pad_ref_rb: vcm_rb / vref_rb.} 40 -1352 0 0 0.25 0.25 {}
T {Every block on the slot vdd_3v3 / vss_3v3 (the pad ring is not reachable inside the slot); all off while enable = 0.} 40 -1328 0 0 0.25 0.25 {}
T {Vs*: 0 V sources, each a same-net join (one net in the layout), written as in the source so that the netlist matches:} 40 -1304 0 0 0.25 0.25 {}
T {  en -> s7_an_0/1_en_3v3, en_b -> s7_an_0/1_en_3v3_b, vcm -> s7_an_0_vcm, s7_an_1_vref, analog_bus2, vref -> s7_an_0_vref, analog_bus3.} 40 -1280 0 0 0.25 0.25 {}
T {analog_bus2 / 3 monitor vcm / vref, or feed them with ext; the harness per-slot bus switches (reg 0x51 bits 6 / 7) are the off switch.} 40 -1256 0 0 0.25 0.25 {}
T {XDO s7_doutpd: 12 hv NMOS pull-downs (gates on vdd_1v2, sources on vss_1v2) hold the unused harness dig_out0..11 low.} 40 -1232 0 0 0.25 0.25 {}
T {Source: netlist/source/slot_7.spice (subckt slot_7). Right edge: custom-pad nets in the order of the pad pins (pad 0 at the bottom).} 40 -1208 0 0 0.25 0.25 {}
N 60 -520 160 -520 {lab=dig_out0}
N 60 -500 160 -500 {lab=dig_out1}
N 60 -480 160 -480 {lab=dig_out2}
N 60 -460 160 -460 {lab=dig_out3}
N 60 -440 160 -440 {lab=dig_out4}
N 60 -420 160 -420 {lab=dig_out5}
N 60 -400 160 -400 {lab=dig_out6}
N 60 -380 160 -380 {lab=dig_out7}
N 60 -360 160 -360 {lab=dig_out8}
N 60 -340 160 -340 {lab=dig_out9}
N 60 -320 160 -320 {lab=dig_out10}
N 60 -300 160 -300 {lab=dig_out11}
N 240 -560 240 -1060 {lab=vdd_1v2}
N 240 -1060 60 -1060 {lab=vdd_1v2}
N 280 -260 280 480 {lab=vss_1v2}
N 280 480 60 480 {lab=vss_1v2}
N 320 -260 320 520 {lab=vss_3v3}
N 60 -800 1580 -800 {lab=enable}
N 60 -760 1580 -760 {lab=dig_in0}
N 60 -740 1580 -740 {lab=dig_in1}
N 60 -720 1580 -720 {lab=dig_in2}
N 60 -700 1580 -700 {lab=dig_in3}
N 60 -680 1580 -680 {lab=dig_in4}
N 60 -660 1580 -660 {lab=dig_in5}
N 60 -620 1580 -620 {lab=analog_bus0}
N 60 -600 1580 -600 {lab=analog_bus1}
N 60 -1100 1680 -1100 {lab=vdd_3v3}
N 60 520 1720 520 {lab=vss_3v3}
N 1680 -860 1680 -1100 {lab=vdd_3v3}
N 620 -160 620 -1100 {lab=vdd_3v3}
N 920 -180 920 -1100 {lab=vdd_3v3}
N 1300 -370 1300 -1100 {lab=vdd_3v3}
N 1720 -480 1720 520 {lab=vss_3v3}
N 600 -40 600 520 {lab=vss_3v3}
N 960 180 960 520 {lab=vss_3v3}
N 1300 -230 1300 520 {lab=vss_3v3}
N 760 0 840 0 {lab=vdd_3v3}
N 760 80 840 80 {lab=vdd_3v3}
N 760 100 840 100 {lab=vdd_3v3}
N 760 120 840 120 {lab=vdd_3v3}
N 760 -1100 760 120 {lab=vdd_3v3}
N 800 -80 840 -80 {lab=vss_3v3}
N 800 -60 840 -60 {lab=vss_3v3}
N 800 -40 840 -40 {lab=vss_3v3}
N 800 20 840 20 {lab=vss_3v3}
N 800 40 840 40 {lab=vss_3v3}
N 800 60 840 60 {lab=vss_3v3}
N 800 140 840 140 {lab=vss_3v3}
N 800 -80 800 520 {lab=vss_3v3}
N 660 -100 840 -100 {lab=ibg}
N 1040 -100 1100 -100 {lab=iprb}
N 1100 -100 1100 -330 {lab=iprb}
N 1100 -330 1200 -330 {lab=iprb}
N 1040 -40 1060 -40 {lab=isp}
N 1400 -310 1480 -310 {lab=vcm_rb}
N 1480 -310 1480 -560 {lab=vcm_rb}
N 1480 -560 1580 -560 {lab=vcm_rb}
N 1400 -290 1520 -290 {lab=vref_rb}
N 1520 -290 1520 -540 {lab=vref_rb}
N 1520 -540 1580 -540 {lab=vref_rb}
N 500 300 500 -120 {lab=en}
N 500 -120 540 -120 {lab=en}
N 480 340 480 -80 {lab=en_b}
N 480 -80 540 -80 {lab=en_b}
N 720 300 720 -140 {lab=en}
N 720 -140 840 -140 {lab=en}
N 700 340 700 -120 {lab=en_b}
N 700 -120 840 -120 {lab=en_b}
N 1160 300 1160 -310 {lab=en}
N 1160 -310 1200 -310 {lab=en}
N 1140 340 1140 -290 {lab=en_b}
N 1140 -290 1200 -290 {lab=en_b}
N 1900 -880 1900 -60 {lab=s7_an_1_iref}
N 1040 -60 1900 -60 {lab=s7_an_1_iref}
N 1900 -880 2620 -880 {lab=s7_an_1_iref}
N 1940 -700 1940 -620 {lab=s7_an_1_vinp}
N 1820 -620 1940 -620 {lab=s7_an_1_vinp}
N 1940 -700 2620 -700 {lab=s7_an_1_vinp}
N 1980 -760 1980 -600 {lab=s7_an_1_vinn}
N 1820 -600 1980 -600 {lab=s7_an_1_vinn}
N 1980 -760 2620 -760 {lab=s7_an_1_vinn}
N 2020 -640 2020 -80 {lab=s7_an_0_iref}
N 1040 -80 2020 -80 {lab=s7_an_0_iref}
N 2020 -640 2620 -640 {lab=s7_an_0_iref}
N 2060 -540 2060 440 {lab=vref}
N 1820 -540 2060 -540 {lab=vref}
N 2060 -280 2470 -280 {lab=vref}
N 2530 -280 2620 -280 {lab=s7_an_0_vref}
N 230 440 2060 440 {lab=vref}
N 2100 -660 2100 -400 {lab=s7_an_0_outn}
N 1820 -660 2100 -660 {lab=s7_an_0_outn}
N 2100 -400 2620 -400 {lab=s7_an_0_outn}
N 2140 -680 2140 -340 {lab=s7_an_0_outp}
N 1820 -680 2140 -680 {lab=s7_an_0_outp}
N 2140 -340 2620 -340 {lab=s7_an_0_outp}
N 2180 -1000 2180 300 {lab=en}
N 1820 -800 2180 -800 {lab=en}
N 2180 -1000 2470 -1000 {lab=en}
N 2530 -1000 2620 -1000 {lab=s7_an_1_en_3v3}
N 2180 -520 2370 -520 {lab=en}
N 2430 -520 2620 -520 {lab=s7_an_0_en_3v3}
N 500 300 2180 300 {lab=en}
N 2220 -940 2220 340 {lab=en_b}
N 1820 -780 2220 -780 {lab=en_b}
N 2220 -940 2370 -940 {lab=en_b}
N 2430 -940 2620 -940 {lab=s7_an_1_en_3v3_b}
N 2220 -580 2470 -580 {lab=en_b}
N 2530 -580 2620 -580 {lab=s7_an_0_en_3v3_b}
N 480 340 2220 340 {lab=en_b}
N 2260 -820 2260 400 {lab=vcm}
N 1820 -560 2260 -560 {lab=vcm}
N 2260 -820 2470 -820 {lab=vcm}
N 2530 -820 2620 -820 {lab=s7_an_1_vref}
N 2260 -460 2470 -460 {lab=vcm}
N 2530 -460 2620 -460 {lab=s7_an_0_vcm}
N 150 400 2260 400 {lab=vcm}
N 90 400 60 400 {lab=analog_bus2}
N 170 440 60 440 {lab=analog_bus3}
C {devices/iopin.sym} 60 -1100 0 1 {name=p_vdd_3v3 lab=vdd_3v3}
C {devices/iopin.sym} 60 520 0 1 {name=p_vss_3v3 lab=vss_3v3}
C {devices/ipin.sym} 60 -800 0 0 {name=p_enable lab=enable}
C {devices/ipin.sym} 60 -760 0 0 {name=p_dig_in0 lab=dig_in0}
C {devices/ipin.sym} 60 -740 0 0 {name=p_dig_in1 lab=dig_in1}
C {devices/ipin.sym} 60 -720 0 0 {name=p_dig_in2 lab=dig_in2}
C {devices/ipin.sym} 60 -700 0 0 {name=p_dig_in3 lab=dig_in3}
C {devices/ipin.sym} 60 -680 0 0 {name=p_dig_in4 lab=dig_in4}
C {devices/ipin.sym} 60 -660 0 0 {name=p_dig_in5 lab=dig_in5}
C {devices/iopin.sym} 60 -620 0 1 {name=p_analog_bus0 lab=analog_bus0}
C {devices/iopin.sym} 60 -600 0 1 {name=p_analog_bus1 lab=analog_bus1}
C {devices/iopin.sym} 60 400 0 1 {name=p_analog_bus2 lab=analog_bus2}
C {devices/iopin.sym} 60 440 0 1 {name=p_analog_bus3 lab=analog_bus3}
C {devices/iopin.sym} 2620 -280 0 0 {name=p_s7_an_0_vref lab=s7_an_0_vref}
C {devices/iopin.sym} 2620 -340 0 0 {name=p_s7_an_0_outp lab=s7_an_0_outp}
C {devices/iopin.sym} 2620 -400 0 0 {name=p_s7_an_0_outn lab=s7_an_0_outn}
C {devices/iopin.sym} 2620 -460 0 0 {name=p_s7_an_0_vcm lab=s7_an_0_vcm}
C {devices/opin.sym} 2620 -520 0 0 {name=p_s7_an_0_en_3v3 lab=s7_an_0_en_3v3}
C {devices/opin.sym} 2620 -580 0 0 {name=p_s7_an_0_en_3v3_b lab=s7_an_0_en_3v3_b}
C {devices/opin.sym} 2620 -640 0 0 {name=p_s7_an_0_iref lab=s7_an_0_iref}
C {devices/iopin.sym} 2620 -700 0 0 {name=p_s7_an_1_vinp lab=s7_an_1_vinp}
C {devices/iopin.sym} 2620 -760 0 0 {name=p_s7_an_1_vinn lab=s7_an_1_vinn}
C {devices/iopin.sym} 2620 -820 0 0 {name=p_s7_an_1_vref lab=s7_an_1_vref}
C {devices/opin.sym} 2620 -880 0 0 {name=p_s7_an_1_iref lab=s7_an_1_iref}
C {devices/opin.sym} 2620 -940 0 0 {name=p_s7_an_1_en_3v3_b lab=s7_an_1_en_3v3_b}
C {devices/opin.sym} 2620 -1000 0 0 {name=p_s7_an_1_en_3v3 lab=s7_an_1_en_3v3}
C {devices/opin.sym} 60 -520 0 1 {name=p_dig_out0 lab=dig_out0}
C {devices/opin.sym} 60 -500 0 1 {name=p_dig_out1 lab=dig_out1}
C {devices/opin.sym} 60 -480 0 1 {name=p_dig_out2 lab=dig_out2}
C {devices/opin.sym} 60 -460 0 1 {name=p_dig_out3 lab=dig_out3}
C {devices/opin.sym} 60 -440 0 1 {name=p_dig_out4 lab=dig_out4}
C {devices/opin.sym} 60 -420 0 1 {name=p_dig_out5 lab=dig_out5}
C {devices/opin.sym} 60 -400 0 1 {name=p_dig_out6 lab=dig_out6}
C {devices/opin.sym} 60 -380 0 1 {name=p_dig_out7 lab=dig_out7}
C {devices/opin.sym} 60 -360 0 1 {name=p_dig_out8 lab=dig_out8}
C {devices/opin.sym} 60 -340 0 1 {name=p_dig_out9 lab=dig_out9}
C {devices/opin.sym} 60 -320 0 1 {name=p_dig_out10 lab=dig_out10}
C {devices/opin.sym} 60 -300 0 1 {name=p_dig_out11 lab=dig_out11}
C {devices/iopin.sym} 60 -1060 0 1 {name=p_vdd_1v2 lab=vdd_1v2}
C {devices/iopin.sym} 60 480 0 1 {name=p_vss_1v2 lab=vss_1v2}
C {s7_ctrl.sym} 1700 -600 0 0 {name=XC}
C {bg_core_pd.sym} 600 -100 0 0 {name=XBG}
C {bias_dist_pd.sym} 940 0 0 0 {name=XD}
C {pad_ref_rb.sym} 1300 -300 0 0 {name=XR}
C {s7_doutpd.sym} 260 -400 0 0 {name=XDO}
C {devices/lab_wire.sym} 690 -100 0 0 {name=l1 sig_type=std_logic lab=ibg}
C {devices/lab_wire.sym} 1090 -100 0 0 {name=l2 sig_type=std_logic lab=iprb}
C {devices/lab_pin.sym} 1060 -40 0 1 {name=l3 sig_type=std_logic lab=isp}
C {devices/lab_wire.sym} 1470 -310 0 0 {name=l4 sig_type=std_logic lab=vcm_rb}
C {devices/lab_wire.sym} 1450 -290 0 0 {name=l5 sig_type=std_logic lab=vref_rb}
C {devices/vsource.sym} 2500 -280 3 0 {name=Vsr0 value=0 savecurrent=false}
C {devices/vsource.sym} 2500 -1000 3 0 {name=Vse1 value=0 savecurrent=false}
C {devices/vsource.sym} 2400 -520 3 0 {name=Vse0 value=0 savecurrent=false}
C {devices/vsource.sym} 2400 -940 3 0 {name=Vseb1 value=0 savecurrent=false}
C {devices/vsource.sym} 2500 -580 3 0 {name=Vseb0 value=0 savecurrent=false}
C {devices/vsource.sym} 2500 -820 3 0 {name=Vsv1 value=0 savecurrent=false}
C {devices/vsource.sym} 2500 -460 3 0 {name=Vsv0 value=0 savecurrent=false}
C {devices/vsource.sym} 120 400 1 0 {name=Vsb2 value=0 savecurrent=false}
C {devices/vsource.sym} 200 440 1 0 {name=Vsb3 value=0 savecurrent=false}
C {devices/lab_wire.sym} 1400 300 0 0 {name=l6 sig_type=std_logic lab=en}
C {devices/lab_wire.sym} 1400 340 0 0 {name=l7 sig_type=std_logic lab=en_b}
C {devices/lab_wire.sym} 1400 400 0 0 {name=l8 sig_type=std_logic lab=vcm}
C {devices/lab_wire.sym} 1400 440 0 0 {name=l9 sig_type=std_logic lab=vref}
C {devices/lab_wire.sym} 1880 -800 0 0 {name=l10 sig_type=std_logic lab=en}
C {devices/lab_wire.sym} 1880 -780 0 0 {name=l11 sig_type=std_logic lab=en_b}
C {devices/lab_wire.sym} 1880 -560 0 0 {name=l12 sig_type=std_logic lab=vcm}
C {devices/lab_wire.sym} 1880 -540 0 0 {name=l13 sig_type=std_logic lab=vref}
C {devices/title.sym} 160 620 0 0 {name=l0 author="Christoph Maier"}
