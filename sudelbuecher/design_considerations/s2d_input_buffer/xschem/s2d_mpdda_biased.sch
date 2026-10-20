v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {s2d_mpdda.sym} 700 0 0 0 {name=xs}
C {s2d_bias_lp.sym} 300 400 0 0 {name=xb}
N 520 -80 480 -80 {lab=vin}
C {devices/lab_pin.sym} 480 -80 0 0 {name=l1 sig_type=std_logic lab=vin}
N 520 -40 480 -40 {lab=vref}
C {devices/lab_pin.sym} 480 -40 0 0 {name=l2 sig_type=std_logic lab=vref}
N 520 0 480 0 {lab=vcm}
C {devices/lab_pin.sym} 480 0 0 0 {name=l3 sig_type=std_logic lab=vcm}
N 520 40 480 40 {lab=vfbp}
C {devices/lab_pin.sym} 480 40 0 0 {name=l4 sig_type=std_logic lab=vfbp}
N 520 80 480 80 {lab=vfbn}
C {devices/lab_pin.sym} 480 80 0 0 {name=l5 sig_type=std_logic lab=vfbn}
N 880 -80 920 -80 {lab=voutp}
C {devices/lab_pin.sym} 920 -80 0 1 {name=l6 sig_type=std_logic lab=voutp}
N 880 -40 920 -40 {lab=voutn}
C {devices/lab_pin.sym} 920 -40 0 1 {name=l7 sig_type=std_logic lab=voutn}
N 580 -140 580 -180 {lab=vdd}
C {devices/lab_pin.sym} 580 -180 0 1 {name=l8 sig_type=std_logic lab=vdd}
N 580 140 580 180 {lab=vss}
C {devices/lab_pin.sym} 580 180 0 1 {name=l9 sig_type=std_logic lab=vss}
N 620 140 620 180 {lab=vbp}
C {devices/lab_pin.sym} 620 180 0 1 {name=l10 sig_type=std_logic lab=vbp}
N 660 140 660 180 {lab=vbn}
C {devices/lab_pin.sym} 660 180 0 1 {name=l11 sig_type=std_logic lab=vbn}
N 700 140 700 180 {lab=vbpc}
C {devices/lab_pin.sym} 700 180 0 1 {name=l12 sig_type=std_logic lab=vbpc}
N 740 140 740 180 {lab=vbnc}
C {devices/lab_pin.sym} 740 180 0 1 {name=l13 sig_type=std_logic lab=vbnc}
N 420 340 460 340 {lab=vbp}
C {devices/lab_pin.sym} 460 340 0 1 {name=l14 sig_type=std_logic lab=vbp}
N 420 380 460 380 {lab=vbn}
C {devices/lab_pin.sym} 460 380 0 1 {name=l15 sig_type=std_logic lab=vbn}
N 420 420 460 420 {lab=vbpc}
C {devices/lab_pin.sym} 460 420 0 1 {name=l16 sig_type=std_logic lab=vbpc}
N 420 460 460 460 {lab=vbnc}
C {devices/lab_pin.sym} 460 460 0 1 {name=l17 sig_type=std_logic lab=vbnc}
N 240 280 240 240 {lab=vdd}
C {devices/lab_pin.sym} 240 240 0 1 {name=l18 sig_type=std_logic lab=vdd}
N 240 520 240 560 {lab=vss}
C {devices/lab_pin.sym} 240 560 0 1 {name=l19 sig_type=std_logic lab=vss}
C {devices/iopin.sym} 60 -240 0 1 {name=p20 lab=vdd}
C {devices/iopin.sym} 60 -200 0 1 {name=p21 lab=vss}
C {devices/ipin.sym} 60 -160 0 0 {name=p22 lab=vin}
C {devices/ipin.sym} 60 -120 0 0 {name=p23 lab=vref}
C {devices/ipin.sym} 60 -80 0 0 {name=p24 lab=vcm}
C {devices/opin.sym} 60 -40 0 0 {name=p25 lab=voutp}
C {devices/opin.sym} 60 0 0 0 {name=p26 lab=voutn}
C {devices/ipin.sym} 60 40 0 0 {name=p27 lab=vfbp}
C {devices/ipin.sym} 60 80 0 0 {name=p28 lab=vfbn}
C {devices/iopin.sym} 60 120 0 1 {name=p29 lab=vbp}
C {devices/iopin.sym} 60 160 0 1 {name=p30 lab=vbn}
C {devices/iopin.sym} 60 200 0 1 {name=p31 lab=vbpc}
C {devices/iopin.sym} 60 240 0 1 {name=p32 lab=vbnc}
T {s2d_mpdda + s2d_bias_lp test fixture (CACE DUT); bias nets are pins for bias-quality perturbation} 60 -340 0 0 0.4 0.4 {}
T {SPDX-FileCopyrightText: 2026 Christoph Maier   SPDX-License-Identifier: Apache-2.0} 60 640 0 0 0.2 0.2 {}

