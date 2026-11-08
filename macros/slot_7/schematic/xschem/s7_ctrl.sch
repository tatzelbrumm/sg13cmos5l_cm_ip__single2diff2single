v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {s7_ctrl: mode control and switch matrix of slot 7 (tier 1, 2026-11-08)} 0 -2420 0 0 0.4 0.4 {}
T {Every harness bit (enable, dig_in0..5) is shifted to 3.3 V by one ls_up_fs (no 1.2 V supply; ~50 nA while its input is 1).} 40 -2360 0 0 0.25 0.25 {}
T {en / en_b = enable at 3.3 V (master enable of the slot); with en = 0 all switches are off.} 40 -2336 0 0 0.25 0.25 {}
T {Key: valid = d3 AND NOT d4 (k1, k0_b). s, m, f = swap / mon / feed qualified by valid; e_b = NOT (ext AND valid).} 40 -2312 0 0 0.25 0.25 {}
T {Switches (tg_hv, a -> b): ld: outp->vinp, outn->vinn | lx: outp->vinn, outn->vinp | sb: outp->bus0, outn->bus1} 40 -2288 0 0 0.25 0.25 {}
T {| bd: bus0->vinp, bus1->vinn | rc: vcm_rb->vcm_pad, vref_rb->vref_pad. vddh / vss: slot vdd_3v3 / vss_3v3.} 40 -2264 0 0 0.25 0.25 {}
T {Source: netlist/source/slot_7.spice (subckt s7_ctrl).} 40 -2240 0 0 0.25 0.25 {}
T {[L] level shifters (ls_up_fs)} 380 -2080 0 0 0.35 0.35 {layer=10}
T {[K] key and qualified bits} 840 -2080 0 0 0.35 0.35 {layer=10}
T {trunks} 1300 -2080 0 0 0.35 0.35 {layer=10}
T {[D] decode (nand2_hv, inv_hv)} 1720 -2080 0 0 0.35 0.35 {layer=10}
T {[M] switch matrix (tg_hv)} 2460 -2080 0 0 0.35 0.35 {layer=10}
T {Modes (dig_in, active only with the key dig_in3 = 1, dig_in4 = 0; otherwise the default):} 120 -440 0 0 0.28 0.28 {}
T {  dig_in0 swap: loop S2D -> D2S crossed (lx instead of ld)} 120 -410 0 0 0.28 0.28 {}
T {  dig_in1 mon:  S2D outp / outn -> analog_bus0 / 1 (sb), loop stays on} 120 -380 0 0 0.28 0.28 {}
T {  dig_in2 feed: analog_bus0 / 1 -> D2S vinp / vinn (bd), loop off; wins over swap and mon} 120 -350 0 0 0.28 0.28 {}
T {  dig_in5 ext:  pad_ref_rb disconnected (rc off), the pads take vcm / vref from analog_bus2 / 3} 120 -320 0 0 0.28 0.28 {}
T {Default (enable = 1, no key): loop direct (ld), bus0 / 1 disconnected, pad_ref_rb drives vcm / vref (rc).} 120 -290 0 0 0.28 0.28 {}
T {} 120 -260 0 0 0.28 0.28 {}
T {Decode (en and):} 120 -230 0 0 0.28 0.28 {}
T {  ld = en AND NOT f AND NOT s        lx = en AND NOT f AND s} 120 -200 0 0 0.28 0.28 {}
T {  sb = en AND m AND NOT f             bd = en AND f} 120 -170 0 0 0.28 0.28 {}
T {  rc = en AND NOT (ext AND valid)} 120 -140 0 0 0.28 0.28 {}
T {Unused shifter outputs: sw_b, mon_b, fd_b, k1_b, k0, ex_b.} 120 -110 0 0 0.28 0.28 {}
T {loop direct: ld = en & !f & !s} 1720 -1670 0 0 0.25 0.25 {layer=10}
T {loop crossed: lx = en & !f & s} 1720 -1150 0 0 0.25 0.25 {layer=10}
T {S2D -> bus: sb = en & m & !f} 1720 -630 0 0 0.25 0.25 {layer=10}
T {bus -> D2S: bd = en & f} 1720 -110 0 0 0.25 0.25 {layer=10}
T {rb connect: rc = en & !(ex & valid)} 1720 410 0 0 0.25 0.25 {layer=10}
N 60 -2000 3080 -2000 {lab=vddh}
N 60 1160 3040 1160 {lab=vss}
N 420 -2000 420 -720 {lab=vddh}
N 1240 -1760 1240 1160 {lab=vss}
N 1640 -2000 1640 460 {lab=vddh}
N 1680 -1400 1680 1160 {lab=vss}
N 60 -1860 440 -1860 {lab=enable}
N 500 -1900 500 -1920 {lab=vddh}
N 540 -1780 540 -1760 {lab=vss}
N 540 -1760 1240 -1760 {lab=vss}
N 60 -1660 440 -1660 {lab=d0}
N 500 -1700 500 -1720 {lab=vddh}
N 540 -1580 540 -1560 {lab=vss}
N 540 -1560 1240 -1560 {lab=vss}
N 60 -1460 440 -1460 {lab=d1}
N 500 -1500 500 -1520 {lab=vddh}
N 540 -1380 540 -1360 {lab=vss}
N 540 -1360 1240 -1360 {lab=vss}
N 60 -1260 440 -1260 {lab=d2}
N 500 -1300 500 -1320 {lab=vddh}
N 540 -1180 540 -1160 {lab=vss}
N 540 -1160 1240 -1160 {lab=vss}
N 60 -1060 440 -1060 {lab=d3}
N 500 -1100 500 -1120 {lab=vddh}
N 540 -980 540 -960 {lab=vss}
N 540 -960 1240 -960 {lab=vss}
N 60 -860 440 -860 {lab=d4}
N 500 -900 500 -920 {lab=vddh}
N 540 -780 540 -760 {lab=vss}
N 540 -760 1240 -760 {lab=vss}
N 60 -660 440 -660 {lab=d5}
N 500 -700 500 -720 {lab=vddh}
N 540 -580 540 -560 {lab=vss}
N 540 -560 1240 -560 {lab=vss}
N 600 -1860 3440 -1860 {lab=en}
N 600 -1840 3440 -1840 {lab=en_b}
N 600 -1640 620 -1640 {lab=sw_b}
N 600 -1440 620 -1440 {lab=mon_b}
N 600 -1240 620 -1240 {lab=fd_b}
N 600 -1040 620 -1040 {lab=k1_b}
N 600 -860 620 -860 {lab=k0}
N 600 -640 620 -640 {lab=ex_b}
N 600 -1660 860 -1660 {lab=sw}
N 800 -1620 860 -1620 {lab=valid}
N 940 -1670 940 -1720 {lab=vddh}
N 920 -1610 920 -1560 {lab=vss}
N 980 -1640 1080 -1640 {lab=s_b}
N 1140 -1660 1140 -1720 {lab=vddh}
N 1120 -1620 1120 -1560 {lab=vss}
N 1000 -1640 1000 -1600 {lab=s_b}
N 1000 -1600 1360 -1600 {lab=s_b}
N 1160 -1640 1320 -1640 {lab=s}
N 600 -1460 860 -1460 {lab=mon}
N 800 -1420 860 -1420 {lab=valid}
N 940 -1470 940 -1520 {lab=vddh}
N 920 -1410 920 -1360 {lab=vss}
N 980 -1440 1080 -1440 {lab=m_b}
N 1140 -1460 1140 -1520 {lab=vddh}
N 1120 -1420 1120 -1360 {lab=vss}
N 1160 -1440 1400 -1440 {lab=m}
N 600 -1260 860 -1260 {lab=fd}
N 800 -1220 860 -1220 {lab=valid}
N 940 -1270 940 -1320 {lab=vddh}
N 920 -1210 920 -1160 {lab=vss}
N 980 -1240 1080 -1240 {lab=f_b}
N 1140 -1260 1140 -1320 {lab=vddh}
N 1120 -1220 1120 -1160 {lab=vss}
N 1000 -1240 1000 -1200 {lab=f_b}
N 1000 -1200 1480 -1200 {lab=f_b}
N 1160 -1240 1440 -1240 {lab=f}
N 600 -660 860 -660 {lab=ex}
N 800 -620 860 -620 {lab=valid}
N 940 -670 940 -720 {lab=vddh}
N 920 -610 920 -560 {lab=vss}
N 980 -640 1520 -640 {lab=e_b}
N 600 -1060 740 -1060 {lab=k1}
N 740 -1060 740 -880 {lab=k1}
N 740 -880 860 -880 {lab=k1}
N 600 -840 860 -840 {lab=k0_b}
N 980 -860 1080 -860 {lab=valid_b}
N 1160 -860 1180 -860 {lab=valid}
N 1180 -860 1180 -800 {lab=valid}
N 1180 -800 800 -800 {lab=valid}
N 940 -890 940 -920 {lab=vddh}
N 920 -830 920 -760 {lab=vss}
N 1140 -880 1140 -920 {lab=vddh}
N 1120 -840 1120 -760 {lab=vss}
N 800 -1620 800 -620 {lab=valid}
N 420 -1920 500 -1920 {lab=vddh}
N 420 -1720 1140 -1720 {lab=vddh}
N 420 -1520 1140 -1520 {lab=vddh}
N 420 -1320 1140 -1320 {lab=vddh}
N 420 -1120 500 -1120 {lab=vddh}
N 420 -920 1140 -920 {lab=vddh}
N 420 -720 940 -720 {lab=vddh}
N 1320 -1640 1320 -960 {lab=s}
N 1360 -1600 1360 -1480 {lab=s_b}
N 1400 -1440 1400 -480 {lab=m}
N 1440 -1240 1440 60 {lab=f}
N 1480 -1520 1480 -440 {lab=f_b}
N 1520 -640 1520 580 {lab=e_b}
N 1560 -1860 1560 540 {lab=en}
N 1480 -1520 1740 -1520 {lab=f_b}
N 1360 -1480 1740 -1480 {lab=s_b}
N 1860 -1500 1960 -1500 {lab=x1_b}
N 2040 -1500 2100 -1500 {lab=x1}
N 1560 -1580 2080 -1580 {lab=en}
N 2080 -1580 2080 -1540 {lab=en}
N 2080 -1540 2100 -1540 {lab=en}
N 2220 -1520 2280 -1520 {lab=ld_b}
N 1640 -1620 2340 -1620 {lab=vddh}
N 1680 -1400 2320 -1400 {lab=vss}
N 1820 -1530 1820 -1620 {lab=vddh}
N 1800 -1470 1800 -1400 {lab=vss}
N 2020 -1520 2020 -1620 {lab=vddh}
N 2000 -1480 2000 -1400 {lab=vss}
N 2180 -1550 2180 -1620 {lab=vddh}
N 2160 -1490 2160 -1400 {lab=vss}
N 2340 -1540 2340 -1620 {lab=vddh}
N 2320 -1500 2320 -1400 {lab=vss}
N 1480 -1000 1740 -1000 {lab=f_b}
N 1320 -960 1740 -960 {lab=s}
N 1860 -980 1960 -980 {lab=x2_b}
N 2040 -980 2100 -980 {lab=x2}
N 1560 -1060 2080 -1060 {lab=en}
N 2080 -1060 2080 -1020 {lab=en}
N 2080 -1020 2100 -1020 {lab=en}
N 2220 -1000 2280 -1000 {lab=lx_b}
N 1640 -1100 2340 -1100 {lab=vddh}
N 1680 -880 2320 -880 {lab=vss}
N 1820 -1010 1820 -1100 {lab=vddh}
N 1800 -950 1800 -880 {lab=vss}
N 2020 -1000 2020 -1100 {lab=vddh}
N 2000 -960 2000 -880 {lab=vss}
N 2180 -1030 2180 -1100 {lab=vddh}
N 2160 -970 2160 -880 {lab=vss}
N 2340 -1020 2340 -1100 {lab=vddh}
N 2320 -980 2320 -880 {lab=vss}
N 1400 -480 1740 -480 {lab=m}
N 1480 -440 1740 -440 {lab=f_b}
N 1860 -460 1960 -460 {lab=x3_b}
N 2040 -460 2100 -460 {lab=x3}
N 1560 -540 2080 -540 {lab=en}
N 2080 -540 2080 -500 {lab=en}
N 2080 -500 2100 -500 {lab=en}
N 2220 -480 2280 -480 {lab=sb_b}
N 1640 -580 2340 -580 {lab=vddh}
N 1680 -360 2320 -360 {lab=vss}
N 1820 -490 1820 -580 {lab=vddh}
N 1800 -430 1800 -360 {lab=vss}
N 2020 -480 2020 -580 {lab=vddh}
N 2000 -440 2000 -360 {lab=vss}
N 2180 -510 2180 -580 {lab=vddh}
N 2160 -450 2160 -360 {lab=vss}
N 2340 -500 2340 -580 {lab=vddh}
N 2320 -460 2320 -360 {lab=vss}
N 1560 20 2100 20 {lab=en}
N 1440 60 2100 60 {lab=f}
N 2220 40 2280 40 {lab=bd_b}
N 1640 -60 2340 -60 {lab=vddh}
N 1680 160 2320 160 {lab=vss}
N 2180 10 2180 -60 {lab=vddh}
N 2160 70 2160 160 {lab=vss}
N 2340 20 2340 -60 {lab=vddh}
N 2320 60 2320 160 {lab=vss}
N 1560 540 2100 540 {lab=en}
N 1520 580 2100 580 {lab=e_b}
N 2220 560 2280 560 {lab=rc_b}
N 1640 460 2340 460 {lab=vddh}
N 1680 680 2320 680 {lab=vss}
N 2180 530 2180 460 {lab=vddh}
N 2160 590 2160 680 {lab=vss}
N 2340 540 2340 460 {lab=vddh}
N 2320 580 2320 680 {lab=vss}
N 2360 -1520 2700 -1520 {lab=ld}
N 2700 -1520 2700 -1480 {lab=ld}
N 2400 -1520 2400 -1320 {lab=ld}
N 2400 -1320 2700 -1320 {lab=ld}
N 2700 -1320 2700 -1280 {lab=ld}
N 2240 -1520 2240 -1160 {lab=ld_b}
N 2240 -1160 2700 -1160 {lab=ld_b}
N 2700 -1160 2700 -1200 {lab=ld_b}
N 2240 -1360 2700 -1360 {lab=ld_b}
N 2700 -1360 2700 -1400 {lab=ld_b}
N 2730 -1480 2730 -1500 {lab=vddh}
N 2730 -1500 2780 -1500 {lab=vddh}
N 2730 -1400 2730 -1380 {lab=vss}
N 2730 -1380 2820 -1380 {lab=vss}
N 2730 -1280 2730 -1300 {lab=vddh}
N 2730 -1300 2780 -1300 {lab=vddh}
N 2730 -1200 2730 -1180 {lab=vss}
N 2730 -1180 2820 -1180 {lab=vss}
N 2660 -1440 2480 -1440 {lab=outp}
N 2740 -1440 2880 -1440 {lab=vinp}
N 2660 -1240 2520 -1240 {lab=outn}
N 2740 -1240 2920 -1240 {lab=vinn}
N 2360 -1000 2700 -1000 {lab=lx}
N 2700 -1000 2700 -960 {lab=lx}
N 2400 -1000 2400 -800 {lab=lx}
N 2400 -800 2700 -800 {lab=lx}
N 2700 -800 2700 -760 {lab=lx}
N 2240 -1000 2240 -640 {lab=lx_b}
N 2240 -640 2700 -640 {lab=lx_b}
N 2700 -640 2700 -680 {lab=lx_b}
N 2240 -840 2700 -840 {lab=lx_b}
N 2700 -840 2700 -880 {lab=lx_b}
N 2730 -960 2730 -980 {lab=vddh}
N 2730 -980 2780 -980 {lab=vddh}
N 2730 -880 2730 -860 {lab=vss}
N 2730 -860 2820 -860 {lab=vss}
N 2730 -760 2730 -780 {lab=vddh}
N 2730 -780 2780 -780 {lab=vddh}
N 2730 -680 2730 -660 {lab=vss}
N 2730 -660 2820 -660 {lab=vss}
N 2660 -920 2480 -920 {lab=outp}
N 2740 -920 2920 -920 {lab=vinn}
N 2660 -720 2520 -720 {lab=outn}
N 2740 -720 2880 -720 {lab=vinp}
N 2360 -480 2700 -480 {lab=sb}
N 2700 -480 2700 -440 {lab=sb}
N 2400 -480 2400 -280 {lab=sb}
N 2400 -280 2700 -280 {lab=sb}
N 2700 -280 2700 -240 {lab=sb}
N 2240 -480 2240 -120 {lab=sb_b}
N 2240 -120 2700 -120 {lab=sb_b}
N 2700 -120 2700 -160 {lab=sb_b}
N 2240 -320 2700 -320 {lab=sb_b}
N 2700 -320 2700 -360 {lab=sb_b}
N 2730 -440 2730 -460 {lab=vddh}
N 2730 -460 2780 -460 {lab=vddh}
N 2730 -360 2730 -340 {lab=vss}
N 2730 -340 2820 -340 {lab=vss}
N 2730 -240 2730 -260 {lab=vddh}
N 2730 -260 2780 -260 {lab=vddh}
N 2730 -160 2730 -140 {lab=vss}
N 2730 -140 2820 -140 {lab=vss}
N 2660 -400 2480 -400 {lab=outp}
N 2740 -400 3280 -400 {lab=bus0}
N 2660 -200 2520 -200 {lab=outn}
N 2740 -200 3320 -200 {lab=bus1}
N 2360 40 3160 40 {lab=bd}
N 3160 40 3160 80 {lab=bd}
N 2400 40 2400 240 {lab=bd}
N 2400 240 3160 240 {lab=bd}
N 3160 240 3160 280 {lab=bd}
N 2240 40 2240 400 {lab=bd_b}
N 2240 400 3160 400 {lab=bd_b}
N 3160 400 3160 360 {lab=bd_b}
N 2240 200 3160 200 {lab=bd_b}
N 3160 200 3160 160 {lab=bd_b}
N 3130 80 3130 60 {lab=vddh}
N 3130 60 3080 60 {lab=vddh}
N 3130 160 3130 180 {lab=vss}
N 3130 180 3040 180 {lab=vss}
N 3130 280 3130 260 {lab=vddh}
N 3130 260 3080 260 {lab=vddh}
N 3130 360 3130 380 {lab=vss}
N 3130 380 3040 380 {lab=vss}
N 3200 120 3280 120 {lab=bus0}
N 3120 120 2880 120 {lab=vinp}
N 3200 320 3320 320 {lab=bus1}
N 3120 320 2920 320 {lab=vinn}
N 2360 560 2700 560 {lab=rc}
N 2700 560 2700 600 {lab=rc}
N 2400 560 2400 760 {lab=rc}
N 2400 760 2700 760 {lab=rc}
N 2700 760 2700 800 {lab=rc}
N 2240 560 2240 920 {lab=rc_b}
N 2240 920 2700 920 {lab=rc_b}
N 2700 920 2700 880 {lab=rc_b}
N 2240 720 2700 720 {lab=rc_b}
N 2700 720 2700 680 {lab=rc_b}
N 2730 600 2730 580 {lab=vddh}
N 2730 580 2780 580 {lab=vddh}
N 2730 680 2730 700 {lab=vss}
N 2730 700 2820 700 {lab=vss}
N 2730 800 2730 780 {lab=vddh}
N 2730 780 2780 780 {lab=vddh}
N 2730 880 2730 900 {lab=vss}
N 2730 900 2820 900 {lab=vss}
N 2660 640 2560 640 {lab=vcm_rb}
N 2740 640 2960 640 {lab=vcm_pad}
N 2660 840 2600 840 {lab=vref_rb}
N 2740 840 3000 840 {lab=vref_pad}
N 2480 -1760 2480 -400 {lab=outp}
N 2480 -1760 3440 -1760 {lab=outp}
N 2520 -1720 2520 -200 {lab=outn}
N 2520 -1720 3440 -1720 {lab=outn}
N 2560 640 2560 980 {lab=vcm_rb}
N 2560 980 3440 980 {lab=vcm_rb}
N 2600 840 2600 1020 {lab=vref_rb}
N 2600 1020 3440 1020 {lab=vref_rb}
N 2880 -1680 2880 120 {lab=vinp}
N 2880 -1680 3440 -1680 {lab=vinp}
N 2920 -1640 2920 320 {lab=vinn}
N 2920 -1640 3440 -1640 {lab=vinn}
N 2960 640 2960 1060 {lab=vcm_pad}
N 2960 1060 3440 1060 {lab=vcm_pad}
N 3000 840 3000 1100 {lab=vref_pad}
N 3000 1100 3440 1100 {lab=vref_pad}
N 3280 -1600 3280 120 {lab=bus0}
N 3280 -1600 3440 -1600 {lab=bus0}
N 3320 -1560 3320 320 {lab=bus1}
N 3320 -1560 3440 -1560 {lab=bus1}
N 2780 -2000 2780 780 {lab=vddh}
N 2820 -1380 2820 1160 {lab=vss}
N 3080 -2000 3080 260 {lab=vddh}
N 3040 180 3040 1160 {lab=vss}
C {devices/iopin.sym} 60 -2000 0 1 {name=p_vddh lab=vddh}
C {devices/iopin.sym} 60 1160 0 1 {name=p_vss lab=vss}
C {devices/ipin.sym} 60 -1860 0 0 {name=p_enable lab=enable}
C {devices/ipin.sym} 60 -1660 0 0 {name=p_d0 lab=d0}
C {devices/ipin.sym} 60 -1460 0 0 {name=p_d1 lab=d1}
C {devices/ipin.sym} 60 -1260 0 0 {name=p_d2 lab=d2}
C {devices/ipin.sym} 60 -1060 0 0 {name=p_d3 lab=d3}
C {devices/ipin.sym} 60 -860 0 0 {name=p_d4 lab=d4}
C {devices/ipin.sym} 60 -660 0 0 {name=p_d5 lab=d5}
C {devices/opin.sym} 3440 -1860 0 0 {name=p_en lab=en}
C {devices/opin.sym} 3440 -1840 0 0 {name=p_en_b lab=en_b}
C {devices/iopin.sym} 3440 -1760 0 0 {name=p_outp lab=outp}
C {devices/iopin.sym} 3440 -1720 0 0 {name=p_outn lab=outn}
C {devices/iopin.sym} 3440 -1680 0 0 {name=p_vinp lab=vinp}
C {devices/iopin.sym} 3440 -1640 0 0 {name=p_vinn lab=vinn}
C {devices/iopin.sym} 3440 -1600 0 0 {name=p_bus0 lab=bus0}
C {devices/iopin.sym} 3440 -1560 0 0 {name=p_bus1 lab=bus1}
C {devices/iopin.sym} 3440 980 0 0 {name=p_vcm_rb lab=vcm_rb}
C {devices/iopin.sym} 3440 1020 0 0 {name=p_vref_rb lab=vref_rb}
C {devices/iopin.sym} 3440 1060 0 0 {name=p_vcm_pad lab=vcm_pad}
C {devices/iopin.sym} 3440 1100 0 0 {name=p_vref_pad lab=vref_pad}
C {ls_up_fs.sym} 520 -1840 0 0 {name=XLE}
C {ls_up_fs.sym} 520 -1640 0 0 {name=XL0}
C {ls_up_fs.sym} 520 -1440 0 0 {name=XL1}
C {ls_up_fs.sym} 520 -1240 0 0 {name=XL2}
C {ls_up_fs.sym} 520 -1040 0 0 {name=XL3}
C {ls_up_fs.sym} 520 -840 0 0 {name=XL4}
C {ls_up_fs.sym} 520 -640 0 0 {name=XL5}
C {devices/lab_wire.sym} 760 -1860 0 0 {name=l1 sig_type=std_logic lab=en}
C {devices/lab_wire.sym} 760 -1840 0 0 {name=l2 sig_type=std_logic lab=en_b}
C {devices/lab_pin.sym} 620 -1640 0 1 {name=l3 sig_type=std_logic lab=sw_b}
C {devices/lab_pin.sym} 620 -1440 0 1 {name=l4 sig_type=std_logic lab=mon_b}
C {devices/lab_pin.sym} 620 -1240 0 1 {name=l5 sig_type=std_logic lab=fd_b}
C {devices/lab_pin.sym} 620 -1040 0 1 {name=l6 sig_type=std_logic lab=k1_b}
C {devices/lab_pin.sym} 620 -860 0 1 {name=l7 sig_type=std_logic lab=k0}
C {devices/lab_pin.sym} 620 -640 0 1 {name=l8 sig_type=std_logic lab=ex_b}
C {nand2_hv.sym} 920 -1640 0 0 {name=XNS}
C {devices/lab_wire.sym} 700 -1660 0 0 {name=l9 sig_type=std_logic lab=sw}
C {inv_hv.sym} 1120 -1640 0 0 {name=XIS}
C {devices/lab_wire.sym} 1060 -1640 0 0 {name=l10 sig_type=std_logic lab=s_b}
C {devices/lab_wire.sym} 1220 -1640 0 0 {name=l11 sig_type=std_logic lab=s}
C {nand2_hv.sym} 920 -1440 0 0 {name=XNM}
C {devices/lab_wire.sym} 700 -1460 0 0 {name=l12 sig_type=std_logic lab=mon}
C {inv_hv.sym} 1120 -1440 0 0 {name=XIM}
C {devices/lab_wire.sym} 1060 -1440 0 0 {name=l13 sig_type=std_logic lab=m_b}
C {devices/lab_wire.sym} 1220 -1440 0 0 {name=l14 sig_type=std_logic lab=m}
C {nand2_hv.sym} 920 -1240 0 0 {name=XNF}
C {devices/lab_wire.sym} 700 -1260 0 0 {name=l15 sig_type=std_logic lab=fd}
C {inv_hv.sym} 1120 -1240 0 0 {name=XIF}
C {devices/lab_wire.sym} 1060 -1240 0 0 {name=l16 sig_type=std_logic lab=f_b}
C {devices/lab_wire.sym} 1220 -1240 0 0 {name=l17 sig_type=std_logic lab=f}
C {nand2_hv.sym} 920 -640 0 0 {name=XNE}
C {devices/lab_wire.sym} 700 -660 0 0 {name=l18 sig_type=std_logic lab=ex}
C {devices/lab_wire.sym} 1100 -640 0 0 {name=l19 sig_type=std_logic lab=e_b}
C {nand2_hv.sym} 920 -860 0 0 {name=XNV}
C {inv_hv.sym} 1120 -860 0 0 {name=XIV}
C {devices/lab_wire.sym} 700 -1060 0 0 {name=l20 sig_type=std_logic lab=k1}
C {devices/lab_wire.sym} 700 -840 0 0 {name=l21 sig_type=std_logic lab=k0_b}
C {devices/lab_wire.sym} 1060 -860 0 0 {name=l22 sig_type=std_logic lab=valid_b}
C {devices/lab_wire.sym} 1060 -800 0 0 {name=l23 sig_type=std_logic lab=valid}
C {nand2_hv.sym} 1800 -1500 0 0 {name=XN1}
C {inv_hv.sym} 2000 -1500 0 0 {name=XI1}
C {devices/lab_wire.sym} 1940 -1500 0 0 {name=l24 sig_type=std_logic lab=x1_b}
C {nand2_hv.sym} 2160 -1520 0 0 {name=XNLD}
C {devices/lab_wire.sym} 2090 -1500 0 0 {name=l25 sig_type=std_logic lab=x1}
C {inv_hv.sym} 2320 -1520 0 0 {name=XILD}
C {nand2_hv.sym} 1800 -980 0 0 {name=XN2}
C {inv_hv.sym} 2000 -980 0 0 {name=XI2}
C {devices/lab_wire.sym} 1940 -980 0 0 {name=l26 sig_type=std_logic lab=x2_b}
C {nand2_hv.sym} 2160 -1000 0 0 {name=XNLX}
C {devices/lab_wire.sym} 2090 -980 0 0 {name=l27 sig_type=std_logic lab=x2}
C {inv_hv.sym} 2320 -1000 0 0 {name=XILX}
C {nand2_hv.sym} 1800 -460 0 0 {name=XN3}
C {inv_hv.sym} 2000 -460 0 0 {name=XI3}
C {devices/lab_wire.sym} 1940 -460 0 0 {name=l28 sig_type=std_logic lab=x3_b}
C {nand2_hv.sym} 2160 -480 0 0 {name=XNSB}
C {devices/lab_wire.sym} 2090 -460 0 0 {name=l29 sig_type=std_logic lab=x3}
C {inv_hv.sym} 2320 -480 0 0 {name=XISB}
C {nand2_hv.sym} 2160 40 0 0 {name=XNBD}
C {inv_hv.sym} 2320 40 0 0 {name=XIBD}
C {nand2_hv.sym} 2160 560 0 0 {name=XNRC}
C {inv_hv.sym} 2320 560 0 0 {name=XIRC}
C {tg_hv.sym} 2700 -1440 0 0 {name=XT1}
C {tg_hv.sym} 2700 -1240 0 0 {name=XT2}
C {devices/lab_wire.sym} 2640 -1520 0 0 {name=l30 sig_type=std_logic lab=ld}
C {devices/lab_wire.sym} 2640 -1360 0 0 {name=l31 sig_type=std_logic lab=ld_b}
C {devices/lab_wire.sym} 2650 -1440 0 0 {name=l32 sig_type=std_logic lab=outp}
C {devices/lab_wire.sym} 2870 -1440 0 0 {name=l33 sig_type=std_logic lab=vinp}
C {devices/lab_wire.sym} 2650 -1240 0 0 {name=l34 sig_type=std_logic lab=outn}
C {devices/lab_wire.sym} 2870 -1240 0 0 {name=l35 sig_type=std_logic lab=vinn}
C {tg_hv.sym} 2700 -920 0 0 {name=XT3}
C {tg_hv.sym} 2700 -720 0 0 {name=XT4}
C {devices/lab_wire.sym} 2640 -1000 0 0 {name=l36 sig_type=std_logic lab=lx}
C {devices/lab_wire.sym} 2640 -840 0 0 {name=l37 sig_type=std_logic lab=lx_b}
C {devices/lab_wire.sym} 2650 -920 0 0 {name=l38 sig_type=std_logic lab=outp}
C {devices/lab_wire.sym} 2870 -920 0 0 {name=l39 sig_type=std_logic lab=vinn}
C {devices/lab_wire.sym} 2650 -720 0 0 {name=l40 sig_type=std_logic lab=outn}
C {devices/lab_wire.sym} 2870 -720 0 0 {name=l41 sig_type=std_logic lab=vinp}
C {tg_hv.sym} 2700 -400 0 0 {name=XT5}
C {tg_hv.sym} 2700 -200 0 0 {name=XT6}
C {devices/lab_wire.sym} 2640 -480 0 0 {name=l42 sig_type=std_logic lab=sb}
C {devices/lab_wire.sym} 2640 -320 0 0 {name=l43 sig_type=std_logic lab=sb_b}
C {devices/lab_wire.sym} 2650 -400 0 0 {name=l44 sig_type=std_logic lab=outp}
C {devices/lab_wire.sym} 2870 -400 0 0 {name=l45 sig_type=std_logic lab=bus0}
C {devices/lab_wire.sym} 2650 -200 0 0 {name=l46 sig_type=std_logic lab=outn}
C {devices/lab_wire.sym} 2870 -200 0 0 {name=l47 sig_type=std_logic lab=bus1}
C {tg_hv.sym} 3160 120 0 1 {name=XT7}
C {tg_hv.sym} 3160 320 0 1 {name=XT8}
C {devices/lab_wire.sym} 3030 40 0 0 {name=l48 sig_type=std_logic lab=bd}
C {devices/lab_wire.sym} 3030 200 0 0 {name=l49 sig_type=std_logic lab=bd_b}
C {devices/lab_wire.sym} 3270 120 0 0 {name=l50 sig_type=std_logic lab=bus0}
C {devices/lab_wire.sym} 3030 120 0 0 {name=l51 sig_type=std_logic lab=vinp}
C {devices/lab_wire.sym} 3270 320 0 0 {name=l52 sig_type=std_logic lab=bus1}
C {devices/lab_wire.sym} 3030 320 0 0 {name=l53 sig_type=std_logic lab=vinn}
C {tg_hv.sym} 2700 640 0 0 {name=XT9}
C {tg_hv.sym} 2700 840 0 0 {name=XT10}
C {devices/lab_wire.sym} 2640 560 0 0 {name=l54 sig_type=std_logic lab=rc}
C {devices/lab_wire.sym} 2640 720 0 0 {name=l55 sig_type=std_logic lab=rc_b}
C {devices/lab_wire.sym} 2650 640 0 0 {name=l56 sig_type=std_logic lab=vcm_rb}
C {devices/lab_wire.sym} 2650 840 0 0 {name=l57 sig_type=std_logic lab=vref_rb}
C {devices/title.sym} 160 1260 0 0 {name=l0 author="Christoph Maier"}
