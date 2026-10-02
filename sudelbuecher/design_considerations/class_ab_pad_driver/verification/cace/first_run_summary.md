<!-- First full CACE run, RUN_2026-10-02_02-08-20, in Claude's cloud container: CACE 2.11.0, ngspice 42 (OSDI 0.3), xschem 3.4.4, IHP-Open-PDK dev branch. Plots not copied. -->


# CACE Summary for d2s_miller_biased

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Gain                 | ngspice              | Gain                 |           0.485 |   0.476323 |          0.5 |   0.504009 |        0.515 |   0.553505 |   Fail ❌    |
| Output offset        | ngspice              | Vos_out              |           -5 mV |   0.106 mV |         0 mV |   0.196 mV |         5 mV |   4.006 mV |   Pass ✅    |
| Integral nonlinearity | ngspice              | INL                  |             any |   1.032 mV |          any |   6.100 mV |        10 mV | 469.095 mV |   Fail ❌    |
| Supply current       | ngspice              | Idd                  |             any | 406.269 uA |          any | 425.663 uA |       600 uA | 449.950 uA |   Pass ✅    |
| Output PMOS quiescent current | ngspice              | IqP                  |          100 uA | 218.270 uA |          any | 239.111 uA |       500 uA | 263.280 uA |   Pass ✅    |
| Output NMOS quiescent current | ngspice              | IqN                  |          100 uA | 217.048 uA |          any | 238.105 uA |       500 uA | 263.115 uA |   Pass ✅    |
| Minimum output device current | ngspice              | Imin                 |           20 uA |  12.308 uA |          any | 119.429 uA |          any | 144.472 uA |   Fail ❌    |
| Gain vs bias quality | ngspice              | Gain                 |           0.485 |   0.487291 |          0.5 |  0.5064955 |        0.515 |   0.555689 |   Fail ❌    |
| Output offset vs bias quality | ngspice              | Vos_out              |           -5 mV |   0.086 mV |         0 mV |   0.240 mV |         5 mV |   0.931 mV |   Pass ✅    |
| Supply current vs bias quality | ngspice              | Idd                  |             any | 259.870 uA |          any | 437.330 uA |       600 uA | 649.916 uA |   Fail ❌    |
| Output PMOS quiescent current vs bias quality | ngspice              | IqP                  |          100 uA | 147.995 uA |          any | 238.871 uA |       500 uA | 339.312 uA |   Pass ✅    |
| Minimum output device current vs bias quality | ngspice              | Imin                 |           20 uA |  22.176 uA |          any |  65.771 uA |          any | 190.683 uA |   Pass ✅    |
| Gain vs load         | ngspice              | Gain                 |             any |   0.498971 |          0.5 |   0.500734 |          any |   0.500754 |   Pass ✅    |
| Integral nonlinearity vs load | ngspice              | INL                  |             any |   5.494 mV |          any |   5.499 mV |        10 mV |   6.141 mV |   Pass ✅    |
| Minimum output device current vs load | ngspice              | Imin                 |             any |  29.551 uA |          any | 141.358 uA |          any | 234.433 uA |   Pass ✅    |
| DC loop gain         | ngspice              | T0                   |           40 dB |  44.104 dB |          any |  66.459 dB |          any |  69.004 dB |   Pass ✅    |
| Loop crossover frequency | ngspice              | fc                   |           1 MHz |  1.523 MHz |          any |  1.619 MHz |          any |  1.694 MHz |   Pass ✅    |
| Phase margin         | ngspice              | PM                   |            45 ° |   71.417 ° |         60 ° |   74.797 ° |          any |   77.195 ° |   Pass ✅    |
| Gain margin          | ngspice              | GM                   |           10 dB |  29.321 dB |          any |  31.113 dB |          any |  32.648 dB |   Pass ✅    |
| Loop crossover frequency vs load | ngspice              | fc                   |             any |  0.959 MHz |          any |  1.607 MHz |          any |  2.175 MHz |   Pass ✅    |
| Phase margin vs load | ngspice              | PM                   |            45 ° |   26.488 ° |          any |   61.457 ° |          any |   86.778 ° |   Fail ❌    |
| Phase margin vs bias error and MOM corner | ngspice              | PM                   |            45 ° |   73.929 ° |          any |   74.797 ° |          any |   75.633 ° |   Pass ✅    |
| Crossover vs bias error and MOM corner | ngspice              | fc                   |           1 MHz |  1.387 MHz |          any |  1.619 MHz |          any |  1.761 MHz |   Pass ✅    |
| Closed-loop gain at 1 kHz | ngspice              | Acl_dB               |             any |  -6.039 dB |     -6.02 dB |  -6.013 dB |          any |  -5.984 dB |   Pass ✅    |
| Closed-loop -3 dB bandwidth | ngspice              | f3dB                 |           1 MHz |  2.219 MHz |          any |  2.228 MHz |          any |  2.236 MHz |   Pass ✅    |
| PSRR at 1 kHz (output-referred) | ngspice              | PSRR_1k              |           40 dB |  72.530 dB |          any |  72.542 dB |          any |  72.549 dB |   Pass ✅    |
| PSRR at 100 kHz (output-referred) | ngspice              | PSRR_100k            |             any |  32.540 dB |          any |  32.549 dB |          any |  32.556 dB |   Pass ✅    |
| CMRR at 1 kHz        | ngspice              | CMRR_1k              |           50 dB |  97.577 dB |          any | 100.022 dB |          any | 101.284 dB |   Pass ✅    |
| Closed-loop output impedance at 1 kHz | ngspice              | Zout_1k              |             any |    0.434 Ω |          any |    0.482 Ω |          1 Ω |    0.573 Ω |   Pass ✅    |
| Closed-loop output impedance at 1 MHz | ngspice              | Zout_1M              |             any |  128.158 Ω |          any |  130.621 Ω |          any |  133.315 Ω |   Pass ✅    |
| Rising slew rate (10-90 %) | ngspice              | SR_rise              |          1 V/us | 2.023 V/us |          any | 2.654 V/us |          any | 3.016 V/us |   Pass ✅    |
| Falling slew rate (90-10 %) | ngspice              | SR_fall              |          1 V/us | 2.607 V/us |          any | 6.649 V/us |          any | 11.286 V/us |   Pass ✅    |
| Overshoot            | ngspice              | Overshoot            |             any |    0.000 % |          any |    0.001 % |         10 % |    0.036 % |   Pass ✅    |
| Settling time to 1 %, rising | ngspice              | ts_rise              |             any | 306.102 ns |          any | 954.806 ns |      1000 ns | 2533.180 ns |   Fail ❌    |
| Settling time to 1 %, falling | ngspice              | ts_fall              |             any | 314.781 ns |          any | 395.884 ns |      1000 ns | 526.725 ns |   Pass ✅    |
| Total harmonic distortion (h2..h7) | ngspice              | THD                  |             any | -51.076 dB |          any | -33.171 dB |       -40 dB | -14.800 dB |   Fail ❌    |
| Output fundamental amplitude | ngspice              | Vout_amp             |             any |    0.502 V |          any |    0.859 V |          any |    1.280 V |   Pass ✅    |
| Output noise density at 1 kHz | ngspice              | En_1k                |             any | 1568.670 nV/rtHz |          any | 1599.370 nV/rtHz |          any | 1629.440 nV/rtHz |   Pass ✅    |
| Output noise density at 100 kHz | ngspice              | En_100k              |             any | 198.626 nV/rtHz |          any | 200.491 nV/rtHz |          any | 202.364 nV/rtHz |   Pass ✅    |
| Integrated output noise, 10 Hz - 10 MHz | ngspice              | Vn_int               |             any | 276.982 uV |          any | 277.944 uV |          any | 278.885 uV |   Pass ✅    |
| Maximum output voltage into load | ngspice              | Vout_max             |           2.8 V |    2.858 V |          any |    3.278 V |          any |    3.300 V |   Pass ✅    |
| Minimum output voltage into load | ngspice              | Vout_min             |             any |    0.354 V |          any |    0.369 V |        0.5 V |    0.385 V |   Pass ✅    |
| Short-circuit current, sourcing | ngspice              | Isc_src              |            5 mA |  59.762 mA |          any |  70.255 mA |          any |  80.422 mA |   Pass ✅    |
| Short-circuit current, sinking | ngspice              | Isc_snk              |            5 mA |  74.216 mA |          any |  82.531 mA |          any |  92.160 mA |   Pass ✅    |
| Output offset - Mismatch | ngspice              | Vos_out              |          -10 mV | -32.363 mV |          any |  -0.242 mV |        10 mV |  48.688 mV |   Fail ❌    |
| Gain - Mismatch      | ngspice              | Gain                 |           0.485 |   0.481141 |          any |  0.5006505 |        0.515 |   0.525164 |   Fail ❌    |
| Output PMOS quiescent current - Mismatch | ngspice              | IqP                  |          100 uA | 211.308 uA |          any | 241.995 uA |       500 uA | 278.822 uA |   Pass ✅    |
| Output offset - Process MC | ngspice              | Vos_out              |          -10 mV |   0.149 mV |          any |   0.189 mV |        10 mV |   0.239 mV |   Pass ✅    |
| Gain - Process MC    | ngspice              | Gain                 |           0.485 |   0.414977 |          any | 0.5105105000000001 |        0.515 |   0.605241 |   Fail ❌    |
| Output PMOS quiescent current - Process MC | ngspice              | IqP                  |          100 uA | 237.963 uA |          any | 239.618 uA |       500 uA | 241.827 uA |   Pass ✅    |

