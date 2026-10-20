
# CACE Summary for s2d_mpdda_biased

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Gain                 | ngspice              | Gain                 |            1.99 |    1.99844 |            2 |    1.99896 |         2.01 |    1.99931 |   Pass ✅    |
| Input offset (systematic) | ngspice              | Vos_in               |           -1 mV |  -0.000 mV |         0 mV |  -0.000 mV |         1 mV |   0.000 mV |   Pass ✅    |
| Integral nonlinearity | ngspice              | INL                  |             any |   0.075 mV |          any |   0.155 mV |         2 mV |   1.037 mV |   Pass ✅    |
| Output common-mode error | ngspice              | Vcm_err              |          -30 mV |   6.181 mV |          any |  12.175 mV |        30 mV |  21.145 mV |   Pass ✅    |
| Supply current       | ngspice              | Idd                  |             any | 112.444 uA |          any | 112.736 uA |       125 uA | 113.152 uA |   Pass ✅    |
| Gain vs vref and vcm | ngspice              | Gain                 |             any |    1.95131 |            2 |   1.997825 |          any |    2.03525 |   Pass ✅    |
| Integral nonlinearity vs vref and vcm | ngspice              | INL                  |             any |   0.173 mV |          any |   5.435 mV |          any | 168.168 mV |   Pass ✅    |
| Output common-mode error vs vref and vcm | ngspice              | Vcm_err              |             any |   4.629 mV |          any |   9.762 mV |          any |  16.937 mV |   Pass ✅    |
| Gain vs bias quality | ngspice              | Gain                 |            1.99 |    1.99876 |            2 |    1.99882 |         2.01 |    1.99894 |   Pass ✅    |
| Output common-mode error vs bias quality | ngspice              | Vcm_err              |          -30 mV | -24.871 mV |          any |   0.352 mV |        30 mV |  12.456 mV |   Pass ✅    |
| Supply current vs bias quality | ngspice              | Idd                  |             any | 112.281 uA |          any | 121.561 uA |       200 uA | 139.372 uA |   Pass ✅    |
| DC loop gain, differential | ngspice              | T0dm                 |           60 dB |  64.259 dB |          any |  65.384 dB |          any |  67.318 dB |   Pass ✅    |
| Crossover, differential | ngspice              | fcdm                 |             any |  0.146 MHz |          any |  1.048 MHz |          any |  3.260 MHz |   Pass ✅    |
| Phase margin, differential | ngspice              | PMdm                 |            60 ° |   86.054 ° |          any |   88.883 ° |          any |   89.887 ° |   Pass ✅    |
| Gain margin, differential | ngspice              | GMdm                 |           10 dB |  29.367 dB |          any |  40.072 dB |          any |  57.570 dB |   Pass ✅    |
| DC loop gain, common mode | ngspice              | T0cm                 |           50 dB |  64.443 dB |          any |  65.602 dB |          any |  67.623 dB |   Pass ✅    |
| Crossover, common mode | ngspice              | fccm                 |             any |  0.146 MHz |          any |  1.050 MHz |          any |  3.137 MHz |   Pass ✅    |
| Phase margin, common mode | ngspice              | PMcm                 |            55 ° |   61.979 ° |          any |   82.119 ° |          any |   89.077 ° |   Pass ✅    |
| Gain margin, common mode | ngspice              | GMcm                 |           10 dB |  14.419 dB |          any |  25.660 dB |          any |  43.659 dB |   Pass ✅    |
| Closed-loop gain at 1 kHz | ngspice              | Acl_dB               |             any |   6.015 dB |      6.02 dB |   6.016 dB |          any |   6.017 dB |   Pass ✅    |
| Closed-loop -3 dB bandwidth | ngspice              | f3dB                 |           1 MHz |  1.357 MHz |          any |  1.545 MHz |          any |  1.817 MHz |   Pass ✅    |
| Output common-mode response to vdd at 1 kHz | ngspice              | CMvdd_1k             |             any | -53.078 dB |          any | -51.148 dB |       -30 dB | -49.768 dB |   Pass ✅    |
| PSRR vdd at 1 kHz (input-referred), mismatch | ngspice              | PSRRp_1k             |           60 dB |  86.206 dB |          any | 100.215 dB |          any | 143.814 dB |   Pass ✅    |
| PSRR vdd at 100 kHz (input-referred), mismatch | ngspice              | PSRRp_100k           |             any |  83.528 dB |          any |  97.759 dB |          any | 113.378 dB |   Pass ✅    |
| PSRR vss at 1 kHz (input-referred), mismatch | ngspice              | PSRRn_1k             |           60 dB |  94.078 dB |          any | 102.065 dB |          any | 126.816 dB |   Pass ✅    |
| PSRR vss at 100 kHz (input-referred), mismatch | ngspice              | PSRRn_100k           |             any |  60.496 dB |          any |  72.553 dB |          any | 101.079 dB |   Pass ✅    |
| CMRR at 1 kHz (vin and vref together), mismatch | ngspice              | CMRR_1k              |           70 dB |  88.007 dB |          any | 103.549 dB |          any | 130.166 dB |   Pass ✅    |
| Rise time 10-90 %    | ngspice              | t_rise               |             any | 103.775 ns |          any | 169.845 ns |          any | 258.155 ns |   Pass ✅    |
| Settling time to 1 % | ngspice              | t_settle             |             any | 221.681 ns |          any | 359.808 ns |      1000 ns | 544.121 ns |   Pass ✅    |
| Overshoot            | ngspice              | Overshoot            |             any |    0.000 % |          any |    0.000 % |          5 % |    0.000 % |   Pass ✅    |
| Largest output common-mode deviation during the step | ngspice              | Vcm_dev              |             any |   9.364 mV |          any |  13.688 mV |        50 mV |  17.517 mV |   Pass ✅    |
| Input noise density at 1 kHz | ngspice              | En_1k                |             any | 588.471 nV/rtHz |          any | 670.381 nV/rtHz | 1000 nV/rtHz | 716.542 nV/rtHz |   Pass ✅    |
| Input noise density at 100 kHz | ngspice              | En_100k              |             any | 141.602 nV/rtHz |          any | 151.588 nV/rtHz |  250 nV/rtHz | 155.598 nV/rtHz |   Pass ✅    |
| Differential output noise, 10 Hz - 10 MHz | ngspice              | Vn_out               |             any | 424.172 uV |          any | 433.582 uV |      1000 uV | 438.073 uV |   Pass ✅    |
| Input offset - Mismatch | ngspice              | Vos_in               |          -20 mV | -16.902 mV |          any |  -1.025 mV |        20 mV |  14.859 mV |   Pass ✅    |
| Gain - Mismatch      | ngspice              | Gain                 |            1.93 |     1.9558 |          any |    1.99967 |         2.07 |    2.04236 |   Pass ✅    |
| Output common-mode error - Mismatch | ngspice              | Vcm_err              |          -60 mV | -17.715 mV |          any |  11.707 mV |        60 mV |  42.345 mV |   Pass ✅    |
| Input offset - Process MC | ngspice              | Vos_in               |           -5 mV |  -0.000 mV |          any |   0.000 mV |         5 mV |   0.000 mV |   Pass ✅    |
| Gain - Process MC    | ngspice              | Gain                 |            1.99 |    1.99892 |          any |    1.99894 |         2.01 |    1.99895 |   Pass ✅    |
| Output common-mode error - Process MC | ngspice              | Vcm_err              |          -30 mV |  12.079 mV |          any |  12.453 mV |        30 mV |  12.792 mV |   Pass ✅    |


## Plots

## INL_vs_vdd

![INL_vs_vdd](./s2d_mpdda_biased/schematic/INL_vs_vdd.png)

## INL_vs_temp

![INL_vs_temp](./s2d_mpdda_biased/schematic/INL_vs_temp.png)

## Gain_vs_corner_r

![Gain_vs_corner_r](./s2d_mpdda_biased/schematic/Gain_vs_corner_r.png)

## Vcm_err_vs_temp

![Vcm_err_vs_temp](./s2d_mpdda_biased/schematic/Vcm_err_vs_temp.png)

## Idd_vs_corner_mos

![Idd_vs_corner_mos](./s2d_mpdda_biased/schematic/Idd_vs_corner_mos.png)

## INL_vs_vcm

![INL_vs_vcm](./s2d_mpdda_biased/schematic/INL_vs_vcm.png)

## Gain_vs_vref

![Gain_vs_vref](./s2d_mpdda_biased/schematic/Gain_vs_vref.png)

## Idd_vs_ibias_err

![Idd_vs_ibias_err](./s2d_mpdda_biased/schematic/Idd_vs_ibias_err.png)

## Vcm_err_vs_ibias_err

![Vcm_err_vs_ibias_err](./s2d_mpdda_biased/schematic/Vcm_err_vs_ibias_err.png)

## PMcm_vs_cload

![PMcm_vs_cload](./s2d_mpdda_biased/schematic/PMcm_vs_cload.png)

## fcdm_vs_cload

![fcdm_vs_cload](./s2d_mpdda_biased/schematic/fcdm_vs_cload.png)

## PMcm_vs_temp

![PMcm_vs_temp](./s2d_mpdda_biased/schematic/PMcm_vs_temp.png)

## f3dB_vs_temp

![f3dB_vs_temp](./s2d_mpdda_biased/schematic/f3dB_vs_temp.png)

## t_settle_vs_cload

![t_settle_vs_cload](./s2d_mpdda_biased/schematic/t_settle_vs_cload.png)

## En_1k_vs_temp

![En_1k_vs_temp](./s2d_mpdda_biased/schematic/En_1k_vs_temp.png)
