
# CACE Summary for s2d_mpdda_pd_sel

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| DC loop gain, differential | ngspice              | T0dm                 |           60 dB |  64.544 dB |          any |  65.670 dB |          any |  67.511 dB |   Pass ✅    |
| Crossover, differential | ngspice              | fcdm                 |             any |  0.146 MHz |          any |  1.050 MHz |          any |  3.262 MHz |   Pass ✅    |
| Phase margin, differential | ngspice              | PMdm                 |            60 ° |   86.082 ° |          any |   88.893 ° |          any |   89.888 ° |   Pass ✅    |
| Gain margin, differential | ngspice              | GMdm                 |           10 dB |  29.411 dB |          any |  40.119 dB |          any |  57.612 dB |   Pass ✅    |
| DC loop gain, common mode | ngspice              | T0cm                 |           50 dB |  64.732 dB |          any |  65.895 dB |          any |  67.825 dB |   Pass ✅    |
| Crossover, common mode | ngspice              | fccm                 |             any |  0.147 MHz |          any |  1.049 MHz |          any |  3.131 MHz |   Pass ✅    |
| Phase margin, common mode | ngspice              | PMcm                 |            55 ° |   62.060 ° |          any |   82.013 ° |          any |   89.043 ° |   Pass ✅    |
| Gain margin, common mode | ngspice              | GMcm                 |           10 dB |  14.454 dB |          any |  25.699 dB |          any |  43.692 dB |   Pass ✅    |

