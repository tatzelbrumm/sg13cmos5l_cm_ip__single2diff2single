
# CACE Summary for sg13cmos5l_IOPadSingle2Diff

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| Gain                 | ngspice              | Gain                 |            1.99 |          ​ |            2 |          ​ |         2.01 |          ​ |   Skip 🟧    |
| Input offset (systematic) | ngspice              | Vos_in               |           -1 mV |          ​ |         0 mV |          ​ |         1 mV |          ​ |   Skip 🟧    |
| Integral nonlinearity | ngspice              | INL                  |             any |          ​ |          any |          ​ |         2 mV |          ​ |   Skip 🟧    |
| Output common-mode error | ngspice              | Vcm_err              |          -30 mV |          ​ |          any |          ​ |        30 mV |          ​ |   Skip 🟧    |
| IO ring current      | ngspice              | Iio                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gain vs vref and vcm | ngspice              | Gain                 |             any |          ​ |            2 |          ​ |          any |          ​ |   Skip 🟧    |
| Integral nonlinearity vs vref and vcm | ngspice              | INL                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output common-mode error vs vref and vcm | ngspice              | Vcm_err              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Input range, low end | ngspice              | Vin_min              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Input range, high end | ngspice              | Vin_max              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gain vs bias select  | ngspice              | Gain                 |            1.99 |          ​ |            2 |          ​ |         2.01 |          ​ |   Skip 🟧    |
| Input offset (systematic) vs bias select | ngspice              | Vos_in               |           -1 mV |          ​ |         0 mV |          ​ |         1 mV |          ​ |   Skip 🟧    |
| Integral nonlinearity vs bias select | ngspice              | INL                  |             any |          ​ |          any |          ​ |         2 mV |          ​ |   Skip 🟧    |
| Output common-mode error vs bias select | ngspice              | Vcm_err              |          -30 mV |          ​ |          any |          ​ |        30 mV |          ​ |   Skip 🟧    |
| IO ring current vs bias select | ngspice              | Iio                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Gain, sel 11         | ngspice              | Gain                 |             any |    1.99819 |            2 |     1.9984 |          any |    1.99855 |   Pass ✅    |
| Input offset (systematic), sel 11 | ngspice              | Vos_in               |             any |  -0.000 mV |          any |  -0.000 mV |          any |   0.000 mV |   Pass ✅    |
| Integral nonlinearity, sel 11 | ngspice              | INL                  |             any |   0.404 mV |          any |   0.910 mV |          any |   6.768 mV |   Pass ✅    |
| Output common-mode error, sel 11 | ngspice              | Vcm_err              |             any |   6.616 mV |          any |  12.353 mV |          any |  16.342 mV |   Pass ✅    |
| IO ring current, sel 11 | ngspice              | Iio                  |             any | 214.176 uA |          any | 267.801 uA |          any | 320.026 uA |   Pass ✅    |
| Gain vs ibias        | ngspice              | Gain                 |            1.99 |          ​ |            2 |          ​ |         2.01 |          ​ |   Skip 🟧    |
| Input offset (systematic) vs ibias | ngspice              | Vos_in               |           -1 mV |          ​ |         0 mV |          ​ |         1 mV |          ​ |   Skip 🟧    |
| Integral nonlinearity vs ibias | ngspice              | INL                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output common-mode error vs ibias | ngspice              | Vcm_err              |          -30 mV |          ​ |          any |          ​ |        30 mV |          ​ |   Skip 🟧    |
| IO ring current vs ibias | ngspice              | Iio                  |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Closed-loop gain at 1 kHz | ngspice              | Acl_dB               |             any |          ​ |      6.02 dB |          ​ |          any |          ​ |   Skip 🟧    |
| Closed-loop -3 dB bandwidth | ngspice              | f3dB                 |           1 MHz |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output common-mode response to iovdd at 1 kHz | ngspice              | CMvdd_1k             |             any |          ​ |          any |          ​ |       -30 dB |          ​ |   Skip 🟧    |
| PSRR iovdd at 1 kHz (input-referred), mismatch | ngspice              | PSRRp_1k             |           60 dB |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| PSRR iovdd at 100 kHz (input-referred), mismatch | ngspice              | PSRRp_100k           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| PSRR iovss at 1 kHz (input-referred), mismatch | ngspice              | PSRRn_1k             |           60 dB |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| PSRR iovss at 100 kHz (input-referred), mismatch | ngspice              | PSRRn_100k           |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| CMRR at 1 kHz (pad and vref together), mismatch | ngspice              | CMRR_1k              |           70 dB |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Rise time 10-90 %    | ngspice              | t_rise               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Settling time to 1 % | ngspice              | t_settle             |             any |          ​ |          any |          ​ |      1000 ns |          ​ |   Skip 🟧    |
| Overshoot            | ngspice              | Overshoot            |             any |          ​ |          any |          ​ |          5 % |          ​ |   Skip 🟧    |
| Largest output common-mode deviation during the step | ngspice              | Vcm_dev              |             any |          ​ |          any |          ​ |        50 mV |          ​ |   Skip 🟧    |
| Input noise density at 1 kHz | ngspice              | En_1k                |             any |          ​ |          any |          ​ | 1000 nV/rtHz |          ​ |   Skip 🟧    |
| Input noise density at 100 kHz | ngspice              | En_100k              |             any |          ​ |          any |          ​ |  250 nV/rtHz |          ​ |   Skip 🟧    |
| Differential output noise, 10 Hz - 10 MHz | ngspice              | Vn_out               |             any |          ​ |          any |          ​ |      1000 uV |          ​ |   Skip 🟧    |
| IO ring current, off | ngspice              | Iio_pd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Core ring current, off | ngspice              | Icore_pd             |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Pad input leakage, off | ngspice              | Ipad_pd              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Internal enable      | ngspice              | Ven3                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Differential output, off | ngspice              | Vod_pd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output common mode, off | ngspice              | Voc_pd               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Enable time          | ngspice              | t_on                 |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output CM glitch, high | ngspice              | Vc_max               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Output CM glitch, low | ngspice              | Vc_min               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Differential output at the end | ngspice              | Vd_end               |             any |          ​ |        0.5 V |          ​ |          any |          ​ |   Skip 🟧    |
| IO ring current, enabled | ngspice              | Iio_on               |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Input offset - Mismatch | ngspice              | Vos_in               |          -20 mV |          ​ |          any |          ​ |        20 mV |          ​ |   Skip 🟧    |
| Gain - Mismatch      | ngspice              | Gain                 |            1.93 |          ​ |          any |          ​ |         2.07 |          ​ |   Skip 🟧    |
| Output common-mode error - Mismatch | ngspice              | Vcm_err              |          -60 mV |          ​ |          any |          ​ |        60 mV |          ​ |   Skip 🟧    |
| Input offset - Process MC | ngspice              | Vos_in               |           -5 mV |          ​ |          any |          ​ |         5 mV |          ​ |   Skip 🟧    |
| Gain - Process MC    | ngspice              | Gain                 |            1.99 |          ​ |          any |          ​ |         2.01 |          ​ |   Skip 🟧    |
| Output common-mode error - Process MC | ngspice              | Vcm_err              |          -30 mV |          ​ |          any |          ​ |        30 mV |          ​ |   Skip 🟧    |

