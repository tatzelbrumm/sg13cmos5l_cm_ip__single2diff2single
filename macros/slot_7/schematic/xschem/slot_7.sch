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
T {Source: netlist/source/slot_7.spice (subckt slot_7). Right edge: custom-pad nets in the order of the pad pins (pad 0 at the bottom).} 40 -1232 0 0 0.25 0.25 {}
N 60 -800 1280 -800 {lab=enable}
N 60 -760 1280 -760 {lab=dig_in0}
N 60 -740 1280 -740 {lab=dig_in1}
N 60 -720 1280 -720 {lab=dig_in2}
N 60 -700 1280 -700 {lab=dig_in3}
N 60 -680 1280 -680 {lab=dig_in4}
N 60 -660 1280 -660 {lab=dig_in5}
N 60 -620 1280 -620 {lab=analog_bus0}
N 60 -600 1280 -600 {lab=analog_bus1}
N 60 -1100 1380 -1100 {lab=vdd_3v3}
N 60 520 1420 520 {lab=vss_3v3}
N 1380 -860 1380 -1100 {lab=vdd_3v3}
N 320 -160 320 -1100 {lab=vdd_3v3}
N 620 -180 620 -1100 {lab=vdd_3v3}
N 1000 -370 1000 -1100 {lab=vdd_3v3}
N 1420 -480 1420 520 {lab=vss_3v3}
N 300 -40 300 520 {lab=vss_3v3}
N 660 180 660 520 {lab=vss_3v3}
N 1000 -230 1000 520 {lab=vss_3v3}
N 460 0 540 0 {lab=vdd_3v3}
N 460 80 540 80 {lab=vdd_3v3}
N 460 100 540 100 {lab=vdd_3v3}
N 460 120 540 120 {lab=vdd_3v3}
N 460 -1100 460 120 {lab=vdd_3v3}
N 500 -80 540 -80 {lab=vss_3v3}
N 500 -60 540 -60 {lab=vss_3v3}
N 500 -40 540 -40 {lab=vss_3v3}
N 500 20 540 20 {lab=vss_3v3}
N 500 40 540 40 {lab=vss_3v3}
N 500 60 540 60 {lab=vss_3v3}
N 500 140 540 140 {lab=vss_3v3}
N 500 -80 500 520 {lab=vss_3v3}
N 360 -100 540 -100 {lab=ibg}
N 740 -100 800 -100 {lab=iprb}
N 800 -100 800 -330 {lab=iprb}
N 800 -330 900 -330 {lab=iprb}
N 740 -40 760 -40 {lab=isp}
N 1100 -310 1180 -310 {lab=vcm_rb}
N 1180 -310 1180 -560 {lab=vcm_rb}
N 1180 -560 1280 -560 {lab=vcm_rb}
N 1100 -290 1220 -290 {lab=vref_rb}
N 1220 -290 1220 -540 {lab=vref_rb}
N 1220 -540 1280 -540 {lab=vref_rb}
N 200 300 200 -120 {lab=en}
N 200 -120 240 -120 {lab=en}
N 180 340 180 -80 {lab=en_b}
N 180 -80 240 -80 {lab=en_b}
N 420 300 420 -140 {lab=en}
N 420 -140 540 -140 {lab=en}
N 400 340 400 -120 {lab=en_b}
N 400 -120 540 -120 {lab=en_b}
N 860 300 860 -310 {lab=en}
N 860 -310 900 -310 {lab=en}
N 840 340 840 -290 {lab=en_b}
N 840 -290 900 -290 {lab=en_b}
N 1600 -880 1600 -60 {lab=s7_an_1_iref}
N 740 -60 1600 -60 {lab=s7_an_1_iref}
N 1600 -880 2320 -880 {lab=s7_an_1_iref}
N 1640 -700 1640 -620 {lab=s7_an_1_vinp}
N 1520 -620 1640 -620 {lab=s7_an_1_vinp}
N 1640 -700 2320 -700 {lab=s7_an_1_vinp}
N 1680 -760 1680 -600 {lab=s7_an_1_vinn}
N 1520 -600 1680 -600 {lab=s7_an_1_vinn}
N 1680 -760 2320 -760 {lab=s7_an_1_vinn}
N 1720 -640 1720 -80 {lab=s7_an_0_iref}
N 740 -80 1720 -80 {lab=s7_an_0_iref}
N 1720 -640 2320 -640 {lab=s7_an_0_iref}
N 1760 -540 1760 440 {lab=vref}
N 1520 -540 1760 -540 {lab=vref}
N 1760 -280 2170 -280 {lab=vref}
N 2230 -280 2320 -280 {lab=s7_an_0_vref}
N 230 440 1760 440 {lab=vref}
N 1800 -660 1800 -400 {lab=s7_an_0_outn}
N 1520 -660 1800 -660 {lab=s7_an_0_outn}
N 1800 -400 2320 -400 {lab=s7_an_0_outn}
N 1840 -680 1840 -340 {lab=s7_an_0_outp}
N 1520 -680 1840 -680 {lab=s7_an_0_outp}
N 1840 -340 2320 -340 {lab=s7_an_0_outp}
N 1880 -1000 1880 300 {lab=en}
N 1520 -800 1880 -800 {lab=en}
N 1880 -1000 2170 -1000 {lab=en}
N 2230 -1000 2320 -1000 {lab=s7_an_1_en_3v3}
N 1880 -520 2070 -520 {lab=en}
N 2130 -520 2320 -520 {lab=s7_an_0_en_3v3}
N 200 300 1880 300 {lab=en}
N 1920 -940 1920 340 {lab=en_b}
N 1520 -780 1920 -780 {lab=en_b}
N 1920 -940 2070 -940 {lab=en_b}
N 2130 -940 2320 -940 {lab=s7_an_1_en_3v3_b}
N 1920 -580 2170 -580 {lab=en_b}
N 2230 -580 2320 -580 {lab=s7_an_0_en_3v3_b}
N 180 340 1920 340 {lab=en_b}
N 1960 -820 1960 400 {lab=vcm}
N 1520 -560 1960 -560 {lab=vcm}
N 1960 -820 2170 -820 {lab=vcm}
N 2230 -820 2320 -820 {lab=s7_an_1_vref}
N 1960 -460 2170 -460 {lab=vcm}
N 2230 -460 2320 -460 {lab=s7_an_0_vcm}
N 150 400 1960 400 {lab=vcm}
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
C {devices/iopin.sym} 2320 -280 0 0 {name=p_s7_an_0_vref lab=s7_an_0_vref}
C {devices/iopin.sym} 2320 -340 0 0 {name=p_s7_an_0_outp lab=s7_an_0_outp}
C {devices/iopin.sym} 2320 -400 0 0 {name=p_s7_an_0_outn lab=s7_an_0_outn}
C {devices/iopin.sym} 2320 -460 0 0 {name=p_s7_an_0_vcm lab=s7_an_0_vcm}
C {devices/opin.sym} 2320 -520 0 0 {name=p_s7_an_0_en_3v3 lab=s7_an_0_en_3v3}
C {devices/opin.sym} 2320 -580 0 0 {name=p_s7_an_0_en_3v3_b lab=s7_an_0_en_3v3_b}
C {devices/opin.sym} 2320 -640 0 0 {name=p_s7_an_0_iref lab=s7_an_0_iref}
C {devices/iopin.sym} 2320 -700 0 0 {name=p_s7_an_1_vinp lab=s7_an_1_vinp}
C {devices/iopin.sym} 2320 -760 0 0 {name=p_s7_an_1_vinn lab=s7_an_1_vinn}
C {devices/iopin.sym} 2320 -820 0 0 {name=p_s7_an_1_vref lab=s7_an_1_vref}
C {devices/opin.sym} 2320 -880 0 0 {name=p_s7_an_1_iref lab=s7_an_1_iref}
C {devices/opin.sym} 2320 -940 0 0 {name=p_s7_an_1_en_3v3_b lab=s7_an_1_en_3v3_b}
C {devices/opin.sym} 2320 -1000 0 0 {name=p_s7_an_1_en_3v3 lab=s7_an_1_en_3v3}
C {s7_ctrl.sym} 1400 -600 0 0 {name=XC}
C {bg_core_pd.sym} 300 -100 0 0 {name=XBG}
C {bias_dist_pd.sym} 640 0 0 0 {name=XD}
C {pad_ref_rb.sym} 1000 -300 0 0 {name=XR}
C {devices/lab_wire.sym} 390 -100 0 0 {name=l1 sig_type=std_logic lab=ibg}
C {devices/lab_wire.sym} 790 -100 0 0 {name=l2 sig_type=std_logic lab=iprb}
C {devices/lab_pin.sym} 760 -40 0 1 {name=l3 sig_type=std_logic lab=isp}
C {devices/lab_wire.sym} 1170 -310 0 0 {name=l4 sig_type=std_logic lab=vcm_rb}
C {devices/lab_wire.sym} 1150 -290 0 0 {name=l5 sig_type=std_logic lab=vref_rb}
C {devices/vsource.sym} 2200 -280 3 0 {name=Vsr0 value=0 savecurrent=false}
C {devices/vsource.sym} 2200 -1000 3 0 {name=Vse1 value=0 savecurrent=false}
C {devices/vsource.sym} 2100 -520 3 0 {name=Vse0 value=0 savecurrent=false}
C {devices/vsource.sym} 2100 -940 3 0 {name=Vseb1 value=0 savecurrent=false}
C {devices/vsource.sym} 2200 -580 3 0 {name=Vseb0 value=0 savecurrent=false}
C {devices/vsource.sym} 2200 -820 3 0 {name=Vsv1 value=0 savecurrent=false}
C {devices/vsource.sym} 2200 -460 3 0 {name=Vsv0 value=0 savecurrent=false}
C {devices/vsource.sym} 120 400 1 0 {name=Vsb2 value=0 savecurrent=false}
C {devices/vsource.sym} 200 440 1 0 {name=Vsb3 value=0 savecurrent=false}
C {devices/lab_wire.sym} 1100 300 0 0 {name=l6 sig_type=std_logic lab=en}
C {devices/lab_wire.sym} 1100 340 0 0 {name=l7 sig_type=std_logic lab=en_b}
C {devices/lab_wire.sym} 1100 400 0 0 {name=l8 sig_type=std_logic lab=vcm}
C {devices/lab_wire.sym} 1100 440 0 0 {name=l9 sig_type=std_logic lab=vref}
C {devices/lab_wire.sym} 1580 -800 0 0 {name=l10 sig_type=std_logic lab=en}
C {devices/lab_wire.sym} 1580 -780 0 0 {name=l11 sig_type=std_logic lab=en_b}
C {devices/lab_wire.sym} 1580 -560 0 0 {name=l12 sig_type=std_logic lab=vcm}
C {devices/lab_wire.sym} 1580 -540 0 0 {name=l13 sig_type=std_logic lab=vref}
C {devices/title.sym} 160 620 0 0 {name=l0 author="Christoph Maier"}
